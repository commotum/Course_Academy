#!/usr/bin/env python3
"""Source-backed trig chain rule families. No database writes; bounded samplers."""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186064281-source-policy.json'))
    raise SystemExit(0)

import argparse, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
H=Path(__file__).with_suffix('');SOURCE=json.loads((H/'source.json').read_text())
KP_ID=17592186064281;KP_UUID=SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.1';SUPPORTED_LEVELS=('moderate','hard')
X=sp.Symbol('x',real=True)
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES={
 'q-310179':('moderate','tan-polynomial-blank',3,tuple(range(1,13))),
 'q-310180':('moderate','sin-special-slope-blank',3,tuple(range(1,13))),
 'q-31153':('moderate','sin-affine-slope-radio',5,tuple(range(1,13))),
 'q-31163':('moderate','cos-plus-cubic-radio',11,tuple(range(3,19))),
 'q-310182':('hard','sin-pi-quadratic-slope-blank',1,tuple(range(1,13))),
 'q-51026':('hard','cos-horizontal-tangent-radio',2,tuple(range(2,13))),
}
def tex(e):return sp.latex(e).replace(r'\operatorname{sec}',r'\sec')
def cos_cubic_inner(t):return str(t)+'-2x'
def answer_values(profile,t,bank):
 # Symbolic normal forms verify values and retain stable identities; they are
 # not an instructional rendering. In particular, SymPy rewrites sin(t-2*x)
 # to -sin(2*x-t), introducing a parity identity absent from this lesson.
 if profile=='q-31163':
  u=cos_cubic_inner(t)
  return [r'-2\sin('+u+r')-9x^{2}',r'-\cos('+u+r')-9x^{2}',
          r'\sin('+u+r')-18x^{2}',r'2\cos('+u+r')-18x^{2}',
          r'2\sin('+u+r')-18x^{2}']
 return [('y='+tex(b)) if profile=='q-51026' else tex(b) for b in bank]
def replace_all(text,mapping):
 mapping={k:v for k,v in mapping.items() if k!=v}
 if not mapping:return text
 return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)
def model(profile,t):
 if profile=='q-310179':
  u=t*X**4-5;f=sp.tan(u);answer=4*t*X**3*sp.sec(u)**2;bank=[answer];at=None
 elif profile=='q-310180':
  u=t*X;f=sp.sin(u);at=sp.pi/(2*t);answer=sp.Integer(0);bank=[answer]
 elif profile=='q-31153':
  u=3*X+t;f=sp.sin(u);at=sp.Integer(2);answer=3*sp.cos(6+t)
  bank=[answer,-answer,t*sp.cos(2),t*sp.cos(6+t),-t*sp.cos(6+t)]
 elif profile=='q-31163':
  u=t-2*X;f=sp.cos(u)-6*X**3;at=None;answer=2*sp.sin(u)-18*X**2
  bank=[-2*sp.sin(u)-9*X**2,-sp.cos(u)-9*X**2,sp.sin(u)-18*X**2,2*sp.cos(u)-18*X**2,answer]
 elif profile=='q-310182':
  u=sp.pi*(t*X**2+2*X-2);f=sp.sin(u);at=sp.Integer(1);answer=2*(t+1)*sp.pi*(-1)**t;bank=[answer]
 elif profile=='q-51026':
  u=X-1;f=t*sp.cos(u);at=1+sp.pi;answer=-sp.Integer(t)
  # Each object is the RHS of y=..., never compare independent equation sides.
  bank=[X-sp.pi-(t+1),X+sp.pi-t,answer,-t*X+t*sp.pi,sp.Integer(0)]
 else:raise ValueError(profile)
 return f,u,at,answer,bank

def eligible(profile,t):
 if t not in PROFILES[profile][3]:return False
 _,_,_,ans,bank=model(profile,t)
 return sum(sp.simplify(b-ans)==0 for b in bank)==1 and all(sp.simplify(b-a)!=0 for i,b in enumerate(bank) for a in bank[:i])

