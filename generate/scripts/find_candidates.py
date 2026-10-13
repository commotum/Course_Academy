#!/usr/bin/env python3
"""Find inventory targets using native EDB reads; never transact or launch generators."""
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


def urgency(inventory):
    """Classify supported bands; unknown bands require classification first."""
    supported = inventory["supported_difficulties"]
    if not supported:
        return 0, "unclassified"
    counts = inventory["available"]
    values = [counts[band] for band in supported]
    if not any(values):
        return 0, "critical"
    if not all(values):
        return 1, "urgent"
    if any(counts[band] < {"easy": 3, "moderate": 2, "hard": 1}[band] for band in supported):
        return 2, "high"
    if any(n < 5 for n in values):
        return 3, "normal"
    return 4, "stocked"


def ranked_candidates(result):
    """Keep topic output and add a globally ranked, flat KP list."""
    states = {"needed-now": 0, "queued": 1, "target-related": 2, "unlocked": 3}
    ranked = []
    for topic in result["topics"]:
        kinds = {trigger["activity_type"] for trigger in topic["triggers"]}
        for kp in topic["knowledge_points"]:
            # Lessons draw within one KP; retrieval draws from the topic pool.
            inventories = []
            if "lesson" in kinds:
                inventories.append(("knowledge-point", kp["inventory"]))
            if kinds & {"review", "assessment"}:
                inventories.append(("topic", topic["topic_inventory"]))
            tier, label = min(urgency(pool) for _, pool in inventories)
            available_total = min(sum(pool["available"].values()) for _, pool in inventories)
            kp.update({"topic_entity": topic["db/id"], "topic_title": topic["topic/title"],
                       "activity_state": topic["activity_state"], "engine_priority": topic["engine_priority"],
                       "assignment_due": topic["assignment_due"], "urgency_tier": tier, "urgency": label,
                       "available_total": available_total,
                       "waiting_since": topic.get("waiting_since"),
                       "inventory_scopes": {scope: pool for scope, pool in inventories}})
            ranked.append(kp)

    def key(kp):
        due = kp["assignment_due"]
        waiting = kp.get("waiting_since")
        return (datetime.fromisoformat(due.replace("Z", "+00:00")).timestamp() if due else float("inf"),
                states[kp["activity_state"]], -kp["engine_priority"], kp["available_total"],
                datetime.fromisoformat(waiting.replace("Z", "+00:00")).timestamp() if waiting else float("inf"),
                kp["topic_entity"], kp["db/id"])

    ranked.sort(key=key)
    for rank, kp in enumerate(ranked, 1):
        kp["rank"] = rank
    for topic in result["topics"]:
        topic["knowledge_points"].sort(key=lambda kp: kp["rank"])
    result["topics"].sort(key=lambda topic: min((kp["rank"] for kp in topic["knowledge_points"]), default=float("inf")))
    result["knowledge_points"] = ranked
    result["sort_order"] = ["assignment_due", "activity_state", "engine_priority_desc", "available_total", "waiting_since", "entity_id"]
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
    parser.add_argument("--after-basis", type=int, help="Last successfully handed-off transaction basis")
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
        response = subprocess.run([str(binary)], input=json.dumps(request), text=True,
            env=database_environment(args.database), stdout=subprocess.PIPE, check=True)
        print(json.dumps(ranked_candidates(json.loads(response.stdout)), indent=2))


if __name__ == "__main__":
    main()
