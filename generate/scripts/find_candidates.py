#!/usr/bin/env python3
"""Rank generator-build candidates using native EDB reads; never transact or generate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from generator_packages import resolve_registered_script
from generator_priority import PRIORITY_FIELDS, PRIORITY_POLICY, PURPOSE_ORDER, priority_key


URGENCY = {"studied": 5, "target": 4, "queued": 3, "target-prerequisite": 2,
           "selected-prerequisite": 2, "studied-or-queued-descendant": 1,
           "immediate": 7, "current-need": 6}
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


ranking_key = priority_key


def baseline_relevance(topic):
    if topic.get("new_scoped_lesson"):
        return 1
    if topic.get("relevance_tier") is not None:
        return topic["relevance_tier"]
    groups = set(topic.get("urgency_groups", []))
    if groups & {"queued", "target"}:
        return 1
    if groups & {"target-prerequisite", "selected-prerequisite"}:
        return 2
    if groups & {"studied", "current-need", "immediate"}:
        return 3
    return 4


def activity_demands(topic, relevance):
    """Native demand is explicit; old snapshots retain their next-stage demand."""
    demands = topic.get("activity_demands")
    if demands is None:
        demands = [{"activity_type": topic["next_activity"], "relevance_tier": relevance}]
        if (topic.get("completed_local_lesson") is False and relevance == 1
                and topic["next_activity"] != "lesson"):
            demands.append({"activity_type": "lesson", "relevance_tier": relevance})
    stages = {}
    for demand in demands:
        stage = demand["activity_type"]
        if stage not in {"lesson", "review", "assessment"}:
            raise ValueError("Unknown activity demand: " + str(stage))
        tier = demand.get("relevance_tier", relevance)
        stages[stage] = min(stages.get(stage, tier), tier)
    return stages


def selection_gate(topics, *, self_directed=False):
    """Report Study shortages; only legacy course mode gates broader authoring."""
    selected_topics, selected_kps, missing, understocked = set(), set(), set(), set()
    for topic in topics:
        selected = topic.get("new_scoped_lesson", False) if self_directed else (
            bool(set(topic.get("urgency_groups", [])) & {"queued", "target"}))
        if not selected:
            continue
        selected_topics.add(topic["db/id"])
        for kp in topic["knowledge_points"]:
            kp_id = kp["db/id"]
            selected_kps.add(kp_id)
            script = kp.get("generator_script")
            if not (kp.get("generator_usable") and isinstance(script, str)
                    and script.startswith("generators/")):
                missing.add(kp_id)
            low = available_total(kp["inventory"]) < 5 if self_directed else (
                any(kp["inventory"]["available"].get(band, 0) < 5 for band in COVERAGE_BANDS))
            if low:
                understocked.add(kp_id)
    return {"open": self_directed or (not missing and not understocked),
            "mode": "study-scope" if self_directed else "direct-selection-completion",
            "selected_knowledge_points": sorted(selected_kps),
            "missing_generators": sorted(missing),
            "understocked_knowledge_points": sorted(understocked),
            "required_per_band": None if self_directed else 5,
            "required_total": 5 if self_directed else None,
            "selected_topic_count": len(selected_topics),
            "selected_knowledge_point_count": len(selected_kps)}


def ranked_candidates(result):
    """Keep complete nested inventories; rank one build job per KP by its strongest reason."""
    self_directed = result.get("self_directed", False)
    gate = selection_gate(result["topics"], self_directed=self_directed)
    result["selection_gate"] = gate
    selected_kps = set(gate["selected_knowledge_points"])
    topic_bands = {}
    for topic in result["topics"]:
        groups = [group for group in topic.get("urgency_groups", []) if group in URGENCY]
        topic["urgency_value"] = max((URGENCY[group] for group in groups), default=0)
        if topic["urgency_value"] and topic.get("studied") and topic.get("reviewed"):
            topic_bands[topic["db/id"]] = {band for band, count in topic["topic_inventory"]["available"].items() if count > 0}
    before = coverage(topic_bands)
    usable = {kp["db/id"] for topic in result["topics"] for kp in topic["knowledge_points"]
              if kp.get("generator_usable", kp.get("has_generator", False))}
    candidates = {}
    for topic in result["topics"]:
        topic_id, u = topic["db/id"], topic["urgency_value"]
        relevance = baseline_relevance(topic)
        demands = activity_demands(topic, relevance)
        for kp in topic["knowledge_points"]:
            for field in ("generated_band", "improved_coverage_band", "coverage_after"):
                kp.pop(field, None)
            stage = topic["next_activity"]
            if stage not in {"lesson", "review", "assessment"}:
                raise ValueError("Unknown next activity: " + str(stage))
            scope = "knowledge-point" if stage == "lesson" else "topic"
            pool = kp["inventory"] if stage == "lesson" else topic["topic_inventory"]
            def stock(activity):
                inventory_scope = "knowledge-point" if activity == "lesson" else "topic"
                inventory = kp["inventory"] if activity == "lesson" else topic["topic_inventory"]
                return {"next_activity": activity, "inventory_scope": inventory_scope,
                        "available_total": available_total(inventory, rated=activity == "assessment"),
                        "required_total": 1 if activity == "assessment" else 5}

            context = {field: topic.get(field) for field in PRIORITY_FIELDS
                       if field not in {"priority_policy", "relevance_tier", "baseline_relevance_tier"}}
            context.update({"priority_policy": PRIORITY_POLICY,
                            "relevance_tier": relevance, "baseline_relevance_tier": relevance,
                            "topic_entity": topic_id, "topic_title": topic["topic/title"],
                            "db/id": kp["db/id"]})
            kp.update({"topic_entity": topic_id, "topic_title": topic["topic/title"],
                       "next_activity": stage, "urgency_groups": topic.get("urgency_groups", []),
                       "urgency_value": u,
                       "kp_available_total": available_total(kp["inventory"]),
                       "inventory_scopes": {**{scope: pool},
                                            **({"knowledge-point": kp["inventory"]} if "lesson" in demands else {}),
                                            **({"topic": topic["topic_inventory"]} if demands.keys() & {"review", "assessment"} else {})},
                       "refill_deficits": {band: max(0, 5 - count) for band, count in kp["inventory"]["available"].items()},
                       "rank": None, **context, **stock(stage)})
            reasons = []
            def reason(purpose, shortage, **extra):
                reasons.append({**context, **stock(stage),
                                "purpose": purpose, "purpose_points": PURPOSE[purpose],
                                "shortage": shortage, "shortage_points": 1000 * shortage,
                                "urgency_points": 100 * u,
                                "score": PURPOSE[purpose] + 1000 * shortage + 100 * u,
                                **extra})
            reason("advance-build", 0)
            for activity, demand_relevance in demands.items():
                supply = stock(activity)
                shortage = supply["required_total"] - supply["available_total"]
                if shortage > 0:
                    reason(activity + "-shortage", shortage,
                           **supply, relevance_tier=demand_relevance)
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
            reasons.sort(key=priority_key)
            kp.update(reasons[0])
            kp["priority_reasons"] = reasons
            admitted = bool(demands) if self_directed else (gate["open"] or kp["db/id"] in selected_kps)
            kp["build_eligible"] = bool(u) and admitted
            kp["build_required"] = kp["build_eligible"] and kp["db/id"] not in usable
            kp["build_exclusion_reason"] = ("outside-urgency-groups" if not u else
                                             ("outside-study-demand" if self_directed else "selected-inventory-incomplete") if not admitted else
                                             "usable-generator-registered" if kp["db/id"] in usable else None)
            kp["build_action"] = ("repair-generator" if kp.get("has_generator") else "create-generator") if kp["build_required"] else None
            if kp["build_required"]:
                candidates.setdefault(kp["db/id"], []).append(kp)
    ranked = []
    for contexts in candidates.values():
        winner = dict(min(contexts, key=ranking_key))
        winner["candidate_topics"] = sorted({kp["topic_entity"] for kp in contexts})
        winner["priority_reasons"] = sorted(
            (reason for kp in contexts for reason in kp["priority_reasons"]), key=priority_key)
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
    result["priority_policy"] = PRIORITY_POLICY
    result["scoring"] = {"formula": "purpose_points + 1000 * shortage + 100 * urgency_value",
                          "use": "diagnostic only; priority_policy determines ordering",
                          "purpose_points": PURPOSE, "urgency_values": URGENCY,
                          "counting": "usable, unseen and unreserved; assessments require rated questions",
                          "queue": "generator-build", "refill_target_per_kp": {"easy": 5, "moderate": 5, "hard": 5}}
    result["sort_order"] = ["shortage_urgency", "relevance_tier", "purpose", "purpose_specific_topic_order",
                            "waiting_since", "topic_entity", "shortage_desc", "knowledge_point_entity"]
    result["priority_order"] = {
        "admission": ("All bounded new-lesson and current activity demands; no all-selected stock gate" if self_directed else
                      "Direct queue/target completion gate; approved refills run independently"),
        "urgency": ["immediate activity shortage", "ordinary activity shortage", "assessment variety", "advance preparation and routine replenishment"],
        "relevance": ["immediate obligation", "bounded new lessons and direct study", "other prerequisite preparation",
                      "other current study", "speculative preparation"],
        "purpose": list(PURPOSE_ORDER),
        "lesson_topic": ["topic_layer", "selected_support_count_desc", "engine_priority_desc"],
        "review_topic": ["review_due_at", "engine_priority_desc"],
        "assessment_topic": ["first_studied_at", "engine_priority_desc"],
    }
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


def discover(database, learner, environment, *, binary, after_basis=None, lineage=None,
             at=None, topics=(), activity_type="assessment", include_registered=False):
    """Capture bounded Study demand together; preserve the course-mode gate."""
    request = {"database": database, "learner": learner, "after_basis": after_basis,
               "lineage": lineage, "at": at, "topics": list(topics),
               "activity_type": activity_type, "include_registered": include_registered,
               "respect_study_scope": True}
    def capture(selected_only):
        response = subprocess.run([str(binary)], input=json.dumps({**request, "selected_only": selected_only}),
                                  text=True, env=environment, stdout=subprocess.PIPE,
                                  check=True, timeout=180)
        result = json.loads(response.stdout)
        check_generator_files(result, environment["EDB_MATH_ROOT"])
        return ranked_candidates(result)

    primary = capture(True)
    if primary.get("self_directed"):
        # Native discovery already captured the full current-need population at
        # one basis. No direct-selection stock gate can hide a scoped lesson.
        return primary
    if not primary["selection_gate"]["open"]:
        return primary
    # Recompute the gate on the full snapshot: a newly selected topic or consumed
    # question between captures must close admission again before workers run.
    return capture(False)


def main():
    from serve_graph_explorer import DEFAULT_DATABASE, DEFAULT_LEARNER, database_environment
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default=os.environ.get("EDB_DATABASE", DEFAULT_DATABASE))
    parser.add_argument("--learner", default=DEFAULT_LEARNER)
    parser.add_argument("--edb-root", type=Path, default=Path(os.environ.get("EDB_ROOT", ROOT.parent / "EDB")))
    parser.add_argument("--after-basis", type=int, help="Validate a previous cursor; ranking still uses the full eligible pool")
    parser.add_argument("--lineage", help="Database lineage accompanying --after-basis")
    parser.add_argument("--at", help="RFC3339 time for review eligibility; defaults to now")
    parser.add_argument("--topic", type=int, action="append", default=[], help="Scheduler-selected topic entity ID; repeatable")
    parser.add_argument("--activity-type", choices=["lesson", "review", "assessment"], default="assessment")
    parser.add_argument("--include-registered", action="store_true",
                        help="Also inspect registered packages outside urgency groups for ongoing replenishment")
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
        environment = database_environment(args.database)
        result = discover(args.database, args.learner, environment, binary=binary,
                          after_basis=args.after_basis, lineage=args.lineage, at=args.at,
                          topics=args.topic, activity_type=args.activity_type,
                          include_registered=args.include_registered)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
