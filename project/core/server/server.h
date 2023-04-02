#include "include/include.h"

/**
 * @brief 采用动态规划算法更新Aset
 * 
 * @param Aset 
 * @param alpha 用户上传的陷门
 */
void Aset_update(ASET_DICT &Aset, fp_t alpha);

/**
 * @brief 根据搜索令牌集获取搜索结果
 * 
 * @param query 搜索令牌集
 * @param Aset 
 * @param Uset 
 * @param Xset 
 * @param query_response 返回搜索结果
 */
void search(QUERY_LIST query, ASET_DICT Aset, USET_DICT Uset, XSET_LIST Xset,
    std::vector<std::byte[FILE_DESC_LEN]> &query_response);