"""Trace saved failed lessons to later offers and completed attempts, read-only."""
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "reference/mathacademy"
OUT = Path(__file__).parent


def read(path):
    return json.loads(path.read_text())


def rel(path):
    return str(path.relative_to(ROOT))


def epoch(value):
    return datetime.fromisoformat(value).timestamp() if value else None


records = []
queues = []
legacy = list((SOURCE / "question-capture").glob("*/state.json"))
legacy += list((SOURCE / "question-capture-workers").glob("*/*/state.json"))
for path in sorted(legacy):
    s = read(path)
    account = path.parent.parent.name if "question-capture-workers" in path.parts else "foundations"
    kind = s.get("task_type")
    snap = (s.get("knowledge_snapshots") or {}).get(str(kind) + "-completed") or {}
    at = epoch(snap.get("finished_at"))
    if at is None:
        continue
    row = {"account": account, "task_id": str(s.get("task_id")),
           "topic_id": str(s.get("topic_id")), "kind": kind, "at": at,
           "source": rel(path), "time_basis": "completion progress-capture time",
           "xp": s.get("earned_xp"), "failed": s.get("activity_outcome") == "failed",
           "failure_kp": s.get("current_kp"), "message": s.get("completion", "")[:450]}
    records.append(row)
    qp = path.with_name("queue-after.json")
    if qp.exists():
        q = read(qp)
        queues.append({"account": account, "at": at, "source": rel(qp),
                       "time_basis": "associated completion progress-capture time, approximate",
                       "tasks": [{"task_id": str(t.get("task_id")),
                                  "topic_id": str(t.get("topic_id")), "kind": t.get("task_type")}
                                 for t in q.get("queue", [])]})

seen_dashboards = set()
modern_paths = list((SOURCE / "capture").glob("*/*/post-activity.json"))
for path in sorted(modern_paths):
    p = read(path)
    a = read(path.with_name("activity.json"))
    c = p.get("completion") or {}
    account = path.parent.parent.name
    at = p.get("first_observed_at") or p.get("observed_at")
    if not c or at is None:
        continue
    failed = "halted due to poor performance" in c.get("text", "")
    row = {"account": account, "task_id": str(a.get("task_id")),
           "topic_id": str(a.get("topic_id")), "kind": a.get("kind"), "at": at,
           "source": rel(path), "time_basis": "first completion observation",
           "xp": c.get("earned_xp"), "failed": failed, "message": c.get("text", "")[:450]}
    events = path.with_name("activity-events.jsonl")
    if events.exists():
        times = [e["at"] for line in events.read_text().splitlines()
                 if (e := json.loads(line)).get("event") == "judgment_saved" and e.get("at")]
        row["first_judgment_at"] = min(times) if times else None
    records.append(row)
    observations = [p.get("observations") or {}]
    observations += [h.get("observations") or {} for h in p.get("observation_history", [])]
    for observation in observations:
        d = observation.get("dashboard") or {}
        name, captured = d.get("html_path"), d.get("captured_at")
        if not name or captured is None or name in seen_dashboards:
            continue
        seen_dashboards.add(name)
        html = Path(name).read_text()
        tasks = []
        for task, href in re.findall(r'<a\b[^>]*\bid="taskStartButton-(\d+)"[^>]*\bhref="([^"]+)"', html):
            match = re.search(r"/topics/(\d+)/(lesson|review)", href)
            tasks.append({"task_id": task, "topic_id": match[1] if match else None,
                          "kind": match[2] if match else "other"})
        queues.append({"account": account, "at": captured, "source": rel(Path(name)),
                       "time_basis": "saved dashboard capture time", "tasks": tasks})

