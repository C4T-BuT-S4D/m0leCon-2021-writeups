# m0leCon CTF 2021 Teaser — Alternating key exchange

## Challenge information

![task title](images/task-title.png)

## Files

### **chall.sage**:

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import random

n = 20
m = 42
G = AlternatingGroup(n)

pub_a = [G.random_element() for _ in range(m)]
pub_b = [G.random_element() for _ in range(m)]

eps_a = [random.choice([1,-1]) for _ in range(m)]
eps_b = [random.choice([1,-1]) for _ in range(m)]

A = prod([x^e for x,e in zip(pub_a, eps_a)])
B = prod([x^e for x,e in zip(pub_b, eps_b)])

abar = [A^(-1) * x * A for x in pub_b]
bbar = [B^(-1) * x * B for x in pub_a]

print(pub_a)
print(pub_b)
print(abar)
print(bbar)

K = A^(-1)*B^(-1)*A*B
shared = "_".join(str(K(i)) for i in range(1,n+1))
dig = sha256(shared.encode()).digest()
key = dig[:16]
iv = dig[16:]
aes = AES.new(key, AES.MODE_CBC, iv=iv)
with open("flag.txt", "rb") as f:
    flag = f.read()
flag_enc = aes.encrypt(pad(flag,16))
print(flag_enc.hex())
```

### **output.txt**:

```
[(1,7,9,12,3,19,16)(2,14,6,10,15)(4,18,5,11,8)(13,20,17), (1,20,3,12,4,13)(5,10,17)(6,19,14,9,18,16,7,8,15,11), (1,12,17,13,19,18,6)(2,14,15,7,3,5,11,4,16,8,9,10,20), (1,12,9,14,2,15,8,4,13,16,19,3,20)(5,18,10,6,7,11,17), (1,2,14,9,6,11,19,13,8,20)(3,7,18,10,17)(4,12)(5,16,15), (1,18,4,20,6,19,14)(2,3,17,5,11,15,7,16,12)(8,10,9), (1,9,17,2,4,5,15)(3,11,19,6,7,20,10,14,12,18,13,8,16), (1,8,6,10,17,20,15,5,18,14,13,11,9,2,16,4)(3,19,7,12), (1,18,8,3,16,11,17,19,7,2,12,10,15,14,4,20,6,13)(5,9), (1,6,5,7,8,18,2)(3,17,4,14,12,11,13,20,15,16,19,10,9), (2,13,16,5,8,20,3,18,17,6,14,10,4,12,19,7)(9,15), (1,16,6,19,13,9,15,10,2,18,14,11,17)(3,7,4,20,12), (1,11,3,6,19)(2,12,9,10,16,4,15,8,13,7,20)(5,14,17), (1,9,11,13,17,7,2,18,16,14,15)(3,4,10,8,5)(6,19)(12,20), (1,8,4,3,20,14,18)(2,13,17,6,9,12,7,11,15,19,10,5,16), (1,15,6,18,3,4,20,13,10,7,11,14,17)(2,19)(5,8,12)(9,16), (1,14,11,8,3,12,15,16,7,10,20,18,9)(2,5,13)(6,19,17), (1,2,10,11,9,8,14,15,17,6,18,7,3,5,20,12,4,13,16), (1,12,6,11,19,7,9,17,20,18,13,10,4,3,5,2,15,16,14), (1,12,13,14,16,7,15)(2,10,4,6,3,17,19,18)(5,11,20,8), (1,19,16,17,15,11,6,8,2,7,12,14,3,4,9)(5,20,18), (1,6,11,4,20,10,2,13,9,5,7,3,16,18,15,8)(14,17), (1,8,16,3,5,4,19,6,12,15)(2,9)(7,10,17)(11,18,20,13,14), (1,16,13,10,9,17,19,18,20,15,4,11,12,14)(2,6,8)(3,5), (1,6,18,5,10,4,8,12,11)(2,20,7,15,3,19,17,13,14,16,9), (2,15,20,12,4,13,8,19,17,18,7)(3,14)(5,9,10,6), (1,15,17,9,8,19,6)(2,11,10,12,18,20,7,14)(3,5,4,16), (1,7,20,5,18,8)(2,11,13,19,16,3,12,10,15,6)(4,9,14), (1,6,3,14,13,16)(2,11)(5,10,20,19,9,8,18,15,7,17,12), (1,11,5,17,18,15,8)(2,9,4,10,19,20,7,14,6,16,3), (1,15,10,9,5,13,18,19,8,7,14,16,2,12)(3,11)(4,6)(17,20), (1,10,7,13,2,12,11,6,15,14,18,17,8,9,3,5,16)(4,19,20), (1,13,20,19,11,3,2,17,15,8,4,6,5,14)(9,18,10,12), (1,7,4,2)(3,14,9,19,16)(5,18,13,11,6,10,15,17), (1,14,13,2,12,11,17,7,10,9,20,5,19,3,6,8,16,4,18), (1,18,6,19,20,2,11,14,10,9,4,5)(3,7,16,8)(12,15)(13,17), (1,12,5,10)(2,20,19,15,16,7,14,13,8,18,17,6,11,3,9,4), (1,17,15,12,10,11,7,3,9,16,19,14,6,2,20,4,8,13,18), (1,10,19,12)(2,18,9,3,11,13,5,7)(4,6,20,8)(14,16,17,15), (1,12,8,11,19,9,10,2,18,4,7,17,6,15,14,16,13,20,3), (1,17,9,5,2,15,8,18,13,4,19,14,7,16,12,11,3,10)(6,20), (1,6,4,17,11,19,12,9,5,7)(3,13,8,18,16)(10,20,15,14)]
[(1,10,5,14,11,2)(3,6,8,18,15,17,12)(7,19,20,9), (1,5,9,11,4,17,14)(2,20,16,3,7,6,15,12)(8,13,10,18), (1,18,20,3,5)(2,12,10,13)(4,17,7,16,9,11,14,15), (1,7,20,9,6,4,14,17,10,16,18,15,19,5,12,11,2,3,13), (1,13,7,17,12)(2,4,6,9,20,15,10,11,5,3,8,16,19,18,14), (1,5,2,7,10,14,9,12,11,16)(3,18,17,6,8,20,15,4), (1,10,13,15,19,6,12,16,2,7,17)(3,9,11)(4,18)(5,14), (1,19,6,3,11,5,14,18,16,15,7,2,10,17,9,12)(4,8,13,20), (1,9,6,17,4,10,13,14,19,7,11,5,15,2,18,20,3,16,12), (1,17,15)(2,13,18,10,5,12,14)(4,8,20)(6,9,16,7)(11,19), (1,13,4,5,19,10,6,3,12,18,14,20,16,2,9,7)(8,11), (1,18,2,10,20,17,13,19,8,11,3,7,14,4,12,16)(6,9), (1,13,10,20,6,18)(3,4,16,15,9,19,17,11,7,14,12,5), (1,11,9,14,13,7,2,5,4,12,15,17,8,3)(6,18)(10,16)(19,20), (1,13,7,15,20,10,12,18,16,8,3,17)(2,5,4)(9,19,11,14), (1,15,11,10,17,20,2,13,14,4,9,19,5,7,12)(6,16,8), (1,16,3,19,9,13,15,6,12,7,18,2,11)(4,5,17,8,20,10,14), (1,13,20,9,19,8,3,16,11,5,12,17,10,7,15,6)(2,4), (1,11,18,13,17,14,16,5,19,8,10,3)(2,6,15,9)(4,7,20), (1,5,12,20,14,16,4,15,13,11,2,8,17,19,3)(6,10,7,9,18), (1,12,8,19,2,15,17,18,6,5,4,7,16,20,10,14,3,9,11), (1,12,10,15,14,16,7,2,11,6,4,5,18,17,19,20)(3,8), (1,3,16,8,9,4,19,13,5,10,12)(2,14,7,15,6,18,20,17,11), (1,7,6,18,9,3)(2,4,15,14,11,12,17,20,16,19,13,5,10,8), (2,14,20,10,16,3,6,17,11,18,9)(4,15,12,7,13,5,19), (1,9,12,17,20,5,14,4,15,10,18,6,16,19,8,2,3,7)(11,13), (1,15,16,19,11,6,9,20,4,18)(2,8,17,12,14,5,13,7), (1,16,19,20,4,5,8,6)(2,11,9,12,7,18,3,13,14,10,15,17), (1,4,5,19,10,8,18,13,12,2,16,14)(3,6,7,20)(9,17,15), (1,2,9,16,12,14,17,6,15,8,4,19,3,11,13,20,10,5)(7,18), (1,15,16,10,8,13)(2,7)(3,6,4,20,11,5,12,14)(18,19), (1,16,11,12,20)(2,17,4,8,10)(3,5,7,19,13,14,18,6,9), (1,2,10,6,17,19,3,14,4,5,12,16,9,11,20,7,18,8)(13,15), (1,11,13,14,17,5,6,19,12,9,3,8,7,10,18,2)(4,15,16,20), (1,19,2,14,4,6)(3,5,13,20,7,8,9,18,10)(11,16,15,12), (1,7,2,3,17,9,12,16,11,5,18,20,6,10,4,19,14,8,15), (1,16,3,10,4,13,7,8,12,11,5,19,9,6,18)(2,15)(14,20), (1,19,6,4)(2,10,3,11,20)(5,8,9,13,12,18,16,7,14,17), (1,20,12,17,8,13)(2,15,5,18,7,6)(3,16,10,19)(4,9), (1,19,17,5)(3,8,18,9,16,10)(4,11,12,6,15)(7,13,20), (1,18,5,11,2,10,7,14,12,9,16,15,20,6,3,17,4,13,19), (1,8,9,11,3,12)(2,4,20,16,19,6,18,10,13,5)(7,17)(14,15)]
[(1,10,9,11,19,12,7)(2,4,18,8,17,5)(6,13,15,20), (1,13,10,19,7,4,20,14)(2,16,12,5,18,17,6)(3,8,11,9), (1,17,18,11,20)(2,5,19,16,12,13,14,6)(3,4,7,8), (1,3,18,13,20,6,10,16,5,12,8,14,11,19,15,17,7,2,4), (1,9,14,15,11,5,4,16,10,6,20,19,8,2,17)(3,13,12,7,18), (1,11,12,10,9,20,19,16)(2,14,18,17,4,13,8,5,6,7), (1,6,2)(3,19,15,10,7,14,4,13,12,18,8)(5,17)(11,16), (1,2,17,5,11,14,19,13,4,8,12,6,7,18,15,10)(3,20,16,9), (1,14,7,18,6,10,12,16,8,3,5,15,13,2,17,19,4,11,20), (2,15)(3,11,8,17,7,5,4)(6,14,13,10)(9,20,16)(12,19,18), (1,7,11,5,20,14,4,6,13,18,3,16,17,15,8,10)(2,9), (1,13,5,16,7,14,18,11,4,8,20,12,3,15,9,2)(6,10), (1,16,14,19,6,15,12,2,13,5,7,17)(3,8,20,10,11,18), (1,18,2,6,5,3,13,4,17,16,7,19,12,9)(8,14)(10,11)(15,20), (1,12,18,3,13,19,20,8,7,11,14,9)(2,5,6,15)(4,17,16), (2,8,12,20,4,3,5,16,6,15,17,13,7,18,19)(9,10,14), (1,15,6,3,19,10,7,13,11,4,2,18,14)(5,16,17,12,9,20,8), (1,14,2,17,7,12,8,13,19,10,18,3,20,6,15,9)(4,16), (1,18,2,11,3,12,5,14,17,15,9,8)(4,10,19,6)(13,20,16), (1,18,17,7,20,5,14,16,19,3,2,4,9,12,15)(6,11,10,8,13), (1,6,2,18,7,9,15,4,19,12,11,10,17,16,13,14,20,8,5), (1,9)(2,10,16,17,11,12,15,20,18,7,8,19,5,14,13,4), (1,14,9,6,16,15,3,17,8,7,18)(2,4,5,13,19,10,11,20,12), (1,18,13,10,11,6)(2,7,12,20,14,15,3,17,8,9,4,16,19,5), (1,10,12,2,11,6,4,5,20,8,14)(3,17,15,16,19,7,13), (1,13,18,6,7,12,20,17,5,16,19,8,11,10,14,15,9,4)(2,3), (2,10,6,20,16,11,18,19,14,15)(3,13,4,9,12,7,5,17), (1,3,5,8,19,12,4,2,6,7,13,11)(9,10,18,14,15,20,16,17), (1,10,13,20)(3,7,4,14,5,18,16,17,15,8,9,11)(6,12,19), (1,2,3,20,8,17,18,4,6,14,7,5,12,10,19,9,16,15)(11,13), (1,10,16,20,2,17,7,5)(3,18,19,14,8,9)(4,13)(11,15), (1,17,13,15,3,5,11,10,6)(2,7,20,18,14)(4,12,16,9,8), (1,5,16,17,7,14,6,2,20,13,11,9,18,4,8,10,12,15)(3,19), (1,9,13,8,11,4,18,2,3,5,12,17,10,15,7,6)(14,20,16,19), (1,17,3,20,13,9,6,11,8)(2,14,19,7)(4,5,16,10,18,15), (1,12,6,7,14,2,17,11,20,10,8,16,15,5,9,19,18,13,4), (1,8,16,3,13,9,7,2,17,15,6,10,11,18,14)(4,19)(5,20), (1,2,20,4,8)(3,7,11,14,13,5,12,17,9,6)(10,16,18,15), (1,14,8,15)(3,18,20,7,12,9)(4,19,17,11,13,10)(6,16), (1,9,11,6,14,8)(2,7,10,19,16)(3,20,13)(12,17,18,15), (1,12,16,3,15,18,11,17,2,4,8,13,5,7,6,14,19,20,10), (1,7,18,9,6,2)(3,17,4,16,20,14,15,10,11,8)(5,19)(12,13)]
[(1,16,15)(2,3,4,11,6)(5,8,9,19,20,18,12)(7,14,13,10,17), (1,20,19,14,15,5)(2,9,13,12,8,7,11,17,3,18)(4,16,10), (1,6,2,11,8,20,10,17,14,12,7,9,4)(3,5,19,16,15,18,13), (1,5,19,9,2,6,11,7,14,15,12,18,20)(3,8,17,16,10,13,4), (1,5,6,2,9,3,17,18,15,7)(4,16,20,8,13)(10,12,11)(14,19), (1,3,18,2,5,13,14)(4,9,7)(6,20,16,10,17,11,8,12,19), (1,4,2,19,13,15,7,12,20,17,18,3,8)(5,9,16,6,14,10,11), (1,11,10,13,2,15,17,9,6,12,14,5,7,3,4,16)(8,19,20,18), (1,3,15,5,13,7,20,12,17,16,18,8,6,19,4,11,2,14)(9,10), (1,11,12,18,4,9,20,16,14,2,19,17,15)(3,10,8,7,13,6,5), (1,20,13,16,3,2,4,14,19,18,8,6,15,12,10,7)(9,11), (1,19,20,8,14)(2,17,16,5,12,3,18,15,9,11,4,6,13), (1,6,19,9,4,12,14,11,7,15,8)(2,16,10)(3,18,5,17,20), (1,19)(2,11,5,9,17,15,16,8,6,13,12)(3,18)(4,7,10,20,14), (1,2,13,5,7,14,20)(3,9,19,8,17,11,18,4,10,12,6,15,16), (1,15,4,8,17,2,16,5,11,3,13,20,14)(6,18)(7,19,10)(9,12), (1,13,9,5,2,17,7,20,19,11,12,8,4)(3,18,16)(6,10,15), (1,19,14,15,12,5,6,4,17,9,7,2,11,16,3,13,8,20,10), (1,13,15,4,14,20,10,6,11,12,2,5,19,3,17,18,8,9,16), (1,7,10,17)(2,12,8,11,5,19,15)(3,20,16,18,13,6,4,14), (1,13,10)(2,20,14,9,5,18,12,16,11,17,3,7,6,8,19), (1,4,6,15,9,10,8,20,12,13,11,7,5,3,17,14)(2,16), (1,15,2,17,13)(3,19,11,5,7,12,20,10,14,18)(4,16,8)(6,9), (1,11,14,17,19,2,5,12,15,4,9,16,18,13)(3,7,6)(10,20), (1,8,11,20,18,16,15,2,12,9,6)(3,13,10,4,14,7,19,17,5), (1,19,14,15,7,18,16,13,8,6,11)(2,20)(3,10,9,4), (1,8,2,6,17,4,19,13)(3,5,11,16,9,7,18)(10,14,12,20), (1,10,13,7,5,8)(2,14,9)(3,6,17,15,18,12,20,19,4,11), (1,18,9,7,13,11,8,16,19,10,4)(2,15,12,5,3,20)(6,17), (1,8,2,3,12,20,6,9,14,4,18)(5,17,10,16,13,11,7), (1,16)(2,12,6,19,5,11,4,9,10,15,13,18,7,8)(3,14)(17,20), (1,14,18)(2,13,16,7,9,20,10,12,5,4,8,15,6,19,17,3,11), (1,18,17,20,6,16,11,7,14,3,10,2,5,15)(4,19,9,13), (2,9,18,12,20)(3,4,11,16,10,13,15,17)(5,8,14,6), (1,10,18,20,3,7,12,14,13,5,2,15,6,19,17,16,8,4,9), (1,6,17,2,4,9,14,10,5,13,3,18)(7,20,8,12)(11,19)(15,16), (1,18,11,12,8,2,15,7,13,16,3,17,20,9,14,6)(4,5,19,10), (1,14,7,15,13,5,16,11,19,4,17,8,20,9,12,18,2,3,6), (1,7,14,3)(2,12,16,11)(4,18,19,5)(6,13,9,20,17,15,10,8), (1,20,5,19,7,17,18,9,4,6,13,14,8,16,3,11,2,12,15), (1,3)(2,8,12,19,17,20,4,5,16,9,10,6,11,7,13,15,14,18), (1,11,2,4)(3,14,16,17,18,19,9,10,8,5)(7,13,12,20,15)]
cb6c75ba0fd13f8c13cb650ad52302d381be36673e0689cac517c92e76e81492e4b1056ebcf8dcc277dc531402d410a0
```

## Solution

First of all, let's analyze the source code.

It looks like an analogue of [Diffie-Hellman key exchange](https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange), but slightly different. It also uses the public keys for _users_ `A` and `B`, the private keys for them and the shared key. The main difference is in math operations: the classical Diffie-Hellman is based on the [discrete logarithm problem](https://en.wikipedia.org/wiki/Discrete_logarithm), but there is nothing like this in the source code. Instead the challenge initializes an [alternating group](https://en.wikipedia.org/wiki/Alternating_group) of degree `n` and does some operations with its elements.

After the imitation of the key exchange, the challenge encrypts the flag using [AES cipher](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) with the derived shared key `K`. So, our goal is to get `K` and decrypt the flag. Initially I thought about a weakness of the alternating group structure, because this group is rarely used in crypto challenges. 

Let's try to understand what the alternating group is.

The alternating group is the subgroup of the [symmetric group](https://en.wikipedia.org/wiki/Symmetric_group), and the symmetric group is a group of all [permutations](https://en.wikipedia.org/wiki/Permutation) of the fixed length `n`. For example, if `n = 3`, then symmetric group contains these elements: `{123, 132, 213, 231, 312, 321}`. The alternating group contains only even permutations (permutation is even if the number of its [inversions](https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)) is even). For `n = 3` it will be: `{123, 231, 312}`. The [order](https://en.wikipedia.org/wiki/Order_(group_theory)) of the symmetric group is `n!` (see [factorial](https://en.wikipedia.org/wiki/Factorial)), and of the alternating group is `n! / 2`. In the challenge `n = 20` and the alternating group contains `20! / 2 = 1216451004088320000` elements. It's not possible to enumerate all permutations and find the correct `K`.

Now let's take a look at the group operations.

The first operation is exponentation `^`, only two exponents are used: `1` and `-1`. One can deduce that `X^1` is just `X`, and `X^(-1)` is the [multiplicative inverse](https://en.wikipedia.org/wiki/Multiplicative_inverse) of `X`. 

The second operation is multiplication `*`, it's just a composition of permutations:

![multiplication](images/multiplication.png)

Note that `*` is [non-commutative operation](https://en.wikipedia.org/wiki/Commutative_property), it means that `X * Y ≠ Y * X`. This property may be obvious from `K` generation. If `*` would be commutative, then `K` always be the same identical element: 

```python
K = A^(-1) * B^(-1) * A * B
```

Now it's the time to recognize the cryptosystem (however it's not too helpful). Since the operation is non-commutative, we can search for cryptography based on such type of operations and find the Wikipedia article [Non-commutative cryptography
](https://en.wikipedia.org/wiki/Non-commutative_cryptography). There is another link to the desired cryptosystem: [Anshel–Anshel–Goldfeld key exchange](https://en.wikipedia.org/wiki/Anshel–Anshel–Goldfeld_key_exchange). The algorithm is the same, and we can also find out what problem AAG cryptosystem is based on: _the conjugation problem_. After some searching one can find that this problem is [NP-complete](https://en.wikipedia.org/wiki/NP-completeness), so let's try to use a primitive approach to solve it.

In short we need to recover the private key `A` (or `B`) to derive `K`, it means that we need to recover the array of exponents `eps_a` (or `eps_b`). The array `eps_a` contains `m` elements, and each element lies in `{1, -1}`, so we need to enumerate `2^m` possible `eps_a` arrays. How could we check the correctness of `A`? There is another array `abar` that contains elements of type `A^(-1) * pub_b[i] * A`. Since we know `pub_b[0]` and `abar[0]` we can check `A` that way. But bruteforce `2^m = 2^42 = 4398046511104` is too hard, so let's use some well-known heuristics to reduce it.

Notice that `eps_a` has _almost equal_ numbers of `1` and `-1` elements. So we don't need to enumerate all possible `eps_a`, we just need to enumerate all `(m / 2)`-[combinations](https://en.wikipedia.org/wiki/Combination) on `m` positions. The number of such combinations is equal to: 

```
  m! / ((m / 2)! * (m / 2)!) = 
