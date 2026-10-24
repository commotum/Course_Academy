#!/usr/bin/env python3
"""Retained tangent findings, tested against current CLI and shared delivery.

Uses only the standard library. Copy this file and tangent-regression-fixtures/
to the pipeline workspace. Defaults resolve there; overrides support isolation.
Historical counterexamples remain negative controls. Family knowledge combined
with bounds is reported explicitly as an unavoidable finite-family limitation.
"""
import argparse
import ast
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def add(x, y): return (x[0] + y[0], x[1] + y[1])
def neg(x): return (-x[0], -x[1])
def mul(x, y): return (x[0]*y[0] + 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def divide(x, y):
    norm = y[0]*y[0] - 3*y[1]*y[1]
    assert norm, 'Zero denominator'
    return mul(x, (y[0]/norm, -y[1]/norm))


def sign(x):
    """Exact sign of a+b*sqrt(3), including rational-square comparisons."""
    a, b = x
    if not a: return (b > 0) - (b < 0)
    if not b or (a > 0) == (b > 0): return (a > 0) - (a < 0)
    gap = a*a - 3*b*b
    return ((a > 0) - (a < 0)) * ((gap > 0) - (gap < 0))


def interval(x):
    positive = sign(x) > 0
    absolute = x if positive else neg(x)
    return positive, sign(add(absolute, (F(-1), F(0)))) < 0


def normalize(tex):
    tex = tex.replace('π', r'\pi').replace(r'\dfrac', r'\frac')
    for token in [r'\left', r'\right', r'\displaystyle', r'\,', r'\!']:
        tex = tex.replace(token, '')
    tex = re.sub(r'\\sqrt\s*\{3\}', 'r', tex)
    def group(start):
        assert tex[start] == '{'
        level, end = 1, start + 1
        while level:
            level += (tex[end] == '{') - (tex[end] == '}')
            end += 1
        return tex[start+1:end-1], end
    while r'\frac' in tex:
        start = tex.index(r'\frac')
        top, middle = group(start+5)
        bottom, end = group(middle)
        tex = tex[:start] + '(' + normalize(top) + ')/(' + normalize(bottom) + ')' + tex[end:]
    tex = tex.replace(r'\pi', 'r').replace(r'\cdot', '*').replace('{', '(').replace('}', ')')
    tex = re.sub(r'\s+', '', tex)
    assert re.fullmatch(r'[0-9r()+*/.\-]+', tex), tex
    return re.sub(r'(?<=[0-9r)])(?=[r(])|(?<=[r)])(?=[0-9])', '*', tex)


@lru_cache(None)
def value(tex):
    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, int): return F(node.value), F(0)
        if isinstance(node, ast.Name) and node.id == 'r': return F(0), F(1)
        if isinstance(node, ast.UnaryOp):
            answer = evaluate(node.operand)
            if isinstance(node.op, ast.USub): return neg(answer)
            if isinstance(node.op, ast.UAdd): return answer
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add): return add(left, right)
            if isinstance(node.op, ast.Sub): return add(left, neg(right))
            if isinstance(node.op, ast.Mult): return mul(left, right)
            if isinstance(node.op, ast.Div): return divide(left, right)
        raise AssertionError(ast.dump(node))
    return evaluate(ast.parse(normalize(tex), mode='eval').body)


FAMILY = {(F(a), F(b)) for a in [-2, 2] for b in [-1, 1]}
EXPECTED = {15: (F(2), F(-1)), 75: (F(2), F(1)),
            105: (F(-2), F(-1)), 165: (F(-2), F(1))}


def target(problem):
    first = re.search(r'\$(.*?)\$', problem, re.S)[1]
    first = first.replace(r'\tan', '').replace(r'\left', '').replace(r'\right', '').strip()
    if r'\circ' in first or '∘' in first or '◦' in first:
        return int(re.search(r'\d+', first)[0])
    radians = value(first)
    assert radians[0] == 0 and (radians[1]*180).denominator == 1
    return int(radians[1]*180)


def bank_case(problem, choices, key):
    degrees = target(problem)
    expected = EXPECTED[degrees % 180]
    vals = [value(choice) for choice in choices]
    assert len(vals) == len(set(vals)) == 5
    assert vals.count(expected) == 1 and value(key) == expected
    bucket = interval(expected)
    bounded = [c for c, v in zip(choices, vals) if interval(v) == bucket]
    return {'target_degrees': degrees, 'interval_candidates': len(bounded),
            'fraction_free_interval_candidates': sum(r'\frac' not in c and r'\dfrac' not in c for c in bounded),
            'family_shape_candidates': sum(v in FAMILY for v in vals),
            'family_and_bounds_candidates': sum(v in FAMILY and interval(v) == bucket for v in vals)}


