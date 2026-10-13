#!/usr/bin/env python3
"""Count displayed matrix rows, then columns. No entry arithmetic is assessed.

Six labeled easy sources; the two unrated legacy cases receive authored easy
assignments. Only easy is supported. Moderate/hard lack a validated higher
demand. There are 25 finite ordered dimension tasks across the package.
Explicit observed profiles replay source formatting and complete recipe banks;
normal banks use ordered \\times dimensions and repair the P/R naming error.
"""
from pathlib import Path
import argparse,hashlib,json,random,re,uuid
import sympy as sp
KP_ID=17592186087693
KP_UUID='f6ae25fc-16eb-598b-a288-742e4b46cb12'
TITLE='Determining the Dimensions of a Matrix'
VERSION='1.1.0'
SUPPORTED_LEVELS=('easy',)
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
HERE=Path(__file__).resolve().with_suffix('')
OBSERVED=json.loads((HERE/'recipes.json').read_text())
TEMPLATES=tuple(sorted({p['template'] for p in OBSERVED.values()}|{'display-radio','display-dual-blank'}))
BANK_PROFILES={**OBSERVED,'authored-rectangular':{'template':'display-radio','field_type':'radio','bank':[{'recipe':s,'separator':r'\times '} for s in ('r,c','c,r','r,r','c,c','r+1,c+1')]},'authored-square':{'template':'display-radio','field_type':'radio','bank':[{'recipe':s,'separator':r'\times '} for s in ('r,c','r-1,c-1','r+1,c+1','r,c+1','r+1,c')]}}
DIMENSIONS=tuple((r,c) for r in range(2,7) for c in range(2,7))
DOMAIN={'rows':[2,6],'columns':[2,6],'meaningful_dimension_pairs':25,'entries':'integers | sqrt positive integers 2..13 | fractions; abs numerator <=30, denominator 1..9','name':'one uppercase letter','incidental_parameters':['entries','name','field_layout','bank_profile'],'task_fingerprint':'ordered row and column counts only; not entry values, response layout, or difficulty label'}
R,C=sp.symbols('r c',integer=True,positive=True)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def validate_parameters(parameters):
 if set(parameters)!= {'entries','name'}:raise ValueError('Parameters must contain exactly entries and name')
 name=parameters['name'];entries=parameters['entries']
 if not isinstance(name,str) or not re.fullmatch('[A-Z]',name):raise ValueError('Invalid matrix name')
 if not isinstance(entries,list) or not 2<=len(entries)<=6:raise ValueError('Rows must be 2..6')
 if any(not isinstance(row,list) or not 2<=len(row)<=6 for row in entries) or len({len(row) for row in entries})!=1:raise ValueError('Matrix must be rectangular, 2..6 columns')
 canonical=[]
 for row in entries:
  vals=[]
  for cell in row:
   s=str(cell).strip()
   if not (re.fullmatch(r'-?\d{1,2}',s) and abs(int(s))<=30 or re.fullmatch(r'-?\\sqrt\{(?:[2-9]|1[0-3])\}',s) or re.fullmatch(r'-?\\frac\{(?:[1-9]|[12][0-9]|30)\}\{[1-9]\}',s)):raise ValueError('Unsupported/illegible entry')
   vals.append(str(int(s)) if re.fullmatch(r'-?\d+',s) else s)
  canonical.append(vals)
 return {'entries':canonical,'name':name}

def sample(rng):
 r,c=rng.choice(DIMENSIONS)
 pool=[str(v) for v in range(-9,10)]+[r'\sqrt{2}',r'-\sqrt{3}',r'\frac{1}{3}']
 return {'entries':[[rng.choice(pool) for _ in range(c)] for _ in range(r)],'name':rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}

