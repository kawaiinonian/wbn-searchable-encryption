#include "method.h"

uint8_t *read_file(const char *path, size_t &len) {
	FILE *fp;
	uint8_t *data;
 
	fp = fopen(path, "rb");
	if (fp == NULL) {
		return NULL;
	}

	fseek(fp, 0, SEEK_END);
	len = ftell(fp);
	data = (uint8_t *)malloc((len + 1) * sizeof(uint8_t));
	rewind(fp);
	len = fread(data, 1, len, fp);
	data[len] = '\0';
	fclose(fp);

    return data;
}

int write_file(const char *path, uint8_t *data, size_t len) {
    FILE * fp = fopen(path, "wb");
    if (fp) {
        assert(len = fwrite(data, 1, len, fp));
        fclose(fp);
        return 0;
    } else {
        return 1;
    }
    
    return 0;
}

int f_aes_cbc_enc(const char *in_path, const char *out_path, const uint8_t *key, size_t key_len, const uint8_t *iv) {
    FILE *fp;
    uint8_t *plaintxt, *ciphertxt;
    size_t in_len, out_len;

    plaintxt = (uint8_t *)read_file(in_path, in_len);
    if (plaintxt == NULL) {
        return 1;
    }

    if (bc_aes_cbc_enc(ciphertxt, &out_len, plaintxt, in_len, key, key_len, iv)) {
        // uint8_t *p1, *p2;
        // for (p1 = p2 = (uint8_t *)path; p1 != '\0'; p1++) {
        //     if (*p1 == '/') {
        //         p2 = p1;
        //     }
        // }
        if (!write_file(out_path, ciphertxt, out_len)) {
            return 1;
        }
    }

    return 0;
}

int f_aes_cbc_dec(const char *in_path, const char *out_path, const uint8_t *key, size_t key_len, const uint8_t *iv) {
    FILE *fp;
    uint8_t *ciphertxt, *plaintxt;
    size_t in_len, out_len;

    ciphertxt = (uint8_t *)read_file(in_path, in_len);
    if (ciphertxt == NULL) {
        return 1;
    }

    if (bc_aes_cbc_dec(plaintxt, &out_len, ciphertxt, in_len, key, key_len, iv)) {
        if (!write_file(out_path, plaintxt, out_len)) {
            return 1;
        }
    }

    return 0;
}

int main() {
    const char *path = "1.txt";
    const char *enc_path = "enc.txt";
    const char *dec_path = "dec.txt";
    uint8_t *seed = (uint8_t *)"1234567812345678123456781234567812345678123456781234567812345678";
    size_t key_len = 64;
    uint8_t *key = (uint8_t *)malloc((key_len + 1) * sizeof(uint8_t));
    uint8_t *iv = (uint8_t *)malloc((key_len + 1) * sizeof(uint8_t));

    rand_init();
    rand_seed(seed, RLC_RAND_SEED);
    rand_bytes(key, key_len);
    rand_bytes(iv, key_len);

    if (f_aes_cbc_enc(path, enc_path, key, key_len, iv)) {
        cout << "Encryption Success!" << endl;
    }

    if (f_aes_cbc_dec(enc_path, dec_path, key, key_len, iv)) {
        cout << "Decryption Success!" << endl;
    }
    
    return 0;
}