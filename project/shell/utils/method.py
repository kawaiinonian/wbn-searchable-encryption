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