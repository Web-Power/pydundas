from pydundas import Api, Session, creds_from_yaml

with Session(**creds_from_yaml('credentials.yaml')) as d:
    a = Api(d)

    papi = a.project()
    print(papi.getProjectIdByName('Awesome project'))
