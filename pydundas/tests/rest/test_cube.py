import unittest
from pydundas import Api


class TestCube(unittest.TestCase):

    def test_no_syntax_error(self):
        self.assertIsNotNone(Api(None).cube())
