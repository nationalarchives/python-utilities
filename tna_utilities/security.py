class CspGenerator:
    """
    A utility class for generating a Content Security Policy (CSP) header value.

    Lets you incrementally add or disallow directive sources (for example for `script-src` or `style-src`) and then produces a correctly formatted CSP string that can be returned from your application or attached to HTTP responses.

    Typical usage:
        # Create a generator with a default-src of 'self'
        csp = CspGenerator()
        # Add additional directives (methods return self for chaining)
        csp.base_uri("'self'") \
           .connect_src(["'self'", "https://api.example.com"]) \
           .font_src("'self'")

    The ``default_src`` argument to ``__init__`` controls the initial
    ``default-src`` directive. If it is omitted, a default of ``'self'`` is
    used. Helper methods such as ``base_uri``, ``child_src``, ``connect_src``,
    and ``font_src`` delegate to :meth:`add_directive` to add or override
    specific CSP directives.
    """

    NONE: str = "'none'"
    SELF: str = "'self'"

    def __init__(self, default_src: str | list[str] | None = None) -> None:
        self.default_src: list[str] = []
        if default_src:
            if isinstance(default_src, list):
                self.default_src.extend(default_src)
            else:
                self.default_src.append(default_src)
        else:
            self.default_src.append(self.SELF)
        self.directives: dict[str, list[str]] = {
            "default-src": self.default_src,
        }

    def add_directive(
        self, directive: str, values: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a directive.
        """

        # If there are no sources, we don't add the directive
        if values is None:
            return self

        # If sources is not a list, normalise string input into a list by splitting on whitespace
        if isinstance(values, str):
            values = values.split(" ")

        # Split every item in the list of values on whitespace and flatten the resulting lists into a single list of sources
        values = [source for value in values for source in value.split(" ") if source]

        # If nothing valid was parsed, do not add the directive
        if not values:
            return self

        # If the values are the same as the default-src, we don't add the directive for simplicity and to avoid redundancy
        if values == self.default_src:
            return self

        # Unless omit_self is True, add 'self' when either it or 'none' is not specified in the sources
        if not omit_self and self.SELF not in values and self.NONE not in values:
            values.insert(0, self.SELF)

        # Add the directive to the directives dictionary
        self.directives[directive] = values

        # Return self to allow for method chaining
        return self

    def disallow(self, directive: str) -> "CspGenerator":
        """
        Disallow a directive by setting it to 'none'.
        """

        self.directives[directive] = [self.NONE]
        return self

    def base_uri(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a base-uri directive.
        """

        return self.add_directive("base-uri", sources, omit_self)

    def child_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a child-src directive.
        """

        return self.add_directive("child-src", sources, omit_self)

    def connect_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a connect-src directive.
        """

        return self.add_directive("connect-src", sources, omit_self)

    def font_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a font-src directive.
        """

        return self.add_directive("font-src", sources, omit_self)

    def form_action(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a form-action directive.
        """

        return self.add_directive("form-action", sources, omit_self)

    def frame_ancestors(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a frame-ancestors directive.
        """

        return self.add_directive("frame-ancestors", sources, omit_self)

    def frame_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a frame-src directive.
        """

        return self.add_directive("frame-src", sources, omit_self)

    def img_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a img-src directive.
        """

        return self.add_directive("img-src", sources, omit_self)

    def manifest_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a manifest-src directive.
        """

        return self.add_directive("manifest-src", sources, omit_self)

    def media_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a media-src directive.
        """

        return self.add_directive("media-src", sources, omit_self)

    def object_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a object-src directive.
        """

        return self.add_directive("object-src", sources, omit_self)

    def prefetch_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a prefetch-src directive.
        """

        return self.add_directive("prefetch-src", sources, omit_self)

    def report_uri(self, uri: str) -> "CspGenerator":
        """
        Add a report-uri directive.

        The report-uri directive is deprecated in favor of report-to however, it is still supported by a few browsers.

        For new implementations, it is recommended to use report-to instead of report-uri.
        """

        self.directives["report-uri"] = [uri]
        return self

    def report_to(self, endpoint_name: str) -> "CspGenerator":
        """
        Add a report-to directive.

        When using report-to, you need to set a Reporting-Endpoints header with the same endpoint name and the URL to send reports to.

        For example:
            # Add the report-to directive to the CSP
            CspGenerator.report_to("csp-endpoint")

            # Set the header for the Reporting-Endpoints
            Reporting-Endpoints: csp-endpoint="https://example.com/csp-reports"
        """

        self.directives["report-to"] = [endpoint_name]
        return self

    def require_trusted_types_for(self) -> "CspGenerator":
        """
        Add a require-trusted-types-for directive.
        """

        self.directives["require-trusted-types-for"] = ["'script'"]
        return self

    def sandbox(self, value: str | None = None) -> "CspGenerator":
        """
        Add a sandbox directive.
        """

        values = [
            "allow-downloads",
            "allow-forms",
            "allow-modals",
            "allow-orientation-lock",
            "allow-pointer-lock",
            "allow-popups",
            "allow-popups-to-escape-sandbox",
            "allow-presentation",
            "allow-same-origin",
            "allow-scripts",
            "allow-top-navigation",
            "allow-top-navigation-by-user-activation",
            "allow-top-navigation-to-custom-protocols",
        ]
        if value is not None and value in values:
            sources = [value]
        else:
            sources = []

        self.directives["sandbox"] = sources
        return self

    def script_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a script-src directive.
        """

        return self.add_directive("script-src", sources, omit_self)

    def script_src_attr(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a script-src-attr directive.
        """

        return self.add_directive("script-src-attr", sources, omit_self)

    def script_src_elem(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a script-src-elem directive.
        """

        return self.add_directive("script-src-elem", sources, omit_self)

    def style_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a style-src directive.
        """

        return self.add_directive("style-src", sources, omit_self)

    def style_src_attr(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a style-src-attr directive.
        """

        return self.add_directive("style-src-attr", sources, omit_self)

    def style_src_elem(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a style-src-elem directive.
        """

        return self.add_directive("style-src-elem", sources, omit_self)

    def worker_src(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a worker-src directive.
        """

        return self.add_directive("worker-src", sources, omit_self)

    def get_csp(self) -> str:
        """
        Get the complete CSP as a string.
        """

        parts: list[str] = []
        for directive, sources in self.directives.items():
            directive_str = directive
            if sources:
                directive_str += " " + " ".join(sources)
            parts.append(directive_str)
        return "; ".join(parts) + ";"


def security_headers(
    x_frame_options: str | None = None,
    x_permitted_cross_domain_policies: str | None = None,
    cross_origin_embedder_policy: str | None = None,
    cross_origin_opener_policy: str | None = None,
    cross_origin_resource_policy: str | None = None,
) -> dict[str, str]:
    """
    Get a dictionary of common security headers.
    """

    headers = [
        {
            "header": "X-Frame-Options",
            "values": ["DENY", "SAMEORIGIN"],
            "default": "DENY",
            "value": x_frame_options,
        },
        {
            "header": "X-Permitted-Cross-Domain-Policies",
            "values": [
                "none",
                "master-only",
                "by-content-type",
                "by-ftp-filename",
                "all",
                "none-this-response",
            ],
            "default": "none",
            "value": x_permitted_cross_domain_policies,
        },
        {
            "header": "Cross-Origin-Embedder-Policy",
            "values": ["unsafe-none", "require-corp", "credentialless"],
            "default": "unsafe-none",
            "value": cross_origin_embedder_policy,
        },
        {
            "header": "Cross-Origin-Opener-Policy",
            "values": [
                "same-origin",
                "same-origin-allow-popups",
                "unsafe-none",
                "noopener-allow-popups",
            ],
            "default": "same-origin",
            "value": cross_origin_opener_policy,
        },
        {
            "header": "Cross-Origin-Resource-Policy",
            "values": ["same-origin", "same-site", "cross-origin"],
            "default": "same-origin",
            "value": cross_origin_resource_policy,
        },
    ]

    return {
        header["header"]: (
            header["value"]
            if header["value"] is not None and header["value"] in header["values"]
            else header["default"]
        )
        for header in headers
    }
