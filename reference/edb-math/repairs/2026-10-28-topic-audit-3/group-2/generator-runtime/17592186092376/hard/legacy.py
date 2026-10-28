"""Source-backed arc-length integral setup. Normal sampling supports two plot-free
families; remaining complete source families expose exact evidence-only replay.
No database operations. See sibling package for bounded capability evidence.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent
from math_format import normalize_prose,normalize_tex,checked_math_content
SNAP=json.loads((HERE/'source-evidence.json').read_text());KP_ID=17592186092376
KP=SNAP['record'];KP_UUID=KP[':knowledge-point/id'];TITLE=KP[':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
T=s.symbols('t',real=True);C=s.cos;S=s.sin;E=s.exp;R=s.sqrt
LEVELS=('moderate','hard');DEFAULTS={'moderate':'q-15163','hard':'q-123027'}

def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def parse_tex(text):
 """Bounded source/rendered TeX parser, including complete definite integrals."""
 text=text.strip().rstrip('.,').replace('⁡','').replace('\\,','').replace('\\!','').replace('\\cdot','*').replace('\\left','').replace('\\right','').replace('\\displaystyle','')
 text=text.replace('{\\int }','\\int')
 if '\\int' in text:
  start=text.index('\\int');prefix=parse_tex(text[:start])if start else s.Integer(1);i=start+4
  assert text[i]=='_';a,i=group(text,i+1);assert text[i]=='^';b,i=group(text,i+1)
  body=text[i:];body=re.sub(r'(?:\\text\{d\}|\\mathrm\{d\}|d)\s*t$','',body)
  return s.Integral(prefix*parse_tex(body),(T,parse_tex(a),parse_tex(b)))
 text=re.sub(r'\\operatorname\{(sin|cos)\}',r'\1',text)
 text=text.replace('{sin}','sin').replace('{cos}','cos').replace('{e}','e').replace('\\sin','sin').replace('\\cos','cos').replace('\\pi','pi')
 text=text.replace('\\operatorname{ln}','log').replace('\\ln','log')
 for command in ('frac','dfrac','sqrt'):
  while '\\'+command in text:
   start=text.index('\\'+command);a,end=group(text,start+len(command)+1)
   if command!='sqrt':b,end=group(text,end);value='(('+str(parse_tex(a))+')/('+str(parse_tex(b))+'))'
   else:value='sqrt('+str(parse_tex(a))+')'
   text=text[:start]+value+text[end:]
 text=re.sub(r'(sin|cos)\^(\d+)',r'\1^{\2}',text)
 text=re.sub(r'(sin|cos)\^\{(\d+)\}\s*\{\((.*?)\)\}',r'\1(\3)^\2',text)
 text=re.sub(r'(sin|cos)\^\{(\d+)\}t',r'\1(t)^\2',text)
 text=re.sub(r'(sin|cos)t',r'\1(t)',text)
 while True:
  m=re.search(r'(sin|cos)\^\{(\d+)\}\s*\(',text)
  if not m:break
  start=m.end()-1;depth=1;end=start+1
  while depth:
   if text[end]=='(':depth+=1
   if text[end]==')':depth-=1
   end+=1
  text=text[:m.start()]+m.group(1)+'('+text[start+1:end-1]+')^'+m.group(2)+text[end:]
 text=text.replace('{','(').replace('}',')')
 return parse_expr(text,local_dict={'t':T,'pi':s.pi,'e':s.E,'sin':S,'cos':C,'sqrt':R,'exp':E,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def square_equal(a,b):
 z=s.expand(s.expand_trig(a**2-b**2))
 return z==0 or s.trigsimp(z)==0

def eq(a,b):
 if a==b:return True
 if isinstance(a,s.Integral)or isinstance(b,s.Integral):
  if not(isinstance(a,s.Integral)and isinstance(b,s.Integral)and a.limits==b.limits):return False
  # Source banks contain only principal roots with positive external factors.
  # Preserve branch/sign; squared comparison is valid only for this form.
  def principal(f):
   return all((exponent==s.Rational(1,2) or (base.is_positive is True))for base,exponent in f.as_powers_dict().items())
  if principal(a.function)and principal(b.function):return square_equal(a.function,b.function)
  return s.simplify(s.trigsimp(a.function-b.function))==0
 return s.simplify(s.trigsimp(a-b))==0

def tex(x):return s.latex(x)
def integral(f,a,b):return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+tex(f)+r'\,\mathrm{d}t'
def expr_integral(f,a,b):return s.Integral(f,(T,a,b))

# Exact source mathematical objects. Banks are complete profiles, never pooled.
# Order corresponds to retained source order; interpretation of opaque compound
# source mistakes remains unspecified. Replay compares every full object.
def evidence(mid):
 t=T;u=S(t);v=C(t)
 if mid=='q-15185':
  x,y,a,b=E(t),E(t)*S(t),-3,1
  fs=[E(t)*R(1+S(2*t)),E(2*t)*R(1+C(2*t)),E(2*t)*R(1+S(2*t)),E(t)*R(2+C(2*t)),E(t)*R(2+S(2*t))]
 elif mid=='q-15163':return data(mid,{'A':2,'B':2})
 elif mid=='q-20909':
  x,y,a,b=t/2,E(t),0,1
  fs=[R(2*E(2*t)+4)/4,R(4*E(2*t)+1)/2,R(E(t)+1)/2,R(E(t)+4)/4,R(E(2*t)+1)/2]
 elif mid=='q-21339':
  x,y,a,b=2*S(3*t)-1,2*C(2*t)+2,0,s.pi/2
  fs=[2*R(6*C(3*t)**2-2*S(2*t)**2),R(9*C(3*t)**2-4*S(2*t)**2),2*R(6*C(3*t)**2+2*S(2*t)**2),4*R(C(3*t)**2+S(2*t)**2),2*R(9*C(3*t)**2+4*S(2*t)**2)]
 elif mid=='q-21347':
  x,y,a,b=S(2*t),S(3*t),s.pi/4,s.pi/2
  fs=[R(2*C(2*t)**2+9*C(3*t)**2),R(16*C(2*t)**2+9*C(3*t)**2),R(4*C(2*t)**2+3*C(3*t)**2),R(2*C(2*t)**2+3*C(3*t)**2),R(4*C(2*t)**2+9*C(3*t)**2)]
 elif mid=='q-21354':
  x,y,a,b=u-v,t-u,0,s.pi/4
  fs=[R(1+S(2*t)+v*v),R(1+S(2*t)-2*v),R(1+S(2*t)+2*v+v*v),R(2+S(2*t)-2*v+v*v),R(2+S(2*t)+v-v*v)]
 elif mid=='q-123027':return data(mid,{'A':3,'B':8})
 elif mid=='q-123030':
  x,y,a,b=C(5*t),6*u,0,s.pi/2
  fs=[R(25*S(5*t)+36*C(6*t)),2*R(5*S(5*t)**2+6*v*v),R(10*S(5*t)**2+12*v*v),R(25*u+36*v*v),R(25*S(5*t)**2+36*v*v)]
 elif mid=='q-15178':
  x,y,a,b=3*v,2*u,0,s.pi/2
  fs=[R(3*u*u+2*v*v),3*u+2*v,R(9*u*u+4*v*v),R(4*u*u+9*v*v),9*u*u+4*v*v]
 elif mid=='q-15182':
  x,y,a,b=C(3*t),3*u,0,s.pi/2
  fs=[9*R(S(3*t)**2+v*v),3*R(S(3*t)**2+v*v),3*R(2*S(3*t)**2+v*v),R(3*u*u+C(3*t)**2),9*R(u*u+C(3*t)**2)]
 elif mid=='q-21353':
  x,y,a,b=E(t),t,0,2
  fs=[R(E(2*t)-1),R(E(2*t)+4),R(E(t)-1),R(E(t)+2),R(E(2*t)+1)]
 else:raise ValueError('Incomplete/unrated source has no eligible replay: '+mid)
 return x,y,s.sympify(a),s.sympify(b),fs

# Supported normal template families; fixed structural roles and response shape.
def data(mid,p):
 if set(p)!={'A','B'} or any(type(v)is not int for v in p.values()):raise ValueError('A and B must be exact integers')
 A=s.Integer(p['A']);B=s.Integer(p['B']);t=T
 if mid=='q-123027':
  assert 2<=A<=6 and 4<=B<=12 and B>A+1
  x,y,a,b=A*C(t),B*t+C(t),s.Integer(-1),s.Integer(1)
  u=S(t);rad=(A*A+1)*u*u-2*B*u+B*B
  fs=[2*R((A*A+1)*u*u/2-B*u+B*B/2),R(A*A*u*u-B*u+B*B),R(u*u-2*B*u+B*B),R(B*u*u-2*u+B),R(rad)]
 elif mid=='q-15163':
  assert A in (2,3) and 2<=B<=5
  x,y,a,b=t+A*S(t),1+C(B*t),s.Integer(2),s.Integer(5)
  u=C(t);v=S(B*t)
  fs=[R(1+4*A*u+4*A*A*u*u+4*B*B*v*v),R(1+A*u+4*A*A*u*u+B*B*v*v),R(1+2*A*u+A*A*u*u+B*B*v*v),R(1+2*A*u+A*A*u*u+4*B*B*v*v),R(1+A*u+A*u*u+B*B*v*v)]
 else:raise ValueError('Normal variants unavailable for source family '+mid)
 return x,y,a,b,fs

def domain(mid):
 if mid=='q-123027':return [{'A':a,'B':b}for a in range(2,7)for b in range(4,13)if b>a+1]
 if mid=='q-15163':return [{'A':a,'B':b}for a in (2,3)for b in range(2,6)]
 raise ValueError(mid)

def fingerprint(q):
 prompt=re.sub(r'!\[.*?\]\(.*?\)\s*','',q[':question/problem'])
 m=re.search(r'\$x\s*=\s*(.*?),\s*(?:\\,)?\s*y\s*=\s*(.*?)\$',prompt,re.S)
 if not m:raise ValueError('Coordinate pair missing')
 x,y=map(parse_tex,m.groups());bounds=re.search(r'from \$t\s*=\s*(.*?)\$ to \$t\s*=\s*(.*?)\$',prompt)
 a,b=map(parse_tex,bounds.groups())
 # Assess supplied derivatives and integration bounds; exclude translations,
 # signs of x/y derivative, bank, solution, seed, labels and option order.
 parts=sorted([s.srepr(s.trigsimp(s.diff(x,T)**2)),s.srepr(s.trigsimp(s.diff(y,T)**2))])
 return hashlib.sha256(json.dumps([parts,s.srepr(a),s.srepr(b)]).encode()).hexdigest()

def build(mid,p,seed,replay=False):
 old=SOURCES[mid];x,y,a,b,fs=evidence(mid)if replay else data(mid,p)
 level=str(old[':question/difficulty'][':db/ident']).split('/')[-1]
 of=old[':question/answer-fields'][0];cv=parse_tex(of[':answer-field/correct'][':answer/value'])
 if replay:correct=next(i for i,f in enumerate(fs)if eq(expr_integral(f,a,b),cv))
 else:correct=4 if mid=='q-123027'else 2
 values=[normalize_tex(integral(f,a,b))for f in fs]
 if replay:
  prompt=normalize_prose(old[':question/problem']);solution=normalize_prose(old[':question/worked-solution'])
 else:
  prompt=normalize_prose('Which of the following gives the length of the curve defined by the parametric equations\n$x='+tex(x)+r',\,y='+tex(y)+'$\nfrom $t='+tex(a)+'$ to $t='+tex(b)+'$?')
  # Preserve observed formula, two derivative computations, substitution, and
  # expansion. No integration or extra reasoning stage is introduced.
  dx,dy=s.diff(x,T),s.diff(y,T)
  opening=r'To compute the arc length $L$ of a parametrically defined curve, we use the formula'
  formula=r'L=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t.'
  dxrow=r'\frac{\mathrm{d}x}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left('+tex(x)+r'\right)='+tex(dx)
  dyrow=r'\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left('+tex(y)+r'\right)='+tex(dy)+'.'
  # Hard source includes an expanded four-term row before collecting sin².
  substitution=r'\int_{'+tex(a)+'}^{'+tex(b)+r'}\sqrt{\left('+tex(dx)+r'\right)^2+\left('+tex(dy)+r'\right)^2}\,\mathrm{d}t'
  rows=[r'L&='+r'\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t',r'&='+substitution]
  if mid=='q-123027':
   A,B=p['A'],p['B'];expanded=f'{A*A}\\sin^2(t)+{B*B}-{2*B}\\sin(t)+\\sin^2(t)'
   rows.append(r'&=\int_{'+tex(a)+'}^{'+tex(b)+r'}\sqrt{'+expanded+r'}\,\mathrm{d}t')
  rows.append('&='+values[correct]+'.')
  solution=normalize_prose(opening+'\n\n$$\n'+formula+'\n$$\n\nComputing the derivatives of $x$ and $y,$ we have\n\n$$\n'+dxrow+'\n$$\n\nand\n\n$$\n'+dyrow+'\n$$\n\nWe substitute these derivatives in the formula for arc length, and we get\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$')
 ident=str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps([prompt,solution,sorted(values)],ensure_ascii=False)))
 fid=str(uuid.uuid5(uuid.UUID(ident),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value}for value in values]
 cid=answers[correct][':answer/id'];random.Random(seed).shuffle(answers)
 q={':question/id':ident,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',cid],':answer-field/choices':answers}]}
 return {'knowledge_point':{'db/id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'sympy':s.__version__,'seed':seed,'template':mid,'bank_profile':'source:'+mid,'parameters':p,'source_basis':SNAP['basis'],'source_question_id':old[':question/id'],'source_ma_id':mid,'evidence_only':replay,'eligible_for_learning':not replay,'mathematical_fingerprint':hashlib.sha256(str([s.diff(x,T)**2,s.diff(y,T)**2,a,b]).encode()).hexdigest(),'domains':'t in real interval; A,B positive integers in documented finite domain'}}

@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unsupported difficulty '+str(level))
 mid=template or DEFAULTS[level]
 if mid not in SOURCES or str(SOURCES[mid].get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]!=level:raise ValueError('Template/difficulty mismatch')
 if profile=='source-replay':
  if parameters not in (None,{}):raise ValueError('Source replay uses original parameters only')
  return build(mid,{},seed,True)
 if profile not in (None,'source:'+mid):raise ValueError('Unknown bank profile')
 if mid not in DEFAULTS.values():raise ValueError('Evidence-only family; no validated normal sampler')
 p=parameters or random.Random(seed).choice(domain(mid))
 return build(mid,p,seed)

def moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)'if a[':answer/id']==f[':answer-field/correct'][1]else'')for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=LEVELS+('all',),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 records=[]
 for l in (LEVELS if a.difficulty=='all'else[a.difficulty]):
  pool=domain(DEFAULTS[l]);random.Random(a.seed).shuffle(pool)
  if not 0<a.count<=len(pool):raise ValueError('Requested count exceeds bounded distinct '+l+' domain of '+str(len(pool)))
  records.extend(generate(l,a.seed+i,parameters=params)for i,params in enumerate(pool[:a.count]))
 print(json.dumps(records,indent=2)if a.format=='json'else'\n\n---\n\n'.join(map(markdown,records)))
