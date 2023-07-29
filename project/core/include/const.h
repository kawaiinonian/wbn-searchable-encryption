#include <cstdint>
extern "C" {
    #include <relic/relic.h>
}

#define LAMBDA 256/8
#define MAX_WORD 32
#define WORD_LEN 32
#define PATH_LEN 16
// #define DEBUG


extern const uint8_t IV[16];
extern ep_t g;
extern bn_t n;