#!/usr/bin/env python3
"""Subtracting Matrices, private basis2275 draft; registered numeric package is frozen.

Seven MA masks, four five-option historical banks, three six-blank layouts.
Historical banks are public evidence-only profiles observed:<MA-id>; scalar
recipes that exactly reproduce opaque options do NOT claim recovered intention.
Normal radio banks are separately authored corresponding-entry operation banks.
All source raw attribute omissions survive public evidence replay. Defaults use
an authored sign-workload policy across every observed layout: easy nonnegative
operands, moderate exactly one requested negative subtrahend, hard three signed
arithmetic roles including two different subtract-negative roles. Moderate and
hard grades are design claims without observed labels; original easy labels are
retained in evidence and are never reclassified. No new matrix operation, field
count, or solution stage is added. See classification/template-extraction.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard have the same optional arguments.
Parameters a,b are flattened integer matrices; targets is six ordered target
cells only in the partial 3x3 family. Explicit invalid inputs raise ValueError.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,normalize_tex,validate_generated_record,validate_prose,validate_tex
HERE=Path(__file__).with_suffix('')
S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186054649;KP_UUID=S['record'][':knowledge-point/id'];TITLE=S['record'][':knowledge-point/title'];VERSION='subtract-matrices-b2275-draft-1'
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES=tuple(SOURCES)
RADIO=('q-108','q-11478','q-11441','q-69603')
LEVEL_TEMPLATES={level:TEMPLATES for level in ('easy','moderate','hard')}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
LHS={'q-108':None,'q-11478':'P-Q','q-11441':'A-B','q-69603':None,'q-319618':'C-D','q-319622':'G-H','q-319625':'P-Q'}
def parse(text):return [[int(v.strip().replace(r'\,','')) for v in row.split('&')] for row in text.split(r'\\')]
def matrices(text):return [parse(m) for m in MATRIX.findall(text)]
def flat(rows):return [v for row in rows for v in row]
def shape(t):
 a,b=matrices(SOURCES[t][':question/problem']);return len(a),len(a[0])
def original(t):
 a,b=matrices(SOURCES[t][':question/problem']);p={'a':flat(a),'b':flat(b)}
 if t=='q-319625':p['targets']=[0,1,4,5,6,8]
 return p

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(parent,x):return str(uuid.uuid5(uuid.UUID(parent),str(x)))
def difference(p):return list(map(int,sp.Matrix(p['a'])-sp.Matrix(p['b'])))
def observed_bank(t,p):
 """Parameterized exact expression patterns, historical intention unresolved."""
 a,b=p['a'],p['b'];c=difference(p)
 def changed(index,value):
  d=c.copy();d[index]=value;return d
 if t=='q-108':return [changed(0,a[0]+b[0]),c,changed(2,a[2]+b[2]),changed(1,-(a[1]+b[1])),changed(3,a[3]+b[3])]
 if t=='q-11478':return [[a[0]-a[3],a[0]-a[3],c[2],c[3]],[c[2],c[3],c[1],c[0]],c,[c[2],c[3],c[0],c[1]],[c[0],c[1],-c[2],-c[3]]]
 if t=='q-11441':return [changed(3,-c[3]),[a[0]]*4,changed(1,c[0]),[c[3]]*4,c]
 if t=='q-69603':return [[a[0]+b[0],a[1]+b[1],a[2]+b[2],c[3],a[4]+b[4],a[5]+b[5]],c[3:]+c[:3],c,[c[0],-(a[1]+b[1]),c[2],c[3],a[4]+b[4],b[5]],[c[0],c[2],c[1],c[3],c[5],c[4]]]
 return None

def authored_bank(t,p):
 """Complete five-option method bank, selected before parameters.
 C; all-entry addition; reversed difference; addition at cell0 only;
 reversed subtraction at cell1 only. No unrelated scalar perturbations.
 """
 a,b=p['a'],p['b'];c=difference(p)
 u=c.copy();u[0]=a[0]+b[0]
 v=c.copy();v[1]=b[1]-a[1]
 return [c,[x+y for x,y in zip(a,b)],[-x for x in c],u,v] if t in RADIO else None

def validate_parameters(level,t,p,raw=False):
 nr,nc=shape(t);n=nr*nc
 if set(p)!=({'a','b','targets'} if t=='q-319625' else {'a','b'}):raise ValueError('Unexpected or missing parameter keys')
 if not all(isinstance(p[k],list) and len(p[k])==n and all(type(x)==int and -12<=x<=12 for x in p[k]) for k in ('a','b')):raise ValueError('Integer matrix entries must have the source-grounded bound -12..12')
 if t=='q-319625':
  z=p['targets']
  if not isinstance(z,list) or len(z)!=6 or z!=sorted(set(z)) or not all(type(i)==int and 0<=i<9 for i in z):raise ValueError('Six ordered distinct target cells required')
 if raw:return
 if t not in LEVEL_TEMPLATES[level]:raise ValueError('Template outside authored level workload')
 if level=='easy' and not all(0<=x<=9 for x in p['a']+p['b']):raise ValueError('Easy: nonnegative one-digit entry subtractions')
 if level in ('moderate','hard'):
  targets=p.get('targets',range(n))
  if level=='moderate':
   if sum(p['b'][i]<0 for i in targets)!=1 or not any(p['a'][i]<0 for i in targets) or not any(p['b'][i]>0 for i in targets):raise ValueError('Moderate requires exactly one requested negative subtrahend, a negative minuend, and a positive subtrahend')
  else:
   roles=[any(test(p['a'][i],p['b'][i]) for i in targets) for test in (lambda a,b:a<0 and b<0,lambda a,b:a>0 and b<0,lambda a,b:a<0 and b>0)]
   if not all(roles):raise ValueError('Hard requires negative-minus-negative, positive-minus-negative and negative-minus-positive requested cells')

def render(t,p,raw):
 nr,nc=shape(t);n=nr*nc;c=difference(p)
 def mat(v):return matrix_tex([v[i:i+nc] for i in range(0,n,nc)])
 it=iter((mat(p['a']),mat(p['b'])))
 prompt=MATRIX.sub(lambda _:next(it),SOURCES[t][':question/problem'])
 if t=='q-319625':
  cells={i:'{{field-'+str(j+1)+'}}' for j,i in enumerate(p['targets'])}
  rows=[[cells.get(i,'$'+str(c[i])+'$') for i in range(r*nc,(r+1)*nc)] for r in range(nr)]
  prompt=prompt.split('\n\n|')[0]+'\n\n| $P-Q=\\,\\,$ |  | '+' | '.join(rows[0])+' |  |\n| --- | --- | --- | --- | --- | --- |\n'+'\n'.join('|  | '+' | '.join(row)+' |  |  |' for row in rows[1:])
 # Explicit ordered nodes retain every subtraction, including negative operands.
 operations=[str(a)+'-'+('('+str(b)+')' if b<0 else str(b)) for a,b in zip(p['a'],p['b'])]
 result=[str(v) for v in c]
 if raw and t=='q-319625':result[1]=r'\,\,'+result[1];result[3]=r'\,\,\,'+result[3]
 lhs=LHS[t] or mat(p['a'])+'-'+mat(p['b'])
 stages=lhs+' & ='
 if t not in ('q-108','q-69603'):stages+=mat(p['a'])+'-'+mat(p['b'])+r' \\  & ='
 stages+=mat(operations)+r' \\  & ='+mat(result)
 solution='We subtract the corresponding entries:\n\n$$\n'+r'\begin{aligned}'+stages+r'\end{aligned}'+'\n$$'
 return prompt,solution,mat,c

def fingerprint(t,p):
 nr,nc=shape(t)
 # Source naming, bank, difficulty, option order are not mathematical tasks.
 return digest({'shape':[nr,nc],'requested_pairs':[[i,p['a'][i],p['b'][i]] for i in p.get('targets',list(range(nr*nc)))]})

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVEL_TEMPLATES:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio','blank',':answer-field.type/radio',':answer-field.type/blank'):raise ValueError('Unknown field type')
 ft=field_type.rsplit('/',1)[-1] if field_type else None
 raw=bool(profile and profile.startswith('observed:'))
 if profile and profile not in ('authored-method','authored-entry','method-derived','entry') and not raw:raise ValueError('Unknown bank profile')
 rng=random.Random(seed)
 if raw:
  source_t=profile.split(':',1)[1]
  if template and template!=source_t:raise ValueError('Observed profile/template mismatch')
  template=source_t
 eligible=list(LEVEL_TEMPLATES[level])
 if ft:eligible=[t for t in eligible if (t in RADIO)==(ft=='radio')]
 if template:
  if template not in SOURCES:raise ValueError('Unknown template')
  if ft and (template in RADIO)!=(ft=='radio'):raise ValueError('Field type/template mismatch')
  if not raw and template not in eligible:raise ValueError('Template outside level or field domain')
  t=template
 elif eligible:t=rng.choice(eligible)
 else:raise ValueError('No template supports requested level/field')
 canonical_profile=('observed:'+t) if raw else ('authored-method' if t in RADIO else 'authored-entry')
 if profile in ('authored-method','method-derived') and t not in RADIO:raise ValueError('Radio bank incompatible with blanks')
 if profile in ('authored-entry','entry') and t in RADIO:raise ValueError('Blank profile incompatible with radio')
 n=shape(t)[0]*shape(t)[1]
 def values(p):return observed_bank(t,p) if raw else authored_bank(t,p)
 if parameters is None:
  for _ in range(10000):
   lo,hi=(0,9) if level=='easy' and not raw else (-12,12)
   p={'a':[rng.randint(lo,hi) for _ in range(n)],'b':[rng.randint(lo,hi) for _ in range(n)]}
   if t=='q-319625':p['targets']=sorted(rng.sample(range(n),6))
   try:validate_parameters(level,t,p,raw)
   except ValueError:continue
   bank=values(p)
   if bank is None or len({tuple(v) for v in bank})==5:break
  else:raise ValueError('Whole-bank sampling exhausted')
 else:p=copy.deepcopy(parameters);validate_parameters(level,t,p,raw);bank=values(p)
 if bank is not None and len({tuple(v) for v in bank})!=5:raise ValueError('Whole bank has mathematically equivalent choices')
 source=SOURCES[t];prompt,solution,mat,c=render(t,p,raw)
 if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)
 q={':question/problem':prompt}
 if not raw or ':question/worked-solution' in source:q[':question/worked-solution']=solution
 if raw:
  q[':question/math-academy-id']=t
  if ':question/difficulty' in source:q[':question/difficulty']=source[':question/difficulty'][':db/ident']
 else:q[':question/difficulty']=':question.difficulty/'+level
 field_content=[]
 for j,idx in enumerate([0] if t in RADIO else p.get('targets',range(n))):
  key='selection' if t in RADIO else 'field-'+str(j+1)
  strings=[mat(v) for v in bank] if bank is not None else [str(c[idx])]
  if not raw:strings=list(map(normalize_tex,strings))
  sf=next(f for f in source[':question/answer-fields'] if f[':answer-field/key']==key)
  correct=mat(c) if bank is not None else str(c[idx])
  field_content.append((key,strings,correct,not raw or ':answer-field/correct' in sf))
 # IDs include all displayed content (order-independent complete bank), grade,
 # and actual source-presence behavior, never seed, profile alias or incidental parameters.
 content={'version':VERSION,'question':copy.deepcopy(q),'fields':[(k,sorted(v),c,has) for k,v,c,has in field_content]}
 ident=uid(KP_UUID,digest(content));fields=[]
 for key,strings,correct,has in field_content:
  fid=uid(ident,key);answers=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
  if bank is not None:rng.shuffle(answers)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if bank is not None else 'blank'),':answer-field/choices':answers}
  if has:f[':answer-field/correct']=[':answer/id',uid(fid,correct)]
  fields.append(f)
 q[':question/id']=ident;q[':question/answer-fields']=fields
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':canonical_profile,'parameters':p,'source_id':source[':db/id'],'source_basis':S['basis'],'source_lineage':S['lineage'],'source_database':S['database'],'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_evidence':'captured label/omission' if raw else ('authored conservative policy; moderate/hard grades unobserved'),'mathematical_fingerprint':fingerprint(t,p),'content_fingerprint':digest(content),'dependency_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'assets':[]}}
 if raw:
  for k in (':question/problem',':question/worked-solution'):
   if k in q:validate_prose(q[k])
  for f in fields:
   for a in f[':answer-field/choices']:validate_tex(a[':answer/value'])
 else:validate_generated_record(record)
 return record

# Easy: nonnegative one-digit operand subtractions, every observed layout.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate (authored grade): exactly one requested subtract-negative cell.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard (authored grade): three distinct signed arithmetic roles, same layouts.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];pieces=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):pieces.append(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
 if ':question/worked-solution' in q:pieces.append(q[':question/worked-solution'])
 return '\n\n'.join(pieces)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 levels=list(LEVEL_TEMPLATES) if args.difficulty=='all' else [args.difficulty]
 out=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
