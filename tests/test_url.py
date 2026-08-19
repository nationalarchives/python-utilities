import unittest

from tna_utilities.url import QueryStringTransformer


class TestQueryStringTransformer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_query = [("a", ["1"]), ("b", ["2", "3"])]

    def test_init(self):
        manipulator = QueryStringTransformer()
        new_qs = manipulator.new()

        self.assertEqual(new_qs.get_query_string(), "")
        self.assertEqual(new_qs.add_parameter("foo", "bar"), new_qs)
        self.assertEqual(new_qs.get_query_string(), "?foo=bar")

    def test_list_init(self):
        manipulator = QueryStringTransformer(self.test_query)

        self.assertEqual(manipulator.get_query_string(), "?a=1&b=2&b=3")

    def test_object_init(self):
        class TestQueryStringObject:
            def lists(self):
                return iter(
                    [
                        ("a", ["1"]),
                        ("b", ["2", "3"]),
                    ]
                )

        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.get_query_string(), "?a=1&b=2&b=3")
        self.assertEqual(new_qs.add_parameter("foo", "bar"), new_qs)
        self.assertEqual(new_qs.get_query_string(), "?a=1&b=2&b=3&foo=bar")

    def test_unhappy_init(self):
        with self.assertRaises(AttributeError):
            QueryStringTransformer(0)

    def test_parameter_values(self):
        manipulator = QueryStringTransformer(self.test_query)

        self.assertEqual(manipulator.parameter_values("a"), ["1"])
        self.assertEqual(manipulator.parameter_values("b"), ["2", "3"])
        with self.assertRaises(KeyError):
            manipulator.parameter_values("c")

    def test_add_parameter(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.add_parameter("c", []), new_qs)
        self.assertTrue(new_qs.parameter_exists("c"))
        self.assertEqual(new_qs.parameter_values("c"), [])

        self.assertEqual(new_qs.add_parameter("d", None), new_qs)
        self.assertTrue(new_qs.parameter_exists("d"))
        self.assertEqual(new_qs.parameter_values("d"), [])

        self.assertEqual(new_qs.add_parameter("e", ""), new_qs)
        self.assertTrue(new_qs.parameter_exists("e"))
        self.assertEqual(new_qs.parameter_values("e"), [""])

        self.assertEqual(new_qs.add_parameter("f", "4"), new_qs)
        self.assertTrue(new_qs.parameter_exists("f"))
        self.assertEqual(new_qs.parameter_values("f"), ["4"])

        self.assertEqual(new_qs.add_parameter("g", ["5", "6"]), new_qs)
        self.assertTrue(new_qs.parameter_exists("g"))
        self.assertEqual(new_qs.parameter_values("g"), ["5", "6"])

        self.assertEqual(new_qs.add_parameter("h", [False]), new_qs)
        self.assertTrue(new_qs.parameter_exists("h"))
        self.assertEqual(new_qs.parameter_values("h"), ["False"])

        with self.assertRaises(ValueError):
            new_qs.add_parameter("h", [True])

        self.assertEqual(
            new_qs.get_query_string(), "?a=1&b=2&b=3&e=&f=4&g=5&g=6&h=False"
        )

    def test_update_parameter(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.update_parameter("a", "10"), new_qs)
        self.assertEqual(new_qs.parameter_values("a"), ["10"])
        self.assertEqual(new_qs.update_parameter("b", ["20", "30"]), new_qs)
        self.assertEqual(new_qs.parameter_values("b"), ["20", "30"])
        self.assertEqual(new_qs.update_parameter("b", "100"), new_qs)
        self.assertEqual(new_qs.parameter_values("b"), ["100"])
        self.assertEqual(new_qs.update_parameter("c", ["40"]), new_qs)
        self.assertEqual(new_qs.parameter_values("c"), ["40"])
        self.assertEqual(new_qs.get_query_string(), "?a=10&b=100&c=40")

    def test_remove_parameter(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.remove_parameter("a"), new_qs)
        self.assertFalse(new_qs.parameter_exists("a"))
        self.assertEqual(new_qs.remove_parameter("b"), new_qs)
        self.assertFalse(new_qs.parameter_exists("b"))
        with self.assertRaises(KeyError):
            new_qs.remove_parameter("c")
        self.assertEqual(new_qs.get_query_string(), "")

    def test_is_value_in_parameter(self):
        manipulator = QueryStringTransformer(self.test_query)
        self.assertTrue(manipulator.is_value_in_parameter("a", "1"))
        self.assertTrue(manipulator.is_value_in_parameter("b", "2"))
        self.assertTrue(manipulator.is_value_in_parameter("b", "3"))
        self.assertFalse(manipulator.is_value_in_parameter("b", "4"))
        with self.assertRaises(KeyError):
            manipulator.is_value_in_parameter("c", "5")

    def test_toggle_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.toggle_parameter_value("a", "1"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("a", "1"))
        self.assertEqual(new_qs.toggle_parameter_value("a", "10"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "10"))
        self.assertEqual(new_qs.toggle_parameter_value("b", "2"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("b", "2"))
        self.assertEqual(new_qs.get_query_string(), "?a=10&b=3")
        self.assertEqual(new_qs.toggle_parameter_value("a", "1"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "1"))
        self.assertEqual(new_qs.get_query_string(), "?a=10&a=1&b=3")
        with self.assertRaises(KeyError):
            new_qs.toggle_parameter_value("c", "4")
        with self.assertRaises(KeyError):
            new_qs.toggle_parameter_value("c", "4")

    def test_add_remove_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.add_parameter_value("a", "10"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "10"))
        self.assertEqual(new_qs.parameter_values("a"), ["1", "10"])
        with self.assertRaises(KeyError):
            new_qs.add_parameter_value("c", "4")

    def test_remove_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.remove_parameter_value("b", "2"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("b", "2"))
        self.assertEqual(new_qs.parameter_values("b"), ["3"])
        with self.assertRaises(KeyError):
            new_qs.remove_parameter_value("c", "4")

    def test_initial_query_string_cannot_be_modified(self):
        manipulator = QueryStringTransformer(self.test_query)

        with self.assertRaises(AttributeError):
            manipulator.add_parameter("c", "4")
        with self.assertRaises(AttributeError):
            manipulator.update_parameter("a", ["3"])
        with self.assertRaises(AttributeError):
            manipulator.add_parameter_value("a", "4")
        with self.assertRaises(AttributeError):
            manipulator.toggle_parameter_value("a", "5")
        with self.assertRaises(AttributeError):
            manipulator.remove_parameter_value("a", "5")
        with self.assertRaises(AttributeError):
            manipulator.remove_parameter("a")

    def test_new_modifyable_instances_do_not_conflict(self):
        manipulator = QueryStringTransformer(self.test_query)

        new_qs_1 = manipulator.new()
        self.assertEqual(new_qs_1.remove_parameter("b"), new_qs_1)
        self.assertEqual(new_qs_1.get_query_string(), "?a=1")

        new_qs_2 = manipulator.new()
        self.assertEqual(new_qs_2.get_query_string(), "?a=1&b=2&b=3")


