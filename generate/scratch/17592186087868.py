#!/usr/bin/env python3
"""Recognize homogeneous first-order linear ODEs, steps 3–7 only.

Source-shaped parameterized masks preserve every complete source bank and all
operative solution stages. raw_q-* profiles are public evidence-only replay;
observed_q-* profiles are normal parameterized source-shaped presentation.
No answer lookup: forcing is derived from the generated equations using SymPy.
Authored hard collects both y and forcing terms, then divides by a nonzero
constant, using the earlier lesson's standard-form prerequisite. No solving,
nonlinear equations, second-order equations, or homogeneous substitution method.
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
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
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

def lhs(a,n):return add(D,mono(a,n)+'y')
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


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio response supported')
 rng=random.Random(seed)
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown complete bank profile')
  selected=PROFILES[profile]['template']
  if template and template!=selected:raise ValueError('Profile/template mismatch')
  template=selected
 if template is None:template=rng.choice([t for t,r in TEMPLATES.items() if r['level']==level])
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Template/level mismatch')
 if profile is None:profile=rng.choice(['authored_hard_'+str(i) for i in range(3)]) if level=='hard' else 'observed_'+template
 bank=list(PROFILES[profile]['bank']) # Complete bank BEFORE parameter sampling.
 if parameters is not None:p=json.loads(json.dumps(parameters));validate_parameters(level,template,p,profile)
 else:
  for attempt in range(100):
   p=sample(template,rng,profile)
   try:validate_parameters(level,template,p,profile);break
   except ValueError:continue
  else:raise ValueError('No eligible whole instance')
 prompt,solution=hard_render(p) if level=='hard' else source_render(template,p)
 norm,forcing,correct,criterion=assessed_from_prompt(prompt)
 if len(set(bank))!=5 or bank.count(correct)!=1:raise ValueError('Ambiguous or incomplete complete bank')
 # Magnitudes/exponents affect presentation, not the finite categorical decision.
 roles=[('zero' if f==0 else ('nonzero_constant' if not f.has(X) else 'nonzero_function')) for f in forcing]
 if level!='hard':roles=[('zero_rhs' if r==[0,0,0] else ('move_y' if r[0] else ('constant_forcing' if r[2]==0 else 'function_forcing'))) for r in p['rhs']]
 fingerprint=digest({'criterion':criterion,'roles':roles,'normalization':level=='hard','constant_coefficient':level!='hard' and p['n']==0})
 content=digest({'version':VERSION,'difficulty':level,'prompt':prompt,'solution':solution,'bank':sorted(bank)})
 qid=uid('q/'+content);fid=uid('field/'+content+'/selection')
 choices=[{':answer/id':uid('answer/'+fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
 correct_id=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
 random.Random(seed).shuffle(choices)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
 evidence=PROFILES[profile]['evidence_only']
 if evidence:question[':question/math-academy-id']=template
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':SOURCE,'source_ids':[template] if level!='hard' else [],'origin':TEMPLATES[template]['origin'],'bank_origin':PROFILES[profile]['origin'],'evidence_only':evidence,'eligible_for_learning':not evidence,'domains':'x in R; derivative divisor nonzero constant' if level=='hard' else 'x in R','mathematical_fingerprint':fingerprint,'content_fingerprint':content,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: six observed homogeneous-selection layouts, constant/monomial forcing,
# one or two moved y terms. No additional stages under parameter variation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: six observed inhomogeneous-selection layouts; preserve each source's
# shared prose and original ordered collect-y chain at changed coefficients.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard (authored): each of three equations requires moving one y-term and one
# forcing term, collecting, and dividing by k=2..5. Same workload each instance.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
