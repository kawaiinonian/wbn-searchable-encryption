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
        buffer_type = c_uint8 * self.MAX_UPDATE * FILE_DESC_LEN
        _ret = buffer_type()
        self.lib.update_interface(skey, doc_input, len(DOC), _ret)
        ret = bytes(_ret)
        return ret

