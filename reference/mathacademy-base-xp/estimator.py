"""Constant-cost provisional lesson base XP, calibrated on 58 captured topics.

Features are prepared from content once, not from learner performance or elapsed
time. This is a workload approximation, not Math Academy's production formula.
See README.md for the all-data calibration and the scope of the seven-XP floor.
"""
import math
import re
from collections import defaultdict

DURATION_MULTIPLIERS = {"easy": 1.0, "moderate": 2.0, "hard": 4.0}
FULL_CONTENT_COEFFICIENTS = {
    "multiplier_1_2_4_math_100": 0.7727506490727063,
    "reading_100": 0.07513004637186382,
    "question_steps": 0.001586056170966394,
    "example_steps": 0.034422123109798704,
    "question_math_100": 2.7349018409710975,
    "extra_fields": 0.06047150091696244,
    "blank_kp": 0.5742034148595132,
    "moderate_kp": 0.8708735238642493,
    "hard_kp": 2.041850919949942,
}


def clean_markdown(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    return re.sub(r"\{\{[^}]*\}\}", "", text)


def prose_words(text):
    text = clean_markdown(text)
    text = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", "", text, flags=re.S)
    return len(re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", text))


def math_tokens(text):
    """Count commands, numbers, letters and operators inside Markdown formulas."""
    text = clean_markdown(text)
    parts = re.findall(r"\$\$(.*?)\$\$|\$([^$]*)\$", text, flags=re.S)
    return sum(len(re.findall(r"\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[+*/=^_−-]", a or b))
               for a, b in parts)


def estimate_lesson_base(kp_count, solution_math_tokens, reading_words=0):
    """Q = sum of per-KP mean worked-question solution token counts, not pool total.

    R = tutorial and canonical-example prose words. Return expected-work XP;
    earned XP, accuracy bonuses, and individual pace are separate calculations.
    This preserves the original unweighted first-pass formula for comparison.
    Use lesson_features() and estimate_from_features() for the current fit.
    """
    if isinstance(kp_count, bool) or not isinstance(kp_count, int) or kp_count < 1:
        raise ValueError("kp_count must be a positive integer")
    if any(not math.isfinite(v) or v < 0 for v in (solution_math_tokens, reading_words)):
        raise ValueError("Content measurements must be finite and nonnegative")
    minutes = 3.16 + 0.64 * kp_count + 0.0159 * solution_math_tokens + 0.0005 * reading_words
    return max(7, math.floor(minutes + 0.5))


def lesson_features(content, tutorial_prose_word_count=0):
    """Prepare current formula's measurements once from lesson content only."""
    grouped = defaultdict(list)
    for question in content["questions"]:
        if question["difficulty"] not in DURATION_MULTIPLIERS:
            raise ValueError("Question needs easy, moderate, or hard difficulty")
        grouped[question["knowledge_point_id"]].append(question)
    if not grouped:
        raise ValueError("A lesson needs at least one knowledge point")
    features = dict.fromkeys(FULL_CONTENT_COEFFICIENTS, 0.0)
    for questions in grouped.values():
        n = len(questions)
        features["multiplier_1_2_4_math_100"] += sum(
            math_tokens(q["worked_solution"])*DURATION_MULTIPLIERS[q["difficulty"]] for q in questions)/n/100
        features["question_steps"] += sum(clean_markdown(q["worked_solution"]).count("=") for q in questions)/n
        features["question_math_100"] += sum(math_tokens(q["problem"]) for q in questions)/n/100
        features["extra_fields"] += sum(max(0, len(q["answer_fields"])-1) for q in questions)/n
        features["blank_kp"] += sum(any(f["type"] == "blank" for f in q["answer_fields"]) for q in questions)/n
        for band in ("moderate", "hard"):
            features[band+"_kp"] += sum(q["difficulty"] == band for q in questions)/n
    examples = content.get("canonical_examples", [])
    features["example_steps"] = sum(clean_markdown(q["worked_solution"]).count("=") for q in examples)
    features["reading_100"] = (tutorial_prose_word_count +
        sum(prose_words(q["problem"])+prose_words(q["worked_solution"]) for q in examples))/100
    return features


def estimate_from_features(features):
    """Current best full-content fit; fixed scalar arithmetic, no dependencies."""
    values = [features[name] for name in FULL_CONTENT_COEFFICIENTS]
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("Content measurements must be finite and nonnegative")
    minutes = sum(FULL_CONTENT_COEFFICIENTS[name]*features[name] for name in FULL_CONTENT_COEFFICIENTS)
    return max(7, math.floor(minutes+0.5))


def estimate_weighted_lesson_base(kp_count, weighted_solution_tokens, reading_words=0, extra_fields=0):
    """Compact alternative, four cached measurements; approximately 2.02 XP MAE.

    weighted_solution_tokens = sum of each KP's mean solution token count after
    applying Easy/Moderate/Hard multipliers 1/2/4. extra_fields uses per-KP means.
    """
    if isinstance(kp_count, bool) or not isinstance(kp_count, int) or kp_count < 1:
        raise ValueError("kp_count must be a positive integer")
    if any(not math.isfinite(v) or v < 0 for v in (weighted_solution_tokens, reading_words, extra_fields)):
        raise ValueError("Content measurements must be finite and nonnegative")
    minutes = (0.237166134453485 + 0.32457203311006777*kp_count +
        0.012009953383993337*weighted_solution_tokens + 0.0007966788300189373*reading_words +
        2.5204476568100143*extra_fields)
    return max(7, math.floor(minutes+0.5))
