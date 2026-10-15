#!/usr/bin/env python3
"""Source-faithful square-flux generator. See adjacent package for evidence."""
import argparse,hashlib,json,os,random,re,sys,uuid
from pathlib import Path
if __name__=='__main__' and sys.prefix != str(Path(__file__).resolve().parents[2]/'.venv'):
 os.execv(str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),[str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),__file__,*sys.argv[1:]])
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-flux-matplotlib')
import sympy as sp
HERE=Path(__file__).with_suffix('');CAPTURE=json.loads((HERE/'source.json').read_text());RAW=CAPTURE['record'];KP_ID=17592186179646;KP_UUID=RAW[':knowledge-point/id'];VERSION='1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions']}
SUPPORTED=('easy','moderate');LENGTHS=(2,4,6,8,10,12);COEFFICIENTS=(-4,-3,-2,-1,sp.Rational(-1,2),sp.Rational(1,2),1,2,3,4)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def number(x):
 x=sp.Rational(x)
 return '-0.5' if x==sp.Rational(-1,2) else '0.5' if x==sp.Rational(1,2) else str(x) if x.q==1 else sp.latex(x)
def coefficient(x):return '' if x==1 else '-' if x==-1 else number(x)
def value_parse(x):
 x=x.replace(' ','')
 m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',x)
 return (-1 if m[1] else 1)*sp.Rational(m[2],m[3]) if m else sp.Rational(x)
def parameters(q):
 p=q[':question/problem'].replace(r'\mathbf ','');field=re.search(r'\$F\s*=\s*(.*?)\$',p)[1];radial='x' in field
 c=re.match(r'(-?[\d.]*)(?:\\,)?[xij]',field.replace(' ',''))[1];c=-1 if c=='-' else 1 if not c else sp.Rational(c)
 return {'c':str(c),'L':int(re.search(r'side length \$(\d+)\$',p)[1]),'axis':'radial' if radial else ('i' if 'i' in field else 'j')}
def level_of(q):return q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
def validate_parameters(level,p):
 if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level+'; no evidenced hard template')
 c=sp.Rational(p['c']);L=p['L'];axis=p['axis']
 if L not in LENGTHS or c not in COEFFICIENTS or axis not in (('i','j') if level=='easy' else ('radial',)):raise ValueError('Outside documented domain')
 if level=='easy' and abs(c)<2:raise ValueError('Uniform bank requires |c| >= 2')
 return c,L,axis

def field(c,axis):
 if axis!='radial':return coefficient(c)+r'\,'+axis
 sign='+' if c>0 else '-';return coefficient(c)+r'x\,i'+sign+coefficient(abs(c))+r'y\,j'

def bank(level,p,profile):
 c,L,axis=validate_parameters(level,p);src=SOURCES[profile];s=parameters(src);c0=sp.Rational(s['c']);L0=s['L']
 values=[sp.Rational(a[':answer/value']) for a in src[':question/answer-fields'][0][':answer-field/choices']]
 if level=='easy':
  # q-127190 has an observed 2L bank; the other profiles use |c|L.
  return [v/L0*L if abs(v)==L0 or profile=='q-127190' else v/(abs(c0)*L0)*abs(c)*L for v in values]
 A=2*c*L**2;A0=2*c0*L0**2
 # Explicit homogeneous value patterns, not inferred psychological mistakes.
 return [sp.cancel(v/A0*A) for v in values]

