from ctypes import *
import secrets

import os
import sys
sys.path.append(os.getcwd() + "/tdsc22/shell/")
from datatype import *

def get_key_from_bytes(data: bytes):
    if len(data) > LAMBDA:
        raise IndexError
    ret = type_key()
    memmove(ret, data, len(data))
    return ret

def get_random_key(length: int):
    return secrets.token_bytes(length)

def get_word_from_bytes(data: bytes):
    if len(data) > WORD_LEN:
        raise IndexError
    ret = type_word()
    memmove(ret, data, len(data))
    return ret

def get_element_from_bytes(data: bytes):
    if len(data) > LAMBDA+1:
        raise IndexError
    ret = type_group()
    memmove(ret, data, len(data))
    return ret
