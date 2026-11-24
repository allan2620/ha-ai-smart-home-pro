"""Unit tests for the dependency-free temperature trend module."""
import importlib.util
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "custom_components" / "ai_smart_home_pro" / "thermal.py"
spec = importlib.util.spec_from_file_location("thermal_under_test", MODULE)
thermal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(thermal)
calculate_trend = thermal.calculate_trend


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
