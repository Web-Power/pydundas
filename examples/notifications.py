from pydundas import Api, Session, creds_from_yaml
import sys

creds = creds_from_yaml('credentials.yaml')

with Session(**creds) as d:
    api = Api(d)
    napi = api.notification()

    # Get all notification with this name.
    notifs = napi.getExactName('Awesome notification')
    if len(notifs) > 1:
        print("More than one notification with this name.")
        sys.exit(1)
    elif not notifs:
        print("No notification with this name.")
        sys.exit(1)

    # There is only one notification, let's keep its id.
    nid = notifs[0]['id']

    # Schedule it right now.
    napi.run(nid)

    # Print some run info.
    runs = napi.getLastRun(nid)
    print(runs)
    print(napi.isRunning(nid))

    # As method says.
    napi.waitForCompletedRun(nid)
    print("Done")
