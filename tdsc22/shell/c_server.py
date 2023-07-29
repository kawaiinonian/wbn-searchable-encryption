from ctypes import *
from typing import List

import os
import sys
sys.path.append(os.getcwd() + "/tdsc22/shell/")
from datatype import *
from method import *

class c_server:
    def __init__(self, sopath) -> None:
        self.lib = cdll.LoadLibrary(sopath)
        self.lib.setting_init()

    def get_hash(self, stag, c):
        l = pointer(type_key())
        self.lib.get_hash(stag, c, l)
        return bytes(l.contents)
    
    def get_exp(self, base, index):
        result = pointer(type_group())
        self.lib.get_exp(base, index, result)
        return bytes(result.contents)
    
    def search(self, tokens: List[type_group], stag, c, edb:dict, xset:list):
        l = self.get_hash(stag, c)
        if l not in edb.keys():
            return b"stop"
        (e, y) = edb[l]
        flag = True

        y = get_key_from_bytes(y)
        for t in tokens:
            base = get_element_from_bytes(t)
            tmp = self.get_exp(base, y)
            if tmp not in xset:
                flag = False
                break
        return e if flag else b""
