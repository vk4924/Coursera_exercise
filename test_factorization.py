import unittest


def factorize(x):
    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = ('string', 1.5)
        for a in self.cases:
            with self.subTest(case=a):
                self.assertRaises(TypeError, factorize, a)

    def test_negative(self):
        self.cases = (-1, -10, -100)
        for a in self.cases:
            with self.subTest(case=a):
                self.assertRaises(ValueError, factorize, a)

    def test_zero_and_one_cases(self):
        self.cases = (0, 1)
        for a in self.cases:
            with self.subTest(case=a):
                self.assertEqual(factorize(a),(a,))

    def test_simple_numbers(self):
        self.cases = (3, 13, 29)
        for a in self.cases:
            with self.subTest(x=a):
                self.assertEqual(factorize(a),(a,))

    def test_two_simple_multipliers(self):
        check_dict = {6: (2, 3), 26: (2,13), 121:(11,11)}
        self.cases = (6, 26, 121)
        for a in self.cases:
            with self.subTest(x=a):
                self.assertEqual(factorize(a), check_dict[a])

    def test_many_multipliers(self):
        check_dict = {1001: (7, 11, 13), 9699690: (2, 3, 5, 7, 11, 13, 17, 19)}
        self.cases = (1001, 9699690)
        for a in self.cases:
            with self.subTest(x=a):
                self.assertEqual(factorize(a), check_dict[a])



if __name__=='__main__':
    unittest.main()
