#!/usr/bin/env python3
"""Measure the compact approximation on every frozen observation; no holdout."""
from collections import Counter
import json
from pathlib import Path

from compact_estimator import estimate_from_outcomes

HERE = Path(__file__).resolve().parent


def main():
    observations = json.loads((HERE / "observations.json").read_text())
    predictions = []
    for row in observations["rows"]:
        outcomes = [q["correct"] for q in row["questions"]]
        predicted = estimate_from_outcomes(row["type"], row["base"], outcomes)
        predictions.append({"task_id": row["task_id"], "type": row["type"],
                            "base": row["base"], "correct": sum(outcomes),
                            "total": len(outcomes), "final_correct": outcomes[-1],
                            "earned": row["earned"], "predicted": predicted,
                            "error": predicted - row["earned"]})
    errors = [abs(p["error"]) for p in predictions]
    result = {
        "observation_timestamp": observations["extracted_at"],
        "method": "All frozen observations; no holdout; provisional round-number penalty thresholds.",
        "counts": dict(Counter(p["type"] for p in predictions)),
        "tasks": len(predictions), "exact": sum(e == 0 for e in errors),
        "total_absolute_error": sum(errors), "maximum_absolute_error": max(errors),
        "mean_absolute_error": sum(errors) / len(errors),
        "penalty_policy": {"lesson_review_accuracy_below": 0.5,
                           "assessment_accuracy_below": 0.2, "negative_floor": -1,
                           "status": "Local defaults, thresholds and floor not identified."},
        "additional_base_unknown_review": {
            "task_id": 13929099, "correct": 2, "total": 5, "earned": -1,
            "policy_prediction": -1,
            "note": "Excluded from base-relative metrics; low-score policy is base-independent."},
        "predictions": predictions,
        "mismatches": [p for p in predictions if p["error"]],
    }
    (HERE / "compact-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("predictions", "mismatches")}, indent=2))


if __name__ == "__main__":
    main()
