"""Read saved captures; write derived evidence here, never to the DB or runners.

Candidate pools are observable proxies, not recovered server eligibility. Each
pool uses the latest progress pages saved at/before the first observed offer,
plus same-account successful lesson anchors aged at least 48 hours.
Diagnostic-credit topics without learning dates remain outside this proxy.
"""
import csv
import hashlib
import heapq
import json
import math
import random
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
AUDIT = ROOT / "reference/mathacademy/capture-audits/2026-10-11-assessment-patterns"
EDGES = ROOT / "reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/selected-relationships.json"
ACCOUNTS = ["foundations", "linear", "multivariable", "differential"]
manifest = {}


def rel(p):
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def read(p):
    b = p.read_bytes()
    manifest[rel(p)] = hashlib.sha256(b).hexdigest()
    return json.loads(b)


def epoch(v):
    if isinstance(v, (int, float)):
        return v
    return datetime.fromisoformat(v.replace("Z", "+00:00")).timestamp() if v else None


frozen = read(AUDIT / "evidence.json")
records = {(r["account"], r["task_id"]): dict(r) for r in frozen["records"]}
offers = {}
for r in frozen["first_old_queue_offers"] + read(AUDIT / "new-dashboard-offers.json"):
    k = (r["account"], str(r["task_id"]))
    if k not in offers or offers[k]["time"] > r["time"]:
        offers[k] = r

# Refresh modern captures without modifying the preceding audits' frozen data.
post_paths = sorted((ROOT / "reference/mathacademy/capture").glob("*/*/post-activity.json"))
posts = []
for p in post_paths:
    a, task = p.parts[-3:-1]
    if a not in ACCOUNTS:
        continue
    d = read(p)
    posts.append((a, p, d))
    activity = read(p.parent / "activity.json")
    cp = read(p.parent / "checkpoint.json")
    completion = d.get("completion") or {}
    records[a, task] = {
        "account": a, "task_id": task, "kind": activity["kind"],
        "topic_id": str(activity["topic_id"]) if activity.get("topic_id") else None,
        "course_id": str(activity.get("course_id")), "title": activity.get("title"),
        "completed_at": cp.get("completed_at"), "started_at": cp.get("started_at"),
        "complete": bool(cp.get("completed_at")),
        "passed": "failed" not in completion.get("text", "").lower(),
        "retake": bool(activity.get("details", {}).get("retake")) or "retake" in activity.get("title", "").lower(),
        "source": rel(p.parent / "activity.json"),
    }
    obs = [d.get("observations") or {}] + [h.get("observations") or {} for h in d.get("observation_history", [])]
    for o in obs:
        dash = o.get("dashboard") or {}
        fn, at = dash.get("html_path"), epoch(dash.get("captured_at"))
        if not fn or not at:
            continue
        htmlpath = Path(fn)
        raw = htmlpath.read_bytes()
        manifest[rel(htmlpath)] = hashlib.sha256(raw).hexdigest()
        s = raw.decode()
        course = re.search(r'id="courseNameLink"[^>]*href="/courses/(\d+)', s)
        if not course:
            continue
        # Restrict to unlocked cards, never completed-task history.
        s = s.split('id="completedTasks"')[0]
        starts = list(re.finditer(r'<div\b[^>]*(?:class="taskUnlocked"[^>]*id="task-(\d+)"|id="task-(\d+)"[^>]*class="taskUnlocked")[^>]*>', s))
        for i, m in enumerate(starts):
            card = s[m.end():starts[i+1].start() if i+1 < len(starts) else len(s)]
            if not re.search(r'taskTypeUnlocked[^>]*>\s*Assessment', card):
                continue
            tid = m[1] or m[2]
            k = a, tid
            if k not in offers or at < offers[k]["time"]:
                offers[k] = {"account": a, "task_id": tid, "course_id": course[1],
                             "time": at, "source": rel(htmlpath)}

corrections = {("foundations", "13945962"): epoch("2026-10-04T19:31:35.217-07:00"),
               ("multivariable", "14041552"): epoch("2026-10-08T01:11:06.326-07:00")}
