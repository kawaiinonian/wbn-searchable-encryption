#ifndef _HEAD_INC_
#include "../include/include.h"
#endif


extern "C" {
    void update(MK master_key, word_file* db[], int word_num, EDB_ITEM *edb, uint8_t xset[][LAMBDA+1]);
    void token_generate(int round, uint8_t *index1, uint8_t *index2[], int len, MK master_key, uint8_t *token_term[]);
    void get_index1(SKs sk, uint8_t *query_words[], int len, MK master_key, uint8_t *index1);
    void get_index2(SKs sk, uint8_t *query_words[], int len, MK master_key, uint8_t *index2);
    void get_stag(MK master_key, uint8_t *query_words[], int len, SKs *sk, uint8_t stag[]);
    void auth(uint8_t *authwords[], int len, SKs *sk);
}