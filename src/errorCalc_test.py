import unittest
from errorCalc import *

mod = errorCalc('testPath.txt')

class TestOneLapCounterClockWise(unittest.TestCase):

#900 2764
#900 7917
#1015 8375
#1246 8690
#1442 8856
#1923 8992
#2837 8992


    global mod

    def test_up_strait(self):
        print mod.calculateError(Point(900,5000))
        #self.assertTrue(mod.calculateError(Point(900,5000))>-10)
        print mod.calculateError(Point(900,8000))
        print mod.calculateError(Point(900,7900))
        print mod.calculateError(Point(1015,8400))
        #self.assertTrue(mod.calculateError(Point(900,8000))>-100)
    def test_up_left(self):
        self.assertTrue(True)

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
