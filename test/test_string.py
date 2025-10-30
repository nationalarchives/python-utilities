import unittest

from tna_utilities.string import slugify, unslugify


class TestSlugify(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("test"), "test")
        self.assertEqual(slugify("  test TEST"), "test-test")
        self.assertEqual(slugify("test 12 3 -4 "), "test-12-3-4")
        self.assertEqual(slugify("test---test"), "test-test")
        self.assertEqual(slugify("test---"), "test")
        self.assertEqual(slugify("test---$"), "test")
        self.assertEqual(slugify("test---$---"), "test")


class TestUnslugify(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(unslugify("test-test"), "Test test")
        self.assertEqual(unslugify("test-test", capitalize_first=False), "test test")
        self.assertEqual(unslugify("test-123"), "Test 123")
        self.assertEqual(unslugify("test-1-2-3"), "Test 1 2 3")
