#!/usr/bin/env python3
"""Fit difficulty-weighted monotone bands using all retained observations.

Compare equal/opposite awards with equal/opposite endpoint bonus/penalty, before
optional penalty caps. No holdout. The CSV's independent awards calibrate perfect
ceilings; rows without question outcomes never receive fabricated accuracy.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path

import numpy as np

from estimator import estimate_earned_xp_with_sequence, rounded

HERE = Path(__file__).resolve().parent
LABELS = {"easy": "E", "moderate": "M", "hard": "H", "E": "E", "M": "M", "H": "H"}
GRID = 100


def bonus(kind, base):
    return 2 if kind == "review" else rounded(base * (Fraction(1,5) if kind == "assessment" else Fraction(1,4)))


def weighted_margin(row, weights):
    mass = sum(weights[LABELS[q["difficulty"]]] for q in row["questions"])
    correct = sum(weights[LABELS[q["difficulty"]]] for q in row["questions"] if q["correct"])
    return Fraction(2*correct-mass, mass)


def grid_predictions(row, signed_margin, family, cap, terminal_override):
    limit = 175 if family == "free_accuracy_bands" else GRID
    levels = np.arange(limit+1, dtype=np.int64)
    base = row["base"]
    extra = bonus(row["type"],base)
    sign = 1 if signed_margin > 0 else -1 if signed_margin < 0 else 0
    if family == "free_accuracy_bands":
        scaled=base*(levels-25)
        prediction=np.sign(scaled)*((2*np.abs(scaled)+100)//200)
        prediction=np.minimum(prediction,base+extra)
    elif family == "equal_opposite_awards":
        prediction = sign * ((2*(base+extra)*levels+GRID)//(2*GRID))
    else:
        # Raw endpoints: B+bonus and -bonus, centered at B/2. Mirrored
        # rounding preserves pair sum B, except the unavoidable odd-B midpoint.
        positive = (2*(GRID*base+(base+2*extra)*levels)+2*GRID)//(4*GRID)
        prediction = positive if sign > 0 else base-positive if sign < 0 else np.full(limit+1,base//2)
    if cap is not None:
        prediction = np.maximum(prediction,-cap)
    n=len(row["questions"]);c=sum(q["correct"] for q in row["questions"])
    if terminal_override and row["type"] == "review" and 2*c>=n and 3*c<2*n and not row["questions"][-1]["correct"]:
        prediction = np.zeros(limit+1,dtype=np.int64)
    return prediction


def fit_type(rows, weights, family, cap, terminal_override):
    limit = 175 if family == "free_accuracy_bands" else GRID
    groups=defaultdict(list)
    for row in rows:
        margin=weighted_margin(row,weights)
        key=(margin+1)/2 if family == "free_accuracy_bands" else abs(margin)
        groups[key].append((row,margin))
    # Force the endpoints even when this particular sample lacks them.
    groups[Fraction(0)];groups[Fraction(1)]
    ordered=sorted(groups)
    parents=[];last_scores=None
    for index, magnitude in enumerate(ordered):
        group=groups[magnitude]
        errors=np.array([grid_predictions(row,margin,family,cap,terminal_override)-row["earned"] for row,margin in group])
        mae=np.abs(errors).sum(axis=0) if len(group) else np.zeros(limit+1,dtype=np.int64)
        squared=(errors*errors).sum(axis=0) if len(group) else np.zeros(limit+1,dtype=np.int64)
        states=[None]*(limit+1);back=[None]*(limit+1)
        prefix=None;prefix_j=None
        for level in range(limit+1):
            if index:
                previous=last_scores[level]
                if previous is not None:
                    changed=(previous[0],previous[1],previous[2]+1)
                    if prefix is None or changed<prefix:
                        prefix,prefix_j=changed,level
                choices=[]
                if prefix is not None:choices.append((prefix,prefix_j))
                if previous is not None:choices.append((previous,level))
                if not choices:continue
                selected,j=min(choices,key=lambda x:(x[0],x[1]))
                states[level]=(selected[0]+int(mae[level]),selected[1]+int(squared[level]),selected[2])
                back[level]=j
            else:
                states[level]=(int(mae[level]),int(squared[level]),1)
            if magnitude==0 and level!=0 or magnitude==1 and level!=limit:
                states[level]=None;back[level]=None
        parents.append(back);last_scores=states
    score,level=min((s,j) for j,s in enumerate(last_scores) if s is not None)
    chosen=[]
    for i in range(len(ordered)-1,-1,-1):
        chosen.append(level)
        level=parents[i][level] if i else None
    chosen.reverse()
    predictions=[];bands=[]
    for magnitude,level in zip(ordered,chosen):
        percentage=level-25 if family=="free_accuracy_bands" else 100*level/GRID
        if not bands or bands[-1]["strength_percent"]!=percentage:
            bands.append({"minimum_weighted_accuracy" if family=="free_accuracy_bands" else "minimum_absolute_margin":str(magnitude),"strength_percent":percentage})
        for row,margin in groups[magnitude]:
            pred=int(grid_predictions(row,margin,family,cap,terminal_override)[level])
            predictions.append({"task_id":row["task_id"],"type":row["type"],"base":row["base"],"earned":row["earned"],
                                "weighted_accuracy":float((margin+1)/2),"signed_margin":str(margin),"predicted":pred,"error":pred-row["earned"]})
    return {"objective":score,"weights":{k:str(v) for k,v in weights.items()},"bands":bands,"predictions":predictions}


def summarize(predictions):
    errors=[abs(p["error"]) for p in predictions]
    return {"tasks":len(errors),"exact":sum(e==0 for e in errors),"mean_absolute_error":sum(errors)/len(errors),
            "maximum_absolute_error":max(errors),"total_absolute_error":sum(errors)}


def main():
    global GRID
    observations=json.loads((HERE/"observations.json").read_text())
    rows=observations["rows"]
    progress=observations["progress_rows"]
    known={str(r["task_id"]):r for r in rows}
    csv_summary={}
    for kind in ("lesson","review","assessment","multistep"):
        selected=[r for r in progress if r["activity-type"].lower()==kind]
        above=[r for r in selected if int(r["xp-earned"])>int(r["xp-possible"])]
        csv_summary[kind]={"rows":len(selected),"above_base_awards":len(above),
                           "above_base_at_proposed_ceiling":sum(int(r["xp-earned"])==int(r["xp-possible"])+bonus(kind,int(r["xp-possible"])) for r in above)}
    candidates=[]
    weight_pairs=sorted({(Fraction(m),Fraction(h)) for m in (1,1.25,1.5,1.75,2,2.5,3,4)
                        for h in (1,1.25,1.5,1.75,2,2.5,3,4,5,6,8) if h>=m})
    for family in ("equal_opposite_awards","mirrored_bonus_endpoints","free_accuracy_bands"):
        for cap in (None,1):
            print('Fitting',family,'cap',cap,flush=True)
            fits_by_type={}
            fixed_by_type={}
            equal_by_type={}
            for kind in ("lesson","review","assessment","multistep"):
                selected=[r for r in rows if r["type"]==kind]
                fits=[]
                for medium,hard in weight_pairs:
                    weights={"E":Fraction(1),"M":medium,"H":hard}
                    fit=fit_type(selected,weights,family,cap,True)
                    fits.append(fit)
                    if (medium,hard)==(2,4):fixed_by_type[kind]=fit
                    if (medium,hard)==(1,1):equal_by_type[kind]=fit
                fits_by_type[kind]=min(fits,key=lambda f:(tuple(f["objective"]),sum(float(Fraction(v)) for v in f["weights"].values())))
            for mode,fits in (("fitted_difficulty",fits_by_type),("fixed_1_2_4",fixed_by_type),("equal_weights",equal_by_type)):
                predictions=[p for fit in fits.values() for p in fit["predictions"]]
                candidates.append({"family":family,"penalty_cap":cap,"weights_mode":mode,"review_terminal_override":True,
                                   "metrics":summarize(predictions),"types":fits,"mismatches":[p for p in predictions if p["error"]]})
    # Refine the best mirrored candidate's rounding intervals at 0.1% strength.
    # This tests grid resolution without another weight search or a data split.
    mirrored=min((c for c in candidates if c["family"]=="mirrored_bonus_endpoints"),key=lambda c:c["metrics"]["total_absolute_error"])
    GRID=1000
    refined={}
    for kind,fit in mirrored["types"].items():
        refined[kind]=fit_type([r for r in rows if r["type"]==kind],{k:Fraction(v) for k,v in fit["weights"].items()},mirrored["family"],mirrored["penalty_cap"],True)
    predictions=[p for fit in refined.values() for p in fit["predictions"]]
    candidates.append({"family":mirrored["family"],"penalty_cap":mirrored["penalty_cap"],"weights_mode":"fitted_difficulty_refined_strength","review_terminal_override":True,
                       "metrics":summarize(predictions),"types":refined,"mismatches":[p for p in predictions if p["error"]]})
    GRID=100
    earlier=[]
    for row in rows:
        pred=estimate_earned_xp_with_sequence(row["type"],row["base"],[q["correct"] for q in row["questions"]])
        earlier.append({"task_id":row["task_id"],"type":row["type"],"earned":row["earned"],"predicted":pred,"error":pred-row["earned"]})
    candidates.sort(key=lambda c:(c["metrics"]["total_absolute_error"],sum(p["error"]**2 for f in c["types"].values() for p in f["predictions"]),sum(len(f["bands"]) for f in c["types"].values())))
    results={"observation_timestamp":observations["extracted_at"],"progress":observations["progress_source"],
             "csv_activity_counts":dict(Counter(r["activity-type"] for r in progress)),
             "csv_bonus_evidence":csv_summary,"outcome_activity_counts":dict(Counter(r["type"] for r in rows)),
             "outcome_tasks":len(rows),"outcome_questions":sum(len(r["questions"]) for r in rows),
             "csv_rows_without_outcomes":[r for r in progress if r["task-id"] not in known],
             "method":"All retained data; monotone 1%-strength bands plus 0.1% refinement of the best mirror; endpoint symmetry and free accuracy families; no holdout. Missing CSV accuracies remain missing.",
             "weight_pairs_tried":len(weight_pairs),"earlier_formula":summarize(earlier),"candidates":candidates}
    (HERE/"band-results.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"tasks":len(rows),"progress":results["progress"],"earlier_formula":results["earlier_formula"],
                      "candidates":[{k:c[k] for k in ("family","penalty_cap","weights_mode","metrics")} for c in candidates],
                      "best_weights":{k:f["weights"] for k,f in candidates[0]["types"].items()}},indent=2))


if __name__=="__main__":
    main()
