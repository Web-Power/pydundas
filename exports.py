from pydundas.dundas import Session

creds=Session.creds_from_yaml('credentials.yaml')
with Session(**creds, ) as d:
    pass

# export vs notification