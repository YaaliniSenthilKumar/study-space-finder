"""Tests for status.py. Run with:  python3 -m unittest test_status.py"""
import unittest

from status import get_status


class TestGetStatus(unittest.TestCase):
    def test_empty_space_is_quiet(self):
        self.assertEqual(get_status(0, 100), "Quiet")

    def test_just_under_half_is_quiet(self):
        self.assertEqual(get_status(49, 100), "Quiet")

    def test_half_full_is_filling_up(self):
        self.assertEqual(get_status(50, 100), "Filling up")

    def test_eighty_five_percent_is_filling_up(self):
        self.assertEqual(get_status(85, 100), "Filling up")

    def test_over_eighty_five_percent_is_full(self):
        self.assertEqual(get_status(86, 100), "Full")

    def test_completely_full_is_full(self):
        self.assertEqual(get_status(100, 100), "Full")

    def test_zero_capacity_raises_error(self):
        with self.assertRaises(ValueError):
            get_status(5, 0)


if __name__ == "__main__":
    unittest.main()
