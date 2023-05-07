import sys
import os
sys.path.append(os.getcwd() + "/project")
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

path = os.getcwd() + "/project/demo/demo.json"
word = b"common_word"
libclient = os.getcwd() + "/project/core/libclient.so"
libserver = os.getcwd() + "/project/core/libserver.so"
usr1 = b"helloworld".ljust(LAMBDA)
usr2 = b"hellowrold".ljust(LAMBDA)
usr3 = b"bellowrold".ljust(LAMBDA)
xset = {}
uset = {}
aset = {}
sk = SEARCH_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk1 = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk2 = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
uk3 = USER_KEY(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
document = load_data_as_bytes(path)
files = []
for k, v in document.items():
    files.append(get_fd(v, usr1+k))
doc = [usr1+d.ljust(LAMBDA) for d in document.keys()]

cusr = c_user(libclient)
cserver = c_server(libserver)

print("load client core success")
xset, index_num = cusr.updateData_generate(sk, files)
xset = {bytes(x.xwd):bytes(x.ywd) for x in xset}
print("finish update")   
dockey, uset = cusr.online_auth(sk, uk1, doc)
uset = {bytes(u.uid):bytes(u.ud) for u in uset}
print("finish online auth")
dockey1 = [dk for dk in dockey]

aid_ini = get_key_from_bytes(32*b'\x00')
aset1, usr_auth1, dockey2 = cusr.offline_auth(uk1, uk2, doc,
            usr2, dockey1, [])
print("finish offline auth")
cserver.Aset_update(aset, bytes(aset1.contents.aid), bytes(aset1.contents.trapgate), None)
dockey2 = [dk for dk in dockey2]
usr_auth1 = [ua for ua in usr_auth1]

aset2, usr_auth2, dockey3 = cusr.offline_auth(uk2, uk3, doc,
            usr3, dockey2, usr_auth1)
cserver.Aset_update(aset, bytes(aset2.contents.aid), bytes(aset2.contents.trapgate), bytes(aset1.contents.aid))
dockey3 = [dk for dk in dockey3]
usr_auth2 = [ua for ua in usr_auth2]


# dockey = [k.contents for k in dockey3]
# print("going to get query")
# query_data = cusr.search_generate(get_word_from_bytes(word), uk1, dockey, [])
# query = [(query_data[i*2*LAMBDA:(i*2+1)*LAMBDA], query_data[(i*2+1)*LAMBDA:(i+1)*2*LAMBDA]) \
#             for i in range(len(dockey))]

query = cusr.search_generate(get_word_from_bytes(word), uk3, dockey3, usr_auth2)
query = [(bytes(q.uid), bytes(q.stk)) for q in query]
print(len(query))
print('going to search on server')
result = cserver.search(query, None, uset, aset, xset)
print("finish search on server")
for r in result:
    if r not in xset.values():
        print("failed")

