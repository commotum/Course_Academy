"""Cheap accuracy-only XP approximations; not recovered Math Academy code.

Inputs include task type and base XP. Negative awards and hidden task state
cannot be recovered from accuracy alone. See the accompanying report.
"""
from fractions import Fraction


def rounded(value):
    """Round once, using floor(x + 1/2), including negative x."""
    value = Fraction(value) + Fraction(1, 2)
    return value.numerator // value.denominator


def _round_ratio(numerator, denominator):
    return (2 * numerator + denominator) // (2 * denominator)


def estimate_earned_xp(kind, base, correct, total):
    """Return the candidate award from task type, base, and whole-task accuracy.

    Questions with multiple fields count once. For fixed quizzes, total includes
    all assigned questions, including unanswered questions at expiry. Predictions
    below the observed accuracy ranges are extrapolations, not identified rules.
    """
    if any(isinstance(v, bool) or not isinstance(v, int) for v in (base, correct, total)):
        raise ValueError("base, correct, and total must be integers")
    if base < 0 or total <= 0 or not 0 <= correct <= total:
        raise ValueError("Require base >= 0, total > 0, and 0 <= correct <= total")
    kind = kind.lower()
    if kind == "lesson":
        if correct == total:
            return _round_ratio(5 * base, 4)
        # 1.4p - .24 = (35C - 6N)/(25N), bounded between 0 and 1.
        numerator = max(0, min(25 * total, 35 * correct - 6 * total))
        return _round_ratio(base * numerator, 25 * total)
    if kind == "review":
        if correct == total:
            return base + 2
        return base if 3 * correct >= 2 * total else _round_ratio(base * correct, total)
    if kind in ("assessment", "quiz"):
        return max(0, _round_ratio(6 * base * (20 * correct - 7 * total), 65 * total))
    if kind == "multistep":
        return _round_ratio(base * (9 * correct - 4 * total), 4 * total)
    raise ValueError("No accuracy-only formula identified for " + kind)


def estimate_earned_xp_with_sequence(kind, base, outcomes):
    """Optional review-state hypothesis using ordered boolean question outcomes.

    At below 2/3 accuracy, reviews ending incorrectly get zero. This fits the
    retained review sample but has only one supporting terminal-error case.
    Other types retain their accuracy-only estimates, including penalty misses.
    """
    outcomes = list(outcomes)
    if not outcomes or any(type(outcome) is not bool for outcome in outcomes):
        raise ValueError("outcomes must be a nonempty sequence of booleans")
    correct, total = sum(outcomes), len(outcomes)
    estimate = estimate_earned_xp(kind, base, correct, total)
    if kind.lower() == "review" and 3 * correct < 2 * total and not outcomes[-1]:
        return 0
    return estimate
