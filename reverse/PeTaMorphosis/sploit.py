#!/usr/bin/env python3

from subprocess import check_output
import string

def enc(data):
    with open("flag.txt", "wb") as f:
        f.write(data)
    check_output(["./chall"])
    with open("out.txt", "rb") as f:
        return f.read()

L = 39
with open("out", "rb") as f:
    need_enc = f.read()
a_enc = enc(b"A" * L)
positions = []
for i in range(L):
    b_enc = enc(b"A" * i + b"B" + b"A" * (L - i - 1))
    for j in range(L):
        if a_enc[j] != b_enc[j]:
            positions.append(j)


al = string.ascii_letters + string.digits + "}{!@#$%^&*()_"

cur = b""
for i in range(L):
    for j in al:
        f_enc = enc(b"A" * i + j.encode() + b"A" * (L - i - 1))
        if len(f_enc) != L:
            continue
        if f_enc[positions[i]] == need_enc[positions[i]]:
            cur += j.encode()
            break

print(cur)
