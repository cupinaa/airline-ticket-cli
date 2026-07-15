import unittest

from airline.validation import crosses_midnight


class ValidationTests(unittest.TestCase):
    def test_same_day_flight_does_not_cross_midnight(self):
        self.assertEqual("no", crosses_midnight("07:30", "09:15"))

    def test_overnight_flight_crosses_midnight(self):
        self.assertEqual("yes", crosses_midnight("23:30", "01:15"))


if __name__ == "__main__":
    unittest.main()
