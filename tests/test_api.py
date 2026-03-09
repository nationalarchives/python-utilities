import unittest
from unittest import mock

from tna_utilities.api import ResourceForbidden, ResourceNotFound, SimpleJsonApiClient


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].upper() == "GET":
        if args[1] == "http://mockapi.com/happy":
            return MockResponse({"foo": "bar"}, 200)

    return MockResponse(None, 404)


class TestSimpleJsonApiClient(unittest.TestCase):
    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_happy(self, mock_get):
        client = SimpleJsonApiClient("http://mockapi.com/")
        response = client.get("/happy")
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"foo": "bar"})
        self.assertIn(
            mock.call("GET", "http://mockapi.com/happy", params={}, headers={}),
            mock_get.call_args_list,
        )
        self.assertEqual(len(mock_get.call_args_list), 1)
