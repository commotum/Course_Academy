"""Audit sparse activity evidence without promoting XP or completion to mastery.

This module deliberately does not import the FIRe scheduler. Its optional replay
adapter produces labelled sensitivity scenarios, never a production-state export.
Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


def _source(path: Path) -> dict[str, Any]:
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _number(value: str) -> int | None:
    return int(value) if value else None


def _counts(values: Any) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def _profile_audit(path: Path, activities: list[dict[str, Any]]) -> dict[str, Any]:
    rows = _rows(path)
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for activity in activities:
        if activity["topic_id"]:
            by_topic[activity["topic_id"]].append(activity)
    completed = [row for row in rows if row["completed"] == "1"]
    unmatched = [row["topic-id"] for row in completed if not any(
        item["completed_at_local"] == row["last-completed-at"]
        for item in by_topic[row["topic-id"]]
    )]
    stale = [row["topic-id"] for row in completed if any(
        item["completed_at_local"] > row["last-completed-at"]
        for item in by_topic[row["topic-id"]]
    )]
    return {
        "source": _source(path), "row_count": len(rows),
        "unique_topics": len({row["topic-id"] for row in rows}),
        "status_counts": _counts(row["mastery-status"] for row in rows),
        "evidence_counts": _counts(row["mastery-evidence"] for row in rows),
        "completed_rows": len(completed),
        "latest_recorded_completion": max((row["last-completed-at"] for row in rows), default=None),
        "topics_shared_with_history": len(set(by_topic) & {row["topic-id"] for row in rows}),
        "shared_topic_status_counts": _counts(row["mastery-status"] for row in rows if row["topic-id"] in by_topic),
        "completed_topics_without_matching_history_timestamp": unmatched,
        "completed_topics_with_later_history_events": stale,
        "ground_truth_for_fire": False,
        "reason": "Statuses mix activity history, queue checkmarks, and local prerequisite-ancestry inference; there are no FIRe state values or observation timestamps.",
    }


def build_audit(
    progress_path: str | Path,
    observations_path: str | Path,
    knowledge_profile_path: str | Path | None = None,
    catalog_path: str | Path | None = None,
) -> dict[str, Any]:
    """Join by exact task ID; retain unknown outcomes, dates, and topic scope.

    Input-integrity failures that destroy an unambiguous join raise ValueError.
    A stale snapshot hash is reported, while each retained observation is checked
    against its matching current row independently.
    """
    progress_path, observations_path = Path(progress_path), Path(observations_path)
    rows = _rows(progress_path)
    data = json.loads(observations_path.read_text(encoding="utf-8"))
    observed = data["tasks"]
    for name, records, key in (("progress", rows, "task-id"), ("observations", observed, "task_id")):
        counts = Counter(record[key] for record in records)
        duplicates = sorted(key for key, count in counts.items() if count > 1)
        if duplicates:
            raise ValueError(f"Duplicate task IDs in {name}: {duplicates}")
    by_id = {task["task_id"]: task for task in observed}
    unknown_ids = sorted(set(by_id) - {row["task-id"] for row in rows})
    if unknown_ids:
        raise ValueError(f"Observed task IDs missing from progress: {unknown_ids}")
    catalog = None
    if catalog_path is not None:
        catalog = {row["topic-id"]: row["topic-name"] for row in _rows(Path(catalog_path))}
    activities = []
    for row_number, row in enumerate(rows, 2):
        # Parse strictly but do not attach an unsupported time zone.
        datetime.strptime(row["completed-at"], "%Y-%m-%d %H:%M")
        task = by_id.get(row["task-id"])
        issues = []
        questions = []
        if task is not None:
            for field, expected in (
                ("date", row["date"]), ("type", row["activity-type"]),
                ("name", row["topic-name"]), ("earned", _number(row["xp-earned"])),
                ("base", _number(row["xp-possible"])), ("url", row["url"]),
            ):
                if task[field] != expected:
                    issues.append({"field": field, "progress": expected, "observation": task[field]})
            for index, question in enumerate(task["questions"], 1):
                if type(question["correct"]) is not bool:
                    raise ValueError(f"Task {task['task_id']}: non-boolean question outcome")
                if type(question["elapsed_seconds"]) is not int or question["elapsed_seconds"] < 0:
                    raise ValueError(f"Task {task['task_id']}: invalid elapsed seconds")
                if question["number"] != index:
                    raise ValueError(f"Task {task['task_id']}: nonconsecutive question order")
                questions.append({
                    "occurrence": index, "correct": question["correct"],
                    "difficulty": question["difficulty"], "answer_state": question["answer_state"],
                    "elapsed_seconds": question["elapsed_seconds"],
                    "topic_id": None, "knowledge_point_id": None, "question_id": None,
                    "answered_at": None,
                })
            groups = task.get("group_question_counts")
            if groups is not None and sum(groups) != len(questions):
                raise ValueError(f"Task {task['task_id']}: group counts disagree with questions")
        topic = row["topic-id"] or None
        catalog_match = None if catalog is None or topic is None else catalog.get(topic) == row["topic-name"]
        activities.append({
            "task_id": row["task-id"], "progress_csv_row": row_number,
            "url": row["url"], "completed_at_local": row["completed-at"],
            "time_zone": None, "activity_type": row["activity-type"],
            "topic_id": topic, "topic_name": row["topic-name"],
            "topic_id_provenance": "progress.csv; local catalog reconciliation described in progress-notes.md" if topic else None,
            "catalog_title_and_id_match": catalog_match,
            "course_code_contextual": row["course-code"],
            "xp_earned": _number(row["xp-earned"]), "xp_base": _number(row["xp-possible"]),
            "status_raw": row["status"], "fire_outcome": None,
            "question_observations": questions or None,
            "question_observation_provenance": "mathacademy-xp-observations.json:tasks/task_id; completed-task DOM" if task else None,
            "group_question_counts": task.get("group_question_counts") if task else None,
            "join_issues": issues,
            "chronology_caveats": ["Task feed date conflicts with yearless question dates; see activity-schema report."] if row["task-id"] == "4748206" else [],
        })
    activities.sort(key=lambda item: (item["completed_at_local"], item["task_id"]))
    question_tasks = [item for item in activities if item["question_observations"]]
    scoped_tasks = [item for item in question_tasks if item["topic_id"]]
    questions = [question for item in question_tasks for question in item["question_observations"]]
    imperfect = [item for item in question_tasks if not all(question["correct"] for question in item["question_observations"])]
    perfect = [item for item in question_tasks if all(question["correct"] for question in item["question_observations"])]
    positive_imperfect = [item for item in imperfect if item["xp_earned"] > 0]
    timestamps = Counter(item["completed_at_local"] for item in activities)
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in activities:
        if item["topic_id"]:
            by_topic[item["topic_id"]].append(item)
    pairs = []
    for topic, items in sorted(by_topic.items()):
        for earlier, later in zip(items, items[1:]):
            pairs.append({
                "topic_id": topic, "earlier_task_id": earlier["task_id"],
                "later_task_id": later["task_id"],
                "calendar_gap_days": (datetime.fromisoformat(later["completed_at_local"]) - datetime.fromisoformat(earlier["completed_at_local"])).total_seconds() / 86400,
                "later_type": later["activity_type"],
                "verified_due_interval": False,
            })
    progress_source = _source(progress_path)
    return {
        "schema_version": 1,
        "sources": {
            "progress": progress_source,
            "question_observations": _source(observations_path),
            "observation_metadata": data["metadata"],
            "catalog": _source(Path(catalog_path)) if catalog_path else None,
        },
        "summary": {
            "activities": len(activities), "activity_types": _counts(item["activity_type"] for item in activities),
            "first_completion_local": activities[0]["completed_at_local"] if activities else None,
            "last_completion_local": activities[-1]["completed_at_local"] if activities else None,
            "completion_timestamp_ties": {key: count for key, count in timestamps.items() if count > 1},
            "activities_with_topic_id": sum(item["topic_id"] is not None for item in activities),
            "distinct_history_topics": len(by_topic),
            "observed_tasks": len(question_tasks), "observed_questions": len(questions),
            "correct_questions": sum(question["correct"] for question in questions),
            "incorrect_questions": sum(not question["correct"] for question in questions),
            "observed_tasks_with_task_topic_id": len(scoped_tasks),
            "observed_questions_with_task_topic_scope": sum(len(item["question_observations"]) for item in scoped_tasks),
            "questions_with_direct_topic_id": 0, "questions_with_knowledge_point_id": 0,
            "observed_elapsed_seconds": sum(question["elapsed_seconds"] for question in questions),
            "missing_question_detail_tasks": len(activities) - len(question_tasks),
            "all_correct_observed_tasks": len(perfect),
            "all_correct_observed_tasks_with_task_topic_id": sum(item["topic_id"] is not None for item in perfect),
            "join_issue_count": sum(len(item["join_issues"]) for item in activities),
            "observation_snapshot_hash_matches": data["metadata"]["progress_snapshot_sha256"] == progress_source["sha256"],
            "snapshot_row_count_delta": len(activities) - data["metadata"]["progress_snapshot_rows"],
            "successive_same_topic_pairs": len(pairs),
            "verified_fire_state_transitions": 0, "verified_due_time_predictions": 0,
            "directly_observed_encompassing_weights": 0,
        },
        "contradictions": [
            {"claim": "Completed implies every question was correct", "counterexample_count": len(imperfect), "task_ids": [item["task_id"] for item in imperfect]},
            {"claim": "Positive earned XP implies every question was correct", "counterexample_count": len(positive_imperfect), "task_ids": [item["task_id"] for item in positive_imperfect]},
            {"claim": "Earned XP divided by displayed base is a bounded correctness rate", "counterexample_count": sum(item["xp_base"] is not None and (item["xp_earned"] < 0 or item["xp_earned"] > item["xp_base"]) for item in activities), "examples": [item["task_id"] for item in activities if item["xp_base"] is not None and (item["xp_earned"] < 0 or item["xp_earned"] > item["xp_base"])][:5]},
        ],
        "identifiability": {
            "observable": ["task completion chronology at minute resolution without verified time zone", "task topic IDs from prior catalog reconciliation", "ordered correctness and displayed elapsed seconds for the 34 sampled tasks", "same-topic completion gaps, not scheduled due intervals"],
            "unidentified": ["task-level FIRe success/failure criterion", "per-question topic/KP identities in the reduced observations", "initial repetition state, interval and diagnostic reset/merge policy", "encompassing edges and weights", "full exercise-time clock, due times and scheduler queue", "per-task time of assignment and learner choice/delay", "historical calibration parameters and model version"],
            "interpretation": "Agreement of a chosen scenario with activity order is a compatibility check. Without observed due/state values it is not a verified FIRe prediction. Question correctness alone cannot identify repetition-state transitions.",
        },
        "knowledge_profile": _profile_audit(Path(knowledge_profile_path), activities) if knowledge_profile_path else None,
        "same_topic_completion_pairs": pairs,
        "activities": activities,
    }


def build_replay_scenario(audit: dict[str, Any], *, outcome_policy: str, clock_policy: str) -> dict[str, Any]:
    """Create explicitly assumed engine inputs from actual observed correctness.

    Unknown topic tasks contribute known displayed elapsed seconds to the partial
    clock but emit no topic event. Unobserved tasks contribute neither time nor
    outcomes. Conflicting joins never emit events. Neither policy is asserted to
    be MA's task success definition; question mode is a question-granularity model.
    """
    if outcome_policy not in {"question_correct", "all_questions_correct"}:
        raise ValueError("Choose question_correct or all_questions_correct explicitly")
    if clock_policy not in {"observed_elapsed_hours", "wall_days"}:
        raise ValueError("Choose observed_elapsed_hours or wall_days explicitly")
    activities = audit["activities"]
    origin = datetime.fromisoformat(activities[0]["completed_at_local"]) if activities else None
    elapsed = 0
    events = []
    omitted = Counter()
    for activity in activities:
        questions = activity["question_observations"]
        if not questions:
            omitted["unobserved_task"] += 1
            continue
        can_emit = activity["topic_id"] is not None and not activity["join_issues"]
        if not can_emit:
            omitted["unmapped_or_conflicting_task"] += 1
        for question in questions:
            elapsed += question["elapsed_seconds"]
            if not can_emit or (outcome_policy == "all_questions_correct" and question is not questions[-1]):
                continue
            time = elapsed / 3600 if clock_policy == "observed_elapsed_hours" else (datetime.fromisoformat(activity["completed_at_local"]) - origin).total_seconds() / 86400
            events.append({
                "event_id": activity["task_id"] + (f":q{question['occurrence']}" if outcome_policy == "question_correct" else ""),
                "task_id": activity["task_id"], "topic_id": activity["topic_id"],
                "activity_type": activity["activity_type"], "time": time,
                "success": question["correct"] if outcome_policy == "question_correct" else all(item["correct"] for item in questions),
                "outcome_provenance": "observed question correctness" if outcome_policy == "question_correct" else "assumed task aggregation: all questions correct",
            })
    return {
        "outcome_policy": outcome_policy, "clock_policy": clock_policy,
        "time_unit": "hours" if clock_policy == "observed_elapsed_hours" else "days",
        "assumptions": [
            "Every retained lesson/review question is assigned to its task's catalog topic; question-level topic links were not retained.",
            "Question correctness is a question-level success flag; task aggregation, when selected, requires every question correct. Neither is a recovered MA FIRe task rule.",
            "Observed elapsed clock sums only sampled questions, includes possible pauses and omits time on all unobserved tasks; it is not a recovered exercise clock." if clock_policy == "observed_elapsed_hours" else "Wall-clock days from the first feed completion are substituted for exercise time; questions share their task's completion time.",
            "Initial repetition state and encompassing graph must be supplied independently as explicit assumptions.",
        ],
        "events": events, "omitted_task_counts": dict(omitted),
        "verified_production_predictions": 0,
    }


def run_history_scenarios(audit: dict[str, Any]) -> dict[str, Any]:
    """Run the reconstructed core on retained evidence under explicit assumptions.

    Calendar scenarios use the core's day unit. The incomplete elapsed clock is
    a sensitivity control, with both event hours and a one-hour base converted
    to days; it is not offered as a faithful historical timing reconstruction.
    No encompassing links, initial state, or observed due dates are fabricated.
    """
    from dataclasses import asdict
    from itertools import product

    from .core import EncompassingGraph, Event, FireEngine, Policy, TopicState

    learner = "sparse-history-scenario"
    by_task = {item["task_id"]: item for item in audit["activities"]}
    runs = []
    for outcome, clock, initial_repetitions, growth, memory_order in product(
        ("question_correct", "all_questions_correct"),
        ("wall_days", "observed_elapsed_hours"), (0.0, 4.0), (2.0, 1.5),
        ("decay-before-add", "literal-add-before-decay"),
    ):
        scenario = build_replay_scenario(audit, outcome_policy=outcome, clock_policy=clock)
        topics = sorted({event["topic_id"] for event in scenario["events"]})
        policy = Policy(
            name="sparse-history-sensitivity",
            base_interval_days=1.0 if clock == "wall_days" else 1 / 24,
            interval_growth=growth,
            memory_order=memory_order,
        )
        graph = EncompassingGraph(topics=topics)
        engine = FireEngine(graph, policy)
        for topic in topics:
            engine.seed(learner, topic, TopicState(
                repetitions=initial_repetitions, memory=1.0, memory_at=0.0,
                interval_days=policy.interval(initial_repetitions), accuracy=policy.prior_accuracy,
            ))
        traces = []
        review_compatibility = []
        reviewed_tasks = set()
        for event in scenario["events"]:
            task = by_task[event["task_id"]]
            at = event["time"] if clock == "wall_days" else event["time"] / 24
            before = engine.states[learner][event["topic_id"]]
            due_before = before.due_at(policy)
            if task["activity_type"] == "Review" and task["task_id"] not in reviewed_tasks:
                reviewed_tasks.add(task["task_id"])
                review_compatibility.append({
                    "task_id": task["task_id"], "topic_id": event["topic_id"],
                    "observed_event_at_days": at, "model_due_at_days": due_before,
                    "model_due_when_review_observed": due_before <= at + 1e-12,
                    "is_verified_prediction": False,
                })
            outcomes = tuple(question["correct"] for question in task["question_observations"])
            if outcome == "question_correct":
                outcomes = (event["success"],)
            receipt = engine.apply(Event(
                id=event["event_id"], learner=learner, topic=event["topic_id"],
                at=at, passed=event["success"], quality=1.0,
                kind=task["activity_type"].lower(), learned=False,
                question_results=outcomes, source="explicit-sparse-history-assumption",
            ))
            traces.append({
                "event_id": event["event_id"], "task_id": task["task_id"],
                "event_hash": receipt["event_hash"], "at_days": at,
                "passed": event["success"], "updates": receipt["updates"],
            })
        end = max((trace["at_days"] for trace in traces), default=0)
        final_states = {
            topic: {**asdict(state), "due_at_days": state.due_at(policy), "memory_at_last_replay_event": state.memory_now(end)}
            for topic, state in sorted(engine.states.get(learner, {}).items())
        }
        runs.append({
            "id": f"{outcome}:{clock}:r{initial_repetitions:g}:growth{growth:g}" + (":literal-add-before-decay" if memory_order == "literal-add-before-decay" else ""),
            "outcome_policy": outcome, "clock_policy": clock,
            "memory_order": memory_order,
            "initial_repetitions_assumption": initial_repetitions,
            "policy": asdict(policy), "policy_id": policy.id, "graph_id": graph.id,
            "event_count": len(traces), "passed_events": sum(event["success"] for event in scenario["events"]),
            "failed_events": sum(not event["success"] for event in scenario["events"]),
            "topic_count": len(topics), "final_states": final_states,
            "observed_review_compatibility": review_compatibility,
            "assumptions": scenario["assumptions"] + [
                f"All {len(topics)} retained topics are assumed previously learned at time zero with repetitions={initial_repetitions:g}, memory=1, accuracy={policy.prior_accuracy}; no initialization/reset information is recoverable.",
                "Encompassing graph is empty, so only direct evidence is replayed; prerequisite links are not imported as practice coverage.",
                "Every emitted event has quality=1; diagnostics and unsampled tasks supply no outcomes. No parameters are fitted to this history.",
            ],
            "traces": traces,
        })
    ranges = {}
    for run in runs:
        for topic, state in run["final_states"].items():
            record = ranges.setdefault(topic, {"minimum_repetitions": state["repetitions"], "maximum_repetitions": state["repetitions"]})
            record["minimum_repetitions"] = min(record["minimum_repetitions"], state["repetitions"])
            record["maximum_repetitions"] = max(record["maximum_repetitions"], state["repetitions"])
    return {
        "schema_version": 1, "source_hashes": {key: audit["sources"][key]["sha256"] for key in ("progress", "question_observations")},
        "implementation_hashes": {
            "core.py": _source(Path(__file__).with_name("core.py"))["sha256"],
            "calibration.py": _source(Path(__file__).with_name("calibration.py"))["sha256"],
            "history.py": _source(Path(__file__))["sha256"],
        },
        "scenario_count": len(runs), "scenarios": runs,
        "final_repetition_ranges_across_assumptions": ranges,
        "verified_production_predictions": 0,
        "interpretation": "These are actual executions of the reconstructed engine on observed answers. Due-at-review agreement is compatibility only: scheduled due values, learner delays, intervening outcomes, and initial state are missing. The partial elapsed clock is a sensitivity control, not recovered exercise time. Distinct resulting states cannot be adjudicated against this history.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--progress", type=Path, default=Path("reference/progress.csv"))
    parser.add_argument("--observations", type=Path, default=Path("reference/mathacademy-xp-observations.json"))
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--replay-output", type=Path)
    args = parser.parse_args()
    result = build_audit(args.progress, args.observations, args.profile, args.catalog)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.replay_output:
        args.replay_output.parent.mkdir(parents=True, exist_ok=True)
        args.replay_output.write_text(json.dumps(run_history_scenarios(result), indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
