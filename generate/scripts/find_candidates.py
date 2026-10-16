#!/usr/bin/env python3
"""Rank generator-build candidates using native EDB reads; never transact or generate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from serve_graph_explorer import DEFAULT_DATABASE, DEFAULT_LEARNER, database_environment
from generator_packages import resolve_registered_script


URGENCY = {"studied": 5, "target": 4, "queued": 3, "target-prerequisite": 2,
           "studied-or-queued-descendant": 1}
PURPOSE = {"lesson-shortage": 60000, "review-shortage": 50000,
           "assessment-shortage": 40000, "hard-variety": 30000,
           "moderate-variety": 20000, "easy-variety": 10000, "advance-build": 0}
COVERAGE_BANDS = ("hard", "moderate", "easy")
COVERAGE_TARGET = (1, 2, 3)


def available_total(inventory, *, rated=False):
    key = "rated_total" if rated else "available_total"
    return inventory.get(key, sum(inventory["available"].values()))


def coverage(topic_bands):
    """At most 24 states: one distinct topic can occupy only one assessment slot."""
    states = {(0, 0, 0)}
    for bands in topic_bands.values():
        following = set(states)
        for state in states:
            for index, band in enumerate(COVERAGE_BANDS):
                if band in bands and state[index] < COVERAGE_TARGET[index]:
                    candidate = list(state)
                    candidate[index] += 1
                    following.add(tuple(candidate))
        states = following
    # Hard coverage takes precedence, then moderate, then easy.
    return max(states)


def check_generator_files(result, math_root, repo_root=ROOT):
    """Check registration bytes/paths without executing scripts or installing dependencies."""
    checked = {}
    for topic in result["topics"]:
        for kp in topic["knowledge_points"]:
            script = kp.get("generator_script")
            if script not in checked:
                error = None
                if script:
                    try:
                        resolve_registered_script(script, Path(repo_root), Path(math_root))
                    except (OSError, ValueError) as exception:
                        error = str(exception)
                checked[script] = (bool(script) and error is None, error)
            kp["generator_usable"], kp["generator_error"] = checked[script]


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() if value else float("inf")


def ranking_key(kp):
    return (-kp["score"],
            timestamp(kp.get("first_studied_at")) if kp["purpose"] == "assessment-shortage" else float("inf"),
            timestamp(kp.get("waiting_since")), kp["topic_entity"], kp["db/id"])


def ranked_candidates(result):
    """Keep complete nested inventories; rank one build job per KP by its strongest reason."""
    topic_bands = {}
    for topic in result["topics"]:
        groups = [group for group in topic.get("urgency_groups", []) if group in URGENCY]
        topic["urgency_value"] = max((URGENCY[group] for group in groups), default=0)
        if (topic["urgency_value"] and topic.get("studied") and topic.get("reviewed")
                and topic["next_activity"] == "assessment"):
            topic_bands[topic["db/id"]] = {band for band, count in topic["topic_inventory"]["available"].items() if count > 0}
    before = coverage(topic_bands)
    usable = {kp["db/id"] for topic in result["topics"] for kp in topic["knowledge_points"]
              if kp.get("generator_usable", kp.get("has_generator", False))}
    candidates = {}
    for topic in result["topics"]:
        topic_id, u = topic["db/id"], topic["urgency_value"]
        for kp in topic["knowledge_points"]:
            stage = topic["next_activity"]
            if stage not in {"lesson", "review", "assessment"}:
                raise ValueError("Unknown next activity: " + str(stage))
            scope = "knowledge-point" if stage == "lesson" else "topic"
            pool = kp["inventory"] if stage == "lesson" else topic["topic_inventory"]
            available = available_total(pool, rated=stage == "assessment")
            required = 1 if stage == "assessment" else 5
            kp.update({"topic_entity": topic_id, "topic_title": topic["topic/title"],
                       "next_activity": stage, "urgency_groups": topic.get("urgency_groups", []),
                       "urgency_value": u, "available_total": available,
                       "kp_available_total": available_total(kp["inventory"]),
                       "required_total": required, "inventory_scope": scope,
                       "first_studied_at": topic.get("first_studied_at"),
                       "waiting_since": topic.get("waiting_since"),
                       "inventory_scopes": {scope: pool},
                       "refill_deficits": {band: max(0, 5 - count) for band, count in kp["inventory"]["available"].items()},
                       "rank": None})
            reasons = []
            def reason(purpose, shortage, **extra):
                reasons.append({"purpose": purpose, "purpose_points": PURPOSE[purpose],
                                "shortage": shortage, "shortage_points": 1000 * shortage,
                                "urgency_points": 100 * u,
                                "score": PURPOSE[purpose] + 1000 * shortage + 100 * u,
                                "topic_entity": topic_id, **extra})
            reason("advance-build", 0)
            if available < required:
                reason(stage + "-shortage", required - available)
            if topic_id in topic_bands:
                for band in kp["inventory"]["supported_difficulties"]:
                    if band in topic_bands[topic_id]:
                        continue
                    proposed = dict(topic_bands)
                    proposed[topic_id] = topic_bands[topic_id] | {band}
                    after = coverage(proposed)
                    if after <= before:
                        continue
                    index = next(i for i in range(3) if after[i] > before[i])
                    improved_band = COVERAGE_BANDS[index]
                    reason(improved_band + "-variety", COVERAGE_TARGET[index] - before[index],
                           generated_band=band, improved_coverage_band=improved_band,
                           coverage_after=dict(zip(COVERAGE_BANDS, after)))
            reasons.sort(key=lambda r: (-r["score"], r.get("generated_band", "")))
            kp.update(reasons[0])
            kp["priority_reasons"] = reasons
            kp["build_required"] = bool(u) and kp["db/id"] not in usable
            kp["build_exclusion_reason"] = ("outside-urgency-groups" if not u else
                                             "usable-generator-registered" if kp["db/id"] in usable else None)
            kp["build_action"] = ("repair-generator" if kp.get("has_generator") else "create-generator") if kp["build_required"] else None
            if kp["build_required"]:
                candidates.setdefault(kp["db/id"], []).append(kp)
    ranked = []
    for contexts in candidates.values():
        winner = dict(min(contexts, key=ranking_key))
        winner["candidate_topics"] = sorted({kp["topic_entity"] for kp in contexts})
        winner["priority_reasons"] = [reason for kp in contexts for reason in kp["priority_reasons"]]
        ranked.append(winner)
    ranked.sort(key=ranking_key)
    for rank, kp in enumerate(ranked, 1):
        kp["rank"] = rank
    ranks = {kp["db/id"]: kp["rank"] for kp in ranked}
    for topic in result["topics"]:
        for kp in topic["knowledge_points"]:
            kp["rank"] = ranks.get(kp["db/id"])
        topic["knowledge_points"].sort(key=lambda kp: (kp["rank"] or float("inf"), kp["db/id"]))
    result["topics"].sort(key=lambda topic: (min((kp["rank"] or float("inf") for kp in topic["knowledge_points"]), default=float("inf")), topic["db/id"]))
    result["knowledge_points"] = ranked
    result["assessment_coverage"] = {"unit": "distinct topics, one slot per topic",
                                     "target": dict(zip(COVERAGE_BANDS, COVERAGE_TARGET)),
                                     "available": dict(zip(COVERAGE_BANDS, before)),
                                     "missing": dict(zip(COVERAGE_BANDS, (n - c for n, c in zip(COVERAGE_TARGET, before)))),
                                     "topic_count": len(topic_bands)}
    result["scoring"] = {"formula": "purpose_points + 1000 * shortage + 100 * urgency_value",
                          "purpose_points": PURPOSE, "urgency_values": URGENCY,
                          "counting": "usable, unseen and unreserved; assessments require rated questions",
                          "queue": "generator-build", "refill_target_per_kp": {"easy": 5, "moderate": 5, "hard": 5}}
    result["sort_order"] = ["score_desc", "assessment_first_studied_at", "waiting_since", "topic_entity", "knowledge_point_entity"]
    return result


def build(edb_root, test=False):
    edb_deps = edb_root / "target/release/deps"
    edb = list(edb_deps.glob("libedb_core-*.rlib"))
    if len(edb) != 1:
        raise RuntimeError("Expected one matching release EDB library; build EDB or set --edb-root")
    libraries = {"edb_core": edb[0]}
    deps = ROOT / "target/release/deps"
    subprocess.run(["cargo", "build", "--release", "--lib", "--offline"], cwd=ROOT, check=True,
                   stdout=sys.stderr)
    for name in ("serde_json", "chrono", "course_academy_engine"):
        candidates = list(deps.glob(f"lib{name}-*.rlib"))
        if not candidates:
            subprocess.run(["cargo", "build", "--release", "--lib", "--offline"], cwd=ROOT, check=True)
            candidates = list(deps.glob(f"lib{name}-*.rlib"))
        libraries[name] = max(candidates, key=lambda p: p.stat().st_mtime_ns)
    sources = [HERE / "find_candidates.rs", HERE / "find_candidates_ranking.rs", *sorted((HERE / "queries").glob("*.edn"))]
    if test:
        sources.append(HERE / "find_candidates_tests.rs")
    fingerprint = hashlib.sha256(b"".join(p.read_bytes() for p in sources)
        + repr((test, [(str(p), p.stat().st_mtime_ns) for p in libraries.values()])).encode()).hexdigest()[:16]
    output = ROOT / ".local/generate" / f"find-candidates-{fingerprint}"
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = output.with_suffix(f".tmp-{os.getpid()}")
        command = ["rustc", "--edition=2024", "-O", str(HERE / "find_candidates.rs")]
        if test:
            command.append("--test")
        for name, path in libraries.items():
            command += ["--extern", f"{name}={path}"]
        command += ["-L", f"dependency={edb_deps}", "-L", f"dependency={deps}", "-o", str(staging)]
        try:
            subprocess.run(command, cwd=ROOT, check=True)
            staging.replace(output)
        finally:
            staging.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default=os.environ.get("EDB_DATABASE", DEFAULT_DATABASE))
    parser.add_argument("--learner", default=DEFAULT_LEARNER)
    parser.add_argument("--edb-root", type=Path, default=Path(os.environ.get("EDB_ROOT", ROOT.parent / "EDB")))
    parser.add_argument("--after-basis", type=int, help="Validate a previous cursor; ranking still uses the full eligible pool")
    parser.add_argument("--lineage", help="Database lineage accompanying --after-basis")
    parser.add_argument("--at", help="RFC3339 time for review eligibility; defaults to now")
    parser.add_argument("--topic", type=int, action="append", default=[], help="Scheduler-selected topic entity ID; repeatable")
    parser.add_argument("--activity-type", choices=["lesson", "review", "assessment"], default="assessment")
    parser.add_argument("--test", action="store_true", help="Run isolated native query fixtures without connecting to EDB")
    args = parser.parse_args()
    if (args.after_basis is None) != (args.lineage is None):
        parser.error("--after-basis and --lineage must be provided together")
    if args.after_basis is not None and args.after_basis < 0 or any(t <= 0 for t in args.topic):
        parser.error("basis must be nonnegative and topic IDs must be positive")
    binary = build(args.edb_root.resolve(), args.test)
    if args.test:
        subprocess.run([str(binary)], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(HERE),
                        "-p", "test_find_candidates.py"], cwd=ROOT, check=True)
    else:
        request = {"database":args.database,"learner":args.learner,"after_basis":args.after_basis,
            "lineage":args.lineage,"at":args.at,"topics":args.topic,"activity_type":args.activity_type}
        environment = database_environment(args.database)
        response = subprocess.run([str(binary)], input=json.dumps(request), text=True,
            env=environment, stdout=subprocess.PIPE, check=True)
        result = json.loads(response.stdout)
        check_generator_files(result, environment["EDB_MATH_ROOT"])
        print(json.dumps(ranked_candidates(result), indent=2))


if __name__ == "__main__":
    main()
