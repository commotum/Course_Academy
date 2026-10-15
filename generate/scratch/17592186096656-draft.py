#!/usr/bin/env python3
"""General-base affine exponential integrals, private basis2275 draft.
Raw source masks vary the base and recompute every dependent endpoint/bank.
Normal masks use complete method-derived banks; opaque historical banks remain
public evidence. All dependencies, formatter, parser and native checker frozen
under this file's private evidence directory. No database operations or plots.
"""
import argparse,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
HERE=Path(__file__).with_suffix('')
def local(name):
 spec=importlib.util.spec_from_file_location('exp96656_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=local('math_format');parser=local('scalar_parser');x=parser.X;u=s.Symbol('u');C=s.Symbol('C')
VERSION='general-base-affine-private-2275-v1';KP_ID=17592186096656
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];CASES=json.loads((HERE/'source-cases.json').read_text());MASKS=json.loads((HERE/'masks.json').read_text());CA={c['template']:c for c in CASES}
SUPPORTED_LEVELS=('easy','moderate','hard')
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(t):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),t))
def task_fingerprint(f,limits):
 rate=s.cancel(s.expand_log(s.simplify(s.diff(f,x)/f),force=True));amp=s.cancel(f.subs(x,0))
 return digest([s.srepr(rate),s.srepr(amp),list(limits)if limits is not None else None,'real'])
def tex(z):return s.latex(s.sympify(z),ln_notation=True).replace(r'\left','').replace(r'\right','')
def strict_int(z,name):
 if type(z)is not int:raise ValueError(name+' must be a built-in integer')
 return z
def raw_scalar(v,n,spaced=False):
 # Source uses rational coefficient/(ln base), with denominator product intact.
 v=s.Rational(v);log=r'\operatorname{ln}'+('⁡'if spaced else '')+str(n)
 sign='-'if v<0 else '';p,q=abs(v.p),v.q
 return sign+r'\frac{'+str(p)+'}{'+(''if q==1 else str(q))+log+'}'
def base_slots(t,n):
 p=CA[t]['anchor_parameters'];k=s.Rational(p['k']);a=s.Rational(p['a']);b=s.Rational(p['b']);out={'n':str(n)}
 if 'L'in p:
  lo=k*p['L']+b;hi=k*p['H']+b;lower=s.Integer(n)**lo;upper=s.Integer(n)**hi;v=a*(upper-lower)/k
  out.update(lower=tex(lower),upper=tex(upper),delta=tex(n**6-1),halfdelta=tex(s.Rational(n**6-1,2)),radio_last=tex(s.Rational(n**5-1,2)),final_op=raw_scalar(v,n),final_op_spaced=raw_scalar(v,n,True))
 return out
def source_render(t,n):
 slots=base_slots(t,n);mask=MASKS[t]
 def fill(z):
  if z is None:return None
  return re.sub('§([^§]+)§',lambda m:slots[m[1]],z)
 return fill(mask['problem']),fill(mask['solution']),[fill(v)for v in mask['values']]
def scalar_tex(p):
 n=s.Integer(p['n']);k=s.Rational(p['k']);v=s.Rational(p['a'])*(n**(k*p['H']+p['b'])-n**(k*p['L']+p['b']))/k
 return raw_scalar(v,n).replace(r'\operatorname{ln}',r'\ln ')
def params_for_source(t,p):
 if type(p)is not dict or set(p)!={'n'}:raise ValueError('Source masks accept exactly n')
 n=strict_int(p['n'],'n')
 if n not in range(2,10):raise ValueError('Base must be integer 2..9')
 if 'L' in CA[t]['anchor_parameters']:
  ap=CA[t]['anchor_parameters'];e=[s.Rational(ap['k'])*ap[v]+ap['b'] for v in ('L','H')]
  if max(s.Integer(n)**abs(v) for v in e)>4096:raise ValueError('Definite arithmetic ceiling 4096')
 return {**CA[t]['anchor_parameters'],'n':n}
