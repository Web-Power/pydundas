from pydundas import Api, Session, creds_from_yaml
import sys

creds = creds_from_yaml('credentials.yaml')

with Session(**creds, loglevel='warn') as d:
    api = Api(d)
    hapi = api.health()
    failings = hapi.check(allchecks=True)
    print(failings)
    for f in failings:
        hapi.check([f], fix=True)
