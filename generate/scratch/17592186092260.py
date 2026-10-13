#!/usr/bin/env python3
"""Linear-exponent e differentiation, basis 1356. No DB writes or plots.

Public raw:<source-id> profiles render parameterized masks and retain omissions.
Completed profiles preserve source family solutions, normalizing ln U+2061 only.
Hard is an explicitly authored shifted/translated tangent calculation, exactly
one chain-rule product, two point evaluations, one point-slope expansion.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,pathlib,random,sys,uuid
import sympy as sp
KP_ID=17592186092260
KP_UUID='a83f86ab-a008-5487-b118-f1495a0fe4d6'
TITLE='Differentiating an Exponential Function with a Linear Exponent'
VERSION='linear-e-1'
DIR=pathlib.Path(__file__).with_suffix('')
MASKS=json.loads((DIR/'masks.json').read_text())
CASES=json.loads((DIR/'source-cases.json').read_text())
CASE={c['template']:c for c in CASES}
X,Y,U=sp.symbols('x y u',real=True)
FAMILY={'q-11816':'direct','q-11817':'direct','q-48003':'direct','q-48007':'direct','q-107420':'power_sum','q-340496':'linear_sum','q-340497':'slope','q-48658':'slope','q-48657':'tangent','shifted_tangent':'tangent'}
LEVEL={c['template']:c['level'] for c in CASES}|{'shifted_tangent':'hard'}

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
 if t=='q-11817':ex=coeff(a)+'x'+(' + ' if b>=0 else ' - ')+str(abs(b))
 s={'exponent':ex,'a_group':'{'+str(a)+'}','ax_e':coeff(a)+'xe','a_e':coeff(a)+'e','ce':coeff(c)+'{e}', 'cae':coeff(ca)+'{e}', 'ae':coeff(a)+'{e}', 'negcae':coeff(-ca)+'{e}', 'a_factor':'('+str(a)+')' if a<0 else str(a),'=a.':'='+str(a)+'.','}=a.':'}='+str(a)+'.','plusd':plus(d),'dot_a':r'\cdot '+('('+str(a)+')' if a<0 else str(a)), 'double_shift':linear(a,2*b),'recipcoef':tex(sp.Rational(-c,a))}
 if t=='q-107420':
  n=p['n'];s.update(poly='{x}^{'+str(n)+'}',polyprime=str(n)+'{x}^{'+str(n-1)+'}',factored=str(n)+'({x}^{'+str(n-1)+'}+{e}',powerprev='{x}^{'+str(n-1)+'}')
 if t=='q-340496':
  r=p['r'];s.update(poly=coeff(r)+'x',sumrow=str(r)+('+' if a>=0 else '-')+coeff(abs(a))+'{e}',plusr_period=plus(r)+'.',plusr=plus(r))
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
  point=(1-b)/a;ans=sp.simplify(der.subs(X,point)*(X-point)+f.subs(X,point))
 else:ans=der
 return f,der,ans

def common_solution(p,t):
 a,b,c,d=[p[k]for k in ['a','b','c','d']];name='y' if FAMILY[t]=='tangent' else 'f';e=linear(a,b)
 outer=term(c,'u')+(plus(d)if d else '')
 factor='('+str(a)+')' if a<0 else str(a)
 solution='First, we express $'+name+'$ as the composite function\n\n$$\n'+name+'='+outer+r',\,u='+e+'.\n$$\n\nDifferentiating gives\n\n$$\n'+r'\frac{\text{d}'+name+r'}{\text{d}u}='+term(c,'u')+r',\,\frac{\text{d}u}{\text{d}x}='+str(a)+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'+r'\begin{aligned}\frac{\text{d}'+name+r'}{\text{d}x} & =\frac{\text{d}'+name+r'}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & ='+term(c,'u')+r'\cdot '+factor+r' \\  & ='+term(c*a,'u')+r' \\  & ='+term(c*a,e)+r'.\end{aligned}'+'\n$$'
 return solution

def hard_question(p):
 a,b,c,d=[p[k] for k in ['a','b','c','d']];f,der,ans=math(p,'shifted_tangent');z=sp.Rational(1-b,a);m=c*a*sp.E;v=c*sp.E+d;e=linear(a,b)
 prompt='Find the equation of the tangent to the curve $y='+term(c,e)+plus(d)+'$ at the point where $x='+tex(z)+'.$'
 s=common_solution(p,'shifted_tangent')
 s+='\n\nNow, to find the slope of the tangent to the curve at $x='+tex(z)+'$, we have to evaluate $'+r'\frac{\text{d}y}{\text{d}x}'+'$ at that point as follows:\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x}{|}_{x='+tex(z)+'} & ='+term(c*a,e)+r'{|}_{x='+tex(z)+r'} \\ & ='+term(c*a,'('+str(a)+')('+tex(z)+')'+plus(b))+r' \\ & ='+tex(m)+r'.\end{aligned}'+'\n$$'
 s+='\n\nAlso, the $y$-value of the point on the curve where $x=x_1='+tex(z)+'$ is\n\n$$\n'+r'\begin{aligned}y_1 & =('+term(c,e)+plus(d)+r'){|}_{x='+tex(z)+r'} \\ & ='+term(c,'('+str(a)+')('+tex(z)+')'+plus(b))+plus(d)+r' \\ & ='+tex(v)+r'.\end{aligned}'+'\n$$'
 # Signed complete factors prevent a bare -- or numeric concatenation.
 s+='\n\nFinally, we find the equation of the tangent at that point:\n\n$$\n'+r'\begin{aligned}y-y_1 & =m(x-x_1) \\ y-('+tex(v)+') & =('+tex(m)+')(x-('+tex(z)+r')) \\ y-('+tex(v)+') & ='+tex(m*X)+'-('+tex(m*z)+r') \\ y & ='+tex(ans)+r'.\end{aligned}'+'\n$$'
 return {':question/problem':prompt,':question/worked-solution':s}

def guard(t,p,raw=False):
 required={'a','b','c','d'}|({'n'}if t=='q-107420' else {'r'}if t=='q-340496' else {'k'}if FAMILY[t]=='slope' else set())
 if set(p)!=required or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required: '+str(required))
 a,b,c,d=[p[k]for k in ['a','b','c','d']]
 if raw and t=='q-48007'and b==0:raise ValueError('whole observed bank collision: doubled zero shift')
 if raw and t=='q-48658'and (b in [1,p['k']] or b==-c*p['k']):raise ValueError('whole observed scalar bank collision')
 if not (a and c and 1<=abs(a)<=6 and abs(c)<=8 and abs(b)<=8 and abs(d)<=8):raise ValueError('coefficient bounds')
 if t=='shifted_tangent':
  if not (2<=abs(a)<=6 and 2<=abs(c)<=6 and b not in (0,1) and 1<=abs(b)<=6 and 1<=abs(d)<=6):raise ValueError('hard requires nonunit factors and nonzero shift/translation; nonzero tangent point')
 elif t=='q-48657':
  if not (2<=a<=6 and 2<=c<=8 and b==d==0 and a!=c):raise ValueError('reciprocal-point tangent profile')
 elif FAMILY[t]=='slope':
  if not(a==-1 and -8<=c<=-2 and d==0 and 2<=p['k']<=6):raise ValueError('shifted-log slope bounds')
 elif t=='q-107420':
  if not(3<=p['n']<=5 and a==-p['n'] and c==-1 and d==0):raise ValueError('power sum: one power-rule term, factored shared derivative scale')
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
 if t=='q-107420':p.update(n=rng.randint(3,5),c=-1);p['a']=-p['n']
 if t=='q-340496':p['r']=signed(2,8)
 if FAMILY[t]=='slope':p.update(a=-1,c=-rng.randint(2,8),k=rng.randint(2,6))
 if t=='q-48657':p.update(a=rng.randint(2,6),b=0,c=rng.randint(2,8))
 if t=='shifted_tangent':p.update(a=signed(2,6),c=signed(2,6),b=rng.choice([-6,-5,-4,-3,-2,-1,2,3,4,5,6]),d=signed(1,6))
 return p

def authored_bank(t,p):
 f,der,ans=math(p,t);a,b,c,d=[p[k]for k in ['a','b','c','d']];E=sp.exp(a*X+b)
 if FAMILY[t]=='direct':
  if t=='q-48007':bank=[ans,c*E,c*E/a,-c*a*E,c*a*E+d]
  elif t=='q-11816':bank=[ans,E/a,X*E,a*X*E,E]
  elif t=='q-48003':bank=[ans,c*E,c*a*X*E,c*a*sp.exp(a*X),c*a*sp.exp(X+b)]
  else:bank=[ans,E/a,a*X*E,E,(a*X+b)*E]
 elif FAMILY[t]=='power_sum':
  n=p['n'];bank=[ans,n*X**(n-1)-E,n*X**(n-1)+a*E,X**n-a*E,-a*E]
 elif FAMILY[t]=='linear_sum':
  r=p['r'];bank=[ans,r+E,r+E/a,r-a*E,a*E]
 elif FAMILY[t]=='slope':
  k=p['k'];bank=[ans,c*k,-k,-c*sp.exp(b),-c*sp.exp(k)]
 elif t=='q-48657':bank=[ans,c*sp.E*X,sp.E*X,a*sp.E*X,c*a*sp.E*X*sp.log(c)]
 else:
  z=sp.Rational(1-b,a);v=c*sp.E+d;m=c*a*sp.E
  bank=[ans,m*X+v,c*sp.E*(X-z)+v,-m*(X-z)+v,m*(X-z)+c*sp.E]
 if len(bank)!=5 or any(sp.expand(bank[i]-bank[j])==0 for i in range(5)for j in range(i)):
  raise ValueError('whole-bank equivalence collision')
 return ['y='+tex(v) if FAMILY[t]=='tangent' else tex(v)for v in bank]

def stable(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,stable(v)))
def identify(q,level,t,p,profile,seed):
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
  random.Random(seed).shuffle(f[':answer-field/choices'])
 f,der,ans=math(p,t)
 semantic=[FAMILY[t],sp.srepr(der)] if FAMILY[t]in ['direct','power_sum','linear_sum'] else [FAMILY[t],sp.srepr(f),sp.srepr(sp.Integer(p['b'])-sp.log(p['k'])if FAMILY[t]=='slope'else sp.Rational(1-p['b'],p['a']))]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'difficulty':level,'template':t,'profile':profile,'bank_origin':'observed-expression-evidence'if profile.startswith('raw:')else'authored-method','parameters':p,'seed':seed,'content_identity':content,'mathematical_fingerprint':hashlib.sha256(stable(semantic).encode()).hexdigest(),'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'evidence_only':profile.startswith('raw:'),'eligible_for_learning':not profile.startswith('raw:'),'authored_level':t in ['q-11816','q-11817','shifted_tangent'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('difficulty')
 if profile and profile.startswith('raw:'):
  implied=profile[4:]
  if template and template!=implied:raise ValueError('profile/template mismatch')
  template=implied
 if template and (template not in LEVEL or LEVEL[template]!=level):raise ValueError('template/difficulty mismatch')
 rng=random.Random(seed)
 candidates=[t for t,l in LEVEL.items()if l==level]
 t=template or rng.choice(candidates);raw=bool(profile and profile.startswith('raw:'))
 if profile not in [None,'completed','authored-method','raw:'+t]:raise ValueError('unknown profile')
 if raw and t not in MASKS:raise ValueError('no raw source')
 if field_type not in [None,'radio','blank']:raise ValueError('field type')
 if raw and field_type:raise ValueError('raw fields are fixed and preserve omissions')
 for attempt in range(1000):
  p=copy.deepcopy(parameters) if parameters is not None else sampled(t,rng)
  try:
   guard(t,p,raw)
   q=simplify_record(render_mask(MASKS[t],slots(t,p)))if t in MASKS else hard_question(p)
   if raw:break
   q.pop(':question/math-academy-id',None)
   q[':question/difficulty']=':question.difficulty/'+level
   if ':question/worked-solution'not in q:q[':question/worked-solution']=common_solution(p,t)
   q={k:(v.replace('ln⁡',r'\ln')if isinstance(v,str)else v)for k,v in q.items()}
   # Retain observed blank fragment layouts. Direct missing-field signed scale uses a blank.
   kind=field_type or ('blank'if t in ['q-48003','q-107420','q-340496','q-340497']else 'radio')
   f,der,ans=math(p,t)
   if kind=='blank' and FAMILY[t]=='tangent':raise ValueError('complete tangent equations use supported radio layout')
   if kind=='radio':vals=authored_bank(t,p)
   else:vals=[tex(ans)]
   q[':question/problem']=q[':question/problem'].replace('{{field-1}}','')
   if kind=='blank':q[':question/problem']=q[':question/problem'].rstrip()+'\n{{field-1}}'
   elif t in ['q-340496','q-340497']:q[':question/problem']=q[':question/problem'].split('\n\n')[0]
   ff={':answer-field/key':'field-1'if kind=='blank'else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':[{':answer/id':'answer-'+str(i),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(vals)],':answer-field/correct':[':answer/id','answer-0']}
   q[':question/answer-fields']=[ff]
   break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('no eligible complete bank')
 return identify(q,level,t,p,profile or 'authored-method',seed)

# Easy: observed one linear-exponent chain product, including scale/vertical translation.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: fixed polynomial sum OR shifted-log slope OR reciprocal-point tangent workload.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard (authored): same tangent method with nonzero exponent shift and vertical translation.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'+ '\n'.join('- $'+a[':answer/value']+'$'for a in f[':answer-field/choices'])+'\n'
 if ':question/worked-solution'in q:s+='\n'+q[':question/worked-solution']+'\n'
 return s
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty]
 rs=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in levels for i in range(args.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n'.join(markdown(r)for r in rs))