def render_plots(p,output_dir):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 c=sp.Rational(p['c']);L=p['L'];axis=p['axis'];h=L/2
 out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);key=digest(p);assets={}
 for role in ('prompt','solution'):
  fig,ax=plt.subplots(figsize=(4,4));lim=1.9*h;ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect='equal');ax.axis('off')
  for end in ((lim,0),(0,lim)):
   start=(-lim,0) if end[1]==0 else (0,-lim);ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'black','lw':1})
  ax.text(lim*.95,-h*.18,'$x$');ax.text(h*.12,lim*.92,'$y$')
  ax.plot([-h,h,h,-h,-h],[-h,-h,h,h,-h],color='#2474bd',lw=1.5)
  if role=='prompt':
   grid=np.linspace(-1.6*h,1.6*h,13);xx,yy=np.meshgrid(grid,grid)
   u=float(c)*xx if axis=='radial' else np.full_like(xx,float(c) if axis=='i' else 0)
   v=float(c)*yy if axis=='radial' else np.full_like(yy,float(c) if axis=='j' else 0)
   scale=max(float(np.max(np.hypot(u,v))),1)/(0.21*h)
   ax.quiver(xx,yy,u,v,angles='xy',scale_units='xy',scale=scale,color='#999999',width=.0025)
  else:
   for k,(x,y,nx,ny,tx,ty) in enumerate(((h,-.45*h,1,0,h,.8*h),(-.45*h,h,0,1,.65*h,h),(-h,-.45*h,-1,0,-h,.8*h),(-.45*h,-h,0,-1,.65*h,-h)),1):
    ax.annotate('',xy=(x+.5*h*nx,y+.5*h*ny),xytext=(x,y),arrowprops={'arrowstyle':'->','color':'#df9700'})
    ax.text(x+.52*h*nx,y+.52*h*ny,f'$n_{k}$',fontsize=9)
    ax.text(tx+.07*h*nx,ty+.12*h*ny,f'$C_{k}$',color='#2474bd',fontsize=10)
   for x,y,label in ((h,-.12*h,number(h)),(-h,-.12*h,number(-h)),(.06*h,h,number(h)),(.06*h,-h,number(-h))):ax.text(x,y,'$'+label+'$',fontsize=9)
  path=out/(key+'-'+role+'.png');fig.savefig(path,dpi=130,bbox_inches='tight',pad_inches=.15,metadata={'Software':'Course Academy square flux '+VERSION});plt.close(fig)
  assets[role]=str(path)
 return assets

MODERATE=r'''First, consider the side ${C}_{1}.$ We have that ${n}_{1}=i,$ and therefore,

$$
\begin{aligned}{\int }_{{C}_{1}}F\cdot {n}_{1}\,\text{d}s & ={\int }_{{C}_{1}}(@F@)\cdot i\,\text{d}s \\  & =@c@{\int }_{{C}_{1}}x\,\text{d}s.\end{aligned}
$$

This is a line integral with respect to arc length, which we can evaluate in the usual way. Parameterizing the side ${C}_{1},$ we have

$$
r(t)=@hcoef@\,i+t\,j,\,⇒\,{r}^{′}(t)=j,\,t\in [-@h@,@h@].
$$

Therefore,

$$
\begin{aligned}@c@{\int }_{{C}_{1}}x\,\text{d}s & =@c@{\int }_{-@h@}^{@h@}@h@\cdot ||{r}^{′}(t)||\,\text{d}t \\  & =@ch@{\int }_{-@h@}^{@h@}\text{d}t \\  & =@ch@(@h@-(-@h@)) \\  & =@chparen@\cdot @L@ \\  & =@one@.\end{aligned}
$$

By symmetry, the flux integrals over the sides ${C}_{2},{C}_{3},$ and ${C}_{4}$ must be the same. Therefore,

$$
{∮}_{C}F\cdot n\,\text{d}s=4\cdot @oneparen@=@A@.
$$'''

