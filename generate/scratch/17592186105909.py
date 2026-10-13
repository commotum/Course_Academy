#!/usr/bin/env python3
"""Volumes from four vertices; math snapshot basis 1356, no database operations.

Observed profiles expose complete scalar banks on positive uniform dilation plus
translation domains. Ratios record evidence, not inferred distractor intent.
Raw profiles preserve missing ratings/solutions/correct refs and one erroneous
basis row. Normal observed profiles repair that row and infer the two keys.
Default authored operation banks use component omissions and tetrahedron halving
(division by six). All arithmetic uses exact SymPy values; no plots are needed.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105909
KP_UUID='57c790ad-c7fb-596c-8b60-cddd9b4e2165'
TITLE='Calculating the Volume of a Parallelepiped Spanned by Three Position Vectors Given Their Coordinates'
VERSION='vertex-volume-1'
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
HOME_DIR=Path(__file__).with_suffix('')
SPECS=json.loads((HOME_DIR/'specs.json').read_text())
SOURCE_TEMPLATE={sid:('unrated_radio' if not s['has_solution'] else 'blank_products_evaluated_cofactors' if s['kind']=='blank' and s['arithmetic_row_count']==3 else 'blank_evaluated_cofactors' if sid in ('q-280314','q-281030') else 'blank_products_cofactors' if s['kind']=='blank' else 'radio_products_direct' if sid=='q-73744' else 'radio_products_cofactors') for sid,s in SPECS.items()}
TEMPLATES={**{SOURCE_TEMPLATE[sid]:('hard',s['kind']) for sid,s in SPECS.items()},**{l+'_'+f:(l,f) for l in ('easy','moderate','hard') for f in ('radio','blank')}}
BANK_PROFILES={**{sid:{'origin':'observed-pattern','scope':'positive uniform dilation + translation; scalar intent unresolved'} for sid in SPECS},**{'raw_'+sid:{'origin':'raw-evidence','scope':'preserve absent metadata and source error'} for sid in SPECS},'authored_components':{'origin':'authored','scope':'complete method bank'}}
class SampleRejected(ValueError):pass
def hashval(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(sp.Rational(v)).replace(' ','')
def scalar(v):return '('+str(v)+')' if v<0 else str(v)
def basis(v,units=(False,False,False)):
 out=''
 for n,ch,unit in zip(v,'ijk',units):
  if not n:continue
  out+=('-' if n<0 else '+' if out else '')+('' if abs(n)==1 and not unit else str(abs(n)))+ch
 return out or '0'
def tupletex(v):return '⟨'+','.join(map(str,v))+'⟩'
def determinant(rows):return r'|\begin{aligned}'+r' \\ '.join(' & '.join(map(str,r)) for r in rows)+r'\end{aligned}|'
def vectors(p):return [[z[i]-p['points'][0][i] for i in range(3)] for z in p['points'][1:]]
def data(p):
 u,v,w=vectors(p);products=[(v[1]*w[2],w[1]*v[2]),(v[0]*w[2],w[0]*v[2]),(v[0]*w[1],w[0]*v[1])];terms=[u[0]*(products[0][0]-products[0][1]),-u[1]*(products[1][0]-products[1][1]),u[2]*(products[2][0]-products[2][1])]
 return u,v,w,products,terms,sum(terms)
def task_key(p):
 # Translation is incidental to volume, but the coordinate subtraction workload
 # is assessed: relative vectors and which entries need signed subtraction both
 # belong to the task. Point names are fixed by the observed response criterion.
 vec=vectors(p);signs=[[(-1 if n<0 else 0 if n==0 else 1) for n in row] for row in p['points']]
 return hashval({'vectors':vec,'coordinate_subtraction_signs':signs})
def validate_parameters(level,p,profile):
 if set(p)!={'points'} or len(p['points'])!=4 or any(len(v)!=3 or any(type(n)!=int for n in v) for v in p['points']):raise ValueError('Exactly four integer points required')
 u,v,w,prod,terms,det=data(p)
 if det==0:raise SampleRejected('Nondegenerate parallelepiped required')
 sid=profile.removeprefix('raw_') if profile and profile.startswith('raw_') else profile
 if sid in SPECS:
  s=SPECS[sid];scale=None
  for row,base in zip([u,v,w],s['vectors']):
   for x,y in zip(row,base):
    if y:
     z=sp.Rational(x,y)
     if scale is None:scale=z
     elif z!=scale:raise ValueError('Observed domain requires one uniform dilation')
    elif x:raise ValueError('Observed zero displacement must remain zero')
  if scale not in (1,2,3):raise ValueError('Observed dilation 1,2,3 only')
  shift=[a-scale*b for a,b in zip(p['points'][0],s['points'][0])]
  if any(abs(x)>8 for x in shift):raise ValueError('Translation coordinate |h|<=8')
  return int(scale)
 if any(abs(n)>8 for row in p['points'] for n in row):raise ValueError('Vertex coordinates |n|<=8')
 bound={'easy':3,'moderate':4,'hard':5}[level]
 if any(abs(n)>bound for row in [u,v,w] for n in row):raise ValueError('Displacement bound exceeded')
 active=sum(t!=0 for t in terms)
 if level=='easy' and (active!=1 or sum(n!=0 for row in [u,v,w] for n in row)>6 or any(n<0 for row in p['points'] for n in row)):raise ValueError('Easy requires one active cofactor, sparse small nonnegative vertices')
 if level=='moderate' and (active!=2 or sum(n!=0 for row in [u,v,w] for n in row)<6 or not any(n<0 for row in [u,v,w] for n in row)):raise ValueError('Moderate requires two active cofactors, mixed displacement signs')
 if level=='hard' and (active!=3 or sum(n!=0 for row in [u,v,w] for n in row)<7 or not any(n<0 for row in [u,v,w] for n in row)):raise ValueError('Hard requires three active cofactors, dense mixed displacement signs')
 if any(abs(t)>150 for t in terms) or abs(det)>200:raise ValueError('Bounded determinant arithmetic required')
 return None

def split_terms(s):
 parts=[];start=0;depth=0
 for i,c in enumerate(s):
  if c=='(':depth+=1
  elif c==')':depth-=1
  elif i and c in '+-' and depth==0:
   parts.append(s[start:i]);start=i
 parts.append(s[start:]);return parts

def dilation_row(row,scale):
 """Homogeneous arithmetic nodes: outer coefficient degree1, inner products
 degree2, explicit product factors degree1, fully evaluated cofactors degree3.
 Original fixed omission of zero terms remains valid under uniform dilation.
 """
 def numbers(t,degree):return re.sub(r'\d+',lambda m:str(int(m[0])*scale**degree),t)
 if '(' not in row:return numbers(row,3)
 result=[]
 for term in split_terms(row):
  sign=term[0] if term.startswith(('+','-')) else '';body=term[1:] if sign else term
  # Parenthesized negative coefficient precedes a minor; standalone -0 stays0.
  m=re.match(r'(\d+)(\(.*\))$',body)
  if m:result.append(sign+numbers(m[1],1)+numbers(m[2],1 if r'\cdot' in m[2] else 2));continue
  if body.startswith('('):
   if scale!=1:body=str(scale)+body
   # Only the minor's numeric factors scale here, not the inserted coefficient.
   inner=term[len(sign):];result.append(sign+(str(scale) if scale!=1 else '')+numbers(inner,1 if r'\cdot' in inner else 2));continue
  result.append(numbers(term,3))
 return ''.join(result)

def observed_solution(p,sid,scale,raw):
 s=SPECS[sid]
 if not s['has_solution']:return None if raw else authored_solution(p)
 u,v,w,products,terms,det=data(p);rows=[]
 for i,(name,point,vec) in enumerate(zip('BCD',p['points'][1:],[u,v,w])):
  units=s['subtraction_units'][str(i)]
  shown=vec[:]
  if raw and sid=='q-73744' and name=='D':shown[1]=3*scale
  # Unit visibility in the reduced basis is an observed style; zero omission is
  # structural under the source-profile dilation domain.
  b_units=s['basis_units'][i][1]
  rows.extend([r'\overset{\to }{A'+name+'} & ='+name.lower()+'-a',' & =('+basis(point,units[0])+')-('+basis(p['points'][0],units[1])+')',' & ='+basis(shown,b_units),' & ='+tupletex(vec)])
 block0=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
 minors=[[[v[1],v[2]],[w[1],w[2]]],[[v[0],v[2]],[w[0],w[2]]],[[v[0],v[1]],[w[0],w[1]]]]
 first=r'\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & ='+determinant([u,v,w])
 cofactor=scalar(u[0])+r'\cdot '+determinant(minors[0])+'-'+scalar(u[1])+r'\cdot '+determinant(minors[1])+'+'+scalar(u[2])+r'\cdot '+determinant(minors[2])
 arith=[dilation_row(row,scale) for row in s['arithmetic_source']]
 block1=r'\begin{aligned}'+r' \\  & ='.join([first,cofactor]+arith+[str(det)+('.' if s['final_det_period'] else '')])+r'\end{aligned}'
 gap=r'\,' if s['absolute_spacing'] else ''
 block2='V=|'+gap+str(det)+gap+'|='+str(abs(det))+'.'
 return s['prose_mask'].replace('@block0@',block0).replace('@block1@',block1).replace('@block2@',block2)

def authored_solution(p):
 u,v,w,products,terms,det=data(p);rows=[]
 for name,point,vec in zip('BCD',p['points'][1:],[u,v,w]):rows.extend([r'\overset{\to }{A'+name+'} & ='+name.lower()+'-a',' & =('+basis(point)+')-('+basis(p['points'][0])+')',' & ='+basis(vec),' & ='+tupletex(vec)])
 minors=[[[v[1],v[2]],[w[1],w[2]]],[[v[0],v[2]],[w[0],w[2]]],[[v[0],v[1]],[w[0],w[1]]]]
 cof=scalar(u[0])+r'\cdot '+determinant(minors[0])+'-'+scalar(u[1])+r'\cdot '+determinant(minors[1])+'+'+scalar(u[2])+r'\cdot '+determinant(minors[2])
 raw=[];evaluated=[]
 for c,m,(a,b) in zip([u[0],-u[1],u[2]],minors,products):
  raw.append(scalar(c)+r'\cdot ('+scalar(m[0][0])+r'\cdot '+scalar(m[1][1])+'-'+scalar(m[1][0])+r'\cdot '+scalar(m[0][1])+')')
  evaluated.append(scalar(c)+r'\cdot ('+scalar(a)+'-'+scalar(b)+')')
 # Group all signed coefficients and use visible multiplication; the +(-c)
 # joins intentionally avoid bare +- or -- and numeric concatenation.
 dr=[r'\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & ='+determinant([u,v,w]),' & ='+cof,' & ='+ '+'.join(raw),' & ='+ '+'.join(evaluated),' & ='+ '+'.join(scalar(t) for t in terms),' & ='+str(det)+'.']
 return 'First, we find the displacement vectors $\\overset{\\to }{AB},$ $\\overset{\\to }{AC},$ and $\\overset{\\to }{AD}$ that span the parallelepiped:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nNow, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.\n\nComputing the triple product, we have\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(dr)+r'\end{aligned}'+'\n$$\n\nTherefore, the volume of the corresponding parallelepiped spanned by $\\overset{\\to }{AB},$ $\\overset{\\to }{AC},$ and $\\overset{\\to }{AD}$ is\n\n$$\nV=|'+str(det)+'|='+str(abs(det))+'.\n$$'

def prompt(p,kind,sid=None):
 if sid:
  s=SPECS[sid];text=s['prompt_mask']
  for i,name in enumerate('ABCD'):
   pieces=[]
   for n,old in zip(p['points'][i],s['spacing'][i]):pieces.append((' ' if old.startswith(' ') else '')+str(n))
   text=text.replace('@'+name+'@',','.join(pieces))
  return text
 text='Calculate the volume '+('$V$ ' if kind=='blank' else '')+'of the parallelepiped spanned by $\\overset{\\to }{AB},$ $\\overset{\\to }{AC},$ and $\\overset{\\to }{AD},$ given the points '+', '.join('$'+name+'('+','.join(map(str,point))+'),$' for name,point in zip('ABC',p['points'][:3]))+' and $D('+','.join(map(str,p['points'][3]))+').$'
 return text+('\n\n$V=${{field-1}}' if kind=='blank' else '')
def bank(p,kind,sid,scale):
 u,v,w,products,terms,det=data(p);correct=sp.Integer(abs(det))
 if kind=='blank':return [correct],[{'operation':'absolute scalar triple product'}]
 if sid:
  vals=[correct*sp.Rational(z) for z in SPECS[sid]['ratios']];recipes=[{'operation':'volume times observed ratio on uniform-dilation domain','ratio':z,'intent':'unresolved'} for z in SPECS[sid]['ratios']]
 else:
  # One full eligible bank chosen first: correct plus omitted determinant column
  # contribution (three wrong sums) and division by six (tetrahedron formula).
  vals=[correct]+[sp.Integer(abs(det-t)) for t in terms]+[correct/6]
  recipes=[{'operation':'absolute determinant'}]+[{'operation':'omit cofactor contribution','column':i} for i in range(3)]+[{'operation':'use tetrahedron divisor6'}]
 if len(set(vals))!=5 or any(x<0 for x in vals) or sum(x==correct for x in vals)!=1:raise SampleRejected('Entire operation bank rejected for collision')
 return vals,recipes

def sample(level,rng,kind):
 # EASY construction: triangular sparse matrix with one active first-row
 # cofactor. Default radio uses a separate complete eligible bank (see generate).
 limit={'easy':3,'moderate':4,'hard':5}[level]
 if level=='easy':
  u=[rng.randint(1,3),0,0];v=[rng.randint(1,3),rng.randint(1,3),0];w=[0,rng.randint(1,3),rng.randint(1,3)];a=[rng.randint(0,3) for _ in range(3)]
 else:u,v,w=[[rng.randint(-limit,limit) for _ in range(3)] for _ in range(3)];a=[rng.randint(-3,3) for _ in range(3)]
 return {'points':[a]+[[x+y for x,y in zip(a,row)] for row in [u,v,w]]}
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 raw=bool(profile and profile.startswith('raw_'));sid=profile.removeprefix('raw_') if raw else profile
 if profile and profile not in BANK_PROFILES:raise ValueError('Unknown profile')
 if sid not in SPECS:sid=None
 if template in SPECS: # Supported source-ID alias; canonical template is family.
  if sid and sid!=template:raise ValueError('Template/profile mismatch')
  sid=template;profile=profile or sid;template=SOURCE_TEMPLATE[sid]
 if sid:
  implied=SOURCE_TEMPLATE[sid]
  if template and template!=implied:raise ValueError('Template/profile mismatch')
  template=implied
  if level!='hard':raise ValueError('Unrated sources explicitly assigned authored hard; observed profiles hard only')
 elif template in set(SOURCE_TEMPLATE.values()):
  if profile is not None:raise ValueError('Observed family requires an observed source profile')
  sid=random.Random(seed).choice([s for s,t in SOURCE_TEMPLATE.items() if t==template]);profile=sid
 else:template=template or level+'_'+(field_type or 'blank')
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('Template/difficulty mismatch')
 kind=TEMPLATES[template][1]
 if field_type and field_type.removeprefix(':answer-field.type/')!=kind:raise ValueError('Field/template mismatch')
 if profile=='authored_components' and kind=='blank':raise ValueError('Radio profile requires radio')
 rng=random.Random(seed)
 for attempt in range(3000):
  if parameters is not None:p=json.loads(json.dumps(parameters))
  elif sid:
   scale=rng.choice([1,2,3]);shift=[rng.randint(-4,4) for _ in range(3)];p={'points':[[scale*x+h for x,h in zip(row,shift)] for row in SPECS[sid]['points']]}
  else:p=sample(level,rng,kind)
  try:
   scale=validate_parameters(level,p,profile)
   vals,recipes=level_bank(p,level) if not sid and kind=='radio' and level in ('easy','moderate') else bank(p,kind,sid,scale)
  except ValueError:
   if parameters is not None:raise
   continue
  problem=prompt(p,kind,sid);solution=observed_solution(p,sid,scale,raw) if sid else authored_solution(p)
  if sid and not raw and not SPECS[sid]['has_solution']:
   problem=problem.replace('AB^(→)',r'\overset{\to }{AB}').replace('AC^(→)',r'\overset{\to }{AC}').replace('AD^(→)',r'\overset{\to }{AD}')
  correct=abs(data(p)[-1]);key=SPECS[sid]['key'] if sid else ('selection' if kind=='radio' else 'field-1')
  content=hashval({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(map(tex,vals)),'field_type':kind,'key':key,'difficulty':None if raw and not SPECS[sid]['has_difficulty'] else level,'correct':None if raw and not SPECS[sid]['has_correct'] else tex(correct)})
  qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));fid=str(uuid.uuid5(uuid.UUID(qid),key));answers=[];recipe_map={}
  for value,recipe in zip(vals,recipes):
   aid=str(uuid.uuid5(uuid.UUID(fid),tex(value)));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(value)});recipe_map[aid]=recipe
   if value==correct:correct_id=aid
  rng.shuffle(answers)
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
  if not raw or SPECS[sid]['has_correct']:field[':answer-field/correct']=[':answer/id',correct_id]
  question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
  if not raw or SPECS[sid]['has_difficulty']:question[':question/difficulty']=':question.difficulty/'+level
  if solution is not None:question[':question/worked-solution']=solution
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':profile,'bank_origin':'raw-evidence' if raw else 'observed-pattern' if sid else 'authored','evidence_only':bool(sid),'eligible_for_learning':not bool(sid),'parameter_fingerprint':task_key(p),'content_fingerprint':content,'recipes':recipe_map,'provenance':PROVENANCE,'source_id':sid,'authored_level_assignment':sid in ('q-128472','q-20138'),'authored_extension':level in ('easy','moderate') or not sid,'repairs':[] if raw else (['AD basis 3j -> j'] if sid=='q-73744' else ['missing correct ref inferred; missing solution authored; hard assigned'] if sid in ('q-128472','q-20138') else []),'plot_rating':'none','sympy_version':sp.__version__}}
 raise SampleRejected('Full-bank bounded sampler exhausted')
def level_bank(p,level):
 """Complete sparse-level bank: correct, double, half, sixth, and the
 determinant of position vectors B,C,D (omitting the displacement operation).
 Scaling errors are explicit method errors, never source-intent hypotheses.
 """
 correct=sp.Integer(abs(data(p)[-1]));wrong=abs(sp.Matrix(p['points'][1:]).det());vals=[correct,2*correct,correct/2,correct/6,wrong]
 if len(set(vals))!=5 or any(v<=0 for v in vals):raise SampleRejected('Sparse-method wholebank collision/domain')
 return vals,[{'operation':x} for x in ('absolute displacement determinant','add absolute forward and reversed triple products (2V)','use triangle base factor 1/2 (V/2)','tetrahedron divisor6','use position vectors instead of displacements')]
# EASY: authored sparse |component|<=3; one active cofactor, nonnegative vertices.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored |component|<=4; two active cofactors, mixed signs.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: observed workload and bounded authored dense signed determinant variants.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f.get(':answer-field/correct',['',None])[1] else '') for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','Source has no worked solution.')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
