#include "client.h"

// #ifdef DEBUG
// #include <fstream>
// typedef std::vector<XSET_ITEM> XSET_LIST;
// typedef std::map<uint8_t*, DOCKEY_ITEM> DOCKEY_DICT;
// typedef std::vector<USET_ITEM> USET_LIST;
// typedef std::map<uint8_t*, USER_AUTH_ITEM> USER_AUTH_DICT;
// typedef std::vector<QUERY_ITEM> QUERY_LIST;
// typedef std::vector<FILE_DESC> FILE_DESC_LIST;
// const char* filename = "/home/kawaiinonian/project/debug";
// const uint8_t n[1] = {'\n'};
// void debug(const uint8_t* d, int len) {
//   std::ofstream outfile;
//   outfile.open(filename, std::ios_base::app | std::ios_base::binary);
//   for (int i = 0; i < len; ++i) {
//     outfile << static_cast<int>(d[i]);
//   }
//   outfile << '\n';
//   outfile.close();
// }

// void _get_xwd(const fp_t kd, const fp_t kd_inv, uint8_t *d, uint8_t *w, fp_t result) {
//     fp_t a, b, c, g;
//     uint8_t dbg1[LAMBDA] = {0}, dbg2[LAMBDA] = {0};
//     fp_read_bin(g, g_init, LAMBDA);
//     F(kd_inv, d, FILE_DESC_LEN, a);
//     F(kd, w, WORD_LEN, b);
//     fp_write_bin(dbg1, LAMBDA, a);
//     fp_write_bin(dbg2, LAMBDA, b);
//     debug(dbg1, LAMBDA);
//     debug(dbg2, LAMBDA);
//     fp_mul_comba(c, a, b);
//     fp_mul_comba(result, g, c);
// }
// #endif

void F(const uint8_t* key, const uint8_t* msg, int msg_len, fp_t result) {
    uint8_t tmp[LAMBDA] = {0};
    md_hmac(tmp, msg, msg_len, key, LAMBDA);
    fp_read_bin(result, tmp, LAMBDA);
}

void F(const fp_t key, uint8_t* msg, int msg_len, fp_t result) {
    uint8_t tmp[LAMBDA] = {0};
    uint8_t k_in_b[LAMBDA] = {0};
    fp_write_bin(k_in_b, LAMBDA, key);
    md_hmac(tmp, msg, msg_len, k_in_b, LAMBDA);
    fp_read_bin(result, tmp, LAMBDA);
}

void get_xwd(const fp_t kd, const fp_t kd_inv, uint8_t *d, uint8_t *w, fp_t result) {
    fp_t a, b, c, g;
    bn_t c_bn;
    fp_read_bin(g, g_init, LAMBDA);
    F(kd_inv, d, PATH_LEN, a);
    F(kd, w, WORD_LEN, b);
    fp_mul_comba(c, a, b);
    fp_prime_back(c_bn, c);
    fp_exp_monty(result, g, c_bn);
}

void updateData_generate(SEARCH_KEY skey, file *fd[], int len,
    XSET_ITEM *xset) {
    int k = 0;
    for (int i = 0; i < len; i++) {
        // printf("calculate keys\n");
        fp_t kd, kd_inv;
        F(skey.K1, fd[i]->d, PATH_LEN, kd);
        F(skey.K2, fd[i]->d, PATH_LEN, kd_inv);
        uint8_t kd_enc[LAMBDA];
        G(skey.K3, fd[i]->d, kd_enc);
        // printf("calculate xset\n");
        // printf("going to calculate %d xset_item\n", fd[i]->wordlen);
        for (int j = 0; j < fd[i]->wordlen; j++) {
            XSET_ITEM tmp;
            fp_t xwd;
            // printf("calculate xwd\n");
            get_xwd(kd, kd_inv, fd[i]->d, fd[i]->words[j], xwd);
            fp_write_bin(tmp.xwd, LAMBDA, xwd);
            // printf("calculate ywd\n");
            get_ywd(kd_enc, fd[i]->d, tmp.ywd);
            xset[k] = tmp;
            k++;
        }
    }
}

void online_auth(SEARCH_KEY skey, USER_KEY ukey, uint8_t doc[][PATH_LEN],
    int doc_len, DOCKEY *dockey, USET_ITEM *uset) {
    for (int i = 0; i < doc_len; i++) {
        fp_t kd, kd_inv;
        uint8_t kd_dockey[LAMBDA], kd_enc[LAMBDA];
        F(skey.K1, doc[i], PATH_LEN, kd);
        F(skey.K2, doc[i], PATH_LEN, kd_inv);
        G(skey.K3, doc[i], kd_enc);
        fp_write_bin(kd_dockey, LAMBDA, kd);
        dockey[i] = DOCKEY(doc[i], DOCKEY_ITEM(kd_enc, kd_dockey));
        USET_ITEM tmp_uset;
        fp_t uid, ud, tmp_kdd, tmp_kud, tmp_kud_inv;
        F(ukey.KUT, doc[i], PATH_LEN, uid);
        F(kd_inv, doc[i],  PATH_LEN, tmp_kdd);
        F(ukey.KU, doc[i], PATH_LEN, tmp_kud);
        fp_inv_binar(tmp_kud_inv, tmp_kud);
        fp_mul_comba(ud, tmp_kdd, tmp_kud_inv);
        fp_write_bin(tmp_uset.ud, LAMBDA, ud);
        fp_write_bin(tmp_uset.uid, LAMBDA, uid);
        uset[i] = tmp_uset;
    }
}

