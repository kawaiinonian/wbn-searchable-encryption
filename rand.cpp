extern "C" {
    #include <relic/relic.h>
    #include <relic/relic_md.h>
    #include <relic/relic_fp.h>
}
#include <cstdio>

int main (){
    core_init();
    uint8_t key[256] = "testtesttest";
    uint8_t d[2048] = "12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg12345678ighsigioerdhg";
    uint8_t result[32]={0};
    md_hmac(result, d, 2048, key, 32);
    fp_t a;
    fp_param_set(NIST_256);
    fp_read_bin(a, result, 32);
    printf("%d\n", sizeof(a));
    printf("%lu\n", *a);
}
