from ctypes import *
from typing import List
from .datatype import *
import secrets

def get_fd(words: List[bytes], path: bytes):
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
    fd = FILE_WITH_WORDS(c_words, len(words), c_path)
    return fd

def get_doc(ds):
    doc_set = []
    for fd in ds:
        d = type_d()
        memmove(d, fd, len(fd))
        doc_set.append(d)
    type_doc = type_d * len(ds)
    doc = type_doc(*doc_set)
    return doc

def get_key_from_bytes(data: bytes):
    if len(data) > LAMBDA:
        raise IndexError
    ret = type_key()
    memmove(ret, data, len(data))
    return ret

def get_element_from_bytes(data: bytes):
    if len(data) > LAMBDA+1:
        raise IndexError
    ret = type_element()
    memmove(ret, data, len(data))
    return ret

def get_d_from_bytes(data: bytes):
    if len(data) > FILE_DESC_LEN:
        raise IndexError
    ret = type_d()
    memmove(ret, data, len(data))
    return ret

def get_word_from_bytes(data: bytes):
    if len(data) > WORD_LEN:
        raise IndexError
    ret = type_word()
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

def get_random_key(length: int):
    return secrets.token_bytes(length)
