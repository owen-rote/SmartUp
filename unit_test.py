import unittest
from datetime import datetime

def is_valid_date_format(date_string):
    try:
        datetime.strptime(date_string, '%m/%d/%Y')
        return True
    except ValueError:
        return False

class TestDateValidation(unittest.TestCase):

    def test_valid_dates(self):
        self.assertTrue(is_valid_date_format("01/01/2023"))
        self.assertTrue(is_valid_date_format("12/31/2022"))
        self.assertTrue(is_valid_date_format("06/15/2023"))

    def test_invalid_format(self):
        self.assertFalse(is_valid_date_format("2023/05/12"))  # Incorrect separator
        self.assertFalse(is_valid_date_format("12-31-2022"))  # Different separator
        self.assertFalse(is_valid_date_format("01/01/23"))    # Year format incorrect
        self.assertFalse(is_valid_date_format("13/01/2023"))  # Month out of range

    def test_invalid_day_and_month(self):
        # Invalid day for month
        self.assertFalse(is_valid_date_format("04/31/2023"))  
        # Month out of range
        self.assertFalse(is_valid_date_format("13/01/2023"))  
        # Leap year test - February 30th doesn't exist
        self.assertFalse(is_valid_date_format("02/30/2023"))  
        # Leap year test - February 29th on a non-leap year
        self.assertFalse(is_valid_date_format("02/29/2021"))  
        # Leap year test - February 29th on a leap year
        self.assertTrue(is_valid_date_format("02/29/2024"))   

    def test_empty_or_none(self):
        self.assertFalse(is_valid_date_format(""))    # Empty string
        self.assertFalse(is_valid_date_format(None))  # None type

if __name__ == '__main__':
    unittest.main()