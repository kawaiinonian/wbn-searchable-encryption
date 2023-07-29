#include "method.h"
#include <fstream>
#include <iostream>
#include <unistd.h>
#include <string>

void readDataFromFile(uint8_t* buffer, int length, const std::string& filename) {
    // 创建输入文件流对象
    std::ifstream file(filename, std::ios::binary);

    if (!file) {
        std::cout << "无法打开文件：" << filename << std::endl;
        return;
    }

    // 读取数据到缓冲区
    file.read(reinterpret_cast<char*>(buffer), length);

    // 关闭文件流
    file.close();
}

void setting_init() {
    core_init();
    ep_param_set(NIST_256);
    bn_new(g1);
    bn_new(g2);
    bn_new(g3);
    bn_new(p);
    bn_new(ord);
    bn_new(n);
    ep_new(g);

    ep_curve_get_gen(g);
    ep_curve_get_ord(p);
    uint8_t n_t[RSA_GROUP] = {0}, ord_t[RSA_GROUP] = {0};
    char buffer[64] = {0};
    getcwd(buffer, 64);
    std::string currentPath(buffer);
    std::cout << "current path is " << currentPath << std::endl;
    std::string n_path = currentPath + "/tdsc22/core/n";
    std::string ord_path = currentPath + "/tdsc22/core/ord";
    readDataFromFile(n_t, RSA_GROUP, n_path);
    readDataFromFile(ord_t, RSA_GROUP, ord_path);
    bn_read_bin(n, n_t, RSA_GROUP);
    bn_read_bin(ord, ord_t, RSA_GROUP);
    bn_rand(g1, RLC_POS, RSA_GROUP*8);
    bn_rand(g2, RLC_POS, RSA_GROUP*8);
    bn_rand(g3, RLC_POS, RSA_GROUP*8);
    bn_mod(g1, g1, n);
    bn_mod(g2, g2, n);
    bn_mod(g3, g3, n);
}
