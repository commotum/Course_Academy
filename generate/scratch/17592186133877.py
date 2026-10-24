#!/usr/bin/env python3
"""Bounded source-faithful curl generator. Pure generation; no database access.

Easy: vary the coefficient of z² in q-105668. Moderate: vary the two
curl-relevant coordinates in q-131340. Other complete profiles replay only.
No hard source supports a hard-level claim. See the adjacent extraction.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133877-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 for p in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):sys.path.insert(0,str(p))
 import sympy as sp
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186133877;KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='curl-source-banks-1'
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate')
PROFILES={sid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1], 'observed':3 if sid=='q-105668' else [-2,1] if sid=='q-131340' else 1, 'domain':list(range(1,13)) if sid=='q-105668' else [[x,z] for x in range(-4,0) for z in range(1,5)] if sid=='q-131340' else [1]} for sid,q in SOURCES.items() if sid not in ('q-41883','q-41899','q-168621')}
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(value,sort_keys=True)))
def fingerprint(problem):
 # Exact functions/points change; identity, seed and choice order never participate.
 s=problem.replace('⁡','').replace(r'\,','').replace(r'\text{curl}','curl').replace('{','').replace('}','')
 return hashlib.sha256(re.sub(r'\s+','',s).encode()).hexdigest()
def vector(v):
 i,j,k=sp.symbols('i j k');return sp.latex(sp.expand(sum(a*b for a,b in zip(v,(i,j,k)))))
def recipes(sid,p):
 if sid=='q-105668':
  z=sp.Symbol('z');a=p
  return [(0,0,-2*a*z),(2,0,0),(0,0,0),(0,2*a*z,0),(0,-2*a*z,2)]
 if sid=='q-131340':
  x,z=p;y=-3
  return [(-x,0,z),(0,-x,y),(-z,0,x),(-y,z,0),(0,z,z)]
 raise ValueError('Replay-only profile has no inferred variation recipes')
def generate(difficulty,seed=0,template=None,parameter=None):
 eligible=[s for s,t in PROFILES.items() if t['level']==difficulty]
 if not eligible:raise ValueError('unsupported difficulty: '+difficulty)
 rng=random.Random(seed);sid=template or rng.choice(eligible);assert sid in eligible,'Template difficulty mismatch'
 t=PROFILES[sid];p=copy.deepcopy(rng.choice(t['domain']) if parameter is None else parameter)
 if p not in t['domain'] or isinstance(p,bool):raise ValueError('Outside validated bounded domain')
 src=SOURCES[sid];problem=src[':question/problem'];solution=src[':question/worked-solution']
 original=p==t['observed'];bank0=src[':question/answer-fields'][0][':answer-field/choices']
 values=[a[':answer/value'] for a in bank0]
 if sid=='q-105668':
  problem=problem.replace('3{z}^{2}',str(p)+'{z}^{2}')
  solution=solution.replace('3{z}^{2}',str(p)+'{z}^{2}').replace('6z',str(2*p)+'z')
  if not original:values=[vector(v) for v in recipes(sid,p)]
 elif sid=='q-131340' and not original:
  x,z=p;point=f'({x},-3,{z})'
  problem=problem.replace('(-2,-3,1)',point)
  solution=solution.replace('(-2,-3,1)',point).replace('-(-2)',f'-({x})').replace('+(1)',f'+({z})').replace(r'=2\,i+\,k.', '= '+vector((-x,0,z))+'.')
  values=[vector(v) for v in recipes(sid,p)]
 key=fingerprint(problem);qid=uid(['mathematical-task',key]);old=src[':question/answer-fields'][0];fid=uid([qid,'selection']);bank=[];correct=None
 for a,value in zip(bank0,values):
  aid=uid([fid,value]);bank.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  if a[':answer/id']==old[':answer-field/correct'][':answer/id']:correct=aid
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':bank,':answer-field/correct':[':answer/id',correct]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid+'-observed-bank','parameter':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'mathematical_fingerprint':key,'dependencies':{'sympy':sp.__version__},'sampling_policy':'a=1..12' if sid=='q-105668' else 'x=-4..-1,z=1..4,y=-3 fixed' if sid=='q-131340' else 'source-only: no inferred new bank','plot_rating':'none','eligible_for_learning':True}}
def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty: '+difficulty)
 cases=[(s,p) for s,t in PROFILES.items() if t['level']==difficulty for p in t['domain']]
 if count<1 or count>len(cases):raise ValueError(f'finite-limit: {len(cases)} tasks at {difficulty}')
 random.Random(seed).shuffle(cases);return [generate(difficulty,seed,s,p) for s,p in cases[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133877-source-policy.json'))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');a=parser.parse_args()
 try:rows=batch(a.difficulty,a.count,a.seed)
 except ValueError as e:parser.error(str(e))
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