records.sort(key=lambda r: r["at"])
queues.sort(key=lambda r: r["at"])
failures = []
for failure in [r for r in records if r["kind"] == "lesson" and r["failed"]]:
    account, topic, at = failure["account"], failure["topic_id"], failure["at"]
    later = [r for r in records if r["account"] == account and r["at"] > at]
    retry = next((r for r in later if r["kind"] == "lesson" and r["topic_id"] == topic
                  and r["task_id"] != failure["task_id"]), None)
    same_queues = [q for q in queues if q["account"] == account and q["at"] >= at]
    offer = next((q for q in same_queues if any(t["kind"] == "lesson" and str(t["topic_id"]) == topic
                  and t["task_id"] != failure["task_id"] for t in q["tasks"])), None)
    absent = [q for q in same_queues if offer and q["at"] < offer["at"] and
              not any(t["kind"] == "lesson" and str(t["topic_id"]) == topic for t in q["tasks"])]
    row = dict(failure)
    row["next_same_topic_lesson"] = retry
    row["first_later_lesson_offer"] = offer
    row["last_absent_before_offer"] = absent[-1] if absent else None
    for label, end in [("offer", offer), ("retry_completion", retry)]:
        if not end:
            continue
        # Completion whose dashboard supplies the first offer is intervening work.
        between = [r for r in later if r["at"] <= end["at"] and r["task_id"] != (retry or {}).get("task_id")]
        practice = [r for r in between if r["kind"] in ("lesson", "review", "multistep", "assignment")]
        row[label + "_elapsed_hours"] = (end["at"] - at) / 3600
        row[label + "_intervening_activities"] = len(between)
        row[label + "_practice_xp"] = sum(r["xp"] for r in practice if isinstance(r.get("xp"), (int, float)))
        row[label + "_practice_awards_missing"] = sum(not isinstance(r.get("xp"), (int, float)) for r in practice)
        row[label + "_activity_counts"] = dict(Counter(r["kind"] for r in between))
        row[label + "_successful_practice_count"] = sum(not r["failed"] for r in practice)
    if offer and absent:
        before_offer = [r for r in later if r["at"] <= absent[-1]["at"]
                        and r["kind"] in ("lesson", "review", "multistep", "assignment")]
        row["last_absent_practice_count"] = len(before_offer)
        row["last_absent_successful_practice_count"] = sum(not r["failed"] for r in before_offer)
    if retry:
        def question_ids(source):
            directory = ROOT / Path(source).parent
            state_path = directory / "state.json"
            if state_path.exists():
                return set(read(state_path).get("questions", {}))
            content = read(directory / "content.json")
            return {str(q["math_academy_id"]) for q in content.get("questions", [])
                    if q.get("math_academy_id")}
        row["reused_observed_question_ids"] = sorted(question_ids(failure["source"]) & question_ids(retry["source"]))
    failures.append(row)

result = {"record_count": len(records), "queue_count": len(queues), "modern_post_count": len(modern_paths),
          "failures": failures,
          "limits": ["Observation times can be later than backend completion; legacy queue times are approximate associated progress captures.",
                     "First observed offer is not first eligibility; dashboard ranking, prerequisites, and course changes can affect visibility.",
                     "Intervening XP and activity counts cover captured completions, not necessarily all account work.",
                     "Successful-practice counts use completed records without an explicit failure status/message; legacy missing outcome fields are not independently regraded.",
                     "Capture agents select work and intentionally choose answer patterns; selected retry timing is not a required delay.",
                     "A currently missing follow-up is right-censored, not evidence that retries are prohibited."]}
(OUT / "evidence.json").write_text(json.dumps(result, indent=2) + "\n")
print("records", len(records), "queues", len(queues), "failed lessons", len(failures))
for r in failures:
    offer = r.get("first_later_lesson_offer")
    retry = r.get("next_same_topic_lesson")
    print(r["account"], r["task_id"], "topic", r["topic_id"], "offer", [round(r.get("offer_elapsed_hours", 0), 2),
          r.get("offer_intervening_activities"), r.get("offer_practice_xp")] if offer else None,
          "retry", retry["task_id"] if retry else None,
          "retry h", round(r.get("retry_completion_elapsed_hours", 0), 2) if retry else None)
