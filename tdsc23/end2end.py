import secrets
import socket
import pickle
import hashlib
import hmac
from array import array
from obliv.voram import create_voram, Ref
import json
import os
from time import time
from tqdm import tqdm
import threading

class OMapUsr:
    """
    一个用户的Omap结构，代码完全参照GitHub上面的demo
    https://github.com/dsroche/obliv
    """
    def __init__(self, oram: Ref) -> None:
        self.generator = oram
        self.map = {}
        self.cnt = 0
    def get(self, word):
        return self.map[word].get()
    def put(self, word, value):
        if word not in self.map.keys():
            self.map[word] = self.generator.create()
            self.cnt += 1
        self.map[word].set(value)

OMap = {}
AccessList = {}
DictW = {}

def get_random_key(length: int):
    return secrets.token_bytes(length)

LAMBDA = 256//8
PATH_LEN = 128//8
port = 32345

def enroll(ukey, size):
    # 登记一个用户，为他分配一个Omap项
    v = create_voram(blobs_limit=size, blob_size=4*8)
    OMap[ukey] = OMapUsr(v)

def share(KeyValues, uid, fid):
    # 更新accesslist
    if fid not in AccessList.keys():
        AccessList[fid] = []
    AccessList[fid].append(uid)
    for item in KeyValues:
        DictW[item[0]] = item[1]

def update(KeyValues):
    # 更新索引
    for item in KeyValues:
        DictW[item[0]] = item[1]

def search(tlist):
    ret = []
    for t in tlist:
        ret.append(DictW[t])
    return ret

def get_omap(word, ukey):
    ret = OMap[ukey].get(word)
    return ret

def put_omap(wordset, uidset, ukeyset):
    ret = {}
    for i, uk in enumerate(ukeyset):
        uid = uidset[i]
        ret[uid] = {}
        for word in wordset:
            if word not in OMap[uk].map.keys():
                OMap[uk].put(word, 0)
            val = OMap[uk].get(word)
            val += 1
            OMap[uk].put(word, val)
            ret[uid][word] = val
    # print(pickle.dumps(ret))
    return ret

def get_hmac(word, cnt, op, key):
    """
    获取hmac = H(word || cnt || op)
    """
    msg = word + bytes(cnt) + bytes(op)
    obj = hmac.new(key, msg, hashlib.sha256)
    return obj.digest()

def get_val(fid, op, hash):
    """
    获取(fid || op) ^ hash，对应Update和Share的14行
    """
    data = (fid + op).ljust(LAMBDA)
    result = [b1 ^ b2 for b1, b2 in zip(data, hash)]
    return result

class owner:
    """
    DO结构
    """
    def __init__(self) -> None:
        self.DictW = dict()
        self.UserKeys = dict()
        self.AccessList = dict()
        self.doc = dict()

    def enroll(self, uid: bytes):
        """
        DO登记一个DU，返回一个DU的Omapkey
        与服务器通讯，在服务器上新建一个OMap项
        """
        ukey = get_random_key(LAMBDA)
        self.UserKeys[uid] = ukey
        return ukey

    def share(self, uid, fid, wlist):
        """
        对uid分享fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        self.AccessList[fid].append(uid)
        key = self.UserKeys[uid]
        # word_set = self.doc[fid]
        KeyValues = []

        # 更新Omap[uid][word]
        cnt = put_omap(wlist, [uid], [key])
        # 更新文件索引
        for word in wlist:
            # 复用了DU用于检索Omap的key，作为对称加密密钥
            addr = get_hmac(word, cnt[uid][word], 0, key)
            val = get_val(fid, b'add', get_hmac(word, cnt[uid][word], 1, key))
            KeyValues.append((addr, val))
        # communicate([KeyValues, uid, fid], b"share")
        share(KeyValues, uid, fid)

    def update(self, fid, op, wlist):
        """
        更新fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        KeyValues = []
        self.doc[fid] = wlist
        # 更新Omap
        cnts = put_omap(wlist, self.AccessList[fid], [self.UserKeys[i] for i in self.AccessList[fid]])
        for uid in self.AccessList[fid]:
            key = self.UserKeys[uid]
            for word in wlist:
                # 复用了DU用于检索Omap的key，作为对称加密密钥
                addr = get_hmac(word, cnts[uid][word], 0, key)
                val = get_val(fid, op, get_hmac(word, cnts[uid][word], 1, key))
                KeyValues.append((addr, val))
        # communicate(KeyValues, b"update")
        update(KeyValues)

class user:
    def __init__(self, uid:bytes) -> None:
        self.uid = uid

    def register(self, key):
        self.ukey = key

    def search(self, word):
        tlist = []
        cnt = get_omap(word, self.ukey)
        for i in range(1, cnt+1):
            t = get_hmac(word, i, 0, self.ukey)
            tlist.append(t)
        # result = communicate(tlist, b"search")
        result = search(tlist)
        return result

def load_data_as_bytes(file_name):
    """
    从 JSON 文件加载数据，将键和值列表里的内容转换为字节串。

    参数：
    file_name (str): JSON 文件名。

    返回：
    dict: 转换为字节串的字典数据。
    """
    with open(file_name, "r") as file:
        data = json.load(file)

    data_as_bytes = {}
    for key, value_list in tqdm(data.items()):
        key_as_bytes = key.encode().ljust(PATH_LEN)
        value_list_as_bytes = [word.encode() for word in value_list]
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes
connection_event = threading.Event()
using_time = []
import struct

