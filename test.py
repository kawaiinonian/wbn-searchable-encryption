# import ctypes as c
from ctypes import *
# key_type = c.c_uint8 * 32
# d_type = c.c_uint8 * 32
# class test(c.Structure):
#     _fields_ = [
#         ("K1", key_type),
#         ("K2", key_type),
#         ("K3", key_type),
#     ]
# k1_d = b'abc'
# k2_d = b'efg'
# k3_d = b'hij'

# k1 = key_type()
# k2 = key_type()
# k3 = key_type()
# c.memmove(k1, k1_d, 32)
# c.memmove(k2, k2_d, 32)
# c.memmove(k3, k3_d, 32)
# input = test(k1, k2, k3)
# d_d = b'doc'
# d = d_type()
# c.memmove(d, d_d, 32)
# input_map = {}
# output_map = {}
# input_map[c.addressof(d)] = input
# # input_map_type = c.POINTER(c.c_void_p)()
# # input_map_type.contents
# lib = c.cdll.LoadLibrary('./test.so') 
# lib.test_map(input_map, c.byref(output_map))
# for k, v in output_map.items():
#     print(str(k)+":"+str(v))
# key = c.c_uint8 * 3
# class test(c.Structure):
#     _fields_ = [("a", key)]

# string = b'abc'
# a1 = key()
# a2 = key()
# c.memmove(a1, string, 3)
# c.memmove(a2, string, 3)

# t1 = test(a1)
# t2 = test(a2)
# t = [c.pointer(t1), c.pointer(t2)]
# t_list_type = c.POINTER(test) * 2
# t_i = t_list_type(*t)
# out_type = c.c_ubyte * 6
# out = out_type()
# lib = c.cdll.LoadLibrary('./test.so') 
# lib.test_map(t_i, out)
# # for byte in out:
# #     print(byte)
# print(bytes(out))
# LAMBDA = 32
# WORD_LEN = 32
# MAX_WORD = 32
# PATH_LEN = 64
# FILE_DESC_LEN = 1100

# type_key = c_uint8 * LAMBDA
# type_word = c_uint8 * WORD_LEN
# type_words = type_word * MAX_WORD
# type_path = c_uint8 * PATH_LEN
# class FILE_DESC(Structure):
#     _fields_ = [
#         ("words", type_words),
#         ("keywords_len", c_int),
#         ("path", type_path),
#     ]
# l = [b'abc', b'efg']
# a = []

# for i in l:
#     new = type_word()
#     memmove(new, i, len(i))
#     a.append(new)
# b = type_words(*a)
# p = b'abc'
# new_type = c_uint8 * 3
# p_c = new_type()
# memmove(p_c, p, len(p))
# fd = FILE_DESC(b, len(l), p_c)

# from project.shell.client.c_user import *
# from project.shell.utils.method import *
# from project.shell.utils.datatype import *

# usr = c_user('/home/kawaiinonian/project/project/core/libclient.so')
# fd = get_fd([b'a',b'b',b'c'],b'01234567890123456789012345678901')
# sk = SEARCH_KEY(
#     get_key_from_bytes(b'0123456789012345678901234567'),
#     get_key_from_bytes(b'0123456789012345678901234567'),
#     get_key_from_bytes(b'0123456789012345678901234567'),
# )
# uk = USER_KEY(
#     get_key_from_bytes(b'0123456789012345678901234563'),
#     get_key_from_bytes(b'0123456789012345678901234562'),
# )
# uk2 = USER_KEY(
#     get_key_from_bytes(b'0123456789012345678901234565'),
#     get_key_from_bytes(b'0123456789012345678901234564'),
# )
# ub = get_key_from_bytes(b'helloworldhelloworldhelloworld')
# f_aid = get_key_from_bytes(b'helloworldhelloworldhelloworld')
# # ret = usr.updateData_generate(sk, [fd])
# # print(ret)
# # print(len(ret))
# dockey, ret = usr.online_auth(sk, uk, [fd])
# print(ret)
# print(len(ret))
# print(bytes(dockey[0].contents.kd_enc))
# aid, uauth, dockey_out, ret2 = usr.offline_auth(uk, uk2, [fd], ub, 
#     [dockey[0].contents], [], f_aid)
# print(bytes(aid))
# print(bytes(uauth[0].contents.offtok))
# print(bytes(uauth[0].contents.uid))
# print(bytes(dockey_out[0].contents.kd_enc))
# ret3 = usr.search_generate(get_word_from_bytes(b'a'), uk2, [dockey_out[0].contents], [uauth[0].contents])
# print(ret3)

# lib = cdll.LoadLibrary('/home/kawaiinonian/project/project/core/libclient.so') 
# string = b"helloworld"
# input_type = c_ubyte * len(string)
# input = input_type()
# memmove(input, string, len(string))
# lib.test_relic(input, len(string))
