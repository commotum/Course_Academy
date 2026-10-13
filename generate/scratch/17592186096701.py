#!/usr/bin/env python3
"""One positive scalar in a nonparallel vector combination, math basis 1356.

Observed profiles replay all 14 sources via complete math-slot masks and explicit
option-to-target ratios. Ratios record banks but do not claim recovered errors.
Normal authored banks use missing normalization, reciprocal, sign and endpoint
errors. Hard is authored: construct a positive fractional oblique known vector,
read its endpoint, subtract horizontally, and normalize a fractional residual.
The next direction-reversal KP is excluded: both combination coefficients >0.
Private Matplotlib renderer uses read-only cached Python3.10 dependencies.
No registration, database writes, or asset pruning. See private README.md.
"""
from pathlib import Path
import argparse,hashlib,json,random,uuid,subprocess,tempfile,os,math
import sympy as sp
KP_ID=17592186096701
KP_UUID='2fbb8f19-f35a-59c4-9b77-8f6c3542ef28'
TITLE='Finding a Scalar Factor in a Linear Combination'
VERSION='positive-scalar-1'
HERE=Path(__file__).with_suffix('');PROFILES={p['source_id']:p for p in json.loads((HERE/'profiles.json').read_text())}
TEMPLATES={'known_unit':'easy','known_multiple':'moderate','fractional_known':'hard'}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def number(v,style='fraction'):
 v=sp.Rational(v)
 if v.q==1:return str(v.p)
 if style=='decimal' and v.q in (2,4,5,10):return str(float(v)).rstrip('0').rstrip('.')
 if style=='slash':return str(v)
 return sp.latex(v)
def term(v,symbol,style='fraction'):return symbol if sp.Rational(v)==1 else number(v,style)+symbol

def normalize(p):
 if set(p)!={'unknown','known','scalar','a','b'}:raise ValueError('Exact parameter keys required')
 if p['unknown'] not in ('a','b'):raise ValueError('Unknown must be a or b')
 v={k:sp.Rational(p[k]) for k in ('known','scalar')}
 for k in ('a','b'):
  if not isinstance(p[k],(list,tuple)) or len(p[k])!=2:raise ValueError('Two coordinates required')
  v[k]=[sp.Rational(x) for x in p[k]]
 v['unknown']=p['unknown']
 if v['known']<=0 or not sp.Rational(1,4)<=v['scalar']<=5:raise ValueError('Positive same-direction scope')
 if abs(v['a'][0]*v['b'][1]-v['a'][1]*v['b'][0])==0:raise ValueError('Nonparallel basis required')
 if any(abs(x)>8 or x.q!=1 for k in ('a','b') for x in v[k]):raise ValueError('Integer basis coordinates magnitude <=8')
 return v

def guard(p,level,observed=False):
 if observed:return
 k,s=p['known'],p['scalar'];a,b=p['a'],p['b']
 if a[1]!=0 or a[0]<2 or a[0]>8:raise ValueError('Horizontal a with length 2..8 required')
 if level=='easy':
  if k!=1 or b[0]!=0 or not 2<=abs(b[1])<=6 or s.q not in (1,2,3) or s>4:raise ValueError('Easy: unit known, perpendicular simple grid ratio')
 elif level=='moderate':
  if p['unknown']!='a' or k.q!=1 or not 2<=k<=4 or b[0]==0 or b[1]==0 or any(abs(x)>3 for x in b) or s.q not in (1,2) or s>3:raise ValueError('Moderate: integer known multiple and oblique translation')
 elif level=='hard':
  if p['unknown']!='a' or k.q not in (2,3) or not 1<k<3 or s.q not in (3,4) or not sp.Rational(1,3)<=s<=sp.Rational(8,3) or b[0]==0 or b[1]==0 or any(abs(x)>3 for x in b) or any((k*x).q==1 for x in b):raise ValueError('Hard: actual fractional endpoint plus noninteger residual ratio')
 else:raise ValueError('Unknown difficulty')

def sample(level,rng):
 if level=='easy':return {'unknown':rng.choice(['a','b']),'known':'1','scalar':str(rng.choice([sp.Rational(n,d) for d in (1,2,3) for n in range(1,4*d+1)])),'a':[rng.randint(2,8),0],'b':[0,rng.choice([-6,-4,-3,-2,2,3,4,6])]}
 if level=='moderate':return {'unknown':'a','known':str(rng.randint(2,4)),'scalar':str(rng.choice([sp.Rational(1,2),1,sp.Rational(3,2),2,sp.Rational(5,2),3])),'a':[rng.randint(2,8),0],'b':[rng.choice([-3,-2,-1,1,2,3]),rng.choice([-3,-2,-1,1,2,3])]}
 return {'unknown':'a','known':str(rng.choice([sp.Rational(3,2),sp.Rational(5,2),sp.Rational(4,3),sp.Rational(5,3),sp.Rational(7,3)])),'scalar':str(rng.choice([sp.Rational(n,d) for d in (3,4) for n in range(1,8) if sp.Rational(n,d).q==d])),'a':[rng.randint(2,8),0],'b':[rng.choice([-3,-2,-1,1,2,3]),rng.choice([-3,-2,-1,1,2,3])]}

