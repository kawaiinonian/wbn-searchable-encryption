#include "const.h"

typedef struct {
    uint8_t **ids;
    uint8_t word[WORD_LEN];
    int len;
}word_file;


typedef struct {
    uint8_t K[LAMBDA],Ks[LAMBDA],Ki[LAMBDA],Kx[LAMBDA],Kz[LAMBDA];
}MK;


typedef struct {
    uint8_t l[LAMBDA], e[PATH_LEN_ENC];
    uint8_t y[LAMBDA]; // to be correct, may not be 256bit
}EDB_ITEM;


typedef struct {
    uint8_t sk1[RSA_GROUP], sk2[RSA_GROUP], sk3[RSA_GROUP]; // to be correct, may not be 256bit
}SKs;