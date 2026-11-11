#!/usr/bin/env python3
"""Seeded internal-division vector practice. All assets belong to OUTPUT_DIR."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math,os,random,re,uuid
from math_format import normalize_prose,normalize_tex,validate_generated_record
VERSION='internal-vectors-3'
KP={'db_id':17592186096653,'id':'feae36e7-ae88-5f3a-957f-e65a92e399ad'}
HERE=Path(__file__).resolve().parent

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:ratio-v2:'+s))
def tex(x):
 x=F(x);return ('-' if x<0 else '')+(str(abs(x.numerator)) if x.denominator==1 else r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}')
def vec(s):return r'\overrightarrow{'+s+'}'
def expr(a,b,u,v):
 out=''
 for x,n in [(F(a),u),(F(b),v)]:
  if not x:continue
  out+=('-' if x<0 else '+' if out else '')+('' if abs(x)==1 else tex(abs(x)))+n
 return out or '0'
def output_dir():
 if not os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'):raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets')
 p=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']).resolve();p.mkdir(parents=True,exist_ok=True);return p

def diagram(p):
 folder=output_dir();name='ratio-'+digest(p)[:24]+'.png';path=folder/name
 if path.exists():return str(path)
 os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-mpl')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 flip=p['mirror'];O=(0,0);A=(-3*flip,3);B=(5*flip,3);t=F(p['r'],p['r']+p['s']);X=(float(A[0]+t*(B[0]-A[0])),3)
 fig,ax=plt.subplots(figsize=(6.4,3.5),dpi=140)
 ax.plot([A[0],B[0]],[3,3],color='#202c36',lw=1.7)
 for P,n,sgn in [(A,p['u'],p['sa']),(B,p['v'],p['sb'])]:
  start,end=(O,P) if sgn==1 else (P,O)
  ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color='#246caf',lw=2))
  ax.text(P[0]*.51+(-.45 if P[0]<0 else .18),1.49,'$'+n+'$',fontsize=17,color='#174d80')
 start,end=(O,X) if p['target']==1 else (X,O)
 ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color='#d08000',lw=2))
 for lab,P in [('O',O),(p['A'],A),(p['B'],B),(p['X'],X)]:
  ax.text(P[0]-.10,P[1]+(.15 if lab!='O' else -.37),'$'+lab+'$',fontsize=16)
 ax.set(xlim=(min(A[0],B[0])-.8,max(A[0],B[0])+.8),ylim=(-.55,3.7));ax.set_aspect('equal');ax.axis('off');fig.tight_layout(pad=.3)
 fig.savefig(path,facecolor='white',metadata={'Software':'Course Academy ratio generator'});plt.close(fig);return str(path)

def derivation(p):
 A,B,X,u,v,r,s,sa,sb,target=[p[k] for k in ('A','B','X','u','v','r','s','sa','sb','target')]
 t=F(r,r+s);a=F(sa*s,r+s);b=F(sb*r,r+s)
 # Ordered direction conversion -> segment -> ratio -> path -> collected result.
 rows=[vec('O'+A)+'='+expr(sa,0,u,v),vec('O'+B)+'='+expr(0,sb,u,v)]
 full=expr(-sa,sb,u,v);oa=expr(sa,0,u,v)
 sol='First express both endpoint vectors in the directions away from $O$:\n\n$$\n'+r'\qquad '.join(rows)+' .\n$$\n\n'
 sol+='Trace the path from $'+A+'$ through $O$ to $'+B+'$:\n\n$$\n'+vec(A+B)+'='+vec(A+'O')+'+'+vec('O'+B)+'='+full+'.\n$$\n\n'
 sol+=f'The ratio ${A+X}:{X+B}={r}:{s}$ gives ${r+s}$ parts in the whole segment. Thus\n\n$$\n'+vec(A+X)+'='+tex(t)+vec(A+B)+'='+tex(t)+'('+full+').\n$$\n\n'
 final=expr(a,b,u,v)
 sol+='Add along the path $O\\to '+A+'\\to '+X+'$ and collect coefficients:\n\n$$\n'+r'\begin{aligned}'+vec('O'+X)+'&='+vec('O'+A)+'+'+vec(A+X)+r'\\'+'&='+oa+'+'+tex(t)+'('+full+')'+r'\\'+'&='+final+r'.\end{aligned}'+'\n$$'
 if target==-1:
  sol+='\n\nThe requested vector has the reverse direction, so negate both coefficients:\n\n$$\n'+vec(X+'O')+'=-'+vec('O'+X)+'='+expr(-a,-b,u,v)+'.\n$$'
 return sol,(target*a,target*b)

def fields_for(identity,kind,values,correct,rng):
 fs=[]
 for i,bank in enumerate(values):
  key='selection' if kind=='radio' else 'field-'+str(i+1);fid=uid(identity+key)
  choices=[{':answer/id':uid(fid+x),':answer/type':':answer.type/math',':answer/value':normalize_tex(x)} for x in bank]
  cid=choices[correct[i]][':answer/id']
  if kind=='radio':rng.shuffle(choices)
  fs.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]})
 return fs

def make(level,p,kind='blank',profile='double-first',seed=0,bank_override=None,source=None):
 p=dict(p);A,B,X,u,v=[p[k] for k in ('A','B','X','u','v')];r,s=p['r'],p['s']
 if min(r,s)<1 or p['sa'] not in (-1,1) or p['sb'] not in (-1,1) or p['target'] not in (-1,1):raise ValueError('invalid instance')
 image=diagram(p);target=vec(('O'+X) if p['target']==1 else (X+'O'))
 givens=[vec('O'+A if p['sa']==1 else A+'O')+'='+u,vec('O'+B if p['sb']==1 else B+'O')+'='+v]
 prompt=f'![]({image})\n\nIn the diagram, ${X}$ lies on the segment ${A+B}$. The given vectors are $'+givens[0]+'$ and $'+givens[1]+f'$. The lengths satisfy ${A+X}:{X+B}={r}:{s}$.'
 prompt+='\n\nExpress $'+target+'$ in terms of $'+u+'$ and $'+v+'$.'
 sol,co=derivation(p);a,b=co
 if kind=='blank':
  prompt+=' Fill in both coefficients, including their signs.\n\n$'+target+'=$ {{field-1}} $'+u+'+$ {{field-2}} $'+v+'$'
  banks=[[tex(a)],[tex(b)]];correct=[0,0]
 else:
  if bank_override is not None:pairs=bank_override
  else:
   t=F(r,r+s);e=F(2*r,2*r+s) if profile=='double-first' else F(r,r+2*s)
   weights=[t,1-t,e,1-e,F(1,2)]
   if len(set(weights))!=5:raise ValueError('bank collision')
   pairs=[(p['target']*p['sa']*(1-w),p['target']*p['sb']*w) for w in weights]
  if len(set(pairs))!=5 or pairs.count(co)!=1:raise ValueError('invalid complete bank')
  banks=[[target+'='+expr(x,y,u,v) for x,y in pairs]];correct=[pairs.index(co)]
 prompt=normalize_prose(prompt);sol=normalize_prose(sol)
 # Absolute output locations are presentation plumbing, never content identity.
 ident=digest({'version':VERSION,'level':level,'prompt':prompt.replace(image,Path(image).name),'solution':sol,'banks':banks})
 row={'knowledge_point':KP,'question':{':question/id':uid(ident),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':fields_for(ident,kind,banks,correct,random.Random(seed))},'generation':{'version':VERSION,'seed':seed,'parameters':p,'template':kind,'profile':profile,'source_question':source,'content_fingerprint':ident}}
 return validate_generated_record(row)

def source_parameters(q):
 prompt=q[':question/problem'];m=re.search(r'([A-Z])([A-Z]):\s*\2([A-Z])\s*=\s*(\d+):\s*(\d+)',prompt)
 A,X,B,r,s=m.groups();u=re.search(r'\{O'+A+r'\}=([a-z])',prompt)[1];v=re.search(r'\{O'+B+r'\}=([a-z])',prompt)[1]
 return dict(A=A,B=B,X=X,u=u,v=v,r=int(r),s=int(s),sa=1,sb=1,target=1,mirror=1)

def replay_source():
 from legacy_banks import BANKS,R,S
 rows=[]
 for q in json.loads((HERE/'source_cases.json').read_text()):
  p=source_parameters(q);kind=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1];pairs=None
  if kind=='radio':pairs=[tuple(F(str(z.subs({R:p['r'],S:p['s']}))) if hasattr(z,'subs') else F(z) for z in pair) for pair in BANKS[q[':question/math-academy-id']]]
  rows.append(make('moderate',p,kind,'source:'+q[':question/math-academy-id'],bank_override=pairs,source=q[':question/id']))
 return rows

def radio_signature(row):
 # This sampler serves radio only with positive internal-division coefficients.
 field=row['question'][':question/answer-fields'][0]
 choices=field[':answer-field/choices'];cid=field[':answer-field/correct'][1]
 index=next(i for i,a in enumerate(choices) if a[':answer/id']==cid)
 scalars=[]
 for a in choices:
  match=re.search(r'\\frac\{(\d+)\}\{(\d+)\}',a[':answer/value'].split('=')[1])
  scalars.append(F(int(match[1]),int(match[2])))
 return index,sorted(scalars).index(scalars[index])

def sample(level,count,seed):
 rng=random.Random(seed);seen=set();out=[]
 # Select distinct essential reduced ratios before cosmetic details. Exhaustion
 # resets the cycle; this is a finite mathematical family, not seed-dependent.
 bound=12 if level=='moderate' else 5
 ratios=sorted({F(r,s) for r in range(1,bound+1) for s in range(1,bound+1)})
 attempts=0
 while len(out)<count:
  attempts+=1
  if attempts>max(1000,count*100):raise ValueError('batch constraints exhausted')
  available=[x for x in ratios if x not in seen]
  if not available:seen.clear();available=ratios
  role=rng.choice([-1,0,1]);eligible=[x for x in available if (x>1)-(x<1)==role]
  ratio=rng.choice(eligible or available)
  A,B,X=rng.sample('ABCDEFGHJKLMNPQRSTUVWXYZ',3);u,v=rng.sample('abcdefghkmnpqrstuvw',2)
  sa,sb,target=(1,1,1) if level!='hard' else rng.choice([(a,b,t) for a in [-1,1] for b in [-1,1] for t in [-1,1] if (a,b,t)!=(1,1,1)])
  p=dict(A=A,B=B,X=X,u=u,v=v,r=ratio.numerator,s=ratio.denominator,sa=sa,sb=sb,target=target,mirror=rng.choice([-1,1]))
  kind='blank' if level=='hard' else rng.choice(['blank','radio']);profile=rng.choice(['double-first','double-second'])
  if kind=='radio':
   t=F(p['r'],p['r']+p['s']);e=F(2*p['r'],2*p['r']+p['s']) if profile=='double-first' else F(p['r'],p['r']+2*p['s'])
   if len({t,1-t,e,1-e,F(1,2)})<5:kind='blank'
  row=make(level,p,kind,profile,seed=rng.getrandbits(64))
  if kind=='radio':
   radios=[x for x in out if x['generation']['template']=='radio']
   group=[x for x in radios if (x['generation']['parameters']['r']<x['generation']['parameters']['s'])==(p['r']<p['s'])]
   # A short visible radio subgroup must not repeat one bank-only answer rule.
   # Try the other complete plausible error profile, then resample mathematics.
   if len(group)==1 and radio_signature(row)[1]==radio_signature(group[0])[1]:
    other='double-second' if profile=='double-first' else 'double-first'
    try:row=make(level,p,kind,other,seed=rng.getrandbits(64))
    except ValueError:continue
    if radio_signature(row)[1]==radio_signature(group[0])[1]:continue
   compare=group if len(group)==1 else radios if len(radios)==1 else []
   if compare:
    while radio_signature(row)[0]==radio_signature(compare[0])[0]:
     row=make(level,p,kind,row['generation']['profile'],seed=rng.getrandbits(64))
  seen.add(ratio);out.append(row)
 return out

def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json'],default='json');a.add_argument('--replay-source',action='store_true');args=a.parse_args()
 if args.count<0:a.error('count must be nonnegative')
 rows=replay_source() if args.replay_source else sample('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
