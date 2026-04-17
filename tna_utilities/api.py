import requests
from requests import JSONDecodeError, Response, codes


class ResourceNotFound(Exception):
    pass


class ResourceForbidden(Exception):
    pass


class ResourceUnauthorized(Exception):
    pass


class SimpleJsonApiClient:
    """
    A simple JSON API client that provides basic functionality for making GET requests to a specified API endpoint.

    It allows for the addition of custom headers and parameters, and handles common HTTP response codes, including 200 (OK), 400 (Bad Request), 403 (Forbidden), and 404 (Not Found).

    The client also includes error handling for connection issues, timeouts, and non-JSON responses.

    :param api_url: The base URL of the API.
    :param default_headers: Optional dictionary of default headers to include in every request.
    :param default_params: Optional dictionary of default parameters to include in every request.
    """

    def __init__(
        self,
        api_url: str,
        default_headers: dict | None = None,
        default_params: dict | None = None,
    ):
        self.api_url: str = api_url.rstrip("/")
        self.headers: dict = (
            {
                "Cache-Control": "no-cache",
                "Accept": "application/json",
            }
            if default_headers is None
            else default_headers.copy()
        )
        if default_params is None:
            default_params = {}
        self.params: dict = default_params.copy()

    def add_default_header(self, key: str, value: str) -> "SimpleJsonApiClient":
        """
        Add a single default header to the requests.
        """

        self.headers[key] = value
        return self

    def add_default_headers(self, headers: dict) -> "SimpleJsonApiClient":
        """
        Add multiple default headers to the requests.
        """

        self.headers = self.headers | headers
        return self

    def add_default_parameter(self, key: str, value) -> "SimpleJsonApiClient":
        """
        Add a single default parameter to the requests.
        """

        self.params[key] = value
        return self

    def add_default_parameters(self, params: dict) -> "SimpleJsonApiClient":
        """
        Add multiple default parameters to the requests.
        """

        self.params = self.params | params
        return self

    def _normalise_url(self, path: str) -> str:
        """
        Normalise a URL, avoiding duplicated slashes
        """

        return f"{self.api_url}/{path.lstrip('/')}"

    def get(
        self,
        path: str = "/",
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int = 10,
    ) -> dict:
        """
        Make a GET request to the specified path of the API endpoint.

        :param path: The path to append to the base API URL for the request.
        :param params: Optional dictionary of query parameters to include in the request. These will be merged with any default parameters set for the client.
        :param headers: Optional dictionary of headers to include in the request. These will be merged with any default headers set for the client.
        :param timeout: Timeout in seconds for the request. Defaults to 10.
        """

        url = self._normalise_url(path)
        response = requests.get(
            url,
            params=self.params if params is None else {**self.params, **params},
            headers=self.headers if headers is None else {**self.headers, **headers},
            timeout=timeout,
        )
        return self._handle_response(response)

    def post(
        self,
        path: str = "/",
        data: dict | None = None,
        json: dict | str | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int = 10,
    ) -> dict:
        """
        Make a POST request to the specified path of the API endpoint.

        :param path: The path to append to the base API URL for the request.
        :param data: Optional dictionary, list of tuples, bytes, or file-like
        object to include in the request body.
        :param json: Optional JSON serialisable Python object to send in the request body.
        :param params: Optional dictionary of query parameters to include in the request. These will be merged with any default parameters set for the client.
        :param headers: Optional dictionary of headers to include in the request. These will be merged with any default headers set for the client.
        :param timeout: Request timeout in seconds.
        """

        url = self._normalise_url(path)
        response = requests.post(
            url,
            params=self.params if params is None else {**self.params, **params},
            headers=self.headers if headers is None else {**self.headers, **headers},
            data=data,
            json=json,
            timeout=timeout,
        )
        return self._handle_response(response)

    def _handle_response(self, response: Response) -> dict:
        """
        Handle the API response, checking for common HTTP status codes and returning the JSON content if the request was successful.
        """

        if response.status_code == codes.ok:
            try:
                return response.json()
            except JSONDecodeError:
                raise Exception(
                    f"Non-JSON response provided for URL {response.url} "
                    f"with status {response.status_code}"
                )
        if response.status_code == 400:
            try:
                error_body = response.json()
            except JSONDecodeError:
                error_body = response.text
            raise Exception(f"Bad request for URL '{response.url}': {error_body}")
        if response.status_code == 401:
            raise ResourceUnauthorized("Unauthorized")
        if response.status_code == 403:
            raise ResourceForbidden("Forbidden")
        if response.status_code == 404:
            raise ResourceNotFound("Resource not found")
        body_preview = (response.text or "").strip()
        if body_preview:
            body_preview = body_preview[:500]
            raise Exception(
                f"Request failed with status {response.status_code} for URL {response.url}. "
                f"Response body: {body_preview}"
            )
        raise Exception(
            f"Request failed with status {response.status_code} for URL {response.url}"
        )
