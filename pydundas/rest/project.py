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
        return self.session.get('Project', **{'params': {'options': 'IncludeChildren'}}).json()

    def getRootFolderIdForProject(self, project_name, resource_type):
        type_to_apiname = {
            "cubeperspectives": "cubePerspectivesRootFolder",
            "dashboards": "dashboardsRootFolder",
            "dataconnectors": "dataConnectorsRootFolder",
            "datacubes": "dataCubesRootFolder",
            "dataresources": "dataResourcesRootFolder",
            "diagramresources": "diagramResourcesRootFolder",
            "hierarchies": "hierarchiesRootFolder",
            "imageresources": "imageResourcesRootFolder",
            "mapresources": "mapResourcesRootFolder",
            "metricsets": "metricSetsRootFolder",
            "reports": "reportsRootFolder",
            "scorecards": "scorecardsRootFolder",
            "slideshows": "slideshowsRootFolder",
            "smallmultiples": "smallMultiplesRootFolder",
            "styles": "stylesRootFolder",
            "themes": "themesRootFolder",
            "timedimensions": "timeDimensionsRootFolder",
        }
        dir_attr = type_to_apiname.get(resource_type.lower(), None)
        if dir_attr:
            # print(self.getProjectByName(project_name)[dir_attr])
            return self.getProjectByName(project_name)[dir_attr]['id']
        else:
            raise Exception("Need a valid resource folder type. Got '{got}' but expected one of: {expect}.".format(
                got=resource_type,
                expect=', '.join(type_to_apiname.keys())
            ))
