"""All-observation base-XP calibration with difficulty and selection weights.

Every coefficient and multiplier is fitted to all captured lessons. There is no
held-out set, cross-validation, or accuracy claim about unseen content.
"""
import copy
import hashlib
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from analyze import HERE, ROOT, MODELS, design, fit, metrics, predict

BANDS = ("easy", "moderate", "hard")


def policy_distributions():
    # The small EDN reader intentionally does not support source comments.
    sys.path.insert(0, str(ROOT / "scripts/question_capture"))
    from edn import loads
    source = ROOT / "schema/engine/3-default-fire-policy.edn"
    raw = source.read_text()
    policy = loads("\n".join(line for line in raw.splitlines() if not line.lstrip().startswith(";")))[0]
    records = policy[":policy/question-selection-weights"]
    distributions = {}
    for row in records:
        kind = str(row[":question-weights/activity-type"]).split("/")[-1]
        distributions[kind] = {}
        for phase in ("initial", "remedial"):
            values = [row[f":question-weights/{phase}-{band}"] for band in BANDS]
            distributions[kind][phase] = dict(zip(BANDS, (v / sum(values) for v in values)))
    return {"source": str(source.relative_to(ROOT)), "sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "distributions": distributions}


def augment(rows, policy):
    missing, kp_count, unsupported_remedial = Counter(), 0, []
    for row in rows:
        grouped = defaultdict(list)
        for q in row["question_samples"]:
            grouped[q["kp"]].append(q)
        f = row["features"]
        for phase in ("initial", "remedial"):
            for band in BANDS:
                f[f"policy_{phase}_{band}_math_100"] = 0.0
        for qs in grouped.values():
            kp_count += 1
            by_band = {band: [q for q in qs if q["difficulty"] == band] for band in BANDS}
            for band in BANDS:
                if not by_band[band]:
                    missing[band] += 1
            for phase, probabilities in policy["distributions"]["lesson"].items():
                total = sum(probabilities[band] for band in BANDS if by_band[band])
                if not total:
                    # A sampled KP can contain only Hard questions, whose
                    # remedial weight is zero. Its remedial time is unobserved.
                    # Borrow its initial estimate for this exploratory feature;
                    # do not claim that the sampler would select a Hard remedy.
                    unsupported_remedial.append({"task_id": row["task_id"], "kp": qs[0]["kp"]})
                    band = next(b for b in BANDS if by_band[b])
                    f[f"policy_{phase}_{band}_math_100"] += sum(q["solution_math_tokens"] for q in qs)/len(qs)/100
                    continue
                for band in BANDS:
                    if by_band[band]:
                        mean = sum(q["solution_math_tokens"] for q in by_band[band]) / len(by_band[band])
                        f[f"policy_{phase}_{band}_math_100"] += probabilities[band] / total * mean / 100
        for phase in ("initial", "remedial"):
            f[f"policy_{phase}_math_100"] = sum(f[f"policy_{phase}_{band}_math_100"] for band in BANDS)
        # Three reference questions are an exploratory assumption, not observed
        # ordinary learner duration: two initial plus one expected remedial.
        f["policy_blend_math_100"] = (2*f["policy_initial_math_100"] + f["policy_remedial_math_100"])/3
        for label, multipliers in (("gentle", (1, 1.5, 2)), ("double_triple", (1, 2, 3))):
            f[f"multiplier_{label}_math_100"] = sum(
                sum(q["solution_math_tokens"] * multipliers[BANDS.index(q["difficulty"])] for q in qs)/len(qs)
                for qs in grouped.values()) / 100
        for band in BANDS:
            f[f"observed_{band}_math_100"] = sum(
                sum(q["solution_math_tokens"] for q in qs if q["difficulty"] == band)/len(qs)
                for qs in grouped.values()) / 100
        f["observed_moderate_hard_math_100"] = f["observed_moderate_math_100"]+f["observed_hard_math_100"]
        f["multiplier_1_2_4_math_100"] = f["observed_easy_math_100"]+2*f["observed_moderate_math_100"]+4*f["observed_hard_math_100"]
    return {"kp_count": kp_count, "kps_without_observed_band": dict(missing),
            "remedial_time_unobserved_borrowed_initial": unsupported_remedial,
            "missing_band_handling": "Renormalize selection weights across bands present in the captured pool, matching local sampler behavior for that pool. Missing from five captured questions does not prove absence from MA's full bank."}


def score(y, predictions):
    errors = predictions - y
    return (int(np.sum(abs(errors))), int(np.sum(errors**2)), -int(np.sum(errors == 0)))


def rounded(x, coefficients):
    return np.maximum(7, np.floor(x @ coefficients + 0.5)).astype(int)


def refine(rows, names, initial):
    """Minimize actual integer-XP absolute error, including the seven-XP floor.

    Each coordinate considers every interval that can change an integer output
    up to the largest observed base. Several starts reduce plateau sensitivity.
    This is a small deterministic search, not a guarantee of a global optimum.
    """
    x = design(rows, names)
    y = np.array([r["base_xp"] for r in rows])
    thresholds = np.arange(7.5, max(y)+1.6, 1.0)
    best, best_score = initial.copy(), score(y, rounded(x, initial))
    for start in (initial, initial*0.8, initial*1.2):
        coefficients = start.copy()
        current_score = score(y, rounded(x, coefficients))
        for _ in range(8):
            improved = False
            for j in range(x.shape[1]):
                positive = x[:, j] > 0
                if not np.any(positive):
                    continue
                rest = x @ coefficients - x[:, j]*coefficients[j]
                boundaries = ((thresholds[:, None]-rest[positive])/x[positive, j]).ravel()
                boundaries = np.unique(np.r_[0, boundaries[boundaries > 0]])
                candidates = np.unique(np.r_[0, coefficients[j], (boundaries[:-1]+boundaries[1:])/2,
                                                boundaries[-1]+1e-7])
                predictions = np.maximum(7, np.floor(rest[:, None]+x[:, j, None]*candidates+0.5)).astype(int)
                error = predictions-y[:, None]
                absolute, square, exact = np.sum(abs(error), axis=0), np.sum(error**2, axis=0), np.sum(error==0, axis=0)
                index = np.lexsort((-exact, square, absolute))[0]
                candidate_score = (int(absolute[index]), int(square[index]), -int(exact[index]))
                if candidate_score < current_score:
                    coefficients[j], current_score = candidates[index], candidate_score
                    improved = True
            if not improved:
                break
        if current_score < best_score:
            best, best_score = coefficients, current_score
    return best


def fit_model(rows, names):
    initial = fit(rows, names)
    coefficients = refine(rows, names, initial)
    predictions = predict(rows, names, coefficients)
    return {"features": names, "coefficients": dict(zip(["intercept", *names], map(float, coefficients))),
            "metrics": metrics(rows, predictions), "predictions": list(map(int, predictions)),
            "least_squares_start_metrics": metrics(rows, predict(rows, names, initial))}


def fit_all(data):
    started = time.perf_counter()
    rows = copy.deepcopy(sorted([r for r in data["activities"] if r["type"] == "lesson"], key=lambda r: r["task_id"]))
    policy = policy_distributions()
    coverage = augment(rows, policy)
    candidates = {name: fit_model(rows, names) for name, names in MODELS.items()}
    extensions = {
        "baseline_plus_difficulty": ["kp", "solution_math_100", "reading_100", "moderate_kp", "hard_kp"],
        "duration_multipliers_1_1.5_2": ["kp", "multiplier_gentle_math_100", "reading_100"],
        "duration_multipliers_1_2_3": ["kp", "multiplier_double_triple_math_100", "reading_100"],
        "policy_initial": ["kp", "policy_initial_math_100", "reading_100"],
        "policy_remedial": ["kp", "policy_remedial_math_100", "reading_100"],
        "policy_blend": ["kp", "policy_blend_math_100", "reading_100"],
        "policy_initial_and_remedial": ["kp", "policy_initial_math_100", "policy_remedial_math_100", "reading_100"],
        "policy_band_duration_coefficients": ["kp", "policy_initial_easy_math_100", "policy_initial_moderate_math_100", "policy_initial_hard_math_100", "reading_100"],
        "learned_monotone_duration_multipliers": ["kp", "solution_math_100", "observed_moderate_hard_math_100", "observed_hard_math_100", "reading_100"],
        "duration_1_2_4_extra_fields": ["kp", "multiplier_1_2_4_math_100", "reading_100", "extra_fields"],
        "duration_1_2_4_tutorials": ["kp", "multiplier_1_2_4_math_100", "reading_100", "tutorials"],
        "duration_1_2_4_full_content": ["kp", "multiplier_1_2_4_math_100", "reading_100", "tutorials", "question_steps", "example_steps", "question_math_100", "extra_fields", "blank_kp", "moderate_kp", "hard_kp"],
    }
    for name, names in extensions.items():
        candidates[name] = fit_model(rows, names)
    # Search duration multipliers with Easy fixed at one and Hard >= Moderate.
    # Selection probabilities remain distinct from these duration multipliers.
    grid = []
    for moderate in np.arange(1, 4.01, .5):
        for hard in np.arange(moderate, 5.01, .5):
            for row in rows:
                grouped = defaultdict(list)
                for q in row["question_samples"]:
                    grouped[q["kp"]].append(q)
                multipliers = dict(zip(BANDS, (1, moderate, hard)))
                row["features"]["grid_multiplier_math_100"] = sum(
                    sum(q["solution_math_tokens"]*multipliers[q["difficulty"]] for q in qs)/len(qs)
                    for qs in grouped.values())/100
            names = ["kp", "grid_multiplier_math_100", "reading_100"]
            model = fit_model(rows, names)
            grid.append({"multipliers": {"easy": 1, "moderate": float(moderate), "hard": float(hard)}, **model})
    chosen_grid = min(grid, key=lambda m: (m["metrics"]["mae"], m["metrics"]["rmse"], -m["metrics"]["exact_fraction"]))
    candidates["fitted_duration_multipliers"] = chosen_grid
    # The loop leaves the last grid's feature values in rows; restore the
    # selected grid so the saved measurements reproduce its predictions.
    for row in rows:
        f = row["features"]
        f["grid_multiplier_math_100"] = sum(chosen_grid["multipliers"][band]*f[f"observed_{band}_math_100"] for band in BANDS)
    selected = min(candidates, key=lambda name: (candidates[name]["metrics"]["mae"], candidates[name]["metrics"]["rmse"],
                                                len(candidates[name]["features"]), name))
    chosen = candidates[selected]
    original = candidates["kp_solution_math_reading"]
    predictions = [{"task_id": r["task_id"], "topic_id": r["topic_id"], "title": r["title"], "base_xp": r["base_xp"],
                    "predicted": p, "error": p-r["base_xp"], "features": r["features"]}
                   for r, p in zip(rows, chosen["predictions"])]
    return {"method": "Fit every candidate, coefficient and multiplier to all observations; no held-out set or cross-validation. Compare rounded base-XP mean absolute error, then squared error. Integer/floor-aware coordinate refinement after nonnegative least squares.",
            "target": "Displayed BASE XP denominator only; no earned XP, bonuses, penalties, correctness or bot/human elapsed times used as targets or model features.",
            "observations_extracted_at": data["extracted_at"], "lesson_n": len(rows), "policy": policy,
            "coverage": coverage, "candidates": candidates, "multiplier_grid": grid,
            "selected_model": selected, "selected_coefficients": chosen["coefficients"], "fit_metrics": chosen["metrics"],
            "original_family_refined_fit_metrics": original["metrics"], "predictions": predictions,
            "analysis_wall_seconds": time.perf_counter()-started}


def plot(report):
    import os
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/course-academy-base-xp-matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = report["predictions"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    axes[0].scatter([r["features"]["kp"] for r in rows], [r["base_xp"] for r in rows], alpha=.6)
    axes[0].set(xlabel="Knowledge points", ylabel="Observed base XP", title="Same KP count, different workload", xticks=[2, 3, 4, 5])
    axes[1].scatter([r["base_xp"] for r in rows], [r["predicted"] for r in rows], alpha=.7)
    axes[1].plot([5, 26], [5, 26], color="grey", linestyle="--", linewidth=1)
    axes[1].set(xlabel="Observed base XP", ylabel="Fitted base XP", title=f"Fit to all {len(rows)} captured lessons", xlim=(5, 26), ylim=(5, 26))
    fig.savefig(HERE / "full-fit.png", dpi=160)
    plt.close(fig)


def main():
    data = json.loads((HERE/"observations.json").read_text())
    report = fit_all(data)
    (HERE/"full-fit-results.json").write_text(json.dumps(report, indent=2)+"\n")
    plot(report)
    print(json.dumps({k: report[k] for k in ("lesson_n", "selected_model", "selected_coefficients", "fit_metrics", "coverage", "analysis_wall_seconds")}, indent=2))
    for name, model in sorted(report["candidates"].items(), key=lambda item: (item[1]["metrics"]["mae"], item[1]["metrics"]["rmse"])):
        print(name, round(model["metrics"]["mae"], 3), round(model["metrics"]["rmse"], 3), model["coefficients"])


if __name__ == "__main__":
    main()
