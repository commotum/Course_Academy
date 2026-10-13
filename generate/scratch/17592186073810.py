#!/usr/bin/env python3
"""Bounded horizontal/vertical point-line distance generator, no database writes.

Five complete easy source banks; each bank is dilated together with its geometry.
Integral dilation k=1..3; k=1 exact source replay, k=2..3 extensions (distance <=24).
Moderate/hard unsupported. Seed, bank order and irrelevant coordinate do not
create distinct questions. CLI: --difficulty easy --count N --seed N --format json.
"""
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186073810
KP_UUID='522b66f4-8a46-5dd0-a9d7-3b081c0ed157'
TITLE='Finding the Distance Between a Point and a Horizontal or Vertical Line'
VERSION='axis-distance-dilation-v1'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PACKAGE=Path(__file__).resolve().with_suffix('')
ROOT=PACKAGE.parents[2]
SOURCES={q[':question/math-academy-id']:q for q in json.loads((PACKAGE/'source.json').read_text())[':knowledge-point/questions']}
CASES={sid:q for sid,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy' and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(v,sort_keys=True,separators=(',',':'))))
def geometry(q):
 p=re.search(r'point \$\(([-\d]+),\s*([-\d]+)\)\$',q[':question/problem']);line=re.search(r'line \$([xy])\s*=\s*([-\d]+)',q[':question/problem'])
 if not p or not line:raise ValueError('Unrecognized geometry: review before generation')
 return line[1],int(p[1]),int(p[2]),int(line[2])
def fingerprint(q):
 axis,x,y,c=geometry(q)
 return digest([axis,x if axis=='x' else y,c])
def data(sid,k):
 axis,x,y,c=geometry(CASES[sid]);return axis,k*x,k*y,k*c

def render_plots(z,sid,k):
 os.environ.setdefault('MPLCONFIGDIR',str(PACKAGE/'matplotlib-cache'))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 axis,x,y,c=z;d=abs((x if axis=='x' else y)-c);fx,fy=(c,y) if axis=='x' else (x,c)
 name=digest([VERSION,z]);out=PACKAGE/'plots';out.mkdir(parents=True,exist_ok=True);path=out/(name+'.png')
 if not path.exists():
  fig,ax=plt.subplots(figsize=(5,5));fig.subplots_adjust(left=.12,bottom=.12,right=.95,top=.9)
  xmin=min(0,x,fx)-3*k;xmax=max(0,x,fx)+3*k;ymin=min(0,y,fy)-3*k;ymax=max(0,y,fy)+3*k
  ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal',xlabel='$x$',ylabel='$y$');ax.grid(color='#cccccc',lw=.7)
  ax.axhline(0,color='black',lw=1.3);ax.axvline(0,color='black',lw=1.3)
  if axis=='x':ax.axvline(c,color='#2373b8',lw=1.8);ax.text(c+.25*k,ymax-1.5*k,f'$x={c}$',bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
  else:ax.axhline(c,color='#2373b8',lw=1.8);ax.text(xmax-3*k,c+.4*k,f'$y={c}$',bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
  ax.plot([x,fx],[y,fy],'--',color='black',lw=1);ax.plot(x,y,'o',color='red',ms=6);ax.plot(fx,fy,'o',color='#2373b8',ms=6)
  ax.annotate(f'$({x},{y})$',(x,y),xytext=(6,-18),textcoords='offset points',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
  ax.annotate(f'{d} units',((x+fx)/2,(y+fy)/2),xytext=(8,12) if axis=='x' else (12,0),textcoords='offset points',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
  ax.set_title('Shortest distance to the line',fontsize=12)
  fig.savefig(path,dpi=120,metadata={'Software':'Course Academy '+VERSION});plt.close(fig)
  (out/(name+'.json')).write_text(json.dumps({'parameters':list(z),'foot':[fx,fy],'distance':d,'bounds':[xmin,xmax,ymin,ymax],'renderer':'Matplotlib','role':'worked-solution'},indent=2)+'\n')
 sha=hashlib.sha256(path.read_bytes()).hexdigest()
 return {'local_path':str(path.relative_to(ROOT)),'path':'images/'+sha[:2]+'/'+sha+'.png','sha256':sha,'role':'worked-solution','unchanged_source_asset':False}

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported difficulty; see capabilities.json')
 sid=template or random.Random(seed).choice(sorted(CASES));k=parameters[1] if parameters else random.Random(seed).randint(2,3)
 if sid not in CASES or type(k)!=int or not 1<=k<=3 or (parameters and parameters!=[sid,k]):raise ValueError('Outside bounded source profile')
 old=CASES[sid];axis,x,y,c=data(sid,k);d=int(sp.Abs(sp.Integer(x if axis=='x' else y)-c));of=old[':question/answer-fields'][0]
 vals=[str(k*sp.Integer(a[':answer/value'])) for a in of[':answer-field/choices']];correct=str(d)
 assert len(set(vals))==5 and correct==str(k*sp.Integer(of[':answer-field/correct'][':answer/value']))
 if k==1:
  problem=old[':question/problem'];worked=old[':question/worked-solution'];ref=re.search(r'!\[\]\((.*?)\)',worked)[1];path=Path('/media/jake/SSD/EDB/math')/ref
  asset={'path':ref,'local_path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'worked-solution','unchanged_source_asset':True}
 else:
  asset=render_plots((axis,x,y,c),sid,k)
  problem=f'Find the shortest distance between the point $({x},{y})$ and the line ${axis}={c}.$'
  oldaxis,ox,oy,oc=geometry(old)
  worked=old[':question/worked-solution']
  worked=re.sub(r'!\[\]\((.*?)\)',lambda m:'![]('+asset['path']+')',worked)
  worked=worked.replace(f'$({ox},{oy})$',f'$({x},{y})$').replace(f'${axis}={oc}$',f'${axis}={c}$').replace(f'${oc}.$',f'${c}.$')
  coord=x if axis=='x' else y;cs=f'({c})' if c<0 else str(c)
  worked=re.sub(r'\$\$.*?\$\$',lambda m:'$$\nd=|'+str(coord)+'-'+cs+'|='+str(d)+'.\n$$',worked,flags=re.S)
 fp=fingerprint({':question/problem':problem});qid=ident(['question',VERSION,fp,sid,digest(sorted(vals))]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 aid=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',aid]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':[sid,k],'source_ids':[sid],'domain':'Euclidean plane; integral coordinates, point off line; distance positive','mathematical_fingerprint':fp,'assets':[asset],'sympy':sp.__version__,'sampling_policy':'full source geometry and bank dilation k=1..3; k>=2 new; source integer-distance easy skill retained','solution_fidelity':'exact source at k=1; source prose with recomputed math and Matplotlib sketch at k>1'}}

def batch(difficulty,count,seed=0):
 if difficulty!='easy':raise ValueError('Unsupported difficulty')
 rs=[generate(difficulty,seed,sid,[sid,k]) for sid in sorted(CASES) for k in range(2,4)];random.Random(seed).shuffle(rs)
 if count>len(rs):raise ValueError('Finite family exhausted; leave shortage explicit')
 return rs[:count]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
