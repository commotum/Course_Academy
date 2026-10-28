"""Algebraic standard-form conversion, with preserved source-replay profiles.

Easy: observed families, bounded coefficients, and their operative row masks.
Moderate (authored): collect both sides, divide a nonconstant coefficient;
    both rational coefficients remain nontrivial. No expansion/cancellation.
Hard: observed square expansion, cancellation, and coefficient collection.
Raw source profiles are public parameterized evidence, including legacy fields.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_prose, checked_math_content
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text()); REC=RAW['record']
KP=17592186087866; KP_UUID=REC[':knowledge-point/id']; TITLE=REC[':knowledge-point/title']
VERSION='standard-form-2.2.0'; LEVELS=('easy','moderate','hard')
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,y,D=s.symbols('x y D',real=True)
FAMILIES={'easy':['q-16400','q-8359','q-103349','q-103354','q-16396','q-79697','q-79699','q-8360'],'moderate':['rational-collect'],'hard':['q-16401']}
ORIGINAL={'q-16400':{'a':2,'b':3,'c':1,'h':4},'q-8359':{'k':1},'q-103349':{'n':1},'q-103354':{'n':1},'q-16396':{'k':1},'q-79697':{'k':1},'q-79699':{'k':5},'q-8360':{'k':2},'q-16401':{'a':1,'b':1,'n':1},'rational-collect':{'a':2,'b':3,'c':1,'d':2,'h':1}}
DOMAINS={'q-8359':'x != 0','q-79697':'x != 0','q-16396':'y != 0','q-79699':'y != 0','q-103354':'cos(n*x) != 0','q-8360':'sin(x) != 0'}
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()
def uid(obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),obj))
def eq(l,r):return (s.sympify(l),s.sympify(r))
def uneval_add(*a):return s.Add(*a,evaluate=False)
def uneval_mul(*a):return s.Mul(*a,evaluate=False)
def tex(e):
 return s.latex(e,order='lex').replace('D',r'\frac{\text{d}y}{\text{d}x}').replace(r'\left', '').replace(r'\right','')
def equation(e):return tex(e[0])+'='+tex(e[1])
def normalized(e):
 residual=s.expand(e[0]-e[1]);a=residual.coeff(D)
 if a==0:raise ValueError('No derivative coefficient')
 r=s.cancel(s.expand(residual/a))
 if s.diff(r,y,2)==0 and s.diff(r,D,2)==0:
  return D+canonical_expression(s.diff(r,y))*y+canonical_expression(r.subs({D:0,y:0}))
 return s.simplify(r)
def data(t,p):
 """Each branch preserves source operations, full bank and solution sequence."""
 if set(p)!=set(ORIGINAL[t]) or any(type(v)!=int for v in p.values()):raise ValueError('Integer parameter shape')
 if t=='rational-collect':
  a,b,c,d,h=(p[z] for z in ('a','b','c','d','h'))
  for value in (a,b,c,d,h):bounds(value,1,8)
  if a<2 or h==0:raise ValueError('Moderate requires a nonunit coefficient and nonzero collected y term')
  A=a*x; B=b*x; C=c+h*x
  P=(B-d)/A;Q=C/A
  stages=[eq(A*D+B*y-h*x,c+d*y),eq(A*D+uneval_mul(B-d,y),C),eq(D+uneval_mul((B-d)/A,y),C/A)]
  bank=[stages[-1],eq(D+uneval_mul((B+d)/A,y),C/A),eq(D+uneval_mul((B-d)/A,y), (c-h*x)/A),eq(D+uneval_mul((B-d)/A,y),C),eq(D+uneval_mul(B-d,y),C/A)];correct=0
 elif t=='q-16400':
  a,b,c,h=(p[z] for z in ('a','b','c','h'))
  if not (2<=a<=5 and 1<=b<=5 and 1<=c<=5 and 1<=h<=8):raise ValueError('Rearrangement bounds')
  P=h*s.sin(x)/a;Q=(c+b*s.cos(x))/a
  stages=[eq(a*D-b*s.cos(x),c-h*y*s.sin(x)),eq(a*D+h*y*s.sin(x),c+b*s.cos(x)),eq(D+P*y,Q)]
  bank=[eq(D+h*s.sin(x)*y,c+b*s.cos(x)),eq(D+h*s.cos(x)*y,c+b*s.sin(x)),stages[-1],eq(D+Q,P*y),eq(D+P*y,c+b*s.cos(x)/a)];correct=2
 elif t=='q-8359':
  k=p['k'];bounds(k,1,8);P=k/x;Q=s.Integer(2)
  stages=[eq(D,(2*x-k*y)/x),eq(D,uneval_add(2*x/x,-k*y/x)),eq(D+k*y/x,2*x/x),eq(D+P*y,Q)]
  bank=[eq(k*y,2*x-x*D),eq(D+P*y-Q,0),eq(x*D+k*y,2*x),eq(D,-P*y+Q),stages[-1]];correct=4
 elif t=='q-103349':
  n=p['n'];bounds(n,1,8);P=2*s.exp(-n*x);Q=x*s.exp(-2*n*x)
  stages=[eq(s.exp(2*n*x)*D+2*s.exp(n*x)*y-x,0),eq(s.exp(2*n*x)*D+2*s.exp(n*x)*y,x),eq(D+P*y,Q)]
  bank=[eq(D+s.exp(-2*n*x)*y-x*s.exp(-n*x),0),stages[-1],eq(D+P*y-Q,0),eq(D-y,Q),eq(D+2*y,Q)];correct=1
 elif t=='q-103354':
  n=p['n'];bounds(n,1,8);C=s.cos(n*x);S=s.sin(n*x);P=-s.tan(n*x);Q=-2*S
  stages=[eq(C*D+s.sin(2*n*x)-S*y,0),eq(C*D-S*y,-s.sin(2*n*x)),eq(D-S*y/C,-s.sin(2*n*x)/C),eq(D-s.tan(n*x)*y,uneval_mul(-2,S,C,1/C)),eq(D+P*y,Q)]
  bank=[eq(D+2*S,s.tan(n*x)*y),eq(D-s.cot(n*x)*y,2*C),eq(D+s.sec(n*x)*y,-2*s.sin(2*n*x)),eq(D+s.sin(2*n*x),s.sec(n*x)*y),stages[-1]];correct=4
 elif t=='q-16396':
  k=p['k'];bounds(k,1,8);P=-k*x;Q=-x**2
  stages=[eq(y*D+x**2*y,k*y**2*x),eq(y*D+x**2*y-k*y**2*x,0),eq(uneval_mul(y,D+x**2-k*y*x),0),eq(D+x**2-k*y*x,0),eq(D+P*y,Q),eq(D+P*y,Q)]
  # Opaque source patterns: exact expressions, no inferred error psychology.
  bank=[eq(D+(k-x**2)/(k+x**2)*y,k),eq(D-k*y,-2*k*x),stages[-1],eq(D,-x**2),eq(D+x**2*y,k*x)];correct=2
 elif t=='q-79697':
  k=p['k'];bounds(k,1,8);P=-k*x;Q=x**2
  stages=[eq(D/x**2,(x+k*y)/x),eq(D,uneval_mul(x**2,(x+k*y)/x)),eq(D,uneval_mul(x,x+k*y)),eq(D,x**2+k*x*y),eq(D+P*y,Q),eq(D+P*y,Q)]
  bank=[eq(D-k*x*y,2*x),eq(D-(1+k*x)*y,0),stages[-1],eq(D-k*y,-x**2),eq(D+k*x*y,1/x)];correct=2
 elif t=='q-79699':
  k=p['k'];bounds(k,2,8);P=-k*s.exp(x);Q=-s.exp(x)
  stages=[eq(k*y**2-y*s.exp(-x)*D,y),eq(-y*s.exp(-x)*D+k*y**2-y,0),eq(uneval_mul(-y,s.exp(-x)*D-k*y+1),0),eq(s.exp(-x)*D-k*y+1,0),eq(uneval_mul(s.exp(x),s.exp(-x)*D-k*y+1),0),eq(D-k*y*s.exp(x)+s.exp(x),0),eq(D+P*y,Q),eq(D+P*y,Q)]
  bank=[stages[-1],eq(D+k*y,-s.exp(x)),eq(D-k*s.exp(x)*y,x),eq(D+k*s.exp(-x)*y,s.exp(-x)),eq(D-k*x*y,-s.exp(-x))];correct=0
 elif t=='q-8360':
  k=p['k'];bounds(k,1,8);P=k*s.cot(x);Q=-s.sin(2*x)
  stages=[eq(D+k*y*s.cot(x)+s.sin(2*x),0),eq(D+k*y*s.cot(x),Q),eq(D+P*y,Q)]
  bank=[eq(D+s.sin(2*x),-k*y*s.cot(x)),eq(D,-k*y*s.cot(x)-s.sin(2*x)),eq(k*y*s.cot(x),-D-s.sin(2*x)),eq(y,-D/(k*s.cot(x))-s.sin(2*x)/(k*s.cot(x))),stages[-1]];correct=4
 else:
  # Hard: expansion and exact cancellation, without another ODE skill.
  a,b,n=(p[z] for z in ('a','b','n'))
  bounds(a,1,6);bounds(abs(b),1,4);bounds(n,1,6);C=s.cos(n*x);P=2*a*b*C;Q=s.Integer(a*a)
  quadratic=b*b*y*y*C*C
  stages=[eq(D+quadratic,(a-b*y*C)**2),eq(D+quadratic,uneval_add(a*a,quadratic,-2*a*b*y*C)),eq(D,a*a-2*a*b*y*C),eq(D+P*y,Q)]
  bank=[stages[-1],eq(D+b*y*C,a*a-a*b*C),eq(D+b*b*y*C*C,(a-b*C)**2),eq(D,a*a),eq(D+4*a*b*y*C,a*a)];correct=0
 return {'P':P,'Q':Q,'stages':stages,'bank':bank,'correct':correct}
def bounds(k,lo,hi):
 if not lo<=k<=hi:raise ValueError('Parameter outside frozen bounds')
def sample(t,rng):
 if t=='rational-collect':return dict(a=rng.randint(2,8),b=rng.randint(1,8),c=rng.randint(1,8),d=rng.randint(1,8),h=rng.randint(1,8))
 if t=='q-16400':return dict(a=rng.randint(2,5),b=rng.randint(1,5),c=rng.randint(1,5),h=rng.randint(1,8))
 if t=='q-16401':return dict(a=rng.randint(1,6),b=rng.randint(1,4),n=rng.randint(1,6))
 return {z:rng.randint(2 if t=='q-79699' else 1,8 if z=='n' else 8) for z in ORIGINAL[t]}
def stage_rows(t,p,m):
 """Operative unevaluated masks: division, cancellation and expansion stay visible."""
 d=tex(D);X=r'{x}^{2}'
 def T(e):return tex(e)
 def fraction(a,b):return r'\frac{'+a+'}{'+b+'}'
 def annotated():return d+r'+\underbrace{('+T(m['P'])+r')}_{P(x)}y=\underbrace{'+T(m['Q'])+r'}_{Q(x)}'
 if t=='q-8359':
  k=p['k'];ky=T(k*y);num='2x-'+ky
  rows=[d+'='+fraction(num,'x'),d+'='+fraction('2x','x')+'-'+fraction(ky,'x'),d+'+'+fraction(ky,'x')+'='+fraction('2x','x'),annotated()]
 elif t=='q-103354':
  n=p['n'];C=T(s.cos(n*x));S=T(s.sin(n*x));S2=T(s.sin(2*n*x));tan=T(s.tan(n*x))
  rows=[C+d+'+'+S2+'-'+S+'y=0',C+d+'-'+S+'y=-'+S2,d+'-('+fraction(S,C)+')y=-'+fraction(S2,C),d+'-('+tan+')y=-'+fraction('2'+S+C,C),annotated()]
 elif t=='q-79697':
  k=p['k'];ky=T(k*y);kx=T(k*x*y);num='x+'+ky
  rows=['('+fraction('1',X)+')'+d+'='+fraction(num,'x'),d+'='+X+'('+fraction(num,'x')+')',d+'=x('+num+')',d+'='+X+'+'+kx,annotated(),equation(m['stages'][-1])]
 elif t=='q-16396':
  k=p['k'];rhs=T(k*y**2*x);inside=d+'+'+X+'-'+T(k*x*y)
  rows=['y'+d+'+'+X+'y='+rhs,'y'+d+'+'+X+'y-'+rhs+'=0','y('+inside+')=0',inside+'=0',annotated(),equation(m['stages'][-1])]
 elif t=='q-79699':
  k=p['k'];E=T(s.exp(x));F=T(s.exp(-x));inside=F+d+'-'+T(k*y)+'+1'
  rows=[T(k*y**2)+'-y'+F+d+'=y','-y'+F+d+'+'+T(k*y**2)+'-y=0','-y('+inside+')=0',inside+'=0',E+'('+inside+')=0',d+'-'+T(k*y*s.exp(x))+'+'+E+'=0',annotated(),equation(m['stages'][-1])]
 elif t=='q-16401':
  a,b,n=(p[z] for z in ('a','b','n'));C=T(s.cos(n*x));quad=T(b*b)+r'{y}^{2}('+C+r')^{2}'
  # Numeric factors use explicit parentheses, never concatenated adjacent digits.
  inner=str(a)+('-(' if b>0 else '+(')+str(abs(b))+')y'+C
  rows=[d+'+'+quad+'=('+inner+r')^{2}',d+'+'+quad+'='+str(a*a)+'+'+quad+('-'+T(2*a*b*y*s.cos(n*x)) if b>0 else '+'+T(-2*a*b*y*s.cos(n*x))),d+'='+str(a*a)+('-'+T(2*a*b*y*s.cos(n*x)) if b>0 else '+'+T(-2*a*b*y*s.cos(n*x))),annotated()]
 elif t=='rational-collect':
  a,b,c,d0,h=(p[z] for z in ('a','b','c','d','h'))
  rows=[T(a*x)+d+'+'+T(b*x*y)+'-'+T(h*x)+'='+str(c)+'+'+T(d0*y),T(a*x)+d+'+('+T(b*x)+'-'+str(d0)+')y='+str(c)+'+'+T(h*x),annotated()]
 else:
  rows=[equation(e) for e in m['stages']];rows[-1]=annotated()
 return rows
def raw_source(t,n):
 """Source masks parameterize every algebraic x component, protecting notation.

 n=1 is an ordinary slot value; no source-return branch exists. Source questions
 are never sampled as completed defaults. Missing refs stay missing in evidence.
 """
 bounds(n,1,8)
 if type(n)!=int:raise ValueError('Exact integer n required')
 q=copy.deepcopy(SOURCES[t])
 derivatives=[r'\frac{\text{d}y}{\text{d}x}',r'\frac{dy}{dx}']
 def transform(v):
  saved={}
  # Protect complete derivatives, formal operator names and TeX command words.
  for token in derivatives+[r'P(x)',r'Q(x)']:
   placeholder='§'+str(len(saved))+'§';saved[placeholder]=token;v=v.replace(token,placeholder)
  def argument(m):
   token=m.group(0);factor=int(m.group(2) or '1')*n
   replacement=token if n==1 else m.group(1)+'('+str(factor)+'x)'
   placeholder='§'+str(len(saved))+'§';saved[placeholder]=replacement;return placeholder
  v=re.sub(r'(\\operatorname\{(?:sin|cos|tan|cot|sec|csc)\}⁡|\\(?:sin|cos|tan|cot|sec|csc)\s*)(2?)x',argument,v)
  tokens={}
  def protect(m):
   key='¤'+str(len(tokens))+'¤';tokens[key]=m.group(0);return key
  v=re.sub(r'\\[A-Za-z]+',protect,v)
  v=v.replace('x','x' if n==1 else '('+str(n)+'x)')
  for key,val in tokens.items():v=v.replace(key,val)
  for key,val in saved.items():v=v.replace(key,val)
  return v
 def walk(o):
  if isinstance(o,dict):
   return {k:(transform(v) if k in (':question/problem',':question/worked-solution',':answer/value') else walk(v)) for k,v in o.items()}
  if isinstance(o,list):return [walk(v) for v in o]
  return o
 return walk(q)
def localize(q,level,seed,raw=False):
 """Convert Pull enums/correct refs into the established local record shape."""
 q=copy.deepcopy(q)
 # Normalize the producer's complete presentation before any content identity.
 # This includes optional prose that is absent in today's source banks.
 def normalize_node(node):
  if isinstance(node,list):
   return [normalize_node(value) for value in node]
  if not isinstance(node,dict):return node
  result={key:normalize_node(value) for key,value in node.items()}
  answer_type=result.get(':answer/type')
  if isinstance(answer_type,dict):answer_type=answer_type.get(':db/ident')
  for key,value in list(result.items()):
   if not isinstance(value,str):continue
   if key in (':question/problem',':question/worked-solution') or key.rsplit('/',1)[-1] in ('feedback','hint') or (key==':answer/value' and answer_type==':answer.type/text'):
    result[key]=validate_prose(normalize_prose(value))
   elif key==':answer/value' and answer_type==':answer.type/math':
    result[key]=normalize_tex(value)
  return result
 q=normalize_node(q)
 q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
 if isinstance(q.get(':question/difficulty'),dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 content={k:v for k,v in q.items() if k!=':question/id'}
 identity=uid(VERSION+':'+level+':'+digest(content));q[':question/id']=identity
 for fi,f in enumerate(q.get(':question/answer-fields',[])):
  f.pop(':db/id',None);f[':answer-field/id']=uid(identity+':field:'+str(fi))
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  old_correct=f.get(':answer-field/correct');old_id=old_correct.get(':answer/id') if isinstance(old_correct,dict) else None
  correct=None
  for a in f.get(':answer-field/choices',[]):
   old=a[':answer/id'];a.pop(':db/id',None)
   a[':answer/id']=uid(f[':answer-field/id']+':'+a[':answer/value'])
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
   if old==old_id:correct=a[':answer/id']
  if old_correct is not None:
   if correct is None:raise ValueError('Correct answer outside owned bank')
   f[':answer-field/correct']=[':answer/id',correct]
  random.Random(str(seed)+f[':answer-field/id']).shuffle(f.get(':answer-field/choices',[]))
 return q
def insert_key(values,value,rng):
 values.insert(rng.randrange(5),value);return values

def non_easy_assignment(t,p,rng,explicit,decision):
 """Choose a complete bank before incidental coefficients, with a uniform key.

 Hard: vary the signed cross-term coefficient by the signed coefficient in
 the square. Moderate: vary the two collected numerator coefficients.
 """
 allowed=list(range(-4,0))+list(range(1,5)) if t=='q-16401' else list(range(1,9))
 keys=('b_candidates',) if t=='q-16401' else ('b_candidates','d_candidates')
 def eligible(values):
  # Both polarity groups remain ambiguous. This condition is independent of
  # the keyed slot, so a bank's minority sign does not predict correctness.
  return t!='q-16401' or 2<=sum(v>0 for v in values)<=3
 if decision is not None:
  if not isinstance(decision,dict) or set(decision)!=set(keys)|{'correct_slot'}:raise ValueError('Complete non-easy decision catalog required')
  assignment=copy.deepcopy(decision);slot=assignment['correct_slot']
  if type(slot)!=int or not 0<=slot<5:raise ValueError('Invalid key slot')
  for key in keys:
   vals=assignment[key]
   if not isinstance(vals,list) or len(vals)!=5 or any(type(v)!=int for v in vals) or len(set(vals))!=5 or not set(vals)<=set(allowed):raise ValueError('Invalid coefficient candidates')
   if vals[slot]!=p[key[0]]:raise ValueError('Catalog key must match prompt coefficients')
   if not eligible(vals):raise ValueError('Hard catalog must contain at least two coefficients of each sign')
 elif explicit:
  while True:
   first=insert_key(rng.sample([v for v in allowed if v!=p['b']],4),p['b'],rng)
   if eligible(first):break
  slot=first.index(p['b']);assignment={'b_candidates':first,'correct_slot':slot}
  if t!='q-16401':
   second=rng.sample([v for v in allowed if v!=p['d']],4);second.insert(slot,p['d']);assignment['d_candidates']=second
 else:
  slot=rng.randrange(5)
  while True:
   assignment={key:rng.sample(allowed,5) for key in keys}
   if eligible(assignment['b_candidates']):break
  assignment['correct_slot']=slot
  for key in keys:p[key[0]]=assignment[key][slot]
 return p,assignment

def choose_assignment(t,p,rng,explicit,decision):
 """Select the answer-bearing coefficient pair before compatible parameters.

 Every candidate uses the same sign combination. In normal generation the
 keyed candidate is uniform among the five pairs, independently of rank.
 Explicit parameter calls retain their original magnitudes unless decision
 supplies the new forcing/linear coefficients.
 """
 upool=list(range(2 if t=='q-79699' else 1,9));vpool=list(range(1,6 if t=='q-16400' else 9))
 if explicit or decision is not None:
  d={'p_sign':1,'q_sign':1,'forcing':2 if t=='q-8359' else p['c'] if t=='q-16400' else 1,'linear':2 if t=='q-103349' else 1}
  catalog=None
  if decision is not None:
   if not isinstance(decision,dict) or set(decision)-set(d)-{'p_candidates','q_candidates','correct_slot'}:raise ValueError('Unknown decision role')
   catalog={k:decision[k] for k in ('p_candidates','q_candidates','correct_slot') if k in decision}
   d.update({k:v for k,v in decision.items() if k in d})
  if any(type(v)!=int for v in d.values()) or d['p_sign'] not in (-1,1) or d['q_sign'] not in (-1,1):raise ValueError('Exact signed integer roles required')
  bounds(d['forcing'],1,5 if t=='q-16400' else 8);bounds(d['linear'],1,8)
  u=p['h'] if t=='q-16400' else d['linear'] if t in ('q-103349','q-103354') else p['k'];v=d['forcing']
  if catalog:
   if set(catalog)!={'p_candidates','q_candidates','correct_slot'}:raise ValueError('Complete candidate catalog required')
   us,vs,slot=catalog['p_candidates'],catalog['q_candidates'],catalog['correct_slot']
   if not isinstance(us,list) or not isinstance(vs,list) or len(us)!=5 or len(vs)!=5 or any(type(z)!=int for z in us+vs) or len(set(us))!=5 or len(set(vs))!=5 or not set(us)<=set(upool) or not set(vs)<=set(vpool) or type(slot)!=int or not 0<=slot<5:raise ValueError('Invalid candidate catalog')
   if (us[slot],vs[slot])!=(u,v):raise ValueError('Catalog key must match prompt coefficients')
  else:
   us=insert_key(rng.sample([z for z in upool if z!=u],4),u,rng)
   vs=insert_key(rng.sample([z for z in vpool if z!=v],4),v,rng)
   slot=us.index(u);vi=vs.index(v);vs[slot],vs[vi]=vs[vi],vs[slot]
 else:
  us=rng.sample(upool,5);vs=rng.sample(vpool,5);slot=rng.randrange(5)
  d={'p_sign':rng.choice((-1,1)),'q_sign':rng.choice((-1,1)),'forcing':vs[slot],'linear':us[slot]}
  if t=='q-16400':p['h']=us[slot];p['c']=vs[slot]
  elif 'k' in p:p['k']=us[slot]
 d.update(p_candidates=us,q_candidates=vs,correct_slot=slot)
 return p,d

def assigned_data(t,p,d):
 """Signed coefficient extension, retaining the source's operative stages."""
 sp,sq=d['p_sign'],d['q_sign'];v=d['forcing']
 u=p['h'] if t=='q-16400' else d['linear'] if t in ('q-103349','q-103354') else p['k']
 U,V=sp*u,sq*v
 X=x**2;E=s.exp(x);F=s.exp(-x);C=s.cos(p.get('n',1)*x);S=s.sin(p.get('n',1)*x);S2=s.sin(2*p.get('n',1)*x)
 if t=='q-16400':
  a,b=p['a'],p['b'];P=U*s.sin(x)/a;Q=(V+sq*b*s.cos(x))/a
  stages=[eq(a*D-sq*b*s.cos(x),V-U*y*s.sin(x)),eq(a*D+U*y*s.sin(x),V+sq*b*s.cos(x)),eq(D+P*y,Q)]
 elif t=='q-8359':
  P=U/x;Q=s.Integer(V)
  stages=[eq(D,(V*x-U*y)/x),eq(D,uneval_add(uneval_mul(V*x,1/x),-U*y/x)),eq(D+U*y/x,uneval_mul(V*x,1/x)),eq(D+P*y,Q)]
 elif t=='q-103349':
  n=p['n'];P=U*s.exp(-n*x);Q=V*x*s.exp(-2*n*x)
  stages=[eq(s.exp(2*n*x)*D+U*s.exp(n*x)*y-V*x,0),eq(s.exp(2*n*x)*D+U*s.exp(n*x)*y,V*x),eq(D+P*y,Q)]
 elif t=='q-103354':
  n=p['n'];P=-U*s.tan(n*x);Q=-2*V*S
  stages=[eq(C*D+V*S2-U*S*y,0),eq(C*D-U*S*y,-V*S2),eq(D-U*S*y/C,-V*S2/C),eq(D-U*s.tan(n*x)*y,uneval_mul(-2*V,S,C,1/C)),eq(D+P*y,Q)]
 elif t=='q-16396':
  P=-U*x;Q=-V*X
  inside=D+V*X-U*y*x
  stages=[eq(y*D+V*X*y,U*y*y*x),eq(y*D+V*X*y-U*y*y*x,0),eq(uneval_mul(y,inside),0),eq(inside,0),eq(D+P*y,Q),eq(D+P*y,Q)]
 elif t=='q-79697':
  P=-U*x;Q=V*X;num=V*x+U*y
  stages=[eq(D/X,num/x),eq(D,uneval_mul(X,uneval_mul(num,1/x))),eq(D,uneval_mul(x,num)),eq(D,V*X+U*x*y),eq(D+P*y,Q),eq(D+P*y,Q)]
 elif t=='q-79699':
  P=-U*E;Q=-V*E;inside=F*D-U*y+V
  stages=[eq(U*y*y-y*F*D,V*y),eq(-y*F*D+U*y*y-V*y,0),eq(uneval_mul(-y,inside),0),eq(inside,0),eq(uneval_mul(E,inside),0),eq(D-U*y*E+V*E,0),eq(D+P*y,Q),eq(D+P*y,Q)]
 elif t=='q-8360':
  P=U*s.cot(x);Q=-V*s.sin(2*x)
  stages=[eq(D+P*y+V*s.sin(2*x),0),eq(D+P*y,Q),eq(D+P*y,Q)]
 else:raise ValueError('Unsupported easy family')
 m={'P':P,'Q':Q,'stages':stages}
 rows=[equation(e) for e in stages]
 # Preserve operative quotients instead of allowing eager CAS cancellation.
 dt=tex(D)
 frac=lambda a,b:r'\frac{'+tex(a)+'}{'+tex(b)+'}'
 if t=='q-8359':
  rows[0]=dt+'='+frac(V*x-U*y,x)
  rows[1]=dt+'='+frac(V*x,x)+('+' if -U>0 else '-')+frac(abs(U)*y,x)
  rows[2]=tex(D+U*y/x)+'='+frac(V*x,x)
 if t=='q-79697':
  num=V*x+U*y
  rows[0]=r'\left('+frac(1,X)+r'\right)'+dt+'='+frac(num,x)
  rows[1]=dt+'='+tex(X)+r'\left('+frac(num,x)+r'\right)'
 if t=='q-103354':
  # tex() simplifies arguments only, whereas numerator multiplication here
  # must remain visible for the double-angle cancellation step.
  rows[3]=tex(D-U*s.tan(p['n']*x)*y)+'='+r'\frac{'+tex(-2*V*S)+tex(C)+'}{'+tex(C)+'}'
 if t=='q-79699':
  rows[4]=tex(E)+r'\left('+tex(inside)+r'\right)=0'
 annotated=dt+r'+\underbrace{('+tex(P)+r')}_{P(x)}y=\underbrace{'+tex(Q)+r'}_{Q(x)}'
 rows[-2 if t in ('q-16396','q-79697','q-79699') else -1]=annotated
 m['rows']=rows
 return m

