#include <cstdint>

#define LAMBDA 256/8
#define MAX_WORD 32
#define WORD_LEN 32
#define PATH_LEN 64
#define FILE_DESC_LEN 1100
#define FILE_DESC_LEN_ENC 1104
// #define DEBUG

extern const uint8_t *g_init;
extern const uint8_t IV[16];