def generate(level,seed=0,template=None,parameters=None,profile=None,output_dir=None):
 rng=random.Random(seed)
 if level not in SUPPORTED:raise ValueError('Unsupported difficulty '+level)
 profiles=[sid for sid,q in SOURCES.items() if level_of(q)==level]
 profile=profile or rng.choice(profiles)
 if profile not in profiles:raise ValueError('Incompatible bank profile')
 template=template or ('uniform-cancellation' if level=='easy' else 'radial-four-sides')
 if template!=('uniform-cancellation' if level=='easy' else 'radial-four-sides'):raise ValueError('Unknown template')
 p=parameters or {'c':str(rng.choice([x for x in COEFFICIENTS if level!='easy' or abs(x)>=2])),'L':rng.choice(LENGTHS),'axis':rng.choice(('i','j')) if level=='easy' else 'radial'}
 p=dict(p);p['c']=str(sp.Rational(p['c']));c,L,axis=validate_parameters(level,p);F=field(c,axis);A=sp.Integer(0) if level=='easy' else 2*c*L**2
 values=bank(level,p,profile)
 assert len(values)==5 and len(set(values))==5 and values.count(A)==1
 src=SOURCES[profile];orig=globals()['parameters'](src);at_source=p==orig
 # Source replay retains original image placement and source notation.
 assets={};refs={}
 if at_source:
  refs['prompt']=re.findall(r'!\[.*?\]\((.*?)\)',src[':question/problem'])[0]
  solsrc=src if ':question/worked-solution' in src else SOURCES['q-226132']
  refs['solution']=re.findall(r'!\[.*?\]\((.*?)\)',solsrc[':question/worked-solution'])[0]
 else:
  assets=render_plots(p,output_dir or HERE/'assets');refs=assets
 if at_source:prompt=src[':question/problem']
 else:
  prompt='![]('+refs['prompt']+')\n\nConsider the vector field $F='+F+'$ and a square $C$ with side length $'+str(L)+'$ centered at $O,$ as shown above. Calculate the flux of $F$ across $C.$'
  if level=='moderate':prompt+='\n\n*Hint: You may use the fact that, due to symmetry, the flux is equal across all four sides of the square.*'
 if level=='easy':
  basis=next(q for q in SOURCES.values() if level_of(q)=='easy' and globals()['parameters'](q)['axis']==axis and (sp.Rational(globals()['parameters'](q)['c'])>0)==(c>0))
  solution=basis[':question/worked-solution'];oldF=re.search(r'\$F=(.*?)\$',basis[':question/problem'])[1];solution=solution.replace('$F='+oldF+'$','$F='+F+'$')
  solution=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+refs['solution']+')',solution)
 else:
  head=SOURCES['q-126890'][':question/worked-solution'].split('First, consider')[0];head=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+refs['solution']+')',head)
  h=sp.Rational(L,2);ch=c*h;one=ch*L
  tokens={'F':F,'c':coefficient(c),'hcoef':coefficient(h),'h':number(h),'ch':number(ch),'chparen':'('+number(ch)+')' if ch<0 else number(ch),'L':str(L),'one':number(one),'oneparen':'('+number(one)+')' if one<0 else number(one),'A':number(A)}
  body=MODERATE
  for k,v in tokens.items():body=body.replace('@'+k+'@',v)
  solution=head+body
 # Identity includes the complete bank; semantic deduplication ignores banks.
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'flux/'+digest([p,sorted(map(str,values))])));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'));answers=[]
 for value in values:
  value=number(value);aid=str(uuid.uuid5(uuid.UUID(fid),'math/'+value));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
 rng.shuffle(answers);correct=next(a[':answer/id'] for a in answers if value_parse(a[':answer/value'])==A)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':RAW[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'source_basis':CAPTURE['basis'],'source_refs':[profile],'dependencies':{'sympy':sp.__version__},'assets':assets,'source_replay':at_source,'inferred_source_key':profile=='q-127199','fingerprint':task_key(p)}}

def task_key(p):
 # Ignore axis/sign aliases for uniform fields; radial sign changes flux direction.
 c=sp.Rational(p['c']);return digest(['uniform',str(abs(c)),p['L']]) if p['axis']!='radial' else digest(['radial',str(c),p['L']])
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED,'hard'),required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
 if a.difficulty not in SUPPORTED:raise SystemExit('unsupported: hard; see classification.md')
 rs=[];used=set()
 for offset in range(max(256,a.count*16)):
  if len(rs)==a.count:break
  r=generate(a.difficulty,a.seed+offset,template=a.template,profile=a.profile,output_dir=a.output_dir);fp=r['generation']['fingerprint']
  if fp in used:continue
  used.add(fp);rs.append(r)
 if len(rs)<a.count:raise SystemExit('finite-limit: requested count exceeds bounded distinct sampler/domain')
 if a.format=='json':print(json.dumps(rs,ensure_ascii=False,indent=2))
 else:
  for r in rs:
   q=r['question'];print(q[':question/problem']+'\n\n'+'\n'.join('- $'+x[':answer/value']+'$' for x in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n\n---')
if __name__=='__main__':main()