def canonical(p):
 # Exclude global grid rescaling; preserve reduced basis geometry and which
 # vector supplies the unknown. Profiles/banks/labels never create math tasks.
 coords=p['a']+p['b'];g=math.gcd(*(abs(int(x)) for x in coords))
 return {'unknown':p['unknown'],'known':str(p['known']),'scalar':str(p['scalar']),'primitive_basis':[[str(x/g) for x in p[k]] for k in ('a','b')]}

def coefficients(p):return (p['known'],p['scalar']) if p['unknown']=='b' else (p['scalar'],p['known'])
def plots(p,profile):
 old=PROFILES.get(profile)
 if old and normalize({k:old[k] for k in ('unknown','known','scalar','a','b')})==p:return old['original_assets']
 ca,cb=coefficients(p);known_symbol='a' if p['unknown']=='b' else 'b';endpoint=('A' if known_symbol=='a' else 'B') if p['known']==1 else 'P'
 assets={};(HERE/'plots').mkdir(exist_ok=True)
 for role in ('prompt','solution'):
  data={'a':[int(x) for x in p['a']],'b':[int(x) for x in p['b']],'ca':float(ca),'cb':float(cb),'ca_exact':str(ca),'cb_exact':str(cb),'unknown':p['unknown'],'solution':role=='solution','endpoint':endpoint,'known_label':'$'+term(p['known'],known_symbol)+'$','remaining_label':'$'+term(p['scalar'],p['unknown'])+'$','grid_increment':1,'renderer_version':2}
  name=digest(data);target=HERE/'plots'/(name+'.png');assets[role]=str(target.resolve())
  if target.exists() and target.with_suffix('.json').exists():continue
  data['target']=str(target.resolve());fd,path=tempfile.mkstemp(prefix='.render-',suffix='.json',dir=HERE/'plots');os.close(fd)
  try:
   Path(path).write_text(json.dumps(data));subprocess.run([str(Path('.venv/bin/python').resolve()),str(HERE/'render.py'),path],check=True,stdout=subprocess.DEVNULL)
  finally:Path(path).unlink(missing_ok=True)
 return assets

def slots(p,style,assets):
 k,s=p['known'],p['scalar'];u=p['unknown'];known_symbol='a' if u=='b' else 'b';known=term(k,known_symbol,style)
 given=known+r'+\lambda b' if u=='b' else r'\lambda a+'+known
 return {'GIVEN':given,'REVERSE_GIVEN':known+r'+\lambda a','KNOWN':known,'TARGET':term(s,u,style),'LENGTH':('' if s==1 else number(s,style))+'|'+u+'|','SCALAR':number(s,style),'PROMPT_PLOT':assets['prompt'],'SOLUTION_PLOT':assets['solution']}

def fill(mask,values):
 for k,v in values.items():mask=mask.replace('@'+k+'@',v)
 if '@' in mask:raise ValueError('Unresolved template component')
 return mask

