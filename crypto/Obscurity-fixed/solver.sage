#!/usr/bin/env sage

def algorithm(stream):
    a = [None] * (len(stream) + 1)
    k = 1

    a[k - 1] = 1
    alpha = a[k - 1] * 2^(k - 1)

    f = (0, 2)
    g = (2^(k - 1), 1)

    def func(h):
        return alpha * h[1] - h[0]

    def add(x, y):
        return (x[0] + y[0], x[1] + y[1])

    def multiply(x, y):
        return (x[0] * y, x[1] * y)

    def big_f(x):
        return max(abs(x[0]), abs(x[1]))

    def find_d(func):
        min_d, min_result = None, 1 << 1024

        for d in range(-10001, 10001 + 1, 2):
            if d == 0:
                continue

            result = func(d)

            if abs(result) < min_result:
                min_d, min_result = d, abs(result)

        return min_d

    for bit in stream:
        a[k] = bit
        alpha += a[k] * 2^k

        if func(g) % (2^(k + 1)) == 0:
            f = multiply(f, 2)
        elif big_f(g) < big_f(f):
            d = find_d(lambda d: big_f(add(f, multiply(g, d))))
            g, f = add(f, multiply(g, d)), multiply(g, 2)
        else:
            d = find_d(lambda d: big_f(add(g, multiply(f, d))))
            g, f = add(g, multiply(f, d)), multiply(f, 2)
        
        k += 1

    return g


def bytes_to_bits(data):
    return sum([list(map(int, bin(byte)[2:].zfill(8))) for byte in data], [])


def bits_to_bytes(bits):
    return bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8))


def xor_bits(s1, s2):
    return [x ^^ y for x, y in zip(s1, s2)]


plaintext = b'Look, a new flag: ptm{'
ciphertext = bytes.fromhex('d51664d413ba62984baf680bf98d9cf797f6da473adb19cd041220ae25cc0a9e7cdce8588f26862cc2d270d9373c17db678d69ffb4280371927cf9144c0bbd526c721d54c3c8f1de1f3fa6e5c84ece35c1')

pt_bits = bytes_to_bits(plaintext)
ct_bits = bytes_to_bits(ciphertext)

keystream = xor_bits(pt_bits, ct_bits)

u, v = algorithm(keystream)

precision = len(ct_bits) + 1
Z = Zp(2, prec=precision)
approximation = Z(u) / Z(v)
key_bits = [int(approximation[i]) for i in range(precision)]

flag = xor_bits(key_bits[1:], ct_bits)
print(bits_to_bytes(flag))
