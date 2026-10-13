"""Independent checks for mixed hard practice and its answer-cue regression.

The five counterfactual cases deliberately share one displayed option bank.
They establish that every alternative can be correct without a prompt, field,
or option-shape change; sampling checks establish that the public default uses
that mixed practice rather than the source-only identity profiles.
"""
from __future__ import annotations

import collections
import re

import sympy as sp
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


PROFILE = 'authored:hard_mixed'
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def _arithmetic(text, symbols=None):
    text = text.replace(r'\left', '').replace(r'\right', '')
    text = text.replace(r'\cdot', '*').replace(r'\big', '').replace(r'\,', '')
    while r'\frac' in text:
        text, replacements = re.subn(
            r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', text)
        assert replacements, ('Unsupported displayed fraction', text)
    text = text.replace('{', '(').replace('}', ')').replace('^', '**')
    assert '\\' not in text, ('Unsupported displayed arithmetic', text)
    return parse_expr(text, local_dict=symbols or {}, transformations=TRANSFORMS)


def _matrix_from_prompt(prompt):
    match = re.search(
        r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]'
        r'|\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', prompt, re.S)
    assert match, 'The learner prompt must contain the matrix'
    inner = match.group(1) if match.group(1) is not None else match.group(2)
    symbol_names = set(re.findall(r'[a-zA-Z]', inner))
    assert len(symbol_names) == 1, ('Expected one matrix parameter', symbol_names)
    variable = sp.Symbol(next(iter(symbol_names)), real=True)
    rows = [[_arithmetic(cell, {str(variable): variable})
             for cell in row.split('&')]
            for row in inner.split(r'\\')]
    assert len(rows) == 3 and all(len(row) == 3 for row in rows)
    return sp.Matrix(rows), variable, prompt[:match.start()] + '{matrix}' + prompt[match.end():]


def _key(values):
    if values is None:
        return 'all-real'
    return tuple(sorted(sp.srepr(sp.simplify(value)) for value in values))


def _choice_values(answer):
    assert answer[':answer/type'] == ':answer.type/text'
    raw = answer[':answer/value']
    if re.match(r'^(?:All|Any)\b', raw):
        return None
    fragments = re.findall(r'\$([^$]+)\$', raw)
    assert fragments and all('=' not in fragment for fragment in fragments), raw
    return [_arithmetic(fragment) for fragment in fragments]


def _check_expansion(record, matrix, variable, determinant):
    """Read every displayed first-block cofactor equality independently."""
    solution = record['question'][':question/worked-solution']
    first = re.search(r'\$\$(.*?)\$\$', solution, re.S)
    assert first, 'Missing worked cofactor expansion'
    text = first.group(1).strip()
    text = text.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    local = {str(variable): variable}

    def determinant_text(match):
        rows = [[_arithmetic(cell, local) for cell in row.split('&')]
                for row in match.group(1).split(r'\\')]
        return '(' + str(sp.Matrix(rows).det()) + ')'

    text = re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',
                  determinant_text, text, flags=re.S)
    count = 0
    for line in text.split(r'\\'):
        _, rhs = line.split(' & =', 1)
        assert sp.expand(_arithmetic(rhs, local) - determinant) == 0, rhs
        count += 1
    steps = record['generation']['solution_intermediates']
    assert len(steps) == 3
    for column, step in enumerate(steps):
        minor = sp.Matrix([[sp.sympify(value) for value in row]
                           for row in step['minor']])
        assert minor == matrix.minor_submatrix(0, column)
        coefficient = sp.sympify(step['coefficient'])
        assert coefficient == matrix[0, column]
        assert sp.expand(sp.sympify(step['value']) - minor.det()) == 0
        assert sp.expand(sp.sympify(step['signed_product']) -
                         (-1) ** column * coefficient * minor.det()) == 0
    return count


