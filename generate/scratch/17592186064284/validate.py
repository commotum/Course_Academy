#!/usr/bin/env python3
"""Validate the finite hard domain, authored fields, and the actual learner grader."""
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('trig_tangent', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def main():
    x = sp.Symbol('x', real=True)
    records = []; checks = []; signatures = set(); ids = set()
    for a in range(1, 10):
        for phase in g.PHASES:
            p = {'a': a, 'phase': phase}
            r = g.generate_hard(33, parameters=p)
            q = r['question']; f = q[':question/answer-fields'][0]
            curve = a * sp.cos(sp.sin(x) + sp.pi * sp.Rational(phase), evaluate=False)
            # Derive the tangent directly by symbolic differentiation of the curve.
            height = sp.simplify(curve.subs(x, 0))
            slope = sp.simplify(sp.diff(curve, x).subs(x, 0))
            line = sp.expand(height + x * slope)
            assert sp.simplify(line.subs(x, 0) - height) == 0
            assert sp.simplify(sp.diff(line, x) - slope) == 0
            assert f[':answer-field/choices'][0][':answer/value'] == sp.latex(line)
            assert f[':answer-field/correct'][1] == f[':answer-field/choices'][0][':answer/id']
            assert f[':answer-field/key'] == 'field-1' and '{{field-1}}' in q[':question/problem']
            assert f'$y={sp.latex(curve)}$' in q[':question/problem']
            assert f'0,{sp.latex(height)}' in q[':question/problem']
            assert sp.latex(line) in q[':question/worked-solution']
            assert q[':question/problem'].count('$') % 2 == 0 and q[':question/worked-solution'].count('$') % 2 == 0
            signature = (sp.srepr(curve), sp.srepr(line))
            assert signature not in signatures and q[':question/id'] not in ids
            signatures.add(signature); ids.add(q[':question/id'])
            assert g.generate_hard(999, parameters=p)['question'] == q
            equivalent = f'({sp.latex(height)})+x*({sp.latex(slope)})'
            checks.append({'label': str(p), 'record': r, 'checks': [
                {'submitted': sp.latex(line), 'expected': 'accepted', 'purpose': 'independently differentiated canonical RHS'},
                {'submitted': equivalent, 'expected': 'accepted', 'purpose': 'reordered affine expression with explicit multiplication'},
                {'submitted': sp.latex(line + 1), 'expected': 'rejected', 'purpose': 'incorrect tangent intercept'},
                {'submitted': sp.latex(line + x), 'expected': 'rejected', 'purpose': 'incorrect tangent slope'}]})
            records.append(r)
    for params in ({'a': 0, 'phase': '0'}, {'a': 10, 'phase': '0'}, {'a': 1, 'phase': '1/2'}, {'a': True, 'phase': '0'}):
        try: g.generate_hard(parameters=params)
        except ValueError: pass
        else: raise AssertionError('invalid parameter accepted')
    for level in ('easy', 'moderate'):
        try: g.generate(level)
        except ValueError: pass
        else: raise AssertionError('uncertified difficulty accepted')
    save('engine-input.json', checks)
    engine = HERE.parents[1] / 'runs/current/check-engine'
    subprocess.run([str(engine), str(HERE / 'engine-input.json'), str(HERE / 'engine-report.json')], check=True)
    source = json.loads((HERE / 'source.json').read_text())
    original = next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id'] == 'q-48644')
    assert ':question/answer-fields' not in original
    replay = g.generate_hard(parameters={'a': 1, 'phase': '0'})
    assert replay['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] == '1'
    # The source's original line is y=1; capture prose is retained verbatim as evidence.
    assert 'y&=1.' in original[':question/worked-solution']
    batch = [g.generate_hard(parameters={'a': 1, 'phase': p}) for p in g.PHASES if p != '0']
    save('generated.json', batch)
    save('review.json', {'original': original, 'source_parameter_replay': replay, 'variants': batch})
    (HERE / 'review.md').write_text('# Original hard source\n\n' + original[':question/problem'] + '\n\n' + original[':question/worked-solution'] +
        '\n\n# Authored blank-field variants\n\n' + '\n\n---\n\n'.join(g.markdown(r) for r in batch) + '\n')
    save('validation.json', {'status': 'passed', 'basis': source['basis'], 'scope': 'hard tangent-line extension only',
        'validated_parameter_pairs': len(records), 'distinct_curves_and_lines': len(signatures), 'seed_identity_independent': True,
        'source_replay': {'question': 'q-48644', 'a': 1, 'phase': '0', 'tangent_rhs': '1', 'mathematics': 'matched',
            'raw_prose_fidelity': 'authored equivalent solution, preserves decomposition/differentiation/chain rule/evaluation/point-slope sequence',
            'source_banks': 0, 'matched_source_banks': 0, 'field_fidelity': 'source field absent; authored RHS blank explicitly identified'},
        'moderate_banks': 'captured and classified; not certified for generation by this hard-only package',
        'native_grading': json.loads((HERE / 'engine-report.json').read_text()),
        'generator_sha256': hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),
        'engine_sha256': hashlib.sha256(engine.read_bytes()).hexdigest(), 'generated_questions': len(batch), 'plots': 'none'})
    print('PASS: 54 distinct exact tangent problems; 216 native learner grading checks; 5 ready instances')

if __name__ == '__main__': main()