lessons, reviews, diagnostics = defaultdict(list), defaultdict(list), defaultdict(list)
quizzes = []
for k, r in records.items():
    if not r.get("complete") or not r.get("completed_at"):
        continue
    if r["kind"] in ("lesson", "review"):
        if "passed" not in r:
            s = read(ROOT / r["source"])
            r["passed"] = s.get("activity_outcome") != "failed" and "failed" not in str(s.get("completion", {})).lower()
        if r["passed"]:
            (lessons if r["kind"] == "lesson" else reviews)[r["account"], str(r["topic_id"])].append(r)
    elif r["kind"] == "diagnostic":
        diagnostics[r["account"]].append(r)
    elif r["kind"] == "assessment":
        if k not in offers:
            continue
        content = read((ROOT / r["source"]).parent / "content.json")
        state = read(ROOT / r["source"]) if r["source"].endswith("state.json") else {}
        questions = content.get("questions", [])
        topics = []
        unattributed = []
        for q in questions:
            href = q.get("kp_href") or q.get("provenance", {}).get("kp_href")
            match = re.search(r"/topics/(\d+)", href or "")
            tid = str(q.get("topic_id"))
            if not match or tid == "None":
                unattributed.append({"question_id": q.get("math_academy_id"), "kp_href": href})
                continue
            assert match and match[1] == tid, (k, tid, href)
            saved = state.get("questions", {}).get(q.get("math_academy_id"), {})
            result = q.get("result") or saved.get("actual_result") or saved.get("after", {}).get("result")
            topics.append({"topic_id": tid, "question_id": q.get("math_academy_id"),
                           "knowledge_point": q.get("knowledge_point"), "result": result,
                           "kp_href": href})
        assert len({q["topic_id"] for q in topics}) == len(topics), k
        quizzes.append({**r, "offer": offers[k], "questions": topics, "unattributed_questions": unattributed, "pool": {}})
for rows in lessons.values():
    for r in rows:
        r["anchor"] = corrections.get((r["account"], r["task_id"]), r["completed_at"])
    rows.sort(key=lambda r: r["anchor"])
quizzes.sort(key=lambda r: r["offer"]["time"])

