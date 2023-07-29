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
data_path = os.getcwd() + "/enron_washed.json"
data_path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
file_raw = load_data_as_bytes(data_path) 
cuser = c_user(libclient)
csver = c_server(libserver)

def measure_storage(db, xset):
    total = 0
    for k, v in db.items():
        total += len(k) + len(v[0]) + len(v[1])
    for xtag in xset:
        total += len(xtag)
    return total

mk = MK(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
# num = [1000, 5000, len(file_raw)]
num = [len(file_raw)]
# num = [10]
# print(len(file_raw))
# num = [1000]
auth_num = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
auth_num = [1000]
auth_word = ["auth_word1", "auth_word2", "auth_word3", "auth_word4"]
using_time = []
using_storage = []
for n in num:
    file_use_raw = dict(islice(file_raw.items(), n))
    file_use = {}
    for f, words in file_use_raw.items():
        for w in words:
            if w not in file_use.keys():
                file_use[w] = []
            file_use[w].append(f)
    # file_use[auth_word[0]] = ["{}".format(i) for i in range(auth_num[0])]
    # file_use[auth_word[1]] = ["{}".format(i) for i in range(auth_num[1])]
    # file_use[auth_word[2]] = ["{}".format(i) for i in range(auth_num[2])]
    # file_use[auth_word[3]] = ["{}".format(i) for i in range(auth_num[3])]
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

    # t1 = time()
    # edb, xset = cuser.update(mk, files)
    # db = {bytes(item.l):(bytes(item.e), bytes(item.y)) for item in edb}
    # xset = [bytes(xtag) for xtag in xset]
    # using_storage.append(measure_storage(db, xset))
    # t2 = time()
    # using_time.append(t2 - t1)

    # for i, w_raw in enumerate(auth_word):
    #     w = [get_word_from_bytes(w_raw)]
    #     for j in range(auth_num[i]):
    #         wordset = list(file_use_raw.values())[j]
    #         for word in wordset:
    #             w.append(get_word_from_bytes(word))
    #     print("finish prepare auth words, total:{}".format(len(w)))
    #     t1 = time()
    #     sk_ptr = cuser.auth(w)
    #     t2 = time()
    #     print("finish auth calculation, using time {}s".format(t2-t1))
    #     using_time.append(t2-t1)
    for i in auth_num:
        w = set()
        word_use = []
        for v in list(file_use_raw.values())[:i]:
            for word in v:
                w.add(word)
        for word in w:
            word_use.append(get_word_from_bytes(word))
        t1 = time()
        sk_ptr = cuser.auth(word_use)
        t2 = time()
        using_time.append(t2-t1)
        print("auth using time %fs"%(t2-t1))
print(using_time)
# print(using_storage)