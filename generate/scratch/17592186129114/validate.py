"""Independent rendered-matrix, source-bank, slot-domain and native grading checks."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('echelon_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, default=str)+'\n')

def parse(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
            for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)]

def oracle(m):
    # SymPy's exact, independent echelon predicate, not the generator's facts.
    return bool(sp.Matrix(m).is_echelon)

def check(r):
    q = r['question']; meta = r['generation']
    assert r == g.generate('easy', meta['seed'], meta['profile'], meta['parameters'], meta['replay'])
    assert q[':question/difficulty'] == ':question.difficulty/easy'
    assert r['knowledge_point']['db_id'] == g.KP_ID
    ms = parse(q[':question/problem'])
    assert ms == meta['parameters']['matrices']
    assert parse(q[':question/worked-solution']) == ms
    assert len(ms) == 3
    assert q[':question/problem'].endswith('Select all that apply.')
    verdicts = re.findall(r'- The matrix \$([ABC])\$\s+is (not in|in) row echelon form', q[':question/worked-solution'])
    assert verdicts == [(label, 'in' if oracle(m) else 'not in') for label, m in zip('ABC', ms)]
    # Independently check any concrete row/entry witness in each rendered paragraph.
    for label, m in zip('ABC', ms):
        paragraph = q[':question/worked-solution'].split('- The matrix $'+label+'$')[1].split('\n\n')[0]
        if 'row contains only zeros' in paragraph:
            row = next(i for i, name in enumerate(('first','second','third','fourth','fifth')) if name+' row' in paragraph)
            assert not any(m[row]) and any(any(v) for v in m[row+1:])
        witness = re.search(r'\$\{([abc])\}_\{(\d)(\d)\}', paragraph)
        if witness:
            name, ri, ci = witness.groups(); assert name == label.lower()
            i, j = int(ri)-1, int(ci)-1
            assert m[i][j] != 0 and not any(m[i][:j])
            above = [next(k for k,v in enumerate(row) if v) for row in m[:i] if any(row)]
            assert above and j <= above[-1]
    negate = '**not**' in q[':question/problem']
    fs = q[':question/answer-fields']; assert [f[':answer-field/key'] for f in fs] == list('ABC')
    ids = [q[':question/id']]
    for f, m in zip(fs, ms):
        assert f[':answer-field/type'] == ':answer-field.type/checkbox'
        answers = f[':answer-field/choices']; assert sorted(a[':answer/value'] for a in answers) == ['false', 'true']
        correct = [a for a in answers if a[':answer/id'] == f[':answer-field/correct'][1]]
        assert len(correct) == 1 and correct[0][':answer/value'] == str(oracle(m) != negate).lower()
        ids += [f[':answer-field/id']] + [a[':answer/id'] for a in answers]
    assert len(ids) == len(set(ids))
    assert meta['mathematical_fingerprint'] == g.fingerprint(q)
    return r

def native(label, r):
    checks = []
    for i, f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index': i, 'submitted_answer_id': a[':answer/id'],
                           'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
                           'purpose': 'Complete field-owned Boolean bank'})
    return {'label': label, 'record': r, 'checks': checks}

def main():
    replays, mapping, inputs, review, coverage = [], [], [], [], {}
    for profile in g.PROFILES:
        source = g.SOURCES[profile]
        r = check(g.generate('easy', 0, profile, g.original(profile), True))
        assert r['question'][':question/problem'] == source[':question/problem']
        source_solution = source[':question/worked-solution']
        if profile == 'q-129225':
            source_solution = source_solution.replace('${a}_{45}', '${c}_{45}')
        if profile == 'q-42366':
            source_solution = source_solution.replace(r'0 & 0 & 0 & 2 \\ 0 & 0 & 0 & 0', r'0 & 0 & 0 & -2 \\ 0 & 0 & 0 & 0')
        assert r['question'][':question/worked-solution'] == source_solution
        for sf, gf in zip(source[':question/answer-fields'], r['question'][':question/answer-fields']):
            assert sf[':answer-field/key'] == gf[':answer-field/key']
            assert sf[':answer-field/type'][':db/ident'] == gf[':answer-field/type']
            for sa in sf[':answer-field/choices']:
                matches = [a for a in gf[':answer-field/choices'] if a[':answer/value'] == sa[':answer/value']]
                assert len(matches) == 1
                correct = sa[':answer/id'] == sf[':answer-field/correct'][':answer/id']
                assert correct == (matches[0][':answer/id'] == gf[':answer-field/correct'][1])
                mapping.append({'source': profile, 'source_db_id': source[':db/id'], 'field': sf[':answer-field/key'], 'source_answer_id': sa[':answer/id'],
                                'value': sa[':answer/value'], 'recipe': 'literal Boolean', 'correct': correct, 'matched': True})
        replays.append({'source': profile, 'matched_choices': 6, 'total_choices': 6, 'matched_distractors': 3, 'total_distractors': 3,
                        'exact_prompt': True, 'exact_solution_after_documented_correction': True, 'correction': g.CORRECTIONS.get(profile)})
        inputs.append(native('source-'+profile, r))
        review.append('## Source '+profile+'\n\n'+g.markdown(r))
        domain = [g.pivot_domain(m) for m in g.original(profile)['matrices']]
        coverage[profile] = {'domains': domain, 'per_matrix_counts': list(map(len, domain)), 'structural_product_upper_bound': sp.prod(map(len, domain)), 'observed': [set(),set(),set()]}
        # Exhaust each declared pivot/zero-position slot, with other matrices fixed.
        for i, choices in enumerate(domain):
            for pivots in choices:
                p = g.original(profile)
                p['matrices'][i] = [[0]*len(p['matrices'][i][0]) if pivot is None else [0]*pivot+[1]+[2]*(len(p['matrices'][i][0])-pivot-1) for pivot in pivots]
                r = check(g.generate('easy', 0, profile, p))
                inputs.append(native(profile+'-matrix-'+str(i)+'-'+str(pivots), r))
                coverage[profile]['observed'][i].add(tuple(-1 if v is None else v for v in pivots))
            assert len(coverage[profile]['observed'][i]) == len(choices)
        for seed in range(30):
            r = check(g.generate('easy', seed, profile))
            assert r['question'] == g.generate('easy', seed+1000, profile, r['generation']['parameters'])['question']
            inputs.append(native(profile+'-sample-'+str(seed),r))
        review.append('## Variant '+profile+'\n\n'+g.markdown(r))
    # A changed zero-row position with every other matrix fixed exercises the
    # rendered ordinal witness; a changed leading-column case exercises indices.
    p = g.original('q-42024'); first = check(g.generate('easy',0,'q-42024',p))
    p['matrices'][0] = [p['matrices'][0][1],p['matrices'][0][0],p['matrices'][0][2]]
    changed = check(g.generate('easy',0,'q-42024',p))
    assert g.fingerprint(first['question']) != g.fingerprint(changed['question'])
    assert 'first row contains only zeros' in changed['question'][':question/worked-solution']
    inputs.append(native('changed-zero-target',changed));review.append('## Changed zero-row position\n\n'+g.markdown(changed))
    # Scaling, trailing values and label order must not add distinct tasks.
    p = g.original('q-42024'); a = g.generate('easy',0,'q-42024',p)
    p['matrices'] = [[[2*v for v in row] for row in m] for m in p['matrices']]
    b = g.generate('easy',0,'q-42024',p); assert g.fingerprint(a['question']) == g.fingerprint(b['question'])
    q = dict(a['question']); ms = list(reversed(parse(q[':question/problem']))); it=iter(ms)
    q[':question/problem'] = g.MATRIX.sub(lambda _: g.latex(next(it)),q[':question/problem'])
    assert g.fingerprint(q) == g.fingerprint(a['question'])
    previews = [check(r) for r in g.batch('easy',5,12345)]
    assert len({g.fingerprint(r['question']) for r in previews}) == 5
    for level in ('moderate','hard'):
        try: g.batch(level,5,0)
        except ValueError: pass
        else: raise AssertionError('Unsupported difficulty accepted')
    save('source-choice-mapping.json',mapping)
    save('source-replay.json',{'passed':True,'basis':g.S['basis'],'complete_banks_matched':13,'complete_banks_total':13,'matched_choices':78,'total_choices':78,
         'matched_distractors':39,'total_distractors':39,'missing_or_extra_options':[],'profiles':replays,'excluded':g.EXCLUDED,'source_corrections':g.CORRECTIONS})
    save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    assert json.loads((HERE/'native-report.json').read_text())['documented_unresolved_checks'] == 0
    save('previews.json',previews)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    for c in coverage.values(): c['observed'] = [sorted(v) for v in c['observed']]
    save('domain-catalog.json',coverage)
    save('validation.json',{'passed':True,'source_templates':2,'complete_source_profiles':13,'source_fidelity':'78/78 Boolean choices, 39/39 incorrect options, 13/13 full banks; exact prompts and solutions after two documented corrections',
         'mathematics':'Independent rendered-matrix parsing and SymPy Matrix.is_echelon; rendered matrices, judgments, witness positions and Boolean keys checked.',
         'actual_grading':'Every field-owned Boolean option through current learning::grade_field; zero unresolved checks', 'checked_instances':len(inputs),
         'all_declared_structural_slot_domains_checked':True,'changed_target_with_other_data_fixed':True,'semantic_duplicate_checks':True,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'assets':[],
         'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'scripts/question_capture/math_format.py')}})
    print('Validated 13 source banks, all structural slot domains and '+str(len(inputs))+' gradable instances.')

if __name__ == '__main__': main()
