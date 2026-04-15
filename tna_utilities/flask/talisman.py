from urllib.parse import urlparse, urlunparse

import flask

from ..security import CspGenerator, common_security_headers

GOOGLE_CSP_POLICY = {
    # "default-src": ["*.gstatic.com"],
    # Fonts from fonts.google.com
    "font-src": ["*.gstatic.com"],
    # <iframe> based embedding for Maps and Youtube
    "frame-src": ["www.google.com", "www.youtube.com"],
    # YouTube video thumbnails
    "img-src": ["img.youtube.com"],
    # Assorted Google-hosted Libraries/APIs
    "script-src": [
        "ajax.googleapis.com",
        "*.googleanalytics.com",
        "*.google-analytics.com",
        "www.youtube.com",
    ],
    # Google Fonts stylesheets and YouTube embedded player styles
    "style-src": [
        "ajax.googleapis.com",
        "fonts.googleapis.com",
        "*.gstatic.com",
    ],
}


class Talisman(object):
    """
    A stripped-down and opinionated reproduction of [wntrblm/flask-talisman](https://github.com/wntrblm/flask-talisman) which is a fork of [GoogleCloudPlatform/flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman).

    Neither GoogleCloudPlatform/flask-talisman nor wntrblm/flask-talisman appears to be actively maintained.

    :param app: The Flask application instance to which the Talisman extension should be applied.
    """

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.app = app
            self.init_app(app, **kwargs)

    def init_app(
        self,
        app: flask.Flask,
        content_security_policy: dict = {},
        allow_google_content_security_policy: bool = False,
        security_headers: dict = {},
        referrer_policy: str = "strict-origin-when-cross-origin",
        force_https: bool = True,
        force_https_permanent: bool = False,
    ):
        """
        Initialises the Talisman extension for the Flask app.

        :param content_security_policy: A dictionary defining the Content Security Policy directives and their values.
        :param allow_google_content_security_policy: If True, includes Google's recommended Content Security Policy directives in addition to the custom directives specified in content_security_policy.
        :param security_headers: A dictionary of additional security headers to apply to responses, where the keys are header names and the values are header values.
        :param referrer_policy: The Referrer-Policy header value to apply to responses. Defaults to "strict-origin-when-cross-origin".
        :param force_https: If True, forces incoming requests to be redirected to HTTPS if they are not already secure and the application is not in debug mode. Defaults to True.
        :param force_https_permanent: If True, uses a permanent redirect (HTTP 301) when forcing HTTPS, otherwise uses a temporary redirect (HTTP 302). Defaults to False.
        """

        self.app = app

        self.app.config.update(
            SESSION_COOKIE_SECURE=force_https and not self.app.debug,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",
            PERMANENT_SESSION_LIFETIME=86400,  # 1 day
        )

        self.content_security_policy = content_security_policy
        self.allow_google_content_security_policy = allow_google_content_security_policy
        self.security_headers = security_headers
        self.referrer_policy = referrer_policy
        self.force_https = force_https
        self.force_https_permanent = force_https_permanent

        self.app.before_request(self._force_https_redirect)
        self.app.after_request(self._apply_extra_headers)

    def _force_https_redirect(self):
        """
        Redirects incoming requests to HTTPS if the request is not secure and the application is not in debug mode.
        """

        criteria = [
            self.app.debug,
            flask.request.is_secure,
            flask.request.headers.get("X-Forwarded-Proto", "http") == "https",
        ]

        if self.force_https and not any(criteria):
            if flask.request.url.startswith("http://"):
                parsed = urlparse(flask.request.url)
                secure_parsed = parsed._replace(scheme="https", fragment="")
                target = urlunparse(secure_parsed)
                code = 302
                if self.force_https_permanent:
                    code = 301
                r = flask.redirect(target, code=code)
                return r

        return None

    def _apply_extra_headers(self, response):
        """
        Applies the configured security headers to the response.
        """

        response.headers["Content-Security-Policy"] = self._csp(
            self.content_security_policy, self.allow_google_content_security_policy
        )
        response.headers.update(common_security_headers(**self.security_headers))
        response.headers["Referrer-Policy"] = self.referrer_policy
        return response

    def _csp(
        self,
        content_security_policy: dict,
        allow_google_content_security_policy: bool = False,
    ):
        """
        Generates a Content-Security-Policy header value based on the provided content security policy configuration and the option to include Google's recommended content security policy directives.
        """

        csp = CspGenerator(default_src=content_security_policy.get("default-src", ""))

        property_methods = [
            ("base-uri", csp.base_uri),
            ("child-src", csp.child_src),
            ("connect-src", csp.connect_src),
            ("font-src", csp.font_src),
            ("form-action", csp.form_action),
            ("frame-ancestors", csp.frame_ancestors),
            ("frame-src", csp.frame_src),
            ("img-src", csp.img_src),
            ("manifest-src", csp.manifest_src),
            ("media-src", csp.media_src),
            ("object-src", csp.object_src),
            ("prefetch-src", csp.prefetch_src),
            ("report-uri", csp.report_uri),
            ("report-to", csp.report_to),
            ("script-src", csp.script_src),
            ("script-src-attr", csp.script_src_attr),
            ("script-src-elem", csp.script_src_elem),
            ("style-src", csp.style_src),
            ("style-src-attr", csp.style_src_attr),
            ("style-src-elem", csp.style_src_elem),
            ("worker-src", csp.worker_src),
        ]
        for directive, method in property_methods:
            method(content_security_policy.get(directive, ""))

        if "sandbox" in content_security_policy:
            csp.sandbox(content_security_policy["sandbox"])

        if content_security_policy.get("require-trusted-types-for", False):
            csp.require_trusted_types_for()

        if allow_google_content_security_policy:
            for x, y in GOOGLE_CSP_POLICY.items():
                csp.add_directive(x, *y)

        return csp.to_string()
