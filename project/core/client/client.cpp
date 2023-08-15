#include "client.h"
#include <iostream>
#include <fstream>
// #include <unordered_map>

const char *filename = "/root/project514/project/debug";

void debug(const uint8_t* d, int len, const char *desc) {
  std::ofstream outfile;
  outfile.open(filename, std::ios_base::app | std::ios_base::binary);
  outfile << desc;
  for (int i = 0; i < len; ++i) {
    outfile << static_cast<int>(d[i]);
  }
  outfile << '\n';
  outfile.close();
}

void F(const uint8_t* key, const uint8_t* msg, int msg_len, uint8_t *result) {
    uint8_t tmp[LAMBDA] = {0};
    md_hmac(result, msg, msg_len, key, LAMBDA);
    // bn_read_bin(result, tmp, LAMBDA);
}

void F(const bn_t key, uint8_t* msg, int msg_len, uint8_t *result) {
    uint8_t tmp[LAMBDA] = {0};
    uint8_t k_in_b[LAMBDA] = {0};
    bn_write_bin(k_in_b, LAMBDA, key);
    md_hmac(result, msg, msg_len, k_in_b, LAMBDA);
    // bn_read_bin(result, tmp, LAMBDA);
}

void get_xwd(const uint8_t* kd, const uint8_t* kd_inv, uint8_t *d, uint8_t *w, ep_t result) {
    bn_t c, a, b;
    bn_new(c);
    bn_new(a);
    bn_new(b);
    uint8_t kdd[LAMBDA] = {0}, kdw[LAMBDA] = {0};
    F(kd_inv, d, PATH_LEN, kdd);
    F(kd, w, WORD_LEN, kdw);
    bn_read_bin(b, kdd, LAMBDA);
    bn_read_bin(a, kdw, LAMBDA);
    bn_mul(c, a, b);
    bn_mod(c, c, n);
    ep_mul(result, g, c);

    bn_free(c);
    bn_free(a);
    bn_free(b);
}

void updateData_generate(SEARCH_KEY skey, file *fd[], int len,
    XSET_ITEM *xset) {
    int k = 0;
    for (int i = 0; i < len; i++) {
        uint8_t kd[LAMBDA] ={0}, kd_inv[LAMBDA] = {0}, kd_enc[LAMBDA] = {0};
        F(skey.K1, fd[i]->d, PATH_LEN, kd);
        F(skey.K2, fd[i]->d, PATH_LEN, kd_inv);
        G(skey.K3, fd[i]->d, kd_enc);
        for (int j = 0; j < fd[i]->wordlen; j++) {
            XSET_ITEM tmp;
            ep_t xwd;
            ep_new(xwd);
            get_xwd(kd, kd_inv, fd[i]->d, fd[i]->words[j], xwd);
            ep_write_bin(tmp.xwd, LAMBDA+1, xwd, true);
            get_ywd(kd_enc, fd[i]->d, tmp.ywd);
            xset[k] = tmp;
            k++;
            ep_free(xwd);
        }
    }
}

void online_auth(SEARCH_KEY skey, USER_KEY ukey, uint8_t doc[][PATH_LEN],
    int doc_len, DOCKEY *dockey, USET_ITEM *uset) {
        // debug(NULL,0, "");
    for (int i = 0; i < doc_len; i++) {
        // fp_t kd, kd_inv;
        uint8_t kd[LAMBDA] = {0}, kd_inv[LAMBDA] = {0}, kd_enc[LAMBDA] = {0};
        F(skey.K1, doc[i], PATH_LEN, kd);
        F(skey.K2, doc[i], PATH_LEN, kd_inv);
        G(skey.K3, doc[i], kd_enc);
        dockey[i] = DOCKEY(doc[i], kd_enc, kd);
        USET_ITEM tmp_uset;
        uint8_t kdd[LAMBDA] = {0}, kud[LAMBDA] = {0}, kud_inv[LAMBDA] = {0};
        bn_t kud_bn, kud_inv_bn, kdd_bn, ud_bn;
        bn_new(kud_bn);
        bn_new(kud_inv_bn);
        bn_new(ud_bn);
        bn_new(kdd_bn);
        F(ukey.KUT, doc[i], PATH_LEN, tmp_uset.uid);
        F(kd_inv, doc[i],  PATH_LEN, kdd);
        F(ukey.KU, doc[i], PATH_LEN, kud);
        bn_read_bin(kud_bn, kud, LAMBDA);
        bn_read_bin(kdd_bn, kdd, LAMBDA);
        bn_mod_inv(kud_inv_bn, kud_bn, n);
        // bn_div(kud_inv_bn, kud_inv_bn, kud_inv_bn);
        bn_mul(ud_bn, kud_inv_bn, kdd_bn);
        bn_mod(ud_bn, ud_bn, n);
        bn_write_bin(tmp_uset.ud, LAMBDA, ud_bn);
        uset[i] = tmp_uset;
        bn_free(kud_bn);
        bn_free(kud_inv_bn);
        bn_free(ud_bn);
        bn_free(kdd_bn);
    }
}

