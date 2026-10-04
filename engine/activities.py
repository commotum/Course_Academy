"""Small application rules, separate from FIRe retention and persistence.

Published practice/diagnostic structure is described in The Math Academy Way's
Practice FAQ and diagnostic technical chapter. Streak stopping and propagation
deduplication below are explicit local policies. The accepted earned-XP rules
are documented in schema/engine/3-xp-weights.edn and the earned-XP report.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import math
from typing import Literal


Outcome = bool | None  # None means an explicitly skipped, presented question.
Number = int | float | Fraction | Decimal


def _outcomes(values: Iterable[Outcome]) -> tuple[Outcome, ...]:
    values = tuple(values)
    if any(value is not None and type(value) is not bool for value in values):
        raise ValueError('outcomes must be bool or None (explicit skip)')
    return values


@dataclass(frozen=True)
class PracticeDecision:
    status: Literal['continue', 'passed', 'failed']
    attempted: int
    correct: int
    streak: int

    @property
    def complete(self) -> bool:
        return self.status != 'continue'

    @property
    def passed(self) -> bool | None:
        return None if not self.complete else self.status == 'passed'


def _practice_prefix(outcomes: Iterable[Outcome], required_streak: int) -> PracticeDecision:
    values = _outcomes(outcomes)
    streak = correct = 0
    status = 'continue'
    for attempted, value in enumerate(values, 1):
        if status != 'continue':
            raise ValueError('outcomes continue beyond the first terminal prefix')
        if value is True:
            correct += 1
            streak += 1
        else:
            streak = 0
        # A qualifying streak on question five passes before the cap is applied.
        status = 'passed' if streak >= required_streak else ('failed' if attempted == 5 else 'continue')
    return PracticeDecision(status, len(values), correct, streak)


def evaluate_kp_prefix(outcomes: Iterable[Outcome]) -> PracticeDecision:
    """Local lesson policy: two consecutive correct, at most five attempts.

    A skip consumes an attempt and breaks the streak; it is not relabeled wrong.
    Passing one KP is not a decision that the entire lesson/topic is mastered.
    """
    return _practice_prefix(outcomes, 2)


def evaluate_review_prefix(outcomes: Iterable[Outcome]) -> PracticeDecision:
    """Local review policy: three consecutive correct, at most five attempts.

    Published evidence makes answer order significant, but does not establish
    this as the universal historical MA review rule. A skip breaks the streak.
    """
    return _practice_prefix(outcomes, 3)


def _number(value: Number, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction, Decimal)):
        raise ValueError(f'{name} must be a finite number')
    try:
        return Fraction(str(value))
    except (ValueError, OverflowError):
        raise ValueError(f'{name} must be a finite number') from None


def round_half_up(value: Number) -> int:
    """Round with floor(x + 1/2), matching the observed-XP analysis.

    Exact ties go toward positive infinity, including negative values; this is
    deliberately different from Python round() and Decimal ROUND_HALF_UP.
    """
    shifted = _number(value, 'value') + Fraction(1, 2)
    return shifted.numerator // shifted.denominator


def _xp_inputs(base: Number, outcomes: Iterable[Outcome]) -> tuple[Fraction, tuple[Outcome, ...]]:
    baseline = _number(base, 'base XP')
    if baseline < 0:
        raise ValueError('base XP must be nonnegative')
    values = _outcomes(outcomes)
    if not values:
        raise ValueError('XP requires at least one presented question')
    return baseline, values


def earned_xp(kind: str, base: Number, correct: int, total: int, *,
              final_correct: bool | None = None) -> int:
    """Version-one earned XP; equal question weights, exact final rounding.

    Quizzes include all assigned questions in total, including unanswered ones.
    Partial reviews require their final outcome (a skip counts as not correct).
    Delivery/mastery decisions are separate: a finished failed task still scores.
    Integer bases use integer arithmetic; exact fractional bases remain supported.
    """
    if type(correct) is not int or type(total) is not int or total <= 0 or not 0 <= correct <= total:
        raise ValueError('Require integer counts with total > 0 and 0 <= correct <= total')
    if final_correct is not None and type(final_correct) is not bool:
        raise ValueError('final_correct must be boolean or None')
    baseline = base if type(base) is int else _number(base, 'base XP')
    if baseline < 0:
        raise ValueError('base XP must be nonnegative')
    b, d = (baseline, 1) if type(baseline) is int else (baseline.numerator, baseline.denominator)
    def scaled(numerator, denominator):
        n, den = b * numerator, d * denominator
        return (2 * n + den) // (2 * den)
    kind = kind.lower()
    if kind == 'lesson':
        if 2 * correct < total:
            return -1
        if correct == total:
            return scaled(5, 4)
        return scaled(min(10 * total, 15 * correct - 3 * total), 10 * total)
    if kind == 'review':
        if 2 * correct < total:
            return -1
        if correct == total:
            return (2 * b + d) // (2 * d) + 2
        if 3 * correct >= 2 * total:
            return scaled(1, 1)
        if final_correct is None:
            raise ValueError('Partial-credit review needs final_correct')
        return scaled(correct, total) if final_correct else 0
    if kind in {'assessment', 'quiz'}:
        if 5 * correct < total:
            return -1
        return max(0, scaled(6 * (20 * correct - 7 * total), 65 * total))
    if kind == 'multistep':
        return max(-1, scaled(9 * correct - 4 * total, 4 * total))
    raise ValueError('No base-relative XP formula for ' + kind)


def assessment_xp_candidate(base: Number, outcomes: Iterable[Outcome]) -> int:
    """Quiz rule; include unanswered assigned questions as None for XP only."""
    baseline, values = _xp_inputs(base, outcomes)
    return earned_xp('assessment', baseline, sum(v is True for v in values), len(values))


def multistep_xp_candidate(base: Number, outcomes: Iterable[Outcome]) -> int:
    """Multistep rule, with the accepted -1 floor; skips receive no credit."""
    baseline, values = _xp_inputs(base, outcomes)
    return earned_xp('multistep', baseline, sum(v is True for v in values), len(values))


def _explicit_award(award: int | None) -> int | None:
    if award is not None and type(award) is not int:
        raise ValueError('explicit XP award must be an integer')
    return award


def lesson_xp_candidate(base: Number, outcomes: Iterable[Outcome], *, award: int | None = None) -> int:
    """Accepted whole-lesson accuracy rule, including partial and failed work.

    The caller must already have established completion of the whole lesson.
    An explicit award is authoritative, including zero or negative XP.
    """
    baseline, values = _xp_inputs(base, outcomes)
    explicit = _explicit_award(award)
    if explicit is not None:
        return explicit
    return earned_xp('lesson', baseline, sum(v is True for v in values), len(values))


def review_xp_candidate(base: Number, outcomes: Iterable[Outcome], *, award: int | None = None) -> int:
    """Accepted review rule, including low-score and final-outcome bands.

    An explicit caller award remains authoritative for imported/observed XP.
    """
    baseline, values = _xp_inputs(base, outcomes)
    explicit = _explicit_award(award)
    if explicit is not None:
        return explicit
    return earned_xp('review', baseline, sum(v is True for v in values), len(values),
                     final_correct=values[-1] is True)


class DiagnosticBalance:
    """Published signed placement balances on a prerequisite DAG, not FIRe.

    Correct evidence propagates down to prerequisites, incorrect evidence up to
    postrequisites. Each answer contributes once to every reachable topic,
    including its own; unit path propagation/deduplication is a local choice.
    Supply a diminished correct weight for slow responses. The source gives no
    exact time curve or separate skip-weight rule, so skip_policy is required:
    'negative' treats explicit 'I don't know' as negative knowledge evidence;
    'neutral' records no balance change. Neither grants positive skip credit.

    This helper does not infer leaf-module correlation, graph coverage, exam
    termination, replacement of prior learner state, or retry eligibility.
    Caller owns occurrence identity and must apply each answer exactly once.
    """
    def __init__(self, prerequisites: Mapping[str, Iterable[str]], *,
                 skip_policy: Literal['negative', 'neutral']):
        if skip_policy not in ('negative', 'neutral'):
            raise ValueError('skip_policy must explicitly be negative or neutral')
        if not isinstance(prerequisites, Mapping):
            raise ValueError('prerequisites must map topics to prerequisite IDs')
        direct: dict[str, frozenset[str]] = {}
        for topic, parents in prerequisites.items():
            self._validate_topic(topic)
            if isinstance(parents, (str, bytes)):
                raise ValueError('prerequisites must be an iterable of topic IDs')
            try:
                parents = tuple(parents)
            except TypeError:
                raise ValueError('prerequisites must be an iterable of topic IDs') from None
            for parent in parents:
                self._validate_topic(parent)
            if len(set(parents)) != len(parents):
                raise ValueError('duplicate prerequisite edge')
            direct[topic] = frozenset(parents)
        topics = set(direct).union(*(set(parents) for parents in direct.values()))
        self._down = {topic: direct.get(topic, frozenset()) for topic in sorted(topics)}
        self._up: dict[str, set[str]] = {topic: set() for topic in self._down}
        for topic, parents in self._down.items():
            for parent in parents:
                self._up[parent].add(topic)
        remaining = {topic: len(parents) for topic, parents in self._down.items()}
        ready = deque(topic for topic, count in remaining.items() if count == 0)
        visited = 0
        while ready:
            topic = ready.popleft()
            visited += 1
            for child in self._up[topic]:
                remaining[child] -= 1
                if remaining[child] == 0:
                    ready.append(child)
        if visited != len(topics):
            raise ValueError('diagnostic prerequisites must be acyclic')
        self.skip_policy = skip_policy
        self._balances = dict.fromkeys(self._down, 0.0)

    @staticmethod
    def _validate_topic(topic: str) -> None:
        if not isinstance(topic, str) or not topic:
            raise ValueError('topic IDs must be nonempty strings')

    def apply(self, topic: str, outcome: Outcome, *, weight: float = 1.0) -> dict[str, float]:
        """Accumulate one presented response and return its topic deltas.

        Weight is a supplied evidence magnitude, never elapsed time or earned
        XP. Reduced weights are accepted only for correct answers; wrong/skip
        evidence uses one. Validation completes before changing any balances.
        """
        self._validate_topic(topic)
        if topic not in self._balances:
            raise ValueError('topic is outside the diagnostic graph')
        _outcomes((outcome,))
        magnitude = _number(weight, 'weight')
        if not 0 < magnitude <= 1:
            raise ValueError('weight must satisfy 0 < weight <= 1')
        if outcome is not True and magnitude != 1:
            raise ValueError('reduced diagnostic weights apply only to correct answers')
        if outcome is None and self.skip_policy == 'neutral':
            return {}
        graph = self._down if outcome is True else self._up
        reached: set[str] = set()
        pending = [topic]
        while pending:
            current = pending.pop()
            if current not in reached:
                reached.add(current)
                pending.extend(graph[current])
        delta = float(magnitude) if outcome is True else -1.0
        if outcome is True and delta == 0:
            raise ValueError('positive diagnostic weight is too small to represent')
        changes = {target: delta for target in sorted(reached)}
        updated = {target: self._balances[target] + delta for target in reached}
        if not all(math.isfinite(value) for value in updated.values()):
            raise ValueError('diagnostic balance overflow')
        self._balances.update(updated)
        return changes

    def snapshot(self) -> dict[str, float]:
        """Return all signed balances, including zero/negative confidence."""
        return dict(self._balances)

    def positive_repetitions(self) -> dict[str, float]:
        """Final positive balances for placement initialization, not review events.

        Call only once the controller determines the diagnostic is complete.
        Nonpositive balances confer no new mastery; this does not revoke or
        overwrite existing learner progress.
        """
        return {topic: balance for topic, balance in self._balances.items() if balance > 0}
