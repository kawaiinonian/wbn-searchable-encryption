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
    char path[PATH_LEN];
    uint8_t dec_flag[8] = "CORRECT";
    FILE_DESC() {
        memset(words, 0, sizeof(words));
        memset(path, 0, sizeof(path));
        keywords_len = 0;
    } 
    ~FILE_DESC() {
        delete words;
        delete &keywords_len;
        delete path;
        delete dec_flag;
    }
    void serialize(uint8_t *result) {
        memcpy(result, words, sizeof(words));
        memcpy(result+sizeof(words), path, sizeof(path));
        memcpy(result+sizeof(words)+sizeof(path), &keywords_len, sizeof(int));
        memcpy(result+sizeof(words)+sizeof(path)+sizeof(int), dec_flag, sizeof(dec_flag));
    }
};

class SEARCH_KEY {
    public:
    uint8_t K1[LAMBDA], K2[LAMBDA], K3[LAMBDA];

    SEARCH_KEY() {
        memset(K1, 0, sizeof(K1));
        memset(K2, 0, sizeof(K2));
        memset(K3, 0, sizeof(K3));
    }
    ~SEARCH_KEY() {
        delete K1, K2, K3;
    }
};

class USER_KEY {
    public:
    uint8_t KU[LAMBDA], KUT[LAMBDA];

    USER_KEY() {
        memset(KU, 0, sizeof(KU));
        memset(KUT, 0, sizeof(KUT));
    }
    ~USER_KEY() {
        delete KU, KUT;
    }
};

class DOCKEY_ITEM {
    public:
    uint8_t Kd_enc[LAMBDA];
    fp_t Kd;
    DOCKEY_ITEM() {
        memset(Kd_enc, 0, sizeof(Kd_enc));
        memset(Kd, 0, sizeof(Kd));
    }
    ~DOCKEY_ITEM() {
        delete Kd_enc, Kd;
    }
};

class USER_AUTH_ITEM {
    public:
    fp_t uid, offtok;
    //std::vector<std::byte[LAMBDA]> AList;
    USER_AUTH_ITEM() {
        memset(uid, 0, sizeof(uid));
        memset(offtok, 0, sizeof(offtok));
    }
    ~USER_AUTH_ITEM() {
        delete uid, offtok;
    }
};

class QUERY_ITEM {
    public:
    fp_t uid, stk_d;
    //std::vector<std::byte[LAMBDA]> AList;
    QUERY_ITEM() {
        memset(uid, 0, sizeof(uid));
        memset(stk_d, 0, sizeof(stk_d));
    }
    ~QUERY_ITEM() {
        delete uid, stk_d;
    }
};

class XSET_ITEM {
    public:
    fp_t xwd;
    uint8_t ywd[FILE_DESC_LEN];
    XSET_ITEM() {
        memset(xwd, 0, sizeof(xwd));
        memset(ywd, 0, sizeof(ywd));
    }
    ~XSET_ITEM() {
        delete xwd, ywd;
    }
};

class ASET_ITEM {
    public:
    fp_t aid, trapgate, f_aid;
    std::vector<uint64_t *> c_aid;
    ASET_ITEM() {
        memset(aid, 0, sizeof(aid));
        memset(trapgate, 0, sizeof(trapgate));
        memset(f_aid, 0, sizeof(f_aid));
    }
    ~ASET_ITEM() {
        delete aid, trapgate, f_aid;
    }
};

class USET_ITEM {
    public:
    fp_t uid, ud;
    USET_ITEM() {
        memset(uid, 0, sizeof(uid));
        memset(ud, 0, sizeof(ud));
    }
    ~USET_ITEM() {
        delete uid, ud;
    }
};