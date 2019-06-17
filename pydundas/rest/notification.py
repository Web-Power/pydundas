import json
import time
from copy import deepcopy


class NotificationNameNotUnique(Exception):
    pass


class NotificationApi:
    """Uses the Api to create an actual notification object."""

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def getByName(self, name):
        """Get all notifications with this exact name. Case insensitive."""
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
            raise NotificationNameNotUnique(f"There is more than one notification with name '{name}'.")

    def getById(self, nid):
        return Notification(
            api=self,
            nid=nid
        )

    # Default filter: all
    def _getIdsWithFilter(self, filters=[]):
        # Note: the returned data from /query is incomplete.
        # That's why this method only returns IDs, the actual full data can be retrieved later.
        everything = []
        pageNumber = 1
        while True:
            batch = self.session.post('notification/query', **{
                # Data snooped from the web UI
                'json': {
                    "pageNumber": pageNumber,
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
        # When updating parts of the notification, all changes are added in there and can be 'commited' via update()
        # to prevent having multiple small updates.
        self.updated_data = None

    def run(self):
        """Run this notification. There is no output
        on success."""
        return self.api.session.post('notification/run', **{'json': [self.id]})

    def isRunning(self):
        """True if the notification is running, False otherwise."""
        japi = self.api.factory.job()
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
        self._prepare_data_for_update()
        self.updated_data['deliverySettings']['subjectTemplate'] = subj

    def get_body(self):
        return self.data["deliverySettings"]["messageTemplate"]

    def set_body(self, subj):
        """
        Update body of notification.
        """
        self._prepare_data_for_update()
        self.updated_data['deliverySettings']['messageTemplate'] = subj

    def get_recipients(self):
        """Returns all recipients."""
        return self.data['deliverySettings']['recipients']

    def set_recipients(self, rcpt_list):
        """Completely replaces recipient list.
        Can be used to remove them all by passing [].
        The caller needs to take care of passing the right object(s).
        """
        if not (isinstance(rcpt_list, list) or isinstance(rcpt_list, tuple)):
            raise ValueError('set_recipients() expects a list of recipients. It got neither a list nor a tuple.')

        self._prepare_data_for_update()
        self.updated_data['deliverySettings']['recipients'] = rcpt_list

    def add_email_recipient(self, email):
        """Add one email recipient to the recipient list."""
        self._prepare_data_for_update()
        self.updated_data['deliverySettings']['recipients'].append(
            self.api.factory.js().notificationRecipient(email)
        )

    def _prepare_data_for_update(self):
        if not self.updated_data:
            self.updated_data = deepcopy(self.data)

    def _walk_and_update_bloody_numerics(self, e):
        if isinstance(e, dict):
            # Trying very hard to not touch the initial object
            newe = deepcopy(e)
            if newe.get('__classType', None) == "dundas.data.SingleNumberValue":
                if newe['value'] is not None:
                    # If you have an exception here, it might be because you have a float, not an int.
                    # I do not expect it, though so I do not want to handle it (yet) not knowing what to expect.
                    newe['value'] = int(newe['value'])
                # I know that such a dict is a leaf
                return newe
            else:
                return {k: self._walk_and_update_bloody_numerics(v) for k, v in e.items()}
        elif isinstance(e, list):
            return [self._walk_and_update_bloody_numerics(v) for v in e]
        else:
            # no dict, no list. Could be a string, a number, None... In any case, we do not care
            return e

    def update(self):
        """
        To update a notification, you can just GET its data, change one field and PUT it back.
        Except.
        Except that for some elements, dundas gives a string back (eg. "3") but *requires* an int (ie. 3).
        Except that the item schedule that you GET must be replaced by its child scheduleRule when you PUT.
        """
        self.updated_data['scheduleRule'] = self.updated_data.pop('schedule')['scheduleRule']
        self.updated_data['runImmediately'] = False
        put_ready = self._walk_and_update_bloody_numerics(self.updated_data)

        self.api.session.put(f'notification/{self.id}', **{'json': put_ready})
        # The notification has been modified. Let's reload its data and remove old updates.
        self.updated_data = None
        self._data_load()

        return

    def json(self):
        """Return proper JSONised data."""
        return json.dumps(self.data)
