from client import user, owner, communicate
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import time
import secrets
from tqdm import tqdm

def get_random_key(length: int):
    """
    返回一个length长度的随机字节串
    """
    return secrets.token_bytes(length)

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
        key_as_bytes = key.encode().ljust(29)
        value_list_as_bytes = [word.encode() for word in value_list]
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes

# 加载数据，load之后的数据集呈现为 bytes:[bytes, bytes]的字典结构
path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
documents = load_data_as_bytes(path)
# 取出全部的文件标识符，构成列表docs
docs = [d for d in documents.keys()]


num = [100, 300, 500]
using_time = []
for n in num:
    do = owner()
    dus = []
    doc = docs[:n]
    # 构建一些DU
    for _ in range(10):
        uid = get_random_key(32)
        du = user(uid)
        ukey = do.enroll(uid)
        du.register(ukey)
        dus.append(du)
    print("finish register")
    # 第一次上传文件，这是因为：本方案中上传文件后并未授权，而授权情况会影响update的时间
    for d in doc:
        do.update(d, b'add', documents[d])
    print("finish update")
    print("now going to share")
    # 将上面上传的文件授权给用户，在服务端构建userlist
    for du in tqdm(dus):
        for d in doc:
            do.share(du.uid, d)
    print("finish share")
    # 再次update之前的文件，现在每次update都要对userlist里面的用户更新它们对应的Omap
    t1 = time.time()
    for d in tqdm(doc):
        do.update(d, b'add', documents[d])
    t2 = time.time()
    using_time.append(t2-t1)
    # 重置服务端
    communicate([], b'reset')

# 绘图
x = np.array(num)
y = np.array(using_time)
plt.plot(x, y)
plt.title("file nums vs. end2end time")
plt.xlabel("file nums")
plt.ylabel("end2end time")
save_path = os.getcwd() + "/tdsc23"    
if not os.path.exists(save_path):
    os.makedirs(save_path)
plt.savefig(save_path + "file_count_vs_end2end_time.png", dpi=300)