def exact_math(p):
 n=s.Integer(p['n']);k=s.Rational(p['k']);a=s.Rational(p['a']);b=s.Rational(p['b']);f=a*n**(k*x+b);F=a*n**(k*x+b)/(k*s.log(n))
 return f,s.simplify(F.subs(x,p['H'])-F.subs(x,p['L']))if'L'in p else F

def record(level,seed,t,profile,p,prompt,solution,values,index,kind,raw=False):
 if not raw:
  prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);values=[fmt.normalize_tex(v)for v in values]
 presence={'difficulty':not raw or MASKS[t]['level_present'],'solution':solution is not None,'correct':index is not None}
 content=digest([VERSION,prompt,solution,kind,sorted(values),presence,level if presence['difficulty']else None,values[index]if index is not None else None]);qid=uid(content);fid=uid(qid+'/field')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 f={':answer-field/id':fid,':answer-field/key':'field-1'if kind=='blank'else'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if index is not None:f[':answer-field/correct']=[':answer/id',answers[index][':answer/id']]
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
 if presence['difficulty']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 fexpr,_=exact_math(p);fp=task_fingerprint(fexpr,(p['L'],p['H'])if'L'in p else None)
 result={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'math_fingerprint':fp,'mathematical_fingerprint':fp,'content_hash':content,'domain':'real x; positive integer base other than 1; nonzero rational slope','source_ids':[t]if t in CA else [],'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':t=='affine' or (t in CA and CA[t]['difficulty_authored'] and not raw),'provenance':{k:v for k,v in SOURCE.items()if k!='record'},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'formatter':fmt.FORMAT_VERSION}}}

 if not raw:fmt.validate_generated_record(result)
 return result

def check_bank(values,correct,definite):
 exprs=[parser.scalar(z).subs(C,0)for z in values]
 def signature(v):
  d=s.diff(v,x)
  if d==0:return (s.Integer(0),s.Integer(0))
  return (s.cancel(s.diff(d,x)/d),s.cancel(d.subs(x,0)))
 if definite:
  def equal(a,b):return s.cancel(s.expand_log(a-b,force=True))==0
 else:
  def equal(a,b):return signature(a)==signature(b)
 if any(equal(v,w)for i,v in enumerate(exprs)for w in exprs[:i]):raise ValueError('Whole-bank equivalent primitives or values')
 if sum(equal(v,correct)for v in exprs)!=1:raise ValueError('Unique mathematically correct answer required')

def normal_source(t,n):
 p=params_for_source(t,{'n':n});prompt,solution,_=source_render(t,n);f,F=exact_math(p);E=s.Integer(n)**(s.Rational(p['k'])*x+p['b']);k=s.Rational(p['k']);a=s.Rational(p['a'])
 if solution is None:prompt,solution=worked(p,False,kind='radio')
 prompt=prompt.replace('Do not round the answer.','Give an exact answer.')
 if'L'in p:
  if CA[t]['field_type']=='blank':values=[scalar_tex(p)];kind='blank'
  else:
   n=s.Integer(n);k=s.Rational(p['k']);lo=n**(k*p['L']+p['b']);hi=n**(k*p['H']+p['b']);values=[tex(z)for z in (F,k*F,s.log(n)*F,-F,a*(hi+lo)/(k*s.log(n)))];kind='radio'
 else:
  # Five complete method-derived mistakes, specialized before parameters.
  if k==-1:wrong=[-E,E/s.log(n),n**(-k*x-p['b'])/s.log(n),-n**(-k*x-p['b'])/s.log(n)]
  elif 0<k<1:wrong=[k*E/s.log(n),E/s.log(n),E/k,s.Integer(n)**x/(k*s.log(n))]
  else:wrong=[E/k,E/s.log(n),-F,s.Integer(n)**(x+p['b'])/s.log(n)]
  values=[tex(z)+'+C'for z in [F,*wrong]];kind='radio'
 check_bank(values,F,'L'in p)
 return p,prompt,solution,values,kind

