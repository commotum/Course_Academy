"""Account observations and retake instructions; never learner database writes."""
from datetime import datetime
from pathlib import Path
import time

from .activity.evidence import correct_grade
from .progress import compare_progress
from .storage import atomic_json, read_json


def _number(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _all_correct(content):
    attempts = content.get("attempts", [])
    return bool(attempts) and all(attempt.get("accepted") and correct_grade(
        attempt.get("grade", attempt.get("feedback", {}).get("grade"))) for attempt in attempts)


def record(config, activity, directory, content, observation):
    directory = Path(directory)
    observed_at = observation.get("observed_at", time.time())
    previous = read_json(directory / "post-activity.json", {})
    completion = {**content.get("completion", {}), **previous.get("completion", {}),
                  **{key: value for key, value in observation.get("completion", {}).items() if value is not None}}
    for key in ("earned_xp", "base_xp", "outcome"):
        if key not in completion and key in observation:
            completion[key] = observation[key]
        if key not in completion and key in content:
            completion[key] = content[key]
    task_id = activity["task_id"]
    marker = directory / "capture-complete.json"
    completed_at = read_json(marker, {}).get("completed_at")
    if completed_at is None:
        completed_at = marker.stat().st_mtime if marker.exists() else observed_at
    earned = _number(completion.get("earned_xp"))
    ledger_path = config.state_root / "xp.json"
    ledger = read_json(ledger_path, {})
    existing = ledger.get(task_id, {})
    base = _number(completion.get("base_xp"))
    ledger[task_id] = {**existing, "task_id": task_id, "kind": activity["kind"],
        "date": existing.get("date", datetime.fromtimestamp(completed_at).astimezone().date().isoformat()),
        "observed_at": observed_at, "earned_xp": earned if earned is not None else existing.get("earned_xp"),
        "base_xp": base if base is not None else existing.get("base_xp"),
        "outcome": completion.get("outcome", existing.get("outcome")), "source": str(directory)}
    atomic_json(ledger_path, ledger)
    totals = {}
    for entry in ledger.values():
        daily = totals.setdefault(entry["date"], {"earned_xp": 0, "counted_tasks": 0, "unknown_tasks": 0})
        xp = _number(entry.get("earned_xp"))
        if xp is None:
            daily["unknown_tasks"] += 1
        else:
            daily["earned_xp"] += xp
            daily["counted_tasks"] += 1
    atomic_json(config.state_root / "daily-xp.json", totals)
    retakes_path = config.state_root / "retakes.json"
    retakes = read_json(retakes_path, {})
    key = activity["kind"] + ":" + str(activity.get("topic_id") or "")
    previous_rule = retakes.get(key, {})
    if activity["kind"] in ("lesson", "review") and completed_at >= previous_rule.get("completed_at", 0):
        if earned is not None and earned < 0:
            retakes[key] = {"force_correct": True, "task_id": task_id, "reason": "negative_xp", "completed_at": completed_at}
        elif activity.get("details", {}).get("force_correct") and earned is not None and earned >= 0 and _all_correct(content):
            retakes[key] = {"force_correct": False, "task_id": task_id, "reason": "all_correct_retake_completed", "completed_at": completed_at}
        elif earned is None:
            retakes[key] = {"force_correct": True, "task_id": task_id, "reason": "previous_outcome_unavailable", "completed_at": completed_at}
        elif previous_rule.get("task_id") == task_id and previous_rule.get("reason") == "previous_outcome_unavailable":
            retakes[key] = {"force_correct": False, "task_id": task_id, "reason": "completion_evidence_recovered", "completed_at": completed_at}
    atomic_json(retakes_path, retakes)
    prior_progress = read_json(config.state_root / "progress.json", {})
    progress = observation.get("progress") or observation.get("courses")
    # Preserve the immediate baseline even when the first progress read fails.
    # Later reads describe the account at their own read time, not task completion.
    if not (directory / "progress-before.json").exists():
        atomic_json(directory / "progress-before.json", prior_progress)
    baseline = read_json(directory / "progress-before.json", {})
    comparison = compare_progress(baseline, {**observation, 'observed_at': observed_at})
    comparison.update(task_id=task_id, baseline_source='progress-before.json')
    atomic_json(directory / "progress-comparison.json", comparison)
    if progress and observed_at >= prior_progress.get("observed_at", 0):
        atomic_json(config.state_root / "progress.json", {"observed_at": observed_at, "progress": progress})
    history = list(previous.get("observation_history", []))
    if not history and previous.get("observations") is not None:
        history.append({"observed_at": previous.get("observed_at"), "observations": previous["observations"]})
    entry = {"observed_at": observed_at, "observations": observation, "progress_comparison": comparison}
    existing_read = next((index for index, item in enumerate(history)
                         if item.get('observed_at') == observed_at and item.get('observations') == observation), None)
    if existing_read is None:
        history.append(entry)
    else:
        history[existing_read] = {**history[existing_read], **entry}
    atomic_json(directory / "post-activity.json", {**previous,
        "first_observed_at": previous.get("first_observed_at", previous.get("observed_at", observed_at)),
        "observed_at": observed_at, "completion": completion,
        "observations": observation, "observation_history": history, "progress_comparison": comparison,
        "accounting_complete": True,
        "missing_observations": observation.get("missing", observation.get("pending_reads", [])), "learner_database_writes": 0})
    return completion


def retake_policy(config, activity):
    records = read_json(config.state_root / "retakes.json", {})
    key = activity["kind"] + ":" + str(activity.get("topic_id") or "")
    rule = records.get(key)
    if rule:
        activity = {**activity, "details": {**activity.get("details", {}), **rule}}
    return activity
