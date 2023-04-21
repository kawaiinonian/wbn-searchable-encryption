extern "C" {
    #include <relic/relic.h>
    #include <relic/relic_fp.h>
}
#include <map>
#include <iostream>
#include <cstring>
#define LAMBDA 256/8

using namespace std;

// class SEARCH_KEY {
//     public:
//     uint8_t K1[LAMBDA], K2[LAMBDA], K3[LAMBDA];

//     SEARCH_KEY(void) {
//         memset(K1, 0, sizeof(K1));
//         memset(K2, 0, sizeof(K2));
//         memset(K3, 0, sizeof(K3));
//     }
//     SEARCH_KEY(uint8_t* _K1, uint8_t* _K2, uint8_t* _K3) {
//         memcpy(K1, _K1, LAMBDA);
//         memcpy(K2, _K2, LAMBDA);
//         memcpy(K3, _K3, LAMBDA);
//     }
//     int test(void) {
//         return 1;
//     }
// };
// typedef std::map<uint8_t*, SEARCH_KEY> test;
// class test {
//     public:
//     char a[3];
//     test();
// };

// int main (){
//     // core_init();
//     // uint8_t test[64] = "helloworldhelloworldhelloworldhelloworldhelloworldhelloworld\n";
//     // uint8_t key[16] = "testkey";
//     // uint8_t iv[16] = "abcdefghijklmno";
//     // uint8_t *out = new uint8_t[81];
//     // size_t *size1 = new size_t;
//     // size_t *size2 = new size_t;
//     // uint8_t *out1 = new uint8_t[81];
//     // *size1 = 81;
//     // // *size2 = 64;
//     // int errcode = bc_aes_cbc_enc(out, size1, test, 64, key, 16, iv);
//     // printf("%s\nerrcode=%d\n", out, errcode);
//     // int errcodd_ = bc_aes_cbc_dec(out1, size1, out, 80, key, 16, iv);
//     // printf("%s\nerrcode=%d\n", out1, errcodd_);
//     uint8_t test[100][100] = {0};
//     printf("%d\n", sizeof(test));
//     return 0;
// }
// extern "C" {
//     void test_map(test *input[], uint8_t *output) {
//         for (int i = 0; i < 2; i++) {
//             memcpy(output+i*sizeof(test), input[i]->a, 3);
//         }
//     }
//     void test_relic(uint8_t *input, int len) {
//         core_init();
//         fp_param_set(NIST_256);
//         fp_t a;
//         printf("%d, %d, %d\n", sizeof(input), len, sizeof(a));
//         fp_read_bin(a, input, 32);
//         uint8_t *ret = new uint8_t[len];
//         // fp_write_bin(ret, len, a);
//         // return ret;
//     }
// }

// int main() {
//     SEARCH_KEY *test_ = new SEARCH_KEY;
//     uint8_t a[16] = "abcdefg";
//     cout << a << endl;
//     cout << "helloworld" << endl;
//     printf("helloworld\n");
//     fflush(stdout);
//     return 0;
// }
// int main () {
//     core_init();
//     printf("%d\n", sizeof(fp_t));
//     return 0;
// }
#define FILE_DESC_LEN 1100
const uint8_t *g_init = (const uint8_t *)"abc";
void F(uint8_t *key, uint8_t *msg, fp_t result) {
    uint8_t tmp[LAMBDA] = {0};
    md_hmac(tmp, msg, FILE_DESC_LEN, key, LAMBDA);
    fp_read_bin(result, tmp, LAMBDA);
}
int main() {
    core_init();
    fp_param_set(NIST_256);
    fp_t g,a,b,c,r;
    uint8_t ku[LAMBDA] = {0}, d[FILE_DESC_LEN], result[LAMBDA] = {0};
    memcpy(ku, "helloworldhelloworldhelloworldh", LAMBDA);
    memcpy(d, "helloworldhelloworldhelloworldhhelloworldhelloworldhelloworldhhelloworldhelloworldhelloworldh", 3*LAMBDA);
    fp_read_bin(g, g_init, LAMBDA);
    F(ku, d, a);
    fp_inv_binar(b, a);
    fp_mul_comba(c, a, b);
    fp_mul_comba(r, g, c);
    fp_write_bin(result, LAMBDA, r);
    printf("%s\n", result);
}