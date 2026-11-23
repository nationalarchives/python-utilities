class ContentNegotiationCases:
    def test_negotiation(self):
        calls = []

        def page(*, preferred_content_type):
            calls.append(preferred_content_type)
            return self.response(
                preferred_content_type or "none", headers={"Vary": "Cookie"}
            )

        view = self.negotiate(["text/html", "text/markdown"])(self.view(page))
        cases = [
            (None, 200, "none"),
            ("", 200, "none"),
            ("*/*", 200, "text/html"),
            ("text/*", 200, "text/html"),
            ("text/*;level=1", 200, "text/html"),
            ("*/*;level=1", 200, "text/html"),
            ("text/markdown", 200, "text/markdown"),
            ("TEXT/MARKDOWN", 200, "text/markdown"),
            ("text/html;q=0.2, text/markdown;q=0.8", 200, "text/markdown"),
            ("text/markdown;q=0.3, text/html;q=0.8", 200, "text/html"),
            ("text/markdown, text/html", 200, "text/html"),
            ("text/markdown;q=0.5, text/html;q=0.5", 200, "text/html"),
            ("*/*;q=1, text/html;q=0.1", 200, "text/markdown"),
            ("text/html;q=0.1, */*;q=1", 200, "text/markdown"),
            ("*/*;q=1, text/html;q=0", 200, "text/markdown"),
            ("text/html;q=0, */*", 200, "text/markdown"),
            ("text/*;q=0, text/html;q=0.5", 200, "text/html"),
            ("text/html;q=0, text/markdown;q=0", 406, ""),
            ("application/json", 406, ""),
            (" , , ", 406, ""),
            ("image/*", 406, ""),
            ("*/html", 406, ""),
            ("*/*;q=0", 406, ""),
        ]
        for accept, status, body in cases:
            with self.subTest(accept=accept):
                before = len(calls)
                response = self.invoke(view, accept)
                self.assertEqual(response.status_code, status)
                self.assertEqual(self.body(response), body)
                self.assertIn("accept", self.vary(response))
                if status == 406:
                    self.assertEqual(len(calls), before)
                    self.assertEqual(response.headers["Cache-Control"], "no-store")
                else:
                    self.assertIn("cookie", self.vary(response))

    def test_invalid_quality_entries_are_ignored(self):
        def page(*, preferred_content_type):
            return self.response(preferred_content_type)

        view = self.negotiate(["text/html", "text/markdown"])(self.view(page))
        for quality in ("invalid", "2", "-1", "NaN", "inf"):
            with self.subTest(quality=quality):
                response = self.invoke(
                    view, f"text/html;q={quality}, text/markdown;q=0.5"
                )
                self.assertEqual(self.body(response), "text/markdown")

    def test_supported_order_and_argument_forwarding(self):
        def page(path, *, preferred_content_type):
            return self.response(f"{path}: {preferred_content_type}")

        view = self.negotiate(["text/markdown", "text/html"])(self.view(page))
        for accept in ("*/*", "text/*", "text/html, text/markdown"):
            for args, kwargs in ((("/example/",), {}), ((), {"path": "/example/"})):
                with self.subTest(accept=accept, args=args, kwargs=kwargs):
                    response = self.invoke(view, accept, *args, **kwargs)
                    self.assertEqual(self.body(response), "/example/: text/markdown")

    def test_empty_options_and_response_preservation(self):
        def no_options(*, preferred_content_type):
            self.fail("View must not be called")

        view = self.negotiate([])(self.view(no_options))
        response = self.invoke(view, "text/html")
        self.assertEqual(response.status_code, 406)
        self.assertIn("accept", self.vary(response))

        for vary in ("Accept-Encoding", "Accept-Encoding, Accept"):
            original = self.response(
                "page content",
                status=201,
                headers={"Vary": vary, "X-Example": "preserved"},
            )

            def page(*, preferred_content_type, response=original):
                """Render a page."""
                return response

            original_view = self.view(page)
            view = self.negotiate(["text/html"])(original_view)
            response = self.invoke(view, None)
            self.assertIs(response, original)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.body(response), "page content")
            self.assertEqual(response.headers["X-Example"], "preserved")
            self.assertEqual(self.vary(response).count("accept"), 1)
            self.assertIn("accept-encoding", self.vary(response))
            self.assertEqual(view.__name__, "page")
            self.assertEqual(view.__doc__, "Render a page.")
            self.assertIs(view.__wrapped__, original_view)

    def test_view_returned_406_is_not_cached(self):
        def page(*, preferred_content_type):
            return self.response(
                "",
                status=406,
                headers={"Cache-Control": "public, max-age=60", "Vary": "Cookie"},
            )

        view = self.negotiate(["text/html"])(self.view(page))
        response = self.invoke(view, "text/html")
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertIn("cookie", self.vary(response))
        self.assertIn("accept", self.vary(response))

    def test_wildcard_vary_is_preserved(self):
        def page(*, preferred_content_type):
            return self.response("page", headers={"Vary": "*"})

        view = self.negotiate(["text/html"])(self.view(page))
        self.assertEqual(self.invoke(view, "text/html").headers["Vary"], "*")

    @staticmethod
    def vary(response):
        return [value.strip().lower() for value in response.headers["Vary"].split(",")]
