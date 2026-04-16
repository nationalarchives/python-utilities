from collections import OrderedDict


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

    :param default_src: The sources for the default-src directive, which serves as a fallback for any directives that are not explicitly set. This can be a string or a list of strings. If not provided, it defaults to "'self'".
    :param allow_objects: If True, allows the use of the object-src directive with a default value of "'self'". If False (the default), disallows the use of the object-src directive by setting it to "'none'".
    """

    NONE = "'none'"
    SELF = "'self'"
    STRICT_DYNAMIC = "'strict-dynamic'"
    UNSAFE_EVAL = "'unsafe-eval'"
    UNSAFE_HASHES = "'unsafe-hashes'"
    UNSAFE_INLINE = "'unsafe-inline'"
    WASM_UNSAFE_EVAL = "'wasm-unsafe-eval'"

    def __init__(
        self,
        default_src: str | list[str] | None = None,
        allow_objects: bool = False,
        allow_iframe_embedding: bool = False,
        allow_children: bool = False,
    ) -> None:
        self.default_src_sources: list[str] = []
        if default_src:
            if isinstance(default_src, list):
                self.default_src_sources.extend(default_src)
            else:
                self.default_src_sources.append(default_src)
        self.default_src_sources = [src for src in self.default_src_sources if src]
        if not self.default_src_sources:
            self.default_src_sources = [self.SELF]
        self.directives: OrderedDict[str, list[str]] = OrderedDict(
            {
                "default-src": self.default_src_sources,
            }
        )
        if not allow_objects:
            self.disallow("object-src")
        if not allow_iframe_embedding:
            self.disallow("frame-ancestors")
        if not allow_children:
            self.disallow("child-src")

    def _process_sources(self, *values: str | list[str]) -> list[str]:
        """
        Process the sources input, which can be a string or a list of strings, and return a flat list of sources.
        """

        processed_values: list[str] = []
        for value in values:
            if isinstance(value, str):
                processed_values.extend(value.split(" "))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        processed_values.extend(item.split(" "))

        # Remove empty strings
        processed_values = [src for src in processed_values if src]

        # Remove duplicates while preserving order
        processed_values = list(dict.fromkeys(processed_values))

        return processed_values

    def add_directive(
        self, directive: str, *values: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a directive.

        :param directive: The name of the directive to add (e.g. "script-src").
        :param values: The sources for the directive, which can be strings or lists of strings. If a string contains spaces, it will be split into multiple sources.
        :param omit_self: If True, the 'self' source will not be automatically added if it is not included in the provided sources. Defaults to False.
        :param replace: If True, the directive will be replaced if it already exists. If False (the default), the new sources will be added to the existing directive, ensuring no duplicates. If the existing directive is set to "'none'", it will be replaced regardless of the value of replace.
        """

        # Flatten the values into a single list of strings, splitting any strings that contain spaces into multiple sources
        processed_values = self._process_sources(*values)

        # If nothing valid was parsed, do not add the directive
        if not processed_values:
            return self

        # Unless omit_self is True, add 'self' when either it or 'none' is not specified in the sources
        if (
            not omit_self
            and self.SELF not in processed_values
            and self.NONE not in processed_values
        ):
            processed_values.insert(0, self.SELF)

        # Add the directive to the directives dictionary, replacing it if replace is True, the directive does not already exist or if the existing directive is just "'none'"
        if (
            directive not in self.directives
            or replace
            or self.directives.get(directive, []) == [self.NONE]
        ):
            self.directives[directive] = processed_values
        else:
            # If the directive already exists, we extend it with the new values, ensuring we don't add duplicates
            existing_values = self.directives[directive]
            for value in processed_values:
                if value not in existing_values:
                    existing_values.append(value)

        # Return self to allow for method chaining
        return self

    def disallow(self, directive: str) -> "CspGenerator":
        """
        Disallow a directive by setting it to 'none'.
        """

        self.directives[directive] = [self.NONE]
        return self

    def base_uri(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a base-uri directive.
        """

        return self.add_directive(
            "base-uri", *sources, omit_self=omit_self, replace=replace
        )

    def child_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a child-src directive.
        """

        return self.add_directive(
            "child-src", *sources, omit_self=omit_self, replace=replace
        )

    def connect_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a connect-src directive.
        """

        return self.add_directive(
            "connect-src", *sources, omit_self=omit_self, replace=replace
        )

    def default_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a default-src directive.
        """

        return self.add_directive(
            "default-src", *sources, omit_self=omit_self, replace=replace
        )

    def font_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a font-src directive.
        """

        return self.add_directive(
            "font-src", *sources, omit_self=omit_self, replace=replace
        )

    def form_action(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a form-action directive.
        """

        return self.add_directive(
            "form-action", *sources, omit_self=omit_self, replace=replace
        )

    def frame_ancestors(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a frame-ancestors directive.
        """

        return self.add_directive(
            "frame-ancestors", *sources, omit_self=omit_self, replace=replace
        )

    def frame_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a frame-src directive.
        """

        return self.add_directive(
            "frame-src", *sources, omit_self=omit_self, replace=replace
        )

    def img_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add an img-src directive.
        """

        return self.add_directive(
            "img-src", *sources, omit_self=omit_self, replace=replace
        )

    def manifest_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a manifest-src directive.
        """

        return self.add_directive(
            "manifest-src", *sources, omit_self=omit_self, replace=replace
        )

    def media_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a media-src directive.
        """

        return self.add_directive(
            "media-src", *sources, omit_self=omit_self, replace=replace
        )

    def object_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add an object-src directive.
        """

        return self.add_directive(
            "object-src", *sources, omit_self=omit_self, replace=replace
        )

    def prefetch_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a prefetch-src directive.
        """

        return self.add_directive(
            "prefetch-src", *sources, omit_self=omit_self, replace=replace
        )

    def report_uri(self, uri: str) -> "CspGenerator":
        """
        Add a report-uri directive.

        The report-uri directive is deprecated in favor of report-to however, it is still supported by a few browsers.

        For new implementations, it is recommended to use report-to instead of report-uri.
        """

        if uri:
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

        if endpoint_name:
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
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a script-src directive.
        """

        return self.add_directive(
            "script-src", *sources, omit_self=omit_self, replace=replace
        )

    def script_src_attr(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a script-src-attr directive.
        """

        return self.add_directive(
            "script-src-attr", *sources, omit_self=omit_self, replace=replace
        )

    def script_src_elem(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a script-src-elem directive.
        """

        return self.add_directive(
            "script-src-elem", *sources, omit_self=omit_self, replace=replace
        )

    def style_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a style-src directive.
        """

        return self.add_directive(
            "style-src", *sources, omit_self=omit_self, replace=replace
        )

    def style_src_attr(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a style-src-attr directive.
        """

        return self.add_directive(
            "style-src-attr", *sources, omit_self=omit_self, replace=replace
        )

    def style_src_elem(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a style-src-elem directive.
        """

        return self.add_directive(
            "style-src-elem", *sources, omit_self=omit_self, replace=replace
        )

    def worker_src(
        self, *sources: str | list[str], omit_self=False, replace=False
    ) -> "CspGenerator":
        """
        Add a worker-src directive.
        """

        return self.add_directive(
            "worker-src", *sources, omit_self=omit_self, replace=replace
        )

    def custom_src(
        self,
        directive_name: str,
        *sources: str | list[str],
        omit_self=False,
        replace=False,
    ) -> "CspGenerator":
        """
        Add a custom directive.
        """

        return self.add_directive(
            directive_name, *sources, omit_self=omit_self, replace=replace
        )

    def to_string(self, simplify=False) -> str:
        """
        Get the complete CSP as a string.

        :param simplify: If True, omit directives whose source list is identical
            to the ``default-src`` directive, keeping only ``default-src`` and
            directives that differ from it. This produces a more compact CSP
            representation without changing its effective policy.
        :return: The CSP as a semicolon-separated string suitable for use in
            the Content-Security-Policy HTTP header.
        """

        directives = self.directives.copy()
        if simplify:
            default_src = self.directives.get("default-src")
            directives = {
                k: v
                for k, v in directives.items()
                if k == "default-src" or v != default_src
            }
        parts = []
        for directive, sources in directives.items():
            directive_str = directive
            if sources:
                directive_str += " " + " ".join(sources)
            parts.append(directive_str)
        return "; ".join(parts) + ";"

    def __str__(self) -> str:
        return self.to_string()

    def to_dict(self) -> dict[str, list[str]]:
        return dict(self.directives)


def common_security_headers(
    x_permitted_cross_domain_policies: str | None = None,
    cross_origin_embedder_policy: str | None = None,
    cross_origin_opener_policy: str | None = None,
    cross_origin_resource_policy: str | None = None,
    x_content_type_options: str | None = "nosniff",
) -> dict[str, str]:
    """
    Get a dictionary of common security headers.

    :param x_permitted_cross_domain_policies: The value for the X-Permitted-Cross-Domain-Policies header. Valid values are "none", "master-only", "by-content-type", "by-ftp-filename", "all", and "none-this-response". If not provided, it defaults to "none".
    :param cross_origin_embedder_policy: The value for the Cross-Origin-Embedder-Policy header. Valid values are "unsafe-none", "require-corp", and "credentialless". If not provided, it defaults to "unsafe-none".
    :param cross_origin_opener_policy: The value for the Cross-Origin-Opener-Policy header. Valid values are "same-origin", "same-origin-allow-popups", "unsafe-none", and "noopener-allow-popups". If not provided, it defaults to "same-origin".
    :param cross_origin_resource_policy: The value for the Cross-Origin-Resource-Policy header. Valid values are "same-origin", "same-site", and "cross-origin". If not provided, it defaults to "same-origin".
    :param x_content_type_options: The value for the X-Content-Type-Options header. Valid values are None and "nosniff". If not provided, it defaults to "nosniff".
    """

    headers = [
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
        {
            "header": "X-Content-Type-Options",
            "values": [None, "nosniff"],
            "default": "nosniff",
            "value": x_content_type_options,
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
    ]

    headers_dict = {
        header["header"]: (
            header["value"]
            if header["value"] in header["values"]
            else (header["default"] or "")
        )
        for header in headers
    }

    return {
        header: value for header, value in headers_dict.items() if value is not None
    }
