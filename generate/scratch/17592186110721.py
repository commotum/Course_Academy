#!/usr/bin/env python3
"""General linear identity parameters; read-only local JSON/Markdown generator.

Easy: two independent one-operation matches (shift/scale/direct), including
source rational values. Moderate: one sign-reversing match and one nonunit
scale, then a signed sum. Hard (authored): two nonunit affine matches, with
nonzero offsets and at least one proper rational result. No coupled systems.
Raw source profiles preserve missing attributes;
these profiles are evidence-only and never sampled by a normal entrypoint.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186110721
KP_UUID='4b1fd794-f42b-5316-80e9-0698cb1f8b87'
TITLE='Solving a General Equation With Infinitely Many Solutions For Unknown Parameters'
VERSION='general-identity-3'
PACKAGE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((PACKAGE/'source.json').read_text())['record'][':knowledge-point/questions']}
# The six coefficients describe (a*u+b)x+(d*v+e)=c*x+f.
SOURCE_CASES={
 'q-287978':('easy','p','q',[1,-3,4,1,0,1]),
 'q-287985':('easy','p','q',[1,-5,2,2,0,6]),
 'q-288583':('moderate','t','m',[2,0,6,-1,1,4]),
 'q-288584':('moderate','s','t',[-1,3,1,2,0,6]),
 'q-288622':('easy','m','n',[1,2,7,5,0,15]),
 'q-288623':('easy','k','r',[2,0,9,1,0,6]),
 'q-288627':('easy','p','q',['1/2',0,4,1,0,20]),
}
TEMPLATES={l:[m for m,v in SOURCE_CASES.items() if v[0]==l] for l in ('easy','moderate')};TEMPLATES['hard']=['affine-pair']
NORMAL_PROFILES=('method-sum','method-components','blank')
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(obj)))
def tex(n):return sp.latex(sp.Rational(n)).replace('- ','-')
def rat(n):
 try:return sp.Rational(n)
 except Exception as e:raise ValueError('exact rational parameter required') from e
def linear(a,b,v,reverse=False,spaces=False):
 a,b=rat(a),rat(b)
 if a==1:t=v
 elif a==-1:t='-'+v
 elif a.p==1 and a.q>1:t=r'\frac{'+v+'}{'+str(a.q)+'}'
 else:t=tex(a)+v
 if reverse:t=tex(b)+('' if t.startswith('-') else '+')+t if b else t
 elif b:t+=('+' if b>0 else '')+tex(b)
 if spaces:t=t.replace('+',' + ').replace('-', ' - ').strip()
 return t

def components(template,p):
 a,b,c,d,e,f=p
 u,v=('k','r') if template=='affine-pair' else SOURCE_CASES[template][1:3]
 old=template in ('q-287978','q-287985')
 L=linear(a,b,u,spaces=old);R=linear(d,e,v,reverse=template=='q-288583',spaces=old)
 lx=('('+L+')' if b else L)+'x';rx='x' if c==1 else tex(c)+'x'
 if old:eq=lx+' + '+R+' = '+rx+' + '+tex(f)
 else:eq=lx+'+'+('('+R+')' if e else R)+'='+rx+('+' if f>=0 else '')+tex(f)
 return u,v,L,R,eq

def render(template,p,field_type):
 u,v,L,R,eq=components(template,p);a,b,c,d,e,f=p;U=(c-b)/a;V=(f-e)/d;T=U+V
 if template in SOURCES:
  source=SOURCES[template];oldp=list(map(rat,SOURCE_CASES[template][3]));ou,ov,oL,oR,oeq=components(template,oldp)
  prompt=source[':question/problem'].replace(oeq,eq)
  if ':question/worked-solution' in source:
   # Component masks preserve every shared sentence and source row omission.
   blocks=re.findall(r'\$\$\n(.*?)\n\$\$',source[':question/worked-solution'],re.S)
   us=(r'\begin{aligned}'+u+' & ='+tex(U)+r'.\end{aligned}') if template.startswith('q-28862') else u+'='+tex(U)+'.'
   vs=(r'\begin{aligned}'+v+' & ='+tex(V)+r'.\end{aligned}') if template=='q-288622' else v+'='+tex(V)+'.'
   add=lambda z:'('+tex(z)+')' if z<0 else tex(z)
   stages=[blocks[0],blocks[1],eq,L+'='+tex(c)+'.',us,R+'='+tex(f)+'.']
   if len(blocks)==8:stages.append(vs)
   stages.append(u+'+'+v+'='+tex(U)+'+'+add(V)+'='+tex(T)+'.')
   it=iter(stages)
   solution=re.sub(r'\$\$\n(.*?)\n\$\$',lambda _: '$$\n'+next(it)+'\n$$',source[':question/worked-solution'],flags=re.S)
   solution=re.sub(r'Finally, since .*?we have',lambda _: 'Finally, since $'+u+'='+tex(U)+'$ and $'+v+'='+tex(V)+',$ we have',solution)
  else:solution=shared_solution(u,v,L,R,eq,c,f,U,V,T)
 else:
  prompt='Consider the equation\n\n$$\n'+eq+'\n$$\n\nwhere $'+u+'$ and $'+v+'$ are constants. Given that this equation has infinitely many solutions, what is the value of $'+u+'+'+v+'?$'
  solution=shared_solution(u,v,L,R,eq,c,f,U,V,T)
 # Normal field overrides are presentation extensions, preserving original sums.
 if field_type:
  prompt=re.sub(r'\n\n\$[^$]*=\$\n\{\{field-1\}\}$','',prompt)
  prompt=re.sub(r'\$p \+ q =\$\n\{\{field-1\}\}$','',prompt)
  if field_type=='blank':prompt+='\n\n$'+u+'+'+v+'=$\n{{field-1}}'
 return prompt,solution,(U,V,T)

def shared_solution(u,v,L,R,eq,c,f,U,V,T):
 # Authored missing-solution completion uses the observed formal rule and prose.
 parts=['Suppose we have an equation of the form','$$\nax+b=cx+d\n$$','where $a,b,c,$ and $d$ are constants. This equation has infinitely many solutions if ','$$\na=c\\,\\text{and}\\,b=d.\n$$','To determine the values of $'+u+'$ and $'+v+'$ such that the equation','$$\n'+eq+'\n$$','has infinitely many solutions, we equate the coefficients of $x,$ and we equate the constants:','- Equating the coefficients of $x,$ we have','$$\n'+L+'='+tex(c)+'.\n$$','Solving this equation for $'+u+',$ we get','$$\n'+u+'='+tex(U)+'.\n$$','- Equating the constants, we have','$$\n'+R+'='+tex(f)+'.\n$$','Solving this equation for $'+v+',$ we get','$$\n'+v+'='+tex(V)+'.\n$$','Finally, since $'+u+'='+tex(U)+'$ and $'+v+'='+tex(V)+',$ we have','$$\n'+u+'+'+v+'='+tex(U)+'+'+('('+tex(V)+')' if V<0 else tex(V))+'='+tex(T)+'.\n$$']
 return '\n\n'.join(parts)

def bank(profile,p):
 a,b,c,d,e,f=p;U=(c-b)/a;V=(f-e)/d;T=U+V
 # Complete authored operation banks; no ad hoc perturbation or recipe pool.
 if profile=='method-sum':return [T,U,V,c+f,U-V]
 if profile=='method-components':return [T,c/a+V,U+f/d,a*(c-b)+V,U+d*(f-e)]
 if profile=='blank':return [T]
 # Explicit observed numeric patterns, with underdetermined intent. Never default.
 mid=profile.split(':',1)[1]
 if mid=='q-287978':return [U,-b,U+2*V,T,c]
 if mid=='q-287985':return []
 if mid in ('q-288583','q-288584'):return [T]
 if mid=='q-288622':return [f,T,U,2*V,c]
 if mid=='q-288623':return [a*c,U,U+f-a,f*a*a,T]
 if mid=='q-288627':return [c+f,T,T/2,f,3*f/2]
 raise ValueError('unknown source profile')

def fingerprint(p):
 a,b,c,d,e,f=p
 # Full normalized displayed coefficient/constant equalities, not only roots.
 # Common nonzero scaling is normalized; bank/profile/layout/seed/name excluded.
 return digest(['general-linear-identity',*[str(z) for z in (b/a,c/a,e/d,f/d)]])

def guard(level,template,p,raw=False):
 if len(p)!=6:raise ValueError('six coefficients required')
 a,b,c,d,e,f=p
 if not a or not d:raise ValueError('nonzero parameter multipliers required')
 U,V=(c-b)/a,(f-e)/d
 if max(abs(z) for z in p)>120 or any(z.q>8 for z in p) or max(abs(U),abs(V))>30:raise ValueError('bounded exact object policy')
 if raw:return
 if level=='easy':
  if not(0<c<=12 and 0<f<=60 and 0<U<=15 and 0<V<=24 and e==0):raise ValueError('easy reduced bounds')
  if template in ('q-287978','q-287985','q-288622'):
   if a!=1 or not 1<=abs(b)<=8 or not 1<=d<=6 or U.q!=1 or V.q!=1:raise ValueError('easy shift/scale shape')
   if template=='q-287978' and (b>=0 or d!=1):raise ValueError('shift-unit shape')
   if template=='q-287985' and (b>=0 or d<2):raise ValueError('shift-scale shape')
   if template=='q-288622' and (b<=0 or d<2):raise ValueError('shift-scale shape')
  elif template=='q-288623':
   if b or d!=1 or not 2<=a<=6 or a.q!=1 or U.q==1:raise ValueError('easy nonintegral scale shape')
  elif template=='q-288627':
   if b or d!=1 or a.p!=1 or not 2<=a.q<=4:raise ValueError('easy reciprocal shape')
 if level=='moderate':
  if not all(z.q==1 for z in p) or max(abs(z) for z in (b,e))>8 or max(abs(c),abs(f))>72 or not 1<=U<=12 or U.q!=1 or V.q!=1 or not 1<=abs(V)<=12:raise ValueError('moderate reduced bounds')
  if template=='q-288583' and not (2<=a<=6 and b==0 and d==-1 and 1<=e<=8 and V<0):raise ValueError('moderate signed constant shape')
  if template=='q-288584' and not (a==-1 and 1<=b<=8 and 1<=c<=8 and 2<=d<=6 and e==0 and V>0):raise ValueError('moderate signed coefficient shape')
 if level=='hard':
  if sp.igcd(sp.igcd(a,b),c)!=1 or sp.igcd(sp.igcd(d,e),f)!=1:raise ValueError('hard affine equalities must be primitive')
  if template!='affine-pair' or not all(z.q==1 for z in p) or not(2<=abs(a)<=6 and 2<=abs(d)<=6 and 1<=abs(b)<=8 and 1<=abs(e)<=8 and 1<=abs(c)<=24 and 1<=abs(f)<=24) or not(0<abs(U)<=12 and 0<abs(V)<=12) or (U.q==V.q==1):raise ValueError('hard reduced two-affine rational bounds')

def sample(level,template,rng):
 if level=='easy':
  c=rng.randint(1,12);f=rng.randint(1,24)
  if template=='q-287978':return [1,-rng.randint(1,8),c,1,0,f]
  if template=='q-287985':
   d=rng.randint(2,6);return [1,-rng.randint(1,8),c,d,0,d*rng.randint(1,10)]
  if template=='q-288622':
   b=rng.randint(1,8);d=rng.randint(2,6);return [1,b,c,d,0,d*rng.randint(1,10)]
  if template=='q-288623':return [rng.randint(2,6),0,c,1,0,f]
  return [sp.Rational(1,rng.randint(2,4)),0,c,1,0,f]
 if level=='moderate':
  U=rng.randint(1,12);V=rng.randint(1,12);scale=rng.randint(2,6);shift=rng.randint(1,8)
  return [scale,0,scale*U,-1,shift,shift+V] if template=='q-288583' else [-1,shift,shift-U,scale,0,scale*V]
 return [rng.choice([-1,1])*rng.randint(2,6),rng.choice([-1,1])*rng.randint(1,8),rng.choice([-1,1])*rng.randint(1,24),rng.choice([-1,1])*rng.randint(2,6),rng.choice([-1,1])*rng.randint(1,8),rng.choice([-1,1])*rng.randint(1,24)]

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('level must be easy, moderate or hard')
 rng=random.Random(seed);template=template or rng.choice(TEMPLATES[level])
 if template not in TEMPLATES[level]:raise ValueError('template level mismatch')
 raw=bool(profile and profile.startswith('raw:'))
 if raw and profile!='raw:'+template:raise ValueError('raw profile must match source template')
 if field_type and field_type.startswith(':answer-field.type/'):field_type=field_type.split('/')[-1]
 if field_type not in (None,'blank','radio'):raise ValueError('only source radio/blank types supported')
 if raw and field_type:raise ValueError('raw layout cannot be overridden')
 source=SOURCES.get(template)
 original_type=source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1] if source else 'blank'
 kind=original_type if raw else field_type or original_type
 profile=profile or ('blank' if kind=='blank' else 'method-sum')
 if not raw and profile not in NORMAL_PROFILES:raise ValueError('unknown normal profile')
 if not raw and profile=='method-components' and level!='hard':raise ValueError('component bank requires both nonzero affine offsets')
 if not raw and (profile=='blank')!=(kind=='blank'):raise ValueError('profile/field mismatch')
 if parameters is None:
  for _ in range(10000):
   p=list(map(rat,sample(level,template,rng)))
   try:
    guard(level,template,p,raw);vals=bank(profile,p)
    if len(set(vals))!=len(vals):continue
    break
   except ValueError:continue
  else:raise ValueError('bounded complete-bank sampling exhausted')
 else:
  p=list(map(rat,[parameters[k] for k in ('a','b','c','d','e','f')] if isinstance(parameters,dict) else parameters));guard(level,template,p,raw);vals=bank(profile,p)
  if len(set(vals))!=len(vals):raise ValueError('whole bank rejected: equivalent options')
 prompt,solution,(U,V,T)=render(template,p,None if raw else kind)
 missing=raw and template in ('q-287978','q-287985')
 key=source[':question/answer-fields'][0][':answer-field/key'] if raw else 'field-1' if kind=='blank' else 'selection'
 values=[tex(z) for z in vals]
 content={'version':VERSION,'level':None if missing else level,'prompt':prompt,'solution':None if missing else solution,'fields':[(key,kind,sorted(values),None if missing else tex(T))]}
 qid=ident(content);fid=ident([qid,'field',key]);answers=[{':answer/id':ident([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
 if answers or not missing:field[':answer-field/choices']=answers
 if not missing:
  correct_value=tex(T)
  field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct_value)]
 if kind=='radio':rng.shuffle(answers)
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if not missing:question.update({':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(z) for k,z in zip(('a','b','c','d','e','f'),p)},'domain':'x and both parameters real','source_ids':[template] if source else ['e-18852'],'provenance':'raw observed evidence' if raw else 'authored completion/extension','eligible_for_normal_practice':not raw,'bank_interpretation':'source numeric-pattern replay; intent underdetermined' if raw else 'authored complete method-error operations','mathematical_fingerprint':fingerprint(p),'content_fingerprint':digest(content),'sympy':sp.__version__}}

# Easy — independent one-operation parameter matches.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate — independent signed matching and scaling; no harder algebra branch.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard — authored two affine matches, a rational result and the same final sum.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
 q=rec['question'];choices='\n'.join('- $'+a[':answer/value']+'$' for f in q[':question/answer-fields'] if f[':answer-field/type'].endswith('/radio') for a in f.get(':answer-field/choices',[]));return q[':question/problem']+('\n\n'+choices if choices else '')+'\n\n'+q.get(':question/worked-solution','[Source omits worked solution.]')
def batch(level,count,seed,**kwargs):
 if count<1:raise ValueError('positive count required')
 records=[];seen=set()
 for i in range(count*200+100):
  rec=generate(level,seed+i,**kwargs);fp=rec['generation']['mathematical_fingerprint']
  if fp in seen:continue
  records.append(rec);seen.add(fp)
  if len(records)==count:return records
 raise ValueError('finite bounded meaningful domain exhausted')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='json');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args();levels=TEMPLATES if args.difficulty=='all' else [args.difficulty];records=[rec for level in levels for rec in batch(level,args.count,args.seed,template=args.template,profile=args.profile)];print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
