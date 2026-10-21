import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prewarm import score_candidate, rank_file, estimate  # noqa: E402
from validate_skill import validate  # noqa: E402


class ScoringTests(unittest.TestCase):
    def test_best_public_repo_context_is_pilot(self):
        result = score_candidate({"name": "Stable repo", "reuse": "5", "stability": "5",
                                  "deliverable": "5", "confidence": "5", "scope_cost": "2",
                                  "sensitivity": "1"})
        self.assertEqual(result["decision"], "pilot")

    def test_secret_work_rejected(self):
        result = score_candidate({"name": "Sensitive", "reuse": "5", "stability": "5",
                                  "deliverable": "5", "confidence": "5", "scope_cost": "1",
                                  "sensitivity": "5"})
        self.assertEqual(result["decision"], "reject")

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            score_candidate({"name": "Bad", "reuse": "6"})

    def test_sample_file(self):
        results = rank_file(ROOT / "examples" / "candidates.csv")
        self.assertEqual(results[0]["decision"], "pilot")
        self.assertEqual(len(results), 5)
        self.assertEqual(next(r for r in results if r["name"] == "Restricted-content inspection")["decision"], "reject")


class EstimatorTests(unittest.TestCase):
    def test_example(self):
        result = estimate(40000, 3, 0.8, 0.1, 1.0, 2000)
        self.assertAlmostEqual(result["future_gross_saved_input_units"], 86400)
        self.assertAlmostEqual(result["lifetime_net_input_units"], 44400)
        self.assertEqual(result["minimum_expected_future_uses_to_break_even"], 2)

    def test_zero_hits(self):
        result = estimate(10000, 3, 0, 0.1, 1.0)
        self.assertIsNone(result["minimum_expected_future_uses_to_break_even"])
        self.assertLess(result["lifetime_net_input_units"], 0)

    def test_bad_fraction(self):
        with self.assertRaises(ValueError):
            estimate(10000, 3, 1.1, 0.1, 1)
        with self.assertRaises(ValueError):
            estimate(10000, 3, float("nan"), 0.1, 1)

    def test_finite_positive_cost(self):
        with self.assertRaises(ValueError):
            estimate(10000, 3, 0.8, 0.1, -1)
        with self.assertRaises(ValueError):
            estimate(0, 3, 0.8, 0.1, 1)


class SkillTests(unittest.TestCase):
    def test_metadata(self):
        validate()


if __name__ == "__main__":
    unittest.main()
