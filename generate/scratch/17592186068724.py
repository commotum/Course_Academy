#!/usr/bin/env python3
"""Natural-log substitution. Bounded source bank profiles; no database writes."""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186068724-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 import os
 executable=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(executable),[str(executable),__file__,*sys.argv[1:]])
H=Path(__file__).with_suffix(''); SOURCE=json.loads((H/'reference/source.json').read_text())
KP_ID=17592186068724; KP_UUID=SOURCE[':knowledge-point/id']; TITLE=SOURCE[':knowledge-point/title']
VERSION='68724-v1'; GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));SUPPORTED_LEVELS=('easy','moderate')
X=sp.Symbol('x',real=True);T=sp.Symbol('t',real=True)
# source, band, numerator scale k, denominator a*x^n+b*x+c, n, variable
CASES=[('q-132982','easy',-16,2,0,3,2,'t'),('q-12501','easy',1,1,0,10,3,'x'),('q-49451','easy',4,1,0,1,2,'x'),('q-49572','easy',1,1,0,9,10,'x'),('q-72605','easy',10,-5,0,2,5,'x'),('q-72566','moderate',1,1,-1,0,3,'x'),('q-113719','moderate',1,-1,1,1,4,'x'),('q-113720','moderate',1,1,-1,0,5,'x'),('q-113721','moderate',1,1,2,0,2,'x')]
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
def case(t):return next(c for c in CASES if c[0]==t)
def defaults(c):return dict(zip(('k','a','b','c','n','variable'),c[2:]))
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def digest(x):return hashlib.sha256(str(x).encode()).hexdigest()
def tex(x):return sp.latex(x,order='lex')
def data(p,level):
 k,a,b,c,n=(sp.Rational(p[z])for z in ('k','a','b','c','n'));z=T if p['variable']=='t'else X
 u=a*z**n+b*z+c;v=sp.diff(u,z);numerator=k*z**(n-1)if level=='easy'else v
 ratio=k/(a*n)if level=='easy'else sp.Integer(1)
 return z,u,v,numerator,sp.cancel(numerator/u),ratio
# Formal log derivatives describe log|u| on every real connected interval u != 0.
def bank(t,p):
 z,u,v,num,f,r=data(p,case(t)[1]);L=sp.log(u);n=sp.Rational(p['n']);a=sp.Rational(p['a']);c=sp.Rational(p['c']);b=sp.Rational(p['b']);k=sp.Rational(p['k'])
 if t=='q-132982':values=[r*L];recipes=['k/(a*n)*ln(u)'];correct=0
 elif t=='q-12501':values=[r*L,L,L/(n-1),L/c,n*L];recipes=['r*ln(u)','ln(u)','ln(u)/(n-1)','ln(u)/c','n*ln(u)'];correct=0
 elif t=='q-49451':values=[L/(a*n),L/k,1/u**2,r*L,r/u**2];recipes=['ln(u)/(a*n)','ln(u)/k','1/u^2','r*ln(u)','r/u^2'];correct=3
 elif t=='q-49572':values=[n*L,1/u**2,L/2,r*L,c*L];recipes=['n*ln(u)','1/u^2','ln(u)/2','r*ln(u)','c*ln(u)'];correct=3
 elif t=='q-72605':values=[-a*r*L,-r/u**2,1/(r*u**2),-L/r,r*L];recipes=['-a*r*ln(u)','-r/u^2','1/(r*u^2)','-ln(u)/r','r*ln(u)'];correct=4
 elif t=='q-72566':
  shifted=a*z**n+b+c;altered=n*a*z**(n-1)+b*z+c
  values=[sp.log(v),sp.log(shifted),L,sp.log(altered),sp.log(1/shifted)];recipes=['ln(v)','ln(a*x^n+b+c)','ln(u)','ln(n*a*x^(n-1)+b*x+c)','ln(1/(a*x^n+b+c))'];correct=2
 else:
  values=[L/v,sp.log(v/u),L,sp.log(u/v),sp.log(v)];recipes=['ln(u)/v','ln(v/u)','ln(u)','ln(u/v)','ln(v)'];correct=2
 return values,correct,recipes

