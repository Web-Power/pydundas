import unittest
from pydundas import Api
from pydundas.rest.constant import ConstantIdError, ConstantNameError


class TestConstant(unittest.TestCase):

    # Change constants in the constant class
    @classmethod
    def setUpClass(cls):
        c = Api(None).constant()
        cls.old_constants = c.__class__.constants
        c.__class__.constants = {
            'NAME': 'id'
        }

    # And restore them
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
        self.assertEqual(c.getNameById('id'), 'NAME')

    def test_get_by_valid_name_returns_good_id(self):
        c = self.get_testable_constant()
        self.assertEqual(c.getIdByName('name'), 'id')

    def test_get_by_wrong_id_returns_ConstantIdError(self):
        c = self.get_testable_constant()
        self.assertRaises(ConstantIdError, c.getNameById, 'unknown id')

    def test_get_by_wrong_name_returns_ConstantNameError(self):
        c = self.get_testable_constant()
        self.assertRaises(ConstantNameError, c.getIdByName, 'unknown name')
