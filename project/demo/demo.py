import sys
sys.path.append("/home/kawaiinonian/project/project")
from shell.client.c_user import c_user
from shell.server.c_server import c_server
from shell.utils.datatype import *
from shell.utils.method import *
import json


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

path = "/home/kawaiinonian/project/project/demo/demo.json"
word = b"common_word"
libclient = "/home/kawaiinonian/project/project/core/libclient.so"
libserver = "/home/kawaiinonian/project/project/core/libserver.so"
usr1 = b"helloworld\x00\x00\x00\x00\x00\x00"
xset = {}
uset = {}
aset = {}
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
document = load_data_as_bytes(path)
doc = []
for k, v in document.items():
    doc.append(get_fd(v, usr1+k))

cusr = c_user(libclient)
print("load client core success")
xset_data, index_num = cusr.updateData_generate(sk, doc)
for i in range(index_num):
    xset[xset_data[i*(LAMBDA+FILE_DESC_LEN_ENC):i*(LAMBDA+FILE_DESC_LEN_ENC)+LAMBDA]] = \
        xset_data[i*(LAMBDA+FILE_DESC_LEN_ENC)+LAMBDA:(i+1)*(LAMBDA+FILE_DESC_LEN_ENC)]
    
dockey_data, uset_data = cusr.online_auth(sk, uk, doc)
print("finish online auth")
for i in range(len(doc)):
    uset[uset_data[(i*2+1)*LAMBDA:(i+1)*2*LAMBDA]] = uset_data[i*2*LAMBDA:(i*2+1)*LAMBDA]

dockey = [k.contents for k in dockey_data]
print("going to get query")
query_data = cusr.search_generate(get_word_from_bytes(word), uk, dockey, [])
query = [(query_data[i*2*LAMBDA:(i*2+1)*LAMBDA], query_data[(i*2+1)*LAMBDA:(i+1)*2*LAMBDA]) \
            for i in range(len(dockey))]

print(len(query))
cserver = c_server(libserver)
result = cserver.search(query, None, uset, aset, xset)
for r in result:
    if r not in xset.values():
        print("failed")