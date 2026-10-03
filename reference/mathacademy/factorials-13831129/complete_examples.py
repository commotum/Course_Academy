#!/usr/bin/env python3
"""Author the requested missing Factorials difficulty and example fields."""
import json
import math
import sys
from pathlib import Path

from build_pilot import edn_uuid, identity, quote
from verify_pilot import facts_hash, read_edn

ROOT = Path(__file__).resolve().parent
RATINGS = {
    'e-5667': ('moderate', 'Product of two factorials, matching observed moderate q-73002 and q-122033.'),
    'e-9519': ('easy', 'A single factorial divided by 0! = 1; comparable to easy zero-factorial practice.'),
    'e-5668': ('easy', 'Cancel the common factorial and multiply three factors, matching easy q-5371 and q-73014.'),
    'q-5370': ('easy', 'Single 5! calculation, between the observed easy 4!, 8!, and 11! questions.'),
    'q-124137': ('easy', '3! + 0! has the same structure as observed easy q-124403, with smaller numbers.'),
    'q-124138': ('easy', '2!/0! uses 0! = 1 and one small factorial, comparable to the easy zero-factorial questions.'),
    'q-19838': ('moderate', 'Two factorial ratios require more cancellation and multiplication than the observed easy single-ratio questions.'),
}
EXAMPLES = {
    'e-5667': {'correct': str(math.factorial(5) * math.factorial(2)),
               'distractors': [('122', 'Add 5! and 2! instead of multiplying.'),
                              ('120', 'Omit the factor 2!.'),
                              ('5040', 'Compute (5 + 2)! instead of 5! times 2!.'),
                              ('10', 'Multiply 5 and 2, ignoring the factorial signs.')]},
    'e-9519': {'correct': str(math.factorial(5) // math.factorial(0)),
               'distractors': [('0', 'Treat the zero in the denominator as making the result zero.'),
                              ('119', 'Subtract 0! = 1 instead of dividing by it.'),
                              ('121', 'Add 0! = 1 instead of dividing by it.'),
                              ('Undefined', 'Use 0! = 0 and conclude division by zero.')]},
    'e-5668': {'correct': str(math.factorial(5) // math.factorial(2)),
               'distractors': [('120', 'Ignore the denominator.'),
                              ('20', 'Keep only 5 times 4 after cancellation, omitting 3.'),
                              ('6', 'Compute (5 - 2)! instead of the quotient.'),
                              ('10', 'Multiply 5 and 2 instead of evaluating the quotient of factorials.')]},
}


def question_map(topic):
    return {q[':question/math-academy-id']: q
            for kp in topic[':topic/knowledge-points']
            for q in [kp[':knowledge-point/canonical-example'], *kp[':knowledge-point/questions']]}


def canonical(value):
    if isinstance(value, dict):
        return {k: canonical(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def build(local):
    before = question_map(read_edn(local / 'content-before.edn')[0][0])
    forms, notes = [], []
    for key, (difficulty, reason) in RATINGS.items():
        assert ':question/difficulty' not in before[key], key
        attrs = [':db/id [:question/math-academy-id ' + quote(key) + ']',
                 ':question/difficulty :question.difficulty/' + difficulty]
        if key in EXAMPLES:
            assert before[key][':question/is-example'] is True
            assert not before[key].get(':question/answer-fields')
            spec = EXAMPLES[key]
            values = [spec['correct'], *[v for v, _ in spec['distractors']]]
            assert len(values) == len(set(values)) == 5
            choices = []
            for i, value in enumerate(values):
                kind = 'text' if value == 'Undefined' else 'math'
                choices.append('{:db/id ' + quote(f'{key}-completion-value-{i}') +
                               ' :answer/id ' + edn_uuid(identity('answer', f'{key}:selection:{value}')) +
                               ' :answer/type :answer.type/' + kind + ' :answer/value ' + quote(value) +
                               ' :db/ensure [:answer/validate]}')
            field = ('{:answer-field/id ' + edn_uuid(identity('field', f'{key}:selection')) +
                     ' :answer-field/key "selection" :answer-field/type :answer-field.type/radio' +
                     ' :answer-field/choices [' + ' '.join(choices) + ']' +
                     ' :answer-field/correct ' + quote(f'{key}-completion-value-0') +
                     ' :db/ensure [:answer-field/validate]}')
            attrs.append(':question/answer-fields [' + field + ']')
        forms.append('{' + ' '.join(attrs) + ' :db/ensure [:question/validate]}')
        notes.append({'math_academy_id': key, 'difficulty': difficulty,
                      'difficulty_provenance': 'authored estimate, not an observed Math Academy rating',
                      'comparison': reason, 'example_field': EXAMPLES.get(key)})
    (ROOT / 'completion-transaction.edn').write_text('[\n' + '\n'.join(forms) + '\n]\n')
    (ROOT / 'completion-review.json').write_text(json.dumps(notes, indent=2) + '\n')
    lines = ['# Factorials difficulty estimates and example answer fields', '',
             'All seven ratings below are authored estimates. Existing observed ratings remain unchanged. '
             'Each canonical example gains a radio field, guided by the radio fields in its KP. '
             'Example distractors are newly authored. Existing practice choices, problems, solutions, '
             'example flags, KP membership, and learner/engine facts remain unchanged.', '',
             '| Question | Difficulty | Comparison |', '|---|---|---|']
    for note in notes:
        lines.append(f"| {note['math_academy_id']} | {note['difficulty']} | {note['comparison']} |")
    for key, spec in EXAMPLES.items():
        lines.extend(['', '## ' + key, '', before[key][':question/problem'], '',
                      '**Correct answer:** ' + spec['correct'], '', '| Distractor | Reason |', '|---|---|'])
        lines.extend(f'| {v} | {reason} |' for v, reason in spec['distractors'])
    (ROOT / 'completion-review.md').write_text('\n'.join(lines) + '\n')
    print('Prepared 7 difficulty estimates, 3 radio fields, and 15 example answer choices.')


def verify(local):
    old_topic = read_edn(local / 'content-before.edn')[0][0]
    new_topic = read_edn(local / 'content-after.edn')[0][0]
    before, after = question_map(old_topic), question_map(new_topic)
    assert set(before) == set(after) and len(after) == 16
    owned = {}
    for key, q in after.items():
        preserved = dict(q)
        if key in RATINGS:
            assert preserved.pop(':question/difficulty') == {':db/ident': ':question.difficulty/' + RATINGS[key][0]}
        if key in EXAMPLES:
            fields = preserved.pop(':question/answer-fields')
            assert len(fields) == 1
            f = fields[0]
            assert f[':answer-field/key'] == 'selection'
            assert f[':answer-field/type'] == {':db/ident': ':answer-field.type/radio'}
            values = {a[':answer/value'] for a in f[':answer-field/choices']}
            expected = {EXAMPLES[key]['correct'], *[v for v, _ in EXAMPLES[key]['distractors']]}
            assert values == expected
            assert f[':answer-field/correct'][':answer/value'] == EXAMPLES[key]['correct']
        assert canonical(preserved) == canonical(before[key]), key
        assert ':question/difficulty' in q
        fields = q[':question/answer-fields']
        assert len(fields) == 1
        for f in fields:
            assert all(k in f for k in (':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct'))
            choices = f[':answer-field/choices']
            assert f[':answer-field/correct'][':db/id'] in {a[':db/id'] for a in choices}
            assert len({(a[':answer/type'][':db/ident'], a[':answer/value']) for a in choices}) == len(choices)
            for a in choices:
                assert all(k in a for k in (':answer/id', ':answer/type', ':answer/value'))
                owner = (key, f[':answer-field/id'])
                assert owned.setdefault(a[':db/id'], owner) == owner
    def relationships(topic):
        return {kp[':knowledge-point/id']: {
            **{k: v for k, v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/canonical-example')},
            'example': kp[':knowledge-point/canonical-example'][':question/id'],
            'practice': sorted(q[':question/id'] for q in kp[':knowledge-point/questions'])}
            for kp in topic[':topic/knowledge-points']}
    assert relationships(old_topic) == relationships(new_topic)
    old_protected = read_edn(local / 'protected-before.edn')
    assert facts_hash(old_protected) == facts_hash(read_edn(local / 'protected-after.edn'))
    report = read_edn(local / 'commit.edn')
    assert report[':edb/committed'] is True
    assert all(row[-1] is True for row in report[':edb/tx-data'])
    result = {'basis_before': report[':edb/db-before-t'], 'basis_after': report[':edb/db-after-t'],
              'estimated_difficulties_added': 7, 'example_fields_added': 3, 'example_choices_added': 15,
              'all_16_questions_have_difficulty_and_complete_answer_fields': True,
              'existing_practice_choices_unchanged': True, 'kp_relationships_unchanged': True,
              'learner_and_engine_facts_unchanged': True, 'protected_facts_count': len(old_protected),
              'protected_facts_sha256': facts_hash(old_protected),
              'practice_questions_still_without_worked_solution': sorted(k for k, q in after.items()
                  if not q[':question/is-example'] and not q.get(':question/worked-solution'))}
    (ROOT / 'completion-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    (build if sys.argv[1] == 'build' else verify)(Path(sys.argv[2]))
