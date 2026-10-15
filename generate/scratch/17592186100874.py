#!/usr/bin/env python3
"""Frozen basis-2275 definite-substitution generator; no database access.

The source power/radical, substitution degree, response contract and four
instructional stages are fixed by each family. Numerical coefficient, shift,
and both endpoints are explicit slots. Observed opaque banks replay exactly;
normal radio sampling uses the separately declared complete method bank.
"""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().with_suffix('')
sys.dont_write_bytecode=True

def frozen(name):
 spec=importlib.util.spec_from_file_location('definite_sub_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=frozen('math_format');printed=frozen('printed');X=printed.x;U=printed.u
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record'];KP_ID=17592186100874
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
VERSION='definite-substitution-2026-10-14-v1';SUPPORTED_LEVELS=('easy','moderate','hard')
# n,r are structural; a,b,c and actual x endpoints l,h are numerical slots.
SPECS={
'q-49527':(1,'1/2','unrated','radio',2,-1,1,'1','2'),
'q-49610':(1,'2','easy','radio',2,1,1,'1','2'),
'q-17103':(3,'3/2','hard','radio',1,1,3,'0','2'),
'q-17104':(3,'3/2','hard','radio',-1,2,1,'0','1'),
'q-318994':(3,'3','hard','blank',1,5,6,'0','1'),
'q-336603':(1,'1/2','easy','blank',10,7,1,'-7/10','-1/5'),
'q-336612':(4,'2','hard','blank',1,1,8,'0','1'),
'q-336783':(1,'2','easy','blank',9,2,1,'0','1/3'),
'q-336788':(1,'3','easy','blank',4,2,1,'0','1/2'),
'q-336803':(2,'3/2','hard','blank',1,1,2,'0','sqrt(3)'),
'q-336804':(2,'1/2','hard','blank',1,1,2,'0','2*sqrt(2)'),
'q-49613':(1,'3/2','moderate','radio',5,-6,1,'2','3'),
'q-49622':(1,'1/2','easy','radio',8,1,1,'0','1/4')}
LEVELS={t:v[2] for t,v in SPECS.items()}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),v))
def task_digest(m):return digest([s.srepr(m['f']),s.srepr(m['lo']),s.srepr(m['hi']),'exact definite integral'])
@lru_cache(None)
def source_tasks():return {task_digest(allowed(t,defaults(t))):t for t in SPECS}
def content_digest(q):
 q=copy.deepcopy(q)
 for field in q[':question/answer-fields']:field[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return digest(q)
def tex(v):return s.latex(v)
def defaults(t):
 z=SPECS[t];return dict(a=z[4],b=z[5],c=z[6],l=z[7],h=z[8])
def exact_int(v):return type(v) is int

def allowed(t,p):
 if t not in SPECS:raise ValueError('unknown template')
 if set(p)!={'a','b','c','l','h'}:raise ValueError('exact declared parameter set required')
 if any(not exact_int(p[k]) or abs(p[k])>12 for k in ('a','b','c')):raise ValueError('builtin integer coefficients, absolute value at most12')
 if not p['a'] or not p['c']:raise ValueError('nonzero a,c required')
 n,r,*_=SPECS[t];r=s.Rational(r)
 lo,hi=[printed.scalar(str(p[k])) for k in ('l','h')]
 if any(z.free_symbols or z.is_real is not True for z in (lo,hi)):raise ValueError('real constant endpoints required')
 if not bool(lo<hi) or abs(lo)>12 or abs(hi)>12:raise ValueError('ordered x endpoints within [-12,12] required')
 z=p['a']*X**n+p['b'];left=s.simplify(z.subs(X,lo));right=s.simplify(z.subs(X,hi))
 # For even degree, include stationary x=0 in the closed interval. For odd
 # degree the inner polynomial is monotone. Real roots stay real throughout.
 candidates=[left,right]+([s.Integer(p['b'])] if n%2==0 and lo<=0<=hi else [])
 if r.q==2 and any(v<0 for v in candidates):raise ValueError('negative radicand on interval')
 if t=='q-17104' and (p['a']>=0 or lo<0):raise ValueError('retain decreasing substitution on nonnegative interval')
 if n==1 and p['c']!=1:raise ValueError('linear source has no external amplitude slot')
 if n>1 and lo<0:raise ValueError('hard source sampling uses nonnegative original interval')
 k=s.Rational(p['c'],p['a']*n);g=U**r;F=k*U**(r+1)/(r+1)
 return dict(n=n,r=r,z=z,lo=lo,hi=hi,L=left,H=right,k=k,g=g,F=F,f=p['c']*X**(n-1)*z**r,A=s.simplify(F.subs(U,right)),B=s.simplify(F.subs(U,left)))

def recipes(t,m,profile):
 A,B,k=m['A'],m['B'],m['k'];T=s.simplify(A-B)
 if SPECS[t][3]=='blank':return [T],['correct']
 if profile in ('method','method-unit','method-scaled'):
  if profile=='method-unit' and k!=1:raise ValueError('profile requires k=1')
  if profile=='method-scaled' and k==1:raise ValueError('profile requires k!=1')
  values=[T,-T,s.simplify(T/k),s.simplify(A+B),A];names=['correct','reversed subtraction','omit differential multiplier','add endpoint values','omit lower endpoint']
  # k=1 makes missing multiplier correct; a second complete profile is explicit.
  if k==1:values=[T,-T,A+B,A,B];names=['correct','reversed subtraction','add endpoint values','omit lower endpoint','use lower endpoint only']
 elif profile=='observed':
  # Unknown numerical error interpretations are retained as complete
  # homogeneous source profiles. Their transformed endpoints stay fixed;
  # changing the substitution/differential scales EVERY option by k/k0.
  if t=='q-49527':values=[2*A-2*B,3*A-B,A-3*B,A-B,2*A-3*B];names=['2A-2B','3A-B','A-3B','A-B','2A-3B']
  elif t=='q-17104':
   r=m['r'];L,H=m['L'],m['H'];scale=k/(r+1)
   values=[-scale*(L**r-H**(r+1)),T,-T,-scale*(L**(r+1)+H**(r+1)),-3*T]
   # Original final choice is +3T (differential multiplier omitted).
   values[-1]=3*T;names=['lower exponent r instead of r+1','correct','reverse endpoints','sum positive endpoint magnitudes','omit factor1/3']
  else:
   origin=allowed(t,defaults(t))
   if m['L']!=origin['L'] or m['H']!=origin['H']:raise ValueError('observed profile requires original transformed bounds')
   ratio=k/origin['k']
   raw=[printed.scalar(a[':answer/value']) for a in SOURCES[t][':question/answer-fields'][0][':answer-field/choices']]
   values=[s.simplify(v*ratio) for v in raw]
   names=['('+a[':answer/value']+') * k/('+tex(origin['k'])+'); retain source expression at fixed L,H; interpretation unresolved' for a in SOURCES[t][':question/answer-fields'][0][':answer-field/choices']]
 else:raise ValueError('complete profile must be observed or method')
 return [s.simplify(v) for v in values],names

def check_bank(values,correct):
 if sum(s.simplify(v-correct)==0 for v in values)!=1:raise ValueError('profile has ambiguous correct option')
 if any(s.simplify(v-w)==0 for i,v in enumerate(values) for w in values[:i]):raise ValueError('complete profile collision')

def power(z,r):
 if r==s.Rational(1,2):return r'\sqrt{'+tex(z)+'}'
 if r==s.Rational(3,2):return r'\sqrt{('+tex(z)+r')^{3}}'
 return '('+tex(z)+')^{'+tex(r)+'}'
def integral(lo,hi,f,var):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'} '+f+r'\,\text{d}'+var

def render(t,p,m):
 n,r,z,lo,hi,L,H,k,g,F=[m[j] for j in ('n','r','z','lo','hi','L','H','k','g','F')]
 factor=p['c']*X**(n-1);body=(tex(factor)+r'\cdot ' if factor!=1 else '')+power(z,r)
 original=integral(lo,hi,body,'x');transformed=integral(L,H,power(U,r)+r'\cdot ('+tex(k)+')','u')
 field=SPECS[t][3]
 src=SOURCES[t][':question/problem']
 if src.startswith('Compute'):prompt='Compute the exact value of the definite integral.\n\n$'+original+'=$\n{{field-1}}'
 elif src.startswith('Evaluate'):prompt='Evaluate the definite integral $'+original+'.$'
 elif src.startswith('Calculate'):prompt='Calculate the definite integral $'+original+'.$'
 else:prompt='$'+original+'=$'
 derivative=s.diff(z,X)
 block=[r'u&='+tex(z),r'\frac{\text{d}u}{\text{d}x}&='+tex(derivative),r'\text{d}u&='+tex(derivative)+r'\,\text{d}x']
 if k!=1:block += [tex(k)+r'\text{d}u&='+tex(factor)+r'\,\text{d}x']
 sol='We start by changing the variable:\n\n$$\n'+r'\begin{aligned}'+r'\\ '.join(block)+r'\end{aligned}'+'\n$$'
 sol+='\n\nNext, we create a table for the limits of integration using the rule $u='+tex(z)+'.$\n\n$$\n'+r'\begin{aligned}x & '+tex(lo)+' & '+tex(hi)+r'\\ u & '+tex(L)+' & '+tex(H)+r'\end{aligned}'+'\n$$'
 sol+='\n\nSo, the integral in terms of the new variable is\n\n$$\n'+original+'='+transformed+'.\n$$'
 rows=[transformed,tex(k)+r'\int_{'+tex(L)+'}^{'+tex(H)+'} u^{'+tex(r)+r'}\,\text{d}u',tex(F)+r'\big|_{'+tex(L)+'}^{'+tex(H)+'}',tex(k/(r+1))+'(('+tex(H)+')^{'+tex(r+1)+'}-('+tex(L)+')^{'+tex(r+1)+'})',tex(m['A'])+'-('+tex(m['B'])+')',tex(s.simplify(m['A']-m['B']))]
 sol+='\n\nFinally, we can solve it and get\n\n$$\n'+r'\begin{aligned}'+rows[0]+' &='+r'\\ &='.join(rows[1:])+r'.\end{aligned}'+'\n$$'
 return prompt,sol

def source_question(t):
 q=copy.deepcopy(SOURCES[t]);q.pop(':db/id',None)
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
 return q

def assemble(t,level,seed,p,profile,raw=False):
 m=allowed(t,p);T=s.simplify(m['A']-m['B'])
 if profile=='method':profile='method-unit' if m['k']==1 else 'method-scaled'
 values,names=recipes(t,m,'observed' if raw else profile);check_bank(values,T)
 field=SPECS[t][3];origin=p==defaults(t)
 if raw:
  if not origin:raise ValueError('raw replay requires original parameters')
  q=source_question(t)
 else:
  prompt,sol=render(t,p,m)
  # Source wording and every original stage are preserved verbatim at source
  # parameters, independently checked against the derived math by validate.py.
  if origin:
   prompt=SOURCES[t][':question/problem']
   if ':question/worked-solution' in SOURCES[t]:sol=SOURCES[t][':question/worked-solution']
  q={':question/problem':fmt.normalize_prose(prompt),':question/worked-solution':fmt.normalize_prose(sol),':question/difficulty':':question.difficulty/'+level}
  rendered=[fmt.normalize_tex(tex(v)) for v in values];key='selection' if field=='radio' else 'field-1'
  content=digest([VERSION,level,q,field,sorted(rendered),tex(T)]);qid=uid('question:'+content);fid=uid('field:'+qid+key)
  choices=[{':answer/id':uid('answer:'+fid+s.srepr(v)),':answer/type':':answer.type/math',':answer/value':vtex} for v,vtex in zip(values,rendered)]
  cid=choices[next(i for i,v in enumerate(values) if s.simplify(v-T)==0)][':answer/id'];random.Random(seed).shuffle(choices)
  q.update({':question/id':qid,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field,':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}]})
 task=task_digest(m)
 result={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':'observed_raw' if raw else profile,'bank_profile':'observed_raw' if raw else profile,'parameters':p,'source_ids':[t],'source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'origin':'raw MA evidence' if raw else 'authored completion of unrated original' if t=='q-49527' else 'source family with complete authored method bank' if field=='radio' and profile.startswith('method') else 'parameterized source family with complete observed profile' if profile=='observed' else 'parameterized source family','recipes':names,'math_fingerprint':task,'reproduces_source_task':source_tasks().get(task),'content_fingerprint':content_digest(q),'domain':'real closed original interval; radical inner expression >=0 everywhere','plot_rating':'none','python_version':sys.version.split()[0],'sympy_version':s.__version__}}
 if not raw:fmt.validate_generated_record(result)
 return result

def sample(t,rng,profile=None):
 n,r,level,field,*_=SPECS[t]
 if profile=='observed' and t in ('q-49610','q-49613','q-49622'):
  origin=allowed(t,defaults(t));a=rng.randint(2,10);b=rng.randint(-6,7)
  return dict(a=a,b=b,c=1,l=str((origin['L']-b)/a),h=str((origin['H']-b)/a))
 if profile=='observed' and t=='q-17103':
  a=rng.choice([1,8]);return dict(a=a,b=1,c=rng.randint(1,9),l='0',h='2' if a==1 else '1')
 if n==1:
  a=rng.randint(2,10);b=rng.randint(-6,7);L=rng.randint(0,4);H=L+rng.randint(1,5)
  if r in ('2','3'):L=rng.randint(-3,3);H=L+rng.randint(1,5)
  return dict(a=a,b=b,c=1,l=str(s.Rational(L-b,a)),h=str(s.Rational(H-b,a)))
 a=-1 if t=='q-17104' else rng.choice([1,2]);b=rng.randint(2,5) if a<0 else rng.randint(1,5)
 lo=rng.choice([s.Integer(0),s.Rational(1,2)])
 hi=s.Integer(1) if a<0 or n==4 else rng.choice([s.Integer(1),s.Integer(2)])
 if n==2:hi=rng.choice([s.Integer(1),s.sqrt(3),2*s.sqrt(2)])
 return dict(a=a,b=b,c=rng.choice([1,n,2*n]),l=str(lo),h=str(hi))

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('difficulty must be easy,moderate,hard')
 if not exact_int(seed):raise ValueError('seed must be builtin int')
 rng=random.Random(seed);templates=[t for t in SPECS if LEVELS[t]==level]
 t=template or rng.choice(templates)
 if t not in SPECS or (LEVELS[t]!=level and t!='q-49527'):raise ValueError('template/difficulty mismatch')
 if t=='q-49527' and level!='easy':raise ValueError('completion has conservative authored easy placement')
 if profile is None:
  if SPECS[t][3]=='blank':profile='blank'
  elif parameters is None:profile=rng.choice(['observed','method'])
  else:
   m=allowed(t,parameters);original=allowed(t,defaults(t))
   profile='observed' if t in ('q-49527','q-17104') or (m['L']==original['L'] and m['H']==original['H']) else 'method'
 if profile=='observed_raw':return assemble(t,level,seed,defaults(t) if parameters is None else parameters,'observed',True)
 if SPECS[t][3]=='blank' and profile!='blank':raise ValueError('blank has no distractor profile')
 if parameters is not None:return assemble(t,level,seed,parameters,profile)
 for attempt in range(200):
  p=sample(t,rng,profile)
  try:
   result=assemble(t,level,seed,p,profile)
   return result
  except ValueError as err:
   if 'profile' not in str(err):raise
 raise ValueError('no collision-free complete bank sampled')

def complete_source(seed=0):return generate('easy',seed=seed,template='q-49527',parameters=defaults('q-49527'),profile='observed')
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_batch(difficulty='all',count=1,seed=0):
 if not exact_int(count) or count<0:raise ValueError('count must be nonnegative builtin int')
 if not exact_int(seed):raise ValueError('seed must be builtin int')
 levels=SUPPORTED_LEVELS if difficulty=='all' else (difficulty,)
 if any(v not in SUPPORTED_LEVELS for v in levels):raise ValueError('unknown difficulty')
 return [generate(level,seed+i) for level in levels for i in range(count)]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['all',*SUPPORTED_LEVELS],default='all');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();records=generate_batch(a.difficulty,a.count,a.seed)
 if a.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
 else:
  for r in records:
   q=r['question'];print(q[':question/problem']+'\n\n'+q[':question/worked-solution']);print('\nAnswer: '+next(x[':answer/value'] for x in q[':question/answer-fields'][0][':answer-field/choices'] if x[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][1]))
if __name__=='__main__':main()
