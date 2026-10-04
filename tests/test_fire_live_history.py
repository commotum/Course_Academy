import copy
import json
from pathlib import Path
import tempfile
import unittest

from engine.fire.live_history import build_live_audit, elapsed_seconds, replay_ability, _catalog_check


ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "reference/fire-live-observations-2026-09-26.json"
PROGRESS = ROOT / "reference/progress.csv"
PRIOR = ROOT / "reference/mathacademy-xp-observations.json"


class LiveHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = build_live_audit(CAPTURE, PROGRESS, PRIOR)

    def test_browser_checksums_and_union_occurrences(self):
        summary = self.audit["summary"]
        self.assertEqual(summary["browser_task_checksums_verified"], 9)
        self.assertEqual(summary["captured_questions"], 162)
        self.assertEqual(summary["prior_question_features_agree"], 74)
        self.assertEqual(summary["source_conflict_count"], 0)
        self.assertEqual(summary["union_question_occurrences"], 396)
        self.assertEqual(summary["union_observed_task_ids"], 39)
        self.assertEqual(summary["union_progress_and_live_task_ids"], 220)
        self.assertEqual(summary["additional_prior_occurrences_with_task_topic_scope_only"], 67)
        self.assertTrue(self.audit["graph_snapshot_audit"]["checksum_verified"])

    def test_tampered_capture_fails_browser_transcription_check(self):
        data = json.loads(CAPTURE.read_text())
        data["tasks"][0]["questions"][0]["result_label"] = "Incorrect"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                build_live_audit(path, PROGRESS, PRIOR)

    def test_prior_disagreement_is_preserved_as_a_conflict(self):
        data = json.loads(PRIOR.read_text())
        old = next(task for task in data["tasks"] if task["task_id"] == "13553418")
        old["questions"][0]["elapsed_seconds"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prior.json"
            path.write_text(json.dumps(data))
            audit = build_live_audit(CAPTURE, PROGRESS, path)
        conflict = audit["source_conflicts"][0]
        self.assertEqual(conflict["field"], "elapsed_seconds")
        self.assertEqual((conflict["previous"], conflict["live"]), (167, 166))

    def test_no_answer_content_is_not_replaced_by_incorrect_result_label(self):
        task = next(task for task in self.audit["tasks"] if task["task_id"] == "12563189")
        incorrect = [q for q in task["questions"] if q["correct"] is False]
        self.assertEqual(len(incorrect), 13)
        for question in incorrect:
            self.assertEqual(question["prior_observation"]["answer_state"], "no_answer")
            self.assertEqual(question["result_label"], "Incorrect")
            self.assertIsNone(question["answer_state"])
            self.assertFalse(question["prior_answer_state_reobserved"])

    def test_reused_questions_keep_distinct_occurrences(self):
        repeated = self.audit["repeated_question_ids_across_tasks"]
        self.assertEqual(set(repeated), {"79870", "112044"})
        for occurrences in repeated.values():
            self.assertEqual(len({item["occurrence_id"] for item in occurrences}), 2)
            self.assertEqual(len({item["task_id"] for item in occurrences}), 2)

    def test_diagnostics_are_excluded_from_both_ability_channels(self):
        replay = self.audit["ability_channel_replay"]
        self.assertEqual(replay["channel_answer_counts"], {"assessment": 18, "practice": 18})
        self.assertEqual(replay["omitted_answer_counts"], {"diagnostic": 126})
        self.assertEqual(replay["global_estimate"]["assessment_mass"], 18)
        self.assertEqual(replay["global_estimate"]["practice_mass"], 18)
        self.assertEqual(replay["retention_events_created"], 0)
        self.assertEqual(len(replay["diagnostic_evidence_separate"]), 126)

    def test_unrecognized_outcome_is_not_false(self):
        tasks = copy.deepcopy(self.audit["tasks"])
        review = next(task for task in tasks if task["kind"] == "review")
        review["questions"][0]["correct"] = None
        replay = replay_ability(tasks)
        self.assertEqual(replay["channel_answer_counts"]["practice"], 17)
        self.assertEqual(replay["omitted_answer_counts"]["unrecognized_result_label"], 1)

    def test_failed_quiz_topics_reviewed_but_not_all_retested(self):
        comparison = self.audit["quiz4_comparison"]
        self.assertEqual(comparison["incorrect_topics"], ["88", "161", "1610"])
        self.assertEqual(comparison["topics_only_in_first_quiz"], ["161", "436"])
        self.assertEqual(comparison["question_ids_shared_between_quizzes"], [])
        topic161 = next(item for item in comparison["per_incorrect_topic"] if item["topic_id"] == "161")
        self.assertEqual(len(topic161["intervening_reviews"]), 1)
        self.assertEqual(topic161["later_quiz_occurrences"], [])
        self.assertFalse(comparison["causal_scheduler_rule_verified"])

    def test_content_id_join_resolves_distinct_step_namespace(self):
        catalogs = {"topics": {"161": "Rules"}, "steps": {"5085": [{"topic-id": "999"}]}, "questions": {"1806": [{"topic-id": "161", "step-id": "18562"}]}, "example_steps": {("161", "5085"): ["18562"]}}
        check = _catalog_check({"topic_id": "161", "step_anchor": "5085", "question_id": "1806"}, catalogs)
        self.assertTrue(check["anchor_collides_with_other_topic_step"])
        self.assertEqual(check["resolved_catalog_step_id"], "18562")
        self.assertTrue(check["question_matches_resolved_example_step"])
        catalogs["example_steps"][("161", "5085")].append("9999")
        self.assertIsNone(_catalog_check({"topic_id": "161", "step_anchor": "5085", "question_id": "1806"}, catalogs)["resolved_catalog_step_id"])

    def test_retained_catalog_validation_recovers_all_example_anchors(self):
        audit = json.loads((ROOT / "engine/fire/fixtures/live-history-audit.json").read_text())
        self.assertEqual(audit["summary"]["unambiguous_content_to_step_joins"], 162)
        self.assertEqual(audit["summary"]["known_questions_matching_resolved_example_step"], 6)
        self.assertEqual(audit["summary"]["catalog_topic_anchor_step_matches"], 0)

    def test_elapsed_label_does_not_accept_invalid_seconds(self):
        self.assertEqual(elapsed_seconds("Elapsed: 3:59"), 239)
        with self.assertRaises(ValueError):
            elapsed_seconds("Elapsed: 3:99")


if __name__ == "__main__":
    unittest.main()
