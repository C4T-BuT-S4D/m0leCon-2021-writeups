from pwn import *
from hashlib import sha256
import itertools
from dataclasses import dataclass
import time

context.log_level = "DEBUG"

r = remote("challs.m0lecon.it", 5886)

r.recvuntil("Give me a string starting with ")
pref = r.recvuntil(' ')[:-1].decode()
r.recvuntil("sha256sum ends in ")
end = r.recvline()[:-2].decode()

i = 0

while True:
    s = pref + str(i)
    if sha256(s.encode()).hexdigest().endswith(end):
        break
    i += 1

r.sendline(s)
r.sendafter("Time limit is one second for each test.\n", "\n")


@dataclass
class D:
    total: int
    ml: int


def stupid(cur, ds):
    result = 10 ** 10
    for perm in itertools.permutations(ds):
        mn = 0
        curr = cur
        for d in perm:
            mn = max(mn, curr + d.ml)
            curr += d.total
        result = min(result, mn)
    return result


cache = set()
start = 0


def brute(left, cur, ans):
    if time.time() - start > 0.65:
        return

    if (left, cur) in cache:
        return
    else:
        cache.add((left, cur))

    global best

    if len(left) < 5:
        best = min(best, max(stupid(cur, [ds[i] for i in left]), ans))
        return

    for i in left:
        d = ds[i]
        nans = max(ans, cur + d.ml)
        if nans >= best:  # cannot optimize more anyway
            continue

        ncur = cur + d.total
        brute(left - {i}, ncur, nans)


iter_number = 0
while True:
    iter_number += 1
    cache = set()
    n = int(r.recvline().decode().strip())
    start = time.time()
    ds = []

    max_lefts = []
    totals = []

    for i in range(n):
        cur = r.recvline().decode().rstrip()

        pos = 0
        lpos = 0
        for c in cur:
            if c == 'L':
                pos += 1
            else:
                pos -= 1
            lpos = max(lpos, pos)

        ds.append(D(ml=lpos, total=pos))

    if len(ds) < 10:
        r.sendline(str(stupid(0, ds)))
        r.recvline()
        continue

    ds.sort(key=lambda x: x.total)
    i = 0
    while i < len(ds) and ds[i].total <= 0:
        i += 1
    ds = sorted(ds[:i], key=lambda x: x.ml) + sorted(ds[i:], key=lambda x: x.ml, reverse=True)
    new_ds = []
    cur = 0
    for d in ds:
        if d.ml >= 0:
            cur += d.total
        else:
            new_ds.append(d)

    best = 0
    cur = 0
    for d in ds:
        best = max(best, cur + d.ml)
        cur += d.total

    brute(frozenset(range(len(ds))), 0, 0)

    r.sendline(str(best))
    r.recvline()
    print('----', iter_number, '----')
