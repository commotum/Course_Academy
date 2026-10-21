"""Learner-facing checkbox generation requires a nonempty correct subset.

This module is also copied into immutable generator packages. Keep it free of
repository imports so registered packages remain relocatable and offline.
"""
from functools import wraps
import hashlib
import inspect

POLICY_VERSION = 'nonempty-checkbox-v1'
MAX_ATTEMPTS = 128

class EmptyCheckboxSelection(ValueError):
    pass

def _enum(value):
    return str(value.get(':db/ident') if isinstance(value, dict) else value)

def checkbox_selection(record):
    if not isinstance(record, dict):
        return []
    question = record.get('question', record)
    values = []
    for field in question.get(':question/answer-fields', []):
        if _enum(field.get(':answer-field/type')) != ':answer-field.type/checkbox':
            continue
        ref = field.get(':answer-field/correct')
        value = ref.get(':answer/value') if isinstance(ref, dict) else None
        if value is None:
            aid = ref.get(':answer/id') if isinstance(ref, dict) else ref[1] if isinstance(ref, (list, tuple)) else ref
            value = next(a[':answer/value'] for a in field.get(':answer-field/choices', [])
                         if str(a[':answer/id']) == str(aid))
        if value not in ('false', 'true'):
            raise ValueError('Checkbox correct answers must be text true or false')
        values.append(value == 'true')
    return values

def _evidence_only(record):
    generation = record.get('generation', {}) if isinstance(record, dict) else {}
    return generation.get('eligible_for_learning') is False or generation.get('raw_evidence') is True or generation.get('evidence_only') is True

def _invalid(record):
    if _evidence_only(record):
        return False
    values = checkbox_selection(record)
    return bool(values) and not any(values)

def _records(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get('records'), list):
        return value['records']
    return [value]

def _seed(seed, attempt, slot=0):
    text = f'{POLICY_VERSION}:{seed}:{attempt}:{slot}'.encode()
    return int.from_bytes(hashlib.sha256(text).digest()[:8], 'big')

def nonempty_checkbox(generator):
    """Preserve valid calls; deterministically resample empty seeded instances.

    Explicit mathematical parameters are never silently changed. Historical
    evidence-only replay remains readable; publication checks eligibility too.
    Batch replacements are generated individually rather than demanding that
    a whole large batch happen to contain no empty subsets on one seed.
    """
    if getattr(generator, '_nonempty_checkbox_policy', False):
        return generator
    signature = inspect.signature(generator)

    @wraps(generator)
    def checked(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        seed = bound.arguments.get('seed')
        explicit = any(bound.arguments.get(name) is not None
                       for name in ('parameters', 'params', 'numbers', 'cases', 'decision_case', 'selection'))
        can_retry = 'seed' in signature.parameters and not explicit
        last_error = None
        for attempt in range(MAX_ATTEMPTS if can_retry else 1):
            if attempt:
                bound.arguments['seed'] = _seed(seed, attempt)
            try:
                result = generator(*bound.args, **bound.kwargs)
            except EmptyCheckboxSelection as error:
                last_error = error
                if can_retry:
                    continue
                raise
            records = _records(result)
            bad = [i for i, record in enumerate(records) if _invalid(record)]
            if bad and not can_retry:
                raise EmptyCheckboxSelection('Checkbox question has no correct selectable option; explicit parameters cannot be resampled')
            if bad and len(records) > 1 and 'count' in signature.parameters:
                for slot in bad:
                    for replacement in range(1, MAX_ATTEMPTS + 1):
                        single = signature.bind(*bound.args, **bound.kwargs)
                        single.arguments['count'] = 1
                        single.arguments['seed'] = _seed(seed, replacement, slot + 1)
                        try:
                            candidates = _records(generator(*single.args, **single.kwargs))
                        except EmptyCheckboxSelection:
                            continue
                        if len(candidates) == 1 and not _invalid(candidates[0]):
                            records[slot] = candidates[0]
                            break
                    else:
                        raise EmptyCheckboxSelection('No nonempty checkbox instance found for this batch slot')
                bad = []
            if bad:
                last_error = EmptyCheckboxSelection('Checkbox question has no correct selectable option')
                continue
            for record in records:
                if isinstance(record, dict) and checkbox_selection(record) and not _evidence_only(record):
                    record.setdefault('generation', {}).setdefault('checkbox_selection_policy', POLICY_VERSION)
            return result
        raise EmptyCheckboxSelection('No nonempty checkbox instance exists in the bounded sampling attempts') from last_error

    checked._nonempty_checkbox_policy = True
    return checked
