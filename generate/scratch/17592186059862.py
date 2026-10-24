#!/usr/bin/env python3
"""Bounded source-derived constant-multiple power derivative generator."""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186059862-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059862
KP_UUID='ffc1d505-17e4-5b0f-9150-506f9edb3350'
TITLE='Differentiating a Power Function Using the Constant Multiple Rule'
VERSION='constant-power-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def mon(c,n):
 c=sp.Rational(c);n=int(n)
 if n==0:return sp.latex(c)
 x='x' if n==1 else 'x^{'+str(n)+'}'
 return ('' if c==1 else '-' if c==-1 else sp.latex(c))+x

def bank(c,n,profile):
 if profile=='q-1214':return [mon(c*n,n+1),mon(c*n,n),mon(c*n,n-1),mon(c*(n+1),n+1),mon(1,n-1)],2
 if profile=='q-272':return [mon(c*n,n-1),mon(c*n,n),mon(c*n*(n-1),n-2),mon(c+n,n-1),r'\frac{'+mon(c,n+1)+'}{'+str(n)+'}'],0
 raise ValueError('Unknown complete source profile')
def fingerprint_parameters(level,p):
 return digest(['power',p[0],p[1]] if level=='easy' else ['root',str(sp.Rational(p[0]))])
def candidates(profile):
 if profile in ('q-1214','q-272'):
  return [[c,n] for c in range(2,13) for n in range(2,10) if not(c+n==c*n)]
 return [[str(sp.Rational(k,3)),3] for k in range(1,37)]
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported hard; see capabilities.json')
 rng=random.Random(seed);sid=template or (rng.choice(['q-1214','q-272']) if difficulty=='easy' else 'root-blank')
 if (sid in ('q-1214','q-272'))!=(difficulty=='easy'):raise ValueError('profile level mismatch')
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if difficulty=='easy':
  c,n=map(int,p);assert [c,n] in candidates(sid)
  prompt='Find the derivative of $f(x) = '+mon(c,n)+'$.'
  values,correct=bank(c,n,sid);key='selection';kind='radio'
  solution='We apply the constant multiple and power rules, as follows:\n\n$$\n'+r'\begin{aligned}'+'\n'+r"f^{′}(x) &= \frac{d}{dx}("+mon(c,n)+r') \\'+'\n'+r'&= '+str(c)+r' \cdot \frac{d}{dx}(x^{'+str(n)+r'}) \\'+'\n'+r'&= '+str(c)+r' \cdot '+str(n)+r'x^{'+str(n-1)+r'} \\'+'\n'+r'&= '+mon(c*n,n-1)+'\n'+r'\end{aligned}'+'\n$$'
 else:
  c=sp.Rational(p[0]);b=int(p[1]);assert c in [sp.Rational(k,3) for k in range(1,37)] and b in (3,-1)
  function=sp.latex(c)+r'\sqrt{x}'+('+' if b>=0 else '')+str(b)
  value=r'\frac{'+sp.latex(c/2)+r'}{\sqrt{x}}' if c!=2 else r'\frac{1}{\sqrt{x}}'
  if c/2==sp.Rational(1,3):value=r'\frac{1}{3\sqrt{x}}'
  # Corrected explicit input and consistent function label from source solution.
  prompt='Find the derivative of $g(x)='+function+'.$\n\n'+r'${g}^{′}(x)\,=\,$'+'\n{{field-1}}'
  values=[value];correct=0;key='field-1';kind='blank'
  solution='We apply the sum, constant multiple, and power rules as follows:\n\n$$\n'+r'\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}('+function+r') \\  & ='+sp.latex(c)+r'\cdot \frac{\text{d}}{\text{d}x}(\sqrt{x})'+('+' if b>=0 else '-')+r'\frac{\text{d}}{\text{d}x}('+str(abs(b))+r') \\  & ='+sp.latex(c)+r'\cdot \frac{\text{d}}{\text{d}x}({x}^{1/2}) \\  & ='+sp.latex(c)+r'\cdot \frac{1}{2}{x}^{(\frac{1}{2}-1)} \\  & ='+sp.latex(c/2)+r'{x}^{-1/2} \\  & ='+value+r'\end{aligned}'+'\n$$'
 fp=fingerprint_parameters(difficulty,p);qid=ident(['question',VERSION,fp,sid]);fid=ident([qid,key]);choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':[sid] if difficulty=='easy' else ['q-142993','q-167561'],'domain':'x real' if difficulty=='easy' else 'x > 0','mathematical_fingerprint':fp,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 pairs=[(s,p) for s in (['q-1214','q-272'] if difficulty=='easy' else ['root-blank'] if difficulty=='moderate' else []) for p in candidates(s)];random.Random(seed).shuffle(pairs);out=[];seen=set()
 for s,p in pairs:
  r=generate(difficulty,seed,s,p);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('Unsupported level or finite distinct family exhausted')

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186059862-source-policy.json'))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',default='json',choices=['json','markdown']);p=a.parse_args();r=batch(p.difficulty,p.count,p.seed);print(json.dumps(r,indent=2) if p.format=='json' else '\n\n---\n\n'.join(z['question'][':question/problem']+'\n\n'+z['question'][':question/worked-solution'] for z in r))
