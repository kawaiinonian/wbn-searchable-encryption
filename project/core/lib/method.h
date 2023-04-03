#include "include/include.h"
#include <relic/relic.h>

void F(uint8_t *key, uint8_t* msg, fp_t result);
void F(const fp_t k, uint8_t* msg, int msg_len, fp_t result);
void F(const uint8_t* key, uint8_t* msg, int msg_len, fp_t result);
void G(uint8_t *key, uint8_t* msg, uint8_t *result);
void setting_init(void);


void get_xwd(const fp_t kd, const fp_t kd_inv, uint8_t *d, uint8_t *w, fp_t result);
void get_ywd(uint8_t *k, uint8_t *d, uint8_t *result);