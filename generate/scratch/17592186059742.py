#!/usr/bin/env python3
"""Two scalar products, then entrywise matrix combination (math basis 2275).
Evidence profiles reproduce original omissions and are ineligible for learning.
Normal profiles complete missing metadata with explicitly authored same-method banks.
No EDB access, registration, plots, or transactions. See adjacent extraction/validation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
import sympy as S
KP_ID=17592186059742
KP_UUID='a6727fdd-a614-5ead-9273-08c0a7fec997'
TITLE='Calculating a Linear Combination of Two Matrices'
VERSION='linear-matrix-combination-1'
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Every family has its own observed prompt layout, response contract and arithmetic masks.
TEMPLATES={
 'easy_integer':('easy',2,2,'radio',None),
 'symmetric_plus':('moderate',2,2,'radio','q-11534'),
 'opaque_subtract':('moderate',2,2,'radio','q-11536'),
 'subtract_square':('moderate',2,2,'radio','q-11532'),
 'half_plus':('moderate',2,2,'radio','q-11531'),
 'negative_plus':('moderate',2,2,'radio','q-126009'),
 'row_blank':('hard',1,4,'blank','q-320656'),
 'partial_blank':('hard',2,3,'blank','q-320671'),
 'rect_radio':('hard',2,3,'radio','q-69642')}
DEFAULTS={
 'easy_integer':dict(a='2',b='3',op='+',A=[[1,2],[3,0]],B=[[3,1],[2,4]],names=['A','B']),
 'symmetric_plus':dict(a='4',b='6',op='+',A=[[-1,1],[1,-1]],B=[[2,-2],[-2,2]],names=['A','B']),
 'opaque_subtract':dict(a='2',b='3',op='-',A=[[2,1],[-2,-1]],B=[[2,1],[1,-1]],names=['P','Q']),
 'subtract_square':dict(a='2',b='3',op='-',A=[[3,-2],[2,-1]],B=[[0,1],[2,1]],names=['H','L']),
 'half_plus':dict(a='3',b='1/2',op='+',A=[[1,3],[-2,2]],B=[[2,0],[4,6]],names=['F','G']),
 'negative_plus':dict(a='-1',b='2',op='+',A=[[3,1],[1,0]],B=[[0,-2],[-2,2]],names=['A','B']),
 'row_blank':dict(a='4',b='1/2',op='-',A=[[4,-1,0,2]],B=[[2,0,4,-6]],names=['F','G']),
 'partial_blank':dict(a='2/3',b='2',op='+',A=[[6,0,15],[-12,6,0]],B=[[3,-1,0],[-2,'1/2',-1]],names=['M','N'],targets=[0,2,4,5]),
 'rect_radio':dict(a='1/3',b='2',op='+',A=[[3,6,15],[-12,9,6]],B=[[1,2,5],[3,4,6]],names=['G','H'])}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'linear-matrix:'+x))
def tex(x):return S.latex(S.Rational(x))
def group(x):return '('+tex(x)+')' if S.Rational(x)<0 else tex(x)
def mat(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(str(x) for x in row) for row in rows)+r'\end{bmatrix}'
def matrix(values,r,c):return mat([values[i*c:(i+1)*c] for i in range(r)])
def term(a,name):return name if a==1 else '-'+name if a==-1 else tex(a)+name
def expression(p):return term(S.Rational(p['a']),p['names'][0])+p['op']+term(S.Rational(p['b']),p['names'][1])
def normalize(p):
 if set(p)-{'a','b','op','A','B','names','targets'}:raise ValueError('unknown parameter keys')
 return dict(a=str(S.Rational(p['a'])),b=str(S.Rational(p['b'])),op=p['op'],A=[[str(S.Rational(x)) for x in row] for row in p['A']],B=[[str(S.Rational(x)) for x in row] for row in p['B']],names=list(p['names']),**({'targets':list(p['targets'])} if 'targets'in p else {}))
def guard(name,p):
 level,r,c,kind,_=TEMPLATES[name]
 if 'targets'in p and name!='partial_blank':raise ValueError('targets only in partial blank family')
 a,b=S.Rational(p['a']),S.Rational(p['b'])
 if p['op'] not in ('+','-') or len(p['A'])!=r or len(p['B'])!=r or any(len(row)!=c for row in p['A']+p['B']):raise ValueError('matrix shape/operator')
 if name in ('symmetric_plus','half_plus','negative_plus','partial_blank','rect_radio','easy_integer') and p['op']!='+':raise ValueError('family addition backbone')
 if name in ('opaque_subtract','subtract_square','row_blank') and p['op']!='-':raise ValueError('family subtraction backbone')
 if len(p['names'])!=2 or len(set(p['names']))!=2 or any(len(n)!=1 or not n.isupper() or not n.isascii() for n in p['names']):raise ValueError('two distinct matrix labels')
 A=[S.Rational(x) for row in p['A'] for x in row];B=[S.Rational(x) for row in p['B'] for x in row]
 if not any(A) or not any(B):raise ValueError('both scalar products must contribute')
 if name=='easy_integer':
  if not(a in (2,3) and b in (2,3) and p['op']=='+' and all(x.q==1 and 0<=x<=4 for x in A+B)):raise ValueError('authored easy bounds')
 elif level=='moderate':
  if name=='half_plus' and not(a in (2,3,4,5,6) and b==S.Rational(1,2)):raise ValueError('observed half-scalar family')
  if name=='negative_plus' and not(a in (-1,-2,-3) and b in (2,3,4,5,6)):raise ValueError('negative first scalar family')
  if name in ('symmetric_plus','opaque_subtract','subtract_square') and not(a in (2,3,4,5,6) and b in (2,3,4,5,6)):raise ValueError('two positive integer scalar family')
  if not(a<0 or b.q>1 or any(x<0 for x in A+B)):raise ValueError('moderate signed or half-scalar workload')
  if not(0<abs(a)<=6 and a.q==1 and 0<b<=6 and b.q in (1,2) and all(x.q==1 and abs(x)<=6 for x in A+B) and all((b*x).q==1 for x in B)):raise ValueError('moderate eight-product arithmetic bounds')
 elif name=='row_blank':
  if not(a in (2,3,4) and b==S.Rational(1,2) and p['op']=='-' and all(x.q==1 and abs(x)<=6 for x in A+B) and all((b*x).q==1 for x in B)):raise ValueError('hard four-entry row workload')
 else:
  if not(a in (S.Rational(1,3),S.Rational(2,3)) and b==2 and p['op']=='+' and all(x.q==1 and abs(x)<=18 and (a*x).q==1 for x in A) and all(x.q in (1,2) and abs(x)<=6 and (b*x).q==1 for x in B)):raise ValueError('hard six-entry workload')
 if name=='partial_blank' and (len(p.get('targets',[]))!=4 or sorted(set(p['targets']))!=sorted(p['targets']) or any(not isinstance(x,int) or not 0<=x<6 for x in p['targets'])):raise ValueError('four ordered distinct target slots')
 return a,b,A,B

def solution(name,p):
 a,b,A,B=guard(name,p);r,c=TEMPLATES[name][1:3];op=p['op'];expr=expression(p);X=[a*x for x in A];Y=[b*x for x in B];C=[x+y if op=='+' else x-y for x,y in zip(X,Y)]
 rows=[group(a)+matrix(list(map(tex,A)),r,c)+op+tex(b)+matrix(list(map(tex,B)),r,c),matrix([group(a)+r'\cdot '+group(x) for x in A],r,c)+op+matrix([tex(b)+r'\cdot '+group(x) for x in B],r,c),matrix(list(map(tex,X)),r,c)+op+matrix(list(map(tex,Y)),r,c)]
 # Source partial 2x3 uses subtraction shorthand for adding a negative; -A+2B keeps +(-v).
 cells=[]
 for x,y in zip(X,Y):
  if name=='partial_blank' and op=='+' and y<0:cells.append(tex(x)+'-'+tex(-y))
  else:cells.append(tex(x)+op+group(y))
 rows += [matrix(cells,r,c),matrix(list(map(tex,C)),r,c)]
 intro=f"We multiply each entry of ${p['names'][0]}$ by ${tex(a)}$ and each entry of ${p['names'][1]}$ by ${tex(b)},$ and then {'add' if op=='+' else 'subtract'} the resulting matrices, as follows:"
 return intro+'\n\n$$\n'+r'\begin{aligned}'+expr+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$',C

def prompt(name,p,C,raw=False):
 r,c=TEMPLATES[name][1:3];expr=expression(p);aa=mat([[tex(x) for x in row]for row in p['A']]);bb=mat([[tex(x)for x in row]for row in p['B']]);n,m=p['names']
 if name in ('symmetric_plus','opaque_subtract'):
  # Observed unrated source spacing is a family presentation slot, not payload lookup.
  expr=term(S.Rational(p['a']),n)+' '+p['op']+' '+term(S.Rational(p['b']),m)
  out=f'Calculate ${expr}$, where\n${n} = {aa}$\nand\n${m} = {bb}$.'
 else:out=f'Calculate ${expr}$, where\n${n}={aa}$\nand\n${m}={bb}.$'
 if name=='row_blank':out+='\n\n| $'+expr+r'=\,\,$ |  | '+' | '.join('{{field-'+str(i+1)+'}}' for i in range(4))+' |  |\n| --- | --- | --- | --- | --- | --- | --- |'
 if name=='partial_blank':
  targets=p['targets'];items=['{{field-'+str(targets.index(i)+1)+'}}' if i in targets else '$'+tex(C[i])+'$' for i in range(6)]
  out+='\n\n| $'+expr+r'=\,\,$ |  | '+' | '.join(items[:3])+' |  |\n| --- | --- | --- | --- | --- | --- |\n'+('|  | ' if raw else '|  |  | ')+' | '.join(items[3:])+(' |  |  |' if raw else ' |  |')
 return out

def bank(name,p,profile,C):
 a,b,A,B=guard(name,p);sgn=1 if p['op']=='+' else -1;X=[a*x for x in A];Y=[b*x for x in B]
 if profile=='method':return [C,[x-sgn*y for x,y in zip(X,Y)],[u+sgn*y for u,y in zip(A,Y)],[x+sgn*v for x,v in zip(X,B)],[sgn*y for y in Y]]
 if profile!='observed-'+TEMPLATES[name][4]:raise ValueError('unsupported complete bank profile')
 if name=='symmetric_plus':return [[-x for x in C],[-C[0],C[1],C[2],C[3]],[C[0],-C[1],-C[2],C[3]],C,[C[0],C[1],C[2],-C[3]]]
 if name=='half_plus':return [[-C[0],C[1],C[2],C[3]],[C[0],-C[1],C[2],C[3]],[C[0],C[1],C[3],C[2]],[C[0],C[1],C[2],-C[3]],C]
 if name=='opaque_subtract':return [[C[0],C[1],B[2],-B[3]],[C[0],C[1],C[2],B[3]],[C[0],C[1],-B[2],-B[3]],C,[C[0],C[1],-B[2],B[3]]]
 if name=='negative_plus':return [[C[0],X[1],C[2],B[3]],[X[i]-Y[i] for i in range(4)],[b,C[1],Y[2],C[3]],C,[A[2],X[1]-Y[1],X[2]-Y[2],-Y[3]]]
 if name=='rect_radio':return [[C[i]for i in (0,2,1,3,5,4)],C,[C[i]for i in (0,1,5,3,4,2)],[C[0],X[1],X[2],C[3],C[4],X[5]+Y[4]],[X[0],C[1],C[2],X[3]+Y[0],C[4],C[5]]]
 raise ValueError('no observed radio bank')

# Authored easy: eight nonnegative integer products and four entrywise additions.
def sample_easy(rng):
 return dict(a=str(rng.choice((2,3))),b=str(rng.choice((2,3))),op='+',A=[[rng.randrange(5)for _ in range(2)]for _ in range(2)],B=[[rng.randrange(5)for _ in range(2)]for _ in range(2)],names=rng.sample(list('ABFGHLMNPQ'),2))
# Moderate: preserve every observed square family, signed inputs and cancellation-friendly half scalar.
def sample_moderate(name,rng):
 p=dict(DEFAULTS[name]);p['names']=rng.sample(list('ABFGHLMNPQ'),2);p['a']=str(rng.choice((-1,-2,-3) if name=='negative_plus' else (2,3,4,5,6)));p['b']='1/2' if name=='half_plus' else str(rng.choice((2,3,4,5,6)))
 p['A']=[[rng.randint(-6,6)for _ in range(2)]for _ in range(2)];d=S.Rational(p['b']).q;p['B']=[[d*rng.randint(-3,3)for _ in range(2)]for _ in range(2)];return p
# Hard: own four-blank row family and six-cell families; partial asks four/gives two.
def sample_hard(name,rng):
 p=dict(DEFAULTS[name]);p['names']=rng.sample(list('ABFGHLMNPQ'),2);r,c=TEMPLATES[name][1:3]
 if name=='row_blank':p['a']=str(rng.choice((2,3,4)));p['A']=[[rng.randint(-6,6)for _ in range(4)]];p['B']=[[2*rng.randint(-3,3)for _ in range(4)]]
 else:
  p['a']=rng.choice(('1/3','2/3'));p['A']=[[3*rng.randint(-6,6)for _ in range(c)]for _ in range(r)];p['B']=[[str(S.Rational(rng.randint(-6,6),2))for _ in range(c)]for _ in range(r)]
  if name=='partial_blank':p['targets']=sorted(rng.sample(range(6),4))
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed);eligible=[n for n,t in TEMPLATES.items()if t[0]==level and (field_type is None or t[3]==field_type)]
 if not eligible:raise ValueError('field type unsupported')
 if template is None and profile and profile.startswith('observed-'):
  template=next((n for n in eligible if profile=='observed-'+str(TEMPLATES[n][4])),None)
  if template is None:raise ValueError('profile/level mismatch')
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('template/level/field mismatch')
 kind=TEMPLATES[name][3];raw=bool(profile and profile.startswith('observed-'));profile=profile or ('blank' if kind=='blank' else 'method')
 if raw and TEMPLATES[name][4] is None:raise ValueError('no observed profile for authored family')
 if kind=='blank' and profile not in ('blank','observed-'+TEMPLATES[name][4]):raise ValueError('blank profile')
 if name=='subtract_square' and raw:pass
 elif kind=='radio' and profile!='method' and profile!='observed-'+str(TEMPLATES[name][4]):raise ValueError('radio profile')
 for attempt in range(1000):
  p=normalize(parameters if parameters is not None else sample_easy(rng) if level=='easy' else sample_moderate(name,rng) if level=='moderate' else sample_hard(name,rng))
  try:guard(name,p)
  except ValueError:
   if parameters is not None:raise
   continue
  sol,C=solution(name,p);problem=prompt(name,p,C,raw=raw)
  values=[] if raw and name=='subtract_square' else [[x]for x in C]if kind=='blank' else bank(name,p,profile,C)
  if kind=='radio' and len({tuple(v)for v in values})!=len(values):
   if parameters is not None:raise ValueError('complete bank collision')
   continue
  break
 else:raise ValueError('no eligible whole instance')
 r,c=TEMPLATES[name][1:3];targets=p.get('targets',list(range(r*c)))
 solution_missing=raw and name in ('symmetric_plus','opaque_subtract');difficulty_missing=solution_missing;fields_missing=raw and name=='subtract_square';correct_missing=solution_missing
 rendered=[tex(C[i])for i in targets]if kind=='blank' else [matrix(list(map(tex,v)),r,c)for v in values]
 identity=digest({'version':VERSION,'level':None if difficulty_missing else level,'problem':problem,'solution':None if solution_missing else sol,'bank':sorted(rendered),'fields_present':not fields_missing,'correct_present':not correct_missing})
 q={':question/id':ident(identity),':question/problem':problem}
 if not difficulty_missing:q[':question/difficulty']=':question.difficulty/'+level
 if not solution_missing:q[':question/worked-solution']=sol
 if not fields_missing:
  fs=[]
  for i in range(4 if kind=='blank' else 1):
   key='field-'+str(i+1)if kind=='blank' else 'selection';fid=ident(identity+':'+key);vv=[rendered[i]]if kind=='blank' else rendered
   ans=[{':answer/id':ident(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v}for v in vv];correct=ans[0][':answer/id']if kind=='blank'else next(a[':answer/id']for a,v in zip(ans,values)if v==C)
   if kind=='radio':rng.shuffle(ans)
   f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':ans}
   if not correct_missing:f[':answer-field/correct']=[':answer/id',correct]
   fs.append(f)
  q[':question/answer-fields']=fs
 mathematical=digest({'A':p['A'],'B':p['B'],'a':p['a'],'signed_b':str(S.Rational(p['b'])*(1 if p['op']=='+' else -1)),'targets':targets if kind=='blank' else 'whole','response':kind})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':name,'bank_profile':profile,'parameters':p,'content_hash':identity,'math_fingerprint':mathematical,'evidence_only':raw,'eligible_for_learning':not raw,'authored_level_assignment':name=='easy_integer' or name in ('symmetric_plus','opaque_subtract'),'source_ids':[TEMPLATES[name][4]]if TEMPLATES[name][4]else [],'runtime':{'python':sys.version.split()[0],'sympy':S.__version__}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):parts.append(f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$'for a in f[':answer-field/choices']))
 parts.append(q.get(':question/worked-solution','(Original solution absent)'));return '\n\n'.join(parts)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();records=[generate(level,args.seed+i,template=args.template,profile=args.profile)for level in (('easy','moderate','hard')if args.difficulty=='all'else(args.difficulty,))for i in range(args.count)];print(json.dumps(records,indent=2)if args.format=='json'else '\n\n---\n\n'.join(map(markdown,records)))
