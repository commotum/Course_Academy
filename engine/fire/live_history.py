"""Audit authorized, saved completed-task DOM observations without live access.

Question outcomes can update an explicitly chosen ability estimator. They never
become inferred task passes, diagnostic placement, or retention credit here.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import asdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from .calibration import AccuracyEstimate


CHANNELS = {"assessment": "assessment", "review": "practice", "lesson": "practice", "multistep": "practice", "diagnostic": None, "supplemental diagnostic": None}
CHECKSUM_ENCODING = "FNV-1a32 over JavaScript UTF-16 code units of compact JSON.stringify-compatible arrays; task rows are [question_dom_id,topic_step_href,difficulty_label,displayed_created,displayed_elapsed,result_label], preserving occurrence order; graph rows are [topic_id,ellipse_fill], sorted lexically by the digit-only string topic ID. No ASCII escaping. Checksums detect transcription differences, not authenticity."


def _source(path):
    path = Path(path)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _csv(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _unique(records, key, name):
    result = {}
    for row in records:
        if row[key] in result:
            raise ValueError(f"Duplicate {name} ID {row[key]}")
        result[row[key]] = row
    return result


def elapsed_seconds(label):
    match = re.fullmatch(r"Elapsed: (\d+):([0-5]\d)", label)
    if not match:
        raise ValueError(f"Unrecognized elapsed label: {label!r}")
    return 60 * int(match[1]) + int(match[2])


def fnv1a32_json(value):
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-16-le", errors="surrogatepass")
    result = 2166136261
    for index in range(0, len(encoded), 2):
        result = ((result ^ (encoded[index] + 256 * encoded[index + 1])) * 16777619) & 0xFFFFFFFF
    return f"{result:08x}"


def _task_checksum(task):
    fields = ("question_dom_id", "topic_step_href", "difficulty_label", "displayed_created", "displayed_elapsed", "result_label")
    actual = fnv1a32_json([[question[field] for field in fields] for question in task["questions"]])
    expected = task.get("browser_rows_fnv1a32")
    if expected is not None and actual != expected:
        raise ValueError(f"Browser checksum mismatch for task {task['task_id']}: {actual} != {expected}")
    return {"expected": expected, "calculated": actual, "verified": None if expected is None else True}


def _completed_local(task):
    value = datetime.strptime(task["date"] + " " + task["displayed_completed"], "%Y-%m-%d Completed @ %I:%M %p")
    return value.strftime("%Y-%m-%d %H:%M")


def _catalogs(root, topic_ids=()):
    if root is None:
        return None
    root = Path(root)
    files = {"topics": root / "Topics.csv", "steps": root / "Lesson-Data/Steps.csv", "questions": root / "Lesson-Data/Questions.csv"}
    topics = {row["topic-id"]: row["topic-name"] for row in _csv(files["topics"])}
    steps, questions = defaultdict(list), defaultdict(list)
    for row in _csv(files["steps"]):
        steps[row["step-id"]].append(row)
    for row in _csv(files["questions"]):
        questions[row["question-id"]].append(row)
    examples = defaultdict(list)
    content_sources = {}
    for topic_id in sorted(set(topic_ids), key=int):
        path = root / "Lessons" / topic_id / "Source" / (topic_id + ".json")
        if not path.is_file():
            continue
        data = json.loads(path.read_text())
        if str(data.get("topic_id")) != topic_id:
            raise ValueError(f"Catalog content topic identity mismatch in {path}")
        content_sources[topic_id] = _source(path)
        for item in data["lesson"]["items"]:
            if item.get("item_type") == "step" and item.get("step_type") == "example" and item.get("content_id") is not None:
                examples[(topic_id, str(item["content_id"]))].append(str(item["step_id"]))
    return {"sources": {**{key: _source(path) for key, path in files.items()}, "topic_content_snapshots": content_sources}, "topics": topics, "steps": steps, "questions": questions, "example_steps": examples}


def _catalog_check(question, catalogs):
    if catalogs is None:
        return None
    topic, anchor, qid = question["topic_id"], question["step_anchor"], question["question_id"]
    steps = catalogs["steps"].get(anchor, [])
    records = catalogs["questions"].get(qid, [])
    resolved_steps = sorted(set(catalogs["example_steps"].get((topic, anchor), [])), key=int)
    return {
        "topic_exists": topic in catalogs["topics"], "topic_name": catalogs["topics"].get(topic),
        "anchor_matches_catalog_step_in_topic": any(row["topic-id"] == topic for row in steps),
        "anchor_collides_with_other_topic_step": bool(steps) and all(row["topic-id"] != topic for row in steps),
        "catalog_step_topics_at_anchor": sorted({row["topic-id"] for row in steps}),
        "question_id_found": bool(records),
        "question_topic_matches": None if not records else any(row["topic-id"] == topic for row in records),
        "catalog_question_step_ids": sorted({row["step-id"] for row in records if row["topic-id"] == topic}),
        "question_topic_and_anchor_match": any(row["topic-id"] == topic and row["step-id"] == anchor for row in records),
        "anchor_example_content_id_match": bool(resolved_steps),
        "example_content_step_candidates": resolved_steps,
        "resolved_catalog_step_id": resolved_steps[0] if len(resolved_steps) == 1 else None,
        "question_matches_resolved_example_step": None if not records or len(resolved_steps) != 1 else any(row["topic-id"] == topic and row["step-id"] == resolved_steps[0] for row in records),
        "interpretation": "The href anchor joins topic + example content_id in saved lesson JSON; step_id is the distinct lesson placement identifier. Only a unique content-to-step relation is resolved. Absence of a question from sampled catalog content does not invalidate an observed DOM question ID.",
    }


def replay_ability(tasks, *, prior_accuracy=0.8, alpha=0.2):
    """Observed direct answers, two declared channels, no retention transitions.

    Diagnostics remain a separate evidence collection and do not enter either
    channel. Unobserved intervening work is omitted. These EWMA values are model
    outputs, not recovered Math Academy ability or placement values.
    """
    global_estimate = AccuracyEstimate(prior_accuracy, prior_accuracy)
    local = {}
    traces = []
    omitted = Counter()
    diagnostics = []
    for task in sorted(tasks, key=lambda item: (item["completed_at_local"], item["task_id"])):
        channel = CHANNELS.get(task["kind"])
        for question in task["questions"]:
            if channel is None:
                omitted[task["kind"]] += 1
                diagnostics.append({"occurrence_id": question["occurrence_id"], "topic_id": question["topic_id"], "correct": question["correct"], "result_label": question["result_label"]})
                continue
            if question["correct"] is None:
                omitted["unrecognized_result_label"] += 1
                continue
            topic = question["topic_id"]
            estimate = local.setdefault(topic, AccuracyEstimate(prior_accuracy, prior_accuracy))
            before = asdict(estimate)
            global_before = asdict(global_estimate)
            outcomes = (question["correct"],)
            estimate.update(outcomes, assessment=channel == "assessment", alpha=alpha)
            global_estimate.update(outcomes, assessment=channel == "assessment", alpha=alpha)
            traces.append({"occurrence_id": question["occurrence_id"], "topic_id": topic, "channel": channel, "correct": question["correct"], "local_before": before, "local_after": asdict(estimate), "global_before": global_before, "global_after": asdict(global_estimate)})
    return {
        "model": "direct-answer two-channel EWMA sensitivity replay",
        "policy": {"prior_accuracy_per_channel": prior_accuracy, "alpha": alpha, "channel_classification": CHANNELS, "unobserved_channel": "keeps prior", "combination": "arithmetic mean of assessment and practice estimates"},
        "channel_answer_counts": dict(Counter(trace["channel"] for trace in traces)),
        "omitted_answer_counts": dict(omitted),
        "global_estimate": {**asdict(global_estimate), "balanced_accuracy": global_estimate.accuracy},
        "topic_estimates": {topic: {**asdict(estimate), "balanced_accuracy": estimate.accuracy} for topic, estimate in sorted(local.items(), key=lambda pair: int(pair[0]))},
        "traces": traces, "diagnostic_evidence_separate": diagnostics,
        "retention_events_created": 0, "diagnostic_placement_inferred": False,
        "assumptions": ["Quiz results are classified as assessment and lesson/review/multistep as practice; this is an explicit local classification.", "Each observed answer is counted once globally and once on its linked topic, with no graph propagation.", "Only the captured tasks are replayed; missing history and unknown initial ability prevent identifying production accuracy values.", "Diagnostic answers remain separate and never become mastery, repetition credit, or ordinary quiz/practice evidence."],
    }


def _quiz_comparison(tasks, progress):
    by_id = {task["task_id"]: task for task in tasks}
    first, later = by_id.get("13553418"), by_id.get("13682227")
    if first is None or later is None:
        return None
    incorrect_topics = sorted({q["topic_id"] for q in first["questions"] if q["correct"] is False}, key=int)
    reviews = [row for row in progress if row["activity-type"] == "Review" and first["completed_at_local"] < row["completed-at"] < later["completed_at_local"]]
    first_topics, later_topics = ({q["topic_id"] for q in task["questions"]} for task in (first, later))
    return {
        "first_task_id": first["task_id"], "later_task_id": later["task_id"],
        "relationship": "Compared by explicit analyst selection of displayed Quiz 4 and Quiz 4 (Retake); no internal retake_of relation is assumed.",
        "incorrect_topics": incorrect_topics,
        "per_incorrect_topic": [{
            "topic_id": topic,
            "intervening_reviews": [{"task_id": row["task-id"], "completed_at_local": row["completed-at"], "observed_results": [q["result_label"] for q in by_id[row["task-id"]]["questions"]] if row["task-id"] in by_id else None} for row in reviews if row["topic-id"] == topic],
            "later_quiz_occurrences": [{"occurrence_id": q["occurrence_id"], "question_id": q["question_id"], "result_label": q["result_label"]} for q in later["questions"] if q["topic_id"] == topic],
        } for topic in incorrect_topics],
        "intervening_review_task_ids": [row["task-id"] for row in sorted(reviews, key=lambda row: row["completed-at"])],
        "topics_only_in_first_quiz": sorted(first_topics - later_topics, key=int),
        "topics_only_in_later_quiz": sorted(later_topics - first_topics, key=int),
        "question_ids_shared_between_quizzes": sorted({q["question_id"] for q in first["questions"]} & {q["question_id"] for q in later["questions"]}, key=int),
        "causal_scheduler_rule_verified": False,
        "interpretation": "Exact topic matches establish observed sequencing and later performance, not why reviews were assigned, scheduled due times, retention deltas, or a universal retake policy.",
    }


def build_live_audit(capture_path, progress_path, prior_path, catalog_root=None):
    capture_path, progress_path, prior_path = map(Path, (capture_path, progress_path, prior_path))
    capture = json.loads(capture_path.read_text())
    progress = _csv(progress_path)
    prior_data = json.loads(prior_path.read_text())
    progress_by_id = _unique(progress, "task-id", "progress task")
    prior_by_id = _unique(prior_data["tasks"], "task_id", "prior task")
    _unique(capture["tasks"], "task_id", "live task")
    catalogs = _catalogs(catalog_root, (q["topic_id"] for task in capture["tasks"] for q in task["questions"]))
    tasks, conflicts = [], []
    occurrences = defaultdict(list)
    prior_matches = 0
    unreobserved_answer_states = Counter()
    for task in capture["tasks"]:
        checksum = _task_checksum(task)
        tid = task["task_id"]
        completed = _completed_local(task)
        row, previous = progress_by_id.get(tid), prior_by_id.get(tid)
        comparisons = []
        if row:
            for field, old, live in (
                ("completed_at_local", row["completed-at"], completed), ("kind", row["activity-type"].lower(), task["kind"]),
                ("title", row["topic-name"], task["title"]), ("earned_xp", int(row["xp-earned"]), task["earned_xp"]),
                ("base_xp", int(row["xp-possible"]) if row["xp-possible"] else None, task["base_xp"]),
                ("url", row["url"], task["url"]),
            ):
                if old != live:
                    conflicts.append({"task_id": tid, "source": "progress.csv", "field": field, "previous": old, "live": live})
        if previous:
            for field, old, live in (
                ("date", previous["date"], task["date"]), ("kind", previous["type"].lower(), task["kind"]),
                ("title", previous["name"], task["title"]), ("earned_xp", previous["earned"], task["earned_xp"]),
                ("base_xp", previous["base"], task["base_xp"]), ("url", previous["url"], task["url"]),
            ):
                if old != live:
                    conflicts.append({"task_id": tid, "source": "prior observations", "field": field, "previous": old, "live": live})
        questions = []
        previous_questions = {q["number"]: q for q in previous["questions"]} if previous else {}
        if previous and len(previous_questions) != len(task["questions"]):
            conflicts.append({"task_id": tid, "source": "prior observations", "field": "question_count", "previous": len(previous_questions), "live": len(task["questions"])})
        for ordinal, original in enumerate(task["questions"], 1):
            if original["ordinal"] != ordinal:
                raise ValueError(f"Nonconsecutive occurrence ordinals for {tid}")
            href = re.fullmatch(r"(?:https://mathacademy\.com)?/topics/(\d+)#(\d+)", original["topic_step_href"])
            if href is None or (href[1], href[2]) != (original["topic_id"], original["step_anchor"]):
                raise ValueError(f"Inconsistent topic/anchor href in {tid}:{ordinal}")
            if original["question_dom_id"] != "question-" + original["question_id"]:
                raise ValueError(f"Inconsistent question DOM ID in {tid}:{ordinal}")
            question = {**original, "occurrence_id": f"{tid}:{ordinal}", "correct": {"Correct": True, "Incorrect": False}.get(original["result_label"]), "elapsed_seconds": elapsed_seconds(original["displayed_elapsed"]), "answer_state": None}
            old = previous_questions.get(ordinal)
            question["prior_observation"] = old
            question["prior_answer_state_reobserved"] = False if old else None
            if old:
                mismatches = []
                for field, a, b in (("correct", old["correct"], question["correct"]), ("difficulty", old["difficulty"], original["difficulty_label"]), ("elapsed_seconds", old["elapsed_seconds"], question["elapsed_seconds"])):
                    if a != b:
                        mismatch = {"task_id": tid, "ordinal": ordinal, "source": "prior observations", "field": field, "previous": a, "live": b}
                        conflicts.append(mismatch)
                        mismatches.append(mismatch)
                prior_matches += not mismatches
                unreobserved_answer_states[old["answer_state"]] += 1
                comparisons.append({"occurrence_id": question["occurrence_id"], "compared_fields_agree": not mismatches, "previous_answer_state": old["answer_state"], "live_result_label": original["result_label"], "live_answer_state": None, "interpretation": "Correct/Incorrect is an outcome label, not an observation of submitted-answer content. Prior no_answer/shown/not_shown subtype remains separately sourced and unverified by this capture."})
            question["catalog_check"] = _catalog_check(question, catalogs)
            questions.append(question)
            occurrences[question["question_id"]].append({"occurrence_id": question["occurrence_id"], "task_id": tid, "topic_id": question["topic_id"], "step_anchor": question["step_anchor"], "result_label": question["result_label"]})
        tasks.append({**{key: value for key, value in task.items() if key != "questions"}, "completed_at_local": completed, "time_zone": None, "in_original_progress": row is not None, "in_prior_observations": previous is not None, "questions": questions, "prior_comparisons": comparisons, "transcription_checksum": checksum})
    tasks.sort(key=lambda task: (task["completed_at_local"], task["task_id"]))
    all_questions = [question for task in tasks for question in task["questions"]]
    checks = [question["catalog_check"] for question in all_questions if question["catalog_check"] is not None]
    repeated = {qid: items for qid, items in occurrences.items() if len({item["task_id"] for item in items}) > 1}
    prior_occurrence_ids = {(task["task_id"], question["number"]) for task in prior_data["tasks"] for question in task["questions"]}
    live_occurrence_ids = {(task["task_id"], question["ordinal"]) for task in tasks for question in task["questions"]}
    remaining_task_scoped = sum(
        (task["task_id"], question["number"]) not in live_occurrence_ids
        and bool(progress_by_id.get(task["task_id"], {}).get("topic-id"))
        for task in prior_data["tasks"] for question in task["questions"]
    )
    graph_capture = capture.get("graph_snapshot")
    graph_audit = None
    if graph_capture:
        nodes = sorted(graph_capture["nodes"], key=lambda node: node[0])
        graph_hash = fnv1a32_json(nodes)
        if graph_hash != graph_capture["browser_nodes_fnv1a32"] or len(nodes) != graph_capture["node_count"] or len({node[0] for node in nodes}) != len(nodes):
            raise ValueError("Graph snapshot count, identity, or checksum validation failed")
        graph_audit = {"captured_at": graph_capture["captured_at"], "course_id": graph_capture["course_id"], "node_count": len(nodes), "checksum_verified": True, "calculated_checksum": graph_hash, "fill_counts": dict(Counter(node[1] for node in nodes)), "numeric_fire_state_observed": False}
    return {
        "schema_version": 1,
        "checksum_encoding": CHECKSUM_ENCODING,
        "sources": {"live_capture": _source(capture_path), "original_progress": _source(progress_path), "prior_observations": _source(prior_path), "catalogs": catalogs["sources"] if catalogs else None, "implementation": _source(Path(__file__)), "calibration_implementation": _source(Path(__file__).with_name("calibration.py"))},
        "summary": {
            "captured_tasks": len(tasks), "captured_questions": len(all_questions), "distinct_question_ids": len(occurrences),
            "distinct_topic_ids": len({q["topic_id"] for q in all_questions}), "distinct_topic_anchor_pairs": len({(q["topic_id"], q["step_anchor"]) for q in all_questions}),
            "task_kind_counts": dict(Counter(task["kind"] for task in tasks)), "result_label_counts": dict(Counter(q["result_label"] for q in all_questions)),
            "displayed_elapsed_seconds_total": sum(q["elapsed_seconds"] for q in all_questions),
            "tasks_joined_to_original_progress": sum(task["in_original_progress"] for task in tasks),
            "new_task_ids_outside_original_progress": [task["task_id"] for task in tasks if not task["in_original_progress"]],
            "tasks_joined_to_prior_observations": sum(task["in_prior_observations"] for task in tasks),
            "prior_question_features_agree": prior_matches,
            "prior_answer_state_counts_not_reobserved": dict(unreobserved_answer_states),
            "source_conflict_count": len(conflicts), "question_ids_repeated_across_tasks": len(repeated),
            "browser_task_checksums_verified": sum(task["transcription_checksum"]["verified"] is True for task in tasks),
            "catalog_topic_matches": sum(check["topic_exists"] for check in checks),
            "catalog_question_ids_found": sum(check["question_id_found"] for check in checks),
            "catalog_question_topic_matches": sum(check["question_topic_matches"] is True for check in checks),
            "catalog_topic_anchor_step_matches": sum(check["anchor_matches_catalog_step_in_topic"] for check in checks),
            "bare_anchor_collisions_with_other_topic_steps": sum(check["anchor_collides_with_other_topic_step"] for check in checks),
            "topic_anchor_matches_example_content_id": sum(check["anchor_example_content_id_match"] for check in checks),
            "unambiguous_content_to_step_joins": sum(check["resolved_catalog_step_id"] is not None for check in checks),
            "known_questions_matching_resolved_example_step": sum(check["question_matches_resolved_example_step"] is True for check in checks),
            "verified_retention_transitions": 0,
            "union_progress_and_live_task_ids": len(set(progress_by_id) | {task["task_id"] for task in tasks}),
            "union_observed_task_ids": len(set(prior_by_id) | {task["task_id"] for task in tasks}),
            "union_question_occurrences": len(prior_occurrence_ids | live_occurrence_ids),
            "union_question_occurrences_with_direct_topic_link": len(live_occurrence_ids),
            "additional_prior_occurrences_with_task_topic_scope_only": remaining_task_scoped,
        },
        "source_conflicts": conflicts,
        "repeated_question_ids_across_tasks": repeated,
        "quiz4_comparison": _quiz_comparison(tasks, progress),
        "ability_channel_replay": replay_ability(tasks),
        "graph_snapshot_audit": graph_audit,
        "limitations": ["The captured topic and anchor hrefs establish direct occurrence scope, unlike the earlier reduced observations.", "No task-level FIRe pass/fail, credit magnitude, diagnostic state/reset result, encompassing weight, current repetition state or due timestamp is exposed here.", "Catalog question/step inventories are sampled content and may use different identifier namespaces or versions; missing IDs do not invalidate observed DOM identities.", "Answer labels and submitted-answer content are distinct. Previously recorded no_answer is neither disproved nor confirmed by a newly captured Incorrect result label.", "Repeated question IDs remain separate task-plus-ordinal occurrences; cross-task duplication is not deduplicated away.", "Completion and answer timestamps lack verified time zone; quiz answer timestamps do not provide individual answer chronology."],
        "tasks": tasks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", type=Path, default=Path("reference/fire-live-observations-2026-09-26.json"))
    parser.add_argument("--progress", type=Path, default=Path("reference/progress.csv"))
    parser.add_argument("--prior", type=Path, default=Path("reference/mathacademy-xp-observations.json"))
    parser.add_argument("--catalog-root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("engine/fire/fixtures/live-history-audit.json"))
    args = parser.parse_args()
    result = build_live_audit(args.capture, args.progress, args.prior, args.catalog_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
