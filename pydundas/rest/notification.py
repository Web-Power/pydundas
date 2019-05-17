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

    def run(self, ids):
        """Run all notifications with given ids. If Id is a string, just run the one."""
        if isinstance(ids, str):
            ids = [ids]

        self.session.post('notification/run', **{'json': ids})

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
