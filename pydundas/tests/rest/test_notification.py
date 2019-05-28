import json
import unittest
from pydundas import Api
from pydundas.rest.notification import Notification
from mock import MagicMock


class TestNotification(unittest.TestCase):

    def test_no_syntax_error(self):
        self.assertIsNotNone(Api(None).notification())

    @staticmethod
    def _numeric_cases():
        return [
            {
                'what': 'Empty array',
                'src': [], 'dst': []
            }, {
                'what': 'Non empty array',
                'src': [1, '3', 're'], 'dst': [1, '3', 're']
            }, {
                'what': 'Nested array',
                'src': [[1], [['32']]], 'dst': [[1], [['32']]]
            },

            {
                'what': 'Empty dict',
                'src': {}, 'dst': {}
            }, {
                'what': 'Non empty dict',
                'src': {'a': 2, 3: '4'}, 'dst': {'a': 2, 3: '4'}
            }, {
                'what': 'Nested dict',
                'src': {1: {1: 3}, 'a': 42}, 'dst': {1: {1: 3}, 'a': 42}
            },

            {
                'what': 'Scalar number',
                'src': 1, 'dst': 1
            }, {
                'what': 'Scalar number-looking string',
                'src': '1', 'dst': '1'
            }, {
                'what': 'Scalar class string',
                'src': "dundas.data.SingleNumberValue", 'dst': "dundas.data.SingleNumberValue"
            },

            {
                'what': 'SingleNumberValue - no change',
                'src': {'__classType': 'dundas.data.SingleNumberValue', 'value': 42},
                'dst': {'__classType': 'dundas.data.SingleNumberValue', 'value': 42}

            }, {
                'what': 'SingleNumberValue - str to int',
                'src': {'__classType': 'dundas.data.SingleNumberValue', 'value': '42'},
                'dst': {'__classType': 'dundas.data.SingleNumberValue', 'value': 42}
            }, {
                'what': 'SingleNumberValue with None - no change',
                'src': {'__classType': 'dundas.data.SingleNumberValue', 'value': None},
                'dst': {'__classType': 'dundas.data.SingleNumberValue', 'value': None}
            }
        ]

    def test__walk_and_update_bloody_numerics(self):
        """Testing the rewriting from the GET json to PUT json."""
        api = MagicMock()
        n = Notification(nid=42, api=api)
        for c in self._numeric_cases():
            # Tofix: updates inplace
            n._walk_and_update_bloody_numerics(c['src'])
            self.assertEqual(
                json.dumps(c['src']),
                json.dumps(c['dst']),
                f"Case {c['what']} is going wrong"
            )

    def test__walk_and_update_bloody_numerics_raises_ValueError_for_float(self):
        api = MagicMock()
        n = Notification(nid=42, api=api)
        with self.assertRaises(ValueError, msg="Float conversion is not supposed to be handled yet."):
            n._walk_and_update_bloody_numerics({'__classType': 'dundas.data.SingleNumberValue', 'value': '42.3'})
