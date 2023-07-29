import socket
import pickle
import ctypes
import time
import struct
import json
import secrets
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import sys
import os
# from project.shell.utils.datatype import SEARCH_KEY, USER_KEY
# from project.shell.utils.method import get_fd, get_key_from_bytes
# from project.shell.client.c_user import c_user
sys.path.append(os.getcwd() + "/project")
from shell.client.c_user import c_user
from shell.server.c_server import c_server
from shell.utils.datatype import *
from shell.utils.method import *

def get_random_key(length: int):
    return secrets.token_bytes(length)

LAMBDA = 256//8
server_addr = socket.gethostname()
server_port = 8080
libclient = os.getcwd() + "/project/core/libclient.so"
path = os.getcwd() + "/project/lab/data/enron1w_washed.json"

cusr = c_user(libclient)


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


def communicate(_payload, _function):
    """
    与服务器通讯，前八个字节为功能，后面是通讯载荷
    返回服务器的返回值，该返回值是结构化后的
    """
    function = bytes(_function).ljust(8)
    payload = pickle.dumps(_payload)
    msg = function + payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_addr, server_port))

        data_size = struct.pack(">I", len(msg))
        client.send(data_size)
        client.send(msg)
        print("finish send data with {}bytes".format(len(msg)))

        response_size = client.recv(4)
        response_size = struct.unpack(">I", response_size)[0]
        print("now going to recv from server with size {}bytes".format(response_size))
        response = client.recv(response_size)
        response = pickle.loads(response)
    except ValueError:
        print("failed")
    finally:
        client.close()
    return response

def get_uk():
    return USER_KEY(
        get_key_from_bytes(get_random_key(LAMBDA)),
        get_key_from_bytes(get_random_key(LAMBDA)),
    )

def main():
    sk = SEARCH_KEY(
        get_key_from_bytes(get_random_key(LAMBDA)),
        get_key_from_bytes(get_random_key(LAMBDA)),
        get_key_from_bytes(get_random_key(LAMBDA)),
    )
    uk = USER_KEY(
        get_key_from_bytes(get_random_key(LAMBDA)),
        get_key_from_bytes(get_random_key(LAMBDA)),
    )
    usr1 = b"helloworld".ljust(LAMBDA)

    document = load_data_as_bytes(path)
    files = []
    num = [200,400,600,800,1000]
    tmp = 0
    for k, v in document.items():
        if tmp < 100:
            v.append(b"common_word")
            tmp += 1
        files.append(get_fd(v, usr1+bytes(k).ljust(LAMBDA)))
    docs = [usr1+d.ljust(LAMBDA) for d in document.keys()]
    from itertools import islice
    unique_words = set()
    for k, v in islice(document.items(), 5000):
        unique_words.update(v)
    
    using_time_update = []
    using_time_search = []
    total_size = []

    for n in num:
        file = files[:n]
        doc = docs[:n]
        t1 = time.time()
        xset, index_num = cusr.updateData_generate(sk, file)
        xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
        ret = communicate(xset, b"update")
        t2 = time.time()
        uks = [get_uk() for _ in range(5)]
        for uk in tqdm(uks):
            dockey, uset = cusr.online_auth(sk, uk, doc)
            uset = {bytes(u.uid):bytes(u.ud) for u in uset}
            dockey = [dk for dk in dockey]
            ret = communicate(uset, b"online")
        total_size.append(communicate([], b"getsize"))
        print(str(ret))
        using_time_update.append(t2-t1)

        uk_do = get_uk()
        dockey, uset = cusr.online_auth(sk, uk_do, doc[:100])
        uset = {bytes(u.uid):bytes(u.ud) for u in uset}
        dockey = [dk for dk in dockey]
        ret = communicate(uset, b"online")

        t1 = time.time()
        query = cusr.search_generate(get_word_from_bytes(b"common_word"), uk_do, dockey, [])
        query = [(bytes(q.uid), bytes(q.stk)) for q in query]
        ret = communicate((query, None), b"search")
        t2 = time.time()
        using_time_search.append(t2-t1)
        print("find {} files".format(len(ret)))
        communicate(None, b"reset")

    save_data = {
        "using_time_update": using_time_update,
        "using_time_search": using_time_search,
        "using_storage_on_server": total_size,
    }
    with open("/root/project515/lab_data/ours", mode="wb") as f:
        pickle.dump(save_data, f)
    with open("/root/project515/lab_data/ours", mode='rb') as f:
        test = pickle.load(f)
    print(test)
    # save_path = os.getcwd() + "/project/lab/fig/"    
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)
    # x = np.array(num)
    # y = np.array(using_time_update)
    # plt.plot(x, y, '.-b', label = 'usr calculate')
    # plt.title("File count to update vs. End2end time")
    # plt.xlabel("File count to search")
    # plt.ylabel("End2end time")
    # # plt.show()
    # plt.savefig(save_path + "File_count_to_update_vs_End2end_time.png", dpi=300)
    # plt.close()

 
main()