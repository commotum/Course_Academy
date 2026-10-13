#!/usr/bin/env python3
"""Area of a quadrilateral; math basis 1356, no database operations.

Observed template masks and complete opaque historical banks are in recipes.json.
Public observed profiles preserve omissions, original diagrams and anomalous math
for fidelity; every such record is evidence-only, ineligible for practice. Uniform
length scaling parameterizes those profiles, with historical numerical banks scaled
as recorded values, not claimed recovered error operations. Default banks use
method operations, and default solutions retain each observed operative chain.

Easy (authored): parallelogram, supplied diagonal, integer sides, 60 degree angle;
one sine-area substitution and doubling. Moderate: observed template layouts,
integer side measurements, usual calculator angles, infer the splitting diagonal
or parallelogram symmetry. Hard (authored): two unequal triangles, decimal lengths
and decimal angles, tenth rounding. Same included-angle sine method throughout.
Raw source replay bypasses authored bounds only under explicit observed profiles.
Normal changed general measurements must admit a common diagonal to within their
angle display precision, and are marked as measurements on a schematic diagram.
Stop at guide step 7; local JSON is review data, never transaction EDN.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR',str(ROOT_MPL:=Path('/tmp/17592186105905-mpl')))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge

KP_ID=17592186105905
KP_UUID='3173d361-b91d-5699-97d8-6595ef59d0a3'
TITLE='Calculating the Area of a Quadrilateral'
VERSION='quadrilateral-sine-5'
ROOT=Path(__file__).resolve().with_suffix('')
RECIPES=json.loads((ROOT/'recipes.json').read_text())
SOURCE=json.loads((ROOT/'source.json').read_text())
NAMESPACE=uuid.UUID(KP_UUID)

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def number(v):
 q=sp.Rational(str(v))
 return str(int(q)) if q.q==1 else str(float(q)).rstrip('0').rstrip('.')
def rounded(v,d): return format(Decimal(str(float(v))).quantize(Decimal(1).scaleb(-d),rounding=ROUND_HALF_UP),f'.{d}f')
def work(v,d):
 s=rounded(v,d)
 return s[:-1]+r'\,'+s[-1] if d==4 else s

def calculations(p,kind):
 a,b,t=(sp.Rational(str(p[k])) for k in ('a','b','theta'))
 u=a*b*sp.sin(sp.pi*t/180)/2
 if kind=='para': v=None; total=2*u
 else:
  c,d,f=(sp.Rational(str(p[k])) for k in ('c','d','phi'))
  v=c*d*sp.sin(sp.pi*f/180)/2; total=u+v
 return u,v,total

def approximate_geometry(p):
 """Recover coordinates using the first triangle and side-side shared diagonal.
 General raster is schematic; its two marked angles agree to displayed precision.
 """
 a,b,t=map(float,[p['a'],p['b'],p['theta']]); A=(0.,0.); B=(a,0.); D=(b*math.cos(math.radians(t)),b*math.sin(math.radians(t)))
 if 'c' not in p:
  # para angle is at B in default raster. Side a is AB, b is BC.
  C=(a-b*math.cos(math.radians(t)),b*math.sin(math.radians(t)))
  D=(C[0]-a,C[1]); return dict(A=A,B=B,C=C,D=D)
 c,d=map(float,[p['c'],p['d']]); vx,vy=D[0]-B[0],D[1]-B[1]; L=math.hypot(vx,vy)
 x=(d*d+L*L-c*c)/(2*L); h2=d*d-x*x
 if h2<=0: raise ValueError('second triangle incompatible with the shared diagonal')
 h=math.sqrt(h2); ex,ey=vx/L,vy/L
 C=(B[0]+x*ex+h*ey,B[1]+x*ey-h*ex)
 return dict(A=A,B=B,C=C,D=D)

def geometry_guard(p):
 if 'c' not in p:return
 a,b,t,c,d,f=map(float,[p[k] for k in ('a','b','theta','c','d','phi')])
 L2=a*a+b*b-2*a*b*math.cos(math.radians(t))
 cosf=(c*c+d*d-L2)/(2*c*d)
 if not -1<cosf<1:raise ValueError('incompatible triangle sides')
 actual=math.degrees(math.acos(cosf)); tolerance=.051 if not float(f).is_integer() else .501
 if abs(actual-f)>tolerance:raise ValueError('inconsistent shared-diagonal measurements')

def validate_parameters(p,kind,level,raw=False,diagonal='BD'):
 keys={'a','b','theta','precision'} | ({'c','d','phi'} if kind=='general' else set())
 if set(p)!=keys:raise ValueError('parameter keys must be '+str(sorted(keys)))
 for k in keys-{'precision'}:
  if not isinstance(p[k],(int,float)) or not math.isfinite(p[k]):raise ValueError('finite numeric parameters required')
 for k in ('a','b')+ (('c','d') if kind=='general' else ()):
  if not 2<=p[k]<=42:raise ValueError('side bounds 2 through 42')
 for k in ('theta',)+(('phi',) if kind=='general' else ()):
  if not 15<=p[k]<=150:raise ValueError('angle bounds 15 through 150 degrees')
 if p['precision'] not in (0,1):raise ValueError('integer or tenth precision required')
 if raw:return
 if level=='easy':
  if kind!='para' or p['theta']!=60 or p['precision']!=0 or any(not float(p[k]).is_integer() or p[k]>20 for k in ('a','b')):raise ValueError('easy requires integer sides <=20, supplied diagonal and 60 degree angle')
 if level=='moderate':
  if any(abs(float(p[k])*10-round(float(p[k])*10))>1e-8 for k in ('theta',)+(('phi',) if kind=='general' else ())):raise ValueError('moderate angle measurements must be integer or one-decimal degrees')
  if any(not float(p[k]).is_integer() for k in ('a','b')+(('c','d') if kind=='general' else ())):raise ValueError('moderate side measurements must be integers')
 if level=='hard':
  if any(abs(float(p[k])*10-round(float(p[k])*10))>1e-8 for k in keys-{'precision'}):raise ValueError('hard measurements must have at most one decimal place')
  if kind!='general' or p['precision']!=1 or float(p['theta']).is_integer() or float(p['phi']).is_integer() or sum(not float(p[k]).is_integer() for k in ('a','b','c','d'))<2:raise ValueError('hard requires asymmetric decimal measurements and tenth rounding')
 geometry_guard(p)
 sidevals=[float(p[k]) for k in ('a','b')+(('c','d') if kind=='general' else ())]
 if max(sidevals)/min(sidevals)>3:raise ValueError('side-ratio ceiling preserves source diagram legibility')
 gp=dict(p)
 if kind=='general' and diagonal=='AC':gp['c'],gp['d']=p['d'],p['c']
 pts=approximate_geometry(gp);poly=[pts[k] for k in 'ABCD'];crosses=[]
 for i in range(4):
  before,vertex,after=poly[(i-1)%4],poly[i],poly[(i+1)%4]
  v1=(vertex[0]-before[0],vertex[1]-before[1]);v2=(after[0]-vertex[0],after[1]-vertex[1])
  crosses.append(v1[0]*v2[1]-v1[1]*v2[0])
  cosine=-(v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2))
  interior=math.degrees(math.acos(max(-1,min(1,cosine))))
  if interior<25:raise ValueError('diagram interior angle below legibility ceiling')
 if not (all(x>0 for x in crosses) or all(x<0 for x in crosses)):raise ValueError('normal quadrilateral must be convex like observed figures')
 u,v,_=calculations(p,kind)
 if level=='hard' and abs(float(u-v))<1:raise ValueError('hard requires unequal component triangle areas')

def render_plots(p,recipe,output_dir=None, supplied_diagonal=False):
 """Atomic deterministic Matplotlib PNG+sidecar, no shared temporary inputs."""
 out=Path(output_dir or ROOT/'plots'); out.mkdir(parents=True,exist_ok=True)
 key=digest({'p':p,'kind':recipe['kind'],'diagonal':recipe['diagonal'],'supplied':supplied_diagonal,'version':VERSION})
 paths={}
 geometry_p=dict(p)
 if recipe['kind']=='general' and recipe['diagonal']=='AC':geometry_p['c'],geometry_p['d']=p['d'],p['c']
 pts=approximate_geometry(geometry_p)
 # General AC source uses a,b at D and c,d at B. Rotate labels without changing sides.
 if recipe['kind']=='general' and recipe['diagonal']=='AC':pts={dict(A='D',B='A',C='B',D='C')[k]:v for k,v in pts.items()}
 for role in ('prompt','solution'):
  path=out/(key+'-'+role+'.png'); side=path.with_suffix('.json'); paths[role]=str(path)
  if path.exists() and side.exists():continue
  fig,ax=plt.subplots(figsize=(6.2,3.8),dpi=135)
  poly=[pts[k] for k in 'ABCD']; ax.add_patch(Polygon(poly,closed=True,fill=recipe['kind']=='para',facecolor='#eaf4fc',edgecolor='black',linewidth=1.8))
  diag=recipe['diagonal']; show=(role=='solution' or supplied_diagonal)
  if show:ax.plot(*zip(pts[diag[0]],pts[diag[1]]),color='gray',linestyle='--',linewidth=1.2)
  xs,ys=zip(*poly); span=max(max(xs)-min(xs),max(ys)-min(ys)); center=(sum(xs)/4,sum(ys)/4)
  for k,(x,y) in pts.items():
   dx,dy=x-center[0],y-center[1]; norm=math.hypot(dx,dy)
   ax.text(x+.045*span*dx/norm,y+.045*span*dy/norm,k,fontstyle='italic',fontsize=12,ha='center',va='center')
  if recipe['kind']=='para':
   pairs=[('A','B',p['a']),('B','C',p['b'])]; angles=[('B',p['theta'])]
  elif diag=='BD':
   pairs=[('A','B',p['a']),('A','D',p['b']),('D','C',p['c']),('B','C',p['d'])]; angles=[('A',p['theta']),('C',p['phi'])]
  else:
   pairs=[('D','A',p['a']),('D','C',p['b']),('A','B',p['c']),('C','B',p['d'])]; angles=[('D',p['theta']),('B',p['phi'])]
  for k,l,value in pairs:
   x,y=pts[k];xx,yy=pts[l];mx,my=(x+xx)/2,(y+yy)/2;nx,ny=yy-y,x-xx
   if nx*(mx-center[0])+ny*(my-center[1])<0:nx,ny=-nx,-ny
   norm=math.hypot(nx,ny)
   ax.text(mx+.055*span*nx/norm,my+.055*span*ny/norm,number(value),fontsize=11,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=.7))
  for i,(k,value) in enumerate(angles):
   v=pts[k]; before=pts['ABCD'[('ABCD'.index(k)-1)%4]];after=pts['ABCD'[('ABCD'.index(k)+1)%4]]
   aa=math.degrees(math.atan2(before[1]-v[1],before[0]-v[0]));bb=math.degrees(math.atan2(after[1]-v[1],after[0]-v[0]));delta=(bb-aa)%360
   if delta>180:aa,bb=bb,aa;delta=360-delta
   ax.add_patch(Wedge(v,.085*span,aa,aa+delta,facecolor=('#76b2db','#eddd65')[i],alpha=.85))
   mid=math.radians(aa+delta/2);ax.text(v[0]+.135*span*math.cos(mid),v[1]+.135*span*math.sin(mid),number(value)+'°',fontsize=10,ha='center',va='center')
  ax.set_aspect('equal');ax.set_xlim(min(xs)-.16*span,max(xs)+.16*span);ax.set_ylim(min(ys)-.16*span,max(ys)+.16*span);ax.axis('off');fig.tight_layout(pad=.1)
  fd,tmp=tempfile.mkstemp(suffix='.png',dir=out);os.close(fd)
  try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
  finally:
   plt.close(fig)
   if os.path.exists(tmp):os.unlink(tmp)
  provenance={'renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0],'parameters':p,'vertices':pts,'side_labels':pairs,'angle_labels':angles,'diagonal':diag if show else None,'drawn_to_scale':False,'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  fd,tmp=tempfile.mkstemp(suffix='.json',dir=out);os.close(fd)
  try:Path(tmp).write_text(json.dumps(provenance,indent=2)+'\n');os.replace(tmp,side)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
 return paths

def replacement_values(p,r,raw=False):
 u,v,total=calculations(p,r['kind']); digits=r['workdigits']
 vals={k:number(value) for k,value in p.items()}
 vals.update(h1=number(sp.Rational(str(p['a']))*sp.Rational(str(p['b']))/2),v1=work(u,digits),answer=rounded(total,p['precision']))
 if v is not None:vals.update(h2=number(sp.Rational(str(p['c']))*sp.Rational(str(p['d']))/2),v2=work(v,digits))
 displaytotal=float(rounded(u,digits))+(float(rounded(v,digits)) if v is not None else float(rounded(u,digits)))
 if raw and r['source_db_id']==17592186234325:
  displaytotal=math.floor(float(total)*10**digits)/10**digits # preserve documented source truncation anomaly
 vals['total']=work(displaytotal,digits)
 return vals

def fill(mask,vals):
 return re.sub(r'\{\{([a-z0-9]+)\}\}',lambda m:vals[m[1]],mask)

def solution(p,r,plots,raw=False):
 vals=replacement_values(p,r,raw)
 mask=r['solution_mask']
 if mask is None:
  # Authored supported completion follows the same full source decomposition chain.
  mask=RECIPES['q-285703']['solution_mask']
  if r['kind']=='para':mask=RECIPES['q-279762']['solution_mask']
  mask=mask.replace('**nearest tenth**','nearest integer' if p['precision']==0 else 'nearest tenth')
 s=fill(mask,vals)
 s=re.sub(r'!\[\]\(images/[^)]+\)',f'![]({plots["solution"]})',s)
 if not raw:
  if r['source_db_id']==17592186234325:
   opening,rest=s.split('\n\n',1);s=opening+'\n\n![]('+plots['solution']+')\n\n'+rest
  if r['source_db_id']==17592186341859:s=s.replace('{A}_{ACD}','{A}_{ACB}')
  # Normal chains show approximate rounded stages, preserving all operation rows.
  s=s.replace(' & ='+vals['v1'],' & ≈'+vals['v1']).replace(' & ='+vals['total'],' & ≈'+vals['total'])
  s=s.replace('nearest integer','nearest tenth' if p['precision']==1 else 'nearest integer')
  s=s.replace('nearest tenth','nearest integer' if p['precision']==0 else 'nearest tenth')
 return s

def bank_values(p,r,profile):
 u,v,total=calculations(p,r['kind']); precision=p['precision']
 if profile.startswith('observed-'):
  anchor=r['parameters']; scale=sp.Rational(str(p['a']))/sp.Rational(str(anchor['a']))
  for k in ('a','b')+(('c','d') if r['kind']=='general' else ()):
   if sp.Rational(str(p[k]))!=sp.Rational(str(anchor[k]))*scale:raise ValueError('opaque source bank permits uniform length scaling only')
  for k in ('theta','phi','precision'):
   if k in anchor and p[k]!=anchor[k]:raise ValueError('opaque source profile retains angles and precision')
  return [rounded(sp.Rational(v)*scale**2,precision) for v in r['bank']]
 if r['kind']=='para':
  # Omit symmetry, omit sine, omit sine and 1/2, omit sine and symmetry.
  products=sp.Rational(str(p['a']))*sp.Rational(str(p['b']))
  values=[total,u,products,2*products,products/2]
 else:
  # Omit first/second triangle, omit both 1/2 factors, subtract instead of adding.
  values=[total,u,v,2*total,abs(u-v)]
 result=[rounded(x,precision) for x in values]
 if len(set(result))!=len(result) or any(float(x)<=0 for x in result):raise ValueError('whole operation bank is ambiguous or outside positive area domain')
 return result

def sampler(level,r,rng):
 if level=='easy':return {'a':rng.randint(2,20),'b':rng.randint(2,20),'theta':60,'precision':0}
 if r['kind']=='para':return {'a':rng.randint(2,32),'b':rng.randint(2,32),'theta':rng.randint(25,135),'precision':0}
 step=1 if level=='moderate' else 10
 p={k:rng.randint(20,320)/10 if step==10 else rng.randint(2,32) for k in ('a','b','c','d')}
 p['theta']=rng.randint(251,1349)/10 if step==10 else rng.randint(25,135)
 L2=p['a']**2+p['b']**2-2*p['a']*p['b']*math.cos(math.radians(p['theta']))
 f=(p['c']**2+p['d']**2-L2)/(2*p['c']*p['d'])
 if not -1<f<1:raise ValueError('sampled sides not eligible')
 p['phi']=round(math.degrees(math.acos(f)),1 if step==10 else 0)
 if step==1:p['phi']=int(p['phi'])
 p['precision']=rng.choice([0,1]) if step==1 else 1
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 raw=bool(profile and profile.startswith('observed-'))
 if raw:
  sourceid=profile.removeprefix('observed-')
  if template is None:template=sourceid
  if template!=sourceid:raise ValueError('source profile belongs to one template')
 if template is None:
  candidates=[k for k,r in RECIPES.items() if (level=='moderate' or (r['kind']=='para')==(level=='easy')) and (not field_type or (r['field_type'] or 'blank')==field_type)]
  template=random.Random(seed).choice(candidates)
 if template not in RECIPES:raise ValueError('unknown template')
 r=RECIPES[template]
 if not raw and ((level=='easy' and r['kind']!='para') or (level=='hard' and r['kind']!='general')):raise ValueError('template outside authored level')
 typ=r['field_type'] or 'blank'
 if field_type and field_type!=typ:raise ValueError('field type differs from preserved template layout')
 if profile is None:profile='method-derived'
 if not raw and profile!='method-derived':raise ValueError('unknown profile')
 rng=random.Random(seed)
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else (dict(r['parameters']) if raw else sampler_safe(level,r,rng))
  if p is None:continue
  try:
   validate_parameters(p,r['kind'],level,raw,r['diagonal'])
   values=bank_values(p,r,profile) if typ=='radio' or raw else [replacement_values(p,r)['answer']]
   if not raw and typ=='blank':values=[replacement_values(p,r)['answer']]
   break
  except ValueError:
   if parameters is not None or raw:raise
 else:raise ValueError('no eligible whole-bank instance found')
 anchor=p==r['parameters']
 if raw and anchor:plots={'prompt':re.findall(r'images/[^)]+',r['problem_mask'])[0],'solution':None}
 else:plots=render_plots(p,r,supplied_diagonal=level=='easy')
 prompt=re.sub(r'!\[\]\(images/[^)]+\)',f'![]({plots["prompt"]})',r['problem_mask'])
 if not raw:
  prompt=prompt.replace('nearest integer','nearest tenth' if p['precision']==1 else 'nearest integer')
  prompt=prompt.replace('nearest tenth','nearest integer' if p['precision']==0 else 'nearest tenth')
  if typ=='blank' and '{{field-1}}' not in prompt:prompt+='\n\nArea: {{field-1}}.'
  if typ=='blank':prompt+='\n\nEnter the rounded number using digits and a decimal point if needed.'
  prompt+='\n\nThe diagram is not drawn to scale. Use the marked measurements.'
  if r['kind']=='general':prompt+=' The marked angles are rounded to the precision shown; calculate the area estimate using the marked values.'
  if level=='easy':prompt+=' The dashed diagonal divides the parallelogram into two congruent triangles.'
 q={':question/problem':prompt}
 if r['has_solution'] or not raw:
  if raw and anchor:
   # Fill every mathematical slot even at the source anchor, keeping exact image refs.
   q[':question/worked-solution']=fill(r['solution_mask'],replacement_values(p,r,True))
  else:q[':question/worked-solution']=solution(p,r,plots,raw)
 if r['has_difficulty'] or not raw:q[':question/difficulty']=':question.difficulty/'+('moderate' if raw else level)
 if raw:q[':question/math-academy-id']=template
 canonical=digest({'version':VERSION,'prompt':prompt,'solution':q.get(':question/worked-solution'),'level':q.get(':question/difficulty'),'values':sorted(values),'field_type':typ if r['has_fields'] or not raw else None,'correct':r['correct_index'] if raw else 0})
 qid=str(uuid.uuid5(NAMESPACE,canonical));q[':question/id']=qid
 if r['has_fields'] or not raw:
  key=r['key'] or 'field-1';fid=str(uuid.uuid5(uuid.UUID(qid),key))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':answers}
  idx=r['correct_index'] if raw else 0
  if idx is not None:f[':answer-field/correct']=[':answer/id',answers[idx][':answer/id']]
  if typ=='radio':rng.shuffle(answers)
  q[':question/answer-fields']=[f]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'difficulty_design':level,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':r['source_db_id'],'evidence_only':raw,'eligible_for_learning':not raw,'authored_levels':level in ('easy','hard') and not raw,'mathematical_fingerprint':task_fingerprint(p,r['kind'],level),'content_hash':canonical,'plots':plots,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}

def task_fingerprint(p,kind,level):
 pairs=[(tuple(sorted([p['a'],p['b']])),p['theta'])]
 if kind=='general':pairs.append((tuple(sorted([p['c'],p['d']])),p['phi']))
 return digest({'kind':kind,'triangles':sorted(pairs),'precision':p['precision'],'assessed_information':'supplied_diagonal' if level=='easy' else 'infer_diagonal'})

def sampler_safe(level,r,rng):
 try:return sampler(level,r,rng)
 except ValueError:return None

# EASY: authored reduced workload, source parallelogram solution chain.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed layouts and included-angle/calculator workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored decimal measured sides/angles; same sum-of-two-sine-areas method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question']; lines=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):lines += [f"- ${a[':answer/value']}$" for a in f[':answer-field/choices']]
 if ':question/worked-solution' in q:lines+=['\nWorked solution:\n'+q[':question/worked-solution']]
 output='\n\n'.join(lines)
 if record['generation']['evidence_only']:
  output=re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![](/media/jake/SSD/EDB/math/'+m[1]+')',output)
 return output
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
