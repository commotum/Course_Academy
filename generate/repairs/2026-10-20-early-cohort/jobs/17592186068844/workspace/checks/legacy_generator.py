#!/usr/bin/env python3
"""Implicit separable general solutions; basis 1356, no database writes.

Eleven observed easy radio templates and complete source banks. Source recipes
are coordinate translations of entire mathematical components, preserving the
original ordered rows and fixed prose. They are not a source-record lookup:
all parameters pass through the same masked builder and domain guards. Observed
error intentions are uncertain; 'observed' is a public evidence bank, while the
normal 'standard' bank uses documented integration errors. Moderate/hard are
bounded authored polynomial instances at the same separation/integration step.
No explicit inversion, initial conditions, integrating factors, or plots.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068844
KP_UUID='a67b149c-f701-5be0-868d-c2f4a4be4be4'
TITLE='Finding a General Solution in Implicit Form'
VERSION='implicit-separable-1'
HERE=Path(__file__).resolve().parent.parent/'17592186068844'
SOURCE=json.loads((HERE/'source.json').read_text())
X,Y=sp.symbols('x y',real=True)
C=sp.Symbol('C',real=True)
D=r'\frac{\text{d}y}{\text{d}x}'
DC=r'\frac{\text{d}y}{\cancel{\text{d}x}}'
TEMPLATES={
 'exp_linear':('easy','q-154359'), 'arcsin_autonomous':('easy','q-154367'),
 'tan_exp':('easy','q-118885'), 'log_exp':('easy','q-14246'),
 'tan_autonomous':('easy','q-154357'), 'power_cube':('easy','q-154361'),
 'exp_affine':('easy','q-154369'), 'root_power':('easy','q-154373'),
 'sin_poly':('easy','q-158035'), 'sec_log':('easy','q-158116'),
 'log_sin':('easy','q-158117'), 'two_x_terms':('moderate',None),
 'two_sided_terms':('hard',None)}
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}


def coordinate(v,n):
 if n==0:return v
 return r'\left('+v+('+' if n>0 else '-')+str(abs(n))+r'\right)'

def mask_math(s):
 """Tokenize complete TeX math components once; protect commands/differentials.

 Only mathematical x/y variable tokens are slots. Text, commands and differential
 variable labels (including cancelled labels) cannot become translation slots.
 """
 s=s.replace('respect to $x:$','respect to @INTVAR@')
 pieces=re.split(r'(\$\$[\s\S]*?\$\$|\$[^$]*?\$)',s)
 for i in range(1,len(pieces),2):
  t=pieces[i];protected=[]
  def keep(m):protected.append(m[0]);return '@P'+str(len(protected)-1)+'@'
  t=re.sub(r'\\(?:text|textrm|mathrm)\{d\}[xy]',keep,t)
  t=re.sub(r'\\[A-Za-z]+',keep,t)
  # ASCII variables inside powers/products, but never function-command letters.
  t=re.sub(r'(?<![A-Za-z])([xy])(?![A-Za-z])',lambda m:'@'+m[1].upper()+'@',t)
  for j,v in enumerate(protected):t=t.replace('@P'+str(j)+'@',v)
  pieces[i]=t
 return ''.join(pieces).replace('@INTVAR@','$x:$')

MASKS={name:{'prompt':mask_math(QS[sid][':question/problem']),
             'solution':mask_math(QS[sid][':question/worked-solution']),
             'bank':[mask_math('$'+a[':answer/value']+'$')[1:-1] for a in QS[sid][':question/answer-fields'][0][':answer-field/choices']]}
       for name,(_,sid) in TEMPLATES.items() if sid}

def render(mask,p):return mask.replace('@X@',coordinate('x',p['h'])).replace('@Y@',coordinate('y',p['k']))
def tex(a):
 t=sp.latex(a).replace(r'\log',r'\ln').replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan')
 return t

def primitive_log(a):return sp.log(sp.Abs(a))

def data(t,p):
 """ODE, reciprocal y factor, x factor, and normalized implicit relation."""
 u=X+p.get('h',0);v=Y+p.get('k',0)
 if t=='exp_linear':A,B,L,R=sp.exp(v),2*u,sp.exp(v),u**2
 elif t=='arcsin_autonomous':A,B,L,R=1/sp.sqrt(1-v**2),sp.Integer(1),sp.asin(v),u
 elif t=='tan_exp':A,B,L,R=sp.sec(v)**2,sp.exp(u),sp.tan(v),sp.exp(u)
 elif t=='log_exp':A,B,L,R=1/v,sp.exp(u),primitive_log(v),sp.exp(u)
 elif t=='tan_autonomous':A,B,L,R=sp.sec(v)**2,sp.Integer(1),sp.tan(v),u
 elif t=='power_cube':A,B,L,R=v**2,u**2,v**3,u**3
 elif t=='exp_affine':A,B,L,R=sp.exp(v),2*(u-1),sp.exp(v),u**2-2*u
 elif t=='root_power':A,B,L,R=sp.sqrt(v),sp.sqrt(u),v**sp.Rational(3,2),u**sp.Rational(3,2)
 elif t=='sin_poly':A,B,L,R=sp.cos(v),3*u**2,sp.sin(v),u**3
 elif t=='sec_log':A,B,L,R=sp.sec(v)*sp.tan(v),1/u,sp.sec(v),primitive_log(u)
 elif t=='log_sin':A,B,L,R=1/v,sp.sin(u),primitive_log(v),-sp.cos(u)
 else:
  a,b=p['a'],p['b'];A=Y**2+(p['d'] if t=='two_sided_terms' else 0);B=a*X**2+b
  L=Y**3/3+(p['d']*Y if t=='two_sided_terms' else 0);R=a*X**3/3+b*X
 return sp.trigsimp(B/A),A,B,L,R

def domain(t,p):
 u='x'+('+'+str(p['h']) if p.get('h',0)>0 else str(p['h']) if p.get('h',0)<0 else '')
 v='y'+('+'+str(p['k']) if p.get('k',0)>0 else str(p['k']) if p.get('k',0)<0 else '')
 return {'exp_linear':'all real x,y; right side plus C>0',
 'arcsin_autonomous':'|'+v+'|<1; arcsin('+v+') principal branch',
 'tan_exp':'0<'+v+'<pi/2', 'log_exp':v+'≠0; each sign branch separately',
 'tan_autonomous':'-pi/2<'+v+'<pi/2', 'power_cube':v+'≠0',
 'exp_affine':'all real x,y; right side plus C>0', 'root_power':u+'≥0, '+v+'>0',
 'sin_poly':'cos('+v+')≠0; each connected branch separately',
 'sec_log':u+'≠0; -pi/2<'+v+'<pi/2; '+v+'≠0',
 'log_sin':v+'≠0; each sign branch separately','two_x_terms':'y≠0',
 'two_sided_terms':'all real x,y; y²+d>0'}[t]

def check_parameters(t,p):
 if t in ('two_x_terms','two_sided_terms'):
  keys={'a','b'}|({'d'} if t=='two_sided_terms' else set())
  if set(p)!=keys or any(type(v)!=int for v in p.values()):raise ValueError('exact integer polynomial parameters required')
  if not 2<=p['a']<=6 or not 1<=abs(p['b'])<=5:raise ValueError('a=2..6, nonzero b=-5..5 required')
  if t=='two_sided_terms' and not 1<=p['d']<=5:raise ValueError('d=1..5 required')
 else:
  if set(p)!={'h','k'} or any(type(v)!=int or abs(v)>6 for v in p.values()):raise ValueError('h,k integer translations -6..6 required')
  if t in ('arcsin_autonomous','tan_autonomous') and p['h']!=0:raise ValueError('autonomous h must be zero; unused constant shift is incidental')

def logdiff(e,v):
 return sp.diff(e.replace(lambda z:z.func==sp.log and z.args[0].func==sp.Abs,lambda z:sp.log(z.args[0].args[0])),v)

def equivalent(a,b):
 """Complete relations F=C equivalent modulo nonzero constant scale/shift."""
 ax,ay=logdiff(a,X),logdiff(a,Y);bx,by=logdiff(b,X),logdiff(b,Y)
 if bx==0 and by==0:return False
 ratio=sp.simplify((ax/bx) if bx!=0 else (ay/by))
 return ratio!=0 and not ratio.free_symbols and sp.simplify(ax-ratio*bx)==0 and sp.trigsimp(ay-ratio*by)==0

def standard_bank(t,p):
 """Complete operation bank, chosen by family before constructing instances."""
 rhs,A,B,L,R=data(t,p);v=Y+p.get('k',0)
 if t in ('exp_linear','exp_affine'):wrongL=sp.exp(2*v)/2;wrongR=B
 elif t in ('tan_exp','tan_autonomous'):wrongL=v;wrongR=sp.sec(v)**2
 elif t in ('arcsin_autonomous',):wrongL=sp.sin(v);wrongR=sp.atan(v)
 elif t in ('log_exp',):wrongL=v;wrongR=sp.exp(v)
 elif t=='sec_log':wrongL=sp.tan(v);wrongR=sp.sec(v)**2
 elif t=='sin_poly':wrongL=v;wrongR=sp.tan(v)
 else:wrongL=A;wrongR=B
 # Uniform first three; last two are explicit per-family integration operations.
 pairs=[(L,R),(L,-R),(L,2*R),(wrongL,R),
        (L,wrongR) if t in ('exp_linear','exp_affine','power_cube','root_power','log_sin','two_x_terms','two_sided_terms') else (wrongR,R)]
 labels=['correct','right primitive sign reversed','spurious factor two on right primitive',
         'wrong left primitive','wrong primitive on right' if pairs[-1][0]==L else 'wrong left primitive function']
 if t=='two_sided_terms':
  pairs[3]=(Y**3/3,R);pairs[4]=(L,p['a']*X**3/3);labels[3:]=['omit linear y primitive','omit linear x primitive']
 elif t=='two_x_terms':pairs[3]=(Y**2,R);pairs[4]=(L,p['a']*X**3/3);labels[3:]=['omit power increment on left','omit linear x primitive']
 values=[tex(l)+'='+tex(r)+'+C' for l,r in pairs]
 for i,(l,r) in enumerate(pairs):
  for ll,rr in pairs[i+1:]:
   if equivalent(l-r,ll-rr):raise ValueError('whole bank rejected: equivalent relations')
 return values,labels

def authored_build(t,p):
 _,A,B,L,R=data(t,p);at,bt,lt,rt=map(tex,(A,B,L,R))
 dx=r'\,\text{d}x';dy=r'\,\text{d}y'
 rhs=r'\frac{'+bt+'}{'+at+'}'
 prompt='Find the general solution to the differential equation (in implicit form) $'+D+'='+rhs+'.$'
 if t=='two_x_terms':prompt+=' Work on an interval where $y\\ne 0.$'
 sep=D+' & ='+rhs+r' \\ ('+at+r')\,'+D+' & ='+bt
 # Keep formal operator, cancellation, substitution, component primitives, then collection.
 left=r'\frac{y^3}{3}'+(('+'+str(p['d'])+'y') if t=='two_sided_terms' else '')
 right=r'\frac{'+str(p['a'])+r'x^3}{3}'+('+' if p['b']>0 else '-')+str(abs(p['b']))+'x+C'
 component_left=r'\int y^2'+dy+(('+'+r'\int '+str(p['d'])+dy) if t=='two_sided_terms' else '')
 component_right=r'\int '+str(p['a'])+'x^2'+dx+('+' if p['b']>0 else '-')+r'\int '+str(abs(p['b']))+dx
 rows=[r'\int ('+at+r')\,'+D+dx+' & ='+r'\int ('+bt+')'+dx,
       r'\int ('+at+r')\,'+DC+r'\,\cancel{\text{d}x}'+' & ='+r'\int ('+bt+')'+dx,
       r'\int ('+at+')'+dy+' & ='+r'\int ('+bt+')'+dx,
       component_left+' & ='+component_right,
       left+' & ='+right]
 solution='To find the general solution, we first separate the variables: \n\n$$\n\\begin{aligned}'+sep+'\\end{aligned}\n$$\n\nThen, we integrate both sides with respect to $x:$\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$\n\nTherefore, the general solution to the differential equation (in implicit form) is\n\n$$\n'+lt+'='+rt+'+C.\n$$'
 return prompt,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed);eligible=[t for t,v in TEMPLATES.items() if v[0]==level];t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('template difficulty mismatch')
 profile=profile or 'standard'
 if profile not in ('standard','observed'):raise ValueError('unknown profile')
 if profile=='observed' and not TEMPLATES[t][1]:raise ValueError('no observed bank at authored level')
 if parameters is None:
  if level=='easy':p={'h':0 if t in ('arcsin_autonomous','tan_autonomous') else rng.randint(-6,6),'k':rng.randint(-6,6)}
  else:p={'a':rng.randint(2,6),'b':rng.choice([i for i in range(-5,6) if i])};p.update({'d':rng.randint(1,5)} if level=='hard' else {})
 else:p=dict(parameters)
 check_parameters(t,p)
 if level=='easy':
  prompt=render(MASKS[t]['prompt'],p);solution=render(MASKS[t]['solution'],p)
  if profile=='observed':
   bank=[render(v,p) for v in MASKS[t]['bank']]
   q=QS[TEMPLATES[t][1]];original=q[':question/answer-fields'][0];correct=next(i for i,a in enumerate(original[':answer-field/choices']) if a[':answer/id']==original[':answer-field/correct'][':answer/id']);recipes=['observed component translation; intention not recovered']*5
  else:
   prompt=prompt.replace('to the differential equation','to the differential equation (in implicit form)',1)
   if t=='sec_log':prompt+=' Also require $'+coordinate('y',p['k'])+r'\ne 0.$'
   bank,recipes=standard_bank(t,p);correct=0
 else:
  prompt,solution=authored_build(t,p);bank,recipes=standard_bank(t,p);correct=0
 rhs,A,B,L,R=data(t,p)
 fp=hashlib.sha256(json.dumps([sp.srepr(rhs),domain(t,p)],sort_keys=True).encode()).hexdigest()
 identity=hashlib.sha256(json.dumps([VERSION,prompt,solution,sorted(bank)],ensure_ascii=False).encode()).hexdigest()
 uid=lambda tag:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+'/'+identity+'/'+tag))
 answers=[{':answer/id':uid('answer/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 ci=answers[correct][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',ci]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,'origin':'observed-template' if level=='easy' else 'authored-missing-'+level,'recipes':recipes,'domain':domain(t,p),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[TEMPLATES[t][1]] if level=='easy' else [],'mathematical_fingerprint':fp,'content_fingerprint':identity,'plot_rating':'none'}}

# EASY: observed separation followed by standard one-component primitives.
# Coordinate translations -6..6 preserve every observed math-stage workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): two x primitives and one y primitive, no inversion.
# a=2..6, |b|=1..5; all terms required and coefficients bounded explicitly.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): two primitives on each side; positive d=1..5 keeps denominator
# nonzero. Same formal separation/integration, no sibling method expansion.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
