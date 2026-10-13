"""Read-only quiz/review comparison and explicitly LOCAL FIRe illustrations.

Run from repo root with PYTHONPATH=capture. Replays are isolated JSON inputs,
never learner/database updates. Local defaults are not recovered MA parameters.
"""
import hashlib
import json
import math
import statistics
import subprocess
from collections import defaultdict
from pathlib import Path

from scripts.analyze_encompassing import observed_outcome
from scripts.database.edn import loads

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
data = json.loads((OUT / "topic-age-evidence.json").read_text())
records = json.loads((OUT / "evidence.json").read_text())["records"]
matched = [r for r in data["rows"] if r["age_hours"] is not None]
first_quiz = {}
for r in sorted(matched, key=lambda r: r["assessment_time"]):
    first_quiz.setdefault((r["account"], r["topic_id"]), r)
reviews = defaultdict(list)
for r in records:
    if r["kind"] != "review" or not r.get("complete") or not r.get("completed_at"):
        continue
    path = ROOT / r["source"]
    state = json.loads(path.read_text())
    completion = state.get("completion")
    if path.name == "activity.json":
        completion = json.loads((path.parent / "content.json").read_text()).get("completion")
    reviews[r["account"], str(r.get("topic_id"))].append({
        **r, "observed_outcome": observed_outcome(state.get("activity_outcome"), completion)})

topic_rows = []
for key, quiz in first_quiz.items():
    lesson = quiz["first_observed_lesson"]
    prior = sorted([r for r in reviews[key] if lesson["age_anchor"] < r["completed_at"] < quiz["assessment_time"]],
                   key=lambda r: r["completed_at"])
    passed = [r for r in prior if r["observed_outcome"] == "passed"]
    def item(r):
        return {"task_id": r["task_id"], "source": r["source"], "outcome": r["observed_outcome"],
                "hours_after_observed_lesson": (r["completed_at"]-lesson["age_anchor"])/3600,
                "hours_before_first_quiz_offer": (quiz["assessment_time"]-r["completed_at"])/3600}
    topic_rows.append({"account": key[0], "topic_id": key[1], "quiz_id": quiz["quiz_id"],
                       "lesson_id": lesson["task_id"], "quiz_topic_age_hours": quiz["age_hours"],
                       "recorded_prior_reviews": [item(r) for r in prior],
                       "first_passed_review": item(passed[0]) if passed else None,
                       "latest_passed_review": item(passed[-1]) if passed else None})
first_recorded = [r["recorded_prior_reviews"][0] for r in topic_rows if r["recorded_prior_reviews"]]
first_passed = [r["first_passed_review"] for r in topic_rows if r["first_passed_review"]]
summary = {"distinct_traceable_account_topics": len(topic_rows),
           "with_recorded_review_before_first_quiz": len(first_recorded),
           "without_recorded_review_before_first_quiz": len(topic_rows)-len(first_recorded),
           "first_recorded_review_under_24h": sum(r["hours_after_observed_lesson"] < 24 for r in first_recorded),
           "first_recorded_review_under_48h": sum(r["hours_after_observed_lesson"] < 48 for r in first_recorded),
           "median_first_recorded_review_hours": statistics.median(r["hours_after_observed_lesson"] for r in first_recorded),
           "with_passed_review_before_first_quiz": len(first_passed),
           "first_passed_review_under_24h": sum(r["hours_after_observed_lesson"] < 24 for r in first_passed),
           "first_passed_review_under_48h": sum(r["hours_after_observed_lesson"] < 48 for r in first_passed)}

policy_path = ROOT / "schema/engine/4-default-fire-policy.edn"
configured = loads(policy_path.read_text())[0]
mapping = {"base-half-life-days": "base_interval_days", "interval-growth": "interval_growth",
           "maximum-half-life-days": "maximum_interval_days", "review-threshold": "due_threshold",
           "initial-retention": "restored_memory", "early-practice-discount-power": "discount_power",
           "initial-accuracy": "prior_accuracy", "accuracy-update-rate": "accuracy_alpha",
           "speed-exponent": "speed_exponent", "minimum-speed": "minimum_speed", "maximum-speed": "maximum_speed",
           "overdue-failure-slope": "failure_overdue_slope", "maximum-failure-multiplier": "maximum_failure_multiplier",
           "gate-slow-implicit": "gate_slow_implicit", "future-horizon-days": "future_horizon_days"}
policy = {local: configured[":policy/"+name] for name,local in mapping.items()}
assert configured[":policy/retention-update-order"] == ":policy.retention-update/decay-before-add"
policy.update(name="local-timing-illustration", memory_order="decay-before-add", speed_exponent=0.0)
binary = ROOT / "target/debug/fire"
scenarios = []
cases = [("no-practice", None, 1), ("direct-at-24h", 1, 1),
         ("direct-at-48h", 2, 1), ("half-implicit-at-48h", 2, .5)]
