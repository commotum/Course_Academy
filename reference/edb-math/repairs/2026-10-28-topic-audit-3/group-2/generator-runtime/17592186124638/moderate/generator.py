#!/usr/bin/env python3
"""Seeded point evaluation. No filesystem outputs, services, or database writes."""
import argparse, copy, hashlib, json, random, uuid
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP={'db_id':17592186124638,'id':'f9289c4d-4f7f-5704-a2cb-272f92d8fef3','title':'Evaluating a Two-Variable Function'}
SOURCES={'poly':'15761064-db02-546d-ba8e-469a8fb53fd1','cubic':'6e391d1a-8298-5c2b-8fbb-e2c14854c2e0','cuberoot':'1a10c57f-681f-57e8-b21b-1312730cce62','root':'0416d0f7-4905-5934-8fa0-8a849f341e25','lnproduct':'d225e24f-f8fc-5851-bdaa-9e7972c2ed2f','exprecip':'9c34765f-7311-53ab-be9b-191b42487450','sin':'64dcbd76-8d54-5023-881a-a57cc6e8bf6c','cosquot':'fb2bfb86-4e76-5321-aed7-06eaaf8188f8','asinquot':'b4986375-d8de-524c-9cca-ad92c58d9cc6','atan':'a8d3d0dc-4e09-5317-a46e-76157b0c960f','lnlinear':'f50b49cb-5ece-5d2a-8bc6-eb00c81b1f11','rational':'911398b5-8165-51fb-be3f-bfee0bb6f77f','acos':'be7cd3c6-b4d8-58fc-a0bb-f9185ad55778','rootquot':'8d127fec-12ff-5644-b095-33e9b94a52d1','mixed':'2c0e2c3d-1459-5fdf-984b-feacfa06311c','nested':'59fa0287-0562-5cf2-8469-946a69dc8adf'}
FAMILIES={'easy':['poly','cubic','cuberoot','root','lnproduct','exprecip','sin','cosquot','asinquot','atan'],'moderate':['lnlinear','rational','acos','rootquot'],'hard':['mixed','nested']}
def C(v): return ('n',str(v))
x=('v','x');y=('v','y')
def N(op,*args): return (op,*args)
def texnum(v): return S.latex(S.sympify(v)).replace(r'\log{',r'\ln{')
def render(t,env=None,parent=0):
 op=t[0]
 if op=='n':
  v=texnum(t[1]);return '('+v+')' if v.startswith('-') and parent>=20 else v
 if op=='v':
  if env is None:return t[1]
  v=texnum(env[t[1]]);return '('+v+')' if v.startswith('-') else v
 prec={'add':10,'sub':10,'mul':20,'pow':30}.get(op,100)
 if op in ('add','sub'):
  left=render(t[1],env,10);right=render(t[2],env,11 if op=='sub' else 10)
  body=left+('+' if op=='add' else '-')+right
  body=body.replace('+-','-')
 elif op=='mul':body=render(t[1],env,20)+r'\cdot '+render(t[2],env,20)
 elif op=='div':body=r'\frac{'+render(t[1],env)+'}{'+render(t[2],env)+'}'
 elif op=='pow':body='{'+render(t[1],env,31)+'}^{'+render(t[2],env)+'}'
 elif op in ('sqrt','cbrt'):body=(r'\sqrt{' if op=='sqrt' else r'\sqrt[3]{')+render(t[1],env)+'}'
 elif op=='log':body=r'\log_{'+render(t[2],env)+r'}\left('+render(t[1],env)+r'\right)'
 else:body='\\'+op+r'\left('+render(t[1],env)+r'\right)'
 return '('+body+')' if prec<parent else body