def mul(z):return '('+tex(z)+')'
def exptex(n,z):return '{'+str(n)+'}^{'+tex(z)+'}'
def integral(n,z,a=1,lo=None,hi=None,var='x'):
 limits=''if lo is None else '_{'+tex(lo)+'}^{'+tex(hi)+'}'
 return r'\int'+limits+' '+(''if a==1 else tex(a)+r'\cdot ')+exptex(n,z)+r'\,\text{d}'+var

def worked(p,definite,kind='blank'):
 n=s.Integer(p['n']);a=s.Rational(p['a']);k=s.Rational(p['k']);b=s.Rational(p['b']);z=k*x+b;f,F=exact_math(p)
 L=p.get('L');H=p.get('H');I=integral(n,z,a,L,H);Fu=r'\frac{'+exptex(n,u)+r'}{\ln '+str(n)+'}'
 prompt=('Evaluate the following integral. Give an exact answer.\n\n$'+I+'=$  \n{{field-1}}')if kind=='blank'else 'What is $'+I+'$?'
 solution='If we let $u='+tex(z)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(k)+r'\quad\Longrightarrow\quad '+tex(1/k)+r'\,\text{d}u=\text{d}x.'+'\n$$\n\n'
 if definite:
  lo=k*L+b;hi=k*H+b
  solution+='Computing our limits of integration, we get the following:\n\n| $x$ | $'+tex(L)+'$ | $'+tex(H)+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
  substituted=integral(n,u,a,lo,hi,'u').replace(r'\,\text{d}u',r'\cdot '+mul(1/k)+r'\,\text{d}u')
  rows=[I+' & ='+substituted,' & ='+mul(a/k)+integral(n,u,1,lo,hi,'u'),' & ='+mul(a/k)+'('+Fu+r')|_{'+tex(lo)+'}^{'+tex(hi)+'}',' & ='+mul(a/(k*s.log(n)))+'('+exptex(n,hi)+'-'+exptex(n,lo)+')',' & ='+mul(a/(k*s.log(n)))+'('+tex(n**hi)+'-'+tex(n**lo)+')',' & ='+scalar_tex(p)]
 else:
  rows=[I+' & ='+integral(n,u,a,var='u').replace(r'\,\text{d}u',r'\cdot '+mul(1/k)+r'\,\text{d}u'),' & ='+mul(a/k)+integral(n,u,var='u'),' & ='+mul(a/k)+Fu+'+C',' & ='+tex(F)+'+C']
 solution+='Then, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,solution