for name, day, coverage in cases:
    edges = [{"advanced": "advanced", "component": "target", "weight": .5}] if coverage == .5 else []
    events = [{"id": "learn-target", "learner": "illustration", "topic": "target", "at": 0,
               "passed": True, "quality": 1.0, "kind": "lesson", "learned": True}]
    if day is not None:
        events.append({"id": name, "learner": "illustration", "topic": "advanced" if edges else "target",
                       "at": day, "passed": True, "quality": 1.0,
                       "kind": "lesson" if edges else "review", "learned": bool(edges)})
    value = {"policy": policy, "edges": edges, "topics": ["target", "advanced"] if edges else ["target"],
             "events": events, "assumptions": ["LOCAL model, not fitted to Math Academy.",
                        "Speed fixed at one using exponent zero; event quality one; no failed work."]}
    input_path = OUT / ("fire-illustration-"+name+"-input.json")
    input_path.write_text(json.dumps(value,indent=2)+"\n")
    result = subprocess.run([str(binary), "replay", str(input_path)], check=True, capture_output=True, text=True)
    replay = json.loads(result.stdout)
    (OUT / ("fire-illustration-"+name+"-output.json")).write_text(json.dumps(replay,indent=2)+"\n")
    updates = [u for receipt in replay["receipts"] for u in receipt["updates"] if u["topic"] == "target"]
    last = updates[-1]
    assert math.isclose(updates[0]["after"]["interval_days"], 2.0)
    for u in updates:
        assert math.isclose(u["after"]["interval_days"], min(policy["maximum_interval_days"],
                  policy["base_interval_days"]*policy["interval_growth"]**u["after"]["repetitions"]))
    scenarios.append({"name": name, "updates": updates, "last_state": last["after"],
                      "next_review_due_days_after_learning": last["due_at"]})

output = {"review_observation_summary": summary, "first_quiz_topics": topic_rows,
          "local_model_policy": policy, "local_scenarios": scenarios,
          "provenance": {"policy_path": str(policy_path.relative_to(ROOT)),
                         "policy_sha256": hashlib.sha256(policy_path.read_bytes()).hexdigest(),
                         "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
                         "core_source_sha256": hashlib.sha256((ROOT / "engine/rust/core.rs").read_bytes()).hexdigest()},
          "limitations": ["No captured review is not proof of no implicit or uncaptured practice.",
                           "Observation/completion bounds are not internal due times.",
                           "Local simulation parameters and coverage are explicit illustrations, not empirical MA estimates.",
                           "Only derived audit files were written; no database or runner operations."]}
(OUT / "fire-timing-followup.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps(summary,indent=2))
for r in scenarios:
    state = r["last_state"]
    print(r["name"], "repetitions", round(state["repetitions"],6), "memory", round(state["memory"],6),
          "half-life days", round(state["interval_days"],6), "next due day",round(r["next_review_due_days_after_learning"],6))

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Optional plot dependencies unavailable; JSON is complete.")
else:
    fig,axes = plt.subplots(2,1,figsize=(10,7),sharex=True,constrained_layout=True)
    names = ["No further practice", "Direct review at 24 h", "Direct review at 48 h", "50% implicit practice at 48 h"]
    for case,label in zip(scenarios,names):
        anchors = sorted([u["after"] for u in case["updates"]],key=lambda s:s["memory_at"])
        for j,state in enumerate(anchors):
            end = anchors[j+1]["memory_at"] if j+1<len(anchors) else 12
            days = np.linspace(state["memory_at"],end,150)
            curve = state["memory"] * np.power(2,-(days-state["memory_at"])/state["interval_days"])
            # Stable color across each scenario's pre/post-event segments.
            color = ["#61676d", "#cf6e2d", "#3978a8", "#329578"][scenarios.index(case)]
            axes[0].plot(days,curve,color=color,label=label if j==len(anchors)-1 else None)
            axes[1].plot(days,np.full(len(days),state["interval_days"]),color=color)
            if j:
                old = anchors[j-1]
                old_memory = old["memory"]*2**(-(state["memory_at"]-old["memory_at"])/old["interval_days"])
                axes[0].plot([state["memory_at"]]*2,[old_memory,state["memory"]],color=color)
                axes[1].plot([state["memory_at"]]*2,[old["interval_days"],state["interval_days"]],color=color)
    axes[0].axhline(policy["due_threshold"],color="#a34848",linestyle="--",label="Local review threshold")
    for ax in axes:
        ax.axvline(2,color="#999",linestyle=":")
        ax.spines[["top","right"]].set_visible(False)
        ax.set_xlim(0,12)
    axes[0].set_ylabel("Local retention score (not probability)")
    axes[0].legend(ncol=2,fontsize=9,loc="upper right")
    axes[1].set(ylabel="Retention half-life (days)",xlabel="Days after initial learning")
    fig.suptitle("How practice changes retention and review timing\nLOCAL FIRe illustration; not fitted Math Academy parameters",fontsize=14)
    fig.savefig(OUT / "fire-timing-illustration.png",dpi=180)
    plt.close(fig)
