import json
import time
import os


class CubePathNotUnique(Exception):
    pass


class CubeApi:
    """Uses the Api to create an actual cube object."""

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def getByPath(self, project, path):
        """Return the one cube matching the path, or None."""
        pid = self.factory.project().getProjectIdByName(project)
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

    def __init__(self, api, cid):
        self.api = api
        self.id = cid
        self.data = self._get_data()

    def _get_data(self):
        return self.api.session.get('datacube/' + self.id).json()

    def warehouse(self):
        """Triggers a warehousing."""
        self.api.session.post('datacube/warehouse/' + self.id, json={})

    def json(self):
        """Return proper JSONised data."""
        return json.dumps(self.data)

    def is_checked_out(self):
        # The key 'isCheckedOut' does not exist if the cube is not checked out.
        return self.data.get('isCheckedOut', False)

    def checkout(self):
        self.api.session.put('file/checkout/' + self.id, json={}).json()

    def undocheckout(self):
        self.api.session.post('file/undocheckout/' + self.id, json={}).json()

    def clear_cache(self):
        """Cache is cleared by updating the 'Last modified date'."""
        # Technically another option would be checkout/undo checkout, but then the cube cannot be
        # checked out already for this to work.
        self.api.session.put(f'file/touch/{self.id}', json={})

    def isWarehousing(self):
        """Is this cube being warehoused right now?"""
        japi = self.api.factory.job()
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