def coefficient_bank(t,p,m,d):
 """A complete bank from five independently assigned coefficient pairs.

 Distinct candidate coefficients make both equation sides distinct. All
 choices are standard form and use exactly the same function structures.
 """
 bank=[]
 for u,v in zip(d['p_candidates'],d['q_candidates']):
  other=dict(d,linear=u,forcing=v);pp=dict(p)
  if t=='q-16400':pp['h']=u;pp['c']=v
  elif 'k' in pp:pp['k']=u
  candidate=assigned_data(t,pp,other)
  bank.append(eq(D+candidate['P']*y,candidate['Q']))
 return bank

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,decision=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields are supported')
 rng=random.Random(seed);t=template or rng.choice(FAMILIES[level])
 if t not in FAMILIES[level]:raise ValueError('Template outside level')
 if profile in ('raw', 'observed-raw'):
  if t not in SOURCES:raise ValueError('No observed profile for authored template')
  p={'n':1} if parameters is None else parameters
  if set(p)!={'n'}:raise ValueError('Raw coordinate component slot is n only')
  q=localize(raw_source(t,p['n']),level,seed,True)
  result_meta=metadata(level,seed,t,p,'observed-raw',False)
  m=data(t,ORIGINAL[t]);raw_domain=str(s.cos(p['n']*x))+' != 0' if t=='q-103354' else str(s.sin(p['n']*x))+' != 0' if t=='q-8360' else DOMAINS.get(t,'real x,y')
  result_meta['domains']=raw_domain
  result_meta['mathematical_fingerprint']=semantic(m['P'].subs(x,p['n']*x),m['Q'].subs(x,p['n']*x),raw_domain,t)
  return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':result_meta}
 if profile not in (None,'method-derived',t):raise ValueError('Unknown complete profile')
 selected='method-derived' if profile is None else profile
 # Choose the complete coefficient bank and keyed role before incidental data.
 # Observed profiles remain unchanged for fidelity/replay.
 assignment = None
 for attempt in range(500):
  if selected=='method-derived' and level=='easy':
   # Assign eligible coefficient roles first, then fill only incidental slots.
   p=copy.deepcopy(parameters if parameters is not None else ORIGINAL[t])
   p,assignment=choose_assignment(t,p,rng,parameters is not None,decision)
   if parameters is None:
    incidental=sample(t,rng)
    for name in p:
     if name not in (('h','c') if t=='q-16400' else ('k',)):
      p[name]=incidental[name]
   data(t,p)  # Enforce the original parameter contract as well as new roles.
   m=assigned_data(t,p,assignment)
   m['bank']=coefficient_bank(t,p,m,assignment)
   m['correct']=assignment['correct_slot']
  elif selected=='method-derived':
   p=copy.deepcopy(parameters if parameters is not None else ORIGINAL[t])
   p,assignment=non_easy_assignment(t,p,rng,parameters is not None,decision)
   if parameters is None:
    incidental=sample(t,rng)
    for name in p:
     if name not in (('b',) if t=='q-16401' else ('b','d')):p[name]=incidental[name]
   m=data(t,p)
   if t=='q-16401':
    m['bank']=[eq(D+2*p['a']*b*s.cos(p['n']*x)*y,m['Q']) for b in assignment['b_candidates']]
   else:
    m['bank']=[eq(D+(b*x-d)/(p['a']*x)*y,m['Q']) for b,d in zip(assignment['b_candidates'],assignment['d_candidates'])]
   m['correct']=assignment['correct_slot']
  else:
   p=copy.deepcopy(parameters) if parameters is not None else sample(t,rng)
   m=data(t,p)
  valid=[standard(e) and s.simplify(s.trigsimp(normalized(e)-normalized(m['stages'][0])))==0 for e in m['bank']]
  collision=any(standard(a) and standard(b) and s.simplify(s.trigsimp(normalized(a)-normalized(b)))==0 for i,a in enumerate(m['bank']) for b in m['bank'][i+1:])
  if valid==[i==m['correct'] for i in range(5)] and not collision and len(set(equation(e) for e in m['bank']))==5:break
  if parameters is not None:raise ValueError('Whole bank collision or ambiguity')
 else:raise ValueError('No eligible complete bank instance')
 domain=str(s.cos(p['n']*x))+' != 0' if t=='q-103354' else 'x != 0' if t=='rational-collect' else DOMAINS.get(t,'real x,y')
 domain_tex={'q-8359':r'\,,\ x\ne 0','q-79697':r'\,,\ x\ne 0','rational-collect':r'\,,\ x\ne 0','q-16396':r'\,,\ y\ne 0','q-79699':r'\,,\ y\ne 0','q-103354':r'\,,\ '+tex(s.cos(p.get('n',1)*x))+r'\ne 0','q-8360':r'\,,\ \sin x\ne 0'}.get(t,'')
 rows_for_instance=m.get('rows') or stage_rows(t,p,m)
 prompt='Write the following first-order linear ODE in standard form.\n\n$$\n'+rows_for_instance[0]+r'\,.'+'\n$$'
 if domain_tex:prompt+='\n\nAssume $'+domain_tex.removeprefix(r'\,,\ ')+'$.'
 source=SOURCES.get(t,SOURCES['q-16400']);sol=source[':question/worked-solution'];prefix=sol.split(r'\begin{aligned}')[0]
 prefix=prefix.replace('$$\n\n$$\n\n','')
 # Align complete rows for authored banks: equality alignment can combine
 # the widest LHS and widest RHS from different rows and clip the result.
 # Source replay retains its captured equality alignment separately.
 rows=['&'+row for row in rows_for_instance] if selected=='method-derived' else [row.replace('=','&=',1) for row in rows_for_instance]
 environment='aligned';size=r'\small ' if t=='q-16401' else ''
 worked=prefix+size+r'\begin{'+environment+'}'+r' \\ '.join(rows)+r'\end{'+environment+'}'+'\n$$\n\nNow, the equation is written in standard form with $P(x)='+tex(m['P'])+'$ and $Q(x)='+tex(m['Q'])+'.$'
 choices=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':equation(e)} for i,e in enumerate(m['bank'])]
 question={':question/id':'draft',':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':'draft',':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':{':answer/id':str(m['correct'])}}]}
 q=localize(question,level,seed)
 meta=metadata(level,seed,t,p,selected,selected=='method-derived');meta['decision']=assignment;meta['domains']=domain;meta['mathematical_fingerprint']=semantic(m['P'],m['Q'],domain,t)
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':meta}
def metadata(level,seed,t,p,profile,eligible):
 refs=[SOURCES[t]] if t in SOURCES else [REC[':knowledge-point/canonical-example']]
 return {'version':VERSION,'seed':seed,'difficulty':level,'template':t,'bank_profile':profile,'parameters':p,'domains':DOMAINS.get(t,'real x,y'),'source_ids':[q[':question/math-academy-id'] for q in refs],'source_entities':[q[':db/id'] for q in refs],'source_question_ids':[q[':question/id'] for q in refs],'lesson_ids':[4056] if level=='moderate' else [],'source_basis':RAW['basis'],'lineage':RAW['lineage'],'python':sys.version.split()[0],'sympy':s.__version__,'eligible_for_learning':eligible,'evidence_only':not eligible,'authored_level':level=='moderate','mathematical_fingerprint':digest([t,p])}
