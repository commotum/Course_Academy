#!/usr/bin/env python3
"""Check displayed systems and every substitution stage with independent exact algebra."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application, parse_expr, standard_transformations,
)

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPAIR = HERE.parents[1]
REPO = next(p for p in HERE.parents if (p / 'Cargo.toml').exists())
PACKAGE = REPAIR / 'generators/17592186198348'
OLD_PACKAGE = Path('/media/jake/SSD/EDB/math/generators/f0/f068c2423967f97d1baa28d1ec02a9decc55f5123725a48764351717ddd17852')
sys.path.insert(0, str(PACKAGE))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


g = load('new_classification', PACKAGE / 'generator.py')
old = load('old_classification', OLD_PACKAGE / 'generator.py')
X, Y = sp.symbols('x y')
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def expression(raw):
    raw = raw.replace(' ', '').replace(r'\left', '').replace(r'\right', '')
    while r'\frac' in raw:
        after = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', raw)
        assert after != raw, raw
        raw = after
    assert '\\' not in raw, raw
    return sp.expand(parse_expr(raw, local_dict={'x': X, 'y': Y}, transformations=TRANSFORMS))


def residual(raw):
    left, right = raw.replace('&', '').split('=')
    return expression(left) - expression(right)


def rows(text):
    return [block.split(r'\\') for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', text, re.S)]


def line_key(expr):
    coeffs = (expr.coeff(X), expr.coeff(Y), expr.subs({X: 0, Y: 0}))
    first = next(v for v in coeffs if v)
    return tuple(sp.cancel(v / first) for v in coeffs)


def y_solutions(expr):
    assert not expr.has(X)
    coefficient, constant = expr.coeff(Y), expr.subs(Y, 0)
    assert sp.expand(expr - coefficient * Y - constant) == 0
    if coefficient:
        return ('one', sp.cancel(-constant / coefficient))
    return ('all',) if constant == 0 else ('none',)


def check(record):
    q = record['question']
    a, b, c, d, e, f = record['generation']['parameters'].values()
    given = rows(q[':question/problem'])
    assert len(given) == 1 and len(given[0]) == 2
    assert given[0][0].strip() != given[0][1].strip()
    assert [residual(s) for s in given[0]] == [a*X+b*Y-c, d*X+e*Y-f]
    determinant = a*e-b*d
    label = ('consistent independent' if determinant else
             'consistent dependent' if a*f == d*c else 'inconsistent')
    field, = q[':question/answer-fields']
    choices = field[':answer-field/choices']
    assert field[':answer-field/type'] == ':answer-field.type/select'
    assert set(v[':answer/value'] for v in choices) == {
        'inconsistent', 'consistent independent', 'consistent dependent'}
    assert len({v[':answer/id'] for v in choices}) == len(choices) == 3
    assert next(v[':answer/value'] for v in choices if v[':answer/id'] == field[':answer-field/correct'][1]) == label
    assert q[':question/difficulty'] == ':question.difficulty/moderate'
    assert record['generation']['difficulty'] == 'moderate'
    worked = rows(q[':question/worked-solution'])
    assert len(worked) == 3
    for row in worked[0]:
        assert line_key(residual(row)) == line_key(a*X+b*Y-c)
    assert len(worked[1]) == 1
    assert residual(worked[1][0]) == X-sp.Rational(c,a)+sp.Rational(b,a)*Y
    assert residual(worked[2][0]) == d*X+e*Y-f
    target = y_solutions((d*X+e*Y-f).subs(X, sp.Rational(c,a)-sp.Rational(b,a)*Y).expand())
    for row in worked[2][1:]:
        assert y_solutions(residual(row)) == target
    assert q[':question/worked-solution'].endswith(f'the system is {label}.')
    return label


def native_fixture(record, name, field_type='select'):
    record = copy.deepcopy(record)
    field = record['question'][':question/answer-fields'][0]
    field[':answer-field/type'] = ':answer-field.type/' + field_type
    return {'label': name + '/' + field_type, 'record': record, 'checks': [
        {'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if a[':answer/id'] == field[':answer-field/correct'][1] else 'rejected',
         'purpose': 'Every classification choice'} for a in field[':answer-field/choices']]}


def main():
    records = []
    for seed in range(12):
        batch = g.batch('moderate', 18, seed)
        assert batch == g.batch('moderate', 18, seed)
        assert {r['generation']['template'] for r in batch} == {'standard', 'rearranged', 'canonical'}
        assert {check(r) for r in batch} == set(g.LABELS)
        records.extend(batch)
    explicit_accepted, explicit_rejected = 0, 0
    for a, b, c in ((6,-6,0), (6,6,6), (-6,-6,-6)):
        for multiplier in g.MULTIPLIERS:
            params = (a,b,c,int(multiplier*a),int(multiplier*b),int(multiplier*c))
            for layout in ('standard', 'rearranged', 'canonical'):
                old_record = old.generate(params, layout)
                old_rows = rows(old_record['question'][':question/problem'])[0]
                duplicate = old_rows[0].strip() == old_rows[1].strip()
                try:
                    record = g.generate(params, layout)
                except ValueError as error:
                    assert duplicate and str(error) == 'The two displayed equations must be distinct'
                    explicit_rejected += 1
                else:
                    assert not duplicate
                    assert record['question'] == old_record['question']
                    check(record)
                    records.append(record)
                    explicit_accepted += 1
    assert explicit_rejected == 4  # All three standard duplicates, plus canonical when c=0.
    for layout in ('standard', 'rearranged', 'canonical'):
        for label in g.LABELS:
            for seed in range(20):
                params = g.sample(random.Random(seed), label, layout)
                record = g.generate(params, layout)
                assert check(record) == label
    for before, after in zip(old.replay(), g.replay()):
        assert before['question'] == after['question']
        check(after)
        records.append(after)
    old_target = old.generate((-2,-3,-9,-2,-3,-9), 'standard')
    new_target = g.generate((-2,-3,-9,-4,-6,-18), 'standard')
    check(new_target)
    records.append(new_target)
    keys = (':question/problem', ':question/worked-solution')
    replacement = {
        'question_db_id': 17592186567832,
        'old': {k: old_target['question'][k] for k in keys},
        'new': {k: new_target['question'][k] for k in keys},
        'old_parameters': [-2,-3,-9,-2,-3,-9],
        'new_parameters': [-2,-3,-9,-4,-6,-18],
        'classification': 'consistent dependent',
        'reason': 'Multiply the second equation by 2 so the displayed equations are distinct while defining the same line.',
    }
    (HERE / 'replacement.json').write_text(json.dumps(replacement, indent=2)+'\n')
    native = [native_fixture(r, f'record-{i}') for i, r in enumerate(records)]
    native += [native_fixture(new_target, 'target-preserved-radio-bank', 'radio')]
    (HERE / 'native-input.json').write_text(json.dumps(native)+'\n')
    harness = REPO / 'generate/scratch/17592186073778/check-engine'
    subprocess.run([str(harness), str(HERE/'native-input.json'), str(HERE/'native-report.json')], check=True)
    native_report = json.loads((HERE / 'native-report.json').read_text())
    cli = subprocess.run([sys.executable, '-B', str(PACKAGE/'generator.py'), '--difficulty', 'moderate', '--count', '18', '--seed', '33', '--format', 'json'], check=True, capture_output=True, text=True)
    cli_records = json.loads(cli.stdout)
    assert cli_records == g.batch('moderate', 18, 33)
    for record in cli_records:
        check(record)
    assert g.batch('unclassified', 18, 33) == cli_records
    for difficulty in ('easy', 'hard'):
        try:
            g.batch(difficulty, 1, 0)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported difficulty accepted')
    assert (PACKAGE/'math_format.py').read_bytes() == (OLD_PACKAGE/'math_format.py').read_bytes()
    verification = {
        'status': 'passed', 'knowledge_point_db_id': g.KP_ID,
        'generator_version': g.VERSION,
        'generator_sha256': hashlib.sha256((PACKAGE/'generator.py').read_bytes()).hexdigest(),
        'helper_sha256': hashlib.sha256((PACKAGE/'math_format.py').read_bytes()).hexdigest(),
        'helper_unchanged': True,
        'batch_records': 216, 'sampler_records': 180,
        'explicit_nonduplicate_records': explicit_accepted,
        'explicit_duplicate_cases_rejected': explicit_rejected,
        'original_replays_unchanged': 2, 'replacement_records': 1,
        'cli_records': len(cli_records), 'all_displayed_substitution_steps_verified': True,
        'all_three_classifications_and_layouts_preserved': True,
        'moderate_only_scope_preserved': True,
        'negative_and_reciprocal_multipliers_and_zero_constants_tested': True,
        'native_grading': {k: native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
        'native_harness': str(harness.relative_to(REPO)),
        'native_harness_sha256': hashlib.sha256(harness.read_bytes()).hexdigest(),
    }
    (HERE/'verification.json').write_text(json.dumps(verification, indent=2)+'\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
