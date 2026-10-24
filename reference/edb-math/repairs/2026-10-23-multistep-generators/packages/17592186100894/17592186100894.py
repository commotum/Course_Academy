#!/usr/bin/env python3
"""Rearrange/separate IVPs: observed replay plus decision-bearing repairs.

No database access. h in {-4,...,4}; h=0 replays source. Translation changes
ODE coefficients/arguments and the initial abscissa together, preserving the
rearrangement, integration, inversion, response fragment and solution stages.
Empirical banks are whole source-expression profiles, with no inferred error
intent. q-104058 is excluded: its initial condition makes 0*y'=2.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186100894-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
HERE=Path(__file__).resolve().with_suffix('')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from math_format import normalize_prose, normalize_tex, checked_math_content
spec=importlib.util.spec_from_file_location('ivp894_parser',HERE/'parse_math.py');pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)
X,Y=pm.X,pm.Y
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];ID=17592186100894
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
VERSION='rearrange-separate-ivp-2026-10-21-v3';SUPPORTED=('easy','moderate');SHIFTS=tuple(range(-4,5))
EXCLUDED={'q-104058':'At x=1,y=1 the supplied equation has left side 0 for every finite derivative, but right side 2; no classical solution satisfies the initial condition.'}
# Exact ODE RHS, initial abscissa, initial ordinate, and particular solution.
MODELS={
'q-20071':(s.exp(4*X-Y),0,5,s.log((s.exp(4*X)+4*s.exp(5)-1)/4)),
'q-79372':(X*Y/(X+1),1,s.E,2*s.exp(X)/(X+1)),
'q-128192':(X*Y**2,1,2,-2/(X**2-2)),
'q-104059':(Y**2*(1/X**2+1),-1,1,X/(1+X-X**2)),
'q-104064':(Y**2*(3*X**2-4*X**3),2,s.Rational(1,8),1/(X**4-X**3)),
'q-104065':(s.cot(X)+8*X,s.pi/2,s.pi**2,s.log(s.sin(X))+4*X**2),
'q-14267':(s.exp(X+Y),0,-s.log(2),-s.log(3-s.exp(X))),
'q-350957':((6*X**2-1)*s.exp(-Y),1,0,s.log(2*X**3-X)),
'q-355546':(5/X**2+8*X,1,6,-5/X+4*X**2+7),
'q-355547':(3/s.sqrt(X)+4*X,1,11,6*s.sqrt(X)+2*X**2+3),
'q-355559':(2*X*(Y**2+1)/Y,0,1,s.sqrt(2*s.exp(2*X**2)-1)),
'q-355564':(4*X*Y/(2*X-1),1,s.exp(2),(2*X-1)*s.exp(2*X)),
'q-355576':(s.exp(-2*X-Y),0,2,s.log((-s.exp(-2*X)+2*s.exp(2)+1)/2)),
'q-355577':(s.exp(-X-Y),0,-s.log(4),s.log(s.Rational(5,4)-s.exp(-X))),
'q-355582':(s.exp(-X-Y),0,0,s.log(2-s.exp(-X))),
'q-4016':(s.exp(X-2*Y),0,0,s.log(2*s.exp(X)-1)/2),
'q-79371':(3*s.exp(-X)+2*X,0,-3,X**2-3*s.exp(-X)),
'q-79373':((4*X**3-1)*s.exp(-Y),1,0,s.log(X**4-X+1)),
'q-79425':(2*X*(2+Y**3)/(3*Y**2),0,1,(3*s.exp(X**2)-2)**s.Rational(1,3)),
'q-355560':(Y**2*(4/X**2+1),2,-1,X/(4-X-X**2)),
'q-104056':(s.exp(-X)-4*X,0,7,-s.exp(-X)-2*X**2+8),
'q-104057':((3*X**2-2*X)*s.exp(-Y),1,1,s.log(X**3-X**2+s.E)),
'q-8306':(Y*(2*X+X**2),1,1,s.exp((X**3+3*X**2-4)/3))}
UNGRADABLE={}
MODELS['q-128199']=(X/Y,0,1,s.sqrt(X**2+1))
MODELS['q-126765']=(2*X*s.sqrt(1-Y**2),0,0,s.sin(X**2))
REPAIRS={
'q-79372':'The source says applying the natural logarithm before exponentiating; use applying the exponential function.',
'q-8306':'The source says applying the natural logarithm before exponentiating; use applying the exponential function.',
'q-128192':'Replace the unavailable cross-reference From part 6 with direct general-solution wording; retain subsequent stages.',
'q-355560':'Captured table lost its fraction layout. Restore y(x)=x/(field-1); canonical field is the denominator 4-x-x².',
'q-104056':'The initial-value substitution line has +2*0² instead of -2*0²; both are zero. Correct the sign without altering the source record.',
'q-79425':'On the declared positive branch K=exp(C1-C2)>0; the source unnecessary ± sign is removed.'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),x))
def tex(x):return normalize_tex(s.latex(x,ln_notation=True))
def level(mid):return QS[mid][':question/difficulty'][':db/ident'].split('/')[-1]
def translate_math(text,h):
 if not h or re.fullmatch(r'x(?:[,:.]|\\mathbin\{:\})?',text.strip()):return text
 tokens={}
 def hold(value):
  key='ZZHOLD'+str(len(tokens))+'ZZ';tokens[key]=value;return key
 def ycall(m):
  arg=m[1]
  return hold('y(x)' if arg=='x' else 'y('+tex(pm.expression(arg)+h)+')')
 text=re.sub(r'\\(?:text|textrm|mathrm)\{d\}x',lambda m:hold(m[0]),text)
 text=re.sub(r'\\(?:text|textrm|mathrm)\{[^{}]*\}',lambda m:hold(m[0]),text)
 text=re.sub(r'y\(([^()]*)\)',ycall,text)
 # The differential's x denotes the independent variable, not a supplied value.
 text=re.sub(r'\\text\{d\}x',lambda m:hold(m[0]),text)
 text=re.sub(r'\\[a-zA-Z]+|x',lambda m:'('+tex(X-h)+')' if m[0]=='x' else m[0],text)
 for key,value in tokens.items():text=text.replace(key,value)
 return text

def translate_prose(text,h):
 return ''.join(part[:len(delim)]+translate_math(part[len(delim):-len(delim)],h)+delim if (delim:='$$' if part.startswith('$$') else '$' if part.startswith('$') else '') else part for part in re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S))
def question_text(mid,h):
 q=QS[mid];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if mid in ('q-79372','q-8306'):sol=sol.replace('Applying the natural logarithm to both sides','Applying the exponential function to both sides')
 if mid=='q-128199':sol=sol.replace('From part 6, we found the general solution','Separating variables and integrating, we find the general solution')
 if mid=='q-126765':
  prompt="Find the nonconstant local solution to $y'=2x\\sqrt{1-y^2}$ by separating variables. Work on a local branch where the sine argument $\\theta$ satisfies $-\\pi/2<\\theta<\\pi/2$. Express the solution as $y=\\sin(\\boxed{\\text{expression}}+C)$.\n\nExpression: {{field-1}}"
  sol += '\n\nThis nonconstant branch applies where $-\\pi/2<x^2+C<\\pi/2$, so $\\cos(x^2+C)>0$. The constant endpoint solutions $y=\\pm1$ also solve the ODE.'
 if mid=='q-128192':
  prompt=re.sub(r'\s+',' ',prompt).replace(' $$ ','\n\n$$\n').replace(' $y(x)', '\n\n$y(x)')
  sol=sol.replace('From part 6, we found the general solution','Separating variables and integrating, we find the general solution')
 if mid=='q-104056':sol=sol.replace(r'+2\cdot {0}^{2}',r'-2\cdot {0}^{2}')
 if mid=='q-79425':sol=sol.replace(r'K=\pm {e}',r'K={e}')
 if mid=='q-355560':prompt=prompt.split('\n\n|')[0]+'\n\n$y(x)=\\frac{x}{\\boxed{\\text{denominator}}}$\n\nDenominator: {{field-1}}'
 return normalize_prose(translate_prose(prompt,h)),normalize_prose(translate_prose(sol,h))
def expected_fragment(mid,h):
 z=MODELS[mid][3].subs(X,X-h)
 if mid=='q-126765':return (X-h)**2
 if mid=='q-355560':return (4-X-X**2).subs(X,X-h)
 if mid=='q-355576':return ((-s.exp(-2*X)+2*s.exp(2)+1)/2).subs(X,X-h)
 return z

def math_fingerprint(mid,h):
 rhs,x0,y0,_=MODELS[mid]
 return digest([s.srepr(s.simplify(rhs.subs(X,X-h))),s.srepr(s.sympify(x0)+h),s.srepr(s.sympify(y0)),'first rearrange then separate'])
def task(q):
 # Question identity for inventory: equation + initial data + fragment contract;
 # answer order and UUIDs do not participate.
 text=normalize_prose(q[':question/problem'])
 return digest(re.sub(r'\s+',' ',text).strip())

@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
 if difficulty not in SUPPORTED:raise ValueError('unsupported difficulty: '+difficulty)
 rng=random.Random(seed);choices=[m for m in MODELS if level(m)==difficulty]
 mid=template or rng.choice([m for m in choices if m not in UNGRADABLE])
 if mid not in choices:raise ValueError('template/level mismatch or excluded source')
 h=0 if replay else parameters['h'] if parameters is not None else rng.choice([z for z in SHIFTS if z])
 if type(h) is not int or h not in SHIFTS:raise ValueError('declared finite h domain required')
 allowed={'h','a','c','bank'} if mid=='q-104065' else {'h','b'} if mid=='q-128199' else {'h'}
 if parameters is not None and not set(parameters)<=allowed:raise ValueError('unknown parameter')
 original=QS[mid];prompt,sol=question_text(mid,h)
 f=original[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'];key=f[':answer-field/key']
 values=[normalize_tex(translate_math(a[':answer/value'],h)) for a in f[':answer-field/choices']]
 profile='observed-'+mid if kind.endswith('/radio') else 'blank-'+mid
 params={'h':h};correct_index=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 if mid=='q-104065' and not replay:
  # Whole profiles precede the winning role. Each role yields its ODE and IC.
  constants=tuple(s.sympify(v,locals={'pi':s.pi}) for v in ('-pi**2','-1','0','1','pi**2'))
  catalogs=[[(b,d),(b,d+s.pi**2/2),(b+2,d-s.pi**2/2),(b+2,d),(b+1,d-s.pi**2/4)] for b in (2,4,6) for d in constants]
  supplied=parameters or {};eligible={}
  for bank_id,bank in enumerate(catalogs):
   if 'bank' in supplied and supplied['bank']!=bank_id:continue
   roles=[i for i,(v,d) in enumerate(bank) if ('a' not in supplied or supplied['a']==v) and ('c' not in supplied or s.simplify(s.sympify(str(supplied['c']).replace('^','**'),locals={'pi':s.pi})-d)==0)]
   if roles:eligible[bank_id]=roles
  if not eligible:raise ValueError('invalid trig parameters or bank')
  bank_id=rng.choice(list(eligible));bank=list(catalogs[bank_id]);role=rng.choice(eligible[bank_id]);a,c=bank[role]
  u=X-h;y0=a*s.pi**2/4+c;z=s.log(s.sin(u))+a*u**2+c
  prompt=normalize_prose(f"Find the particular solution to $\\sin({tex(u)})\\frac{{\\mathrm{{d}}y}}{{\\mathrm{{d}}x}}-\\left({tex(2*a*u)}\\right)\\sin({tex(u)})=\\cos({tex(u)})$ that satisfies $y({tex(h+s.pi/2)})={tex(y0)}$. Assume that ${h}<x<{tex(h+s.pi)}$.")
  sol=normalize_prose(f"We first rearrange and separate, then integrate and apply the initial condition.\n\n$$y'=\\frac{{\\cos({tex(u)})}}{{\\sin({tex(u)})}}+{tex(2*a*u)}.$$\n\nUse $v=\\sin({tex(u)})$, so $\\mathrm{{d}}v=\\cos({tex(u)})\\mathrm{{d}}x$. On the given interval, sine is positive. Thus\n\n$$\\int\\mathrm{{d}}y=\\int\\frac{{\\mathrm{{d}}v}}{{v}}+\\int \\left({tex(2*a*u)}\\right)\\mathrm{{d}}x.$$\n\n$$y=\\ln(\\sin({tex(u)}))+{tex(a*u**2)}+C.$$\n\nAt $x={tex(h+s.pi/2)}$, $\\sin({tex(u)})=1$ and hence\n\n$${tex(y0)}={tex(a*s.pi**2/4)}+C,\\qquad C={tex(c)}.$$\n\nTherefore $y={tex(z)}$.")
  # A separate seeded permutation holds order fixed across winning-role controls.
  random.Random(seed).shuffle(bank);correct_index=bank.index((a,c))
  values=['y='+tex(s.log(s.sin(u))+v*u**2+d) for v,d in bank]
  params.update(a=a,c=str(c).replace('**','^'),bank=bank_id);profile='authored-role-complete-bank-v3-'+str(bank_id)
 if mid=='q-128199' and not replay:
  b=(parameters or {}).get('b',rng.choice((-2,-1,1,2)))
  if type(b) is not int or b not in (-2,-1,1,2):raise ValueError('invalid radical ordinate')
  u=X-h;z=s.sign(b)*s.sqrt(u**2+b**2)
  prompt=normalize_prose(f"Find the solution to the initial value problem\n\n$$y'=\\frac{{{tex(u)}}}{{y}},\\quad y({h})={b}.$$\n\n$y(x)=$ {{{{field-1}}}}")
  sol=normalize_prose(f"Separating variables and integrating gives $\\int y\\,\\mathrm{{d}}y=\\int \\left({tex(u)}\\right)\\,\\mathrm{{d}}x$, so $y^2={tex(u**2)}+K$.\n\nThe condition $y({h})={b}$ gives $K={b**2}$. Since the initial value is {'positive' if b>0 else 'negative'}, choose the {'positive' if b>0 else 'negative'} branch. Therefore $y={tex(z)}$.")
  values=[tex(z)];params['b']=b

 # Seed/choice order do not enter content identity. Whole mathematical task does.
 content=digest([mid,prompt,sorted(values),profile]);qid=uid('question:'+content);fid=uid('field:'+qid+key)
 answers=[{':answer/id':uid('answer:'+fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 cid=answers[correct_index][':answer/id']
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]}
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':mid,'bank_profile':profile,'parameters':params,'source_ids':[mid],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'eligible_for_learning':mid not in UNGRADABLE,'grading_exclusion':UNGRADABLE.get(mid),'math_fingerprint':digest([mid,prompt]),'domain':'connected real interval through translated initial point where the original ODE and solution are defined; positive branch when specified','plot_rating':'none','recipe':('whole role-complete coefficient/constant bank; ODE and IC from selected role' if mid=='q-104065' and not replay else 'signed branch from initial ordinate' if mid=='q-128199' and not replay else 'complete source bank under simultaneous x -> x-h; corrected source scaffolds'),'python_version':sys.version.split()[0],'sympy_version':s.__version__}}

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--shift',type=int);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--replay',action='store_true');a=p.parse_args()
 if a.count<1:raise ValueError('positive count required')
 candidates=[(m,h) for m in MODELS if level(m)==a.difficulty and (a.template is None or a.template==m) and (a.replay or m not in UNGRADABLE) for h in ([0] if a.replay else [a.shift] if a.shift is not None else [v for v in SHIFTS if v])]
 random.Random(a.seed).shuffle(candidates)
 if a.count>len(candidates):raise ValueError('finite variant limit: '+str(len(candidates)))
 records=[generate(a.difficulty,a.seed+i,m,{'h':h},a.replay) for i,(m,h) in enumerate(candidates[:a.count])]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186100894-source-policy.json'))

if __name__=='__main__':main()
