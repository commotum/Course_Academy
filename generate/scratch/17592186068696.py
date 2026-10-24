#!/usr/bin/env python3
"""Graphical discontinuity recognition; frozen math basis 1356.

Only graph reading is assessed: no limit calculation or symbolic continuity test.
Observed profiles preserve every full bank, legacy field, and attribute omission.
They are parameterized horizontal affine graph/prose/bank recipes, not payload
returns. Normal easy serves list, image-selection and one/two-blank families.
Moderate/hard are explicitly authored graph-reading workloads (see extraction).
The Matplotlib renderer plots traced source branches and independently recorded
open/filled markers. Vertical values are unnumbered in practice source graphs;
the trace preserves pixel geometry, without inventing exact underlying formulas.
Each whole bank is chosen before parameters and rejected on criterion collisions.
No EDB client, registration, transactions, or writes outside this private folder.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186068696-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, os, random, re, sys, tempfile, threading, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path('/tmp')/'kp68696-matplotlib'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import sympy as sp
KP_ID=17592186068696
KP_UUID='31eacf5a-75a5-5b38-8c24-4b1598ecf3a7'
TITLE='Identifying Points of Discontinuity'
VERSION='graph-discontinuity-2-zero-axes'
ROOT=Path(__file__).resolve().parent / str(KP_ID)
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
PLOTS=json.loads((ROOT/'plot-spec.json').read_text())
ASSET_ROOT=Path('/media/jake/SSD/EDB/math')
LOCK=threading.RLock()
BREAKS={'q-48080':[-2,0],'q-48090':[1,2,4],'q-104021':[-2,1,3],
'q-131299':[2],'q-131334':[-1,2],'q-131482':[2],'q-131483':[-1,2],
'q-104020':[0,2],'q-104023':[-2,0],'q-48087':[-2,2],'q-104025':[-1,2],'q-48088':[-3,0]}
SELECT={'q-104040':-3,'q-48074':1,'q-48076':-1,'q-104036':-2,'q-48038':1}
BLANK={q for q in BREAKS if '131' in q}
NS=uuid.UUID(KP_UUID)
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(o):return hashlib.sha256(canonical(o).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(NS,s))
def number(v):
 v=sp.Rational(str(v));return str(v.p) if v.q==1 else str(float(v)).rstrip('0').rstrip('.')
def affine(v,p):return sp.Rational(str(p['scale']))*sp.Rational(str(v))+sp.Rational(str(p['shift']))
def numeric_math_mask(text,p):
 """Coordinate slots are numeric atoms inside complete math components only.
 Sources contain only x coordinates, never coefficients, formulas or units.
 """
 if p['shift']==0 and p['scale']==1:return text
 def edit(m):
  part=m.group(0)
  if '±' in part or r'\pm' in part:
   # A symmetric pair becomes an ordinary complete two-coordinate component.
   n=re.search(r'\d+(?:\.\d+)?',part)
   if n:
    a=number(affine('-'+n.group(),p));b=number(affine(n.group(),p))
    if part.startswith('$'):return f'$x={a}$ and $x={b}$'
    return f'x={a},{b}'
  return re.sub(r'(?<![A-Za-z\d])-?\d+(?:\.\d+)?',lambda t:number(affine(t.group(),p)),part)
 # source math answers are delimiter-free; text/prose math is delimited.
 if '$' not in text and text.startswith('x'):
  return edit(re.match(r'[\s\S]+',text))
 return re.sub(r'\$[^$]*\$',edit,text)
def atomic_json(path,data):
 path=Path(path);path.parent.mkdir(exist_ok=True,parents=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.json.tmp')
 with os.fdopen(fd,'w') as f:json.dump(data,f,indent=2);f.write('\n')
 os.replace(tmp,path)
def render(spec,p,force=False):
 """Matplotlib only; unique temporary assets, synchronized global pyplot state.
 Sidecars contain the exact plotted geometry and axes transform for readback.
 """
 transformed=copy.deepcopy(spec)
 for c in transformed['curves']:
  for xy in c:xy[0]=float(affine(xy[0],p))
 for m in transformed['markers']:m['x']=float(affine(m['x'],p))
 transformed['breaks']=[float(affine(x,p)) for x in spec['breaks']]
 transformed['vertical_asymptotes']=[float(affine(x,p)) for x in spec.get('vertical_asymptotes',[])]
 lo,hi,bot,top=spec['bounds'];curve_view=[float(affine(lo,p)),float(affine(hi,p)),bot,top]
 # The axes are always the true x=0 and y=0. Extend the viewport rather
 # than moving the origin when a translated graph lies to one side.
 margin=max(.6,.6*p.get('grid',1))
 transformed['curve_view_bounds']=curve_view
 transformed['bounds']=[min(curve_view[0],-margin),max(curve_view[1],margin),min(bot,-.6),max(top,.6)]
 key=digest({'version':VERSION,'geometry':transformed,'grid':p.get('grid',1)})
 path=ROOT/'plots'/f'{key}.png';side=path.with_suffix('.json');path.parent.mkdir(exist_ok=True)
 with LOCK:
  if path.exists() and side.exists() and not force:return str(path)
  width=max(4.7, (transformed['bounds'][1]-transformed['bounds'][0])/p.get('grid',1)*.40)
  fig,ax=plt.subplots(figsize=(width,4),dpi=140);fig.patch.set_facecolor('white')
  ax.set_xlim(*transformed['bounds'][:2]);ax.set_ylim(*transformed['bounds'][2:]);ax.set_facecolor('white')
  for c in transformed['curves']:
   a=np.array(c);ax.plot(a[:,0],a[:,1],color='#e52525',lw=1.5)
  for x in transformed['vertical_asymptotes']:ax.axvline(x,color='#888',ls='--',lw=.8)
  for m in transformed['markers']:
   # Source y uses its raster calibration, authored markers supply exact y.
   y=m.get('y',(spec.get('origin_pixel',[0,0])[1]-m.get('y_pixel',0))/spec.get('pixels_per_x_unit',1))
   ax.plot(m['x'],y,'o',ms=5.5,mec=m.get('color','#e52525'),mfc='white' if m['kind']=='open' else m.get('color','#e52525'),mew=1.2,zorder=5)
  grid=p.get('grid',1);lo,hi,bot,top=transformed['bounds']
  ticks=np.arange(np.ceil(lo/grid)*grid,hi,grid)
  # Source-readable integer coordinate scale for easy; half-unit grid moderate;
  # hard uses unit ticks with midpoint reading. Tick values are part of task.
  ax.set_xticks(ticks);ax.set_yticks([])
  ax.grid(axis='x',color='#dddddd',lw=.6)
  ax.spines[['top','right']].set_visible(False)
  ax.spines['bottom'].set_position(('data',0));ax.spines['left'].set_position(('data',0))
  ax.tick_params(axis='x',labelsize=9,pad=3)
  # Labels follow the positive ends of the actual axes, not the frame.
  ax.annotate('$x$',xy=(hi,0),xytext=(3,-10),textcoords='offset points',ha='left',va='top',annotation_clip=False)
  ax.annotate('$y$',xy=(0,top),xytext=(-8,3),textcoords='offset points',ha='left',va='bottom',annotation_clip=False)
  ax.annotate('',xy=(hi,0),xytext=(hi-.2,0),arrowprops={'arrowstyle':'->','color':'black','lw':.9})
  ax.annotate('',xy=(0,top),xytext=(0,top-.2),arrowprops={'arrowstyle':'->','color':'black','lw':.9})
  fig.tight_layout(pad=.4);fig.canvas.draw()
  fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.png');os.close(fd)
  fig.savefig(tmp);axes={'xlim':list(ax.get_xlim()),'ylim':list(ax.get_ylim()),'ticks':list(map(float,ticks)),'pixel_bounds':list(map(float,ax.get_window_extent().bounds)),'origin_pixel':list(map(float,ax.transData.transform((0,0)))),'horizontal_spine':list(map(float,ax.spines['bottom'].get_transform().transform(ax.spines['bottom'].get_path().vertices).flatten())),'vertical_spine':list(map(float,ax.spines['left'].get_transform().transform(ax.spines['left'].get_path().vertices).flatten())),'label_anchors':{'x':[hi,0],'y':[0,top]}}
  plt.close(fig);os.replace(tmp,path)
  atomic_json(side,{'renderer':'Matplotlib','python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'geometry':transformed,'parameters':p,'axes':axes,'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 return str(path)
def asset(path,p,raw):
 if raw and p['shift']==0 and p['scale']==1:return path
 return render(PLOTS[path],p)
def replace_assets(text,p,raw):return re.sub(r'images/[a-f0-9/]+\.png',lambda m:asset(m.group(),p,raw),text)
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def infer_family(qid):return 'select_graph' if qid in SELECT else ('blank_2' if qid in BLANK and len(BREAKS[qid])==2 else 'blank_1' if qid in BLANK else 'list_breaks')
def authored_spec(xs,level,orientation=1):
 """Three discontinuities plus a continuous corner only in hard.
 Curves use exact elementary geometry; no formulas are asked of learners.
 """
 a,b,c=map(float,xs);left=a-1.4;right=c+1.4
 curves=[[[left,-1.2],[a-0.03,.4]],[[a+.03,.4],[b,.9]],[[b,2.1],[c-.08,3.7]],[[c+.08,-3.7],[c+.45,-.6],[right,.8]]]
 # hole at a, jump at b, asymptote at c. The adjacent hole pieces meet in y.
 # Leave a small marker-sized gap, with the ring supplying the missing point.
 curves[0][-1]=[a-.015,.4];curves[1][0]=[a+.015,.4]
 curves[2]=[[float(t),float(2.1+.42*(1/(c-t)-1/(c-b)))] for t in np.linspace(b,c-.03,150)]
 curves[3]=[[float(t),float(-.55/(t-c)+.25)] for t in np.linspace(c+.03,right,150)]
 markers=[{'x':a,'y':.4,'kind':'open','color':'red'},{'x':a,'y':1.3,'kind':'filled','color':'red'},
 {'x':b,'y':.9,'kind':'open','color':'red'},{'x':b,'y':2.1,'kind':'filled','color':'red'}]
 if level=='hard':
  # A visibly connected corner in the final branch is a distractor, not a break.
  corner=(c+right)/2;join=c+.45;curves[-1]=[[float(t),float(-.55/(t-c)+.25)] for t in np.linspace(c+.03,join,90)]+[[corner,-1.4],[right,.8]]
 for line in curves:
  for v in line:v[1]*=orientation
 for m in markers:m['y']*=orientation
 return {'curves':curves,'markers':markers,'breaks':[a,b,c],'bounds':[left,right,-4,4],'vertical_asymptotes':[c],'origin_pixel':[0,0],'pixels_per_x_unit':1,'authored':True,'orientation':orientation}
def simple_blank_spec(xs):
 # Supplied graph repair is authored because the omitted legacy widget is unavailable.
 a=float(xs[0]);curves=[[[a-2,-1],[a,0]],[[a,1],[a+2,2]]]
 markers=[{'x':a,'y':0,'kind':'open','color':'red'},{'x':a,'y':1,'kind':'filled','color':'red'}]
 if len(xs)==2:
  b=float(xs[1]);curves=[[[a-2,-1],[a,0]],[[a,.8],[b-.01,.8]],[[b+.01,.8],[b+2,1.8]]];markers[1]['y']=.8
  markers.extend([{'x':b,'y':.8,'kind':'open','color':'red'},{'x':b,'y':1.8,'kind':'filled','color':'red'}])
 return {'curves':curves,'markers':markers,'breaks':list(xs),'bounds':[a-2,float(xs[-1])+2,-2,3],'vertical_asymptotes':[]}
def settext(xs):
 xs=sorted(set(map(sp.Rational,xs)));vals=[f'$x={number(x)}$' for x in xs]
 return vals[0]+' only' if len(vals)==1 else ' and '.join(vals)
def complete_set_bank(xs):
 xs=tuple(sorted(map(sp.Rational,xs)));n=len(xs)
 if n==2:
  a,b=xs;c=b+1
  if c in xs:raise ValueError('whole-bank collision')
  bank=[xs,(a,),(b,),(a,c),(b,c)]
 elif n==3:bank=[xs,xs[1:],(xs[0],xs[2]),xs[:2],(xs[1],)]
 else:raise ValueError('list workload must have 2 or 3 breaks')
 if len(set(bank))!=5:raise ValueError('whole-bank collision')
 return bank

def assemble(problem,solution,fields,level,metadata,preserve_difficulty=True):
 # Content identity excludes seed and parameter aliases; full displayed banks included.
 identity={'version':VERSION,'problem':problem,'solution':solution,'level':level if preserve_difficulty else None,
 'fields':[{'key':f['key'],'type':f['type'],'choices':sorted([(a['type'],a['value']) for a in f['choices']]),'correct':next(((a['type'],a['value']) for a in f['choices'] if a.get('original_id',a['value'])==f.get('correct')),None)} for f in fields]}
 key=digest(identity);q={':question/id':uid(key),':question/problem':problem}
 if solution is not None:q[':question/worked-solution']=solution
 if preserve_difficulty:q[':question/difficulty']=':question.difficulty/'+level
 if metadata.pop('fields_present',True):
  owned=[]
  for index,f in enumerate(fields):
   fid=uid(key+':field:'+str(index));choices=[];original={}
   for a in f['choices']:
    aid=uid(fid+':'+canonical((a['type'],a['value'])));original[a.get('original_id',a['value'])]=aid
    choices.append({':answer/id':aid,':answer/type':a['type'],':answer/value':a['value']})
   # Canonical construction then shuffle: no source order influences identity.
   choices.sort(key=lambda a:a[':answer/id']);random.Random(metadata['seed']+index).shuffle(choices)
   ff={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':choices}
   if 'correct' in f:ff[':answer-field/correct']=[':answer/id',original[f['correct']]]
   owned.append(ff)
  q[':question/answer-fields']=owned
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':{k:v for k,v in SOURCE.items() if k!='record'},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__},'content_fingerprint':key,**metadata}}

# EASY: recovered integer coordinate graphical families, source-shaped prose/stages.
def observed(qid,p,seed,raw=False,bank_profile='authored'):
 q=QUESTIONS[qid];family=infer_family(qid)
 problem=replace_assets(numeric_math_mask(q[':question/problem'],p),p,raw)
 solution=replace_assets(numeric_math_mask(q.get(':question/worked-solution',''),p),p,raw)
 fields=[]
 if raw or family=='select_graph' or family.startswith('blank'):
  for f in q.get(':question/answer-fields',[]):
   ff={'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']),'choices':[]}
   for a in f[':answer-field/choices']:
    val=a[':answer/value'];typ=enum(a[':answer/type'])
    if typ==':answer.type/image':val=asset(val,p,raw)
    elif family.startswith('blank'):val=number(affine(val,p))
    else:val=numeric_math_mask(val,p)
    ff['choices'].append({'type':typ,'value':val,'original_id':a[':answer/id']})
   if ':answer-field/correct' in f:ff['correct']=f[':answer-field/correct'][':answer/id']
   fields.append(ff)
 if not raw:
  if family=='list_breaks':
   xs=[affine(x,p) for x in BREAKS[qid]];bank=complete_set_bank(xs)
   fields=[{'key':'selection','type':':answer-field.type/radio','choices':[{'type':':answer.type/text','value':settext(s)} for s in bank],'correct':settext(xs)}]
  elif family.startswith('blank'):
   graph=render(simple_blank_spec(BREAKS[qid]),p)
   # Preserve operative sentences and field layout, normalize only HTML whitespace.
   problem=re.sub(r'\n[ \t]+','\n',problem);problem=re.sub(r'\n{3,}','\n\n',problem)
   problem=f'![]({graph})\n\n'+problem
  elif family=='select_graph' and '![]' not in solution:
   correct=q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
   sentences=solution.split('\n\n');solution=sentences[0]+'\n\n![]('+asset(correct,p,False)+')\n\n'+'\n\n'.join(sentences[1:])
 target=[affine(x,p) for x in BREAKS.get(qid,[SELECT.get(qid,0)])]
 missing_plot=qid in BLANK
 legacy=qid=='q-48080'
 opaque_slashes=any('\\\\' in a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])
 return assemble(problem,solution,fields,'easy',{'seed':seed,'template':family,'profile':('observed:' if raw else 'authored:')+qid,'parameters':p,'source_ids':[q[':question/id']],
 'evidence_only':raw,'eligible_for_learning':not raw,'source_anomalies':{'omitted_plot':missing_plot,'legacy_field':legacy,'decoded_double_slashes':opaque_slashes,'fieldless':':question/answer-fields' not in q},
 'fields_present':':question/answer-fields' in q if raw else True,
 'mathematical_fingerprint':digest({'criterion':'graph-selection' if family=='select_graph' else 'coordinate-set','target':list(map(str,target)),'scale_reading':p.get('grid',1),'break_count':len(target)}),'raw_source_replay':raw},preserve_difficulty=':question/difficulty' in q if raw else True)

# MODERATE: authored three mixed breaks, signed half-unit coordinates all labelled.
# HARD: same recognition operation; three half-unit breaks, unit-tick midpoint
# reading and one connected corner. No algebra/limits or additional KP demands.
def extended(level,p,seed):
 xs=p['coordinates'];graph=render(authored_spec(xs,level,p['orientation']),{'scale':1,'shift':0,'grid':.5 if level=='moderate' else 1})
 bank=complete_set_bank(xs);answer=settext(xs)
 problem=f'![]({graph})\n\nWhat are the points of discontinuity of the function plotted above?'
 solution='The graph breaks at '+answer.replace(' only','')+", meaning that we can't draw the plot without taking our pencil off of the paper when passing through these points.\n\nTherefore, the correct answer is "+answer.replace(' only','')+'.'
 fields=[{'key':'selection','type':':answer-field.type/radio','choices':[{'type':':answer.type/text','value':settext(s)} for s in bank],'correct':answer}]
 return assemble(problem,solution,fields,level,{'seed':seed,'template':'mixed_breaks_'+level,'profile':'authored:three-break-subsets','parameters':p,'source_ids':[],'scope_anchor':'e-3568; introduction -> continuity-at-point -> KP68695 -> KP68696 -> KP68697','evidence_only':False,'eligible_for_learning':True,'authored_level':True,'mathematical_fingerprint':digest({'level':level,'coordinates':xs,'grid':.5 if level=='moderate' else 1,'corner':level=='hard'})})
def validate_parameters(level,p,raw=False):
 if level=='easy':
  if set(p)-{'scale','shift','grid'}:raise ValueError('unknown parameters')
  if sp.Rational(str(p['scale'])) not in (1,2):raise ValueError('easy scale is 1 or 2')
  if sp.Rational(str(p['shift'])).q!=1 or abs(p['shift'])>3:raise ValueError('easy integer shift |h|<=3')
  if p.get('grid',1)!=1:raise ValueError('easy unit ticks')
 else:
  if set(p)!={'coordinates','orientation'}:raise ValueError('coordinates and orientation required')
  xs=list(map(lambda x:sp.Rational(str(x)),p['coordinates']))
  if len(xs)!=3 or xs!=sorted(set(xs)) or any(abs(x)>4 or x.q not in (1,2) for x in xs):raise ValueError('three ordered half-unit coordinates within [-4,4]')
  if min(xs[1]-xs[0],xs[2]-xs[1])<sp.Rational(3,2):raise ValueError('separated readable breaks')
  if level=='moderate' and sum(x.q==2 for x in xs)!=1:raise ValueError('moderate has exactly one midpoint coordinate')
  if level=='hard' and sum(x.q==2 for x in xs)!=2:raise ValueError('hard has exactly two midpoint coordinates')
  if not xs[0]<0<xs[-1]:raise ValueError('signed workload required')
  if p['orientation'] not in (-1,1):raise ValueError('orientation +/-1')
def coordinate_catalog(level):
 import itertools
 return [list(map(float,xs)) for xs in itertools.combinations([sp.Rational(i,2) for i in range(-8,9)],3) if xs[0]<0<xs[-1] and min(xs[1]-xs[0],xs[2]-xs[1])>=sp.Rational(3,2) and sum(x.q==2 for x in xs)==(1 if level=='moderate' else 2)]
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed)
 if level=='easy':
  raw=bool(profile and profile.startswith('observed:'))
  eligible=list(QUESTIONS)
  if template:eligible=[q for q in eligible if infer_family(q)==template or q==template]
  if field_type:eligible=[q for q in eligible if ('blank' if q in BLANK else 'radio')==field_type.removeprefix(':answer-field.type/')]
  if profile:
   if not profile.startswith(('observed:','authored:')):raise ValueError('unknown profile')
   qid=profile.split(':',1)[1]
   if qid not in eligible:raise ValueError('profile/template incompatibility')
  else:
   if not eligible:raise ValueError('no compatible family')
   qid=rng.choice(eligible) # entire source-shaped family/bank selected first
  p=dict(parameters) if parameters is not None else {'scale':rng.choice([1,2]),'shift':rng.randint(-3,3)}
  if 'scale' not in p or 'shift' not in p:raise ValueError('scale and shift required')
  validate_parameters(level,p,raw)
  return observed(qid,p,seed,raw)
 if profile not in (None,'authored:three-break-subsets') or template not in (None,'mixed_breaks_'+level) or field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('unsupported authored profile/layout')
 # Complete subset bank is fixed before parameter sampling.
 p=copy.deepcopy(parameters) if parameters is not None else {'coordinates':rng.choice(coordinate_catalog(level)),'orientation':rng.choice([-1,1])}
 validate_parameters(level,p)
 return extended(level,p,seed)
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  text+='Field '+f[':answer-field/key']+'\n\n'
  for a in f[':answer-field/choices']:
   v=a[':answer/value'];text+='- '+('![]('+v+')' if a[':answer/type']==':answer.type/image' else v)+'\n'
 text+='\nWorked solution:\n\n'+q.get(':question/worked-solution','[absent]')+'\n'
 return text

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186068696-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in rows))
