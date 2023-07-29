import sys
import os
sys.path.append(os.getcwd() + "/tdsc22")
from shell.c_server import *
from shell.c_user import *
from shell.datatype import *
from shell.method import *
import json
from time import time
from itertools import islice
import socket
import pickle
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
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes

libclient = os.getcwd() + "/tdsc22/core/libclient.so"
libserver = os.getcwd() + "/tdsc22/core/libserver.so"
data_path = os.getcwd() + "/tdsc22/lab/data/enron1w_washed.json"
# data_path = os.getcwd() + "/project/demo/demo.json"
file_raw = load_data_as_bytes(data_path) 
cuser = c_user(libclient)
csver = c_server(libserver)

mk = MK(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)


# n = len(file_raw)
authword = b'unique_word_for_auth'
uniqueword = b'unique_word_for_search'
n = 1000
authnum = 1000
searchnum = 1000
file_use_raw = dict(islice(file_raw.items(), n))
for i, words in enumerate(file_use_raw.values()):
    if i == searchnum:
        break
    words.append(uniqueword)
for i, words in enumerate(file_use_raw.values()):
    if i == authnum:
        break
    words.append(authword)
file_use = {}
for f, words in file_use_raw.items():
    for w in words:
        if w not in file_use.keys():
            file_use[w] = []
        file_use[w].append(f)
# file_use[authword] = [str(i).encode() for i in range(5)]
files = []
for w in file_use:
    word = get_key_from_bytes(w)
    ids = []
    for fid in file_use[w]:
        one_id = type_id()
        memmove(one_id, fid, len(fid))
        ids.append(pointer(one_id))
    p_type = POINTER(type_id) * len(file_use[w])
    p_fids = p_type(*ids)
    files.append(WORD_FILE(p_fids, word, len(file_use[w])))

edb, xset = cuser.update(mk, files)
db = {bytes(item.l):(bytes(item.e), bytes(item.y)) for item in edb}
xset = [bytes(xtag) for xtag in xset]
port = 22345
# sk_ptr = cuser.auth([get_word_from_bytes(authword), get_word_from_bytes(b'reports')])
w = set()
word_use = []
for v in list(file_use_raw.values())[:authnum]:
    for word in v:
        w.add(word)
for word in w:
    word_use.append(get_word_from_bytes(word))
w_copy = w.copy()
sk_ptr = cuser.auth(word_use)
print("finish auth")
# sk_ptr = cuser.auth([get_word_from_bytes(authword)])
sk = sk_ptr.contents

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
            request = client_socket.recv(1024)
            op, stag, tokens, cnt = pickle.loads(request)
            if op == 'search':
                stag = get_key_from_bytes(stag)
                ret = csver.search(tokens, stag, cnt, db, xset)
                client_socket.send(pickle.dumps(ret))
            elif op == 'shutdown':
                break
            else:
                print('no such option')
                break
        server_socket.close()
    except Exception as e:
        server_socket.close()
        print("server fault: ", e)

def client():
    connection_event.wait()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    # word = [get_word_from_bytes(b'reports'), get_word_from_bytes(b'unique_word_with_size5')]
    word_search = [uniqueword, authword]
    try:
        t1 = time()
        stag = cuser.get_stag(mk, word_search, w, sk_ptr)
        print("finish calculate stag")
        stag = bytes(stag.contents)
        if len(word_search) > 1:
            index1, index2 = cuser.get_index(sk, word_search, w, mk)
        print("finish calculat index")
        cnt = 0
        result = []
        while True:
            # tokens = cuser.token_generate(sk, word, mk, cnt)
            if len(word_search) > 1:
                tokens = cuser.token_generate(mk, cnt, index1, index2, len(word_search))
                tokens = [bytes(token.contents) for token in tokens]
            else:
                tokens = []
            request = ('search', stag, tokens, cnt)
            client_socket.send(pickle.dumps(request))
            response = client_socket.recv(1024)
            response = pickle.loads(response)
            if response == b"stop":
                break
            else:
                result.append(bytes(response))
                cnt += 1
        t2 = time()
        print(len(result))
        print("search files using {}s".format(t2-t1))
        request = ('shutdown', None, None, None)
        client_socket.send(pickle.dumps(request))
    except Exception as e:
        request = ('shutdown', None, None, None)
        client_socket.send(pickle.dumps(request))
        print("client fault: ", e)


# 创建并启动服务器线程
server_thread = threading.Thread(target=server)
server_thread.start()

# 创建并启动客户端线程
client_thread = threading.Thread(target=client)
client_thread.start()

client_thread.join()
server_thread.join()