def value_tex(value,tree):
 # SymPy's exact log(a,b) is stored as ln(a)/ln(b). Keep the authored
 # logarithm base in choices instead of exposing that untaught conversion.
 log_nodes=[node for _,node in nodes(tree) if node[0]=='log']
 natural=any(node[0]=='ln' for _,node in nodes(tree))
 if log_nodes and not natural:
  bases={evaluate(node[2],{}) for node in log_nodes}
  if len(bases)==1:
   base=next(iter(bases));replacements={}
   # Undo CAS log-combination (including powers containing ln(base)) before
   # replacing log atoms. Otherwise the supposedly base-preserving label can
   # hide a change-of-base expression inside its argument. All log inputs
   # here have already passed the real positive-domain check.
   value=S.expand_log(value,force=True)
   for atom in value.atoms(S.log):
    if atom.args[0]!=base:
     label=S.Symbol(r'\log_{'+texnum(base)+r'}\left('+texnum(atom.args[0])+r'\right)')
     replacements[atom]=label*S.log(base)
   value=S.cancel(value.xreplace(replacements))
 return texnum(value)

class DomainError(ValueError):pass

def evaluate(t,env):
 op=t[0]
 if op=='n':return S.sympify(t[1])
 if op=='v':return S.sympify(env[t[1]])
 a=[evaluate(k,env) for k in t[1:]]
 if op=='div' and a[1]==0:raise DomainError('Division by zero is undefined.')
 if op=='sqrt' and a[0]<0:raise DomainError('A negative radicand has no real square root.')
 if op in ('ln','log') and a[0]<=0:raise DomainError('A real logarithm requires a positive argument.')
 if op in ('arcsin','arccos') and abs(a[0])>1:raise DomainError('The argument of an inverse sine or cosine must lie in $[-1,1]$.')
 if op=='add':v=a[0]+a[1]
 elif op=='sub':v=a[0]-a[1]
 elif op=='mul':v=a[0]*a[1]
 elif op=='div':v=a[0]/a[1]
 elif op=='pow':v=a[0]**a[1]
 elif op=='sqrt':v=S.sqrt(a[0])
 elif op=='cbrt':v=S.real_root(a[0],3)
 elif op=='ln':v=S.log(a[0])
 elif op=='log':v=S.log(a[0],a[1])
 else:v={'sin':S.sin,'cos':S.cos,'arcsin':S.asin,'arccos':S.acos,'arctan':S.atan}[op](a[0])
 v=S.simplify(v)
 if v.is_real is not True or not v.is_finite:raise DomainError('The substituted expression has no finite real value.')
 return v

def nodes(t):
 if t[0] not in ('n','v'):
  for i,k in enumerate(t[1:],1):
   for path,node in nodes(k): yield (i,)+path,node
  yield (),t

def replace(t,path,new):
 if not path:return new
 parts=list(t);parts[path[0]]=replace(parts[path[0]],path[1:],new);return tuple(parts)

def errors(t,env):
 """Concrete single-error models; never correct+an arbitrary offset."""
 for name,e in [('swapped coordinates',{'x':env['y'],'y':env['x']}),('lost sign of x',dict(env,x=abs(env['x']))),('lost sign of y',dict(env,y=abs(env['y']))),('negated x',dict(env,x=-env['x'])),('negated y',dict(env,y=-env['y']))]:yield name,t,e
 for path,node in nodes(t):
  op=node[0];tag=render(node)
  for j,child in enumerate(node[1:]):yield 'omitted operation '+tag+' retaining operand '+str(j+1),replace(t,path,child),env
  if op in ('add','sub','mul','div'):
   for other in {'add':['sub'],'sub':['add'],'mul':['add'],'div':['mul']}[op]:yield 'used '+other+' instead of '+op+' in '+tag,replace(t,path,N(other,*node[1:])),env
  if op=='pow':
   yield 'reversed exponent sign in '+tag,replace(t,path,N('pow',node[1],N('mul',C(-1),node[2]))),env
   yield 'multiplied instead of exponentiating in '+tag,replace(t,path,N('mul',*node[1:])),env
  if op=='sqrt':yield 'used negative square root in '+tag,replace(t,path,N('mul',C(-1),node)),env
  if op=='arccos':yield 'used inverse sine in '+tag,replace(t,path,N('arcsin',node[1])),env
  if op=='sin':yield 'used cosine in '+tag,replace(t,path,N('cos',node[1])),env
  if op=='cos':yield 'used sine in '+tag,replace(t,path,N('sin',node[1])),env

