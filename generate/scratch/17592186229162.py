#!/usr/bin/env python3
"""Nonresonant exponential trial particular solutions, math basis1356.

Only a*y'+b*y=sum(c_i*exp(k_i*x)), with distinct k_i and a*k_i+b!=0.
All fields are RHS-only blanks. Raw profiles preserve the missing fields of two
unrated originals; normal presentation supplies mathematically derived
answers/solutions and authored easy ratings. Source replay is computed from reusable arithmetic/prose masks.
No payload lookup, database client, plotting, or sibling resonance methods.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from math import gcd
from pathlib import Path
import sympy as sp
KP_ID=17592186229162
KP_UUID='42bcc7e2-88f7-5ef9-8c51-77c1e2c8e8af'
TITLE='Finding a Particular Solution to a First-Order Inhomogeneous ODE With Exponential Forcing'
VERSION='nonresonant-exponential-1'
EVIDENCE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'single':'easy','legacy_single':'easy','two_and':'moderate','two_comma':'moderate','two_doublecomma':'moderate','two_hard':'hard'}
CASES=[
 ('q-332393','legacy_single',{'a':9,'b':18,'k':[2],'c':[4]}),
 ('q-332645','legacy_single',{'a':5,'b':10,'k':[-3],'c':[15]}),
 ('q-332644','single',{'a':3,'b':-6,'k':[4],'c':[9]}),
 ('q-332655','single',{'a':5,'b':-20,'k':[-1],'c':[15]}),
 ('q-332659','single',{'a':6,'b':-18,'k':[-2],'c':[24]}),
 ('q-332664','single',{'a':7,'b':14,'k':[-5],'c':[21]}),
 ('q-332667','two_hard',{'a':4,'b':8,'k':[2,3],'c':[5,3]}),
 ('q-332668','two_and',{'a':3,'b':9,'k':[1,4],'c':[7,4]}),
 ('q-332669','two_comma',{'a':1,'b':3,'k':[2,5],'c':[2,1]}),
 ('q-332670','two_doublecomma',{'a':2,'b':-6,'k':[1,2],'c':[3,-2]})]
PROFILES={q:{'template':t,'parameters':p,'raw':True} for q,t,p in CASES}
OPENING='To find the general solution of an inhomogeneous first-order linear equation with constant coefficients on the left-hand side, we must find the sum of the complementary and particular solutions.'
def exp(k): return '{e}^{'+coef(k)+'x}'
def coef(v):
 v=sp.Rational(v)
 if v==1:return ''
 if v==-1:return '-'
 return sp.latex(v).replace("- ","-")
def term(v,f):return coef(v)+f
def summ(parts):return ''.join(('+' if i and not v.startswith('-') else '')+v for i,v in enumerate(parts))
def signed(v,f):return ('+' if v>=0 else '-')+term(abs(v),f)
def block(s):return '$$\n'+s+'\n$$'
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def validate_parameters(level,t,p,raw=False):
 if set(p)!= {'a','b','k','c'}:raise ValueError('Expected a,b,k,c only')
 if not all(type(v) is int for v in [p['a'],p['b'],*p['k'],*p['c']]):raise ValueError('Integer coefficients only')
 a,b,k,c=p['a'],p['b'],p['k'],p['c']; n=1 if t in ('single','legacy_single') else 2
 if len(k)!=n or len(c)!=n or len(set(k))!=n:raise ValueError('Distinct exponential terms required')
 if a<=0 or b==0 or any(v==0 for v in [*k,*c]) or any(a*v+b==0 for v in k):raise ValueError('Nonzero, nonresonant terms required; resonance belongs to sibling KP29163')
 if not raw:
  if not 1<=a<=9 or abs(b)>30 or any(abs(v)>5 for v in k) or any(abs(v)>30 for v in c):raise ValueError('Comparable source workload bounds violated')
  if b%a:raise ValueError('Source workload retains integer complementary exponent')
  if level=='moderate' and a>3:raise ValueError('Moderate leading coefficient 1..3')
  if level=='hard' and (a<4 or a>7 or a//gcd(a,b,*c)<4 or any(v%a==0 for v in c)):raise ValueError('Hard displayed leading coefficient4..7, primitive whole-ODE leading coefficient>=4, and both normalized forcing coefficients nonintegral required')
def sample(level,t,rng):
 for _ in range(500):
  a=rng.randint(1,9) if level=='easy' else rng.randint(1,3) if level=='moderate' else rng.randint(4,7)
  b=a*rng.choice([-4,-3,-2,-1,1,2,3,4]); k=rng.sample([-5,-4,-3,-2,-1,1,2,3,4,5],1 if level=='easy' else 2)
  c=[a*rng.choice([-3,-2,-1,1,2,3])] if level=='easy' else [rng.choice([-9,-7,-5,-3,-2,-1,1,2,3,5,7,9]) for _ in k]
  p={'a':a,'b':b,'k':k,'c':c}
  try:validate_parameters(level,t,p);return p
  except ValueError:pass
 raise ValueError('Eligible sampling exhausted')
def render(p,t,raw):
 a,b,k,c=p['a'],p['b'],p['k'],p['c']; es=[exp(v) for v in k]; n=len(k)
 syms=[r'\alpha ',r'\beta '][:n]; den=[a*v+b for v in k]; ans=[sp.Rational(v,d) for v,d in zip(c,den)]
 forcing=summ([term(v,e) for v,e in zip(c,es)])
 trial=summ([s+e for s,e in zip(syms,es)]); derivative=summ([term(v,s+e) for v,s,e in zip(k,syms,es)])
 answer=summ([term(v,e) for v,e in zip(ans,es)])
 equation=term(a,r'\frac{\text{d}y}{\text{d}x}')+signed(b,'y')+'='+forcing
 prompt='Given that the differential equation \n\n'+block(equation)+'\n\nhas the complementary solution ${y}_{c}(x)=A'+exp(sp.Rational(-b,a))+'$, find the particular solution ${y}_{p}(x)$ to this equation.\n\n${y}_{p}(x)=$\n{{field-1}}'
 if t=='legacy_single':
  prompt='Given that the differential equation\n$'+str(a)+r'\frac{dy}{dx} '+('+' if b>0 else '-')+' '+str(abs(b))+'y = '+term(c[0],'e^{'+coef(k[0])+'x}')+'$\nhas the complementary solution $y_{c}(x) = Ae^{'+coef(sp.Rational(-b,a))+'x}$, find the particular solution $y_{p}(x)$ to this equation.$y_{p}(x) =$\n{{field-1}}'
 if n==1:
  suffix=' and $'+es[0]+'$ is not a term in the complementary solution'
  constants='where $\\alpha $ is a constant that is to be determined.'
  substitute='To find the value of $\\alpha ,$'
  distributed='('+str(a*k[0])+('+' if b>0 else '-')+str(abs(b))+')'+syms[0]+es[0]
  rows=[term(a,'('+derivative+')')+signed(b,'('+trial+')'),distributed,term(den[0],syms[0]+es[0])]
  aligned=' \\\\ '.join(v+' & ='+forcing for v in rows)+r' \\ \alpha  & ='+sp.latex(ans[0]).replace("- ","-")
 else:
  suffix=' and neither $'+es[0]+'$ nor $'+es[1]+'$ is a term in the complementary solution'
  constants='where $\\alpha $ and $\\beta $ are constants that are to be determined.'
  substitute='To find the values of $\\alpha $ and $\\beta ,$'
  distributed=summ(['('+term(a*v,s)+signed(b,s)+')'+e for v,s,e in zip(k,syms,es)])
  rows=[term(a,'('+derivative+')')+signed(b,'('+trial+')'),distributed,summ([term(d,s+e) for d,s,e in zip(den,syms,es)])]
  aligned=' \\\\ '.join(v+' & ='+forcing for v in rows)+('.' if t=='two_comma' else '')
 solution=OPENING+'\n\nWe see that the right-hand side is $'+forcing+',$'+suffix+', so we assume a particular solution of the form\n\n'+block('{y}_{p}='+trial+',')+'\n\n'+constants+'\n\nCalculating the first derivative of ${y}_{p}$ gives\n\n'+block(r'\frac{\text{d}{y}_{p}}{\text{d}x}='+derivative+('.' if n==2 else ''))+'\n\n'+substitute+' we substitute ${y}_{p}$ and ${y}_{p}^{′}$ into the differential equation:\n\n'+block(r'\begin{aligned}'+aligned+r'\end{aligned}')
 if n==2:
  sep={'two_and':r'\,\text{and}\,','two_comma':r',\,','two_doublecomma':r',\,\,','two_hard':r',\,\,'}[t]
  solved=sep.join(s+'='+sp.latex(v).replace("- ","-") for s,v in zip([r'\alpha ',r'\beta '],ans))
  coeff=sep.join(term(d,s)+'='+str(v) for d,s,v in zip(den,[r'\alpha ',r'\beta '],c))
  solution+='\n\nEquating coefficients of $'+es[0]+'$ and $'+es[1]+',$ respectively, gives\n\n'+block(coeff+(',' if t=='two_and' else '.'))+'\n\nSo, we have\n\n'+block(solved+'.')
 solution+='\n\nTherefore, the particular solution ${y}_{p}(x)$ is\n\n'+block('{y}_{p}(x)='+answer+'.')
 if t=='legacy_single' and raw:solution=None
 if not raw and t=='legacy_single':prompt=prompt.replace('equation.$y','equation.\n\n$y')
 if not raw:prompt=prompt.replace('to this equation.','to this equation. Use a linear combination of the displayed forcing exponentials.')
 bankanswer=answer
 return prompt,solution,bankanswer

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'blank'):raise ValueError('Unsupported level/field')
 raw=False
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown observed profile')
  spec=PROFILES[profile]; raw=True
  if template and template!=spec['template']:raise ValueError('Profile/template mismatch')
  template=spec['template'];parameters=parameters or spec['parameters']
 eligible=[t for t,l in TEMPLATES.items() if l==level]
 if template and template not in eligible:raise ValueError('Template/level mismatch')
 rng=random.Random(seed);t=template or rng.choice([v for v in eligible if v!='legacy_single'])
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,t,rng)
 validate_parameters(level,t,p,raw)
 prompt,solution,answer=render(p,t,raw)
 missing=raw and t=='legacy_single'; q={':question/problem':prompt}
 if not missing:q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=solution
 # Equation normalized by leading a, with ordered terms sorted: common scaling
 # and term permutation do not count as new mathematical tasks.
 task=[str(sp.Rational(p['b'],p['a'])),sorted((v,str(sp.Rational(c,p['a']))) for v,c in zip(p['k'],p['c']))]
 fingerprint=sha(task); content=sha([VERSION,q,answer if not missing else None,'blank'])
 qid=uid('q:'+content);fid=uid('f:'+content);aid=uid('a:'+content+answer)
 field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank'}
 if not missing:field.update({':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':answer}],':answer-field/correct':[':answer/id',aid]})
 q.update({':question/id':qid,':question/answer-fields':[field]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,'raw_evidence':raw,'parameter_fingerprint':fingerprint,'content_fingerprint':content,'source_analysis':SOURCE,'source_ids':[profile] if profile else [v for v,u,w in CASES if u==t],'plot_rating':'none','authored_extension':not raw,'presentation_repairs':[] if raw else ['clarify the required trial-form fragment']+(['derived missing answer,solution,authored easy rating; paragraph separation'] if t=='legacy_single' else []),'sympy_version':sp.__version__}}
# EASY: single exponential, integer complementary exponent. Original
# unrated blanks receive an authored easy assignment only in repaired output.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two independent nonresonant trials; a1..3, signed exponents/forcing.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same method as observed q332667; a4..7 and primitive leading
# a/gcd(a,b,*c)>=4 so a common scaling cannot collapse the ODE to moderate.
# Both normalized forcing coefficients remain genuinely fractional. No third term, resonance, general solution/IVP.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question']; f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\nAnswer: $'+(f.get(':answer-field/choices') or [{':answer/value':'[missing in original]'}])[0][':answer/value']+'$\n\n'+q.get(':question/worked-solution','[missing in original]')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=list(PROFILES));p.add_argument('--format',choices=['markdown','json'],default='markdown');args=p.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 if args.count<1:p.error('Positive count required')
 rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
