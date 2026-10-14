#!/usr/bin/env python3
"""Matched-derivative power substitution. Draft only; stops at generation step 7.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard have the same optional arguments.
Each complete bank is chosen before parameters. Explicit inputs never resample.
Observed opaque banks are public evidence-only profiles; defaults choose method-
derived authored banks. Source solutions retain their complete prose and ordered
stages. Coefficient/power/shift extensions preserve each level's workload.
No files or databases are written by generation. See private extraction evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068722
KP_UUID='b89c50f3-2181-5b61-96cb-386ef88d2035'
TITLE='Integrating an Expression Involving a Power Function Multiplied by Its Derivative'
VERSION='matched-power-1'
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X=sp.Symbol('x',real=True)
U=sp.Symbol('u',positive=True)
TEMPLATES={'polynomial_calculate':'easy','polynomial_equals':'easy','root_dot':'moderate','root_product':'moderate','reciprocal_root':'hard'}
PROFILES={
 'historical_2189':('polynomial_calculate','evidence-only expression-pattern replay; original intention unresolved'),
 'observed_2195':('polynomial_equals','observed retain derivative/sign/no-increment operations'),
 'observed_113581':('root_dot','observed power/derivative/reciprocal-factor operations; intent inferred'),
 'historical_2390':('root_product','evidence-only expression-pattern replay; compound exponent/factor intention unresolved'),
 'observed_72382':('reciprocal_root','observed reciprocal/power/retained-x operations'),
 'authored_polynomial_calculate':('polynomial_calculate','authored method-derived complete bank'),
 'authored_polynomial_equals':('polynomial_equals','authored method-derived complete bank'),
 'authored_root_dot':('root_dot','authored method-derived complete bank'),
 'authored_root_product':('root_product','authored method-derived complete bank'),
 'authored_reciprocal_root':('reciprocal_root','authored method-derived complete bank')}
SOURCE_IDS={'historical_2189':'q-2189','observed_2195':'q-2195','observed_113581':'q-113581','historical_2390':'q-2390','observed_72382':'q-72382'}
class SampleRejected(ValueError): pass

def power(t,k): return '{'+t+'}^{'+str(k)+'}'
def xp(k): return 'x' if k==1 else power('x',k)
def monomial(c,k): return ('' if c==1 else str(c))+xp(k)
def frac(a,b): return r'\frac{'+a+'}{'+b+'}'
def sqrt(t): return r'\sqrt{'+t+'}'
def fp(f,k): return '('+f+')^{'+str(k)+'}'
def rational(q): return str(q.p) if q.q==1 else frac(str(q.p),str(q.q))
def block(t): return '$$\n'+t+'\n$$'
def align(rows): return block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
def primitive(t): return t+'+C'
def hashof(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(kind,h): return str(uuid.uuid5(uuid.UUID(KP_UUID),kind+':'+h))

def guard(level,p):
 if set(p)!={'a','m','b','n'}: raise ValueError('Parameters require exactly a,m,b,n')
 if any(type(v)!=int for v in p.values()): raise ValueError('All parameters must be integers')
 a,m,b,n=(p[k] for k in ('a','m','b','n'))
 if not 1<=a<=5 or not 2<=m<=6 or not -6<=b<=6 or a*m>30: raise ValueError('Inner workload bounds: a=1..5, m=2..6, b=-6..6, am<=30')
 if level=='easy' and not 2<=n<=12: raise ValueError('Easy outer exponent n=2..12')
 if level!='easy' and n!=0: raise ValueError('Root families require n=0 (fixed square-root demand)')

def components(template,p):
 a,m,b,n=(p[k] for k in ('a','m','b','n'))
 term=monomial(a,m); f=(str(b)+'+'+term if template=='reciprocal_root' and b>0 else term+('+'+str(b) if b>=0 else str(b)))
 # Zero shift omits the inactive constant in both prompt and solution.
 if b==0:f=term
 d=monomial(a*m,m-1); F=a*X**m+b; D=sp.diff(F,X)
 q=sp.Integer(n) if TEMPLATES[template]=='easy' else sp.Rational(1,2) if TEMPLATES[template]=='moderate' else sp.Rational(-1,2)
 h=d+fp(f,n) if q.is_Integer else d+sqrt(f) if q>0 else frac(d,sqrt(f))
 I=r'\int '+h+r'\,\text{d}x'
 return f,d,F,D,q,I

def solution(template,p):
 f,d,F,D,q,I=components(template,p); n=p['n']; level=TEMPLATES[template]
 desc='parentheses' if level=='easy' else 'square root' if level=='moderate' else 'radical'
 text=f'We note that ${d}$ is the derivative of the quantity in the {desc}. So we make a substitution\n\n'+block('u='+f+'.')
 text+='\n\nIts derivative is given by\n\n'+align([frac(r'\text{d}u',r'\text{d}x')+' & ='+d+r'\,⟹\,\text{d}u='+d+r'\,\text{d}x,'])
 text+='\n\nand rewriting our integral, we get\n\n'
 if level=='easy':
  rows=[I+' & ='+r'\int '+fp(f,n)+r'\,'+d+r'\,\text{d}x',' & ='+r'\int '+power('u',n)+r'\,\text{d}u.']
 elif level=='moderate':
  sep=r'\cdot ' if template=='root_dot' else r'\,'
  rows=[I+' & ='+r'\int '+sqrt(f)+sep+d+r'\,\text{d}x',' & ='+r'\int '+sqrt('u')+r'\,\text{d}u',' & ='+r'\int '+power('u','1/2')+r'\,\text{d}u.']
 else:
  rows=[I+' & ='+r'\int '+frac('1',sqrt(f))+r'\,'+d+r'\,\text{d}x',' & ='+r'\int '+frac('1',sqrt('u'))+r'\,\text{d}u',' & ='+r'\int '+frac('1',power('u','1/2'))+r'\,\text{d}u',' & ='+r'\int '+power('u','-1/2')+r'\,\text{d}u.']
 text+=align(rows)+'\n\nWe can now solve the integral using the power rule:\n\n'
 if level=='easy':
  text+=block(r'\int '+power('u',n)+r'\,\text{d}u='+primitive(frac(power('u',n+1),str(n+1))))
  ans=frac(fp(f,n+1),str(n+1))
 elif level=='moderate':
  text+=align([r'\int '+power('u','1/2')+r'\,\text{d}u & ='+primitive(frac(power('u','3/2'),'('+frac('3','2')+')')),' & ='+primitive(frac('2'+power('u','3/2'),'3'))])
  ans=frac('2'+fp(f,'3/2'),'3')
 else:
  text+=align([r'\int '+power('u','-1/2')+r'\,\text{d}u & ='+primitive(frac(power('u','1/2'),'('+frac('1','2')+')')),' & ='+primitive('2'+power('u','1/2')),' & ='+primitive('2'+sqrt('u'))])
  ans='2'+sqrt(f)
 text+=f'\n\nLastly, we substitute $u={f}$ back in the expression. So the final result is\n\n'
 text+=align([I+' & ='+primitive(ans)+'.']) if level=='hard' else block(I+'='+primitive(ans)+'.')
 return text

def bank(template,p,profile):
 """Construct a complete ordered recipe bank; index 0 is mathematically correct.
 No source literal lookup and no first-valid pooling. Returned expressions omit C
 solely for derivative equality; rendered values include the source's +C.
 """
 f,d,F,D,q,I=components(template,p); n=p['n']; m=p['m']; a=p['a']; R=q+1
 correct=F**R/R
 ct=frac(fp(f,n+1),str(n+1)) if q.is_Integer else frac('2'+fp(f,'3/2'),'3') if q>0 else '2'+sqrt(f)
 values=[(correct,ct,'power_rule')]
 def add(e,t,label): values.append((e,t,label))
 if profile=='historical_2189':
  add(F**(n+1)/((n+1)*X),frac(fp(f,n+1),str(n+1)+'x'),'divide_primitive_by_x')
  add(F**n/n,frac(fp(f,n),str(n)),'omit_exponent_increment')
  add(D*F**(n+1)/(m-1),frac(d+fp(f,n+1),str(m-1)),'historical_derivative_retained_denominator_m_minus_one')
  add(a*m*X**(m-2)*F**(n+1)/(m-1),frac(monomial(a*m,m-2)+fp(f,n+1),str(m-1)),'historical_lower_multiplier_power_denominator_m_minus_one')
 elif profile=='observed_2195':
  add(D*correct,frac(d+fp(f,n+1),str(n+1)),'retain_derivative')
  add(-D*correct,'-'+frac(d+fp(f,n+1),str(n+1)),'retain_derivative_and_reverse_sign')
  add(-D*F**n/n,'-'+frac(d+fp(f,n),str(n)),'retain_derivative_reverse_sign_omit_increment')
  add(F**n/n,frac(fp(f,n),str(n)),'omit_exponent_increment')
 elif profile=='observed_113581':
  add(q*F**R,frac(fp(f,'3/2'),'2'),'divide_by_reciprocal_of_original_exponent')
  add(-q*F**(q-1),'-'+frac('1','2'+sqrt(f)),'differentiate_power_and_reverse_sign')
  add(-F**(q-1)/q,'-'+frac('2',sqrt(f)),'derivative_exponent_reciprocal_coefficient_reverse_sign')
  add(R*F**R,frac('3'+fp(f,'3/2'),'2'),'multiply_by_successor')
 elif profile=='historical_2390':
  add(-R*F**R,'-'+frac('3'+fp(f,'3/2'),'2'),'reverse_sign_multiply_by_successor')
  add(-correct,'-'+ct,'reverse_sign')
  add((1/q+1)*F**(1/R),'3'+fp(f,'2/3'),'historical_reciprocal_successor_coefficient_reciprocal_exponent_plus_one')
  add(R*F**(1/R),frac('3'+fp(f,'2/3'),'2'),'reciprocal_successor_multiply_by_successor')
 elif profile=='observed_72382':
  add(2*F**sp.Rational(3,2),'2'+sqrt(fp(f,3)),'use_positive_integrand_power_successor')
  add(F**R*R,frac(sqrt(f),'2'),'multiply_by_successor')
  add(2*X*F**R,'2x'+sqrt(f),'retain_x')
  add(F**sp.Rational(3,2)/2,frac(sqrt(fp(f,3)),'2'),'positive_integrand_power_and_multiply_by_half')
 elif q.is_Integer:
  add(F**n/n,frac(fp(f,n),str(n)),'omit_exponent_increment')
  add(F**R*R,str(R)+fp(f,n+1),'multiply_by_successor')
  add(D*correct,frac(d+fp(f,n+1),str(n+1)),'retain_derivative')
  add(-correct,'-'+ct,'reverse_sign')
 elif q>0:
  add(F**R*R,frac('3'+fp(f,'3/2'),'2'),'multiply_by_successor')
  add(F**q/q,'2'+sqrt(f),'omit_exponent_increment')
  add(D*correct,frac('2'+d+fp(f,'3/2'),'3'),'retain_derivative')
  add(-correct,'-'+ct,'reverse_sign')
 else:
  add(F**R*R,frac(sqrt(f),'2'),'multiply_by_successor')
  add(F**sp.Rational(3,2)/sp.Rational(3,2),frac('2'+fp(f,'3/2'),'3'),'drop_reciprocal_sign_before_power_rule')
  add(D*correct,'2'+d+sqrt(f),'retain_derivative')
  add(-correct,'-'+ct,'reverse_sign')
 # Group adjacent numeric factors visibly. 2*d cannot be written 212x^5.
 if profile.startswith('authored_') and not q.is_Integer:
  e,t,label=values[3]; values[3]=(e,frac('2'+r'\cdot '+d+fp(f,'3/2'),'3') if q>0 else '2'+r'\cdot '+d+sqrt(f),label)
 return [(e,primitive(t),label) for e,t,label in values]

def make(level,seed,template,p,profile):
 guard(level,p)
 f,d,F,D,q,I=components(template,p); entries=bank(template,p,profile)
 derivatives=[sp.diff(e,X) for e,t,l in entries]
 for i in range(5):
  for j in range(i):
   if sp.simplify(derivatives[i]-derivatives[j])==0: raise SampleRejected('Complete bank collision modulo integration constant')
 if sp.simplify(derivatives[0]-D*F**q)!=0: raise AssertionError('Incorrect primitive')
 problem=('$'+I+'=$') if template=='polynomial_equals' else ('Calculate $'+I+'.$')
 sol=solution(template,p); texts=[v for e,v,l in entries]
 identity=hashof({'version':VERSION,'level':level,'problem':problem,'solution':sol,'bank':sorted(texts)})
 fid=uid('field',identity); qid=uid('question',identity)
 choices=[{':answer/id':uid('answer',fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in texts]
 correct=choices[0][':answer/id']; random.Random(seed).shuffle(choices)
 evidence=profile.startswith('historical_')
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile][1],'source':SOURCE,'source_question_ids':[SOURCE_IDS[profile]] if profile in SOURCE_IDS else [],'eligible_for_learning':not evidence,'evidence_only':evidence,'plot_rating':'none','parameter_fingerprint':hashof({'level':level,'integrand':sp.srepr(D*F**q),'domain':'real' if level=='easy' else 'inner>0'}),'content_fingerprint':identity,'domain':'real x' if level=='easy' else f'{f}>0; each connected open interval','recipes':[l for e,t,l in entries],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Supported levels easy/moderate/hard, field radio')
 rng=random.Random(seed)
 if profile is not None:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  t=PROFILES[profile][0]
  if template not in (None,t):raise ValueError('Profile/template mismatch')
  template=t
 eligible=[t for t,l in TEMPLATES.items() if l==level]
 if template is not None and template not in eligible:raise ValueError('Level/template mismatch')
 # Fixed explicit parameters without a template choose the first family, independent
 # of option shuffle seed. Default sampling serves both observed family layouts.
 template=template or (eligible[0] if parameters is not None else rng.choice(eligible))
 profile=profile or 'authored_'+template
 for _ in range(100):
  p=dict(parameters) if parameters is not None else {'a':rng.randint(1,5),'m':rng.randint(2,6),'b':rng.randint(-6,6),'n':rng.randint(2,12) if level=='easy' else 0}
  try:return make(level,seed,template,p,profile)
  except SampleRejected:
   if parameters is not None:raise
 raise SampleRejected('Bounded sampler exhausted')

# EASY: matched polynomial power, substitution then integer successor/divisor.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: same matched derivative, square root -> u^(1/2) -> successor/divisor.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: reciprocal root -> reciprocal fractional power -> negative power, then rule.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=list(dict.fromkeys(TEMPLATES.values())) if args.difficulty=='all' else [args.difficulty]
 try:records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 except ValueError as exc:ap.error(str(exc))
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