class TestTolerantQueryStringTransformer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_query = [("a", ["1"]), ("b", ["2", "3"])]

    def test_add_parameter(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.add_parameter("h", [False]), new_qs)
        self.assertTrue(new_qs.parameter_exists("h"))
        self.assertEqual(new_qs.parameter_values("h"), ["False"])

        self.assertEqual(new_qs.add_parameter("h", [True]), new_qs)
        self.assertTrue(new_qs.parameter_exists("h"))
        self.assertEqual(new_qs.parameter_values("h"), ["True"])

        self.assertEqual(new_qs.get_query_string(), "?a=1&b=2&b=3&h=True")

    def test_update_parameter(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.update_parameter("a", "10"), new_qs)
        self.assertEqual(new_qs.parameter_values("a"), ["10"])
        self.assertEqual(new_qs.update_parameter("b", ["20", "30"]), new_qs)
        self.assertEqual(new_qs.parameter_values("b"), ["20", "30"])
        self.assertEqual(new_qs.update_parameter("b", "100"), new_qs)
        self.assertEqual(new_qs.parameter_values("b"), ["100"])
        self.assertEqual(new_qs.update_parameter("c", ["40"]), new_qs)
        self.assertEqual(new_qs.parameter_values("c"), ["40"])
        self.assertEqual(new_qs.get_query_string(), "?a=10&b=100&c=40")
        self.assertEqual(new_qs.update_parameter("c", "50"), new_qs)
        self.assertEqual(new_qs.parameter_values("c"), ["50"])
        self.assertEqual(new_qs.get_query_string(), "?a=10&b=100&c=50")

    def test_remove_parameter(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.remove_parameter("a"), new_qs)
        self.assertFalse(new_qs.parameter_exists("a"))
        self.assertEqual(new_qs.remove_parameter("b"), new_qs)
        self.assertFalse(new_qs.parameter_exists("b"))
        self.assertEqual(new_qs.remove_parameter("c"), new_qs)
        self.assertEqual(new_qs.get_query_string(), "")

    def test_is_value_in_parameter(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertTrue(new_qs.is_value_in_parameter("a", "1"))
        self.assertTrue(new_qs.is_value_in_parameter("b", "2"))
        self.assertTrue(new_qs.is_value_in_parameter("b", "3"))
        self.assertFalse(new_qs.is_value_in_parameter("b", "4"))
        self.assertFalse(new_qs.is_value_in_parameter("c", "5"))

    def test_toggle_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.toggle_parameter_value("a", "1"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("a", "1"))
        self.assertEqual(new_qs.toggle_parameter_value("a", "10"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "10"))
        self.assertEqual(new_qs.toggle_parameter_value("b", "2"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("b", "2"))
        self.assertEqual(new_qs.get_query_string(), "?a=10&b=3")
        self.assertEqual(new_qs.toggle_parameter_value("a", "1"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "1"))
        self.assertEqual(new_qs.toggle_parameter_value("c", "4"), new_qs)
        self.assertEqual(new_qs.get_query_string(), "?a=10&a=1&b=3&c=4")
        self.assertEqual(new_qs.toggle_parameter_value("c", "4"), new_qs)
        self.assertEqual(new_qs.get_query_string(), "?a=10&a=1&b=3")

    def test_add_remove_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.add_parameter_value("a", "10"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("a", "10"))
        self.assertEqual(new_qs.parameter_values("a"), ["1", "10"])
        self.assertEqual(new_qs.add_parameter_value("c", "4"), new_qs)
        self.assertTrue(new_qs.is_value_in_parameter("c", "4"))
        self.assertEqual(new_qs.parameter_values("c"), ["4"])

    def test_remove_parameter_value(self):
        manipulator = QueryStringTransformer(self.test_query, tolerant=True)
        new_qs = manipulator.new()

        self.assertEqual(new_qs.remove_parameter_value("b", "2"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("b", "2"))
        self.assertEqual(new_qs.parameter_values("b"), ["3"])
        self.assertEqual(new_qs.remove_parameter_value("c", "4"), new_qs)
        self.assertFalse(new_qs.is_value_in_parameter("c", "4"))
