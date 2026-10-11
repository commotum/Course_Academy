"""Normalize source queue records without discarding their details."""
from __future__ import annotations

import re

KINDS = {"lesson", "review", "assessment", "diagnostic", "multistep"}


def activity_kind(value):
    value = str(value or "").strip().lower()
    if "diagnostic" in value or "placement" in value:
        return "diagnostic"
    if "multi" in value or value == "assignment":
        return "multistep"
    if "assessment" in value or "quiz" in value or "exam" in value:
        return "assessment"
    if "lesson" in value:
        return "lesson"
    if "review" in value:
        return "review"
    return value


def normalize_activity(raw, position=0):
    item = dict(raw)
    item["kind"] = activity_kind(item.get("kind") or item.get("task_type") or item.get("type"))
    item["task_id"] = str(item.get("task_id") or item.get("id") or "")
    if not item["task_id"] or not re.fullmatch(r"[A-Za-z0-9_-]+", item["task_id"]):
        raise ValueError("Activity requires a valid source task ID")
    item.setdefault("title", "")
    item.setdefault("url", item.get("href", ""))
    item.setdefault("details", {})
    if not isinstance(item["details"], dict):
        item["details"] = {"text": item["details"]}
    item["started"] = bool(item.get("started") or item.get("in_progress") or item.get("resume"))
    item["position"] = int(item.get("position", position))
    for key in ("course_id", "topic_id"):
        if item.get(key) is not None:
            item[key] = str(item[key])
    return item
