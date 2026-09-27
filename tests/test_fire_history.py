"""Evidence-boundary and join checks for the real sparse history."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from engine.fire.history import build_audit, build_replay_scenario, run_history_scenarios


ROOT = Path(__file__).resolve().parents[1]


class HistoryAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = build_audit(ROOT / "reference/progress.csv", ROOT / "reference/mathacademy-xp-observations.json")

    def test_real_snapshot_coverage_and_stale_metadata(self):
        summary = self.audit["summary"]
        self.assertEqual(summary["activities"], 217)
        self.assertEqual(summary["observed_tasks"], 34)
        self.assertEqual(summary["observed_questions"], 308)
        self.assertEqual(summary["correct_questions"], 205)
        self.assertEqual(summary["observed_questions_with_task_topic_scope"], 70)
        self.assertEqual(summary["join_issue_count"], 0)
        self.assertFalse(summary["observation_snapshot_hash_matches"])
        self.assertEqual(summary["snapshot_row_count_delta"], 3)

    def test_unknown_state_stays_unknown(self):
        for activity in self.audit["activities"]:
            self.assertIsNone(activity["fire_outcome"])
            self.assertIsNone(activity["time_zone"])
            for question in activity["question_observations"] or []:
                self.assertIsNone(question["topic_id"])
                self.assertIsNone(question["knowledge_point_id"])
        self.assertEqual(self.audit["summary"]["verified_due_time_predictions"], 0)

    def test_xp_is_not_replay_outcome(self):
        scenario = build_replay_scenario(self.audit, outcome_policy="question_correct", clock_policy="observed_elapsed_hours")
        # This zero-XP review still contains three correct answers.
        results = [event["success"] for event in scenario["events"] if event["task_id"] == "13409092"]
        self.assertEqual(results, [True, True, False, True, False])
        self.assertEqual(len(scenario["events"]), 70)
        self.assertTrue(all(a["time"] <= b["time"] for a, b in zip(scenario["events"], scenario["events"][1:])))
        self.assertEqual(scenario["omitted_task_counts"], {"unobserved_task": 183, "unmapped_or_conflicting_task": 23})

    def test_aggregation_is_explicit_and_keeps_partial_review_distinct(self):
        scenario = build_replay_scenario(self.audit, outcome_policy="all_questions_correct", clock_policy="wall_days")
        self.assertEqual(len(scenario["events"]), 11)
        self.assertEqual(sum(event["success"] for event in scenario["events"]), 2)
        self.assertEqual(scenario["verified_production_predictions"], 0)
        with self.assertRaises(ValueError):
            build_replay_scenario(self.audit, outcome_policy="xp_positive", clock_policy="wall_days")
        with self.assertRaises(TypeError):
            build_replay_scenario(self.audit)

    def test_conflicting_join_cannot_emit_engine_event(self):
        altered = copy.deepcopy(self.audit)
        task = next(item for item in altered["activities"] if item["task_id"] == "13409092")
        task["join_issues"] = [{"field": "earned", "progress": 1, "observation": 0}]
        scenario = build_replay_scenario(altered, outcome_policy="question_correct", clock_policy="observed_elapsed_hours")
        self.assertEqual(len(scenario["events"]), 65)
        self.assertNotIn("13409092", {event["task_id"] for event in scenario["events"]})

    def test_duplicate_id_fails_instead_of_silently_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observations.json"
            data = json.loads((ROOT / "reference/mathacademy-xp-observations.json").read_text())
            data["tasks"].append(data["tasks"][0])
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Duplicate task IDs"):
                build_audit(ROOT / "reference/progress.csv", path)

    def test_mismatch_is_reported_without_changing_observation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observations.json"
            data = json.loads((ROOT / "reference/mathacademy-xp-observations.json").read_text())
            data["tasks"][0]["earned"] = 99
            path.write_text(json.dumps(data))
            audit = build_audit(ROOT / "reference/progress.csv", path)
            self.assertEqual(audit["summary"]["join_issue_count"], 1)
            task = next(item for item in audit["activities"] if item["task_id"] == data["tasks"][0]["task_id"])
            self.assertEqual(task["join_issues"][0]["observation"], 99)
            self.assertEqual(task["xp_earned"], 4)

    def test_replay_executes_evidence_under_alternative_assumptions(self):
        result = run_history_scenarios(self.audit)
        self.assertEqual(result["scenario_count"], 32)
        self.assertEqual(result["verified_production_predictions"], 0)
        self.assertEqual(set(result["implementation_hashes"]), {"core.py", "calibration.py", "history.py"})
        for run in result["scenarios"]:
            self.assertEqual(run["topic_count"], 8)
            self.assertEqual(len(run["observed_review_compatibility"]), 6)
            self.assertEqual(len(run["traces"]), run["event_count"])
            for trace in run["traces"]:
                # No fabricated graph may leak implicit credit into the history.
                self.assertEqual(len(trace["updates"]), 1)
                self.assertTrue(trace["updates"][0]["direct"])
        ranges = result["final_repetition_ranges_across_assumptions"]
        self.assertGreater(ranges["1042"]["maximum_repetitions"], ranges["1042"]["minimum_repetitions"])

    def test_memory_timestamp_interpretations_change_actual_replay(self):
        runs = run_history_scenarios(self.audit)["scenarios"]
        base_id = "question_correct:wall_days:r0:growth2"
        ordinary = next(item for item in runs if item["id"] == base_id)
        literal = next(item for item in runs if item["id"] == base_id + ":literal-add-before-decay")
        self.assertEqual(ordinary["event_count"], literal["event_count"])
        self.assertNotEqual(ordinary["final_states"]["893"]["due_at_days"], literal["final_states"]["893"]["due_at_days"])
        self.assertTrue(all(not item["is_verified_prediction"] for item in literal["observed_review_compatibility"]))

    def test_partial_clock_converts_events_and_interval_to_same_unit(self):
        result = run_history_scenarios(self.audit)
        run = next(item for item in result["scenarios"] if item["id"] == "question_correct:observed_elapsed_hours:r0:growth2")
        scenario = build_replay_scenario(self.audit, outcome_policy="question_correct", clock_policy="observed_elapsed_hours")
        self.assertAlmostEqual(run["policy"]["base_interval_days"] * 24, 1)
        for trace, event in zip(run["traces"], scenario["events"]):
            self.assertAlmostEqual(trace["at_days"] * 24, event["time"])
        # Unknown-topic questions consume sampled elapsed time but cannot emit
        # guessed topic events. Dropping their duration would falsify this check.
        first = scenario["events"][0]
        elapsed_before_first = 0
        for activity in self.audit["activities"]:
            for question in activity["question_observations"] or []:
                elapsed_before_first += question["elapsed_seconds"]
                if activity["task_id"] == first["task_id"]:
                    self.assertAlmostEqual(first["time"] * 3600, elapsed_before_first)
                    return
        self.fail("First replay event did not join to observed elapsed sequence")


if __name__ == "__main__":
    unittest.main()
