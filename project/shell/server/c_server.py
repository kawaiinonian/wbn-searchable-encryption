import ctypes as c
from typing import List, Union, Dict, Tuple

from datatype import *
from method import *

class c_server:
    def __init__(self, sopath) -> None:
        self.lib = c.cdll.LoadLibrary(sopath)
        self.lib.setting_init()

    def Aset_update(self, Aset: Dict[bytes, Aset_item], aid: bytes, alpha: bytes, aidA):
        if aid not in Aset.keys():
            Aset[aid] = Aset_item(alpha)
        if aidA is not None:
            Aset[aidA].dlist.append(aid)
            Aset[aid].alpha = self.multi(Aset[aidA].alpha, Aset[aid].alpha)

    def multi(self, key1: bytes, key2: bytes)-> bytes:
        bkey1 = get_key_from_bytes(key1)
        bkey2 = get_key_from_bytes(key2)
        buf_type = c_ubyte * LAMBDA
        buf = buf_type()
        self.lib.get_multi(bkey1, bkey2, buf)
        return bytes(buf)

    def power(self, key1: bytes, key2:bytes)->bytes:
        bkey1 = get_element_from_bytes(key1)
        bkey2 = get_key_from_bytes(key2)
        buf = type_element()
        self.lib.get_exp(bkey1, bkey2, buf)
        return bytes(buf)
        
    def search(self, token: List[Tuple[bytes, bytes]], aid, Uset: Dict[bytes, bytes], \
        Aset: Dict[bytes, Aset_item], Xset: Dict[bytes, bytes]):

        ret = []
        for i, t in enumerate(token):
            if t[0] in Uset.keys():
                x = self.power(t[1], Uset[t[0]])
            else:
                continue
            if x in Xset.keys():
                ret.append((i, Xset[x]))
            elif aid is not None and aid in Aset.keys():
                x = self.power(x, Aset[aid].alpha)
                if x in Xset.keys():
                    ret.append((i, Xset[x]))

        return ret