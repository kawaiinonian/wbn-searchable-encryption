#include "client.h"

#ifdef DEBUG
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::map<uint8_t*, DOCKEY_ITEM> DOCKEY_DICT;
typedef std::vector<USET_ITEM> USET_LIST;
typedef std::map<uint8_t*, USER_AUTH_ITEM> USER_AUTH_DICT;
typedef std::vector<QUERY_ITEM> QUERY_LIST;
#endif

void updateData_generate(SEARCH_KEY skey, FILE_DESC_LIST DOC, 
    XSET_LIST &Xset_to_server) {
    int i, j;

    for (i = 0; i < DOC.size(); i++) {
        uint8_t d[FILE_DESC_LEN] = {0};
        DOC[i].serialize(d);
        fp_t Kd, Kd_inv;
        F(skey.K1, d, Kd);
        F(skey.K1, d, Kd_inv);
        uint8_t Kd_enc[LAMBDA];
        G(skey.K3, d, Kd_enc);
        for (j = 0; j < DOC[i].keywords_len; j++) {
            XSET_ITEM tmp_item;
            get_xwd(Kd, Kd_inv, d, DOC[i].words[j], tmp_item.xwd);
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
        uint8_t* d = new uint8_t[FILE_DESC_LEN];
        memset(d, 0, sizeof(d));
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
        key_to_user.insert(std::make_pair(d, tmp_doc_item));
        uset_to_server.push_back(tmp_uset_item);
    }

    return;
}


void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t* ub, FILE_DESC_LIST DOC, 
    USER_AUTH_DICT User_AuthA, DOCKEY_DICT Doc_KeyA, fp_t f_aid, fp_t &n_aid,
    USER_AUTH_DICT &auth_to_userB, DOCKEY_DICT &key_to_userB,
    ASET_ITEM &tmp_Aset_to_server) {

    F(A_ukey.KUT, ub, tmp_Aset_to_server.aid);
    fp_t tmp_alpha;
    F(A_ukey.KU, ub, tmp_alpha);
    fp_inv_binar(tmp_Aset_to_server.trapgate, tmp_alpha);
    memcpy(tmp_Aset_to_server.f_aid, f_aid, sizeof(f_aid));
    for (int i = 0; i < DOC.size(); i++) {
        uint8_t *d = new uint8_t[FILE_DESC_LEN];
        memset(d, 0, sizeof(d));
        USER_AUTH_ITEM tmp_user_auth;
        DOC[i].serialize(d);
        fp_t tmp_tok;
        if (User_AuthA.find(d) == User_AuthA.end()) {
            F(A_ukey.KUT, d, tmp_user_auth.uid);
            fp_t tmp_kuad, tmp_kuau, g, tmp;
            F(A_ukey.KU, d, tmp_kuad);
            F(A_ukey.KU, ub, LAMBDA, tmp_kuau);
            fp_read_bin(g, g_init, LAMBDA);
            fp_mul_comba(tmp, g, tmp_kuad);
            fp_mul_comba(tmp_user_auth.offtok, tmp, tmp_kuau);
        } else {
            fp_t tmp_kuau;
            F(A_ukey.KU, ub, LAMBDA, tmp_kuau);
            fp_mul_comba(tmp_user_auth.offtok, User_AuthA.find(d)->second.offtok, tmp_kuau);
            memcpy(tmp_user_auth.uid, User_AuthA.find(d)->second.uid, sizeof(fp_t));
        }
        F(A_ukey.KUT, ub, LAMBDA, n_aid);
        auth_to_userB.insert(std::make_pair(d, tmp_user_auth));
        key_to_userB.insert(std::make_pair(d, Doc_KeyA.find(d)->second));
    }
    return;
}


void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY_DICT Doc_Key,
    USER_AUTH_DICT User_Auth, QUERY_LIST &query_list) {

    DOCKEY_DICT::iterator iter;
    iter = Doc_Key.begin();
    while (iter != Doc_Key.end()) {
        QUERY_ITEM tmp_q;
        if (User_Auth.find(iter->first) == User_Auth.end()) {
            fp_t g, tmp_kdw, tmp_kud, tmp;
            F(ukey.KUT, iter->first, tmp_q.uid);
            fp_read_bin(g, g_init, LAMBDA);
            F(iter->second.Kd, word, WORD_LEN, tmp_kdw);
            F(ukey.KU, iter->first, tmp_kud);
            fp_mul_comba(tmp, tmp_kdw, tmp_kud);
            fp_mul_comba(tmp_q.stk_d, tmp, g);
        } else {
            memcpy(tmp_q.uid, User_Auth.find(iter->first)->second.uid, LAMBDA);
            fp_t tmp_kdw;
            F(iter->second.Kd, word, WORD_LEN, tmp_kdw);
            fp_mul_comba(tmp_q.stk_d, tmp_kdw, User_Auth.find(iter->first)->second.offtok);
        }
        query_list.push_back(tmp_q);
        iter++;
    }
    
    return;
}

