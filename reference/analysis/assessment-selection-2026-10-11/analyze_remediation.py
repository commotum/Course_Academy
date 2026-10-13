"""Separate assessment retakes, missed-topic follow-ups, and intervening practice.

Uses the frozen EDB-rated assessment snapshot and its indexed source documents;
does not query or modify the database, schema, engine, or source captures.
"""
from pathlib import Path
import collections
import csv
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREVIOUS = ROOT / "reference/analysis/question-difficulty-2026-10-11"
BANDS = ("easy", "moderate", "hard")


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def distribution(rows, field="database_difficulty"):
    counts = collections.Counter(r.get(field) for r in rows)
    n = sum(counts[b] for b in BANDS)
    return {
        "rated_questions": n,
        "counts": {b: counts[b] for b in BANDS},
        "percent": {b: round(100 * counts[b] / n, 2) if n else None for b in BANDS},
    }


def write_csv(name, rows):
    assert rows
    with (OUT / name).open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


previous_summary = json.loads((OUT / "summary.json").read_text())
questions = read_csv(OUT / "assessment-questions.csv")
tasks = {t["task_id"]: t for t in read_csv(OUT / "assessment-tasks.csv")}
by_task = collections.defaultdict(list)
for q in questions:
    by_task[q["task_id"]].append(q)
indexed_tasks = {t["task_id"]: t for t in json.loads((PREVIOUS / "source-tasks.json").read_text())}
appearances = collections.defaultdict(list)
for line in (PREVIOUS / "source-appearances.jsonl").read_text().splitlines():
    row = json.loads(line)
    appearances[row["task_id"]].append(row)
ratings = {r["question_mid"]: r["difficulty"] for r in read_csv(PREVIOUS / "rated-questions.csv")}
progress = read_csv(ROOT / "reference/progress.csv")

retake_rows = []
pair_rows = []
practice_tasks = []
practice_rows = []
for pair in previous_summary["retakes"]:
    original = tasks[pair["original"]]
    retake = tasks[pair["retake"]]
    source = ROOT / original["source_file"]
    content = json.loads(source.read_text())
    state_path = source.parent / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    expired = bool(content.get("recovery", {}).get("expired_unanswered") or
                   state.get("recovery", {}).get("expired_unanswered"))
    missed = {q["topic_mid"]: q for q in by_task[pair["original"]]
              if q["grade"].lower() == "incorrect"}
    assert pair["shared_question_ids"] == 0
    assert pair["shared_topics"] == pair["retake_topics"]
    pair_rows.append({**pair, "stream": original["stream"], "expired_unanswered_original": expired,
                      "original_source_file": original["source_file"],
                      "retake_source_file": retake["source_file"],
                      "original_completion": state.get("completion", "")})
    for q in by_task[pair["retake"]]:
        old = missed.get(q["topic_mid"])
        retake_rows.append({**q, "original_task_id": pair["original"],
                           "expired_unanswered_original": expired,
                           "original_topic_missed": old is not None,
                           "original_missed_question": old["question_mid"] if old else "",
                           "original_missed_difficulty": old["database_difficulty"] if old else "",
                           "same_knowledge_point_as_miss": old["kp_href"] == q["kp_href"] if old else ""})
    if original["stream"] != "human-history":
        continue
    # Human completion timestamps are recorded directly in progress.csv.
    # Match only practice between the failed quiz and its named retake.
    for event in sorted(progress, key=lambda r: r["completed-at"]):
        if not (original["completed_at"] < event["completed-at"] < retake["completed_at"]):
            continue
        if event["topic-id"] not in missed or event["activity-type"] not in ("Review", "Lesson"):
            continue
        tid = event["task-id"]
        qs = appearances.get(tid, [])
        practice_tasks.append({"original_task_id": pair["original"], "retake_task_id": pair["retake"],
                               "practice_task_id": tid, "activity_type": event["activity-type"].lower(),
                               "topic_mid": event["topic-id"], "topic_title": event["topic-name"],
                               "completed_at": event["completed-at"], "captured_questions": len(qs),
                               "source_file": indexed_tasks.get(tid, {}).get("source_file", "")})
        for q in qs:
            practice_rows.append({**q, "original_task_id": pair["original"],
                                  "retake_task_id": pair["retake"], "topic_mid": event["topic-id"],
                                  "database_difficulty": ratings.get(q["question_mid"], "")})

