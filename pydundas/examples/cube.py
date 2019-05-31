from pydundas import Api, Session, creds_from_yaml
import sys
import json
creds = creds_from_yaml('credentials.yaml')

with Session(**creds) as d:
    api = Api(d)
    capi = api.cube()
    cube = capi.getByPath('Awesome Project', '/relevant/path')
    if cube is None:
        print("Gotcha, no cube named like that.")
        sys.exit(1)
    print(json.dumps(cube.data))
    cube.warehouse()
    print(cube.isWarehousing())
    cube.waitForWarehousingCompletion()
    print('Done')
