#!/usr/bin/env python3
"""Private distributivity draft: frozen2275 sources; registered numeric unchanged.

Easy: one distributed negative group, one cancellation, entrywise difference.
Moderate: two cancellation pairs with a negative difference; surviving matrix.
Hard (authored/calibration uncertain): two cancellation pairs, three-term negative
 group, surviving difference of signed 3x2 matrices. No scalar multiplication,
 matrix multiplication, equation solving, or new response skill.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,normalize_tex,validate_generated_record
D=Path(__file__).with_suffix('')
SOURCE=json.loads((D/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
KP={'db_id':17592186100992,'id':'16e62b0e-adda-5d35-aeb9-961057dce8f0','title':SOURCE['record'][':knowledge-point/title']}
VERSION='matrix-distributivity-draft-v1'
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
OPENING='First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:'
SUBTRACT='We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:'
# Fixed source expression/order; slots are whole supplied matrices. The canceled
# supplied values do not inflate the assessed task fingerprint.
SPECS={
 'q-13535':('easy','PQR','Q + R - (Q + P)','R','P','Q'),
 'q-13536':('moderate','ABC','(A+B)-C-(B-C)','A',None,'B'),
 'q-13550':('easy','JKL','K+L-(K+J)','L','J','K'),
 'q-13543':('easy','MNO','M+O-(N+M)','O','N','M'),
 'q-279581':('easy','ABC','A+B-(C+B)','A','C','B'),
 'q-69623':('easy','FGH','G+H-(H+F)','G','F','H'),
 'q-69627':('easy','CVN','C+V-(N+C)','V','N','C'),
 'authored-hard':('hard','ABCD','(A+B)-C-(B-C+D)','A','D','B')}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP['id']),x))
def matrix(rows):return matrix_tex(rows,augmented=False)
def parse_matrix(text):
 m=MATRIX.fullmatch(text.strip())
 if not m:raise ValueError('Expected ordinary bmatrix')
 return [[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]
def anchor(template):
 q=ORIGINALS[template]
 return {name:parse_matrix(m[0]) for name,m in zip(SPECS[template][1],MATRIX.finditer(q[':question/problem']))}
def result(p,t):
 _,_,_,x,y,_=SPECS[t]
 return sp.Matrix(p[x])-(sp.Matrix(p[y]) if y else sp.zeros(*sp.Matrix(p[x]).shape))
def replace_matrices(text,values):
 iterator=iter(values)
 out=MATRIX.sub(lambda _:matrix(next(iterator)),text)
 try:next(iterator);raise ValueError('Extra matrix mask component')
 except StopIteration:return out

def subtraction_cells(a,b):return [[str(x)+'-'+('('+str(y)+')' if y<0 else str(y)) for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def symbolic_stages(t):
 if t=='q-13536':return ['A+B-C-B+C',r'A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C}','A']
 if t=='authored-hard':return ['A+B-C-B+C-D',r'A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C}-D','A-D']
 expression=SPECS[t][2].replace(' ','');expanded=expression.replace('-(','-').replace(')','');position=expanded.index('-',expanded.index('+'))
 # Subtraction group contains two positive terms, both become negative.
 expanded=expanded[:position+1]+expanded[position+1:].replace('+','-')
 cancel=SPECS[t][5]
 canceled=re.sub(r'\b'+cancel+r'\b',lambda _:r'\cancel{'+cancel+'}',expanded)
 return [expanded,canceled,SPECS[t][3]+'-'+SPECS[t][4]]

def solution(p,t):
 r=result(p,t).tolist();x,y=SPECS[t][3:5]
 if t in ORIGINALS and ':question/worked-solution' in ORIGINALS[t]:
  original=ORIGINALS[t][':question/worked-solution']
  vals=[p[x]] if y is None else [p[x],p[y],subtraction_cells(p[x],p[y]),r]
  return replace_matrices(original,vals)
 stages=symbolic_stages(t);expr=SPECS[t][2]
 symbolic=r'\begin{aligned}'+expr+' & ='+stages[0]+r' \\  & ='+stages[1]+r' \\  & ='+stages[2]+r'\end{aligned}'
 first=OPENING+'\n\n$$\n'+symbolic+'\n$$\n\n'
 numerical=r'\begin{aligned}'+x+'-'+y+' & ='+matrix(p[x])+'-'+matrix(p[y])+r' \\  & ='+matrix(subtraction_cells(p[x],p[y]))+r' \\  & ='+matrix(r)+r'\end{aligned}'
 return first+SUBTRACT+'\n\n$$\n'+numerical+'\n$$'

def problem(p,t):
 if t in ORIGINALS:return replace_matrices(ORIGINALS[t][':question/problem'],[p[n] for n in SPECS[t][1]])
 return 'Find $'+SPECS[t][2]+'$, if\n\n$$\n'+r',\,'.join(n+'='+matrix(p[n]) for n in SPECS[t][1])+'.\n$$'

def raw_bank(p,t,f):
 # Every complete historical bank is kept as an explicit evidence profile.
 # Relative-cell masks parameterize opaque choices, without asserting recovered
 # distractor intentions or allowing them into learner defaults.
 old=anchor(t);a=result(old,t);b=result(p,t)
 values=[]
 for v in f.get(':answer-field/choices',[]):
  text=v[':answer/value']
  if MATRIX.fullmatch(text):
   m=sp.Matrix(parse_matrix(text))
   # Genuine supplied objects remain supplied objects, not output offsets.
   supplied=next((n for n in SPECS[t][1] if m==sp.Matrix(old[n])),None)
   val=matrix(p[supplied]) if supplied else matrix(sp.zeros(*m.shape).tolist()) if m.is_zero_matrix else matrix((b+m-a).tolist())
  else:
   index=int(f[':answer-field/key'].split('-')[-1])-1
   val=str(b[index//b.cols,index%b.cols]+int(text)-a[index//a.cols,index%a.cols])
  values.append(val)
 return values

def authored_bank(p,t):
 a=sp.Matrix(p[SPECS[t][3]]);z=sp.Matrix(p[SPECS[t][5]]);r=result(p,t)
 if SPECS[t][4] is None:
  c=sp.Matrix(p['C']);bank=[r,a-2*c,a+2*z,a-z,a-c]
 else:
  b=sp.Matrix(p[SPECS[t][4]])
  bank=[r,a+b,b-a,r+z,r-z]
 if len({tuple(m) for m in bank})!=5:raise ValueError('Whole complete method bank collides')
 return [matrix(m.tolist()) for m in bank]

def check_parameters(p,t,raw):
 _,names,_,_,_,_=SPECS[t]
 if set(p)!=set(names):raise ValueError('Exact matrix parameter names required')
 shape=(len(p[names[0]]),len(p[names[0]][0]))
 expected=(3,2) if t=='authored-hard' else tuple(sp.Matrix(anchor(t)[names[0]]).shape)
 if shape!=expected:raise ValueError('Template matrix shape')
 limit=60 if raw else 9
 for n in names:
  if len(p[n])!=shape[0] or any(len(row)!=shape[1] for row in p[n]):raise ValueError('Conformable rectangular matrices required')
  bound=60 if n not in [SPECS[t][3],SPECS[t][4]] else limit
  if any(type(v)is not int or abs(v)>bound for row in p[n] for v in row):raise ValueError('Bounded integer matrix entries')
 if not raw and t=='authored-hard':
  for n in ['A','D']:
   if not any(v<0 for row in p[n] for v in row) or not any(v>0 for row in p[n] for v in row):raise ValueError('Hard surviving matrices require mixed signs')
 if not raw and t=='q-13536' and not any(v!=0 for row in p['A'] for v in row):raise ValueError('Nonzero surviving matrix')

def make_fields(p,t,profile,raw):
 if raw:
  q=ORIGINALS[t];fields=[]
  if ':question/answer-fields' not in q:return None
  for f in q[':question/answer-fields']:
   vals=raw_bank(p,t,f)
   correct=None
   if ':answer-field/correct' in f:correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
   fields.append((f[':answer-field/key'],f[':answer-field/type'][':db/ident'],vals,correct))
  return fields
 if t=='q-279581':return [('field-'+str(i+1),':answer-field.type/blank',[str(v)],0) for i,v in enumerate(result(p,t))]
 return [('selection',':answer-field.type/radio',authored_bank(p,t),0)]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 eligible=[t for t,s in SPECS.items() if s[0]==level]
 if field_type is not None:
  ft=field_type.split('/')[-1]
  if ft not in ['radio','blank']:raise ValueError('Source-supported field type required')
  eligible=[t for t in eligible if ('blank' if t=='q-279581' else 'radio')==ft]
 if template is None:
  if not eligible:raise ValueError('No supported template for requested field type/level')
  template=rng.choice(eligible)
 if template not in SPECS:raise ValueError('Unknown template')
 # Bank is fixed before sampling any parameters. raw is never a default.
 profile=profile or 'authored-method'
 raw=profile=='source-original'
 if profile not in ['source-original','authored-method']:raise ValueError('Unsupported complete profile')
 if raw and template not in ORIGINALS:raise ValueError('No observed hard profile')
 if SPECS[template][0]!=level:raise ValueError('Level/template scope mismatch')
 if field_type is not None:
  expected='blank' if template=='q-279581' else 'radio'
  if field_type not in [expected,':answer-field.type/'+expected]:raise ValueError('Source-shaped field contract')
 for _ in range(1000):
  names=SPECS[template][1];shape=(3,2) if template=='authored-hard' else sp.Matrix(anchor(template)[names[0]]).shape
  p=copy.deepcopy(parameters) if parameters is not None else {n:[[rng.randint(-9,9) for _ in range(shape[1])] for _ in range(shape[0])] for n in names}
  try:
   check_parameters(p,template,raw);fields=make_fields(p,template,profile,raw);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('Whole-bank resampling exhausted')
 q={':question/problem':problem(p,template)}
 if not raw or ':question/worked-solution' in ORIGINALS[template]:q[':question/worked-solution']=solution(p,template)
 if not raw or ':question/difficulty' in ORIGINALS[template]:q[':question/difficulty']=':question.difficulty/'+level
 if fields is not None:q[':question/answer-fields']=[]
 for index,(key,typ,vals,correct) in enumerate(fields or []):
  f={':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in vals]}
  if correct is not None:f['_correct_index']=correct
  q[':question/answer-fields'].append(f)
 if not raw:
  q[':question/problem']=normalize_prose(q[':question/problem']);q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
 canonical=copy.deepcopy(q)
 for f in canonical.get(':question/answer-fields',[]):
  if '_correct_index' in f:f['_correct_value']=f[':answer-field/choices'][f.pop('_correct_index')][':answer/value']
  f[':answer-field/choices'].sort(key=lambda a:json.dumps(a,sort_keys=True))
 identity=digest([VERSION,canonical])
 qid=uid(identity);q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  fid=uid(qid+':field:'+str(i)+':'+f[':answer-field/key']);f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:a[':answer/id']=uid(fid+':'+a[':answer/value'])
  if '_correct_index'in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][f.pop('_correct_index')][':answer/id']]
  if f[':answer-field/type']==':answer-field.type/radio':random.Random(seed+i+781).shuffle(f[':answer-field/choices'])
 x,y=SPECS[template][3:5]
 # Canonical assessed operation: symbolic distributivity structure with names
 # alpha-normalized, plus surviving operands. Canceled entries are incidental.
 symbols={n:sp.Symbol('v'+str(i)) for i,n in enumerate(SPECS[template][1])}
 tokens=re.findall(r'[A-Z]|[()+-]',SPECS[template][2]);aliases={}
 canon=[]
 for v in tokens:
  if v.isalpha():aliases.setdefault(v,str(len(aliases)));canon.append('m'+aliases[v])
  else:canon.append(v)
 family='single-cancellation-difference' if SPECS[template][0]=='easy' else 'double-cancellation-survivor' if SPECS[template][0]=='moderate' else 'double-cancellation-difference'
 fp=digest([family,p[x],p[y] if y else None,('full-matrix',shape)])
 record={'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'template':template,'bank_profile':profile,'parameters':p,'seed':seed,'parameter_fingerprint':fp,'mathematical_key':fp,'content_hash':identity,'source':{k:v for k,v in SOURCE.items() if k!='record'},'source_question':template if template in ORIGINALS else None,'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_evidence':'observed' if template in ORIGINALS and ':question/difficulty' in ORIGINALS[template] else 'authored; calibration uncertain','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'bank_interpretation':'opaque relative-cell masks; supplied-object choices explicit; no recovered wrong-operation claim' if raw else 'complete method bank: correct; fail negative distribution on subtractand; reverse residual difference; retain positive canceled term; retain negative canceled term' if SPECS[template][4] else 'complete method bank: correct; fail reversing inner negative C; fail reversing inner B; drop leading B; drop final positive C','domain':'ordinary conformable integer matrices; source shapes; normal assessed entries -9..9; canceled entries -60..60; hard 3x2 mixed-sign surviving operands'}}
 if not raw:validate_generated_record(record)
 return record

# Easy: six source-shaped single-cancellation families; fieldless/unrated
# originals are completed only in authored learner output.
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)
# Moderate: observed double cancellation; whole source bank evidence-only.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)
# Hard: authored double cancellation + signed surviving subtraction.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)
def markdown(r):
 q=r['question'];text=q[':question/problem']
 for f in q.get(':question/answer-fields',[]):
  text+='\n\n'+f[':answer-field/key']+':\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])
 return text+'\n\n'+q.get(':question/worked-solution','[Absent in raw source]')
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=2);a.add_argument('--format',choices=['json','markdown'],default='json');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 if args.count<1:a.error('Positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
