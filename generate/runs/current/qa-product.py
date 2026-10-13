"""Parent checks using displayed inputs and immutable banks, not generator answers."""
import importlib.util
import json
from pathlib import Path
import sympy as sp

R = Path(__file__).resolve().parent
REPO = R.parents[2]
F = REPO / 'generate/scratch/17592186115393'
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
g = module('parent_product_generator', F.with_suffix('.py'))
v = module('parent_product_parser', F / 'validate.py')

def equal(a, b):
    if isinstance(a, sp.MatrixBase) or isinstance(b, sp.MatrixBase):
        return isinstance(a, sp.MatrixBase) and isinstance(b, sp.MatrixBase) and a.shape == b.shape and all(sp.simplify(x-y) == 0 for x, y in zip(a, b))
    return sp.simplify(a-b) == 0

def cross(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

def expected_from_prompt(rec):
    name = rec['generation']['template']
    level = rec['question'][':question/difficulty'].split('/')[-1]
    values = v.prompt_values(rec['question'][':question/problem'], name)
    t = g.t
    if level == 'easy':
        return (values[0]*values[1]).diff(t)
    if level == 'moderate':
        f = values[0]
        other = values[1] if len(values) == 2 else f.diff(t)
        result = sp.diff(sum(a*b for a, b in zip(f, other)), t)
        if name == 'dot_self_evaluate':
            result = result.subs(t, rec['generation']['parameters']['x'])
        return result
    f = values[0]
    return cross(f, values[1]).diff(t) if len(values) == 2 else cross(f.diff(t), f).diff(t)

def check(rec):
    expected = expected_from_prompt(rec)
    field = rec['question'][':question/answer-fields'][0]
    for answer in field[':answer-field/choices']:
        assert equal(expected, v.display_value(answer[':answer/value'])) == (answer[':answer/id'] == field[':answer-field/correct'][1])

source = json.loads((R/'sources/17592186115393.json').read_text())['record']
qs = {q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
cases = json.loads((F/'source-cases.json').read_text())
counts = {'source_questions':0, 'source_values':0, 'source_designations':0, 'default_displayed_products':0}
for case in cases:
    s = qs[case['source_id']]
    r = g.generate(g.TEMPLATES[case['template']][0], 27, case['template'], parameters=case['parameters'], profile=case['bank_profile'])
    check(r)
    assert v.prose(s[':question/worked-solution']) == v.prose(r['question'][':question/worked-solution'])
    for index, field in enumerate(s[':question/answer-fields']):
        p = 'cross_matrix_legacy' if case['template']=='cross_matrix' and index==0 else case['bank_profile']
        r = g.generate(g.TEMPLATES[case['template']][0], 27, case['template'], parameters=case['parameters'], profile=p)
        check(r)
        f = r['question'][':question/answer-fields'][0]
        unmatched = [v.display_value(a[':answer/value']) for a in f[':answer-field/choices']]
        for answer in field[':answer-field/choices']:
            val = v.display_value(answer[':answer/value'])
            matches = [i for i, x in enumerate(unmatched) if equal(val, x)]
            assert len(matches) == 1
            unmatched.pop(matches[0]);counts['source_values'] += 1
        assert not unmatched
        if ':answer-field/correct' in field:
            designated = next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert equal(v.display_value(designated[':answer/value']),v.display_value(field[':answer-field/correct'][':answer/value']))
            counts['source_designations'] += 1
    counts['source_questions'] += 1
for level in ('easy', 'moderate', 'hard'):
    for seed in range(30):
        check(g.generate(level, seed));counts['default_displayed_products'] += 1
(R/'qa/17592186115393-independent.json').write_text(json.dumps(counts, indent=2)+'\n')
print(json.dumps(counts))
