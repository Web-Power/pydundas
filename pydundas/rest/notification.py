import time


class Notification:

    def __init__(self, session):
        self.session = session

    def getContainingName(self, name):
        """Get all notification containing this name. Case insensitive."""
        return self._getWithFilter(filters=[{
            "field": "Name",
            "operator": "Contains",
            "value": name,
            "options": "None"
        }])

    def getExactName(self, name):
        """Get all notification with this exact name. Case insensitive."""
        return self._getWithFilter(filters=[{
            "field": "Name",
            "operator": "Equals",
            "value": name,
            "options": "None"
        }])

    def getById(self, nid):
        return self.session.get(f'notification/{nid}').json()

    def run(self, ids):
        """Run all notifications with given ids. If Id is a string, just run the one. There is no output
        on success."""
        if isinstance(ids, str):
            ids = [ids]

        return self.session.post('notification/run', **{'json': ids})

    def isRunning(self, nid):
        """True if the notification in parameter is running, false otherwise."""
        lastrun = self.getLastRun(nid)
        if lastrun:
            return lastrun['status'].lower() == 'running'.lower()
        else:
            return False

    def waitForCompletedRun(self, nid):
        """Wait for the notification in parameter to be complete."""
        while self.isRunning(nid):
            time.sleep(15)

    def getLastRun(self, nid):
        """Return the Last run of the notification given in ID."""
        pageNumber = 1
        pageSize = 25  # That's what Dundas uses as default.
        while True:
            batch = self.session.post('job/query', **{
                'json': {
                    "queryJobsOptions": {
                        "pageNumber": pageNumber,
                        "pageSize": pageSize,
                        "orderBy": [{
                            "jobQueryField": "LastRunTime",
                            "sortDirection": "Descending"
                        }],
                        "filter": [{
                            "field": "None",
                            "operator": "And",
                            "options": "None",
                            "value": [{
                                "field": "JobKind",
                                "operator": "Equals",
                                "value": "Notification",
                                "options": "None"
                            }, {
                                "field": "Status",
                                "operator": "Equals",
                                "value": "Deleted",
                                "options": "InvertOperator"}],
                        }]
                    }
                }
            }).json()
            if batch:
                for n in batch:
                    if n['relatedItemId'] == nid:
                        return n
            else:
                return None

    # Default filter: all
    def _getWithFilter(self, filters=[]):

        everything = []
        pageNumber = 1
        pageSize = 25  # That's what Dundas uses as default.
        while True:
            batch = self.session.post('notification/query', **{
                # Data snooped from the web UI
                'json': {
                    "pageNumber": pageNumber,
                    "pageSize": pageSize,
                    "orderBy": [{
                        "notificationQueryField": "Name",
                        "sortDirection": "Ascending"
                    }],
                    "filter": filters
                }
            }).json()
            if batch:
                everything += batch
                pageNumber += 1
            else:
                break

        return everything
