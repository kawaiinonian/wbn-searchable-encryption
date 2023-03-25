#define LAMBDA 256
#define MAX_WORD 128


typedef std::map<FILE_DESC, USER_AUTH_ITEM> USER_AUTH_DICT;
typedef std::vector<QUERY_ITEM> QUERY_LIST;
typedef std::vector<DOCKEY_ITEM> DOCKEY_LIST;
typedef std::map<std::byte[], std::byte[]> USET_DICT;
typedef std::vector<XSET_ITEM> XSET_LIST;
typedef std::vector<FILE_DESC> FILE_DESC_LIST;
// to be changed: for coding with no error
typedef int group_element;
typedef std::string keyword;