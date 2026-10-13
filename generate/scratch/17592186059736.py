#!/usr/bin/env python3
"""Cross-product determinants, fixed math basis 1356. No EDB access or writes.

Observed recipes retain complete formal determinant/minor/arithmetic/component/
tuple row sequences. Explicit observed profiles are opaque bilinear-covariance
banks, not claims about author error intent; each scales both input vectors and
all bank vectors together. Default banks use the full five-operation authored
bank. Moderate/hard are authored arithmetic workloads, never observed labels.
API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus generate_easy/moderate/hard. See adjacent evidence README.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as S
ROOT=Path(__file__).with_suffix('')
KP_ID=17592186059736
KP_UUID='733eab11-2a26-5402-8df5-bba50c9beaf9'
TITLE='Calculating the Cross Product Using Determinants'
VERSION='cross-determinants-1'
NS=uuid.UUID(KP_UUID)
ATOM=re.compile(r'\\frac\{\d+\}\{\d+\}|\\sqrt\{\d+\}|\d+')
I,J,K=S.symbols('i j k')
def scalar(x):
 x=str(x).replace('\\\\','\\').strip().replace(' ','').replace(r'\,','').replace(r'\cdot','*')
 x=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',x)
 x=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',x)
 x=x.replace(')(',')*(')
 x=re.sub(r'(?<=[0-9)])(?=sqrt\()', '*', x)
 for b in 'ijk': x=re.sub(r'(?<=[\d)])'+b,'*'+b,x)
 return S.sympify(x,locals={'i':I,'j':J,'k':K})
def vector(x):
 x=x.strip()
 if x.startswith('⟨'):return S.Matrix([scalar(t) for t in x[1:-1].split(',')])
 z=S.expand(scalar(x));return S.Matrix([z.coeff(b) for b in (I,J,K)])
def tex(x):return S.latex(S.simplify(x)).replace(' ','')
def tuple_tex(v):return '⟨'+','.join(tex(z) for z in v)+'⟩'
def basis_tex(v,thin=False):
 out=''
 for z,b in zip(v,'ijk'):
  if z==0:continue
  neg=z.could_extract_minus_sign(); z=-z if neg else z
  sign='-' if neg else ('+' if out else '')
  c='' if z==1 else tex(z)
  if z.is_Add:c='('+c+')'
  out+=sign+c+(r'\,' if thin and c else '')+b
 return out or '0i+0j+0k'
def product(a,b):return '('+tex(a)+')('+tex(b)+')'
def formal(a,b,labels=('u','v')):
 A=[tex(x) for x in a];B=[tex(x) for x in b]
 det='|'+r'\begin{aligned}i & j & k \\ '+' & '.join(A)+r' \\ '+' & '.join(B)+r'\end{aligned}|'
 minors=[]
 for p,q in ((1,2),(0,2),(0,1)):
  minors.append('|'+r'\begin{aligned}'+A[p]+' & '+A[q]+r' \\ '+B[p]+' & '+B[q]+r'\end{aligned}|')
 pairs=((1,2,2,1),(0,2,2,0),(0,1,1,0))
 mult=[];evals=[]
 for p,q,r,t in pairs:
  mult.append('('+product(a[p],b[q])+'-'+product(a[r],b[t])+')')
  x,y=a[p]*b[q],a[r]*b[t]
  evals.append('('+tex(x)+'-('+tex(y)+'))')
 row=lambda v:v[0]+'i-'+v[1]+'j+'+v[2]+'k'
 c=a.cross(b)
 return 'Using the determinant formula, we get\n\n$$\n'+r'\begin{aligned}'+labels[0]+r'\times '+labels[1]+' & ='+det+r' \\  & ='+row(minors)+r' \\  & ='+row(mult)+r' \\  & ='+row(evals)+r' \\  & ='+basis_tex(c)+r' \\  & ='+tuple_tex(c)+r'.\end{aligned}'+'\n$$'
def scale_atom(raw,s):
 # Original lexical scalar is one complete component, never a prose replacement.
 value=scalar(raw)*s
 return raw if S.simplify(s-1)==0 else tex(value)
def scale_numbers(raw,scales):
 it=iter(scales)
 out=ATOM.sub(lambda m:scale_atom(m.group(),next(it)),raw)
 try:next(it);raise ValueError('Extra scaler')
 except StopIteration:pass
 return out
def scale_vector(raw,s):
 if raw.startswith('⟨'):return scale_numbers(raw,[s]*len(ATOM.findall(raw)))
 # Whole basis vector protects basis labels and includes implicit unit coefficients.
 return basis_tex(vector(raw)*s)
RECIPES=json.loads((ROOT/'recipes.json').read_text())
def replay(recipe,sa,sb,raw=False):
 a=S.Matrix([scalar(z)*sa for z in recipe['a']]);b=S.Matrix([scalar(z)*sb for z in recipe['b']]);s=sa*sb
 prompt=recipe['prompt_mask'].replace('@@A@@',scale_vector(recipe['a_raw'],sa)).replace('@@B@@',scale_vector(recipe['b_raw'],sb))
 rows=[]
 for row in recipe['solution_rows']:
  if row['kind']=='matrix':
   idx=[sa if x=='a' else sb for x in row['scalers']]
  elif row['kind']=='product':idx=[sa if x=='a' else sb for x in row['scalers']]
  else:idx=[s]*len(ATOM.findall(row['text']))
  rows.append(scale_numbers(row['text'],idx))
 solution=recipe['solution_prefix']+r' \\  & ='.join(rows)+recipe['solution_suffix'] if rows else formal(a,b,recipe['labels'])
 if recipe['id']=='q-282147' and not raw:
  # Raw source loses grouping of the three minors in its distributed row.
  canonical=formal(a,b,recipe['labels']);replacement=canonical.split(r' \\  & =')[2]
  chunks=solution.split(r' \\  & =');chunks[2]=replacement;solution=r' \\  & ='.join(chunks)
 fields=[]
 for f in recipe['fields']:
  typ=f['type'];key=f['key']
  vals=[scale_vector(z,s) if typ=='radio' else scale_numbers(z,[s]*len(ATOM.findall(z))) for z in f['values']]
  # Normalize doubled math slashes from the captured blank values.
  if not raw:vals=[z.replace('\\\\','\\') for z in vals]
  fields.append((key,typ,vals,f['correct_index']))
 return a,b,prompt,solution,fields

def validate_params(level,a,b):
 if len(a)!=3 or len(b)!=3:raise ValueError('Exactly three coordinates required')
 if any(z.free_symbols or z.is_real is not True for z in list(a)+list(b)):raise ValueError('Exact real constants only')
 if level=='easy':
  if any(abs(z)>30 for z in list(a)+list(b)):raise ValueError('Easy coordinate magnitude <=30')
 elif level=='moderate':
  if any(z==0 or not z.is_Integer or abs(z)>8 for z in list(a)+list(b)):raise ValueError('Moderate: six nonzero integers of magnitude <=8')
 elif level=='hard':
  if any(z==0 or not z.is_Rational or abs(z)>8 or z.q>5 for z in list(a)+list(b)) or sum(z.q>1 for z in list(a)+list(b))!=2:raise ValueError('Hard: six nonzero rationals <=8, exactly two reduced nonintegers, denominators 2..5')
 else:raise ValueError('difficulty')
def sample(level,rng):
 if level=='easy':
  vals=[S.Integer(rng.choice([x for x in range(-6,7) if x])) for _ in range(6)];vals[rng.randrange(6)]=S.Integer(0)
 elif level=='moderate':vals=[S.Integer(rng.choice([x for x in range(-8,9) if x])) for _ in range(6)]
 else:
  vals=[S.Integer(rng.choice([x for x in range(-6,7) if x])) for _ in range(6)]
  for idx in rng.sample(range(6),2):
   d=rng.randint(2,5);n=rng.choice([x for x in range(-7,8) if x and S.gcd(x,d)==1]);vals[idx]=S.Rational(n,d)
 return S.Matrix(vals[:3]),S.Matrix(vals[3:])
def operation_bank(a,b):
 c=a.cross(b);minor=S.Matrix([a[1]*b[2]+a[2]*b[1],-(a[0]*b[2]+a[2]*b[0]),a[0]*b[1]+a[1]*b[0]])
 return [c,-c,S.Matrix([c[0],-c[1],c[2]]),minor,S.Matrix([c[1],c[2],c[0]])]
def unique_bank(vals):
 for n,v in enumerate(vals):
  for w in vals[:n]:
   if all(S.simplify(x-y)==0 for x,y in zip(v,w)):raise ValueError('Complete bank collision; reject whole instance')
def stable(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 if template in RECIPES or profile and profile.startswith('observed:'):
  template=template or profile.split(':',1)[1].removesuffix(':raw');r=RECIPES[template]
  if profile is not None and profile not in (f'observed:{template}',f'observed:{template}:raw'):raise ValueError('Incompatible observed bank profile')
  if level!='easy':raise ValueError('Observed templates have only easy/authored-unrated replay labels')
  if field_type and field_type!=r['fields'][0]['type']:raise ValueError('Field type incompatible')
  parameters=parameters or {'a_scale':1,'b_scale':1}
  if set(parameters)!={'a_scale','b_scale'}:raise ValueError('Observed covariance profiles require a_scale,b_scale')
  sa,sb=map(scalar,(parameters['a_scale'],parameters['b_scale']))
  if any(z not in (S.Rational(1,2),S.Integer(1),S.Integer(2)) for z in (sa,sb)):raise ValueError('Observed covariance scale in {1/2,1,2}')
  raw=profile==f'observed:{template}:raw'
  a,b,prompt,solution,specs=replay(r,sa,sb,raw)
  # Public raw replay is explicit evidence, including the malformed dot symbol.
  if template=='q-1408' and raw:prompt=prompt.replace(r'\times',r'\cdot')
  validate_params('easy',a,b)
  for _,typ,vals,_ in specs:
   if typ=='radio':unique_bank([vector(z) for z in vals])
  profile=profile or f'observed:{template}'
 else:
  template=template or 'tuple_radio';profile=profile or 'authored:five_operations'
  if template not in ('tuple_radio','basis_radio','tuple_blank','basis_blank'):raise ValueError('Unknown template')
  if profile!='authored:five_operations':raise ValueError('Unknown bank profile')
  typ='blank' if template.endswith('blank') else 'radio'
  if field_type and field_type!=typ:raise ValueError('Field type incompatible')
  for attempt in range(1000):
   if parameters is not None:
    if set(parameters)!={'a','b'}:raise ValueError('a,b required')
    a=S.Matrix([scalar(z) for z in parameters['a']]);b=S.Matrix([scalar(z) for z in parameters['b']])
   else:a,b=sample(level,rng)
   validate_params(level,a,b)
   try:
    bank=operation_bank(a,b);unique_bank(bank);break
   except ValueError:
    if parameters is not None:raise
  else:raise ValueError('No eligible complete bank')
  c=a.cross(b);is_basis=template.startswith('basis');render=basis_tex if is_basis else tuple_tex
  prompt='Let $u='+render(a)+'$ and $v='+render(b)+r'.$ Find $u\times v.$'
  solution=formal(a,b)
  if typ=='radio':specs=[('selection','radio',[render(z) for z in bank],0)]
  else:
   prompt+='\n\n'+(r'$u\times v=$'+'\n\n{{field-1}}'+r'$\,i\,+\,$'+'\n{{field-2}}'+r'$\,j\,+\,$'+'\n{{field-3}}'+r'$\,k$' if is_basis else r'$u\times v=⟨${{field-1}}$,$'+'\n{{field-2}}$,$\n{{field-3}}$⟩$')
   specs=[(f'field-{i+1}','blank',[tex(z)],0) for i,z in enumerate(c)]
  parameters={'a':[str(z) for z in a],'b':[str(z) for z in b]}
 math_fp=stable({'a':[str(z) for z in a],'b':[str(z) for z in b],'operation':'ordered-cross-product'})
 content=stable({'version':VERSION,'prompt':prompt,'solution':solution,'fields':[(k,t,sorted(v),v[c]) for k,t,v,c in specs]})
 fields=[]
 for n,(key,typ,vals,correct) in enumerate(specs):
  fid=uid(content+':field:'+key+':'+str(n));answers=[{':answer/id':uid(fid+':'+z),':answer/type':':answer.type/math',':answer/value':z} for z in vals]
  ref=answers[correct][':answer/id']
  if typ=='radio':rng.shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':answers,':answer-field/correct':[':answer/id',ref]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':parameters,'mathematical_fingerprint':math_fp,'content_fingerprint':content,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'level_origin':'authored' if level!='easy' or template=='q-1408' else 'observed-or-authored-default','bank_intent':'opaque covariance; no recovered error intent' if template in RECIPES else 'complete authored operation bank'}}
# EASY: observed signed/zero integer, sparse fraction/radical workloads; defaults one zero.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE (authored): six nonzero integer entries, six substantive products.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored): same six-product determinant, exactly two reduced fractions.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+=f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 return out+'\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='markdown');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
 rows=[generate(l,args.seed+n,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for n in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
