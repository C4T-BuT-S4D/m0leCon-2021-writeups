# Automatic Rejection Machine

## Writeup
We are given a binary that checks the flag for correctnes, all it does is shuffle the flag and compare the hash of each slice of size 3 (perhaps with some salt, I'm not sure what is a part of the hash and what is not) with some constants. The hash constants didn't seem googlable enough, so I just wrote a simple brute force in cuda.

```bash
nvcc brute.cu -run
```

## flag
ptm{5m0l_chunk5_5m0l_53cur17y}
