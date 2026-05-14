import unittest

from tna_utilities.security import CspGenerator, common_security_headers


class TestSecurityCSP(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_domain = "https://example.com"
        self.test_domain_2 = "https://another.net"

    def test_init(self):
        generator = CspGenerator()
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_str_output(self):
        generator = CspGenerator()
        self.assertEqual(
            str(generator),
            "default-src 'self'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_dict_output(self):
        generator = CspGenerator()
        self.assertEqual(
            generator.to_dict(),
            {
                "default-src": ["'self'"],
                "object-src": ["'none'"],
                "frame-ancestors": ["'none'"],
                "child-src": ["'none'"],
            },
        )

    def test_init_none(self):
        generator = CspGenerator(CspGenerator.NONE)
        self.assertEqual(
            generator.to_string(),
            "default-src 'none'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_list(self):
        generator = CspGenerator([CspGenerator.NONE, self.test_domain])
        self.assertEqual(
            generator.to_string(),
            f"default-src 'none' {self.test_domain}; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_empty_string(self):
        generator = CspGenerator("")
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_list_of_empty_strings(self):
        generator = CspGenerator([""])
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; object-src 'none'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_allow_objects(self):
        generator = CspGenerator([""], allow_objects=True)
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; frame-ancestors 'none'; child-src 'none';",
        )

    def test_init_allow_iframe_embedding(self):
        generator = CspGenerator([""], allow_iframe_embedding=True)
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; object-src 'none'; child-src 'none';",
        )

    def test_init_allow_children(self):
        generator = CspGenerator([""], allow_children=True)
        self.assertEqual(
            generator.to_string(),
            "default-src 'self'; object-src 'none'; frame-ancestors 'none';",
        )

    def test_init_allow_all_optional(self):
        generator = CspGenerator(
            [""], allow_objects=True, allow_iframe_embedding=True, allow_children=True
        )
        self.assertEqual(generator.to_string(), "default-src 'self';")

    def test_init_overwrite_default_disallows(self):
        generator = CspGenerator(CspGenerator.NONE)
        generator.object_src(self.test_domain, omit_self=True)
        self.assertEqual(
            generator.to_string(),
            f"default-src 'none'; object-src {self.test_domain}; frame-ancestors 'none'; child-src 'none';",
        )

    def test_add_directive(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'self' {self.test_domain};", generator.to_string())

    def test_add_directive_none(self):
        generator = CspGenerator()
        generator.script_src(CspGenerator.NONE)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("script-src 'none';", generator.to_string())

    def test_add_directive_multiple(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain, self.test_domain_2)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_directive_duplicates(self):
        generator = CspGenerator()
        generator.script_src(
            self.test_domain, self.test_domain_2, self.test_domain, self.test_domain
        )
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_directive_list(self):
        generator = CspGenerator()
        generator.script_src([self.test_domain, self.test_domain_2])
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_directive_mixed_types(self):
        generator = CspGenerator()
        test_domain_3 = "https://third.org"
        test_domain_4 = "https://fourth.io"
        test_domain_5 = "https://fifth.co"
        test_domain_6 = "https://sixth.edu"
        generator.script_src(
            self.test_domain,
            f"{self.test_domain_2} {test_domain_3}",
            [test_domain_4, f"{test_domain_5} {test_domain_6}"],
        )
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2} {test_domain_3} {test_domain_4} {test_domain_5} {test_domain_6};",
            generator.to_string(),
        )

    def test_add_directive_space_separated_list(self):
        generator = CspGenerator()
        generator.script_src(f"{self.test_domain} {self.test_domain_2}")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_directive_empty(self):
        generator = CspGenerator()
        generator.script_src()
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertNotIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_no_simplify_duplicated_directives(self):
        generator = CspGenerator()
        generator.script_src(CspGenerator.SELF)
        csp = generator.to_string()
        self.assertIn("default-src 'self';", csp)
        self.assertIn("script-src 'self';", csp)

    def test_simplify_duplicated_directives(self):
        generator = CspGenerator()
        generator.script_src(CspGenerator.SELF)
        csp = generator.to_string(simplify=True)
        self.assertIn("default-src 'self';", csp)
        self.assertNotIn("script-src", csp)

    def test_add_directive_existing_self(self):
        generator = CspGenerator()
        generator.script_src([CspGenerator.SELF, self.test_domain])
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'self' {self.test_domain};", generator.to_string())

    def test_add_directive_existing_none(self):
        generator = CspGenerator()
        generator.script_src([CspGenerator.NONE, self.test_domain])
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'none' {self.test_domain};", generator.to_string())

    def test_add_directive_omit_self(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain, omit_self=True)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src {self.test_domain};", generator.to_string())

    def test_add_directive_list_omit_self(self):
        generator = CspGenerator()
        generator.script_src([self.test_domain, self.test_domain_2], omit_self=True)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_directive_omit_self_existing_none(self):
        generator = CspGenerator()
        generator.script_src([CspGenerator.NONE, self.test_domain], omit_self=True)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'none' {self.test_domain};", generator.to_string())

    def test_add_disallow_directive(self):
        generator = CspGenerator()
        generator.disallow("script-src")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("script-src 'none';", generator.to_string())

    def test_add_directive_chained(self):
        generator = CspGenerator()
        self.assertEqual(generator.script_src(self.test_domain), generator)

    def test_add_multiple_directives(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain)
        generator.style_src(self.test_domain_2)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'self' {self.test_domain};", generator.to_string())
        self.assertIn(f"style-src 'self' {self.test_domain_2};", generator.to_string())

    def test_add_multiple_same_directives(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain)
        generator.script_src(self.test_domain_2)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"script-src 'self' {self.test_domain} {self.test_domain_2};",
            generator.to_string(),
        )

    def test_add_multiple_same_directives_replace(self):
        generator = CspGenerator()
        generator.script_src(self.test_domain)
        generator.script_src(self.test_domain_2, replace=True)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"script-src 'self' {self.test_domain_2};", generator.to_string())

    def test_add_custom_directive(self):
        generator = CspGenerator()
        generator.custom_src("custom-directive", self.test_domain)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(
            f"custom-directive 'self' {self.test_domain};", generator.to_string()
        )

    def test_add_directive_sources(self):
        directives = [
            ("base-uri", "base_uri"),
            ("child-src", "child_src"),
            ("connect-src", "connect_src"),
            # ("fenced-frame-src", "fenced_frame_src"),  # Experimental
            ("font-src", "font_src"),
            ("form-action", "form_action"),
            ("frame-ancestors", "frame_ancestors"),
            ("frame-src", "frame_src"),
            ("img-src", "img_src"),
            ("manifest-src", "manifest_src"),
            ("media-src", "media_src"),
            ("object-src", "object_src"),
            ("prefetch-src", "prefetch_src"),
            ("script-src", "script_src"),
            ("script-src-attr", "script_src_attr"),
            ("script-src-elem", "script_src_elem"),
            ("style-src", "style_src"),
            ("style-src-attr", "style_src_attr"),
            ("style-src-elem", "style_src_elem"),
            # ("trusted-types", "trusted_types"),  # Not technically part of the CSP spec
            ("worker-src", "worker_src"),
        ]
        for directive, method in directives:
            generator = CspGenerator()
            getattr(generator, method)(self.test_domain)
            self.assertIn("default-src 'self';", generator.to_string())
            self.assertIn(
                f"{directive} 'self' {self.test_domain};", generator.to_string()
            )

    def test_add_report_uri(self):
        generator = CspGenerator()
        report_uri = "https://report.example.com"
        generator.report_uri(report_uri)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"report-uri {report_uri};", generator.to_string())

    def test_add_empty_report_uri(self):
        generator = CspGenerator()
        generator.report_uri("")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertNotIn("report-uri", generator.to_string())

    def test_add_report_to(self):
        generator = CspGenerator()
        report_endpoint_name = "csp_report_endpoint"
        generator.report_to(report_endpoint_name)
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn(f"report-to {report_endpoint_name};", generator.to_string())

    def test_add_empty_report_to(self):
        generator = CspGenerator()
        generator.report_to("")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertNotIn("report-to", generator.to_string())

    def test_add_require_trusted_types_for(self):
        generator = CspGenerator()
        generator.require_trusted_types_for()
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("require-trusted-types-for 'script';", generator.to_string())

    def test_add_sandbox(self):
        generator = CspGenerator()
        generator.sandbox()
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("sandbox;", generator.to_string())

    def test_add_sandbox_value(self):
        generator = CspGenerator()
        generator.sandbox("allow-scripts")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("sandbox allow-scripts;", generator.to_string())

    def test_add_sandbox_invalid_value(self):
        generator = CspGenerator()
        generator.sandbox("pizza")
        self.assertIn("default-src 'self';", generator.to_string())
        self.assertIn("sandbox;", generator.to_string())


