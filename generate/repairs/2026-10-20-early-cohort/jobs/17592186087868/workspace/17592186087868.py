#!/usr/bin/env python3
"""Seeded homogeneous/inhomogeneous ODE recognition with source checkbox replay.

Current source contract and role variation are implemented below the retained
legacy equation and source-mask helpers. Only easy/moderate are supported.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186087868
KP_UUID='739a8f10-413a-5a1d-a47e-4afd0b14eb44'
TITLE='Identifying Homogeneous and Inhomogeneous ODEs'
VERSION='homogeneous-recognition-1'
HOME=Path(__file__).with_suffix('')
RECIPES=json.loads((HOME/'recipes.json').read_text())
D='{y}^{′}'
X,Y,V=sp.symbols('x y D',real=True)
SOURCE={'database': 'math', 'basis': 5242, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
PROFILES={prefix+key:{'template':key,'bank':r['bank'],'origin':'observed','evidence_only':prefix=='raw_'} for key,r in RECIPES.items() for prefix in ('raw_','observed_')}
# A complete eligible categorical bank is selected before hard parameters.
for pos,anchor in enumerate(('q-331605','q-331742','q-331744')):
 PROFILES['authored_hard_'+str(pos)]={'template':'collect_and_normalize','bank':RECIPES[anchor]['bank'],'origin':'authored','evidence_only':False,'nonzero_index':pos}
TEMPLATES={key:{'level':r['level'],'field_type':'radio','origin':'observed'} for key,r in RECIPES.items()}
TEMPLATES['collect_and_normalize']={'level':'hard','field_type':'radio','origin':'authored'}

def mono(a,n):
 if not a:return '0'
 base='' if n==0 else ('x' if n==1 else '{x}^{'+str(n)+'}')
 return ('-' if a<0 else '')+('' if abs(a)==1 and base else str(abs(a)))+base

def sy(b):return ('-' if b<0 else '')+('' if abs(b)==1 else str(abs(b)))+'y'
def add(left,right):return left+('+' if not right.startswith('-') else '')+right

def lhs(a,n):return add(D,sy(a) if n==0 else mono(a,n)+'y')
def eq(a,n,r):return lhs(a,n)+'='+(sy(r[0]) if r[0] else mono(r[1],r[2]))
def final(a,n,b):
 if n==0:
  v=a-b
  return add(D,sy(v)) if v else D
 if a>0:return D+'+('+add(mono(a,n),mono(-b,0))+')y'
 return D+'-('+add(mono(-a,n),mono(b,0))+')y'

def subset_label(indices):
 names=['I','II','III']; vals=[names[i] for i in indices]
 if len(vals)==3:return 'I, II, and III'
 if len(vals)==2:return ' and '.join(vals)+' only'
 if len(vals)==1:return vals[0]+' only'
 return 'None'

def render_mask(mask,slots):
 return re.sub(r'\{\{(\w+)\}\}',lambda m:slots[m[1]],mask)

def source_render(template,p):
 r=RECIPES[template];slots={}
 for i,row in enumerate(p['rhs']):
  e=eq(p['a'],p['n'],row)
  slots['eq'+str(i)]=e;slots['aligned_eq'+str(i)]=e.replace('=',' & =')
  if row[0]:
   slots['move'+str(i)]=add(lhs(p['a'],p['n']),sy(-row[0]))+' & =0'
   slots['collect'+str(i)]=final(p['a'],p['n'],row[0])+' & =0'
  slots['force'+str(i)]=mono(row[1],row[2])
 return render_mask(r['problem_mask'],slots),render_mask(r['solution_mask'],slots)

def hard_render(p):
 eqs=[];blocks=[]
 for i,(k,a,n,b,d,e,m) in enumerate(p['equations']):
  original=add(add(str(k)+D,mono(a,n)+'y'),mono(d,m))+'='+add(sy(b),mono(e,m))
  moved=add(add(add(str(k)+D,mono(a,n)+'y'),sy(-b)),mono(d,m))+'='+mono(e,m)
  coeff=add(mono(a,n),mono(-b,0));forcing=mono(e-d,m)
  collected=str(k)+D+'+('+coeff+')y='+forcing
  standard=D+r'+\frac{'+coeff+'}{'+str(k)+'}y='+('0' if d==e else r'\frac{'+forcing+'}{'+str(k)+'}')
  eqs.append(original)
  classification='homogeneous' if d==e else 'inhomogeneous'
  forcing_value='0' if d==e else r'\frac{'+forcing+'}{'+str(k)+'}'
  blocks.append('- '+['First','Next','Finally'][i]+', we consider the equation\n\n$$\n'+original+'.\n$$\n\nWe collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $'+str(k)+'$:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(row.replace('=',' & =') for row in (original,moved,collected,standard))+r'.\end{aligned}'+'\n$$\n\nThe forcing function is $Q(x)='+forcing_value+'$, which is '+('identically zero' if d==e else 'not identically zero')+'. Therefore, this equation is '+classification+'.')
 target=p['target'];ans=subset_label([i for i,r in enumerate(p['equations']) if (r[4]!=r[5])==(target=='inhomogeneous')])
 prompt='Which of the following first-order linear differential equations are '+target+'?\n\n'+'\n'.join('- $'+e+'$' for e in eqs)
 opening="A first-order linear differential equation is homogeneous if it can be written in the form\n\n$$\n{y}^{′}+P(x)y=0.\n$$\n\nA first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as\n\n$$\n{y}^{′}+P(x)y=Q(x)\n$$\n\nwhere $Q$ is not identical to zero.\n\nTo determine which equations are inhomogeneous, we examine each one in turn.\n\n"
 return prompt,opening+'\n\n'.join(blocks)+'\n\nTherefore, the correct answer is "'+ans+'."'


def validate_parameters(level,template,p,profile):
 if template!='collect_and_normalize':
  if set(p)!={'a','n','rhs'}:raise ValueError('Expected a, n, rhs only')
  src=RECIPES[template]['parameters']
  if type(p['a'])!=int or not 1<=abs(p['a'])<=9 or p['a']*src['a']<=0:raise ValueError('Signed coefficient range/sign')
  if type(p['n'])!=int or not ((p['n']==0) if src['n']==0 else 1<=p['n']<=3):raise ValueError('Power workload')
  if len(p['rhs'])!=3:raise ValueError('Three equations required')
  for r,s in zip(p['rhs'],src['rhs']):
   if len(r)!=3 or any(type(v)!=int for v in r):raise ValueError('Integer RHS triple')
   b,c,m=r
   if s[0]:
    if not 1<=abs(b)<=5 or b*s[0]<=0 or c or m:raise ValueError('y-term role/sign')
   elif s[1]:
    if b or not 1<=abs(c)<=9 or not ((m==0) if s[2]==0 else 1<=m<=3):raise ValueError('Forcing role')
   elif r!=[0,0,0]:raise ValueError('Zero role')
   if p['n']==0 and b==p['a']:raise ValueError('Avoid vanished y coefficient')
 else:
  if set(p)!={'equations','target'} or p['target']!='inhomogeneous' or len(p['equations'])!=3:raise ValueError('Hard contract')
  pos=PROFILES[profile]['nonzero_index']
  for i,row in enumerate(p['equations']):
   if len(row)!=7 or any(type(v)!=int for v in row):raise ValueError('Hard integer components')
   k,a,n,b,d,e,m=row
   if not(2<=k<=5 and 1<=abs(a)<=5 and 1<=n<=3 and 1<=abs(b)<=5 and 1<=abs(d)<=5 and 1<=abs(e)<=5 and 1<=m<=3):raise ValueError('Hard bounds')
   if (d!=e)!=(i==pos):raise ValueError('Whole-bank forcing-position eligibility')


def sample(template,rng,profile):
 if template=='collect_and_normalize':
  pos=PROFILES[profile]['nonzero_index'];equations=[]
  for i in range(3):
   d=rng.choice([v for v in range(-5,6) if v]);e=d if i!=pos else rng.choice([v for v in range(-5,6) if v and v!=d])
   equations.append([rng.randint(2,5),rng.choice([v for v in range(-5,6) if v]),rng.randint(1,3),rng.choice([v for v in range(-5,6) if v]),d,e,rng.randint(1,3)])
  return {'equations':equations,'target':'inhomogeneous'}
 s=RECIPES[template]['parameters'];p={'a':rng.randint(1,9)*(1 if s['a']>0 else -1),'n':rng.randint(1,3) if s['n'] else 0,'rhs':[]}
 for b,c,m in s['rhs']:
  p['rhs'].append([rng.randint(1,5)*(1 if b>0 else -1),0,0] if b else ([0,rng.choice([v for v in range(-9,10) if v]),rng.randint(1,3) if m else 0] if c else [0,0,0]))
 return p


def parse_expr(s):
 """Independent readback of concrete displayed polynomial/rational operands."""
 from sympy.parsing.sympy_parser import parse_expr as parse, standard_transformations, implicit_multiplication_application
 s=s.strip().rstrip('.,').replace('{y}^{′}','D').replace('{y}^{\u2032}','D')
 while r'\frac{' in s:
  s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
  # Fractions may contain the source's braced power notation.
  s=re.sub(r'\{x\}\^\{(\d+)\}',r'x**\1',s)
  if r'\frac{' in s and not re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',s):raise ValueError('Unparsed fraction')
 s=re.sub(r'\{x\}\^\{(\d+)\}',r'x**\1',s)
 s=s.replace('{','(').replace('}',')').replace('^','**').replace('&','').strip()
 if '\\' in s:raise ValueError('Unexpected concrete command '+s)
 return parse(s,local_dict={'x':X,'y':Y,'D':V}, transformations=standard_transformations+(implicit_multiplication_application,))

def canonical_equation(text):
 l,r=text.split('=');z=sp.expand(parse_expr(l)-parse_expr(r));a=z.coeff(V)
 if a==0:raise ValueError('First derivative absent')
 normalized=sp.expand(z/a)
 if sp.diff(normalized,Y,2)!=0 or sp.diff(normalized,V)!=1:raise ValueError('Not linear first-order')
 return normalized

def assessed_from_prompt(prompt):
 eqs=re.findall(r'^- \$(.*?)\$',prompt,re.M)
 if len(eqs)!=3:raise ValueError('Expected three concrete ODEs')
 criterion='inhomogeneous' if 'are inhomogeneous?' in prompt else 'homogeneous'
 normal=[canonical_equation(s) for s in eqs]
 forcing=[sp.simplify(-z.subs({Y:0,V:0})) for z in normal]
 correct=subset_label([i for i,f in enumerate(forcing) if (f!=0)==(criterion=='inhomogeneous')])
 return normal,forcing,correct,criterion

def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+str(KP_ID)+'/'+value))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


# Current source contract: equation-labelled checkboxes, not legacy subset radio.
from itertools import product
from math_format import normalize_prose, validate_generated_record
from generator_policy import nonempty_checkbox
CURRENT=json.loads((HOME/'source-kp.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CURRENT[':knowledge-point/questions']}
VERSION='homogeneous-checkbox-recognition-2'
ROLE_NAMES=('zero','move_y','constant_forcing','function_forcing')

def role_catalog(level):
 result=[]
 for roles in product(ROLE_NAMES,repeat=3):
  ny=roles.count('move_y');nz=roles.count('zero')
  nf=sum(r.endswith('forcing') for r in roles)
  if not 1<=ny<=2 or nz>1:continue
  if level=='moderate' and nf==0:continue
  result.append(roles)
 return result

def validate_current(level,p):
 if set(p)!={'a','n','rhs'} or type(p['a'])!=int or not 1<=abs(p['a'])<=9 or type(p['n'])!=int or not 0<=p['n']<=3 or len(p['rhs'])!=3:raise ValueError('Coefficient/degree/three-equation contract')
 roles=[]
 for row in p['rhs']:
  if len(row)!=3 or any(type(v)!=int for v in row):raise ValueError('Integer RHS triple')
  b,c,m=row
  if b:
   if not 1<=abs(b)<=5 or c or m:raise ValueError('Moved-y bounds')
   roles.append('move_y')
  elif c:
   if not 1<=abs(c)<=9 or not 0<=m<=3:raise ValueError('Forcing bounds')
   roles.append('constant_forcing' if m==0 else 'function_forcing')
  elif m:raise ValueError('Zero exponent encoding')
  else:roles.append('zero')
 if tuple(roles) not in role_catalog(level):raise ValueError('Unsupported workload or empty correct subset')
 if len({eq(p['a'],p['n'],r) for r in p['rhs']})!=3:raise ValueError('Duplicate equations')
 return roles

def sample_current(level,rng):
 roles=rng.choice(role_catalog(level)) # Decision roles first.
 p={'a':rng.choice([v for v in range(-9,10) if v]),'n':rng.randrange(4),'rhs':[]}
 for role in roles:
  if role=='zero':row=[0,0,0]
  elif role=='move_y':row=[rng.choice([v for v in range(-5,6) if v]),0,0]
  else:row=[0,rng.choice([v for v in range(-9,10) if v]),0 if role=='constant_forcing' else rng.randint(1,3)]
  p['rhs'].append(row)
 return p

def current_render(level,p):
 target='homogeneous' if level=='easy' else 'inhomogeneous'
 opening=RECIPES['q-331601' if level=='easy' else 'q-331744']['solution_mask'].split('- First,')[0]
 equations=[eq(p['a'],p['n'],r) for r in p['rhs']];blocks=[];selected=[]
 for i,(row,e) in enumerate(zip(p['rhs'],equations)):
  b,c,m=row
  block='- '+['First','Next','Finally'][i]+', we consider the equation\n\n$$\n'+e+'.\n$$\n\n'
  if b:
   moved=add(lhs(p['a'],p['n']),sy(-b))+' & =0'
   collected=final(p['a'],p['n'],b)+' & =0'
   block+='We move the term involving $y$ to the left side so that all $y$-terms are together:\n\n$$\n'+r'\begin{aligned}'+e.replace('=',' & =')+r' \\ '+moved+r' \\ '+collected+r'\end{aligned}'+'\n$$\n\nThis matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.'
  elif c:
   if m==0 and level=='easy':block+='The presence of the constant term $'+mono(c,m)+'$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.'
   else:block+='Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)='+mono(c,m)+'$ is not identically zero. Therefore, this equation is inhomogeneous.'
  else:block+='The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.'
  if bool(c)==(level=='moderate'):selected.append('$'+e+'$')
  blocks.append(block)
 conclusion='Therefore, the correct answer is '+'; '.join(selected)+(' only.' if len(selected)<3 else '.')
 return 'Which of the following first-order linear differential equations are '+target+'?\n\nSelect all that apply.',opening+'\n\n'.join(blocks)+'\n\n'+conclusion,equations

def own_question(q,seed):
 # Normalize before deriving identities. Raw source comparison is kept separate.
 q=json.loads(json.dumps(q));q.pop(':db/id',None)
 q[':question/problem']=normalize_prose(q[':question/problem'])
 q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
 for f in q[':question/answer-fields']:f[':answer-field/key']=normalize_prose(f[':answer-field/key'])
 canonical={'difficulty':q[':question/difficulty'],'problem':q[':question/problem'],'solution':q[':question/worked-solution'],'fields':[(f[':answer-field/key'],f[':answer-field/correct'],sorted(a[':answer/value'] for a in f[':answer-field/choices'])) for f in q[':question/answer-fields']]}
 content=digest(canonical);q[':question/id']=uid('q/'+content)
 for i,f in enumerate(q[':question/answer-fields']):
  f[':answer-field/id']=uid('field/'+content+'/'+str(i));correct=f[':answer-field/correct']
  for a in f[':answer-field/choices']:a[':answer/id']=uid('answer/'+f[':answer-field/id']+'/'+a[':answer/value'])
  f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
 return q,content

@nonempty_checkbox
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty: '+str(level))
 if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Checkbox response required')
 rng=random.Random(seed)
 if profile and profile.startswith('raw_'):template=profile[4:]
 if template is not None and (template not in RECIPES or RECIPES[template]['level']!=level):raise ValueError('Source template/level mismatch')
 replay=bool(profile and profile.startswith('raw_'))
 if replay:
  p=json.loads(json.dumps(parameters if parameters is not None else RECIPES[template]['parameters']))
  if p!=RECIPES[template]['parameters']:raise ValueError('Source replay needs original parameters')
  src=SOURCES[template];q={k:v for k,v in src.items() if k not in (':db/id',':question/id')}
  q[':question/difficulty']=src[':question/difficulty'][':db/ident']
  q[':question/answer-fields']=[{':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':[{':answer/type':':answer.type/text',':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':f[':answer-field/correct'][':answer/value']} for f in src[':question/answer-fields']]
 else:
  if profile not in (None,'checkbox-roles'):raise ValueError('Unknown current profile')
  if parameters is not None:p=json.loads(json.dumps(parameters));validate_current(level,p)
  else:
   for attempt in range(100):
    p=sample_current(level,rng)
    try:validate_current(level,p);break
    except ValueError:continue
   else:raise ValueError('No distinct supported instance')
  prompt,solution,equations=current_render(level,p)
  q={':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[]}
  for e,r in zip(equations,p['rhs']):
   q[':question/answer-fields'].append({':answer-field/key':'$'+e+'$',':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':[{':answer/type':':answer.type/text',':answer/value':v} for v in ('false','true')],':answer-field/correct':str(bool(r[1])==(level=='moderate')).lower()})
 roles=validate_current(level,p)
 q,content=own_question(q,seed)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template if replay else 'recognition','profile':'source-replay' if replay else 'checkbox-roles','parameters':p,'roles':roles,'source_ids':[template] if template else list(SOURCES),'source':SOURCE,'evidence_only':replay,'eligible_for_learning':not replay,'content_fingerprint':content,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 validate_generated_record(record)
 return record

# Easy: six observed homogeneous-selection layouts, constant/monomial forcing,
# one or two moved y terms. No additional stages under parameter variation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: six observed inhomogeneous-selection layouts; preserve each source's
# shared prose and original ordered collect-y chain at changed coefficients.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard is unsupported in this source-backed package; API raises explicitly.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question']
 return q[':question/problem']+'\n\n'+'\n'.join('- [ ] '+f[':answer-field/key'] for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<0:ap.error('--count must be nonnegative')
 records=[generate(args.difficulty,args.seed+i,args.template,profile=args.profile) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

if __name__=='__main__':main()
