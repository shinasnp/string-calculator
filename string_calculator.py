import re


class NegativeNumberException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DelimiterStrategy:
    def split(self, numbers: str):
        raise NotImplementedError


class DefaultDelimiterStrategy(DelimiterStrategy):
    def split(self, numbers: str):
        # Default strategy: Split by comma and newline, and allow negative numbers
        return re.findall(r'-?\d+', numbers)


class CustomDelimiterStrategy(DelimiterStrategy):
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def split(self, numbers: str):
        # Custom strategy: Split by the given delimiter
        return numbers.split(self.delimiter)


class StringCalculator:
    def __init__(self):
        self.delimiter_strategy = DefaultDelimiterStrategy()  # Default to comma and newline

    def add(self, numbers: str) -> int:
        if not numbers:
            return 0

        # Check for custom delimiter and switch strategy if needed
        if numbers.startswith("//"):
            numbers = self._remove_delimiters_from_input(numbers)
            self._set_custom_delimiter(numbers)

        # Use the current delimiter strategy to split the numbers
        number_list = self._split_numbers(numbers)

        # Check for negative numbers and raise exception if any found
        self._check_for_negative_numbers(number_list)

        # Return the sum of the numbers
        return sum(number_list)

    def _set_custom_delimiter(self, numbers: str):
        """Extract the custom delimiter if provided."""
        # Custom delimiter may have multiple delimiters wrapped with square brackets
        delimiter_part = numbers.split("\n")[0]  # Get the first line with delimiter information
        if delimiter_part.startswith("//"):
            delimiter = delimiter_part[2:]  # Strip "//"
            if delimiter.startswith("[") and delimiter.endswith("]"):
                delimiter = delimiter[1:-1]  # Strip the square brackets for a multi-character delimiter
            self.delimiter_strategy = CustomDelimiterStrategy(delimiter)

    def _remove_delimiters_from_input(self, numbers: str) -> str:
        """Remove the custom delimiter line from the input."""
        if numbers.startswith("//"):
            parts = numbers.split("\n", 1)
            numbers = parts[1] if len(parts) > 1 else ""  # Remove the delimiter line
        return numbers

    def _split_numbers(self, numbers: str):
        """Use the appropriate delimiter strategy to split the numbers."""
        # If a custom delimiter is set, use that; otherwise, use the default
        numbers = self.delimiter_strategy.split(numbers)

        # Convert the string digits to integers
        return [int(num) for num in numbers]

    def _check_for_negative_numbers(self, numbers: list):
        """Check for negative numbers and raise an exception if any are found."""
        negative_numbers = [num for num in numbers if num < 0]
        if negative_numbers:
            raise NegativeNumberException(f"negative numbers not allowed: {', '.join(map(str, negative_numbers))}")


# Example of running the calculator with test cases (for testing purposes)
if __name__ == "__main__":
    calculator = StringCalculator()

    # Test cases
    print(calculator.add(""))  # Output: 0
    print(calculator.add("1"))  # Output: 1
    print(calculator.add("1,5"))  # Output: 6
    print(calculator.add("1\n2,3"))  # Output: 6
    print(calculator.add("//;\n1;2"))  # Output: 3
    print(calculator.add("//;\n1;;2"))  # Output: 3 (handles extra delimiters correctly)
    print(calculator.add("//;\n;1;2;"))  # Output: 3 (handles extra delimiters at the start and end)
    print(calculator.add("//;\n1;;"))  # Output: 1 (handles trailing empty numbers correctly)
    print(calculator.add("//;\n;;"))  # Output: 0 (empty input after delimiters)

    # Negative test case - should raise an exception
    try:
        print(calculator.add("//;\n1;-2;3"))  # Raises exception for negative numbers
    except NegativeNumberException as e:
        print(e)  # Output: negative numbers not allowed: -2
