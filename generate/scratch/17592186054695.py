#!/usr/bin/env python3
"""Exact bounded easy graph banks; source assets replayed, variants use Matplotlib."""
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
KP_ID=17592186054695
KP_UUID='ebeb4e5a-adbe-5a94-b05d-61933a687892'
TITLE='Sketching a Line Using Two Points'
VERSION='two-point-lines-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
CONTRACT=json.loads((PACKAGE/'contract.json').read_text());PROFILES=CONTRACT['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def line(p):return tuple(sp.Rational(z) for z in p)
def fingerprint(p):return digest([str(z) for z in line(p)])
def candidates(sid):
 return [[m,0] for m in (-4,-3,-2,-1)] if sid=='q-102054' else [[str(sp.Rational(-1,d)),b] for d in (2,3,4) for b in (2,3,4)]
def bank(sid,p):
 m,b=line(p)
 return [(-m,m),(m,-m),(m/2,0),(m,0),(-m,0)] if sid=='q-102054' else [(-m,-b),(m,2*b),(m,b),(-m,0),(m,0)]
def render_plot(p,points=()):
 m,b=line(p);points=tuple(tuple(sp.Rational(z) for z in pt) for pt in points)
 if not points:
  for path,value in CONTRACT['source_asset_lines'].items():
   if line(value)==(m,b):return path,None
 else:
  for sid,t in PROFILES.items():
   sm,sb=line(t['parameters']);sx=t['second_x']
   if (m,b)==(sm,sb) and points==((0,sb),(sx,sm*sx+sb)):
    return re.findall(r'!\[.*?\]\((.*?)\)',t['solution'])[0],None
 key=digest([str(m),str(b),[[str(z) for z in pt] for pt in points]])
 out=PACKAGE/'assets'/('line-'+key+'.png');out.parent.mkdir(exist_ok=True)
 if not out.exists():
  xmax=max(9.5,max((float(pt[0])+1.5 for pt in points),default=0));xmin=-4.5;ymin=-6.5;ymax=9.5
  fig,ax=plt.subplots(figsize=(4.5,4.5),dpi=120);ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.set_aspect('equal',adjustable='box')
  ax.set_xticks(range(-4,int(xmax)+1,2));ax.set_yticks(range(-6,10,2));ax.set_xticks(range(-4,int(xmax)+1),minor=True);ax.set_yticks(range(-6,10),minor=True)
  ax.grid(which='both',color='#c8c8c8',linewidth=.7);ax.set_axisbelow(True)
  ax.spines[['right','top']].set_visible(False);ax.spines[['left','bottom']].set_position('zero');ax.spines[['left','bottom']].set_linewidth(1.3)
  ax.tick_params(which='both',length=0,labelsize=8,pad=4)
  ax.set_xticklabels(['' if i==0 else str(i) for i in ax.get_xticks().astype(int)]);ax.set_yticklabels(['' if i==0 else str(i) for i in ax.get_yticks().astype(int)])
  ax.plot([xmin,xmax],[float(m*xmin+b),float(m*xmax+b)],color='red',linewidth=1.7)
  if points:ax.scatter([float(x) for x,y in points],[float(y) for x,y in points],s=20,c='blue',zorder=5)
  ax.plot(xmax,0,'>k',clip_on=False,markersize=5);ax.plot(0,ymax,'^k',clip_on=False,markersize=5);ax.text(xmax+.25,0,'$x$',fontsize=12);ax.text(.1,ymax+.3,'$y$',fontsize=12)
  fig.tight_layout(pad=1.5);fig.savefig(out,metadata={'Software':VERSION});plt.close(fig)
 data=out.read_bytes();sha=hashlib.sha256(data).hexdigest();relative=f'images/{sha[:2]}/{sha}.png'
 return relative,{'local':str(out),'path':relative,'sha256':sha,'line':[str(m),str(b)],'points':[[str(z) for z in pt] for pt in points]}
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported bounded band; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice(list(PROFILES));t=PROFILES[sid];p=parameters or rng.choice(candidates(sid));m,b=line(p)
 if (m,b) not in [line(z) for z in candidates(sid)]:raise ValueError('Outside validated finite domain')
 x2=1 if sid=='q-102054' else 4*int(sp.denom(m));y2=m*x2+b
 asset,info=render_plot((m,b),[(0,b),(x2,y2)]);assets=[info] if info else []
 prompt=t['prompt'];sol=t['solution'];original_asset=re.findall(r'!\[.*?\]\((.*?)\)',sol)[0]
 if sid=='q-102054':prompt=prompt.replace('-2',str(m));sol=sol.replace('-2',str(m))
 else:
  d=int(sp.denom(m));expr=f'{b}-\\frac{{1}}{{{d}}}'
  prompt=prompt.replace(r'2-\frac{1}{2}',expr);sol=sol.replace(r'2-\frac{1}{2}',expr)
  sol=sol.replace('x=8.',f'x={x2}.').replace(f'{expr}(8)',f'{expr}({x2})').replace('=2-0',f'={b}-0').replace('=2.',f'={b}.').replace('(0,2)',f'(0,{b})').replace('=2-4',f'={b}-4').replace('=-2.',f'={y2}.').replace('(8,-2)',f'({x2},{y2})')
 sol=sol.replace(original_asset,asset)
 values=[];objects=bank(sid,p)
 for z in objects:
  value,inf=render_plot(z);values.append(value)
  if inf:assets.append(inf)
 fp=fingerprint(p);qid=ident(['question',VERSION,fp,sid,[[str(z) for z in obj] for obj in objects]]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,value]),':answer/type':':answer.type/image',':answer/value':value} for value in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[t['correct_index']][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':[str(m),str(b)],'second_point':[str(x2),str(y2)],'source_ids':[sid],'domain':'x real; two distinct points; bounded negative slopes','mathematical_fingerprint':fp,'recipes':t['recipes'],'choice_lines':[[str(z) for z in obj] for obj in objects],'assets':assets,'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}
def batch(difficulty,count,seed):
 if difficulty!='easy':raise ValueError('Unsupported bounded band')
 pairs=[(sid,p) for sid in PROFILES for p in candidates(sid)];random.Random(seed).shuffle(pairs);rs=[];used=set()
 for sid,p in pairs:
  rec=generate(difficulty,seed,sid,p);fp=rec['generation']['mathematical_fingerprint']
  if fp not in used:rs.append(rec);used.add(fp)
  if len(rs)==count:return rs
 raise ValueError('Finite validated family exhausted; shortage explicit')
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('![]('+z[':answer/value']+')' for z in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