def default_masks(p,field_type,level):
 # Authored peers reuse the complete observed path/matching sequence.
 reference='q-19338' if p['unknown']=='b' else 'q-70187' if p['known']==1 else 'q-20435'
 c=PROFILES[reference];pm=c['prompt_mask'];sm=c['solution_mask']
 if field_type=='blank':pm='![](@PROMPT_PLOT@)\n\nConsider the picture above. If $c=@GIVEN@,$ then $\\lambda =$\n{{field-1}}.'
 if level=='hard':
  ca,cb=coefficients(p);C=[ca*p['a'][i]+cb*p['b'][i] for i in range(2)]
  coord=lambda xy:'('+', '.join(number(x) for x in xy)+')'
  pm+='\n\nThe grid has unit squares. The exact point coordinates are $O=(0,0)$, $A='+coord(p['a'])+'$, $B='+coord(p['b'])+'$, and $C='+coord(C)+'$.'
  P=[p['known']*x for x in p['b']];res=C[0]-P[0]
  extra='The endpoint of the known component has coordinates\n\n$$\nP='+coord(P)+'.\n$$\n\nThe remaining horizontal displacement is\n\n$$\n'+number(C[0])+'-('+number(P[0])+')='+number(res)+'.\n$$\n\nCompared with the horizontal length of $a$, its scalar factor is\n\n$$\n\\frac{'+number(res)+'}{'+number(p['a'][0])+'}='+number(p['scalar'])+'.\n$$\n\n'
  sm=sm.replace('In $△OPC,$ we have:',extra+'In $△OPC,$ we have:')
 return pm,sm

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed);old=PROFILES.get(profile)
 if profile and not old and profile!='authored_operations':raise ValueError('Unknown complete profile')
 if old and level!=old['level']:raise ValueError('Observed profile level mismatch')
 if template and template not in TEMPLATES:raise ValueError('Unknown template')
 if old:
  expected='known_unit' if old['known']==1 else 'known_multiple'
  if template and template!=expected:raise ValueError('Profile template mismatch')
  template=expected
 else:
  template=template or next(k for k,v in TEMPLATES.items() if v==level)
  if TEMPLATES[template]!=level:raise ValueError('Template workload boundary')
 field_type=field_type or (old['field_type'] if old else rng.choice(['radio','blank']))
 if field_type not in ('radio','blank') or old and field_type!=old['field_type']:raise ValueError('Observed field type / supported form')
 if old and parameters is None:parameters={k:old[k] for k in ('unknown','known','scalar','a','b')}
 explicit=parameters is not None
 for attempt in range(200):
  try:
   p=normalize(parameters if explicit else sample(level,rng));guard(p,level,observed=old is not None)
   if old:
    if p['unknown']!=old['unknown'] or p['known']!=old['known'] or p['a']!=old['a'] or p['b']!=old['b']:raise ValueError('Replay profile preserves known component, unknown role and original basis geometry')
    if p['scalar'].q not in ((1,2,3) if level=='easy' else (1,2)) or p['scalar']>(5 if level=='easy' else 4):raise ValueError('Observed-level target ratio workload boundary')
   s=p['scalar'];values=[]
   if field_type=='blank':values=[s]
   elif old:values=[s*sp.Rational(r) for r in old['bank_ratios']]
   else:
    # Whole five-option bank: correct, wrong direction, reciprocal, missing
    # normalization, and failure to remove the known vector's contribution.
    u=p['a'] if p['unknown']=='a' else p['b'];axis=0 if p['unknown']=='a' else 1
    ca,cb=coefficients(p);C=ca*p['a'][axis]+cb*p['b'][axis]
    values=[s,-s,1/s,s*abs(u[axis]),s+p['known'] if level=='easy' else C/u[axis]]
   if len(set(values))!=len(values):raise ValueError('Complete bank collision')
   break
  except ValueError:
   if explicit or old:raise
 else:raise ValueError('No eligible complete instance')
 assets=plots(p,profile);style=old['scalar_style'] if old else 'fraction';sv=slots(p,style,assets)
 pm,sm=(old['prompt_mask'],old['solution_mask']) if old else default_masks(p,field_type,level)
 prompt,solution=fill(pm,sv),fill(sm,sv)
 key=old['key'] if old else 'field-1' if field_type=='blank' else 'selection'
 styles=old['bank_styles'] if old else ['fraction']*len(values)
 answers=[number(v,style) for v,style in zip(values,styles)]
 # Preserve each source scalar spelling, including slash-form blank fragments.
 fingerprint=digest(canonical(p));content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'field_type':field_type,'key':key,'bank':sorted(answers),'task':fingerprint})
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{VERSION}/{content}'));fid=str(uuid.uuid5(uuid.UUID(qid),key))
 bank=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in answers];correct=bank[values.index(s)][':answer/id'];rng.shuffle(bank)
 q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':bank,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile or 'authored_operations','bank_profile':profile or 'authored_operations','authored':old is None,'parameters':{k:[str(x) for x in v] if isinstance(v,list) else str(v) for k,v in p.items()},'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'parameter_fingerprint':fingerprint,'mathematical_fingerprint':fingerprint,'content_fingerprint':content,'plots':assets,'domain':'Both coefficients positive; a and b nonparallel; one unknown scalar only.'}}

# EASY: unit known component; horizontal/vertical grid ratio, denominators <=3.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: construct 2..4 times an oblique known vector; remaining positive ratio.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored missing level): genuinely fractional oblique endpoint and residual.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,indent=2))
 else:
  for r in records:
   q=r['question'];print(q[':question/problem']);print('\nChoices:',', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']));print('\n'+q[':question/worked-solution']+'\n')
