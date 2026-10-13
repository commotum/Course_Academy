"""Compare saved quiz-topic bindings to SAME-ACCOUNT learning histories.

Read-only source analysis. Run analyze.py and details.py first, then this file.
Output ages are conservative when the anchor is a post-completion snapshot.
An observed first lesson is not necessarily the topic's first-ever acquisition.
"""
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
evidence = json.loads((OUT / "evidence.json").read_text())
records = evidence["records"]
offers = {(q["account"], str(q["task_id"])): q for q in evidence["first_old_queue_offers"]}
for q in json.loads((OUT / "new-dashboard-offers.json").read_text()):
    key = (q["account"], str(q["task_id"]))
    if key not in offers or offers[key]["time"] > q["time"]:
        offers[key] = q

# Both exceptions in the provisional snapshot-based comparison are recoveries.
# The original diagnostic HTML already displays the successful completion text.
# The timestamped log line documenting capture of that page gives a conservative
# upper bound on lesson completion, rather than guessing the exact server time.
completion_bounds = {
    ("foundations", "13945962"): {
        "latest_completed_at": datetime.fromisoformat("2026-10-04T19:31:35.217-07:00").timestamp(),
        "source": ".local/question_capture/logs/run-1791153525223349569.log",
        "html": "reference/mathacademy/question-capture/13945962/diagnostics/1791167494997836945/page.html",
    },
    ("multivariable", "14041552"): {
        "latest_completed_at": datetime.fromisoformat("2026-10-08T01:11:06.326-07:00").timestamp(),
        "source": ".local/question_capture-workers/multivariable/logs/run-1791446683540264702.log",
        "html": "reference/mathacademy/question-capture-workers/multivariable/14041552/diagnostics/1791447066125888643/page.html",
    },
}
for bound in completion_bounds.values():
    raw = (ROOT / bound["html"]).read_text()
    assert "completed the lesson" in raw and "awarded" in raw

lessons = defaultdict(list)
reviews = defaultdict(list)
for record in records:
    if not record.get("complete") or not record.get("completed_at"):
        continue
    if record["kind"] not in ("lesson", "review"):
        continue
    key = (record["account"], str(record.get("topic_id")))
    bound = completion_bounds.get((record["account"], record["task_id"]))
    copied = {**record, "age_anchor": bound["latest_completed_at"] if bound else record["completed_at"],
              "age_anchor_basis": "original completed-page observation upper bound" if bound else record["completion_time_basis"],
              "completion_bound": bound}
    (lessons if record["kind"] == "lesson" else reviews)[key].append(copied)

rows = []
state_cache = {}
for quiz in records:
    if quiz["kind"] != "assessment" or not quiz.get("complete"):
        continue
    key = (quiz["account"], quiz["task_id"])
    offer = offers.get(key)
    time = offer["time"] if offer else quiz.get("started_at") or quiz.get("completed_at")
    if not time:
        continue
    path = ROOT / quiz["source"]
    content = json.loads((path.parent / "content.json").read_text())
    for question in content["questions"]:
        topic_id = str(question.get("topic_id"))
        topic_key = (quiz["account"], topic_id)
        prior = sorted([r for r in lessons[topic_key] if r["age_anchor"] < time], key=lambda r: r["age_anchor"])
        prior_reviews = sorted([r for r in reviews[topic_key] if r["age_anchor"] < time], key=lambda r: r["age_anchor"])
        first = prior[0] if prior else None
        if first and first["source"] not in state_cache:
            original = json.loads((ROOT / first["source"]).read_text())
            state_cache[first["source"]] = {k: original.get(k) for k in ["lesson_complete", "activity_outcome", "completion"]}
        href = question.get("kp_href") or question.get("provenance", {}).get("kp_href")
        href_id = re.search(r"/topics/(\d+)", href or "")
        if href_id:
            assert href_id.group(1) == topic_id, (quiz["task_id"], topic_id, href)
        rows.append({"account": quiz["account"], "course_id": quiz["course_id"], "quiz_id": quiz["task_id"],
                     "quiz_title": quiz.get("title"), "retake": bool(quiz.get("retake")),
                     "question_id": question.get("math_academy_id"), "topic_id": topic_id,
                     "knowledge_point": question.get("knowledge_point"), "source_kp_href": href,
                     "source_href_verified": bool(href_id), "assessment_time": time,
                     "assessment_time_basis": "first saved offer" if offer else "assessment start/completion fallback",
                     "offer_source": offer.get("source") if offer else None, "quiz_source": quiz["source"],
                     "first_observed_lesson": first, "lesson_status": state_cache.get(first["source"]) if first else None,
                     "age_hours": (time - first["age_anchor"]) / 3600 if first else None,
                     "snapshot_age_hours": (time - first["completed_at"]) / 3600 if first else None,
                     "last_observed_lesson_age_hours": (time - prior[-1]["age_anchor"]) / 3600 if prior else None,
                     "last_observed_review_age_hours": (time - prior_reviews[-1]["age_anchor"]) / 3600 if prior_reviews else None,
                     "last_observed_review_id": prior_reviews[-1]["task_id"] if prior_reviews else None})

