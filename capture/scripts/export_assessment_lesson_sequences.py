#!/usr/bin/env python3
"""Cross-check assessment KP positions against complete captured lesson definitions.

This helper reads local captures and an optional frozen database export only.
Select lessons through small activity.json files before reading content.json.
Rerun with --reuse-source after the database mapping is exported to reuse the
source projections and add identity/order comparisons without rereading captures.
The stable resolved-question-identities.json projection supplies completed joins;
the downstream questions.json report is not an input to avoid circular hashes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


DEFAULT_DIRECTORY = "reference/mathacademy/assessment-kp-position-analysis-2026-10-16"


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def timestamp(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            pass
    return None


def latest_timestamp(*values):
    times = [t for v in values if (t := timestamp(v)) is not None]
    return max(times) if times else None


def path_label(root, path):
    return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)


def extract_lesson(root, activity_path, activity):
    content_path = activity_path.with_name("content.json")
    row = dict(account=activity_path.parent.parent.name, task_id=activity_path.parent.name,
               topic_id=str(activity.get("topic_id")), course_id=str(activity.get("course_id")),
               title=activity.get("title"), source_file=path_label(root, content_path),
               activity_file=path_label(root, activity_path),
               activity_sha256=sha256(activity_path.read_bytes()), complete=False, errors=[])
    row["task_key"] = row["account"] + "/" + row["task_id"]
    if not content_path.exists():
        row["errors"].append("missing_content")
        return row
    raw = content_path.read_bytes()
    row["source_sha256"] = sha256(raw)
    content = json.loads(raw)
    del raw
    definition = content.get("lesson_definition") or {}
    row["content_captured_at"] = content.get("captured_at")
    row["definition_complete"] = definition.get("complete", False)
    row["definition_issues"] = definition.get("issues", [])
    row["definition_source_url"] = definition.get("source_url")
    row["definition_title"] = definition.get("title")
    completion_path = activity_path.with_name("capture-complete.json")
    if completion_path.exists():
        completion_raw = completion_path.read_bytes()
        completion = json.loads(completion_raw)
        row["completion_file"] = path_label(root, completion_path)
        row["completion_sha256"] = sha256(completion_raw)
        row["capture_completed_at"] = completion.get("completed_at")
        if str(completion.get("task_id")) != row["task_id"]:
            row["errors"].append("completion_task_identity_conflict")
    row["sequence_observed_by"] = latest_timestamp(row.get("content_captured_at"),
                                                   row.get("capture_completed_at"))
    source_path = definition.get("source_file")
    if source_path:
        source_path = Path(source_path)
        if not source_path.is_absolute():
            source_path = root / source_path
        row["definition_source_file"] = path_label(root, source_path)
        if source_path.exists():
            row["definition_source_sha256"] = sha256(source_path.read_bytes())
        else:
            row["errors"].append("missing_definition_source_file")
    for key, expected in (("topic_id", row["topic_id"]), ("task_id", row["task_id"]),
                          ("kind", "lesson")):
        if str(content.get(key)) != expected:
            row["errors"].append("content_" + key + "_conflict")
    if str(definition.get("topic_id")) != row["topic_id"]:
        row["errors"].append("definition_topic_identity_conflict")
    if not definition.get("complete"):
        row["errors"].append("definition_not_complete")
    if definition.get("issues"):
        row["errors"].append("definition_reports_issues")
    steps = definition.get("steps", [])
    positions = [s.get("position") for s in steps]
    if not positions or not all(type(p) is int for p in positions):
        row["errors"].append("missing_or_invalid_step_positions")
        steps = []
    elif len(set(positions)) != len(positions):
        row["errors"].append("duplicate_step_positions")
        steps = []
    else:
        if sorted(positions) not in (list(range(len(positions))), list(range(1, len(positions) + 1))):
            row["errors"].append("noncontiguous_step_positions")
        steps = sorted(steps, key=lambda s: s["position"])
    row["steps"] = [{k: s.get(k) for k in ("position", "type", "content_id", "math_academy_id", "title")}
                    for s in steps]
    examples = []
    for step in steps:
        if step.get("type") == "tutorial":
            continue
        if step.get("type") != "example":
            row["errors"].append("unsupported_nonexample_step_type:" + str(step.get("type")))
            continue
        content_id = str(step.get("content_id"))
        if not re.fullmatch(r"\d+", content_id):
            row["errors"].append("invalid_example_content_id")
            continue
        # This prefix is justified by the explicit example step, not a KP anchor.
        examples.append("e-" + content_id)
    if not examples:
        row["errors"].append("no_example_stages")
    if len(set(examples)) != len(examples):
        row["errors"].append("duplicate_example_stages")
    row["ordered_example_ids"] = examples
    row["lesson_kps"] = len(examples)
    row["complete"] = not row["errors"]
    return row


def collect(root, topic_ids, workers=3):
    selected = []
    activity_count = 0
    for path in sorted((root / "reference/mathacademy/capture").glob("*/*/activity.json")):
        activity_count += 1
        activity = json.loads(path.read_bytes())
        if activity.get("kind") == "lesson" and str(activity.get("topic_id")) in topic_ids:
            selected.append((path, activity))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        lessons = list(pool.map(lambda pair: extract_lesson(root, *pair), selected))
    return lessons, activity_count


def canonical_order(mapping, entities):
    order = [mapping.get("kps", {}).get(str(entity), {}).get("canonical_example_id") for entity in entities]
    return order if order and all(re.fullmatch(r"e-\d+", e or "") for e in order) else None


def position_options(lessons, example_id):
    grouped = defaultdict(list)
    for lesson in lessons:
        order = lesson["ordered_example_ids"]
        if example_id in order:
            grouped[(order.index(example_id) + 1, len(order))].append(lesson["task_key"])
    return [dict(position=pos, lesson_kps=size, relative_position=(pos - 1) / (size - 1) if size > 1 else None,
                 lesson_task_keys=keys) for (pos, size), keys in sorted(grouped.items())]


def compare(inventory, lessons, mapping, resolved_questions=None):
    by_topic = defaultdict(list)
    for lesson in lessons:
        if lesson["complete"]:
            by_topic[lesson["topic_id"]].append(lesson)
    topics = {}
    for topic_id in sorted({q["topic_id"] for q in inventory["questions"]}):
        relevant = by_topic[topic_id]
        groups = defaultdict(list)
        for lesson in relevant:
            groups[tuple(lesson["ordered_example_ids"])].append(lesson)
        db_topic = mapping.get("topics", {}).get(topic_id, {})
        db_order = canonical_order(mapping, db_topic.get("ordered_kp_entities") or [])
        variants = []
        for order, evidence in sorted(groups.items()):
            times = [l["sequence_observed_by"] for l in evidence if l["sequence_observed_by"] is not None]
            variants.append(dict(ordered_example_ids=list(order), lesson_kps=len(order),
                                 lesson_task_keys=[l["task_key"] for l in evidence],
                                 first_observed_by=min(times) if times else None,
                                 last_observed_by=max(times) if times else None,
                                 matches_database_order=list(order) == db_order if db_order else None))
        if not mapping:
            status = "database_mapping_not_available"
        elif not db_order:
            status = "database_order_not_unique_or_missing_canonical_identity"
        elif not variants:
            status = "no_complete_source_sequence"
        elif all(v["matches_database_order"] for v in variants):
            status = "all_source_sequences_match_database"
        elif any(v["matches_database_order"] for v in variants):
            status = "some_source_sequences_match_database"
        else:
            status = "source_database_order_conflict"
        topics[topic_id] = dict(topic_id=topic_id, source_order_status="unique" if len(variants) == 1 else
                                "conflicting" if len(variants) > 1 else "missing",
                                source_variants=variants, database_order=db_order, database_comparison=status)
    tasks = {t["task_key"]: t for t in inventory["assessments"]}
    task_times = defaultdict(list)
    for q in inventory["questions"]:
        if (time := timestamp(q.get("captured_at"))) is not None:
            task_times[q["task_key"]].append(time)
    resolved_by_occurrence = {q["occurrence_id"]: q for q in (resolved_questions or [])}
    rows = []
    for q in inventory["questions"]:
        task = tasks[q["task_key"]]
        times = task_times[q["task_key"]] + [t for t in [timestamp(task.get("completed_at"))] if t is not None]
        reference_time = min(times) if times else None
        db_question = mapping.get("questions", {}).get(q["question_id"], {})
        memberships = {m["kp_entity"] for m in db_question.get("memberships", [])
                       if q["topic_id"] in m["topic_ids"] and ":org/Math-Academy" in m.get("sources", [])}
        entity = next(iter(memberships)) if len(memberships) == 1 else None
        example_id = mapping.get("kps", {}).get(str(entity), {}).get("canonical_example_id")
        identity_evidence = "Math Academy-attributed database question/KP membership within source topic" if entity else None
        resolved = resolved_by_occurrence.get(q["occurrence_id"])
        if resolved and resolved.get("mapping_status") == "positioned":
            if any(resolved.get(k) != q.get(k) for k in ("question_id", "topic_id", "source_sha256")):
                raise ValueError("Resolved question inventory conflict: " + q["occurrence_id"])
            resolved_entity = resolved.get("kp_entity")
            resolved_example = resolved.get("canonical_example_id")
            if (resolved_entity not in mapping.get("topics", {}).get(q["topic_id"], {}).get("kp_entities", [])
                    or resolved_example != mapping.get("kps", {}).get(str(resolved_entity), {}).get("canonical_example_id")
                    or (entity is not None and (entity != resolved_entity or example_id != resolved_example))):
                raise ValueError("Resolved question database identity conflict: " + q["occurrence_id"])
            entity, example_id = resolved_entity, resolved_example
            identity_evidence = resolved.get("mapping_evidence")
        relevant = by_topic[q["topic_id"]]
        prior = [l for l in relevant if reference_time is not None and l["sequence_observed_by"] is not None
                 and l["sequence_observed_by"] < reference_time]
        same_account_prior = [l for l in prior if l["account"] == q["account"]]
        position_sets = {"all_source": position_options(relevant, example_id),
                         "prior_source": position_options(prior, example_id),
                         "same_account_prior_source": position_options(same_account_prior, example_id)}
        db_order = topics[q["topic_id"]]["database_order"]
        db_position = (db_order.index(example_id) + 1, len(db_order)) if db_order and example_id in db_order else None
        row = dict(occurrence_id=q["occurrence_id"], question_id=q["question_id"], task_key=q["task_key"],
                   topic_id=q["topic_id"], kp_entity=entity, canonical_example_id=example_id,
                   identity_evidence=identity_evidence,
                   assessment_reference_time=reference_time, database_position=db_position,
                   available_source_lessons=len(relevant), available_prior_source_lessons=len(prior),
                   available_same_account_prior_source_lessons=len(same_account_prior), **position_sets)
        for key, selected_lessons in (("all_source", relevant), ("prior_source", prior),
                                      ("same_account_prior_source", same_account_prior)):
            options = position_sets[key]
            missing = len(selected_lessons) - sum(len(p["lesson_task_keys"]) for p in options)
            row[key + "_missing_example_lessons"] = missing
            row[key + "_unique"] = len(options) == 1 and not missing
            row[key + "_matches_database"] = bool(db_position and row[key + "_unique"] and
                (options[0]["position"], options[0]["lesson_kps"]) == db_position)
        rows.append(row)
    return topics, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", default=DEFAULT_DIRECTORY)
    parser.add_argument("--reuse-source", action="store_true")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    directory = root / args.directory
    inventory_path = directory / "capture-inventory.json"
    inventory_raw = inventory_path.read_bytes()
    inventory = json.loads(inventory_raw)
    topic_ids = {q["topic_id"] for q in inventory["questions"]}
    output = directory / "source-lesson-sequences.json"
    if args.reuse_source:
        previous = json.loads(output.read_text())
        if previous["inventory_sha256"] != sha256(inventory_raw):
            raise ValueError("Inventory changed; rerun without --reuse-source")
        lessons, scanned = previous["lessons"], previous["summary"]["activity_files_scanned"]
    else:
        lessons, scanned = collect(root, topic_ids, args.workers)
    mapping_path = directory / "database/mapping.json"
    mapping_raw = mapping_path.read_bytes() if mapping_path.exists() else None
    mapping = json.loads(mapping_raw) if mapping_raw else {}
    resolved_path = directory / "resolved-question-identities.json"
    resolved_raw = resolved_path.read_bytes() if resolved_path.exists() else None
    resolved_questions = json.loads(resolved_raw) if resolved_raw else []
    topics, questions = compare(inventory, lessons, mapping, resolved_questions)
    summary = dict(activity_files_scanned=scanned, assessed_topics=len(topic_ids),
                   relevant_lesson_captures=len(lessons), complete_source_lessons=sum(l["complete"] for l in lessons),
                   invalid_lesson_captures=sum(not l["complete"] for l in lessons),
                   source_topic_order_status=dict(Counter(t["source_order_status"] for t in topics.values())),
                   source_database_comparison=dict(Counter(t["database_comparison"] for t in topics.values())),
                   assessed_question_occurrences=len(questions))
    for key in ("all_source", "prior_source", "same_account_prior_source"):
        summary[key + "_unique_question_positions"] = sum(q[key + "_unique"] for q in questions)
        summary[key + "_matching_database_question_positions"] = sum(q[key + "_matches_database"] for q in questions)
        eligible = [q[key][0] for q in questions if q[key + "_matches_database"] and q[key][0]["lesson_kps"] > 1]
        summary[key + "_matching_database_multi_kp_positions"] = len(eligible)
        summary[key + "_mean_normalized_position"] = (sum(p["relative_position"] for p in eligible) / len(eligible)
                                                      if eligible else None)
        summary[key + "_first_count"] = sum(p["position"] == 1 for p in eligible)
        summary[key + "_last_count"] = sum(p["position"] == p["lesson_kps"] for p in eligible)
    result = dict(generated_at=datetime.now(timezone.utc).isoformat(), schema_version=1,
                  inventory_file=path_label(root, inventory_path), inventory_sha256=sha256(inventory_raw),
                  mapping_file=path_label(root, mapping_path) if mapping else None,
                  mapping_sha256=sha256(mapping_raw) if mapping_raw else None,
                  resolved_questions_file=path_label(root, resolved_path) if resolved_raw else None,
                  resolved_questions_sha256=sha256(resolved_raw) if resolved_raw else None,
                  database_identity=mapping.get("identity"),
                  methodology={
                      "selection": "Small activity.json declares kind=lesson and a topic present in assessment inventory.",
                      "order": "Complete lesson_definition, distinct contiguous explicit step positions; tutorials omitted from KP rank.",
                      "identity": "e-<content_id> only for explicit example steps; use Math Academy-attributed database question/KP/topic membership or the separately resolved resolved-question-identities.json identity, cross-checked against the database KP canonical example and topic membership. No additional title/anchor inference occurs in this helper; downstream questions.json is not an input.",
                      "version": "All complete source sequences retained; uniqueness requires the full canonical-example sequence, and position comparisons include both position and lesson size.",
                      "time": "Prior source evidence uses max(content captured_at, capture completed_at) strictly before earliest recorded question captured_at or task completion in that assessment. These are recorded capture times, not proof of original presentation time or learner exposure.",
                      "scope": "Current capture/<account>/<task> only; no legacy insertion-order inference and no database writes.",
                      "reuse": "--reuse-source retains source hashes from the original extraction rather than checking current source files again."},
                  summary=summary, topics=topics, lessons=lessons, questions=questions,
                  script_sha256=sha256(Path(__file__).read_bytes()))
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
