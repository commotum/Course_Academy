import copy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from find_candidates import check_generator_files, coverage, discover, ranked_candidates
from generator_priority import PRIORITY_POLICY, priority_key


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


def ranked_contexts(result):
    """Inspect comparator behavior even when admission withholds a build."""
    return sorted((kp for t in result["topics"] for kp in t["knowledge_points"]), key=priority_key)


def approved(t):
    for kp in t["knowledge_points"]:
        kp.update(has_generator=True, generator_usable=True,
                  generator_script="generators/ab/" + "ab" * 32 + "/generator.py")
    return t


class RankingTests(unittest.TestCase):
    def test_diagnostic_scores_remain_available(self):
        result = rank(topic(1, inventory(1)),
                      topic(2, inventory(4), groups=("target",)),
                      topic(3, stage="review", groups=("studied",)),
                      topic(4, stage="assessment", groups=("studied",)))
        self.assertEqual([(kp["topic_entity"], kp["score"]) for kp in ranked_contexts(result)],
                         [(1, 64300), (2, 61400), (3, 55500), (4, 41500)])

    def test_five_total_is_sufficient_and_advance_build_is_still_listed(self):
        result = rank(topic(1, inventory(5), groups=("target",)),
                      topic(2, inventory(4), groups=("target",)))
        rows = result["knowledge_points"]
        self.assertEqual([(r["topic_entity"], r["purpose"], r["score"]) for r in rows],
                         [(2, "lesson-shortage", 61400), (1, "advance-build", 400)])
        self.assertEqual(rows[1]["refill_deficits"], {"easy": 0, "moderate": 5, "hard": 5})

    def test_engine_topic_priority_precedes_kp_shortage_within_same_layer(self):
        a, b = topic(1, inventory(4)), topic(2, inventory(1))
        a.update(assignment_due="2000-01-01T00:00:00Z", engine_priority=1e12, activity_state="needed-now")
        self.assertEqual([r["topic_entity"] for r in rank(a, b)["knowledge_points"]], [1, 2])

    def test_membership_score_is_diagnostic_and_queue_and_target_share_relevance(self):
        a = topic(1, inventory(5), groups=("studied", "target", "queued", "target-prerequisite"))
        result = rank(a, topic(2, inventory(5)), topic(3, inventory(5), groups=("target",)))
        self.assertEqual([r["score"] for r in result["knowledge_points"]], [500, 300, 400])
        self.assertEqual([r["relevance_tier"] for r in result["knowledge_points"]], [1, 1, 1])

    def test_review_uses_topic_stock_while_lesson_uses_own_kp(self):
        review = topic(1, inventory(5), stage="review", groups=("studied",))
        review["knowledge_points"][0]["inventory"] = inventory()
        lesson = topic(2, inventory(5))
        lesson["knowledge_points"][0]["inventory"] = inventory()
        rows = ranked_contexts(rank(review, lesson))
        self.assertEqual([(r["topic_entity"], r["score"]) for r in rows], [(2, 65300), (1, 500)])
        self.assertEqual(rows[1]["inventory_scope"], "topic")
        self.assertEqual(rows[1]["kp_available_total"], 0)

    def test_assessment_demands_use_oldest_first_study(self):
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

    def test_selected_review_precedes_speculative_lesson_even_with_smaller_score(self):
        selected = topic(1, inventory(4), stage="review", groups=("queued",))
        future = topic(2, groups=("studied-or-queued-descendant",))
        rows = ranked_contexts(rank(future, selected))
        self.assertEqual([r["topic_entity"] for r in rows], [1, 2])
        self.assertLess(rows[0]["score"], rows[1]["score"])

    def test_direct_selection_precedes_earlier_prerequisite_with_larger_shortage(self):
        direct = topic(1, inventory(4))
        direct.update(topic_layer=38, selected_support_count=1)
        prerequisite = topic(2, groups=("selected-prerequisite",))
        prerequisite.update(topic_layer=0, selected_support_count=100, engine_priority=1e12)
        rows = ranked_contexts(rank(prerequisite, direct))
        self.assertEqual([r["topic_entity"] for r in rows], [1, 2])
        self.assertEqual([r["relevance_tier"] for r in rows], [1, 2])
        self.assertEqual([r["shortage"] for r in rows], [1, 5])

    def test_direct_review_precedes_prerequisite_lesson(self):
        direct = topic(1, inventory(4), stage="review", groups=("target",))
        prerequisite = topic(2, groups=("selected-prerequisite",))
        rows = ranked_contexts(rank(prerequisite, direct))
        self.assertEqual([(r["topic_entity"], r["purpose"]) for r in rows],
                         [(1, "review-shortage"), (2, "lesson-shortage")])

    def test_direct_advance_work_precedes_prerequisite_lesson(self):
        direct = topic(1, inventory(5))
        prerequisite = topic(2, groups=("selected-prerequisite",))
        rows = ranked_contexts(rank(prerequisite, direct))
        self.assertEqual([(r["topic_entity"], r["purpose"]) for r in rows],
                         [(1, "advance-build"), (2, "lesson-shortage")])

    def test_direct_membership_wins_when_topic_is_also_a_prerequisite(self):
        for direct in ("queued", "target"):
            with self.subTest(direct=direct):
                t = topic(1, groups=("studied", "selected-prerequisite", direct))
                row, = rank(t)["knowledge_points"]
                self.assertEqual((row["relevance_tier"], row["baseline_relevance_tier"]), (1, 1))

    def test_current_and_speculative_fallback_tiers_remain_distinct(self):
        current = topic(1, stage="review", groups=("current-need",))
        speculative = topic(2, groups=("studied-or-queued-descendant",))
        speculative["activity_demands"] = [{"activity_type": "lesson"}]
        rows = rank(speculative, current)["knowledge_points"]
        self.assertEqual([r["relevance_tier"] for r in rows], [3, 4])
        self.assertTrue(all(r["relevance_tier"] == 4 for r in rows[1]["priority_reasons"]))
        self.assertEqual(priority_key(rows[1])[0], 4)

    def test_immediate_demand_does_not_promote_other_purposes_on_the_topic(self):
        selected = topic(1, stage="review")
        selected.update(relevance_tier=1, activity_demands=[
            {"activity_type": "lesson", "relevance_tier": 1},
            {"activity_type": "review", "relevance_tier": 0}])
        row, = rank(selected)["knowledge_points"]
        self.assertEqual((row["purpose"], row["relevance_tier"], row["baseline_relevance_tier"]),
                         ("review-shortage", 0, 1))
        reasons = {r["purpose"]: r for r in row["priority_reasons"]}
        self.assertEqual(reasons["lesson-shortage"]["relevance_tier"], 1)
        self.assertEqual(reasons["advance-build"]["relevance_tier"], 1)

    def test_ready_active_bank_has_no_immediate_shortage_priority(self):
        ready = topic(1, inventory(5), stage="review", groups=("immediate",))
        ready.update(relevance_tier=3, activity_demands=[
            {"activity_type": "review", "relevance_tier": 0}])
        row, = rank(ready)["knowledge_points"]
        self.assertEqual((row["purpose"], row["relevance_tier"]), ("advance-build", 3))

    def test_earlier_lesson_finishes_all_kps_before_larger_later_shortages(self):
        early = topic(1, inventory(4))
        early.update(topic_layer=10, selected_support_count=1)
        early["knowledge_points"].append({"db/id": 11, "inventory": inventory(2), "has_generator": False})
        late = topic(2)
        late.update(topic_layer=11, selected_support_count=100, engine_priority=1e12)
        rows = rank(late, early)["knowledge_points"]
        self.assertEqual([r["db/id"] for r in rows], [11, 10, 20])
        self.assertEqual([r["shortage"] for r in rows], [3, 1, 5])

    def test_more_distinct_selected_support_breaks_layer_tie(self):
        a, b = topic(1), topic(2, inventory(4))
        a.update(topic_layer=10, selected_support_count=2)
        b.update(topic_layer=10, selected_support_count=3)
        self.assertEqual([r["topic_entity"] for r in rank(a, b)["knowledge_points"]], [2, 1])

    def test_review_urgency_uses_due_date_not_prerequisite_layer(self):
        a, b = topic(1, stage="review"), topic(2, stage="review")
        a.update(topic_layer=1, selected_support_count=100, review_due_at="2026-10-15T00:00:00Z")
        b.update(topic_layer=100, selected_support_count=1, review_due_at="2026-10-01T00:00:00Z")
        self.assertEqual([r["topic_entity"] for r in rank(a, b)["knowledge_points"]], [2, 1])

    def test_multiple_demands_keep_per_kp_lesson_and_pooled_review_stock_separate(self):
        t = topic(1, inventory(5), stage="review")
        t.update(completed_local_lesson=False, relevance_tier=1, activity_demands=[
            {"activity_type": "lesson", "relevance_tier": 1},
            {"activity_type": "review", "relevance_tier": 0}])
        t["knowledge_points"][0]["inventory"] = inventory(2)
        row, = rank(t)["knowledge_points"]
        self.assertEqual((row["purpose"], row["shortage"], row["available_total"], row["inventory_scope"]),
                         ("lesson-shortage", 3, 2, "knowledge-point"))
        self.assertEqual(set(row["inventory_scopes"]), {"topic", "knowledge-point"})
        self.assertNotIn("review-shortage", [r["purpose"] for r in row["priority_reasons"]])

    def test_selected_imported_mastery_without_local_lesson_retains_lesson_demand(self):
        t = topic(1, inventory(5), stage="review")
        t["completed_local_lesson"] = False
        t["knowledge_points"][0]["inventory"] = inventory(2)
        row, = rank(t)["knowledge_points"]
        self.assertEqual((row["purpose"], row["shortage"]), ("lesson-shortage", 3))

    def test_explicit_re_study_can_demand_a_lesson_after_local_completion(self):
        t = topic(1, stage="review")
        t.update(completed_local_lesson=True, activity_demands=[
            {"activity_type": "lesson", "relevance_tier": 0}])
        row, = rank(t)["knowledge_points"]
        self.assertEqual((row["purpose"], row["relevance_tier"]), ("lesson-shortage", 0))

    def test_shared_kp_reasons_preserve_each_topic_ranking_context(self):
        a, b = topic(1, inventory(4)), topic(2, stage="review")
        a.update(topic_layer=10, selected_support_count=3)
        b.update(topic_layer=20, selected_support_count=1, activity_demands=[
            {"activity_type": "review", "relevance_tier": 0}])
        b["knowledge_points"][0]["db/id"] = 10
        row, = rank(a, b)["knowledge_points"]
        self.assertEqual((row["topic_entity"], row["purpose"]), (2, "review-shortage"))
        reasons = {r["purpose"]: r for r in row["priority_reasons"] if r["purpose"] != "advance-build"}
        self.assertEqual((reasons["lesson-shortage"]["topic_entity"], reasons["lesson-shortage"]["topic_layer"]), (1, 10))
        self.assertEqual((reasons["review-shortage"]["topic_entity"], reasons["review-shortage"]["topic_layer"]), (2, 20))

    def test_finder_and_worker_aliases_have_identical_keys(self):
        row, = rank(topic(1))["knowledge_points"]
        request = {**row, "topic": row["topic_entity"], "knowledgePoint": row["db/id"]}
        del request["topic_entity"], request["db/id"]
        self.assertEqual(priority_key(row), priority_key(request))
        self.assertEqual(row["priority_policy"], PRIORITY_POLICY)

    def test_legacy_jobs_keep_relative_order_until_refreshed(self):
        old = [{"topic": 1, "knowledgePoint": 10, "score": 65000},
               {"topic": 2, "knowledgePoint": 20, "score": 40000}]
        current, = rank(topic(3))["knowledge_points"]
        self.assertEqual(sorted([old[1], current, old[0]], key=priority_key), [current, *old])
        self.assertEqual(priority_key(old[0])[0], 5)


