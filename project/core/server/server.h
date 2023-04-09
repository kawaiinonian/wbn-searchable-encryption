#ifndef _HEAD_INC_
#include "../include/include.h"
#endif

#include "../lib/method.h"

/**
 * @brief 采用动态规划算法更新Aset
 * 
 * @param Aset 
 * @param aitem
 */
void Aset_update(ASET_LIST &Aset, ASET_ITEM aitem);

/**
 * @brief 根据搜索令牌集获取搜索结果
 * 
 * @param query 搜索令牌集
 * @param aid
 * @param Aset 
 * @param Uset 
 * @param Xset 
 * @param query_response 返回搜索结果
 */
void search(QUERY_LIST query, fp_t aid, ASET_LIST Aset, USET_LIST Uset, XSET_LIST Xset,
    std::vector<uint8_t *> &query_response);
