import secrets
import socket
import pickle
import hashlib
import hmac
import struct 
from obliv.voram import create_voram, Ref
import json
import os
from time import time
from tqdm import tqdm


class OMapUsr:
    """
    一个用户的Omap结构，代码完全参照GitHub上面的demo
    https://github.com/dsroche/obliv
    """
    def __init__(self, oram: Ref) -> None:
        self.generator = oram
        self.map = {}
        self.cnt = 0
    def get(self, word):
        return self.map[word].get()
    def put(self, word, value):
        if word not in self.map.keys():
            self.map[word] = self.generator.create()
            self.cnt += 1
        self.map[word].set(value)

# OMap: Dict[str, OMapUsr]
# AccessList: Dict[str, list]
OMap = {}
AccessList = {}
DictW = {}

def get_random_key(length: int):
    return secrets.token_bytes(length)

LAMBDA = 256//8
PATH_LEN = 128//8

def enroll(ukey, size):
    # 登记一个用户，为他分配一个Omap项
    v = create_voram(blobs_limit=size, blob_size=4*8)
    OMap[ukey] = OMapUsr(v)

def share(KeyValues, uid, fid):
    # 更新accesslist
    if fid not in AccessList.keys():
        AccessList[fid] = []
    AccessList[fid].append(uid)
    for item in KeyValues:
        DictW[item[0]] = item[1]


def update(KeyValues):
    # 更新索引
    for item in KeyValues:
        DictW[item[0]] = item[1]

def search(tlist):
    ret = []
    for t in tlist:
        ret.append(DictW[t])
    return ret

def get_omap(word, ukey):
    ret = OMap[ukey].get(word)
    return ret

def put_omap(wordset, uidset, ukeyset):
    ret = {}
    for i, uk in enumerate(ukeyset):
        uid = uidset[i]
        ret[uid] = {}
        for word in wordset:
            if word not in OMap[uk].map.keys():
                OMap[uk].put(word, 0)
            val = OMap[uk].get(word)
            val += 1
            OMap[uk].put(word, val)
            ret[uid][word] = val
    # print(pickle.dumps(ret))
    return ret


def get_hmac(word, cnt, op, key):
    """
    获取hmac = H(word || cnt || op)
    """
    msg = word + bytes(cnt) + bytes(op)
    obj = hmac.new(key, msg, hashlib.sha256)
    return obj.digest()

def get_val(fid, op, hash):
    """
    获取(fid || op) ^ hash，对应Update和Share的14行
    """
    data = (fid + op).ljust(LAMBDA)
    result = [b1 ^ b2 for b1, b2 in zip(data, hash)]
    return result

class owner:
    """
    DO结构
    """
    def __init__(self) -> None:
        self.DictW = dict()
        self.UserKeys = dict()
        self.AccessList = dict()
        self.doc = dict()

    def enroll(self, uid: bytes):
        """
        DO登记一个DU，返回一个DU的Omapkey
        与服务器通讯，在服务器上新建一个OMap项
        """
        ukey = get_random_key(LAMBDA)
        self.UserKeys[uid] = ukey
        return ukey

    def share(self, uid, fid, wlist):
        """
        对uid分享fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        self.AccessList[fid].append(uid)
        key = self.UserKeys[uid]
        # word_set = self.doc[fid]
        KeyValues = []

        # 更新Omap[uid][word]
        cnt = put_omap(wlist, [uid], [key])
        # 更新文件索引
        for word in wlist:
            # 复用了DU用于检索Omap的key，作为对称加密密钥
            addr = get_hmac(word, cnt[uid][word], 0, key)
            val = get_val(fid, b'add', get_hmac(word, cnt[uid][word], 1, key))
            KeyValues.append((addr, val))
        # communicate([KeyValues, uid, fid], b"share")
        share(KeyValues, uid, fid)

    def update(self, fid, op, wlist):
        """
        更新fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        KeyValues = []
        self.doc[fid] = wlist
        # 更新Omap
        cnts = put_omap(wlist, self.AccessList[fid], [self.UserKeys[i] for i in self.AccessList[fid]])
        for uid in self.AccessList[fid]:
            key = self.UserKeys[uid]
            for word in wlist:
                # 复用了DU用于检索Omap的key，作为对称加密密钥
                addr = get_hmac(word, cnts[uid][word], 0, key)
                val = get_val(fid, op, get_hmac(word, cnts[uid][word], 1, key))
                KeyValues.append((addr, val))
        # communicate(KeyValues, b"update")
        update(KeyValues)

class user:
    def __init__(self, uid:bytes) -> None:
        self.uid = uid

    def register(self, key):
        self.ukey = key

    def search(self, word):
        tlist = []
        cnt = get_omap(word, self.ukey)
        for i in range(1, cnt+1):
            t = get_hmac(word, i, 0, self.ukey)
            tlist.append(t)
        # result = communicate(tlist, b"search")
        result = search(tlist)
        return result

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
        key_as_bytes = key.encode().ljust(PATH_LEN)
        value_list_as_bytes = [word.encode() for word in value_list]
        data_as_bytes[key_as_bytes] = value_list_as_bytes

    return data_as_bytes


data_path = os.getcwd() + "/project/lab/data/enron1w_washed.json"
# data_path = os.getcwd() + "/enron_washed.json"
documents = load_data_as_bytes(data_path)
# 取出全部的文件标识符，构成列表docs
docs = [d for d in documents.keys()]
# num = [1000, 5000, len(docs)]
# num = [len(docs)]
num = [1000]
auth_num = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for n in num:
    do = owner()
    dus = []
    doc = docs[:n]
    uid = get_random_key(LAMBDA)
    du = user(uid)
    ukey = do.enroll(uid)
    enroll(ukey, n*10)
    du.register(ukey)
    using_time = []
    t1 = time()
    for d in tqdm(doc, mininterval=10):
        do.share(du.uid, d, documents[d])
    t2 = time()
    using_time.append(t2-t1)
    for i in auth_num:
        t1 = time()
        for d in tqdm(doc[:i]):
            do.share(du.uid, d, documents[d])
        t2 = time()
        using_time.append(t2-t1)
        print("share using time %fs"%(t2-t1))
    print(using_time)
