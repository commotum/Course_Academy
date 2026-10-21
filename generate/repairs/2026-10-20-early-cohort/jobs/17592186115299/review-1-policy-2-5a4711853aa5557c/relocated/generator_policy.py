"""Learner-facing checkbox generation requires a nonempty correct subset.

This module is also copied into immutable generator packages. Keep it free of
repository imports so registered packages remain relocatable and offline.
"""
from functools import wraps
import copy
import hashlib
import inspect
import json
import re
import uuid

POLICY_VERSION = 'nonempty-checkbox-v1'
MAX_ATTEMPTS = 128
NONE_POLICY_VERSION = 'explicit-source-none-v1'

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

def explicit_none_checkbox(record, label='None of the above'):
    """Preserve a source-backed None option without changing ordinary truths.

    Callers opt in only for checkbox families with reviewed source evidence.
    A new response shape gets fresh question/field/answer identities so it
    cannot revise an earlier generated question or share its owned banks.
    Raw evidence and non-checkbox records remain unchanged.
    """
    if not checkbox_selection(record) or _evidence_only(record):
        return record
    question = record.get('question', record)
    fields = question[':question/answer-fields']
    none = [f for f in fields if f.get(':answer-field/key') in (label, 'None')]
    if none:
        if len(none) != 1:
            raise ValueError('Duplicate None checkbox options')
        ordinary = [f for f in fields if f is not none[0]]
        expected = not any(checkbox_selection({':question/answer-fields': ordinary}))
        if checkbox_selection({':question/answer-fields': none}) != [expected]:
            raise ValueError('None checkbox disagrees with the ordinary options')
        return record
    result = copy.deepcopy(record)
    question = result.get('question', result)
    fields = question[':question/answer-fields']
    selected = checkbox_selection(record)
    old_id = str(question[':question/id'])
    qid = uuid.uuid5(uuid.NAMESPACE_URL, NONE_POLICY_VERSION + ':' + old_id)
    question[':question/id'] = str(qid)
    question.pop(':db/id', None)
    for index, field in enumerate(fields):
        fid = uuid.uuid5(qid, 'field:' + str(field.get(':answer-field/id', index)))
        ref = field.get(':answer-field/correct')
        aid = ref.get(':answer/id') if isinstance(ref, dict) else ref[1] if isinstance(ref, (list, tuple)) else ref
        correct = None
        for answer in field.get(':answer-field/choices', []):
            old = str(answer[':answer/id'])
            new = str(uuid.uuid5(fid, 'answer:' + old))
            if old == str(aid):
                correct = new
            answer[':answer/id'] = new
            answer.pop(':db/id', None)
        if correct is None:
            raise ValueError('None migration requires a field-owned correct answer')
        field[':answer-field/id'] = str(fid)
        field[':answer-field/correct'] = [':answer/id', correct]
        field.pop(':db/id', None)
    fid = uuid.uuid5(qid, 'field:none')
    answers = [{':answer/id': str(uuid.uuid5(fid, value)),
                ':answer/type': ':answer.type/text', ':answer/value': value}
               for value in ('false', 'true')]
    fields.append({':answer-field/id': str(fid), ':answer-field/key': label,
                   ':answer-field/type': ':answer-field.type/checkbox',
                   ':answer-field/choices': answers,
                   ':answer-field/correct': [':answer/id', answers[int(not any(selected))][':answer/id']]})
    # This instruction describes the old implicit empty-selection contract.
    question[':question/problem'] = re.sub(
        r'\s*If none apply, leave all (?:boxes|checkboxes) unchecked\.', '',
        question[':question/problem'], flags=re.I)
    generation = result.setdefault('generation', {})
    generation['explicit_none_policy'] = NONE_POLICY_VERSION
    fingerprint = hashlib.sha256(json.dumps(question, sort_keys=True, ensure_ascii=False,
                                            default=str).encode()).hexdigest()
    generation['content_fingerprint'] = fingerprint
    for name in ('content_hash', 'content_id', 'content_identity'):
        if name in generation:
            generation[name] = fingerprint
    return result

def _prepare_result(value, none_label):
    if none_label is None:
        return value
    if isinstance(value, list):
        return [explicit_none_checkbox(r, none_label) for r in value]
    if isinstance(value, dict) and isinstance(value.get('records'), list):
        return {**value, 'records': [explicit_none_checkbox(r, none_label) for r in value['records']]}
    return explicit_none_checkbox(value, none_label)

def nonempty_checkbox(generator, *, none_label=None):
    """Preserve valid calls; deterministically resample empty seeded instances.

    Explicit mathematical parameters are never silently changed. Historical
    evidence-only replay remains readable; publication checks eligibility too.
    Batch replacements are generated individually rather than demanding that
    a whole large batch happen to contain no empty subsets on one seed.
    """
    if getattr(generator, '_nonempty_checkbox_policy', False) and getattr(generator, '_source_none_label', None) == none_label:
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
                result = _prepare_result(generator(*bound.args, **bound.kwargs), none_label)
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
                            candidates = _records(_prepare_result(generator(*single.args, **single.kwargs), none_label))
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
    checked._source_none_label = none_label
    return checked
