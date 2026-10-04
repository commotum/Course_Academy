"""Fit cheap content-only base-XP estimates from saved captures; never contact MA/EDB.

Run with /home/jake/Developer/MA/.venv/bin/python. Outputs stay beside this script.
Capture states are read once, then all fitting uses the frozen observations.json.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import os

import numpy as np
from bs4 import BeautifulSoup
from estimator import clean_markdown, math_tokens, prose_words

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FEATURES = {
    "kp": "Number of captured knowledge points",
    "tutorials": "Number of saved tutorial slides",
    "moderate_kp": "Sum over KPs of fraction of captured questions labelled moderate",
    "hard_kp": "Sum over KPs of fraction of captured questions labelled hard",
    "question_steps": "Sum over KPs of mean equals-sign count in worked question solutions",
    "example_steps": "Equals-sign count in canonical-example solutions, summed over examples",
    "question_math_100": "Sum over KPs of mean question-prompt math token count, divided by 100",
    "solution_math_100": "Sum over KPs of mean worked-solution math token count, divided by 100",
    "reading_100": "Tutorial plus canonical-example prose words, divided by 100; excludes formulas and image paths",
    "extra_fields": "Sum over KPs of mean max(0, answer-field count minus one)",
    "blank_kp": "Sum over KPs of fraction of questions requiring a blank answer",
}
# Small candidate families; the current calibration fits all captured lessons.
MODELS = {
    "median": [],
    "kp_only": ["kp"],
    "kp_tutorials": ["kp", "tutorials"],
    "kp_difficulty": ["kp", "moderate_kp", "hard_kp"],
    "kp_question_steps": ["kp", "question_steps"],
    "kp_example_steps": ["kp", "example_steps"],
    "kp_question_steps_tutorials": ["kp", "question_steps", "tutorials"],
    "kp_question_steps_reading": ["kp", "question_steps", "reading_100"],
    "kp_solution_math_reading": ["kp", "solution_math_100", "reading_100"],
    "kp_prompt_math": ["kp", "question_math_100"],
    "kp_extra_fields": ["kp", "extra_fields"],
    "kp_blank_answers": ["kp", "blank_kp"],
    "kp_difficulty_steps": ["kp", "moderate_kp", "hard_kp", "question_steps"],
}


def tutorial_words(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select("style, script, svg, math, mjx-container, .mjpage, .stepHeader, .helpButton"):
        tag.decompose()
    return len(re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", soup.get_text(" ", strip=True)))


def base_from_completion(text):
    match = re.search(r"(?:of|all of) the task's (\d+) XP", text)
    if match:
        return int(match[1]), "completion task denominator"
    match = re.search(r"-?\d+/(\d+) XP", text)
    return (int(match[1]), "recovered completion denominator") if match else (None, None)


def extract():
    rows, excluded = [], []
    for source in sorted((ROOT / "reference/mathacademy/question-capture").glob("*/state.json")):
        raw = source.read_bytes()
        state = json.loads(raw)
        base, evidence = base_from_completion(state.get("completion", ""))
        row = {"task_id": state["task_id"], "topic_id": state.get("topic_id"),
               "type": state.get("task_type", "lesson"), "base_xp": base,
               "base_evidence": evidence, "source": str(source.relative_to(ROOT)),
               "state_sha256": hashlib.sha256(raw).hexdigest(),
               "complete": bool(state.get("activity_complete")), "features": {}}
        content_source = source.parent / "content.json"
        content = json.loads(content_source.read_text()) if content_source.exists() else {}
        questions = content.get("questions", [])
        row["captured_question_count"] = len(questions)
        row["question_difficulties"] = dict(Counter(q.get("difficulty") for q in questions))
        row["title"] = state.get("title")
        topic = source.parent / "selection/topic.edn"
        if topic.exists():
            match = re.search(r':topic/title "((?:\\.|[^"\\])*)"', topic.read_text())
            if match:
                row["title"] = json.loads('"' + match[1] + '"')
        if row["type"] == "assessment":
            row["details"] = state.get("assessment_details", {})
        if row["type"] == "lesson":
            examples = content.get("canonical_examples", [])
            grouped = defaultdict(list)
            for q in questions:
                grouped[q["knowledge_point_id"]].append(q)
            kps = set(state.get("kps", {}))
            if (not row["complete"] or base is None or not kps or set(grouped) != kps or
                    {q["knowledge_point_id"] for q in examples} != kps):
                excluded.append({"task_id": row["task_id"], "reason": "Incomplete lesson structure or missing base"})
                continue
            tutorials = list(source.parent.glob("tutorial-*.html"))
            f = row["features"]
            f.update(kp=len(kps), tutorials=len(tutorials))
            f["moderate_kp"] = sum(sum(q["difficulty"] == "moderate" for q in qs) / len(qs) for qs in grouped.values())
            f["hard_kp"] = sum(sum(q["difficulty"] == "hard" for q in qs) / len(qs) for qs in grouped.values())
            f["question_steps"] = sum(sum(clean_markdown(q["worked_solution"]).count("=") for q in qs) / len(qs) for qs in grouped.values())
            f["example_steps"] = sum(clean_markdown(q["worked_solution"]).count("=") for q in examples)
            for field, key in (("problem", "question_math_100"), ("worked_solution", "solution_math_100")):
                f[key] = sum(sum(math_tokens(q[field]) for q in qs) / len(qs) for qs in grouped.values()) / 100
            f["reading_100"] = (sum(tutorial_words(p.read_text()) for p in tutorials) +
                sum(prose_words(q["problem"]) + prose_words(q["worked_solution"]) for q in examples)) / 100
            f["extra_fields"] = sum(sum(max(0, len(q["answer_fields"]) - 1) for q in qs) / len(qs) for qs in grouped.values())
            f["blank_kp"] = sum(sum(any(a["type"] == "blank" for a in q["answer_fields"]) for q in qs) / len(qs) for qs in grouped.values())
            row["kp_question_counts"] = {kp: len(qs) for kp, qs in grouped.items()}
            row["question_samples"] = [{"id": q["math_academy_id"], "kp": q["knowledge_point_id"],
                "difficulty": q["difficulty"], "solution_equals": clean_markdown(q["worked_solution"]).count("="),
                "prompt_math_tokens": math_tokens(q["problem"]), "solution_math_tokens": math_tokens(q["worked_solution"])}
                for q in questions]
        rows.append(row)
    historical = list(csv.DictReader((ROOT / "reference/progress.csv").open()))
    return {"extracted_at": datetime.now(timezone.utc).isoformat(), "features": FEATURES,
            "excluded": excluded, "activities": rows, "historical_progress": historical,
            "notes": ["Base is the displayed denominator, excluding earned XP and bonuses.",
                      "No solver times, bot durations, correctness, priority scores, or personal progress are model inputs.",
                      "Per-KP means avoid pricing the bot's intentionally expanded five-question sequence as normal expected workload."]}


def design(rows, names):
    return np.array([[1, *(r["features"][n] for n in names)] for r in rows], dtype=float)


def fit(rows, names):
    if not names:
        return np.array([np.median([r["base_xp"] for r in rows])])
    x, y = design(rows, names), np.array([r["base_xp"] for r in rows])
    # Small nonnegative least squares: enumerate active subsets of the features.
    # Nonnegative slopes make the workload estimate monotone in measured work.
    best, best_error = np.zeros(x.shape[1]), float("inf")
    for size in range(1, x.shape[1] + 1):
        for subset in itertools.combinations(range(x.shape[1]), size):
            coef = np.linalg.lstsq(x[:, subset], y, rcond=None)[0]
            if np.any(coef < -1e-9):
                continue
            candidate = np.zeros(x.shape[1])
            candidate[list(subset)] = np.maximum(0, coef)
            error = float(np.sum((x @ candidate - y) ** 2))
            if error < best_error:
                best, best_error = candidate, error
    return best


def predict(rows, names, coef):
    # Empirical seven-XP floor is supported in this lesson sample and old CSV.
    # No upper cap: larger activities should remain able to cost more than 25.
    return np.maximum(7, np.floor(design(rows, names) @ coef + 0.5)).astype(int)


def metrics(rows, predictions):
    actual = np.array([r["base_xp"] for r in rows])
    error = np.array(predictions) - actual
    return {"n": len(rows), "mae": float(np.mean(abs(error))), "rmse": float(np.sqrt(np.mean(error ** 2))),
            "exact_fraction": float(np.mean(error == 0)), "within_1_fraction": float(np.mean(abs(error) <= 1)),
            "within_2_fraction": float(np.mean(abs(error) <= 2)), "within_3_fraction": float(np.mean(abs(error) <= 3)),
            "max_absolute_error": int(np.max(abs(error))), "mean_bias": float(np.mean(error))}


def observed_bases(data):
    """Keep provenance and all differing values; prefer newest captured observation."""
    observations = defaultdict(list)
    for row in data["historical_progress"]:
        if row["activity-type"] in ("Lesson", "Review") and row["topic-id"] and row["xp-possible"]:
            key = row["activity-type"].lower() + ":" + row["topic-id"]
            observations[key].append({"task_id": int(row["task-id"]), "base_xp": int(row["xp-possible"]),
                                     "source": "reference/progress.csv", "date": row["completed-at"]})
    for row in data["activities"]:
        if row["type"] in ("lesson", "review") and row["base_xp"] is not None:
            key = row["type"] + ":" + str(row["topic_id"])
            observations[key].append({"task_id": row["task_id"], "base_xp": row["base_xp"], "source": row["source"]})
    result = {}
    for key, rows in sorted(observations.items()):
        rows = sorted(rows, key=lambda r: r["task_id"], reverse=True)
        result[key] = {"base_xp": rows[0]["base_xp"], "source": rows[0]["source"],
                       "task_id": rows[0]["task_id"], "observed_values": sorted({r["base_xp"] for r in rows}),
                       "observations": rows}
    (HERE / "observed-bases.json").write_text(json.dumps({
        "observations_extracted_at": data["extracted_at"],
        "policy": "Latest task ID per activity type/topic; retain conflicting old values. Observations are not assumed immutable across content revisions.",
        "bases": result}, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Read current saved captures again; otherwise reuse frozen dataset")
    args = parser.parse_args()
    dataset = HERE / "observations.json"
    started = time.perf_counter()
    if args.refresh or not dataset.exists():
        dataset.write_text(json.dumps(extract(), indent=2) + "\n")
    data = json.loads(dataset.read_text())
    observed_bases(data)
    from difficulty_fit import fit_all, plot
    report = fit_all(data)
    report["analysis_wall_seconds"] = time.perf_counter() - started
    (HERE / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    plot(report)
    print(json.dumps({k: report[k] for k in ("lesson_n", "selected_model", "selected_coefficients", "fit_metrics", "analysis_wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
