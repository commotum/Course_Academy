#!/usr/bin/env python3
"""Special-case chain rule: f(x,y), y=y(x), independent x.

Nine observed easy solution masks and raw five-choice banks; authored complete
method-derived normal banks. Scalar function coefficient a is a same-workload
variation, never claimed as a new template. Moderate coefficient bookkeeping and
hard product-rule dependencies are explicit missing-level designs. No graphics,
EDB access, registration, transactions, or shared edits. See private evidence.

Public API generate(level, seed=0, template=None, field_type=None,
parameters=None, profile=None); wrappers generate_easy/moderate/hard.
Raw profiles retain exact original wording, mathematical stages and bank strings
at a=1, including the radial source's missing positive-domain restriction. They
are evidence-only and must not be delivered as eligible learning questions.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186166748
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCE=CAPTURE['record']
KP_UUID=SOURCE[':knowledge-point/id'];TITLE=SOURCE[':knowledge-point/title']
VERSION='special-case-chain-rule-1'
X,Y=s.symbols('x y',real=True)
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
FAMILIES={'sine_power':'q-94588','x_log_sum':'q-95121','y_log_power':'q-170670','reciprocal_exp':'q-95088','radial_power':'q-95114','x_exp_sine':'q-95117','polynomial_sine':'q-95118','cosine_reciprocal':'q-95119','quotient_power':'q-95122'}
TEMPLATES={**{k:'easy' for k in FAMILIES},'weighted_polynomial_sine':'moderate','weighted_x_exp_sine':'moderate','polynomial_product_dependency':'hard','exponential_product_dependency':'hard'}
# Select a complete profile before sampling parameters. Never fill from a pool.
PROFILES={**{f'observed:{q}':{'template':t,'eligible':False,'origin':'observed opaque bank; explicit value-pattern scaling'} for t,q in FAMILIES.items()},**{f'operations:{t}':{'template':t,'eligible':True,'origin':'authored whole operation bank'} for t in TEMPLATES}}
FX=r'\frac{∂f}{∂x}';FY=r'\frac{∂f}{∂y}';YD=r'\frac{\text{d}y}{\text{d}x}';D=r'\frac{\text{d}f}{\text{d}x}'
OPENING='The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:'
PARTIAL='First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ '
SUBSTITUTE='Writing the above results in terms of $x,$ we get'
DEPENDENCY='Next, we take the derivative $y$ with respect to $x,$ and we get'
FINAL='Finally, putting the derivatives into the multivariable chain rule, we get'
class SampleRejected(ValueError):pass

def tex(v):return s.latex(v).replace(r'\log',r'\ln')
def grouped(v):return r'\left('+v+r'\right)'
def scale(v,a):return v if a==1 else str(a)+r'\cdot '+grouped(v)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+str(v)))
def equal(a,b):
 d=s.cancel(s.expand(a-b))
 if d==0:return True
 # An exact nonzero value at a valid positive point proves nonidentity. This
 # short circuit avoids expensive trig rewrites; no float tolerance is used.
 for point in (1,2,3):
  if d.subs(X,point).is_zero is False:return False
 return s.simplify(d)==0

def base(t):
 """Exact source function/dependency, independent of the TeX renderer."""
 return {'sine_power':(s.sin(X**2+Y),X**2),'x_log_sum':(X*s.log(X+Y),X**2),'y_log_power':(Y*s.log(X**2+1),X**2+1),'reciprocal_exp':(1/(X+Y),s.exp(-X)),'radial_power':(s.sqrt(X**2+Y**2),X**3),'x_exp_sine':(X*s.exp(Y),s.sin(X)),'polynomial_sine':(X**2+X*Y,s.sin(X)),'cosine_reciprocal':(s.cos(X**2+Y),1/X),'quotient_power':(Y/(X+1),X**3)}[t]

def validate_parameters(t,p):
 if t in FAMILIES:
  if set(p)!={'a'} or type(p['a']) is not int or not 1<=abs(p['a'])<=5:raise ValueError('Easy: only integer nonzero scalar a, |a|<=5')
 else:
  if set(p)!={'a','b','c','k'} or any(type(v)is not int for v in p.values()):raise ValueError('Require integer a,b,c,k')
  if not all(1<=abs(p[v])<=4 for v in ('a','b','c')) or not 2<=p['k']<=4:raise ValueError('Authored levels: nonzero |a,b,c|<=4 and frequency k=2..4')
 return p

def sampled(t,r):
 signed=(-4,-3,-2,-1,1,2,3,4)
 return {'a':r.choice((*signed,-5,5))} if t in FAMILIES else {**{v:r.choice(signed) for v in ('a','b','c')},'k':r.randint(2,4)}

def scale_solution(text,a):
 """Scale complete expression nodes, keeping every source arithmetic row.

 All four $$ blocks after the formal rule are retained. Only complete RHS math
 expressions are slots; commas/periods, derivative labels and prose are fixed.
 The y-derivative block is intentionally unscaled.
 """
 n=0
 def block(m):
  nonlocal n
  n+=1
  if n in (1,4) or a==1:return m[0]
  b=m[1]
  def expression_slot(mm):
   prefix=mm[1];v=mm[2];suffix=mm[3]
   if v.strip() in (FX,FY):return mm[0]
   return prefix+scale(v,a)+suffix
  # A complete RHS terminates at equality, row, partial separator or end.
  b=re.sub(r'(=)(.*?)(?=(?:=|\\\\|\\,|\\end\{aligned\}))',lambda mm: expression_slot((None,mm[1],mm[2].rstrip(' ,. '),mm[2][len(mm[2].rstrip(' ,. ')):])),b,flags=re.S)
  return '$$'+b+'$$'
 return re.sub(r'\$\$(.*?)\$\$',block,text,flags=re.S)

def source_render(t,p,raw):
 q=SOURCES[FAMILIES[t]];a=p['a'];f,h=base(t);f=a*f
 prompt=q[':question/problem']
 if a!=1:
  prompt=re.sub(r'(f\(x,y\)=)(.*?)(\$)',lambda m:m[1]+scale(m[2],a)+m[3],prompt,count=1)
 if t=='radial_power' and not raw:prompt+=' Assume $x>0.$'
 solution=scale_solution(q[':question/worked-solution'],a)
 # Normal solutions use the EXACT observed teaching chains, with domain repair
 # in the prompt. Raw evidence does not erase that unsupported source branch.
 return f,h,prompt,solution

def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def mul(a,b):return grouped(tex(a))+r'\cdot '+grouped(tex(b))

def authored_render(t,p):
 a,b,c,k=(p[v] for v in ('a','b','c','k'))
 trig=s.cos if 'exponential' in t else s.sin
 product='product_dependency' in t
 h=c*X*trig(k*X) if product else c*s.sin(k*X)
 f=a*X*s.exp(b*Y) if 'exp' in t else a*X**2+b*X*Y
 A=s.diff(f,X);B=s.diff(f,Y);C=s.diff(h,X)
 aa=A.subs(Y,h);bb=B.subs(Y,h)
 prompt=f'If $f(x,y)={tex(f)}$ and $y={tex(h)},$ compute ${D}.$'
 partials=block([FX+'='+tex(A)+r',\,'+FY+'='+tex(B)])
 substitution=block([FX+' & ='+tex(aa)+',',FY+' & ='+tex(bb)+'.'])
 dependency_rows=[]
 if product:
  # Independently differentiated factors before the dependency product rule.
  dep=f'{c}x';arg=f'{k}x'
  dependency_rows=[r'\frac{\text{d}}{\text{d}x}('+dep+') & ='+str(c)+',',r'\frac{\text{d}}{\text{d}x}('+tex(trig(k*X))+') & ='+tex(s.diff(trig(k*X),X))+',',YD+' & ='+str(c)+r'\cdot '+grouped(tex(trig(k*X)))+'+'+grouped(dep)+r'\cdot '+grouped(tex(s.diff(trig(k*X),X))), ' & ='+tex(C)+'.']
 else:dependency_rows=[YD+' & ='+tex(C)+'.']
 # Full substitution, product, expansion and collection. The exponential mask
 # retains factoring; the polynomial mask retains distributed terms separately.
 first=tex(aa)+'+'+mul(bb,C)
 expanded=s.expand(aa+bb*C)
 last=s.factor(aa+bb*C)
 rows=[D+' & ='+first,' & ='+tex(expanded)]
 if tex(last)!=tex(expanded):rows.append(' & ='+tex(last))
 rows[-1]+='.'
 sol='\n\n'.join([OPENING,'$$\n'+D+'='+FX+'+'+FY+r'\cdot '+YD+'\n$$',PARTIAL,partials,SUBSTITUTE,substitution,DEPENDENCY,block(dependency_rows),FINAL,block(rows)])
 return f,h,prompt,sol

def operation_bank(f,h,t):
 """Five complete expressions from real substitution/chain operations.

 Correct; omit y-chain; reverse y-chain sign; omit y'; substitute y for y'.
 A repeated component is not patched: reject the whole bank.
 """
 A=s.diff(f,X).subs(Y,h);B=s.diff(f,Y).subs(Y,h);C=s.diff(h,X)
 vals=[A+B*C,A,A-B*C,A+B,B*C] if t=='reciprocal_exp' else [A+B*C,A,A-B*C,A+B,A+B*h]
 if t=='radial_power':
  xp=s.Symbol('x',positive=True)
  vals=[s.simplify(v.subs(X,xp)).subs(xp,X) for v in vals]
 for i,a in enumerate(vals):
  if any(equal(a,b) for b in vals[:i]):raise SampleRejected('Ambiguous complete bank')
 return [tex(v) for v in vals],['correct','omit_y_chain','reverse_y_chain','omit_dependency_derivative','omit_x_partial' if t=='reciprocal_exp' else 'substitute_y_for_y_prime']

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio response type supported')
 r=random.Random(seed)
 if profile is not None:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  pt=PROFILES[profile]['template']
  if template is not None and template!=pt:raise ValueError('Profile/template mismatch')
  template=pt
 if template is None:template=r.choice([t for t,d in TEMPLATES.items() if d==level])
 if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template/level mismatch')
 profile=profile or 'operations:'+template
 raw=profile.startswith('observed:')
 for attempt in range(1000):
  p=validate_parameters(template,dict(parameters) if parameters is not None else sampled(template,r))
  f,h,prompt,sol=source_render(template,p,raw) if template in FAMILIES else authored_render(template,p)
  try:
   if raw:
    q0=SOURCES[FAMILIES[template]];field0=q0[':question/answer-fields'][0]
    values=[scale(a[':answer/value'],p['a']) for a in field0[':answer-field/choices']]
    correct=next(i for i,a in enumerate(field0[':answer-field/choices']) if a[':answer/id']==field0[':answer-field/correct'][':answer/id'])
    recipes=['observed_expression_pattern; original error operation opaque']*5
   else:values,recipes=operation_bank(f,h,template);correct=0
   break
  except SampleRejected:
   if parameters is not None:raise
 else:raise SampleRejected('No eligible complete bank')
 domain='x>0' if template=='radial_power' else ('x+x^2>0' if template=='x_log_sum' else 'x!=0' if template=='cosine_reciprocal' else 'x!=-1' if template=='quotient_power' else 'x+exp(-x)!=0' if template=='reciprocal_exp' else 'real x')
 identity=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':sol,'bank':sorted(values),'domain':domain})
 question_id=uid(identity);field_id=uid(question_id+':selection')
 choices=[{':answer/id':uid(field_id+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct_id=choices[correct][':answer/id'];r.shuffle(choices)
 q={':question/id':question_id,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
 # Canonical functions, dependency and workload; bank aliases do not affect task.
 fingerprint=digest([s.srepr(s.simplify(f.subs(Y,h))),domain,level])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'level':level,'seed':seed,'parameters':p,'bank_profile':profile,'profile_origin':PROFILES[profile]['origin'],'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'source_ids':[FAMILIES[template]] if template in FAMILIES else [],'source_database':CAPTURE['database'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'domain':domain,'raw_source_domain_error':raw and template=='radial_power','operation_recipes':recipes,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plot_rating':'none'}}

# EASY: observed nine families; nonzero signed whole-function scale |a|<=5.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (AUTHORED): independent coefficients in f and a simple nonunit-frequency
# sine dependency. Same two-term special rule; no product in y'(x).
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (AUTHORED): y=c*x*sin(k*x) or c*x*cos(k*x); y' requires exactly one
# product rule and both resulting terms enter the unchanged special-case rule.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return '\n\n'.join([q[':question/problem'],*[('- '+a[':answer/value']+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '')) for a in f[':answer-field/choices']],q[':question/worked-solution']])
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
 records=[generate(d,a.seed+i,template=a.template,profile=a.profile) for d in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
