#!/usr/bin/env python3
"""KP68916: frozen-basis2275 reciprocal-trigonometric substitution templates.

Source-backed E/M/H; exact finite rational slots, complete source bank profiles,
served parameterized solutions with source row omissions preserved. No EDB writes.
The nonlinear sec source is ineligible reference-only at original parameters: the
lesson route places derivative-proportional nonlinear substitution after this KP.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
sp=importlib.util.spec_from_file_location('kp68916_format',HERE/'reference/math_format.py');fmt=importlib.util.module_from_spec(sp);sp.loader.exec_module(fmt)
KP=17592186068916;VERSION='reciprocal-linear-2275-v1'
SOURCE=json.loads((HERE/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,u,C=s.symbols('x u C',real=True)
# level, field kind, integrand family, source parameters
CONFIG={
'q-10143':('easy','radio','sec_tan',{'a':'7','b':'0','c':1}),
'q-10157':('easy','radio','csc_cot',{'a':'8','b':'0','c':1}),
'q-113983':('easy','radio','poly_sec',{'a':'1','b':'0','c':1,'d':1}),
'q-2203':('easy','radio','sec_tan',{'a':'10','b':'0','c':1}),
'q-13663':('moderate','radio','csc2',{'a':'3','b':'0','c':2,'lo':'1/3','hi':'1/2'}),
'q-355818':('moderate','blank','csc2',{'a':'5','b':'0','c':5,'lo':'1/4','hi':'1/2'}),
'q-346368':('hard','blank','csc_cot',{'a':'1/4','b':'0','c':1,'lo':'1/6','hi':'1/2'}),
'q-350060':('hard','blank','sec2',{'a':'1','b':'-1/4','c':3,'lo':'-1/4','hi':'0'}),
'q-350071':('hard','blank','csc_cot',{'a':'1','b':'-1/6','c':4,'lo':'1/6','hi':'1/2'}),
'q-10578':('hard','radio','sec_tan',{'a':'1','b':'-1/3','c':1,'lo':'-1/3','hi':'1/6'}),
}
ENDPOINTS={
'q-13663':(('1/3','1/2'),('1/4','1/2'),('1/6','1/2')),
'q-355818':(('1/3','1/2'),('1/4','1/2'),('1/6','1/2')),
'q-346368':(('1/6','1/2'),('1/4','1/2'),('1/3','1/2')),
'q-350060':(('-1/4','0'),('-1/3','0'),('0','1/4')),
'q-350071':(('1/6','1/2'),('1/4','1/2'),('1/3','1/2')),
'q-10578':(('-1/3','1/6'),('-1/4','1/3'),('-1/3','1/4')),
}
SEC_ANGLES=('-1/3','-1/4','0','1/6','1/4','1/3');CSC_ANGLES=('1/6','1/4','1/3','1/2','2/3','3/4','5/6')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+v))
def rat(v):
 if type(v)is not str or not __import__('re').fullmatch(r'-?(?:0|[1-9]\d*)(?:/[1-9]\d*)?',v):raise ValueError('rational slots require canonical rational strings')
 z=s.Rational(v)
 if str(z)!=v:raise ValueError('rational slots require reduced canonical spelling')
 return z

def tex(v):return fmt.normalize_tex(s.latex(v,fold_short_frac=False))
def atom(t):return '('+t+')'
def fn(name,arg,power=None):return '\\'+name+(f'^{{{power}}}' if power else '')+'('+arg+')'
def product(c,t):
 c=s.sympify(c)
 if t.startswith('-'):return product(-c,t[1:])
 return t if c==1 else '-'+t if c==-1 else tex(c)+t

def integrand(kind,arg,p):
 if kind=='sec_tan':return fn('sec',arg)+fn('tan',arg)
 if kind=='csc_cot':return fn('csc',arg)+fn('cot',arg)
 if kind=='sec2':return fn('sec',arg,2)
 if kind=='csc2':return fn('csc',arg,2)
 return '('+product(p['c'],fn('sec',arg,2))+'+'+tex(p['d'])+')'+fn('sec',arg)+fn('tan',arg)
def primitive(kind,arg,p):
 if kind=='sec_tan':return fn('sec',arg)
 if kind=='csc_cot':return '-'+fn('csc',arg)
 if kind=='sec2':return fn('tan',arg)
 if kind=='csc2':return '-'+fn('cot',arg)
 return tex(p['c']/s.Integer(3))+fn('sec',arg,3)+'+'+product(p['d'],fn('sec',arg))
def fun(kind,z):return {'sec_tan':s.sec(z)*s.tan(z),'csc_cot':s.csc(z)*s.cot(z),'sec2':s.sec(z)**2,'csc2':s.csc(z)**2}[kind]
def prim(kind,z):return {'sec_tan':s.sec(z),'csc_cot':-s.csc(z),'sec2':s.tan(z),'csc2':-s.cot(z)}[kind]
def integral(body,var='x',bounds=None):return '\\int'+('_{'+tex(bounds[0])+'}^{'+tex(bounds[1])+'}' if bounds else '')+' '+body+r'\,\text{d}'+var

def guard(sid,p):
 level,field,kind,orig=CONFIG[sid]
 if type(p)is not dict or set(p)!=set(orig):raise ValueError('unexpected or missing parameter slots')
 if type(p['c'])is not int or not 1<=p['c']<=6:raise ValueError('c must be an integer1..6')
 a,b=rat(p['a']),rat(p['b'])
 if kind=='poly_sec':
  if p!=orig:raise ValueError('nonlinear source is reference-only at original parameters; outside linear-argument curriculum')
 elif level=='easy':
  if a not in range(2,11) or b!=0 or p['c']>5:raise ValueError('easy positive integer scale2..10, zero shift, coefficient1..5')
 elif level=='moderate':
  if a not in range(2,7) or b!=0:raise ValueError('moderate scale2..6, zero shift')
 else:
  allowed=('1/2','1/3','1/4') if sid=='q-346368' else ('1','2','3','4')
  bs=('0',) if sid=='q-346368' else ('-1/6','-1/4','-1/3','1/6','1/4','1/3')
  if p['a']not in allowed or p['b']not in bs:raise ValueError('outside hard reciprocal-scale or shifted linear workload')
 if level!='easy':
  lo,hi=rat(p['lo']),rat(p['hi']);angles=SEC_ANGLES if kind.startswith('sec') else CSC_ANGLES
  if (p['lo'],p['hi'])not in ENDPOINTS[sid] or p['lo']not in angles or p['hi']not in angles or lo>=hi:raise ValueError('familiar endpoint angles in a common pole-free component required')
  if sid=='q-13663' and p['lo']not in ('1/6','1/4','1/3'):raise ValueError('source radio bank lower angle requires positive cotangent')
  # The entire public explicit-parameter interface shares these bounded slots.
 return a,b

def instances(sid):
 level,_,kind,orig=CONFIG[sid]
 if kind=='poly_sec':
  yield dict(orig)
 elif level=='easy':
  for a,c in itertools.product(range(2,11),range(1,6)):yield {'a':str(a),'b':'0','c':c}
 else:
  aa=range(2,7) if level=='moderate' else ('1/2','1/3','1/4') if sid=='q-346368' else range(1,5)
  bs=('0',) if level=='moderate' or sid=='q-346368' else ('-1/6','-1/4','-1/3','1/6','1/4','1/3')
  angles=SEC_ANGLES if kind.startswith('sec') else CSC_ANGLES
  for a,b,c,(lo,hi) in itertools.product(aa,bs,range(1,7),ENDPOINTS[sid]):
   p={'a':str(a),'b':b,'c':c,'lo':lo,'hi':hi}
   try:guard(sid,p)
   except ValueError:continue
   yield p

def core(sid,p,profile):
 level,field,kind,_=CONFIG[sid];a,b=guard(sid,p);c=s.Integer(p['c']);arg=a*x+b*s.pi;A=tex(arg);r=c/a
 definite=level!='easy';lo=rat(p['lo'])*s.pi if definite else None;hi=rat(p['hi'])*s.pi if definite else None
 xb=((lo-b*s.pi)/a,(hi-b*s.pi)/a) if definite else None
 body=integrand(kind,A,p) if kind=='poly_sec' else product(c,integrand(kind,A,p))
 I=integral(body,bounds=xb)
 if kind=='poly_sec':
  correct=c*s.sec(x)**3/3+p['d']*s.sec(x)+C
  values=[c*s.tan(x)**3/3+p['d']*s.tan(x)+C,c*s.sec(x)**2/2+C,correct,c*s.sec(x)**3/3+C,c*s.tan(x)**3/3+p['d']*s.sec(x)+C]
 elif not definite:
  correct=r*prim(kind,arg)+C
  if sid=='q-2203':values=[c*a*s.sec(arg)+C,r*s.csc(arg)+C,c*s.sec(arg)**2+C,r*s.sec(x)+C,correct]
  else:
   F=s.sec(arg) if kind=='sec_tan' else s.csc(arg)
   values=[r*F+C,c*F+C,-c*a*F+C,-r*F+C,c*a*F+C] if sid=='q-10143' else [c*F+C,r*F+C,c*a*F+C,-r*F+C,-c*a*F+C]
 else:
  pl,ph=prim(kind,lo),prim(kind,hi);correct=s.simplify(r*(ph-pl))
  if sid=='q-13663':
   delta=s.cot(lo)-s.cot(hi);values=[-a/c*delta,c*a*delta,-c*delta,correct,delta]
  elif sid=='q-10578':
   L,H=s.sec(lo),s.sec(hi)
   if profile=='observed':values=[correct,r*(-H-L/2),r*(s.cot(hi)-L/2),r*(-L*s.cot(hi)+L/2),r*(s.tan(hi)+L)]
   else:values=[correct,-correct,r*(ph+pl),r*ph,r*(s.tan(hi)-s.tan(lo))]
  else:values=[correct]
 values=list(map(s.simplify,values));mathvals=[s.diff(v,x) if not definite else v for v in values]
 # Primitive banks compare derivatives, permitting arbitrary constant shifts.
 for i in range(len(mathvals)):
  for j in range(i):
   diff=mathvals[i]-mathvals[j]
   if diff.has(x):
    numeric=s.N(diff.subs(x,s.Rational(2,7)),24)
    if numeric.is_real and numeric.is_finite and abs(numeric)>s.Float('1e-18'):continue
   if s.trigsimp(diff)==0:raise ValueError('equivalent complete bank members')
 # Prompt source wording; rendered mathematical slots replace entire components.
 if sid in ('q-10143','q-10157','q-113983'):prompt='Calculate the integral $'+I+'.$'
 elif sid in ('q-2203','q-10578'):prompt='$'+I+'=$'
 elif sid=='q-13663':prompt='Evaluate the integral $'+I+'.$'
 else:prompt='Evaluate the following integral. '+('Do not round the answer.' if profile=='observed' else 'Give an exact answer.')+'\n\n$'+I+'=$\n{{field-1}}'
 if kind=='poly_sec':
  opening='If we let $u='+fn('sec','x')+',$ then'
  diff=r'\frac{\text{d}u}{\text{d}x}='+fn('sec','x')+fn('tan','x')+r'\,⟹\,'+fn('sec','x')+fn('tan','x')+r'\,\text{d}x=\text{d}u.'
  rows=[integral('('+product(c,'u^{2}')+'+'+tex(p['d'])+')','u'),tex(c/3)+'u^{3}+'+product(p['d'],'u')+'+C',primitive(kind,'x',p)+'+C']
 else:
  opening='If we let $u='+A+',$ then'
  factor=s.Integer(1)/a
  diff=r'\frac{\text{d}u}{\text{d}x}='+tex(a)+r'\,⟹\,\text{d}x='+('' if factor==1 else tex(factor)+(r'\,' if sid=='q-346368' else ''))+r'\text{d}u.'
  iu=integral(integrand(kind,'u',p),'u',(lo,hi) if definite else None)
  sub=integral(product(c,integrand(kind,'u',p))+(r'\cdot '+tex(factor) if factor!=1 else ''),'u',(lo,hi) if definite else None)
  scaled=product(r,iu)
  if not definite:
   rows=[sub,scaled,product(r,primitive(kind,'u',p))+'+C',tex(correct)]
  else:
   base=primitive(kind,'u',p)
   endpoint=product(r,'('+primitive(kind,tex(hi),p)+'-('+primitive(kind,tex(lo),p)+'))')
   numeric=product(r,'('+tex(ph)+'-('+tex(pl)+'))')
   if kind in ('csc2','csc_cot') and sid!='q-346368':
    positive='cot' if kind=='csc2' else 'csc'
    bracket=product(-r,fn(positive,'u'))+r'\big|_{'+tex(lo)+'}^{'+tex(hi)+'}'
    endpoint=product(-r,'('+fn(positive,tex(hi))+'-'+fn(positive,tex(lo))+')')
    numeric=product(-r,'('+tex(-ph)+'-'+tex(-pl)+')')
   else:
    bracket=product(r,atom(base) if sid=='q-346368' else base)+r'\big|_{'+tex(lo)+'}^{'+tex(hi)+'}'
    if sid=='q-346368':
     endpoint=product(r,'(-'+fn('csc',tex(hi))+'+'+fn('csc',tex(lo))+')')
     numeric=product(r,'(-'+tex(-ph)+'+'+tex(-pl)+')')
   if sid=='q-350060':rows=[scaled,bracket,numeric,tex(correct)]
   elif sid=='q-10578':rows=[scaled,bracket,endpoint,tex(correct)]
   else:rows=[sub,scaled,bracket,endpoint,numeric,tex(correct)]
 table=''
 if definite:table='Calculating the limits for $u$ gives'+(' ' if sid=='q-10578' else '')+'\n\n| $x$ | $'+tex(xb[0])+'$ | $'+tex(xb[1])+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
 sentence='Using the above, we can '+('rewrite' if sid=='q-346368' else 'write')+' the integral in terms of $u$ and evaluate:'
 solution=opening+'\n\n$$\n'+diff+'\n$$\n\n'+table+sentence+'\n\n$$\n'+r'\begin{aligned}'+I+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,solution,values,correct,{'integrand':str((p['c']*s.sec(x)**2+p['d'])*s.sec(x)*s.tan(x)) if kind=='poly_sec' else str(c*fun(kind,arg)),'bounds':list(map(str,xb)) if definite else None,'argument':str(arg),'primitive':str(correct),'stage_count':len(rows)}

@fmt.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(seed)is not int:raise ValueError('seed must be an integer, excluding bool')
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio','blank'):raise ValueError('unknown field type')
 if profile not in (None,'observed','method'):raise ValueError('profile must be observed or method')
 eligible=[k for k,v in CONFIG.items() if v[0]==level and (not field_type or v[1]==field_type) and (k!='q-113983' or template==k and profile=='observed')]
 if template is not None and template not in eligible:raise ValueError('template/field/difficulty mismatch')
 if parameters is not None and type(parameters)is not dict:raise ValueError('parameters must be a dictionary')
 rng=random.Random(seed);sid=template or rng.choice(eligible);p=dict(parameters) if parameters is not None else None
 if p is None:
  candidates=list(instances(sid));rng.shuffle(candidates)
  for candidate in candidates:
   try:out=core(sid,candidate,profile or 'method');p=candidate;break
   except ValueError:continue
  else:raise ValueError('no complete eligible banks')
 else:out=core(sid,p,profile or 'method')
 prompt,solution,values,correct,model=out
 prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);vals=[tex(v) for v in values];cv=tex(correct)
 kind=CONFIG[sid][1];key='selection' if kind=='radio' else 'field-1'
 ident=digest([VERSION,level,prompt,solution,kind,sorted(vals),cv]);qid=uid(ident);fid=uid(ident+key)
 choices=[{':answer/id':uid(ident+key+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(ident+key+cv)]}
 domain=('x real on any connected interval with cos(argument)!=0' if CONFIG[sid][2].startswith(('sec','poly')) else 'x real on any connected interval with sin(argument)!=0') if level=='easy' else 'closed x interval; transformed endpoints ordered in one pole-free component; all operands finite real'
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':sid,'parameters':p,'bank_profile':profile or 'method','source_id':sid,'source_basis':2275,'source_lineage':SOURCE['lineage'],'eligible_for_learning':sid!='q-113983','evidence_only':sid=='q-113983','scope_role':'reference-only nonlinear source; plausible source misassignment' if sid=='q-113983' else 'linear-argument curriculum practice','source_repairs':['authored easy rating, derivative-verified key and source-style solution'] if sid=='q-10157' else [],'domain':domain,'model':model,'mathematical_fingerprint':digest([model['integrand'],model['bounds']]),'content_fingerprint':ident,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'math_format':'frozen local copy'}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def capacity(level,template=None,field_type=None,profile=None):
 seen=set()
 for sid,conf in CONFIG.items():
  if sid=='q-113983':continue
  if conf[0]!=level or (template and sid!=template) or (field_type and conf[1]!=field_type):continue
  for p in instances(sid):
   try:_,_,_,_,model=core(sid,p,profile or 'method')
   except ValueError:continue
   seen.add(digest([model['integrand'],model['bounds']]))
 return len(seen)
def batch(level,seed=0,count=1,**kw):
 if set(kw)-{'template','field_type','profile'}:raise ValueError('unsupported batch selector')
 if level not in ('all','easy','moderate','hard'):raise ValueError('unknown batch difficulty')
 if type(seed)is not int or type(count)is not int or count<1:raise ValueError('seed/count must be strict integers; count positive')
 if level=='all':return [r for lev in ('easy','moderate','hard') for r in batch(lev,seed,count,**kw)]
 if count==1:return [generate(level,seed,**kw)]
 eligible=[k for k,v in CONFIG.items() if v[0]==level and (k!='q-113983' or kw.get('template')==k and kw.get('profile')=='observed') and (not kw.get('template') or k==kw['template']) and (not kw.get('field_type') or v[1]==kw['field_type'])]
 pool=[(sid,p) for sid in eligible for p in instances(sid)]
 if count>len(pool):raise ValueError(f'count exceeds finite parameter capacity upper bound {len(pool)}')
 random.Random(seed).shuffle(pool);out=[];seen=set()
 for sid,p in pool:
  try:r=generate(level,seed+len(out),template=sid,parameters=p,profile=kw.get('profile'),field_type=kw.get('field_type'))
  except ValueError:continue
  fp=r['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError(f'count exceeds finite meaningful task capacity {len(seen)}')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/id']+' $'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=['observed','method']);ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
 try:out=batch(args.difficulty,args.seed,args.count,template=args.template,profile=args.profile,field_type=args.field_type)
 except ValueError as exc:ap.error(str(exc))
 print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
