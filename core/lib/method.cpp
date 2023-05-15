#include "method.h"
#include <iostream>

void setting_init() {
    core_init();
    ep_param_set(NIST_256);
    ep_new(g);
    bn_new(n);
    ep_curve_get_gen(g);
    ep_curve_get_ord(n);
    std::cout << bn_is_prime(n) << std::endl;
}

// void F(uint8_t *key, uint8_t *msg, fp_t result) {
//     uint8_t tmp[LAMBDA] = {0};
//     md_hmac(tmp, msg, FILE_DESC_LEN, key, LAMBDA);
//     fp_read_bin(result, tmp, LAMBDA);
// }

// void F(const uint8_t* key, const uint8_t* msg, int msg_len, fp_t result) {
//     uint8_t tmp[LAMBDA] = {0};
//     md_hmac(tmp, msg, msg_len, key, LAMBDA);
//     fp_read_bin(result, tmp, LAMBDA);
// }

// void F(const fp_t key, uint8_t* msg, int msg_len, fp_t result) {
//     uint8_t tmp[LAMBDA] = {0};
//     uint8_t k_in_b[LAMBDA] = {0};
//     fp_write_bin(k_in_b, LAMBDA, key);
//     md_hmac(tmp, msg, msg_len, k_in_b, LAMBDA);
//     fp_read_bin(result, tmp, LAMBDA);
// }

void G(uint8_t *key, uint8_t* msg, uint8_t *result) {
    md_hmac(result, msg, PATH_LEN, key, LAMBDA);
}

// void get_xwd(const fp_t kd, const fp_t kd_inv, uint8_t *d, uint8_t *w, fp_t result) {
//     fp_t a, b, c, g;
//     fp_read_bin(g, g_init, LAMBDA);
//     F(kd_inv, d, PATH_LEN, a);
//     F(kd, w, WORD_LEN, b);
//     fp_mul_comba(c, a, b);
//     fp_mul_comba(result, g, c);
// }

int get_ywd(uint8_t *k, uint8_t *d, uint8_t *result) {
    size_t size = PATH_LEN + 16;
    int ret = bc_aes_cbc_enc(result, &size, d, PATH_LEN, k, LAMBDA, IV);
    if (ret == RLC_ERR) {
        printf("failed to aes\n");
    }
    return ret;
}
