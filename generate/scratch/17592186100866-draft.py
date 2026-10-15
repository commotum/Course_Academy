#!/usr/bin/env python3
"""Exact 2x2 matrix/column-vector multiplication; unregistered review draft.

Easy: source integer workload. Moderate: authored integer-matrix/decimal-vector
workload. Hard: authored decimal-matrix/decimal-vector workload, both rows have
opposing nonzero products. All retain two ordered row dot products. Raw observed
profiles preserve missing attributes and legacy duplicate fields, are ineligible
for learning, and use explicit opaque bank slots where source intent is unknown.
No registered generator imports, database access, or writes occur here.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex, normalize_tex, normalize_prose, validate_tex, validate_prose, validate_generated_record
KP=17592186100866
HERE=Path(__file__).with_suffix('')
CAP=json.loads((HERE/'source.json').read_text()); RECORD=CAP['record']
KP_UUID=RECORD[':knowledge-point/id']; TITLE=RECORD[':knowledge-point/title']
VERSION='matrix-column-draft-2.0'
LEVELS=('easy','moderate','hard')
KEYS=('a','b','c','d','u','v')
TEMPLATES=('named-radio','inline-radio','what-radio','named-blank','inline-blank')
ELIGIBLE_PROFILES={'named-radio':('authored-method','source-method:q-13564','source-method:q-126511','source-method:q-13565'),'inline-radio':('authored-method','source-method:q-13555'),'what-radio':('authored-method',),'named-blank':('component-blanks',),'inline-blank':('component-blanks',)}
GROUPS={'named-radio':['q-13564','q-126511','q-126512','q-13565'], 'inline-radio':['q-13555','q-13629','q-13560'], 'named-blank':['q-275589'], 'inline-blank':['q-318640','q-318644'], 'what-radio':['q-13566']}
SOURCES={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions'] if ':question/math-academy-id' in q}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(text):
 return [[row.split('&') for row in body.split('\\\\')] for body in MATRIX.findall(text)]
def parameters_of(q):
 A,V=matrices(q[':question/problem']); names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem'])
 return dict(zip(KEYS,[str(s.Rational(c.strip())) for row in A+V for c in row]))|{'matrix_name':names[1] if names else 'A','vector_name':names[2] if names else 'x'}
def template_of(mid):return next(t for t,ids in GROUPS.items() if mid in ids)
def hashof(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def tex(n):
 if isinstance(n,str) and ('\\' in n or n=='∗'): return n
 n=s.Rational(n)
 if n.q==1:return str(n)
 # Finite decimal arithmetic is anchored to prerequisite e-4323. Exact conversion.
 q=n.q
 while q%2==0:q//=2
 while q%5==0:q//=5
 if q!=1:return s.latex(n)
 for k in range(1,8):
  z=n*10**k
  if z.q==1:
   a=str(abs(int(z))).zfill(k+1);return ('-' if n<0 else '')+a[:-k]+'.'+a[-k:]
 raise ValueError('Decimal exceeds workload')
def vec(x,y):return matrix_tex([[tex(x)],[tex(y)]])
def mathdata(p):
 a,b,c,d,u,v=(s.Rational(p[k]) for k in KEYS)
 return dict(zip(KEYS,(a,b,c,d,u,v)))|{'r':a*u+b*v,'t':c*u+d*v}
def canonical_parameters(p):
 if set(p)-set(KEYS)-{'matrix_name','vector_name','opaque_slots'}:raise ValueError('Unknown parameter')
 if not all(k in p for k in KEYS):raise ValueError('Six ordered operands required')
 out={k:str(s.Rational(str(p[k]))) for k in KEYS}
 out.update(matrix_name=p.get('matrix_name','A'),vector_name=p.get('vector_name','x'))
 if out['matrix_name'] not in ('A','Z','X','H') or out['vector_name'] not in ('x','y','n','a'):raise ValueError('Unsupported label')
 if 'opaque_slots' in p:out['opaque_slots']=[[str(s.Rational(str(x))) for x in pair] for pair in p['opaque_slots']]
 return out
# Explicit complete bank expressions. Observed ±1 values remain evidence-only;
# their reproduction does not establish a defensible learner-error explanation.
RECIPES={
'q-13564':[('r','t'),('-r','-t'),('r','-t'),('-r','t'),('v','u')],
'q-126511':[('r','t'),('a+b','c+d'),('-a-b','-c-d'),('t','r'),('a','c')],
'q-126512':[('r','t'),('z0','z1'),('a*u','c*u'),('b*u','d*u'),('a*u+c*v','b*u+d*v')],
'q-13555':[('r','t'),('r','r'),('r','-t'),('-r','-t'),('-r','t')],
'q-13565':[('r','t'),('-t','-r'),('r','-t'),('-r','-t'),('-t','r')],
'q-13629':[('r','t'),('r+1','t'),('r','t-1'),('r','t+1'),('r-1','t-1')],
'q-13560':[('r','t'),('r+1','t'),('t','r'),('r','r'),('t','t')],
'q-13566':[('r','t'),('r','-t'),('-r','-t'),('t','r'),('z0','z1')],
'authored-method':[('r','t'),('a*u+c*v','b*u+d*v'),('a*u','c*u'),('b*v','d*v'),('t','r')],
}
def bank(profile,p):
 data=mathdata(p)
 if 'opaque_slots' in p:
  if len(p['opaque_slots'])!=1 or len(p['opaque_slots'][0])!=2:raise ValueError('One opaque observed vector slot required')
  data|={'z0':s.Rational(p['opaque_slots'][0][0]),'z1':s.Rational(p['opaque_slots'][0][1])}
 mid=profile.removeprefix('observed:').removeprefix('source-method:')
 if mid not in RECIPES:return []
 if mid in ('q-126512','q-13566') and 'z0' not in data:raise ValueError('Opaque source banks require explicit observed vector slot; never inferred')
 return [tuple(s.sympify(e,locals=data) for e in pair) for pair in RECIPES[mid]]
def guard(p,level,observed=False):
 d=mathdata(p); vals=[d[k] for k in KEYS]
 if any(abs(x)>11 for x in vals):raise ValueError('Operand magnitude exceeds source arithmetic ceiling')
 if observed:return
 if not d['u'] or not d['v']:raise ValueError('Nonzero vector components required')
 if level=='easy':
  if any(x.q!=1 for x in vals):raise ValueError('Easy requires integer operands')
 elif level=='moderate':
  if any(d[k].q!=1 for k in KEYS[:4]) or any((d[k]*10).q!=1 for k in ('u','v')) or not any(d[k].q!=1 for k in ('u','v')):raise ValueError('Moderate requires integer matrix and a tenths vector')
  if any(not d[k] for k in KEYS[:4]) or not any(d[k].q!=1 for k in ('r','t')):raise ValueError('Moderate retains four nonzero products and decimal output')
 else:
  if any(x.q==1 or (x*10).q!=1 or abs(x)>9 for x in vals):raise ValueError('Hard requires all six nonintegral tenths bounded by 9')
  if d['a']*d['u']*d['b']*d['v']>=0 or d['c']*d['u']*d['d']*d['v']>=0:raise ValueError('Hard requires opposing nonzero products in both rows')
  if any((d[k]*10).q==1 for k in ('r','t')):raise ValueError('Hard requires hundredths arithmetic in both outputs')
def factor(x,wrap=True):return '('+tex(x)+')' if x<0 and wrap else tex(x)
def render(template,p,style=None):
 d=mathdata(p);a,b,c,dd,u,v=(d[k] for k in KEYS);r,t=d['r'],d['t']
 A=matrix_tex([[tex(a),tex(b)],[tex(c),tex(dd)]]);V=vec(u,v);AV=A+V;target=p['matrix_name']+p['vector_name']
 if template.startswith('named'):
  prompt=f'Find ${target}$ if'+('' if template=='named-blank' else ' ')+'\n$'+p['matrix_name']+'='+A+'$\nand\n$'+p['vector_name']+'='+V+'.$'
  if template.endswith('blank'):prompt+='\n\n| $'+target+r'=\,\,$ |  | {{field-1}} |  |'+'\n| --- | --- | --- | --- |\n|  | {{field-2}} |  |  |'
 elif template=='inline-blank':prompt='Compute the following:\n\n| $'+AV+r'=\,\,$ |  | {{field-1}} |  |'+'\n| --- | --- | --- | --- |\n|  | {{field-2}} |  |  |'
 elif template=='what-radio':prompt='What is $'+AV+'$?'
 else:prompt='$'+AV+'=$'
 # Preserve source conditional negative-parentheses masks; default wraps all.
 coef=[True]*4;vw=True
 if style in ('q-13555','q-13565'):vw=False
 if style=='q-275589':coef[2]=False
 row1=factor(a,coef[0])+r'\cdot '+factor(u,vw)+'+'+factor(b,coef[1])+r'\cdot '+factor(v,vw)
 row2=factor(c,coef[2])+r'\cdot '+factor(u,vw)+'+'+factor(dd,coef[3])+r'\cdot '+factor(v,vw)
 prefix=target+'=' if template=='named-blank' else ''
 solution='We multiply each row in the matrix by the column vector using the dot product. Multiplying the first row, we get\n\n$$\n'+r'\begin{aligned}'+prefix+AV+' & ='+vec(row1,'∗')+'='+vec(r,'∗')+r'.\end{aligned}'+'\n$$\n\nMultiplying the second row, we get\n\n$$\n'+r'\begin{aligned}'+prefix+AV+' & ='+vec(r,row2)+'='+vec(r,t)+r'.\end{aligned}'+'\n$$\n\nTherefore, \n'
 if template.startswith('named'):solution+='$'+target+'='+vec(r,t)+'.$'
 else:solution+='\n$$\n'+AV+'='+vec(r,t)+'.\n$$'
 return normalize_prose(prompt),normalize_prose(solution)
def _sample(level,rng):
 if level=='easy':nums=[rng.randint(-11,11) for _ in range(4)]+[rng.choice([i for i in range(-9,10) if i]) for _ in range(2)]
 elif level=='moderate':nums=[rng.choice([i for i in range(-9,10) if i]) for _ in range(4)]+[s.Rational(rng.choice([i for i in range(-89,90) if i]),10) for _ in range(2)]
 else:nums=[s.Rational(rng.choice([i for i in range(-89,90) if i%10]),10) for _ in range(6)]
 return canonical_parameters(dict(zip(KEYS,map(str,nums)))|{'matrix_name':rng.choice(('A','Z','X','H')),'vector_name':rng.choice(('x','y','n','a'))})
def public_guard(result):
 q=result['question']
 for key in (':question/problem',':question/worked-solution'):
  if key in q:
   value=q[key]
   if any(ord(c)<32 and c not in '\n\t' for c in value):raise ValueError('Unintended C0 control character')
   validate_prose(value)
   if normalize_prose(value)!=value:raise ValueError('Unnormalized prose')
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   value=a[':answer/value']
   if any(ord(c)<32 for c in value):raise ValueError('Unintended answer C0')
   validate_tex(value)
   if normalize_tex(value)!=value:raise ValueError('Unnormalized answer')
 if ':question/worked-solution' in q:validate_generated_record(result)
 return result

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed); observed=bool(profile and profile.startswith('observed:'));mid=profile[9:] if observed else None
 if observed:
  if level!='easy':raise ValueError('Original labels and authored unrated assignment are easy only')
  if mid not in SOURCES:raise ValueError('Unknown observed profile')
  expected=template_of(mid)
  if template and template!=expected:raise ValueError('Profile/template mismatch')
  template=expected
 else:
  eligible=list(TEMPLATES)
  if field_type:eligible=[t for t in eligible if t.endswith(field_type.removeprefix(':answer-field.type/'))]
  if template and template not in eligible:raise ValueError('Field/template mismatch')
  template=template or rng.choice(eligible)
  profile=profile or rng.choice(ELIGIBLE_PROFILES[template])
  if profile not in ELIGIBLE_PROFILES[template]:raise ValueError('Unsupported complete profile')
 if template not in TEMPLATES:raise ValueError('Unknown template')
 if field_type and field_type.removeprefix(':answer-field.type/')!=template.split('-')[-1]:raise ValueError('Wrong field type')
 if observed and parameters is None:raise ValueError('Observed replay requires explicit parameters; no source-payload shortcut')
 for _ in range(10000):
  p=canonical_parameters(parameters) if parameters is not None else _sample(level,rng)
  try:
   guard(p,level,observed);values=bank(profile,p)
   if values and len(set(values))!=len(values):raise ValueError('Whole-bank mathematical collision')
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('Sampling exhausted')
 style=mid if observed else profile.removeprefix('source-method:') if profile.startswith('source-method:') else None
 prompt,solution=render(template,p,style);data=mathdata(p)
 source=SOURCES[mid] if observed else None
 specs=[]
 if observed:
  for f in source.get(':question/answer-fields',[]):
   is_radio=f[':answer-field/type'][':db/ident'].endswith('/radio');key=f[':answer-field/key']
   entries=values if is_radio else [(data['r' if key=='field-1' else 't'],)]
   specs.append((key,':answer-field.type/'+('radio' if is_radio else 'blank'),entries,':answer-field/correct' in f))
 else:
  specs=[('selection',':answer-field.type/radio',values,True)] if values else [('field-1',':answer-field.type/blank',[(data['r'],)],True),('field-2',':answer-field.type/blank',[(data['t'],)],True)]
 q={':question/problem':prompt}
 if not observed or ':question/worked-solution' in source:q[':question/worked-solution']=solution
 if not observed or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 content={'version':VERSION,'question':q,'banks':[(key,typ,sorted([tuple(map(str,v)) for v in entries]),has_correct) for key,typ,entries,has_correct in specs]}
 ident=hashof(content);qid=uid('question:'+ident);q[':question/id']=qid;fields=[]
 for index,(key,typ,entries,has_correct) in enumerate(specs):
  fid=uid(qid+':'+key+':'+str(index));choices=[]
  for value in entries:
   value=normalize_tex(vec(*value) if len(value)==2 else tex(value[0]));aid=uid(fid+':'+value)
   choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  correct=choices[0][':answer/id'];rng.shuffle(choices)
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':choices}
  if has_correct:field[':answer-field/correct']=[':answer/id',correct]
  fields.append(field)
 if not observed or ':question/answer-fields' in source:q[':question/answer-fields']=fields
 cols=sorted([(str(data['a']),str(data['c']),str(data['u'])),(str(data['b']),str(data['d']),str(data['v']))])
 return public_guard({'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'template':template,'bank_profile':profile,'parameters':p,'seed':seed,'source_basis':CAP['basis'],'lineage':CAP['lineage'],'mathematical_fingerprint':hashof(cols),'content_fingerprint':ident,'eligible_for_learning':not observed,'evidence_only':observed,'authored_difficulty':level!='easy','source_references':[mid] if mid else list(GROUPS[template]),'python_version':sys.version.split()[0],'sympy_version':s.__version__}})
# Easy: observed integer arithmetic, every source-shaped layout supported.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: authored decimal vector; four scalar products and two row sums.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored decimal factors on both sides, opposing products, hundredths.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--format',choices=('markdown','json'),default='json');args=parser.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,indent=2))
 else:
  for record in records:
   question=record['question'];meta=record['generation']
   difficulty=question.get(':question/difficulty','unrated').split('/')[-1]
   print('## Generated variant — '+difficulty)
   print('\nTemplate: '+meta['template']+'; bank: '+meta['bank_profile'])
   print('\n'+question[':question/problem'])
   for field in question.get(':question/answer-fields',[]):
    print('\nField: '+field[':answer-field/key'])
    correct=field.get(':answer-field/correct',[None,None])[1]
    for answer in field.get(':answer-field/choices',[]):
     print('- $'+answer[':answer/value']+'$'+(' **(correct)**' if answer[':answer/id']==correct else ''))
   print('\n**Worked solution**\n')
   print(question.get(':question/worked-solution','[Source has no worked solution]'))
