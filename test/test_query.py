import unittest

from tna_utilities.query import QueryStringManipulator


class TestQueryStringObject:
    def lists(self):
        return iter(
            [
                ("a", ["1"]),
                ("b", ["2", "3"]),
            ]
        )


class TestQuery(unittest.TestCase):
    def test_init(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        self.assertEqual(manipulator.get_query_string(), "?a=1&b=2&b=3")

    def test_filter_values(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        self.assertEqual(manipulator.filter_values("a"), ["1"])
        self.assertEqual(manipulator.filter_values("b"), ["2", "3"])
        with self.assertRaises(AttributeError):
            manipulator.filter_values("c")

    def test_add_filter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)

        manipulator.add_filter("c", [])
        self.assertTrue(manipulator.filter_exists("c"))
        self.assertEqual(manipulator.filter_values("c"), [])

        manipulator.add_filter("d", None)
        self.assertTrue(manipulator.filter_exists("d"))
        self.assertEqual(manipulator.filter_values("d"), [])

        manipulator.add_filter("e", "")
        self.assertTrue(manipulator.filter_exists("e"))
        self.assertEqual(manipulator.filter_values("e"), [""])

        manipulator.add_filter("f", "4")
        self.assertTrue(manipulator.filter_exists("f"))
        self.assertEqual(manipulator.filter_values("f"), ["4"])

        manipulator.add_filter("g", ["5", "6"])
        self.assertTrue(manipulator.filter_exists("g"))
        self.assertEqual(manipulator.filter_values("g"), ["5", "6"])

        manipulator.add_filter("h", [False])
        self.assertTrue(manipulator.filter_exists("h"))
        self.assertEqual(manipulator.filter_values("h"), ["False"])

        self.assertEqual(
            manipulator.get_query_string(), "?a=1&b=2&b=3&e=&f=4&g=5&g=6&h=False"
        )

    def test_update_filter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        manipulator.update_filter("a", "10")
        self.assertEqual(manipulator.filter_values("a"), ["10"])
        manipulator.update_filter("b", ["20", "30"])
        self.assertEqual(manipulator.filter_values("b"), ["20", "30"])
        manipulator.update_filter("c", ["40"])
        self.assertEqual(manipulator.filter_values("c"), ["40"])
        self.assertEqual(manipulator.get_query_string(), "?a=10&b=20&b=30&c=40")

    def test_remove_filter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        manipulator.remove_filter("a")
        self.assertFalse(manipulator.filter_exists("a"))
        manipulator.remove_filter("b")
        self.assertFalse(manipulator.filter_exists("b"))
        with self.assertRaises(AttributeError):
            manipulator.remove_filter("c")
        self.assertEqual(manipulator.get_query_string(), "?")

    def test_is_value_in_filter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        self.assertTrue(manipulator.is_value_in_filter("a", "1"))
        self.assertTrue(manipulator.is_value_in_filter("b", "2"))
        self.assertTrue(manipulator.is_value_in_filter("b", "3"))
        self.assertFalse(manipulator.is_value_in_filter("b", "4"))
        with self.assertRaises(AttributeError):
            self.assertFalse(manipulator.is_value_in_filter("c", "5"))

    def test_toggle_filter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        manipulator.toggle_filter_value("a", "1")
        self.assertFalse(manipulator.is_value_in_filter("a", "1"))
        manipulator.toggle_filter_value("a", "10")
        self.assertTrue(manipulator.is_value_in_filter("a", "10"))
        manipulator.toggle_filter_value("b", "2")
        self.assertFalse(manipulator.is_value_in_filter("b", "2"))
        self.assertEqual(manipulator.get_query_string(), "?a=10&b=3")
        manipulator.toggle_filter_value("a", "1")
        self.assertTrue(manipulator.is_value_in_filter("a", "1"))
        self.assertEqual(manipulator.get_query_string(), "?a=10&a=1&b=3")

    def test_add_remove_filter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        manipulator.add_filter_value("a", "10")
        self.assertTrue(manipulator.is_value_in_filter("a", "10"))
        self.assertEqual(manipulator.filter_values("a"), ["1", "10"])

    def test_remove_filter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringManipulator(test_query)
        manipulator.remove_filter_value("b", "2")
        self.assertFalse(manipulator.is_value_in_filter("b", "2"))
        self.assertEqual(manipulator.filter_values("b"), ["3"])
