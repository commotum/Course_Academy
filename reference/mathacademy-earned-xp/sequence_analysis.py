#!/usr/bin/env python3
"""Compare answer-order and difficulty hypotheses on the entire frozen XP sample.

No holdout or live activity. The difficulty comparisons substitute weighted
accuracy into the existing review rule; they do not falsify all weighted models.
"""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

from estimator import estimate_earned_xp, estimate_earned_xp_with_sequence, rounded

HERE = Path(__file__).resolve().parent
LABELS = {"easy": "E", "moderate": "M", "hard": "H", "E": "E", "M": "M", "H": "H"}


def features(row):
    questions = row["questions"]
    outcomes = [q["correct"] for q in questions]
    sequence = "".join("C" if correct else "I" for correct in outcomes)
    difficulties = [LABELS.get(q.get("difficulty"), "?") for q in questions]
    longest = run = 0
    for correct in outcomes:
        run = 0 if correct else run + 1
        longest = max(longest, run)
    return {"task_id": row["task_id"], "type": row["type"], "base": row["base"], "earned": row["earned"],
            "correct": sum(outcomes), "total": len(outcomes), "sequence": sequence,
            "difficulty_sequence": "".join(difficulties), "easy_count": difficulties.count("E"),
            "easy_wrong": sum(d == "E" and not c for d, c in zip(difficulties, outcomes)),
            "longest_wrong_run": longest, "last_correct": outcomes[-1],
            "unanswered_count": sum(q.get("status") in ("unanswered", "expired_unanswered") or q.get("answer_state") == "no_answer" for q in questions)}


def summarize(rows, predictor):
    predictions = []
    for row in rows:
        f = features(row)
        prediction = predictor(row, f)
        predictions.append({**f, "predicted": prediction, "error": prediction-row["earned"]})
    errors = [abs(r["error"]) for r in predictions]
    return {"tasks": len(rows), "exact": sum(e == 0 for e in errors),
            "mean_absolute_error": sum(errors)/len(errors), "maximum_absolute_error": max(errors),
            "mismatches": [r for r in predictions if r["error"]]}


def original(row, f):
    return estimate_earned_xp(row["type"], row["base"], f["correct"], f["total"])


def sequence_candidate(row, f):
    return estimate_earned_xp_with_sequence(row["type"], row["base"], [q["correct"] for q in row["questions"]])


def consecutive_candidate(row, f):
    return 0 if 3*f["correct"] < 2*f["total"] and f["longest_wrong_run"] >= 2 else original(row, f)


def easy_errors_candidate(row, f):
    return 0 if 3*f["correct"] < 2*f["total"] and f["easy_wrong"] >= 2 else original(row, f)


def weighted_candidate(hard_weight):
    weights = {"E": 1, "M": 2, "H": hard_weight}
    def predict(row, f):
        ds = f["difficulty_sequence"]
        p = Fraction(sum(weights[d] for d, q in zip(ds, row["questions"]) if q["correct"]), sum(weights[d] for d in ds))
        base = row["base"]
        return base+2 if p == 1 else base if p >= Fraction(2,3) else rounded(base*p)
    return predict


def main():
    observations = json.loads((HERE/"observations.json").read_text())
    rows = observations["rows"]
    reviews = [r for r in rows if r["type"] == "review"]
    candidates = {"accuracy_only": original, "low_accuracy_final_wrong_zero": sequence_candidate,
                  "low_accuracy_consecutive_wrong_zero": consecutive_candidate,
                  "low_accuracy_two_easy_mistakes_zero": easy_errors_candidate,
                  "weighted_accuracy_1_2_3": weighted_candidate(3),
                  "weighted_accuracy_1_2_4": weighted_candidate(4)}
    results = {"observation_timestamp": observations["extracted_at"],
               "method": "Whole-data exploratory comparisons; no holdout; one low-accuracy terminal-error review",
               "review_comparisons": {name: summarize(reviews,predictor) for name,predictor in candidates.items()},
               "with_sequence_overall": summarize(rows,sequence_candidate),
               "with_sequence_nonnegative": summarize([r for r in rows if r["earned"]>=0],sequence_candidate),
               "sixty_percent_review_easy_counts": dict(sorted(Counter(features(r)["easy_count"] for r in reviews if 5*features(r)["correct"] == 3*features(r)["total"]).items())),
               "diagnostic_examples": [features(r) for r in rows if r["task_id"] in (13409092,13938605,12698374,13930486,13938412,12601433,13933898,12225370,4833336)]}
    (HERE/"sequence-results.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"review_exact": {k:v["exact"] for k,v in results["review_comparisons"].items()},
                      "overall_exact": results["with_sequence_overall"]["exact"],
                      "nonnegative_exact": results["with_sequence_nonnegative"]["exact"],
                      "remaining_exceptions": results["with_sequence_overall"]["mismatches"]},indent=2))


if __name__ == "__main__":
    main()
