import sys
import os
sys.path.append(os.getcwd() + "/project")
from shell.client.c_user import c_user
from shell.server.c_server import c_server
from shell.utils.datatype import *
from shell.utils.method import *
import json
import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import tqdm
import pickle
import socket
import threading

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
    for key, value_list in data.items():
        key_as_bytes = key.encode()
        value_list_as_bytes = [word.encode() for word in value_list]
        if len(value_list_as_bytes) == 0:
            value_list_as_bytes.append(b"comman_word")
        else:
            value_list_as_bytes[-1] = b"comman_word"
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes



path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
# path = os.getcwd() + "/enron_washed.json"
libserver = os.getcwd() + "/project/core/libserver.so"
libclient = os.getcwd() + "/project/core/libclient.so"
usr1 = b"helloworld".ljust(LAMBDA)
word = b"comman_word"
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk1 = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
usr = get_random_key(LAMBDA)
document = load_data_as_bytes(path)
# for i in range(100):
#     document[str(i).encode()].append(b'unique_word_with_size5')
for i, word in enumerate(document.values()):
    if i == 100:
        break
    word.append(b'unique_word_with_size5')

files = []
for k, v in document.items():
    files.append(get_fd(v, bytes(k).ljust(PATH_LEN)))
docs = [d.ljust(PATH_LEN) for d in document.keys()]

cusr = c_user(libclient)
csvr = c_server(libserver)
print("load client core success")
using_time_usr = []
using_time_svr= []
xwds = []
Xset = {}
Uset = {}
Aset = {}

port = 34567

n = len(docs)
n = 1000
auth_num = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
# auth_num = [900, 1000]
file = files[:n]
doc = docs[:n]
auth_doc = doc[:1000]
t1 = time.time()
xset, index_num = cusr.updateData_generate(sk, file)
Xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
t2 = time.time()
print("update using time {}s".format(t2-t1))

# auth_doc = doc[:i]
dockey, uset = cusr.online_auth(sk, uk, auth_doc)
dockey = [dk for dk in dockey]
uset = {bytes(u.uid):bytes(u.ud) for u in uset}
Uset.update(uset)
tmpset, usrauth, dockey1 = cusr.offline_auth(uk, uk1, 
        auth_doc, usr, dockey, [])
usrauth = [ua for ua in usrauth]
csvr.Aset_update(Aset, bytes(tmpset.contents.aid), bytes(tmpset.contents.trapgate), None)

connection_event = threading.Event()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    connection_event.set()
    try:
        client_socket, addr = server_socket.accept()
        while True:
            request = client_socket.recv(102400)
            # t1 = time.time()
            op, tokens, aid = pickle.loads(request)
            if op == 'search':
                result = csvr.search(tokens, aid, Uset, Aset, Xset)
                client_socket.send(pickle.dumps(result))
            elif op == 'shutdown':
                break
            # t2 = time.time()
            # print("search on server using time {}s".format(t2-t1))
        server_socket.close()
    except Exception as e:
        server_socket.close()
        print(e)

def client():
    connection_event.wait()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    word = get_word_from_bytes(b'unique_word_with_size5')
    try:
        t1 = time.time()
        query = cusr.search_generate(word, uk1, dockey1, usrauth)
        query = [(bytes(q.uid), bytes(q.stk)) for q in query]
        request = ('search', query, bytes(tmpset.contents.aid))
        print("total message length", len(pickle.dumps(request)))
        client_socket.send(pickle.dumps(request))
        response = client_socket.recv(102400)
        response = pickle.loads(response)
        t2 = time.time()
        # print(response)
        print("search files using {}s".format(t2-t1))
        request = ('shutdown', None, None)
        client_socket.send(pickle.dumps(request))
    except Exception as e:
        request = ('shutdown', None, None)
        client_socket.send(pickle.dumps(request))
        print(e)

# 创建并启动服务器线程
server_thread = threading.Thread(target=server)
server_thread.start()

# 创建并启动客户端线程
client_thread = threading.Thread(target=client)
client_thread.start()

client_thread.join()
server_thread.join()
Uset.clear()
Aset.clear()
