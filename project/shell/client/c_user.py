import ctypes as c
from typing import List

from ..utils.datatype import *
class c_user:
    MAX_UPDATE = 512
    MAX_AUTH = 512
    def __init__(self, sopath:str) -> None:
        self.lib = c.cdll.LoadLibrary(sopath)
        self.lib.setting_init()

    def updateData_generate(self, skey: SEARCH_KEY, DOC: List[FILE_DESC]):
        doc_ptr = [pointer(i) for i in DOC]
        doc_input_type = POINTER(FILE_DESC) * len(DOC)
        doc_input = doc_input_type(*doc_ptr)
        buffer_type = c_ubyte * len(DOC) * 2 * LAMBDA
        _ret = buffer_type()
        self.lib.update_interface(skey, doc_input, len(DOC), _ret)
        ret = bytes(_ret)
        return ret

    def online_auth(self, skey: SEARCH_KEY, ukey: USER_KEY, DOC: List[FILE_DESC]):
        doc_ptr = [pointer(i) for i in DOC]
        doc_input_type = POINTER(FILE_DESC) * len(DOC)
        doc_input = doc_input_type(*doc_ptr)
        # buffer_type1 = c_ubyte * (FILE_DESC_LEN + 2*LAMBDA) * len(DOC)
        buffer_type = c_ubyte * 2*LAMBDA * len(DOC)
        # buf1 = buffer_type1()
        dockey_buf_type = POINTER(DOC_KEY) * len(DOC)
        tmp = [pointer(DOC_KEY()) for _ in range(len(DOC))]
        dockey_buf = dockey_buf_type(*tmp)

        buf = buffer_type()
        self.lib.online_auth_interface(skey, ukey, doc_input, len(DOC), dockey_buf, buf)
        return dockey_buf, bytes(buf)

    def offline_auth(
        self, aukey: USER_KEY, bukey: USER_KEY, DOC: List[FILE_DESC], ub: type_key,
        DOCKEY_LIST: List[DOC_KEY], USERAUTH_LIST: List[USER_AUTH], f_aid: type_key,
    ):
        doc_ptr = [pointer(i) for i in DOC]
        doc_input_type = POINTER(FILE_DESC) * len(DOC)
        doc_input = doc_input_type(*doc_ptr)

        dockey_type = POINTER(DOC_KEY) * len(DOC)
        doc_tmp = [pointer(DOC_KEY()) for _ in range(len(DOC))]
        dockey_out = dockey_type(*doc_tmp)

        dockey_type_in = POINTER(DOC_KEY) * len(DOCKEY_LIST)
        dockey_in_ptr = [pointer(i) for i in DOCKEY_LIST]
        dockey_in = dockey_type_in(*dockey_in_ptr)

        user_auth_type = POINTER(USER_AUTH) * len(DOC)
        user_auth_tmp = [pointer(USER_AUTH()) for _ in range(len(DOC))]
        user_authb = user_auth_type(*user_auth_tmp)

        user_auth_type_in = POINTER(USER_AUTH) * len(USERAUTH_LIST)
        user_autha_ptr = [pointer(i) for i in USERAUTH_LIST]
        user_autha = user_auth_type_in(*user_autha_ptr)

        buffer_type = c_ubyte * 3 * LAMBDA
        buf = buffer_type()
        n_aid = type_key()
        self.lib.offline_auth_interface(aukey, bukey, ub, doc_input, len(DOC), user_autha,
            len(USERAUTH_LIST), dockey_in, f_aid, n_aid, user_authb, dockey_out, buf)
        
        return n_aid, user_authb, dockey_out, buf

    def search_generate(
        self, word: type_word, ukey: USER_KEY, DOCKEY_LIST: List[DOC_KEY], 
        USERAUTH_LIST: List[USER_AUTH]
    ):
        dockey_type = POINTER(DOC_KEY) * len(DOCKEY_LIST)
        dockey_ptr = [pointer(i) for i in DOCKEY_LIST]
        dockey = dockey_type(*dockey_ptr)
        user_auth_type = POINTER(USER_AUTH) * len(USERAUTH_LIST)
        user_auth_ptr = [pointer(i) for i in USERAUTH_LIST]
        user_auth = user_auth_type(*user_auth_ptr)
        buf_type = c_ubyte * 2 * LAMBDA * len(DOCKEY_LIST)
        buf = buf_type()
        self.lib.search_interface(word, ukey, dockey, len(DOCKEY_LIST), user_auth, buf)
        return bytes(buf)