def _check_solving(record, variable, expected):
    """Every displayed solving equation must retain the complete root set."""
    solution = record['question'][':question/worked-solution']
    blocks = re.findall(r'\$\$(.*?)\$\$', solution, re.S)
    if expected is None:
        assert len(blocks) == 1
        assert 'singular for all values of $' + str(variable) + '.$' in solution
        return 0
    assert len(blocks) == 2
    assert 'for all values' not in solution
    text = blocks[1].strip()
    text = text.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    local = {str(variable): variable}
    count = 0
    for line in text.split(r'\\'):
        lhs, rhs = line.split(' & =', 1)
        left = _arithmetic(lhs, local)
        rhs = rhs.replace(r'\,', '')
        if ',' in rhs:
            assert left == variable, line
            values = [_arithmetic(value, local) for value in rhs.split(',')]
            assert len(values) == len({_key([value]) for value in values}), line
        else:
            residual = sp.expand(left - _arithmetic(rhs, local))
            assert residual != 0, line
            values = sp.solve(residual, variable)
        assert _key(values) == _key(expected), line
        count += 1
    assert count >= 2
    conclusion = solution.split('Therefore,')[-1]
    assignments = re.findall(r'\$' + re.escape(str(variable)) + r'=([^$]+)\$', conclusion)
    assert len(assignments) == len(expected), conclusion
    values = [_arithmetic(value.rstrip('.'), local) for value in assignments]
    assert _key(values) == _key(expected), conclusion
    return count


def check_record(g, record):
    """Validate learner-visible mathematics without the generator's solvers."""
    question, meta = record['question'], record['generation']
    assert meta['matrix_recipe'] == PROFILE
    assert meta['bank_profile'] == PROFILE
    assert meta['template'] == 'mixed_singular_radio'
    assert question[':question/difficulty'] == ':question.difficulty/hard'
    matrix, variable, prompt_shell = _matrix_from_prompt(question[':question/problem'])
    a, b, c, d, e, f, h, i, j = list(matrix)
    determinant = sp.expand(a * (e * j - f * i) - b * (d * j - f * h) +
                            c * (d * i - e * h))
    polynomial = sp.Poly(determinant, variable)
    assert meta['parameters']['target'] == 0
    expected = None if polynomial.is_zero else sorted(
        sp.solve(polynomial.as_expr(), variable), key=float)
    assert polynomial.is_zero or polynomial.degree() in (1, 2)
    assert expected is None or len(expected) in (1, 2)
    assert expected is None or all(root.is_real is True for root in expected)
    roots = None if meta['roots'] is None else [sp.sympify(root) for root in meta['roots']]
    assert _key(expected) == _key(roots)
    stored_matrix = sp.Matrix([[sp.sympify(value) for value in row] for row in meta['matrix']])
    stored_symbols = stored_matrix.free_symbols
    assert len(stored_symbols) == 1
    internal = next(iter(stored_symbols))
    assert stored_matrix.subs(internal, variable) == matrix
    assert sp.expand(sp.sympify(meta['determinant']).subs(internal, variable) - determinant) == 0
    assert sp.expand(sp.sympify(meta['residual']).subs(internal, variable) - determinant) == 0
    params = meta['parameters']
    rebuilt = sp.Matrix(3, 3, [constant + linear * variable + quadratic * variable ** 2
                              for constant, linear, quadratic in
                              zip(params['constants'], params['linear'], params['quadratic'])])
    assert rebuilt == matrix
    fields = question[':question/answer-fields']
    assert len(fields) == 1
    field = fields[0]
    assert field[':answer-field/type'] == ':answer-field.type/radio'
    choices = field[':answer-field/choices']
    assert len(choices) == 5
    assert len({answer[':answer/id'] for answer in choices}) == 5
    values = [_choice_values(answer) for answer in choices]
    assert len({_key(value) for value in values}) == 5
    assert sorted(0 if value is None else len(value) for value in values) == [0, 1, 1, 2, 2]
    anchors = [sp.Integer(value) for value in params['option_roots']]
    assert len(anchors) == 2 and all(anchors) and anchors[0] != anchors[1]
    assert sum(anchors) != 0
    expected_bank = [None, [anchors[0]], [anchors[1]], anchors, [-value for value in anchors]]
    assert {_key(value) for value in values} == {_key(value) for value in expected_bank}
    good = [answer[':answer/id'] for answer, value in zip(choices, values)
            if _key(value) == _key(expected)]
    assert good == [field[':answer-field/correct'][1]]
    for answer, value in zip(choices, values):
        stored = next(item for item in meta['choice_math']
                      if item['value'] == answer[':answer/value'])
        assert _key(value) == _key(None if stored['set'] is None else
                                  [sp.sympify(item) for item in stored['set']])
    rows = _check_expansion(record, matrix, variable, determinant)
    solving_rows = _check_solving(record, variable, expected)
    correct_slot = next(index for index, values in enumerate(expected_bank)
                        if _key(values) == _key(expected))
    return {'outcome': 'all-real' if expected is None else str(len(expected)) + '-root',
            'correct_slot': correct_slot, 'prompt_shell': prompt_shell,
            'field_key': field[':answer-field/key'], 'expansion_rows': rows,
            'solving_rows': solving_rows,
            'bank': sorted(answer[':answer/value'] for answer in choices)}