def recipe_value(recipe,r,c):
 # Restricted symbolic recipes, never answer lookup tables or arbitrary fits.
 return tuple(int(sp.sympify(s,locals={'r':R,'c':C}).subs({R:r,C:c})) for s in recipe.split(','))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level)+'; only easy is validated')
 if field_type not in (None,'radio','blank'):raise ValueError('Unsupported field type')
 if template is not None and template not in TEMPLATES:raise ValueError('Unsupported template')
 if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unsupported profile')
 observed=profile in OBSERVED
 if observed:
  spec=OBSERVED[profile]
  if level!='easy':raise ValueError('Observed profiles are assigned easy only')
  if template is not None and template!=spec['template']:raise ValueError('Profile/template mismatch')
  template=spec['template']
 else:
  template=template or ('display-dual-blank' if field_type=='blank' or field_type is None and seed%2 else 'display-radio')
  if template not in ('display-radio','display-dual-blank'):raise ValueError('Observed template needs an explicit observed profile')
  spec=None
 kind=spec['field_type'] if spec else 'blank' if template.endswith('dual-blank') else 'radio'
 if field_type is not None and field_type!=kind:raise ValueError('Field/layout mismatch')
 if profile is not None and not observed and (kind!='radio' or BANK_PROFILES[profile]['template']!=template):raise ValueError('Profile/layout mismatch')
 rng=random.Random(seed)
 for attempt in range(100):
  p=validate_parameters(parameters if parameters is not None else sample(rng))
  r,c=len(p['entries']),len(p['entries'][0]);name=p['name']
  selected=profile if observed else profile or ('authored-square' if r==c else 'authored-rectangular') if kind=='radio' else None
  bank=BANK_PROFILES[selected]['bank'] if kind=='radio' else []
  values=[recipe_value(a['recipe'],r,c) for a in bank]
  valid=not values or len(set(values))==5 and values.count((r,c))==1 and all(1<=x<=8 and 1<=y<=8 for x,y in values)
  if selected=='authored-square' and r!=c or selected=='authored-rectangular' and r==c:valid=False
  if valid:break
  if parameters is not None:raise ValueError('Complete bank invalid at explicit dimensions')
 else:raise ValueError('No eligible complete bank in bounded sampling')
 array=r' \\ '.join(' & '.join(row) for row in p['entries'])
 if observed:
  prompt=spec['prompt_mask'].replace('@ARRAY@',array).replace('@NAME@',name)
  keys=spec['field_keys']
 else:
  matrix=r'\begin{bmatrix}'+array+r'\end{bmatrix}'
  prompt=f'What are the dimensions of the matrix ${name}$, where\n\n$$\n{name}={matrix}\n$$'
  keys=['selection'] if kind=='radio' else ['field-1','field-2']
  if kind=='blank':prompt+='\n\nThe dimensions are {{field-1}}$\\times ${{field-2}}.'
 solution_name='R' if observed and spec.get('solution_name')=='R' and name=='P' else name
 solution=f'The matrix ${solution_name}$ has ${r}$ rows and ${c}$ columns. Therefore, its dimensions are ${r}\\times {c}.$'
 displayed=[[str(x)+a['separator']+str(y) for a,(x,y) in zip(bank,values)]] if kind=='radio' else [[str(r if key=='field-1' else c)] for key in keys]
 content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'fields':[(key,kind,sorted(vals)) for key,vals in zip(keys,displayed)]})
 question_id=uid(content);fields=[]
 for key,vals in zip(keys,displayed):
  fieldid=uid(content+':field:'+key)
  answers=[{':answer/id':uid(fieldid+':answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
  idx=values.index((r,c)) if kind=='radio' else 0
  correct=answers[idx][':answer/id'];rng.shuffle(answers)
  fields.append({':answer-field/id':fieldid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':question_id,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':selected if kind=='radio' else profile,'bank_origin':'observed' if observed else 'authored','authored_extension':not observed,'difficulty_origin':'observed-easy-or-authored-unrated-easy' if observed else 'authored-easy-same-counting-demand','parameter_fingerprint':digest({'rows':r,'columns':c}),'content_fingerprint':content,'domain':DOMAIN,'source_analysis':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_ids':[spec['source']] if observed else ['e-4367'],'legacy_inferred_key':spec['missing_correct'] if observed else False,'solution_label_anomaly_preserved':observed and spec.get('solution_name')=='R' and name=='P'},'plot_rating':'none'}}

# EASY: observed count-first task; ordinary default variations span 25 shapes.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# Unsupported entrypoints reject instead of relabeling easy counting practice.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def batch(level,count,seed=0,template=None,field_type=None,profile=None):
 """Sample ordered shapes without replacement; incidental changes never pad count."""
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
 if not isinstance(count,int) or not 1<=count<=len(DIMENSIONS):raise ValueError('Finite limit: at most 25 distinct ordered dimension tasks')
 rng=random.Random(seed);shapes=list(DIMENSIONS);rng.shuffle(shapes);records=[]
 for i,(r,c) in enumerate(shapes):
  params={'name':rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ'),'entries':[[str(rng.randrange(-9,10)) for _ in range(c)] for _ in range(r)]}
  try:rec=generate(level,seed+i,template,field_type,params,profile)
  except ValueError as error:
   if 'Complete bank invalid' in str(error):continue
   raise
  records.append(rec)
  if len(records)==count:return records
 raise ValueError('Finite limit: requested profile supplies only '+str(len(records))+' distinct tasks')

def markdown(record):
 q=record['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'][1]
  lines += [f"Field {f[':answer-field/key']} ({f[':answer-field/type'].split('/')[-1]}):"]
  lines += [('- [x] ' if a[':answer/id']==correct else '- [ ] ')+ '$'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 lines+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=tuple(BANK_PROFILES));parser.add_argument('--field-type',choices=['radio','blank'])
 args=parser.parse_args()
 if args.count<1:parser.error('Count must be positive')
 try:records=[rec for level in (SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]) for rec in batch(level,args.count,args.seed,args.template,args.field_type,args.profile)]
 except ValueError as e:parser.error(str(e))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(rec) for rec in records))
if __name__=='__main__':main()
