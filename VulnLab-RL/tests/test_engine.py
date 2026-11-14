import unittest

from vulnlab.engine import score_submission


class ScoringTests(unittest.TestCase):
    def test_perfect_match_scores_100(self):
        result = score_submission({
            "scenario_id": "AUTHZ-001",
            "findings": [{
                "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
                "severity": "high",
                "evidence": "The design omits an ownership check for the authenticated user.",
            }],
        })
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["missing"], [])

    def test_wrong_severity_reduces_score(self):
        result = score_submission({
            "scenario_id": "AUTHZ-001",
            "findings": [{
                "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
                "severity": "low",
                "evidence": "The design omits an ownership check for the authenticated user.",
            }],
        })
        self.assertEqual(result["score"], 80)

    def test_missing_finding_scores_zero(self):
        result = score_submission({"scenario_id": "AUTHZ-001", "findings": []})
        self.assertEqual(result["score"], 0)
        self.assertEqual(len(result["missing"]), 1)

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            score_submission({"scenario_id": "NOT-A-SCENARIO", "findings": []})

    def test_invalid_findings_type_is_rejected(self):
        with self.assertRaises(ValueError):
            score_submission({"scenario_id": "AUTHZ-001", "findings": "not-a-list"})


if __name__ == "__main__":
    unittest.main()
