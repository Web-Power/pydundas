import unittest
from pydundas import Api


class TestApi(unittest.TestCase):

    # Change apis in the api class
    @classmethod
    def setUpClass(cls):
        a = Api(None)
        cls.old_apis = a.__class__.apis
        a.__class__.apis = ['a1', 'a2']

    # And restore them
    @classmethod
    def tearDownClass(cls):
        a = Api(None)
        a.__class__.apis = cls.old_apis

    @staticmethod
    def get_testable_api():
        a = Api(None)
        # a.define_all()
        return a

    def test_all_api_methods_exists(self):
        c = self.get_testable_api()
        # exists...
        self.assertIsNotNone(getattr(c, 'a1', None))
        # ... and is a method.
        self.assertTrue(callable(getattr(c, 'a1', None)))

        self.assertIsNotNone(getattr(c, 'a2', None))
        self.assertTrue(callable(getattr(c, 'a2', None)))
