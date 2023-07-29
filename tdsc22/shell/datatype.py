from ctypes import *

LAMBDA = 32
PATH_LEN = 64
PATH_LEN_ENC = PATH_LEN + 16
WORD_LEN = 32
RSA_GROUP = 2048//8

type_word = c_ubyte * WORD_LEN
type_key = c_ubyte * LAMBDA
type_id_enc = c_ubyte * PATH_LEN_ENC
type_id = c_ubyte * PATH_LEN
type_rsa = c_ubyte * RSA_GROUP
type_group = c_ubyte * (LAMBDA+1)
p = POINTER(type_id)
pp = POINTER(p)

class WORD_FILE(Structure):
    _fields_ = [
        ("ids", pp),
        ("word", type_word),
        ("len", c_int),
    ]

class EDB_ITEM(Structure):
    _fields_ = [
        ("l", type_key),
        ("e", type_id_enc),
        ("y", type_key),
    ]

class SK(Structure):
    _fields_ = [
        ("sk1", type_rsa),
        ("sk2", type_rsa),
        ("sk3", type_rsa),
    ]

class MK(Structure):
    _fields_ = [
        ("K", type_key),
        ("Ks", type_key),
        ("Ki", type_key),
        ("Kx", type_key),
        ("Kz", type_key),
    ]
