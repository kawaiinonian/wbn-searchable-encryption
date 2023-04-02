#include "client.h"

// uint8_t F(uint8_t *key, std::string str);
// uint8_t G(uint8_t *key, std::string str); 

// group_element ? 
// byte ? 
// SecByteBlock for Enc ? 
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::map<uint8_t [2048], DOCKEY_ITEM> DOCKEY_DICT;
typedef std::vector<USET_ITEM> USET_LIST;

void updateData_generate(SEARCH_KEY skey, FILE_DESC_LIST DOC, 
    XSET_LIST &Xset_to_server) {
    int i, j;

    for (i = 0; i < DOC.size(); i++) {
        uint8_t d[FILE_DESC_LEN];
        DOC[i].serialize(d);
        fp_t Kd, Kd_inv;
        F(skey.K1, d, Kd);
        F(skey.K1, d, Kd_inv);
        uint8_t Kd_enc[LAMBDA];
        G(skey.K3, d, Kd_enc);
        for (j = 0; j < DOC[i].keywords_len; j++) {
            XSET_ITEM tmp_item;
            get_xwd(Kd, Kd_inv, tmp_item.xwd);
            get_ywd(Kd_enc, d, tmp_item.ywd);
            Xset_to_server.push_back(tmp_item);
        }
    }
    return;
}


void online_auth(SEARCH_KEY skey, USER_KEY ukey, FILE_DESC_LIST DOC, 
    DOCKEY_DICT &key_to_user, USET_LIST &uset_to_server) {
    
    for (int i = 0; i < DOC.size(); i++) {
        USET_ITEM tmp_uset_item;
        DOCKEY_ITEM tmp_doc_item;
        uint8_t d[FILE_DESC_LEN] = {0};
        DOC[i].serialize(d);
        fp_t Kd_inv;
        F(skey.K1, d, tmp_doc_item.Kd);
        F(skey.K1, d, Kd_inv);
        G(skey.K3, d, tmp_doc_item.Kd_enc);
        fp_t tmp_kdd, tmp_kud, tmp_kud_inv;
        F(ukey.KUT, d, tmp_uset_item.uid);
        F(Kd_inv, d, FILE_DESC_LEN, tmp_kdd);
        F(ukey.KU, d, tmp_kud);
        fp_inv_binar(tmp_kud_inv, tmp_kud);
        fp_mul_comba(tmp_uset_item.ud, tmp_kdd, tmp_kud_inv);
        key_to_user.insert(std::pair<uint8_t[FILE_DESC_LEN], DOCKEY_ITEM>(d, tmp_doc_item));
        uset_to_server.push_back(tmp_uset_item);
    }

    return;
}


void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t* ub, FILE_DESC_LIST DOC, 
    USER_AUTH_DICT User_AuthA, DOCKEY_DICT Doc_KeyA, 
    USER_AUTH_DICT &auth_to_userB, DOCKEY_DICT &key_to_userB,
    ASET_ITEM &tmp_Aset_to_server) {

    F(A_ukey.KUT, ub, tmp_Aset_to_server.aid);
    fp_t tmp_alpha;
    F(A_ukey.KU, ub, tmp_alpha);
    fp_inv_binar(tmp_Aset_to_server.trapgate, tmp_alpha);
    for (int i = 0; i < DOC.size(); i++) {
        uint8_t d[FILE_DESC_LEN] = {0};
        DOC[i].serialize(d);
        if (User_AuthA.find(d) == User_AuthA.end()) {
            
        } else {
            
        }
    }

    return;
}


void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY_DICT Doc_Key,
    USER_AUTH_DICT User_Auth, QUERY_LIST &query_list) {

    
    return;
}

