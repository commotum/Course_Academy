"""Check vector task givens, image roles and exact response dependencies offline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from fractions import Fraction as F
from plot import render_plots


def enum(v): return str(v.get(':db/ident') if isinstance(v, dict) else v)
def answer_id(v):
    return str(v[':answer/id'] if isinstance(v, dict) else v[1] if isinstance(v, (list, tuple)) else v)


def fingerprint(q):
    result = {k: q[k] for k in (':question/problem', ':question/requires-calculator') if k in q}
    fields = []
    for f in q[':question/answer-fields']:
        correct = next(a for a in f[':answer-field/choices'] if str(a[':answer/id']) == answer_id(f[':answer-field/correct']))
        row = {':answer-field/key': f[':answer-field/key'], ':answer-field/type': enum(f[':answer-field/type']),
               ':answer-field/correct': {':answer/type': enum(correct[':answer/type']), ':answer/value': correct[':answer/value']}}
        if enum(f[':answer-field/type']) not in (':answer-field.type/blank', ':answer-field.type/free'):
            row[':answer-field/choices'] = sorted([{':answer/type': enum(a[':answer/type']), ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a: json.dumps(a, sort_keys=True))
        fields.append(row)
    result[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def parse(value):
    return F(re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'\1/\2', value))


def check(record, directory):
    q = record['question']; p = record['generation']['parameters']
    prompt = q[':question/problem']; solution = q[':question/worked-solution']
    assert not re.search(r'\\(?:overrightarrow|overset)|O\\to|\bpath\b|\bopposite\b|\breverse\b|\bPC\b|\bOP\b', prompt, re.I), 'Prompt supplies a construction or residual decision'
    assert prompt.startswith('The three vectors share an origin, and each grid square has the same side length.')
    a, b = p['a'], p['b']; k = F(p['k']); r = F(p['r'])
    det = a[0]*b[1]-a[1]*b[0]
    assert det and r > 0
    # Recover the a coefficient from the displayed endpoint and known b term.
    c = [k*b[i]-r*a[i] for i in (0, 1)]
    residual = [c[i]-k*b[i] for i in (0, 1)]
    coefficient = F(residual[0]*b[1]-residual[1]*b[0], det)
    assert all(residual[i] == coefficient*a[i] for i in (0, 1))
    field, = q[':question/answer-fields']
    kval = '-' if k == -1 else '' if k == 1 else str(k)
    equation = r'\mathbf{c}=\lambda\mathbf{a}' + ('+' if k > 0 else '') + kval + r'\mathbf{b}'
    expected_tail = ('Given $' + equation + r'$, find $\lambda$.'
                     if enum(field[':answer-field/type']) == ':answer-field.type/radio'
                     else 'If $' + equation + r'$, then $\lambda=$ {{field-1}}.')
    assert prompt.split('\n\n')[-1] == expected_tail, 'Visible coefficient differs from the diagram and assessed calculation'
    correct = next(a for a in field[':answer-field/choices'] if str(a[':answer/id']) == answer_id(field[':answer-field/correct']))
    assert parse(correct[':answer/value']) == coefficient
    assert len({parse(a[':answer/value']) for a in field[':answer-field/choices']}) == len(field[':answer-field/choices'])
    assert r'\lambda=' + correct[':answer/value'] in solution
    # Ordinary samples must reference the clean prompt role, never its worked
    # construction role. Compare content-addressed published refs as well as raw.
    os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'] = str(directory)
    assets = render_plots(p)
    for role, text in [('prompt', prompt), ('solution', solution)]:
        refs = re.findall(r'!\[[^]]*\]\(([^)]+)\)', text)
        assert len(refs) == 1
        sha = hashlib.sha256((directory/assets[role]).read_bytes()).hexdigest()
        assert refs[0] in (assets[role], f'images/{sha[:2]}/{sha}.png'), 'Incorrect prompt/solution diagram role or changed geometry'
    checks = []
    if enum(field[':answer-field/type']) == ':answer-field.type/blank':
        checks = [dict(field_index=0, submitted=str(coefficient), expected='accepted', control='equivalent', purpose='Exact signed coefficient from endpoint subtraction'),
                  dict(field_index=0, submitted=str(-coefficient), expected='rejected', control='wrong', purpose='Length-only answer loses the residual reversal')]
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--records', required=True); parser.add_argument('--inventory', required=True); parser.add_argument('--output', required=True)
    args = parser.parse_args(); records = json.loads(Path(args.records).read_text()); native = []
    with tempfile.TemporaryDirectory(prefix='vector-refill-plots-') as temporary:
        for rec in records:
            controls = check(rec, Path(temporary))
            if controls: native.append(dict(fingerprint=fingerprint(rec['question']), checks=controls))
    covered = sorted(fingerprint(rec['question']) for rec in records)
    Path(args.output).write_text(json.dumps(dict(status='passed', checked_fingerprints=covered,
        check_results=[dict(id='independent-vector-task', status='passed', checked_fingerprints=covered)], native_checks=native), indent=2)+'\n')