void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t ub[], 
    uint8_t doc[][PATH_LEN], int doc_len, USER_AUTH authas[], int auth_len, 
    DOCKEY Dockey[], int dockey_len, ASET_ITEM *aset, USER_AUTH auth2b[], 
    DOCKEY dockey2b[]) {

    ep_t offtok;
    bn_t alpha;
    bn_new(alpha);
    uint8_t tmp[LAMBDA] = {0};
    F(A_ukey.KUT, ub, LAMBDA, aset->aid);
    F(A_ukey.KU, ub, LAMBDA, tmp);
    bn_read_bin(alpha, tmp, LAMBDA);
    bn_mod_inv(alpha, alpha, n);
    bn_write_bin(aset->trapgate, LAMBDA, alpha);
    std::map<const uint8_t*, USER_AUTH_ITEM, Uint8ArrayComparator> user_auth_a;
    std::map<const uint8_t*, DOCKEY_ITEM, Uint8ArrayComparator> doc_key_a;
    std::cout << "now construct map" << std::endl;
    for (int i = 0; i < auth_len; i++) {
        user_auth_a.insert(std::make_pair(authas[i].d, USER_AUTH_ITEM(authas[i].uid, authas[i].offtok)));
    }
    for (int i = 0; i < dockey_len; i++) {
        doc_key_a.insert(std::make_pair(Dockey[i].d, DOCKEY_ITEM(Dockey[i].Kd_enc, Dockey[i].Kd)));
    }
    std::cout << "now compute data to user" << std::endl;
    for (int i = 0; i < doc_len; i++) {
        
        if (user_auth_a.find(doc[i]) == user_auth_a.end()) {
            uint8_t uid[LAMBDA] = {0}, kud[LAMBDA] = {0}, kuu[LAMBDA] = {0};
            ep_t offtok;
            ep_new(offtok);
            bn_t a, b, index;
            bn_new(a);
            bn_new(b);
            bn_new(index);
            F(A_ukey.KUT, doc[i], PATH_LEN, uid);
            F(A_ukey.KU, doc[i], PATH_LEN, kud);
            F(A_ukey.KU, ub, LAMBDA, kuu);
            bn_read_bin(a, kud, LAMBDA);
            bn_read_bin(b, kuu, LAMBDA);
            bn_mul(index, a, b);
            ep_mul(offtok, g, index);
            auth2b[i] = USER_AUTH(doc[i], uid, offtok);
            dockey2b[i] = DOCKEY(doc[i], doc_key_a.find(doc[i])->second.Kd_enc, doc_key_a.find(doc[i])->second.Kd);
            bn_free(a);
            bn_free(b);
            bn_free(index);
            ep_free(offtok);
        } else {
            uint8_t uid[LAMBDA] = {0}, kuu[LAMBDA] = {0};
            ep_t offtok, new_offtok;
            ep_new(offtok);
            ep_new(new_offtok);
            bn_t index;
            bn_new(index);
            F(A_ukey.KU, ub, LAMBDA, kuu);
            bn_read_bin(index, kuu, LAMBDA);
            ep_read_bin(offtok, user_auth_a.find(doc[i])->second.offtok, LAMBDA+1);
            std::cout << "now compute dG" << std::endl;
            ep_mul(new_offtok, offtok, index);
            auth2b[i] = USER_AUTH(doc[i], user_auth_a.find(doc[i])->second.uid, new_offtok);
            dockey2b[i] = DOCKEY(doc[i], doc_key_a.find(doc[i])->second.Kd_enc, doc_key_a.find(doc[i])->second.Kd);    
            bn_free(index);
            ep_free(offtok);
            ep_free(new_offtok);
        }
    }
    bn_free(alpha);

}


void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY dkey[], int doc_len,
    USER_AUTH usr_au[], int auth_len, TOKEN tk[], DOCKEY retdkey[]) {
    std::map<const uint8_t*, USER_AUTH_ITEM, Uint8ArrayComparator> user_auth;
    std::map<const uint8_t*, DOCKEY_ITEM, Uint8ArrayComparator> doc_key;
    for (int i = 0; i < auth_len; i++) {
        user_auth.insert(std::make_pair(usr_au[i].d, USER_AUTH_ITEM(usr_au[i].uid, usr_au[i].offtok)));
    }
    for (int i = 0; i < doc_len; i++) {
        doc_key.insert(std::make_pair(dkey[i].d, DOCKEY_ITEM(dkey[i].Kd_enc, dkey[i].Kd)));
    }
    int k = 0;
    for (auto &iter : doc_key) {
        uint8_t d[PATH_LEN] = {0};
        memcpy(d, iter.first, PATH_LEN);
        retdkey[k] = DOCKEY(d, iter.second.Kd_enc, iter.second.Kd);
        if (user_auth.find(iter.first) == user_auth.end()) {
            uint8_t uid[LAMBDA] = {0}, kdw[LAMBDA] = {0}, kud[LAMBDA] = {0};
            bn_t kdw_bn, kud_bn, index;
            ep_t stk;
            ep_new(stk);
            bn_new(kdw_bn);
            bn_new(kud_bn);
            bn_new(index);
            F(ukey.KUT, d, PATH_LEN, uid);
            F(iter.second.Kd, word, WORD_LEN, kdw);
            F(ukey.KU, d, PATH_LEN, kud);
            bn_read_bin(kdw_bn, kdw, LAMBDA);
            bn_read_bin(kud_bn, kud, LAMBDA);

            bn_mul(index, kud_bn, kdw_bn);
            bn_mod(index, index, n);
            ep_mul(stk, g, index);

            tk[k] = TOKEN(uid, stk);
            bn_free(kdw_bn);
            bn_free(kud_bn);
            bn_free(index);
            ep_free(stk);
        } else {
            uint8_t uid[LAMBDA] = {0}, kdw[LAMBDA] = {0};
            ep_t stk, offtok;
            ep_new(stk);
            ep_new(offtok);
            F(iter.second.Kd, word, WORD_LEN, kdw);
            bn_t index;
            bn_new(index);
            bn_read_bin(index, kdw, LAMBDA);
            ep_read_bin(offtok, user_auth.find(iter.first)->second.offtok, LAMBDA+1);
            ep_mul(stk, offtok, index);
            tk[k] = TOKEN(user_auth.find(iter.first)->second.uid, stk);
            bn_free(index);
            ep_free(stk);
            ep_free(offtok);
        }
        k++;
    }
}
