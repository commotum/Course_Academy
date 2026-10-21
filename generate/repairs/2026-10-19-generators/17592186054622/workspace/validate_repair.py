#!/usr/bin/env python3
"""Reproducible independent checks; run with the job's Python, from workspace."""
import collections
import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import sys
import sympy as sp
import generator as g

ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence'
REPO=Path('/home/jake/Developer/Course_Academy')
PYTHON=REPO/'.venv/bin/python'
k=sp.Symbol('k')

def save(name,data):
    (E/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def key(r):
    f=r['question'][':question/answer-fields'][0]
    ref=f[':answer-field/correct']; ident=ref[1] if isinstance(ref,list) else ref
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ident)

def expr(s):
    return sp.sympify(re.sub(r'(\d)k',r'\1*k',s))

def expected(r):
    p=r['generation']['parameters']
    if r['generation']['template']=='numeric':
        return sum(exponent*value for exponent,value in zip([p['a'],p['b']],[p['u'],p['v']]))
    return sp.expand(sum(p[zexp]*(k if p['symbol']==z else p['n']) for z,zexp in [('x','a'),('y','b')]))

def canonical(s):
    # Only syntactic normalization for replay, no inferred mathematical equivalence.
    s=s.replace('⁡','').replace('{log}',r'\log').replace(r'\left','').replace(r'\right','')
    return re.sub(r'[\s{}]','',s)

def check_record(r):
    wanted=expected(r)
    assert sp.expand(expr(key(r))-wanted)==0
    f=r['question'][':question/answer-fields'][0]
    answers=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(map(str,answers)))==5
    assert sum(sp.expand(v-wanted)==0 for v in answers)==1
    p=r['generation']['parameters']; base=p['base']
    target=g.log(base,g.power('x',p['a'])+g.power('y',p['b']))
    q=r['question']; assert target in q[':question/problem'] and target in q[':question/worked-solution']
    assert key(r) in q[':question/worked-solution']
    assert g.weighted(p,'x')+'+'+g.weighted(p,'y') in q[':question/worked-solution']
    # Independent exponent identity with positive arguments, including signed logarithms.
    if r['generation']['template']=='numeric':
        x,y=sp.Rational(base)**p['u'],sp.Rational(base)**p['v']
        assert x**p['a']*y**p['b']==sp.Rational(base)**wanted
    else:
        for trial in [-2,1,4]:
            u=trial if p['symbol']=='x' else p['n']; v=trial if p['symbol']=='y' else p['n']
            assert (sp.Rational(base)**u)**p['a']*(sp.Rational(base)**v)**p['b']==sp.Rational(base)**wanted.subs(k,trial)


def replay():
    definitions=[('expand',dict(c=5,z='p',p=3)),('condense',dict(a=3,b=2,base=2)),
      ('numeric',dict(a=2,b=3,u=3,v=2,base=5)),('symbolic',dict(a=1,b=3,symbol='x',n=4,base=2))]
    originals=json.loads((E/'source-cases.json').read_text()); records=[]; reports=[]
    for q,(family,p) in zip(originals,definitions):
        r=g.build(family,p); records.append(r)
        sf=q[':question/answer-fields'][0]; gf=r['question'][':question/answer-fields'][0]
        src=collections.Counter(canonical(a[':answer/value']) for a in sf[':answer-field/choices'])
        dst=collections.Counter(canonical(a[':answer/value']) for a in gf[':answer-field/choices'])
        assert src==dst,(family,src,dst)
        assert canonical(q[':question/problem'])==canonical(r['question'][':question/problem'])
        if ':answer-field/correct' in sf:
            assert canonical(sf[':answer-field/correct'][':answer/value'])==canonical(key(r))
            assert q[':question/difficulty'][':db/ident']==r['question'][':question/difficulty']
            check_record(r)
        reports.append({'source':q[':question/math-academy-id'],'source_uuid':q[':question/id'],
             'prompt_math_and_wording_match':True,'matched_choices':5,'total_choices':5,
             'matched_distractors':4 if ':answer-field/correct' in sf else None,
             'recorded_key_verified':':answer-field/correct' in sf,
             'missing_source':[] if ':question/worked-solution' in q else ['key','solution','difficulty'],
             'solution':'same law list, expansion, substitution, conclusion' if family in ('numeric','symbolic') else 'authored completion, not observed'})
    save('source-replay.json',reports); save('source-replay-records.json',records)
    return records


