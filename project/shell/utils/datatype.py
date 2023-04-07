from dataclasses import dataclass
from ctypes import *
import array
# from typing import A
LAMBDA = 32
WORD_LEN = 32
MAX_WORD = 32
PATH_LEN = 64
FILE_DESC_LEN = 1100

type_key = c_uint8 * LAMBDA
type_word = c_uint8 * WORD_LEN
type_words = type_word * MAX_WORD
type_path = c_uint8 * PATH_LEN

class SEARCH_KEY(Structure):
    _fields_ = [
        ("k1", type_key),
        ("k2", type_key),
        ("k3", type_key),
    ]


class FILE_DESC(Structure):
    _fields_ = [
        ("words", type_words),
        ("keywords_len", c_int),
        ("path", type_path),
    ]