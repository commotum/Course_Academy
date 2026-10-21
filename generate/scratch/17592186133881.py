#!/usr/bin/env python3
"""Visual curl, conservative affine-field variants; see sibling extraction.

Positive global scaling and statement/choice order are not variant slots.
Difficulty follows observed visual family and response layout, never arithmetic.
Source diagrams have no numeric axes: replay retains original bytes, not guessed
coefficients. Proposed exact affine realizations are separately labelled below.
"""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-curl-matplotlib')
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
P=Path(__file__).with_suffix('');VERSION='visual-curl-affine-v1'
KP_ID=17592186133881;KP_UUID='d42243ea-58fc-53f6-a0b6-f995bf1d697c';TITLE='Interpreting the Curl of a Vector Field'
SOURCE=json.loads((P/'source.json').read_text());PROVENANCE={k:SOURCE[k] for k in ('basis','lineage','database')}
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y=sp.symbols('x y',real=True)
# Visual realization (a,b,c,d,u,v) of (ax+by+u,cx+dy+v,0).
# No exact coefficient is claimed to have been recovered from unscaled sources.
REALIZATIONS={
 'q-105092':(0,0,0,0,1,0),'q-105667':(0,0,0,0,1,-1),'q-105671':(0,0,0,0,0,-1),
 'q-131366':(0,0,0,-1,0,0),'q-105693':(-1,0,0,0,0,0),'q-105700':(1,0,0,1,0,0),
 'q-105669':(0,-1,1,0,0,0),'q-105695':(0,1,-1,0,0,0),'q-131361':(0,1,-1,0,0,0),
 'q-105664':(0,-1,1,0,0,0),'q-105692':(1,-1,1,1,0,0),'q-105694':(1,1,-1,1,0,0),
 'q-131363':(1,-1,1,1,0,0),'q-105103':(0,1,-1,0,0,0)}
FAMILIES={sid:('uniform' if sid in ('q-105092','q-105667','q-105671') else 'gradient' if sid in ('q-131366','q-105693','q-105700') else 'spiral' if sid in ('q-105692','q-105694','q-131363') else 'rotation') for sid in SOURCES}
SUPPORTED=('moderate','hard')

def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def canonical_key(params):
 # Exact field modulo a positive overall scale. Includes non-cosmetic direction,
 # anisotropy and expansion/rotation ratio; excludes seed and answer layout.
 vals=[sp.Rational(v) for v in params];scale=next(abs(v) for v in vals if v)
 return ','.join(str(v/scale) for v in vals)
def truth(sid,curl):
 q=SOURCES[sid];lines=[line for line in q[':question/problem'].splitlines() if re.match(r'(?:- \*\*)?(?:I|II|III|IV)\.',line)]
 assert len(lines)==4
 out=[]
 for line in lines:
  if 'irrotational' in line:out.append((curl!=0) if 'not irrotational' in line else (curl==0))
  elif 'positive' in line:out.append(curl>0)
  elif 'negative' in line:out.append(curl<0)
  elif r'\ne' in line:out.append(curl!=0)
  else:out.append(curl==0)
 return out

def subset_text(flags):
 labels=[k for k,v in zip(('I','II','III','IV'),flags) if v]
 return ' and '.join(labels)+' only'
def parameters(sid,rng):
 family=FAMILIES[sid];a,b,c,d,u,v=REALIZATIONS[sid]
 if family=='uniform':
  # Fixed qualitative direction, variable slope; axial directions have one
  # substantive variant only and cannot multiply by arrow length.
  if u and v:return (0,0,0,0,rng.randint(1,4),-rng.randint(1,4))
  return REALIZATIONS[sid]
 if family=='gradient':
  # Radial anisotropy changes relative component growth. Axial examples
  # retain their sole observed axis and are finite, rather than fake variants.
  if a and d:return (rng.randint(1,4),0,0,rng.randint(1,4),0,0)
  return REALIZATIONS[sid]
 if family=='rotation':return (0,b*rng.randint(1,4),c*rng.randint(1,4),0,0,0)
 # Expansion versus angular velocity: all eigenvalues have positive real part;
 # rotation direction remains the observed profile sign.
 k=rng.randint(1,4);h=rng.randint(1,4)
 return (k,b*h,c*h,k,0,0)

