#!/usr/bin/env python3
"""Concave quadrilateral area practice; self-contained seeded package.
Geometry, area relationship and progression adapted from 17592186105906.py;
source banks are evidence-only replay, authored banks use complete error profiles.
"""
import argparse, copy, hashlib, json, math, os, random, re, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-area-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
from math_format import normalize_prose, normalize_tex, validate_generated_record
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source_cases.json').read_text())
KP=DATA['knowledge_point']; NS=uuid.UUID(KP['id']); VERSION='3.0.0'
LEVELS=('easy','moderate','hard')
# Every combination is one complete authored four-error profile, chosen before values.
ERRORS=('outer','given','add','omit_half','half_result','half_given','twice_given')
PROFILES=(('outer','given','add','omit_half'),
 ('outer','given','add','half_result'),
 ('given','omit_half','half_given','twice_given'),
 ('outer','half_result','half_given','twice_given'),
 ('add','omit_half','half_result','twice_given'),
 ('outer','double_outer','half_given','twice_given'))
HARD_PROFILES=PROFILES+(('given','omit_sine','half_given','twice_given'),
 ('outer','omit_sine','half_result','twice_given'))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def n(x):return str(int(x)) if float(x).is_integer() else format(x,'.8g')
def rounded(x):return math.floor(x+.5)
def labels(p):
 s=p.get('label_shift',0);return ['ABCD'[(i+s)%4] for i in range(4)]
def names(p):
 a,b,c,d=labels(p);return a+b+c+d,a+b+d,b+c+d,a+b,a+d,b+a+d

def vertices(p):
 a,b,t=p['a'],p['b'],math.radians(p['angle']);T=a*b*math.sin(t)/2
 A=(0.,0.);B=(a,0.);D=(b*math.cos(t),b*math.sin(t))
 C=tuple(p['quadrilateral']/T*(B[i]+D[i])/2 for i in (0,1))
 rot=math.radians(p.get('orientation',0));ct,st=math.cos(rot),math.sin(rot)
 return {k:(ct*x-st*y,st*x+ct*y) for k,(x,y) in zip(labels(p),[A,B,C,D])}

def diagram(p,level,output):
 output=Path(output);output.mkdir(parents=True,exist_ok=True)
 filename='area-'+digest({'p':p,'level':level,'renderer':VERSION})[:24]+'.png';path=output/filename
 if path.exists():return filename
 v=vertices(p);la=labels(p);A,B,C,D=[v[k] for k in la];scale=max(p['a'],p['b'])
 fig,ax=plt.subplots(figsize=(5.2,3.8),dpi=150);ax.set_aspect('equal');ax.axis('off')
 ax.add_patch(Polygon([A,B,C,D],facecolor='#e7f1fa',edgecolor='#172b3a',lw=1.8))
 ax.plot(*zip(B,D),color='#172b3a',lw=1.2,ls=(0,(5,4)))
 center=tuple((A[i]+B[i]+D[i])/3 for i in (0,1))
 for k,(x,y) in v.items():
  dx,dy=x-center[0],y-center[1]
  if k==la[2]:dx,dy=(B[0]+D[0])/2-x,(B[1]+D[1])/2-y
  length=math.hypot(dx,dy);offset=.055*scale
  ax.text(x+dx/length*offset,y+dy/length*offset,k,fontsize=14,fontstyle='italic',ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=.35))
 for pt,val in [(B,p['a']),(D,p['b'])]:
  x,y=(A[0]+pt[0])/2,(A[1]+pt[1])/2;dx,dy=pt[0]-A[0],pt[1]-A[1];length=math.hypot(dx,dy);nx,ny=dy/length,-dx/length
  if nx*(x-center[0])+ny*(y-center[1])<0:nx,ny=-nx,-ny
  ax.text(x+.13*scale*nx,y+.13*scale*ny,n(val)+' '+p['unit'],ha='center',va='center',fontsize=12)
 r=.09*min(p['a'],p['b']);rot=math.radians(p.get('orientation',0))
 if p['angle']==90:
  e=(math.cos(rot)*r,math.sin(rot)*r);f=(-math.sin(rot)*r,math.cos(rot)*r)
  pts=[(A[0]+e[0],A[1]+e[1]),(A[0]+e[0]+f[0],A[1]+e[1]+f[1]),(A[0]+f[0],A[1]+f[1])];ax.plot(*zip(*pts),color='#172b3a',lw=1)
 else:
  start=p.get('orientation',0);ax.add_patch(Arc(A,2*r,2*r,theta1=start,theta2=start+p['angle'],color='#a96b00',lw=1.5))
  mid=rot+math.radians(p['angle']/2)
  # Exterior callout keeps the angle and notch labels separate even for small notches.
  pos=(A[0]-.19*scale*math.cos(mid),A[1]-.19*scale*math.sin(mid))
  ax.annotate(str(p['angle'])+'°',xy=(A[0]+r*math.cos(mid),A[1]+r*math.sin(mid)),xytext=pos,ha='center',va='center',fontsize=11,arrowprops=dict(arrowstyle='-',linestyle=':',color='#777',linewidth=.7))
 xs,ys=zip(*v.values());ax.set_xlim(min(xs)-.3*scale,max(xs)+.3*scale);ax.set_ylim(min(ys)-.3*scale,max(ys)+.3*scale)
 fig.tight_layout(pad=.3);fig.savefig(path,facecolor='white');plt.close(fig);return filename

