#!/usr/bin/env python3
"""Finding a rectangular matrix entry, frozen math basis 1356.

Public raw:q-* profiles reproduce every source through the same matrix/index
recipes, preserving absent ratings, correct refs and solutions. They are evidence
only. completed:q-* authors the missing references/prose for the two unrated
sources. Default banks are complete indexing-error operations, not translations
of opaque historical scalar banks. Easy preserves source layouts and workload;
moderate/hard author longer visual scans without arithmetic or new procedures.
See the adjacent classification, extraction, validation and review evidence.
No database clients, plots, transactions or engine modifications.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186100988
KP_UUID='8d783281-8364-5597-a804-a4ea0d76bec8'
TITLE='Finding an Entry of a Matrix'
VERSION='rectangular-entry-lookup-v6'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
TEMPLATES=('inline_no_entry_radio','inline_radio','display_radio','display_should_radio','display_noperiod_radio','display_blank')
STYLE={'q-13488':'inline_radio','q-13496':'inline_radio','q-279260':'display_radio','q-279539':'display_blank','q-279540':'display_blank','q-13497':'display_should_radio','q-125561':'display_noperiod_radio'}
# Complete observed banks, each slot maps a displayed scalar to a real cell,
# target, missing-entry text, or explicitly opaque external value. Cell origins
# are hypotheses when values repeat; no recovered author intent is claimed.
OBSERVED={
 'q-13488':[('cell',2,1),('external','zero'),('cell',2,3),('missing',),('target',)],
 'q-13496':[('cell',2,4),('cell',3,3),('cell',2,1),('cell',3,4),('missing',)],
 'q-279260':[('cell',1,1),('external','two'),('target',),('cell',2,1),('cell',2,3)],
 'q-279539':[('target',)],'q-279540':[('target',)],
 'q-13497':[('missing',),('cell',2,3),('cell',1,4),('cell',2,1),('target',)],
 'q-125561':[('cell',1,1),('target',),('cell',3,2),('cell',2,1),('cell',2,2)]}
VALID_RADIO_PROFILES=('location_no_entry','four_locations','swap_no_entry')
DEFAULT_PROFILES=VALID_RADIO_PROFILES+('overflow_locations','blank')
EASY_DIMENSIONS=((2,3),(2,4),(3,2),(3,4),(5,4))
def level_templates(level):return TEMPLATES if level=='easy' else TEMPLATES[1:]
def level_profiles(level):return DEFAULT_PROFILES if level=='easy' else VALID_RADIO_PROFILES+('blank',)

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(key):return str(uuid.uuid5(uuid.UUID(KP_UUID),key))
def ordinal(n):return str(n)+('th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th'))
def parse_matrix(text):
 match=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S)
 if not match:raise ValueError('Matrix not found')
 return [[int(c.strip()) for c in row.split('&')] for row in match[1].split(r'\\')]
def parse_index(text):
 m=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',text)
 if not m:raise ValueError('Index not found')
 return m[1],int(m[2]),int(m[3])
def source_parameters(source):
 q=SOURCES[source];letter,i,j=parse_index(q[':question/problem'])
 return {'matrix':parse_matrix(q[':question/problem']),'i':i,'j':j,'letter':letter.upper(),'external':{'zero':0,'two':2}}
def matrix_body(a):return r' \\ '.join(' & '.join(str(x) for x in row) for row in a)
def matrix_display(p,style,solution=False):
 body=matrix_body(p['matrix']);letter=p['letter']
 if style=='inline_radio':return letter+' = '+r'\begin{bmatrix}'+body+r'\end{bmatrix}'
 tail='' if solution and style in ('display_should_radio','display_noperiod_radio') else '.'
 return letter+'=['+r'\begin{aligned}'+body+r'\end{aligned}]'+tail

def target(p):
 a=p['matrix'];i,j=p['i'],p['j']
 return a[i-1][j-1] if i<=len(a) and j<=len(a[0]) else None

def observed_bank(p,source):
 out=[]
 for recipe in OBSERVED[source]:
  if recipe[0]=='cell':v=p['matrix'][recipe[1]-1][recipe[2]-1]
  elif recipe[0]=='target':v=target(p)
  elif recipe[0]=='external':v=p['external'][recipe[1]]
  else:v=None
  out.append((':answer.type/text','No such entry') if v is None else (':answer.type/math',str(v)))
 return out

def default_positions(p,profile):
 m,n=len(p['matrix']),len(p['matrix'][0]);i,j=p['i'],p['j']
 if profile=='overflow_locations':
  if i==m+1 and 1<=j<=n:
   col=j+1 if j<n else j-1
   return [None,(m,j),(1,j),(m,col),(1,col)]
  if j==n+1 and 1<=i<=m:
   row=i+1 if i<m else i-1
   return [None,(i,n),(i,1),(row,n),(row,1)]
  raise ValueError('Exactly one row or column index must overflow by one')
 if target(p) is None:raise ValueError('Numeric profiles require an existing entry')
 nxtrow=i+1 if i<m else i-1;nxtcol=j+1 if j<n else j-1
 positions=[(i,j)]
 if profile=='blank':return positions
 if profile=='location_no_entry':return positions+[(nxtrow,j),(i,nxtcol),(nxtrow,nxtcol),None]
 if profile=='four_locations':
  if n>=3:
   othercol=j-1 if j>1 and j-1!=nxtcol else j+2 if j+2<=n else j-2
   extra=(i,othercol)
  else:
   otherrow=i-1 if i>1 and i-1!=nxtrow else i+2 if i+2<=m else i-2
   extra=(otherrow,j)
  return positions+[(nxtrow,j),(i,nxtcol),(nxtrow,nxtcol),extra]
 if profile=='swap_no_entry':
  if i==j or j>m or i>n:raise ValueError('Swapped indices must exist and differ')
  return positions+[(j,i),(nxtrow,j),(i,nxtcol),None]
 raise ValueError('Unknown default profile')
def default_bank(p,profile):
 positions=default_positions(p,profile)
 if len(set(positions))!=len(positions):raise ValueError('Complete error profile has repeated locations')
 return [(':answer.type/text','No such entry') if loc is None else (':answer.type/math',str(p['matrix'][loc[0]-1][loc[1]-1])) for loc in positions]

def render(p,style,include_solution=True):
 i,j=p['i'],p['j'];letter=p['letter'];sub=letter.lower()
 entry=(sub if style=='inline_radio' else '{'+sub+'}')+'_{'+str(i)+str(j)+'}'
 if style=='inline_radio':prompt=render_inline(p)
 else:prompt='Find the entry $'+entry+'$ of the matrix $'+letter+'$, where \n\n$$\n'+matrix_display(p,style)+'\n$$'
 if style=='display_blank':prompt+='\n\n$'+entry+'=$\n{{field-1}}'
 solution=None
 if include_solution:
  correct=target(p)
  opening='The entry $'+entry+'$ '+('should lie' if style=='display_should_radio' or correct is None else 'lies')+' at the intersection of the $'+str(i)+'$'+ordinal(i)[len(str(i)):]+' row and $'+str(j)+'$'+ordinal(j)[len(str(j)):]+' column.'
  if correct is None:
   m,n=len(p['matrix']),len(p['matrix'][0])
   solution=opening+' The matrix has $'+str(m)+'$ rows and $'+str(n)+'$ columns, so there is no such entry.'
  else:solution=opening+' Therefore, $'+entry+'='+str(correct)+'.$'
  if style=='inline_radio':solution+='\n\n$'+matrix_display(p,style)+'.$'
  else:solution+='\n\n$$\n'+matrix_display(p,style,True)+'\n$$'
 return prompt,solution

# Shared exact source masks: the inline source period belongs outside its $...$.
# Keeping this separate makes punctuation fidelity explicit, not anchor-only.
def render_inline(p):
 entry=p['letter'].lower()+'_{'+str(p['i'])+str(p['j'])+'}'
 return 'Find the entry $'+entry+'$ of the matrix $'+p['letter']+'$, where\n$'+matrix_display(p,'inline_radio')+'$.'

def guard(p,level,observed_source=None,allow_overflow=False):
 if set(p)-{'matrix','i','j','letter','external'} or not {'matrix','i','j','letter'}<=set(p):raise ValueError('Invalid parameter keys')
 a=p['matrix'];i,j=p['i'],p['j']
 if not isinstance(a,list) or len(a)<2 or not all(isinstance(row,list) for row in a):raise ValueError('Invalid matrix')
 m,n=len(a),len(a[0])
 if n<2 or m==n or any(len(row)!=n for row in a):raise ValueError('Rectangular nonsquare matrix required')
 if any(type(v)is not int or not -9<=v<=9 for row in a for v in row):raise ValueError('Signed one-digit integer entries required')
 if type(i)is not int or type(j)is not int or not 1<=i<=9 or not 1<=j<=9:raise ValueError('Single-digit positive indices required')
 if not isinstance(p['letter'],str) or not re.fullmatch('[A-Z]',p['letter']):raise ValueError('One uppercase matrix label required')
 external=p.get('external',{})
 if set(external)-{'zero','two'} or any(type(v)is not int or not -9<=v<=9 for v in external.values()):raise ValueError('Invalid external scalars')
 if observed_source:
  original=source_parameters(observed_source)
  if (m,n)!=(len(original['matrix']),len(original['matrix'][0])):raise ValueError('Observed profile dimensions fixed')
  if set(external)!={'zero','two'}:raise ValueError('Observed replay requires external scalar parameters')
 else:
  if allow_overflow:
   if level!='easy' or not ((i==m+1 and j<=n) or (j==n+1 and i<=m)):raise ValueError('Only easy one-index overflow by one is supported')
  elif i>m or j>n:raise ValueError('Numeric defaults require existing entries')
  if level=='easy' and ((m,n) not in EASY_DIMENSIONS):raise ValueError('Easy dimension bound')
  if level=='moderate' and ((m,n) not in ((5,6),(6,5)) or max(i,j)<4):raise ValueError('Moderate scanning bound')
  if level=='hard' and ((m,n) not in ((6,7),(7,6)) or max(i,j)<5):raise ValueError('Hard scanning bound')
 return p

def sample(level,rng,profile):
 dimensions={'easy':EASY_DIMENSIONS,'moderate':((5,6),(6,5)),'hard':((6,7),(7,6))}
 for _ in range(10000):
  m,n=rng.choice(dimensions[level]);i,j=rng.randint(1,m),rng.randint(1,n)
  if profile=='overflow_locations':
   if rng.choice((True,False)):i=m+1
   else:j=n+1
  p={'matrix':[[rng.randint(-9,9) for _ in range(n)] for _ in range(m)],'i':i,'j':j,'letter':rng.choice('ACEFY')}
  try:guard(p,level,allow_overflow=profile=='overflow_locations');bank=default_bank(p,profile)
  except ValueError:continue
  if len(set(bank))==len(bank):return p
 raise ValueError('No eligible whole instance found')

# EASY: observed direct lookup, original forms; completed unrated raw profiles
# remain explicit evidence. Normal default profiles use indexing-location errors.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): 30-cell rectangular scan, index at least 4 in one direction.
# Same two subscripts and exactly one entry read; no algebra or matrix operation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): 42-cell scan, index at least 5 in one direction; no extra method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);source=None;raw=False;completion=False
 if profile and (profile.startswith('raw:') or profile.startswith('completed:')):
  mode,source=profile.split(':',1)
  if source not in SOURCES:raise ValueError('Unknown source profile')
  raw=mode=='raw';completion=mode=='completed';old=SOURCES[source]
  observed_level=old.get(':question/difficulty',{}).get(':db/ident')
  if level!='easy':raise ValueError('Observed or completed source profiles use easy workload')
  style=STYLE[source]
  if template is not None and template!=style:raise ValueError('Template/profile mismatch')
  p=source_parameters(source) if parameters is None else json.loads(json.dumps(parameters))
  guard(p,level,source)
  kind=old[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
  bank=observed_bank(p,source)
  prompt,solution=render(p,style,':question/worked-solution' in old or completion)
  if style=='inline_radio':prompt=render_inline(p)
 else:
  if profile is not None and profile not in level_profiles(level):raise ValueError('Bank profile not supported at this level')
  allowed=[s for s in level_templates(level) if field_type is None or s.endswith('_'+field_type.removeprefix(':answer-field.type/'))]
  if profile is not None:
   allowed=[s for s in allowed if (s=='display_blank')==(profile=='blank')]
  if not allowed:raise ValueError('Unsupported field/profile combination')
  style=template or rng.choice(allowed)
  if style not in allowed:raise ValueError('Unsupported template/field combination')
  kind='blank' if style.endswith('_blank') else 'radio'
  bank_profile=profile or ('blank' if kind=='blank' else rng.choice([p for p in level_profiles(level) if p!='blank']))
  if (bank_profile=='blank')!=(kind=='blank'):raise ValueError('Field/profile mismatch')
  profile=bank_profile
  p=sample(level,rng,profile) if parameters is None else json.loads(json.dumps(parameters))
  guard(p,level,allow_overflow=profile=='overflow_locations');bank=default_bank(p,profile)
  prompt,solution=render(p,'inline_radio' if style=='inline_no_entry_radio' else style)
  if style=='inline_radio':prompt=render_inline(p)
 if field_type and field_type not in (kind,':answer-field.type/'+kind):raise ValueError('Unsupported field type')
 if len(set(bank))!=len(bank):raise ValueError('Whole bank has equivalent duplicate options')
 correct_value=(':answer.type/text','No such entry') if target(p) is None else (':answer.type/math',str(target(p)))
 if bank.count(correct_value)!=1:raise ValueError('Whole bank must contain exactly one valid answer')
 # Keep raw capture replay intact; learner matrices need centered columns and
 # automatically sized brackets, rather than equation-pair alignment.
 if not raw:
  prompt=prompt.replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
  if solution is not None:solution=solution.replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
 question={':question/problem':prompt}
 if solution is not None:question[':question/worked-solution']=solution
 if not raw or ':question/difficulty' in old:question[':question/difficulty']=(':question.difficulty/'+level if not raw else observed_level)
 key='field-1' if kind=='blank' else 'selection'
 correct_present=not raw or ':answer-field/correct' in old[':question/answer-fields'][0]
 # Display identity includes all content and actual attribute presence; profile
 # names, incidental external parameters and option order are not identity input.
 content={'version':VERSION,'question':question,'field_type':kind,'key':key,'bank':sorted(bank),'correct_present':correct_present,'correct':correct_value if correct_present else None}
 identity=digest(content);qid=uid('question:'+identity);fid=uid(qid+':field:'+key)
 answers=[{':answer/id':uid(fid+':answer:'+digest([ty,val])),':answer/type':ty,':answer/value':val} for ty,val in bank]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if correct_present:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if (a[':answer/type'],a[':answer/value'])==correct_value)]
 if kind=='radio':rng.shuffle(answers)
 question[':question/id']=qid;question[':question/answer-fields']=[field]
 m,n=len(p['matrix']),len(p['matrix'][0])
 task=[m,n,p['i'],p['j'],target(p)]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':style,'profile':profile,'parameters':p,'source':source,'source_provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'origin':'observed-parameterized' if raw else 'authored-completion' if completion else 'authored-default','evidence_only':bool(raw or completion),'eligible_for_learning':not raw and not completion,'content_identity':identity,'mathematical_fingerprint':digest(task),'task_components':task,'difficulty_claim':'observed' if raw and observed_level else 'unrated raw' if raw else 'authored visual-reading workload','bank_recipes':OBSERVED[source] if source else {'location_no_entry':'target,neighbor row,neighbor column,diagonal neighbor,missing','four_locations':'target,neighbor row,neighbor column,diagonal neighbor,other nearby column or row','swap_no_entry':'target,swapped indices,neighbor row,neighbor column,missing','overflow_locations':'missing,clamp overflow index,restart overflow index at1,clamp plus adjacent other index,restart plus adjacent other index','blank':'target'}[profile],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0];ref=f.get(':answer-field/correct',['',None])[1]
 options='\n'.join('- '+a[':answer/value']+(' (correct)' if a[':answer/id']==ref else '') for a in f[':answer-field/choices'])
 return q[':question/problem']+'\n\n'+options+'\n\n'+q.get(':question/worked-solution','[Source worked solution absent.]')

def generate_batch(level,seed,count,template=None,field_type=None,profile=None):
 """Keep existence contrasts together within each represented radio layout.

 Explicit bank requests and one-item requests retain the single-item API.
 Unpaired slots use banks that do not offer an absence decision.
 """
 if count<1:raise ValueError('count must be positive')
 if level!='easy' or count==1 or profile is not None or field_type=='blank' or template=='display_blank':
  return [generate(level,seed+k,template,field_type,profile=profile) for k in range(count)]
 rng=random.Random(seed);records=[]
 styles=[s for s in level_templates(level) if s!='display_blank']
 if template is not None:
  if template not in styles:raise ValueError('Unsupported template')
  styles=[template]
 while len(records)<count:
  left=count-len(records)
  pair=left>=2 and (not records or rng.choice((True,False)))
  if pair:
   style=rng.choice(styles)
   for bank in (rng.choice(('location_no_entry','swap_no_entry')),'overflow_locations'):
    records.append(generate(level,rng.getrandbits(64),template=style,field_type='radio',profile=bank))
  else:
   bank='four_locations' if template is not None or field_type=='radio' else rng.choice(('blank','four_locations'))
   records.append(generate(level,rng.getrandbits(64),template=template,field_type=field_type,profile=bank))
 rng.shuffle(records)
 for index,record in enumerate(records):
  record['generation']['batch']={'seed':seed,'count':count,'index':index,'rule':'layout-existence-contrasts'}
 return records

def main():
 cli=argparse.ArgumentParser();cli.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=2);cli.add_argument('--format',choices=('markdown','json'),default='markdown');cli.add_argument('--template');cli.add_argument('--profile');cli.add_argument('--field-type',choices=('radio','blank'))
 args=cli.parse_args()
 if args.count<1:cli.error('count must be positive')
 records=[r for level in LEVELS if args.difficulty in ('all',level) for r in generate_batch(level,args.seed,args.count,args.template,args.field_type,args.profile)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
