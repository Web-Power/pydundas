from pydundas import Api, Session, creds_from_yaml


creds = creds_from_yaml('credentials.yaml')

with Session(**creds) as d:
    api = Api(d)
    napi = api.notification()

    # Get notification with this name.
    n = napi.getByName('Awesome notification')

    print(n.json())
    print("Before:")
    print(n.get_subject())
    print(n.get_body())
    print(n.get_recipients())

    n.set_subject("Wonderful subject")
    n.set_body("Meaningful body")
    n.set_recipients([])
    n.add_email_recipient('hi@there.com')

    print("Updating.")
    n.update()

    print("After:")
    print(n.get_subject())
    print(n.get_body())
    print(n.get_recipients())

    # Schedule it right now.
    n.run()

    # Print some run info.
    print(n.isRunning())

    # As method says.
    n.waitForCompletedRun()
    print("Done")
