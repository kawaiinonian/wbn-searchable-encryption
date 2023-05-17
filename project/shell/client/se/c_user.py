import ctypes as c
from typing import List

from se.datatype import *
from se.method import *

class c_user:
    def __init__(self, sopath:str) -> None:
        self.lib = c.cdll.LoadLibrary(sopath)
        self.lib.setting_init()

    def updateData_generate(self, skey: SEARCH_KEY, files: List[FILE_WITH_WORDS]):
        files_ptr = [pointer(i) for i in files]
        # print(files[0].wordlen)
        files_input_type = POINTER(FILE_WITH_WORDS) * len(files)
        files_input = files_input_type(*files_ptr)
        word_num = 0
        for f in files:
            word_num += f.wordlen
        xset_type = Xset_item * word_num
        xset = xset_type()
        # print("we will product %d xset item"%(word_num))
        self.lib.updateData_generate(skey, files_input, len(files), xset)
        return xset, word_num

    def online_auth(self, skey: SEARCH_KEY, ukey: USER_KEY, doc_set: List[str]):
        doc = get_doc(doc_set)
        ret_dockey_type = DOC_KEY * len(doc_set)
        ret_dockey = ret_dockey_type()
        ret_uset_type = Uset_item * len(doc_set)
        ret_uset = ret_uset_type()
        self.lib.online_auth(skey, ukey, doc, len(doc_set), ret_dockey, ret_uset)
        return ret_dockey, ret_uset


    def offline_auth(
        self, aukey: USER_KEY, bukey: USER_KEY, doc_set: List[str], ub: type_key,
        DOCKEY_LIST: List[DOC_KEY], USERAUTH_LIST: List[USER_AUTH],
    ):
        doc = get_doc(doc_set)
        input_dockey_type = DOC_KEY * len(DOCKEY_LIST)
        input_dockey = input_dockey_type(*DOCKEY_LIST)
        input_userauth_type = USER_AUTH * len(USERAUTH_LIST)
        input_userauth = input_userauth_type(*USERAUTH_LIST)
        ret_dockey_type = DOC_KEY * len(doc_set)
        ret_dockey = ret_dockey_type()
        ret_userauth_type = USER_AUTH * len(doc_set)
        ret_userauth = ret_userauth_type()
        # ret_aset_type = (Aset_c_item)
        ret_aset = pointer(Aset_c_item())
        self.lib.offline_auth(aukey, bukey, ub, doc, len(doc_set),
            input_userauth, len(USERAUTH_LIST), input_dockey, 
            len(DOCKEY_LIST), ret_aset, ret_userauth, ret_dockey)
        return ret_aset, ret_userauth, ret_dockey


    def search_generate(
        self, word: type_word, ukey: USER_KEY, DOCKEY_LIST: List[DOC_KEY], 
        USERAUTH_LIST: List[USER_AUTH]
    ):
        input_dockey_type = DOC_KEY * len(DOCKEY_LIST)
        input_dockey = input_dockey_type(*DOCKEY_LIST)
        input_userauth_type = USER_AUTH * len(USERAUTH_LIST)
        input_userauth = input_userauth_type(*USERAUTH_LIST)
        ret_token_type = Token * len(DOCKEY_LIST)
        ret_token = ret_token_type()
        self.lib.search_generate(word, ukey, input_dockey, len(DOCKEY_LIST),
            input_userauth, len(USERAUTH_LIST), ret_token)
        return ret_token
    
    def gen_key(self):
        return get_random_key(LAMBDA)
