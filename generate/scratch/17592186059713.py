#!/usr/bin/env python3
"""Alternative vector notation; local steps 3–7 generator, no database operations.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard expose the same keyword arguments.
CLI: --difficulty easy|moderate|hard|all --seed N --count N --format markdown|json
and optional --template/--profile. Raw evidence profiles preserve source omissions.
Normal radio profiles use five complete operation-derived choices selected BEFORE
sampling. Whole-bank collisions reject explicit inputs or resample sampled inputs.
Fixed prompt/solution/bank/level determine identities independent of seed/order.
Exact arithmetic: SymPy Integer/Matrix; source and authored scopes in README.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059713
KP_UUID='fc55e44b-82d0-5145-8a24-d43bc60dc594'
TITLE='Calculating Sums and Scalar Multiplication of Vectors Given in Alternative Notation'
VERSION='alternative-vector-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
OPENING='To compute the result, we just need to perform the required operations with each component separately:'
TEMPLATES={'sum_lower':'easy','sum_upper':'easy','subtract':'easy','scalar':'easy','linear_combination':'moderate','nested_combination':'hard'}
PROFILES={'sum_lower':['component_bank','raw-q-1300'], 'sum_upper':['component_bank','raw-q-1324'], 'subtract':['component_bank','raw-q-1323'], 'scalar':['scalar_source_bank','raw-q-1386'], 'linear_combination':['distribution_bank'], 'nested_combination':['nested_bank']}
SOURCE_PARAMS={'q-1300':{'a':[-3,1],'b':[4,6]},'q-1324':{'a':[1,3],'b':[6,3]},'q-1323':{'a':[4,1],'b':[1,-4]},'q-1386':{'a':[8,-7],'p':3}}
SOURCE_TEMPLATE={'q-1300':'sum_lower','q-1324':'sum_upper','q-1323':'subtract','q-1386':'scalar'}

def uid(data): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(data,sort_keys=True,ensure_ascii=False)))
def tex(x): return str(x)
def vec(x, style='normal'):
 x,y=map(str,x)
 if style=='raw-sub': return f'⟨ - {abs(int(x))},{y}⟩' if int(x)<0 else f'⟨{x}, {y}⟩'
 return f'⟨{x},{y}⟩'
def bracket(x): return f'({x})' if int(x)<0 else str(x)
def label(name,style):
 if style=='historic': return name+'^(→)'
 return r'\overset{\to }{'+name+'}'
def matrix(v): return sp.Matrix([sp.Integer(x) for x in v])
def aslist(v): return [int(x) for x in v]
def expression(t,p,style):
 a,b,c=[label(n,style) for n in (('U','V','W') if t=='sum_upper' else ('u','v','w'))]
 if t.startswith('sum'): return a+'+'+b
 if t=='subtract': return a+' - '+b
 if t=='scalar': return str(p['p'])+label('v',style)
 if t=='linear_combination': return str(p['p'])+a+('+' if p['s']==1 else '-')+str(p['q'])+b
 return str(p['p'])+a+'-('+str(p['q'])+b+('+' if p['s']==1 else '-')+str(p['r'])+c+')'

def validate_parameters(level,t,p,raw=False):
 needed={'a','b'} if t.startswith('sum') or t=='subtract' else {'a','p'} if t=='scalar' else {'a','b','p','q','s'} if t=='linear_combination' else {'a','b','c','p','q','r','s'}
 if set(p)!=needed: raise ValueError(f'parameters require exactly {sorted(needed)}')
 for k in needed:
  if k in 'abc':
   if not isinstance(p[k],(list,tuple)) or len(p[k])!=2 or any(type(x)!=int for x in p[k]): raise ValueError('vectors require two integer coordinates')
  elif type(p[k])!=int: raise ValueError('integer coefficients required')
 if any(abs(x)> (9 if level=='easy' else 6) for k in needed if k in 'abc' for x in p[k]): raise ValueError('coordinate bound exceeded')
 if t=='scalar' and not 2<=abs(p['p'])<=6: raise ValueError('easy scalar magnitude 2–6')
 if level in ('moderate','hard'):
  if any(x==0 for k in needed if k in 'abc' for x in p[k]): raise ValueError('nonzero coordinates retain every component product')
  if any(not 2<=p[k]<= (6 if level=='moderate' else 4) for k in needed if k in 'pqr'): raise ValueError('nonunit positive scalar bound exceeded')
  if p['s'] not in (-1,1): raise ValueError('s must be ±1')

def compute(t,p):
 a=matrix(p['a']); b=matrix(p.get('b',[0,0])); c=matrix(p.get('c',[0,0]))
 if t.startswith('sum'): return a+b
 if t=='subtract': return a-b
 if t=='scalar': return p['p']*a
 if t=='linear_combination': return p['p']*a+p['s']*p['q']*b
 return p['p']*a-(p['q']*b+p['s']*p['r']*c)

def bank(t,p,profile):
 a=matrix(p['a']); b=matrix(p.get('b',[0,0])); c=matrix(p.get('c',[0,0])); z=compute(t,p)
 if t.startswith('sum'):
  vals=[z,a-b,b-a,sp.Matrix([a[0]+b[0],a[1]-b[1]]),sp.Matrix([a[0]-b[0],a[1]+b[1]])]
  names=['correct','subtract both','reverse subtraction','subtract y','subtract x']
 elif t=='subtract' and profile=='raw-q-1323':
  vals=[z,sp.Matrix([a[0],b[1]]),sp.Matrix([-z[0],a[1]+b[1]]),sp.Matrix([z[0],-z[1]]),sp.Matrix([b[0],a[0]-b[0]])]
  names=['correct','opaque-coordinate selection','opaque mixed operation','flip final y','opaque-coordinate selection and difference']
 elif t=='subtract':
  vals=[z,a+b,b-a,sp.Matrix([a[0]-b[0],a[1]+b[1]]),sp.Matrix([a[0]+b[0],a[1]-b[1]])]
  names=['correct','add both','reverse subtraction','add y','add x']
 elif t=='scalar':
  n=p['p']; vals=[z,-z,a+sp.ones(2,1)*n,sp.Matrix([-z[0],z[1]]),-a-sp.ones(2,1)*n]
  names=['correct','negate scalar','add scalar componentwise','flip scaled x','negate componentwise scalar addition']
 elif t=='linear_combination':
  n,m,s=p['p'],p['q'],p['s'];vals=[z,n*a-s*m*b,a+s*m*b,n*a+s*b,sp.Matrix([n*a[0]+s*m*b[0],a[1]+s*b[1]])]
  names=['correct','reverse combining sign','omit first scalar','omit second scalar','omit both y scalars']
 else:
  n,m,r,s=p['p'],p['q'],p['r'],p['s'];vals=[z,n*a-m*b+s*r*c,n*a+m*b+s*r*c,a-(m*b+s*r*c),n*a-(b+s*c)]
  names=['correct','fail outer minus on last term','omit outer subtraction','omit first scalar','omit inner scalars']
 if len({tuple(v) for v in vals})!=5: raise ValueError('whole-bank collision')
 if any(abs(x)>120 for v in vals for x in v): raise ValueError('whole-bank arithmetic bound')
 return [(name,aslist(v)) for name,v in zip(names,vals)]

def raw_prompt(t,p):
 if t=='scalar': return f"If $v^(→) = ⟨{p['a'][0]},{p['a'][1]}⟩$, then ${p['p']}v^(→) =$"
 if t=='subtract': return f"If $u^(→) = ⟨{p['a'][0]}, {p['a'][1]}⟩$ and $v^(→) = ⟨{p['b'][0]},{p['b'][1]}⟩$, then $u^(→) - v^(→) =$"
 u,v=('U','V') if t=='sum_upper' else ('u','v')
 return f"If ${label(u,'modern')}={vec(p['a'])}$ and ${label(v,'modern')}={vec(p['b'])}$, then ${expression(t,p,'modern')}=$"

def sum_solution(t,p):
 u,v=('U','V') if t=='sum_upper' else ('u','v');a,b=p['a'],p['b'];z=aslist(compute(t,p))
 # Original compact aligned sequence, preserved at all parameter values.
 parts=[f"{expression(t,p,'modern')} & ={vec(a)}+{vec(b)}",f" & =⟨{a[0]}+{bracket(b[0])},{a[1]}+{bracket(b[1])}⟩",f" & ={vec(z)}"]
 return OPENING+'\n\n$$\n'+r'\begin{aligned}'+' \\\\ '.join(parts)+r'\end{aligned}'+'\n$$'

def normal_prompt(t,p):
 if t.startswith('sum'): return raw_prompt(t,p)
 if t in ('subtract','scalar'):
  return raw_prompt(t,p).replace('u^(→)',label('u','modern')).replace('v^(→)',label('v','modern'))
 defs=[f"${label(n,'modern')}={vec(p[k])}$" for n,k in zip(('u','v','w'),'abc') if k in p]
 return 'If '+', '.join(defs[:-1])+' and '+defs[-1]+', then $'+expression(t,p,'modern')+'=$'

def normal_solution(t,p):
 if t.startswith('sum'): return sum_solution(t,p)
 a=p['a'];b=p.get('b');c=p.get('c');z=aslist(compute(t,p));e=expression(t,p,'modern');rows=[]
 if t=='subtract':
  rows=[vec(a)+' - '+vec(b),f'⟨{a[0]}-{bracket(b[0])},{a[1]}-{bracket(b[1])}⟩',vec(z)]
 elif t=='scalar':
  n=p['p'];rows=[bracket(n)+r'\cdot '+vec(a),f'⟨{bracket(n)}\\cdot {bracket(a[0])},{bracket(n)}\\cdot {bracket(a[1])}⟩',vec(z)]
 else:
  n,m,s=p['p'],p['q'],p['s']; op='+' if s==1 else '-';na=[n*x for x in a];mb=[m*x for x in b]
  if t=='linear_combination':
   rows=[f'{n}\\cdot {vec(a)}{op}{m}\\cdot {vec(b)}',f'⟨{n}\\cdot {bracket(a[0])}{op}{m}\\cdot {bracket(b[0])},{n}\\cdot {bracket(a[1])}{op}{m}\\cdot {bracket(b[1])}⟩',f'⟨{na[0]}{op}{bracket(mb[0])},{na[1]}{op}{bracket(mb[1])}⟩',vec(z)]
  else:
   r=p['r'];rc=[r*x for x in c];inner=[mb[i]+s*rc[i] for i in range(2)]
   rows=[f'{n}\\cdot {vec(a)}-({m}\\cdot {vec(b)}{op}{r}\\cdot {vec(c)})',f'⟨{n}\\cdot {bracket(a[0])}-({m}\\cdot {bracket(b[0])}{op}{r}\\cdot {bracket(c[0])}),{n}\\cdot {bracket(a[1])}-({m}\\cdot {bracket(b[1])}{op}{r}\\cdot {bracket(c[1])})⟩',f'{vec(na)}-({vec(mb)}{op}{vec(rc)})',f'{vec(na)}-{vec(inner)}',f'⟨{na[0]}-{bracket(inner[0])},{na[1]}-{bracket(inner[1])}⟩',vec(z)]
 return OPENING+'\n\n$$\n'+r'\begin{aligned}'+e+' &= '+(' \\\\ &= '.join(rows))+r'\end{aligned}'+'\n$$'

def raw_values(t,items):
 if t=='subtract':
  styles=[lambda v:f'⟨{v[0]}, {v[1]}⟩',lambda v:f'⟨{v[0]},{v[1]}⟩',lambda v:f'⟨ - {abs(v[0])},{v[1]}⟩' if v[0]<0 else vec(v),lambda v:vec(v),lambda v:f'⟨{v[0]}, {v[1]}⟩']
 else:
  styles=[lambda v:vec(v),lambda v:f'⟨ - {abs(v[0])}, {v[1]}⟩' if v[0]<0 else vec(v),lambda v:vec(v),lambda v:f'⟨ - {abs(v[0])},{v[1]}⟩' if v[0]<0 else vec(v),lambda v:f'⟨ - {abs(v[0])}, {v[1]}⟩' if v[0]<0 else vec(v)]
 return [f(v) for f,(_,v) in zip(styles,items)]

def sample(t,rng):
 level=TEMPLATES[t];lim=9 if level=='easy' else 6
 vals=list(range(-lim,lim+1)) if level=='easy' else list(range(-lim,0))+list(range(1,lim+1))
 p={'a':[rng.choice(vals),rng.choice(vals)]}
 if t!='scalar': p['b']=[rng.choice(vals),rng.choice(vals)]
 if t=='scalar': p['p']=rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
 if level in ('moderate','hard'): p.update(p=rng.randint(2,6 if level=='moderate' else 4),q=rng.randint(2,6 if level=='moderate' else 4),s=rng.choice([-1,1]))
 if level=='hard': p.update(c=[rng.choice(vals),rng.choice(vals)],r=rng.randint(2,4))
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('invalid difficulty')
 rng=random.Random(seed)
 if profile and not template:
  eligible=[t for t,v in PROFILES.items() if profile in v and TEMPLATES[t]==level]
 else: eligible=[t for t,v in TEMPLATES.items() if v==level]
 if not eligible: raise ValueError('profile not eligible for difficulty')
 t=template or rng.choice(eligible)
 if TEMPLATES.get(t)!=level: raise ValueError('template difficulty mismatch')
 profile=profile or PROFILES[t][0]
 if profile not in PROFILES[t]: raise ValueError('profile mismatch')
 raw=profile.startswith('raw-');sid=profile[4:] if raw else None
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('only observed radio type is supported')
 p=parameters
 for attempt in range(10000):
  p=dict(p) if parameters is not None else sample(t,rng)
  validate_parameters(level,t,p,raw)
  try: items=[('correct',aslist(compute(t,p)))] if raw and ':question/answer-fields' not in QS[sid] else bank(t,p,profile)
  except ValueError:
   if parameters is not None: raise
   continue
  break
 else: raise ValueError('no eligible whole bank')
 prompt=raw_prompt(t,p) if raw else normal_prompt(t,p)
 solution=sum_solution(t,p) if t.startswith('sum') else normal_solution(t,p)
 values=raw_values(t,items) if raw and t in ('subtract','scalar') else [vec(v) for _,v in items]
 q={':question/problem':prompt}
 if not raw or ':question/difficulty' in QS[sid]: q[':question/difficulty']=':question.difficulty/'+level
 if not raw or ':question/worked-solution' in QS[sid]: q[':question/worked-solution']=solution
 hasfield=not raw or ':question/answer-fields' in QS[sid]
 content=[VERSION,level,prompt,q.get(':question/worked-solution'), sorted(values) if hasfield else None,raw]
 identity=uid(content);q[':question/id']=identity
 if raw:
  q[':db/id']=QS[sid][':db/id'];q[':question/math-academy-id']=sid
 if hasfield:
  fid=uid([identity,'selection']);choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
  if not raw or ':answer-field/correct' in QS[sid][':question/answer-fields'][0]: f[':answer-field/correct']=[':answer/id',choices[0][':answer/id']]
  rng.shuffle(choices)
  if raw:
   sf=QS[sid][':question/answer-fields'][0];f[':db/id']=sf[':db/id']
   original_values=raw_values(t,bank(t,SOURCE_PARAMS[sid],profile))
   original_by_value={v[':answer/value']:v for v in sf[':answer-field/choices']}
   for ch in choices:
    index=values.index(ch[':answer/value'])
    ch[':db/id']=original_by_value[original_values[index]][':db/id']
  q[':question/answer-fields']=[f]
 fingerprint=hashlib.sha256(json.dumps([t,sorted(p.items())],sort_keys=True).encode()).hexdigest()
 # Coordinate tasks are distinct; uppercase/lowercase aliases do not inflate diversity.
 mathematical=hashlib.sha256(json.dumps([t.replace('sum_upper','sum').replace('sum_lower','sum'),p],sort_keys=True).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':t,'level':level,'seed':seed,'parameters':p,'profile':profile,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'raw_evidence':raw,'evidence_only':raw,'eligible_for_learning':not raw,'authorship':'observed mask with explicit operation bank' if level=='easy' else 'authored missing-level extension','recipes':[n for n,_ in items],'correct_value':vec(aslist(compute(t,p))),'mathematical_fingerprint':mathematical,'parameter_fingerprint':fingerprint,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'bounds':{'coordinates':9 if level=='easy' else 6,'moderate_scalars':[2,6],'hard_scalars':[2,4],'all_choice_components_max':120}}}

# EASY: one sum, subtraction or scalar multiplication; completed sum fields authored.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): four nonzero products and two component sums, no nesting.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): six nonzero products, an inner sum and outer subtraction in each component.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];out=q[':question/problem']+'\n'
 for f in q.get(':question/answer-fields',[]):
  out+='\n'+'\n'.join(f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices'])+'\n'
 if ':question/worked-solution' in q: out+='\n'+q[':question/worked-solution']+'\n'
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1: ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(markdown(r) for r in records))
