import socket
import pickle
import ctypes
import struct

import os
import sys
sys.path.append(os.getcwd() + "/project/")

from shell.server.c_server import c_server
from shell.utils.datatype import *

Xset = {}
Uset = {}
Aset = {}
libserver = os.getcwd() + "/project/core/libserver.so"
server = c_server(libserver)

def update(data):
    update_xset = pickle.loads(data)
    Xset.update(update_xset)
    return pickle.dumps("update {} peers".format(len(update_xset)))

def online(data):
    update_uset = pickle.loads(data)
    Uset.update(update_uset)
    return pickle.dumps("update {} Uid-Ud peers".format(len(update_uset)))

def offline(data):
    (aid, alpha, aidA) = pickle.loads(data)
    server.Aset_update(Aset, aid, alpha, aidA)
    return pickle.dumps("update a new offline auth user")

def search(data):
    (token, aid) = pickle.loads(data)
    result = server.search(token, aid, Uset, Aset, Xset)
    return pickle.dumps(result)

def reset(data):
    Xset.clear()
    Uset.clear()
    Aset.clear()
    return pickle.dumps(b"reset success")

def measure_size():
    total = 0
    for k, v in Xset.items():
        total += (len(k) + len(v))
    for k, v in Uset.items():
        total += (len(k) + len(v))
    for k, v in Aset.items():
        total += (len(k) + len(v))

    return pickle.dumps(total)

def recvall(sock, size):
    data = b''
    while len(data) < size:
        more = sock.recv(size - len(data))
        if not more:
            raise EOFError('socket closed with %d bytes left in this block'.format(size - len(data)))
        data += more
    return data

def main():
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
        datasize = clientsocket.recv(4)
        datasize = struct.unpack(">I", datasize)[0]
        print(datasize)
        data = recvall(clientsocket, datasize)
        print("finish second recv")
        print(len(data))

        cmd = data[:8]
        payload = data[8:]
        print(cmd)
        

        if cmd == b'update'.ljust(8):
            ret = update(payload)
        elif cmd == b'online'.ljust(8):
            ret = online(payload)
        elif cmd == b'offline'.ljust(8):
            ret = offline(payload)
        elif cmd == b'reset'.ljust(8):
            ret = reset(payload)
        elif cmd == b'search'.ljust(8):
            ret = search(payload)
        elif cmd == b'getsize'.ljust(8):
            ret = measure_size()

        ret_size = struct.pack(">I", len(ret))
        clientsocket.send(ret_size)
        clientsocket.send(ret)
        # 关闭连接
        clientsocket.close()

main()