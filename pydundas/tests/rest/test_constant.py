import unittest
from pydundas import Api
from pydundas.rest.constant import ConstantIdError, ConstantNameError


class TestConstant(unittest.TestCase):

    # Change constants in the constant class before tests run...
    @classmethod
    def setUpClass(cls):
        c = Api(None).constant()
        cls.old_constants = c.__class__.constants
        c.__class__.constants = {
            'NAME': 'id',
            'NAME1': 'iddup',
            'NAME2': 'iddup',
        }

    # ...and restore them at the end of tests.
    @classmethod
    def tearDownClass(cls):
        c = Api(None).constant()
        c.__class__.constants = cls.old_constants

    @staticmethod
    def get_testable_constant():
        c = Api(None).constant()
        return c

    def test_get_by_valid_id_returns_good_name(self):
        c = self.get_testable_constant()
        self.assertEqual(c.getNamesById('id'), ['NAME'])

    def test_get_by_valid_id_returns_multiple_names(self):
        c = self.get_testable_constant()
        self.assertCountEqual(c.getNamesById('iddup'), ['NAME1', 'NAME2'])

    def test_get_by_valid_name_returns_good_id(self):
        c = self.get_testable_constant()
        self.assertEqual(c.getIdByName('name'), 'id')

    def test_get_by_wrong_id_returns_ConstantIdError(self):
        c = self.get_testable_constant()
        self.assertRaises(ConstantIdError, c.getNamesById, 'unknown id')

    def test_get_by_wrong_name_returns_ConstantNameError(self):
        c = self.get_testable_constant()
        self.assertRaises(ConstantNameError, c.getIdByName, 'unknown name')

    def test_constants_become_attributes(self):
        c = self.get_testable_constant()
        self.assertEqual(c.NAME, 'id')
