"""Account observations and retake instructions; never learner database writes."""
from datetime import datetime
from pathlib import Path
import time

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


def record(config, activity, directory, content, observation):
    directory = Path(directory)
    observed_at = observation.get("observed_at", time.time())
    completion = {**content.get("completion", {}), **observation.get("completion", {})}
    for key in ("earned_xp", "base_xp", "outcome"):
        if key not in completion and key in observation:
            completion[key] = observation[key]
        if key not in completion and key in content:
            completion[key] = content[key]
    task_id = activity["task_id"]
    completed_at = (directory / "capture-complete.json").stat().st_mtime if (directory / "capture-complete.json").exists() else observed_at
    earned = _number(completion.get("earned_xp"))
    ledger_path = config.state_root / "xp.json"
    ledger = read_json(ledger_path, {})
    existing = ledger.get(task_id, {})
    ledger[task_id] = {**existing, "task_id": task_id, "kind": activity["kind"],
        "date": existing.get("date", datetime.fromtimestamp(completed_at).astimezone().date().isoformat()),
        "observed_at": observed_at, "earned_xp": earned if earned is not None else existing.get("earned_xp"),
        "base_xp": _number(completion.get("base_xp")) or existing.get("base_xp"),
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
        elif activity.get("details", {}).get("force_correct") and earned is not None and earned >= 0:
            retakes[key] = {"force_correct": False, "task_id": task_id, "reason": "all_correct_retake_completed", "completed_at": completed_at}
        elif earned is None:
            retakes[key] = {"force_correct": True, "task_id": task_id, "reason": "previous_outcome_unavailable", "completed_at": completed_at}
        elif previous_rule.get("task_id") == task_id and previous_rule.get("reason") == "previous_outcome_unavailable":
            retakes[key] = {"force_correct": False, "task_id": task_id, "reason": "completion_evidence_recovered", "completed_at": completed_at}
    atomic_json(retakes_path, retakes)
    prior_progress = read_json(config.state_root / "progress.json", {})
    progress = observation.get("progress") or observation.get("courses")
    if progress:
        atomic_json(directory / "progress-before.json", prior_progress)
        atomic_json(config.state_root / "progress.json", {"observed_at": observed_at, "progress": progress})
    atomic_json(directory / "post-activity.json", {"observed_at": observed_at, "completion": completion,
        "observations": observation, "accounting_complete": True,
        "missing_observations": observation.get("missing", observation.get("pending_reads", [])), "learner_database_writes": 0})
    return completion


def retake_policy(config, activity):
    records = read_json(config.state_root / "retakes.json", {})
    key = activity["kind"] + ":" + str(activity.get("topic_id") or "")
    rule = records.get(key)
    if rule:
        activity = {**activity, "details": {**activity.get("details", {}), **rule}}
    return activity
