"""Small, replayable accuracy and difficulty estimators for FIRe.

Separate assessment/practice accuracy and their average are described by Justin
Skycak in Math Academy Podcast #6, Part 3 (2026-01-28), at 21:33–23:42:
https://www.justinmath.com/math-academy-podcast-6-part-3/

The EWMA, fractional evidence weighting, initial values, and use of the prior
for an unobserved channel are reconstruction policies, not published MA
parameters. A caller must classify assessment evidence explicitly; a diagnostic
or a task label does not automatically establish equivalent assessment context.

These classes have no graph behavior. The engine routes local ability evidence;
a global learner estimate must receive each direct answer once, without graph
multiplication. Difficulty consumes only direct serious-student assessments.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def _number(value: float, name: str, *, low: float = 0,
            high: float | None = None) -> None:
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value)):
        raise ValueError(f'{name} must be a finite number')
    if value < low or (high is not None and value > high):
        raise ValueError(f'{name} outside [{low}, {high}]')


def _outcomes(values: tuple[bool, ...]) -> tuple[bool, ...]:
    try:
        outcomes = tuple(values)
    except TypeError as error:
        raise ValueError('outcomes must contain boolean answers') from error
    if any(type(correct) is not bool for correct in outcomes):
        raise ValueError('outcomes must contain boolean answers, not unknowns or scores')
    return outcomes


@dataclass
class AccuracyEstimate:
    """Two recency-weighted channels, balanced independently of answer counts.

    ``mass`` records the weighted count of observations, not EWMA confidence or
    a weight used to combine the two channels. An unobserved channel keeps its
    supplied starting estimate. All answers count, including answers in failed
    tasks or first lessons that have not yet established mastery.

    Dataclass fields form the serialization format: ``asdict(estimate)`` and
    ``AccuracyEstimate(**payload)`` round-trip JSON-compatible snapshots.
    """
    assessment_accuracy: float = 0.8
    practice_accuracy: float = 0.8
    assessment_mass: float = 0.0
    practice_mass: float = 0.0

    def __post_init__(self) -> None:
        for field in ('assessment_accuracy', 'practice_accuracy'):
            _number(getattr(self, field), field, high=1)
        for field in ('assessment_mass', 'practice_mass'):
            _number(getattr(self, field), field)

    @property
    def accuracy(self) -> float:
        return (self.assessment_accuracy + self.practice_accuracy) / 2

    def update(self, outcomes: tuple[bool, ...], *, assessment: bool,
               alpha: float = 0.2, weight: float = 1.0) -> AccuracyEstimate:
        """Apply ordered outcomes atomically to one channel and return self.

        Each answer uses ``1 - (1 - alpha)**weight`` as its EWMA step. A zero
        weight or empty batch is a no-op. Fractional weights can represent
        local graph coverage; global direct evidence normally uses weight one.
        """
        self.__post_init__()
        if type(assessment) is not bool:
            raise ValueError('assessment must be an explicit boolean')
        answers = _outcomes(outcomes)
        _number(alpha, 'alpha', high=1)
        _number(weight, 'weight')
        if alpha == 0:
            raise ValueError('alpha must be positive')
        if not answers or weight == 0:
            return self
        accuracy_field = 'assessment_accuracy' if assessment else 'practice_accuracy'
        mass_field = 'assessment_mass' if assessment else 'practice_mass'
        new_mass = getattr(self, mass_field) + weight * len(answers)
        _number(new_mass, mass_field)
        step = 1.0 if alpha == 1 else -math.expm1(weight * math.log1p(-alpha))
        updated = getattr(self, accuracy_field)
        for correct in answers:
            updated = (1 - step) * updated + step * int(correct)
        _number(updated, accuracy_field, high=1)
        setattr(self, accuracy_field, updated)
        setattr(self, mass_field, new_mass)
        return self


@dataclass
class DifficultyEstimate:
    """Population assessment accuracy, without graph-propagated observations.

    Smaller accuracy means harder material. Only answers explicitly marked as
    both serious-student work and assessment work contribute. The zero-evidence
    fallback is supplied policy; no hidden pseudocounts or cohort inference are
    added. Fields serialize with ``dataclasses.asdict`` and the constructor.
    """
    assessment_correct: float = 0.0
    assessment_total: float = 0.0
    prior_accuracy: float = 0.8

    def __post_init__(self) -> None:
        _number(self.assessment_correct, 'assessment_correct')
        _number(self.assessment_total, 'assessment_total')
        _number(self.prior_accuracy, 'prior_accuracy', high=1)
        if self.assessment_correct > self.assessment_total:
            raise ValueError('assessment_correct cannot exceed assessment_total')

    @property
    def accuracy(self) -> float:
        return (self.assessment_correct / self.assessment_total
                if self.assessment_total else self.prior_accuracy)

    def update(self, outcomes: tuple[bool, ...], *, serious: bool,
               assessment: bool) -> DifficultyEstimate:
        """Count an eligible batch once; exclude practice and nonserious work."""
        self.__post_init__()
        if type(serious) is not bool or type(assessment) is not bool:
            raise ValueError('serious and assessment must be explicit booleans')
        answers = _outcomes(outcomes)
        if not serious or not assessment or not answers:
            return self
        correct = self.assessment_correct + sum(answers)
        total = self.assessment_total + len(answers)
        _number(correct, 'assessment_correct')
        _number(total, 'assessment_total')
        self.assessment_correct = correct
        self.assessment_total = total
        return self
