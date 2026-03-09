import unittest
from unittest import mock
import requests

from tna_utilities.api import ResourceForbidden, ResourceNotFound, SimpleJsonApiClient



def mocked_get_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://mockapi.com/test':
        return MockResponse({"key1": "value1"}, 200)

    return MockResponse(None, 404)



class TestSimpleJsonApiClient(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_get_requests)
    def test_happy(self, mock_get):
        client = SimpleJsonApiClient("http://mockapi.com/")
        response = client.get("/test")
        assert response == {"key1": "value1"}
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"key1": "value1"})
        self.assertIn(mock.call('http://mockapi.com/test'), mock_get.call_args_list)
        self.assertEqual(len(mock_get.call_args_list), 1)


