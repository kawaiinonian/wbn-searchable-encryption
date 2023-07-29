from ctypes import *
from typing import List

import os
import sys
sys.path.append(os.getcwd() + "/tdsc22/shell/")
from datatype import *
from shell.datatype import *
from shell.method import *
from copy import deepcopy

class c_user:
    def __init__(self, sopath) -> None:
        self.lib = cdll.LoadLibrary(sopath)
        self.lib.setting_init()

    def update(self, mk: MK, files: List[WORD_FILE]):
        files_ptr = [pointer(i) for i in files]
        files_input_type = POINTER(WORD_FILE) * len(files)
        files_input = files_input_type(*files_ptr)
        item_num = 0
        for f in files:
            item_num += f.len
        edb_type = EDB_ITEM * item_num
        edb = edb_type()
        xset_type = type_group * item_num
        xset = xset_type()
        self.lib.update(mk, files_input, len(files), edb, xset)
        # print("func complete")
        return edb, xset
    
    def auth(self, authwords: List[type_word]):
        words_ptr = [pointer(i) for i in authwords]
        words_input_type = POINTER(type_word) * len(authwords)
        words_input = words_input_type(*words_ptr)

        sk_alloc = SK()
        sk_ptr = pointer(sk_alloc)
        self.lib.auth(words_input, len(authwords), sk_ptr)
        return sk_ptr
    
    def get_stag(self, mk, query_words: list, wordset: set, sks: POINTER(SK)):
        wordset_copy = []
        for word in wordset:
            if word != query_words[0]:
                wordset_copy.append(word)
        # wordset_copy = list(wordset_copy.discard(query_words[0]))
        word4stag = [get_word_from_bytes(i) for i in wordset_copy]
        words_ptr = [pointer(i) for i in word4stag]
        words_input_type = POINTER(type_word) * len(word4stag)
        words_input = words_input_type(*words_ptr)

        stag = pointer(type_key())
        self.lib.get_stag(mk, words_input, len(words_ptr), sks, stag)
        return stag
    
    def get_index(self, sks: SK, query_words: list, wordset: set, mk):
        wordset_copy = []
        for word in wordset:
            if word != query_words[0]:
                wordset_copy.append(word)
        # word4index1 = wordset_copy.discard(query_words[0])
        word4index1 = [get_word_from_bytes(i) for i in wordset_copy]
        words_ptr = [pointer(i) for i in word4index1]
        words_input_type = POINTER(type_word) * len(word4index1)
        words_input = words_input_type(*words_ptr)
        index1 = pointer(type_rsa())
        self.lib.get_index1(sks, words_input, len(words_ptr), mk, index1)

        index2 = []
        for word in query_words[1:]:
            wordset_copy = []
            for w in wordset:
                if w != word:
                    wordset_copy.append(w)
            word4index2 = [get_word_from_bytes(i) for i in wordset_copy]
            words_ptr = [pointer(i) for i in word4index2]
            words_input_type = POINTER(type_word) * len(word4index2)
            words_input = words_input_type(*words_ptr)
            one_index = pointer(type_key())
            self.lib.get_index2(sks, words_input, len(words_input), mk, one_index)
            index2.append(one_index)
        index2_type = POINTER(type_key) * len(word4index2)
        index2 = index2_type(*index2)
        return index1, index2
    
    # def token_generate(self, sks: SK, query_words: List[type_word], mk, round):
    #     words_ptr = [pointer(i) for i in query_words]
    #     words_input_type = POINTER(type_word) * len(query_words)
    #     words_input = words_input_type(*words_ptr)

    #     token_alloc = [pointer(type_group()) for _ in range(len(query_words) - 1)]
    #     tokens_type = POINTER(type_group) * (len(query_words)-1)
    #     tokens = tokens_type(*token_alloc)
    #     self.lib.token_generate(sks, words_input, len(query_words), round, mk, tokens)
    #     return tokens
    def token_generate(self, mk, round, index1, index2, num):
        token_alloc = [pointer(type_group()) for _ in range(num-1)]
        tokens_type = POINTER(type_group) * (num-1)
        tokens = tokens_type(*token_alloc)
        self.lib.token_generate(round, index1, index2, num, mk, tokens)
        return tokens
    
# sopath = '/root/project515/tdsc22/core/libclient.so'
# usr = c_user(sopath)