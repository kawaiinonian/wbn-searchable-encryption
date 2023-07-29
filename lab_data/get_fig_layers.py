import sys
import os
sys.path.append(os.getcwd() + "/project")
from shell.client.c_user import c_user
from shell.server.c_server import c_server
from shell.utils.datatype import *
from shell.utils.method import *
import json
# import matplotlib.pyplot as plt
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
libserver = os.getcwd() + "/project/core/libserver.so"
libclient = os.getcwd() + "/project/core/libclient.so"
usr1 = b"helloworld".ljust(LAMBDA)
usr2 = b"worldhello".ljust(LAMBDA)
word = b"comman_word"
num = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
# num = [1, 2, 3, 4, 5]
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk1 = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)

document = load_data_as_bytes(path)
files = []
for k, v in document.items():
    files.append(get_fd(v, usr1+bytes(k).ljust(LAMBDA)))
docs = [usr1+d.ljust(LAMBDA) for d in document.keys()]


cusr = c_user(libclient)
csvr = c_server(libserver)
print("load client core success")
using_time_search = []

xwds = []

file = files[:100]
doc = docs[:100]
xset, index_num = cusr.updateData_generate(sk, file)
xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
dockey, uset = cusr.online_auth(sk, uk1, doc)
uset = {bytes(u.uid):bytes(u.ud) for u in uset}
dockey = [dk for dk in dockey]
aset = {}

# query = cusr.search_generate(get_word_from_bytes(word), uk1, dockey, [])
# query = [(bytes(q.uid), bytes(q.stk)) for q in query]
# t1 = time.time()
# result = csvr.search(query, None, uset, aset, xset)
# t2 = time.time()
# if (len(result)) != 100:
#     print("doesn't find 100 files, something maybe wrong")
# using_time_search.append(t2 - t1)

uk = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
usr = b"helloworld".ljust(LAMBDA)

tmp_aset, usrauth, dockey = cusr.offline_auth(uk1, uk, doc, usr, dockey, [])
dockey = [dk for dk in dockey]
usrauth = [ua for ua in usrauth]
csvr.Aset_update(aset, bytes(tmp_aset.contents.aid), bytes(tmp_aset.contents.trapgate), None)
query = cusr.search_generate(get_word_from_bytes(word), uk, dockey, usrauth)
query = [(bytes(q.uid), bytes(q.stk)) for q in query]
t1 = time.time()
result = csvr.search(query, bytes(tmp_aset.contents.aid), uset, aset, xset)
t2 = time.time()
if (len(result)) != 100:
    print("doesn't find 100 files, something maybe wrong")
using_time_search.append(t2 - t1)
uk_last = uk
last_aset = tmp_aset

for _ in tqdm(range(99)):
    uk = USER_KEY(
        get_key_from_bytes(get_random_key(LAMBDA)),
        get_key_from_bytes(get_random_key(LAMBDA)),
    )
    usr = get_random_key(LAMBDA)
    tmp_aset, usrauth, dockey = cusr.offline_auth(uk_last, uk, doc, usr, dockey, usrauth)
    dockey = [dk for dk in dockey]
    usrauth = [ua for ua in usrauth]
    csvr.Aset_update(aset, bytes(tmp_aset.contents.aid), bytes(tmp_aset.contents.trapgate), bytes(last_aset.contents.aid))
    query = cusr.search_generate(get_word_from_bytes(word), uk, dockey, usrauth)
    query = [(bytes(q.uid), bytes(q.stk)) for q in query]
    t1 = time.time()
    result = csvr.search(query, bytes(tmp_aset.contents.aid), uset, aset, xset)
    t2 = time.time()
    if (len(result)) != 100:
        print("doesn't find 100 files, something maybe wrong")
    using_time_search.append(t2 - t1)
    uk_last = uk
    last_aset = tmp_aset


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as mplt
save_path_dir = os.getcwd() + "/lab_data/"   
x = np.array([i for i in range(len(using_time_search))])
y = np.array(using_time_search) * 1000
sns.set_style("whitegrid")

df_update = pd.DataFrame({'Auth layers': x, 'Calculation time(ms)': y})
plt = sns.lineplot(data=df_update, x='Auth layers', y='Calculation time(ms)')
mplt.ylim(0, 500)
plt.set_title("Auth layers vs. search calculation time")
save_path = save_path_dir + "Auth_layers_vs_search_using_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()