from obliv.voram import create_voram, Ref
import socket
import pickle
from typing import Dict

class OMapUsr:
    """
    一个用户的Omap结构，代码完全参照GitHub上面的demo
    https://github.com/dsroche/obliv
    """
    def __init__(self, oram: Ref) -> None:
        self.generator = oram
        self.map = {}
    def get(self, word):
        return self.map[word].get()
    def put(self, word, value):
        if word not in self.map.keys():
            self.map[word] = self.generator.create()
        self.map[word].set(value)

# OMap: Dict[str, OMapUsr]
# AccessList: Dict[str, list]
OMap = {}
AccessList = {}
DictW = {}

# OMap = dict() : OMap_dict()

def enroll(data):
    # 登记一个用户，为他分配一个Omap项
    ukey = pickle.loads(data)
    v = create_voram(blobs_limit=10, blob_size=5, nodesize=256)
    OMap[ukey] = OMapUsr(v)
    return pickle.dumps(True)

def share(data):
    # 恢复客户端数据
    data = pickle.loads(data)
    KeyValues, uid, fid = data[0], data[1], data[2]
    # 更新accesslist
    if fid not in AccessList.keys():
        AccessList[fid] = []
    AccessList[fid].append(uid)
    for item in KeyValues:
        DictW[item[0]] = item[1]


def update(data):
    KeyValues = pickle.loads(data)
    # 更新索引
    for item in KeyValues:
        DictW[item[0]] = item[1]
    return pickle.dumps(True)

def search(data):
    tlist = pickle.loads(data)
    ret = []
    for t in tlist:
        ret.append(DictW[t])

def get_omap(data):
    l = pickle.loads(data)
    word, ukey = l[0], l[1]
    ret = OMap[ukey].get(word)
    return pickle.dumps(ret)

def put_omap(data):
    l = pickle.loads(data)
    wordset, uidset, ukeyset = l[0], l[1], l[2]
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
    return pickle.dumps(ret)

def reset():
    OMap.clear()
    AccessList.clear()
    DictW.clear()
    return pickle.dumps(True)

def main():
    enroll(pickle.dumps('word'))
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostname() 
    port = 8080
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    # 设置最大连接数，超过后排队
    serversocket.listen(5)
    while True:
        # 建立客户端连接
        clientsocket, addr = serversocket.accept()      
        # print("连接地址: %s" % str(addr))
        data = b""
        while True:
            recv = clientsocket.recv(1024)
            data += recv
            if len(recv) < 1024:
                break
        # data = clientsocket.recv(1024)
            # 前8个字节
        # print("finish recv")
        cmd = data[:8]
        payload = data[8:]

        if cmd == b'enroll'.ljust(8):
            ret = enroll(data = payload)
        elif cmd == b'share'.ljust(8):
            share(data = payload)
        elif cmd == b'update'.ljust(8):
            ret = update(data = payload)
        elif cmd == b'search'.ljust(8):
            search(data = payload)
        elif cmd == b'putmap'.ljust(8):
            ret = put_omap(data = payload)
        elif cmd == b'getmap'.ljust(8):
            ret = get_omap(data = payload)
        elif cmd == b'reset'.ljust(8):
            ret = reset()
        else:
            ret = b'no such cmd'
            ret = pickle.dumps(ret)
        clientsocket.send(ret)
        # 关闭连接
        clientsocket.close()

main()