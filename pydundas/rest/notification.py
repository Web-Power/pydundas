import time


class NotificationNameNotUnique(Exception):
    pass


class NotificationApi:
    """Uses the Api to create an actual notification object."""

    def __init__(self, session=None, api=None):
        self.session = session
        self.api = api

    def getByName(self, name):
        """Get all notification with this exact name. Case insensitive."""
        everything = self._getIdsWithFilter(filters=[{
            "field": "Name",
            "operator": "Equals",
            "value": name,
            "options": "None"
        }])

        if len(everything) == 0:
            return None
        elif len(everything) == 1:
            return self.getById(everything[0])
        else:
            raise NotificationNameNotUnique(f"There are more than one notification with name '{name}'.")

    def getById(self, nid):
        return Notification(
            api=self,
            nid=nid
        )

    # Default filter: all
    def _getIdsWithFilter(self, filters=[]):
        # Note: the returned data from /query is not the same as GET notification/id.
        # That's why this method only returns IDs, the actual full data can be retrieved later.
        everything = []
        while True:
            batch = self.session.post('notification/query', **{
                # Data snooped from the web UI
                'json': {
                    "pageNumber": 1,
                    "pageSize": 25,  # That's what Dundas uses as default.
                    "orderBy": [{
                        "notificationQueryField": "Name",
                        "sortDirection": "Ascending"
                    }],
                    "filter": filters
                }
            }).json()
            if batch:
                everything += [b['id'] for b in batch]
                pageNumber += 1
            else:
                break
        return everything


class Notification:
    """Actual notification object."""

    def __init__(self, api, nid):
        self.api = api
        self.id = nid
        self._data_load()

    def run(self):
        """Run this notification. There is no output
        on success."""
        return self.api.session.post('notification/run', **{'json': [self.id]})

    def isRunning(self):
        """True if the notification is running, False otherwise."""
        japi = self.api.api.job()
        run = japi.getByIdAndType(
            kind=japi.NOTIFICATION,
            relatedId=self.id
        )

        if run:
            # https://www.dundas.com/support/api-docs/NET/#html/T_Dundas_BI_WebApi_Models_JobData.htm
            return run['status'].lower() == 'running'
        else:
            # It never ran
            return False

    def waitForCompletedRun(self):
        """Wait for the notification in parameter to be complete."""
        while self.isRunning():
            # Notification sending is quick, let's check often.
            time.sleep(2)

    def _data_load(self):
        # Can be called by the constructor or after a change to get the latest complete data.
        self.data = self._get_data()

    def _get_data(self):
        return self.api.session.get(f'notification/{self.id}').json()

