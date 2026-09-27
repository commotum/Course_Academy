#!/usr/bin/env python3
"""Analyze completed Math Academy observations; read-only, stdlib only.

Defaults: mathacademy-xp-observations.json and progress.csv beside this script.
Example: python3 analyze-mathacademy-xp.py --observations /tmp/ma-xp-observed.json \
    --progress /path/to/progress.csv

All predictions use exact Fraction arithmetic. R(x) = floor(x + 1/2),
so ties go toward positive infinity, including for hypothetical negative inputs.
These candidate formulas are empirical hypotheses, not recovered platform code.
"""

import argparse
import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


DIFFICULTY_WEIGHTS = {"E": 1, "M": 2, "H": 3}


def number(value):
    if value is None or value == "":
        return None
    return Fraction(str(value))


def scalar(value):
    if value is None:
        return None
    return value.numerator if value.denominator == 1 else str(value)


def exact(value):
    if value is None:
        return None
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": str(value),
        "decimal_for_display": float(value),
    }


def round_half_up(value):
    """Exact floor(value + 1/2); matches the stated candidate definition."""
    shifted = value + Fraction(1, 2)
    return shifted.numerator // shifted.denominator


def candidate_prediction(kind, base, accuracy):
    if base is None or accuracy is None:
        return None
    if kind == "Assessment":
        raw = base * Fraction(6, 5) * (accuracy - Fraction(7, 20)) / Fraction(13, 20)
        return {
            "model": "assessment_linear_35_percent_zero_20_percent_bonus",
            "raw": exact(raw),
            "rounded_before_clamp": round_half_up(raw),
            "predicted_xp": max(0, round_half_up(raw)),
        }
    if kind == "Multistep":
        raw = base * (Fraction(9, 4) * accuracy - 1)
        return {
            "model": "multistep_linear_9_over_4_slope",
            "raw": exact(raw),
            "rounded_before_clamp": round_half_up(raw),
            "predicted_xp": round_half_up(raw),
        }
    return None


def task_summary(task):
    questions = task.get("questions", [])
    count = len(questions)
    correct = sum(q.get("correct") is True for q in questions)
    incorrect = sum(q.get("correct") is False for q in questions)
    unknown = count - correct - incorrect
    accuracy = Fraction(correct, count) if count and not unknown else None
    base, earned = number(task.get("base")), number(task.get("earned"))
    kind = task.get("type")
    difficulty = {}
    for label in sorted({q.get("difficulty") or "unknown" for q in questions}):
        selected = [q for q in questions if (q.get("difficulty") or "unknown") == label]
        difficulty[label] = {
            "total": len(selected),
            "correct": sum(q.get("correct") is True for q in selected),
            "incorrect": sum(q.get("correct") is False for q in selected),
        }
    known_difficulty = all(q.get("difficulty") in DIFFICULTY_WEIGHTS for q in questions)
    difficulty_sum = (
        sum(DIFFICULTY_WEIGHTS[q["difficulty"]] for q in questions)
        if count and known_difficulty else None
    )
    correct_difficulty_sum = (
        sum(DIFFICULTY_WEIGHTS[q["difficulty"]] for q in questions if q.get("correct") is True)
        if count and known_difficulty and not unknown else None
    )
    durations = [number(q.get("elapsed_seconds")) for q in questions]
    shown_durations = [duration for duration in durations if duration is not None]
    predicted = candidate_prediction(kind, base, accuracy)
    if predicted is not None:
        predicted["matches_observed"] = earned == predicted["predicted_xp"] if earned is not None else None
        predicted["observed_minus_predicted"] = scalar(earned - predicted["predicted_xp"]) if earned is not None else None
    perfect = bool(count and not unknown and correct == count)
    bonuses = None
    if perfect and base is not None and earned is not None:
        bonuses = {}
        possibilities = {
            "round_1_25_times_base": round_half_up(Fraction(5, 4) * base),
            "round_1_20_times_base": round_half_up(Fraction(6, 5) * base),
            "base_plus_2": base + 2,
            "base_plus_minimum_2_or_rounded_quarter": base + max(2, round_half_up(base / 4)),
        }
        for name, value in possibilities.items():
            bonuses[name] = {"predicted_xp": scalar(Fraction(value)), "matches_observed": earned == value}
    return {
        "task_id": str(task["task_id"]),
        "type": kind,
        "name": task.get("name"),
        "url": task.get("url"),
        "earned": scalar(earned),
        "base": scalar(base),
        "question_count": count,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "unknown_outcome_count": unknown,
        "accuracy": exact(accuracy),
        "perfect": perfect,
        "observed_group_count": task.get("groups"),
        "difficulty_counts": difficulty,
        "difficulty_sum_E1_M2_H3": difficulty_sum,
        "correct_difficulty_sum_E1_M2_H3": correct_difficulty_sum,
        "difficulty_sum_matches_base": base == difficulty_sum if base is not None and difficulty_sum is not None else None,
        "elapsed_seconds_total_of_available_values": scalar(sum(shown_durations, Fraction(0))) if shown_durations else None,
        "elapsed_seconds_missing_count": count - len(shown_durations),
        "answer_state_counts": dict(sorted(Counter(q.get("answer_state") or "unknown" for q in questions).items())),
        "candidate": predicted,
        "perfect_bonus_predictions": bonuses,
    }


