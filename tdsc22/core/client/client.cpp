#include "client.h"
#include <iostream>

void F(const uint8_t* key, const uint8_t* msg, int msg_len, uint8_t *result) {
    uint8_t tmp[LAMBDA] = {0};
    md_hmac(result, msg, msg_len, key, LAMBDA);
}

void word2prime(uint8_t word[], bn_t w) {
    bn_t r;
    bn_new(r);
    bn_zero(r);
    do{
        uint8_t rut[LAMBDA] = {0}, mac[LAMBDA] = {0}, hash[LAMBDA] = {0};
        bn_write_bin(rut, LAMBDA, r);
        // md_hmac(mac, rut, LAMBDA, key, LAMBDA);
        md_map_sh256(mac, rut, LAMBDA);
        md_map_sh256(hash, word, WORD_LEN);
        bn_t low, high;
        bn_new(low);
        bn_new(high);
        bn_read_bin(low, mac, LAMBDA);
        bn_read_bin(high, hash, LAMBDA);
        bn_lsh(high, high, LAMBDA);
        bn_add(w, high, low);

        bn_free(low);
        bn_free(high);
        bn_add_dig(r, r, 1);
    }while(!bn_is_prime(w));
    bn_free(r);
}

void Fp(const uint8_t* key, bn_t msg, bn_t result) {
    uint8_t* msg_t = new uint8_t[msg->used * 8];
    uint8_t md[LAMBDA] = {0};
    bn_write_bin(msg_t, msg->used * 8, msg);
    md_hmac(md, msg_t, msg->used * 8, key, LAMBDA);
    bn_read_bin(result, md, LAMBDA);
    bn_mod(result, result, p);
    delete[] msg_t;
}

void update(MK master_key, word_file* db[], int word_num, EDB_ITEM *edb, uint8_t xset[][LAMBDA+1]) {
    int cnt = 0;
    // std::cout << word_num << std::endl;
    for (int i = 0; i < word_num; i++) {
        uint8_t stag[LAMBDA] = {0}, kw[LAMBDA] = {0}, g1w_t[RSA_GROUP] = {0}, g2w_t[RSA_GROUP] = {0}, g3w_t[RSA_GROUP] = {0};
        bn_t w, g1w, g2w, g3w;
        bn_new(w);
        bn_new(g1w);
        bn_new(g2w);
        bn_new(g3w);
        word2prime(db[i]->word, w);
        // bn_print(w);
        bn_mod_inv(w, w, ord);
        bn_mxp(g1w, g1, w, n);
        bn_write_bin(g1w_t, RSA_GROUP, g1w);
        bn_mxp(g2w, g2, w, n);
        bn_write_bin(g2w_t, RSA_GROUP, g2w);
        bn_mxp(g3w, g3, w, n);
        bn_write_bin(g3w_t, RSA_GROUP, g3w);
        // bn_print(g1w);
        F(master_key.Ks, g1w_t, RSA_GROUP, stag);// get stag_w
        F(master_key.K, stag, LAMBDA, kw);// get k_w
        // std::cout << db[i]->len << std::endl;
        for (int j = 0; j < db[i]->len; j++) {
            bn_t c, z, xind, id, y, g2tmp;
            ep_t xtag;
            uint8_t c_t[LAMBDA] = {0};
            bn_new(c);
            bn_new(z);
            bn_new(xind);
            bn_new(id);
            bn_new(y);
            bn_new(g2tmp);
            ep_new(xtag);
            bn_zero(c);
            bn_add_dig(c, c, j);
            bn_write_bin(c_t, LAMBDA, c);
            F(stag, c_t, LAMBDA, edb[cnt].l);// get l

            // std::cout << db[i]->ids[j] << std::endl;
            // get e
            size_t size = PATH_LEN_ENC;
            int ret = bc_aes_cbc_enc(edb[cnt].e, &size, db[i]->ids[j], PATH_LEN, kw, LAMBDA, IV);
            if (ret != RLC_OK)
                std::cout << "encrypt error" << std::endl;
            

            bn_read_bin(id, db[i]->ids[j], PATH_LEN);
            // std::cout << "compute xind" << std::endl;
            Fp(master_key.Ki, id, xind); // get xind

            // bn_lsh(g2w, g2w, LAMBDA);
            bn_add(g2tmp, g2w, c);
            // std::cout << "compute z" << std::endl;
            Fp(master_key.Kz, g2tmp, z); // get z
            // bn_print(z);

            bn_t tmp_index;
            bn_new(tmp_index);
            // std::cout << "compute xtag" << std::endl;
            Fp(master_key.Kx, g3w, tmp_index);    // get xtag and append to xset
            ep_mul(xtag, g, tmp_index);
            // ep_print(xtag);
            ep_mul(xtag, xtag, xind);
            ep_write_bin(xset[cnt], LAMBDA+1, xtag, true);
            bn_free(tmp_index);

            // std::cout << "compute y" << std::endl;

            bn_mod_inv(z, z, p);    // get y
            bn_mul(y, xind, z);
            bn_mod(y, y, p);
            // std::cout << y->used << std::endl;
            bn_write_bin(edb[cnt].y, LAMBDA, y);

            bn_free(c);
            bn_free(z);
            bn_free(xind);
            bn_free(id);
            bn_free(y);
            bn_free(g2tmp);
            ep_free(xtag);
            cnt++;
            if(cnt % 10000 == 0)
                std::cout << "has compute pairs num: " << cnt << std::endl;
        }
        bn_free(w);
        bn_free(g1w);
        bn_free(g2w);
        bn_free(g3w);
        // std::cout << "now free bnt" << std::endl;
    }
}


