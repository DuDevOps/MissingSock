import unittest

class FirstTestCase(unittest.TestCase):

    def setup(self):
        """  setup is run before each unittest """
        print(f"{__name__} call of setup ")
        pass

    def teardown(self):
        """ teardown is run after each unittest"""
        print(f"{__name__} call of teardown ")
        pass

class SecondTestCase(unittest.TestCase):
    def test_first(self):
        self.assertEqual(4,4,"Just a check")

    def test_second(self):
        self.assertEqual(5,5,"just 2nd unittest")

if __name__ == '__main__':
    unittest.main()