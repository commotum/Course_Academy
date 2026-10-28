#!/usr/bin/env python3
"""Local area approximation |J(u0,v0)| deltaA, memory-only review records.

Twelve observed easy function families (q-161886 added at basis 2268); each raw five-choice bank has an explicit
proportional expression replay profile. Scalar distractor intent is underdetermined:
these profiles are evidence-only, never default sampled banks. Normal questions
select a complete authored derivative-operation or area-stage bank before sampling.
Moderate (canonical monomial sum) and hard (sibling sum/difference powers) are
explicitly authored missing levels. Both keep four derivatives, ad-bc, point
substitution and absolute area scaling. No integration/orientation/inverses.
All source shared prose and full mathematical solution sequence are preserved;
standard LaTeX normalizes source unicode notation. Duplicate legacy banks replay
separately, never as two demands in one question. Exact values and stable identity.
No database or shared-engine edits. See sibling evidence folder for verification.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186129282
KP_UUID='6d82be73-0720-5267-8698-427641b0e66e'
TITLE='Identifying the Local Area Scale Factor of a Transformation'
VERSION='local-area-1-audit9837'
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
u,v=sp.symbols('u v',real=True)
TEMPLATES={
 'poly_sum':('easy','q-161788',{'u0':1,'v0':2}),
 'log_product':('easy','q-161832',{'u0':1,'v0':5}),
 'exp_product':('easy','q-161831',{'u0':-1,'v0':1}),
 'reciprocal_product':('easy','q-161873',{'u0':2,'v0':2}),
 'sqrt_sum':('easy','q-161874',{'u0':4,'v0':2}),
 'cos_sum':('easy','q-161875',{'u0':0,'v0':3}),
 'quotient_product':('easy','q-161885',{'u0':2,'v0':4}),
 'sqrt_product':('easy','q-161887',{'u0':1,'v0':4}),
 'log_difference':('easy','q-161877',{'u0':2,'v0':1}),
 'sin_sum':('easy','q-161878',{'u0':-3,'v0':3}),
 'exp_sum':('easy','q-161876',{'u0':-2,'v0':2}),
 'cubic_difference':('easy','q-161886',{'u0':3,'v0':1}),
 'canonical_monomial':('moderate',None,{'a':1,'b':1,'c':1,'n':3,'u0':-1,'v0':2}),
 'powers':('hard',None,{'a':1,'b':1,'p':1,'q':1,'r':1,'s':1,'m':3,'n':2,'u0':2,'v0':1})}
# Explicit replay-only proportional shapes. These are not recovered error intent.
OBSERVED_FACTORS={
 'poly_sum':['1/13','18/13','7/13','1','5/26'],
 'log_product':['1','1/5','11/5','8/5','3/5'],
 'exp_product':['1/4','1/2','2','3/2','1'],
 'reciprocal_product':['2','1','6/7','9/7','5/7'],
 'sqrt_sum':['15/7','1','3','3/7','12/7'],
 'cos_sum':['2','1','8/3','3/2','1/2'],
 'quotient_product':['1','1/3','3','2','4'],
 'sqrt_product':['4','2','3','1','1/2'],
 'log_difference':['4','5/3','1','2','1/3'],
 'sin_sum':['12/5','1','6/5','2/5','7/5'],
 'exp_sum':['21/11','18/11','13/11','1','17/11'],
 'cubic_difference':['4/13','5/26','9/13','1/2','1']}
BANK_PROFILES={}
for t,fs in OBSERVED_FACTORS.items():
 BANK_PROFILES['observed_'+t]={'template':t,'origin':'observed proportional shapes; intent unresolved','factors':fs}
for t in ('poly_sum','exp_product'):
 BANK_PROFILES['legacy_'+t]={'template':t,'origin':'legacy duplicate bank; repaired field layout/designation','factors':OBSERVED_FACTORS[t]}
for t in TEMPLATES:
 for b in (('area',) if t in ('log_product','cos_sum','quotient_product','sqrt_product') else ('area','determinant')):
  BANK_PROFILES['authored_'+b+'_'+t]={'template':t,'origin':'authored complete '+b+' operation bank','bank':b}
class SampleRejected(ValueError):pass

def tex(z):return sp.latex(z,mul_symbol=None)
def equivalent(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def clean(z):return sp.factor(sp.trigsimp(z))
def block(z):return '$$\n'+z+'\n$$'
def matrix(a,b,c,d):return r'\left|\begin{matrix}'+a+'&'+b+r'\\'+c+'&'+d+r'\end{matrix}\right|'
def area(z):return ('' if z==1 else tex(z)+r'\,')+r'\delta A'
J=r'\frac{\partial(x,y)}{\partial(u,v)}'
PARTIALS=[r'\frac{\partial x}{\partial u}',r'\frac{\partial x}{\partial v}',r'\frac{\partial y}{\partial u}',r'\frac{\partial y}{\partial v}']
OPENING='Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:'
COMPUTING='Computing the corresponding Jacobian determinant, we obtain the following:'
ENDING='Therefore, we have'

def functions(t,p):
 if t=='poly_sum':return u**2+v,2*u-v**3
 if t=='log_product':return sp.log(u*v),u*v**2
 if t=='exp_product':return v*sp.exp(u),u*sp.exp(v)
 if t=='reciprocal_product':return 1/u-v,u**2*v
 if t=='sqrt_sum':return sp.sqrt(u)+v**2,u*v
 if t=='cos_sum':return sp.cos(u)-v**2,u+v
 if t=='quotient_product':return u**2/v,u*v
 if t=='sqrt_product':return sp.sqrt(u*v),u*v**2
 if t=='log_difference':return sp.log(u-v),v-u**2
 if t=='sin_sum':return u+v**2,sp.sin(u+v)
 if t=='exp_sum':return sp.exp(u+v),u**3+v
 if t=='cubic_difference':return u**3-v,v-u
 if t=='canonical_monomial':return p['a']*u*v**p['n'],p['b']*u**2+p['c']*v**2
 if t=='powers':return p['a']*(p['p']*u+p['q']*v)**p['m'],p['b']*(p['r']*u-p['s']*v)**p['n']
 raise ValueError(t)

def validate_parameters(t,p):
 if set(p)!=set(TEMPLATES[t][2]) or any(type(z)is not int for z in p.values()):raise ValueError('Exact parameter keys and integers required')
 if any(abs(p[k])>9 for k in ('u0','v0')):raise ValueError('Small exact coordinates required')
 a,b=p['u0'],p['v0']
 if t=='log_product' and a*b<=0:raise ValueError('uv>0')
 if t=='reciprocal_product' and a==0:raise ValueError('u!=0')
 if t=='sqrt_sum' and a not in (1,4,9):raise ValueError('u positive perfect square 1,4,9')
 if t=='quotient_product' and b==0:raise ValueError('v!=0')
 if t=='sqrt_product' and (a<=0 or b<=0 or int(sp.sqrt(a*b))**2!=a*b):raise ValueError('Positive u,v and perfect square uv required')
 if t=='log_difference' and a-b<=0:raise ValueError('u-v>0')
 if t=='cos_sum' and a!=0:raise ValueError('Familiar angle u=0')
 if t in ('exp_product','sin_sum','exp_sum') and a+b!=0:raise ValueError('Familiar evaluation u+v=0')
 if t=='canonical_monomial' and any(abs(p[k]) not in (1,2,3) for k in ('u0','v0')):raise ValueError('Moderate coordinates are nonzero integers of magnitude at most 3')
 if t=='powers' and any(abs(p[k]) not in (1,2) for k in ('u0','v0')):raise ValueError('Hard coordinates are nonzero integers of magnitude at most 2')
 if t=='canonical_monomial' and (any(p[k] not in (1,2,3) for k in ('a','b','c')) or p['n'] not in (2,3)):raise ValueError('Canonical small scales; power 2/3')
 if t=='powers' and (any(p[k] not in (1,2) for k in ('a','b','p','q','r','s')) or (p['m'],p['n']) not in ((3,2),(2,3))):raise ValueError('Sibling sum/difference powers 3/2; small coefficients')

def sample(t,rng):
 p=dict(TEMPLATES[t][2]);p.update(u0=rng.choice([-4,-3,-2,-1,1,2,3,4]),v0=rng.choice([-4,-3,-2,-1,1,2,3,4,5]))
 if t=='log_product':p.update(u0=rng.randint(1,5),v0=rng.choice([3,4,5,6,7,8]))
 if t=='sqrt_sum':p['u0']=rng.choice([1,4,9])
 if t=='sqrt_product':p.update(u0=rng.choice([1,4,9]),v0=rng.choice([1,4,9]))
 if t=='cos_sum':p['u0']=0
 if t in ('exp_product','sin_sum','exp_sum'):p['v0']=-p['u0']
 if t=='log_difference':p['u0']=rng.choice([2,3,4,5]);p['v0']=rng.randint(-3,p['u0']-1)
 if t=='canonical_monomial':
  p.update(u0=rng.choice([-3,-2,-1,1,2,3]),v0=rng.choice([-3,-2,-1,1,2,3]))
  p.update({k:rng.randint(1,3) for k in ('a','b','c')});p['n']=rng.choice([2,3])
 if t=='powers':
  p.update(u0=rng.choice([-2,-1,1,2]),v0=rng.choice([-2,-1,1,2]))
  p.update({k:rng.randint(1,2) for k in ('a','b','p','q','r','s')});p['m'],p['n']=rng.choice([(3,2),(2,3)])
 return p

def compute(t,p):
 validate_parameters(t,p);x,y=functions(t,p);d=[clean(sp.diff(x,u)),clean(sp.diff(x,v)),clean(sp.diff(y,u)),clean(sp.diff(y,v))]
 A=d[0]*d[3];B=d[1]*d[2];j=clean(A-B);subs={u:p['u0'],v:p['v0']};j0=sp.simplify(j.subs(subs));C=sp.Abs(j0)
 if C.is_positive is not True or C.has(sp.zoo,sp.nan,sp.oo):raise SampleRejected('Nonzero finite local scale required')
 if t in ('canonical_monomial','powers') and C>500:raise SampleRejected('Authored workload bound: area scale at most 500')
 return x,y,d,A,B,j,j0,C

def bank(profile,data,p):
 x,y,d,A,B,j,j0,C=data;info=BANK_PROFILES[profile]
 if 'factors'in info:
  vals=[sp.simplify(C*sp.Rational(f)) for f in info['factors']];recipes=['scale*('+f+') replay shape; intent unresolved' for f in info['factors']]
 elif info['bank']=='area':
  vals=[C,C**2,1/C,2*C,C/2];recipes=['absolute evaluated determinant','square area scale','reciprocal area scale','double area scale','halve area scale']
 else:
  subs={u:p['u0'],v:p['v0']};a,b=[sp.simplify(z.subs(subs)) for z in (A,B)];vals=[C,sp.Abs(a+b),sp.Abs(a),sp.Abs(b),sp.Abs(2*a-b)];recipes=['absolute ad-bc','absolute ad+bc','omit bc','omit ad','double ad']
 if len(vals)!=5 or any(z.is_nonnegative is not True or z.has(sp.zoo,sp.nan,sp.oo) for z in vals) or any(equivalent(a,b) for i,a in enumerate(vals) for b in vals[:i]):raise SampleRejected('Reject entire ambiguous/domain-invalid bank')
 if sum(equivalent(z,C) for z in vals)!=1:raise SampleRejected('Exactly one correct option required')
 return vals,recipes

def render(t,p,data):
 x,y,d,A,B,j,j0,C=data;u0,v0=p['u0'],p['v0'];point=f'({u0},{v0})'
 prompt=f'Consider a small rectangle $Δ$ whose bottom-left corner is located at the point ${point}$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by\n\n'+block(r'T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}'+tex(x)+r'\\'+tex(y)+r'\end{aligned}]?')
 subs={u:sp.Integer(u0),v:sp.Integer(v0)}
 # Substitute in the expression tree with evaluate=False to retain coordinate powers.
 def substitution(z):
  if z in subs:return sp.Symbol('('+str(subs[z])+')')
  if not z.args:return z
  return z.func(*(substitution(a) for a in z.args),evaluate=False)
 substituted=tex(substitution(j))
 symbolic_rows={
 'poly_sum':[r'-6uv^{2}-2'], 'log_product':[r'2v-v',r'v'],
 'exp_product':[r'uv e^{u+v}-e^{u+v}',r'(uv-1)e^{u+v}'],
 'reciprocal_product':[r'-1+2uv'], 'sqrt_sum':[r'\frac{1}{2}\sqrt{u}-2v^{2}'],
 'cos_sum':[r'-\sin u+2v'], 'quotient_product':[r'\frac{2u^{2}}{v}+\frac{u^{2}}{v}',r'\frac{3u^{2}}{v}'],
 'sqrt_product':[r'v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}',r'\frac{1}{2}v\sqrt{uv}'],
 'log_difference':[r'\frac{1-2u}{u-v}'], 'sin_sum':[r'(1-2v)\cos(u+v)'],
 'exp_sum':[r'e^{u+v}(1-3u^{2})'], 'cubic_difference':[r'3u^{2}-1']}.get(t,[tex(sp.expand(A-B)),tex(j)])
 rows=[J+' & ='+matrix(*PARTIALS),r'& ='+matrix(*(tex(z) for z in d)),r'& =('+tex(d[0])+r')\cdot ('+tex(d[3])+r')-('+tex(d[1])+r')\cdot ('+tex(d[2])+')',*[r'& ='+z for z in symbolic_rows],r'\left.'+J+r'\right|_{'+point+'} & ='+r'\left('+tex(j)+r'\right)\big|_{u='+str(u0)+',v='+str(v0)+'}',*([r'& ='+substituted] if t!='log_product' else []),r'& ='+tex(j0)]
 solution=OPENING+'\n\n'+block(r'\text{Area}(T(Δ))\approx\left|'+J+r'\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}')+'\n\n'+COMPUTING+'\n\n'+block(r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}')+'\n\n'+ENDING+'\n\n'+block(r'\begin{aligned}\text{Area}(T(Δ)) & \approx|'+tex(j0)+r'|\cdot\delta A\\ & ='+area(C)+r'.\end{aligned}')
 return prompt,solution

def ident(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed layout is one five-choice radio field')
 rng=random.Random(seed)
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
  pt=BANK_PROFILES[profile]['template']
  if template and template!=pt:raise ValueError('Profile/template mismatch')
  template=pt
 t=template or rng.choice([k for k,z in TEMPLATES.items() if z[0]==level])
 if t not in TEMPLATES or TEMPLATES[t][0]!=level:raise ValueError('Template/level mismatch')
 profile=profile or 'authored_area_'+t # complete bank selected before parameter sampling
 if parameters is None:
  for _ in range(1000):
   p=sample(t,rng)
   try:data=compute(t,p);vals,recipes=bank(profile,data,p);break
   except SampleRejected:continue
  else:raise SampleRejected('No valid sample')
 else:p=dict(parameters);data=compute(t,p);vals,recipes=bank(profile,data,p)
 prompt,solution=render(t,p,data);C=data[-1]
 prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 canonical={'x':sp.srepr(data[0]),'y':sp.srepr(data[1]),'point':[p['u0'],p['v0']],'domain':domain(t)}
 fp=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()
 key=json.dumps({'v':VERSION,'task':canonical,'problem':prompt,'solution':solution,'bank':sorted(area(z) for z in vals)},sort_keys=True)
 qid=ident(key);fid=ident(qid+'|selection');answers=[];correct=None
 for val in vals:
  aid=ident(fid+'|'+area(val));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':area(val)})
  if equivalent(val,C):correct=[':answer/id',aid]
 rng.shuffle(answers)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':correct}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'provenance':({**PROVENANCE,'basis':2268} if t=='cubic_difference' else PROVENANCE),'seed':seed,'difficulty':level,'template':t,'parameters':p,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'recipes':recipes,'source_refs':[TEMPLATES[t][1]] if TEMPLATES[t][1] else [],'authored_level':level!='easy','domain':domain(t),'plot':'none','parameter_fingerprint':fp,'exact':{'x':str(data[0]),'y':str(data[1]),'partials':[str(z) for z in data[2]],'ad':str(data[3]),'bc':str(data[4]),'jacobian':str(data[5]),'jacobian_at_point':str(data[6]),'area_scale':str(C)}}}
def domain(t):return {'log_product':'uv>0','reciprocal_product':'u!=0','sqrt_sum':'u>0','quotient_product':'v!=0','sqrt_product':'u>0,v>0','log_difference':'u-v>0'}.get(t,'R²')
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return '\n\n'.join(['### '+r['generation']['difficulty']+' / '+r['generation']['template']+' / '+r['generation']['bank_profile'],q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)];print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
