#include "include/include.h"
#include "lib/method.h"
#include <relic/relic.h>
#include <string>
#include <map>
#include <vector>


/***************************************
 * @brief 生成加密的文件索引
 * @param skey 用户作为DO的密钥组
 * @param DOC 要加密的文件标识符集
 * @param Xset_to_server 返回给服务器的文件-关键词索引
****************************************/
void updateData_generate(SEARCH_KEY skey, FILE_DESC_LIST DOC, 
    XSET_LIST &Xset_to_server);


/***************************************
 * @brief 由DO授权给DU
 * @param skey DO的密钥组
 * @param ukey DU的密钥组
 * @param DOC 要授权的文件标识符集
 * @param key_to_user 返回给DU的文件密钥集
 * @param uset_to_server 返回给服务器更新DU-文件授权关系
****************************************/
void online_auth(SEARCH_KEY skey, USER_KEY ukey, FILE_DESC_LIST DOC, 
    DOCKEY_DICT &key_to_user, USET_LIST &uset_to_server);

/***************************************
* @brief 由DU授权给DU
* @param A_ukey 授权DU的密钥组
* @param B_ukey 被授权DU的密钥组
* @param ub
* @param DOC 要授权的文件标识符集
* @param User_AuthA 授权DU的被授权信息字典，组织形式为 文件标识符d-被授权信息组
* @param Dok_KeyA 授权DU的文件密钥集
* @param auth_to_userB 返回给被授权DU的被授权信息字典
* @param key_to_userB 返回给被授权DU的文件密钥集
* @param tmp_Aset_to_server 返回给服务器的Aset授权关系更新信息
****************************************/
void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, uint8_t* ub, FILE_DESC_LIST DOC, 
    USER_AUTH_DICT User_AuthA, DOCKEY_DICT Doc_KeyA, 
    USER_AUTH_DICT &auth_to_userB, DOCKEY_DICT &key_to_userB,
    ASET_ITEM &tmp_Aset_to_server);

/***************************************
 * @brief 生成搜索令牌
 * @param word 要搜索的关键词
 * @param ukey 搜索者DU的密钥组
 * @param Doc_Key 搜索者的文件密钥集
 * @param User_Auth 搜索者的被授权情况字典
 * @param query_list 返回的查询令牌集
 ***************************************/
void search_generate(uint8_t* word, USER_KEY ukey, DOCKEY_DICT Doc_Key,
    USER_AUTH_DICT User_Auth, QUERY_LIST &query_list);

