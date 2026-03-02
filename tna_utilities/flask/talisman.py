import flask

from ..security import CspGenerator, common_security_headers

GOOGLE_CSP_POLICY = {
    "default-src": [CspGenerator.SELF, "*.gstatic.com"],
    # Fonts from fonts.google.com
    "font-src": [CspGenerator.SELF, "themes.googleusercontent.com", "*.gstatic.com"],
    # <iframe> based embedding for Maps and Youtube
    "frame-src": [CspGenerator.SELF, "www.google.com", "www.youtube.com"],
    # Assorted Google-hosted Libraries/APIs
    "script-src": [
        CspGenerator.SELF,
        "ajax.googleapis.com",
        "*.googleanalytics.com",
        "*.google-analytics.com",
    ],
    # Used by generated code from http://www.google.com/fonts
    "style-src": [
        CspGenerator.SELF,
        "ajax.googleapis.com",
        "fonts.googleapis.com",
        "*.gstatic.com",
    ],
}


class Talisman(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.app = app
            self.init_app(**kwargs)

    def init_app(
        self,
        content_security_policy: dict = {},
        allow_google_content_security_policy: bool = False,
        security_headers: dict = {},
        referrer_policy: str = "strict-origin-when-cross-origin",
        force_https: bool = True,
        force_https_permanent: bool = False,
    ):
        self.app.config["SESSION_COOKIE_SECURE"] = force_https and not self.app.debug
        self.app.config["SESSION_COOKIE_HTTPONLY"] = True
        self.app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

        self.content_security_policy = content_security_policy
        self.allow_google_content_security_policy = allow_google_content_security_policy
        self.security_headers = security_headers
        self.referrer_policy = referrer_policy
        self.force_https = force_https
        self.force_https_permanent = force_https_permanent

        self.app.before_request(self._force_https_redirect)
        self.app.after_request(self._apply_extra_headers)

    def _force_https_redirect(self):
        criteria = [
            self.app.debug,
            flask.request.is_secure,
            flask.request.headers.get("X-Forwarded-Proto", "http") == "https",
        ]

        if self.force_https and not any(criteria):
            if flask.request.url.startswith("http://"):
                url = flask.request.url.replace("http://", "https://", 1)
                code = 302
                if self.force_https_permanent:
                    code = 301
                r = flask.redirect(url, code=code)
                return r

    def _apply_extra_headers(self, response):
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
        csp = CspGenerator()

        csp.base_uri(content_security_policy.get("base-uri", ""))
        csp.child_src(content_security_policy.get("child-src", ""))
        csp.connect_src(content_security_policy.get("connect-src", ""))
        csp.font_src(content_security_policy.get("font-src", ""))
        csp.form_action(content_security_policy.get("form-action", ""))
        csp.frame_ancestors(content_security_policy.get("frame-ancestors", ""))
        csp.frame_src(content_security_policy.get("frame-src", ""))
        csp.img_src(content_security_policy.get("img-src", ""))
        csp.manifest_src(content_security_policy.get("manifest-src", ""))
        csp.media_src(content_security_policy.get("media-src", ""))
        csp.object_src(content_security_policy.get("object-src", ""))
        csp.prefetch_src(content_security_policy.get("prefetch-src", ""))
        csp.report_uri(content_security_policy.get("report-uri", ""))
        csp.report_to(content_security_policy.get("report-to", ""))
        csp.script_src(content_security_policy.get("script-src", ""))
        csp.script_src_attr(content_security_policy.get("script-src-attr", ""))
        csp.script_src_elem(content_security_policy.get("script-src-elem", ""))
        csp.style_src(content_security_policy.get("style-src", ""))
        csp.style_src_attr(content_security_policy.get("style-src-attr", ""))
        csp.style_src_elem(content_security_policy.get("style-src-elem", ""))
        csp.worker_src(content_security_policy.get("worker-src", ""))
        if "sandbox" in content_security_policy:
            csp.sandbox(content_security_policy["sandbox"])
        if content_security_policy.get("require-trusted-types-for", False):
            csp.require_trusted_types_for()

        if allow_google_content_security_policy:
            csp.default_src(*GOOGLE_CSP_POLICY["default-src"])
            csp.font_src(*GOOGLE_CSP_POLICY["font-src"])
            csp.frame_src(*GOOGLE_CSP_POLICY["frame-src"])
            csp.script_src(*GOOGLE_CSP_POLICY["script-src"])
            csp.style_src(*GOOGLE_CSP_POLICY["style-src"])

        return csp.to_string()