def run():
    source_records=replay()
    rng=random.Random(90817)
    records=[g.generate(rng) for _ in range(64)]
    controls=[];proof=[]
    for family in ['numeric','symbolic']:
        for seed in [59,83,137,181]:
            roles=g.draw_role_bank(random.Random(seed),family)
            group=[g.build_role_bank(family,roles,key) for key in range(5)]
            banks=[[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']] for r in group]
            assert all(bank==banks[0] for bank in banks)
            keys=[key(r) for r in group];assert len(set(keys))==5
            assert all(keys.count(value)==1 for value in banks[0])
            if family=='symbolic':
                subgroup={(p['symbol'],'x' if p['a']>1 else 'y',p['n']>0) for p in roles}
            else:subgroup={(p['u']>0,p['v']>0) for p in roles}
            assert len(subgroup)==1
            proof.append({'family':family,'subgroup':str(subgroup),'seed':seed,'correct_values':keys,
                          'any_fixed_bank_only_strategy_correct':1,'total':5,'baseline':0.2})
            controls.extend(group)
    records+=controls
    checks=[];coverage=collections.Counter()
    for r in records:
        check_record(r)
        f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
        checks.append({'label':r['question'][':question/id'],'record':r,'checks':[
            {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected'}
            for a in f[':answer-field/choices']]})
        p=r['generation']['parameters'];family=r['generation']['template']
        coverage[family]+=1
        if family=='symbolic':coverage[str((p['symbol'],'x' if p['a']>1 else 'y',p['n']>0))]+=1
    save('samples.json',records);save('grader-input.json',checks)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],check=True)
    subprocess.run([str(PYTHON),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'samples.json'),
                    '--source',str(ROOT.parent/'source/source.json'),'--inventory',str(ROOT.parent/'source/inventory.json'),
                    '--difficulty','hard','--output',str(E/'delivery')],check=True)
    accepted=json.loads((E/'delivery/accepted.json').read_text());assert len(accepted)>=64
    with tempfile.TemporaryDirectory() as tmp:
        for name in json.loads((ROOT/'package.json').read_text())['files']:shutil.copy2(ROOT/name,Path(tmp)/name)
        cmd=[str(PYTHON),'-B',str(Path(tmp)/'generator.py'),'--difficulty','hard','--count','5','--seed','99317','--format','json']
        one=subprocess.check_output(cmd,cwd=tmp);two=subprocess.check_output(cmd,cwd=tmp)
        assert one==two and len(json.loads(one))==5
    render=[source_records[2]]
    for family in ['numeric','symbolic']:
        render.append(next(r for r in records if r['generation']['template']==family))
    for symbol in ['x','y']:
        render.append(next(r for r in records if r['generation']['template']=='symbolic' and r['generation']['parameters']['symbol']==symbol and r['generation']['parameters']['n']<0))
    save('render-input.json',render)
    save('counterfactual-cue-proof.json',proof)
    save('validation-summary.json',{'passed':True,'source_banks':4,'questions':len(records),
                                  'grading_checks':len(records)*5,'accepted_after_delivery':len(accepted),
                                  'coverage':coverage,'relocation_and_determinism':True,'conditional_bank_proofs':proof})
    print(json.dumps({'passed':True,'questions':len(records),'delivery':len(accepted),'coverage':coverage}))


if __name__=='__main__':run()


