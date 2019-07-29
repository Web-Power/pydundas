from pydundas import Api, Session, creds_from_yaml
import sys

creds = creds_from_yaml('credentials.yaml')

with Session(**creds, loglevel='warn') as d:
    api = Api(d)
    hapi = api.health()
    # hapi.heck return True is all is fine, which needs to be transformed to not 0, hence the not.
    sys.exit(not hapi.check(allchecks=True))
