#!/usr/bin/env python3
"""Private all-level review draft for counting the dimensions of a matrix.

Easy retains all eight original evidence profiles and source-shaped normal masks.
Moderate/hard are authored counting-workload bands, not recovered MA labels:
moderate extends exactly one axis to 7..12; hard extends both axes to 7..12.
They introduce no entry operations. There are exactly 25+60+36=121 distinct
ordered dimension tasks, not an unlimited
bank. Names, entries, fields and choice profiles do not increase that number.
The registered easy-only script and its evidence are never modified here.
"""
from pathlib import Path
import argparse,hashlib,json,random,re,sys,uuid
import sympy as sp
KP_ID=17592186087693
KP_UUID='f6ae25fc-16eb-598b-a288-742e4b46cb12'
TITLE='Determining the Dimensions of a Matrix'
VERSION='2.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
HERE=Path(__file__).resolve().with_suffix('')
OBSERVED=json.loads((HERE/'recipes.json').read_text())
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCE_RECORDS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
NORMAL_TEMPLATES=tuple(sorted({p['template'] for p in OBSERVED.values()}))
TEMPLATES=NORMAL_TEMPLATES+('display-radio','display-dual-blank')
BANK_PROFILES={**OBSERVED,
 'authored-rectangular':{'field_type':'radio','bank':[{'recipe':s,'separator':r'\times '} for s in ('r,c','c,r','r,r','c,c','r+1,c+1')]},
 'authored-square':{'field_type':'radio','bank':[{'recipe':s,'separator':r'\times '} for s in ('r,c','r-1,c-1','r+1,c+1','r,c+1','r+1,c')]}}
LEVEL_BOUNDS={'easy':(2,6),'moderate':(2,12),'hard':(7,12)}
DIMENSIONS={'easy':tuple((r,c) for r in range(2,7) for c in range(2,7)),
 'moderate':tuple((r,c) for r in range(2,13) for c in range(2,13) if (2<=r<=6 and 7<=c<=12) or (7<=r<=12 and 2<=c<=6)),
 'hard':tuple((r,c) for r in range(7,13) for c in range(7,13))}
DOMAIN={'level_bounds':LEVEL_BOUNDS,'meaningful_dimension_pairs':{k:len(v) for k,v in DIMENSIONS.items()},'meaningful_union':121,'entries':'easy: bounded source-compatible integers, radicals, fractions; moderate/hard: single-digit integers only','name':'one uppercase letter','incidental_parameters':['entries','name','field_layout','bank_profile','difficulty_alias'],'task_fingerprint':'ordered row and column counts only; dimensions are NOT a commutative product','difficulty_claim':'Authored extended enumeration: easy zero, moderate exactly one, hard two axes longer than six. No empirical MA moderate/hard labels.'}
R,C=sp.symbols('r c',integer=True,positive=True)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))

def validate_parameters(parameters,level):
 """Explicit and sampled inputs use identical workload and legibility guards."""
 if not isinstance(parameters,dict) or set(parameters)!= {'entries','name'}:raise ValueError('Parameters must contain exactly entries and name')
 name=parameters['name'];entries=parameters['entries'];lo,hi=LEVEL_BOUNDS[level]
 if not isinstance(name,str) or not re.fullmatch('[A-Z]',name):raise ValueError('Invalid matrix name')
 if not isinstance(entries,list) or not lo<=len(entries)<=hi:raise ValueError(f'{level} requires {lo}..{hi} rows')
 if any(not isinstance(row,list) or not lo<=len(row)<=hi for row in entries) or len({len(row) for row in entries})!=1:raise ValueError(f'{level} requires a rectangular matrix with {lo}..{hi} columns')
 if (len(entries),len(entries[0])) not in DIMENSIONS[level]:raise ValueError('Shape does not meet '+level+' extended-axis workload')
 canonical=[]
 for row in entries:
  vals=[]
  for cell in row:
   if isinstance(cell,bool) or not isinstance(cell,(str,int)):raise ValueError('Cell must be a supported scalar string or integer')
   s=str(cell).strip()
   integer=bool(re.fullmatch(r'-?\d{1,2}',s)) and abs(int(s))<=(30 if level=='easy' else 9)
   special=level=='easy' and (re.fullmatch(r'-?\\sqrt\{(?:[2-9]|1[0-3])\}',s) or re.fullmatch(r'-?\\frac\{(?:[1-9]|[12][0-9]|30)\}\{[1-9]\}',s))
   if not (integer or special):raise ValueError('Unsupported/illegible entry for '+level)
   vals.append(str(int(s)) if integer else s)
  canonical.append(vals)
 return {'entries':canonical,'name':name}

def recipe_value(recipe,r,c):
 return tuple(int(sp.sympify(s,locals={'r':R,'c':C}).subs({R:r,C:c})) for s in recipe.split(','))

