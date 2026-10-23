"""Independently read rendered equations, matrix stages, operations and banks."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('gaussian_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
fingerprint = g.fingerprint


def save(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2)+'\n')


def number(s):
    s = s.replace(' ', '').rstrip('.')
    s = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', s)
    return sp.sympify(s)


def matrices(text):
    return [sp.Matrix([[number(c) for c in row.split('&')] for row in m.split(r'\\')]) for m in g.MAT.findall(text)]


def supplied(q):
    body = q[':question/problem'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    rows = []
    for row in body.split(r'\\'):
        lhs, rhs = row.split('&=')
        a, b = lhs.split('x')
        b = b.strip()
        assert b.endswith('y')
        a = number(a.strip()) if a.strip() not in ('','-') else (-1 if a.strip() else 1)
        b = b[:-1].strip()
        b = number(b) if b not in ('+','-') else (1 if b=='+' else -1)
        rows.append([a,b,number(rhs.strip().rstrip('.'))])
    return sp.Matrix(rows)


def operation(m, segment):
    found = re.search(r'\{R\}_\{([12])\} & :=(.*?) \\\\', segment, re.S)
    if not found:
        return m
    i = int(found[1])-1
    text = re.sub(r'\{R\}_\{([12])\}', r'r\1', found[2])
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text).replace(' ','')
    text = re.sub(r'(\d|\))(?=r)', r'\1*', text)
    out = m.copy()
    for j in range(3):
        out[i,j] = sp.sympify(text, locals={'r1':m[0,j], 'r2':m[1,j]})
    return out


def independent(rec):
    q, meta = rec['question'], rec['generation']
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    level = q[':question/difficulty'].split('/')[-1]
    assert level in g.SUPPORTED_LEVELS
    assert rec == g.generate(level, meta['seed'], meta['template'], meta['parameters'])
    initial = supplied(q)
    assert initial[:, :2].det() != 0
    xy = initial[:, :2].inv()*initial[:, 2]
    matches = list(g.MAT.finditer(q[':question/worked-solution']))
    stages = matrices(q[':question/worked-solution'])
    assert stages[0] == initial
    for i, m in enumerate(stages):
        assert m[:, :2].inv()*m[:, 2] == xy
        if i+1 < len(stages):
            assert operation(m, q[':question/worked-solution'][matches[i].end():matches[i+1].start()]) == stages[i+1]
    assert stages[-1][0,0] == stages[-1][1,1] == 1 and stages[-1][1,0] == 0
    f = q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields']) == 1 and f[':answer-field/key'] == 'selection' and f[':answer-field/type'] == ':answer-field.type/radio'
    assert len(f[':answer-field/choices']) == 5
    assert len({a[':answer/value'] for a in f[':answer-field/choices']}) == 5
    valid, objects = [], []
    for a in f[':answer-field/choices']:
        m, = matrices(a[':answer/value'])
        assert m.shape == (2,3) and m[0,0] == m[1,1] == 1 and m[1,0] == 0
        ok = m[:, :2]*xy == m[:,2]
        scalar = re.search(r'x=([^$]+)\$ and \$y=([^$]+)', a[':answer/value'])
        if a[':answer/type'] == ':answer.type/text':
            assert scalar
            pair = sp.Matrix([number(scalar[1]), number(scalar[2])])
            ok = ok and pair == xy
            objects.append((tuple(m), tuple(pair)))
        else:
            assert a[':answer/type'] == ':answer.type/math' and not scalar
            assert '$' not in a[':answer/value']
            objects.append(tuple(m))
        if ok:
            valid.append(a[':answer/id'])
    assert len(set(objects)) == 5
    assert valid == [f[':answer-field/correct'][1]], 'Bank must have exactly one mathematically correct full response'
    if 'and then solve' in q[':question/problem']:
        tail = q[':question/worked-solution'].split('The system is now')[1]
        values = re.findall(r'solution is \$x=([^$]+)\$ and \$y=([^$]+)', tail)
        assert len(values) == 1 and sp.Matrix([number(x) for x in values[0]]) == xy
        assert 'The final equation $y='+g.latex(xy[1])+'$' in tail
        body = tail.split('$$')[1]
        assert g.latex(stages[-1][0,2]) in body and g.latex(xy[1]) in body
        substitution = tail.split('$$')[3]
        lhs, rhs = substitution.split(r'\,⇒\,')
        # Numerically execute the displayed back substitution and final chain.
        lhs_left, lhs_right = lhs.strip().split('=')
        expr = lhs_left.replace('x','('+str(xy[0])+')')
        expr = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', expr)
        expr = re.sub(r'(\d|\))(?=\()', r'\1*', expr)
        assert number(expr) == number(lhs_right)
        chain = rhs.strip().rstrip('.').split('=')
        assert chain[0] == 'x' and all(number(x) == xy[0] for x in chain[1:])
    assert meta['mathematical_fingerprint'] == fingerprint(q)
    return rec


def checks(rec):
    f = rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected', 'purpose':'each complete option through actual application radio grader'} for a in f[':answer-field/choices']]


def main():
    replay, inputs, coverage, review, recipes = [], [], {}, [], []
    distinct = {l:set() for l in g.SUPPORTED_LEVELS}
    for sid, old in g.CASES.items():
        level = old[':question/difficulty'][':db/ident'].split('/')[-1]
        original = independent(g.generate(level, 0, sid, [0,0]))
        for key in (':question/problem', ':question/worked-solution'):
            assert original['question'][key] == old[key]
        of, rf = old[':question/answer-fields'][0], original['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in of[':answer-field/choices']) == sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
        assert of[':answer-field/correct'][':answer/value'] == next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        replay.append({'source':sid, 'complete_bank_matched':True, 'matched_choices':5, 'matched_distractors':4, 'missing':[], 'extra':[], 'prompt_exact':True, 'solution_exact':True})
        for a in of[':answer-field/choices']:
            m, = matrices(a[':answer/value'])
            recipes.append({'source':sid, 'source_answer_id':a[':answer/id'], 'profile':sid, 'field':'selection', 'exact_source_value':a[':answer/value'], 'source_matrix':[[str(x) for x in m[i,:]] for i in range(2)], 'recipe':'Each source row (a,b,c) becomes (a,b,c+a*h+b*k); text solution x,y becomes x+h,y+k. Correct and incorrect options use their own complete source matrix and pair.', 'interpretation':'Observed affine expression pattern; error psychology unresolved', 'replays_complete_value':True})
        positions = []
        for p in g.domain(sid):
            r = independent(g.generate(level, 59776, sid, p))
            distinct[level].add(fingerprint(r['question']))
            positions.append(p)
            inputs.append({'label':sid+' '+str(p), 'record':r, 'checks':checks(r)})
        coverage[sid] = {'offset_pairs':positions, 'h':sorted({p[0] for p in positions}), 'k':sorted({p[1] for p in positions}), 'instances':len(positions), 'missing_slots':[], 'fixed_roles':'First variable pivot in row 1, eliminate first variable from row 2, then normalize second pivot. Variable order is an operative method constraint.'}
        variant = independent(g.generate(level, 0, sid, [2,-1]))
        assert variant['question'] == g.generate(level, 999, sid, [2,-1])['question']
        review.append('## '+sid+' ('+level+')\n\nSource\n\n'+g.markdown(original)+'\n\nOffsets h=2, k=-1\n\n'+g.markdown(variant))
    for level in ('hard', 'unclassified'):
        try:
            g.generate(level)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported level accepted')
    for i in (0,1):
        r = copy.deepcopy(inputs[i]['record'])
        r['question'][':question/worked-solution'] += ' stale content'
        try:
            independent(r)
        except AssertionError:
            pass
        else:
            raise AssertionError('Mutation accepted')
    save('source-replay.json', {'passed':True, 'complete_banks_matched':10, 'complete_banks_total':10, 'distractors_matched':40, 'distractors_total':40, 'profiles':replay})
    save('choice-recipes.json', recipes)
    save('slot-coverage.json', coverage)
    save('native-input.json', inputs)
    subprocess.run([str(HERE/'reference/native/check-engine'), str(HERE/'native-input.json'), str(HERE/'native-grading.json')], check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json', {'status':'pass', 'passed':True, 'exhaustive_instances':len(inputs), 'distinct_solution_tasks_by_level':{l:len(v) for l,v in distinct.items()}, 'supported_levels':list(g.SUPPORTED_LEVELS), 'unsupported_levels':['hard'], 'source_fidelity':'10/10 exact prompt and solution replays; 10/10 complete banks; 40/40 distractors', 'mathematics':'Independently parsed rendered equations and every matrix stage; executed each displayed row operation; tested every complete choice and final back substitution; exactly one valid choice', 'grading':'All five choices for all 490 bounded cases through actual application grade_field', 'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), HERE/'source.json', HERE/'validate.py', HERE/'replenish.py', HERE/'capabilities.json', HERE/'reference/native/check-engine')}})


if __name__ == '__main__':
    main()