# Easy: observed bounded rearrangement, reciprocal, cancellation and trig families.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: authored collection followed by exact nonconstant division.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed quadratic expansion and exact cancellation, four ordered rows.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def standard(e):
 l,r=e
 return s.expand(l).coeff(D)==1 and not r.has(D,y) and s.simplify(l-D).subs(y,0)==0 and s.diff(l-D,y,2)==0
def canonical_expression(e):
 # Contract double-angle quotients using the actual denominator argument;
 # CAS heuristics alone do not normalize sin(16x)/cos(8x) consistently.
 for C in s.denom(s.together(e)).atoms(s.cos):
  arg=C.args[0];e=e.xreplace({s.sin(2*arg):2*s.sin(arg)*C})
 return s.factor(s.trigsimp(s.cancel(e)))
def semantic(P,Q,domain,t=None):
 workload='square-expand-cancel' if t=='q-16401' else 'rational-collect-divide' if t=='rational-collect' else t
 return digest([s.srepr(canonical_expression(P)),s.srepr(canonical_expression(Q)),domain,workload])
def markdown(r):
 q=r['question'];chunks=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  chunks.append('\n'.join(('- [x] ' if a[':answer/id']==correct else '- [ ] ')+'$'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[])))
 if ':question/worked-solution' in q:chunks.append(q[':question/worked-solution'])
 return '\n\n'.join(chunks)
