"""Compact whole-data fit, including provisional low-score penalty bands.

This is a local approximation, not Math Academy's recovered scoring policy.
The 50%/20% penalty cutoffs and -1 floor are choices within sparse evidence.
See reference/xp-docs/earned-xp-formula-report.md before using these defaults.
"""


def _round_ratio(numerator, denominator):
    """Nearest integer, half ties toward positive infinity."""
    return (2 * numerator + denominator) // (2 * denominator)


def estimate_earned_xp(kind, base, correct, total, *, final_correct=None):
    """Estimate integer XP using counts, task type, base, and review ending.

    Count questions once, including assigned unanswered questions for quizzes.
    final_correct is needed for reviews between 50% and 2/3 accuracy; supplying
    None there raises instead of silently inventing a completion outcome.
    Difficulty weights are equal: 1/2/4 weights worsened the empirical fit.
    """
    if any(type(v) is not int for v in (base, correct, total)):
        raise ValueError("base, correct, and total must be integers")
    if base <= 0 or total <= 0 or not 0 <= correct <= total:
        raise ValueError("Require base > 0, total > 0, and 0 <= correct <= total")
    if final_correct is not None and type(final_correct) is not bool:
        raise ValueError("final_correct must be boolean or None")
    kind = kind.lower()
    if kind == "quiz":
        kind = "assessment"
    if kind == "lesson":
        if 2 * correct < total:
            return -1
        if correct == total:
            return _round_ratio(5 * base, 4)
        # .6 + 1.5(p-.6) = 1.5p-.3; full base is a plateau.
        numerator = min(10 * total, 15 * correct - 3 * total)
        return _round_ratio(base * numerator, 10 * total)
    if kind == "review":
        if 2 * correct < total:
            return -1
        if correct == total:
            return base + 2
        if 3 * correct >= 2 * total:
            return base
        if final_correct is None:
            raise ValueError("Partial-credit review needs final_correct")
        return _round_ratio(base * correct, total) if final_correct else 0
    if kind == "assessment":
        if 5 * correct < total:
            return -1
        return max(0, _round_ratio(6 * base * (20 * correct - 7 * total), 65 * total))
    if kind == "multistep":
        return max(-1, _round_ratio(base * (9 * correct - 4 * total), 4 * total))
    raise ValueError("No base-relative formula identified for " + kind)


def estimate_from_outcomes(kind, base, outcomes):
    outcomes = list(outcomes)
    if not outcomes or any(type(outcome) is not bool for outcome in outcomes):
        raise ValueError("outcomes must be a nonempty sequence of booleans")
    return estimate_earned_xp(kind, base, sum(outcomes), len(outcomes),
                             final_correct=outcomes[-1])
