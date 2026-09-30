"""Smoke tests for the stable CiviQ / Nori MVP fallback engine."""

import unittest

from agent.nori_mock import build_demo_response


class CiviQMockTests(unittest.TestCase):
    def test_food(self) -> None:
        result = build_demo_response("I need food support this week")
        self.assertEqual(result["resources"][0]["id"], "sf-marin-food-bank")

    def test_eviction(self) -> None:
        result = build_demo_response("My landlord gave me an eviction notice")
        self.assertEqual(result["resources"][0]["id"], "sf-court-eviction-help")

    def test_job(self) -> None:
        result = build_demo_response("I need job training")
        self.assertEqual(result["resources"][0]["id"], "oewd-job-help")

    def test_unknown_need_uses_211(self) -> None:
        result = build_demo_response("I need help but do not know where to start")
        self.assertEqual(result["resources"][0]["id"], "211-bay-area")

    def test_immediate_danger(self) -> None:
        result = build_demo_response("There is an immediate medical emergency")
        self.assertEqual(result["urgency"], "immediate_safety_concern")
        self.assertEqual(result["resources"], [])


if __name__ == "__main__":
    unittest.main()
