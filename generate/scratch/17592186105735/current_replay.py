"""Current-source replay and independent validation, without changing frozen v2 IDs.

Current source profiles retain numerical residual banks as empirical evidence.
They are excluded from production sampling; v2's complete operation banks are
used there. Coefficient-two radicals and the larger source a-vector are replay
extensions only, outside the deliberately narrower production sampling policy.
"""
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('v2', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def scalar(s):
    s = re.sub(r'\\sqrt\{(\d+)\}', r'sqrt(\1)', s.replace(r'\,', ''))
    s = re.sub(r'(?<=\d)(?=sqrt)', '*', s)
    return sp.sympify(s)

def parameters(q):
    prompt = q[':question/problem'].replace(r'\langle', '⟨').replace(r'\rangle', '⟩')
    vs = [[scalar(x) for x in v.replace(r'\,', '').split(',')]
          for v in re.findall('⟨([^⟩]+)⟩', prompt)]
    assert len(vs) in (2, 3) and all(len(v) == 3 for v in vs)
    return dict(zip(('a', 'd') if len(vs) == 2 else ('a', 'b', 'c'), vs))

def fingerprint(q):
    p = parameters(q)
    task = {'method': 'supplied-cross-dot' if 'd' in p else 'cross-then-dot',
            'vectors': {k: [sp.srepr(x) for x in xs] for k, xs in sorted(p.items())}}
    return hashlib.sha256(json.dumps(task, sort_keys=True).encode()).hexdigest()

def render_current(mid, p, template):
    # Extend the same operation masks locally for replay. No literal question or
    # worked-solution text is substituted from the source capture.
    args = {k: [str(x) for x in xs] for k, xs in p.items()}
    if mid in g.SPECS:
        anchor = g.SPECS[mid][2]
        assert all([sp.sympify(x) for x in anchor[k]] == xs for k, xs in p.items())
        args = copy.deepcopy(anchor)
    if mid == 'q-317306':
        # g.render uses its val/tex callbacks; a fresh module avoids changing the
        # frozen production generator's numeric grammar or sampling contract.
        spec = importlib.util.spec_from_file_location('replay_mask', HERE.with_suffix('.py'))
        mask = importlib.util.module_from_spec(spec); spec.loader.exec_module(mask)
        mask.val = sp.sympify
        mask.tex = lambda x: sp.latex(sp.sympify(x)).replace(r'2 \sqrt', r'2\sqrt').replace('- ', '-')
        return mask.render(template, args)
    prompt, solution = g.render(template, args)
    if mid == 'q-128093':
        b, c = args['b'], args['c']
        group, tex = g.group, g.tex
        old = '('+group(b[1])+r'\cdot '+group(c[2])+'-'+group(b[2])+r'\cdot '+group(c[1])+')i-('+group(b[0])+r'\cdot '+group(c[2])+'-'+group(b[2])+r'\cdot '+group(c[0])+')j+('+group(b[0])+r'\cdot '+group(c[1])+'-'+group(b[1])+r'\cdot '+group(c[0])+')k'
        # Source has commuted second products in all three minors, and an
        # ungrouped first negative b0 in the j minor. Roles remain identical.
        new = '('+group(b[1])+r'\cdot '+group(c[2])+'-'+group(c[1])+r'\cdot '+group(b[2])+')i-('+tex(b[0])+r'\cdot '+group(c[2])+'-'+group(c[0])+r'\cdot '+group(b[2])+')j+('+group(b[0])+r'\cdot '+group(c[1])+'-'+group(c[0])+r'\cdot '+group(b[1])+')k'
        assert old in solution
        solution = solution.replace(old, new)
    return prompt, solution

def template_for(q):
    mid = q[':question/math-academy-id']
    if mid == 'q-20065': return 'cross_radio'
    if mid in g.SPECS: return g.SPECS[mid][1]
    return {'q-128090': 'dot_int_radio', 'q-73451': 'dot_int_radio',
            'q-128093': 'cross_radio', 'q-317306': 'dot_radical_thin_blank'}[mid]

def validate_source(q):
    p = parameters(q); mid = q[':question/math-academy-id']; template = template_for(q)
    d = p.get('d', list(sp.Matrix(p['b']).cross(sp.Matrix(p['c']))) if 'b' in p else None)
    t = sp.Matrix(p['a']).dot(sp.Matrix(d))
    prompt, solution = render_current(mid, p, template)
    assert prompt == q[':question/problem'], (mid, 'prompt fidelity')
    assert solution == q[':question/worked-solution'], (mid, 'solution fidelity')
    fields = q[':question/answer-fields']; assert len(fields) == 1
    f = fields[0]; choices = f[':answer-field/choices']; vals = [scalar(a[':answer/value']) for a in choices]
    ft = str(f[':answer-field/type'][':db/ident']).split('/')[-1]
    assert len(vals) == (5 if ft == 'radio' else 1) and len(set(vals)) == len(vals)
    assert scalar(f[':answer-field/correct'][':answer/value']) == t and vals.count(t) == 1
    expected_level = 'easy' if 'd' in p else 'moderate'
    assert str(q[':question/difficulty'][':db/ident']) == ':question.difficulty/'+expected_level
    residuals = [sp.simplify(x-t) for x in vals]
    # One explicit complete numerical profile, never a pooled distractor list.
    bank = [sp.simplify(t+r) for r in residuals]
    assert bank == vals
    return {'source_id': mid, 'level': expected_level, 'template': template,
            'profile': 'current:'+mid if ft == 'radio' else 'blank',
            'parameters': {k: list(map(str, xs)) for k, xs in p.items()},
            'prompt_exact': True, 'worked_solution_exact': True,
            'complete_bank_matched': len(vals), 'distractors_matched': len(vals)-1,
            'correct': str(t), 'values': list(map(str, vals)), 'residuals': list(map(str, residuals)),
            'bank_interpretation': 'empirical replay only' if ft == 'radio' else 'canonical scalar',
            'plot_rating': 'none', 'mathematical_fingerprint': fingerprint(q)}

def fixture_source(q):
    def enum(x):return str(x[':db/ident'])
    f = q[':question/answer-fields'][0]
    field = {':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'],
             ':answer-field/type': enum(f[':answer-field/type']),
             ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])],
             ':answer-field/choices': [{':answer/id': str(a[':answer/id']), ':answer/type': enum(a[':answer/type']),
                                       ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]}
    record = {'knowledge_point': {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE},
              'question': {':question/id': str(q[':question/id']), ':question/problem': q[':question/problem'],
                           ':question/worked-solution': q[':question/worked-solution'],
                           ':question/difficulty': enum(q[':question/difficulty']), ':question/answer-fields': [field]},
              'generation': {'template': template_for(q)}}
    if field[':answer-field/type'].endswith('/radio'):
        checks = [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == field[':answer-field/correct'][1] else 'rejected', 'purpose': 'complete source bank'} for a in field[':answer-field/choices']]
    else:
        t = scalar(f[':answer-field/correct'][':answer/value'])
        checks = [{'submitted': s, 'expected': outcome, 'purpose': 'source scalar grading'} for s, outcome in [(str(t),'accepted'),(str(t-3)+'+3','accepted'),(str(t+1),'rejected')]]
    return {'label': q[':question/math-academy-id'], 'record': record, 'checks': checks}
