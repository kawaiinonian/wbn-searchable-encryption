#include <cryptlib.h>
#include <aes.h>


#include <string>
#include <map>
#include <vector>

typedef std::map<FILE_DESC, USER_AUTH_ITEM> USER_AUTH_DICT;
typedef std::vector<QUERY_ITEM> QUERY_LIST;
typedef std::vector<DOCKEY_ITEM> DOCKEY_LIST;
typedef std::map<std::byte[LAMBDA], std::byte[LAMBDA]> USET_DICT;
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::vector<FILE_DESC> FILE_DESC_LIST;
typedef std::map<std::byte[LAMBDA], group_element> ASET_DICT;
// to be changed: for coding with no error
typedef int group_element;
typedef std::string keyword;

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
    std::byte Kd, Kd_enc;
    DOCKEY_ITEM() {

    }
};

class USER_AUTH_ITEM{
    public:
    std::byte uid[LAMBDA];
    group_element offtok;
    //std::vector<std::byte[LAMBDA]> AList;
    std::byte aid[LAMBDA];
    USER_AUTH_ITEM(){

    }
};

class QUERY_ITEM {
    public:
    std::byte uid[LAMBDA];
    group_element stk_d;
    //std::vector<std::byte[LAMBDA]> AList;
    std::byte aid[LAMBDA];
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

class ASET_ITEM {
    public:
    std::byte aid[LAMBDA];
    group_element trapgate;
    ASET_ITEM() {
        
    }
}