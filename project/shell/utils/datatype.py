from dataclasses import dataclass
from ctypes import *
import array
# from typing import A
LAMBDA = 32
WORD_LEN = 32
MAX_WORD = 32
PATH_LEN = 64
FILE_DESC_LEN = 1100
FILE_DESC_LEN_ENC = 1104

type_key = c_ubyte * LAMBDA
type_word = c_ubyte * WORD_LEN
type_words = type_word * MAX_WORD
type_path = c_ubyte * PATH_LEN
type_d = c_ubyte * FILE_DESC_LEN

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


class FILE_DESC(Structure):
    _fields_ = [
        ("words", type_words),
        ("keywords_len", c_int),
        ("path", type_path),
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
        ("offtok", type_key),        
    ]


class Aset_item:
    def __init__(self, alpha: bytes) -> None:
        self.alpha = alpha
        self.dlist = []