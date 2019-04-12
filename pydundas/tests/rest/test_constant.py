import unittest
from pydundas import Api
from pydundas.rest.constant import ConstantIdError, ConstantNameError


class TestPydundas(unittest.TestCase):

    @staticmethod
    def get_testable_constant():
        c = Api(None).constant()
        c.__class__.constants = {
            'NAME': 'id'
        }
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
