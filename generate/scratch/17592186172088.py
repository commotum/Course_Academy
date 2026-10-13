#!/usr/bin/env python3
"""Identify constant three-dimensional vector fields from qualitative diagrams.

Basis 1356, math, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Observed: seven moderate and three hard, ten complete banks. Easy is authored:
recognize axis and sign among constant fields. Moderate additionally rejects a
variable component; hard verifies that all four formulas fail (None). Positive
common scale changes presentation, not the mathematical task. No calculus,
trajectories, multicomponent target fields, or added nonlinear target families.

Observed formula bodies are parsed into coefficient/function/basis components;
coordinate permutations, uniform sign and common scale transform these recipes.
The full extracted worked prose uses whole-equation slots, not string replacement
of short expressions. Exact source parameters pass the same normal constructor.
Source profiles have the original domain limitations (the log option is defined
only where its argument is positive); it still cannot describe a constant field
on the displayed full region. Original PNGs are reused only for the exact same
signed constant field; other geometry is rendered with private Matplotlib.

The finite task catalog has six possible axis/sign targets. Profile/bank and
coefficient aliases do not inflate this count. Different banks have different
content identities. The positive scale and the source magnitudes remain in the
presentation identity. UUIDs are owned by question/field and stable under seed
or option shuffling. Local JSON only; no database operations.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,os,uuid,platform
from pathlib import Path
import sympy as sp
KP_ID=17592186172088
KP_UUID='888aa30d-7179-507c-a30c-38209587333b'
TITLE='Identifying a Three-Dimensional Vector Field'
VERSION='3d-field-v1'
HERE=Path(__file__).resolve().parent/str(KP_ID)
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
COORDS='xyz';BASES='ijk';X,Y,Z=sp.symbols('x y z',real=True)
SYMS=dict(zip(COORDS,(X,Y,Z)))
PROFILES={
 'q-122559':('moderate','x',1,1), 'q-122664':('moderate','z',1,2),
 'q-122651':('moderate','x',1,2), 'q-122668':('moderate','y',-1,1),
 'q-122670':('hard','z',-1,1), 'q-123748':('moderate','x',-1,2),
 'q-123749':('hard','y',-1,1), 'q-123750':('hard','x',1,1),
 'q-122662':('moderate','y',1,3), 'q-122667':('moderate','x',-1,1),
 'authored-easy':('easy','x',1,1)}
PROMPT='Which of the following could be the function that generates the vector field above?'
TEMPLATES={'easy':'constant_sign','moderate':'constant_match','hard':'constant_none'}

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))

def parse_terms(value):
 """Parse the complete source formula into exact signed scalar/basis recipes."""
 if value=='None of the listed':return None
 name,rhs=value.split('=',1);terms=[]
 for m in re.finditer(r'([+-]?)([^+-]*?)([ijk])(?=[+-]|$)',rhs):
  sign=-1 if m[1]=='-' else 1;body=m[2]
  clean=body.replace(r'\,','')
  n=re.match(r'^(\d+)(.*)$',clean)
  coefficient=sign*int(n[1]) if n else sign
  func=n[2] if n else clean
  style='spaced-unit' if body==r'\,' else 'regular'
  terms.append({'coefficient':coefficient,'function':func,'basis':m[3],'style':style})
 if not terms or ''.join(m[0] for m in re.finditer(r'([+-]?)([^+-]*?)([ijk])(?=[+-]|$)',rhs))!=rhs:raise ValueError('Unparsed RHS '+rhs)
 return {'name':name,'terms':terms}

RECIPES={p:[parse_terms(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']] for p,q in QUESTIONS.items()}

def scalar(function):
 if not function:return sp.Integer(1)
 if function in SYMS:return SYMS[function]
 m=re.fullmatch(r'\{([xyz])\}\^\{2\}',function)
 if m:return SYMS[m[1]]**2
 m=re.fullmatch(r'\{e\}\^\{([xyz])\}',function)
 if m:return sp.exp(SYMS[m[1]])
 m=re.fullmatch(r'\\operatorname\{(ln|sin)\}⁡([xyz])',function)
 if m:return (sp.log if m[1]=='ln' else sp.sin)(SYMS[m[2]])
 raise ValueError('Unsupported scalar '+function)

def transform(recipe,p):
 if recipe is None:return 'None of the listed',None
 perm=dict(zip(COORDS,p['permutation']));bmap=dict(zip(BASES,(BASES[COORDS.index(perm[c])] for c in COORDS)))
 rhs='';components=[sp.Integer(0)]*3
 for term in recipe['terms']:
  c=term['coefficient']*p['flip']*p['scale'];fn=re.sub('[xyz]',lambda m:perm[m[0]],term['function']);b=bmap[term['basis']]
  components[BASES.index(b)]+=c*scalar(fn)
  sign='-' if c<0 else ('+' if rhs else '');a=abs(c)
  coefficient='' if a==1 else str(a)+r'\,'
  gap=r'\,' if fn or term['style']=='spaced-unit' and a==1 else ''
  rhs+=sign+coefficient+fn+gap+b
 return recipe['name']+'='+rhs,components

def extracted_solution(profile):
 """All source math equations are complete slots; surrounding prose stays fixed."""
 q=QUESTIONS[profile];solution=q[':question/worked-solution']
 values=[c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices']]
 # Longest first avoids a complete short equation prefix consuming a longer one.
 slots={v:'@@equation'+str(n)+'@@' for n,v in enumerate(values) if v!='None of the listed'}
 for v in sorted(slots,key=len,reverse=True):solution=solution.replace(v,slots[v])
 return solution,slots

SOLUTION_TEMPLATES={p:extracted_solution(p) for p in QUESTIONS}

def render_solution(profile,p,values):
 if profile=='authored-easy':
  axis=p['permutation'][0];basis=BASES[COORDS.index(axis)];others=[b for b in BASES if b!=basis];sign='positive' if p['flip']>0 else 'negative'
  return ('We notice the following:\n\n- Each vector in our vector field is parallel to the $'+axis+'$-axis. So, the $'+others[0]+'$ and $'+others[1]+'$ components of our vector field are zero everywhere. Therefore, we can rule out the following options:\n\n$$\n'+values[2]+r',\,'+values[3]+'\n$$\n\n- Moreover, each vector in our vector field is pointing in the *'+sign+'* $'+axis+'$-direction, so the $'+basis+'$ component of our vector field is '+sign+'. Therefore, we can rule out the following option:\n\n$$\n'+values[1]+'\n$$\n\nTherefore, we conclude that the diagram corresponds to the vector field $'+values[0]+'.$')
 solution,slots=SOLUTION_TEMPLATES[profile];perm=dict(zip(COORDS,p['permutation']));bmap=dict(zip(BASES,(BASES[COORDS.index(perm[c])] for c in COORDS)))
 solution=re.sub(r'\$([xyz])\$',lambda m:'$'+perm[m[1]]+'$',solution)
 solution=re.sub(r'\$([ijk])\$',lambda m:'$'+bmap[m[1]]+'$',solution)
 if p['flip']==-1:
  solution=solution.replace('positive','@@positive@@').replace('negative','positive').replace('@@positive@@','negative')
 original=[c[':answer/value'] for c in QUESTIONS[profile][':question/answer-fields'][0][':answer-field/choices']]
 for i,v in enumerate(original):
  if v in slots:solution=solution.replace(slots[v],values[i])
 return solution

def render_plots(components,profile,p,output_dir=None):
 """Reuse only exact signed field geometry; otherwise Matplotlib from this instance."""
 exact=profile in QUESTIONS and p=={'permutation':'xyz','flip':1,'scale':1}
 if exact:
  ref=re.search(r'!\[\]\(([^)]+)\)',QUESTIONS[profile][':question/problem'])[1]
  path=Path('/media/jake/SSD/EDB/math')/ref
  if not path.exists():raise FileNotFoundError(path)
  return {'prompt':str(path),'source_asset':True,'components':[str(c) for c in components]}
 output=Path(output_dir) if output_dir else HERE/'plots';output.mkdir(parents=True,exist_ok=True)
 key=digest(['plot-v2',*[str(c) for c in components]]);png=output/(key+'.png');sidecar=png.with_suffix('.json')
 if not png.exists() or not sidecar.exists():
  fd,tmp=tempfile.mkstemp(prefix='input-',suffix='.json',dir=output);os.close(fd)
  try:
   Path(tmp).write_text(json.dumps({'components':[float(c) for c in components],'exact_components':[str(c) for c in components],'output':str(png),'asset_key':key}))
   subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),tmp],check=True,capture_output=True)
  finally:Path(tmp).unlink(missing_ok=True)
 return {'prompt':str(png),'sidecar':str(sidecar),'source_asset':False,'components':[str(c) for c in components]}

def eligible(profile,p):
 if set(p)!={'permutation','flip','scale'}:raise ValueError('Expected permutation, flip, scale')
 if p['permutation'] not in ('xyz','xzy','yxz','yzx','zxy','zyx'):raise ValueError('Invalid permutation')
 if type(p['flip']) is not int or p['flip'] not in (-1,1):raise ValueError('Invalid flip')
 if type(p['scale']) is not int or not 1<=p['scale']<=3:raise ValueError('Scale must be integer 1..3')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('Invalid level')
 if template not in (None,TEMPLATES[level]):raise ValueError('Invalid level template')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Radio only')
 rng=random.Random(seed)
 raw_observed=profile=='observed:q-123750'
 if raw_observed:profile='q-123750'
 if profile is None:profile=rng.choice([k for k,v in PROFILES.items() if v[0]==level])
 if profile not in PROFILES or PROFILES[profile][0]!=level:raise ValueError('Invalid profile for difficulty')
 p=dict(parameters) if parameters is not None else {'permutation':rng.choice(('xyz','xzy','yxz','yzx','zxy','zyx')),'flip':rng.choice((-1,1)),'scale':rng.randint(1,3)}
 eligible(profile,p)
 if profile=='authored-easy':
  recipes=[{'name':name+'(x,y,z)','terms':[{'coefficient':c,'function':'','basis':b,'style':'regular'}]} for name,c,b in [('F',1,'i'),('G',-1,'i'),('H',1,'j'),('K',1,'k')]]+[None]
 else:recipes=RECIPES[profile]
 base_axis,sign,mag=PROFILES[profile][1:];axis=p['permutation'][COORDS.index(base_axis)];components=[sp.Integer(0)]*3;components[COORDS.index(axis)]=sign*mag*p['flip']*p['scale']
 transformed=[transform(r,p) for r in recipes];values=[v for v,c in transformed];vectors=[c for v,c in transformed]
 # Assessed relation: same constant axis/sign pattern; no absolute arrow scale given.
 matches=[]
 for n,c in enumerate(vectors):
  if c is not None and all(sp.simplify(e)==0 for i,e in enumerate(c) if i!=COORDS.index(axis)):
   along=sp.simplify(c[COORDS.index(axis)])
   if not along.free_symbols and along!=0 and sp.sign(along)==sign*p['flip']:matches.append(n)
 if len(matches)>1:raise ValueError('Ambiguous qualitative bank')
 correct_index=matches[0] if matches else values.index('None of the listed')
 # Complete formula equivalence, disregarding function letters, disallows duplicate options.
 for i,c in enumerate(vectors):
  for other in vectors[i+1:]:
   if c is not None and other is not None and all(sp.simplify(a-b)==0 for a,b in zip(c,other)):raise ValueError('Duplicate formula')
 solution=render_solution(profile,p,values)
 if profile=='q-123750' and not raw_observed:
  basis=BASES[COORDS.index(axis)]
  solution=solution.replace('so the $'+basis+'$ component of our vector field is constant', 'so every component of our vector field is constant')
 assets=render_plots(components,profile,p)
 problem='![]('+assets['prompt']+')\n\n'+PROMPT
 content=digest([VERSION,problem,solution,sorted(values)])
 qid=uid('question/'+content);fid=uid(qid+'/selection');answers=[]
 for v in values:answers.append({':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text' if v=='None of the listed' else ':answer.type/math',':answer/value':v})
 correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
 task=digest({'target_axis':axis,'target_sign':sign*p['flip'],'constant':True})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'dependencies':{'python':platform.python_version(),'sympy':sp.__version__},'seed':seed,'template':TEMPLATES[level],'bank_profile':('observed:q-123750' if raw_observed else profile),'parameters':p,'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'authored':profile=='authored-easy','source_ids':[] if profile=='authored-easy' else [profile],'mathematical_fingerprint':task,'content_fingerprint':content,'components':[str(c) for c in components],'choice_components':{v:None if c is None else [str(e) for e in c] for v,c in transformed},'plot':assets,'domain':'A full region containing negative, zero and positive coordinates. Logarithm option has its own positive-argument domain; no absolute arrow scale is specified.','meaningful_target_catalog_size':6,'difficulty_claim':'authored missing level' if level=='easy' else 'observed'}}

# EASY: authored axis/sign recognition. No variable-component elimination.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed three elimination stages: missing components, sign, constancy.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: observed None banks; check all four component formulas before selecting None.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n\n'.join('- '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']) for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
 records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (TEMPLATES if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
