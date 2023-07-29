#define LAMBDA 256/8
#define MAX_WORD 32
#define WORD_LEN 32
#define PATH_LEN 64
#define PATH_LEN_ENC 64+16
#define RSA_GROUP 2048/8

extern "C" {
    #include <relic/relic.h>
}

extern bn_t g1, g2, g3;
extern ep_t g;
extern bn_t n, p, ord;
extern const uint8_t IV[16];