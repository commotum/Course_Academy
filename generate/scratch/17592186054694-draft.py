#!/usr/bin/env python3
"""Local three-level draft; immutable original evidence at math basis 2275.
Easy: observed integer substitution. Moderate: authored signed nonunit products.
Hard: authored half-integer products and half-unit coordinate reading.
All levels retain equation -> four x=0,1,2,3 values -> points -> connected line.
No database, registration, publication, or engine mutation.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,re,sys,uuid,tempfile,threading
from pathlib import Path
import sympy as sp
KP_ID=17592186054694
KP_UUID='2491cf6c-260b-5992-a910-9fe6a80e30bc'
TITLE='Plotting a Line Using a Table'
VERSION='line-table-draft-2275-v1'
HERE=Path(__file__).resolve().with_suffix('')
os.environ.setdefault('MPLCONFIGDIR',str(HERE/'matplotlib-cache'))
S=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES={'unit_positive':{'source':'q-54397','m':1,'b':-2},'unit_negative':{'source':'q-59676','m':-1,'b':1},'double_positive':{'source':'q-71695','m':2,'b':2}}
LOCK=threading.RLock()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def atom(path,content):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='write-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as out:out.write(content)
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def tex(v):return sp.latex(sp.Rational(v))
def suffix(b):return '+'+tex(b) if b>0 else '-'+tex(-b) if b<0 else ''
def rhs(m,b):return ('x' if m==1 else '-x' if m==-1 else tex(m)+'x')+suffix(b)
def arithmetic(m,b,i):return ('' if m==1 else '-' if m==-1 else tex(m))+f'({i})'+suffix(b)+'='+tex(m*i+b)
def bank(profile,m,b):
 if profile=='q-54397':return [(-m,0),(m,b),(-m,-b/2),(m,-b),(m,0)]
 if profile=='q-59676':return [(m,2*b),(-m,-2*b),(-m,-b),(2*m,4*b),(m,b)]
 if profile=='q-71695':return [(m,-b),(-m,b),(-m/2,b),(m,b),(m/2,b)]
 if profile in ('signed-products','half-units'):return [(m,b),(-m,b),(m,-b),(m,0),(2*m,b)]
 raise ValueError('Unknown complete profile')
def task_domain(level):
 bs=[sp.Integer(b) for b in range(-8,9) if b]
 if level=='easy':return [(sp.Integer(m),b) for m in (1,-1,2) for b in bs]
 if level=='moderate':return [(sp.Integer(m),b) for m in (-2,-3,-4) for b in bs]
 if level=='hard':return [(sp.Rational(m,2),sp.Rational(b,2)) for m in (-5,-3,-1,1,3,5) for b in range(-11,12,2)]
 raise ValueError('Unknown difficulty')
def profile_for(level,template):return TEMPLATES[template]['source'] if level=='easy' else 'signed-products' if level=='moderate' else 'half-units'
def recipe_names(profile):
 return {'q-54397':['reverse product and omit constant','correct','reverse product and reverse/halve constant (empirical compound pattern)','reverse constant sign','omit constant'],'q-59676':['double constant','reverse entire doubled-constant expression','reverse entire expression','double product and quadruple constant (empirical compound pattern)','correct'],'q-71695':['reverse constant sign','reverse product sign','reverse and halve product','correct','halve product'],'signed-products':['correct','reverse product sign','reverse constant sign','omit constant','double product'],'half-units':['correct','reverse product sign','reverse constant sign','omit constant','double product']}[profile]
def render_plot(m,b,points_only,bounds,step,output_dir=None):
 """No input file: arguments belong to this call. Unique temp PNG + atomic sidecar."""
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 data={'renderer':'Matplotlib','version':VERSION,'m':str(m),'b':str(b),'points_only':points_only,'bounds':bounds,'grid_increment':str(step),'table_x':[0,1,2,3],'table_y':[str(m*i+b) for i in range(4)],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__,'numpy':np.__version__}}
 data['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 path=Path(output_dir or HERE/'images')/('line-'+digest(data)+'.png');side=Path(str(path)+'.json');path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists() and side.exists():return str(path)
 with LOCK:
  fig,ax=plt.subplots(figsize=(4.8,4.8),dpi=120);fig.subplots_adjust(left=.10,right=.95,bottom=.10,top=.95)
  xmin,xmax,ymin,ymax=bounds;ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal');st=float(step)
  major=max(1,int((ymax-ymin)/10));major=2 if major==1 and st==1 and ymax-ymin>14 else major
  ticks=lambda lo,hi,s:np.arange(np.ceil(lo/s)*s,hi+s/10,s)
  ax.set_xticks(ticks(xmin,xmax,major));ax.set_yticks(ticks(ymin,ymax,major));ax.set_xticks(ticks(xmin,xmax,st),minor=True);ax.set_yticks(ticks(ymin,ymax,st),minor=True)
  ax.grid(which='both',color='#cdcdcd',lw=.55)
  for side_name in ('top','right'):ax.spines[side_name].set_visible(False)
  for side_name in ('left','bottom'):ax.spines[side_name].set_position('zero');ax.spines[side_name].set_linewidth(.8)
  ax.tick_params(which='both',length=0,labelsize=9,pad=3)
  # Suppress duplicate zero numeral while retaining the zero axes themselves.
  ax.set_xticklabels(['' if v==0 else f'{v:g}' for v in ax.get_xticks()]);ax.set_yticklabels(['' if v==0 else f'{v:g}' for v in ax.get_yticks()])
  ax.annotate('',xy=(xmax,0),xytext=(xmax-.4,0),arrowprops={'arrowstyle':'->','lw':1,'color':'black'});ax.annotate('',xy=(0,ymax),xytext=(0,ymax-.4),arrowprops={'arrowstyle':'->','lw':1,'color':'black'})
  ax.text(xmax+.12,0,'$x$',fontsize=12,va='center');ax.text(0,ymax+.12,'$y$',fontsize=12,ha='center')
  if not points_only:
   xx=np.linspace(xmin,xmax,801);ax.plot(xx,float(m)*xx+float(b),color='#ff0000',lw=1.4,zorder=3)
  ax.plot(range(4),[float(m*i+b) for i in range(4)],'o',color='#0000ff',ms=4,zorder=4)
  fig.canvas.draw();data['pixel_points']=[list(ax.transData.transform((i,float(m*i+b)))) for i in range(4)];data['pixel_origin']=list(ax.transData.transform((0,0)));data['pixel_unit']=list(ax.transData.transform((1,1))-ax.transData.transform((0,0)));data['dimensions']=[576,576]
  fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.png',dir=path.parent);os.close(fd)
  try:fig.savefig(tmp,metadata={'Software':VERSION});os.replace(tmp,path)
  finally:
   plt.close(fig)
   if os.path.exists(tmp):os.unlink(tmp)
  data['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();atom(side,(json.dumps(data,indent=2)+'\n').encode())
 return str(path)
def solution(template,m,b,points,line):
 info=TEMPLATES[template];src=SOURCES[info['source']]
 if ':question/worked-solution' not in src:src=SOURCES['q-54397'];sm,sb=sp.Integer(1),sp.Integer(-2)
 else:sm,sb=sp.Integer(info['m']),sp.Integer(info['b'])
 sol=src[':question/worked-solution']
 for i in range(4):sol=sol.replace(arithmetic(sm,sb,i),f'@@CALC{i}@@')
 row='| $y$ | '+' | '.join('$'+tex(sm*i+sb)+'$' for i in range(4))+' |'
 sol=sol.replace(row,'@@ROW@@').replace('y='+rhs(sm,sb),'y=@@EQ@@')
 refs=re.findall(r'!\[\]\(([^)]+)\)',sol);assert len(refs)==2
 sol=sol.replace(refs[0],'@@POINTS@@').replace(refs[1],'@@LINE@@').replace('@@EQ@@',rhs(m,b)).replace('@@ROW@@','| $y$ | '+' | '.join('$'+tex(m*i+b)+'$' for i in range(4))+' |').replace('@@POINTS@@',points).replace('@@LINE@@',line)
 for i in range(4):sol=sol.replace(f'@@CALC{i}@@',arithmetic(m,b,i))
 assert '@@' not in sol
 return sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """parameters.source_replay=True retains exact original asset refs/omissions.
 Original replay remains publicly parameterized; non-anchor replay raises.
 """
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 rng=random.Random(seed);explicit=parameters is not None;raw=bool((parameters or {}).get('source_replay',False))
 if template is None:
  if profile in SOURCES:template=next(t for t,v in TEMPLATES.items() if v['source']==profile)
  else:template=rng.choice(list(TEMPLATES)) if level!='easy' else rng.choice(list(TEMPLATES))
 if template not in TEMPLATES:raise ValueError('Unknown template')
 profile=profile or profile_for(level,template) # Complete profile selected before parameters.
 domain=task_domain(level)
 if level=='easy':domain=[p for p in domain if p[0]==TEMPLATES[template]['m']]
 if explicit:m,b=sp.Rational(parameters['m']),sp.Rational(parameters['b'])
 else:m,b=rng.choice(domain)
 if (m,b) not in domain:raise ValueError('Outside documented level workload bounds')
 if raw and (profile!=TEMPLATES[template]['source'] or (m,b)!=(TEMPLATES[template]['m'],TEMPLATES[template]['b']) or level!='easy'):raise ValueError('Source replay requires original template/profile/parameters')
 if profile!=profile_for(level,template):raise ValueError('Profile does not belong to this level/template')
 lines=[tuple(map(sp.Rational,v)) for v in bank(profile,m,b)]
 if len(set(lines))!=5 or lines.count((m,b))!=1:raise ValueError('Reject whole ambiguous bank')
 step=sp.Rational(1,2) if level=='hard' else sp.Integer(1)
 # Every bank member controls bounds; every table marker has at least one unit margin.
 ys=[s*i+c for s,c in lines for i in range(4)];extent=max(6,int(sp.ceiling(max(map(abs,ys))))+1)
 bounds=[-5,5,-extent,extent];bounds[0]=-extent;bounds[1]=extent
 if 489/(2*extent)*float(step)<5:raise ValueError('Reject whole illegible bank')
 fresh=[render_plot(s,c,False,bounds,step) for s,c in lines];freshpoints=render_plot(m,b,True,bounds,step)
 src=SOURCES[TEMPLATES[template]['source']]
 oldeq=re.search(r'\$y\s*=\s*([^$]+)\$',src[':question/problem'])[0]
 # Preserve punctuation placement and the legacy right-aligned negative table.
 prompt=src[':question/problem'].replace(oldeq,'$y ='+rhs(m,b)+'$' if template=='unit_negative' else '$y='+rhs(m,b)+'.$')
 if raw:prompt=src[':question/problem'] # The same formula mask is verified above; source spacing is evidence.
 correct=lines.index((m,b));assets=[a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']] if raw else fresh
 srcsol=src.get(':question/worked-solution');points=re.findall(r'!\[\]\(([^)]+)\)',srcsol)[0] if raw and srcsol else freshpoints
 sol=solution(template,m,b,points,assets[correct])
 fp=digest({'equation':[str(m),str(b)],'table_x':[0,1,2,3],'requested':'complete table then identify line','grid_increment':str(step)})
 identity=digest({'version':VERSION,'difficulty':None if raw and ':question/difficulty' not in src else level,'prompt':prompt,'solution':None if raw and not srcsol else sol,'bank':sorted(assets),'key':None if raw and ':answer-field/correct' not in src[':question/answer-fields'][0] else assets[correct]})
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'line:'+str(s)+','+str(c))),':answer/type':':answer.type/image',':answer/value':asset} for (s,c),asset in zip(lines,assets)]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in src[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
 if not raw:rng.shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if not raw or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
 if not raw or srcsol:q[':question/worked-solution']=sol
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':{'m':str(m),'b':str(b),'source_replay':raw},'source_question':TEMPLATES[template]['source'],'source_basis':S['basis'],'source_lineage':S['lineage'],'difficulty_origin':'observed easy; negative inferred same workload' if level=='easy' else 'authored missing level','evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':fp,'content_identity':identity,'domain':'x,y real; bounded exact rational linear equations','lines':[[str(s),str(c)] for s,c in lines],'recipes':recipe_names(profile),'assets':assets+[points],'recreated_assets':fresh+[freshpoints],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__},'source_omissions':['difficulty','worked solution','correct ref'] if raw and not srcsol else []}}
# Easy: three observed parameter shapes, 48 substantive equation tasks.
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)
# Moderate (authored): negative nonunit integer product, |m|=2..4; 48 tasks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)
# Hard (authored): odd halves m,b, |m|<=5/2, |b|<=11/2; 72 tasks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');o=ap.parse_args()
 if o.count<1:ap.error('count must be positive')
 out=[generate(l,o.seed+i,template=o.template,profile=o.profile) for l in (['easy','moderate','hard'] if o.difficulty=='all' else [o.difficulty]) for i in range(o.count)]
 print(json.dumps(out,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
