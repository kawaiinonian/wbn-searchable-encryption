

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

typedef CryptoPP::SecByteBlock KEY;
typedef std::map<FILE_DESC, USER_AUTH_ITEM> USER_AUTH_DICT;
typedef std::vector<QUERY_ITEM> QUERY_LIST;
typedef std::vector<DOCKEY_ITEM> DOCKEY_LIST;
typedef std::map<KEY, KEY> USET_DICT;
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::vector<FILE_DESC> FILE_DESC_LIST;
typedef std::map<KEY, KEY> ASET_DICT;
// to be changed: for coding with no error
typedef std::vector<std::string> keyword;

class FILE_DESC {
    public:
    keyword words;
    std::string dec_flag = "CORRECT";
    FILE_DESC() {

    } 
};

class SEARCH_KEY {
    public:
    KEY K1, K2, K3;

    SEARCH_KEY() {

    }
};

class USER_KEY {
    public:
    KEY KU, KUT;

    USER_KEY() {

    }
};

class DOCKEY_ITEM {
    public:
    FILE_DESC d;
    KEY Kd, Kd_enc;
    DOCKEY_ITEM() {

    }
};

class USER_AUTH_ITEM {
    public:
    KEY uid, offtok, aid;
    //std::vector<std::byte[LAMBDA]> AList;
    USER_AUTH_ITEM() {

    }
};

class QUERY_ITEM {
    public:
    KEY uid, stk_d, aid;
    //std::vector<std::byte[LAMBDA]> AList;
    QUERY_ITEM() {
        
    }
};

class XSET_ITEM {
    public:
    KEY xwd, ywd;
    XSET_ITEM() {

    }
};

class ASET_ITEM {
    public:
    KEY aid, trapgate;
    ASET_ITEM() {
        
    }
};