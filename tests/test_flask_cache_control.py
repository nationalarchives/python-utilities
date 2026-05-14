import unittest

from flask import Flask

from tna_utilities.flask import cacheable_duration, do_not_cache, set_cache_control


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
