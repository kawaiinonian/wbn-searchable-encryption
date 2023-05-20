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

def get_uk(num):
    ret = []
    for _ in range(num):
        uk = USER_KEY(
            get_key_from_bytes(get_random_key(LAMBDA)),
            get_key_from_bytes(get_random_key(LAMBDA)),
        )
        ret.append(uk)

    return ret

path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
libclient = os.getcwd() + "/project/core/libclient.so"
usr1 = b"helloworld".ljust(LAMBDA)
num = [500, 1000, 3000, 5000, 10000, 20000, 50000, 100000]
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
document = load_data_as_bytes(path)
files = []
for k, v in document.items():
    files.append(get_fd(v, usr1+bytes(k).ljust(LAMBDA)))
docs = [usr1+d.ljust(LAMBDA) for d in document.keys()]

cusr = c_user(libclient)
print("load client core success")
using_time = []
for n in num:
    doc = docs[:10]
    uks = get_uk(n)
    t1 = time.time()
    for uk in uks:
        _, _ = cusr.online_auth(sk, uk, doc)
    t2 = time.time()
    using_time.append(t2-t1)

x = np.array(num)
y = np.array(using_time)
plt.plot(x, y)
plt.title("User count vs. Calculation time")
plt.xlabel("User count")
plt.ylabel("Calculation time")
plt.show()
