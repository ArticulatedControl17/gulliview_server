import unittest
from errorCalc import *

mod = errorCalc('testPath.txt')

class TestOneLapCounterClockWise(unittest.TestCase):
    global mod
    def test_up_strait(self):
        self.assertEqual(mod.calculateError(Point(105,60)), 5)

    def test_up_left(self):
        self.assertTrue(False)

    def test_left_strait(self):
        self.assertTrue(True)

    def test_left_down(self):
        self.assertTrue(True)

    def test_down_strait(self):
        self.assertTrue(True)

    def test_down_right(self):
        self.assertTrue(True)

    def test_right_strait(self):
        self.assertTrue(True)

    def test_right_up(self):
        self.assertTrue(True)

    def test_up_strait_one_lap(self):
        self.assertTrue(True)

    #def test_split(self):
    #    s = 'hello world'
    #    self.assertEqual(s.split(), ['hello', 'world'])
    #    # check that s.split fails when the separator is not a string
    #    with self.assertRaises(TypeError):
    #        s.split(2)

if __name__ == '__main__':
    unittest.main()
