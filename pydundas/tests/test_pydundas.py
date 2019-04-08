import unittest
from pydundas.dundas import Session
from mock import MagicMock, patch


class TestMatch(unittest.TestCase):

    @patch('pydundas.dundas.requests.session')
    def test_get_calls_get(self, req):
        session = Session('user', 'pwd', 'url')

        get = MagicMock()
        req.return_value.get = get

        session.get('an/url')
        get.assert_called()

    @patch('pydundas.dundas.requests.session')
    def test_get_check_raise(self, req):
        session = Session('user', 'pwd', 'url')

        statusraise = MagicMock()
        req.return_value.get.return_value.raise_for_status = statusraise

        session.get('an/url')
        statusraise.assert_called()


