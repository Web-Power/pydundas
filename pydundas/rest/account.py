class AccountApi:

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def is_api_account(self, account_id):
        account = self.session.get('account/' + account_id).json()
        return account.get('isApiAccount', False)
