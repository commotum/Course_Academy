"""Accept answer evidence without promoting solver guesses into source facts."""
from __future__ import annotations
import copy
import re
from urllib.parse import urlsplit
from .text import markdown

class UnsupportedContent(ValueError):
    """Required source evidence is absent; obtain a final capture judgment."""


def image_answer(field: dict) -> str | None:
    """MA's -a-1 filename convention applies only to image-led radio choices.

    A text alternative such as DNE does not invalidate an otherwise unambiguous
    image choice set. Images in the problem statement never participate.
    """
    if field.get('type') != 'radio':
        return None
    choices = field.get('choices', [])
    images = [c for c in choices if c.get('type') == 'image']
    if not images or len(images) <= len(choices) / 2:
        return None
    candidates, families = [], set()
    for choice in images:
        source = choice.get('source_url') or choice.get('original_url') or choice.get('value', '')
        match = re.search(r'(?:!\[[^\]]*\]\(|src=["\'])([^)"\']+)', source)
        if match:
            source = match[1]
        filename = urlsplit(source).path.rsplit('/', 1)[-1]
        match = re.fullmatch(r'(.+)-a-(\d+)(?:[-_][^.]*)?(?:\.(?:svg|png|jpg|jpeg|gif|webp))?', filename, flags=re.I)
        if not match:
            return None
        families.add(match[1])
        if match[2] == '1':
            candidates.append(choice['value'])
    return candidates[0] if len(candidates) == 1 and len(families) == 1 else None


def evidence_value(field: dict, question: dict) -> str:
    evidence = field.get('evidence') or field.get('correct_evidence') or {}
    value = field.get('correct_value')
    kind = evidence.get('kind')
    if kind in ('ma_answer', 'ma_correct_grade'):
        if not evidence.get('source_file') or evidence.get('value') != value:
            raise UnsupportedContent('Correct-answer evidence lacks its source or differs from the value')
        if kind == 'ma_correct_grade' and evidence.get('grade', 'correct') != 'correct':
            raise UnsupportedContent('A submitted value without a correct grade is not an answer key')
        return value
    if kind == 'worked_solution':
        quote = evidence.get('solution_quote')
        solution = question.get('worked_solution', '')
        if (evidence.get('matches_worked_solution') is True and evidence.get('value') == value
                and evidence.get('source_file') and isinstance(quote, str) and quote.strip()
                and quote in solution):
            return value
        raise UnsupportedContent('Extracted answer has no checked quotation from the worked solution')
    inferred = image_answer(field)
    if inferred is not None:
        field['evidence'] = {'kind': 'radio_image_filename', 'value': inferred,
                             'reason': 'Unique -a-1 original filename in image-led radio choices'}
        return inferred
    raise UnsupportedContent('Answer field has no confirmed Math Academy evidence')


def authoritative_question(original: dict, *, example=False) -> dict:
    q = copy.deepcopy(original)
    mid = str(q.get('math_academy_id', ''))
    if not re.fullmatch(r'e-\d+' if example else r'q-\d+', mid):
        raise UnsupportedContent('Question requires a verified prefixed source identity')
    if not isinstance(q.get('problem'), str) or not q['problem'].strip():
        raise UnsupportedContent('Source problem is missing')
    required_errors = [error for error in q.get('errors', [])
                       if not str(error).startswith('Screenshot unavailable:')]
    if required_errors and not q.get('source_errors_resolved'):
        raise UnsupportedContent('Source extraction contains unresolved errors: ' + '; '.join(map(str, required_errors)))
    q['answer_fields'] = q.get('answer_fields', q.get('fields', []))
    if not example and not q['answer_fields']:
        raise UnsupportedContent('Practice question requires complete answer fields')
    if example and not q.get('worked_solution'):
        raise UnsupportedContent('Canonical example requires its worked solution')
    keys = set()
    for field in q['answer_fields']:
        key = field.get('key')
        if not isinstance(key, str) or not key or key in keys:
            raise UnsupportedContent('Answer-field keys must be present and unique')
        keys.add(key)
        if field.get('type') not in ('radio', 'select', 'blank'):
            raise UnsupportedContent('Unsupported answer-field type')
        correct = evidence_value(field, q)
        if not isinstance(correct, str):
            raise UnsupportedContent('Confirmed correct answer must be a string')
        choices = field.setdefault('choices', [])
        if field['type'] == 'blank' and not choices:
            choices.append({'type': field.get('value_type', 'math'), 'value': correct})
        if field['type'] in ('radio', 'select') and (len(choices) < 2 or field.get('choices_complete') is False):
            raise UnsupportedContent('Source choices are incomplete')
        signatures = set()
        for choice in choices:
            if choice.get('type') not in ('math', 'text', 'image') or not isinstance(choice.get('value'), str):
                raise UnsupportedContent('Answer values require supported types and exact strings')
            signatures.add((choice['type'], choice['value']))
        corrects = [s for s in signatures if s[1] == correct and
                    (not field.get('correct_type') or s[0] == field['correct_type'])]
        if len(corrects) != 1:
            raise UnsupportedContent('Correct answer does not select one typed source choice')
        field['correct_value'], field['correct_type'] = correct, corrects[0][0]
    difficulty = q.get('difficulty')
    if difficulty:
        q['difficulty'] = {'E': 'easy', 'M': 'moderate', 'H': 'hard'}.get(difficulty, difficulty)
        if q['difficulty'] not in ('easy', 'moderate', 'hard'):
            raise UnsupportedContent('Question difficulty is not a source E/M/H category')
    return q