class SelectionGateTests(unittest.TestCase):
    def test_closed_gate_withholds_every_nonselected_build_including_immediate(self):
        direct = topic(1, inventory(4))
        prerequisite = topic(2, groups=("selected-prerequisite",))
        immediate = topic(3, groups=("immediate",))
        immediate["activity_demands"] = [{"activity_type": "lesson", "relevance_tier": 0}]
        result = rank(prerequisite, immediate, direct)
        self.assertFalse(result["selection_gate"]["open"])
        self.assertEqual([kp["db/id"] for kp in result["knowledge_points"]], [10])
        outside = [kp for kp in ranked_contexts(result) if kp["db/id"] != 10]
        self.assertTrue(all(not kp["build_required"] for kp in outside))
        self.assertTrue(all(kp["build_exclusion_reason"] == "selected-inventory-incomplete" for kp in outside))

    def test_a_single_missing_band_keeps_gate_closed_even_when_lesson_stock_is_ready(self):
        t = approved(topic(1, inventory(5, 4, 5)))
        gate = rank(t)["selection_gate"]
        self.assertEqual(gate["selected_knowledge_points"], [10])
        self.assertEqual(gate["missing_generators"], [])
        self.assertEqual(gate["understocked_knowledge_points"], [10])
        self.assertFalse(gate["open"])
        self.assertEqual(gate["required_per_band"], 5)

    def test_a_fully_stocked_bank_still_needs_an_approved_generator(self):
        gate = rank(topic(1, inventory(5, 5, 5)))["selection_gate"]
        self.assertEqual(gate["missing_generators"], [10])
        self.assertEqual(gate["understocked_knowledge_points"], [])
        self.assertFalse(gate["open"])

    def test_usable_legacy_script_does_not_open_gate_before_migration(self):
        t = topic(1, inventory(5, 5, 5), registered=True)
        t["knowledge_points"][0].update(generator_usable=True, generator_script="generate/legacy.py")
        gate = rank(t)["selection_gate"]
        self.assertEqual(gate["missing_generators"], [10])
        self.assertFalse(gate["open"])

    def test_all_selected_kps_ready_opens_gate_and_deduplicates_shared_membership(self):
        a = approved(topic(1, inventory(5, 5, 5), groups=("queued", "target")))
        b = approved(topic(2, inventory(5, 5, 5), groups=("target",)))
        b["knowledge_points"][0]["db/id"] = 10
        prerequisite = topic(3, groups=("selected-prerequisite",))
        result = rank(prerequisite, a, b)
        gate = result["selection_gate"]
        self.assertTrue(gate["open"])
        self.assertEqual(gate["selected_knowledge_points"], [10])
        self.assertEqual((gate["selected_topic_count"], gate["selected_knowledge_point_count"]), (2, 1))
        self.assertEqual([kp["db/id"] for kp in result["knowledge_points"]], [30])

    def test_shared_selected_kp_is_admitted_from_its_strongest_context(self):
        a = topic(1)
        b = topic(2, groups=("immediate",))
        b["knowledge_points"][0]["db/id"] = 10
        b["activity_demands"] = [{"activity_type": "review", "relevance_tier": 0}]
        result = rank(a, b)
        row, = result["knowledge_points"]
        self.assertFalse(result["selection_gate"]["open"])
        self.assertEqual((row["db/id"], row["topic_entity"], row["relevance_tier"]), (10, 2, 0))
        self.assertEqual(result["selection_gate"]["selected_knowledge_points"], [10])

    def test_no_direct_selection_opens_gate(self):
        result = rank(topic(1, groups=("studied-or-queued-descendant",)))
        self.assertTrue(result["selection_gate"]["open"])
        self.assertEqual(result["selection_gate"]["selected_knowledge_points"], [])
        self.assertEqual(len(result["knowledge_points"]), 1)

    def discover_snapshots(self, *snapshots, include_registered=False):
        responses = [SimpleNamespace(stdout=json.dumps(snapshot)) for snapshot in snapshots]
        with patch("find_candidates.subprocess.run", side_effect=responses) as run, \
                patch("find_candidates.check_generator_files"):
            result = discover("math", "learner", {"EDB_MATH_ROOT": "/tmp/math"}, binary="finder",
                              include_registered=include_registered)
        return result, [json.loads(call.kwargs["input"]) for call in run.call_args_list]

    def test_discovery_stops_after_selected_only_capture_when_gate_closed(self):
        result, requests = self.discover_snapshots({"basis": 1, "topics": [topic(1)]})
        self.assertFalse(result["selection_gate"]["open"])
        self.assertEqual([request["selected_only"] for request in requests], [True])

    def test_closed_discovery_preserves_outside_registered_refills_without_expansion(self):
        from inventory_jobs import ranked_requests
        selected = topic(1)
        outside = approved(topic(2, inventory(4, 5, 5), groups=()))
        result, requests = self.discover_snapshots(
            {"basis": 1, "topics": [selected, outside]}, include_registered=True)
        self.assertFalse(result["selection_gate"]["open"])
        self.assertEqual(result["selection_gate"]["selected_knowledge_points"], [10])
        self.assertEqual([request["selected_only"] for request in requests], [True])
        self.assertTrue(requests[0]["include_registered"])
        jobs = ranked_requests(result)
        self.assertEqual([(job["knowledgePoint"], job["jobKind"], job["missing"])
                          for job in jobs], [(10, "build", 5), (20, "refill", 1)])

    def test_discovery_expands_only_after_all_selected_banks_are_ready(self):
        selected = approved(topic(1, inventory(5, 5, 5)))
        result, requests = self.discover_snapshots(
            {"basis": 1, "topics": [selected]},
            {"basis": 2, "topics": [selected, topic(2, groups=("selected-prerequisite",))]})
        self.assertTrue(result["selection_gate"]["open"])
        self.assertEqual([request["selected_only"] for request in requests], [True, False])
        self.assertEqual([kp["db/id"] for kp in result["knowledge_points"]], [20])
        self.assertEqual(result["basis"], 2)

    def test_full_capture_recloses_gate_after_inventory_or_selection_changes(self):
        selected = approved(topic(1, inventory(5, 5, 5)))
        depleted = approved(topic(1, inventory(5, 5, 4)))
        for changed in ([depleted], [selected, topic(3, groups=("target",))]):
            with self.subTest(selected_topics=[t["db/id"] for t in changed]):
                result, requests = self.discover_snapshots(
                    {"basis": 1, "topics": [selected]},
                    {"basis": 2, "topics": [*changed, topic(2, groups=("selected-prerequisite",))]})
                self.assertFalse(result["selection_gate"]["open"])
                self.assertEqual([request["selected_only"] for request in requests], [True, False])
                self.assertNotIn(20, [kp["db/id"] for kp in result["knowledge_points"]])


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

    def test_reviewed_topic_still_supplies_variety_while_awaiting_another_review(self):
        stocked = topic(1, inventory(hard=5, supported=["hard"]), stage="review", groups=("studied",), registered=True)
        stocked["reviewed"] = True
        candidate = topic(2, inventory(easy=1, supported=["easy", "hard"]), stage="assessment", groups=("studied",))
        result = rank(stocked, candidate)
        self.assertEqual(result["assessment_coverage"]["available"]["hard"], 1)
        self.assertEqual(result["knowledge_points"][0]["purpose"], "advance-build")

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
