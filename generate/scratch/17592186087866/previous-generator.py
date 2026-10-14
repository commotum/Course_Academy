"""Source-backed first-order ODE standard-form generator (easy/hard).

No moderate workload is inferred from absence. Normal CLI rejects that band.
Every complete source bank has its own profile. No seed/order aliases are tasks.
"""
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
try:
 import sympy as s
except ModuleNotFoundError:
 if __name__!='__main__':raise
 import os
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if not interpreter.is_file() or Path(sys.executable).resolve()==interpreter.resolve():raise
 os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
HERE=Path(__file__).with_suffix(''); ROOT=HERE.parents[2]
RAW=json.loads((HERE/'reference/source.json').read_text()); REC=RAW['record']
KP=17592186087866; KP_UUID=REC[':knowledge-point/id']; TITLE=REC[':knowledge-point/title']
VERSION='standard-form-1.0.0'; LEVELS=('easy','hard')
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,y,D=s.symbols('x y D',real=True)
FAMILIES={'easy':['q-16400','q-8359','q-103349','q-103354','q-16396','q-79697','q-79699','q-8360'],'hard':['q-16401']}
ORIGINAL={'q-16400':{'a':2,'b':3,'c':1,'h':4},'q-8359':{'k':1},'q-103349':{'n':1},'q-103354':{'n':1},'q-16396':{'k':1},'q-79697':{'k':1},'q-79699':{'k':5},'q-8360':{'k':2},'q-16401':{'a':1,'b':1,'n':1}}
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
 return s.simplify(s.expand(residual/a))
def data(t,p):
 """Each branch preserves source operations, full bank and solution sequence."""
 if set(p)!=set(ORIGINAL[t]) or any(type(v)!=int for v in p.values()):raise ValueError('Integer parameter shape')
 if t=='q-16400':
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
  n=p['n'];bounds(n,1,6);P=2*s.exp(-n*x);Q=x*s.exp(-2*n*x)
  stages=[eq(s.exp(2*n*x)*D+2*s.exp(n*x)*y-x,0),eq(s.exp(2*n*x)*D+2*s.exp(n*x)*y,x),eq(D+P*y,Q)]
  bank=[eq(D+s.exp(-2*n*x)*y-x*s.exp(-n*x),0),stages[-1],eq(D+P*y-Q,0),eq(D-y,Q),eq(D+2*y,Q)];correct=1
 elif t=='q-103354':
  n=p['n'];bounds(n,1,6);C=s.cos(n*x);S=s.sin(n*x);P=-s.tan(n*x);Q=-2*S
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
  bounds(a,1,6);bounds(b,1,4);bounds(n,1,6);C=s.cos(n*x);P=2*a*b*C;Q=s.Integer(a*a)
  quadratic=b*b*y*y*C*C
  stages=[eq(D+quadratic,(a-b*y*C)**2),eq(D+quadratic,uneval_add(a*a,quadratic,-2*a*b*y*C)),eq(D,a*a-2*a*b*y*C),eq(D+P*y,Q)]
  bank=[stages[-1],eq(D+b*y*C,a*a-a*b*C),eq(D+b*b*y*C*C,(a-b*C)**2),eq(D,a*a),eq(D+4*a*b*y*C,a*a)];correct=0
 return {'P':P,'Q':Q,'stages':stages,'bank':bank,'correct':correct}
def bounds(k,lo,hi):
 if not lo<=k<=hi:raise ValueError('Parameter outside frozen bounds')