def validate(g):
    """Return a report and representative records for the native grader."""
    outcomes, slots = collections.Counter(), collections.Counter()
    signatures, fingerprints, seen_outcomes, records = set(), set(), set(), []
    expansion_rows = solving_rows = identity_checks = 0
    for seed in range(80):
        record = g.generate('hard', seed=seed)
        checked = check_record(g, record)
        outcomes[checked['outcome']] += 1
        slots[checked['correct_slot']] += 1
        signatures.add((checked['prompt_shell'], checked['field_key']))
        fingerprints.add(record['generation']['parameter_fingerprint'])
        expansion_rows += checked['expansion_rows']
        solving_rows += checked['solving_rows']
        if checked['correct_slot'] not in seen_outcomes:
            records.append(('mixed-hard:sample:' + str(seed), record))
            seen_outcomes.add(checked['correct_slot'])
        if seed < 10:
            replay = g.generate('hard', seed=seed + 1000,
                                parameters=record['generation']['parameters'])
            check_record(g, replay)
            assert replay['question'][':question/id'] == record['question'][':question/id']
            for key in ('parameter_fingerprint', 'content_fingerprint'):
                assert replay['generation'][key] == record['generation'][key]
            old = record['question'][':question/answer-fields'][0]
            new = replay['question'][':question/answer-fields'][0]
            assert old[':answer-field/id'] == new[':answer-field/id']
            assert old[':answer-field/correct'] == new[':answer-field/correct']
            assert set(answer[':answer/id'] for answer in old[':answer-field/choices']) == set(
                answer[':answer/id'] for answer in new[':answer-field/choices'])
            identity_checks += 1
    assert set(outcomes) == {'all-real', '1-root', '2-root'}
    assert set(slots) == set(range(5))
    assert len(signatures) == 1, 'Outcome is leaking through prompt or field structure'
    assert len(fingerprints) >= 60

    # A single visible bank can have any of its five alternatives correct.
    x = sp.Symbol('u', real=True)
    transform = sp.Matrix([[1, 1, 1], [1, 0, 1], [1, 1, 0]])
    cases = [(x - 1, 0), (x - 1, 1), (x - 2, 1), (x - 1, x - 2), (x + 1, x + 2)]
    banks, ids = set(), set()
    counterfactual_slots = []
    for number, (first, second) in enumerate(cases):
        matrix = sp.expand(transform * sp.Matrix([[first, 1, 0], [0, second, 0], [0, 0, 1]]) * transform)
        parameters = {'constants': [int(sp.expand(value).coeff(x, 0)) for value in matrix],
                      'linear': [int(sp.expand(value).coeff(x, 1)) for value in matrix],
                      'quadratic': [0] * 9, 'target': 0, 'option_roots': [1, 2]}
        record = g.generate('hard', seed=500, profile=PROFILE, parameters=parameters)
        checked = check_record(g, record)
        banks.add(tuple(checked['bank']))
        ids.add(record['question'][':question/id'])
        counterfactual_slots.append(checked['correct_slot'])
        signatures.add((checked['prompt_shell'], checked['field_key']))
        expansion_rows += checked['expansion_rows']
        solving_rows += checked['solving_rows']
        records.append(('mixed-hard:fixed-bank:' + str(number), record))
    assert len(banks) == 1 and len(ids) == 5
    assert set(counterfactual_slots) == set(range(5)) and len(signatures) == 1
    return ({'status': 'pass', 'default_samples': 80, 'outcomes': dict(outcomes),
             'correct_bank_slots': dict(slots), 'distinct_parameters': len(fingerprints),
             'same_parameter_identity_checks': identity_checks,
             'fixed_bank_counterfactual_cases': 5, 'displayed_expansion_rows': expansion_rows,
             'displayed_solving_rows': solving_rows,
             'shared_prompt_and_field_shape': True,
             'every_answer_position_can_be_correct_with_same_bank': True}, records)
