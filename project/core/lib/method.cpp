#include "method.h"

char *read_file(const char *path, int &len) {
	FILE *fp;
	char *data;
 
	fp = fopen(path, "rb");
	if (fp == NULL) {
		return NULL;
	}

	fseek(fp, 0, SEEK_END);
	len = ftell(fp);
	data = (char *)malloc((len + 1) * sizeof(char));
	rewind(fp);
	len = fread(data, 1, len, fp);
	data[len] = '\0';
	fclose(fp);

    return data;
}

int write_file(const char *path, char *data, int len) {
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

int f_aes_cbc_enc(const char *path, uint8_t *key, int key_len, uint8_t *iv) {

    return 0;
}

int f_aes_cbc_dec(const char *path, uint8_t *key, int key_len, uint8_t *iv) {

    return 0;
}

int main() {
    int len;
    char *data = read_file("1.txt", len);

    cout << data << endl;
    cout << len << endl;

    write_file("2.txt", data, len);

    return 0;
}