class CspGenerator:
    """
    A utility class to generate a CSP.
    """

    CSP_NONE: str = "'none'"
    CSP_SELF: str = "'self'"

    def __init__(self, default_src: str | list[str] | None = None) -> None:
        self.default_src: list[str] = []
        if default_src:
            if isinstance(default_src, list):
                self.default_src.extend(default_src)
            else:
                self.default_src.append(default_src)
        else:
            self.default_src.append(self.CSP_SELF)
        self.directives: dict = {
            "default-src": self.default_src,
        }

    def add_directive(
        self, directive: str, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a directive.
        """

        # If there are no sources, we don't add the directive
        if sources is None:
            return self

        # If sources is not a list, we convert it to a list
        if not isinstance(sources, list):
            # If there are spaces in the sources, we split it into a list, otherwise we create a list with the single source
            if " " in sources:
                sources = sources.split(" ")
            else:
                sources = [sources]

        # If the sources are the same as the default-src, we don't add the directive
        if sources == self.default_src:
            return self

        # If the option is not passed to omit self and self or none is not already in the sources, we add self to the beginning of the sources
        if (
            not omit_self
            and self.CSP_SELF not in sources
            and self.CSP_NONE not in sources
        ):
            sources.insert(0, self.CSP_SELF)

        # Add the directive to the directives dictionary
        self.directives[directive] = sources

        # Return self to allow for method chaining
        return self

    def disallow(self, directive: str) -> "CspGenerator":
        """
        Disallow a directive by setting it to 'none'.
        """

        self.directives[directive] = [self.CSP_NONE]
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

    # def fenced_frame_src(
    #     self, sources: str | list[str] | None = None, omit_self=False
    # ) -> "CspGenerator":
    #     """
    #     Add a fenced-frame-src directive.
    #     """

    #     return self.add_directive("fenced-frame-src", sources, omit_self)

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

    def report_to(self, uri: str) -> "CspGenerator":
        """
        Add a report-to directive.
        """

        # The report-uri directive has been deprecated in favor of report-to, but we will add both for backwards compatibility
        self.directives["report-uri"] = [uri]
        self.directives["report-to"] = [uri]
        return self

    def require_trusted_types_for(self) -> "CspGenerator":
        """
        Add a require-trusted-types-for directive.
        """

        self.directives["require-trusted-types-for"] = ["'script'"]
        return self

    def sandbox(
        self, sources: str | list[str] | None = None, omit_self=False
    ) -> "CspGenerator":
        """
        Add a sandbox directive.
        """

        return self.add_directive("sandbox", sources, omit_self)

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

    # def trusted_types(
    #     self, sources: str | list[str] | None = None, omit_self=False
    # ) -> "CspGenerator":
    #     """
    #     Add a trusted-types directive.
    #     """

    #     return self.add_directive("trusted-types", sources, omit_self)

    # def upgrade_insecure_requests(
    #     self, sources: str | list[str] | None = None, omit_self=False
    # ) -> "CspGenerator":
    #     """
    #     Add a upgrade-insecure-requests directive.
    #     """

    #     self.directives["upgrade-insecure-requests"] = []
    #     return self

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
            if header["value"] is not None
            and header["value"] in header["values"]
            else header["default"]
        )
        for header in headers
    }
