import unittest

from flask import Flask, session
from tna_utilities.flask.talisman import Talisman


class TestTalisman(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "my_secret_key"
        self.app.config["SESSION_COOKIE_SECURE"] = False
        self.app.config["SESSION_COOKIE_HTTPONLY"] = False
        self.app.config["SESSION_COOKIE_SAMESITE"] = None

        @self.app.route("/")
        def index():
            session["test"] = "12345"
            return "OK"

        self.test_client = self.app.test_client()

    def test_naked_app(self):
        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)

        self.assertNotIn("Content-Security-Policy", rv.headers)

        self.assertNotIn("X-Permitted-Cross-Domain-Policies", rv.headers)
        self.assertNotIn("Cross-Origin-Embedder-Policy", rv.headers)
        self.assertNotIn("Cross-Origin-Opener-Policy", rv.headers)
        self.assertNotIn("Cross-Origin-Resource-Policy", rv.headers)

        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn("session=", rv.headers["Set-Cookie"])
        self.assertNotIn("Secure", rv.headers["Set-Cookie"])
        self.assertNotIn("HttpOnly", rv.headers["Set-Cookie"])
        self.assertNotIn("SameSite", rv.headers["Set-Cookie"])

    def test_default_talisman_app(self):
        Talisman(self.app, force_https=False)

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)

        self.assertIn("Content-Security-Policy", rv.headers)
        self.assertEqual(
            "default-src 'self'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
            rv.headers["Content-Security-Policy"],
        )

        self.assertIn("X-Permitted-Cross-Domain-Policies", rv.headers)
        self.assertEqual("none", rv.headers["X-Permitted-Cross-Domain-Policies"])
        self.assertIn("Cross-Origin-Embedder-Policy", rv.headers)
        self.assertEqual("unsafe-none", rv.headers["Cross-Origin-Embedder-Policy"])
        self.assertIn("Cross-Origin-Opener-Policy", rv.headers)
        self.assertEqual("same-origin", rv.headers["Cross-Origin-Opener-Policy"])
        self.assertIn("Cross-Origin-Resource-Policy", rv.headers)
        self.assertEqual("same-origin", rv.headers["Cross-Origin-Resource-Policy"])

        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn("session=", rv.headers["Set-Cookie"])
        self.assertNotIn(" Secure", rv.headers["Set-Cookie"])  # force_https is False
        self.assertIn(" HttpOnly", rv.headers["Set-Cookie"])
        self.assertIn(" SameSite=Lax", rv.headers["Set-Cookie"])

    def test_talisman_app_google(self):
        Talisman(self.app, force_https=False, allow_google_content_security_policy=True)

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 200)

        self.assertIn("Content-Security-Policy", rv.headers)
        self.assertIn("default-src 'self';", rv.headers["Content-Security-Policy"])
        self.assertIn(
            "frame-src 'self' www.google.com www.youtube.com;",
            rv.headers["Content-Security-Policy"],
        )
        self.assertIn(
            "font-src 'self' *.gstatic.com;",
            rv.headers["Content-Security-Policy"],
        )
        self.assertIn(
            "img-src 'self' img.youtube.com;",
            rv.headers["Content-Security-Policy"],
        )
        self.assertIn(
            "script-src 'self' ajax.googleapis.com *.googleanalytics.com *.google-analytics.com www.youtube.com;",
            rv.headers["Content-Security-Policy"],
        )
        self.assertIn(
            "style-src 'self' ajax.googleapis.com fonts.googleapis.com *.gstatic.com;",
            rv.headers["Content-Security-Policy"],
        )

    def test_talisman_force_https(self):
        Talisman(self.app)

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 302)

        self.assertIn("Location", rv.headers)
        self.assertEqual(
            "https://localhost/",
            rv.headers["Location"],
        )

        rv = self.test_client.get("/", follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        self.assertIn("Set-Cookie", rv.headers)
        self.assertIn(" Secure", rv.headers["Set-Cookie"])

    def test_talisman_force_https_permanent(self):
        Talisman(self.app, force_https_permanent=True)

        rv = self.test_client.get("/")

        self.assertEqual(rv.status_code, 301)

        self.assertIn("Location", rv.headers)
        self.assertEqual(
            "https://localhost/",
            rv.headers["Location"],
        )
