class Api:

    def __init__(self, session):
        self.session = session
        self._project = None

    def project(self):
        if not self._project:
            from .project import Project
            self._project = Project(self.session)

        return self._project
