"""Dependency-free tests for safe diagnostic thermal computations."""
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

    def test_empty_and_short_history(self):
        self.assertIsNone(thermal.calculate_trend([]))
        self.assertIsNone(thermal.calculate_trend([
            (self.now - timedelta(minutes=20), 20), (self.now, 20.1)
        ]))

    def test_warming_and_cooling(self):
        old = self.now - timedelta(hours=2)
        self.assertEqual(thermal.calculate_trend([(old, 20), (self.now, 21)]), 0.5)
        self.assertEqual(thermal.calculate_trend([(old, 21), (self.now, 20)]), -0.5)

    def test_coverage(self):
        self.assertEqual(thermal.quality_label([]), "Afventer målinger")
        samples = [(self.now - timedelta(minutes=10 * i), 21) for i in reversed(range(73))]
        self.assertEqual(thermal.quality_label(samples), "God datadækning")

    def test_restore_filters_old_invalid(self):
        raw = [[(self.now-timedelta(hours=100)).isoformat(), 21],
               [(self.now-timedelta(hours=1)).isoformat(), "nan"],
               [(self.now-timedelta(hours=1)).isoformat(), 23],
               ["not-a-date", 20]]
        self.assertEqual(thermal.restore_history(raw, self.now),
                         [(self.now-timedelta(hours=1), 23)])

    def test_pair_restore_and_average(self):
        pairs = [((self.now-timedelta(minutes=10*i)).isoformat(), 21, 1)
                 for i in reversed(range(19))]
        pairs += [["bad", 20, 0], [self.now.isoformat(), 21, "inf"]]
        restored = thermal.restore_pairs(pairs, self.now)
        self.assertEqual(len(restored), 19)
        self.assertEqual(thermal.mean_temperature_gap(restored), 20)
        self.assertIsNone(thermal.mean_temperature_gap(restored[:5]))

    def test_temperature_status(self):
        self.assertEqual(thermal.heating_observation(-0.2, 19, 21), "Under mål og faldende")
        self.assertEqual(thermal.heating_observation(None, 19, 21), "Afventer temperaturhistorik")
        self.assertEqual(thermal.heating_observation(0, 21, 21), "Temperaturen er omtrent stabil")


if __name__ == "__main__":
    unittest.main()