def logtex(arg,absolute=True):return r'\operatorname{ln}'+(r'\left|'+tex(arg)+r'\right|'if absolute else r'\left('+tex(arg)+r'\right)')
def answertex(t,p):
 z,u,v,num,f,r=data(p,case(t)[1]);n=sp.Rational(p['n']);a=sp.Rational(p['a']);b=sp.Rational(p['b']);c=sp.Rational(p['c']);k=sp.Rational(p['k'])
 absolute=t not in ('q-132982','q-49451')
 L=logtex(u,absolute)
 def scale(s,txt):return txt if s==1 else '-'+txt if s==-1 else tex(s)+txt
 if t=='q-132982':return [scale(r,L)]
 if t=='q-12501':arr=[scale(r,L),L,scale(1/(n-1),L),scale(1/c,L),scale(n,L)]
 elif t=='q-49451':arr=[scale(1/(a*n),L),scale(1/k,L),tex(1/u**2),scale(r,L),tex(r/u**2)]
 elif t=='q-49572':arr=[scale(n,L),tex(1/u**2),scale(sp.Rational(1,2),L),scale(r,L),scale(c,L)]
 elif t=='q-72605':arr=[scale(-a*r,L),tex(-r/u**2),tex(1/(r*u**2)),scale(-1/r,L),scale(r,L)]
 elif t=='q-72566':arr=[logtex(v),logtex(a*z**n+b+c),L,logtex(n*a*z**(n-1)+b*z+c),logtex(1/(a*z**n+b+c))]
 else:arr=[r'\frac{'+L+'}{'+tex(v)+'}',logtex(v/u),L,logtex(u/v),logtex(v)]
 return [s+'+C'for s in arr]

def render(t,p):
 level=case(t)[1];z,u,v,num,f,r=data(p,level);var=str(z);inner=tex(u);outside=tex(num);monomial=tex(z**(p['n']-1));integral=r'\int \frac{'+outside+'}{'+inner+r'}\,\text{d}'+var
 if t=='q-132982':
  prompt=SOURCES[t][':question/problem'].replace('-16t',outside).replace('2{t}^{2}+3',inner)
 elif t=='q-12501':prompt='Calculate the integral of $'+r'\frac{'+outside+'}{'+inner+'}$ with respect to $'+var+'.$'
 elif t in ('q-49451','q-72605','q-72566'):prompt='$'+integral+'=$'
 else:prompt='Calculate $'+integral+'.$'
 intro='Let $u='+inner+'.$ Then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+var+'}='+tex(v)
 if level=='moderate':
  intro+=r'\,⟹\,\text{d}u=('+tex(v)+r')\,\text{d}'+var+',\n$$\n\nand we can solve the resulting integral as follows:\n\n'
  rows=[integral+r' & =\int \frac{1}{'+inner+r'}\cdot ('+outside+r')\,\text{d}'+var,r' & =\int \frac{1}{u}\,\text{d}u',r' & =\operatorname{ln}|u|+C',r' & ='+logtex(u)+'+C']
 else:
  factor=sp.Rational(1,p['a']*p['n']);constant='K'if t=='q-132982'else'C';prefix=''if p['k']==1 else tex(sp.Rational(p['k']))
  intro+=r'\,⟹\,'+tex(factor)+r'\text{d}u='+monomial+r'\,\text{d}'+var+'.\n$$\n\n'+('We can solve the required integral as follows:'if t=='q-132982'else'and we can solve the resulting integral as follows:')+'\n\n'
  rows=[integral+' & ='+prefix+r'\int \frac{1}{'+inner+r'}\cdot '+monomial+r'\,\text{d}'+var,' & ='+prefix+r'\int \frac{1}{u}\cdot '+tex(factor)+r'\,\text{d}u',' & ='+tex(r)+r'\int \frac{1}{u}\,\text{d}u',' & ='+tex(r)+r'\operatorname{ln}|u|+'+constant]
  if t=='q-72605':rows.insert(2,' & ='+r'\frac{'+str(-p['k'])+'}{'+str(-p['a']*p['n'])+r'}\int \frac{1}{u}\,\text{d}u')
  final=answertex(t,p)[bank(t,p)[1]];final=final if t!='q-132982'else final+'+K';rows.append(' & ='+final)
 solution=intro+'$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,solution

