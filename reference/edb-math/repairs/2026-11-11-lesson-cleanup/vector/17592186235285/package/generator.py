#!/usr/bin/env python3
"""Seeded signed scalar-factor practice; source replay and authored error banks."""
from __future__ import annotations
import argparse, hashlib, itertools, json, os, random, uuid
from pathlib import Path
from fractions import Fraction as F
from math_format import normalize_prose, normalize_tex, validate_generated_record
from plot import render_plots
KP_ID=17592186235285
KP_UUID='58a49d00-cc58-5228-af38-9369cf31d8c8'
VERSION='direction-reversal-v3-independent'
HERE=Path(__file__).resolve().parent
# Each tuple is a complete authored profile, chosen before geometry/values.
ERRORS=('sign','reciprocal','omit_reference','under_path','over_path','under_reference','over_reference')
NEGATIVE_ERRORS=('reciprocal','under_path','over_path','under_reference','over_reference')
PROFILES=tuple(('omit_reference',)+x for x in itertools.combinations(NEGATIVE_ERRORS,3))+tuple(('sign',x,'opposite_'+x,'omit_reference') for x in NEGATIVE_ERRORS if x!='reciprocal')

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(x)))
def tex(x):
 x=F(x)
 return str(x.numerator) if x.denominator==1 else ('-' if x<0 else '')+rf'\frac{{{abs(x.numerator)}}}{{{x.denominator}}}'
def term(x,var):
 x=F(x);return ('-' if x==-1 else '' if x==1 else tex(x))+var

def finalize(level,prompt,solution,values,field,rng,meta):
 prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 values=[normalize_tex(v) for v in values]
 identity=digest([VERSION,level,prompt,solution,field,sorted(values)])
 fid=uid(identity+':field')
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[0][':answer/id'];rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection' if field=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+field,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Finding a Scalar Factor When Direction Reverses'},'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[f]},'generation':{'version':VERSION,**meta}}
 return validate_generated_record(record)

def error_values(p,profile):
 r=F(p['r']);A=max(map(abs,p['a']));L=r*A
 choices={'sign':r,'reciprocal':-1/r,'omit_reference':-L,'under_path':-(L-1)/A,'over_path':-(L+1)/A,'under_reference':-L/(A-1),'over_reference':-L/(A+1)}
 choices.update({'opposite_'+n:-choices[n] for n in NEGATIVE_ERRORS})
 return [-r]+[choices[n] for n in profile]

def sample_parameters(level,rng):
 # First choose the assessed residual ratio and known component case.
 r=rng.choice([F(1),F(2),F(3),F(4)] if level!='hard' else [F(i,2) for i in range(1,9)])
 k=rng.choice([1,2,3,4] if level=='hard' else [2,3,4])*(-1 if level=='hard' else 1)
 scale=rng.choice([2,4]) if r.denominator==2 else rng.choice([2,3,4])
 direction=rng.choice([(1,0),(-1,0),(0,1),(0,-1)] if level=='easy' else [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)])
 a=[scale*x for x in direction]
 bs=[(1,1),(1,2),(2,1),(-1,2),(-2,1),(-1,-1),(-1,-2),(1,-2)]
 b=list(rng.choice([v for v in bs if a[0]*v[1]-a[1]*v[0]]))
 return {'a':a,'b':b,'k':str(k),'r':str(r)}

def generate(level,seed=0,*,parameters=None,field_type=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);field=field_type or rng.choice(['radio','blank'])
 if field not in ('radio','blank'):raise ValueError('Unknown field')
 chosen=tuple(profile) if profile is not None else rng.choice(PROFILES)
 for attempt in range(300):
  p=dict(parameters) if parameters is not None else sample_parameters(level,rng)
  r=F(p['r']);k=F(p['k']);a=p['a'];b=p['b'];A=max(map(abs,a));L=r*A
  if not (0<r<=4 and r.denominator in (1,2) and k in (-4,-3,-2,-1,1,2,3,4) and a[0]*b[1]!=a[1]*b[0] and L.denominator==1 and A>1):raise ValueError('Invalid geometry')
  values=[-r] if field=='blank' else error_values(p,chosen)
  if len(set(values))==len(values):break
  if parameters is not None:raise ValueError('Complete error bank collides')
 else:raise ValueError('No eligible instance for complete profile')
 assets=render_plots(p)
 av=r'\mathbf{a}';bv=r'\mathbf{b}';cv=r'\mathbf{c}'
 kb=term(k,bv);ra=term(-r,av);eq=cv+r'=\lambda'+av+('+' if k>0 else '')+kb
 prompt='The three vectors share an origin, and each grid square has the same side length.\n\n'+f'![]({assets["prompt"]})\n\n'
 prompt+=rf'Given ${eq}$, find $\lambda$.' if field=='radio' else rf'If ${eq}$, then $\lambda=$ '+'{{field-1}}.'
 reversal='reverse its direction and scale its length' if k<0 else 'keep its direction and scale its length'
 solution=rf'''First trace ${kb}$ from the common origin $O$ to a point $P$: {reversal}. The remaining path from $P$ to the endpoint $C$ must be the unknown multiple of ${av}$.

![]({assets['solution']})

Following the grid direction of ${av}$ takes ${A}$ steps, while the parallel path $PC$ has ${tex(L)}$ steps. Their length ratio is $\frac{{{tex(L)}}}{{{A}}}={tex(r)}$. The remaining path points in the opposite direction to ${av}$, so
$$
\overrightarrow{{PC}}={ra}.
$$
Adding the path vectors gives
$$
\begin{{aligned}}
{cv}&=\overrightarrow{{OP}}+\overrightarrow{{PC}}\\
&={kb}+({ra})\\
&={ra}{'+' if k>0 else ''}{kb}.
\end{{aligned}}
$$
Because ${av}$ and ${bv}$ are nonparallel, these coefficients are unique. Comparing with ${eq}$ gives $\lambda={tex(-r)}$. The minus sign records the reversed direction.'''
 return finalize(level,prompt,solution,[tex(v) for v in values],field,rng,{'seed':seed,'template':'construct-'+field,'bank_profile':list(chosen) if field=='radio' else 'blank','parameters':p,'plot_assets':assets,'source':{'database':'math','basis':10545,'support':['tutorial-15990','e-26144']},'error_recipes':list(chosen) if field=='radio' else [],'rejections':attempt})

