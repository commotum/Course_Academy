"""Parse printed tasks independently, validate both fragments and native grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
s = importlib.util.spec_from_file_location('parallel', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)
x, y = sp.symbols('x y', real=True)

def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2)+'\n')

def expression(text):
    text = re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', text)
    return sp.expand(parse_expr(text, local_dict={'x': x, 'y': y},
                    transformations=standard_transformations+(implicit_multiplication_application,)))

def polynomial(text):
    l, r = text.split('=')
    return expression(l)-expression(r)

def normalized(text):
    e = polynomial(text)
    a, b = e.coeff(x), e.coeff(y)
    assert a or b
    scale = a if a else b
    return tuple(sp.cancel(z/scale) for z in (a, b, e.subs({x: 0, y: 0})))

def printed(q):
    p = q[':question/problem']
    pts = [tuple(map(int, z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)', p)]
    u, v = pts[0]
    if 'line passing through the points' in p:
        (a, b), (c, d) = pts[1:3]
        m = sp.Rational(d-b, c-a)
        ref = None
    else:
        ref = p.split('parallel to $')[1].split('$')[0]
        e = polynomial(ref)
        m = -e.coeff(x)/e.coeff(y)
    return u, v, m, ref

def fingerprint(q):
    u, v, m, _ = printed(q)
    return g.digest([str(m), str(v-m*u)])

def check(rec):
    q, meta = rec['question'], rec['generation']
    assert rec == g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'],
                             meta['template'], meta['parameters'], meta['replay'])
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    assert fingerprint(q) == meta['mathematical_fingerprint']
    u, v, m, ref = printed(q)
    fs = q[':question/answer-fields']
    assert [f[':answer-field/key'] for f in fs] == ['field-1', 'field-2']
    assert all(f[':answer-field/type'] == ':answer-field.type/blank' and len(f[':answer-field/choices']) == 1 for f in fs)
    values = [f[':answer-field/choices'][0][':answer/value'] for f in fs]
    assert all('$' not in val and '=' not in val for val in values)
    assert all(f[':answer-field/correct'][1] == f[':answer-field/choices'][0][':answer/id'] for f in fs)
    assert len({f[':answer-field/choices'][0][':answer/id'] for f in fs}) == 2
    lhs, C = map(expression, values)
    A, B = lhs.coeff(x), lhs.coeff(y)
    assert lhs == A*x+B*y and A.is_Integer and B.is_Integer and C.is_Integer
    assert A > 0 and sp.gcd(A, B) == 1 and -A/B == m and A*u+B*v == C
    if not meta['replay']:
        assert g.CONVENTION in q[':question/problem']
    target = normalized(values[0]+'='+values[1])
    blocks = re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', q[':question/worked-solution'], re.S)
    assert len(blocks) == 3
    for index, block in enumerate(blocks):
        for row in block.split('\\\\'):
            row = row.replace('&', '').strip()
            if 'y_1' in row or 'y_2' in row or row.startswith('m') or row.startswith('='):
                continue
            if index == 0 and ref is None:
                continue
            assert normalized(row) == (normalized(ref) if index == 0 else target), row
    return rec

def native(label, rec):
    q = rec['question']
    vals = [f[':answer-field/choices'][0][':answer/value'] for f in q[':question/answer-fields']]
    lhs, C = map(expression, vals)
    A, B = lhs.coeff(x), lhs.coeff(y)
    checks = []
    for index, cases in enumerate([
        [(vals[0], 'accepted', 'canonical LHS'), (str(B*y+A*x), 'accepted', 'reordered LHS'),
         (f'{A}*x+({B})*y', 'accepted', 'explicit multiplication'),
         (str(lhs+1), 'rejected', 'constant on LHS'), (str(-lhs), 'rejected', 'violates positive A'),
         (str(2*lhs), 'rejected', 'violates coprime A,B'), (str(A*x-B*y), 'rejected', 'wrong slope')],
        [(vals[1], 'accepted', 'canonical RHS'), (f'({C-1})+1', 'accepted', 'equivalent numeric RHS'),
         (str(C+1), 'rejected', 'wrong intercept'), (str(C-1), 'rejected', 'wrong intercept')]]):
        checks += [{'field_index': index, 'submitted': v, 'expected': e, 'purpose': p} for v, e, p in cases]
    return {'label': label, 'record': rec, 'checks': checks}

def main():
    source = json.loads((HERE/'source.json').read_text())
    replay, inputs, review = [], [], []
    for template, old in g.sources().items():
        level = g.DATA[template][0]
        r = check(g.generate(level, 0, template, {'t': 0}, replay=True))
        assert r['question'][':question/problem'] == old[':question/problem']
        old_fields = sorted(old[':question/answer-fields'], key=lambda f: f[':answer-field/key'])
        assert all(f[':answer-field/key'] == o[':answer-field/key'] and
                   f[':answer-field/type'] == o[':answer-field/type'][':db/ident']
                   for f, o in zip(r['question'][':question/answer-fields'], old_fields))
        assert all(not o.get(':answer-field/choices') and not o.get(':answer-field/correct') for o in old_fields)
        assert ':question/worked-solution' not in old and ':question/difficulty' not in old
        replay.append({'source': template, 'prompt_exact': True, 'field_contract_exact': True,
                       'observed_answers': 0, 'matched_answers': 0,
                       'complete_bank_replay': 'not applicable: both source blank banks missing',
                       'answer_solution_difficulty_origin': 'authored additions; no source fidelity claimed'})
        review.append('## Original '+template+'\n\n'+old[':question/problem']+'\n\nNo source answers, solution or rating.\n\n'+g.markdown(r))
    fps, counts = set(), {}
    for level in ('easy', 'moderate'):
        counts[level] = 0
        for template, p in g.candidates(level):
            r = check(g.generate(level, 1913, template, p))
            fp = fingerprint(r['question'])
            assert fp not in fps
            fps.add(fp)
            assert r['question'] == g.generate(level, 999, template, p)['question']
            inputs.append(native(template+'-'+str(p['t']), r))
            counts[level] += 1
    for level, template, p in [('hard', 'q-214093', {'t': 1}), ('easy', 'q-216399', {'t': 1}),
                               ('easy', 'q-214093', {'t': 9}), ('easy', 'q-214093', {'t': -9}),
                               ('easy', 'q-214093', {'t': 1.5}), ('easy', 'q-214093', {'t': True})]:
        try:
            g.generate(level, 0, template, p)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid parameters accepted')
    try:
        g.batch('easy', 18, 0)
    except ValueError:
        pass
    else:
        raise AssertionError('Finite capacity exceeded')
    # Source t=0 is excluded from committed pool regardless of missing grading.
    previews = []
    used = {fingerprint(q) for q in source['record'][':knowledge-point/questions']}
    used.add(fingerprint(source['record'][':knowledge-point/canonical-example']))
    for level in ('easy', 'moderate'):
        for r in g.batch(level, 17, 1913):
            if fingerprint(r['question']) not in used:
                previews.append(r)
                used.add(fingerprint(r['question']))
    save('previews.json', previews)
    save('native-input.json', inputs)
    subprocess.run([str(HERE/'check-engine'), str(HERE/'native-input.json'), str(HERE/'native-grading.json')], check=True)
    report = json.loads((HERE/'native-grading.json').read_text())
    assert report['documented_unresolved_checks'] == 0
    save('source-replay.json', {'source_basis': source['basis'], 'passed': True, 'sources': replay,
                              'fidelity_limits': 'No source answers/solutions/ratings exist. Original prompts and both field contracts replay exactly. Production prompts add an explicit normalization convention.'})
    for level in ('easy', 'moderate'):
        for r in [r for r in previews if r['question'][':question/difficulty'].endswith('/'+level)][:5]:
            review.append('## Production variant\n\n'+g.markdown(r))
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    paths = [HERE.with_suffix('.py'), HERE/'validate.py', HERE/'source.json', ROOT/'engine/rust/learning.rs',
             ROOT/'engine/rust/symbolic.rs', ROOT/'generate/runs/current/check-engine.rs']
    save('validation.json', {'passed': True, 'exhaustive_instances': 34, 'bounded_counts': counts,
                            'unused_after_source_exclusion': {'easy': 16, 'moderate': 16},
                            'native_grading': {k: report[k] for k in ('entry_point', 'accepted_checks', 'rejected_checks', 'documented_unresolved_checks')},
                            'mathematics': 'independently parsed prompt slope and target incidence; integer primitive direction; every numerical solution row; both exact blank values',
                            'source_fidelity': 'two exact prompts and four field contracts; absent keys/solutions/ratings are explicitly authored',
                            'supported_levels': ['easy', 'moderate'],
                            'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})
    print('Validated all 34 bounded tasks and both source replays')

if __name__ == '__main__':
    main()
