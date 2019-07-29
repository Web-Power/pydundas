import importlib


class Api:

    apis = [
        'constant',
        'cube',
        'health',
        'job',
        'js',
        'notification',
        'project',
    ]

    def __init__(self, session):
        self.session = session
        self.define_all()

    def define_all(self):
        """
        After the 3rd copy/paste/replace I went meta.
        All (or most at least) classes will have the same template:
        Create a _apiname attribute holding the instance Apiname(self.session)

        This method gets an array of apinames to create that way, and the magic is done all dynamically.
        In comments are the lines you would need to explicitly write for eg. notification().

        """
        for api in self.apis:
            setattr(self, api, self._define_one(api))

    def _define_one(self, c):
        # On its own function to use closure to not have variable reuse inside the for loop.
        def template():
            # if not self._notification:
            apimethod = '_ ' + c
            if not getattr(self, apimethod, None):
                # from .notification import NotificationApi

                # __module__ is pydundas.rest.api, and relative imports need the package name, which is everything
                # up to the last dot.
                pkg = self.__module__.rpartition('.')[0]
                mod = importlib.import_module('.' + c, pkg)
                cls = getattr(mod, c.capitalize() + 'Api')

                # self._notification = Notification (self.session, self)
                setattr(self, apimethod, cls(session=self.session, api=self))

            return getattr(self, apimethod)

        return template