= 42! / (21! * 21!) = 
= 538257874440
```

A bit smaller, but not enough. Now let's try to apply [meet-in-the-middle attack](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack). We can split `A` that way:

```python
A = mul(pub_a[i] ^ eps_a[i] for i in range(m))

A1 = mul(pub_a[i] ^ eps_a[i] for i in range(0, m // 2))
A2 = mul(pub_a[i] ^ eps_a[i] for i in range(m // 2, m))

A = A1 * A2
```

Now look at `abar[0]`:

```python
abar[0] = A^(-1) * pub_b[0] * A
abar[0] = (A1 * A2)^(-1) * pub_b[0] * (A1 * A2)

A2 * abar[0] * A2^(-1) == A1^(-1) * pub_b[0] * A1
```

We can enumerate `A1` and `A2` differently and _meet them in the middle_, it means we need to bruteforce:

```
  2 * ((m / 2)! / ((m / 4)! * (m / 4)!)) =
= 2 * (21! / (10! * 11!)) =
= 705432
```

and store half of it in the table. Looks great! Note that `{1, -1}` are not equally distributed, so we need to add an additional bias (for example enumerate all 9-, 10-, 11-, 12- and 13-combinations on 21 elements). Here is an example algorithm in `sage`:

```python
def find_eps_a(pub_a, pub_b, abar):
    import itertools

    table = dict()
    left, right = pub_a[:m // 2], pub_a[m // 2:]

    for offset in range(-2, 3):
        for combination in itertools.combinations(range(m // 2), m // 4 + offset):
            eps = [1] * (m // 2)

            for i in combination:
                eps[i] = -1

            A1 = prod([x^e for x, e in zip(left, eps)])
            candidate = A1^(-1) * pub_b[0] * A1
            table[candidate] = tuple(eps)

    for offset in range(-2, 3):
        for combination in itertools.combinations(range(m // 2), m // 4 + offset):
            eps = [1] * (m // 2)

            for i in combination:
                eps[i] = -1

            A2 = prod([x^e for x, e in zip(right, eps)])
            candidate = A2 * abar[0] * A2^(-1)

            if candidate in table:
                return list(table[candidate]) + eps
```

When we found `eps_a` we can calculate `K` and decrypt the flag:

```python
K = A^(-1) * prod([x^e for x, e in zip(bbar, eps_a)])
```

_Note: I don't know is it the indended solution._

## Flag

```
ptm{c0njug4t10n_w1th_cycl35_1s_fun!}
```
