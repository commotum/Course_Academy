#!/usr/bin/env python3
"""Bounded linear-exponential integral templates; no database operations."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 python=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if python.exists() and Path(sys.executable).resolve()!=python.resolve():os.execv(str(python),[str(python),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
KP_ID=17592186096655
KP_UUID='f4b340f6-0ac6-5bbf-a7d4-0088ca3c4e5e'
TITLE='Integrating the Exponential Function With a Linear Exponent'
VERSION='linear-exponential-integrals-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CASES=json.loads((HERE/'source-cases.json').read_text())
SUPPORTED_LEVELS=('easy','moderate')
x=sp.Symbol('x',positive=True)
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(sp.sympify(v),ln_notation=True).replace('e^{','{e}^{')
def math(p):
 a=sp.Rational(p['a']);k=sp.Rational(p['k']);b=sp.Rational(p.get('b',0)); f=a*sp.exp(k*x+b)
 L=sp.log(p['base']) if p.get('bound')=='log' else sp.Rational(p.get('L',0));H=sp.log(p['base']) if p.get('bound')=='log' else sp.Rational(p.get('H',0))
 if p.get('bound')=='log':L=sp.Integer(0)
 ans=sp.expand(a/k*(sp.exp(k*H+b)-sp.exp(k*L+b))) if 'bound' in p else a/k*sp.exp(k*x+b)
 return f,ans,L,H

def printed(q):
 import sys,re
 sys.path.insert(0,str(HERE))
 from scalar_parser import scalar,group
 text=q[':question/problem'].replace('z','x')
 tail=text.split(r'\int',1)[1].lstrip().lstrip('}').lstrip()
 limits=None
 if tail.startswith('_'):
  l,j=group(tail,1);assert tail[j]=='^';h,j=group(tail,j+1);tail=tail[j:];limits=(scalar(l),scalar(h))
 tail=re.split(r'\\(?:text|textrm)\{d\}x|dx',tail)[0].rstrip().removesuffix(r'\,')
 return sp.simplify(scalar(tail)),limits

def fingerprint(q):
 f,limits=printed(q)
 return digest([sp.srepr(f),None if limits is None else [sp.srepr(v) for v in limits],'real'])

def bank(c,p):
 a=sp.Rational(p['a']);k=sp.Rational(p['k']);b=sp.Rational(p.get('b',0));E=sp.exp(k*x+b);f,ans,L,H=math(p);t=c['profile']
 if t=='legacy':return [k*E,-E,E,-a/k*E,a/k*E]
 if t=='fraction-shift':return [sp.exp(x+b)/k,-E/k,E/k,k*E,E]
 if t=='scaled':return [k/a*E,a*E,a/k*E,k*E,a/k*sp.exp(a*x)]
 if t=='unit-definite':return [sp.exp(-1),sp.E-1,sp.E,sp.Integer(p['H']),sp.Rational(1,p['H'])]
 if t=='positive-log':return [a/k,a/k*(p['base']**k+1),ans,a/k*p['base']**k,p['base']**k-1]
 if t=='negative-log':return [a*sp.Rational(20,9),a*sp.Rational(20,81),a*sp.Rational(2,27),a*sp.Rational(16,9),a*sp.Rational(8,81)]
 if t=='negative-coefficient-log':return [a*sp.Rational(5,16),a*sp.Rational(15,32),a*sp.Rational(3,16),a*sp.Rational(15,16),a*sp.Rational(5,8)]
 if t=='product':return [k*E,E/k,-sp.exp(x**2)/k,E,sp.exp(k*x/2)/k]
 return [ans]

def bounds(c,p):
 if set(p)!=set(c['parameters']):raise ValueError('Parameter shape')
 if any(not isinstance(v,(int,str)) for v in p.values()):raise ValueError('Exact parameters only')
 a,k=sp.Rational(p['a']),sp.Rational(p['k'])
 if a==0 or k==0 or abs(a)>20 or abs(k)>12:raise ValueError('Nonzero bounded coefficient/slope')
 if c['profile']=='negative-log' and (k!=-4 or p['base']!=3):raise ValueError('Sparse observed bank fixes slope/base')
 if c['profile']=='negative-coefficient-log' and (k!=-2 or p['base']!=4):raise ValueError('Sparse observed bank fixes slope/base')
 if c['profile']=='unit-definite' and (a!=k or k!=sp.Rational(1,p['H']) or p['H']<=1):raise ValueError('Unit transformed limits')
 if c['profile']=='product' and (a!=1 or p['b']!=0 or k<=0):raise ValueError('Equal exponent product')
 if c['profile']=='legacy' and (k>=0 or a<=0):raise ValueError('Source signed features')
 if c['profile']=='fraction-shift' and (a!=1 or not 0<k<1):raise ValueError('Reciprocal slope')
 if c['profile']=='scaled' and (a<=0 or k<=0 or a==k or k==1):raise ValueError('Distinct bank coefficients')
 if 'bound' in p:
  if p['bound']=='log' and p['b']!=0:raise ValueError('Observed log families have zero shift')
  if p['bound']=='log' and not 2<=p['base']<=6:raise ValueError('Log base range')
  _,_,L,H=math(p)
  if not L<H:raise ValueError('Ordered limits')

def render(c,p):
 a,k,b=sp.Rational(p['a']),sp.Rational(p['k']),sp.Rational(p.get('b',0));f,ans,L,H=math(p)
 v='z' if c['profile']=='product' else 'x';kt=tex(k*x+b).replace('x',v);ft=tex(f).replace('x',v)
 body=ft
 if c['profile']=='product':body=tex(sp.exp(k*x/2)).replace('x',v)*2
 integral=r'\int '+body+r'\,\text{d}'+v
 if 'bound' in p:integral=r'\int_{'+tex(L)+'}^{'+tex(H)+'}'+ft+r'\,\text{d}'+v
 if c['field_type']=='blank':problem='Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$  \n{{field-1}}'
 elif c['profile']=='fraction-shift':problem='Calculate $'+integral+'.$'
 elif c['profile']=='legacy':problem='What is $'+integral+'$?'
 elif c['source_id'] in ('q-13775',):problem='Evaluate $'+integral+'.$'
 elif c['source_id']=='q-30922':problem='Evaluate the integral $'+integral+'.$'
 else:problem='$'+integral+'=$'
 prefix=''
 if c['profile']=='product':prefix='First, we notice that\n\n$$\n'+integral+'='+r'\int '+ft+r'\,\text{d}'+v+'.\n$$\n\n'
 solution=prefix+'If we let $u='+kt+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+v+'}='+tex(k)+r'\quad\Longrightarrow\quad\text{d}'+v+'='+tex(1/k)+r'\,\text{d}u.'+'\n$$\n\n'
 if 'bound' in p:
  lo=k*L+b;hi=k*H+b
  solution+='Computing our limits of integration, we get the following:\n\n| $'+v+'$ | $'+tex(L)+'$ | $'+tex(H)+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
  I=r'\int_{'+tex(L)+'}^{'+tex(H)+'}'+tex(sp.exp(k*x+b))+r'\,\text{d}x'
  U=r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}{e}^{u}\,\text{d}u'
  first=integral+'&='+tex(a)+I
  subst='&='+tex(a)+r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}{e}^{u}\cdot '+tex(1/k)+r'\,\text{d}u'
  pull='&='+tex(a/k)+U
  ev='&='+tex(a/k)+r'\left[{e}^{u}\right]_{'+tex(lo)+'}^{'+tex(hi)+'}'
  exponent='&='+tex(a/k)+r'\left({e}^{'+tex(hi)+'}-{e}^{'+tex(lo)+r'}\right)'
  exact='&='+tex(a/k)+r'\left('+tex(sp.exp(hi))+'-'+tex(sp.exp(lo))+r'\right)'
  final='&='+tex(ans)
  if c['profile']=='unit-definite':rows=[integral+'&='+U,'&='+r'\left[{e}^{u}\right]_{0}^{1}',exponent,exact,final]
  elif p['bound']=='log':
   n=p['base'];power=sp.Integer(n)**k
   logpull='&='+tex(a/k)+r'\int_{0}^{\ln('+str(n)+'^{'+tex(k)+r'})}{e}^{u}\,\text{d}u'
   symbolic='&='+tex(a/k)+r'\left('+str(n)+'^{'+tex(k)+r'}-1\right)'
   numerical='&='+tex(a/k)+r'\left('+tex(power)+r'-1\right)'
   product='&='+tex(a/k)+r'\cdot '+tex(power-1)
   rows=[first,subst,logpull,ev,exponent,symbolic,numerical,product,final]
   if c['source_id']=='q-13786':rows.insert(6,'&='+tex(a/k)+r'\left(\frac{1}{'+str(n)+'^{'+tex(-k)+r'}}-1\right)')
   if c['source_id'] in ('q-30922','q-349596'):rows.pop(-2)
  elif c['source_id']=='q-349601':rows=[first,subst,pull,ev,exponent,final]
  else:rows=[first,subst,pull,ev,exponent,exact,final]
 else:
  rows=[r'\int '+ft+r'\,\text{d}'+v+'&='+r'\int '+tex(a)+r'{e}^{u}\cdot '+tex(1/k)+r'\,\text{d}u','&='+tex(a/k)+r'\int {e}^{u}\,\text{d}u','&='+tex(a/k)+r'{e}^{u}+C','&='+tex(ans).replace('x',v)+'+C']
  if c['profile']=='product':rows.insert(0,r'\int '+ft+r'\,\text{d}z&=\int {e}^{'+tex(k)+r'(u/'+tex(k)+r')}\cdot '+tex(1/k)+r'\,\text{d}u')
  if c['profile']=='product':rows[1]='&='+rows[1].split('&=')[1]
 solution+='Then, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return problem,solution

def sample(c,rng):
 p=dict(c['parameters']);t=c['profile'];a=sp.Rational(p['a']);k=sp.Rational(p['k'])
 if t=='fraction-shift':p.update(k='1/'+str(rng.randint(2,10)),b=rng.randint(-5,5))
 elif t=='unit-definite':h=rng.randint(2,10);p.update(a='1/'+str(h),k='1/'+str(h),H=h)
 elif t=='product':p['k']=2*rng.randint(1,6)
 elif t in ('negative-log','negative-coefficient-log'):p['a']=rng.randint(1,20)*(1 if a>0 else -1)
 else:
  p['a']=rng.randint(2,20)*(1 if a>0 else -1);p['k']=rng.randint(2,10)*(1 if k>0 else -1)
  if p.get('bound')=='log':p['base']=rng.randint(2,6)
  if 'bound' not in p or p.get('bound')=='numeric':p['b']=rng.randint(-4,4)
 return p

def generate(level='easy',seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported hard band: no source evidence')
 rng=random.Random(seed);eligible=[c for c in CASES if c['level']==level];c=next((c for c in eligible if c['template']==template),None) if template else rng.choice(eligible)
 if c is None or profile not in (None,c['profile']):raise ValueError('Unsupported template/profile')
 for attempt in range(300):
  p=parameters or sample(c,rng)
  try:
   bounds(c,p);values=bank(c,p)
   if any(sp.simplify(v-w)==0 for i,v in enumerate(values) for w in values[:i]):raise ValueError('Equivalent options')
   ans=math(p)[1];matches=[i for i,v in enumerate(values) if sp.simplify(v-ans)==0]
   if len(matches)!=1:raise ValueError('Unique correct value')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('Bounded resampling exhausted')
 problem,solution=render(c,p);fp=fingerprint({':question/problem':problem});qid=uid(VERSION+'/'+c['template']+'/'+digest(p));fid=uid(qid+'/field')
 choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/math',':answer/value':tex(v).replace('x','z' if c['profile']=='product' else 'x')+(' + C' if 'bound' not in p else '')} for i,v in enumerate(values)]
 f={':answer-field/id':fid,':answer-field/key':'field-1' if c['field_type']=='blank' else 'selection',':answer-field/type':':answer-field.type/'+c['field_type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[matches[0]][':answer/id']]}
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[f]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':c['template'],'profile':c['profile'],'parameters':p,'domain':'real x; nonzero linear slope; ordered finite limits','source_ids':[c['source_id']],'math_fingerprint':fp,'dependencies':{'sympy':sp.__version__},'solution_policy':'Preserved substitution sentences and sequence; corrected differential variables; standardized TeX'}}

def batch(level,count,seed=0,template=None,profile=None):
 out=[];seen=set()
 for i in range(max(200,count*100)):
  if len(out)>=count:break
  r=generate(level,seed+i,template,profile=profile);fp=r['generation']['math_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 return out

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();out=batch(args.difficulty,args.count,args.seed,args.template);print(json.dumps(out,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,out)))
