import requests
from requests import JSONDecodeError, Response, Timeout, TooManyRedirects, codes


class ResourceNotFound(Exception):
    pass


class ResourceForbidden(Exception):
    pass


class SimpleJsonApiClient:
    """
    A simple JSON API client that provides basic functionality for making GET requests to a specified API endpoint.

    It allows for the addition of custom headers and parameters, and handles common HTTP response codes, including 200 (OK), 400 (Bad Request), 403 (Forbidden), and 404 (Not Found).

    The client also includes error handling for connection issues, timeouts, and non-JSON responses.

    :param api_url: The base URL of the API.
    :param defaultHeaders: Optional dictionary of default headers to include in every request.
    :param defaultParams: Optional dictionary of default parameters to include in every request.
    """

    def __init__(
        self, api_url: str, defaultHeaders: dict = {}, defaultParams: dict = {}
    ):
        self.api_url: str = api_url.rstrip("/")
        self.headers: dict = (
            {
                "Cache-Control": "no-cache",
                "Accept": "application/json",
            }
            if defaultHeaders
            else defaultHeaders
        )
        self.params: dict = defaultParams

    def add_parameter(self, key: str, value):
        """
        Add a single parameter to the request.
        """

        self.params[key] = value

    def add_parameters(self, params: dict):
        """
        Add multiple parameters to the request.
        """

        self.params = self.params | params

    def add_header(self, key: str, value):
        """
        Add a single header to the request.
        """

        self.headers[key] = value

    def add_headers(self, headers: dict):
        """
        Add multiple headers to the request.
        """

        self.headers = self.headers | headers

    def get(self, path: str = "/"):
        """
        Make a GET request to the specified path of the API endpoint.
        """

        url = f"{self.api_url}/{path.lstrip('/')}"
        try:
            response = requests.get(
                url,
                params=self.params,
                headers=self.headers,
            )
        except ConnectionError:
            raise Exception("A connection error occured")
        except Timeout:
            raise Exception("The request timed out")
        except TooManyRedirects:
            raise Exception("Too many redirects")
        except Exception as e:
            raise Exception(e)
        return self._handle_response(response)

    def post(
        self, path: str = "/", data: dict | None = None, json: dict | str | None = None
    ):
        """
        Make a POST request to the specified path of the API endpoint.
        """

        url = f"{self.api_url}/{path.lstrip('/')}"
        try:
            response = requests.post(
                url,
                params=self.params,
                headers=self.headers,
                data=data,
                json=json,
            )
        except ConnectionError:
            raise Exception("A connection error occured")
        except Timeout:
            raise Exception("The request timed out")
        except TooManyRedirects:
            raise Exception("Too many redirects")
        except Exception as e:
            raise Exception(e)
        return self._handle_response(response)

    def _handle_response(self, response: Response):
        """
        Handle the API response, checking for common HTTP status codes and returning the JSON content if the request was successful.
        """

        if response.status_code == codes.ok:
            try:
                return response.json()
            except JSONDecodeError:
                raise Exception("Non-JSON response provided")
        if response.status_code == 400:
            raise Exception("Bad request")
        if response.status_code == 403:
            raise ResourceForbidden("Forbidden")
        if response.status_code == 404:
            raise ResourceNotFound("Resource not found")
        raise Exception("Request failed")