# Follow an observed assessment miss to its first subsequent captured assessment
# question on the same topic, within one capture account. Review success is not
# interpreted here: these are later rechecks, not proof of pending remediation.
later_rows = []
pending_by_account = collections.defaultdict(dict)
for task in sorted(tasks.values(), key=lambda t: (t["account_group"], t["completed_at"], t["task_id"])):
    pending = pending_by_account[task["account_group"]]
    for q in by_task[task["task_id"]]:
        prior = pending.pop(q["topic_mid"], None)
        if prior is not None:
            later_rows.append({**q, "prior_missed_task_id": prior["task_id"],
                               "prior_missed_question": prior["question_mid"],
                               "prior_missed_difficulty": prior["database_difficulty"],
                               "later_assessment_is_retake": task["retake"] == "True",
                               "same_knowledge_point_as_miss": prior["kp_href"] == q["kp_href"]})
        if q["grade"].lower() == "incorrect":
            pending[q["topic_mid"]] = q

nonexpired = [q for q in retake_rows if not q["expired_unanswered_original"]]
missed_rechecks = [q for q in retake_rows if q["original_topic_missed"]]
later_regular = [q for q in later_rows if not q["later_assessment_is_retake"]]
expired_originals = {p["original"] for p in pair_rows if p["expired_unanswered_original"]}
summary = {
    "assessment_snapshot": previous_summary["snapshot"],
    "practice_ratings_snapshot": json.loads((PREVIOUS / "snapshot.json").read_text()),
    "retake_pairs": pair_rows,
    "all_retake_questions": distribution(retake_rows),
    "retakes_excluding_expired_original": distribution(nonexpired),
    "human_retake_questions": distribution([q for q in retake_rows if q["stream"] == "human-history"]),
    "retake_rechecks_of_original_missed_topics": distribution(missed_rechecks),
    "retake_missed_topic_rechecks_excluding_expired_original": distribution(
        [q for q in missed_rechecks if not q["expired_unanswered_original"]]),
    "later_regular_quiz_rechecks": distribution(later_regular),
    "later_regular_quiz_rechecks_excluding_expired_original": distribution(
        [q for q in later_regular if q["prior_missed_task_id"] not in expired_originals]),
    "human_later_regular_quiz_rechecks": distribution([q for q in later_regular if q["stream"] == "human-history"]),
    "human_intervening_practice_tasks": dict(collections.Counter(t["activity_type"] for t in practice_tasks)),
    "human_intervening_practice_questions": {
        kind: distribution([q for q in practice_rows if q["activity_type"] == kind])
        for kind in ("review", "lesson")
    },
    "human_intervening_practice_source_questions": {
        kind: distribution([q for q in practice_rows if q["activity_type"] == kind], "source_difficulty")
        for kind in ("review", "lesson")
    },
    "proposed_weights": {"initial": [50, 40, 10], "remedial": [45, 40, 15]},
    "limits": [
        "Retake sample: eight quizzes, including only three human quizzes; automated answering policies affect performance.",
        "One original quiz expired unanswered; source Incorrect labels do not establish attempted mistakes there.",
        "Observed proportions are served questions, affected by topic, knowledge-point, and question supply; they do not recover Math Academy's sampling formula.",
        "Later regular quizzes are linked to first subsequent captured same-topic questions; intervening reviews may already have resolved the miss.",
        "Practice links match recorded human topic and completion time; incomplete captures prevent counts from being a full inventory or proof of causal scheduling.",
        "Assessment ratings use frozen basis 1171; intervening practice ratings use frozen basis 1149, not a fresh live database read.",
    ],
}
assert len(retake_rows) == 67 and len(pair_rows) == 8
assert len({(q["task_id"], q["question_mid"]) for q in retake_rows}) == 67
assert all(q["database_difficulty"] == q["source_difficulty"] for q in retake_rows)
assert all(q["database_difficulty"] == q["source_difficulty"] for q in practice_rows if q["database_difficulty"])
write_csv("assessment-retake-questions.csv", retake_rows)
write_csv("assessment-later-missed-topic-rechecks.csv", later_rows)
write_csv("assessment-intervening-practice-tasks.csv", practice_tasks)
write_csv("assessment-intervening-practice-questions.csv", practice_rows)
(OUT / "remediation-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "retake_pairs"}, indent=2))
