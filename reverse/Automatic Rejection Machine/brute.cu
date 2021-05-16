#include <stdio.h>
#include <stdint.h>

#define LENGTH(a) (sizeof(a) / sizeof(a[0]))

typedef struct hash_res {
        uint64_t a;
        uint64_t b;
#ifdef __cplusplus
        __device__ __host__ bool operator== (hash_res h) {
                return a = h.a && b == h.b;
        }
#endif
} HashRes;

__device__ HashRes somehash(int a, int b, int c) {
        HashRes h;
        int i;
        uint64_t r[4];
        uint64_t cv;


        h.a = a | (b << 8) | (c << 16) | 0xAABBCCDD11000000LL;
        h.b = 0x9E3779B912881288LL;

        r[0] = 0xDEADBEEFFEEDBEEFLL;
        r[1] = 0x1BADB002FACECAFELL;
        r[2] = 0xFEEDFACE08920892LL;
        r[3] = 0xCAFEFEED12401240LL;
        for (i = 0; i <= 0xf; ++i) {
                r[i & 3] = r[0] + r[1] + ((r[2] + r[3]) ^ (r[0] << (r[2] & 0x3f)));
                cv = r[i & 3];
                h.a += ((cv + h.b) << 9) ^ (cv - h.b) ^ ((cv + h.b) >> 14);
                h.b += ((cv + h.a) << 9) ^ (cv - h.a) ^ ((cv + h.a) >> 14);
        }
        return h;
}

__global__ void kernel(HashRes target, char *res) {
        uint64_t i;
        char a, b, c;
        const int index = threadIdx.x + (blockIdx.x<<10);
        const int stride = gridDim.x<<10;

        for (i = index; i < 0x1000000; i += stride) {
                a = (i >>  0) & 0xff;
                b = (i >>  8) & 0xff;
                c = (i >> 16) & 0xff;
                if (somehash(a, b, c) == target) {
                        res[0] = a;
                        res[1] = b;
                        res[2] = c;
                }
        }
}

void someshuffle(int *a) {
        int i;
        int j;
        int tmp;
        int dest[] = {0x0, 0x2, 0xb, 0x6, 0x4, 0x5, 0x3, 0x7, 0x8, 0x9, 0xa, 0x1, 0xc, 0x16, 0x18, 0xf, 0x11, 0x10, 0x12, 0x13, 0x17, 0x14, 0xd, 0x15, 0xe, 0x1d, 0x1c, 0x1b, 0x1a, 0x19};

        for (i = 0; i < 30; ++i) {
                for (j = i; dest[j] >= 0; j = tmp) {
                        tmp = a[i];
                        a[i] = a[dest[j]];
                        a[dest[j]] = tmp;
                        tmp = dest[j];
                        dest[j] = tmp - 30;
                }
        }
}

int main() {
        const HashRes targets[] = {
                {0xB4D8846071AC9EE5LL, 0x1E1FF00814E134FELL},
                {0x6B198E7941B7002ELL, 0xBC6FA839EFE36443LL},
                {0xC3C71AD9A664B6C3LL, 0x5692A2F09C98D986LL},
                {0xF084A1A59CD01E68LL, 0xBC52E78A7E4DF2DFLL},
                {0xDA219D93290B91A8LL, 0x5703D0286FA5D32FLL},
                {0x6274B1B118DA82B2LL, 0xA746EBFB0954EBBCLL},
                {0x5F6DF7BD4F1967A2LL, 0x16D5B5BDEE98CF8ELL},
                {0x52E8B6DF7E62E39ALL, 0x99F9455FB0C8D933LL},
                {0x5FFD82D53AF933DLL, 0xFF9084A16FF0141CLL},
                {0xE17C5F0781D52F9BLL, 0x1A0F4431548E51D1LL},
                {0xF2E8573D8F0F01DDLL, 0x250039177F4DEF91LL},
                {0x8851491ECBC7AF7CLL, 0xAD427C6695B91D24LL},
                {0x5E0071D97D98D094LL, 0x264DDA52B0C37B03LL},
                {0xA5811271D6D7C428LL, 0xE0133FC719F34136LL},
                {0xE508ACE2412B2633LL, 0x74321A3E9FACE34CLL},
                {0xFF5B8A59E8EBF70BLL, 0x76275A516F88C986LL},
                {0x1604D76F74599CC4LL, 0xF744BCD8F2016F58LL},
                {0xA0B6A7A0239E4EA7LL, 0xF1EFC57F15CB9AB4LL},
                {0xB0D1AD4FB4ED946ALL, 0x81CA31324D48E689LL},
                {0xE6A9979C51869F49LL, 0xA666637EE4BC2457LL},
                {0x6475B6AB4884B93CLL, 0x5C033B1207DA898FLL},
                {0xB66DC7E0DEC3443ELL, 0xE4899C99CFA0235CLL},
                {0x3B7FD8D4D0DCAF6BLL, 0xB1A4690DB34A7A7CLL},
                {0x8041D2607129ADABLL, 0xA6A1294A99894F1ALL},
                {0xDDE37A1C4524B831LL, 0x3BC8D81DE355B65CLL},
                {0x6C61AB15A63AD91ELL, 0x8FA4E37F4A3C7A39LL},
                {0x268B598404E773AFLL, 0x74F4F040AE13F867LL},
                {0x4DF78E91FD682404LL, 0xABE1FC425A9A671ALL},
                {0x1BB06615C8A31DD5LL, 0x9F56E9AEF2FA5D55LL},
                {0x239DCF030B3CE09BLL, 0x24556A34B61CA998LL},
        };
        int i;
        char *ans;
        char shuffled_flag[LENGTH(targets)] = {0};
        char flag[LENGTH(targets) + 1] = {0};
        int shuffle_order[LENGTH(targets) + 1] = {0};

        int device_id;
        int smcount;

        cudaGetDevice(&device_id);
        cudaDeviceGetAttribute(&smcount, cudaDevAttrMultiProcessorCount, device_id);


        cudaMallocManaged(&ans, 3);
        for (i = 0; i < LENGTH(targets); i++) {
                kernel<<<smcount, 1024>>>(targets[i], ans);
                cudaDeviceSynchronize();
                shuffled_flag[i] = ans[0];
        }
        cudaFree(ans);


        for (i = 0; i < LENGTH(targets); i++) {
                shuffle_order[i] = i;
        }

        someshuffle(shuffle_order);

        for (i = 0; i < LENGTH(targets); i++) {
                flag[shuffle_order[i]] = shuffled_flag[i];
        }
        puts(flag);
}
