import time


class UnknownCheckError(Exception):
    pass


class CheckTooLongError(Exception):
    pass


class HealthApi:
    """Uses the Api to create an actual cube object."""

    # Snooped from the GUI
    all_checks = {
        "DBI0010": "Check Application DB Connectivity",
        "DBI0011": "Check Warehouse DB Connectivity",
        "DBI0020": "Check App DB Settings",
        "DBI0021": "Check Warehouse DB Settings",
        "DBI0030": "Check fragmented indexes in App DB",
        "DBI0031": "Check fragmented indexes in Warehouse DB",
        "DBI0040": "Check if Scheduler service is running",
        "DBI0100": "Check for ADSI Hotfix 2683913",
        "DBI0206": "Invalid Child Count",
        "DBI0210": "Invalid Checked-Out References",
        "DBI0211": "Mark Inactive Entries",
        "DBI0212": "Detect Invalid Project IDs",
        "DBI0213": "Invalid Checked-Out Entity Data",
        "DBI0214": "Fix Invalid Inactive Entries",
        "DBI0215": "Find Entities with Missing Data",
        "DBI0216": "Invalid Subentry Revisions",
        "DBI0217": "Orphaned References",
        "DBI0218": "Detect and Fix Privileges Where Everyone Group Has Incorrect Assignee Kind",
        "DBI0219": "Missing Referenced Entities",
        "DBI0220": "Detect and Remove Duplicate Tenant Project Folders",
        "DBI0221": "Circular References",
        "DBI0222": "Orphaned Tenant Overrides",
        "DBI0223": "Detect Invalid Project Temp Folder Privileges",
        "DBI0224": "Detect Invalid Project Privilege Inheritance",
        "DBI0300": "Orphaned Account, Group and Tenant Data",
        "DBI0305": "Detect License Seat Usage Issues",
        "DBI0400": "Check Log Filter Settings",
        "DBI2000": "Detect Unused Warehouse Tables",
        "DBI2010": "Detect Invalid Default Time Dimensions",
        "DBI2015": "Detect Transient and Inactive Native Structures",
        "DBI2020": "Detect and Remove Duplicate Storage Jobs",
        "DBI2025": "Third-Party Drivers for Data Connectors",
        "DBI2030": "Notifications with Invalid Metric Set References",
        "DBI2035": "Detect Missing Warehouse Tables",
    }

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def check(self, checks=[], fix=False, allchecks=False):
        """
            Run specific checks or all checks if all is True.
            :returns List of failing checks IDs. Can be empty.
        """
        if allchecks:
            checks = list(self.all_checks.keys())
        else:
            for c in checks:
                if c not in self.all_checks:
                    raise UnknownCheckError(f"Check {c} does not exists.")

        for c in checks:
            self.session.logger.debug(f"Enqueueing {'and fixing ' if fix else ''}{c}: {self.all_checks[c]}.")

        trigger = self.session.post('health', json={
            'ChecksToIgnore': [],
            'ChecksToRun': checks,
            'FixErrors': fix
        })

        # The output is quoted, and it's not directly valid as query parameter for the GET.
        contextId = trigger.text.replace('"', '')
        status = self._wait_for_completion(contextId)
        return self.find_failing(status)

    def _wait_for_completion(self, contextId):
        """Starting a healthcheck is actually on triggering them. This waits for them to complete."""

        # If the checks are not done after 30 seconds something is really wrong
        timeout = 30
        while True:
            timeout -= 1
            if timeout <= 0:
                raise(CheckTooLongError("Check ran for more than 30 seconds, this is not normal"))

            time.sleep(0.5)
            status = self.session.get("health", params={"contextId": contextId}).json()
            # status is hash with up to 2 (or 3) entries
            # - healthChecks: verbose blahblah about events for all checks (started, completed)
            # - healthCheckResult: only set at the end
            # - Error: (from the doc, not yet seen in real life)

            if 'healthCheckResult' in status:
                return status

    def find_failing(self, status):
        result = status['healthCheckResult']
        if result.get('totalWarnings', 0) + result.get('totalErrors', 0) > 0:
            # Example:
            # "healthChecks": [
            # {
            #   "__classType": "dundas.health.HealthChecks",
            #   "value": [
            #     {
            #       "__classType": "dundas.health.HealthCheckMessage",
            #       "messageAttributes": "None",
            #       "messageTime": "2019-07-29T12:57:48.1569714Z",
            #       "severity": "Information",
            #       "text": "Beginning health check."
            #     },
            failings = {}
            for hc in status['healthChecks']:
                if hc["__classType"] == "dundas.health.HealthChecks":
                    for hcm in hc['value']:
                        if hcm["__classType"] == "dundas.health.HealthCheckMessage":
                            # https://www.dundas.com/support/api-docs/NET/#html/T_Dundas_BI_WebApi_Models_HealthCheckMessageData.htm
                            if hcm['severity'].lower() in ('warning', 'error'):
                                failings[hcm['checkId']] = ''
                                self.session.logger.warn(
                                    "{severity} for {id} (desc): {msg}.".format(
                                        severity=hcm['severity'],
                                        id=hcm['checkId'],
                                        desc=self.all_checks[hcm['checkId']],
                                        msg=hcm['text'],
                                    )
                                )
            return list(failings.keys())
        else:
            return []

    def fix(self, checks=[], allchecks=False):
        """Fix one or more checks"""
        self.check(checks, fix=True, allchecks=allchecks)
