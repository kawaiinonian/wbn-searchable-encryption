#include "client.h"

KEY F(KEY key, std::string str);
KEY G(KEY key, std::string str); 

// group_element ? 
// byte ? 
// SecByteBlock for Enc ? 

void updateData_generate(SEARCH_KEY skey, FILE_DESC_LIST DOC, 
    XSET_LIST &Xset_to_server) {
    int i, j;
    XSET_LIST tmp_set;

    for (i = 0; i < DOC.size(); i++) {
        KEY Kd = F(skey.K1, DOC[i].dec_flag);
        KEY Kd_inv = F(skey.K1, DOC[i].dec_flag);
        KEY Kd_enc = G(skey.K1, DOC[i].dec_flag);
        for (j = 0; j < DOC[i].words.size(); j++) {
            XSET_ITEM tmp_item;
            // Group
            // Encrypt
            tmp_set.push_back(tmp_item);
        }
    }

    std::random_shuffle(tmp_set.begin(), tmp_set.end());
    Xset_to_server = tmp_set;

    return;
}


void online_auth(SEARCH_KEY skey, USER_KEY ukey, FILE_DESC_LIST DOC, 
    DOCKEY_LIST &key_to_user, USET_DICT &uset_to_server) {
    

    return;
}


void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, FILE_DESC_LIST DOC, 
    USER_AUTH_DICT User_AuthA, DOCKEY_LIST Doc_KeyA, 
    USER_AUTH_DICT &auth_to_userB, DOCKEY_LIST &key_to_userB,
    ASET_ITEM &tmp_Aset_to_server) {


    return;
}


void search_generate(keyword word, USER_KEY ukey, DOCKEY_LIST Doc_Key,
    USER_AUTH_DICT User_Auth, QUERY_LIST &query_list) {

    
    return;
}

