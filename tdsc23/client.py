import secrets


def get_random_key(length: int):
    return secrets.token_bytes(length)

LAMBDA = 256//8

def encrypt(word, cnt, key):
    pass

def hmac(word, cnt, ptr, key):
    pass

def get_val(fid, op, hash):
    pass

class owner:
    def __init__(self, type:str) -> None:
        self.DictW = dict()
        self.UserKeys = dict()
        self.AccessList = dict()
        if type == 'Q':
            self.type = 'queue'
            self.FileCnts = dict()
            self.Queues = dict()
        else:
            self.type = 'omap'
            self.Omap = dict()

    def enroll(self, uid: bytes):
        if self.type == 'omap':
            ukey = get_random_key(LAMBDA)
            self.UserKeys[uid] = ukey
            return ukey
        else:
            ukey = get_random_key(LAMBDA)
            ukey_inv = get_random_key(LAMBDA)
            self.UserKeys[uid] = (ukey, ukey_inv)
            return (ukey, ukey_inv)
    
    def share(self, uid, fid):
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        self.AccessList[fid].append(uid)
        key = self.UserKeys[uid]
        word_set = self.doc[fid]
        KeyValues = []
        if self.type == 'queue':
            CntDiffs = []
            for word in word_set:
                if word not in self.FileCnts[uid].keys():
                    self.FileCnts[uid][word] = 0
                self.FileCnts[uid][word] += 1
                cnt = self.FileCnts[uid][word]
                CntDiffs.append((uid, encrypt(word, cnt, key[1])))
                addr = hmac(word, cnt, 0, key[0])
                val = get_val(fid, 'add', hmac(word, cnt, 1, key[0]))
                KeyValues.append((addr, val))
            return KeyValues, CntDiffs, uid, fid


        if self.type == 'omap':
            for word in word_set:
                if word not in self.Omap[uid].keys():
                    self.Omap[uid][word] = 0
                self.Omap[uid][word] += 1
                cnt = self.Omap[uid][word]
                addr = hmac(word, cnt, 0, key)
                val = get_val(fid, 'add', hmac(word, cnt, 1, key))
                KeyValues.append((addr, val))
            return KeyValues, uid, fid

    def update(self, fid, op, wlist):
        if fid not in self.AccessList.keys():
            self.AccessList[fid] = []
        if self.type == 'queue':
            CntDiffs = []
        KeyValues = []
        for uid in self.AccessList[fid]:
            key = self.UserKeys[uid]
            if self.type == 'queue':
                for word in wlist:
                    if word not in self.FileCnts[uid].keys():
                        self.FileCnts[uid][word] = 0
                    self.FileCnts[uid][word] += 1
                    cnt = self.FileCnts[uid][word]
                    CntDiffs.append((uid, encrypt(word, cnt, key[1])))
                    addr = hmac(word, cnt, 0, key[0])
                    val = get_val(fid, op, hmac(word, cnt, 1, key[0]))
                    KeyValues.append((addr, val))
            
            if self.type == 'omap':
                for word in wlist:
                    if word not in self.Omap[uid].keys():
                        self.Omap[uid][word] = 0
                    self.Omap[uid][word] += 1
                    cnt = self.Omap[uid][word]
                    addr = hmac(word, cnt, 0, key)
                    val = get_val(fid, op, hmac(word, cnt, 1, key))
                    KeyValues.append((addr, val))

        if self.type == 'omap':
            return KeyValues
        else:
            return KeyValues, CntDiffs


class user:
    def __init__(self, type:str, uid:bytes) -> None:
        if type == 'Q':
            self.type = 'queue'
        else:
            self.type = 'omap'
            self.FileCnts = dict()
        self.uid = uid

    def register(self, key):
        self.ukey = key

    def search(self, word):
        tlist = []