def derivation(p,level):
 poly,outer,target,s1,s2,ang=names(p);Q=p['quadrilateral'];T=p['a']*p['b']*math.sin(math.radians(p['angle']))/2
 result=T-Q
 return dict(polygon=poly,outer_name=outer,target=target,sides=[s1,s2],angle_name=ang,outer=T,given=Q,unrounded=result,key=rounded(result))

def error_values(p,d):
 T,Q=d['outer'],d['given'];r=T-Q
 return {'outer':T,'given':Q,'add':T+Q,'omit_half':2*T-Q,'half_result':r/2,'half_given':T-Q/2,'twice_given':T-2*Q,'omit_sine':p['a']*p['b']/2-Q,'double_outer':2*T}

def bank(p,d,level,profile):
 raw=error_values(p,d);values=[d['key']]+[rounded(raw[e]) for e in profile]
 # Rounding is incidental: disallow adjacent integers and crowded rounded banks.
 spacing=2
 if min(values)<=0 or min(abs(x-y) for i,x in enumerate(values) for y in values[i+1:])<spacing:raise ValueError('colliding or crowded error profile')
 return values

def solution(p,level,d):
 poly,outer,target=d['polygon'],d['outer_name'],d['target'];s1,s2=d['sides'];a,b=p['a'],p['b'];Q=d['given'];u=p['unit'];unit=r'\,\text{'+u+r'}^{2}'
 factor='' if p['angle']==90 else r'\cdot\sin'+str(p['angle'])+r'^\circ'
 formula=r'\frac12\cdot '+s1+r'\cdot '+s2+('' if p['angle']==90 else r'\cdot\sin\angle '+d['angle_name'])
 final=('=' if p['angle']==90 else r'\approx')+(n(d['outer']) if p['angle']==90 else f'{d["outer"]:.6f}')+unit
 text=(f'First calculate the area of the enclosing triangle ${outer}$. '+('The given sides are perpendicular.' if p['angle']==90 else 'Use the two given sides and their included angle, with the calculator in degree mode.')+'\n\n$$\n'+r'\begin{aligned}'+f'A_{{{outer}}}&='+formula+r'\\'+'&='+r'\frac12\cdot '+n(a)+r'\cdot '+n(b)+factor+r'\\'+'&'+final+r'.\end{aligned}'+'\n$$\n\n'+f'The enclosing triangle consists of the quadrilateral ${poly}$ and the missing triangle ${target}$. ')
 expr=(n(d['outer']) if p['angle']==90 else n(a*b/2)+r'\sin'+str(p['angle'])+r'^\circ')+'-'+n(Q)
 text+='Subtract the quadrilateral area:\n\n$$\n'+r'\begin{aligned}'+f'A_{{{target}}}&=A_{{{outer}}}-A_{{{poly}}}'+r'\\'+'&='+expr+r'\\'+r'&\approx'+f'{d["unrounded"]:.6f}'+unit+r'.\end{aligned}'+'\n$$'
 text+='\n\nKeep full precision until this subtraction is complete. Rounded to the nearest integer, the area is $'+n(d['key'])+unit+'$.'
 return text

