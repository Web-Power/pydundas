class UnknowJobKindException(Exception):
    pass


class JobApi:

    NOTIFICATION = 'Notification'
    WAREHOUSE = 'UpdateDataWarehouse'

    known_kinds = [NOTIFICATION, WAREHOUSE]

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def getByIdAndType(self, relatedId, kind):
        """Get a job by ID of its relation (notification or cube) and kind. Expects a unique result."""
        if kind not in self.known_kinds:
            raise UnknowJobKindException(f"Jobkind {kind} unknown. Expects one of {self.known_kinds}.")

        jobs = self.session.post('job/query/', json={
            "queryJobsOptions": {
                "filter": [
                    {
                        "field": "JobKind",
                        "operator": "Equals",
                        "value": kind
                    },
                    {
                        "field": "relatedItemId",
                        "operator": "Equals",
                        "value": relatedId
                    }
                ],
                "pageNumber": 1,
                # If there are more than 1, there is an issue. Let's accept at least 2 to check.
                "pageSize": 2
            }
        }).json()
        if len(jobs) == 0:
            # It never ran
            return None
        elif len(jobs) == 1:
            # https://www.dundas.com/support/api-docs/NET/#html/T_Dundas_BI_WebApi_Models_JobData.htm
            return jobs[0]
        else:
            raise RuntimeError(f"More than one {kind} job found for id {relatedId}. It does not make sense.")