def leaf_nodes(t):
 if t[0] in ('n','v'):yield t
 else:
  for child in t[1:]:yield from leaf_nodes(child)

def make_instance(f,r,case=None):
 a=r.choice([-3,-2,-1,1,2,3]); b=r.choice([-3,-2,-1,1,2,3]);c=r.randint(-5,5)
 env={'x':S.Integer(a),'y':S.Integer(b)};case=case or r.choice(['valid','valid','boundary','invalid'])
 if f=='poly':
  u=r.choice([x,y]);t=N('add',N('add',N('pow',u,C(2)),N('mul',x,y)),C(c))
 elif f=='cubic':t=N('add',N('sub',N('mul',C(r.choice([2,3])),N('pow',y,C(3))),x),C(c))
 elif f=='cuberoot':
  q=r.choice([-3,-2,-1,0,1,2,3]);t=N('cbrt',N('add',N('mul',x,y),C(q**3-a*b)))
 elif f=='root':
  v=r.choice([0,1,4,9,16]);t=N('sqrt',N('add',N('mul',x,N('pow',y,C(2))),C(v-a*b*b)))
 elif f=='lnproduct':
  env['y']=S.exp(r.choice([-2,-1,1,2,3]));t=N('add',N('mul',x,N('ln',y)),C(c))
 elif f=='exprecip':t=N('add',N('pow',C(2),N('mul',C(-1),x)),N('div',C(1),y))
 elif f in ('sin','cosquot'):
  env['y']=r.choice([-S.pi/3,-S.pi/4,-S.pi/6,S.pi/6,S.pi/4,S.pi/3,2*S.pi/3,3*S.pi/4]);t=N('mul',x,N('sin',y)) if f=='sin' else N('div',x,N('cos',y))
 elif f=='asinquot':
  env['x']=r.choice([-S.Integer(1),-S.Rational(1,2),S.Rational(1,2),S.Integer(1)]);env['y']=S.Integer(r.choice([-1,1,2]));t=N('div',N('pow',C('E'),y),N('arcsin',x))
 elif f=='atan':
  env['x']=r.choice([-S.pi,0,S.pi]);env['y']=S.Integer(r.choice([-1,0,1]));t=N('sub',N('mul',C(r.choice([2,4])),N('arctan',y)),x)
 elif f=='lnlinear':
  target=r.choice([1,2,4,8]) if case=='valid' else 0 if case=='boundary' else r.choice([-1,-2,-4]);t=N('ln',N('add',N('sub',N('mul',C(3),x),N('mul',C(2),y)),C(target-3*a+2*b)))
 elif f=='rational':
  d=r.choice([-2,-1,1,2]) if case=='valid' else 0;t=N('div',N('sub',N('mul',C(2),y),x),N('add',N('sub',N('pow',x,C(3)),N('pow',y,C(2))),C(d-a**3+b*b)))
 elif f=='acos':
  arg=r.choice([-S.Rational(1,2),0,S.Rational(1,2)]) if case=='valid' else r.choice([-1,1]) if case=='boundary' else r.choice([-2,2]);t=N('mul',x,N('arccos',N('add',y,C(arg-b))))
 elif f=='rootquot':
  v=r.choice([1,4,9]) if case=='valid' else 0 if case=='boundary' else r.choice([-1,-4]);d=r.choice([-2,-1,1,2]);
  if case=='invalid' and r.choice([True,False]):v=r.choice([0,1,4]);d=0
  t=N('div',N('sqrt',N('add',N('sub',x,y),C(v-a+b))),N('add',N('add',x,y),C(d-a-b)))
 elif f=='mixed':
  a=r.choice([1,2,4]);b=r.choice([-2,-1,1,2]);v=r.choice([0,1,4,9]);d=r.randint(-2,2)
  if case=='invalid':
   reason=r.choice(['log','root','denominator'])
   if reason=='log':a=r.choice([-2,0])
   if reason=='root':v=-1
   if reason=='denominator':b=r.choice([-2,-1]);d=a-2**(-b)
  if case=='boundary':v=0
  if case!='invalid' and S.Rational(2)**(-b)-a+d==0:d+=1
  env={'x':S.Integer(a),'y':S.Integer(b)}
  t=N('div',N('add',N('log',N('mul',x,N('pow',y,C(2))),C(2)),N('sqrt',N('add',N('sub',x,y),C(v-a+b)))),N('add',N('sub',N('pow',C(2),N('mul',C(-1),y)),x),C(d)))
 elif f=='nested':
  arg=r.choice([S.Rational(1,9),S.Rational(1,3),3,9,27]);v=r.choice([1,4,9]);
  if case=='invalid':
   if r.choice([True,False]):arg=r.choice([-3,0])
   else:v=r.choice([-1,0])
  elif case=='boundary':arg=1
  t=N('div',N('log',N('add',N('add',N('pow',x,C(2)),y),C(arg-a*a-b)),C(3)),N('sqrt',N('add',N('sub',x,y),C(v-a+b))))
 else:raise ValueError(f)
 if any(abs(S.sympify(node[1]))>32 for node in leaf_nodes(t) if node[0]=='n'):
  return make_instance(f,r,case)
 return t,env,case

