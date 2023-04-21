import sys
sys.path.append("/home/kawaiinonian/project/project/")
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

path = "/home/kawaiinonian/project/project/lab/data/enron10w_washed.json"
libclient = "/home/kawaiinonian/project/project/core/libclient.so"
usr1 = b"helloworld\x00\x00\x00\x00\x00\x00"
num = [500, 1000, 3000, 5000, 10000, 20000, 30000, 50000]
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
document = load_data_as_bytes(path)
docs = []
for k, v in document.items():
    docs.append(get_fd(v, usr1+k))

cusr = c_user(libclient)
print("load client core success")
using_time = []

for n in num:
    t1 = time.time()
    doc = docs[:n]
    _, _ = cusr.updateData_generate(sk, doc)
    t2 = time.time()
    using_time.append(t2-t1)

x = np.array(num)
y = np.array(using_time)
plt.plot(x, y)
plt.title("File count to update vs. Calculation time")
plt.xlabel("File count to update")
plt.ylabel("Calculation time")
plt.show()