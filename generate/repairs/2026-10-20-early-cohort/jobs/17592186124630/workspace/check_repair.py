#!/usr/bin/env python3
"""Regression checks against public records, with a separate typed theorem oracle."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
PYTHON = sys.executable
OUT = BASE / 'evidence'
OUT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('generator', BASE / '17592186124630.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def save(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def cli(*args, cwd=BASE, entry=None):
    return subprocess.run([PYTHON, str(entry or BASE/'17592186124630.py'), *map(str,args)],
                          cwd=cwd, capture_output=True, text=True)


def rank(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    pivot = 0
    for j in range(len(a[0])):
        found = next((i for i in range(pivot,len(a)) if a[i][j]), None)
        if found is None: continue
        a[pivot],a[found]=a[found],a[pivot]
        factor = a[pivot][j]
        a[pivot]=[x/factor for x in a[pivot]]
        for i in range(len(a)):
            if i!=pivot:
                factor=a[i][j]
                a[i]=[x-factor*y for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a): break
    return pivot


def value(term,n,r):
    # Parse rendered expressions, without generator target/profile metadata.
    term=term.strip()
    if term=='invertible': return ('property','invertible')
    if term==r'\text{invertible}': return ('property','invertible')
    if term=='n+1': return ('scalar',n+1)
    if term in ('not invertible','diagonal','not identity','identity'): return ('property',term)
    if term=='n': return ('scalar',n)
    if term=='0': return ('scalar',0)
    if term==r'\mathbb{R}^{n}': return ('space','full')
    if term==r'\{0\}': return ('space','zero')
    if term==r'\operatorname{Col}(A)': return ('space','full' if r==n else 'zero' if r==0 else 'proper-column')
    if term==r'\operatorname{Null}(A)': return ('space','zero' if r==n else 'full' if r==0 else 'proper-null')
    if term in (r'\dim(\operatorname{Col}(A))', r'\operatorname{rank}(A)'): return ('scalar',r)
    if term in (r'\dim(\operatorname{Null}(A))', r'\operatorname{nullity}(A)'): return ('scalar',n-r)
    raise AssertionError('Unparsed visible term: '+term)


HOLE = r'\underline{\phantom{WWWW}}'

def visible(record):
    p=record['question'][':question/problem']
    block=p.split('$$')[1].strip().removeprefix(r'\begin{gathered}').removesuffix(r'\end{gathered}')
    assert block.count(HOLE)==1
    prop,rows=block.split(r' \\ \Updownarrow \\ \left\{\begin{aligned}')
    assert prop.startswith(r'A\text{ is }')
    rows=rows.removesuffix(r'\end{aligned}\right.').split(r' \\ ')
    assert len(rows)==4
    return prop.removeprefix(r'A\text{ is }'),rows


def oracle(record, candidate):
    prop,rows=visible(record)
    for n in (1,2,3,5):
        for kind in ('identity','triangular','zero','singular'):
            a=[[int(i==j)*(0 if kind=='zero' or (kind=='singular' and i==n-1) else 2)
                +int(kind=='triangular' and j==i+1) for j in range(n)] for i in range(n)]
            r=rank(a)
            p=prop.replace(HOLE,candidate)
            property_value = value(p,n,r)
            if property_value[0]!='property': return False
            lhs = {'invertible':r==n, 'not invertible':r!=n,
                   'diagonal':all(a[i][j]==0 for i in range(n) for j in range(n) if i!=j),
                   'identity':all(a[i][j]==int(i==j) for i in range(n) for j in range(n)),
                   'not identity':any(a[i][j]!=int(i==j) for i in range(n) for j in range(n))}[property_value[1]]
            right=True
            for row in rows:
                terms=row.replace(HOLE,candidate).replace('&','').split('=')
                vals=[value(t,n,r) for t in terms]
                right &= all(v==vals[0] for v in vals)
            if right != lhs: return False
    return True


def validate(records):
    cases=[]
    for rec in records:
        q=rec['question'];f=q[':question/answer-fields'][0]
        assert len(f[':answer-field/choices'])==5
        truths=[]
        checks=[]
        for a in f[':answer-field/choices']:
            truth=oracle(rec,a[':answer/value'])
            checks.append({'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if truth else 'rejected',
                           'purpose':'typed mathematical witness, dimensions 1,2,3,5; invertible and singular matrices'})
            if truth: truths.append(a)
        assert len(truths)==1,(rec['generation'],truths)
        assert f[':answer-field/correct']==[':answer/id',truths[0][':answer/id']]
        v=truths[0][':answer/value']
        prop,rows=visible(rec)
        completion=q[':question/problem'].split('$$')[1].strip().replace(HOLE, r'\text{invertible}' if v=='invertible' else v)
        assert completion in q[':question/worked-solution']
        assert ('"invertible".' if v=='invertible' else '$'+v+'$.') in q[':question/worked-solution']
        cases.append({'label':rec['generation']['target']+'/'+rec['generation']['bank_profile'], 'record':rec,'checks':checks})
    return cases


def coverage(records):
    groups=defaultdict(list)
    positions=Counter()
    for rec in records:
        f=rec['question'][':question/answer-fields'][0]
        key=f[':answer-field/correct'][1]
        a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==key)
        bank=tuple(sorted(x[':answer/value'] for x in f[':answer-field/choices']))
        groups[bank].append(a[':answer/value'])
        positions[next(i for i,x in enumerate(f[':answer-field/choices']) if x[':answer/id']==key)]+=1
    stats=[]
    for bank,keys in groups.items():
        counts=Counter(keys)
        if bank == tuple(sorted(['invertible','not invertible','diagonal','not identity','identity'])):
            assert list(counts)==['invertible']
            stats.append({'bank':bank,'answers':dict(counts),'fixed_fact':'Source adjective contract: invertible is the property characterized by this theorem. No alternative property is in scope; use the complete five-adjective source bank, not a single grammatically eligible option.'})
            continue
        assert len(counts)==4, ('bank predicts part of answer',bank,counts)
        stats.append({'bank':bank,'answers':dict(counts),'best_bank_only_strategy':max(counts.values())/len(keys),'uniform_choice_baseline':0.2, 'eligible_target_baseline':0.25})
    assert set(positions)==set(range(5)),positions
    return {'records':len(records),'semantic_targets':len({r['generation']['target'] for r in records}),
            'correct_positions':dict(positions),'bank_groups':stats,
            'mathematical_invariants':'The missing location is relevant evidence; the full theorem and its fixed correct fragments are the assessed finite recognition skill.'}


def main(delivery=False):
    commands=[]
    for count in (0,1,5,11):
        r=cli('--difficulty','easy','--count',count,'--seed',0,'--format','json')
        assert r.returncode==0,r.stderr
        data=json.loads(r.stdout)
        assert isinstance(data,list) and len(data)==count
        assert len({x['generation']['target'] for x in data})==count
        assert data==g.generate('easy',count,0)
    for args in [('--count',12),('--count',-1),('--difficulty','moderate'),('--difficulty','hard')]:
        r=cli(*args);assert r.returncode!=0
        if args==('--count',12):assert 'Finite limit: 11' in r.stderr
    sampled=[r for seed in (0,1,4) for r in g.generate('easy',11,seed)]
    assert len({(r['generation']['target'],r['generation']['bank_profile']) for r in sampled})==13
    validate(sampled)
    save('sampled-pool.json',sampled)
    sample=g.generate('easy',5,0)
    validate(sample)
    save('sample.json',sample)
    records=[]
    for profile_index,(profile,targets) in enumerate(g.BANKS.items()):
        for i,target in enumerate(targets):
            # Rotate all five response positions, independently of target values.
            rec=g.make_record(target,profile,0)
            f=rec['question'][':question/answer-fields'][0]
            pos=next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
            shift=(pos-i-profile_index)%5
            f[':answer-field/choices']=f[':answer-field/choices'][shift:]+f[':answer-field/choices'][:shift]
            records.append(rec)
    cases=validate(records)
    save('assignments.json',records)
    save('grader-input.json',cases)
    save('coverage-before.json',coverage(records))
    # Exact source replay, including every source bank and the original difficulty.
    source=json.load(open(BASE.parent/'source/source.json'))['material']['kp']
    assert source==g.SOURCE
    fidelity=[];replays=[]
    for q in source[':knowledge-point/questions']:
        sid=q[':question/math-academy-id'];r=g.replay(sid);rq=r['question']
        assert rq[':question/problem']==q[':question/problem']
        assert rq[':question/worked-solution']==q[':question/worked-solution']
        assert rq[':question/difficulty']==q[':question/difficulty'][':db/ident']
        f=rq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        assert [(a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']]==[(a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices']]
        actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert actual==sf[':answer-field/correct'][':answer/value']
        assert f[':answer-field/key']==sf[':answer-field/key']
        assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        fidelity.append({'source':sid,'source_question_uuid':q[':question/id'],'matched_choices':5,'matched_distractors':4,'complete_bank':True})
        replays.append(r)
    save('source-replays.json',replays);save('source-fidelity.json',fidelity)
    # Source evidence changed: old missing-marker cases really are visible now.
    for sid in ('q-141343','q-141192','q-142302'):
        assert r'\underline{\phantom{' in g.SOURCES[sid][':question/problem']
    # Retain independent witnesses to every earlier ambiguous-bank observation.
    # The new profiles cannot contain these colliding pairs.
    for n in (1,2,3,5):
        inv=[[2*int(i==j) for j in range(n)] for i in range(n)]
        assert rank(inv)==n  # inverse and all positive powers are diagonal nonzero too
        inverse=[[Fraction(int(i==j),2) for j in range(n)] for i in range(n)]
        power=[[2**n*int(i==j) for j in range(n)] for i in range(n)]
        assert rank(inverse)==rank(power)==rank(inv)
        assert n-rank(inverse)==n-rank(inv)==0
    # Direct visible source-expression duplicates, not a source-key assertion.
    banks={sid:[a[':answer/value'].replace('\\\\','\\') for a in q[':question/answer-fields'][0][':answer-field/choices']] for sid,q in g.SOURCES.items()}
    assert 'n' in banks['q-141192'] and '{n}' in banks['q-141192']
    assert '1' in banks['q-141192'] and '{1}' in banks['q-141192']
    assert r'\text{dim(Col}({A}^{-1}))' in banks['q-141343'] and r'\text{dim(Col}(A))' in banks['q-141343']
    assert all(x in banks['q-142357'] for x in [r'\text{Col}(A)',r'\text{Col}({A}^{-1})',r'\text{Col}({A}^{n})'])
    assert all(x in banks['q-141345'] for x in [r'\text{Null}(A)',r'\text{Null}({A}^{-1})'])
    # Relocation: copy only declared runtime files to a temporary root and run there.
    manifest=json.load(open(BASE/'package.json'))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for f in manifest['files']:
            target=root/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(BASE/f,target)
        p=cli('--count',5,'--seed',0,'--format','json',cwd=root,entry=root/manifest['entrypoint'])
        assert p.returncode==0,p.stderr
        assert json.loads(p.stdout)==sample
    inventory=json.load(open(BASE.parent/'source/inventory.json'))
    original_ids={q[':question/id'] for q in source[':knowledge-point/questions']}
    assert len(inventory['questions'])==16
    assert all(q[':question/id'] in original_ids for q in inventory['questions'])
    save('inventory-audit.json',{'inventory_basis':inventory['basis'],'inspected':16,'original_sources':16,
        'generated_records':0,'affected_generated_records':0,'conclusion':'Verified absence of generated inventory records at captured basis. The count failure is an execution defect; source ambiguities are retained separately and sources are not relabeled generated.'})
    (BASE/'affected-inventory.json').write_text('{"affected_questions": []}\n')
    if delivery:
        cmd=[PYTHON,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(OUT/'assignments.json'),
             '--source',str(BASE.parent/'source/source.json'),'--inventory',str(BASE.parent/'source/inventory.json'),
             '--difficulty','easy','--output',str(OUT/'delivery'),'--asset-root',str(OUT),'--math-root','/media/jake/SSD/EDB/math']
        r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
        commands.append({'command':cmd,'result':r.stdout})
        accepted=json.load(open(OUT/'delivery/accepted.json'));assert len(accepted)==13
        validate(accepted);save('coverage-after.json',coverage(accepted))
        # A repeated batch is actually removed by shared within-batch deduplication.
        save('duplicate-probe.json',records[:1]*2)
        cmd[cmd.index(str(OUT/'assignments.json'))]=str(OUT/'duplicate-probe.json')
        cmd[cmd.index(str(OUT/'delivery'))]=str(OUT/'delivery-duplicates')
        r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
        report=json.load(open(OUT/'delivery-duplicates/delivery.json'))
        assert report['duplicate_count']==1 and report['accepted_count']==1
        commands.append({'command':cmd,'result':r.stdout})
        cmd[cmd.index(str(OUT/'duplicate-probe.json'))]=str(OUT/'sampled-pool.json')
        cmd[cmd.index(str(OUT/'delivery-duplicates'))]=str(OUT/'delivery-sampled')
        r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
        sampled_accepted=json.load(open(OUT/'delivery-sampled/accepted.json'))
        assert len(sampled_accepted)==13
        validate(sampled_accepted)
        save('coverage-sampled-before.json',coverage(sampled))
        save('coverage-sampled-after.json',coverage(sampled_accepted))
        commands.append({'command':cmd,'result':r.stdout})
    # Relevant counterfactuals: same full theorem, same complete bank, moved blank.
    for profile in g.BANKS:
        same=[r for r in records if r['generation']['bank_profile']==profile]
        keys=[]
        for r in same:
            f=r['question'][':question/answer-fields'][0]
            keys.append(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
        assert len(set(keys))==len(same)
    # Irrelevant counterfactual: choice order changes neither mathematical key nor IDs.
    for r in records:
        r2=g.make_record(r['generation']['target'],r['generation']['bank_profile'],31)
        f=r['question'][':question/answer-fields'][0];f2=r2['question'][':question/answer-fields'][0]
        assert f[':answer-field/correct']==f2[':answer-field/correct']
        assert r['question'][':question/problem']==r2['question'][':question/problem']
        assert r['question'][':question/id']==r2['question'][':question/id']
    save('validation.json',{'passed':True,'source_banks':16,'matched_choices':80,'matched_distractors':64,
        'count_failure_reproduced_before':'before.json','count_contract':[0,1,5,11], 'finite_limit_rejected':12,
        'mathematical_records':13,'oracle_checks':65,'matrix_dimensions':[1,2,3,5],
        'counterfactuals':{'relevant':'12 mathematical assignments with four changing answers per complete bank; one fixed source adjective contract','irrelevant':'all 13 option-order changes preserve prompt, correct answer identity and question identity'},
        'relocation_passed':True,'delivery_checked':delivery,'commands':commands})
    print(json.dumps({'passed':True,'source_banks':16,'assignments':13,'grader_cases':65,'delivery_checked':delivery}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--delivery',action='store_true');main(p.parse_args().delivery)
