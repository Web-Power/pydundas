Manage sessions for [Dundas](https://www.dundas.com/).

# Description


Dundas has a very complete [REST API](https://www.dundas.com/support/api-docs/rest/). You need a user to use it, and if you forget
to log out, you will burn through your elastic hours very quickly.

In short, Dundas is very friendly and lets you have more users than paid for logged
in at the same time (elastic hours), but you should not abuse it (if you burn through
them, you are blocked). 

Always be sure to be logged out, even in case of exception or multiple path is a pain.
This is the idea behind this module. You will not need to remember yourself to log
out, it will be done for you, in all cases if you so wish.

# Why this module is useful

It currently does 2 things for you.

If you use `dundas.Session` within a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers),
the context manager wil log you in and out automagically, no matter what happens. You can
use the session object as a normal object as well as long as you do not forget to log in and out
yourself.

Each and every call to the API needs to have the same `sessionId` parameter. This module creates
shortcuts for you for `get`, `post` and `delete`, to make your life easier. You do not need
to repeat the host, api path prefix or sessionId every single time.

# Installation

Simply with pip:

```bash
python3 -m pip install pydundas
```

or, assuming you do not have permission to store the module globally:

```bash
python3 -m pip install --user pydundas
```

The module should be able to work with python2 as well, but it is untested and as python2 will be end of life'd in a few
months anyway I did not look into it.

# Examples

You can see all the [examples](https://github.com/lomignet/pydundas/blob/master/example.py) as one python file.

You can use pydundas as a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers) or as a normal python object. The context manager
makes it impossible for you to forget to log out.

All the examples below assume a `url`, `user` and `pwd` variables.

## Happy flow with context manager

```python
with Session(user=user, pwd=pwd, url=url) as d:
    print(d.get('Server').text)
```

Output (example):
```json
[{"name":"winterfell","serverGroupId":1,"lastSeenTime":"2019-03-29T09:33:38.880327Z","__classType":"dundas.configuration.ServerInfo"}]
```
When the variable `d` comes out of scope, so outside the `with` statement, you will be
automagically logged out.
## Change loglevel

```python
with Session(user=user, pwd=pwd, url=url, loglevel='debug') as d:
    print(d.get('Server').text)
```

You will have the same output as before, with extra statements:
```
Logging in.
Logged in.
[{"name":"winterfell","serverGroupId":1,"lastSeenTime":"2019-03-29T09:33:38.880327Z","__classType":"dundas.configuration.ServerInfo"}]
Logging out.
Logged out.
```

Note that you can access the logger yourself to tune it to your heart's content.
```python
# Logger object are persistent. Let's restore loglevel to warning.
Session.setLogLevel('warning')

# Actually work on the logger
logger = logging.getLogger('pydundas.dundas')
```

## Read credentials from a yaml file
If you have a yaml file with a `user`, `pwd` and `url` key, then you can read it from pydundas:
```yaml
user: arya
pwd: 'valar morghulis'
url: winterfell.got
```

```python
from pydundas import creds_from_yaml
creds=creds_from_yaml('credentials.yaml')
with Session(**creds) as d:
    print(d.get('Server').text)
```

## Exception within the context manager are properly handled
```python
with Session(user=user, pwd=pwd, url=url) as d:
        d.get('you/know/nothing')
``` 
output:
```
404 Client Error: Not Found for url: https://winterfell.got/api/you/know/nothing?sessionId=fbeb7897-5981-412b-a981-7783f88894bd
```

You are still automagically logged out.


## Wrong credentials
```python
with Session(user=user, pwd='valar dohaeris', url=url) as d:
        d.get('Server')
```
will give you:

```json
{"logOnFailureReason":"UnrecognizedCredentials","message":"The provided user credentials were not recognized."}

```

## Full control without context manager
You can do it, but do not forget to log in/out yourself:
```python
d = Session(user=user, pwd=pwd, url=url)
d.login()
print(d.get('Server').text)
d.logout()
```
You will get, as with the first example:
```json
[{"name":"winterfell","serverGroupId":1,"lastSeenTime":"2019-03-29T09:33:38.880327Z","__classType":"dundas.configuration.ServerInfo"}]
```

## No context manager, object reuse
No context manager and you reuse a logged-out Dundas session object. Nothing prevents you to log in again:
```python
# d comes from the previous example, for instance.
d.login()
print(d.get('Server').text)
d.logout()
```

with the same output as previously.

## No context manager, forget to log in
```python
d = Session(user=user, pwd=pwd, url=url)
# Oops, no login!
print(d.get('Server').text)
d.logout()
```
You will get:
 ```json
440 Client Error:  for url: https://reports.webpower.io/api/Server
```

The same would happen if you reuse an object after logging out.


## No context manager, forget to log out

I'm not that mean and I won't burn through your elastic hours, but be careful and that's why context the manager is awesome.

# Develop

You can either use `conda` or `virtualenv`. Most relevant commands are in the Makefile.
First edit the first line of the makefile to choose if you want to use conda or virtualenv. 

```bash
# Build an environment with all dependencies
make devinit

# Tests
make pep8
make unittest

# Build a package
make package

# Clean up everything
make purge

```