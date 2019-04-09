class ProjectNotFound(Exception):
    pass


class Project:

    def __init__(self, session):
        self.session = session

    def getProjectIDByName(self, name):
        ll = list(filter(lambda x: x['objectType'] == 'Project' and x['name'] == name, self.getAll()))
        if len(ll):
            return ll[0]['projectId']
        else:
            raise ProjectNotFound("No project named '{}'.".format(name))

    def getAll(self):
        """"Returns json representation of all projects."""
        return self.session.get('Project', **{'params': {'options': 'None'}}).json()