def fingerprint(q):
 sys.path.insert(0,str(H));from parser import prompt
 return digest(sp.srepr(sp.cancel(prompt(q[':question/problem']))))
def generate(level,seed=0,template=None,parameters=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('hard: no observed hard source workload; bounded capability exception')
 rng=random.Random(seed);eligible=[c for c in CASES if c[1]==level];c=case(template)if template else rng.choice(eligible)
 if c not in eligible:raise ValueError('template difficulty mismatch')
 for attempt in range(100):
  p=defaults(c)
  if parameters is not None:p.update(parameters)
  else:
   # Bounded extension varies constant or linear coefficient, retaining degree/sign/field shape.
   if level=='easy':p['c']=rng.randint(1,19 if c[0]=='q-132982'else 20)
   elif c[0]=='q-113719':p['c']=rng.randint(1,20)
   else:p['b']=(1 if p['b']>0 else -1)*rng.randint(1,12)
  fixed=defaults(c);vary='c'if level=='easy'or c[0]=='q-113719'else'b'
  if any(p[key]!=value for key,value in fixed.items()if key!=vary):raise ValueError('outside certified fixed parameters')
  if not isinstance(p[vary],int):raise ValueError('integer parameter required')
  if vary=='c' and not 1<=p[vary]<=(19 if c[0]=='q-132982'else 20):raise ValueError('outside certified constant range')
  if vary=='b' and (not 1<=abs(p[vary])<=12 or p[vary]*fixed[vary]<=0):raise ValueError('outside certified signed linear range')
  vals,correct,recipes=bank(c[0],p);z,u,v,num,f,r=data(p,level)
  derivatives=[sp.cancel(sp.diff(a,z))for a in vals]
  # Compare antiderivatives modulo constants, the correct notion for +C options.
  if any(sp.simplify(a-b)==0 for i,a in enumerate(derivatives)for b in derivatives[i+1:]):
   if parameters is not None:raise ValueError('whole-bank antiderivative collision')
   continue
  assert sp.simplify(derivatives[correct]-f)==0
  problem,solution=render(c[0],p);fp=digest(sp.srepr(f));qid=uid('task:'+fp);fid=uid('field:'+qid);answers=[]
  for value in answertex(c[0],p):answers.append({':answer/id':uid('answer:'+fid+':'+value),':answer/type':':answer.type/math',':answer/value':value})
  field={':answer-field/id':fid,':answer-field/key':'field-1'if c[0]=='q-132982'else'selection',':answer-field/type':':answer-field.type/blank'if c[0]=='q-132982'else':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':c[0],'bank_profile':c[0],'recipes':recipes,'seed':seed,'parameters':p,'domain':'real connected intervals where denominator != 0; blank positive quadratic is positive on R','source_basis':1934,'source_question_id':SOURCES[c[0]][':db/id'],'mathematical_fingerprint':fp,'sympy_version':sp.__version__,'plots':'none'}}
 raise ValueError('bounded profile sampling exhausted')
def batch(level,count,seed=0):
 records=[];seen=set()
 for j in range(max(200,count*30)):
  r=generate(level,seed+j,template=[c[0]for c in CASES if c[1]==level][j%len([c for c in CASES if c[1]==level])]);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:records.append(r);seen.add(fp)
  if len(records)==count:return records
 return records

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186068724-source-policy.json'))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--template');a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args()
 try:
  records=batch(args.difficulty,args.count,args.seed)if not args.template else[generate(args.difficulty,args.seed,args.template)]
  print(json.dumps(records,indent=2)if args.format=='json'else'\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in records))
 except ValueError as e:a.exit(2,str(e)+'\n')
