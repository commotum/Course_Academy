import collections
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OLD = Path('/media/jake/SSD/EDB/math/generators')

def load(path, name):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    sys.path.pop(0)
    return m

def rank(a):
    a = [[Fraction(x) for x in r] for r in a]
    p = 0
    for c in range(len(a[0])):
        i = next((i for i in range(p, len(a)) if a[i][c]), None)
        if i is None:
            continue
        a[p], a[i] = a[i], a[p]
        q = a[p][c]
        a[p] = [x/q for x in a[p]]
        for j in range(len(a)):
            if j != p:
                q = a[j][c]
                a[j] = [x-q*y for x,y in zip(a[j],a[p])]
        p += 1
    return p

def answer(f):
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])

def vector_columns(prompt):
    # Read the displayed column vectors, not the generation parameters.
    pieces = re.findall(r'\\mathbf\{a\}_\{?\d\}?\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', prompt, re.S)
    return [[int(x.strip()) for x in p.split(r'\\')] for p in pieces]

def field_truth(key, vectors, independent):
    if key.startswith('The set') or key.startswith('The vectors'):
        return independent if 'linearly independent' in key else not independent
    if 'only' in key or 'Every column' in key:
        return independent
    if 'infinitely' in key or 'free variable' in key:
        return not independent
    lhs=key.split('=')[0].replace('$','')
    terms = re.findall(r'([+-]?)(\d*)\\mathbf\{a\}_\{(\d)\}', lhs)
    assert terms, key
    coeff = [0] * len(vectors)
    for sign,num,i in terms:
        coeff[int(i)-1] = (-1 if sign=='-' else 1) * int(num or 1)
    return all(sum(c*v[i] for c,v in zip(coeff,vectors))==0 for i in range(3))

results=[]
mods={}
for kp,filename,old_dir in [
    ('17592186119924','generate.py','af/af4dc7eb0c482966b75877a9c85bdcd3e655656123b4eb3fbffd2c00655c3f24'),
    ('17592186119925','generator.py','a5/a5ea85eae7b38ce699ccbdc0c28a45c9070d21ed46537500c53f5f54f94fd522')]:
    m=load(ROOT/'packages'/kp/filename,'new_'+kp)
    old=load(OLD/old_dir/filename,'old_'+kp)
    mods[kp]=m
    # Raw replay includes legacy response shapes. Compare all replay content
    # except the intentional checkbox prompt addition and generation version.
    sf='source_cases.json' if kp.endswith('924') else 'source-cases.json'
    cases=json.loads((ROOT/'packages'/kp/sf).read_text())
    before=[old.render(c) if kp.endswith('924') else old.replay_source(c) for c in cases]
    after=[m.render(c) if kp.endswith('924') else m.replay_source(c) for c in cases]
    for a,b in zip(before,after):
        qa,qb=a['question'],b['question']
        expected_prompt=qa[':question/problem']
        if kp.endswith('924'):
            expected_prompt=expected_prompt.replace('Select all that apply.','Select all that apply. If none apply, leave all boxes unchecked.')
        assert expected_prompt == qb[':question/problem']
        assert qa[':question/worked-solution']==qb[':question/worked-solution']
        assert [(f[':answer-field/key'],f[':answer-field/type'],[v[':answer/value'] for v in f[':answer-field/choices']],answer(f)) for f in qa[':question/answer-fields']] == [(f[':answer-field/key'],f[':answer-field/type'],[v[':answer/value'] for v in f[':answer-field/choices']],answer(f)) for f in qb[':question/answer-fields']]
    replay_count=len(cases)
    for band in ['easy','moderate','hard']:
        records=m.generate(band,120,4242)
        assert records==m.generate(band,120,4242)
        counts=collections.Counter();ranks=collections.Counter();regimes=collections.Counter();challenges=collections.Counter();identities=set()
        for r in records:
            q=r['question'];fs=q[':question/answer-fields'];g=r['generation']
            assert len(fs)==3
            assert len(set(f[':answer-field/key'] for f in fs))==3
            assert 'If none apply, leave all boxes unchecked.' in q[':question/problem']
            vectors=vector_columns(q[':question/problem'])
            assert len(vectors) in (2,3),q[':question/problem']
            a=list(map(list,zip(*vectors)));rk=rank(a);ind=rk==len(vectors)
            ranks[rk]+=1
            if kp.endswith('924'):
                assert vectors==g['parameters']['vectors']
                regimes[g['parameters']['regime']]+=1
                assert g['parameters']['independent']==ind
                w=g['parameters']['witness']
                if w is not None:
                    assert any(w) and all(sum(c*v[i] for c,v in zip(w,vectors))==0 for i in range(3))
            else:
                assert a==g['matrix']
                challenges[g['challenge']]+=1
                assert len(g['pivots'])==rk
                states=[[[Fraction(x) for x in row] for row in state] for state in g['states']]
                assert states[0]==a
                for prior,op,nxt in zip(states,g['operations'],states[1:]):
                    copy=[row[:] for row in prior]
                    i,j=op['i'],op['j']
                    if op['kind']=='swap':copy[i],copy[j]=copy[j],copy[i]
                    else:copy[i]=[x+Fraction(op['factor'])*y for x,y in zip(copy[i],copy[j])]
                    assert copy==nxt
                assert rank(states[-1])==rk
                assert 'Append the zero right-hand side' in q[':question/worked-solution']
                assert q[':question/worked-solution'].count('Apply $')==len(g['operations'])
            selected=0
            for f in fs:
                key=f[':answer-field/key']
                assert key not in ('I','II','III','selection') and 'None of' not in key
                assert f[':answer-field/type']==':answer-field.type/checkbox'
                assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
                expected=field_truth(key,vectors,ind)
                assert answer(f)==str(expected).lower(),(kp,band,key)
                selected+=expected
                for identity in [f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:
                    assert identity not in identities
                    identities.add(identity)
            counts[selected]+=1
            assert q[':question/id'] not in identities
            identities.add(q[':question/id'])
        assert len(records)==120
        assert counts[0]>0,(kp,band,counts)
        results.append({'kp':kp,'band':band,'seed':4242,'records':120,'deterministic_repeat':True,'displayed_vector_rank_checked':True,'displayed_statement_truth_checked':True,'row_transitions_checked':not kp.endswith('924'),'selected_count_histogram':dict(counts),'rank_histogram':dict(ranks),'regime_histogram':dict(regimes),'challenge_histogram':dict(challenges),'source_replay_records_compared':replay_count})

out={'checks':results,'total_generated_records':sum(x['records'] for x in results),'native_or_ui_grading_tested':False,'note':'All-false booleans are verified at generator-record level. Native explicit-false submission and UI behavior are separate root-agent checks.'}
(ROOT/'review'/'offline-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
