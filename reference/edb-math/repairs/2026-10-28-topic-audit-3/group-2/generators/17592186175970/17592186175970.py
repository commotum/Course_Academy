#!/usr/bin/env python3
"""Elliptic-cylinder component questions. Pure deterministic generation; no DB writes.
Easy: normalized ellipse, sine component. Moderate: normalize positive integer
coefficients, cosine or sine component. No hard template. See package extraction.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186175970-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,itertools,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186175970
KP_UUID='9d646eda-468b-5ae5-b7b0-0d53a948a808'
TITLE='Parametrizing an Elliptic Cylinder'
VERSION='elliptic-cylinder-1'
HERE=Path(__file__).resolve().with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
# One complete bank per observed profile; no pooled recipes.
PROFILES={
'q-103980':dict(a=2,b=2,plane='xy',target='sin',level='moderate',recipes=['cosh','u2','acos','bsinh','bsin'],legacy=True),
'q-103981':dict(a=2,b=3,plane='xz',target='sin',level='moderate',recipes=['u2','asin','btan','bsin','u'],legacy=True),
'q-164526':dict(a=5,b=1,plane='xy',target='cos',level='moderate',recipes=['bsin','acos','au','a2u2','2acosh']),
'q-164530':dict(a=4,b=2,plane='xz',target='cos',level='moderate',recipes=['sin','u2','bcosh','cos','acos']),
'q-164534':dict(a=5,b=2,plane='xz',target='cos',level='moderate',recipes=['sin','au2','cosh','acos','au']),
'q-164522':dict(a=2,b=6,plane='xy',target='sin',level='moderate',recipes=['bsinh','bsin','cosh','bhalfcos','bu2']),
'q-164524':dict(a=5,b=2,plane='xy',target='sin',level='easy',recipes=['b2u2','bsin','bcos','b2sinh','cosh'])}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def expression(recipe,a,b,u):
 t=sp.Symbol('t',real=True);v=sp.Symbol(u,real=True)
 return {'cosh':sp.cosh(t),'u2':v**2,'acos':a*sp.cos(t),'bsinh':b*sp.sinh(t),'bsin':b*sp.sin(t),'asin':a*sp.sin(t),'btan':b*sp.tan(t),'u':v,'au':a*v,'a2u2':a*a*v*v,'2acosh':2*a*sp.cosh(t),'sin':sp.sin(t),'bcosh':b*sp.cosh(t),'cos':sp.cos(t),'au2':a*v*v,'bhalfcos':sp.Rational(b,2)*sp.cos(t),'bu2':b*v*v,'b2u2':b*b*v*v,'bcos':b*sp.cos(t),'b2sinh':b*b*sp.sinh(t)}[recipe]
def tex(e):return sp.latex(e)
def term(c,v):return (str(c) if c!=1 else '')+v+'^{2}'
def data(level,p):
 a,b=p['a'],p['b'];plane=p['plane'];target=p['target'];assert plane in ('xy','xz') and target in ('sin','cos')
 assert type(a)==type(b)==int and 1<=a<=12 and 1<=b<=12
 v,w=plane;u=next(c for c in 'xyz' if c not in plane)
 normal=rf'\frac{{{v}^{{2}}}}{{{a*a}}}+\frac{{{w}^{{2}}}}{{{b*b}}}=1'
 from math import gcd
 c1,c2,c3=b*b,a*a,a*a*b*b;d=gcd(gcd(c1,c2),c3);c1//=d;c2//=d;c3//=d
 eq=normal if level=='easy' else term(c1,v)+'+'+term(c2,w)+'='+str(c3)
 t=sp.Symbol('t',real=True);vec=[u if c==u else tex(a*sp.cos(t)) if c==v else tex(b*sp.sin(t)) for c in 'xyz']
 index='xyz'.index(v if target=='cos' else w)
 return a,b,v,w,u,normal,eq,vec,index

def task(p):return [p['a'],p['b'],p['plane'],p['target']]
def generate(level,seed=0,template=None,parameters=None,profile=None,replay=False):
 if level not in ('easy','moderate'):raise ValueError('Unsupported hard: no observed same-backbone hard template')
 rng=random.Random(seed)
 eligible=[s for s,c in PROFILES.items() if c['level']==level and not c.get('legacy')]
 profile=profile or template or rng.choice(eligible);c=PROFILES[profile]
 if c['level']!=level:raise ValueError('Profile/difficulty mismatch')
 if c.get('legacy') and not replay:raise ValueError('Incomplete unrated source profile is evidence-only')
 p=dict(parameters or dict(a=rng.randint(2,12),b=rng.randint(2,12),plane=rng.choice(['xy','xz']),target=c['target']))
 if p['target']!=c['target']:raise ValueError('Profile target mismatch')
 a,b,v,w,u,normal,eq,vec,index=data(level,p)
 bank=[expression(r,a,b,u) for r in c['recipes']]
 if len(set(bank))!=5:raise ValueError('Profile bank collision')
 right=expression('acos' if p['target']=='cos' else 'bsin',a,b,u)
 assert bank.count(right)==1
 fp=digest(task(p));qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+fp+':'+profile));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(e))),':answer/type':':answer.type/math',':answer/value':tex(e)} for e in bank]
 missing=vec.copy();missing[index]=r'\text{_____}'
 ordinal=['first','second','third'][index]
 prompt='$$\nf(t,'+u+')=⟨'+r',\,'.join(missing)+'⟩\n$$\n\n'+f'The vector-valued function $f(t,{u})$ above parametrizes the elliptic cylinder defined in Cartesian coordinates as ${eq}.$ What is the {ordinal} component of $f?$'
 planar='⟨'+tex(a*sp.cos(sp.Symbol('t',real=True)))+r',\,'+tex(b*sp.sin(sp.Symbol('t',real=True)))+'⟩'
 recall=f'Recall that the ellipse ${eq}$'+(f', or equivalently ${normal}$,' if level=='moderate' else '')+f' in the ${v}{w}$-plane has the parametrization\n\n$$\n⟨{v},{w}⟩={planar},\\quad t\\in[0,2\\pi),\n$$'
 solution=recall+'\n\nsince\n\n$$\n'+rf'\begin{{aligned}}\frac{{{v}^2}}{{{a*a}}}+\frac{{{w}^2}}{{{b*b}}}&=\frac{{({tex(a*sp.cos(sp.Symbol("t",real=True)))})^2}}{{{a*a}}}+\frac{{({tex(b*sp.sin(sp.Symbol("t",real=True)))})^2}}{{{b*b}}}\\&=\cos^2 t+\sin^2 t\\&=1.\end{{aligned}}'+'\n$$\n\n'+f'Now, for any point $(x,y,z)$ on our surface, we obtain the following:\n\n$$\nf(t,{u})=⟨x,y,z⟩=⟨'+r',\,'.join(vec)+'⟩\n$$\n\n'+f'where $t\\in[0,2\\pi)$ and ${u}\\in(-\\infty,\\infty)$.\n\nTherefore, the {ordinal} component of $f$ is ${tex(right)}$.'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[bank.index(right)][':answer/id']]}]},'generation':{'version':VERSION,'seed':seed,'template':('normalized' if level=='easy' else 'normalize')+'-'+p['target'],'bank_profile':profile,'parameters':p,'mathematical_fingerprint':fp,'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'source_question':profile,'evidence_only':c.get('legacy',False),'dependencies':{'sympy':sp.__version__},'domain':'t in [0,2pi), free coordinate real; positive integer semiaxes 1..12','solution_corrections':['q-164524 first substituted denominator must be a^2, not a']}}

def batch(level,count,seed):
 rng=random.Random(seed);result=[];used=set()
 for i in range(10000):
  if len(result)==count:return result
  try:r=generate(level,seed+i)
  except ValueError:continue
  fp=r['generation']['mathematical_fingerprint']
  if fp not in used:result.append(r);used.add(fp)
 raise ValueError(f'Bounded distinct capacity exhausted; requested {count}, found {len(result)}')
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186175970-source-policy.json'))


from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();r=batch(args.difficulty,args.count,args.seed);print(json.dumps(_apply_source_notation(r),indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,r)))
