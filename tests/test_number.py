import unittest

from tna_utilities.number import numberish


class TestNumber(unittest.TestCase):

    def test_happy(self):
        self.assertEqual(numberish(0), "None")
        self.assertEqual(numberish(1), "1")
        self.assertEqual(numberish(99), "99")
        self.assertEqual(numberish(100), "100")
        self.assertEqual(numberish(999), "999")
        self.assertEqual(numberish(1000), "1 thousand")
        self.assertEqual(numberish(1001), "About 1 thousand")
        self.assertEqual(numberish(1337), "About 1.3 thousand")
        self.assertEqual(numberish(9999), "About 10 thousand")
        self.assertEqual(numberish(10000), "10 thousand")
        self.assertEqual(numberish(10001), "About 10 thousand")
        self.assertEqual(numberish(11000), "11 thousand")
        self.assertEqual(numberish(11001), "About 11 thousand")
        self.assertEqual(numberish(11499), "About 11 thousand")
        self.assertEqual(numberish(11500), "About 12 thousand")
        self.assertEqual(numberish(11999), "About 12 thousand")
        self.assertEqual(numberish(100000), "100 thousand")
        self.assertEqual(numberish(100001), "About 100 thousand")
        self.assertEqual(numberish(1000000), "1 million")
        self.assertEqual(numberish(1000001), "About 1 million")
        self.assertEqual(numberish(1234567), "About 1.2 million")
        self.assertEqual(numberish(12345678), "About 12 million")
        self.assertEqual(numberish(123456789), "About 120 million")
        self.assertEqual(numberish(1234567890), "About 1.2 billion")
        self.assertEqual(numberish(1337.1337), "About 1.3 thousand")

    def test_happy_simplified(self):
        self.assertEqual(numberish(0, simple_units=True), "None")
        self.assertEqual(numberish(1, simple_units=True), "1")
        self.assertEqual(numberish(99, simple_units=True), "99")
        self.assertEqual(numberish(100, simple_units=True), "100")
        self.assertEqual(numberish(999, simple_units=True), "999")
        self.assertEqual(numberish(1000, simple_units=True), "1k")
        self.assertEqual(numberish(1001, simple_units=True), "About 1k")
        self.assertEqual(numberish(1337, simple_units=True), "About 1.3k")
        self.assertEqual(numberish(9999, simple_units=True), "About 10k")
        self.assertEqual(numberish(10000, simple_units=True), "10k")
        self.assertEqual(numberish(10001, simple_units=True), "About 10k")
        self.assertEqual(numberish(11000, simple_units=True), "11k")
        self.assertEqual(numberish(11001, simple_units=True), "About 11k")
        self.assertEqual(numberish(11499, simple_units=True), "About 11k")
        self.assertEqual(numberish(11500, simple_units=True), "About 12k")
        self.assertEqual(numberish(11999, simple_units=True), "About 12k")
        self.assertEqual(numberish(100000, simple_units=True), "100k")
        self.assertEqual(numberish(100001, simple_units=True), "About 100k")
        self.assertEqual(numberish(1000000, simple_units=True), "1m")
        self.assertEqual(numberish(1000001, simple_units=True), "About 1m")
        self.assertEqual(numberish(1234567, simple_units=True), "About 1.2m")
        self.assertEqual(numberish(12345678, simple_units=True), "About 12m")
        self.assertEqual(numberish(123456789, simple_units=True), "About 120m")
        self.assertEqual(numberish(1234567890, simple_units=True), "About 1.2b")
        self.assertEqual(numberish(1337.1337, simple_units=True), "About 1.3k")

    def test_happy_prefix_string(self):
        self.assertEqual(
            numberish(1499999, simple_units=True, prefix_text="Approx "), "Approx 1.5m"
        )
        self.assertEqual(
            numberish(1499999, simple_units=True, prefix_text="~"), "~1.5m"
        )

    def test_happy_prefix_tuple(self):
        self.assertEqual(
            numberish(1000000, simple_units=True, prefix_text=("Almost ", "Over ")),
            "1m",
        )
        self.assertEqual(
            numberish(1499999, simple_units=True, prefix_text=("Almost ", "Over ")),
            "Almost 1.5m",
        )
        self.assertEqual(
            numberish(1500000, simple_units=True, prefix_text=("Almost ", "Over ")),
            "1.5m",
        )
        self.assertEqual(
            numberish(1500001, simple_units=True, prefix_text=("Almost ", "Over ")),
            "Over 1.5m",
        )

    def test_unhappy(self):
        with self.assertRaises(ValueError):
            numberish("one")
        with self.assertRaises(ValueError):
            numberish(None)
        with self.assertRaises(ValueError):
            numberish({})
        with self.assertRaises(ValueError):
            numberish([])