void auth(uint8_t *authwords[], int len, SKs *sk) {
    bn_t sk1, sk2, sk3, tmp;
    bn_new(sk1);
    bn_new(sk2);
    bn_new(sk3);
    bn_new(tmp);
    // bn_new(tmp);
    // bn_copy(sk1, g1);
    // bn_add_dig(tmp, ord, 1);
    // bn_mxp(sk2, sk1, tmp, n);
    // if (bn_cmp(sk2, g1) == RLC_EQ)
    //     std::cout << "success" << std::endl;
    // bn_print(ord);
    // bn_print(n);
    bn_copy(sk1, g1);
    // bn_copy(tmp, g1);
    bn_copy(sk2, g2);
    bn_copy(sk3, g3);
    bn_zero(tmp);
    bn_add_dig(tmp, tmp, 1);
    for (int i = 0; i < len; i++) {
        bn_t w;
        bn_new(w);
        word2prime(authwords[i], w);
        bn_mul(tmp, tmp, w);
        bn_mod(tmp, tmp, ord);
        // bn_mxp(tmp, tmp, w, n);
        // bn_mod_inv(w, w, ord);
        // bn_mxp(sk1, sk1, w, n);
        // bn_mxp(tmp, tmp, w, n);
        // if (bn_cmp(tmp, g1) == RLC_EQ)
        //     std::cout << "success" << std::endl;
        // bn_print(w);
        // bn_print(sk1);
        // bn_mxp(sk2, sk2, w, n);
        // bn_mxp(sk3, sk3, w, n);
        bn_free(w);
        // std::cout << authwords[i] << std::endl;
    }
    bn_mod_inv(tmp, tmp, ord);
    bn_mxp(sk1, sk1, tmp, n);
    bn_mxp(sk2, sk2, tmp, n);
    bn_mxp(sk3, sk3, tmp, n);
    bn_write_bin(sk->sk1, RSA_GROUP, sk1);
    // bn_print(sk1);
    bn_write_bin(sk->sk2, RSA_GROUP, sk2);
    // bn_print(sk2);
    bn_write_bin(sk->sk3, RSA_GROUP, sk3);
    // bn_print(sk3);
    bn_free(sk1);
    bn_free(sk2);
    bn_free(sk3);
    bn_free(tmp);
}


void get_stag(MK master_key, uint8_t *query_words[], int len, SKs* sk, uint8_t stag[]) {
    // get index
    bn_t sk1;
    bn_new(sk1);
    bn_read_bin(sk1, sk->sk1, RSA_GROUP);
    for (int i = 0; i < len; i++) {
        bn_t w;
        bn_new(w);
        word2prime(query_words[i], w);
        bn_mxp(sk1, sk1, w, n);
        // bn_print(sk1);

        bn_free(w);
        // std::cout << query_words[i] << std::endl;
    }
    uint8_t sk1_t[RSA_GROUP] = {0};
    bn_write_bin(sk1_t, RSA_GROUP, sk1);
    // if (bn_cmp(sk1, g1) == RLC_EQ)
    //     std::cout << "equal!" << std::endl;
    F(master_key.Ks, sk1_t, RSA_GROUP, stag); // get stag
    bn_free(sk1);
}

