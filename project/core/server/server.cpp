#include "server.h"


void get_multi(uint8_t *key1, uint8_t *key2, uint8_t *ret) {
    bn_t a, b, c;
    bn_new(a);
    bn_new(b);
    bn_new(c);
    bn_read_bin(a, key1, LAMBDA);
    bn_read_bin(b, key2, LAMBDA);
    bn_mul(c, a, b);
    bn_mod(c, c, n);
    bn_write_bin(ret, LAMBDA, c);
    bn_free(a);
    bn_free(b);
    bn_free(c);
}

void get_exp(uint8_t *key1, uint8_t *key2, uint8_t *ret) {
    ep_t element, result;
    ep_new(element);
    ep_new(result);
    bn_t index;
    bn_new(index);
    ep_read_bin(element, key1, LAMBDA+1);
    bn_read_bin(index, key2, LAMBDA);
    ep_mul_basic(result, element, index);
    // ep_print(result);
    ep_write_bin(ret, LAMBDA+1, result, true);
    ep_free(element);
    ep_free(result);
    bn_free(index);
}

