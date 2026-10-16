import copy
from pathlib import Path
import tempfile
import unittest

from find_candidates import check_generator_files, coverage, ranked_candidates


def inventory(easy=0, moderate=0, hard=0, *, supported=None, unrated=0):
    return {"available": dict(zip(("easy", "moderate", "hard"), (easy, moderate, hard))),
            "available_total": easy + moderate + hard + unrated,
            "rated_total": easy + moderate + hard, "unrated_total": unrated,
            "supported_difficulties": supported if supported is not None else ["easy", "moderate", "hard"]}


def topic(eid, counts=None, *, stage="lesson", groups=("queued",), registered=False):
    counts = counts if counts is not None else inventory()
    return {"db/id": eid, "topic/title": str(eid), "urgency_groups": list(groups),
            "next_activity": stage, "studied": stage != "lesson", "reviewed": stage == "assessment",
            "first_studied_at": None, "waiting_since": None,
            "activity_state": "queued", "engine_priority": 0, "assignment_due": None,
            "triggers": [{"activity_type": stage}], "topic_inventory": counts,
            "knowledge_points": [{"db/id": eid * 10, "inventory": counts,
                                  "has_generator": registered}]}


def rank(*topics):
    return ranked_candidates({"basis": 123, "topics": list(topics)})


class RankingTests(unittest.TestCase):
    def test_proposed_scores_and_order(self):
        result = rank(topic(1, inventory(1)),
                      topic(2, inventory(4), groups=("target",)),
                      topic(3, stage="review", groups=("studied",)),
                      topic(4, stage="assessment", groups=("studied",)))
        self.assertEqual([(kp["topic_entity"], kp["score"]) for kp in result["knowledge_points"]],
                         [(1, 64300), (2, 61400), (3, 55500), (4, 41500)])

    def test_five_total_is_sufficient_and_advance_build_is_still_listed(self):
        result = rank(topic(1, inventory(5), groups=("target",)),
                      topic(2, inventory(4), groups=("target",)))
        rows = result["knowledge_points"]
        self.assertEqual([(r["topic_entity"], r["purpose"], r["score"]) for r in rows],
                         [(2, "lesson-shortage", 61400), (1, "advance-build", 400)])
        self.assertEqual(rows[1]["refill_deficits"], {"easy": 0, "moderate": 5, "hard": 5})

    def test_legacy_priorities_and_deadlines_do_not_override_new_score(self):
        a, b = topic(1, inventory(4)), topic(2, inventory(1))
        a.update(assignment_due="2000-01-01T00:00:00Z", engine_priority=1e12, activity_state="needed-now")
        self.assertEqual([r["topic_entity"] for r in rank(a, b)["knowledge_points"]], [2, 1])

    def test_urgency_is_highest_membership_and_target_precedes_queue(self):
        a = topic(1, inventory(5), groups=("studied", "target", "queued", "target-prerequisite"))
        result = rank(a, topic(2, inventory(5), groups=("target",)), topic(3, inventory(5)))
        self.assertEqual([r["score"] for r in result["knowledge_points"]], [500, 400, 300])

    def test_review_uses_topic_stock_while_lesson_uses_own_kp(self):
        review = topic(1, inventory(5), stage="review", groups=("studied",))
        review["knowledge_points"][0]["inventory"] = inventory()
        lesson = topic(2, inventory(5))
        lesson["knowledge_points"][0]["inventory"] = inventory()
        rows = rank(review, lesson)["knowledge_points"]
        self.assertEqual([(r["topic_entity"], r["score"]) for r in rows], [(2, 65300), (1, 500)])
        self.assertEqual(rows[1]["inventory_scope"], "topic")
        self.assertEqual(rows[1]["kp_available_total"], 0)

    def test_assessment_stage_is_exclusive_and_oldest_first_study_breaks_ties(self):
        a, b, c = [topic(n, stage="assessment", groups=("studied",)) for n in (1, 2, 3)]
        a["first_studied_at"] = "2026-10-10T00:00:00Z"
        b["first_studied_at"] = "2026-10-01T00:00:00Z"
        a["waiting_since"] = "2000-01-01T00:00:00Z"
        rows = rank(c, a, b)["knowledge_points"]
        self.assertEqual([r["topic_entity"] for r in rows], [2, 1, 3])
        self.assertTrue(all(r["purpose"] == "assessment-shortage" and r["score"] == 41500 for r in rows))

    def test_unrated_questions_count_for_lesson_and_review_but_not_assessment(self):
        rows = rank(*(topic(n, inventory(unrated=5), stage=stage, groups=("studied",))
                      for n, stage in enumerate(("lesson", "review", "assessment"), 1)))["knowledge_points"]
        self.assertEqual(rows[0]["topic_entity"], 3)
        self.assertEqual(rows[0]["purpose"], "assessment-shortage")
        self.assertEqual([r["purpose"] for r in rows[1:]], ["advance-build", "advance-build"])

    def test_ineligible_topics_and_usable_generators_are_excluded_from_flat_build_queue(self):
        result = rank(topic(1, groups=()), topic(2, registered=True), topic(3))
        self.assertEqual([r["db/id"] for r in result["knowledge_points"]], [30])
        self.assertEqual(len(result["topics"]), 3)
        nested = {t["db/id"]: t["knowledge_points"][0] for t in result["topics"]}
        self.assertEqual(nested[1]["build_exclusion_reason"], "outside-urgency-groups")
        self.assertEqual(nested[2]["build_exclusion_reason"], "usable-generator-registered")
        self.assertIsNone(nested[2]["rank"])

    def test_shared_kp_is_one_build_using_strongest_topic_reason(self):
        a, b = topic(1, inventory(1)), topic(2, inventory(5), stage="review", groups=("studied",))
        b["knowledge_points"][0] = copy.deepcopy(a["knowledge_points"][0])
        result = rank(b, a)
        self.assertEqual(len(result["knowledge_points"]), 1)
        row = result["knowledge_points"][0]
        self.assertEqual((row["score"], row["candidate_topics"]), (64300, [1, 2]))
        self.assertTrue(all(t["knowledge_points"][0]["rank"] == 1 for t in result["topics"]))

    def test_registered_paths_are_checked_without_running_them(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "generator.py").write_text("raise AssertionError('Must never run during discovery')\n")
            a, b = topic(1, registered=True), topic(2, registered=True)
            a["knowledge_points"][0]["generator_script"] = "generator.py"
            b["knowledge_points"][0]["generator_script"] = "missing.py"
            result = {"topics": [a, b]}
            check_generator_files(result, root / "math", root)
            row, = ranked_candidates(result)["knowledge_points"]
            self.assertEqual(row["db/id"], 20)
            self.assertEqual(row["build_action"], "repair-generator")
            self.assertTrue(row["generator_error"])

    def test_ties_use_waiting_date_then_stable_ids(self):
        a, b = topic(1, inventory(5)), topic(2, inventory(5))
        b["waiting_since"] = "2026-10-01T00:00:00Z"
        self.assertEqual([r["db/id"] for r in rank(a, b)["knowledge_points"]], [20, 10])
        a["waiting_since"] = b["waiting_since"]
        self.assertEqual([r["db/id"] for r in rank(b, a)["knowledge_points"]], [10, 20])