# EASY: indefinite a^linear, observed negative/unit, integer and reciprocal
# slopes. The expanded affine family uses exactly the canonical four stages.
# No definite limits or external scale in this level.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed definite integral families; expanded family allows either
# a nonunit slope or a nonunit outside coefficient, retaining six source stages.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored): same substitution/limits/primitive/evaluation method, jointly
# nonunit scale and slope, nonzero shift. No nonlinear substitution/new operators.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def authored_bounds(level,p):
 keys={'a','k','b','n'}|({'L','H'}if level!='easy'else set())
 if type(p)is not dict or set(p)!=keys:raise ValueError('Exact authored parameter shape required')
 for key,v in p.items():strict_int(v,key)
 a,k,b,n=[p[t]for t in ('a','k','b','n')]
 if n not in range(2,7)or k==0 or abs(k)>3 or abs(b)>3 or not 1<=a<=3:raise ValueError('Authored coefficient bounds')
 if level=='easy':
  if a!=1 or abs(k)<2:raise ValueError('Expanded easy unit external coefficient and nonunit slope bank')
 else:
  if not(p['L']in(0,1)and p['H']in(1,2,3)and p['L']<p['H']):raise ValueError('Ordered integer limits -2..3')
  if not all(-2<=k*t+b<=6 and s.Integer(n)**abs(k*t+b)<=4096 for t in (p['L'],p['H'])):raise ValueError('Endpoint exponent workload -2..6')
  if level=='moderate'and not(a==1 or abs(k)==1):raise ValueError('Moderate has at most one nonunit scale')
  if level=='hard'and not(2<=a<=3 and 2<=abs(k)<=3 and b!=0):raise ValueError('Hard jointly nonunit scales and nonzero affine shift')
 return p

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown level')
 strict_int(seed,'seed')
 if template is not None and template not in {*CA,'affine'}:raise ValueError('Unknown template')
 if profile not in (None,'observed_raw','method'):raise ValueError('Unknown profile')
 if field_type not in (None,'radio','blank'):raise ValueError('Unknown field type')
 if profile=='observed_raw'and template not in CA:raise ValueError('Raw profile requires an observed template')
 rng=random.Random(seed)
 if template is None:
  eligible=[t for t,c in CA.items()if c['level']==level and(field_type is None or field_type==c['field_type'])]
  if field_type in (None,'radio'if level=='easy'else'blank'):eligible+=['affine']
  if not eligible:raise ValueError('Unsupported field at this level')
  template=rng.choice(eligible)
 raw=profile=='observed_raw'
 if template in CA:
  c=CA[template]
  if c['level']!=level:raise ValueError('Source level mismatch (unrated evidence has authored easy route only)')
  if field_type not in(None,c['field_type']):raise ValueError('Observed answer shape fixed')
  if parameters is not None:params_for_source(template,parameters)
  for _ in range(200):
   n=parameters['n']if parameters is not None else rng.randint(2,9)
   try:
    p=params_for_source(template,{'n':n})
    if raw:
     prompt,solution,values=source_render(template,n);index=MASKS[template]['correct_index'];kind=c['field_type']
     # Known raw omissions remain omitted; bank mathematics independently audited.
     return record(level,seed,template,'observed_raw',p,prompt,solution,values,index,kind,True)
    p,prompt,solution,values,kind=normal_source(template,n)
    return record(level,seed,template,'method',p,prompt,solution,values,0,kind)
   except ValueError:
    if parameters is not None:raise
  raise ValueError('Whole-bank sampling exhausted')
 kind='radio'if level=='easy'else'blank'
 if field_type not in(None,kind):raise ValueError('Expanded authored family response shape fixed')
 for _ in range(2000):
  p=parameters if parameters is not None else dict(a=1 if level=='easy'else rng.randint(1,3),k=rng.choice([-3,-2,-1,1,2,3]),b=rng.randint(-3,3),n=rng.randint(2,6))
  if parameters is None and level!='easy':p.update(L=rng.choice([0,1]),H=rng.randint(1,3))
  try:
   authored_bounds(level,p);prompt,solution=worked(p,level!='easy',kind);f,F=exact_math(p)
   if kind=='blank':values=[scalar_tex(p)]
   else:
    n=s.Integer(p['n']);k=s.Rational(p['k']);E=n**(k*x+p['b']);values=[tex(z)+'+C'for z in (F,E/k,E/s.log(n),-F,n**(-k*x-p['b'])/(k*s.log(n)))]
   check_bank(values,F,level!='easy')
   return record(level,seed,'affine','method',dict(p),prompt,solution,values,0,kind)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('Authored bounded sampling exhausted')

def batch(level,count,seed=0,template=None,profile=None):
 strict_int(count,'count')
 if count<1:raise ValueError('Positive count required')
 if template in CA:
  capacity=0
  for n in range(2,10):
   try:params_for_source(template,{'n':n});capacity+=1
   except ValueError:pass
  if count>capacity:raise ValueError('Requested count exceeds the finite source-template mathematical domain')
 out=[];seen=set()
 for i in range(max(1000,count*100)):
  r=generate(level,seed+i,template,profile=profile);fp=r['generation']['math_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('Requested count exceeds sampled unique task domain')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[raw source has no worked solution]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args();levels=SUPPORTED_LEVELS if args.difficulty=='all'else[args.difficulty];out=[r for l in levels for r in batch(l,args.count,args.seed,args.template,args.profile)];print(json.dumps(out,indent=2)if args.format=='json'else'\n\n'.join(map(markdown,out)))
