import ctypes as c
from typing import List

from ..utils.datatype import *
class c_user:
    MAX_UPDATE = 512
    def __init__(self, sopath:str) -> None:
        self.lib = c.cdll.LoadLibrary(sopath)

    def updateData_generate(self, skey: SEARCH_KEY, DOC: List[FILE_DESC]):
        doc_ptr = [pointer(i) for i in DOC]
        doc_input_type = POINTER(FILE_DESC) * self.MAX_UPDATE
        doc_input = doc_input_type(*doc_ptr)
        buffer_type = c_ubyte * self.MAX_UPDATE * FILE_DESC_LEN
        _ret = buffer_type()
        self.lib.update_interface(skey, doc_input, len(DOC), _ret)
        ret = bytes(_ret)
        return ret

    def online_auth(self, skey: SEARCH_KEY, ukey: USER_KEY, DOC: List[FILE_DESC]):
        doc_ptr = [pointer(i) for i in DOC]
        doc_input_type = POINTER(FILE_DESC) * self.MAX_UPDATE
        doc_input = doc_input_type(*doc_ptr)
        buffer_type1 = c_ubyte * (FILE_DESC_LEN + 2*LAMBDA) * len(DOC)
        buffer_type2 = c_ubyte * 2*LAMBDA * len(DOC)
        buf1 = buffer_type1()
        buf2 = buffer_type2()
        self.lib.online_auth_interface(skey, ukey, doc_input, len(DOC), buf1, buf2)
        return bytes(buf1), bytes(buf2)

    def offline_auth(self):