void get_index1(SKs sk, uint8_t *query_words[], int len, MK master_key, uint8_t *index1) {
    bn_t sk2;
    bn_new(sk2);
    bn_read_bin(sk2, sk.sk2, RSA_GROUP);
    for (int i = 0; i < len; i++) {
        // get index
        bn_t w;
        bn_new(w);
        word2prime(query_words[i], w);
        bn_mxp(sk2, sk2, w, n);
        bn_free(w);
    }
    bn_write_bin(index1, RSA_GROUP, sk2);
    bn_free(sk2);
}

void get_index2(SKs sk, uint8_t *query_words[], int len, MK master_key, uint8_t *index2) {
    bn_t sk3;
    bn_new(sk3);
    bn_read_bin(sk3, sk.sk3, RSA_GROUP);
    for (int j = 0; j < len; j++) {
        bn_t w;
        bn_new(w);
        word2prime(query_words[j], w);
        bn_mxp(sk3, sk3, w, n);
        bn_free(w);
    }
    bn_t result;
    bn_new(result);
    Fp(master_key.Kx, sk3, result);
    bn_write_bin(index2, LAMBDA, result);
    bn_free(result);
    bn_free(sk3);
}

void token_generate(int round, uint8_t *index1, uint8_t *index2[], int len, MK master_key, uint8_t *token_term[]) {
    bn_t index1_t, index1_used;
    bn_new(index1_t);
    bn_new(index1_used);
    bn_read_bin(index1_t, index1, RSA_GROUP);
    bn_add_dig(index1_t, index1_t, round);
    Fp(master_key.Kz, index1_t, index1_used);
    for (int i = 0; i < len-1; i++) {
        bn_t index2_t, index;
        ep_t token;
        ep_new(token);
        bn_new(index2_t);
        bn_new(index);
        bn_read_bin(index2_t, index2[i], LAMBDA);
        bn_mul(index, index1_used, index2_t);
        ep_mul(token, g, index);
        // std::cout << sizeof(token_term[i]) << std::endl;
        ep_write_bin(token_term[i], LAMBDA+1, token, true);
        // ep_read_bin(token, token_term[i], LAMBDA+1);
        bn_free(index);
        bn_free(index2_t);
        ep_free(token);
    }
    bn_free(index1_t);
    bn_free(index1_used);
}

// void token_generate(SKs sk, uint8_t *query_words[], int len, int round, MK master_key, uint8_t *token_term[]) {
//     bn_t c, index1, index2, index, sk2;
//     bn_new(c);
//     bn_new(index1);
//     bn_new(index2);
//     bn_new(index);
//     bn_new(sk2);
//     bn_zero(c);
//     bn_add_dig(c, c, round);
//     bn_read_bin(sk2, sk.sk2, RSA_GROUP);
//     // bn_print(sk2);
//     for (int i = 1; i < len; i++) {
//         // get index
//         bn_t w;
//         bn_new(w);
//         word2prime(query_words[i], w);
//         bn_mxp(sk2, sk2, w, n);
//         bn_free(w);
//     }
//     // bn_lsh(sk2, sk2, LAMBDA);
//     bn_add(sk2, sk2, c);
//     Fp(master_key.Kz, sk2, index1);
//     bn_t sk3, sk3tmp;
//     bn_new(sk3);
//     bn_new(sk3tmp);
//     bn_read_bin(sk3, sk.sk3, RSA_GROUP);
//     // bn_print(sk3);
//     for (int i = 1; i < len; i++) {
//         bn_copy(sk3tmp, sk3);
//         for (int j = 0; j < len; j++) {
//             if (j == i)
//                 continue;
//             else {
//                 bn_t w;
//                 bn_new(w);
//                 word2prime(query_words[j], w);
//                 bn_mxp(sk3tmp, sk3tmp, w, n);
//                 bn_free(w);
//             }
//         }
//         Fp(master_key.Kx, sk3tmp, index2);
//         // bn_mul(index, index1, index2);
//         ep_t tmp;
//         ep_new(tmp);
//         ep_mul(tmp, g, index2);
//         // bn_print(index1);
//         // ep_print(tmp);
//         ep_mul(tmp, tmp, index1);
//         ep_write_bin(token_term[i-1], LAMBDA+1, tmp, true);
//         ep_free(tmp);
//     }
//     bn_free(sk3);
//     bn_free(sk3tmp);
//     bn_free(c);
//     bn_free(sk2);
//     bn_free(index1);
//     bn_free(index2);
//     bn_free(index);
// }
