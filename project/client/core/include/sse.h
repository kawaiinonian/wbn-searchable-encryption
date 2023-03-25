#include "include/const.h"
// to be changed: for coding with no error
#include "include/include.h"


/***************************************
 * @brief 生成加密的文件索引
 * @param skey 用户作为DO的密钥组
 * @param DOC 要加密的文件标识符集
 * @param Xset_to_server 返回给服务器的文件-关键词索引
****************************************/
void updateData_generate(SEARCH_KEY skey, FILE_DESC_LIST DOC, XSET_LIST &Xset_to_server);


/***************************************
 * @brief 由DO授权给DU
 * @param skey DO的密钥组
 * @param ukey DU的密钥组
 * @param DOC 要授权的文件标识符集
 * @param key_to_user 返回给DU的文件密钥集
 * @param uset_to_server 返回给服务器更新DU-文件授权关系的字典
****************************************/
void online_auth(SEARCH_KEY skey, USER_KEY ukey, FILE_DESC_LIST DOC, 
    DOCKEY_LIST &key_to_user, USET_DICT &uset_to_server);

/***************************************
* @brief 由DU授权给DU
* @param A_ukey 授权DU的密钥组
* @param B_ukey 被授权DU的密钥组
* @param DOC 要授权的文件标识符集
* @param User_AuthA 授权DU的被授权信息字典，组织形式为 文件标识符d-被授权信息组
* @param Dok_KeyA 授权DU的文件密钥集
* @param auth_to_userB 返回给被授权DU的被授权信息字典
* @param key_to_userB 返回给被授权DU的文件密钥集
****************************************/
void offline_auth(USER_KEY A_ukey, USER_KEY B_ukey, FILE_DESC_LIST DOC, 
    USER_AUTH_DICT User_AuthA, DOCKEY_LIST Doc_KeyA, 
    USER_AUTH_DICT &auth_to_userB, DOCKEY_LIST &key_to_userB);

/***************************************
 * @brief 生成搜索令牌
 * @param word 要搜索的关键词
 * @param ukey 搜索者DU的密钥组
 * @param Doc_Key 搜索者的文件密钥集
 * @param User_Auth 搜索者的被授权情况字典
 * @param query_list 返回的查询令牌集
 ***************************************/
void search_generate(keyword word, USER_KEY ukey, DOCKEY_LIST Doc_Key,
    USER_AUTH_DICT User_Auth, QUERY_LIST &query_list);

class SEARCH_KEY {
    public:
    std::byte K1[LAMBDA], K2[LAMBDA], K3[LAMBDA];

    SEARCH_KEY(std::byte *K[]) {

    }
};

class USER_KEY {
    public:
    std::byte KU[LAMBDA], KUT[LAMBDA];

    USER_KEY() {

    }
};

class DOCKEY_ITEM {
    public:
    FILE_DESC d;
    std:: byte Kd, Kd_enc;
    DOCKEY_ITEM() {

    }
};

class USER_AUTH_ITEM{
    public:
    std::byte uid[LAMBDA];
    group_element offtok;
    std::vector<std::byte[LAMBDA]> AList;
    USER_AUTH_ITEM(){

    }
};

class QUERY_ITEM {
    public:
    std::byte uid[LAMBDA];
    group_element stk_d;
    std::vector<std::byte[LAMBDA]> AList;
    QUERY_ITEM() {
        
    }
};

class FILE_DESC{
    public:
    keyword words[MAX_WORD];
    //std:: string dec_flag = "CORRECT";
    FILE_DESC() {

    } 
};

class XSET_ITEM {
    public:
    group_element xwd;
    std::byte ywd[LAMBDA];
    XSET_ITEM() {

    }
};