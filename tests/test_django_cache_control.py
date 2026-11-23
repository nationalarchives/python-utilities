import importlib.util
import unittest

HAS_DJANGO = importlib.util.find_spec("django") is not None

if HAS_DJANGO:
    import django

    HAS_DJANGO = django.VERSION >= (6, 0)

if HAS_DJANGO:
    from django import conf
    from django.http import HttpResponse
    from django.test import RequestFactory

    from tna_utilities.django import (
        cacheable_duration,
        cacheable_duration_cloudfront,
        do_not_cache,
        set_cache_control,
    )


def setUpModule():
    if HAS_DJANGO:
        if not conf.settings.configured:
            conf.settings.configure(SECRET_KEY="test-secret", INSTALLED_APPS=[])
        django.setup()


@unittest.skipUnless(HAS_DJANGO, "Django 6 requires Python 3.12 or later")
class TestDjangoCacheControl(unittest.TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_cache_control(self):
        cases = [
            (do_not_cache(), "no-store"),
            (cacheable_duration(), "public, max-age=3600"),
            (cacheable_duration(60), "public, max-age=60"),
            (set_cache_control("private, max-age=120"), "private, max-age=120"),
            (cacheable_duration_cloudfront(), "public, max-age=3600"),
            (
                cacheable_duration_cloudfront(60, 120, 30, 15),
                "public, max-age=60, s-maxage=120, stale-while-revalidate=30, stale-if-error=15",
            ),
            (
                cacheable_duration_cloudfront(60, 0, 0, -1),
                "public, max-age=60",
            ),
            (
                cacheable_duration_cloudfront(60, 60),
                "public, max-age=60",
            ),
        ]
        for decorator, expected in cases:
            with self.subTest(expected=expected):
                original = HttpResponse(
                    "OK", status=201, headers={"Cache-Control": "private"}
                )

                @decorator
                def page(request, response=original):
                    return response

                response = page(self.request)
                self.assertIs(response, original)
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.content, b"OK")
                self.assertEqual(response.headers["Cache-Control"], expected)

    def test_metadata_and_argument_forwarding(self):
        def page(request, value):
            """Example view."""
            return HttpResponse(value)

        decorated = set_cache_control("private, max-age=120")(page)
        response = decorated(self.request, value="OK")
        self.assertEqual(response.content, b"OK")
        self.assertEqual(response.headers["Cache-Control"], "private, max-age=120")
        self.assertEqual(decorated.__name__, "page")
        self.assertEqual(decorated.__doc__, "Example view.")
        self.assertIs(decorated.__wrapped__, page)

    def test_outer_decorator_replaces_inner_header(self):
        @set_cache_control("no-store")
        @cacheable_duration(60)
        def page(request):
            return HttpResponse("OK")

        response = page(self.request)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