def inspect(records):
    cases, groups = [], defaultdict(list)
    for record in records:
        question = record['question']
        field = question[':question/answer-fields'][0]
        choices = field[':answer-field/choices']
        key = next(c[':answer/value'] for c in choices if c[':answer/id'] == field[':answer-field/correct'][1])
        case = bank_case(question[':question/problem'], [c[':answer/value'] for c in choices], key)
        cases.append(case)
        prompt = question[':question/problem']
        unit = 'degrees' if r'\circ' in prompt else 'radians'
        operation = '+' if '+' in prompt.split('Use the fact that')[1] else '-'
        for name in ['all', 'unit:'+unit, 'operation:'+operation, 'operation-unit:'+operation+'/'+unit]:
            groups[name].append(case)
    def counts(rows):
        return {'count': len(rows), 'unique_interval': sum(r['interval_candidates'] == 1 for r in rows),
                'unique_fraction_free_interval': sum(r['fraction_free_interval_candidates'] == 1 for r in rows),
                'unique_family_shape': sum(r['family_shape_candidates'] == 1 for r in rows),
                'family_and_bounds_unique': sum(r['family_and_bounds_candidates'] == 1 for r in rows)}
    return {**counts(cases), 'cases': cases, 'groups': {name: counts(rows) for name, rows in groups.items()}}


def assert_repaired(report):
    for case in report['cases']:
        assert case['interval_candidates'] >= 2, case
        assert case['fraction_free_interval_candidates'] >= 2, case
        assert case['family_shape_candidates'] >= 2, case
        # Report this remaining strategy honestly; it is not a repaired failure.
        assert case['family_and_bounds_candidates'] == 1, case


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=here)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--inventory', type=Path)
    parser.add_argument('--fixtures', type=Path, default=here/'tangent-regression-fixtures')
    parser.add_argument('--output', type=Path, default=here/'evidence/tangent-regression/current')
    parser.add_argument('--math-root', type=Path, default=Path('/media/jake/SSD/EDB/math'))
    args = parser.parse_args()
    package = args.package.resolve()
    source = (args.source or package.parent/'source/source.json').resolve()
    inventory = (args.inventory or package.parent/'source/inventory.json').resolve()
    repo = next(p for p in [package, *package.parents] if (p/'generate/pipeline/check_delivery.py').is_file())
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    fixtures = args.fixtures.resolve()
    historical = {str(i): inspect(json.loads((fixtures/f'review-{i}-batch.json').read_text())) for i in [1, 2]}
    assert historical['1']['unique_interval'] > 0, 'Lost the original interval counterexample'
    assert historical['2']['unique_family_shape'] > 0, 'Lost the original shape counterexample'
    proof = [bank_case(s['original_prompt'], s['bank'], s['key']) for s in json.loads((fixtures/'source-banks.json').read_text())]
    assert len({interval(v) for v in FAMILY}) == 4
    assert all(r['family_and_bounds_candidates'] == 1 for r in proof)
    result = {'historical_negative_controls': historical, 'source_bank_proof': proof,
              'criterion_classification': {
                  '0c0b5701fdc1e1f51385': 'Fixable: bounds or fraction-free bounds uniquely identify an option.',
                  '5177439f65fd0aa4269e': 'Fixable: prompt-blind unique canonical shape. Combined learned-family plus bounds is a finite-family limitation, also present in original source banks.'},
              'limitation': 'A learner who knows the four exact identities can combine that knowledge with quadrant/magnitude. Final-answer choice cannot require formula execution.',
              'sets': {}}
    for name, count, seed in [('requested', 5, 3750266970), ('fresh', 8, 73), ('catalog', 128, 42)]:
        assets = output/(name+'-assets'); assets.mkdir(exist_ok=True)
        command = [sys.executable, str(package/'generator.py'), '--difficulty', 'moderate', '--count', str(count), '--seed', str(seed), '--format', 'json']
        generated = subprocess.run(command, cwd=package, env={**os.environ, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(assets)}, capture_output=True, text=True, check=True)
        batch = output/(name+'.json'); batch.write_text(generated.stdout)
        records = json.loads(generated.stdout); assert len(records) == count
        before = inspect(records); assert_repaired(before)
        delivery = output/(name+'-delivery')
        filter_command = [sys.executable, str(repo/'generate/pipeline/check_delivery.py'), '--input', str(batch), '--source', str(source), '--inventory', str(inventory), '--difficulty', 'moderate', '--output', str(delivery), '--asset-root', str(assets), '--math-root', str(args.math_root)]
        filtered = subprocess.run(filter_command, cwd=package, capture_output=True, text=True, check=True)
        (output/(name+'-delivery.log')).write_text(filtered.stdout+filtered.stderr)
        accepted = json.loads((delivery/'accepted.json').read_text())
        assert len(accepted) == count, 'Delivery shortage: do not silently discard witnesses'
        after = inspect(accepted); assert_repaired(after)
        result['sets'][name] = {'command': command, 'filter_command': filter_command, 'batch_sha256': hashlib.sha256(batch.read_bytes()).hexdigest(), 'generated': before, 'delivered': after}
    result['passed'] = True
    (output/'regression.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': True, 'report': str(output/'regression.json'), 'sets': {name: {k: report['delivered'][k] for k in ['count', 'unique_interval', 'unique_family_shape', 'family_and_bounds_unique']} for name, report in result['sets'].items()}, 'limitation': result['limitation']}))


if __name__ == '__main__':
    main()
