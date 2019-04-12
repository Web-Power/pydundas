import importlib


class Api:

    def __init__(self, session):
        self.session = session
        self.define_all([
            'constant',
            'project'
        ])

    def define_all(self, calls):
        """
        After the 3rd copy/paste/replace I went meta.
        All (or most at least) classes will have the same template:
        Create a _apiname attribute holding the instance Apiname(self.session)

        This method gets an array of apinames to create that way, and the magic is done all dynamically.
        In comments are the lines you would need to explicitly write for eg. notification().

        """
        for c in calls:

            # This is the method that will be bound the proper attribute name.
            def template():
                # if not self._notification:
                apimethod = '_ ' + c
                if not getattr(self, apimethod, None):
                    # from .notification import Notification

                    # __module__ is pydundas.rest.api, and relative imports need the package name, which is everything
                    # up to the last dot.
                    pkg = self.__module__.rpartition('.')[0]
                    mod = importlib.import_module('.' + c, pkg)
                    cls = getattr(mod, c.capitalize())

                    # self._notification = Notification(self.session)
                    setattr(self, apimethod, cls(self.session))

                # return self._notification
                return getattr(self, apimethod)

            setattr(self, c, template)
