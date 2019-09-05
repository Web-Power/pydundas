class AccountApi:

    def __init__(self, session=None, api=None):
        self.session = session
        self.factory = api

    def is_api_account(self, account_id):
        return self.session.get('account/' + account_id).json()['isApiAccount']