def sample(t,rng):
 if t=='q-16400':return dict(a=rng.randint(2,5),b=rng.randint(1,5),c=rng.randint(1,5),h=rng.randint(1,8))
 if t=='q-16401':return dict(a=rng.randint(1,6),b=rng.randint(1,4),n=rng.randint(1,6))
 return {z:rng.randint(2 if t=='q-79699' else 1,6 if z=='n' else 8) for z in ORIGINAL[t]}
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unsupported band: no validated moderate template')
 rng=random.Random(seed);t=template or rng.choice(FAMILIES[level])
 if t not in FAMILIES[level] or profile not in (None,t):raise ValueError('Whole observed source profile required')
 p=parameters if parameters is not None else sample(t,rng);m=data(t,p)
 # Closed source-shaped bank. Equal valid standard-form choices are ambiguous.
 valid=[standard(e) and s.simplify(normalized(e)-normalized(m['stages'][0]))==0 for e in m['bank']]
 if valid != [i==m['correct'] for i in range(5)]:raise ValueError('Ambiguous/invalid bank')
 if len(set(equation(e) for e in m['bank']))!=5:raise ValueError('Duplicate rendered choice')
 core=normalized(m['stages'][0]);domain=str(s.cos(p['n']*x))+' != 0' if t=='q-103354' else DOMAINS.get(t,'real x,y')
 # Canonical forcing scale removes dependent scaling; prompts are not seed aliases.
 fp=semantic(m['P'],m['Q'],domain)
 question_id=uid(VERSION+':'+level+':'+t+':'+digest(p));field_id=uid(question_id+':selection')
 choices=[{':answer/id':uid(field_id+':'+equation(e)),':answer/type':':answer.type/math',':answer/value':equation(e)} for e in m['bank']]
 domain_tex={'q-8359':r'\,,\ x\ne 0','q-79697':r'\,,\ x\ne 0','q-16396':r'\,,\ y\ne 0','q-79699':r'\,,\ y\ne 0','q-103354':r'\,,\ '+tex(s.cos(p.get('n',1)*x))+r'\ne 0','q-8360':r'\,,\ \sin x\ne 0'}.get(t,'')
 prompt='Write the following first-order linear ODE in standard form.\n\n$$\n'+equation(m['stages'][0])+domain_tex+r'\,.'+'\n$$'
 source=SOURCES[t];sol=source[':question/worked-solution'];prefix=sol.split(r'\begin{aligned}')[0]
 # Preserve source instructional prose and block structure; remove empty math blocks.
 prefix=prefix.replace('$$\n\n$$\n\n','')
 rows=[]
 for i,e in enumerate(m['stages']):
  row=equation(e)
  if i==len(m['stages'])-1 or (t in ('q-16396','q-79697','q-79699') and i==len(m['stages'])-2):
   row=tex(D)+r'+\underbrace{('+tex(m['P'])+r')}_{P(x)}y=\underbrace{'+tex(m['Q'])+r'}_{Q(x)}'
  rows.append(row.replace('=','&=',1))
 worked=prefix+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nNow, the equation is written in standard form with $P(x)='+tex(m['P'])+'$ and $Q(x)='+tex(m['Q'])+'.$'
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':{':question/id':question_id,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[m['correct']][':answer/id']]}]},'generation':{'version':VERSION,'seed':seed,'template':t,'bank_profile':t,'parameters':p,'domains':domain,'source_ids':[t],'source_basis':RAW['basis'],'lineage':RAW['lineage'],'python':sys.version.split()[0],'sympy':s.__version__,'mathematical_fingerprint':fp,'eligible_for_learning':True,'evidence_only':False}}
def standard(e):
 l,r=e
 return s.expand(l).coeff(D)==1 and not r.has(D,y) and s.simplify(l-D).subs(y,0)==0 and s.diff(l-D,y,2)==0
def semantic(P,Q,domain):
 # Multiplying y by any nonzero constant changes only Q's scale; exclude it.
 scale=s.expand(Q).as_ordered_terms()[0].as_coeff_Mul()[0] if Q!=0 else s.Integer(1)
 shape=s.simplify(s.trigsimp(Q/scale)) if Q!=0 else Q
 return digest([s.srepr(s.trigsimp(P)),s.srepr(shape),domain])
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return q[':question/problem']+'\n\n'+'\n'.join(('- [x] ' if a[':answer/id']==correct else '- [ ] ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--parameters');a=ap.parse_args()
 if a.count<1 or a.count>100:ap.error('Count must be in 1..100')
 out=[];seen=set()
 for i in range(2000):
  if len(out)==a.count:break
  try:r=generate(a.difficulty,a.seed+i,a.template,json.loads(a.parameters) if a.parameters else None)
  except ValueError:
   if a.parameters or a.difficulty not in LEVELS:raise
   continue
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 if len(out)<a.count:raise ValueError('Bounded distinct count unavailable; returned count is not padded')
 print(json.dumps(out,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
if __name__=='__main__':main()
