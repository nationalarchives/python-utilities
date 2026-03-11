import json
from unittest import TestCase, mock

from tna_utilities.api import ResourceForbidden, ResourceNotFound, SimpleJsonApiClient

MOCK_API_BASE_URL = "http://mockapi.com/"


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, headers={}):
            self.json_data = json_data
            self.status_code = status_code
            self.headers = headers

    class MockResponseGet(MockResponse):
        def __init__(self, json_data, status_code, headers={}):
            super().__init__(json_data, status_code, headers)

        def json(self):
            return self.json_data

    class MockResponsePost(MockResponse):
        def __init__(self, json_data, status_code, headers={}, data=None, json=None):
            super().__init__(json_data, status_code, headers)
            self.data = data
            self.json = json

    if args[0].upper() == "GET":
        if args[1] == f"{MOCK_API_BASE_URL}happy":
            return MockResponseGet({"foo": "bar"}, 200)
        elif args[1] == f"{MOCK_API_BASE_URL}badrequest":
            return MockResponseGet(None, 400)
        elif args[1] == f"{MOCK_API_BASE_URL}forbidden":
            return MockResponseGet(None, 403)
        elif args[1] == f"{MOCK_API_BASE_URL}servererror":
            return MockResponseGet(None, 500)
    elif args[0].upper() == "POST":
        if args[1] == f"{MOCK_API_BASE_URL}post":
            return MockResponseGet({"foo": "bar"}, 200)

    return MockResponsePost(None, 404)


class TestSimpleJsonApiClient(TestCase):
    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_happy(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.get("/happy")
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"foo": "bar"})
        # called_mock_get_urls = [call.args[1] for call in mock_get.call_args_list if call.args[0].upper() == "GET"]
        # self.assertIn(
        #     f"{MOCK_API_BASE_URL}happy",
        #     called_mock_get_urls,
        # )
        # self.assertEqual(len(called_mock_get_urls), 1)

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_bad_request(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(Exception):
            client.get("/badrequest")

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_not_found(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(ResourceNotFound):
            client.get("/notfound")

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_resource_forbidden(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(ResourceForbidden):
            client.get("/forbidden")

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_other_exception(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(Exception):
            client.get("/servererror")

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_post(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.post("/post", data={"foo": "bar"})
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"foo": "bar"})

    @mock.patch("requests.request", side_effect=mocked_requests)
    def test_post_json(self, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.post("/post", json=json.dumps({"foo": "bar"}))
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"foo": "bar"})
