import unittest

import geodn


class TestGeoDN(unittest.TestCase):

    def test_github(self):
        self.assertEqual(geodn.main('github.com'), 'US')

    def test_python(self):
        self.assertEqual(geodn.main('python.org'), 'US')


if __name__ == '__main__':
    unittest.main()
