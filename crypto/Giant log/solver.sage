#!/usr/bin/env sage

import socket
import hashlib


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(60)
sock.connect(('challs.m0lecon.it', 6428))

file = sock.makefile('rw')

line = file.readline().strip().split(' ')
prefix = line[6]
ends = line[13][:-1]

for i in range(100000000000):
    cand = prefix + str(i)

    if hashlib.sha256(cand.encode()).hexdigest().endswith(ends):
        print(cand)
        break

file.write(cand + '\n')
file.flush()

print('connected')

line = file.readline().strip()
y = int(line, 16)

print(len(str(y)))
print(file.readline().strip())

p = 0x83f39daf527c6cf6360999dc47c4f0944ca1a67858a11bd915ee337f8897f36eff98355d7c35c2accdf4555b03a9552b4bf400915320ccd0ba60b0cb7fcad723
g = 0x15a5f7dec38869e064dd933e23c64f785492854fbe8a6e919d991472ec68edf035eef8c15660d1f059ca1600ee99c7f91a760817d7a3619a3e93dd0162f7474bbf

# declaration of p-adic integers ring with precision 1000 
Z = Zp(p, prec=1000)

# calculating the logarithm
x_Z = Z(y).log() / Z(g).log()

# lifting the solution to ordinary integers
x = x_Z.lift()

file.write(hex(x) + '\n')
file.flush()

print(file.readline().strip())
print(file.readline().strip())
print(file.readline().strip())

sock.close()