def build(level,p,seed=0,kind=None,profile=None,output=None,source=None):
 p=dict(p);p.setdefault('orientation',0);p.setdefault('label_shift',0)
 if not 0<p['angle']<180 or min(p['a'],p['b'])<=0:raise ValueError('invalid triangle')
 d=derivation(p,level)
 if not 0<d['given']<d['outer'] or d['key']<=0:raise ValueError('invalid area relationship')
 kind=kind or 'radio';profile=tuple(profile or HARD_PROFILES[0]);rng=random.Random(seed)
 u=p['unit'];unit=r'\,\text{'+u+r'}^{2}';poly,outer,target=d['polygon'],d['outer_name'],d['target']
 output=output or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not output:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
 # Reject infeasible error banks before spending time rendering a diagram.
 values=bank(p,d,level,profile) if kind=='radio' and source is None else [d['key']]
 image=diagram(p,level,output)
 prompt=f'![Concave quadrilateral {poly} with measurements]({image})\n\nThe area of the quadrilateral ${poly}$ is ${n(d["given"])}{unit}$. '
 s1,s2=d['sides'];prompt+=f'The sides ${s1}={n(p["a"])}\\,\\text{{{u}}}$ and ${s2}={n(p["b"])}\\,\\text{{{u}}}$ meet at '+('a right angle. ' if p['angle']==90 else f'${p["angle"]}^\\circ$. ')
 if kind=='blank':prompt+=f'The area of $\\triangle {target}$, rounded to the **nearest integer**, is {{{{field-1}}}} $'+r'\text{'+u+r'}^{2}$.'
 else:prompt+=f'What is the area of $\\triangle {target}$, rounded to the **nearest integer**?'
 prompt+='\n\nYou may use a scientific calculator.'
 values=[normalize_tex(n(v)+(unit if kind=='radio' else '')) for v in values]
 sol=solution(p,level,d);key=values[0]
 if source is not None:
  # Full observed bank replay, never sampled as an authored misconception profile.
  sq=source['source'];sf=sq[':question/answer-fields'][0]
  values=[normalize_tex(x[':answer/value']) for x in sf[':answer-field/choices']];key=normalize_tex(sf[':answer-field/correct'][':answer/value'])
  prompt=normalize_prose(sq[':question/problem']);sol=re.sub(r'\\text\{\s*m\}',lambda _:r'\text{mm}',normalize_prose(sq[':question/worked-solution'])) if sq[':question/math-academy-id']=='q-285754' else normalize_prose(sq[':question/worked-solution'])
 prompt=normalize_prose(prompt);sol=normalize_prose(sol)
 qid=str(uuid.uuid5(NS,digest(dict(version=VERSION,level=level,problem=prompt,solution=sol,values=sorted(values),key=key))))
 fid=str(uuid.uuid5(uuid.UUID(qid),'field'));fieldkey='selection' if kind=='radio' else 'field-1'
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=next(x[':answer/id'] for x in answers if x[':answer/value']==key)
 if kind=='radio':rng.shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':fieldkey,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 q[':question/requires-calculator']=True
 record={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,'contract':'triangle-complement-full-calculation-v1','seed':seed,'parameters':p,'template':level+'_'+kind,'band_origin':'authored numerical progression; imported anchors are hard/unclassified','bank_profile':list(profile) if kind=='radio' else [],'source_question_ids':[source['source'][':question/id']] if source else [c['source'][':question/id'] for c in DATA['cases']],'derivation':d,'semantic_instance':digest({'a':p['a'],'b':p['b'],'angle':p['angle'],'given':d['given']})}}
 validate_generated_record(record);return record

