from pydundas import Api, Session, creds_from_yaml

creds = creds_from_yaml('credentials.yaml')

with Session(**creds) as d:
    api = Api(d)
    napi = api.notification()

    # Get notification with this name.
    n = napi.getByName('Awesome notification')

    # Schedule it right now.
    n.run()

    # Print some run info.
    print(n.isRunning())

    # As method says.
    n.waitForCompletedRun()
    print("Done")
