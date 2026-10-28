#!/usr/bin/env python3
"""Seeded linear-exponent differentiation; captured math basis 3947.

Easy and moderate preserve source workloads. replay_source() reconstructs the
original parameter anchors and incomplete source contracts from masks. Normal
learning records complete missing fields and use documented repaired banks.
No asset generation, network access, database access or repository runtime paths.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,pathlib,random,sys,uuid
import sys
sys.dont_write_bytecode=True
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186092260
KP_UUID='a83f86ab-a008-5487-b118-f1495a0fe4d6'
TITLE='Differentiating an Exponential Function with a Linear Exponent'
VERSION='linear-e-workspace-5'
DIR=pathlib.Path(__file__).resolve().parent/'data'
MASKS=json.loads((DIR/'masks.json').read_text())
CASES=json.loads((DIR/'source-cases.json').read_text())
CASE={c['template']:c for c in CASES}
X,Y,U=sp.symbols('x y u',real=True)
BASIC=('q-11816','q-11817')
SCALAR_RADIO=BASIC+('q-48007','q-48657')
COEFFICIENTS=tuple(range(-6,-1))+tuple(range(2,7))
OUTER_COEFFICIENTS=tuple(range(-8,-1))+tuple(range(2,9))
CANONICAL=json.loads((DIR/'canonical-source.json').read_text())
FAMILY={'e-727':'direct','q-11816':'direct','q-11817':'direct','q-48003':'direct','q-48007':'direct','q-107420':'power_sum','q-340496':'linear_sum','q-340497':'slope','q-48658':'slope','q-48657':'tangent'}
LEVEL={c['template']:c['level'] for c in CASES}
SOURCE={q[':question/math-academy-id']:q for q in json.loads((DIR/'source-questions.json').read_text())}

def tex(z):
 return sp.latex(sp.sympify(z)).replace(r'\log',r'\ln')
def coeff(n):return '' if n==1 else '-' if n==-1 else str(n)
def linear(a,b,style='standard'):
 if style=='left':return str(b)+('+' if a>0 else '-')+coeff(abs(a))+'x'
 s=coeff(a)+'x'
 if b:s+=('+' if b>0 else '-')+str(abs(b))
 return s
def term(c,e):return coeff(c)+'{e}^{'+e+'}'
def plus(n):return ('+' if n>=0 else '-')+str(abs(n))
def slots(t,p):
 a,b,c,d=(p[k] for k in ['a','b','c','d']);ca=c*a
 ex=linear(a,b,'left' if t in ['q-48003','q-107420','q-340497','q-48658'] else 'standard')
 s={'a_value':str(a),'exponent':ex,'a_group':'{'+str(a)+'}','ax_e':coeff(a)+'xe','a_e':coeff(a)+'e','ce':coeff(c)+'{e}', 'cae':coeff(ca)+'{e}', 'ae':coeff(a)+'{e}', 'negcae':coeff(-ca)+'{e}', 'a_factor':'('+str(a)+')' if a<0 else str(a),'=a.':'='+str(a)+'.','}=a.':'}='+str(a)+'.','plusd':plus(d),'dot_a':r'\cdot '+('('+str(a)+')' if a<0 else str(a)), 'double_shift':linear(a,2*b),'recipcoef':tex(sp.Rational(-c,a))}
 if t=='q-107420':
  n=p['n'];s.update(poly='{x}^{'+str(n)+'}',polyprime=str(n)+'{x}^{'+str(n-1)+'}',factored=str(n)+'({x}^{'+str(n-1)+'}'+('+' if c*a>0 else '-')+'{e}',polysign='+' if c>0 else '-',powerprev='{x}^{'+str(n-1)+'}')
 if t=='q-340496':
  r=p['r'];s.update(poly=coeff(r)+'x',sumrow=str(r)+('+' if a>=0 else '-')+coeff(abs(a))+'{e}',plusr_period=plus(r)+'.',plusr=plus(r),linear_answer=str(r)+('+' if a>0 else '')+term(a,ex))
  # The standalone derivative of the linear term occurs in its own sum row.
 if t in ['q-340497','q-48658']:
  k=p['k'];point=str(b)+'-ln⁡('+str(k)+')';log='ln⁡('+str(k)+')'
  s.update(point=point,subexp=str(b)+'-('+point+')',logk=log,evalproduct=str(ca)+r'\cdot '+str(k),slope=str(ca*k),ca_e=coeff(ca)+'e',b_group='{'+str(b)+'}',k_group='{'+str(k)+'}',b=str(b))
 if t in ['q-340497','q-48658']:s['=slope.']='='+str(ca*p['k'])+'.'
 if t=='q-48657':
  s.update(pointtex=tex(sp.Rational(1,a)),pointraw='1/'+str(a),subexp=str(a)+'(1/'+str(a)+')',caex=coeff(ca)+'ex',ca_e=coeff(ca)+'e',cex=coeff(c)+'ex',c_e=coeff(c)+'e',aex=coeff(a)+'ex',logc='ln⁡('+str(c)+')')
 return s

def render_mask(v,s):
 if isinstance(v,str):
  import re
  return re.sub(r'@@(.*?)@@',lambda m:s[m[1]],v)
 if isinstance(v,list):return [render_mask(w,s) for w in v]
 if isinstance(v,dict):return {k:render_mask(w,s) for k,w in v.items()}
 return v

def simplify_record(v):
 if isinstance(v,list):return list(map(simplify_record,v))
 if isinstance(v,dict):
  if set(v)=={':db/ident'}:return v[':db/ident']
  return {k:simplify_record(w) for k,w in v.items() if k!=':db/id'}
 return v

def math(p,t):
 a,b,c,d=[sp.Integer(p[k])for k in ['a','b','c','d']]
 f=c*sp.exp(a*X+b)+d
 if t=='q-107420':f=X**p['n']+f
 if t=='q-340496':f=p['r']*X+f
 der=sp.diff(f,X)
 if FAMILY[t]=='slope':ans=sp.simplify(der.subs(X,b-sp.log(p['k'])))
 elif FAMILY[t]=='tangent':
  point=(sp.Integer(p.get('t',1))-b)/a;ans=sp.simplify(der.subs(X,point)*(X-point)+f.subs(X,point))
 else:ans=der
 return f,der,ans

def common_solution(p,t):
 a,b,c,d=[p[k]for k in ['a','b','c','d']];name='y' if FAMILY[t]=='tangent' else 'f';e=linear(a,b)
 outer=term(c,'u')+(plus(d)if d else '')
 factor='('+str(a)+')' if a<0 else str(a)
 solution='First, we express $'+name+'$ as the composite function\n\n$$\n'+name+'='+outer+r',\,u='+e+'.\n$$\n\nDifferentiating gives\n\n$$\n'+r'\frac{\text{d}'+name+r'}{\text{d}u}='+term(c,'u')+r',\,\frac{\text{d}u}{\text{d}x}='+str(a)+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'+r'\begin{aligned}\frac{\text{d}'+name+r'}{\text{d}x} & =\frac{\text{d}'+name+r'}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & ='+term(c,'u')+r'\cdot '+factor+r' \\  & ='+term(c*a,'u')+r' \\  & ='+term(c*a,e)+r'.\end{aligned}'+'\n$$'
 return solution

def tangent_question(p):
 a,c,t=p['a'],p['c'],p.get('t',1);z=sp.Rational(t,a);v=c*sp.exp(t);m=a*v
 f,der,ans=math(p,'q-48657')
 prompt='Find the equation of the tangent to the curve $y='+term(c,linear(a,0))+'$ at the point where $x='+tex(z)+'.$'
 solution=common_solution(p,'q-48657')
 solution+='\n\nNow, to find the slope of the tangent to the curve at $x='+tex(z)+'$, evaluate the derivative:\n\n$$\n'+r'\begin{aligned}m &= '+term(c*a,linear(a,0))+r'\big|_{x='+tex(z)+r'} \\ &= '+term(c*a,'('+str(a)+')('+tex(z)+')')+r' \\ &= '+tex(m)+r'.\end{aligned}'+'\n$$'
 solution+='\n\nAlso, the $y$-value of the point on the curve is\n\n$$\n'+r'\begin{aligned}y_1 &= '+term(c,linear(a,0))+r'\big|_{x='+tex(z)+r'} \\ &= '+term(c,'('+str(a)+')('+tex(z)+')')+r' \\ &= '+tex(v)+r'.\end{aligned}'+'\n$$'
 solution+='\n\nFinally, we find the equation of the tangent at that point:\n\n$$\n'+r'\begin{aligned}y-y_1 &=m(x-x_1) \\ y-('+tex(v)+') &= ('+tex(m)+')(x-('+tex(z)+r')) \\ y-('+tex(v)+') &= '+tex(m*X)+'-('+tex(m*z)+r') \\ y &= '+tex(ans)+r'.\end{aligned}'+'\n$$'
 return {':question/problem':prompt,':question/worked-solution':solution}

def guard(t,p,raw=False):
 required={'a','b','c','d'}|({'t'} if t=='q-48657' and 't' in p else set())|({'n'}if t=='q-107420' else {'r'}if t=='q-340496' else {'k'}if FAMILY[t]=='slope' else set())
 if set(p)!=required or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required: '+str(required))
 a,b,c,d=[p[k]for k in ['a','b','c','d']]
 if raw and t=='q-48007'and b==0:raise ValueError('whole observed bank collision: doubled zero shift')
 if raw and t=='q-48658'and (b in [1,p['k']] or b==-c*p['k']):raise ValueError('whole observed scalar bank collision')
 if not (a and c and 1<=abs(a)<=6 and abs(c)<=8 and abs(b)<=8 and abs(d)<=8):raise ValueError('coefficient bounds')
 if t=='q-48657':
  if not (2<=abs(a)<=6 and 2<=abs(c)<=8 and b==d==0 and p.get('t',1) in [-1,0,1,2]):raise ValueError('reciprocal-point tangent profile')
 elif FAMILY[t]=='slope':
  if not(a==-1 and 2<=abs(c)<=8 and d==0 and 2<=p['k']<=6):raise ValueError('shifted-log slope bounds')
 elif t=='q-107420':
  if not(3<=p['n']<=5 and abs(a)==p['n'] and abs(c)==1 and d==0):raise ValueError('power sum: one power-rule term, factored shared derivative scale')
 elif t=='q-340496':
  if not(2<=abs(a)<=6 and c==1 and d==0 and 2<=abs(p['r'])<=8):raise ValueError('linear sum requires both nonzero derivative terms')
 elif t=='q-48003':
  if not(a==-1 and d==0 and 2<=abs(c)<=8):raise ValueError('signed scale reflection')
 elif t=='q-48007':
  if not(2<=abs(a)<=6 and 2<=abs(c)<=6 and d!=0):raise ValueError('scaled translated exponential')
 else:
  if not(c==1 and d==0 and 2<=abs(a)<=6 and (b==0 if t=='q-11816' else b!=0)):raise ValueError('direct exponent profile')

def sampled(t,rng):
 signed=lambda lo,hi:rng.choice([-1,1])*rng.randint(lo,hi)
 p=dict(a=signed(2,6),b=rng.randint(-8,8),c=1,d=0)
 if t=='q-11816':p['b']=0
 if t=='q-11817':p['b']=rng.choice([i for i in range(-8,9)if i])
 if t=='q-48003':p.update(a=-1,c=signed(2,8))
 if t=='q-48007':p.update(c=signed(2,6),d=signed(1,8))
 if t=='q-107420':p.update(c=rng.choice([-1,1]),n=rng.randint(3,5));p['a']=rng.choice([-1,1])*p['n']
 if t=='q-340496':p['r']=signed(2,8)
 if FAMILY[t]=='slope':p.update(a=-1,c=signed(2,8),k=rng.randint(2,6))
 if t=='q-48657':p.update(t=rng.choice([-1,0,1,2]),a=signed(2,6),b=0,c=signed(2,8))
 return p

def authored_bank(t,p,scalar_coefficients=None,outer_coefficients=None):
 f,der,ans=math(p,t);a,b,c,d=[p[k]for k in ['a','b','c','d']];E=sp.exp(a*X+b)
 if FAMILY[t]=='direct':
  if t in SCALAR_RADIO:
   if scalar_coefficients is None:raise ValueError('scalar radio requires shared slope coefficients')
   bank=[ans]+[c*v*E for v in scalar_coefficients if v!=a]
  elif t=='q-48003':bank=[ans,c*E,c*a*X*E,c*a*sp.exp(a*X),c*a*sp.exp(X+b)]
  else:raise ValueError('unknown direct radio family')
 elif FAMILY[t]=='power_sum':
  n=p['n'];bank=[ans,n*X**(n-1)-E,n*X**(n-1)+a*E,X**n-a*E,-a*E]
 elif FAMILY[t]=='linear_sum':
  r=p['r'];bank=[ans,r+E,r+E/a,r-a*E,a*E]
 elif FAMILY[t]=='slope':
  if outer_coefficients is None:raise ValueError('slope radio requires shared outer coefficients')
  k=p['k'];bank=[ans]+[-v*k for v in outer_coefficients if v!=c]
 elif t=='q-48657':
  if scalar_coefficients is None:raise ValueError('tangent radio requires shared slope coefficients')
  target=p.get('t',1);v=c*sp.exp(target)
  bank=[ans]+[v*(s*X+1-target) for s in scalar_coefficients if s!=a]
 else:raise ValueError('unknown bank family')
 if len(bank)!=5 or any(sp.simplify(bank[i]-bank[j])==0 for i in range(5)for j in range(i)):
  raise ValueError('whole-bank equivalence collision')
 return ['y='+tex(sp.expand(v)) if FAMILY[t]=='tangent' else tex(v)for v in bank]

def stable(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,stable(v)))
def identify(q,level,t,p,profile,seed):
 q=copy.deepcopy(q)
 for key in [':question/problem',':question/worked-solution']:
  if key in q:q[key]=normalize_prose(q[key].replace('ln⁡',r'\ln'))
 for field in q.get(':question/answer-fields',[]):
  for answer in field[':answer-field/choices']:answer[':answer/value']=normalize_tex(answer[':answer/value'].replace('ln⁡',r'\ln'))
 # Content IDs depend on actual presentation, never recipe alias/unused parameters/order.
 clean=copy.deepcopy(q);clean.pop(':question/id',None)
 for f in clean.get(':question/answer-fields',[]):
  f.pop(':answer-field/id',None)
  if ':answer-field/correct'in f:
   key=f[':answer-field/correct'];key_id=key[1]if isinstance(key,list)else key[':answer/id']
   designated=next(a[':answer/value']for a in f[':answer-field/choices']if a.get(':answer/id')==key_id)
   f[':answer-field/correct']=[':answer/value',designated]
  f[':answer-field/choices']=sorted([{k:v for k,v in a.items()if k!=':answer/id'}for a in f[':answer-field/choices']],key=stable)
 content=uid([VERSION,clean])
 q[':question/id']=content
 for f in q.get(':question/answer-fields',[]):
  oldcorrect=f.get(':answer-field/correct');oldid=oldcorrect[1] if isinstance(oldcorrect,list)else oldcorrect.get(':answer/id')if isinstance(oldcorrect,dict)else None
  f[':answer-field/id']=uid([content,f[':answer-field/key']])
  for a in f[':answer-field/choices']:
   old=a.get(':answer/id');a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
   if old==oldid:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  random.Random(uid([seed,content])).shuffle(f[':answer-field/choices'])
 f,der,ans=math(p,t)
 semantic=[FAMILY[t],sp.srepr(der)] if FAMILY[t]in ['direct','power_sum','linear_sum'] else [FAMILY[t],sp.srepr(f),sp.srepr(sp.Integer(p['b'])-sp.log(p['k'])if FAMILY[t]=='slope'else sp.Rational(p.get('t',1)-p['b'],p['a']))]
 if FAMILY[t]=='slope':semantic=[FAMILY[t],p['a'],p['c'],p['k']]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'difficulty':level,'template':t,'profile':profile,'bank_origin':'observed-expression-evidence'if (profile.startswith('raw:') or profile=='observed-bank')else'authored-method','parameters':p,'seed':seed,'content_identity':content,'mathematical_fingerprint':hashlib.sha256(stable(semantic).encode()).hexdigest(),'source':{'database':'math','basis':3947,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'evidence_only':profile.startswith('raw:'),'eligible_for_learning':not profile.startswith('raw:'),'authored_level':t=='q-11816','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def replay_source(template,seed=0):
 if template=='e-727':
  return identify(simplify_record(CANONICAL),'easy',template,dict(a=5,b=4,c=1,d=0),'raw:e-727',seed)
 if template not in CASE:raise ValueError('source replay template')
 case=CASE[template]
 q=simplify_record(render_mask(MASKS[template],slots(template,case['parameters'])))
 return identify(q,case['level'],template,case['parameters'],'raw:'+template,seed)

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,scalar_coefficients=None,outer_coefficients=None):
 if level not in ['easy','moderate']:raise ValueError('unsupported difficulty: '+level)
 if profile not in [None,'completed','authored-method','observed-bank']:raise ValueError('unknown profile')
 if field_type is not None:raise ValueError('field type is fixed by the source family')
 if template and (template not in LEVEL or LEVEL[template]!=level):raise ValueError('template/difficulty mismatch')
 rng=random.Random(seed);t=template or rng.choice([t for t,l in LEVEL.items() if l==level])
 bank_coefficients=None
 if scalar_coefficients is not None:
  if t not in SCALAR_RADIO or len(scalar_coefficients)!=5 or len(set(scalar_coefficients))!=5 or any(type(v)!=int or v not in COEFFICIENTS for v in scalar_coefficients):
   raise ValueError('five distinct eligible scalar coefficients required for scalar radio')
  bank_coefficients=list(scalar_coefficients)
 elif t in SCALAR_RADIO:
  if parameters is None:bank_coefficients=rng.sample(COEFFICIENTS,5)
  else:
   a=parameters['a'];bank_coefficients=[a]+rng.sample([v for v in COEFFICIENTS if v!=a],4)
 outer_bank=None
 if outer_coefficients is not None:
  if t!='q-48658' or len(outer_coefficients)!=5 or len(set(outer_coefficients))!=5 or any(type(v)!=int or v not in OUTER_COEFFICIENTS for v in outer_coefficients):
   raise ValueError('five distinct eligible outer coefficients required for slope radio')
  outer_bank=list(outer_coefficients)
 elif t=='q-48658':
  if parameters is None:outer_bank=rng.sample(OUTER_COEFFICIENTS,5)
  else:
   c=parameters['c'];outer_bank=[c]+rng.sample([v for v in OUTER_COEFFICIENTS if v!=c],4)
 chosen_outer=rng.choice(outer_bank) if outer_bank is not None and parameters is None else None
 # Choose the answer-bearing coefficient from the whole bank before other values.
 chosen_slope=rng.choice(bank_coefficients) if bank_coefficients is not None and parameters is None else None
 for attempt in range(1000):
  p=copy.deepcopy(parameters) if parameters is not None else sampled(t,rng)
  if chosen_slope is not None:p['a']=chosen_slope
  if chosen_outer is not None:p['c']=chosen_outer
  if outer_bank is not None and p['c'] not in outer_bank:raise ValueError('outer coefficient must belong to bank')
  if bank_coefficients is not None and p['a'] not in bank_coefficients:raise ValueError('inner slope must belong to scalar bank')
  try:
   guard(t,p)
   q=simplify_record(render_mask(MASKS[t],slots(t,p)))
   if t=='q-11817':
    q[':question/problem']=render_mask(SOURCE[t][':question/problem'].replace('2x+5','@@exponent@@'),slots(t,p))
    q[':question/worked-solution']=render_mask(MASKS[t][':question/worked-solution'],slots(t,p))
   if t=='q-48657':q=tangent_question(p)
   q.pop(':question/math-academy-id',None)
   q[':question/difficulty']=':question.difficulty/'+level
   if ':question/worked-solution' not in q:q[':question/worked-solution']=common_solution(p,t)
   kind='blank' if t in ['q-48003','q-107420','q-340496','q-340497'] else 'radio'
   f,der,ans=math(p,t)
   vals=authored_bank(t,p,bank_coefficients,outer_bank) if kind=='radio' else [tex(ans)]
   # Preserve both accepted strings, including their source ordering styles.
   if t=='q-340496':
    E=term(p['a'],linear(p['a'],p['b']))
    vals=[E+plus(p['r']),str(p['r'])+('+' if p['a']>0 else '')+E]
   q[':question/problem']=q[':question/problem'].replace('{{field-1}}','').rstrip()
   if kind=='blank':q[':question/problem']+='\n{{field-1}}'
   ff={':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':[{':answer/id':'answer-'+str(i),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(vals)],':answer-field/correct':[':answer/id','answer-0']}
   q[':question/answer-fields']=[ff]
   break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('no eligible complete bank')
 profile='authored-slope-bank' if t=='q-48658' else 'authored-scalar-bank' if t in SCALAR_RADIO else 'authored-method'
 result=identify(q,level,t,p,profile,seed)
 if bank_coefficients is not None:result['generation']['scalar_coefficients']=bank_coefficients
 if outer_bank is not None:result['generation']['outer_coefficients']=outer_bank
 result['generation']['rejections']=attempt
 return result

# Easy: observed one linear-exponent chain product, including scale/vertical translation.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: fixed polynomial sum OR shifted-log slope OR reciprocal-point tangent workload.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard is explicitly unsupported without source difficulty evidence.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_batch(level,count,seed=0,**kwargs):
 if count<1:raise ValueError('count must be positive')
 records=[];seen=set();duplicates=0
 for offset in range(max(100,count*100)):
  record=generate(level,seed+offset,**kwargs);identity=record['question'][':question/id']
  if identity in seen:duplicates+=1;continue
  seen.add(identity);record['generation']['batch_duplicate_rejections']=duplicates;records.append(record)
  if len(records)==count:return records
 raise ValueError('requested count exhausts the sampled family; reduce count')

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'+ '\n'.join('- $'+a[':answer/value']+'$'for a in f[':answer-field/choices'])+'\n'
 if ':question/worked-solution'in q:s+='\n'+q[':question/worked-solution']+'\n'
 return s
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('--count must be positive')
 levels=[args.difficulty]
 rs=generate_batch(args.difficulty,args.count,args.seed,template=args.template,profile=args.profile)
 print(json.dumps(rs,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n'.join(markdown(r)for r in rs))
