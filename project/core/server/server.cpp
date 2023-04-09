#include "server.h"
#ifdef DEBUG
typedef std::vector<ASET_ITEM> ASET_LIST;
#endif

void Aset_update(ASET_LIST &Aset, ASET_ITEM aitem) {
    int i, j, k;
    int cmp1, cmp2;

    cmp1 = cmp2 = 1;
    for (k = 0; k < Aset.size(); k++) {
        if (cmp1 != 0) {
            cmp1 = memcmp(Aset[k].aid, aitem.aid, LAMBDA); // check aid
            if (cmp1 == 0) i = k;
        }
        if (cmp2 != 0) {
            cmp2 = memcmp(Aset[k].aid, aitem.f_aid, LAMBDA); // check f_aid
            if (cmp2 == 0) j = k;
        }
        if (cmp1 == 0 && cmp2 == 0) { // both found
            break;
        }
    }

    if (cmp1 != 0) { // if ASet[aid] is NULL, then init
        Aset.push_back(aitem);
        i = k;
    }

    if (cmp2 == 0) { // if f_aid found
        Aset[j].c_aid.push_back(Aset[i].aid);
        fp_mul_comba(Aset[i].trapgate, Aset[i].trapgate, Aset[j].trapgate);
    }

    return;
}

void search(QUERY_LIST query, fp_t aid, ASET_LIST Aset, USET_LIST Uset, XSET_LIST Xset,
    std::vector<uint8_t *> &query_response) {
    fp_t x;
    int i, j, cmp;

    for (i = 0; i < query.size(); i++) {
        cmp = 1;
        for (j = 0; j < Uset.size(); j++) {
            cmp = memcmp(Uset[j].uid, query[i].uid, LAMBDA);
            if (cmp == 0) {
                break;
            }
        }
        assert(cmp == 0);

        fp_mul_comba(x, query[i].stk_d, Uset[j].ud);
        if (aid) { // if aid works
            cmp = 1;
            for (j = 0; j < Aset.size(); j++) {
                cmp = memcmp(Aset[j].aid, aid, LAMBDA);
                if (cmp == 0) {
                    break;
                }
            }
            assert(cmp == 0);
            fp_mul_comba(x, x, Aset[j].trapgate);
        }

        cmp = 1;
        for (j = 0; j < Xset.size(); j++) {
            cmp = memcmp(Xset[j].xwd, x, LAMBDA);
            if (cmp == 0) {
                break;
            }
        }
        assert(cmp == 0);
        query_response.push_back(Xset[j].ywd);
    }

    return;
}

int main() {
    ASET_LIST Aset;
    ASET_ITEM a1, a2;

    setting_init();

    memset(a1.aid, 0, LAMBDA);
    memset(a1.trapgate, 0, LAMBDA);

    memset(a2.aid, 1, LAMBDA);
    memset(a1.trapgate, 1, LAMBDA);
    memset(a2.f_aid, 0, LAMBDA);

    Aset.push_back(a1);
    Aset.push_back(a2);

    ASET_ITEM in;
    memset(in.aid, 1, LAMBDA);
    memset(in.trapgate, 1, LAMBDA);
    memset(in.f_aid, 0, LAMBDA);
    Aset_update(Aset, in);

    return 0;
}