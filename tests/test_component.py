import unittest

from tna_utilities.component import (
    PAGINATION_GAP,
    paginate,
    tna_frontend_pagination,
    tna_frontend_pagination_items,
)


class TestComponent(unittest.TestCase):
    def test_pagination_first(self):
        self.assertEqual(
            paginate(42, 1),
            [
                1,
                2,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_second(self):
        self.assertEqual(
            paginate(42, 2),
            [
                1,
                2,
                3,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_third(self):
        self.assertEqual(
            paginate(42, 3),
            [
                1,
                2,
                3,
                4,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_fourth(self):
        self.assertEqual(
            paginate(42, 4),
            [
                1,
                2,
                3,
                4,
                5,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_fifth(self):
        self.assertEqual(
            paginate(42, 5),
            [
                1,
                PAGINATION_GAP,
                4,
                5,
                6,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_sixth(self):
        self.assertEqual(
            paginate(42, 6),
            [
                1,
                PAGINATION_GAP,
                5,
                6,
                7,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_fifth_from_last(self):
        self.assertEqual(
            paginate(42, 37),
            [
                1,
                PAGINATION_GAP,
                36,
                37,
                38,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_four_from_last(self):
        self.assertEqual(
            paginate(42, 38),
            [
                1,
                PAGINATION_GAP,
                37,
                38,
                39,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_three_from_last(self):
        self.assertEqual(
            paginate(42, 39),
            [
                1,
                PAGINATION_GAP,
                38,
                39,
                40,
                41,
                42,
            ],
        )

    def test_pagination_two_from_last(self):
        self.assertEqual(
            paginate(42, 40),
            [
                1,
                PAGINATION_GAP,
                39,
                40,
                41,
                42,
            ],
        )

    def test_pagination_one_from_last(self):
        self.assertEqual(
            paginate(42, 41),
            [
                1,
                PAGINATION_GAP,
                40,
                41,
                42,
            ],
        )

    def test_pagination_last(self):
        self.assertEqual(
            paginate(42, 42),
            [
                1,
                PAGINATION_GAP,
                41,
                42,
            ],
        )

    def test_pagination_first_larger_around(self):
        self.assertEqual(
            paginate(42, 1, around=3),
            [
                1,
                2,
                3,
                4,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_second_larger_around(self):
        self.assertEqual(
            paginate(42, 2, around=3),
            [
                1,
                2,
                3,
                4,
                5,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_third_larger_around(self):
        self.assertEqual(
            paginate(42, 3, around=3),
            [
                1,
                2,
                3,
                4,
                5,
                6,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_fourth_larger_around(self):
        self.assertEqual(
            paginate(42, 4, around=3),
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_fifth_larger_around(self):
        self.assertEqual(
            paginate(42, 5, around=3),
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_sixth_larger_around(self):
        self.assertEqual(
            paginate(42, 6, around=3),
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_seventh_larger_around(self):
        self.assertEqual(
            paginate(42, 7, around=3),
            [
                1,
                PAGINATION_GAP,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_first_no_around(self):
        self.assertEqual(
            paginate(42, 1, around=0),
            [
                1,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_second_no_around(self):
        self.assertEqual(
            paginate(42, 2, around=0),
            [
                1,
                2,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_third_no_around(self):
        self.assertEqual(
            paginate(42, 3, around=0),
            [
                1,
                PAGINATION_GAP,
                3,
                PAGINATION_GAP,
                42,
            ],
        )

    def test_pagination_no_pages(self):
        with self.assertRaises(ValueError):
            paginate(0, 1)

    def test_pagination_invalid_pages(self):
        with self.assertRaises(TypeError):
            paginate(None, 1)

    def test_pagination_negative_current_page(self):
        with self.assertRaises(ValueError):
            paginate(42, -1)

    def test_pagination_negative_around(self):
        with self.assertRaises(ValueError):
            paginate(42, 1, around=-1)

    def test_tna_frontend_pagination_items(self):
        self.assertEqual(
            tna_frontend_pagination_items(42, 6, "/test?page="),
            [
                {"number": 1, "current": False, "href": "/test?page=1"},
                {"ellipsis": True},
                {"number": 5, "current": False, "href": "/test?page=5"},
                {"number": 6, "current": True, "href": "/test?page=6"},
                {"number": 7, "current": False, "href": "/test?page=7"},
                {"ellipsis": True},
                {"number": 42, "current": False, "href": "/test?page=42"},
            ],
        )

    def test_tna_frontend_pagination_items_custom_transformer(self):
        def custom_transformer(item, current_page, base_url):
            return {
                "page": item,
                "is_current": item == current_page,
                "url": f"{base_url}{item}",
            }

        self.assertEqual(
            tna_frontend_pagination_items(
                42, 6, "/test?page=", transformer=custom_transformer
            ),
            [
                {"page": 1, "is_current": False, "url": "/test?page=1"},
                {"ellipsis": True},
                {"page": 5, "is_current": False, "url": "/test?page=5"},
                {"page": 6, "is_current": True, "url": "/test?page=6"},
                {"page": 7, "is_current": False, "url": "/test?page=7"},
                {"ellipsis": True},
                {"page": 42, "is_current": False, "url": "/test?page=42"},
            ],
        )

    def test_tna_frontend_pagination_items_custom_transformer_lambda(self):
        self.assertEqual(
            tna_frontend_pagination_items(
                42,
                6,
                "/test?page=",
                transformer=lambda item, current_page, base_url: {
                    "page": item,
                    "is_current": item == current_page,
                    "url": f"{base_url}{item}",
                },
            ),
            [
                {"page": 1, "is_current": False, "url": "/test?page=1"},
                {"ellipsis": True},
                {"page": 5, "is_current": False, "url": "/test?page=5"},
                {"page": 6, "is_current": True, "url": "/test?page=6"},
                {"page": 7, "is_current": False, "url": "/test?page=7"},
                {"ellipsis": True},
                {"page": 42, "is_current": False, "url": "/test?page=42"},
            ],
        )

    def test_tna_frontend_pagination_items_custom_ellipsis(self):
        self.assertEqual(
            tna_frontend_pagination_items(
                42, 6, "/test?page=", ellipsis={"number": None}
            ),
            [
                {"number": 1, "current": False, "href": "/test?page=1"},
                {"number": None},
                {"number": 5, "current": False, "href": "/test?page=5"},
                {"number": 6, "current": True, "href": "/test?page=6"},
                {"number": 7, "current": False, "href": "/test?page=7"},
                {"number": None},
                {"number": 42, "current": False, "href": "/test?page=42"},
            ],
        )

    def test_tna_frontend_pagination(self):
        pagination = tna_frontend_pagination(42, 6, "/test?page=")

        self.assertIn("items", pagination)
        self.assertEqual(
            pagination["items"],
            [
                {"number": 1, "current": False, "href": "/test?page=1"},
                {"ellipsis": True},
                {"number": 5, "current": False, "href": "/test?page=5"},
                {"number": 6, "current": True, "href": "/test?page=6"},
                {"number": 7, "current": False, "href": "/test?page=7"},
                {"ellipsis": True},
                {"number": 42, "current": False, "href": "/test?page=42"},
            ],
        )

        self.assertIn("previous", pagination)
        self.assertEqual(
            pagination["previous"],
            {
                "href": "/test?page=5",
            },
        )

        self.assertIn("next", pagination)
        self.assertEqual(
            pagination["next"],
            {
                "href": "/test?page=7",
            },
        )

    def test_tna_frontend_pagination_first(self):
        pagination = tna_frontend_pagination(42, 1, "/test?page=")

        self.assertIn("items", pagination)
        self.assertEqual(
            pagination["items"],
            [
                {"number": 1, "current": True, "href": "/test?page=1"},
                {"number": 2, "current": False, "href": "/test?page=2"},
                {"ellipsis": True},
                {"number": 42, "current": False, "href": "/test?page=42"},
            ],
        )

        self.assertNotIn("previous", pagination)

        self.assertIn("next", pagination)
        self.assertEqual(
            pagination["next"],
            {
                "href": "/test?page=2",
            },
        )

    def test_tna_frontend_pagination_last(self):
        pagination = tna_frontend_pagination(42, 42, "/test?page=")

        self.assertIn("items", pagination)
        self.assertEqual(
            pagination["items"],
            [
                {"number": 1, "current": False, "href": "/test?page=1"},
                {"ellipsis": True},
                {"number": 41, "current": False, "href": "/test?page=41"},
                {"number": 42, "current": True, "href": "/test?page=42"},
            ],
        )

        self.assertIn("previous", pagination)
        self.assertEqual(
            pagination["previous"],
            {
                "href": "/test?page=41",
            },
        )

        self.assertNotIn("next", pagination)

    def test_tna_frontend_pagination_custom_properties(self):
        pagination = tna_frontend_pagination(
            42,
            6,
            "/test?page=",
            custom_properties={
                "items": "foobar",
                "classes": "test-class",
                "attributes": {"data-test": "value"},
            },
        )

        self.assertIn("items", pagination)
        self.assertNotEqual(pagination["items"], "foobar")

        self.assertIn("classes", pagination)
        self.assertEqual(pagination["classes"], "test-class")

        self.assertIn("attributes", pagination)
        self.assertEqual(pagination["attributes"], {"data-test": "value"})

    def test_tna_frontend_pagination_custom_next_previous_properties(self):
        pagination = tna_frontend_pagination(
            42,
            6,
            "/test?page=",
            previous_page_properties={"text": "Go back one", "href": "NONONO"},
            next_page_properties={
                "title": "Another page please",
                "description": "foobar",
            },
        )

        self.assertIn("previous", pagination)
        self.assertEqual(
            pagination["previous"], {"text": "Go back one", "href": "/test?page=5"}
        )

        self.assertIn("next", pagination)
        self.assertEqual(
            pagination["next"],
            {
                "href": "/test?page=7",
                "title": "Another page please",
                "description": "foobar",
            },
        )
