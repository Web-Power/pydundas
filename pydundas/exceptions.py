class LoginFailedError(Exception):
    """
    Exception raised when login fails.
    """
    pass


class NotLoggedInError(Exception):
    """
    Exception raised when an api call is done before login.
    """
    pass


class YamlNotReadableError(Exception):
    """
    Exception raised a credential file is not readable, for any reason.
    """
    pass
