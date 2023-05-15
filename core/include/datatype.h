#include "const.h"

extern "C" {
#include <relic/relic_fp.h>
}

#include <string>
#include <map>
#include <vector>

#include <cassert>
#include <cstring>

class FILE_DESC;
class SEARCH_KEY;
class USER_KEY;
class DOCKEY_ITEM;
class USER_AUTH_ITEM;
class QUERY_ITEM;
class XSET_ITEM;
class ASET_ITEM;
class USET_ITEM;
class file;

// typedef std::map<file, USER_AUTH_ITEM> USER_AUTH_DICT;
// typedef std::vector<QUERY_ITEM> QUERY_LIST;
// typedef std::map<file, DOCKEY_ITEM> DOCKEY_DICT;
// typedef std::vector<USET_ITEM> USET_LIST;
// typedef std::vector<XSET_ITEM> XSET_LIST;
// typedef std::vector<FILE_DESC> FILE_DESC_LIST;
// typedef std::vector<ASET_ITEM> ASET_LIST;
// to be changed: for coding with no error
// typedef std::vector<std::string> keyword;
// typedef std::string keyword;

// typedef struct {
//     uint8_t words[MAX_WORD][WORD_LEN];
//     int keywords_len;
//     char path[PATH_LEN];
// }fd;

// typedef struct {
//     uint8_t d[FILE_DESC_LEN];
//     uint8_t kd_enc[LAMBDA], kd[LAMBDA];
// }dockey;

// typedef struct {
//     uint8_t ud[LAMBDA], uid[LAMBDA];
// }uset;

// typedef struct {
//     uint8_t d[FILE_DESC_LEN];
//     uint8_t uid[LAMBDA], offtok[LAMBDA];
// }userauth;


// typedef struct {
//     uint8_t uid[LAMBDA], stk_d[LAMBDA];
// }query;

// class FILE_DESC {
//     public:
//     uint8_t words[MAX_WORD][WORD_LEN];
//     int keywords_len;
//     char path[PATH_LEN];
//     uint8_t dec_flag[8] = "CORRECT";
//     FILE_DESC(void) {
//         memset(words, 0, sizeof(words));
//         memset(path, 0, sizeof(path));
//         keywords_len = 0;
//     } 
//     FILE_DESC(fd *input) {
//         memset(words, 0, sizeof(words));
//         memset(path, 0, sizeof(path));
//         for (int i = 0; i < input->keywords_len; i++) {
//             memcpy(words[i], input->words[i], WORD_LEN);
//         }
//         keywords_len = input->keywords_len;
//         memcpy(path, input->path, PATH_LEN);
//     }
//     void serialize(uint8_t *result) {
//         memcpy(result, words, sizeof(words));
//         memcpy(result+sizeof(words), path, sizeof(path));
//         memcpy(result+sizeof(words)+sizeof(path), &keywords_len, sizeof(int));
//         memcpy(result+sizeof(words)+sizeof(path)+sizeof(int), dec_flag, sizeof(dec_flag));
//     }
// };


class file {
    public:
    uint8_t words[MAX_WORD][WORD_LEN];
    int wordlen;
    uint8_t d[PATH_LEN];
};


// class file {
//     public:
//     uint8_t data[FILE_DESC_LEN];
//     file(uint8_t *serialized) {
//         memcpy(data, serialized, FILE_DESC_LEN);
//     }
//     void serialize (uint8_t *d) const{
//         memcpy(d, data, FILE_DESC_LEN);
//     }
//     bool operator<(const file& other) const {
//     // 实现比较逻辑
//     // 返回值为 true 表示 this 对象小于 other 对象，否则返回 false
//         return std::memcmp(this->data, other.data, FILE_DESC_LEN) < 0;
//     }
// };

class SEARCH_KEY {
    public:
    uint8_t K1[LAMBDA], K2[LAMBDA], K3[LAMBDA];

