#!/usr/bin/env python3.8

def encrypt_data(plaintext):
    from pwn import remote
    from hashlib import sha256
    
    with remote('challs.m0lecon.it', 2561) as io:
        line = io.recvline().strip().decode()
        words = line.split(' ')
        prefix = words[6]
        suffix = words[13][:-1]

        for i in range(10000000000):
            candidate = prefix + str(i)
            
            if sha256(candidate.encode()).hexdigest().endswith(suffix):
                break
        
        io.sendline(candidate.encode())

        io.recvline()
        io.sendline(plaintext.hex().encode())
        return bytes.fromhex(io.recvline().strip().decode())
    

def bytes_to_bit_string(data):
    return ''.join(bin(byte)[2:].zfill(8) for byte in data)


def bit_string_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


def xor_bit_strings(s1, s2):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(s1, s2))


plaintext = b'\x00' * 1000
ciphertext = encrypt_data(plaintext)
keystream = bytes_to_bit_string(ciphertext[:1000])
encrypted_flag = bytes_to_bit_string(ciphertext[1000:])

for start in range(1, len(keystream)):
    suffix = keystream[start:]

    if keystream.count(suffix) > 1:
        index = keystream.find(suffix)
        key = keystream[index + len(suffix):]
        flag = xor_bit_strings(encrypted_flag, key)
        print(bit_string_to_bytes(flag))

# run it several time to get the flag
