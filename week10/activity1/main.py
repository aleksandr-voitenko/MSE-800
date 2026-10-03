import unittest
from calculator import calculator

class TestCalculator(unittest.TestCase):

    def test_add(self):
        result = calculator.add(2, 3)
        self.assertEqual(result, 5)

    def test_divide(self):
        result = calculator.divide(10, 2)
        self.assertEqual(result, 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(10, 0)

if __name__ == '__main__':
    unittest.main()
