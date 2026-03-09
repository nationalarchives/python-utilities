from unittest import TestCase, mock

from tna_utilities.api import ResourceForbidden, ResourceNotFound, SimpleJsonApiClient

MOCK_API_BASE_URL = "http://mockapi.com/"


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, headers={}):
            self.json_data = json_data
            self.status_code = status_code
            self.headers = headers

        def json(self):
            return self.json_data

    if args[0].upper() == "GET":
        if args[1] == f"{MOCK_API_BASE_URL}happy":
            return MockResponse({"foo": "bar"}, 200)
        elif args[1] == f"{MOCK_API_BASE_URL}badrequest":
            return MockResponse(None, 400)
        elif args[1] == f"{MOCK_API_BASE_URL}forbidden":
            return MockResponse(None, 403)
        elif args[1] == f"{MOCK_API_BASE_URL}servererror":
            return MockResponse(None, 500)

    return MockResponse(None, 404)


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
