import unittest
from unittest.mock import patch
from pydundas import Api
from pydundas.rest.constant import ConstantIdError, ConstantNameError, ConstantApi


class TestConstant(unittest.TestCase):

    # Will be used to mock the actual constants.
    mocked_constants = {
            'NAME': 'id',
            'NAME1': 'iddup',
            'NAME2': 'iddup',
        }

    def test_get_by_valid_id_returns_good_name(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertEqual(c.getNamesById('id'), ['NAME'])

    def test_get_by_valid_id_returns_multiple_names(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertCountEqual(c.getNamesById('iddup'), ['NAME1', 'NAME2'])

    def test_get_by_valid_name_returns_good_id(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertEqual(c.getIdByName('name'), 'id')

    def test_get_by_wrong_id_returns_ConstantIdError(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertRaises(ConstantIdError, c.getNamesById, 'unknown id')

    def test_get_by_wrong_name_raises_ConstantNameError(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertRaises(ConstantNameError, c.getIdByName, 'unknown name')

    def test_constants_become_attributes(self):
        with patch.dict(ConstantApi.constants, self.mocked_constants, clear=True):
            c = Api(None).constant()
            self.assertEqual(c.NAME, 'id')
