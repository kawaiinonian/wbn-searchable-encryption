#ifndef _HEAD_INC_
#include "../include/include.h"
#endif

#include "../lib/method.h"

extern "C" {
    void updateData_generate(SEARCH_KEY skey, file *fd[], int len, XSET_ITEM *xset);
    void online_auth(SEARCH_KEY skey, USER_KEY ukey, uint8_t doc[][PATH_LEN], int doc_len, 
        DOCKEY *dockey, USET_ITEM *uset);
    void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t ub[], 
        uint8_t doc[][PATH_LEN], int doc_len, USER_AUTH authas[], int auth_len, 
        DOCKEY Dockey[], int dockey_len, ASET_ITEM *aset, USER_AUTH auth2b[], 
        DOCKEY dockey2b[]);
    void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY dkey[], int doc_len,
        USER_AUTH usr_au[], int auth_len, TOKEN tk[]);
}