void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t ub[], 
    uint8_t doc[][PATH_LEN], int doc_len, USER_AUTH authas[], int auth_len, 
    DOCKEY Dockey[], int dockey_len, ASET_ITEM *aset, USER_AUTH auth2b[], 
    DOCKEY dockey2b[]) {
    fp_t aid, tmp_alpha, alpha;
    F(A_ukey.KUT, ub, LAMBDA, aid);
    F(A_ukey.KU, ub, LAMBDA, tmp_alpha);
    fp_inv_binar(alpha, tmp_alpha);
    fp_write_bin(aset->aid, LAMBDA, aid);
    fp_write_bin(aset->trapgate, LAMBDA, alpha);
    std::map<const uint8_t*, USER_AUTH_ITEM, Uint8ArrayComparator> user_auth_a;
    std::map<const uint8_t*, DOCKEY_ITEM, Uint8ArrayComparator> doc_key_a;
    for (int i = 0; i < auth_len; i++) {
        // user_auth_a[authas[i].d] = USER_AUTH_ITEM(authas[i].uid, authas[i].offtok);
        user_auth_a.insert(std::make_pair(authas[i].d, USER_AUTH_ITEM(authas[i].uid, authas[i].offtok)));
    }
    for (int i = 0; i < dockey_len; i++) {
        // doc_key_a[Dockey[i].d] = DOCKEY_ITEM(Dockey[i].Kd_enc, Dockey[i].Kd);
        doc_key_a.insert(std::make_pair(Dockey[i].d, DOCKEY_ITEM(Dockey[i].Kd_enc, Dockey[i].Kd)));
    }
    for (int i = 0; i < doc_len; i++) {
        fp_t g, kuad, kuau, tmp, offtok, uid;
        bn_t tmp_bn;
        if (user_auth_a.find(doc[i]) == user_auth_a.end()) {
            F(A_ukey.KUT, doc[i], PATH_LEN, uid);
            F(A_ukey.KU, doc[i], PATH_LEN, kuad);
            F(A_ukey.KU, ub, LAMBDA, kuau);
            fp_read_bin(g, g_init, LAMBDA);
            fp_mul_comba(tmp, kuad, kuau);
            fp_prime_back(tmp_bn, tmp);
            // fp_mul_comba(offtok, tmp, g);
            fp_exp_monty(offtok, g, tmp_bn);
            auth2b[i] = USER_AUTH(doc[i], uid, offtok);
            dockey2b[i] = DOCKEY(doc[i], doc_key_a.find(doc[i])->second);
        } else {
            F(A_ukey.KU, ub, LAMBDA, kuau);
            USER_AUTH_ITEM auth_item = user_auth_a.find(doc[i])->second;
            // fp_mul_comba(offtok, auth_item.offtok, kuau);
            fp_prime_back(tmp_bn, kuau);
            fp_exp_monty(offtok, g, tmp_bn);
            auth2b[i] = USER_AUTH(doc[i], auth_item.uid, offtok);
            dockey2b[i] = DOCKEY(doc[i], doc_key_a.find(doc[i])->second);
        }
    }
}


void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY dkey[], int doc_len,
    USER_AUTH usr_au[], int auth_len, TOKEN tk[]) {
    std::map<const uint8_t*, USER_AUTH_ITEM, Uint8ArrayComparator> user_auth;
    std::map<const uint8_t*, DOCKEY_ITEM, Uint8ArrayComparator> doc_key;
    for (int i = 0; i < auth_len; i++) {
        // user_auth[usr_au[i].d] = USER_AUTH_ITEM(usr_au[i].uid, usr_au[i].offtok);
        user_auth.insert(std::make_pair(usr_au[i].d, USER_AUTH_ITEM(usr_au[i].uid, usr_au[i].offtok)));
    }
    for (int i = 0; i < doc_len; i++) {
        // doc_key[dkey[i].d] = DOCKEY_ITEM(dkey[i].Kd_enc, dkey[i].Kd);
        doc_key.insert(std::make_pair(dkey[i].d, DOCKEY_ITEM(dkey[i].Kd_enc, dkey[i].Kd)));
    }
    int k = 0;
    for (auto &iter : doc_key) {
        uint8_t d[PATH_LEN];
        memcpy(d, iter.first, PATH_LEN);
        if (user_auth.find(iter.first) == user_auth.end()) {
            fp_t uid, stk, kdw, kud, g, tmp;
            bn_t tmp_bn;
            F(ukey.KUT, d, PATH_LEN, uid);
            F(iter.second.Kd, word, WORD_LEN, kdw);
            F(ukey.KU, d, PATH_LEN, kud);
            fp_mul_comba(tmp, kdw, kud);
            fp_read_bin(g, g_init, LAMBDA);
            fp_prime_back(tmp_bn, tmp);
            // fp_mul_comba(stk, g, tmp);
            fp_exp_monty(stk, g, tmp_bn);
            tk[k] = TOKEN(uid, stk);
        } else {
            fp_t kdw, stk;
            bn_t tmp_bn;
            USER_AUTH_ITEM item = user_auth.find(iter.first)->second;
            F(iter.second.Kd, word, WORD_LEN, kdw);
            // fp_mul_comba(stk, kdw, item.offtok);
            fp_prime_back(tmp_bn, kdw);
            fp_exp_monty(stk, kdw, tmp_bn);
            tk[k] = TOKEN(item.uid, stk);
        }
        k++;
    }
}
