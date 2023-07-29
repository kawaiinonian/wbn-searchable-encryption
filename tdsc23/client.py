import secrets
import socket
import pickle
import hashlib
import hmac
import struct 

def get_random_key(length: int):
    return secrets.token_bytes(length)

LAMBDA = 256//8
server_addr = socket.gethostname()
server_port = 8080


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
    data = fid + op
    result = [b1 ^ b2 for b1, b2 in zip(data, hash)]
    return result

def put_Omap(word_set, uid_set, ukey_set):
    """
    令服务端在Omap中修改数据，服务器将为每个uid in uid_set, word in word set 更新Omap[uid][word]
    返回一个字典，
    呈现为：bytes(uid):dict(bytes(ukey):int(cnt))的格式
    """
    cnts = communicate([word_set, uid_set, ukey_set], b"putmap")
    return cnts

def get_Omap(word, uid):
    """
    获取Omap[uid][word]
    """
    cnt = communicate([word, uid], b"getmap")
    return cnt

def get_size():
    size = communicate([], b"getsize")
    return size

def communicate(_payload, _function):
    """
    与服务器通讯，前八个字节为功能，后面是通讯载荷
    返回服务器的返回值，该返回值是结构化后的
    """
    function = bytes(_function).ljust(8)
    payload = pickle.dumps(_payload)
    msg = function + payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_addr, server_port))
        data_size = struct.pack(">I", len(msg))
        client.send(data_size)
        client.send(msg)
        response_size = client.recv(4)
        response_size = struct.unpack(">I", response_size)[0]
        response = client.recv(response_size)
        response = pickle.loads(response)
    except ValueError:
        print("failed")
    finally:
        client.close()
    return response

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
        communicate(ukey, b"enroll")
        return ukey

    
    def share(self, uid, fid):
        """
        对uid分享fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        self.AccessList[fid].append(uid)
        key = self.UserKeys[uid]
        word_set = self.doc[fid]
        KeyValues = []

        # 更新Omap[uid][word]
        cnt = put_Omap(word_set, [uid], [key])
        # 更新文件索引
        for word in word_set:
            # 复用了DU用于检索Omap的key，作为对称加密密钥
            addr = get_hmac(word, cnt[uid][word], 0, key)
            val = get_val(fid, b'add', get_hmac(word, cnt[uid][word], 1, key))
            KeyValues.append((addr, val))
        communicate([KeyValues, uid, fid], b"share")


    def update(self, fid, op, wlist):
        """
        更新fid
        """
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        KeyValues = []
        self.doc[fid] = wlist
        # 更新Omap
        cnts = put_Omap(wlist, self.AccessList[fid], [self.UserKeys[i] for i in self.AccessList[fid]])
        for uid in self.AccessList[fid]:
            key = self.UserKeys[uid]
            for word in wlist:
                # 复用了DU用于检索Omap的key，作为对称加密密钥
                addr = get_hmac(word, cnts[uid][word], 0, key)
                val = get_val(fid, op, get_hmac(word, cnts[uid][word], 1, key))
                KeyValues.append((addr, val))
        communicate(KeyValues, b"update")



class user:
    def __init__(self, uid:bytes) -> None:
        self.uid = uid

    def register(self, key):
        self.ukey = key

    def search(self, word):
        tlist = []
        cnt = get_Omap(word, self.ukey)
        for i in range(1, cnt+1):
            t = get_hmac(word, i, 0, self.ukey)
            tlist.append(t)
        result = communicate(tlist, b"search")
        return result


# def test():
#     cnts = put_Omap(['hello'], ['word'])
#     print(cnts) 
#     cnt = get_Omap('hello', 'word')
#     print(cnt)

# test()