#!/usr/bin/env python3
"""Reproduce whole-data earned-XP analysis without touching capture/progress data.

Default: use frozen observations. --refresh reads current completed captures and
the historical XP sample, verifying outcomes against retained activity metadata.
No holdout, cross-validation, or live interaction with Math Academy is performed.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

from estimator import estimate_earned_xp, rounded

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LABELS = {"E": "E", "M": "M", "H": "H", "easy": "E", "moderate": "M", "hard": "H"}


def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def completion_xp(text):
    base_match = re.search(r"(?:of|all of) the task's (\d+) XP", text) or re.search(r"-?\d+/(\d+) XP", text)
    if not base_match:
        return None, None
    base = int(base_match[1])
    pair = re.search(r"(-?\d+)/(\d+) XP", text)
    if pair:
        return base, int(pair[1])
    award = re.search(r"awarded\s+(-?\d+)\s+of\s+the task's \d+ XP", text)
    if award:
        return base, int(award[1])
    if re.search(r"awarded all of the task's \d+ XP", text):
        bonus = re.search(r"bonus of (\d+) XP", text)
        return base, base + (int(bonus[1]) if bonus else 0)
    loss = re.search(r"(?:lost|penalty of) (\d+) XP", text)
    return base, -int(loss[1]) if loss else None


def extract():
    rows, excluded = [], []
    for path in sorted((ROOT / "reference/mathacademy/question-capture").glob("*/state.json")):
        state = json.loads(path.read_text())
        base, earned = completion_xp(state.get("completion", ""))
        reason = None
        if not state.get("activity_complete"):
            reason = "incomplete activity"
        elif base is None or earned is None:
            reason = "completion lacks base/earned XP pair"
        if reason:
            excluded.append({"source": str(path.relative_to(ROOT)), "task_id": state["task_id"], "reason": reason})
            continue
        questions = []
        for qid, q in state.get("questions", {}).items():
            outcome = q.get("actual_result")
            if outcome not in ("Correct", "Incorrect"):
                raise ValueError(f"Unknown outcome: {path}: {qid}")
            questions.append({"id": qid, "correct": outcome == "Correct", "kp_id": q.get("kp_id"),
                              "status": q.get("status"), "intended": q.get("intended")})
        metadata_path = path.parent / "activity-metadata.json"
        metadata_verified = False
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())
            if isinstance(metadata, list):
                by_id = {q["id"].replace("question-", "q-"): q for q in metadata}
                if len(metadata) != len(questions) or set(by_id) != {q["id"] for q in questions}:
                    raise ValueError(f"Question occurrence mismatch: {path}")
                for q in questions:
                    observed = by_id[q["id"]]
                    if observed.get("result") != ("Correct" if q["correct"] else "Incorrect"):
                        raise ValueError(f"History outcome mismatch: {path}: {q['id']}")
                    q["difficulty"] = observed.get("difficulty")
                metadata_verified = True
        content_path = path.parent / "content.json"
        content = json.loads(content_path.read_text()) if content_path.exists() else {}
        title = content.get("title") or content.get("topic_title")
        if state.get("earned_xp") is not None and state["earned_xp"] != earned:
            raise ValueError(f"Earned XP mismatch: {path}")
        rows.append({"task_id": state["task_id"], "type": state.get("task_type", "lesson"),
                     "title": title, "topic_id": state.get("topic_id"), "base": base, "earned": earned,
                     "questions": questions, "source": str(path.relative_to(ROOT)),
                     "source_sha256": source_hash(path), "history_verified": metadata_verified,
                     "completion": state.get("completion"), "origin": "capture"})
    historical = ROOT / "reference/mathacademy-xp-observations.json"
    for task in json.loads(historical.read_text())["tasks"]:
        if task.get("base") is None:
            excluded.append({"task_id": int(task["task_id"]), "reason": "diagnostic has no displayed base", "source": str(historical.relative_to(ROOT))})
            continue
        rows.append({"task_id": int(task["task_id"]), "type": task["type"].lower(), "title": task["name"],
                     "base": task["base"], "earned": task["earned"], "questions": task["questions"],
                     "source": str(historical.relative_to(ROOT)), "source_sha256": source_hash(historical),
                     "origin": "historical"})
    if len({r["task_id"] for r in rows}) != len(rows):
        raise ValueError("Overlapping task IDs require explicit reconciliation")
    # Later collections retain correct AND incorrect outcomes, including perfect
    # tasks. Join compact question sequences to the CSV's independent XP awards.
    import csv
    progress_path = ROOT / "reference/progress.csv"
    progress = list(csv.DictReader(progress_path.open()))
    progress_by_id = {int(r["task-id"]): r for r in progress}
    if len(progress_by_id) != len(progress):
        raise ValueError("Duplicate progress task IDs")
    by_id = {r["task_id"]: r for r in rows}

    def reconcile(new):
        old = by_id.get(new["task_id"])
        if old is not None:
            for key in ("type", "base", "earned"):
                if old[key] != new[key]:
                    raise ValueError(f"Conflicting {key}: {new['task_id']}")
            old_features = [(q["correct"], LABELS.get(q.get("difficulty"))) for q in old["questions"]]
            new_features = [(q["correct"], LABELS.get(q.get("difficulty"))) for q in new["questions"]]
            if old_features != new_features:
                raise ValueError(f"Conflicting outcomes/order/difficulty: {new['task_id']}")
            old.setdefault("corroborating_sources", []).append(new["source"])
            if new.get("kp_question_counts"):
                old["kp_question_counts"] = new["kp_question_counts"]
            return
        rows.append(new)
        by_id[new["task_id"]] = new

    compact_path = ROOT / "reference/question-difficulty-observations-2026-10-03.json"
    for tid, kind, groups in json.loads(compact_path.read_text())["tasks"]:
        record = progress_by_id[int(tid)]
        questions = []
        for kp_index, group in enumerate(groups):
            for token in group.split():
                if not re.fullmatch("[EMH][CI]", token):
                    raise ValueError("Unknown compact outcome " + token)
                questions.append({"correct": token[1] == "C", "difficulty": token[0], "kp_index": kp_index})
        reconcile({"task_id": int(tid), "type": kind.lower(), "title": record["topic-name"],
                   "base": int(record["xp-possible"]), "earned": int(record["xp-earned"]),
                   "questions": questions, "source": str(compact_path.relative_to(ROOT)),
                   "source_sha256": source_hash(compact_path), "award_source": str(progress_path.relative_to(ROOT)),
                   "kp_question_counts": [len(g.split()) for g in groups], "origin": "compact_history"})
    live_path = ROOT / "reference/fire-live-observations-2026-09-26.json"
    for task in json.loads(live_path.read_text())["tasks"]:
        if task["base_xp"] is None:
            continue
        questions = [{"correct": q["result_label"] == "Correct", "difficulty": q["difficulty_label"]} for q in task["questions"]]
        reconcile({"task_id": int(task["task_id"]), "type": task["kind"], "title": task["title"],
                   "base": task["base_xp"], "earned": task["earned_xp"], "questions": questions,
                   "source": str(live_path.relative_to(ROOT)), "source_sha256": source_hash(live_path), "origin": "live_history"})
    for tid, record in progress_by_id.items():
        old = by_id.get(tid)
        if old is not None:
            if (record["activity-type"].lower(), int(record["xp-possible"]), int(record["xp-earned"])) != (old["type"], old["base"], old["earned"]):
                raise ValueError(f"Conflicting CSV award: {tid}")
            old["date"] = record["completed-at"]
    return {"extracted_at": datetime.now(timezone.utc).isoformat(), "scope": "All complete local captures and historical question-level XP observations with displayed base; no holdout",
            "progress_source": {"path": str(progress_path.relative_to(ROOT)), "sha256": source_hash(progress_path),
                                "rows": len(progress), "with_outcomes": sum(tid in by_id for tid in progress_by_id)},
            "progress_rows": progress, "rows": rows, "excluded": excluded}


def metrics(rows):
    errors = [abs(r["predicted"] - r["earned"]) for r in rows]
    return {"tasks": len(rows), "exact": sum(e == 0 for e in errors),
            "mae": sum(errors) / len(errors), "maximum_absolute_error": max(errors),
            "total_absolute_error": sum(errors)}


def analyze(observations):
    rows = []
    by_kind = defaultdict(list)
    same_inputs = defaultdict(list)
    for task in observations["rows"]:
        n = len(task["questions"])
        c = sum(q["correct"] for q in task["questions"])
        p = Fraction(c, n)
        predicted = estimate_earned_xp(task["type"], task["base"], c, n)
        row = {k: v for k, v in task.items() if k not in ("questions", "completion", "source_sha256")}
        row.update(correct=c, total=n, accuracy=float(p), accuracy_fraction=str(p), predicted=predicted,
                   error=predicted-task["earned"])
        rows.append(row)
        by_kind[task["type"]].append(row)
        same_inputs[(task["type"], task["base"], p)].append(row)
    conflicts = [[r for r in group] for group in same_inputs.values() if len({r["earned"] for r in group}) > 1]
    # Constrain an imperfect-lesson line anchored at (accuracy, multiplier)=(.6,.6).
    # Award rounding gives intervals, not exact latent multipliers. A cap at 1
    # introduces only lower bounds when the observed award equals the base.
    lower, upper = Fraction(0), None
    for r in by_kind["lesson"]:
        p = Fraction(r["correct"], r["total"])
        if p <= Fraction(3, 5) or p == 1 or r["earned"] < 0:
            continue
        lo = (Fraction(2*r["earned"]-1, 2*r["base"]) - Fraction(3, 5)) / (p-Fraction(3, 5))
        lower = max(lower, lo)
        if r["earned"] < r["base"]:
            hi = (Fraction(2*r["earned"]+1, 2*r["base"]) - Fraction(3, 5)) / (p-Fraction(3, 5))
            upper = hi if upper is None else min(upper, hi)
    comparisons = {}
    for kind, group in by_kind.items():
        variants = {"identity_accuracy": [], "selected": []}
        for r in group:
            identity = {**r, "predicted": rounded(Fraction(r["base"]*r["correct"],r["total"]))}
            variants["identity_accuracy"].append(identity)
            variants["selected"].append(r)
        comparisons[kind] = {name: metrics(selected) for name, selected in variants.items()}
    return {"observation_timestamp": observations["extracted_at"], "method": "Whole-data agreement; no train/test split or cross-validation",
            "counts": dict(Counter(r["type"] for r in rows)), "overall": metrics(rows),
            "nonnegative": metrics([r for r in rows if r["earned"] >= 0]),
            "by_type": {kind: {"all": metrics(group), "nonnegative": metrics([r for r in group if r["earned"] >= 0])} for kind,group in by_kind.items()},
            "comparisons": comparisons,
            "lesson_slope_interval": {"inclusive_lower": str(lower), "exclusive_upper": str(upper), "selected": "7/5"},
            "identical_input_conflicts": conflicts, "mismatches": [r for r in rows if r["error"]], "predictions": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    path = HERE / "observations.json"
    if args.refresh:
        observations = extract()
        path.write_text(json.dumps(observations, indent=2)+"\n")
    else:
        observations = json.loads(path.read_text())
    results = analyze(observations)
    (HERE / "results.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({k: results[k] for k in ("counts", "overall", "nonnegative", "by_type", "lesson_slope_interval", "mismatches")},indent=2))
