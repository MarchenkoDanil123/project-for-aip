import unittest
from main import *


class RunLengthEncodingTest(unittest.TestCase):
    def test_round_complex_1(self):
        self.assertMultiLineEqual(str(round_complex(-0.5+0.8660254037844386j)), '-0.50+0.87j')

    def test_round_complex_2(self):
        self.assertMultiLineEqual(str(round_complex((-0.5-0.8660254037844386j))), '-0.50-0.87j')

    def test_start(self):
        self.assertMultiLineEqual(str(start()), '1')

    def test_calculator(self):
        self.assertMultiLineEqual(str(calculator()), '1')

    def test_query_handle(self):
        self.assertMultiLineEqual(str(query_handler()), '1')

    def test_round_complex_(self):
        self.assertMultiLineEqual(str(round_complex((-4.5-6.866025444386j))), '-4.50-6.87j')

    def test_round_complex_3(self):
        self.assertMultiLineEqual(str(round_complex((-9.5-100.37844386j))), '-9.50-100.38j')

    def test_round_complex_4(self):
        self.assertMultiLineEqual(str(round_complex((-3.5-0.8660256j))), '-3.50-0.87j')

    def test_round_complex_5(self):
        self.assertMultiLineEqual(str(round_complex((-0.5-0.6j))), '-0.50-0.60j')


if __name__ == "__main__":
    unittest.main()