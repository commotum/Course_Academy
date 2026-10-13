#!/usr/bin/env python3
"""Bounded source-bank generator for fractional-power substitution integrals."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064205
KP_UUID='0ae5760b-9277-596c-8546-dca4fd985bd7'
TITLE='Integrating an Algebraic Function With Fractional Exponent'
VERSION='fractional-affine-shifts-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def base(t,b):
 a=t['a'];v=t['variable'];ax=v if a==1 else str(a)+v
 if a<0:return str(b)+ax
 return ax+('+' if b>=0 else '')+str(b)
def candidates(sid):return [[b] for b in range(-100,101) if b!=0]
def fingerprint_parameters(t,b):return digest([t['a'],b,t['numerator'],t['denominator']])
def generate(difficulty='moderate',seed=0,template=None,parameters=None):
 if difficulty not in ('moderate','hard'):raise ValueError('Unsupported difficulty; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([s for s,t in PROFILES.items() if t['difficulty']==difficulty]);t=PROFILES[sid]
 if t['difficulty']!=difficulty:raise ValueError('Template difficulty mismatch')
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if p not in candidates(sid):raise ValueError('Outside validated shift bounds')
 b=p[0]
 def render(s):return s.replace('@@BASE@@',base(t,b)).replace('@@ALTERED@@',base(t,b-2))
 values=[render(z['value']) for z in t['bank']];fp=fingerprint_parameters(t,b)
 qid=ident(['question',VERSION,fp,sid,digest(sorted(values))]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in values]
 solution=render(t['solution'])
 # Source evidence is retained. Correct only the documented source exponent
 # typo and end-variable prose in generated instances.
 if sid=='q-17019':solution=solution.replace('^{3/2}','^{2/3}')
 solution=solution.replace('final answer in terms of $u$ at the very end','final answer in terms of $'+t['variable']+'$ at the very end')
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(z[':answer/id'] for z,r in zip(choices,t['bank']) if r['correct'])]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':[sid],'domain':'Real roots; even roots require base >= 0; reciprocal excludes base = 0. Differentiate on open intervals away from zero. Distractor even roots additionally require their radicands >= 0.','mathematical_fingerprint':fp,'sympy':sp.__version__,'sampling_policy':'shift-only; source slope and rational exponent fixed'}}
def batch(difficulty,count,seed):
 if difficulty not in ('moderate','hard'):raise ValueError('Unsupported difficulty; see capabilities.json')
 if count<1:raise ValueError('positive count required')
 pairs=[(s,p) for s,t in PROFILES.items() if t['difficulty']==difficulty for p in candidates(s)];random.Random(seed).shuffle(pairs);out=[];seen=set()
 for i,(s,p) in enumerate(pairs):
  r=generate(difficulty,seed+i,s,p);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('Finite validated family exhausted; shortage explicit')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for z in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();r=batch(a.difficulty,a.count,a.seed);print(json.dumps(r,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,r)))
