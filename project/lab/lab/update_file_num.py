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
    print("loading raw data")
    for key, value_list in tqdm(data.items(), mininterval=1):
        key_as_bytes = key.encode()
        value_list_as_bytes = [word.encode() for word in value_list]
        # if len(value_list_as_bytes) == 0:
        #     value_list_as_bytes.append(b"comman_word")
        # else:
        #     value_list_as_bytes[-1] = b"comman_word"
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes



path = os.getcwd() + "/enron_washed.json"
# path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
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
document = load_data_as_bytes(path)
files = []
print("process raw data to file desc")
for k, v in tqdm(document.items()):
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

def measure_size():
    total = 0
    for k, v in Xset.items():
        total += (len(k) + len(v))
    for k, v in Uset.items():
        total += (len(k) + len(v))
    for k, v in Aset.items():
        total += (len(k) + len(v.alpha))
    return total

# num = [100]
num = [len(docs)]
using_time = []
auth_num = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
percent = 0.5
using_storage = []

def reset():
    Xset.clear()
    Uset.clear()
    Aset.clear()

for n in num:
    file = files[:n]
    doc = docs[:n]
    ws = 0
    for f in file:
        ws += f.wordlen
    print(ws)
    t1 = time.time()
    xset, index_num = cusr.updateData_generate(sk, file)
    t2 = time.time()
    print("update using time %fs"%(t2-t1))
    Xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
    using_time.append(t2-t1)
    # for au in auth_num:
    #     auth_doc = doc[:au]
    #     t1 = time.time()
    #     dockey, uset = cusr.online_auth(sk, uk, auth_doc)
    #     t2 = time.time()
    #     # print("online auth using time %fs"%(t2-t1))
    #     dockey = [dk for dk in dockey]
    #     uk = USER_KEY(
    #         get_key_from_bytes(get_random_key(LAMBDA)),
    #         get_key_from_bytes(get_random_key(LAMBDA)),
    #     )
    #     usr = b"helloworld".ljust(LAMBDA)
    #     t1 = time.time()
    #     tmp_aset, usrauth, dockey = cusr.offline_auth(uk1, uk, auth_doc, usr, dockey, [])
    #     t2 = time.time()
    #     print("offline auth using time %fs"%(t2-t1))
        # dockey = [dk for dk in dockey]
        # usrauth = [ua for ua in usrauth]
        # uk_last = uk
        # last_aset = tmp_aset
        # for i in range(8):
        #     uk = USER_KEY(
        #         get_key_from_bytes(get_random_key(LAMBDA)),
        #         get_key_from_bytes(get_random_key(LAMBDA)),
        #     )
        #     usr = get_random_key(LAMBDA)
        #     t1 = time.time()
        #     tmp_aset, usrauth, dockey = cusr.offline_auth(uk_last, uk, auth_doc, usr, dockey, usrauth)
        #     t2 = time.time()
        #     # if i % 2 == 1:
        #     print("offline auth using time %fs"%(t2-t1))
        #     dockey = [dk for dk in dockey]
        #     usrauth = [ua for ua in usrauth]
        #     uk_last = uk
        #     last_aset = tmp_aset
    auth_doc = doc[:int(n*0.05)]
    for _ in tqdm(range(int(1000*percent)), mininterval=1):
        uk = USER_KEY(
            get_key_from_bytes(get_random_key(LAMBDA)),
            get_key_from_bytes(get_random_key(LAMBDA)),
        )
        dockey, uset = cusr.online_auth(sk, uk, auth_doc)
        uset = {bytes(u.uid):bytes(u.ud) for u in uset}
        Uset.update(uset)
    dockey = [dk for dk in dockey]
    for i in tqdm(range(int(1000*(1-percent)))):
        uk1 = USER_KEY(
            get_key_from_bytes(get_random_key(LAMBDA)),
            get_key_from_bytes(get_random_key(LAMBDA)),
        )
        usr = get_random_key(LAMBDA)
        aset, _, _ = cusr.offline_auth(uk, uk1, auth_doc, usr, dockey, [])
        csvr.Aset_update(Aset, bytes(aset.contents.aid), bytes(aset.contents.trapgate), None)
    using_storage.append(measure_size())
    reset()
print(using_storage)
# print(using_time)
#     uset = {bytes(u.uid):bytes(u.ud) for u in uset}
#     dockey = [dk for dk in dockey]
#     t1 = time.time()
#     query = cusr.search_generate(get_word_from_bytes(word), uk, dockey, [])
#     t2 = time.time()
#     if len(query) != n:
#         print("doesn't take n tokens, something maybe wrong")
#     using_time_usr.append(t2-t1)
#     query = [(bytes(q.uid), bytes(q.stk)) for q in query]
#     t1 = time.time()
#     result = csvr.search(query, None, uset, aset, xset)
#     t2 = time.time()
#     if (len(result)) != n:
#         print("doesn't find n files, something maybe wrong")
#     using_time_svr.append(t2-t1)

