#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cassert>
#include <iostream>

#include <relic/relic.h>
#include <relic/relic_bc.h>
#include <relic/relic_rand.h>

#include "../include/const.h"

using namespace std;

/***************************************
 * @brief 读取文件
 * @param path 输入：文件路径
 * @param len 输出：文件长度
 * @return 文件内容
****************************************/
uint8_t *read_file(const char *path, size_t &len);

/***************************************
 * @brief 写入文件
 * @param path 输入：文件路径
 * @param data 输入：文件内容
 * @param len 输入：文件长度
 * @return 0：成功 others：失败
****************************************/
int write_file(const char *path, uint8_t *data, size_t len);

/***************************************
 * @brief 加密文件，结果会存放在同目录下
 * @param in_path 输入：读文件路径
 * @param out_path 输入：写文件路径
 * @param key 输入：密钥
 * @param key_len 输入：密钥长度
 * @param iv 输入：向量
 * @return 0：成功 others：失败
****************************************/
int f_aes_cbc_enc(const char *in_path, const char *out_path, const uint8_t *key, size_t key_len, const uint8_t *iv);
/***************************************
 * @brief 解密文件，结果会存放在同目录下
 * @param in_path 输入：读文件路径
 * @param out_path 输入：写文件路径
 * @param key 输入：密钥
 * @param key_len 输入：密钥长度
 * @param iv 输入：向量
 * @return 0: 成功 others: 失败
****************************************/
int f_aes_cbc_dec(const char *in_path, const char *out_path, const uint8_t *key, size_t key_len, const uint8_t *iv);