def sample(level,rng,output,seed,kind=None):
 # Answer-bearing case and complete bank profile precede numerical details.
 region=rng.choice(['small_notch','large_notch']);angle_case=rng.choice(['acute','obtuse'])
 kind=kind or rng.choice(['radio','blank'])
 profiles=HARD_PROFILES
 profile=rng.choice(profiles)
 if 'twice_given' in profile:region='large_notch'
 for attempt in range(300):
  # The geometry and two-step task stay fixed. Only the half-product becomes
  # less automatic: a small integer, then a half-integer, then a quarter.
  if level=='easy':a,b=rng.choice([2,4]),rng.randint(4,10)
  elif level=='moderate':a,b=rng.choice([5,7,9,11]),rng.choice([5,7,9,11])
  else:a,b=rng.choice([2.5,3.5,4.5,5.5,6.5]),rng.choice([5,7,9])
  if rng.randrange(2):a,b=b,a
  if max(a,b)/min(a,b)>3:continue
  angle=rng.choice([35,42,45,46,52,55,56,63,66,70,75] if angle_case=='acute' else [105,110,115,117,120])
  T=a*b*math.sin(math.radians(angle))/2
  ratio=rng.uniform(.56,.78) if region=='small_notch' else rng.uniform(.23,.44)
  Q=rounded(T*ratio)
  if not 0<Q<T or T-Q<2 or abs((T-Q)%1-.5)<.08:continue
  p=dict(a=a,b=b,angle=angle,quadrilateral=Q,unit=rng.choice(['cm','in']),orientation=rng.choice([0,90,180,270]),label_shift=rng.randrange(4))
  try:r=build(level,p,seed,kind,profile,output)
  except ValueError as e:
   if 'colliding or crowded' in str(e):continue
   raise
  return r
 raise RuntimeError('Unable to construct complete plausible bank')

def generate_batch(level,count,seed,output):
 rng=random.Random(seed);records=[];seen=set()
 kinds=['radio' if i%2==0 else 'blank' for i in range(count)];rng.shuffle(kinds)
 for i in range(count):
  for attempt in range(100):
   r=sample(level,rng,output,rng.getrandbits(64),kinds[i]);sig=r['generation']['semantic_instance']
   if sig not in seen:seen.add(sig);records.append(r);break
  else:raise RuntimeError('semantic batch exhausted')
 # A finite delivered bank must not accidentally make one numerical rank the
 # answer in every question of a visible angle family. Reauthor a complete
 # plausible error profile on the same geometry; do not alter numbers or keys.
 groups={}
 for i,r in enumerate(records):
  if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio'):
   theta=r['generation']['parameters']['angle']
   groups.setdefault('right' if theta==90 else 'acute' if theta<90 else 'obtuse',[]).append(i)
 def rank(r):
  f=r['question'][':question/answer-fields'][0]
  vals=[float(re.match(r'-?\d+(?:\.\d+)?',a[':answer/value'])[0]) for a in f[':answer-field/choices']]
  k=r['generation']['derivation']['key'];return sorted(vals).index(k)
 for indices in groups.values():
  if len(indices)<2:continue
  if len({rank(records[i]) for i in indices})==1:
   oldrank=rank(records[indices[0]]);repaired=False
   candidates=list(HARD_PROFILES);rng.shuffle(candidates)
   for i in reversed(indices):
    r=records[i];p=r['generation']['parameters'];d=derivation(p,level)
    for profile in candidates:
     try:values=bank(p,d,level,profile)
     except ValueError:continue
     if sorted(values).index(d['key'])!=oldrank:
      records[i]=build(level,p,r['generation']['seed'],'radio',profile,output);repaired=True;break
    if repaired:break
   if not repaired:raise RuntimeError('Finite bank lacks rank variation with supported error profiles')
  # Random option ordering may accidentally agree throughout a small batch.
  fields=[records[i]['question'][':question/answer-fields'][0] for i in indices]
  positions=[next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]) for f in fields]
  if len(set(positions))==1:
   choices=fields[-1][':answer-field/choices'];choices.append(choices.pop(0))
 return records

def replay(source_id,output):
 c=next(c for c in DATA['cases'] if source_id in (c['source'][':question/id'],c['source'][':question/math-academy-id']))
 kind=c['source'][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
 return build('hard',c['parameters'],kind=kind,output=output,source=c)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=LEVELS,default='hard');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source');args=ap.parse_args()
 if args.count<0:ap.error('count must be nonnegative')
 out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not out:ap.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
 records=[replay(args.replay_source,out)] if args.replay_source else generate_batch(args.difficulty,args.count,args.seed,out)
 print(json.dumps(records,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
