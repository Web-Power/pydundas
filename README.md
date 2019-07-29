Manage sessions for [Dundas](https://www.dundas.com/).

# Description


Dundas has a very complete [REST API](https://www.dundas.com/support/api-docs/rest/).

With completeness comes complexity, and this module will help you use the query in an
easier way.

# Why this module is useful

It currently does 3 things for you.

If you use `dundas.Session` within a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers),
the context manager wil log you in and out automagically, no matter what happens. You can
use the session object as a normal object as well as long as you do not forget to log in and out
yourself.

Each and every call to the API needs to have the same `sessionId` parameter. This module creates
shortcuts for you for `get`, `post` and `delete`, to make your life easier. You do not need
to repeat the host, api path prefix or sessionId every single time.

Some API calls are ported and might have helper methods. I am updating the module based on what I
need and use, so I do not expect to have everything ported on my own.


# Installation

Simply with pip, from [pypi](https://pypi.org/project/pydundas/):

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

You can see all the [examples](https://github.com/lomignet/pydundas/blob/master/pydundas/examples) in one directory.

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

# API calls

## Constant
Most constants can be used via their human-readable name.
```python
from pydundas import Api, Session, creds_from_yaml

with Session(**creds_from_yaml('credentials.yaml')) as d:
    a=Api(d)
    c = a.constant()
    # returns ['STANDARD_EXCEL_EXPORT_PROVIDER_ID']
    print(c.getNamesById('679e6337-48aa-4aa3-ad3d-db30ce943dc9'))
    # returns '679e6337-48aa-4aa3-ad3d-db30ce943dc9'
    print(c.getIdByName('STANDARD_EXCEL_EXPORT_PROVIDER_ID'))
```

## Cube
You can warehouse a cube, and get some information about it:
```python
with Session(**creds) as d:
    api = Api(d)
    capi = api.cube()
    cube = capi.getByPath('Awesome Project', '/relevant/path')
    cube = capi.getByPath('DP', '/CustomReports/2daysent/1mailing sendouts')
    if cube is None:
        print("Gotcha, no cube named like that.")
        sys.exit(1)
    print(cube.json())
    print(cube.is_checked_out())

    cube.warehouse()
    print(cube.isWarehousing())
    cube.waitForWarehousingCompletion()
```
## Health
You can run all checks, and fix the failing one:
```python
with Session(**creds, loglevel='warn') as d:
    api = Api(d)
    hapi = api.health()
    failings = hapi.check(allchecks=True)
    print(failings)
    for f in failings:
        hapi.check([f], fix=True)
```
## Notification

You can get a notification by its name and then run it.
```python
    napi = api.notification()
    notif = napi.getExactName(name='Awesome notification')

    if len(notif) != 1:
        print("None or more than one notification with this name.")
        sys.exit(1)
    napi.run(notif[0]['id'])
```

## Project
For example, to find the ID of a project:
```python
from pydundas import Api, Session, creds_from_yaml

with Session(**creds_from_yaml('credentials.yaml')) as d:
    api=Api(d)
    project = a.project()
    print(project.getProjectIdByName('DP'))
```

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
