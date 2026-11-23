import unittest

from content_negotiation_cases import ContentNegotiationCases
from flask import Flask

from tna_utilities.flask import get_requested_accept


class TestFlaskContentNegotiation(ContentNegotiationCases, unittest.TestCase):
    negotiate = staticmethod(get_requested_accept)
    view = staticmethod(lambda handler: handler)

    def setUp(self):
        self.app = Flask(__name__)

    def response(self, body, status=200, headers=None):
        return self.app.response_class(body, status=status, headers=headers)

    def invoke(self, view, accept, *args, **kwargs):
        headers = {} if accept is None else {"Accept": accept}
        with self.app.test_request_context(headers=headers):
            return view(*args, **kwargs)

    @staticmethod
    def body(response):
        return response.get_data(as_text=True)

    def test_tuple_response(self):
        @get_requested_accept(["text/html"])
        def page(*, preferred_content_type):
            return "page content", 202, {"X-Example": "preserved"}

        response = self.invoke(page, None)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.body(response), "page content")
        self.assertEqual(response.headers["X-Example"], "preserved")
        self.assertIn("accept", self.vary(response))
