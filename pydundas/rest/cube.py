import time
import os


class CubePathNotUnique(Exception):
    pass


class CubeApi:
    """Uses the Api to create an actual cube object."""

    def __init__(self, session=None, api=None):
        self.session = session
        self.api = api

    def getByPath(self, project, path):
        """Return the one cube matching the path, or None."""
        pid = self.api.project().getProjectIdByName(project)
        root_dir, root_id = self._getRootFolderId(pid)
        cubefile = self._getFileByName(
            # If a path starts with '/a' all preceding components are removed
            path=os.path.join(root_dir, os.path.join(root_dir, path[1:] if path.startswith('/') else path)),
            root_folder_id=root_id
        )
        return self.getById(cubefile['id']) if cubefile is not None else None

    def getById(self, cid):
        """Get a cube by its id."""
        return Cube(
            api=self,
            cid=cid,
            data=self.session.get('datacube/' + cid).json()
        )

    def _getRootFolderId(self, pid):
        full_project = self.session.get(f'project/{pid}').json()
        return full_project['dataCubesRootFolder']['fullName'], full_project['dataCubesRootFolder']['id']

    def _getFileByName(self, path, root_folder_id):
        """Does the actual API call."""
        cubedir, _, name = path.rpartition('/')
        matches = self.session.post('file/query', json={
            "queryFileSystemEntriesOptions": {
                "entryIds": [root_folder_id],
                "filter": [{
                        "field": "Location",
                        "operator": "Equals",
                        "Value": cubedir,
                        "options": "None"
                    },
                    {
                        "field": "Name",
                        "operator": "StartsWith",
                        "Value": name,
                        "options": "None"
                    },
                    {
                        "field": "ObjectType",
                        "operator": "In",
                        "options": "None",
                        "value": ["DataCube"]
                    },

                ],
                "pageNumber": 1,
                # We just need to make sure there is only one, so if we get 2+ answers
                # there's an issue
                "pageSize": 2,
                "queryOptions": "RecursiveQuery"
            }}).json()

        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        else:
            raise CubePathNotUnique(f"There are more than one cube at path'{path}'.")


class Cube:
    """Actual cube object."""

    def __init__(self, api, cid, data):
        self.api = api
        self.id = cid
        self.data = data

    def warehouse(self):
        """Triggers a warehousing."""
        self.api.session.post('datacube/warehouse/' + self.id, json={})

    def isWarehousing(self):
        """Is this cube being warehoused right now?"""
        japi = self.api.api.job()
        run = japi.getByIdAndType(
            kind=japi.WAREHOUSE,
            relatedId=self.id
        )

        if run:
            # https://www.dundas.com/support/api-docs/NET/#html/T_Dundas_BI_WebApi_Models_JobData.htm
            return run['status'].lower() == 'running'
        else:
            # It never ran
            return False

    def waitForWarehousingCompletion(self):
        while self.isWarehousing():
            time.sleep(15)