    SEARCH_KEY(void) {
        memset(K1, 0, sizeof(K1));
        memset(K2, 0, sizeof(K2));
        memset(K3, 0, sizeof(K3));
    }
    SEARCH_KEY(uint8_t* _K1, uint8_t* _K2, uint8_t* _K3) {
        memcpy(K1, _K1, LAMBDA);
        memcpy(K2, _K2, LAMBDA);
        memcpy(K3, _K3, LAMBDA);
    }
};

class USER_KEY {
    public:
    uint8_t KU[LAMBDA], KUT[LAMBDA];

    USER_KEY() {
        memset(KU, 0, sizeof(KU));
        memset(KUT, 0, sizeof(KUT));
    }
};

class DOCKEY_ITEM {
    public:
    uint8_t Kd_enc[LAMBDA], Kd[LAMBDA];
    DOCKEY_ITEM(uint8_t Kd_enc[], uint8_t Kd[]) {
        memcpy(this->Kd, Kd, LAMBDA);
        memcpy(this->Kd_enc, Kd_enc, LAMBDA);
    }
};

class DOCKEY {
    public:
    uint8_t d[PATH_LEN], Kd_enc[LAMBDA], Kd[LAMBDA];
    DOCKEY(uint8_t d[], uint8_t Kd_enc[], uint8_t Kd[]) {
        memcpy(this->d, d, PATH_LEN);
        memcpy(this->Kd, Kd, LAMBDA);
        memcpy(this->Kd_enc, Kd_enc, LAMBDA);
    }
};


class USER_AUTH {
    public:
    uint8_t d[PATH_LEN], uid[LAMBDA], offtok[LAMBDA+1];
    //std::vector<std::byte[LAMBDA]> AList;
    USER_AUTH(uint8_t d[], uint8_t uid[], ep_t offtok) {
        memcpy(this->d, d, PATH_LEN);
        memcpy(this->uid, uid, LAMBDA);
        ep_write_bin(this->offtok, LAMBDA+1, offtok, true);
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
};

class XSET_ITEM {
    public:
    uint8_t xwd[LAMBDA+1], ywd[PATH_LEN+16];
    XSET_ITEM() {
        memset(xwd, 0, sizeof(xwd));
        memset(ywd, 0, sizeof(ywd));
    }
};

class ASET_ITEM {
    public:
    uint8_t aid[LAMBDA], trapgate[LAMBDA], f_aid[LAMBDA];
    ASET_ITEM() {
        memset(aid, 0, sizeof(aid));
        memset(trapgate, 0, sizeof(trapgate));
        memset(f_aid, 0, sizeof(f_aid));
    }
};

class USET_ITEM {
    public:
    uint8_t uid[LAMBDA], ud[LAMBDA];
    USET_ITEM() {
        memset(uid, 0, sizeof(uid));
        memset(ud, 0, sizeof(ud));
    }
};

class USER_AUTH_ITEM {
    public:
    uint8_t uid[LAMBDA], offtok[LAMBDA+1];
    USER_AUTH_ITEM(uint8_t uid[], uint8_t offtok[]) {
        memcpy(this->uid, uid, LAMBDA);
        memcpy(this->offtok, offtok, LAMBDA+1);
    }
    // ~USER_AUTH_ITEM() {
    //     // delete []this->uid;
    //     ep_free(this->offtok);
    // }
};

struct Uint8ArrayComparator {
    bool operator()(const uint8_t* a, const uint8_t* b) const {
        for (size_t i = 0; i < arraySize; ++i) {
            if (a[i] < b[i]) {
                return true;
            }
            if (a[i] > b[i]) {
                return false;
            }
        }
        return false;
    }
    static constexpr size_t arraySize = PATH_LEN;  // 根据实际需求调整数组大小
};

class TOKEN {
    public:
    uint8_t uid[LAMBDA], stk[LAMBDA+1];
    TOKEN(uint8_t uid[], ep_t stk) {
        memcpy(this->uid, uid, LAMBDA);
        ep_write_bin(this->stk, LAMBDA+1, stk, true);
    }
};