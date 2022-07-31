import unittest


class NamedTest(unittest.TestCase):
    def test_constructor(self):
        name = "test_name"
        named = Named(name)


if __name__ == '__main__':
    unittest.main()
