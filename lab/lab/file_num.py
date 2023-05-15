import sys
import os
sys.path.append(os.getcwd() + "/project")
from shell.client.c_user import c_user
from shell.utils.datatype import *
from shell.utils.method import *
import json
import matplotlib.pyplot as plt
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
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes

path = os.getcwd() + "/project/lab/data/enron10w_washed.json"
libclient = os.getcwd() + "/project/core/libclient.so"
usr1 = b"helloworld".ljust(LAMBDA)
num = [500, 1000, 3000, 5000, 10000, 20000, 30000, 50000]
# num = [500, 1000, 3000]
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
ub = get_random_key(LAMBDA)
document = load_data_as_bytes(path)
files = []
for k, v in document.items():
    files.append(get_fd(v, usr1+k))
doc = [usr1+d.ljust(LAMBDA) for d in document.keys()]

cusr = c_user(libclient)
print("load client core success")
using_time = []
using_time_off = []

for n in num:
    d = doc[:n]
    dockey_data, _ = cusr.online_auth(sk, uk, d)
    dockey = [k for k in dockey_data]
    t1 = time.time()
    _, _, _ = cusr.offline_auth(uk, uk1, d,
                ub, dockey, [])
    t2 = time.time()
    using_time_off.append(t2-t1)
    t1 = time.time()
    dockey_data, _ = cusr.online_auth(sk, uk, d)
    t2 = time.time()
    using_time.append(t2-t1)


x = np.array(num)
y = np.array(using_time)
z = np.array(using_time_off)

plt.plot(x, y, 'b-', label = 'online')
plt.plot(x, z, 'o--', label = 'offline')
plt.title("File count vs. Calculation time")
plt.xlabel("File count")
plt.ylabel("Calculation time")
plt.show()

# x = np.array(num)
# y = np.array(using_time_off)
# plt.plot(x, y)
# plt.title("File count vs. Calculation time -- offline")
# plt.xlabel("File count")
# plt.ylabel("Calculation time -- offline")
# plt.show()