SOURCE_PROFILES={
'q-120254':['r-1/2','-r-1','r','-r','-r+1/2'],
'q-120257':['r','-2*r','1/r','2*r','-r'],
'q-120260':['-r+3/2','-r+1/2','-r+2','-r','-r+1'],
'q-367051':['-r/k','k','r','-k','-r'],
'q-367052':['-r','r','-2*r','1','-1/r'],
'q-367060':['-r-1/2','-r','-r+1/2','-r+1','-r-1'],
'q-70148':['r-1','-r+1','-r','r','-r+1/2'],
'q-77451':['-r','3*r/2','1/r','-1/r','r'],
'authored':['-r','r','-1/r','1/r','-r-1'],
'blank':['-r']}

def replay(source_id,seed=0):
 q=json.loads((HERE/'source-replay.json').read_text())[source_id]
 case=next(x for x in json.loads((HERE/'source-cases.json').read_text()) if x['source_id']==source_id)
 f=q[':question/answer-fields'][0];field=f[':answer-field/type'][':db/ident'].rsplit('/',1)[-1]
 import sympy as sp
 p=case['parameters'];r=sp.Rational(p['r']);k=sp.Rational(p['k'])
 values=[F(str(sp.sympify(expr,locals={'r':r,'k':k}))) for expr in SOURCE_PROFILES[case['bank_profile']]]
 styles=p.get('answer_style','fraction')
 def styled(v,i):
  st=styles[i] if isinstance(styles,list) else styles
  return str(float(v)) if st=='decimal' and v.denominator==2 else tex(v)
 pairs=[(v,styled(v,i)) for i,v in enumerate(values)]
 vals=[t for v,t in pairs if v==-F(p['r'])]+[t for v,t in pairs if v!=-F(p['r'])]
 return finalize(case['level'],q[':question/problem'],q[':question/worked-solution'],vals,field,random.Random(seed),{'seed':seed,'template':'source-'+case['template'],'bank_profile':case['bank_profile'],'parameters':case['parameters'],'source':{'database':'math','basis':10545,'question_ids':[q[':db/id']], 'math_academy_ids':[source_id]}})

def batch(level,count,seed):
 rng=random.Random(seed);out=[];seen=set();semantic_seen=set();cue_history={};outcome_history={}
 fields=['radio' if i%2==0 else 'blank' for i in range(count)];rng.shuffle(fields)
 # Spread distinct ratio/component calculations; when recurring visible banks
 # would teach one rank/position, select a counterexample from the same family.
 for index in range(count):
  if len(seen)==(32 if level=='hard' else 12):seen.clear()
  for attempt in range(2000):
   rec=generate(level,rng.getrandbits(64),field_type=fields[index]);p=rec['generation']['parameters'];sig=(p['r'],p['k'])
   import math
   scale=math.gcd(*[abs(v) for v in p['a']+p['b']]);semantic=(sig,tuple(v//scale for v in p['a']+p['b']))
   if sig in seen or semantic in semantic_seen:continue
   history=outcome_history.get(fields[index],[])
   if history and all(x==p['r'] for x in history):continue
   field=rec['question'][':question/answer-fields'][0];groups=[]
   if field[':answer-field/type'].endswith('/radio'):
    vals=[parse_value(a[':answer/value']) for a in field[':answer-field/choices']];v=-F(p['r']);rank=sorted(vals).index(v);position=vals.index(v)
    negative_integers=[x for x in vals if x<0 and x.denominator==1]
    min_integer=(bool(negative_integers) and v==max(negative_integers))
    max_integer=(bool(negative_integers) and v==min(negative_integers))
    groups=['radio', 'radio-'+('axis' if 0 in p['a'] else 'diagonal'),'radio-'+str(sum(x<0 for x in vals))+'neg']
    # This excludes a demonstrated batch cue, not a mathematical outcome.
    if any(len(cue_history.get(group,[]))>=1 and
      (all(t[0]==rank for t in cue_history[group]) or all(t[1]==position for t in cue_history[group]) or
       (min_integer and all(t[2] for t in cue_history[group])) or (max_integer and all(t[3] for t in cue_history[group])) or all(t[4]==v for t in cue_history[group])) for group in groups):continue
   break
  else:raise ValueError('Requested batch exceeds supported distinct calculations')
  seen.add(sig);semantic_seen.add(semantic);outcome_history.setdefault(fields[index],[]).append(p['r'])
  for group in groups:cue_history.setdefault(group,[]).append((rank,position,min_integer,max_integer,v))
  rec['generation']['batch_selection_rejections']=attempt;out.append(rec)
 return out

def parse_value(value):
 import re
 value=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'\1/\2',value)
 return F(value)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source');ns=ap.parse_args()
 if ns.count<0:ap.error('count must be nonnegative')
 level='moderate' if ns.difficulty=='unclassified' else ns.difficulty
 if ns.replay_source:records=[replay(ns.replay_source,ns.seed)]
 else:records=[r for l in (['easy','moderate','hard'] if level=='all' else [level]) for r in batch(l,ns.count,ns.seed)]
 print(json.dumps(records,indent=2))
if __name__=='__main__':main()
