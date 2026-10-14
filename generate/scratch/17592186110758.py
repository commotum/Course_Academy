#!/usr/bin/env python3
"""Bounded, source-backed tangent/cotangent radio questions; no database writes."""
import argparse,copy,functools,hashlib,json,math,os,random,re,sys,uuid
from pathlib import Path
try: import sympy as sp
except ImportError:
 if __name__=='__main__':
  runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186110758
KP_UUID='74d05ad6-7e4a-5c50-92d1-ca4b2f00cbb1'
TITLE='Computing a Tangent or Cotangent Using the Pythagorean Identity'
VERSION='unit-circle-trig-1'
HERE=Path(__file__).resolve().with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('easy','moderate')
DATA={
 'q-64974':dict(n=4,d=3,known='y',target='cot',level=None),
 'q-65073':dict(n=45,d=7,known='y',target='tan',level='easy'),
 'q-124789':dict(n=14,d=5,known='y',target='tan',level='moderate'),
 'q-124791':dict(n=12,d=5,known='x',target='tan',level='moderate'),
 'q-124796':dict(n=1,d=8,known='x',target='tan',level='easy'),
 'q-64730':dict(n=2,d=2,known='y',target='tan',level='easy'),
 'q-65072':dict(n=9,d=5,known='y',target='tan',level='easy'),
 'q-65075':dict(n=17,d=9,known='x',target='cot',level='easy')}
PRIMARY={'easy':'q-65072','moderate':'q-124789'}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(x):return sp.latex(sp.simplify(x)).replace(' ','')
@functools.lru_cache(None)
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def parse_math(t):
 t=t.replace(' ','').replace('\\dfrac','\\frac')
 while '\\sqrt{' in t or '\\frac{' in t:
  old=t;t=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',t);t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
  if old==t:raise ValueError(t)
 t=re.sub(r'(\d|\))sqrt\(',r'\1*sqrt(',t)
 return sp.simplify(sp.sympify(t))
def values(profile,p):
 n,d=sp.Integer(p['n']),sp.Integer(p['d']);m=d*d-n;k=sp.sqrt(n)/d;o=sp.sqrt(m)/d
 x,y=(k,o) if p['known']=='x' else (o,k);correct=sp.simplify(y/x if p['target']=='tan' else x/y)
 if profile=='q-65072':bank=[1/o,k,o,correct,1/correct]
 elif profile=='q-124789':bank=[sp.sqrt(n+40)/m,sp.sqrt(n+1)/m,1/correct,sp.sqrt(n)/m,correct]
 else:bank=[parse_math(a[':answer/value']) for a in sources()[profile][':question/answer-fields'][0][':answer-field/choices']]
 return [sp.simplify(v) for v in bank],correct

def allowed(level,profile,p,replay=False):
 if profile not in DATA or set(p)!=set(DATA[profile]):return False
 if type(p['n']) is not int or type(p['d']) is not int or not 0<p['n']<p['d']**2:return False
 if replay:return p==DATA[profile]
 if level not in SUPPORTED_LEVELS or p['level']!=level:return False
 if profile not in PRIMARY.values():return profile!='q-64730' and p==DATA[profile] and level==p['level']
 if p['known']!='y' or p['target']!='tan':return False
 n,d=p['n'],p['d'];m=d*d-n
 if level=='easy':
  if not (5<=d<=30 and math.isqrt(n)**2==n and math.isqrt(m)**2==m):return False
 else:
  if not (3<=d<=8 and 1<=n<d*d and math.isqrt(n)**2!=n and math.isqrt(m)**2!=m):return False
  if sp.sqrt(sp.Rational(n,m)).is_Rational:return False
 bank,correct=values(profile,p)
 return all(v.is_real and v.is_finite for v in bank) and len(set(map(str,bank)))==5 and sum(sp.simplify(v-correct)==0 for v in bank)==1

def candidates(level):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported '+str(level)+': no source-backed hard template')
 profile=PRIMARY[level]
 for d in range(5,31) if level=='easy' else range(3,9):
  for n in range(1,d*d):
   p=dict(DATA[profile],n=n,d=d)
   if allowed(level,profile,p):yield dict(profile=profile,parameters=p)
 for profile,p in DATA.items():
  if profile not in (PRIMARY[level],'q-64730') and p['level']==level:yield dict(profile=profile,parameters=dict(p))

def replacements(profile,p):
 n,d=p['n'],p['d'];m=d*d-n
 if profile=='q-65072':return {3:str(math.isqrt(n)),5:str(d),9:str(n),25:str(d*d),16:str(m),4:str(math.isqrt(m))}
 if profile=='q-124789':return {14:str(n),5:str(d),25:str(d*d),11:str(m),154:str(n*m)}
 return {}
def parameterize(text,profile,p):
 table=replacements(profile,p)
 return re.sub(r'\d+',lambda m:table.get(int(m[0]),m[0]),text)

def task_fingerprint(p):
 # Swapping axes, reciprocal function, a different bank or a scaled fraction
 # does not create fresh mathematics. Count unordered squared coordinates.
 s=sp.Rational(p['n'],p['d']**2)
 return digest(sorted([str(s),str(1-s)]))
