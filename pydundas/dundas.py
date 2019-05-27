import requests
import logging
from .exceptions import YamlNotReadableError, LoginFailedError


# Helper method, not really part of the class itself.
def creds_from_yaml(yamlpath):
    """Make everyone's life easy. This returns a dictionary that can be used with ** to initialise your session."""
    # Only import yaml if you actually require it.
    import yaml
    try:
        with open(yamlpath, 'r') as f:
            try:
                creds = yaml.load(f, Loader=yaml.Loader)
            except yaml.YAMLError as e:
                raise YamlNotReadableError from e

            mandatory_keys = ["url", "user", "pwd"]
            try:
                return {k: creds[k] for k in mandatory_keys}
            except KeyError:
                raise (YamlNotReadableError(
                    "File '{}' needs to be valid yaml and have 'user', 'pwd' and 'url' fields.".format(yamlpath))
                )

    except FileNotFoundError as e:
        raise YamlNotReadableError from e
    except OSError as e:  # permission, isADirectory and more weird stuff
        raise YamlNotReadableError from e


class Session:

    def __init__(self, *, user, pwd, url, loglevel=None):

        # For session reuse - TCP connection reuse, keeps cookies.
        self.s = requests.session()

        self.user, self.pwd = user, pwd
        self.url = url if url.startswith('http') else 'https://{}'.format(url)
        self.endpoint = self.url + '/api/'

        # Will be setup within login()
        self.session_id = None

        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():
            # First creation of this logger. Custom loggers need a handler, so let's give one.
            h = logging.StreamHandler()
            logger.addHandler(h)
        self.logger = logger
        self.setLogLevel(loglevel)
        # Shut up urllib3
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def __enter__(self):
        """Context manager entry point."""
        self.login()
        return self

    def __exit__(self, *args):
        """Context manager exit point."""
        self.logout()

    @classmethod
    def setLogLevel(cls, loglevel):
        # Note: default log level on creation is warning.
        if loglevel:
            logging.getLogger(__name__).setLevel(loglevel.upper())

    def _setlogging(self, loglevel):

        # A useful/annoying thing with the logging module is that `logging.getLogger()` returns the same object
        # if called with the same name parameter, but you can still add multiple handlers if you are not careful.
        # If multiple dundas.session objects are created, the handlers would be duplicated and that's not what you want.
        # I am trying to get around this problem here.

        logger = logging.getLogger(__name__)
        # logger.setLevel(loglevel.upper())

        if not logger.hasHandlers():
            # First creation of this logger. Custom loggers need a handler, so let's give one.
            h = logging.StreamHandler()
            logger.addHandler(h)

        logger.setLevel(loglevel.upper())
        self.logger = logger

    def login(self):
        login_data = {
            'accountName': self.user,
            'password': self.pwd,
            'deleteOtherSessions': False,
            'isWindowsLogOn': False
        }
        self.logger.info('Logging in.')
        # We can't use self.post() yet as session_id is not set.
        r = self.s.post(self.endpoint + 'logon/', json=login_data)
        # The following line exceptions out on not 200 return code.
        r.raise_for_status()

        resp = r.json()
        if resp['logOnFailureReason'].lower() == "none":
            # We're in!
            self.logger.info('Logged in.')
            self.session_id = resp['sessionId']
        else:
            raise LoginFailedError(r.text)

    def logout(self):
        """If you do not logout, session will stay active, potentially burning through your elastic hours very fast."""

        # If session_id is not defined, we did not even log in (or we are already logged out).
        self.logger.info('Logging out.')
        if self.is_loggedin():
            self.delete('session/current')
            self.session_id = None
            self.logger.info('Logged out.')
        else:
            self.logger.info('Was not yet Logged in.')

    def is_loggedin(self):
        return bool(getattr(self, 'session_id'))

    # All get/post/delete will have the same url base, and will all require the same
    # params parameter. Let's make everybody's life easy.
    # A query could legitimately need to extend the 'params' parameter, hence the merge of kwargs
    # with the hardcoded dict with sessionId.

    def extend_with_sessionid(self, kwargs):
        if 'params' in kwargs:
            kwargs['params']['sessionId'] = self.session_id
        else:
            kwargs['params'] = {'sessionId': self.session_id}
        return kwargs

    def _raise_for_status(self, r):
        """Log body of the request in case of HTTPError. It might contain some explanation of what went wrong."""
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error(r.json())
            raise

    def get(self, url, **kwargs):
        r = self.s.get(self.endpoint + url, **self.extend_with_sessionid(kwargs))
        self._raise_for_status(r)
        return r

    def post(self, url, **kwargs):
        r = self.s.post(self.endpoint + url, **self.extend_with_sessionid(kwargs))
        self._raise_for_status(r)
        return r

    def delete(self, url, **kwargs):
        r = self.s.delete(self.endpoint + url, **self.extend_with_sessionid(kwargs))
        self._raise_for_status(r)
        return r

    def put(self, url, **kwargs):
        r = self.s.put(self.endpoint + url, **self.extend_with_sessionid(kwargs))
        self._raise_for_status(r)
        return r
