#!/usr/bin/env python3
"""Triangle-area generator, steps 3–7; math basis1356, no database writes.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus individually documented easy/moderate/hard entrypoints.
Use project .venv; CLI --difficulty easy|moderate|hard|all --seed --count
--format markdown|json [--template NAME] [--profile NAME].
Source-shaped solutions preserve source component and arithmetic stages. Public
raw profiles preserve omissions and opaque historical banks as evidence only.
All normal radio banks derive complete errors from the displayed area method.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, sys, tempfile, threading, uuid
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/triangle-area-mpl')
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon, Wedge

KP_ID=17592186105903
KP_UUID='acc86fb6-2ef4-5f8f-b204-6e1fdbbf0530'
TITLE='Calculating the Area of a Triangle'
VERSION='triangle-area-2'
ROOT=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS=SOURCE['record'][':knowledge-point/questions']
BYID={q[':question/math-academy-id']:q for q in QUESTIONS}
PLOT_LOCK=threading.RLock()
# First side u=AB, second side v=AC (included A) or BC (included B).
ANCHORS={
 'q-18021':dict(u='3',v='7',angle=128),
 'q-18023':dict(u='5',v='13',angle=20),
 'q-18027':dict(u='26',v='22',angle=11),
 'q-279752':dict(u='4',v='8',angle=40),
 'q-279753':dict(u='18',v='12',angle=120),
 'q-280260':dict(u='5',v='5',angle=60),
}
TEMPLATES={
 'radio_A':dict(kind='radio',vertex='A',digits=2,sources=['q-18021','q-18027']),
 'radio_B_calculator':dict(kind='radio',vertex='B',digits=2,sources=['q-18023']),
 'blank_B_tenth_above':dict(kind='blank',vertex='B',digits=1,sources=['q-279752']),
 'blank_A_tenth_ft':dict(kind='blank',vertex='A',digits=1,sources=['q-279753']),
 'blank_B_hundredth':dict(kind='blank',vertex='B',digits=2,sources=['q-280260']),
 'decimal_sides':dict(kind='radio',vertex='A',digits=2,sources=[],level='moderate'),
 'angle_sum':dict(kind='radio',vertex='B',digits=2,sources=[],level='hard'),
}
SOURCE_TEMPLATE={s:k for k,t in TEMPLATES.items() for s in t['sources']}
PROFILES={'method_sine':{'eligible':True,'operations':['area','omit_half','omit_sine','cosine_absolute','sine_squared']},
          'blank':{'eligible':True,'operations':['area']}}
for sid in ('q-18021','q-18023','q-18027'):
 PROFILES['raw_'+sid]={'eligible':False,'source':sid,'operations':['area-scaled opaque observed decimal ratio']*5}
for sid in ('q-279752','q-279753','q-280260'):
 PROFILES['raw_'+sid]={'eligible':False,'source':sid,'operations':['area']}


def stable(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x): return hashlib.sha256(stable(x).encode()).hexdigest()
def ident(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+stable(x)))
def rat(x):
 if isinstance(x,float): raise ValueError('Use exact decimal strings, not float parameters')
 try: return sp.Rational(str(x))
 except Exception as e: raise ValueError('Expected rational side') from e

def number(x):
 x=sp.Rational(x)
 if x.q==1:return str(x.p)
 # finite decimal sides only, but output a rational product exactly when needed
 d=Decimal(str(x.p))/Decimal(str(x.q))
 return format(d,'f').rstrip('0').rstrip('.')
def rounded(x,digits):
 return format(Decimal(str(sp.N(x,60))).quantize(Decimal(10)**-digits,rounding=ROUND_HALF_UP),f'.{digits}f')
def sine6(angle):
 s=rounded(sp.sin(sp.pi*angle/180),6)
 return s[:5]+r'\,'+s[5:]
def truncated_sine6(angle):
 from decimal import ROUND_DOWN
 value=format(Decimal(str(sp.N(sp.sin(sp.pi*angle/180),60))).quantize(Decimal('.000001'),rounding=ROUND_DOWN),'.6f')
 return value[:5]+r'\,'+value[5:]
def area(p):return sp.Rational(1,2)*rat(p['u'])*rat(p['v'])*sp.sin(sp.pi*p['angle']/180)
def canonical(p):
 # Inputs define the assessed triangle; swapping the two supplied sides does
 # not create another mathematical task. Unit spelling is incidental here; numerical side lengths and rounding determine the task.
 return dict(sides=sorted([str(rat(p['u'])),str(rat(p['v']))]),angle=p['angle'],
             given_angles=sorted(p.get('given_angles',[])))

def normalize(p,level,raw=False):
 required={'u','v','angle'} | ({'given_angles'} if level=='hard' and not raw else set())
 if set(p)!=required:raise ValueError('Exact parameter keys required: '+str(required))
 u,v=rat(p['u']),rat(p['v']); angle=p['angle']
 if not isinstance(angle,int) or isinstance(angle,bool) or not 10<=angle<=160:raise ValueError('Angle must be integer 10..160')
 if u<=0 or v<=0 or u>60 or v>60:raise ValueError('Sides must be positive and at most 60')
 if level=='easy' or raw:
  if u.q!=1 or v.q!=1:raise ValueError('Easy source workload uses integer sides')
 elif level=='moderate':
  if not (2<=u<=30 and 2<=v<=30 and (u*10).q==1 and (v*10).q==1 and u.q!=1 and v.q!=1):
   raise ValueError('Moderate requires both noninteger one-decimal sides in [2,30]')
 elif level=='hard':
  if not(2<=u<=30 and 2<=v<=30 and (u*100).q==1 and (v*100).q==1 and (u*10).q!=1 and (v*10).q!=1):
   raise ValueError('Hard requires two non-tenth hundredth sides in [2,30]')
  angles=p['given_angles']
  if not isinstance(angles,list) or len(angles)!=2 or any(not isinstance(a,int) or isinstance(a,bool) or not 15<=a<=140 for a in angles):raise ValueError('Two bounded integer angles required')
  if sum(angles)+angle!=180:raise ValueError('Triangle angles must sum to180')
  if u!=v or angles[0]!=angles[1]:raise ValueError('Hard isosceles triangle requires equal supplied sides and equal base angles')
 return {**p,'u':number(u),'v':number(v)}


def source_solution(sid,p,raw=False):
 """Mask full mathematical components, then render all source stages.
 No literal-payload branch at the anchor; the same mask handles changed inputs.
 """
 q=BYID[sid]
 if ':question/worked-solution' not in q:return None
 a=ANCHORS[sid]; u0,v0=rat(a['u']),rat(a['v']);u,v=rat(p['u']),rat(p['v'])
 old=rounded(area(a),TEMPLATES[SOURCE_TEMPLATE[sid]]['digits'])
 new=rounded(area(p),TEMPLATES[SOURCE_TEMPLATE[sid]]['digits'])
 second='AC' if TEMPLATES[SOURCE_TEMPLATE[sid]]['vertex']=='A' else 'BC'
 replacements={
  f'AB={number(u0)}':f'AB={number(u)}',
  f'{second}={number(v0)}':f'{second}={number(v)}',
  '{'+str(a['angle'])+'}':'{'+str(p['angle'])+'}',
  (r'0.788\,010' if sid=='q-18021' else sine6(a['angle'])):(truncated_sine6(p['angle']) if raw and sid=='q-18021' else sine6(p['angle'])),
  f'\\cdot {number(v0)}\\cdot {number(u0)}\\cdot':f'\\cdot {number(v)}\\cdot {number(u)}\\cdot',
  f'= {number(u0*v0/2)}':f'= {number(u*v/2)}',
  f'={number(u0*v0/2)}\\cdot':f'={number(u*v/2)}\\cdot',
  '≈'+old:'≈'+new,
 }
 # Source 93.5 includes the ordinary ellipsis after the six-place sine; fixed.
 text=q[':question/worked-solution']; slots={}
 for i,(oldpart,newpart) in enumerate(sorted(replacements.items(),key=lambda x:-len(x[0]))):
  key=f'@@COMPONENT{i}@@';text=text.replace(oldpart,key);slots[key]=newpart
 for key,value in slots.items():text=text.replace(key,value)
 return text


def authored_solution(t,p):
 vertex=t['vertex'];pair='bc' if vertex=='A' else 'ac';second='b' if vertex=='A' else 'a';edge='AC' if vertex=='A' else 'BC'
 prefix=''
 if 'given_angles' in p:
  a,b=p['given_angles']
  prefix=f'The angles of a triangle sum to $180^{{\\circ}}$. Thus the included angle is\n\n$$\nm∠B=180^{{\\circ}}-{a}^{{\\circ}}-{b}^{{\\circ}}={p["angle"]}^{{\\circ}}.\n$$\n\n'
 return prefix + f'''The formula for the area of the triangle is 

$$
A=\\frac{{1}}{{2}}{pair}\\operatorname{{sin}}⁡{vertex},
$$

where $∠{vertex}$ is between the sides of lengths ${second}$ and $c.$ 

Here, we have

$$
\\begin{{aligned}}c & =AB={p['u']}, \\\\ {second} & ={edge}={p['v']}, \\\\ m∠{vertex} & ={{{p['angle']}}}^{{∘}}.\\end{{aligned}}
$$

Since 

$$
\\operatorname{{sin}}⁡{{{p['angle']}}}^{{∘}}={sine6(p['angle'])},
$$

rounded to six decimal places,  we calculate the area as follows:
 

$$
\\begin{{aligned}}A & =\\frac{{1}}{{2}}\\cdot {p['v']}\\cdot {p['u']}\\cdot \\operatorname{{sin}}⁡{{{p['angle']}}}^{{∘}} \\\\  & ={number(rat(p['u'])*rat(p['v'])/2)}\\cdot ({sine6(p['angle'])}) \\\\  & ≈{rounded(area(p),t['digits'])},\\end{{aligned}}
$$

rounded to two decimal places.'''


def render_plot(p,t):
 """Actual equal-scale geometry, Matplotlib150DPI; atomic concurrent cache."""
 spec=dict(parameters=p,vertex=t['vertex'],unit=('ft' if t.get('unit') else ''),renderer=matplotlib.__version__,version=VERSION)
 key=digest(spec); folder=ROOT/'plots';folder.mkdir(exist_ok=True)
 dest=folder/(key+'.png');side=dest.with_suffix('.json')
 with PLOT_LOCK:
  if dest.exists() and side.exists():return str(dest),json.loads(side.read_text())
  u,v=float(rat(p['u'])),float(rat(p['v'])); theta=math.radians(p['angle']);phi=math.radians(15)
  points=[(0.,0.),(u*math.cos(phi),u*math.sin(phi)),(v*math.cos(phi+theta),v*math.sin(phi+theta))]
  labels=[t['vertex'], 'B' if t['vertex']=='A' else 'A','C'];centroid=tuple(sum(z[i] for z in points)/3 for i in (0,1))
  span=max(u,v);pad=.15*span;radius=.18*min(u,v)
  fig,ax=plt.subplots(figsize=(6,4),dpi=150);ax.set_aspect('equal');ax.axis('off')
  ax.add_patch(Polygon(points,closed=True,facecolor='none',edgecolor='black',linewidth=1.7))
  ax.add_patch(Wedge(points[0],radius,15,15+p['angle'],facecolor='#80c6ae',edgecolor='black',linewidth=.6))
  texts=[];text_data=[]
  def label(x,y,s):
   texts.append(ax.text(x,y,s,fontsize=13,ha='center',va='center',bbox={'facecolor':'white','edgecolor':'none','pad':.4}));text_data.append([x,y,s])
  for i,(x,y) in enumerate(points):
   dx,dy=x-centroid[0],y-centroid[1];norm=math.hypot(dx,dy)
   label(x+pad*.5*dx/norm,y+pad*.5*dy/norm,labels[i])
  for j,length in ((1,p['u']),(2,p['v'])):
   a,b=points[0],points[j];x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
   nx,ny=-(b[1]-a[1]),b[0]-a[0]
   if nx*(centroid[0]-x)+ny*(centroid[1]-y)>0:nx,ny=-nx,-ny
   norm=math.hypot(nx,ny)
   label(x+pad*.7*nx/norm,y+pad*.7*ny/norm,length+(' ft' if t.get('unit') else ''))
  mid=phi+theta/2
  if 'given_angles' not in p:
   if p['angle']<35 or max(u,v)/min(u,v)>2.5:
    # Narrow sectors need an exterior callout so the number never erases sides.
    lx=.07*span*math.cos(phi)+.22*span*math.sin(phi)
    ly=.07*span*math.sin(phi)-.22*span*math.cos(phi)
    ax.plot([radius*math.cos(mid),lx],[radius*math.sin(mid),ly],color='#666666',linewidth=.7,linestyle=':')
    label(lx,ly,str(p['angle'])+'°')
   else:label(radius*1.8*math.cos(mid),radius*1.8*math.sin(mid),str(p['angle'])+'°')
  else:
   for j,angle in zip((1,2),p['given_angles']):
    x,y=points[j];dx,dy=centroid[0]-x,centroid[1]-y;norm=math.hypot(dx,dy)
    label(x+pad*1.8*dx/norm,y+pad*1.8*dy/norm,str(angle)+'°')
  allcoords=points+[(x,y) for x,y,_ in text_data]
  ax.set_xlim(min(x for x,y in allcoords)-pad,max(x for x,y in allcoords)+pad)
  ax.set_ylim(min(y for x,y in allcoords)-pad,max(y for x,y in allcoords)+pad)
  fig.subplots_adjust(left=.02,right=.98,bottom=.03,top=.97);fig.canvas.draw()
  renderer=fig.canvas.get_renderer();boxes=[list(tx.get_window_extent(renderer).bounds) for tx in texts]
  width,height=fig.canvas.get_width_height()
  if any(x<0 or y<0 or x+w>width or y+h>height for x,y,w,h in boxes):plt.close(fig);raise ValueError('Rendered label clipped')
  for i,a in enumerate(boxes):
   for b in boxes[i+1:]:
    if min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])>1 and min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])>1:
     plt.close(fig);raise ValueError('Rendered labels overlap')
  fd,temp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=folder);os.close(fd)
  try:fig.savefig(temp,dpi=150);os.replace(temp,dest)
  finally:
   plt.close(fig)
   if os.path.exists(temp):os.unlink(temp)
  metadata={**spec,'dpi':150,'canvas_pixels':[width,height],'vertices':points,'vertex_labels':labels,'labels':text_data,
   'label_bounds_pixels':boxes,'axes_bounds_pixels':list(ax.bbox.bounds),'geometry_bounds':[[min(z[i] for z in points),max(z[i] for z in points)] for i in (0,1)],
   'png_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'python':sys.version.split()[0]}
  # Fresh and cached calls expose the same JSON-native metadata shape.
  metadata=json.loads(json.dumps(metadata))
  fd,temp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=folder)
  with os.fdopen(fd,'w') as f:json.dump(metadata,f,indent=2)
  os.replace(temp,side)
 return str(dest),metadata


def bank_values(p,t,profile):
 exact=area(p);digits=t['digits'];correct=rounded(exact,digits)
 if profile.startswith('raw_'):
  sid=profile[4:];a=ANCHORS[sid];q=BYID[sid];f=q[':question/answer-fields'][0]
  oldcorrect=rounded(area(a),digits)
  values=[]
  for option in f[':answer-field/choices']:
   raw=option[':answer/value']
   # Correct value is recomputed, even though designation may be absent.
   if sp.Rational(raw)==sp.Rational(oldcorrect):values.append(correct)
   else:values.append(rounded(sp.Rational(correct)*sp.Rational(raw)/sp.Rational(oldcorrect),digits))
 elif profile=='blank':values=[correct]
 elif profile=='method_sine':
  product=rat(p['u'])*rat(p['v']); sine=sp.sin(sp.pi*p['angle']/180)
  values=[correct,rounded(product*sine,digits),rounded(product/2,digits),
   rounded(product*abs(sp.cos(sp.pi*p['angle']/180))/2,digits),rounded(product*sine**2/2,digits)]
 else:raise ValueError('Unknown profile')
 if len(values)!=len(set(values)) or any(sp.Rational(v)<=0 for v in values):raise ValueError('Whole bank invalid/collision')
 return values,correct


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 if profile and profile not in PROFILES:raise ValueError('Unknown bank profile')
 raw=bool(profile and profile.startswith('raw_'))
 sid=profile[4:] if raw else None
 if raw:
  inferred=SOURCE_TEMPLATE[sid]
  if template is not None and template!=inferred:raise ValueError('Profile/template mismatch')
  template=inferred
  if level!='easy':raise ValueError('Observed source scope is easy; unrated raw record omits difficulty')
 requested_kind=field_type
 if profile=='method_sine':
  if field_type not in (None,'radio'):raise ValueError('Profile field mismatch')
  requested_kind='radio'
 elif profile=='blank':
  if field_type not in (None,'blank'):raise ValueError('Profile field mismatch')
  requested_kind='blank'
 choices=[k for k,t in TEMPLATES.items() if t.get('level','easy')==level and (requested_kind is None or t['kind']==requested_kind)]
 if template is None:
  if not choices:raise ValueError('Unsupported field type')
  template=rng.choice(choices)
 if template not in choices:raise ValueError('Template outside difficulty/field scope')
 t={**TEMPLATES[template],'unit':template=='blank_A_tenth_ft'}
 profile=profile or ('blank' if t['kind']=='blank' else 'method_sine')
 if (t['kind']=='blank')!=(profile=='blank' or (raw and len(BYID[sid][':question/answer-fields'][0][':answer-field/choices'])==1)):
  raise ValueError('Profile field mismatch')
 # Choose whole family/bank first, then parameters. Explicit invalid values fail.
 for attempt in range(300):
  if parameters is not None:p=normalize(parameters,level,raw)
  elif raw:p=normalize(ANCHORS[sid],level,raw)
  elif level=='easy':p=normalize(dict(u=str(rng.randint(2,60)),v=str(rng.randint(2,60)),angle=rng.randint(15,150)),level)
  elif level=='moderate':
   p=normalize(dict(u=number(sp.Rational(rng.choice([n for n in range(21,300) if n%10]),10)),v=number(sp.Rational(rng.choice([n for n in range(21,300) if n%10]),10)),angle=rng.randint(15,150)),level)
  else:
   a=rng.randint(25,80);theta=180-2*a
   side=number(sp.Rational(rng.choice([n for n in range(201,3000) if n%10]),100))
   p=normalize(dict(u=side,v=side,angle=theta,given_angles=[a,a]),level)
  try:
   values,correct=bank_values(p,t,profile)
   source_id=sid or (t['sources'][0] if t['sources'] else None)
   source_q=BYID[source_id] if source_id else None
   at_anchor=raw and p==normalize(ANCHORS[sid],level,True)
   if at_anchor:
    imagepath=re.search(r'!\[\]\((.*?)\)',source_q[':question/problem']).group(1);plotmeta={'original_asset':imagepath,'sha256':hashlib.sha256((Path('/media/jake/SSD/EDB/math')/imagepath).read_bytes()).hexdigest()}
   else:imagepath,plotmeta=render_plot(p,t)
   if source_q:
    prompt=re.sub(r'!\[\]\(.*?\)',lambda _:f'![]({imagepath})',source_q[':question/problem'])
    solution=source_solution(source_id,p,raw)
    if solution is None and not raw:solution=authored_solution(t,p)
    if not raw and template=='blank_B_tenth_above':solution=solution.replace('lengths $a$ and $b.$','lengths $a$ and $c.$')
   else:
    prompt=f'![]({imagepath})\n\nFind the area of $△ABC$. Round your answer to two decimal places.'
    solution=authored_solution(t,p)
   q={':question/problem':prompt}
   if solution is not None:q[':question/worked-solution']=solution
   if not raw or ':question/difficulty' in source_q:q[':question/difficulty']=':question.difficulty/'+level
   identity=digest(dict(version=VERSION,level=q.get(':question/difficulty'),prompt=prompt,solution=solution,bank=sorted(values),kind=t['kind']))
   fieldid=ident([identity,'field']); key='selection' if t['kind']=='radio' else 'field-1'
   answers=[{':answer/id':ident([identity,fieldid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
   f={':answer-field/id':fieldid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+t['kind'],':answer-field/choices':answers}
   if not raw or ':answer-field/correct' in source_q[':question/answer-fields'][0]:
    f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
   rng.shuffle(answers);q[':question/id']=ident(identity);q[':question/answer-fields']=[f]
   return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
    'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':profile,'parameters':p,
     'source':{k:v for k,v in SOURCE.items() if k!='record'},'source_ids':t['sources'],'eligible_for_learning':not raw,
     'evidence_only':raw,'authored_level':level!='easy' or (source_q is not None and ':question/difficulty' not in source_q),
     'difficulty_basis':('authored_missing_level' if level!='easy' else 'inferred_unrated' if source_q is not None and ':question/difficulty' not in source_q else 'observed_easy'),'math_fingerprint':digest({**canonical(p),'digits':t['digits']}),
     'content_fingerprint':identity,'recipes':PROFILES[profile]['operations'],'plot':plotmeta,
     'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}
  except ValueError:
   if parameters is not None or raw:raise
 if parameters is None:raise ValueError('No eligible instance after bounded complete-bank attempts')

# EASY: observed integer sides, directly supplied included angle, tenth or
# hundredth rounding; five eligible source-shaped families sampled uniformly.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE authored: same formula/stages, two noninteger one-decimal side lengths,
# one supplied integer included angle. Both decimals are required, no progression.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD authored: included angle deduced from the other two integer interior
# angles, equal hundredth side lengths (isosceles); same direct area method, no inverse problem.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$\n'
 return s+'\n'+q.get(':question/worked-solution','[Worked solution absent in raw evidence]')
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