def send_data(socket:socket.socket, data):
    # 将数据长度打包为4字节无符号整数，并发送给接收端
    length = len(data)
    socket.sendall(struct.pack('!I', length))
    
    # 按照分片大小发送数据
    chunk_size = 10240  # 分片大小为1024字节
    offset = 0
    while offset < length:
        chunk = data[offset:offset+chunk_size]
        socket.sendall(chunk)
        offset += len(chunk)

def receive_data(socket:socket.socket):
    # 接收数据长度信息
    length_bytes = socket.recv(4)
    length = struct.unpack('!I', length_bytes)[0]
    
    # 按照分片大小接收数据
    data = b''
    remaining = length
    chunk_size = 10240  # 分片大小为1024字节
    while remaining > 0:
        chunk = socket.recv(min(chunk_size, remaining))
        data += chunk
        remaining -= len(chunk)
    
    return data

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    connection_event.set()
    try:
        client_socket, addr = server_socket.accept()      
        while True:
            # request = client_socket.recv(102400)
            request = receive_data(client_socket)
            op, data = pickle.loads(request)
            # print(op)
            if op == 'getomap':
                word, ukey = data
                # print(data)
                ret = get_omap(word, ukey)
                # client_socket.send(pickle.dumps(ret))
                send_data(client_socket, pickle.dumps(ret))
            elif op == 'search':
                tlist = data
                ret = search(tlist)
                # ret = array('u', ret)
                msg = pickle.dumps(ret)
                print("return msg using bytes: ", len(msg))
                # client_socket.send(msg)
                send_data(client_socket, msg)
            elif op == 'shutdown':
                break
            else:
                print("no such option")
        server_socket.close()
    except Exception as e:
        server_socket.close()
        print("server fault: ", e)

def client(du:user):
    connection_event.wait()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    word = b'unique_word_with_size5'
    # for _ in range(10):
    t1 = time()
    request = ('getomap', (word, du.ukey))
    try:
        # client_socket.send(pickle.dumps(request))
        # response = client_socket.recv(1024)
        send_data(client_socket, pickle.dumps(request))
        response = receive_data(client_socket)
        cnt = pickle.loads(response)
        tlist = []
        for i in range(1, cnt+1):
            t = get_hmac(word, i, 0, du.ukey)
            tlist.append(t)
        request = ('search', tlist)
        print("tokens using bytes: ", len(pickle.dumps(request)))
        # client_socket.send(pickle.dumps(request))
        # response = client_socket.recv(202400)
        send_data(client_socket, pickle.dumps(request))
        response = receive_data(client_socket)
        result = pickle.loads(response)
        t2 = time()
        print(len(result))
        print("search files using {}s".format(t2-t1))
        using_time.append(t2-t1)
        request = ('shutdown', None)
        # client_socket.send(pickle.dumps(request))
        send_data(client_socket, pickle.dumps(request))
    except Exception as e:
        request = ('shutdown', None)
        # client_socket.send(pickle.dumps(request))
        send_data(client_socket, pickle.dumps(request))
        print("client fault: ", e)
    finally:
        client_socket.close()



data_path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
# data_path = os.getcwd() + "/enron_washed.json"
documents = load_data_as_bytes(data_path)
# 取出全部的文件标识符，构成列表docs
docs = [d for d in documents.keys()]
num = [1000, 5000, len(docs)]
num = [1000]
auth_num = [5, 50, 200, 1000]
# for n in num:
#     do = owner()
#     dus = []
#     doc = docs[:n]
#     uid = get_random_key(LAMBDA)
#     du = user(uid)
#     ukey = do.enroll(uid)
#     enroll(ukey, n*10)
#     du.register(ukey)
#     for d in tqdm(doc):
#         do.share(du.uid, d, documents[d])
    # using_time = []
    # for i in auth_num:
    #     t1 = time()
    #     for d in tqdm(doc[:i]):
    #         do.share(du.uid, d, documents[d])
    #     t2 = time()
    #     using_time.append(t2-t1)
    # print("update using time %fs"%(t2-t1))
    # print(using_time)

# for i in range(5):
#     documents[str(i).encode().ljust(PATH_LEN)].append(b'unique_word_with_size5')
for i, words in enumerate(documents.values()):
    if i == 1000:
        break
    words.append(b'unique_word_with_size5')

    # n = len(docs)
n = 1000
do = owner()
dus = []
doc = docs[:n]
uid = get_random_key(LAMBDA)
du = user(uid)
ukey = do.enroll(uid)
enroll(ukey, n*10)
du.register(ukey)
for d in tqdm(doc, mininterval=1):
    do.share(du.uid, d, documents[d])
for _ in range(3):
    # 创建并启动服务器线程
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # 创建并启动客户端线程
    client_thread = threading.Thread(target=client, args=(du,))
    client_thread.start()

    client_thread.join()
    server_thread.join()
    # OMap.clear()
    # AccessList.clear()
    # DictW.clear()
import numpy as np
avg = np.array(using_time)
print(np.mean(avg))