def text_parts(profile,t):
 q=ORIGINALS[profile];p=q[':question/problem'];s=q[':question/worked-solution'];original=PROFILES[profile][2]
 if t==original:return p,s
 if profile=='q-310179':
  mapping={r'3{x}^{4}':str(t)+r'{x}^{4}',r'12{x}^{3}':str(4*t)+r'{x}^{3}'}
 elif profile=='q-310180':
  mapping={r'\frac{\pi }{6}':r'\frac{\pi }{'+str(2*t)+'}',r'3x':str(t)+'x',r'=3.':'='+str(t)+'.',r'\cdot 3':r'\cdot '+str(t),r'3\operatorname{cos}':str(t)+r'\operatorname{cos}',r'3\cdot ':str(t)+r'\cdot ',r'3\cdot 0':str(t)+r'\cdot 0'}
 elif profile=='q-31153':
  mapping={r'3x+5':'3x+'+str(t),r'3\cdot 2+5':r'3\cdot 2+'+str(t),r'\operatorname{cos}⁡11':r'\operatorname{cos}⁡'+str(6+t)}
 elif profile=='q-31163':mapping={'11-2x':cos_cubic_inner(t)}
 elif profile=='q-310182':
  # All source spacing forms are recorded; replacement is simultaneous.
  a='' if t==1 else str(t);d=str(2*t);m=str(2*(t+1));sgn=str((-1)**t);final=tex(2*(t+1)*sp.pi*(-1)**t)
  mapping={r'x^{2} + 2x - 2':a+r'x^{2} + 2x - 2',r'x^{2} +2x - 2':a+r'x^{2} +2x - 2',r'x^{2} +2x - 2':a+r'x^{2} +2x - 2',r'1^{2} +2\cdot1 - 2':a+r'\cdot1^{2} +2\cdot1 - 2',r'2x + 2':d+'x + 2',r'2x+2':d+'x+2',r'2\cdot1+2':d+r'\cdot1+2',r'-4\pi':final,r'4\pi \cos(\pi)':m+r'\pi \cos('+str(t)+r'\pi)',r'4\pi \cdot (-1)':m+r'\pi \cdot ('+sgn+')'}
 elif profile=='q-51026':
  # Source numeric 2 appears only as amplitude, negative point ordinate,
  # derivative coefficient and tangent ordinate in this prompt/solution.
  mapping={'2':str(t)}
 return replace_all(p,mapping),replace_all(s,mapping)

def task_key(profile,t):
 f,_,at,_,_=model(profile,t)
 return json.dumps([('tangent' if profile=='q-51026' else 'slope' if at is not None else 'derivative'),sp.srepr(sp.expand_trig(f)),sp.srepr(at) if at is not None else None],separators=(',',':'))

def generate(level,seed,profile=None,t=None):
 rng=random.Random(seed)
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 if profile is None:profile=rng.choice([p for p,v in PROFILES.items() if v[0]==level])
 assert PROFILES[profile][0]==level
 if t is None:t=rng.choice([t for t in PROFILES[profile][3] if eligible(profile,t)])
 assert eligible(profile,t),'Parameter/profile collision or out of bounded range'
 f,u,at,answer,bank=model(profile,t);p,s=text_parts(profile,t)
 original=ORIGINALS[profile];sf=original[':question/answer-fields'][0]
 ftype=sf[':answer-field/type'][':db/ident'];key=sf[':answer-field/key']
 fp=task_key(profile,t);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),fp));fid=str(uuid.uuid5(uuid.UUID(qid),key))
 choices=[];correct=None
 for b,val in zip(bank,answer_values(profile,t,bank),strict=True):
  aid=str(uuid.uuid5(uuid.UUID(fid),sp.srepr(b)))
  choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
  if sp.simplify(b-answer)==0:correct=aid
 q={':question/id':qid,':question/problem':p,':question/worked-solution':s,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ftype,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':PROFILES[profile][1],'profile':profile,'parameters':{'t':t},'parameter_fingerprint':fp,'source_ids':[profile],'source_basis':SOURCE['basis'],'sympy_version':sp.__version__,'domain':'Real x; for tan derivatives, exclude zeros of cos(t*x^4-5). Other functions entire real.','sampler_policy':'One parameter varies; all other observed parameters fixed. Explicit bounded narrower sampling.'}}

def batch(level,count,seed):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 pairs=[(p,t) for p,v in PROFILES.items() if v[0]==level for t in v[3] if eligible(p,t)]
 random.Random(seed).shuffle(pairs)
 return [generate(level,seed,p,t) for p,t in pairs[:count]]
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value']+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186064281-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS,required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
