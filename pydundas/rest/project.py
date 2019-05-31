class ProjectNotFound(Exception):
    pass


class ProjectApi:

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def getProjectIdByName(self, name):
        """Return a project Id based on its exact name."""
        return self.getProjectByName(name)['projectId']

    def getProjectByName(self, name):
        """Returns the first project with the name given in parameter. The output will contain the whole project
        definition."""
        ll = list(filter(lambda x: x['objectType'] == 'Project' and x['name'] == name, self.getAll()))
        if len(ll):
            return ll[0]
        else:
            raise ProjectNotFound("No project named '{}'.".format(name))

    def getAll(self):
        """"Returns json representation of all projects."""
        return self.session.get('Project', **{'params': {'options': 'None'}}).json()
