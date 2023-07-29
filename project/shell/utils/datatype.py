from dataclasses import dataclass
from ctypes import *
import array
# from typing import A
LAMBDA = 32
WORD_LEN = 32
MAX_WORD = 32
PATH_LEN = 16
PATH_LEN_ENC = PATH_LEN + 16
FILE_DESC_LEN = 1100
FILE_DESC_LEN_ENC = 1104

type_key = c_ubyte * LAMBDA
type_element = c_ubyte * (LAMBDA + 1)
type_word = c_ubyte * WORD_LEN
type_words = type_word * MAX_WORD
type_path = c_ubyte * PATH_LEN
type_d = c_ubyte * PATH_LEN
type_d_enc = c_ubyte * PATH_LEN_ENC
p = POINTER(c_ubyte)
pp = POINTER(p)

class SEARCH_KEY(Structure):
    _fields_ = [
        ("k1", type_key),
        ("k2", type_key),
        ("k3", type_key),
    ]

class USER_KEY(Structure):
    _fields_ = [
        ("ku", type_key),
        ("kut", type_key),
    ]

class FILE_WITH_WORDS(Structure):
    _fields_ = [
        ("words", pp),
        ("wordlen", c_int),
        ("d", type_path),
    ]

class DOC_KEY(Structure):
    _fields_ = [
        ("d", type_d),
        ("kd_enc", type_key),
        ("kd", type_key),
    ]

class USER_AUTH(Structure):
    _fields_ = [
        ("d", type_d),
        ("uid", type_key),
        ("offtok", type_element),        
    ]

class Xset_item(Structure):
    _fields_ = [
        ("xwd", type_element),
        ("ywd", type_d_enc),
    ]

class Aset_item:
    def __init__(self, alpha: bytes) -> None:
        self.alpha = alpha
        self.dlist = []

class Aset_c_item(Structure):
    _fields_ = [
        ("aid", type_key),
        ("trapgate", type_key),
    ]

class Uset_item(Structure):
    _fields_ = [
        ("uid", type_key),
        ("ud", type_key),
    ]

class Token(Structure):
    _fields_ = [
        ("uid", type_key),
        ("stk", type_element),
    ]