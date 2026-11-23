import importlib.util
import unittest
from functools import wraps

from content_negotiation_cases import ContentNegotiationCases

HAS_DJANGO = importlib.util.find_spec("django") is not None

if HAS_DJANGO:
    import django

    HAS_DJANGO = django.VERSION >= (6, 0)

if HAS_DJANGO:
    from django import conf
    from django.http import HttpResponse
    from django.test import RequestFactory

    from tna_utilities.django import get_requested_accept


def setUpModule():
    if HAS_DJANGO:
        if not conf.settings.configured:
            conf.settings.configure(SECRET_KEY="test-secret", INSTALLED_APPS=[])
        django.setup()


@unittest.skipUnless(HAS_DJANGO, "Django 6 requires Python 3.12 or later")
class TestDjangoContentNegotiation(ContentNegotiationCases, unittest.TestCase):
    if HAS_DJANGO:
        negotiate = staticmethod(get_requested_accept)

    def setUp(self):
        self.factory = RequestFactory()

    @staticmethod
    def view(handler):
        @wraps(handler)
        def wrapped(request, *args, **kwargs):
            return handler(*args, **kwargs)

        return wrapped

    @staticmethod
    def response(body, status=200, headers=None):
        return HttpResponse(body, status=status, headers=headers)

    def invoke(self, view, accept, *args, **kwargs):
        headers = {} if accept is None else {"HTTP_ACCEPT": accept}
        request = self.factory.get("/", **headers)
        return view(request, *args, **kwargs)

    @staticmethod
    def body(response):
        return response.content.decode()