def fingerprint(q):
 text=q[':question/problem'];m=re.search(r'Given that the \$([xy])\$-coordinate.*? is \$(.*?)(?:,\$|\$)',text)
 if not m:raise ValueError('Missing printed coordinate')
 given=parse_math(m[2]);s=sp.simplify(given**2)
 return digest(sorted([str(s),str(1-s)]))

def render_plots(p,output_dir):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 from matplotlib.patches import Wedge
 output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
 k=float(sp.sqrt(p['n'])/p['d']);o=float(sp.sqrt(p['d']**2-p['n'])/p['d']);x,y=(k,o) if p['known']=='x' else (o,k)
 refs={}
 for role in ('prompt','solution'):
  path=output_dir/(digest({'version':VERSION,'parameters':p,'role':role})+'.png')
  if not path.exists():
   fig,ax=plt.subplots(figsize=(4.1,4.1),dpi=120);fig.subplots_adjust(.07,.05,.94,.94)
   ax.set_aspect('equal');ax.set_xlim(-1.95,1.95);ax.set_ylim(-1.95,1.95)
   ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_xticklabels(['−1','','1']);ax.set_yticklabels(['−1','','1']);ax.grid(color='#bbbbbb',lw=.6)
   for spine in ax.spines.values():spine.set_visible(False)
   ax.tick_params(length=0);t=np.linspace(0,2*np.pi,721);ax.plot(np.cos(t),np.sin(t),color='#2877b9',lw=1.7)
   for a,b in [((-1.95,0),(1.95,0)),((0,-1.95),(0,1.95))]:ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color='black',lw=1.5))
   ax.text(1.88,-.15,'$x$');ax.text(.07,1.83,'$y$');ax.plot([0,x],[0,y],color='black',lw=1.4);ax.plot(x,y,'ko',ms=3)
   angle=math.degrees(math.atan2(y,x));ax.add_patch(Wedge((0,0),.35,0,angle,color='#e7a600'))
   ax.text(.43*math.cos(math.radians(angle/2)),.43*math.sin(math.radians(angle/2)),'$\\theta$')
   ax.annotate('$P$' if role=='prompt' else '$P(\\cos\\theta,\\sin\\theta)$',(x,y),xytext=(4,8),textcoords='offset points',fontsize=10 if role=='prompt' else 9)
   fig.savefig(path,metadata={'Software':VERSION});plt.close(fig)
  refs[role]=str(path)
 return refs

def generate(level,seed=0,template=None,parameters=None,profile=None,replay=False,output_dir=None):
 profile=profile or template or PRIMARY.get(level)
 if parameters is None:
  pool=list(candidates(level));random.Random(seed).shuffle(pool);entry=next(e for e in pool if e['profile']==profile);p=entry['parameters']
 else:p=dict(parameters)
 if not allowed(level,profile,p,replay):raise ValueError('Outside bounded profile domain')
 src=sources()[profile];bank,correct=values(profile,p);problem=parameterize(src[':question/problem'],profile,p);solution=parameterize(src.get(':question/worked-solution',''),profile,p)
 # Original numeric/asset parameters retain original layout and bytes for replay.
 # Changed geometry is always drawn from the same coordinates.
 assets={}
 if p!=DATA[profile]:
  assets=render_plots(p,output_dir or HERE/'assets')
  problem=re.sub(r'!\[\]\([^)]*\)',lambda _:f"![]({assets['prompt']})",problem)
  solution=re.sub(r'!\[\]\([^)]*\)',lambda _:f"![]({assets['solution']})",solution)
 key=digest({'version':VERSION,'profile':profile,'parameters':p,'bank':list(map(str,bank))});qid=str(uuid.uuid5(uuid.UUID(KP_UUID),key));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 choices=[]
 for i,v in enumerate(bank):
  original=src[':question/answer-fields'][0][':answer-field/choices'][i][':answer/value']
  value=original if sp.simplify(parse_math(original)-v)==0 else tex(v)
  choices.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i)+':'+str(v))),':answer/type':':answer.type/math',':answer/value':value})
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if ':answer-field/correct' in src[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',choices[next(i for i,v in enumerate(bank) if sp.simplify(v-correct)==0)][':answer/id']]
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if p['level']:q[':question/difficulty']=':question.difficulty/'+p['level']
 if solution:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'parameters':p,'template':profile,'bank_profile':profile,'source_id':profile,'mathematical_fingerprint':task_fingerprint(p),'assets':assets,'eligible_for_learning':bool(p['level'] and solution and ':answer-field/correct' in field and len(set(map(str,bank)))==5),'dependencies':{'sympy':sp.__version__}}}
def batch(level,count,seed=0):
 pool=list(candidates(level));random.Random(seed).shuffle(pool);records=[];used=set()
 for entry in pool:
  fp=task_fingerprint(entry['parameters'])
  if fp in used:continue
  records.append(generate(level,seed,profile=entry['profile'],parameters=entry['parameters']));used.add(fp)
  if len(records)==count:return records
 raise ValueError(f'Finite domain: requested {count}, available {len(records)}')
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();records=batch(a.difficulty,a.count,a.seed);print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
