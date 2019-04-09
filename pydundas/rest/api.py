class Api:

    def __init__(self, session):
        self.session = session

    def project(self):
        if not getattr(self, '_project', None):
            from .project import Project
            self._project = Project(self.session)

        return self._project
