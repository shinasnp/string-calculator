import unittest
from string_calculator import StringCalculator, NegativeNumberException


class TestStringCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = StringCalculator()

    # Test cases

    def test_empty_string(self):
        self.assertEqual(self.calculator.add(""), 0)

    def test_single_number(self):
        self.assertEqual(self.calculator.add("1"), 1)

    def test_two_numbers_comma(self):
        self.assertEqual(self.calculator.add("1,5"), 6)

    def test_numbers_with_newline_and_comma(self):
        self.assertEqual(self.calculator.add("1\n2,3"), 6)

    def test_custom_delimiter(self):
        self.assertEqual(self.calculator.add("//;\n1;2"), 3)

    def test_extra_delimiters(self):
        self.assertEqual(self.calculator.add("//;\n1;;2"), 3)  # Handles extra delimiters correctly

    def test_delimiters_at_start_and_end(self):
        self.assertEqual(self.calculator.add("//;\n;1;2;"), 3)  # Handles extra delimiters at the start and end

    def test_trailing_empty_numbers(self):
        self.assertEqual(self.calculator.add("//;\n1;;"), 1)  # Handles trailing empty numbers correctly

    def test_empty_input_after_delimiters(self):
        self.assertEqual(self.calculator.add("//;\n;;"), 0)  # Empty input after delimiters

    def test_multiple_negative_numbers(self):
        with self.assertRaises(NegativeNumberException) as context:
            self.calculator.add("//;\n1;-2;3")
        self.assertEqual(str(context.exception), "negative numbers not allowed: -2")

    def test_custom_delimiter_with_square_brackets(self):
        self.assertEqual(self.calculator.add("//[***]\n1***2***3"), 6)  # Handles custom delimiter with square brackets

    def test_multiple_custom_delimiters(self):
        self.assertEqual(self.calculator.add("//[***][###]\n1***2###3"), 6)  # Handles multiple custom delimiters

    def test_negative_number_in_multiple_delimiters(self):
        with self.assertRaises(NegativeNumberException) as context:
            self.calculator.add("//[***][###]\n1***-2###3")
        self.assertEqual(str(context.exception), "negative numbers not allowed: -2")


if __name__ == '__main__':
    unittest.main()
