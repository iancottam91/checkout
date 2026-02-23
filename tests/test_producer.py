import re
import unittest
from app.producer.producer import generate_uk_postcode
from app.producer.producer import generate_webaddres


class TestGenerateUKPostcode(unittest.TestCase):

    def test_returns_string(self):
        """Test that the function returns a string."""
        result = generate_uk_postcode()
        self.assertIsInstance(result, str)


    def test_correct_length_range(self):
        """Test that the total postcode length is within expected range."""
        result = generate_uk_postcode()
        self.assertGreaterEqual(len(result), 6)
        self.assertLessEqual(len(result), 8)

class TestGenerateWebAddress(unittest.TestCase):

    def test_returns_string(self):
        """Test that the function returns a string."""
        result = generate_webaddres()
        self.assertIsInstance(result, str)


    def test_correct_length_range(self):
        """Test that the address is in the correct shape."""
        result = generate_webaddres()
        self.assertGreaterEqual(len(result), 8)


if __name__ == '__main__':
    unittest.main()
