#include <server.h>

void Aset_update(ASET_LIST &Aset, ASET_LIST tmpAset) {
    int i, j, cmp;

    for(i = 0; i < tmpAset.size(); i++) {
        cmp = 1;
        for (j = 0; j < Aset.size(); j++) {
            cmp = memcmp(Aset[j].aid, tmpAset[i].aid, 32);
            if (cmp == 0) {
                break;
            }
        }
        if (cmp == 0) {
            memcpy(Aset[j].trapgate, tmpAset[i].trapgate, 32);
        } else {
            ASET_ITEM 
        }
    }

    return;
}

void search(QUERY_LIST query, ASET_LIST Aset, USET_LIST Uset, XSET_LIST Xset,
    std::vector<uint8_t[FILE_DESC_LEN]> &query_response) {
    fp_t x;
    int i, j, cmp;

    for (i = 0; i < query.size(); i++) {
        cmp = 1;
        for (j = 0; j < Uset.size(); j++) {
            cmp = memcmp(Uset[j].uid, query[i].uid, 32);
            if (cmp == 0) {
                break;
            }
        }
        assert(cmp == 0);

        fp_mul_comba(x, query[i].stk_d, Uset[j].ud);
        if (query[i].aid_flag) { // if aid works
            cmp = 1;
            for (j = 0; j < Aset.size(); j++) {
                cmp = memcmp(Aset[j].aid, query[i].aid, 32);
                if (cmp == 0) {
                    break;
                }
            }
            assert(cmp == 0);
            fp_mul_comba(x, x, Aset[j].trapgate);
        }

        cmp = 1;
        for (j = 0; j < Xset.size(); j++) {
            cmp = memcmp(Xset[j].xwd, x, 32);
            if (cmp == 0) {
                break;
            }
        }
        assert(cmp == 0);
        query_response.push_back(Xset[j].ywd);
    }

    return;
}