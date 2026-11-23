import importlib.util
import unittest
from itertools import product

HAS_DJANGO = importlib.util.find_spec("django") is not None

if HAS_DJANGO:
    import django

    HAS_DJANGO = django.VERSION >= (6, 0)

if HAS_DJANGO:
    from django import conf
    from django.http import HttpResponse
    from django.test import Client, override_settings
    from django.urls import path
    from django.utils.csp import CSP
    from django.views.decorators.csp import csp_override

    from tna_utilities.django import csp_settings, security_settings

    def index(request):
        request.session["test"] = "12345"
        return HttpResponse("OK")

    def nonce_view(request):
        return HttpResponse(str(request._csp_nonce))

    @csp_override({"default-src": [CSP.SELF]})
    def overridden_view(request):
        return HttpResponse("OK")

    def existing_headers_view(request):
        response = HttpResponse("OK")
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    urlpatterns = [
        path("", index),
        path("nonce/", nonce_view),
        path("override/", overridden_view),
        path("existing/", existing_headers_view),
    ]


def setUpModule():
    if HAS_DJANGO:
        if not conf.settings.configured:
            conf.settings.configure(
                SECRET_KEY="test-secret",
                ROOT_URLCONF=__name__,
                ALLOWED_HOSTS=["testserver"],
                INSTALLED_APPS=[],
                SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies",
                MIDDLEWARE=[],
            )
        django.setup()


@unittest.skipUnless(HAS_DJANGO, "Django 6 requires Python 3.12 or later")
class TestDjangoSecurity(unittest.TestCase):
    middleware = (
        "django.middleware.csp.ContentSecurityPolicyMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
    )

    def configured(self, **kwargs):
        return override_settings(
            MIDDLEWARE=self.middleware, **security_settings(**kwargs)
        )

    def test_default_headers_and_cookie(self):
        with self.configured():
            response = Client().get("/", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Security-Policy"],
            "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
        )
        self.assertEqual(response["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["Referrer-Policy"], "strict-origin-when-cross-origin")
        cookie = response.cookies["sessionid"]
        self.assertTrue(cookie["secure"])
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertEqual(cookie["max-age"], 86400)

    def test_https_redirect_and_query(self):
        with self.configured():
            response = Client().get("/?test=1")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://testserver/?test=1")
        self.assertIn("Content-Security-Policy", response)

    def test_secure_cookie_and_debug(self):
        for secure, force_https, debug in product((False, True), repeat=3):
            with self.subTest(secure=secure, force_https=force_https, debug=debug):
                with self.configured(
                    session_cookie_secure=secure, force_https=force_https, debug=debug
                ):
                    response = Client().get("/", secure=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    bool(response.cookies["sessionid"]["secure"]),
                    secure or (force_https and not debug),
                )

    def test_native_https_redirect_options(self):
        config = security_settings()
        with override_settings(
            MIDDLEWARE=self.middleware,
            SECURE_SSL_HOST="secure.example.com",
            SECURE_REDIRECT_EXEMPT=[r"^existing/$"],
            **config,
        ):
            client = Client()
            redirect = client.get("/?test=1")
            exempt = client.get("/existing/")
        self.assertEqual(redirect["Location"], "https://secure.example.com/?test=1")
        self.assertEqual(exempt.status_code, 200)

    def test_google_and_typekit_with_custom_csp(self):
        custom = {
            "default-src": [CSP.SELF, "example.com"],
            "img-src": ["img.example.com"],
        }
        with self.configured(
            content_security_policy=custom,
            allow_google_content_security_policy=True,
            allow_typekit_content_security_policy=True,
        ):
            response = Client().get("/", secure=True)
        csp = response["Content-Security-Policy"]
        self.assertIn("default-src 'self' example.com", csp)
        self.assertIn("img-src 'self' img.example.com img.youtube.com", csp)
        self.assertIn("font-src 'self' *.gstatic.com data: use.typekit.net", csp)
        self.assertIn(
            "style-src 'self' ajax.googleapis.com fonts.googleapis.com *.gstatic.com "
            "googletagmanager.com tagmanager.google.com *.typekit.net",
            csp,
        )
        self.assertEqual(custom["img-src"], ["img.example.com"])

    def test_individual_provider_options(self):
        for option, expected in (
            (
                "allow_google_content_security_policy",
                "font-src 'self' *.gstatic.com data:",
            ),
            (
                "allow_typekit_content_security_policy",
                "font-src 'self' use.typekit.net",
            ),
        ):
            with self.subTest(option=option):
                with self.configured(**{option: True}):
                    response = Client().get("/", secure=True)
                self.assertIn(expected, response["Content-Security-Policy"])

    def test_custom_independent_directives_and_referrer_policy(self):
        with self.configured(
            content_security_policy={
                "base-uri": [CSP.SELF],
                "form-action": [CSP.SELF],
                "frame-ancestors": [CSP.SELF],
                "sandbox": ["allow-scripts", "allow-downloads"],
            },
            referrer_policy="no-referrer",
        ):
            response = Client().get("/", secure=True)
        self.assertIn("form-action 'self'", response["Content-Security-Policy"])
        self.assertIn(
            "sandbox allow-scripts allow-downloads", response["Content-Security-Policy"]
        )
        self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_native_csp_nonce_and_override(self):
        with self.configured(
            content_security_policy={"script-src": [CSP.SELF, CSP.NONCE]}
        ):
            client = Client()
            first = client.get("/nonce/", secure=True)
            second = client.get("/nonce/", secure=True)
            overridden = client.get("/override/", secure=True)
        nonce = first.content.decode()
        self.assertIn(f"'nonce-{nonce}'", first["Content-Security-Policy"])
        self.assertNotEqual(nonce, second.content.decode())
        self.assertEqual(overridden["Content-Security-Policy"], "default-src 'self'")

    def test_native_report_only_and_disabled_directive(self):
        config = security_settings(content_security_policy={"form-action": None})
        with override_settings(
            MIDDLEWARE=self.middleware,
            SECURE_CSP_REPORT_ONLY={
                "default-src": [CSP.SELF],
                "report-uri": "/report/",
            },
            **config,
        ):
            response = Client().get("/", secure=True)
        self.assertNotIn("form-action", response["Content-Security-Policy"])
        self.assertEqual(
            response["Content-Security-Policy-Report-Only"],
            "default-src 'self'; report-uri /report/",
        )

    def test_preserves_existing_response_headers(self):
        with self.configured():
            response = Client().get("/existing/", secure=True)
        self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_csp_helper_returns_independent_native_values(self):
        custom = {"script-src": [CSP.SELF, CSP.NONCE], "sandbox": True}
        policy = csp_settings(custom)
        policy["script-src"].append("example.com")
        self.assertEqual(custom["script-src"], [CSP.SELF, CSP.NONCE])
        self.assertIs(policy["sandbox"], True)
        self.assertEqual(csp_settings()["form-action"], [CSP.NONE])
