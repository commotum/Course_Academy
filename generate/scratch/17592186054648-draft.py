#!/usr/bin/env python3
"""Draft only: parameterized 2x2 entrywise addition; registered numeric baseline untouched.

Four observed prompt/solution backbones and five complete evidence-bank profiles.
Default banks are explicitly authored; observed opaque patterns require explicit
parameters and remain evidence-only. Moderate/hard are authored arithmetic bands.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex, normalize_prose, normalize_tex, validate_generated_record, validate_prose, validate_tex, FORMAT_VERSION
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186054648; KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']; VERSION='2.1.0-draft'
LEVELS=('easy','moderate','hard')
TEMPLATES={'named-radio':{'field_type':'radio'},'inline-question':{'field_type':'radio'},'inline-equality':{'field_type':'radio'},'cell-blanks':{'field_type':'blank'}}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def flatten(body): return [x.strip() for row in body.split(r'\\') for x in row.split('&')]
def read_values(text): return [[int(x) for x in flatten(m)] for m in MATRIX.findall(text)]
def latex(v):return matrix_tex([v[:2],v[2:]])
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(parent,v):return str(uuid.uuid5(uuid.UUID(parent),str(v)))
def addition(p):return [int(v) for v in sp.Matrix(p['a'])+sp.Matrix(p['b'])]
def change(c,i,x):v=c.copy();v[i]=x;return v
# These are exact observed expression patterns, not inferred cognitive explanations.
# Opaque copies/offsets/compound errors are retained only in explicit evidence profiles.
def observed_bank(name,p):
 a,b=p['a'],p['b'];c=addition(p)
 if name=='observed-q-101':return [[c[0],-(a[1]-b[1]),c[2],-abs(a[3])-abs(b[3])],[c[0],a[1]-b[1],a[2],c[3]],[-(a[0]-b[0]),-(a[1]-b[1]),c[2],c[3]],c,change(c,3,-abs(a[3])-abs(b[3]))]
 if name=='observed-q-11440':return [c,[a[1],a[0],c[2],c[3]],[a[1]]*4,[-c[0],c[1],c[2],-c[3]],[c[0]]*4]
 if name=='observed-q-100':return [[a[0]-b[0],b[1]-a[1],c[2],c[3]],change(c,1,b[1]-a[1]),c,[c[1]]*4,change(c,0,-c[0])]
 if name=='observed-q-125630':return [change(c,2,c[1]),change(c,1,b[3]),c,change(c,2,c[0]),change(c,0,c[0]+1)]
 if name=='observed-q-125631':return [change(c,0,a[3]),change(c,1,-c[1]),[-c[0],c[1],-c[2],c[3]],c,change(c,1,a[1])]
 raise ValueError('Unknown observed bank')
OBSERVED_RECIPES={
 'observed-q-101':['[c00, -(a01-b01), c10, -|a11|-|b11|]','[c00, a01-b01, a10, c11]','[-(a00-b00), -(a01-b01), c10, c11]','c','c with c11=-|a11|-|b11|'],
 'observed-q-11440':['c','[a01,a00,c10,c11]','all entries=a01','[-c00,c01,c10,-c11]','all entries=c00'],
 'observed-q-100':['[a00-b00,b01-a01,c10,c11]','c with c01=b01-a01','c','all entries=c01','c with c00=-c00'],
 'observed-q-125630':['c with c10=c01','c with c01=b11','c','c with c10=c00','c with c00=c00+1 (observed offset; intent unresolved)'],
 'observed-q-125631':['c with c00=a11','c with c01=-c01','[-c00,c01,-c10,c11]','c','c with c01=a01']}
AUTHORED_RECIPES={
 'authored-correspondence':['entrywise A+B','entrywise A-B','entrywise B-A','retain A without adding B','transpose the complete sum'],
 'authored-signs':['entrywise A+B','add absolute B entries','add absolute A entries to B','negate the complete sum','add transposed B instead of corresponding B']}
# Field-presence contracts are extracted independently of prompt/solution/value recipes.
# Raw API assembly never returns a captured question payload or literal choice bank.
RAW_PROFILES={}
for _q in SOURCE['record'][':knowledge-point/questions']:
 _ma=_q.get(':question/math-academy-id');_name='raw-'+(_ma or 'independent-'+str(_q[':db/id']))
 _template='inline-question' if _ma=='q-101' else 'inline-equality' if _ma=='q-100' else 'cell-blanks' if '{{field-' in _q[':question/problem'] else 'named-radio'
 RAW_PROFILES[_name]={'template':_template,'bank':'observed-'+_ma if _template!='cell-blanks' else None,
  'difficulty':_q.get(':question/difficulty',{}).get(':db/ident'),'solution_present':':question/worked-solution' in _q,
  'fields':[{'key':_f[':answer-field/key'],'type':_f[':answer-field/type'][':db/ident'].split('/')[-1],'correct_present':':answer-field/correct' in _f} for _f in _q.get(':question/answer-fields',[])],
  'source_db_id':_q[':db/id'],'role':'MA original' if _ma else 'independently authored inventory'}
BANK_PROFILES={**{k:{'origin':'observed-completed-evidence-only','recipes':v} for k,v in OBSERVED_RECIPES.items()},**{k:{'origin':'authored','recipes':v} for k,v in AUTHORED_RECIPES.items()},**{k:{'origin':'raw-evidence-only','recipes':OBSERVED_RECIPES[v['bank']] if v['bank'] else []} for k,v in RAW_PROFILES.items()}}

def bank(profile,p):
 if profile.startswith('observed-'):return observed_bank(profile,p)
 a,b=p['a'],p['b'];c=addition(p)
 if profile=='authored-correspondence':return [c,[x-y for x,y in zip(a,b)],[y-x for x,y in zip(a,b)],a.copy(),[c[0],c[2],c[1],c[3]]]
 if profile=='authored-signs':return [c,[x+abs(y) for x,y in zip(a,b)],[abs(x)+y for x,y in zip(a,b)],[-x for x in c],[a[i]+b[j] for i,j in enumerate((0,2,1,3))]]
 raise ValueError('Unknown bank profile')
class SampleRejected(ValueError):pass

def canonical_parameters(p):
 if not isinstance(p,dict) or set(p)-{'a','b','names','wrap_first','nested'}:raise ValueError('Unknown parameter slot')
 p=copy.deepcopy(p);p.setdefault('names',['A','B']);p.setdefault('wrap_first',[]);p.setdefault('nested',False)
 if set(p)!= {'a','b','names','wrap_first','nested'}:raise ValueError('Supply both operand matrices')
 if any(not isinstance(p[k],list) or len(p[k])!=4 or any(type(v)!=int for v in p[k]) for k in ('a','b')):raise ValueError('Each operand needs four exact integer entries')
 if not isinstance(p['names'],list) or len(p['names'])!=2 or len(set(p['names']))!=2 or any(not re.fullmatch('[A-Z]',x) for x in p['names']):raise ValueError('Distinct uppercase matrix names required')
 if not isinstance(p['wrap_first'],list) or any(type(x)!=int or x not in range(4) for x in p['wrap_first']):raise ValueError('Invalid notation slots')
 p['wrap_first']=sorted(set(p['wrap_first']))
 if type(p['nested'])!=bool:raise ValueError('nested must be boolean')
 return p

def validate_parameters(level,p):
 a,b=p['a'],p['b'];vals=a+b
 if level=='easy':
  if any(abs(x)>12 for x in vals):raise ValueError('Easy entries must be between -12 and 12')
 elif level=='moderate':
  if any(not 1<=abs(x)<=25 for x in vals) or sum(x*y<0 for x,y in zip(a,b))!=2 or sum(abs(x)>=10 for x in vals)<2:raise ValueError('Moderate: nonzero ±1..25, two opposite-sign pairs and at least two two-digit entries')
 elif level=='hard':
  c=addition(p)
  if any(not 10<=abs(x)<=99 for x in vals) or any(x*y>=0 for x,y in zip(a,b)) or sum(x>0 for x in c)!=2 or sum(x<0 for x in c)!=2:raise ValueError('Hard: opposite-sign two-digit pairs; two positive and two negative sums')
 else:raise ValueError('Unknown level')

def sample(level,rng):
 p={'names':['A','B'],'wrap_first':[],'nested':False}
 if level=='easy':p.update(a=[rng.randint(-12,12) for _ in range(4)],b=[rng.randint(-12,12) for _ in range(4)])
 elif level=='moderate':
  a=[rng.choice((-1,1))*rng.randint(1,25) for _ in range(4)];opp=set(rng.sample(range(4),2));b=[(-1 if i in opp else 1)*(1 if x>0 else -1)*rng.randint(1,25) for i,x in enumerate(a)];p.update(a=a,b=b)
 else:
  a=[];b=[];positive=set(rng.sample(range(4),2))
  for i in range(4):
   sign=rng.choice((-1,1));small=rng.randint(10,98);large=rng.randint(small+1,99)
   # C sign is determined by the larger absolute operand.
   large_a=(sign>0)==(i in positive)
   a.append(sign*(large if large_a else small));b.append(-sign*(small if large_a else large))
  p.update(a=a,b=b)
 return canonical_parameters(p)

def prompt_solution(template,p):
 a,b,c=p['a'],p['b'],addition(p);A,B=p['names'];pair=A+'+'+B
 ma,mb=latex(a),latex(b)
 if template=='named-radio':prompt='Calculate $'+pair+'$, where\n\n$$\n'+A+'='+ma+r',\,'+B+'='+mb+'.\n$$'
 elif template=='inline-question':prompt='What is $'+ma+' + '+mb+'$?'
 elif template=='inline-equality':prompt='$'+ma+'+'+mb+'=$'
 elif template=='cell-blanks':prompt='Calculate $'+pair+',$ where $'+A+'='+ma+'$ and \n$'+B+'='+mb+'.$\n\n| $'+pair+r'=\,\,$ |  | {{field-1}} | {{field-2}} |  |'+'\n| --- | --- | --- | --- | --- |\n|  | {{field-3}} | {{field-4}} |  |  |'
 else:raise ValueError('Unknown template')
 terms=[]
 for i,(x,y) in enumerate(zip(a,b)):
  left='('+str(x)+')' if x<0 and i in p['wrap_first'] else str(x)
  right='('+str(y)+')' if y<0 else str(y)
  terms.append(left+'+'+right)
 opening=r'\begin{aligned}'+(pair+' & ='+ma+'+'+mb if template!='inline-equality' else ma+'+'+mb+' & ='+latex(terms))
 if template!='inline-equality':opening+=r' \\  & ='+latex(terms)
 solution=opening+r' \\  & ='+latex(c)+r'\end{aligned}'
 if p['nested']:solution=r'\begin{aligned}'+solution+r'\end{aligned}'
 solution='We add the corresponding entries:\n\n$$\n'+solution+'\n$$'
 return normalize_prose(prompt),normalize_prose(solution)

# EASY — observed 2x2 integer addition, same whole-matrix or four-cell response.
# MODERATE — authored signed-entry workload; same four additions, no new stage.
# HARD — authored two-digit sign comparisons; same operation/layout/stages.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Supported levels: easy, moderate, hard')
 if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
 raw=RAW_PROFILES.get(profile)
 if raw or profile and profile.startswith('observed-'):
  if parameters is None:raise ValueError('Raw/observed evidence-only profiles require explicit parameters')
  if level!='easy':raise ValueError('Observed profiles use the easy dispatch band; raw absence of rating is preserved')
  inferred=raw['template'] if raw else {'observed-q-101':'inline-question','observed-q-100':'inline-equality'}.get(profile,'named-radio')
  if template and template!=inferred:raise ValueError('Observed profile/backbone mismatch')
  template=inferred
 eligible=[t for t,v in TEMPLATES.items() if not field_type or v['field_type']==field_type]
 if template and template not in eligible:raise ValueError('Unsupported template/field type')
 if not eligible:raise ValueError('Unsupported field type')
 fixed=canonical_parameters(parameters) if parameters is not None else None
 select=random.Random(digest([level,fixed])) if fixed is not None else random.Random(seed)
 template=template or select.choice(eligible);radio=TEMPLATES[template]['field_type']=='radio'
 if not radio and profile and not raw:raise ValueError('Normal blanks have no choice-bank profile')
 profile=(profile or select.choice(list(AUTHORED_RECIPES))) if radio else profile
 effective_profile=raw['bank'] if raw else profile
 rng=random.Random(seed)
 for _ in range(1024):
  p=fixed or sample(level,rng)
  try:validate_parameters(level,p)
  except ValueError:
   if fixed is not None:raise
   continue
  values=bank(effective_profile,p) if radio else [[x] for x in addition(p)]
  if radio and (len(values)!=5 or len(set(map(tuple,values)))!=5):
   if fixed is not None:raise SampleRejected('Complete bank has equivalent options')
   continue
  prompt,solution=prompt_solution(template,p);c=addition(p)
  strings=[normalize_tex(latex(v)) for v in values] if radio else [str(x) for x in c]
  contracts=raw['fields'] if raw else ([{'key':'selection','type':'radio','correct_present':True}] if radio else [{'key':'field-'+str(i+1),'type':'blank','correct_present':True} for i in range(4)])
  identity_fields=[]
  for contract in contracts:
   key=contract['key'];slot=int(key.split('-')[-1])-1 if contract['type']=='blank' else 0
   vals=strings if radio else [strings[slot]];correct=latex(c) if radio else strings[slot]
   row={'key':key,'type':contract['type'],'bank':sorted(vals)}
   if contract['correct_present']:row['correct']=correct
   identity_fields.append(row)
  difficulty=raw['difficulty'] if raw else ':question.difficulty/'+level
  displayed_solution=solution if not raw or raw['solution_present'] else None
  # Attribute presence, displayed grade, full prompt/solution and whole keyed banks
  # enter identity; profile aliases, generation seed and choice order do not.
  content=digest([VERSION,difficulty,prompt,displayed_solution,sorted(identity_fields,key=lambda f:json.dumps(f,sort_keys=True))]);qid=uid(KP_UUID,content);fields=[]
  for i,contract in enumerate(contracts):
   key=contract['key'];slot=int(key.split('-')[-1])-1 if contract['type']=='blank' else 0
   # Duplicate raw keys have separate field ownership; normal unique keys stay stable.
   occurrence=sum(x['key']==key for x in contracts[:i]);fid=uid(qid,key if occurrence==0 else key+'#'+str(occurrence))
   vals=strings if radio else [strings[slot]];answers=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
   if radio:random.Random(seed+i).shuffle(answers)
   field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+contract['type'],':answer-field/choices':answers}
   if contract['correct_present']:field[':answer-field/correct']=[':answer/id',uid(fid,latex(c) if radio else strings[slot])]
   fields.append(field)
  question={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
  if difficulty is not None:question[':question/difficulty']=difficulty
  if displayed_solution is not None:question[':question/worked-solution']=displayed_solution
  mathematical=digest(sorted([p['a'],p['b']]))
  record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':profile,'operation_profile':effective_profile,'bank_origin':BANK_PROFILES[profile]['origin'] if profile else 'no-bank','bank_recipes':BANK_PROFILES[profile]['recipes'] if profile else [],'authored_level':not raw and level!='easy','raw_replay':bool(raw),'raw_source_role':raw['role'] if raw else None,'raw_source_db_id':raw['source_db_id'] if raw else None,'evidence_only':bool(raw or profile and profile.startswith('observed-')),'native_eligible':not raw or all(contract['correct_present'] for contract in contracts),'source_database':SOURCE['database'],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'content_fingerprint':content,'mathematical_fingerprint':mathematical,'parameter_fingerprint':mathematical,'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'plot_rating':'none','assets':[]}}
  if raw:
   # Raw absent attributes stay absent; shared format checks run on every present item.
   validate_prose(prompt)
   if displayed_solution is not None:validate_prose(displayed_solution)
   for field in fields:
    for answer in field[':answer-field/choices']:validate_tex(answer[':answer/value'])
   record['generation']['math_format']=FORMAT_VERSION
   return record
  return validate_generated_record(record)
 raise SampleRejected('Complete bank failed bounded parameter sampling')

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  correct=f.get(':answer-field/correct',[None,None])[1]
  s+='\n'+f[':answer-field/key']+':\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])+'\n'
 return s+'\nWorked solution:\n\n'+q.get(':question/worked-solution','Absent in raw source evidence.')
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template',choices=tuple(TEMPLATES));parser.add_argument('--profile',choices=tuple(BANK_PROFILES));parser.add_argument('--parameters',help='JSON operand/notation slots; required for evidence profiles');parser.add_argument('--field-type',choices=('radio','blank'));parser.add_argument('--format',choices=('markdown','json'),default='markdown');a=parser.parse_args()
 if a.count<1:parser.error('--count must be positive')
 levels=LEVELS if a.difficulty=='all' else (a.difficulty,)
 try:records=[generate(l,a.seed+i,a.template,a.field_type,json.loads(a.parameters) if a.parameters else None,a.profile) for l in levels for i in range(a.count)]
 except ValueError as e:parser.error(str(e))
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