class VarietyTests(unittest.TestCase):
    def test_one_topic_cannot_fill_multiple_slots_and_flexible_topics_can_move(self):
        self.assertEqual(coverage({1: {"easy", "moderate", "hard"}}), (1, 0, 0))
        self.assertEqual(coverage({1: {"hard", "moderate"}, 2: {"hard"}}), (1, 1, 0))

    def test_existing_generators_count_toward_global_coverage(self):
        stocked = [topic(n, inventory(**{band: 1}), stage="assessment", groups=("studied",), registered=True)
                   for n, band in enumerate(("hard", "moderate", "moderate", "easy", "easy", "easy"), 1)]
        candidate = topic(7, inventory(1), stage="assessment", groups=("studied",))
        result = rank(*stocked, candidate)
        self.assertEqual(result["assessment_coverage"]["available"], {"hard": 1, "moderate": 2, "easy": 3})
        self.assertEqual(result["knowledge_points"][0]["purpose"], "advance-build")
        self.assertEqual(len(result["knowledge_points"]), 1)

    def test_only_a_useful_observed_band_receives_variety_points(self):
        hard = topic(1, inventory(hard=1), stage="assessment", groups=("studied",), registered=True)
        useful = topic(2, inventory(easy=1, supported=["easy", "moderate"]), stage="assessment", groups=("studied",))
        unknown = topic(3, inventory(easy=1, supported=["easy"]), stage="assessment", groups=("studied",))
        rows = rank(hard, useful, unknown)["knowledge_points"]
        self.assertEqual((rows[0]["purpose"], rows[0]["generated_band"], rows[0]["score"]),
                         ("moderate-variety", "moderate", 22500))
        self.assertEqual(rows[1]["purpose"], "advance-build")

    def test_existing_band_or_more_copies_cannot_fake_distinct_topic_variety(self):
        t = topic(1, inventory(20, 20, 20), stage="assessment", groups=("studied",))
        result = rank(t)
        self.assertEqual(result["assessment_coverage"]["missing"], {"hard": 0, "moderate": 2, "easy": 3})
        self.assertEqual(result["knowledge_points"][0]["purpose"], "advance-build")

    def test_new_hard_capability_can_free_another_topic_for_moderate(self):
        flexible = topic(1, inventory(moderate=1, hard=1), stage="assessment", groups=("studied",), registered=True)
        candidate = topic(2, inventory(easy=1, supported=["easy", "hard"]), stage="assessment", groups=("studied",))
        row, = rank(flexible, candidate)["knowledge_points"]
        self.assertEqual((row["purpose"], row["generated_band"]), ("moderate-variety", "hard"))

    def test_next_activity_depletion_precedes_variety(self):
        t = topic(1, inventory(supported=["hard"]), stage="assessment", groups=("studied",))
        row, = rank(t)["knowledge_points"]
        self.assertEqual(row["purpose"], "assessment-shortage")
        self.assertIn("hard-variety", [r["purpose"] for r in row["priority_reasons"]])

    def test_refresh_removes_obsolete_variety_instructions(self):
        t = topic(1, inventory(easy=1, supported=["easy", "hard"]), stage="assessment", groups=("studied",))
        result = rank(t)
        self.assertEqual(result["knowledge_points"][0]["generated_band"], "hard")
        t["topic_inventory"] = inventory(easy=1, hard=1)
        t["knowledge_points"][0]["inventory"] = t["topic_inventory"]
        refreshed = ranked_candidates(result)["knowledge_points"][0]
        self.assertEqual(refreshed["purpose"], "advance-build")
        self.assertNotIn("generated_band", refreshed)
        self.assertNotIn("coverage_after", refreshed)


if __name__ == "__main__":
    unittest.main()
