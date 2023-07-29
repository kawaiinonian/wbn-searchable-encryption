# import matplotlib.pyplot as plt
# import pickle
# import numpy as np
# import os 

# path = os.getcwd() + "/lab_data/"
# with open(path + "ours", mode='rb') as f:
#     ours = pickle.load(f)
# with open(path + "tdsc23", mode='rb') as f:
#     tdsc23 = pickle.load(f)

# num = [200, 400, 600, 800, 1000]
# x = np.array(num)
# y = np.array(ours["using_time_update"])
# z = np.array(tdsc23["using_time_update"])
# plt.plot(x, y, 'b', label = "ours")
# plt.plot(x, z, 'm', label = "tdsc23")
# plt.title("file nums vs. using time update")
# plt.xlabel("file nums")
# plt.ylabel("using time update")
# plt.legend(loc='upper left')
# save_path = path + "end2end_update_time.png"
# plt.savefig(save_path, dpi=300)

import seaborn as sns
import pandas as pd
import pickle
import numpy as np
import os 
import json
from itertools import islice

path = os.getcwd() + "/lab_data/"
with open(path + "ours", mode='rb') as f:
    ours = pickle.load(f)
with open(path + "tdsc23", mode='rb') as f:
    tdsc23 = pickle.load(f)

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

path_data = os.getcwd() + "/project/lab/data/enron1w_washed.json"
document = load_data_as_bytes(path_data)

nfile = [200, 400, 600, 800, 1000]
num = []
for n in nfile:
    total = 0
    for _, v in islice(document.items(), n):
        total += len(v)
    num.append(total)
# num = [200, 400, 600, 800, 1000]
x = np.array(num)
y_ours = np.array(ours["using_storage_on_server"])/1000
y_tdsc23 = np.array(tdsc23["using_storage_on_server"])/1000

# Prepare a pandas DataFrame for seaborn
df_ours = pd.DataFrame({'DB size': x, 'using storage on server(KB)': y_ours, 'method': 'ours'})
df_tdsc23 = pd.DataFrame({'DB size': x, 'using storage on server(KB)': y_tdsc23, 'method': '[7]'})
df = pd.concat([df_ours, df_tdsc23])

sns.set_style("whitegrid")
plt = sns.lineplot(data=df, x='DB size', y='using storage on server(KB)', hue='method', style = "method")
plt.set_title("DB size vs. using storage on server")
save_path = path + "storage_cost_on_server.png"
plt.get_figure().savefig(save_path, dpi=300)
