"""Dependency-free tests for observed temperature trend and storage validation."""
import importlib.util
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "custom_components" / "ai_smart_home_pro" / "thermal.py"
spec = importlib.util.spec_from_file_location("thermal_under_test", MODULE)
thermal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(thermal)


class ThermalTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 24, tzinfo=timezone.utc)

    def test_empty_trend(self):
        self.assertIsNone(thermal.calculate_trend([]))

    def test_too_short(self):
        self.assertIsNone(thermal.calculate_trend([
            (self.now - timedelta(minutes=20), 20), (self.now, 20.1)
        ]))

    def test_warming_and_cooling(self):
        a = self.now - timedelta(hours=2)
        self.assertEqual(thermal.calculate_trend([(a, 20), (self.now, 21)]), 0.5)
        self.assertEqual(thermal.calculate_trend([(a, 21), (self.now, 20)]), -0.5)

    def test_coverage(self):
        self.assertEqual(thermal.quality_label([]), "Afventer målinger")
        samples = [(self.now - timedelta(minutes=10 * i), 21.0) for i in reversed(range(73))]
        self.assertEqual(thermal.quality_label(samples), "God datadækning")

    def test_restore_rejects_invalid_and_old(self):
        raw = [
            [(self.now - timedelta(hours=100)).isoformat(), 21.0],
            [(self.now - timedelta(hours=1)).isoformat(), "nan"],
            [(self.now - timedelta(hours=1)).isoformat(), 23.0],
            ["invalid-date", 22.0],
            [(self.now + timedelta(days=1)).isoformat(), 20.0],
            [(self.now - timedelta(hours=2)).isoformat(), 41],
        ]
        self.assertEqual(thermal.restore_history(raw, self.now), [
            (self.now - timedelta(hours=1), 23.0)
        ])


if __name__ == "__main__":
    unittest.main()
