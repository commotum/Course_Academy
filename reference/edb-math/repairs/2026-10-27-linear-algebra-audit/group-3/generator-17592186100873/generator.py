#!/usr/bin/env python3
"""Seeded easy selected-entry generator. Source banks replay without loss.
Local source data and shared math helper are the only runtime files.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
from math_format import matrix_tex,normalize_prose,normalize_tex,checked_math_content
import sympy as sp
CAPTURE=json.loads((HERE/'source-data.json').read_text()); SOURCE=CAPTURE['record']
KP_ID=17592186100873; VERSION='selected-entry-v5'; LEVELS=('easy',)
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
TARGET=re.compile(r'\{?([a-z])\}?_\{([1-5])([1-5])\}')
def matrices(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in MAT.findall(text)]
def params(q):
 a,b=matrices(q[':question/problem']); _,i,j=TARGET.search(q[':question/problem']).groups()
 return {'A':a,'B':b,'row':int(i),'column':int(j)}
def typename(f):return f[':answer-field/type'][':db/ident'].split('/')[-1]
TEMPLATES={s:{'field_type':typename(q[':question/answer-fields'][0]),'terms':len(params(q)['B'])} for s,q in SOURCES.items()}
PROFILES=('other-product-entries',)
DECISIONS=('positive-products','negative-products','mixed-products','cancellation','zero-product')
def ordinal(n):return str(n)+{1:'st',2:'nd',3:'rd'}.get(n,'th')
def factor(n):return '('+str(n)+')' if n<0 else str(n)
def hashof(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),x))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def validate_parameters(p,level,evidence=False):
 if set(p)!={'A','B','row','column'}:raise ValueError('Exact parameter keys A,B,row,column required')
 a,b,i,j=p['A'],p['B'],p['row'],p['column']
 if not (isinstance(a,list) and isinstance(b,list) and 2<=len(a)<=5 and 2<=len(b)<=3):raise ValueError('Source-shaped dimensions')
 if any(not isinstance(r,list) for r in a+b):raise ValueError('Rows required')
 n=len(b);m=len(b[0])
 if not 2<=m<=5 or any(len(r)!=n for r in a) or any(len(r)!=m for r in b):raise ValueError('Conformable rectangular matrices')
 if any(type(x)is not int or abs(x)>20 for r in a+b for x in r):raise ValueError('Integer operand bound 20')
 if type(i)is not int or type(j)is not int or not 1<=i<=len(a) or not 1<=j<=m:raise ValueError('Eligible target required')
 row=a[i-1];col=[r[j-1] for r in b];terms=[x*y for x,y in zip(row,col)]
 if max(map(abs,row+col))>10:raise ValueError('Selected operand source ceiling 10')
 if max(map(abs,terms))>30 or sum(map(abs,terms))>58:raise ValueError('Product/L1 source ceiling')
 if not evidence:
  if sum(x!=0 for x in terms)<2:raise ValueError('At least two substantive products')
  if level=='easy':
   if n==3 and not any(abs(x)<=1 or abs(y)<=1 for x,y in zip(row,col)):raise ValueError('Easy three-term unit/zero support')
 return row,col,terms

def render_problem(src,p):
 text=src[':question/problem'];ms=list(MAT.finditer(text))
 for match,value in reversed(list(zip(ms,(p['A'],p['B'])))):text=text[:match.start()]+matrix_tex(value,augmented=False)+text[match.end():]
 return TARGET.sub(lambda m: ('{'+m[1]+'}' if m[0].startswith('{') else m[1])+'_{'+str(p['row'])+str(p['column'])+'}',text)

def render_solution(src,p):
 a,b,i,j=p['A'],p['B'],p['row'],p['column']; row=a[i-1];col=[r[j-1] for r in b]
 terms=[x*y for x,y in zip(row,col)];letter=TARGET.search(src[':question/problem'])[1]
 labels=re.search(r'Let \$([A-Z])\s*=\s*([A-Z])([A-Z])',src[':question/problem']).groups()
 focused_a=[[str(v) if ri==i-1 else r'{\color{lightgray}{'+str(v)+'}}' for v in row] for ri,row in enumerate(a)]
 focused_b=[[str(v) if ci==j-1 else r'{\color{lightgray}{'+str(v)+'}}' for ci,v in enumerate(row)] for row in b]
 full='The full matrix product is\n\n$$\n'+labels[0]+'='+matrix_tex(focused_a,augmented=False)+matrix_tex(focused_b,augmented=False)+'\n$$'
 intro=f'Multiplying the ${i}$'+ordinal(i)[-2:]+f' row in ${labels[1]}$ by the ${j}$'+ordinal(j)[-2:]+f' column in ${labels[2]}$, we get'
 old=src.get(':question/worked-solution','')
 implicit=bool(old and r'\cdot' not in old)
 expansion='+'.join(factor(x)+'('+str(y)+')' if implicit else factor(x)+r'\cdot '+factor(y) for x,y in zip(row,col))
 signed=''.join(('+' if k and x>=0 else '')+str(x) for k,x in enumerate(terms))
 stages=[matrix_tex([row],augmented=False)+matrix_tex([[x] for x in col],augmented=False),expansion,signed,str(sum(terms))+'.']
 return full+'\n\n'+intro+'\n\n$$\n'+r'\begin{aligned}{'+letter+'}_{'+str(i)+str(j)+r'} & ='+(r' \\  & ='.join(stages))+r'\end{aligned}'+'\n$$'

def decision_of(terms):
 if any(x==0 for x in terms):return 'zero-product'
 if sum(terms)==0:return 'cancellation'
 if min(terms)>0:return 'positive-products'
 if max(terms)<0:return 'negative-products'
 return 'mixed-products'

def sample_parameters(rng,anchor,target,decision):
 n=len(anchor['B']);h=len(anchor['A']);w=len(anchor['B'][0]);i,j=target
 # The indexed target is already chosen. Natural sampling does not overweight
 # rare answer categories; explicit cases remain available for coverage tests.
 for draw in range(1,10001):
  row=[rng.randint(-6,6) for _ in range(n)]; col=[rng.randint(-6,6) for _ in range(n)]
  t=[x*y for x,y in zip(row,col)]
  if decision is not None and decision_of(t)!=decision:continue
  if sum(x!=0 for x in t)<2:continue
  if n==3 and not any(abs(x)<=1 or abs(y)<=1 for x,y in zip(row,col)):continue
  if max(map(abs,t))>30 or sum(map(abs,t))>58:continue
  a=[[rng.randint(-6,6) for _ in range(n)] for _ in range(h)]
  b=[[rng.randint(-6,6) for _ in range(w)] for _ in range(n)]
  a[i-1]=row
  for k,v in enumerate(col):b[k][j-1]=v
  return {'A':a,'B':b,'row':i,'column':j},draw
 raise ValueError('Cannot sample selected decision')

@checked_math_content
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,target=None,decision=None):
 if level not in LEVELS:raise ValueError('Only source-justified easy difficulty is supported')
 rng=random.Random(seed)
 eligible=[s for s,t in TEMPLATES.items() if field_type in (None,t['field_type'])]
 if profile and profile.startswith('observed:'):
  sid=profile.split(':',1)[1]
  if template not in (None,sid):raise ValueError('Profile/template mismatch')
  template=sid
 if template is None:template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Unsupported template/field')
 src=SOURCES[template];anchor=params(src);ft=TEMPLATES[template]['field_type']
 replay=bool(profile and profile.startswith('observed:'))
 if profile is None:profile=rng.choice(PROFILES) if ft=='radio' else 'blank'
 if not replay and profile not in (PROFILES if ft=='radio' else ('blank',)):raise ValueError('Incompatible bank')
 h,n,w=len(anchor['A']),len(anchor['B']),len(anchor['B'][0])
 if target is None:
  target=(parameters['row'],parameters['column']) if parameters is not None else (anchor['row'],anchor['column']) if replay else (rng.randint(1,h),rng.randint(1,w))
 if not (1<=target[0]<=h and 1<=target[1]<=w):raise ValueError('Invalid target')
 supported_decisions=list(DECISIONS if n==3 else DECISIONS[:-1])
 if decision is not None and decision not in supported_decisions and not (replay or parameters is not None):raise ValueError('Decision incompatible with complete bank')
 explicit=parameters is not None
 if replay and explicit and parameters!=anchor:raise ValueError('Observed banks replay only at original parameters')
 factor_draws=0
 for attempt in range(1,1001):
  if explicit:p=copy.deepcopy(parameters)
  elif replay:p=copy.deepcopy(anchor)
  else:
   p,draws=sample_parameters(rng,anchor,target,decision);factor_draws+=draws
  try:
   row,col,terms=validate_parameters(p,level,evidence=replay)
   if (len(p['A']),len(p['B']),len(p['B'][0]))!=(h,n,w):raise ValueError('Preserve source dimensions')
   product=sp.Matrix(p['A'])*sp.Matrix(p['B']);answer=int(product[p['row']-1,p['column']-1])
   if replay:
    vals=[int(a[':answer/value']) for a in src[':question/answer-fields'][0][':answer-field/choices']]
    if vals.count(answer)!=1:raise ValueError('Source key absent or ambiguous')
   elif ft=='blank':vals=[answer]
   elif profile=='other-product-entries':
    others=list(set(int(product[x,y]) for x in range(h) for y in range(w) if (x,y)!=(p['row']-1,p['column']-1))-{answer})
    if len(others)<4:raise ValueError('Four distinct wrong entries needed')
    vals=[answer]+rng.sample(sorted(others),4)
   else:raise ValueError('Unknown bank profile')
   if len(vals)!=len(set(vals)):raise ValueError('Whole bank has colliding values')
   break
  except ValueError:
   if explicit or replay:raise
 else:raise ValueError('No eligible whole instance for chosen target and decision')
 problem=normalize_prose(render_problem(src,p));solution=normalize_prose(render_solution(src,p));sf=src[':question/answer-fields'][0]
 # Original complete wording and solutions are exact at replay parameters.
 if replay and p==anchor and ':question/worked-solution' in src:solution=normalize_prose(src[':question/worked-solution'])
 q={':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level}
 qid=uid(hashof([VERSION,q,ft,sf[':answer-field/key'],sorted(vals)]));q[':question/id']=qid
 fid=uid(qid+':field:'+sf[':answer-field/key']);answers=[];correct=None
 for v in vals:
  aid=uid(fid+':'+str(v));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':normalize_tex(str(v))})
  if v==answer:correct=aid
 if ft=='radio':rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 q[':question/answer-fields']=[f]
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{
 'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,
 'mathematical_fingerprint':hashof([row,col]),'decision_case':decision_of(terms),
 'sampling_policy':'conditional-case' if decision is not None else 'natural-factors','requested_decision':decision,
 'requested_target':list(target),'attempts':attempt,'factor_draws':factor_draws,'source_question_id':src[':question/id'],
 'source_difficulty':src.get(':question/difficulty'),
 'source_omissions':[k for k in (':question/difficulty',':question/worked-solution') if k not in src]+([':answer-field/correct'] if ':answer-field/correct' not in sf else []),
 'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],
 'source_sha256':CAPTURE['source_sha256'],'python_version':sys.version.split()[0],'sympy_version':sp.__version__,
 'bank_recipes':profile,'replay':replay}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];out=[f"Level: {q.get(':question/difficulty','MISSING (raw source)')} | template: {g['template']} | profile: {g['bank_profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out.append('Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+')')
  key=f.get(':answer-field/correct',[None,None])[1]
  if key is None:out.append('Correct designation: MISSING (raw source)')
  out.extend(('* [correct] ' if a[':answer/id']==key else '* ')+a[':answer/value'] for a in f[':answer-field/choices'])
 out.append('Worked solution:\n'+q.get(':question/worked-solution','MISSING (raw source)'));return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+k,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for k in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