def eligible_bank(profile,r,c):
 if profile is None:return True
 values=[recipe_value(a['recipe'],r,c) for a in BANK_PROFILES[profile]['bank']]
 if profile=='authored-square' and r!=c or profile=='authored-rectangular' and r==c:return False
 return not values or len(values)==5 and len(set(values))==5 and values.count((r,c))==1 and all(1<=x<=14 and 1<=y<=14 for x,y in values)

def sample(rng,level,profile):
 shapes=[(r,c) for r,c in DIMENSIONS[level] if eligible_bank(profile,r,c)]
 if not shapes:raise ValueError('Selected complete bank has no eligible shape')
 r,c=rng.choice(shapes)
 pool=[str(v) for v in range(-9,10)]
 if level=='easy':pool += [r'\sqrt{2}',r'-\sqrt{3}',r'\frac{1}{3}']
 return {'entries':[[rng.choice(pool) for _ in range(c)] for _ in range(r)],'name':rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}

def choose_spec(rng,level,template,field_type,profile):
 observed=profile in OBSERVED
 if observed:
  if level!='easy':raise ValueError('Observed profiles belong to easy/unrated evidence only')
  spec=OBSERVED[profile]
  if template is not None and template!=spec['template']:raise ValueError('Profile/template mismatch')
  template=spec['template'];kind=spec['field_type']
 else:
  candidates=NORMAL_TEMPLATES if level=='easy' else ('display-radio','display-dual-blank')
  if template is None:
   if field_type is not None:candidates=tuple(t for t in candidates if ('blank' if t.endswith('dual-blank') else 'radio')==field_type)
   if profile is not None:candidates=tuple(t for t in candidates if not t.endswith('dual-blank'))
   template=rng.choice(candidates)
  if level!='easy' and template not in ('display-radio','display-dual-blank'):raise ValueError('Larger authored matrices require the legible display layout')
  kind='blank' if template.endswith('dual-blank') else 'radio'
  spec=next((x for x in OBSERVED.values() if x['template']==template),None)
 if field_type is not None and field_type!=kind:raise ValueError('Field/layout mismatch')
 if profile is not None and not observed and kind!='radio':raise ValueError('Profile/layout mismatch')
 # Complete bank is chosen before random matrix dimensions/entries, never pooled.
 selected=profile if observed or profile is not None else rng.choice(('authored-square','authored-rectangular')) if kind=='radio' else None
 if level=='moderate' and kind=='radio' and profile is None:selected='authored-rectangular'
 return observed,template,spec,kind,selected

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
 if field_type not in (None,'radio','blank'):raise ValueError('Unsupported field type')
 if template is not None and template not in TEMPLATES:raise ValueError('Unsupported template')
 if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unsupported profile')
 rng=random.Random(seed)
 # For fixed explicit parameters the default profile is deterministic, independent
 # of seed; choose its full bank before validating/evaluating those parameters.
 selection_rng=random.Random(int(digest({'level':level,'template':template,'field_type':field_type,'parameters':parameters,'profile':profile}),16)) if parameters is not None else rng
 observed,template,spec,kind,selected=choose_spec(selection_rng,level,template,field_type,profile)
 # Explicit square/rectangular defaults choose their applicable whole bank; the
 # externally supplied dimensions are an eligibility filter, not sampled params.
 if parameters is not None and profile is None and kind=='radio':
  entries=parameters.get('entries',[]) if isinstance(parameters,dict) else []
  selected='authored-square' if isinstance(entries,list) and entries and isinstance(entries[0],list) and len(entries)==len(entries[0]) else 'authored-rectangular'
 p=validate_parameters(parameters if parameters is not None else sample(rng,level,selected),level)
 r,c=len(p['entries']),len(p['entries'][0]);name=p['name']
 if not eligible_bank(selected,r,c):raise ValueError('Complete bank invalid at explicit dimensions')
 bank=BANK_PROFILES[selected]['bank'] if kind=='radio' else []
 values=[recipe_value(a['recipe'],r,c) for a in bank]
 array=r' \\ '.join(' & '.join(row) for row in p['entries'])
 if spec:
  prompt=spec['prompt_mask'].replace('@ARRAY@',array).replace('@NAME@',name);keys=spec['field_keys']
 else:
  prompt=f'What are the dimensions of the matrix ${name}$, where\n\n$$\n{name}='+r'\begin{bmatrix}'+array+r'\end{bmatrix}'+'\n$$';keys=['selection'] if kind=='radio' else ['field-1','field-2']
  if kind=='blank':prompt+='\n\nThe dimensions are {{field-1}}$\\times ${{field-2}}.'
 solution_name='R' if observed and spec.get('solution_name')=='R' and name=='P' else name
 solution=f'The matrix ${solution_name}$ has ${r}$ rows and ${c}$ columns. Therefore, its dimensions are ${r}\\times {c}.$'
 displayed=[[str(x)+a['separator']+str(y) for a,(x,y) in zip(bank,values)]] if kind=='radio' else [[str(r if key=='field-1' else c)] for key in keys]
 raw_source=SOURCE_RECORDS[spec['source']] if observed else None
 # Raw replay preserves absent source attributes. Completed normal fields and
 # labels are authored; the missing legacy designation never becomes "matched".
 has_solution=not observed or ':question/worked-solution' in raw_source
 has_difficulty=not observed or ':question/difficulty' in raw_source
 correct_presence=[not observed or ':answer-field/correct' in f for f in raw_source[':question/answer-fields']] if observed else [True]*len(keys)
 content=digest({'version':VERSION,'difficulty':level if has_difficulty else None,'prompt':prompt,'solution':solution if has_solution else None,'fields':[(key,kind,sorted(vals),present) for key,vals,present in zip(keys,displayed,correct_presence)]})
 fields=[]
 for key,vals,present in zip(keys,displayed,correct_presence):
  fieldid=uid(content+':field:'+key)
  answers=[{':answer/id':uid(fieldid+':answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
  idx=values.index((r,c)) if kind=='radio' else 0;correct=answers[idx][':answer/id'];rng.shuffle(answers)
  field={':answer-field/id':fieldid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
  if present:field[':answer-field/correct']=[':answer/id',correct]
  fields.append(field)
 q={':question/id':uid(content),':question/problem':prompt,':question/answer-fields':fields}
 if has_difficulty:q[':question/difficulty']=':question.difficulty/'+level
 if has_solution:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'level':level,'template':template,'parameters':p,'bank_profile':selected,'bank_origin':'observed-expression-pattern' if observed else 'authored-counting-operations','authored_extension':not observed,'evidence_only':observed,'eligible_for_learning':not observed,'difficulty_origin':'source-easy-or-raw-unrated' if observed else 'authored-counting-workload-band','parameter_fingerprint':digest({'rows':r,'columns':c}),'content_fingerprint':content,'domain':DOMAIN,'workload':{'operation':'count horizontal rows; count vertical columns; report in order','independent_counts':2,'rows_counted':r,'columns_counted':c,'axis_count_band':LEVEL_BOUNDS[level],'extended_axis_counts':int(r>6)+int(c>6)},'source_analysis':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_ids':[spec['source']] if observed else ['e-4367'],'missing_correct_preserved':spec['missing_correct'] if observed else False,'solution_label_anomaly_preserved':observed and spec.get('solution_name')=='R' and name=='P'},'plot_rating':'none','draft_only':True}}

# EASY: observed 2..6 by 2..6 arrays. Entry number forms are not extra workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE (authored): exactly one unlabelled axis requires 7..12 counts,
# the other 2..6. Row/column orientations are peers with one extended count.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored): both unlabelled axes require 7..12 sequential counts.
# Single-digit entries and display math retain legibility; no new matrix method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def batch(level,count,seed=0,template=None,field_type=None,profile=None):
 """Finite ordered-shape sampling without replacement; never pad using entries."""
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
 if not isinstance(count,int) or not 1<=count<=len(DIMENSIONS[level]):raise ValueError('Finite '+level+' limit: '+str(len(DIMENSIONS[level]))+' distinct ordered dimension tasks')
 rng=random.Random(seed);shapes=list(DIMENSIONS[level]);rng.shuffle(shapes);records=[]
 for i,(r,c) in enumerate(shapes):
  params={'name':rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ'),'entries':[[str(rng.randrange(-9,10)) for _ in range(c)] for _ in range(r)]}
  try:rec=generate(level,seed+i,template,field_type,params,profile)
  except ValueError as error:
   if 'Complete bank invalid' in str(error):continue
   raise
  records.append(rec)
  if len(records)==count:return records
 raise ValueError('Finite limit: selected profile supplies only '+str(len(records))+' distinct tasks')

def markdown(record):
 q=record['question'];gen=record['generation'];label='ORIGINAL SOURCE EVIDENCE / parameterized replay' if gen['evidence_only'] else 'GENERATED';lines=['### '+label+' — '+q.get(':question/difficulty','unrated (raw capture)')+'; '+gen['difficulty_origin'],q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  lines += [f"Field {f[':answer-field/key']} ({f[':answer-field/type'].split('/')[-1]}):"]
  lines += [('- [x] ' if a[':answer/id']==correct else '- [ ] ')+ '$'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 if ':question/worked-solution' in q:lines+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=tuple(BANK_PROFILES));parser.add_argument('--field-type',choices=['radio','blank'])
 args=parser.parse_args()
 try:records=[rec for level in (SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]) for rec in batch(level,args.count,args.seed,args.template,args.field_type,args.profile)]
 except ValueError as e:parser.error(str(e))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(rec) for rec in records))
if __name__=='__main__':main()
