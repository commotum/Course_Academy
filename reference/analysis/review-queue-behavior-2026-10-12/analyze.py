"""Read saved queues and failed-review follow-ups; never contact MA or EDB."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "reference/mathacademy"
OUTPUT = Path(__file__).with_name("evidence.json")


def read(path):
    return json.loads(path.read_text())


def relative(path):
    return str(path.relative_to(ROOT))


def dashboard_queue(post):
    dashboard = (post.get("observations") or {}).get("dashboard") or {}
    name = dashboard.get("html_path")
    if not name:
        return None
    path = Path(name)
    if not path.exists():
        raise FileNotFoundError(path)
    # These links are action buttons, unlike topic/history/prerequisite links.
    html = path.read_text()
    matches = re.findall(
        r'<a\b[^>]*\bid="taskStartButton-(\d+)"[^>]*\bhref="([^"]+)"', html
    )
    result = []
    for task, href in matches:
        topic = re.search(r"/topics/(\d+)/(lesson|review)", href)
        result.append({"task_id": task, "topic_id": topic[1] if topic else None,
                       "kind": topic[2] if topic else "other", "href": href})
    return {"path": relative(path), "tasks": result}


counts = {}
all_review = []
legacy_failures = []
paths = list((SOURCE / "question-capture").glob("*/queue-after.json"))
paths += list((SOURCE / "question-capture-workers").glob("*/*/queue-after.json"))
for path in sorted(paths):
    account = path.parent.parent.name if "question-capture-workers" in path.parts else "foundations"
    counts.setdefault(account, Counter())["snapshots"] += 1
    data = read(path)
    queue = data.get("queue") or []
    if queue and all(q.get("task_type") == "review" for q in queue):
        counts[account]["all_review"] += 1
        counts[account]["five_reviews"] += len(queue) == 5
        all_review.append({"account": account, "path": relative(path),
                           "tasks": [q["task_id"] for q in queue],
                           "topics": [q.get("topic_id") for q in queue],
                           "size": len(queue)})
    state_path = path.with_name("state.json")
    if state_path.exists():
        state = read(state_path)
        if state.get("task_type") == "review" and state.get("activity_outcome") == "failed":
            legacy_failures.append({"account": account, "path": relative(state_path),
                                    "task_id": state.get("task_id"),
                                    "topic_id": state.get("topic_id"),
                                    "earned_xp": state.get("earned_xp"),
                                    "sequence": state.get("review_sequence"),
                                    "next_queue_path": relative(path),
                                    "next_queue": [{k: q.get(k) for k in
                                                    ("task_id", "topic_id", "task_type")}
                                                   for q in queue]})

modern_rows = {}
modern_failed = []
modern_count = 0
for path in sorted((SOURCE / "capture").glob("*/*/post-activity.json")):
    modern_count += 1
    post = read(path)
    activity = read(path.with_name("activity.json"))
    completion = post.get("completion") or {}
    account = path.parent.parent.name
    row = {"path": relative(path), "account": account,
           "task_id": str(activity.get("task_id")), "kind": activity.get("kind"),
           "topic_id": str(activity.get("topic_id")),
           "observed_at": post.get("first_observed_at") or post.get("observed_at"),
           "earned_xp": completion.get("earned_xp")}
    modern_rows.setdefault(account, []).append(row)
    # XP alone is not a failure classifier: use the observed terminal message.
    if completion.get("kind") == "review" and "halted due to poor performance" in completion.get("text", ""):
        modern_failed.append({**row, "message": completion.get("text"),
                              "next_queue": dashboard_queue(post)})

for rows in modern_rows.values():
    rows.sort(key=lambda r: r["observed_at"] or 0)
for failure in modern_failed:
    rows = modern_rows[failure["account"]]
    index = next(i for i, r in enumerate(rows) if r["task_id"] == failure["task_id"])
    failure["next_captured_activities"] = rows[index + 1:index + 6]
    failure["later_same_topic"] = [r for r in rows[index + 1:]
                                   if r["topic_id"] == failure["topic_id"]][:6]

result = {
    "scope": "Exact legacy queue-after patterns and modern post-activity patterns; no repair subfolders. Snapshots are not independent episodes. Review origin is not inferred from task-ID order.",
    "legacy_counts": {a: dict(c) for a, c in counts.items()},
    "legacy_distinct_all_review_queues": len({(r["account"], tuple(r["tasks"])) for r in all_review}),
    "legacy_all_review_snapshots": all_review,
    "legacy_explicit_failed_reviews": legacy_failures,
    "modern_post_activity_count": modern_count,
    "modern_explicit_failed_reviews": modern_failed,
    "follow_up_limit": "Next captured completions do not prove uninterrupted full history, first offer time, or why a task was assigned. Failed-review origins are not classified here.",
}
OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"legacy_counts": result["legacy_counts"],
                  "distinct_all_review": result["legacy_distinct_all_review_queues"],
                  "legacy_failed": len(legacy_failures),
                  "modern_posts": modern_count, "modern_failed": len(modern_failed)}, indent=2))