class TestCommonSecurityHeaders(unittest.TestCase):
    def test_security_headers_default(self):
        headers = common_security_headers()
        self.assertDictEqual(
            headers,
            {
                "Cross-Origin-Embedder-Policy": "unsafe-none",
                "Cross-Origin-Opener-Policy": "same-origin",
                "Cross-Origin-Resource-Policy": "same-origin",
                "X-Content-Type-Options": "nosniff",
                "X-Permitted-Cross-Domain-Policies": "none",
            },
        )

    def test_security_headers_invalid(self):
        headers = common_security_headers(
            cross_origin_embedder_policy="0",
            cross_origin_opener_policy="None",
            cross_origin_resource_policy="",
            x_content_type_options="[]",
            x_permitted_cross_domain_policies="True",
        )
        self.assertDictEqual(
            headers,
            {
                "Cross-Origin-Embedder-Policy": "unsafe-none",
                "Cross-Origin-Opener-Policy": "same-origin",
                "Cross-Origin-Resource-Policy": "same-origin",
                "X-Content-Type-Options": "nosniff",
                "X-Permitted-Cross-Domain-Policies": "none",
            },
        )

    def test_security_headers_custom(self):
        headers = common_security_headers(
            cross_origin_embedder_policy="require-corp",
            cross_origin_opener_policy="noopener-allow-popups",
            cross_origin_resource_policy="cross-origin",
            x_content_type_options=None,
            x_permitted_cross_domain_policies="all",
        )
        self.assertDictEqual(
            headers,
            {
                "Cross-Origin-Embedder-Policy": "require-corp",
                "Cross-Origin-Opener-Policy": "noopener-allow-popups",
                "Cross-Origin-Resource-Policy": "cross-origin",
                "X-Permitted-Cross-Domain-Policies": "all",
            },
        )
