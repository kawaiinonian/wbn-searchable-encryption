import sys
import os
sys.path.append(os.getcwd() + "/tdsc22")
from shell.c_server import *
from shell.c_user import *
from shell.datatype import *
from shell.method import *
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

libclient = os.getcwd() + "/tdsc22/core/libclient.so"
libserver = os.getcwd() + "/tdsc22/core/libserver.so"
file_path = os.getcwd() + "/tdsc22/demo/demo.json"
file_raw = load_data_as_bytes(file_path) 
cuser = c_user(libclient)
csver = c_server(libserver)

mk = MK(
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
    get_key_from_bytes(get_random_key(LAMBDA)),
)
files = []
for w in file_raw:
    word = get_key_from_bytes(w)
    ids = []
    for fid in file_raw[w]:
        one_id = type_id()
        memmove(one_id, fid, len(fid))
        ids.append(pointer(one_id))
    p_type = POINTER(type_id) * len(file_raw[w])
    p_fids = p_type(*ids)
    files.append(WORD_FILE(p_fids, word, len(file_raw[w])))


edb, xset = cuser.update(mk, files)
db = {bytes(item.l):(bytes(item.e), bytes(item.y)) for item in edb}
xset = [bytes(xtag) for xtag in xset]

word1 = b"common_word"
word2 = b"word1"
word3 = b"word2"
word = []
word.append(get_word_from_bytes(word1))
# word.append(get_word_from_bytes(word2))
# word.append(get_word_from_bytes(word3))
sk_ptr = cuser.auth(word)
sk = sk_ptr.contents
stag = cuser.get_stag(mk, word, sk_ptr)
cnt = 0
result = []
while True:
    tokens = cuser.token_generate(sk, word, mk, cnt)
    tokens = [bytes(token.contents) for token in tokens]
    ret = csver.search(tokens, stag, cnt, db, xset)
    if ret == b"stop":
        break
    else:
        result.append(bytes(ret))
    cnt += 1

print(result)
