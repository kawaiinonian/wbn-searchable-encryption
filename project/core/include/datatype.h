#include <relic/relic_fp.h>

#include <string>
#include <map>
#include <vector>

class FILE_DESC;
class SEARCH_KEY;
class USER_KEY;
class DOCKEY_ITEM;
class USER_AUTH_ITEM;
class QUERY_ITEM;
class XSET_ITEM;
class ASET_ITEM;
class USET_ITEM;

// typedef CryptoPP::SecByteBlock fp_t;
typedef std::map<uint8_t*, USER_AUTH_ITEM> USER_AUTH_DICT;
typedef std::vector<QUERY_ITEM> QUERY_LIST;
typedef std::map<uint8_t*, DOCKEY_ITEM> DOCKEY_DICT;
typedef std::vector<USET_ITEM> USET_LIST;
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::vector<FILE_DESC> FILE_DESC_LIST;
typedef std::vector<ASET_ITEM> ASET_LIST;
// to be changed: for coding with no error
// typedef std::vector<std::string> keyword;
// typedef std::string keyword;

class FILE_DESC {
    public:
    uint8_t words[MAX_WORD][WORD_LEN];
    int keywords_len;
    std::string dec_flag = "CORRECT";
    FILE_DESC() {

    } 
    void serialize(uint8_t *result) {

    }
};

class SEARCH_KEY {
    public:
    uint8_t K1[LAMBDA], K2[LAMBDA], K3[LAMBDA];

    SEARCH_KEY() {

    }
};

class USER_KEY {
    public:
    uint8_t KU[LAMBDA], KUT[LAMBDA];

    USER_KEY() {

    }
};

class DOCKEY_ITEM {
    public:
    uint8_t Kd_enc[LAMBDA];
    fp_t Kd;
    DOCKEY_ITEM() {

    }
};

class USER_AUTH_ITEM {
    public:
    fp_t uid, offtok;
    //std::vector<std::byte[LAMBDA]> AList;
    USER_AUTH_ITEM() {

    }
};

class QUERY_ITEM {
    public:
    int aid_flag;
    fp_t uid, stk_d;
    //std::vector<std::byte[LAMBDA]> AList;
    QUERY_ITEM() {
        
    }
};

class XSET_ITEM {
    public:
    fp_t xwd;
    uint8_t ywd[FILE_DESC_LEN];
    XSET_ITEM() {

    }
};

class ASET_ITEM {
    public:
    fp_t aid, trapgate, f_aid;
    // std::vector<fp_t> c_aid;
    ASET_ITEM() {
        
    }
};

class USET_ITEM {
    public:
    fp_t uid, ud;
};