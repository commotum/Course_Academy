"""Derive quiz intervals and authoritative new dashboard offer times."""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
evidence = json.loads((OUT / "evidence.json").read_text())
records = evidence["records"]
intervals = []
for account, cid in [("linear", "76"), ("linear", "55"), ("differential", "61"),
                     ("multivariable", "54"), ("foundations", "136")]:
    offers = sorted([v for v in evidence["first_old_queue_offers"]
                     if v["account"] == account and v["course_id"] == cid and "Retake" not in v["title"]],
                    key=lambda q: q["time"])
    for previous, offer in zip(offers, offers[1:]):
        previous_record = next(r for r in records if r["account"] == account and r["task_id"] == str(previous["task_id"]))
        start = previous_record["completed_at"]
        rows = [r for r in records if r["account"] == account and r["course_id"] == cid and r.get("complete")
                and r["kind"] in ["lesson", "review", "multistep"] and r.get("completed_at")
                and start < r["completed_at"] < offer["time"]]
        earned = sum(r["xp"]["earned"] or 0 for r in rows if r.get("xp"))
        missing = sum(not r.get("xp") for r in rows)
        intervals.append({"account": account, "course_id": cid, "quiz": offer["title"], "task_id": offer["task_id"],
                          "previous_quiz_task_id": previous["task_id"], "learning_activity_count": len(rows),
                          "missing_xp_records": missing, "earned_learning_xp_since_previous_quiz_completion": earned,
                          "optional_xp_remaining": offer["optional_xp_remaining"],
                          "difference_from_150": earned + (offer["optional_xp_remaining"] or 0) - 150,
                          "source": offer["source"]})
(OUT / "quiz-intervals.json").write_text(json.dumps(intervals, indent=2) + "\n")

offers = {}
for p in (ROOT / "reference/mathacademy/capture").glob("*/*/post-activity.json"):
    d = json.loads(p.read_text())
    dashboard = d.get("observations", {}).get("dashboard", {})
    fn = dashboard.get("html_path")
    if not fn or not Path(fn).exists():
        continue
    text = Path(fn).read_text()
    cid_match = re.search(r'id="courseNameLink"[^>]*href="/courses/(\d+)', text)
    if not cid_match:
        continue
    # Exact unlocked task opening tags stop completed history from qualifying.
    starts = list(re.finditer(r'<div\b[^>]*class="taskUnlocked"[^>]*id="task-(\d+)"[^>]*>|<div\b[^>]*id="task-(\d+)"[^>]*class="taskUnlocked"[^>]*>', text))
    for n, m in enumerate(starts):
        card = text[m.start():starts[n+1].start() if n+1 < len(starts) else len(text)]
        if not re.search(r'taskTypeUnlocked[^>]*>\s*Assessment', card):
            continue
        tid = m.group(1) or m.group(2)
        key = (p.parts[-3], tid)
        t = dashboard.get("captured_at", d.get("observed_at"))
        if key not in offers or t < offers[key]["time"]:
            title = re.search(r'taskNameUnlocked[^>]*>(.*?)</div>', card, re.S)
            offers[key] = {"account": key[0], "course_id": cid_match.group(1), "task_id": tid,
                           "time": t, "title": title.group(1).strip() if title else None,
                           "after_task_id": p.parts[-2], "source": fn}
(OUT / "new-dashboard-offers.json").write_text(json.dumps(list(offers.values()), indent=2) + "\n")
fully_known = [r for r in intervals if r["missing_xp_records"] == 0]
print("Intervals", len(intervals), "complete XP coverage", len(fully_known),
      "exactly 150", sum(r["difference_from_150"] == 0 for r in fully_known))
print("New timestamped quiz offers", len(offers))
for cid in ["154", "76", "155", "145"]:
    rows = [r for r in offers.values() if r["course_id"] == cid]
    print(cid, sorted(rows, key=lambda r: r["time"])[:1])
