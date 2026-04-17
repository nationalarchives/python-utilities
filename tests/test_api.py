import json
from unittest import TestCase, mock

from requests import Timeout
from tna_utilities.api import (
    ResourceForbidden,
    ResourceNotFound,
    ResourceUnauthorized,
    SimpleJsonApiClient,
)

MOCK_API_BASE_URL = "http://mockapi.com/"


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(
            self,
            json_data: dict | None,
            status_code: int,
            headers: dict | None = None,
        ):
            self.json_data = json_data
            self.status_code = status_code
            self.headers = headers if headers is not None else {}

        def json(self):
            return self.json_data

    if args[0] == f"{MOCK_API_BASE_URL}happy":
        return MockResponse({"foo": "bar"}, 200)
    elif args[0] == f"{MOCK_API_BASE_URL}badrequest":
        return MockResponse(None, 400)
    elif args[0] == f"{MOCK_API_BASE_URL}unauthorized":
        return MockResponse(None, 401)
    elif args[0] == f"{MOCK_API_BASE_URL}forbidden":
        return MockResponse(None, 403)
    elif args[0] == f"{MOCK_API_BASE_URL}servererror":
        return MockResponse(None, 500)
    elif args[0] == f"{MOCK_API_BASE_URL}timeout":
        raise Timeout("Request timed out")

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(
            self,
            json_data: dict | None,
            status_code: int,
            headers: dict | None = None,
            data: dict | None = None,
            json: dict | None = None,
        ):
            self.status_code = status_code
            self.headers = headers if headers is not None else {}
            self.data = data
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == f"{MOCK_API_BASE_URL}post":
        return MockResponse({"response": "success"}, 200)

    return MockResponse(None, 404)


class TestSimpleJsonApiClient(TestCase):
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_happy(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.get("/happy")
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"foo": "bar"})

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_bad_request(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(Exception):
            client.get("/badrequest")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_not_found(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(ResourceNotFound):
            client.get("/notfound")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_resource_unauthorized(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(ResourceUnauthorized):
            client.get("/unauthorized")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_resource_forbidden(self, mock_get, mock_post):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(ResourceForbidden):
            client.get("/forbidden")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_resource_timeout(self, mock_get, mock_post):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(Timeout):
            client.get("/timeout")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_other_exception(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        with self.assertRaises(Exception):
            client.get("/servererror")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_post(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.post("/post", data={"foo": "bar"})
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"response": "success"})

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_post_json(self, mock_post, mock_get):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        response = client.post("/post", json=json.dumps({"foo": "bar"}))
        self.assertEqual(type(response), dict)
        self.assertDictEqual(response, {"response": "success"})

    def test_default_headers(self):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        self.assertDictEqual(
            client.headers,
            {
                "Cache-Control": "no-cache",
                "Accept": "application/json",
            },
        )

    def test_blank_default_headers(self):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL, default_headers={})
        self.assertDictEqual(
            client.headers,
            {},
        )

    def test_appending_to_default_headers(self):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        client.add_default_header("Authorization", "Bearer token")
        self.assertDictEqual(
            client.headers,
            {
                "Cache-Control": "no-cache",
                "Accept": "application/json",
                "Authorization": "Bearer token",
            },
        )

    def test_updating_default_headers(self):
        client = SimpleJsonApiClient(MOCK_API_BASE_URL)
        client.add_default_header("Accept", "application/xml")
        self.assertDictEqual(
            client.headers,
            {
                "Cache-Control": "no-cache",
                "Accept": "application/xml",
            },
        )

    def test_appending_headers(self):
        client = SimpleJsonApiClient(
            MOCK_API_BASE_URL,
            default_headers={"Authorization": "Bearer token"},
        )
        client.add_default_header("Cache-Control", "no-cache")
        self.assertDictEqual(
            client.headers,
            {
                "Cache-Control": "no-cache",
                "Authorization": "Bearer token",
            },
        )

    def test_custom_default_headers(self):
        client = SimpleJsonApiClient(
            MOCK_API_BASE_URL, default_headers={"Authorization": "Bearer token"}
        )
        self.assertDictEqual(
            client.headers,
            {
                "Authorization": "Bearer token",
            },
        )

    def test_default_params(self):
        client = SimpleJsonApiClient(
            MOCK_API_BASE_URL, default_params={"api_key": "secret"}
        )
        self.assertDictEqual(client.params, {"api_key": "secret"})

    def test_appending_to_default_params(self):
        client = SimpleJsonApiClient(
            MOCK_API_BASE_URL, default_params={"api_key": "secret"}
        )
        client.add_default_parameter("user_id", "12345")
        self.assertDictEqual(client.params, {"api_key": "secret", "user_id": "12345"})

    def test_updating_default_params(self):
        client = SimpleJsonApiClient(
            MOCK_API_BASE_URL, default_params={"api_key": "secret"}
        )
        client.add_default_parameter("api_key", "new_secret")
        self.assertDictEqual(client.params, {"api_key": "new_secret"})