def record(level,f,t,env,case,r,source=None):
 try:value=evaluate(t,env)
 except DomainError:value=None
 # Pick a complete authored error profile, then validate the whole bank.
 # Every recipe is concrete; a failed profile is discarded without replacing
 # individual entries by the next successful recipe from a pool.
 n=4 if value is None else 3 if f not in ('poly','cubic','cuberoot','lnproduct','sin','cosquot','asinquot','atan','exprecip') else 4
 models=list(errors(t,env));cache={};vals=None
 if source is not None:
  vals=[(v,'correct' if v==source['correct'] else 'original source option') for typ,v in source['bank']]
 else:
  for _ in range(2500):
   profile=r.sample(range(len(models)),n);candidate=[];invalid=False
   for index in profile:
    if index not in cache:
     desc,alt,e=models[index]
     try:
      v=evaluate(alt,e)
      if (value is not None and S.simplify(v-value)==0) or len(texnum(v))>100 or abs(float(v))>10000:cache[index]=None
      else:cache[index]=(normalize_tex(value_tex(v,t)),v,desc)
     except (DomainError,TypeError,ZeroDivisionError):cache[index]=None
    item=cache[index]
    if item is None or any(S.simplify(item[1]-prev[1])==0 for prev in candidate):
     invalid=True;break
    candidate.append(item)
   if invalid:continue
   if value is not None:
    numbers=[entry[1] for entry in candidate]+[value]
    # A visible answer form or lone sign must not isolate the key. Zero is
    # necessarily unique in a distinct bank and remains a legitimate result.
    if value!=0 and sum(S.sign(v)==S.sign(value) for v in numbers)<2:continue
    if sum(v.is_Integer==value.is_Integer for v in numbers)<2:continue
    if sum(v.is_Rational==value.is_Rational for v in numbers)<2:continue
    pairs=[(i,j) for i,v in enumerate(numbers) for j,w in enumerate(numbers) if i<j and v!=0 and S.simplify(v+w)==0]
    if len(pairs)==1 and len(numbers)-1 in pairs[0]:continue
   vals=[(key,desc) for key,v,desc in candidate]
   vals.append(('Undefined' if value is None else normalize_tex(texnum(value)),'correct'))
   if value is not None and n==3:vals.append(('Undefined','incorrect domain rejection'))
   break
  if vals is None:raise ValueError('no valid complete error profile')
 r.shuffle(vals)
 point=texnum(env['x'])+','+texnum(env['y'])
 prompt='Evaluate the real-valued function\n\n$$\nf(x,y)='+render(t)+'\n$$\n\nat the point $('+point+')$.'
 rows=[];failure=None
 for _,node in nodes(t):
  try:v=evaluate(node,env)
  except DomainError as exc:
   failure=str(exc);break
  row=render(node,env)+' &='+texnum(v)
  if row not in rows:rows.append(row)
 sol='Substitute $x='+texnum(env['x'])+'$ and $y='+texnum(env['y'])+'$ throughout the expression. Keep parentheses around signed inputs:\n\n$$\nf('+point+')='+render(t,env)+'\n$$\n\nEvaluate the inner operations before combining them:'
 if rows:sol+='\n\n$$\n\\begin{aligned}\n'+(' \\\\\n'.join(rows))+'\n\\end{aligned}\n$$'
 if value is None:
  # The failing node's immediate inputs have already been evaluated above.
  sol+='\n\n'+failure+' Therefore, the function is **undefined** at this point.'
 else:sol+='\n\nThus $f('+point+')='+texnum(value)+'$.'
 if source is not None:
  prompt=source['prompt'];sol=source['solution']
 prompt=normalize_prose(prompt);sol=normalize_prose(sol)
 identity=json.dumps([level,prompt,sol,vals],ensure_ascii=False)
 def uid(label):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:point-eval:v1:'+identity+':'+label))
 choices=[{':answer/id':uid('answer'+str(i)),':answer/type':':answer.type/text' if v=='Undefined' else ':answer.type/math',':answer/value':v} for i,(v,_) in enumerate(vals)]
 correct=next(choices[i][':answer/id'] for i,(_,desc) in enumerate(vals) if desc=='correct')
 q={':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':uid('field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 out={'knowledge_point':KP,'question':q,'metadata':{'generator':'point-evaluation-v1','family':f,'case':case,'source_question_ids':[SOURCES[f]],'authored_error_profile':[desc for _,desc in vals],'parameters':{k:str(v) for k,v in env.items()},'expression_tree':t,'numeric_rank':None if value is None or source is not None else sum(bool(v<value) for _,v,_ in candidate)}}
 validate_generated_record(out);return out

def bank_roles(record):
 field=record['question'][':question/answer-fields'][0]
 choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
 return next(i for i,c in enumerate(choices) if c[':answer/id']==correct),record['metadata']['numeric_rank']

def candidate_batch(level,count,r):
 out=[];seen=set();families=[];case_queues={}
 while len(out)<count:
  if not families:families=FAMILIES[level][:];r.shuffle(families)
  f=families.pop();made=False
  if not case_queues.get(f):
   case_queues[f]=['valid','invalid','boundary'];r.shuffle(case_queues[f])
  case=case_queues[f].pop()
  for attempt in range(150):
   t,env,case=make_instance(f,r,case)
   try:q=record(level,f,t,env,case,r)
   except ValueError:continue
   sig=q['question'][':question/problem']
   if sig in seen:continue
   seen.add(sig);out.append(q);made=True;break
  if not made:raise RuntimeError('cannot construct '+f)
 return out

def generate(level,count,seed):
 r=random.Random(seed)
 # Reject complete candidate batches using the same deterministic random
 # stream. Retrying only a boundary item can be impossible (a valid log(1)
 # numerator is necessarily zero); its earlier partner must also be eligible
 # for replacement. Zero and cancellation remain in the sampling domain.
 for _ in range(100):
  out=candidate_batch(level,count,r);roles={}
  for q in out:roles.setdefault(q['metadata']['family'],[]).append(bank_roles(q))
  good=True
  for values in roles.values():
   ranks=[rank for _,rank in values if rank is not None]
   if len(values)>1 and len({position for position,_ in values})==1:good=False
   if len(ranks)>1 and len(set(ranks))==1:good=False
  if good:return out
 raise RuntimeError('cannot construct a batch without a repeated family cue')

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True);p.add_argument('--count',type=int,required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
 if a.count<0:p.error('count must be nonnegative')
 print(json.dumps(generate(a.difficulty,a.count,a.seed),ensure_ascii=False))
if __name__=='__main__':main()
