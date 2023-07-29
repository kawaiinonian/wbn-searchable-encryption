#include "server.h"

void F(const uint8_t* key, const uint8_t* msg, int msg_len, uint8_t *result) {
    uint8_t tmp[LAMBDA] = {0};
    md_hmac(result, msg, msg_len, key, LAMBDA);
}

void get_hash(uint8_t stag[], int c, uint8_t *result) {
    bn_t c_bn;
    bn_new(c_bn);
    bn_zero(c_bn);
    bn_add_dig(c_bn, c_bn, c);
    uint8_t c_t[LAMBDA];
    bn_write_bin(c_t, LAMBDA, c_bn);
    F(stag, c_t, LAMBDA, result);
    bn_free(c_bn);
}

void get_exp(uint8_t base[], uint8_t index[], uint8_t *result) {
    ep_t base_ep;
    bn_t index_bn;
    ep_new(base_ep);
    bn_new(index_bn);
    ep_read_bin(base_ep, base, LAMBDA+1);
    bn_read_bin(index_bn, index, LAMBDA);
    ep_mul(base_ep, base_ep, index_bn);
    ep_write_bin(result, LAMBDA+1, base_ep, true);
    bn_free(index_bn);
    ep_free(base_ep);
}