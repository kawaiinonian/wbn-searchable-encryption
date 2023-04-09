from ctypes import *
from typing import List
from datatype import *

def get_fd(words: List[str], path: str):
    if len(words) > MAX_WORD:
        raise IndexError
    _words = []
    for word in words:
        new_word = type_word()
        memmove(new_word, word, len(word))
        _words.append(new_word)
    c_words = type_words(*_words)
    c_path = type_path()
    memmove(c_path, path, len(path))
    fd = FILE_DESC(c_words, len(words), c_path)
    return fd

def get_key_from_bytes(data: bytes):
    if len(data) > LAMBDA:
        raise IndexError
    ret = type_key()
    memmove(ret, data, len(data))
    return ret

def get_d_from_bytes(data: bytes):
    if len(data) > FILE_DESC_LEN:
        raise IndexError
    ret = type_d()
    memmove(ret, data, len(data))
    return ret

# def get_dockey(d: bytes, kd_enc: bytes, kd: bytes):
#     if len(kd) != len(kd_enc) or len(kd) != LAMBDA or len(d) != FILE_DESC_LEN:
#         raise IndexError

#     return DOC_KEY(
#         get_d_from_bytes(d), 
#         get_key_from_bytes(kd_enc),
#         get_key_from_bytes(kd)
#     )

def get_query_from_bytes(data: bytes):
    pass