"""Compare simple policies against the saved candidate evidence, without rereads.

Odds ratios are descriptive; repeated observations are not independent samples.
Replay conditions on the number of selected topics inside the observable pool.
"""
import hashlib
import heapq
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
raw = (OUT / "evidence.json").read_bytes()
data = json.loads(raw)
quizzes = [q for q in data["quizzes"] if not q["retake"] and q["candidates"] and q["page_gap_seconds"] is not None]


def mh(qs, feature, keys=(), restrict=lambda r: True):
    num = den = 0
    strata = 0
    for q in qs:
        groups = defaultdict(list)
        for r in q["candidates"]:
            if restrict(r):
                age = "48–60h" if r["age_hours"]<60 else "60–72h" if r["age_hours"]<72 else "72h+"
                attrs = {"native": r["native"], "age": age, "band": r["band"],
                         "tested": r["previously_tested"], "covered": r["preoffer_local_graph"]["weight"]>=.5}
                groups[tuple(attrs[k] for k in keys)].append(r)
        for rs in groups.values():
            a = sum(r["selected"] and feature(r) for r in rs)
            b = sum(not r["selected"] and feature(r) for r in rs)
            c = sum(r["selected"] and not feature(r) for r in rs)
            d = sum(not r["selected"] and not feature(r) for r in rs)
            if (a+b)*(c+d)*(a+c)*(b+d) == 0:
                continue
            num += a*d/len(rs)
            den += b*c/len(rs)
            strata += 1
    return {"informative_strata": strata, "odds_ratio": num/den if den else None}


checks = {}
for name, feature, keys, restriction in [
    ("prior_test_native", lambda r:r["previously_tested"], ("native",), lambda r:True),
    ("prior_test_native_age", lambda r:r["previously_tested"], ("native","age"), lambda r:True),
    ("prior_test_native_age_coverage", lambda r:r["previously_tested"], ("native","age","covered"), lambda r:True),
    ("prior_test_native_band", lambda r:r["previously_tested"], ("native","band"), lambda r:True),
    ("coverage_native_untested", lambda r:r["preoffer_local_graph"]["weight"]>=.5, ("native",), lambda r:not r["previously_tested"]),
    ("coverage_native_age_untested", lambda r:r["preoffer_local_graph"]["weight"]>=.5, ("native","age"), lambda r:not r["previously_tested"]),
    ("coverage_native_band_untested", lambda r:r["preoffer_local_graph"]["weight"]>=.5, ("native","band"), lambda r:not r["previously_tested"]),
    ("dark_band_native_age_history", lambda r:r["band"]>=3, ("native","age","tested"), lambda r:True),
    ("recent_direct_review_native_age_history", lambda r:r["last_review_age_hours"] is not None and r["last_review_age_hours"]<24, ("native","age","tested"), lambda r:True),
]:
    checks[name] = {"all": mh(quizzes,feature,keys,restriction)}
    for account in ["foundations","linear","multivariable","differential"]:
        checks[name][account] = mh([q for q in quizzes if q["account"]==account],feature,keys,restriction)

replays = []
models = [("linear", h, c) for h in [.5,.25,.1] for c in [.75,.9,.95]]
models += [("squared_floor_0.1", .25, None), ("half_or_more_0.1", .25, None)]
for model, history_weight, coverage_strength in models:
        totals = defaultdict(Counter)
        expected = defaultdict(Counter)
        rng = random.Random(10122026)
        for q in quizzes:
            rs = q["candidates"]
            n = sum(r["selected"] for r in rs)
            if not n:
                continue
            for r in rs:
                if r["selected"]:
                    totals[q["account"]]["repeat"] += r["previously_tested"]
                    totals[q["account"]]["covered"] += r["preoffer_local_graph"]["weight"] >= .5
                    totals[q["account"]]["native"] += r["native"]
            # Course factor only controls a known difference in MA's policy.
            # Our proposed application policy would omit it.
            def coverage_factor(r):
                c = r["preoffer_local_graph"]["weight"]
                if model == "squared_floor_0.1":
                    return max(.1,(1-c)**2)
                if model == "half_or_more_0.1":
                    return .1 if c>=.5 else 1
                return 1-coverage_strength*c
            weights = [(history_weight if r["previously_tested"] else 1)*coverage_factor(r)*(4 if r["native"] else 1) for r in rs]
            for _ in range(1000):
                selected = heapq.nsmallest(n,range(len(rs)),key=lambda i:-math.log(max(rng.random(),1e-15))/weights[i])
                for i in selected:
                    expected[q["account"]]["repeat"] += rs[i]["previously_tested"]/1000
                    expected[q["account"]]["covered"] += (rs[i]["preoffer_local_graph"]["weight"]>=.5)/1000
                    expected[q["account"]]["native"] += rs[i]["native"]/1000
        replays.append({"model":model,"history_weight":history_weight,"coverage_strength":coverage_strength,"native_course_weight":4,
                        "observed_by_account":dict(totals),"expected_by_account":dict(expected),
                        "observed_total":{k:sum(v[k] for v in totals.values()) for k in ["repeat","covered","native"]},
                        "expected_total":{k:sum(v[k] for v in expected.values()) for k in ["repeat","covered","native"]}})

result={"evidence_sha256":hashlib.sha256(raw).hexdigest(),"conditional_odds":checks,"replays":replays}
(OUT / "sensitivity.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v["all"] for k,v in checks.items()},indent=2))
for r in replays:
    print(r["model"],r["history_weight"],r["coverage_strength"],r["observed_total"],r["expected_total"])
