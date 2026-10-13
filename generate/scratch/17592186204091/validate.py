"""Exact source replay, independent symbolic solution checks and real blank grading."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def save(name, value): (HERE/name).write_text(json.dumps(value, indent=2, default=str)+'\n')

def parse(problem):
    # Reads rendered mathematics independently, including the incomplete legacy prompt.
    compact = re.sub(r'\s+', '', problem)
    match = re.search(r'(\d*)\(([pkmqr])([+-]\d+)\)([xuvzw])([+-]\d+)=(-?\d+)', compact)
    assert match, problem
    s, k, h, x, b, c = match.groups()
    return {'variable': x, 'parameter': k, 'scale': int(s or 1), 'shift': int(h), 'left': int(b), 'right': int(c)}

def expr(text):
    text = re.sub(r'\{\{(.*?)\}_\{⏟\}\}_\{[ab]\}', r'\1', text)
    text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', text.strip().rstrip('.'))
    return parse_expr(text, transformations=standard_transformations+(implicit_multiplication_application,))

def independent(rec):
    q, meta = rec['question'], rec['generation']; p = parse(q[':question/problem'])
    assert p == meta['parameters'] and rec['knowledge_point']['db_id'] == g.KP_ID
    level = q[':question/difficulty'].split('/')[-1]
    assert rec == g.generate(level, meta['seed'], meta['template'], p, meta['bank_profile'])
    assert meta['parameter_fingerprint'] == g.fingerprint(p)
    x, k = sp.Symbol(p['variable']), sp.Symbol(p['parameter'])
    # Find the exceptional coefficient root from the actual rendered equation.
    eq = re.search(r'\$\$\n(.*?)\n\$\$', q[':question/problem'], re.S)[1]
    left, right = map(expr, eq.split('=')); difference = sp.expand(left-right)
    coeff = difference.coeff(x); constant = difference.subs(x, 0)
    roots = sp.solve(coeff, k); assert len(roots) == 1 and constant != 0
    root = roots[0]; assert sp.solveset(sp.Eq(left.subs(k, root), right), x, domain=sp.S.Reals) == sp.S.EmptySet
    assert sp.solveset(sp.Eq(left.subs(k, root+1), right), x, domain=sp.S.Reals) != sp.S.EmptySet
    f = q[':question/answer-fields'][0]; answers = f[':answer-field/choices']
    assert len(q[':question/answer-fields']) == len(answers) == 1
    assert f[':answer-field/key'] == 'field-1' and f[':answer-field/type'] == ':answer-field.type/blank'
    assert answers[0][':answer/type'] == ':answer.type/math' and expr(answers[0][':answer/value']) == root
    assert f[':answer-field/correct'] == [':answer/id', answers[0][':answer/id']]
    assert q[':question/problem'].count('{{field-1}}') == 1
    ids = [q[':question/id'], f[':answer-field/id'], answers[0][':answer/id']]
    assert len(set(ids)) == 3
    for value in ids: uuid.UUID(value)
    displays = re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', q[':question/worked-solution'], re.S)
    assert len(displays) == 2
    for line in displays[0].split(r'\\'):
        a, b = map(expr, line.replace('&', '').split('='))
        assert sp.simplify(a-b-difference) == 0, line
    for line in displays[1].split(r'\\'):
        a, b = map(expr, line.replace('&', '').split('='))
        assert sp.solve(a-b, k) == roots, line
    for text in (q[':question/problem'], q[':question/worked-solution']):
        assert text.count('$') % 2 == 0 and text.count('{') == text.count('}')

def checks(rec):
    value = int(rec['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
    return [{'field_index': 0, 'submitted': text, 'expected': expected, 'purpose': 'Actual learner blank grading: equivalent and incorrect mathematical entries'}
            for expected, entries in [('accepted', (str(value), str(value)+'.0', str(value)+'+0', r'\frac{'+str(2*value)+'}{2}')),
                                      ('rejected', (str(value+1), str(value-1), '0'))] for text in entries]

def main():
    source = json.loads((HERE/'source.json').read_text()); replays = []; cases = []; excluded = []; review = []
    for q in source['record'][':knowledge-point/questions']:
        mid = q[':question/math-academy-id']; p = parse(q[':question/problem'])
        if ':question/worked-solution' not in q or ':answer-field/correct' not in q[':question/answer-fields'][0]:
            excluded.append({'source': mid, 'reason': 'Unrated; missing worked solution, correct answer and choice bank. Preserved; excluded from validated template fidelity and inventory.'})
            continue
        level = q[':question/difficulty'][':db/ident'].split('/')[-1]
        rec = g.generate(level, parameters=p); independent(rec); new = rec['question']; f = new[':question/answer-fields'][0]; old = q[':question/answer-fields'][0]
        assert new[':question/problem'] == q[':question/problem'], (mid, 'prompt')
        assert new[':question/worked-solution'] == q[':question/worked-solution'], (mid, 'solution')
        assert old[':answer-field/type'][':db/ident'] == f[':answer-field/type'] and old[':answer-field/key'] == f[':answer-field/key']
        assert [a[':answer/value'] for a in old[':answer-field/choices']] == [a[':answer/value'] for a in f[':answer-field/choices']]
        assert old[':answer-field/correct'][':answer/value'] == f[':answer-field/choices'][0][':answer/value']
        cases.append({'source_id': mid, 'difficulty': level, 'parameters': p, 'template': rec['generation']['template'], 'bank_profile': 'blank-integer', 'full_bank_matched': True, 'matched_values': 1, 'total_values': 1, 'incorrect_choices': 0, 'exact_prompt': True, 'exact_solution': True})
        replays.append(rec); review.append('## Source '+mid+' and exact replay\n\n'+g.markdown(rec))
    variants = []
    for level in g.SUPPORTED_LEVELS:
        for seed in range(100):
            rec = g.generate(level, seed); independent(rec); variants.append(rec)
        batch = g.batch(level, 18, 811); assert len({r['generation']['parameter_fingerprint'] for r in batch}) == 18
        for rec in batch: independent(rec)
        review.append('## '+level+' variant\n\n'+g.markdown(g.generate(level, 811)))
    # All roots/signs and domain boundaries, independently checked from displayed math.
    boundaries = []
    for scale in (1, 2, 9):
        for shift in (-9, -1, 1, 9):
            for left in (-9, 9):
                for right in (-10, 0, 10):
                    if left == right: continue
                    r = g.generate('easy' if scale == 1 else 'moderate', parameters={'variable': 'x', 'parameter': 'p', 'scale': scale, 'shift': shift, 'left': left, 'right': right})
                    independent(r); boundaries.append(r)
    reference = replays[0]; changed = copy.deepcopy(reference['generation']['parameters']); changed['variable'] = 'w'; changed['parameter'] = 'r'; changed['left'] = -9; changed['right'] = 9
    assert g.fingerprint(changed) == reference['generation']['parameter_fingerprint']
    if changed['scale'] != 1: changed['scale'] = 9; assert g.fingerprint(changed) == reference['generation']['parameter_fingerprint']
    assert g.generate('moderate', 1, parameters=reference['generation']['parameters'])['question'] == g.generate('moderate', 99, parameters=reference['generation']['parameters'])['question']
    negative = 0
    for level, p in [('hard', None), ('moderate', dict(reference['generation']['parameters'], scale=0)), ('moderate', dict(reference['generation']['parameters'], right=reference['generation']['parameters']['left'])), ('moderate', dict(reference['generation']['parameters'], shift=0))]:
        try: g.generate(level, parameters=p)
        except ValueError: negative += 1
        else: raise AssertionError('Invalid parameters accepted')
    for attribute in ('answer', 'solution'):
        bad = copy.deepcopy(reference)
        if attribute == 'answer': bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = '0'
        else: bad['question'][':question/worked-solution'] = bad['question'][':question/worked-solution'].replace('p & =4.', 'p & =5.')
        try: independent(bad)
        except AssertionError: negative += 1
        else: raise AssertionError('Corruption accepted')
    records = replays+variants+boundaries
    save('source-cases.json', cases); save('excluded-source.json', excluded)
    save('engine-input.json', [{'label': str(i), 'record': r, 'checks': checks(r)} for i, r in enumerate(records)])
    binary = ROOT/'generate/runs/current/check-engine'
    result = subprocess.run([str(binary), str(HERE/'engine-input.json'), str(HERE/'engine-report.json')], capture_output=True, text=True)
    (HERE/'engine.log').write_text(result.stdout+result.stderr); assert result.returncode == 0, result.stderr
    engine = json.loads((HERE/'engine-report.json').read_text()); assert engine['documented_unresolved_checks'] == 0
    (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    save('review.json', {'replays': replays, 'variants': [g.generate(level, 811) for level in g.SUPPORTED_LEVELS]})
    save('validation.json', {'status': 'pass', 'supported_levels': list(g.SUPPORTED_LEVELS), 'source_basis': source['basis'], 'lineage': source['lineage'],
         'source_coverage': {'complete_source_questions': len(cases), 'complete_question_banks_matched': len(cases), 'matched_values': len(cases), 'total_values': len(cases), 'missing_options': [], 'extra_options': [], 'excluded_incomplete': excluded},
         'fidelity': 'Exact prompt, solution, answer-field type/key, complete singleton bank and correct value for all five complete sources; incomplete source explicitly excluded.',
         'mathematics': {'independent_display_checks': len(records), 'boundary_cases': len(boundaries), 'distinct_roots_per_level': 18, 'negative_controls': negative},
         'native_grading': {k: engine[k] for k in ('entry_point', 'accepted_checks', 'rejected_checks', 'documented_unresolved_checks')},
         'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), Path(__file__), HERE/'source.json', binary)}})
    print('Validated five exact complete sources, both levels, boundaries and native blank grading.')

if __name__ == '__main__': main()
