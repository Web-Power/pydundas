from pydundas import Session
from pydundas.exceptions import LoginFailedError
import requests

# If url does not start with http, then 'https://' will be prepended,
url = 'winterfell.got'
user = 'arya'
pwd = 'valar morghulis'

print("Context manager, happy flow, you are automagically logged in and out. " +
      "Expect some json describing your server.")
with Session(user=user, pwd=pwd, url=url) as d:
    print(d.get('Server').text)


print("\nYou can do the same with extra debugging statements")
with Session(user=user, pwd=pwd, url=url, loglevel='debug') as d:
    print(d.get('Server').text)

# Logger object are persistent. Let's restore loglevel to warning.
Session.setLogLevel('warning')

try:
    print("\nException within the context manager, expect a 404.")
    with Session(user=user, pwd=pwd, url=url) as d:
        d.get('you/know/nothing')
except requests.exceptions.HTTPError as e:
    print(e)
    print("You are still automagically logged out.")


try:
    print("\nYou will know if your credentials are wrong.")
    with Session(user=user, pwd='valar dohaeris', url=url) as d:
        d.get('Server')
except LoginFailedError as e:
    print(e)

print("\nNo context manager. You need to log in and out yourself. Expect some json describing your server.")
e3 = Session(user=user, pwd=pwd, url=url)
e3.login()
print(e3.get('Server').text)
e3.logout()


try:
    print("\nNo context manager and you reuse a logged-out Dundas session object. " +
          "Expect a 440 (Login Time-out) error.")
    print(e3.get('Server').text)
except requests.exceptions.HTTPError as e:
    print(e)

print("\nNo context manager and you reuse a logged-out Dundas session object. " +
      "Nothing prevents you to log in again. " +
      "Expect some json describing your server.")
e3.login()
print(e3.get('Server').text)
e3.logout()


try:
    print("\nNo context manager and you forgot to login. Expect a 440 (Login Time-out) error.")
    e6 = Session(user=user, pwd=pwd, url=url)
    print(e6.get('Server').text)
    e6.logout()
except requests.exceptions.HTTPError as e:
    print(e)


print("\nNo context manager and you forget to logout.")
print("I'm not that mean and I won't burn through your elastic hours, but be careful " +
      "and that's why context the manager is awesome.")
