"""Read-only analysis of saved Math Academy activity and queue evidence.

Run from the repository root. Writes only this audit's derived JSON.
Course IDs in progress scopes are deliberately NOT treated as enrollment IDs.
"""
import csv
import html
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MA = ROOT / "reference/mathacademy"
ACCOUNTS = ["foundations", "linear", "multivariable", "differential"]
NAMES = {"111": "Mathematical Foundations II", "136": "Mathematical Foundations III",
         "55": "Linear Algebra", "54": "Multivariable Calculus", "61": "Differential Equations",
         "76": "Methods of Proof", "154": "Mathematical Methods for the Physical Sciences I",
         "155": "Mathematical Methods for the Physical Sciences II", "145": "Mathematics for Machine Learning"}
NAMES.update({"historical:Calculus I": "Calculus I", "historical:Calculus II": "Calculus II"})


def read(path):
    return json.loads(path.read_text()) if path.exists() else {}


def stamp(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            pass
    return None


def local(value):
    return datetime.fromtimestamp(value, ZoneInfo("America/Los_Angeles")).isoformat() if value else None


def relative(path):
    return str(path.relative_to(ROOT))


def course_at(account, task_id):
    """Reconstruct OLD enrollment episodes from diagnostics and retained profiles.

    Main MF II -> MF III boundary inferred from quiz numbering restart, course
    content and retained MF III profile; do not pretend it is an exact enrollment
    timestamp. Other boundaries are explicit placement task IDs on each account.
    """
    tid = int(task_id)
    if account == "foundations":
        return "154" if tid >= 14070542 else "136" if tid >= 13949162 else "111"
    if account == "linear":
        return "76" if tid >= 14095701 else "54" if tid >= 14095567 else "55"
    if account == "multivariable":
        return "61" if tid >= 14097559 else "76" if tid >= 14097330 else "54"
    return "61"


def compact_card(card):
    return {k: card.get(k) for k in ["task_id", "title", "topic_id", "optional_xp_remaining",
            "assessment_requirement", "progress", "in_progress", "assessment_is_retake"]}


records = {}
queues = []
first_seen = {}
ledger = {}
for account in ACCOUNTS:
    state_root = ROOT / (".local/question_capture" if account == "foundations"
                         else f".local/question_capture-workers/{account}")
    events = [json.loads(line) for line in (state_root / "journal.jsonl").read_text().splitlines()]
    finishes = {str(e["task_id"]): e["timestamp"] for e in events
                if e.get("event") == "activity_captured"}
    for day, tasks in read(state_root / "daily-xp.json").items():
        for tid, xp in tasks.items():
            ledger[(account, str(tid))] = {"earned": xp.get("earned"), "base": xp.get("base"),
                                          "date": day, "source": relative(state_root / "daily-xp.json")}
    for e in events:
        if e.get("event") not in ("queue_observed", "queue_observation_corrected"):
            continue
        q = e.get("queue", [])
        diag = next((i for i in q if i.get("task_type") == "diagnostic"), None)
        assessment = next((i for i in q if i.get("task_type") == "assessment"), None)
        anchor = (assessment or {}).get("task_id") or e.get("after_task_id") or (q[0].get("task_id") if q else None)
        cid = str(diag["course_id"]) if diag and diag.get("course_id") else course_at(account, anchor) if anchor else None
        row = {"account": account, "time": e["timestamp"], "local_time": local(e["timestamp"]),
               "course_id": cid, "course_basis": "diagnostic" if diag else "inferred enrollment episode",
               "after_task_id": e.get("after_task_id"), "selected": (e.get("selected") or {}).get("task_id"),
               "tasks": [{"task_id": i.get("task_id"), "kind": i.get("task_type"),
                          "title": i.get("title"), "in_progress": i.get("in_progress")} for i in q],
               "assessments": [compact_card(i) for i in q if i.get("task_type") == "assessment"],
               "source": relative(state_root / "journal.jsonl")}
        queues.append(row)
        for c in row["assessments"]:
            key = (account, str(c["task_id"]))
            if key not in first_seen or row["time"] < first_seen[key]["time"]:
                first_seen[key] = {**c, **{k: row[k] for k in ["account", "time", "local_time", "course_id", "source", "after_task_id", "selected"]}}

    old_root = MA / ("question-capture" if account == "foundations" else f"question-capture-workers/{account}")
    for p in old_root.glob("*/state.json"):
        d = read(p)
        tid = str(d["task_id"])
        cid = str(d["course_id"]) if d.get("course_id") else course_at(account, tid)
        aq = read(p.parent / "assessment-queue.json")
        snap_times = [stamp(s.get("finished_at")) for s in d.get("knowledge_snapshots", {}).values() if isinstance(s, dict)]
        snap_times = [s for s in snap_times if s]
        completed_at = min(snap_times) if snap_times else finishes.get(tid)
        grades = Counter(str(q.get("actual_result", q.get("live_result", q.get("after", {}).get("result", "unknown"))))
                         for q in d.get("questions", {}).values())
        records[(account, tid)] = {
            "account": account, "task_id": tid, "kind": d.get("task_type"), "course_id": cid,
            "course_basis": "explicit diagnostic" if d.get("course_id") else "inferred enrollment episode",
            "title": d.get("title", aq.get("title")), "topic_id": str(d.get("topic_id")) if d.get("topic_id") else None,
            "complete": bool(d.get("activity_complete")), "completed_at": completed_at,
            "completion_time_basis": "post-activity snapshot (may be recovered)" if snap_times else "capture journal",
            "started_at": d.get("assessment_pacing", {}).get("started_at"),
            "grades": dict(grades) if d.get("task_type") in ["diagnostic", "assessment"] else None,
            "answer_policy": d.get("answer_policy"), "diagnostic_id": d.get("diagnostic_id"),
            "retake": bool(d.get("assessment_is_retake", aq.get("assessment_is_retake", False))),
            "source": relative(p), "xp": ledger.get((account, tid)),
        }

    for tid, xp in read(ROOT / f".local/capture/{account}/xp.json").items():
        ledger[(account, tid)] = {"earned": xp.get("earned_xp"), "base": xp.get("base_xp"),
                                  "date": xp.get("date"), "source": relative(ROOT / f".local/capture/{account}/xp.json")}
    for p in (MA / f"capture/{account}").glob("*/activity.json"):
        d = read(p)
        cp = read(p.parent / "checkpoint.json")
        tid = str(d["task_id"])
        text = cp.get("completion", {}).get("completion", {}).get("source_text", "")
        grades = Counter(re.findall(r"(?m)^(Correct|Incorrect)\b", text))
        records[(account, tid)] = {"account": account, "task_id": tid, "kind": d["kind"],
            "course_id": str(d.get("course_id")), "course_basis": "explicit activity enrollment",
            "title": d.get("title"), "topic_id": d.get("topic_id"),
            "complete": bool(cp.get("completed_at")), "started_at": cp.get("started_at"),
            "completed_at": cp.get("completed_at"), "completion_time_basis": "live checkpoint",
            "grades": dict(grades) if d["kind"] == "diagnostic" else None,
            "retake": "retake" in d.get("title", "").lower(), "source": relative(p),
            "xp": ledger.get((account, tid))}

    # New queue HTML is original evidence. mtime is not claimed as offer time.
    for p in (MA / f"capture/{account}/queue").glob("queue-*.html"):
        s = p.read_text()
        m = re.search(r'<a[^>]*id="courseNameLink"[^>]*href="/courses/(\d+)[^"]*"[^>]*>(.*?)</a>', s, re.S)
        if not m:
            continue  # individual card files have no enrolled-course context
        cid, name = m.groups()
        NAMES[cid] = html.unescape(re.sub(r"<[^>]+>", "", name)).strip()
        # Only unlocked cards, excluding completed task history.
        pattern = r'<div\b[^>]*class="taskUnlocked"[^>]*id="task-(\d+)"[^>]*>|<div\b[^>]*id="task-(\d+)"[^>]*class="taskUnlocked"[^>]*>'
        starts = list(re.finditer(pattern, s))
        cards = []
        for n, match in enumerate(starts):
            card = s[match.start():starts[n+1].start() if n+1 < len(starts) else s.find('id="completedTasks"', match.start()) if 'id="completedTasks"' in s[match.start():] else len(s)]
            if not re.search(r'taskTypeUnlocked[^>]*>\s*Assessment', card):
                continue
            title = re.search(r'taskNameUnlocked[^>]*>(.*?)</div>', card, re.S)
            cards.append({"task_id": match.group(1) or match.group(2),
                          "title": html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else None})
        queues.append({"account": account, "course_id": cid, "course_basis": "original Learn HTML",
                       "time": None, "assessments": cards, "source": relative(p)})

# Standalone original captures outside runner roots.
p = MA / "diagnostic-capture/14033238/state.json"
d = read(p)
records[("multivariable", "14033238")] = {"account": "multivariable", "task_id": "14033238", "kind": "diagnostic",
    "course_id": "54", "course_basis": "explicit diagnostic", "complete": d.get("status") == "completed",
    "grades": d.get("summary"), "completed_at": None, "source": relative(p),
    "completion_time_basis": "no authoritative saved timestamp", "title": "Multivariable Calculus: Placement Exam"}
p = MA / "assessment-13930620/content.json"
d = read(p)
records[("foundations", "13930620")] = {"account": "foundations", "task_id": "13930620", "kind": "assessment",
    "course_id": "111", "course_basis": "historical MF II enrollment episode", "complete": True,
    "title": "Quiz 5", "retake": False, "completed_at": None, "source": relative(p)}

historical = list(csv.DictReader((ROOT / "reference/progress.csv").open()))
course_summary = {}
for cid, name in NAMES.items():
    rs = [r for r in records.values() if r["course_id"] == cid]
    qs = [q for q in queues if q["course_id"] == cid]
    completed = [r for r in rs if r["kind"] == "assessment" and r["complete"]]
    prior = [r for r in historical if r["course"] == name and r["activity-type"] == "Assessment"]
    offered = {str(c["task_id"]): c for q in qs for c in q["assessments"]}
    all_quizzes = {r["task_id"]: {"title": r.get("title"), "retake": r.get("retake")} for r in completed}
    for r in prior:
        all_quizzes.setdefault(r["task-id"], {"title": r["topic-name"], "retake": "retake" in r["topic-name"].lower()})
    course_summary[cid] = {"name": name, "accounts": sorted({r["account"] for r in rs}),
        "captured_activity_kinds": dict(Counter(r["kind"] for r in rs)),
        "completed_original_quizzes": sum(not q.get("retake") for q in all_quizzes.values()),
        "completed_retakes": sum(bool(q.get("retake")) for q in all_quizzes.values()),
        "completed_quiz_titles": sorted({q.get("title") or "unknown" for q in all_quizzes.values()}),
        "unique_offered_assessment_tasks": len(offered), "queue_observations": len(qs),
        "offered_not_captured": [c for tid, c in offered.items() if (next((r for r in rs if r['task_id'] == tid and r['complete']), None)) is None]}

diags = [r for r in records.values() if r["kind"] == "diagnostic"]
for d in diags:
    end = d.get("completed_at")
    # Account/course episode closes at the next different diagnostic on that account.
    subsequent = [r.get("started_at") or r.get("completed_at") for r in diags
                  if r["account"] == d["account"] and r["course_id"] != d["course_id"] and
                  (r.get("started_at") or r.get("completed_at") or 0) > (end or 0)]
    limit = min(subsequent) if subsequent else float("inf")
    offers = [v for v in first_seen.values() if v["account"] == d["account"] and v["course_id"] == d["course_id"]
              and end and end <= v["time"] < limit and "retake" not in (v.get("title") or "").lower()]
    d["first_old_queue_offer_after_diagnostic"] = min(offers, key=lambda v: v["time"]) if offers else None
    d["hours_to_first_old_queue_offer"] = (d["first_old_queue_offer_after_diagnostic"]["time"] - end) / 3600 if offers else None

# Native versus prerequisite topic membership comes from retained course graphs,
# not from account names or arbitrary progress-snapshot scopes.
graphs = {}
graph_root = Path("/home/jake/Developer/MA/COURSES/Math-Academy/University")
for p in graph_root.glob("*/GRAPH-*/Topics.csv"):
    with p.open() as handle:
        graphs[p.parent.parent.name] = {row["topic-id"] for row in csv.DictReader(handle)}
graph_names = {"55": "Linear-Algebra", "54": "Multivariable-Calculus", "61": "Differential-Equations",
               "76": "Methods-of-Proof", "154": "Mathematical-Methods-for-the-Physical-Sciences-I",
               "155": "Mathematical-Methods-for-the-Physical-Sciences-II", "145": "Mathematics-for-Machine-Learning"}
metrics = []
for cid, graph_name in graph_names.items():
    native = graphs.get(graph_name)
    if native is None:
        continue
    for account in ACCOUNTS:
        cr = [r for r in records.values() if r["account"] == account and r["course_id"] == cid
              and r.get("complete") and r["kind"] in ["lesson", "review", "multistep"]]
        if not cr:
            continue
        offers = [v for v in first_seen.values() if v["account"] == account and v["course_id"] == cid]
        first = min(offers, key=lambda v: v["time"]) if offers else None
        pre = [r for r in cr if r.get("completed_at") and r["completed_at"] < first["time"]] if first else []
        def xp_counts(rows):
            return {"activities": len(rows), "missing_xp_records": sum(not r.get("xp") for r in rows),
                    "earned_xp": sum(r["xp"]["earned"] or 0 for r in rows if r.get("xp")),
                    "native_earned_xp": sum(r["xp"]["earned"] or 0 for r in rows
                                            if r.get("xp") and str(r.get("topic_id")) in native)}
        metrics.append({"account": account, "course_id": cid, "course": NAMES[cid],
                        "membership_source": str(graph_root / graph_name / ("GRAPH-" + graph_name) / "Topics.csv"),
                        "completed_learning": xp_counts(cr), "before_first_old_queue_quiz": xp_counts(pre) if first else None,
                        "first_old_queue_quiz": first,
                        "last_learning_completed_at": max(r.get("completed_at") or 0 for r in cr)})

payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "records": list(records.values()),
           "course_summary": course_summary, "diagnostics": diags, "first_old_queue_offers": list(first_seen.values()),
           "xp_topic_membership_metrics": metrics,
           "queues": queues, "historical_csv_assessments": [r for r in historical if r["activity-type"] == "Assessment"],
           "limitations": ["Completed captures and offered queue tasks are separate measures.",
                           "Old non-diagnostic course association uses inferred enrollment episodes, not progress scope IDs.",
                           "New hashed queue HTML has no authoritative observation timestamp; mtime is not used.",
                           "Late-recovered post-activity snapshots can delay old completion timestamps.",
                           "XP ledgers are observed rewards, not proof of the service's quiz eligibility counter."]}
(OUT / "evidence.json").write_text(json.dumps(payload, indent=2) + "\n")
print("Canonical records:", len(records), "queue observations:", len(queues))
for cid, c in course_summary.items():
    print(cid, c["name"], c["captured_activity_kinds"], "quizzes", c["completed_original_quizzes"],
          "retakes", c["completed_retakes"], "offered", c["unique_offered_assessment_tasks"], "uncaptured", c["offered_not_captured"])
for d in diags:
    print("DIAGNOSTIC", d["account"], d["task_id"], NAMES[d["course_id"]], local(d.get("completed_at")),
          d.get("grades"), "hours to offer", d["hours_to_first_old_queue_offer"])