def hard_pool_cues(records):
 """Return incidental strategies that answer every member of a finite pool.

 A count of at least two is repeated practice. Retain each legitimate
 mathematical instance, but continue the deterministic candidate stream when
 the proposed pool lets one bank-only cue replace expansion throughout it.
 Prompt polarity may break a unique opposite pair, so test that cue separately.
 """
 if len(records)<2:return []
 perfect=None
 for record in records:
  question=record['question'];field=question[':question/answer-fields'][0]
  choices=field[':answer-field/choices'];values=[]
  for choice in choices:
   match=re.search(r'([+-])\s*(\d+)\s*y\s*\\cos',choice[':answer/value'])
   if not match:raise ValueError('Unrecognized hard-bank coefficient')
   values.append(int(match[2])*(1 if match[1]=='+' else -1))
  positive=[i for i,v in enumerate(values) if v>0]
  unpaired=[i for i,v in enumerate(values) if -v not in values]
  polarity=1 if re.search(r'=\(\d+-',question[':question/problem']) else -1
  matching_pair=[i for i,v in enumerate(values) if -v in values and v*polarity>0]
  predictions={
   'smallest_positive':min(positive,key=lambda i:values[i]),
   'unique_unpaired':unpaired[0] if len(unpaired)==1 else None,
   'polarity_unique_pair':matching_pair[0] if len(matching_pair)==1 else None,
  }
  predictions.update({'rank_'+str(i):values.index(v) for i,v in enumerate(sorted(values))})
  predictions.update({'position_'+str(i):i for i in range(5)})
  key=field[':answer-field/correct'][1]
  successes={name for name,index in predictions.items() if index is not None and choices[index][':answer/id']==key}
  perfect=successes if perfect is None else perfect & successes
 return sorted(perfect)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--parameters');ap.add_argument('--profile');ap.add_argument('--decision',help='Explicit signed coefficient roles as JSON');a=ap.parse_args()
 if a.count<1 or a.count>100:ap.error('Count must be in 1..100')
 out=[]
 for level in LEVELS if a.difficulty=='all' else (a.difficulty,):
  seen=set();batch=[]
  for i in range(2000):
   if len(batch)==a.count:break
   try:r=generate(level,a.seed+i,a.template,parameters=json.loads(a.parameters) if a.parameters else None,profile=a.profile,decision=json.loads(a.decision) if a.decision else None)
   except ValueError:
    if a.parameters or a.template:raise
    continue
   fp=r['generation']['mathematical_fingerprint']
   if fp not in seen:
    batch.append(r);seen.add(fp)
    if level=='hard' and a.profile in (None,'method-derived') and len(batch)==a.count and hard_pool_cues(batch):
     # Keep the prefix and seek a decision-relevant counterexample to the cue.
     # Do not change the caller's seed or pad/reorder a hand-picked batch.
     batch.pop()
  if len(batch)<a.count:raise ValueError('Bounded distinct count unavailable; returned count is not padded')
  out.extend(batch)
 print(json.dumps(out,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
if __name__=='__main__':main()
