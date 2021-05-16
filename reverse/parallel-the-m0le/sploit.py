#!/usr/bin/env python3

L = 16

def func1(s):
    for i in range(0, L, 4):
        s[i], s[i + 3] = s[i + 3], s[i]
        s[i], s[i + 1] = s[i + 1], s[i]

def func1_re(s):
    for i in range(0, L, 4):
        s[i], s[i + 1] = s[i + 1], s[i]
        s[i], s[i + 3] = s[i + 3], s[i]

def func2(s):
    for i in range(L // 2):
        s[i] ^= s[L - i - 1]

def func3(s):
    for i in range(L):
        s[i] = (s[i] >> (8 - i % 8)) | (s[i] << (i % 8))
        s[i] %= 256

def func3_re(s):
    for i in range(L):
        s[i] = (s[i] >> (i % 8)) | (s[i] << (8 - i % 8))
        s[i] %= 256

def func4(s):
    for i in range(L // 2):
        s[L - i - 1] ^= s[i]

xor = b"{reverse_fake_flag}ptm"

def func5(s):
    for i in range(L):
        s[i] ^= xor[i]

def func6(s):
    for i in range(L):
        s[i] ^= 255

def func7(s):
    for i in range(L):
        v3 = s[i]
        v5 = 7
        j = v3 >> 1
        while j != 0:
            v3 = j & 1 | (2 * v3)
            v5 -= 1
            j >>= 1
        s[i] = v3 << v5
        s[i] %= 256

def func8(s):
    for i in range(L // 2):
        s[i], s[L - i - 1] = s[L - i - 1], s[i]

def func9(s):
    for i in range(L):
        s[i] += 42
        s[i] %= 256

def func9_re(s):
    for i in range(L):
        s[i] -= 42
        s[i] %= 256

def func10(s):
    for i in range(L):
        s[i] = (16 * s[i]) | (s[i] >> 4) & 0xF
        s[i] %= 256

def func11(s):
    for i in range(L):
        s[i] = (4 * s[i]) & 0x20 | (2 * s[i]) & 0x40 | s[i] & 0x80 | (8 * s[i]) & 0x10 | (((8 * s[i]) & 0x20 | (4 * s[i]) & 0x40 | (2 * s[i]) & 0x80 | (16 * s[i]) & 0x10) >> 4)
        s[i] %= 256

def func12(s):
    for i in range(L):
        s[i] = ~(i ^ s[i])
        s[i] %= 256

def func12_re(s):
    for i in range(L):
        s[i] = ~s[i] ^ i
        s[i] %= 256

def func13(s):
    for i in range(L):
        s[i] = (i + s[i]) % 256

def func13_re(s):
    for i in range(L):
        s[i] = (s[i] - i) % 256

def func14(s):
    for i in range(L):
        if ord('a') <= s[i] <= ord('z'):
            s[i] -= 0x20
        elif ord('A') <= s[i] <= ord('Z'):
            s[i] += 0x20

def I(f):
    return f

def R(f):
    d = {}
    for i in range(0, 256, 16):
        data = [j for j in range(i, i + 16)]
        f(data)
        for j in range(16):
            d[data[j]] = i + j
    def fr(s):
        for i in range(L):
            s[i] = d[s[i]]
    return fr

rf = [
    func1_re,
    I(func2),
    func3_re,
    I(func4),
    I(func5),
    I(func6),
    R(func7),
    I(func8),
    func9_re,
    R(func10),
    R(func11),
    func12_re,
    func13_re,
    I(func14),
]

from itertools import combinations, permutations
from tqdm import tqdm

data = b"".fromhex("2aad2e5a49fb2d9adb908dd00eb48c8a6607ab619f75b0272f3c1eb33fe9edaf")

part1 = list(data[:16])
part2 = list(data[16:])

for c in tqdm(list(combinations(enumerate(rf), len(rf) // 2))):
    for p in permutations(c):
        data1 = part1.copy()
        for _, f in p:
            f(data1)
        data2 = part2.copy()
        for _, f in p[::-1]:
            f(data2)

        if data1 == data2:
            indexes = set(range(len(rf)))
            for i, _ in p:
                indexes -= {i}
            for lp in permutations(indexes):
                data = data1.copy()
                for i in lp:
                    rf[i](data)
                data = bytes(data)
                if data.startswith(b"ptm{"):
                    print(data.decode())
                    exit(0)
