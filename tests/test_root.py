import unittest

from tna_utilities import strtobool


class TestStrToBool(unittest.TestCase):
    def test_truthy_values(self):
        self.assertTrue(strtobool("yes"))
        self.assertTrue(strtobool("y"))
        self.assertTrue(strtobool("yES"))
        self.assertTrue(strtobool("t"))
        self.assertTrue(strtobool("true"))
        self.assertTrue(strtobool("True"))
        self.assertTrue(strtobool("TRUE"))
        self.assertTrue(strtobool("on"))
        self.assertTrue(strtobool("ON"))
        self.assertTrue(strtobool("1"))

    def test_falsy_values(self):
        self.assertFalse(strtobool("no"))
        self.assertFalse(strtobool("n"))
        self.assertFalse(strtobool("NO"))
        self.assertFalse(strtobool("f"))
        self.assertFalse(strtobool("false"))
        self.assertFalse(strtobool("False"))
        self.assertFalse(strtobool("FALSE"))
        self.assertFalse(strtobool("off"))
        self.assertFalse(strtobool("OFF"))
        self.assertFalse(strtobool("0"))

    def test_incorrect_values(self):
        with self.assertRaises(ValueError):
            strtobool(" yes ")
        with self.assertRaises(ValueError):
            strtobool("2")
        with self.assertRaises(ValueError):
            self.assertFalse(strtobool(""))
        with self.assertRaises(ValueError):
            self.assertFalse(strtobool("yeah"))
        with self.assertRaises(ValueError):
            self.assertFalse(strtobool("   "))

    def test_invalid_values(self):
        with self.assertRaises(TypeError):
            strtobool(True)
        with self.assertRaises(TypeError):
            strtobool(False)
        with self.assertRaises(TypeError):
            strtobool(None)
        with self.assertRaises(TypeError):
            strtobool(0)
        with self.assertRaises(TypeError):
            strtobool(1)
        with self.assertRaises(TypeError):
            strtobool(3.14)
        with self.assertRaises(TypeError):
            strtobool([])
        with self.assertRaises(TypeError):
            strtobool({})
        with self.assertRaises(TypeError):
            strtobool(())
        with self.assertRaises(TypeError):
            strtobool(lambda: "true")
        with self.assertRaises(TypeError):
            strtobool()