native = {}
for m in frozen["xp_topic_membership_metrics"]:
    p = Path(m["membership_source"])
    manifest[rel(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    native[m["course_id"]] = {r["topic-id"] for r in csv.DictReader(p.open())}
for cid, suffix in [("111", "II"), ("136", "III")]:
    p = Path(f"/home/jake/Developer/MA/COURSES/Math-Academy/Mathematical-Foundations/Mathematical-Foundations-{suffix}/GRAPH-Mathematical-Foundations-{suffix}/Topics.csv")
    manifest[rel(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    native[cid] = {r["topic-id"] for r in csv.DictReader(p.open())}

# Keep the latest complete page strictly at/before each offer. A later page must
# not supply that assessment's own pre-selection evidence.
def snapshot(a, p, courses, fallback=None):
    for c in courses:
        cid, at = str(c.get("course_id")), epoch(c.get("captured_at") or fallback)
        if not at:
            continue
        for q in quizzes:
            if q["account"] != a or at > q["offer"]["time"]:
                continue
            old = q["pool"].get(cid)
            if old is None or at > old["at"]:
                q["pool"][cid] = {"at": at, "source": rel(p), "topics": c.get("topics", [])}

snapshot_files = Counter()
for a in ACCOUNTS:
    base = ROOT / ("reference/mathacademy/question-capture" if a == "foundations" else f"reference/mathacademy/question-capture-workers/{a}")
    for p in sorted(base.glob("*/knowledge-state/*.json")):
        d = read(p)
        snapshot(a, p, d.get("courses", []), d.get("finished_at"))
        snapshot_files[a] += 1
for a, p, d in posts:
    for o in [d.get("observations") or {}] + [h.get("observations") or {} for h in d.get("observation_history", [])]:
        snapshot(a, p, o.get("courses", []), o.get("observed_at"))
    snapshot_files[a] += 1

edge_records = read(EDGES)


def edge_graph(account=None, before=None):
    g = defaultdict(dict)
    for e in edge_records:
        if account is None:
            weight = e["weight"]
        else:
            local = next((x for x in e["account_estimates"] if x["account"] == account), None)
            if local is None:
                continue
            exposures = [x for x in local["sequence"] if epoch(x["at"]) < before]
            if not exposures or not any(x["rising"] for x in exposures):
                continue
            # Time-local crossing frequency, not the final fitted fraction.
            weight = sum(x["rising"] for x in exposures) / len(exposures)
        g[e["source"]][e["target"]] = weight
    return g


def closure(g, source):
    # Topological flow makes explicit overrides apply before propagating further,
    # matching core.rs; overriding only the final answers would not do that.
    reachable = {source}
    todo = [source]
    while todo:
        for target in g.get(todo.pop(), {}):
            if target not in reachable:
                reachable.add(target)
                todo.append(target)
    degrees = dict.fromkeys(reachable, 0)
    for node in reachable:
        for target in g.get(node, {}):
            degrees[target] += 1
    todo = sorted(n for n in reachable if degrees[n] == 0)
    best = {source: 1.0}
    processed = 0
    while todo:
        node = todo.pop()
        processed += 1
        if node != source and node in g.get(source, {}):
            best[node] = g[source][node]
        for target, weight in g.get(node, {}).items():
            best[target] = max(best.get(target, 0), best.get(node, 0)*weight)
            degrees[target] -= 1
            if degrees[target] == 0:
                todo.append(target)
    assert processed == len(reachable), "Encompassing cycle"
    best.pop(source, None)
    return best


fixed_graph = edge_graph()
fixed_closures = {}
output = []
for q in quizzes:
    a, at, cid = q["account"], q["offer"]["time"], q["course_id"]
    selected = {x["topic_id"] for x in q["questions"]}
    # Count only quizzes actually completed before this observed offer; include
    # retakes as assessment exposure, never diagnostics as ordinary quiz history.
    earlier = [p for p in quizzes if p["account"] == a and p["task_id"] != q["task_id"] and p["completed_at"] < at]
    tested = {x["topic_id"] for p in earlier for x in p["questions"]}
    latest_diag = max((r["completed_at"] for r in diagnostics[a] if r["completed_at"] < at), default=None)
    pages = {c:p for c,p in q["pool"].items() if at-p["at"] <= 3600}
    observed = {}
    for scope, p in pages.items():
        for t in p["topics"]:
            tid = str(t["topic_id"])
            if tid not in observed or observed[tid]["at"] < p["at"]:
                observed[tid] = {**t, "at": p["at"], "source": p["source"], "scope": scope}
    rows = []
    if pages:
        for topic in observed.values():
            tid = str(topic["topic_id"])
            ls = [r for r in lessons[a, tid] if r["anchor"] < at]
            band = topic.get("display_band")
            if not ls or at - ls[0]["anchor"] < 48*3600 or not isinstance(band, int) or band <= 0:
                continue
            age = (at - ls[0]["anchor"])/3600
            rs = [r for r in reviews[a, tid] if r["completed_at"] < at]
            previous = [p for p in earlier if any(x["topic_id"] == tid for x in p["questions"])]
            rows.append({"topic_id": tid, "title": topic["title"], "selected": tid in selected,
                         "previously_tested": tid in tested, "prior_test_count": len(previous),
                         "last_test_age_hours": (at-max(p["completed_at"] for p in previous))/3600 if previous else None,
                         "prior_wrong_count": sum(x["result"] == "Incorrect" for p in previous for x in p["questions"] if x["topic_id"] == tid),
                         "prior_correct_count": sum(x["result"] == "Correct" for p in previous for x in p["questions"] if x["topic_id"] == tid),
                         "native": tid in native.get(cid, set()), "band": band, "age_hours": age,
                         "band_source": topic["source"], "band_scope": topic["scope"], "band_at": topic["at"],
                         "lesson_id": ls[0]["task_id"], "lesson_source": ls[0]["source"],
                         "learned_after_latest_diagnostic": latest_diag is None or ls[0]["anchor"] > latest_diag,
                         "prior_review_count": len(rs),
                         "last_review_age_hours": (at-max(r["completed_at"] for r in rs))/3600 if rs else None})
    ids = {r["topic_id"] for r in rows}
    local_graph = edge_graph(a, at)
    cover = {"retrospective_graph": {}, "preoffer_local_graph": {}}
    for source in ids:
        if source not in fixed_closures:
            fixed_closures[source] = closure(fixed_graph, source)
        for label, paths in [("retrospective_graph", fixed_closures[source]), ("preoffer_local_graph", closure(local_graph, source))]:
            for target, weight in paths.items():
                if target not in ids:
                    continue
                if weight > cover[label].get(target, {}).get("weight", 0):
                    cover[label][target] = {"weight": weight, "source_topic": source}
    for r in rows:
        for label, cs in cover.items():
            r[label] = cs.get(r["topic_id"], {"weight": 0, "source_topic": None})
    output.append({"account": a, "task_id": q["task_id"], "title": q["title"], "course_id": cid,
                   "retake": q["retake"], "offer": q["offer"], "completed_at": q["completed_at"],
                   "questions": q["questions"], "unattributed_questions": q["unattributed_questions"], "previously_tested_selected": sorted(selected & tested),
                   "preoffer_pages": {c:{k:v for k,v in p.items() if k != "topics"} for c,p in pages.items()},
                   "page_gap_seconds": at-max(p["at"] for p in pages.values()) if pages else None,
                   "selected_outside_proxy_pool": sorted(selected-ids), "candidates": rows,
                   "native_membership_known": cid in native})


def table(qs, field, predicate=lambda r: True):
    groups = defaultdict(lambda: Counter())
    for q in qs:
        for r in q["candidates"]:
            if predicate(r):
                g = str(field(r))
                groups[g]["candidate_appearances"] += 1
                groups[g]["selected"] += r["selected"]
    return {k: {**v, "selection_rate": v["selected"]/v["candidate_appearances"]} for k,v in groups.items()}


ordinary = [q for q in output if not q["retake"]]
usable = [q for q in ordinary if q["page_gap_seconds"] is not None and q["candidates"]]


def mh(qs, exposed, restrict=lambda r: True):
    """Descriptive common odds ratio conditional on quiz and course membership.

    Repeated topics/accounts are not independent; no significance test/CI.
    """
    num = den = 0
    strata = 0
    for q in qs:
        for is_native in [False, True]:
            rs = [r for r in q["candidates"] if r["native"] == is_native and restrict(r)]
            a = sum(r["selected"] and exposed(r) for r in rs)
            b = sum(not r["selected"] and exposed(r) for r in rs)
            c = sum(r["selected"] and not exposed(r) for r in rs)
            d = sum(not r["selected"] and not exposed(r) for r in rs)
            if (a+b)*(c+d)*(a+c)*(b+d) == 0:
                continue
            num += a*d/len(rs)
            den += b*c/len(rs)
            strata += 1
    return {"strata": strata, "odds_ratio": num/den if den else None}


summary = {
    "records": len(records), "snapshot_files": dict(snapshot_files), "input_files": len(manifest),
    "assessment_tasks": len(output), "ordinary_tasks": len(ordinary),
    "question_appearances": sum(len(q["questions"]) for q in output),
    "ordinary_question_appearances": sum(len(q["questions"]) for q in ordinary),
    "unattributed_question_slots": sum(len(q["unattributed_questions"]) for q in output),
    "ordinary_repeated_topic_appearances": sum(len(q["previously_tested_selected"]) for q in ordinary),
    "usable_proxy_pool_tasks": len(usable), "pool_candidate_appearances": sum(len(q["candidates"]) for q in usable),
    "selected_within_proxy_pool": sum(r["selected"] for q in usable for r in q["candidates"]),
    "selected_outside_proxy_pool": sum(len(q["selected_outside_proxy_pool"]) for q in usable),
    "by_account": {},
    "prior_test_table": table(usable, lambda r: r["previously_tested"]),
    "prior_test_native_only": table(usable, lambda r: r["previously_tested"], lambda r: r["native"]),
    "prior_result_table": table(usable, lambda r: "never_tested" if not r["previously_tested"] else "prior_wrong" if r["prior_wrong_count"] else "prior_correct_only" if r["prior_correct_count"] else "prior_result_unknown"),
    "age_table": table(usable, lambda r: "48–60h" if r["age_hours"]<60 else "60–72h" if r["age_hours"]<72 else "72h+"),
    "band_table": table(usable, lambda r: r["band"]),
    "encompassing_table": table(usable, lambda r: "none" if r["preoffer_local_graph"]["weight"]==0 else "under_half" if r["preoffer_local_graph"]["weight"]<.5 else "half_or_more"),
    "prior_test_odds_ratio": mh(usable, lambda r: r["previously_tested"]),
    "prior_test_after_diagnostic_odds_ratio": mh(usable, lambda r: r["previously_tested"], lambda r: r["learned_after_latest_diagnostic"]),
    "encompassing_odds_ratio": mh(usable, lambda r: r["preoffer_local_graph"]["weight"]>=.5),
    "encompassing_untested_odds_ratio": mh(usable, lambda r: r["preoffer_local_graph"]["weight"]>=.5, lambda r: not r["previously_tested"]),
    "retrospective_encompassing_untested_odds_ratio": mh(usable, lambda r: r["retrospective_graph"]["weight"]>=.5, lambda r: not r["previously_tested"]),
}
for a in ACCOUNTS:
    qs = [q for q in usable if q["account"] == a]
    allqs = [q for q in ordinary if q["account"] == a]
    summary["by_account"][a] = {
        "ordinary_tasks": len(allqs), "questions": sum(len(q["questions"]) for q in allqs),
        "repeat_questions": sum(len(q["previously_tested_selected"]) for q in allqs),
        "usable_pools": len(qs), "prior_test_table": table(qs, lambda r: r["previously_tested"]),
        "prior_test_odds_ratio": mh(qs, lambda r: r["previously_tested"]),
        "encompassing_untested_odds_ratio": mh(qs, lambda r: r["preoffer_local_graph"]["weight"]>=.5, lambda r: not r["previously_tested"]),
    }

# Find concrete counterexamples to a hard untested-first rule, holding native
# course membership fixed. Such a rule is not the existing implementation's
# effective behavior unless all candidate-admission assumptions are correct.
counterexamples = []
for q in usable:
    for native_status in [True, False]:
        rs = [r for r in q["candidates"] if r["native"] == native_status]
        repeated = [r for r in rs if r["selected"] and r["previously_tested"]]
        waiting = [r for r in rs if not r["selected"] and not r["previously_tested"]]
        if repeated and waiting:
            counterexamples.append({"account": q["account"], "task_id": q["task_id"], "native": native_status,
                                    "page_sources": q["preoffer_pages"],
                                    "repeated_selected": repeated, "untested_not_selected": waiting})

# Monte Carlo replay tests simple relative weights, conditional on how many
# questions fell INSIDE our known-age proxy. This is sensitivity analysis, not
# identification of MA's weights or a complete server-quiz reproduction.
simulations = []
for history_weight in [1, .5, .25, .1]:
    for coverage_strength in [0, .75]:
        for course_weight in [1, 4]:
            totals = Counter()
            expected = Counter()
            rng = random.Random(10122026)
            for q in usable:
                rs = q["candidates"]
                n = sum(r["selected"] for r in rs)
                if not n:
                    continue
                for r in rs:
                    if r["selected"]:
                        totals["repeat"] += r["previously_tested"]
                        totals["covered"] += r["preoffer_local_graph"]["weight"] >= .5
                        totals["native"] += r["native"]
                weights = [(history_weight if r["previously_tested"] else 1)*(1-coverage_strength*r["preoffer_local_graph"]["weight"])*(course_weight if r["native"] else 1) for r in rs]
                for _ in range(500):
                    # Exponential races implement weighted draws without replacement.
                    chosen = heapq.nsmallest(n, range(len(rs)), key=lambda i: -math.log(max(rng.random(), 1e-15))/weights[i])
                    for i in chosen:
                        expected["repeat"] += rs[i]["previously_tested"]/500
                        expected["covered"] += (rs[i]["preoffer_local_graph"]["weight"]>=.5)/500
                        expected["native"] += rs[i]["native"]/500
            simulations.append({"history_weight": history_weight, "coverage_strength": coverage_strength,
                                "native_course_weight": course_weight, "observed": dict(totals), "expected": dict(expected)})

assert all(p["at"]<=q["offer"]["time"] for q in output for p in q["preoffer_pages"].values())
assert all(r["age_hours"]>=48 for q in output for r in q["candidates"])
assert all(0<=r["preoffer_local_graph"]["weight"]<=1 for q in output for r in q["candidates"])
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "evidence.json").write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "summary": summary, "quizzes": output, "hard_priority_counterexamples": counterexamples, "simulations": simulations}, indent=2)+"\n")
(OUT / "input-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
print(json.dumps(summary, indent=2))
print("Hard-priority counterexample strata:", len(counterexamples))
print("Simulations:", json.dumps(simulations))
