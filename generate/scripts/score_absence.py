#!/usr/bin/env python3
"""Score missing difficulty levels for a saved find_candidates.py discovery.

Read only frozen, KP-linked evidence; never query or transact the database.
The discovery and inventory must identify the same database lineage and basis.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
LEVELS = ("easy", "moderate", "hard")
GROUPS = ((), ("easy",), ("moderate",), ("hard",), ("easy", "moderate"),
          ("moderate", "hard"), ("easy", "hard"), ("no rated evidence",))


def group_key(row):
    return tuple(row["missing_levels"]) if row["rated_questions"] else ("no rated evidence",)


def group_label(key):
    return "None" if not key else "No rated evidence" if key == ("no rated evidence",) else "–".join(key).capitalize()


def format_score(value):
    if value is None:
        return "—"
    text = f"{value:.4f}"
    return ">99.9999" if text == "100.0000" else text


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def score(candidates, analysis):
    identity = read(analysis / "database/identity.json")
    if candidates["cursor"]["basis"] != candidates["basis"]:
        raise ValueError("Discovery cursor and database basis disagree")
    if (candidates["database"], candidates["cursor"]["lineage"], candidates["basis"]) != (
        identity["database"], identity["lineage"], identity["basis"]
    ):
        raise ValueError("Discovery and frozen inventory must share database, lineage and basis")
    inventory = {r["kp_entity"]: r for r in read(analysis / "kp-inventory.json")}
    # Deduplicate the global reference distribution by question entity, rather
    # than KP membership. Unrated questions do not enter either denominator.
    ratings = {}
    for kp in read(analysis / "database/pool-inventory.json"):
        for q in kp.get(":knowledge-point/questions", []):
            level = q.get(":question/difficulty", {}).get(":db/ident", "").split("/")[-1]
            if level not in LEVELS:
                continue
            entity = q[":db/id"]
            if entity in ratings and ratings[entity] != level:
                raise ValueError(f"Conflicting difficulty for question {entity}")
            ratings[entity] = level
    baseline = Counter(ratings.values())
    total = sum(baseline.values())
    if not total or any(not baseline[level] for level in LEVELS):
        raise ValueError("Reference distribution must contain all three difficulty levels")
    selected = {}
    for topic in candidates["topics"]:
        for kp in topic["knowledge_points"]:
            entry = selected.setdefault(kp["db/id"], dict(kp=kp, topics=[]))
            if all(t["entity"] != topic["db/id"] for t in entry["topics"]):
                entry["topics"].append(dict(entity=topic["db/id"], title=topic["topic/title"],
                    math_academy_id=topic.get("topic/math-academy-id"), triggers=topic["triggers"]))
    rows = []
    for entity, entry in selected.items():
        source = inventory[entity]  # Fail rather than silently omit an unmatched KP.
        n = source["rated_questions"]
        if n != sum(source["counts"].values()):
            raise ValueError(f"Inconsistent rated counts for KP {entity}")
        levels = {}
        for level in LEVELS:
            observed = source["counts"][level] > 0 or source["distinct_capture_counts"][level] > 0
            if observed:
                state = "observed"
            elif not n:
                state = "no rated evidence"
            else:
                state = "missing"
            p = baseline[level] / total
            zero = math.exp(n * math.log1p(-p)) if state == "missing" else None
            confidence = -100 * math.expm1(n * math.log1p(-p)) if state == "missing" else None
            levels[level] = dict(status=state, expected_share=p,
                zero_observation_probability=zero, absence_confidence_score=confidence)
        missing = [level for level in LEVELS if levels[level]["status"] == "missing"]
        missing_share = sum(baseline[level] / total for level in missing)
        hybrid_zero = math.exp(n * math.log1p(-missing_share)) if missing else None
        hybrid_score = -100 * math.expm1(n * math.log1p(-missing_share)) if missing else None
        rows.append(dict(kp_entity=entity, kp_id=entry["kp"]["knowledge-point/id"],
            title=source["title"], example_id=source["example_id"], topics=entry["topics"],
            total_questions=source["total_questions"], rated_questions=n,
            unrated_questions=source["unknown_questions"], counts=source["counts"],
            capture_counts=source["distinct_capture_counts"], levels=levels,
            missing_levels=missing, hybrid=dict(expected_missing_share=missing_share if missing else None,
                zero_observation_probability=hybrid_zero, absence_confidence_score=hybrid_score)))
    rows.sort(key=lambda r: (r["topics"][0]["title"], r["title"], r["kp_entity"]))
    summary = dict(topics=len(candidates["topics"]), distinct_kps=len(rows),
        kps_with_rated_questions=sum(r["rated_questions"] > 0 for r in rows),
        kps_without_rated_questions=sum(r["rated_questions"] == 0 for r in rows),
        missing_level_counts={level: sum(r["levels"][level]["status"] == "missing" for r in rows)
                             for level in LEVELS},
        scores_at_least_99={level: sum((r["levels"][level]["absence_confidence_score"] or 0) >= 99
                                     for r in rows) for level in LEVELS})
    groups = []
    for key in GROUPS:
        members = [r for r in rows if group_key(r) == key]
        scores = [r["hybrid"]["absence_confidence_score"] for r in members
                  if r["hybrid"]["absence_confidence_score"] is not None]
        groups.append(dict(label=group_label(key), missing_levels=list(key) if key != ("no rated evidence",) else [],
            kps=len(members),
            median_level_scores={level: median(r["levels"][level]["absence_confidence_score"] for r in members)
                                 for level in key if level in LEVELS and members},
            median_hybrid_score=median(scores) if scores else None))
    return dict(database=identity, discovery_at=candidates["at"], learner=candidates["learner"],
        formula="100 * (1 - (1 - p) ** n)",
        hybrid_formula="100 * (1 - (1 - sum(p[level] for level in missing_levels)) ** n)",
        baseline=dict(distinct_rated_questions=total, counts=dict(baseline)),
        summary=summary, groups=groups, kps=rows)


def markdown(result):
    s = result["summary"]
    lines = ["# Candidate KP absence confidence scores", "",
        f"Discovery at {result['discovery_at']}, EDB `{result['database']['database']}` "
        f"basis **{result['database']['basis']}**. Each distinct surfaced KP appears once.", "",
        f"**{s['distinct_kps']} KPs across {s['topics']} topics:** "
        f"{s['kps_with_rated_questions']} have rated questions; "
        f"{s['kps_without_rated_questions']} have no rated evidence and receive no score.", "",
        "For each missing level: **score = 100 × (1 − (1 − p)ⁿ)**. "
        "n counts distinct rated practice questions in the KP. Unrated questions and repeated "
        "appearances do not increase n. Scores are heuristic evidence of absence, not posterior probabilities.", "",
        "The **hybrid score** measures the entire missing-level pattern: "
        "**100 × [1 − (1 − Σ p_missing)ⁿ]**. For two missing levels A and B, "
        "the chance of observing neither under the reference distribution is (1 − p_A − p_B)ⁿ. "
        "For one missing level, the hybrid equals that level's score. With no missing levels "
        "or no rated evidence, the hybrid is not applicable.", "",
        "A high hybrid score says the combined gap is surprising. It does not imply equally strong "
        "evidence for every missing level; read the separate scores alongside it. "
        "All scores use the same reference-distribution and independent-draw assumptions.", "",
        "The global reference distribution deduplicates KP-linked questions by entity. "
        "An observed database or captured question establishes that a level exists; its cell says ‘Observed’.", "",
        "| Level | Reference questions | Expected share | KPs scored | Scores ≥99 |",
        "|---|---:|---:|---:|---:|"]
    for level in LEVELS:
        count = result["baseline"]["counts"][level]
        lines.append(f"| {level.title()} | {count:,} | "
            f"{100 * count / result['baseline']['distinct_rated_questions']:.4f}% | "
            f"{s['missing_level_counts'][level]} | {s['scores_at_least_99'][level]} |")
    lines += ["", "## All groups", "",
        "Scores below are **medians of the per-KP scores**, not a pooled group confidence. "
        "The detailed tables retain every KP's individual scores.", "",
        "| Missing levels | KPs | Median easy score | Median moderate score | Median hard score | Median hybrid score |",
        "|---|---:|---:|---:|---:|---:|"]
    for group in result["groups"]:
        cells = [format_score(group["median_level_scores"].get(level)) for level in LEVELS]
        lines.append(f"| {group['label']} | {group['kps']} | " + " | ".join(cells)
                     + " | " + format_score(group["median_hybrid_score"]) + " |")
    def escape(text):
        return text.replace("|", "\\|").replace("\n", " ")
    for key in GROUPS:
        members = [r for r in result["kps"] if group_key(r) == key]
        lines += ["", f"## Missing levels: {group_label(key)} — {len(members)} KPs", "",
            "| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in members:
            cells = []
            for level in LEVELS:
                value = r["levels"][level]
                cells.append(format_score(value["absence_confidence_score"]) if value["status"] == "missing"
                             else "Observed" if value["status"] == "observed" else "No rated evidence")
            hybrid = r["hybrid"]["absence_confidence_score"]
            cells.append(format_score(hybrid))
            topics = "; ".join(t["title"] for t in r["topics"])
            lines.append(f"| {escape(topics)} | {escape(r['title'])} | {r['kp_entity']} | "
                f"{r['total_questions']} | {r['rated_questions']} | {r['unrated_questions']} | "
                + " | ".join(str(r["counts"][level]) for level in LEVELS) + " | "
                + " | ".join(cells) + " |")
    lines += ["", "Counts in Easy/Moderate/Hard columns are database pool counts. "
        "Scores for different missing levels are calculated separately. "
        "Values that would round to 100.0000 are displayed as >99.9999; "
        "the JSON retains zero-observation probabilities for these cases.", "",
        "[Full precision scores and metadata](scores.json) · [Discovery output](candidates.json)", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--analysis", type=Path, default=ROOT / "reference/mathacademy/kp-difficulty-analysis-2026-10-12")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = score(read(args.candidates), args.analysis)
    args.output.mkdir(parents=True, exist_ok=True)
    if args.candidates.resolve() != (args.output / "candidates.json").resolve():
        (args.output / "candidates.json").write_bytes(args.candidates.read_bytes())
    inputs = [args.output / "candidates.json", *(args.analysis / name for name in (
        "database/identity.json", "database/pool-inventory.json", "kp-inventory.json"))]
    result["inputs"] = [dict(path=str(p.resolve()), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs]
    write(args.output / "scores.json", result)
    (args.output / "report.md").write_text(markdown(result))
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
