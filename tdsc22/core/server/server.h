#ifndef _HEAD_INC_
#include "../include/include.h"
#endif

extern "C" {
    void get_exp(uint8_t base[], uint8_t index[], uint8_t *result);
    void get_hash(uint8_t stag[], int c, uint8_t *result);
}