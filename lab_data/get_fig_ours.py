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

path = os.getcwd() + "/project/lab/data/enron10w_washed.json"
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
for k, v in document.items():
    files.append(get_fd(v, usr1+bytes(k).ljust(LAMBDA)))
docs = [usr1+d.ljust(LAMBDA) for d in document.keys()]


cusr = c_user(libclient)
csvr = c_server(libserver)
print("load client core success")
using_time_update = []
using_time_usr_search_online = []
using_time_svr_search_online = []
using_time_usr_search_offline = []
using_time_svr_search_offline = []
using_time_online = []
using_time_offline = []

xwds = []


for n in num:
    file = files[:n]
    doc = docs[:n]
    ws = 0
    for f in file:
        ws += f.wordlen
    xwds.append(ws)
    t1 = time.time()
    xset, index_num = cusr.updateData_generate(sk, file)
    t2 = time.time()
    using_time_update.append(t2 - t1)
    aset = {}
    print("update using time %fs"%(t2-t1))
    xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
    t1 = time.time()
    dockey, uset = cusr.online_auth(sk, uk, doc)
    t2 = time.time()
    using_time_online.append(t2 - t1)
    uset = {bytes(u.uid):bytes(u.ud) for u in uset}
    dockey = [dk for dk in dockey]

    t1 = time.time()
    query = cusr.search_generate(get_word_from_bytes(word), uk, dockey, [])
    t2 = time.time()
    if len(query) != n:
        print("doesn't take n tokens, something maybe wrong")
    using_time_usr_search_online.append(t2-t1)

    query = [(bytes(q.uid), bytes(q.stk)) for q in query]
    t1 = time.time()
    result = csvr.search(query, None, uset, aset, xset)
    t2 = time.time()
    if (len(result)) != n:
        print("doesn't find n files, something maybe wrong in online")
    using_time_svr_search_online.append(t2-t1)

    t1 = time.time()
    tmpset, usr_auth, dockey1 = cusr.offline_auth(uk, uk1, doc,
                                                usr2, dockey, [])
    t2 = time.time()
    using_time_offline.append(t2 - t1)

    csvr.Aset_update(aset, bytes(tmpset.contents.aid), bytes(tmpset.contents.trapgate), None)
    dockey1 = [dk for dk in dockey1]
    usr_auth = [ua for ua in usr_auth]

    t1 = time.time()
    query = cusr.search_generate(get_word_from_bytes(word), uk1, dockey1, usr_auth)
    t2 = time.time()
    using_time_usr_search_offline.append(t2 - t1)

    query = [(bytes(q.uid), bytes(q.stk)) for q in query]
    t1 = time.time()
    result = csvr.search(query, bytes(tmpset.contents.aid), uset, aset, xset)
    t2 = time.time()
    if (len(result)) != n:
        print("doesn't find n files, something maybe wrong")
    using_time_svr_search_offline.append(t2 - t1)

print(using_time_usr_search_online)
print(using_time_svr_search_online)
print(using_time_usr_search_offline)
print(using_time_svr_search_offline)
print(using_time_online)
print(using_time_offline)

import seaborn as sns
import pandas as pd
import numpy as np
import os 

save_path_dir = os.getcwd() + "/lab_data/"   
x = np.array(num)

sns.set_style("whitegrid")

df_update = pd.DataFrame({'File count to update': x, 'Calculation time(s)': using_time_update})
plt = sns.lineplot(data=df_update, x='File count to update', y='Calculation time(s)')
plt.set_title("File count to update vs. using time")
save_path = save_path_dir + "File_count_to_update_vs_Calculation_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()
del plt

df_online_auth = pd.DataFrame({'File count to auth': x, 'Calculation time(s)': using_time_online, "method": "online"})
df_offline_auth = pd.DataFrame({'File count to auth': x, 'Calculation time(s)': using_time_offline, "method": "offline"})
df_auth = pd.concat([df_online_auth, df_offline_auth])
plt = sns.lineplot(data=df_auth, x='File count to auth', y='Calculation time(s)', hue='method', style="method")
plt.set_title("File count to auth vs. using time")
save_path = save_path_dir + "File_count_to_auth_vs_Calculation_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()
del plt

df_online_usr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_usr_search_online, "method": "client"})
df_online_svr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_svr_search_online, "method": "server"})
df = pd.concat([df_online_usr, df_online_svr])
plt = sns.lineplot(data=df, x='File count to search', y='Calculation time(s)', hue='method', style="method")
plt.set_title("File count to search vs. using time")
save_path = save_path_dir + "File_count_to_search_onlineauth_vs_Calculation_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()
del plt

df_offline_usr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_usr_search_offline, "method": "client"})
df_offline_svr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_svr_search_offline, "method": "server"})
df = pd.concat([df_offline_usr, df_offline_svr])
plt = sns.lineplot(data=df, x='File count to search', y='Calculation time(s)', hue='method', style="method")
plt.set_title("File count to search vs. using time")
save_path = save_path_dir + "File_count_to_search_offlineauth_vs_Calculation_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()
del plt

df_online_usr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_usr_search_online, "method": "online-authed"})
df_offline_usr = pd.DataFrame({'File count to search': x, 'Calculation time(s)': using_time_usr_search_offline, "method": "offline-authed"})
df = pd.concat([df_online_usr, df_offline_usr])
plt = sns.lineplot(data=df, x='File count to search', y='Calculation time(s)', hue='method', style="method")
plt.set_title("File count to search vs. using time")
save_path = save_path_dir + "File_count_to_search_vs_Calculation_time.png"
plt.get_figure().savefig(save_path, dpi=300)
plt.get_figure().clf()
del plt