"""Read-only negative controls and conditional age-crossing forecasts.

Run after analyze.py and topic_age.py. Writes derived audit evidence only.
Historical lesson coverage is not the service's current eligible-topic pool.
"""
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
evidence = json.loads((OUT / "evidence.json").read_text())
ages = json.loads((OUT / "topic-age-evidence.json").read_text())
records = evidence["records"]
lessons = [r for r in records if r["kind"] == "lesson" and r.get("complete") and r.get("completed_at")]
zone = ZoneInfo("America/Los_Angeles")

def unique_prior(account, time):
    result = {}
    for r in sorted(lessons, key=lambda r: r["completed_at"]):
        if r["account"] == account and r["completed_at"] < time:
            result.setdefault(str(r["topic_id"]), r)
    return result

def native_topics(account, cid):
    metric = next(m for m in evidence["xp_topic_membership_metrics"] if m["account"] == account and m["course_id"] == cid)
    with Path(metric["membership_source"]).open() as handle:
        return {r["topic-id"] for r in csv.DictReader(handle)}

queue = next(q for q in evidence["queues"] if str(q.get("after_task_id")) == "14072172")
diag = next(d for d in evidence["diagnostics"] if d["account"] == "linear" and d["course_id"] == "55")
prior = unique_prior("linear", queue["time"])
native = native_topics("linear", "55")
negative_control = {
    "queue": queue,
    "hours_after_diagnostic": (queue["time"] - diag["completed_at"]) / 3600,
    "distinct_observed_learned_topics": len(prior),
    "observed_topics_at_least_24h": sum(queue["time"] - r["completed_at"] >= 24*3600 for r in prior.values()),
    "observed_native_topics_at_least_24h": sum(t in native and queue["time"] - r["completed_at"] >= 24*3600 for t,r in prior.items()),
    "observed_topics_at_least_48h": sum(queue["time"] - r["completed_at"] >= 48*3600 for r in prior.values()),
    "any_in_progress": any(t["in_progress"] for t in queue["tasks"]),
}

new_courses = []
for account, cid, diag_id in [("multivariable", "155", "14111253"), ("differential", "145", "14110945")]:
    diag = next(d for d in evidence["diagnostics"] if d["account"] == account and d["task_id"] == diag_id)
    source = f"reference/mathacademy/capture/{account}/{diag_id}/post-activity.json"
    obs = json.loads((ROOT / source).read_text())["observations"]
    course = next(c for c in obs["courses"] if c["course_id"] == cid)
    topics = {t["topic_id"]: t for t in course["topics"]}
    current = [r for r in lessons if r["account"] == account and r["course_id"] == cid and r["completed_at"] > diag["completed_at"]]
    last = max(r["completed_at"] for r in current)
    before = unique_prior(account, diag["completed_at"])
    older = {t:r for t,r in before.items() if t in topics and last-r["completed_at"] >= 48*3600}
    quizzed = {r["topic_id"] for r in ages["rows"] if r["account"] == account and r["assessment_time"] < diag["completed_at"]}
    first_new = {}
    for r in sorted(current, key=lambda r: r["completed_at"]):
        if r["topic_id"] in topics:
            first_new.setdefault(r["topic_id"], r)
    new_courses.append({
        "account": account, "course_id": cid, "post_diagnostic_source": source,
        "post_diagnostic_band_counts": dict(Counter(t["display_band"] for t in topics.values())),
        "historical_native_lesson_topics_48h_by_last_activity": len(older),
        "historical_older_topic_bands_after_diagnostic": dict(Counter(topics[t]["display_band"] for t in older)),
        "historical_older_blue_unquizzed": sum(topics[t]["display_band"] > 0 and t not in quizzed for t in older),
        "historical_older_previously_quizzed": sum(t in quizzed for t in older),
        "new_lesson_activity_count": len(current),
        "repeated_previously_captured_lesson_activity_count": sum(r["topic_id"] in before for r in current),
        "first_six_native_post_diagnostic_lessons": [{
            "task_id": r["task_id"], "topic_id": r["topic_id"], "title": r["title"],
            "previously_captured_lesson": r["topic_id"] in before,
            "completed_local": datetime.fromtimestamp(r["completed_at"],zone).isoformat(),
            "conditional_48h_crossing_local": datetime.fromtimestamp(r["completed_at"]+48*3600,zone).isoformat(),
            "source": r["source"],
        } for r in list(first_new.values())[:6]],
    })

payload = {"negative_control": negative_control, "courses_without_quizzes": new_courses,
           "limitations": ["Historical first observed lessons are not current service eligibility.",
                           "Forecasts concern recorded post-diagnostic learning timestamps, not promised quiz offers.",
                           "No runners or website actions were initiated."]}
(OUT / "topic-age-controls.json").write_text(json.dumps(payload, indent=2)+"\n")
print(json.dumps(payload, indent=2))
