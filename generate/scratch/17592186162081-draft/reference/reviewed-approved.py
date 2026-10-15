#!/usr/bin/env python3
"""Calculating Line Integrals of Unity. Local draft; no database operations.

Basis 2275. Six public original profiles preserve complete banks and omissions.
Opaque segment banks use explicitly evidence-only homothetic expression masks;
normal practice uses complete positive geometric operation banks. Easy uses all
observed families; moderate/hard use the same diagonal length chain with rational
legs (common denominator 2 / mixed reduced denominators 3 and 4). No parametric
integration, weighted integrands, piecewise paths, or three-dimensional curves.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'unity-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import threading
_RENDER_LOCK=threading.RLock()
KP_ID=17592186162081
KP_UUID='b4ac9e7d-ea92-5cd3-af26-4c902196e80b'
TITLE='Calculating Line Integrals of Unity'
VERSION='unity-geometric-1'
ROOT=Path(__file__).resolve().parent/str(KP_ID)
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
P={
'q-122567':('semicircle',{'r':3}),
'q-122768':('diagonal_plain',{'x1':0,'y1':3,'x2':4,'y2':0}),
'q-122766':('vertical',{'x1':2,'y1':-1,'x2':2,'y2':3}),
'q-122767':('horizontal',{'x1':1,'y1':-2,'x2':5,'y2':-2}),
'q-122769':('diagonal_helper',{'x1':-1,'y1':-1,'x2':3,'y2':1}),
'q-122770':('diagonal_helper',{'x1':-3,'y1':1,'x2':3,'y2':-2})}
TEMPLATES=('semicircle','vertical','horizontal','diagonal_plain','diagonal_helper')
NS=uuid.UUID('b4ac9e7d-ea92-5cd3-af26-4c902196e80b')
def dump(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def uid(v):return str(uuid.uuid5(NS,v))
def tex(v):return sp.latex(sp.simplify(v)).replace(' \\sqrt','\\sqrt')
def rat(v):
 if isinstance(v,float):raise ValueError('Exact integers or rational strings required')
 v=sp.Rational(str(v))
 if abs(v)>12:raise ValueError('Coordinate/radius bound is 12')
 return v

def data(template,p):
 if template=='semicircle':
  if set(p)!={'r'}:raise ValueError('radius slot only')
  r=rat(p['r'])
  if r<=0:raise ValueError('positive radius')
  return {'r':r,'L':sp.pi*r}
 if set(p)!={'x1','y1','x2','y2'}:raise ValueError('four exact coordinate slots required')
 d={k:rat(v) for k,v in p.items()};d['a']=abs(d['x2']-d['x1']);d['b']=abs(d['y2']-d['y1']);d['L']=sp.sqrt(d['a']**2+d['b']**2)
 if d['L']==0:raise ValueError('nondegenerate path required')
 if template=='vertical' and (d['a']!=0 or d['b']==0):raise ValueError('vertical geometry')
 if template=='horizontal' and (d['b']!=0 or d['a']==0):raise ValueError('horizontal geometry')
 if template.startswith('diagonal') and (d['a']==0 or d['b']==0):raise ValueError('two nonzero legs required')
 return d

def workload(level,t,d):
 if t=='semicircle':
  if level!='easy' or d['r'].q!=1 or d['r']>10:raise ValueError('normal semicircle easy integer radius 1..10')
  return
 a,b=d['a'],d['b']
 if level=='easy':
  if any(v.q!=1 for k,v in d.items() if k in ('x1','y1','x2','y2')) or max(a,b)>10:raise ValueError('easy integer coordinates, legs <=10')
 elif level=='moderate':
  if not t.startswith('diagonal') or a.q!=2 or b.q!=2 or not(1<=a<=sp.Rational(19,2) and 1<=b<=sp.Rational(19,2)):raise ValueError('moderate: both reduced half-integer legs 3/2..19/2')
 elif level=='hard':
  if not t.startswith('diagonal') or sorted([int(a.q),int(b.q)])!=[3,4] or not(1<=a<=8 and 1<=b<=8):raise ValueError('hard: mixed reduced thirds/quarters legs in [1,8]')
 else:raise ValueError('difficulty')

def bank(t,d,profile):
 L=d['L']
 if profile.startswith('original:'):
  sid=profile.split(':',1)[1];st,anchor=P[sid]
  if st!=t:raise ValueError('profile/template mismatch')
  ad=data(t,anchor)
  if t=='semicircle':
   r=d['r'];return [r*sp.pi,r*sp.pi/2,sp.Integer(1),2*r*sp.pi,sp.Integer(0)],['half circumference','quarter circumference','unity integrand','full circumference','zero']
  # Opaque evidence mask: homothetic source lengths, not an inferred error method.
  scale=sp.simplify(L/ad['L'])
  if not scale.is_Rational or scale<=0:raise ValueError('original evidence masks require positive rational homothety')
  if sp.simplify(d['a']-scale*ad['a'])!=0 or sp.simplify(d['b']-scale*ad['b'])!=0:raise ValueError('source geometric leg ratio required')
  values={
  'q-122768':[5,3,3*sp.sqrt(5),4,4*sp.sqrt(5)],
  'q-122766':[3,2,5,4,6],
  'q-122767':[3,sp.Rational(7,2),2,4,sp.Rational(5,2)],
  'q-122769':[2,2*sp.sqrt(5),4,5,5*sp.sqrt(2)],
  'q-122770':[5,3,3*sp.sqrt(5),5*sp.sqrt(3),3*sp.sqrt(2)]}[sid]
  return [sp.simplify(v*scale) for v in values],['evidence-only homogeneous source-expression mask']*5
 if profile!='geometric':raise ValueError('unknown complete bank profile')
 if t=='semicircle':
  r=d['r'];return [L,2*sp.pi*r,sp.pi*r/2,2*r,sp.pi*r**2],['arc length','full circumference','quarter circumference','diameter','disk area']
 if t in ('horizontal','vertical'):
  lo,hi=sorted([d['y1'],d['y2']] if t=='vertical' else [d['x1'],d['x2']])
  return [L,abs(hi+lo),abs(hi),abs(lo),L**2],['difference','absolute endpoint sum','upper-coordinate magnitude','lower-coordinate magnitude','squared length']
 a,b=d['a'],d['b']
 return [L,a,b,a+b,a*a+b*b],['Pythagorean length','horizontal leg','vertical leg','sum of legs','squared length']

def valid_bank(values,normal=True):
 if normal and any(v.is_real is not True or v<=0 for v in values):raise ValueError('whole bank needs positive real geometric answers')
 for i,v in enumerate(values):
  for w in values[i+1:]:
   if sp.simplify(v-w)==0:raise ValueError('equivalent complete scalar choices')


def plot_recipe(t,d,helper=False):
 if t=='semicircle':
  r=float(d['r']);return {'kind':t,'radius':str(d['r']),'center':[0,0],'theta':[0,math.pi],'direction':'counterclockwise','bounds':[-r-1,r+1,-1,r+1],'helper':False}
 pts=[[str(d['x1']),str(d['y1'])],[str(d['x2']),str(d['y2'])]]
 return {'kind':t,'endpoints':pts,'direction':'first to second','helper':helper,'helper_corner':[str(d['x2']),str(d['y1'])], 'bounds':[min(0,float(d['x1']),float(d['x2']))-1,max(0,float(d['x1']),float(d['x2']))+1,min(0,float(d['y1']),float(d['y2']))-1,max(0,float(d['y1']),float(d['y2']))+1]}

def _render_plot(t,d,helper=False):
 recipe=plot_recipe(t,d,helper);h=hashlib.sha256(dump({'recipe':recipe,'renderer':'matplotlib','version':matplotlib.__version__,'style':9}).encode()).hexdigest();dest=ROOT/'assets'/f'{h}.png';side=dest.with_suffix('.json')
 if dest.exists() and side.exists():return str(dest),recipe
 # Each invocation has independent figure and temporary files; atomic rename.
 fig,ax=plt.subplots(figsize=(4.5,3.8),dpi=120)
 lo,hi,bot,top=recipe['bounds'];ax.set_xlim(lo,hi);ax.set_ylim(bot,top);ax.set_aspect('equal',adjustable='box')
 ax.spines[['top','right']].set_visible(False);ax.spines[['left','bottom']].set_position('zero')
 ax.set_xlabel('$x$',loc='right');ax.set_ylabel('$y$',loc='top',rotation=0)
 ax.annotate('',xy=(hi,0),xytext=(hi-.25,0),arrowprops={'arrowstyle':'->','color':'black','lw':1})
 ax.annotate('',xy=(0,top),xytext=(0,top-.25),arrowprops={'arrowstyle':'->','color':'black','lw':1})
 color='#246fb3'
 if t=='semicircle':
  r=float(d['r']);ang=np.linspace(0,math.pi,241);ax.plot(r*np.cos(ang),r*np.sin(ang),c=color,lw=1.8)
  for u in (.3,1.5,2.5):ax.annotate('',xy=(r*math.cos(u+.12),r*math.sin(u+.12)),xytext=(r*math.cos(u),r*math.sin(u)),arrowprops={'arrowstyle':'->','color':color,'lw':1.5})
  ax.set_xticks([-r,0,r],[f'${tex(-d["r"])}$','0',f'${tex(d["r"])}$']);ax.set_yticks([r],[f'${tex(d["r"])}$']);ax.text(.7*r,.78*r,'$C$',c=color,fontsize=13)
 else:
  x1,y1,x2,y2=[float(d[k]) for k in ('x1','y1','x2','y2')]
  ax.plot([x1,x2],[y1,y2],c=color,lw=1.8,marker='o',ms=4)
  for u in (.22,.42,.62,.82):ax.annotate('',xy=(x1+(u+.045)*(x2-x1),y1+(u+.045)*(y2-y1)),xytext=(x1+u*(x2-x1),y1+u*(y2-y1)),arrowprops={'arrowstyle':'->','color':color,'lw':1.3})
  dx,dy=x2-x1,y2-y1
  offset=(18,0) if dx==0 else (0,18) if dy==0 else (-18,18) if dx*dy>0 else (-18,-18)
  ax.annotate('$C$',((x1+x2)/2,(y1+y2)/2),xytext=offset,textcoords='offset points',ha='center',va='center',color=color,fontsize=13)
  if helper:ax.plot([x1,x2,x2],[y1,y1,y2],c=color,ls='--',lw=1.2)
  # Only distinct coordinate ticks; zero never obscures coordinate reading.
  for axis,keys in ((ax.xaxis,('x1','x2')),(ax.yaxis,('y1','y2'))):
   vals=sorted(set([sp.Integer(0)]+[d[k] for k in keys]));axis.set_ticks([float(v) for v in vals]);axis.set_ticklabels([f'${tex(v)}$' for v in vals])
  # Explicit endpoint labels make fractional positions readable at native size.
  for (x,y),keys,offset in zip(((x1,y1),(x2,y2)),(('x1','y1'),('x2','y2')),((8,-18),(8,8))):
   label='$('+tex(d[keys[0]])+','+tex(d[keys[1]])+')$'
   offset=(-8,-18) if x<=(x1+x2)/2 else (8,8)
   ax.annotate(label,(x,y),xytext=offset,textcoords='offset points',ha='right' if offset[0]<0 else 'left',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':1.5})
 ax.tick_params(labelsize=10);fig.tight_layout(pad=1.2);fig.canvas.draw()
 transform=ax.transData.get_affine().get_matrix().tolist()
 if t=='semicircle':testpoints=[(float(d['r'])*math.cos(u),float(d['r'])*math.sin(u)) for u in (0,.4,1.2,2.1,math.pi)]
 else:testpoints=[(float(d['x1'])+u*float(d['x2']-d['x1']),float(d['y1'])+u*float(d['y2']-d['y1'])) for u in (0,.2,.5,.8,1)]
 curvepixels=[[float(x),456-float(y)] for x,y in ax.transData.transform(testpoints)]
 fd,tmp=tempfile.mkstemp(prefix=h+'-',suffix='.png',dir=dest.parent);os.close(fd)
 try:
  fig.savefig(tmp,dpi=120,facecolor='white');plt.close(fig);os.replace(tmp,dest)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 payload={'recipe':recipe,'renderer':{'name':'matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0]},'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'native_pixels':[540,456],'data_transform':transform,'curve_samples_pixels':curvepixels}
 fd,tmp=tempfile.mkstemp(prefix=h+'-',suffix='.json',dir=dest.parent)
 with os.fdopen(fd,'w') as f:json.dump(payload,f,indent=2)
 os.replace(tmp,side);return str(dest),recipe

def render_plot(t,d,helper=False):
 # Matplotlib mathtext has process-global caches; serialize threads, while
 # per-process calls retain unique atomic files and can run concurrently.
 with _RENDER_LOCK:return _render_plot(t,d,helper)

OPEN='The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,\n\n$$\n'+r'{\int }_{C}\,\text{d}s=L.'+'\n$$\n\n'
def solution(t,d,helper=None,source_id=None):
 L=tex(d['L'])
 if t=='semicircle':
  r=tex(d['r']);return 'The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,\n\n$$\n'+r'\int_C \,\textrm d s = L.'+'\n$$\n\n'+f'In this case, $C$ is a semicircle of radius $r = {r}.$ Its arc length is given by\n\n$$\n'+r'\begin{aligned}L=\pi r='+L+r' .\end{aligned}'+'\n$$\n\nTherefore,\n\n$$\n'+r'\int_C \,\textrm d s = '+L+'.\n$$'
 if t in ('vertical','horizontal'):
  axis='y' if t=='vertical' else 'x';lo,hi=sorted([d[axis+'1'],d[axis+'2']]);low='('+tex(lo)+')' if lo<0 else tex(lo)
  article='a' if t=='vertical' else 'the';return OPEN+f'In this case, the path $C$ is {article} line segment directed along the ${axis}$-axis. Therefore, we have\n\n$$\n'+r'{\int }_{C}\,\text{d}s='+tex(hi)+'-'+low+'='+L+'.\n$$'
 a,b=d['a'],d['b'];aa,bb=tex(b),tex(a)
 intro=f'In this case, the path $C$ is the hypotenuse of a right triangle whose legs have lengths ${aa}$ and ${bb}'
 if t=='diagonal_helper':intro+=':$ \n\n![]('+helper+')\n\nTherefore, we have\n\n'
 else:intro+='.$ Therefore, we have\n\n'
 chain=r'\begin{aligned}L & =\sqrt{{'+aa+r'}^{2}+{'+bb+r'}^{2}} \\  & =\sqrt{'+tex(b*b)+'+'+tex(a*a)+r'} \\  & =\sqrt{'+tex(a*a+b*b)+r'} \\  & ='+L+r'.\end{aligned}'
 return OPEN+intro+'$$\n'+chain+'\n$$\n\nTherefore,\n\n$$\n'+r'{\int }_{C}\,\text{d}s='+L+'.\n$$'

def sample(level,t,rng):
 if t=='semicircle':return {'r':rng.randint(1,10)}
 if level=='easy':
  if t in ('vertical','horizontal'):
   # Endpoint-operation bank needs five positive distinct values.
   lo=rng.choice([-4,-3,-2,1,2]);hi=rng.choice([5,6,7,8]);fixed=rng.randint(-4,4)
   return dict(x1=fixed,y1=lo,x2=fixed,y2=hi) if t=='vertical' else dict(x1=lo,y1=fixed,x2=hi,y2=fixed)
  a,b=rng.sample(range(2,11),2)
 elif level=='moderate':a,b=rng.sample([sp.Rational(n,2) for n in range(3,20,2)],2)
 else:
  a=rng.choice([sp.Rational(n,3) for n in range(4,24) if n%3]);b=rng.choice([sp.Rational(n,4) for n in range(5,32) if n%2]);
  if rng.choice([True,False]):a,b=b,a
 x,y=rng.randint(-2,1),rng.randint(-2,1);sgn=rng.choice([-1,1]);return {k:str(v) for k,v in dict(x1=x,y1=y,x2=x+a,y2=y+sgn*b).items()}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed);profile=profile or 'geometric';raw=profile.startswith('original:');sid=profile.split(':',1)[1] if raw else None
 if raw and sid not in P:raise ValueError('unknown original profile')
 t=template or (P[sid][0] if raw else rng.choice(TEMPLATES if level=='easy' else TEMPLATES[-2:]))
 if t not in TEMPLATES:raise ValueError('template')
 if raw and level!='easy':raise ValueError('original profiles are source easy/unrated only')
 p=parameters if parameters is not None else (P[sid][1] if raw else None)
 for attempt in range(300):
  pp=p if p is not None else sample(level,t,rng)
  try:
   d=data(t,pp)
   if not raw:workload(level,t,d)
   values,recipes=bank(t,d,profile);valid_bank(values,not raw);break
  except ValueError:
   if p is not None:raise
 else:raise ValueError('no eligible whole instance')
 anchor=raw and {k:str(rat(v)) for k,v in pp.items()}=={k:str(rat(v)) for k,v in P[sid][1].items()}
 path,geometry=render_plot(t,d);helper=None
 if t=='diagonal_helper':helper,hg=render_plot(t,d,True)
 if anchor:
  import re
  refs=re.findall(r'!\[.*?\]\((.*?)\)',QUESTIONS[sid][':question/problem']+' '+QUESTIONS[sid].get(':question/worked-solution',''))
  path=refs[0];helper=refs[1] if len(refs)>1 else None
 if t=='semicircle':prompt='![]('+path+')\n\nCalculate $\\displaystyle \\int_{C}ds$, where $C$ is the arc of a semicircle of radius $'+tex(d['r'])+'$ traversed once in the counterclockwise direction, as shown above.'
 else:prompt='![]('+path+')\n\nCalculate ${\\int }_{C}\\,\\text{d}s,$ where $C$ is the line segment shown above.'
 sol=solution(t,d,helper,sid)
 value_tex=[tex(v) for v in values]
 if raw:
  # Source notation mask, computed from exact expressions at all parameters.
  value_tex=[tex(v).replace(' ','').replace(r'\pi','π') if t=='semicircle' else tex(v).replace(' ','') for v in values]
 # Stable content identity includes displayed bank, actual level and presence omissions.
 omitted=raw and sid=='q-122567';body={'prompt':prompt,'solution':None if omitted else sol,'bank':sorted(value_tex),'difficulty':None if omitted else level,'version':VERSION}
 ident=uid(dump(body));fid=uid(ident+'selection')
 answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in value_tex]
 correct_index=next(i for i,v in enumerate(values) if sp.simplify(v-d['L'])==0)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not omitted:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':ident,':question/problem':prompt,':question/answer-fields':[field]}
 if not omitted:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
 # Task equivalence excludes translations, orientation and profile aliases.
 roles=['semicircle',str(d['r'])] if t=='semicircle' else (['axis',str(d['L'])] if t in ('vertical','horizontal') else ['diagonal',*sorted([str(d['a']),str(d['b'])])])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':t,'profile':profile,'parameters':{k:str(rat(v)) for k,v in pp.items()},'source_id':sid,'source':{k:v for k,v in SOURCE.items() if k!='record'},'recipes':recipes,'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':hashlib.sha256(dump(roles).encode()).hexdigest(),'geometry':geometry,'length':str(d['L']),'values':[str(v) for v in values],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}

# Easy: all five observed family masks, integer arithmetic and original radicals.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: one two-leg Pythagorean workload with reduced half-integer legs.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: same stages, mixed reduced thirds/quarters, no new calculus branch.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for a in q[':question/answer-fields'][0][':answer-field/choices']:out+='- $'+a[':answer/value']+'$\n'
 return out+'\n'+q.get(':question/worked-solution','[Original worked solution absent]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
