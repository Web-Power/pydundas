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
        everything = self._getWithFilter(filters=[{
            "field": "Name",
            "operator": "Equals",
            "value": name,
            "options": "None"
        }])

        if len(everything) == 0:
            return None
        elif len(everything) == 1:
            return Notification(
                api=self,
                nid=everything[0]['id'],
                data=everything[0]
            )
        else:
            raise NotificationNameNotUnique(f"There are more than one notification with name '{name}'.")

    def getById(self, nid):
        return Notification(
            api=self,
            nid=nid,
            data=self.session.get(f'notification/{nid}').json()
        )

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


class Notification:
    """Actual notification object."""

    def __init__(self, api, nid, data):
        self.api = api
        self.id = nid
        self.data = data

    def run(self):
        """Run this notification. There is no output
        on success."""
        return self.api.session.post('notification/run', **{'json': [self.id]})

    def isRunning(self):
        """True if the notification is running, false otherwise."""
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
            time.sleep(15)
