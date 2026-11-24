"""Tests for the dependency-free observational trend estimator."""
import unittest
from datetime import datetime, timedelta, timezone

from custom_components.ai_smart_home_pro.thermal import calculate_trend


class TrendTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 24, tzinfo=timezone.utc)

    def test_insufficient_samples(self):
        self.assertIsNone(calculate_trend([]))
        self.assertIsNone(calculate_trend([(self.now, 21.0)]))

    def test_short_window_returns_none(self):
        points = [(self.now - timedelta(minutes=20), 20.0), (self.now, 20.1)]
        self.assertIsNone(calculate_trend(points))

    def test_warming(self):
        points = [(self.now - timedelta(hours=2), 20.0), (self.now, 21.0)]
        self.assertEqual(calculate_trend(points), 0.5)

    def test_cooling(self):
        points = [(self.now - timedelta(hours=1), 21.0), (self.now, 20.5)]
        self.assertEqual(calculate_trend(points), -0.5)


if __name__ == "__main__":
    unittest.main()
