import time
from copy import deepcopy


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

    def get_subject(self):
        return self.data["deliverySettings"]["subjectTemplate"]

    def set_subject(self, subj):
        """
        Update subject of notification.
        """

        data = deepcopy(self.data)
        data['deliverySettings']['subjectTemplate'] = subj
        self._update(data)

    def get_body(self):
        return self.data["deliverySettings"]["messageTemplate"]

    def set_body(self, subj):
        """
        Update subject of notification.
        """

        data = deepcopy(self.data)
        data['deliverySettings']['messageTemplate'] = subj
        self._update(data)

    def _walk_and_update_bloody_numerics(self, e):
        # Updates the object in place.
        if isinstance(e, dict):
            if e.get('__classType', None) == "dundas.data.SingleNumberValue":
                if e['value'] is not None:
                    # If you have an exception here, it might be because you have a float, not an int.
                    # I do not expect it, though so I do not want to handle it (yet) not knowing what to expect.
                    e['value'] = int(e['value'])
            else:
                for k, v in e.items():
                    self._walk_and_update_bloody_numerics(v)
        elif isinstance(e, list):
            for v in e:
                self._walk_and_update_bloody_numerics(v)
        else:
            # no dict, no list. Could be a string, a number, None... In any case, we do not care
            pass

    def _update(self, data):
        """
        To update a notification, you can just GET its data, change one field and PUT it back.
        Except.
        Except that for some elements, dundas gives a string back (eg. "3") but *requires* an int (ie. 3).
        Except that the item schedule that you GET must be replaced by its child scheduleRule when you PUT.
        """

        data['scheduleRule'] = data.pop('schedule')['scheduleRule']
        data['runImmediately'] = False
        self._walk_and_update_bloody_numerics(data)

        self.api.session.put(f'notification/{self.id}', **{'json': data})
        # The notification has been modified. Let's reload its data.
        self._data_load()

        return