def render_plots(params,output_dir):
 output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
 key=canonical_key(params);slug=hashlib.sha256(json.dumps([list(params),'scale3']).encode()).hexdigest();path=output_dir/(slug+'.png');data=output_dir/(slug+'.json')
 if not path.exists():
  a,b,c,d,u,v=map(float,params);grid=np.linspace(-3,3,13);X,Y=np.meshgrid(grid,grid);U=a*X+b*Y+u;V=c*X+d*Y+v
  # One global normalization retains relative arrow magnitude. Never normalize
  # per arrow: that would change the visual evidence for local rotation.
  factor=3*max(1,float(np.max(np.hypot(U,V))))
  fig,ax=plt.subplots(figsize=(5,5));ax.quiver(X,Y,U,V,color='#333333',angles='xy',scale_units='xy',scale=factor,width=.0036)
  ax.axhline(0,color='black',lw=.7);ax.axvline(0,color='black',lw=.7)
  ax.annotate('',xy=(3.5,0),xytext=(3.2,0),arrowprops={'arrowstyle':'->','lw':.7});ax.annotate('',xy=(0,3.5),xytext=(0,3.2),arrowprops={'arrowstyle':'->','lw':.7})
  ax.text(3.45,-.18,'x');ax.text(.12,3.4,'y');ax.set(xlim=(-3.6,3.6),ylim=(-3.6,3.6),aspect='equal');ax.set_xticks([]);ax.set_yticks([])
  for spine in ax.spines.values():spine.set_visible(False)
  fig.tight_layout();fig.savefig(path,dpi=130,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
  data.write_text(json.dumps({'parameters':list(params),'canonical_field':key,'grid':grid.tolist(),'U':U.tolist(),'V':V.tolist(),'scale':factor,'renderer':'Matplotlib','normalization':'single global factor','role':'prompt'},indent=2)+'\n')
 return {'prompt':str(path),'data':str(data),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def fields(sid,flags,identity):
 q=SOURCES[sid];result=[]
 for old in q[':question/answer-fields']:
  key=old[':answer-field/key'];typ=old[':answer-field/type'][':db/ident'];fid=uid(identity+'/field/'+key)
  values=[a[':answer/value'] for a in old[':answer-field/choices']]
  correct=subset_text(flags) if typ.endswith('/radio') else str(flags[('I','II','III','IV').index(key)]).lower()
  assert correct in values
  choices=[{':answer/id':uid(fid+'/answer/'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
  result.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/answer/'+correct)]})
 return result

def solution(sid,curl):
 # Preserve paddlewheel -> zero/nonzero -> irrotational -> right hand ->
 # per-statement conclusions. Source q-105664 clockwise typo corrected here.
 q=SOURCES[sid];flags=truth(sid,curl)
 intro='Recall that $\\text{curl}\\,F$ denotes the curl of the vector field $F.$\n\nTo understand intuitively whether a vector field has curl at a point $P$, imagine that $F$ represents the velocity field of flowing water. Place a paddlewheel at $P$ with its axis in the $z$-direction. If it rotates, the field has nonzero curl; if it does not, the field has zero curl.\n\n'
 if curl==0:
  action='The arrows produce no local paddlewheel rotation. Thus $\\text{curl}\\,F=0$ throughout space. The field is irrotational, and its zero curl points in neither the positive nor the negative $z$-direction.'
 else:
  sense='counterclockwise' if curl>0 else 'clockwise';direction='positive' if curl>0 else 'negative';screen='out of' if curl>0 else 'into'
  action=f'The arrows turn a paddlewheel {sense}. Thus $\\text{{curl}}\\,F\\ne 0$ throughout space, so $F$ is not irrotational. Curl measures local rotation, even when the arrows also spread outward. Wrap the fingers of your right hand in the {sense} direction: your thumb points {screen} the screen, in the {direction} $z$-direction.'
 conclusions='\n\nWith that in mind, check each statement:\n\n'+'\n'.join(f'- Statement {k} is {str(v).lower()}.' for k,v in zip(('I','II','III','IV'),flags))
 return intro+action+conclusions+'\n\nTherefore, the correct answer is "'+subset_text(flags)+'."'

def generate(level,seed=0,template=None,params=None,replay=False,output_dir=None):
 if level not in SUPPORTED:raise ValueError('Easy unsupported: no rated source layout or calibrated family; no synthetic downgrade.')
 rng=random.Random(seed);candidates=[s for s,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+level]
 sid=template or rng.choice(candidates);assert sid in candidates
 params=tuple(params if params is not None else REALIZATIONS[sid] if replay else parameters(sid,rng));a,b,c,d,u,v=params;curl=sp.diff(c*x+d*y+v,x)-sp.diff(a*x+b*y+u,y)
 assert sp.sign(curl)==sp.sign(REALIZATIONS[sid][2]-REALIZATIONS[sid][1])
 flags=truth(sid,curl);identity=VERSION+'/'+sid+'/'+canonical_key(params)
 prompt=SOURCES[sid][':question/problem'];assets=[]
 if not replay:
  asset=render_plots(params,output_dir or P/'assets');assets=[asset];prompt=re.sub(r'!\[.*?\]\(.*?\)',f'![]({asset["prompt"]})',prompt,count=1)
 question={':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':SOURCES[sid][':question/worked-solution'] if replay else solution(sid,curl),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields(sid,flags,identity)}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':sid,'bank_profile':'source-bank:'+sid,'parameters':list(params),'canonical_field':canonical_key(params),'curl':str(curl),'domain':'R^3; F_z=0 and independent of z','source_basis':PROVENANCE['basis'],'source_id':sid,'parameter_evidence':'exact proposed affine realization; source replay retains unscaled original diagram','replay':replay,'assets':assets,'dependencies':{'sympy':sp.__version__,'matplotlib':matplotlib.__version__,'numpy':np.__version__}}}

def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n```json\n'+json.dumps(q[':question/answer-fields'],indent=2)+'\n```'

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');args=p.parse_args()
 if args.difficulty not in SUPPORTED:p.error('Unsupported difficulty '+args.difficulty)
 if args.count<1:p.error('count must be positive')
 records=[];used=set()
 for i in range(512):
  if len(records)==args.count:break
  r=generate(args.difficulty,args.seed+i,template=args.template);key=r['generation']['canonical_field']
  if key in used:continue
  used.add(key);records.append(r)
 if len(records)<args.count:p.error('Bounded 512 attempts exhausted genuine normalized affine variants; requested '+str(args.count)+', produced '+str(len(records)))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
