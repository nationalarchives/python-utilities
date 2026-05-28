import unittest

from flask import Flask

from tna_utilities.flask import (
    cacheable_duration,
    cacheable_duration_cloudfront,
    do_not_cache,
    set_cache_control,
    vary_by_cookies,
    vary_by_headers,
)


class TestFlaskCacheControl(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.test_client = self.app.test_client()

    def test_naked_route(self):
        @self.app.route("/")
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertNotIn("Cache-Control", rv.headers)

    def test_do_not_cache_route(self):
        @self.app.route("/")
        @do_not_cache()
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "no-store",
        )

    def test_cacheable_duration_route(self):
        @self.app.route("/")
        @cacheable_duration()
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "public, max-age=3600",
        )

    def test_cacheable_duration_custom_duration_route(self):
        @self.app.route("/")
        @cacheable_duration(60)
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "public, max-age=60",
        )

    def test_set_cache_control_route(self):
        @self.app.route("/")
        @set_cache_control("private, max-age=120")
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "private, max-age=120",
        )

    def test_vary_by_cookies_route(self):
        @self.app.route("/")
        @vary_by_cookies()
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Vary", rv.headers)
        self.assertEqual(
            rv.headers["Vary"],
            "Cookie",
        )

    def test_vary_by_headers_route(self):
        @self.app.route("/")
        @vary_by_headers("Accept-Encoding, User-Agent")
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Vary", rv.headers)
        self.assertEqual(
            rv.headers["Vary"],
            "Accept-Encoding, User-Agent",
        )

    def test_cache_control_and_vary_by_headers_route(self):
        @self.app.route("/")
        @set_cache_control("private, max-age=120")
        @vary_by_headers("Accept-Encoding, User-Agent")
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Vary", rv.headers)
        self.assertEqual(
            rv.headers["Vary"],
            "Accept-Encoding, User-Agent",
        )
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "private, max-age=120",
        )

    def test_cacheable_duration_cloudfront_route(self):
        @self.app.route("/")
        @cacheable_duration_cloudfront(client_seconds=60, cloudfront_seconds=120)
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "public, max-age=60, s-maxage=120",
        )

    def test_cacheable_duration_cloudfront_route_extras(self):
        @self.app.route("/")
        @cacheable_duration_cloudfront(
            client_seconds=60,
            cloudfront_seconds=120,
            stale_while_revalidate_seconds=30,
            stale_if_error_seconds=15,
        )
        def index():
            return "OK"

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)
        self.assertIn("Cache-Control", rv.headers)
        self.assertEqual(
            rv.headers["Cache-Control"],
            "public, max-age=60, s-maxage=120, stale-while-revalidate=30, stale-if-error=15",
        )