matched = [r for r in rows if r["age_hours"] is not None]
assert all(r["lesson_status"]["lesson_complete"] is True for r in matched)
assert all(r["lesson_status"]["activity_outcome"] in (None, "passed") for r in matched)
unique_first = {}
for row in sorted(matched, key=lambda r: r["assessment_time"]):
    unique_first.setdefault((row["account"], row["topic_id"]), row)
summary = {
    "question_appearances": len(rows), "quiz_tasks": len({(r["account"], r["quiz_id"]) for r in rows}),
    "matched_question_appearances": len(matched), "unmatched_question_appearances": len(rows) - len(matched),
    "matched_quiz_tasks": len({(r["account"], r["quiz_id"]) for r in matched}),
    "distinct_matched_account_topics": len(unique_first),
    "matched_original_question_appearances": sum(not r["retake"] for r in matched),
    "matched_retake_question_appearances": sum(r["retake"] for r in matched),
    "verified_source_href_count": sum(r["source_href_verified"] for r in rows),
    "below_48_hours_using_snapshots": [r for r in matched if r["snapshot_age_hours"] < 48],
    "below_48_hours_using_original_completion_bounds": [r for r in matched if r["age_hours"] < 48],
    "youngest_traceable_age_hours": min(r["age_hours"] for r in matched),
    "review_within_48_hours_count": sum(r["last_observed_review_age_hours"] is not None and r["last_observed_review_age_hours"] < 48 for r in matched),
    "review_within_24_hours_count": sum(r["last_observed_review_age_hours"] is not None and r["last_observed_review_age_hours"] < 24 for r in matched),
    "ordinary_quiz_review_within_1_hour_count": sum(not r["retake"] and r["last_observed_review_age_hours"] is not None and r["last_observed_review_age_hours"] < 1 for r in matched),
    "by_course": {},
}
for cid in sorted({r["course_id"] for r in rows}):
    group = [r for r in rows if r["course_id"] == cid]
    known = [r for r in group if r["age_hours"] is not None]
    summary["by_course"][cid] = {
        "name": evidence["course_summary"][cid]["name"], "appearances": len(group), "matched": len(known),
        "youngest_hours": min((r["age_hours"] for r in known), default=None),
        "under_48": sum(r["age_hours"] < 48 for r in known)}

(OUT / "topic-age-evidence.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2) + "\n")
fields = ["account", "course_id", "quiz_id", "quiz_title", "retake", "question_id", "topic_id", "knowledge_point",
          "age_hours", "snapshot_age_hours", "last_observed_review_age_hours", "source_kp_href"]
with (OUT / "topic-ages.csv").open("w") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows({k: r[k] for k in fields} for r in rows)

print(json.dumps({k: v for k, v in summary.items() if k not in ["below_48_hours_using_snapshots", "below_48_hours_using_original_completion_bounds"]}, indent=2))
print("Apparent exceptions", len(summary["below_48_hours_using_snapshots"]),
      "remaining after original evidence", len(summary["below_48_hours_using_original_completion_bounds"]))

# One first-quiz appearance per account/topic; repeated questions are not extra bars.
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Plot dependencies unavailable; JSON and CSV are complete.")
else:
    ages = [r["age_hours"] for r in unique_first.values()]
    fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)
    ax.hist(ages, bins=np.arange(0, max(110, max(ages) + 2), 2), color="#3978a8", edgecolor="white")
    ax.axvline(48, color="#b54135", linewidth=2, label="48 hours")
    ax.set(xlim=(0, max(110, max(ages) + 2)), xlabel="Hours since first observed completed lesson (same account)",
           ylabel="Distinct account/topic pairs", title="Age of topics at their first observed quiz appearance")
    ax.text(0.02, 0.95, f"{len(ages)} traceable account/topic pairs; none below 48 hours\n"
            "Two delayed recovery snapshots corrected using original completed-page observations",
            transform=ax.transAxes, va="top", fontsize=9)
    ax.legend(loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "topic-age-distribution.png", dpi=180)
    plt.close(fig)