def summarize_csv(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["activity-type"]].append(row)
    results = {}
    for kind, subset in sorted(groups.items()):
        ceiling = {
            "Lesson": ("R(1.25 B)", lambda b: round_half_up(Fraction(5, 4) * b)),
            "Multistep": ("R(1.25 B)", lambda b: round_half_up(Fraction(5, 4) * b)),
            "Assessment": ("R(1.20 B)", lambda b: round_half_up(Fraction(6, 5) * b)),
            "Review": ("B + 2", lambda b: b + 2),
        }.get(kind)
        pairs = Counter((row.get("xp-earned", ""), row.get("xp-possible", "")) for row in subset)
        comparison = Counter()
        ceiling_counterexamples = []
        for row in subset:
            b, y = number(row.get("xp-possible")), number(row.get("xp-earned"))
            if ceiling is None or b is None or y is None:
                comparison["not_evaluable"] += 1
                continue
            limit = ceiling[1](b)
            key = "equal" if y == limit else "above" if y > limit else "below"
            comparison[key] += 1
            if key == "above":
                ceiling_counterexamples.append({"task_id": row.get("task-id"), "earned": scalar(y), "base": scalar(b), "predicted_ceiling": scalar(Fraction(limit))})
        results[kind] = {
            "row_count": len(subset),
            "ceiling_hypothesis": ceiling[0] if ceiling else None,
            "ceiling_comparison": {name: comparison[name] for name in ("equal", "below", "above", "not_evaluable")},
            "ceiling_counterexamples": ceiling_counterexamples,
            "earned_base_frequencies": [
                {"earned": scalar(number(e)), "base": scalar(number(b)), "count": n}
                for (e, b), n in sorted(pairs.items(), key=lambda item: (number(item[0][1]) or -1, number(item[0][0]) or 0))
            ],
        }
    return results


def main():
    sibling = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, default=sibling / "mathacademy-xp-observations.json")
    parser.add_argument("--progress", type=Path, default=sibling / "progress.csv")
    args = parser.parse_args()
    raw = json.loads(args.observations.read_text())
    tasks = raw if isinstance(raw, list) else raw["tasks"]
    with args.progress.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    summaries = [task_summary(task) for task in tasks]
    models = defaultdict(list)
    types = defaultdict(list)
    for task in summaries:
        types[task["type"]].append(task)
        if task["candidate"] and task["candidate"]["matches_observed"] is not None:
            models[task["candidate"]["model"]].append(task)
    fits = {}
    for name, evaluated in sorted(models.items()):
        misses = [task for task in evaluated if not task["candidate"]["matches_observed"]]
        fits[name] = {
            "evaluated_count": len(evaluated),
            "exact_match_count": len(evaluated) - len(misses),
            "counterexample_count": len(misses),
            "absolute_error_total": scalar(sum((abs(number(task["candidate"]["observed_minus_predicted"])) for task in evaluated), Fraction(0))),
            "counterexample_task_ids": [task["task_id"] for task in misses],
        }
    bonus_fits = {}
    for kind, subset in sorted(types.items()):
        perfect = [task for task in subset if task["perfect"]]
        evaluated = [task for task in perfect if task["perfect_bonus_predictions"]]
        candidates = sorted({name for task in evaluated for name in task["perfect_bonus_predictions"]})
        bonus_fits[kind] = {
            "observed_task_count": len(subset),
            "perfect_task_count": len(perfect),
            "perfect_tasks_with_base_count": len(evaluated),
            "perfect_task_ids": [task["task_id"] for task in perfect],
            "models": {
                name: {
                    "evaluated_count": len(evaluated),
                    "exact_match_count": sum(task["perfect_bonus_predictions"][name]["matches_observed"] for task in evaluated),
                    "counterexample_task_ids": [task["task_id"] for task in evaluated if not task["perfect_bonus_predictions"][name]["matches_observed"]],
                } for name in candidates
            },
        }
    observed_ids = [task["task_id"] for task in summaries]
    csv_ids = {row.get("task-id") for row in rows}
    output = {
        "inputs": {"observations": str(args.observations.resolve()), "progress": str(args.progress.resolve())},
        "rounding": "Exact Fraction R(x)=floor(x+1/2); ties toward positive infinity. No binary-float arithmetic in predictions.",
        "model_status": "Empirical candidate formulas; fits do not identify production code or prove extrapolations.",
        "models": {
            "assessment_linear_35_percent_zero_20_percent_bonus": "max(0, R(B * (6/5) * (p - 7/20) / (13/20)))",
            "multistep_linear_9_over_4_slope": "R(B * ((9/4) * p - 1)); no unobserved negative/history cap imposed",
            "p": "correct questions / all observed questions; prediction omitted if any outcome is unknown",
        },
        "coverage": {
            "observed_task_count": len(summaries),
            "observed_question_count": sum(task["question_count"] for task in summaries),
            "csv_row_count": len(rows),
            "duplicate_observation_task_ids": sorted(tid for tid, n in Counter(observed_ids).items() if n > 1),
            "observed_task_ids_missing_from_csv": sorted(set(observed_ids) - csv_ids),
        },
        "candidate_fits": fits,
        "perfect_bonus_fits_by_type": bonus_fits,
        "difficulty_sum_base_hypothesis": {
            "formula": "B = #E + 2 #M + 3 #H; included as a falsifiable naive hypothesis",
            "evaluated_count": sum(task["difficulty_sum_matches_base"] is not None for task in summaries),
            "exact_match_count": sum(task["difficulty_sum_matches_base"] is True for task in summaries),
            "counterexample_task_ids": [task["task_id"] for task in summaries if task["difficulty_sum_matches_base"] is False],
        },
        "csv_ceiling_observations_by_type": summarize_csv(rows),
        "tasks": summaries,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
