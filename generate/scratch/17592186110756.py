"""Reciprocal ratio from one unit-circle coordinate; source-backed moderate band.

Five complete observed bank profiles are retained independently. Offset and
radicand substitutions whose error interpretation is unknown remain explicit
observed expression recipes. They are not explained to the learner as mistakes.
Easy/hard have no validated source-backed band; CLI rejects them explicitly.
"""
import argparse, functools, hashlib, json, math, os, random, sys, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-17592186110756-mpl')
D=Path(__file__).with_suffix(''); ROOT=D.parents[2]
SOURCE=json.loads((D/'source.json').read_text());KP_ID=17592186110756
KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='unit-circle-reciprocal-1.0';SUPPORTED=('moderate',)
PROFILES={
 'y-rational':{'source':17592186110900,'axis':'y','original':{'b':5,'r':1}},
 'x-rational':{'source':17592186259728,'axis':'x','original':{'b':3,'r':1}},
 'y-radical-signed':{'source':17592186335785,'axis':'y','original':{'b':3,'r':3}},
 'x-radical':{'source':17592186335786,'axis':'x','original':{'b':5,'r':15}},
 'y-radical-offset':{'source':17592186354407,'axis':'y','original':{'b':3,'r':2}},
}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def values(profile,p):return _values(profile,int(p['b']),int(p['r']))
@functools.lru_cache(maxsize=None)
def _values(profile,bval,rval):
 b,r=map(sp.Integer,(bval,rval));d=b*b-r
 assert b in range(3,9) and 0<r<b*b and sp.sqrt(d).is_integer is not True
 if 'rational' in profile:assert r==1
 else:assert r>1 and sp.sqrt(r).is_integer is not True
 c,s=sp.sqrt(d).as_coeff_Mul();s=sp.simplify(s*s);assert c.is_Integer and s.is_Integer
 known=sp.sqrt(r)/b;missing=sp.sqrt(d)/b;correct=sp.simplify(1/missing)
 if profile=='y-rational':bank=[(b+4)*sp.sqrt(s)/c,b*sp.sqrt(s)/(b+4),sp.sqrt(s)/c,correct,(b+2)*sp.sqrt(s)/(c*s)]
 elif profile=='x-rational':bank=[correct,c*sp.sqrt(2*b)/b,(b+2)*sp.sqrt(s)/c,b*sp.sqrt(b)/c,b/c]
 elif profile=='y-radical-signed':bank=[-known/missing,-correct,correct/b,known/missing,correct]
 elif profile=='x-radical':bank=[correct,b*sp.sqrt(b)/(c*s),2*b*sp.sqrt(b)/(c*s),missing,b]
 else:bank=[d/r,sp.sqrt(d)/r,(b+2)/sp.sqrt(d),correct,d/b]
 bank=list(map(sp.simplify,bank))
 assert all(sp.simplify(a-z)!=0 for i,a in enumerate(bank) for z in bank[i+1:]),'Colliding complete bank'
 assert sum(sp.simplify(a-correct)==0 for a in bank)==1
 return known,missing,correct,bank

@functools.lru_cache(maxsize=None)
def domain(profile):
 cases=[]
 for b in range(3,9):
  for r in ([1] if 'rational' in profile else range(2,b*b)):
   p={'b':b,'r':r}
   try:values(profile,p)
   except AssertionError:continue
   cases.append(p)
 return cases

def render_plots(axis,p,output_dir):
 """Exact QI coordinate controls P, radius, angle, and solution point label."""
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import Wedge
 known=sp.sqrt(p['r'])/p['b'];missing=sp.sqrt(p['b']**2-p['r'])/p['b']
 x,y=(missing,known) if axis=='y' else (known,missing)
 output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True);assets={}
 for role in ('prompt','solution'):
  key=digest({'axis':axis,'parameters':p,'role':role,'version':VERSION});path=output_dir/(key+'.png')
  if not path.exists():
   fig,ax=plt.subplots(figsize=(4.3,4.3),dpi=140);theta=float(sp.atan2(y,x));t=sp.pi
   import numpy as np
   angles=np.linspace(0,2*np.pi,500);ax.plot(np.cos(angles),np.sin(angles),color='#2c78b8',lw=1.8)
   ax.set(xlim=(-1.35,1.35),ylim=(-1.35,1.35),aspect='equal');ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.grid(color='#dddddd',lw=.5)
   for s in ax.spines.values():s.set_visible(False)
   ax.annotate('',(1.30,0),(-1.30,0),arrowprops={'arrowstyle':'->','lw':1.2});ax.annotate('',(0,1.30),(0,-1.30),arrowprops={'arrowstyle':'->','lw':1.2})
   ax.text(1.30,-.13,'$x$');ax.text(.06,1.26,'$y$');ax.plot([0,float(x)],[0,float(y)],color='black',lw=1.5);ax.scatter([float(x)],[float(y)],color='black',s=14)
   ax.add_patch(Wedge((0,0),.25,0,theta*180/math.pi,color='#edae00'));ax.text(.32*math.cos(theta/2),.32*math.sin(theta/2),r'$\theta$',fontsize=11)
   label=r'$P$' if role=='prompt' else r'$P(\cos\theta,\sin\theta)$'
   # Keep the long solution label on its own line above the figure.
   if role=='solution':ax.set_title(label,fontsize=11,pad=8)
   else:ax.annotate(label,(float(x),float(y)),xytext=(6,5),textcoords='offset points',fontsize=12)
   fig.tight_layout();fig.savefig(path,metadata={'Software':VERSION});plt.close(fig)
  assets[role]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'renderer':'matplotlib','axis':axis,'parameters':p,'point':[str(x),str(y)],'role':role}
 return assets

def generate(difficulty,seed,template=None,parameters=None,profile=None,output_dir=None,plots=True):
 if difficulty not in SUPPORTED:raise ValueError(f'Unsupported difficulty: {difficulty}; see capabilities.json')
 name=profile or template or random.Random(seed).choice(list(PROFILES));assert name in PROFILES
 p=parameters or random.Random(seed).choice(domain(name));p={k:int(p[k]) for k in ('b','r')}
 known,missing,correct,bank=values(name,p);axis=PROFILES[name]['axis'];given='sin' if axis=='y' else 'cos';other='cos' if axis=='y' else 'sin';target='sec' if axis=='y' else 'csc';b,r=p['b'],p['r'];d=b*b-r
 lx=sp.latex;assets=render_plots(axis,p,output_dir or D/'plots') if plots else {}
 img=lambda role:f"![]({assets[role]['path']})\n\n" if assets else ''
 prompt=img('prompt')+f'The diagram above shows the unit circle. Given that the ${axis}$-coordinate of the point $P$ is ${lx(known)}$, use the Pythagorean identity to find $\\{target}\\theta$.'
 solution=img('solution')+rf'''Any point $(x,y)$ on the unit circle is related to the central angle $\theta$ as follows:

$$x=\cos\theta,\qquad y=\sin\theta.$$

We're given that ${axis}={lx(known)}$ at the point $P$. Therefore, we have

$$\{given}\theta={lx(known)}.$$

We can use the Pythagorean identity to find $\{other}\theta$:

$$\begin{{aligned}}
\sin^2\theta+\cos^2\theta &= 1 \\
\{other}^2\theta &= 1-\{given}^2\theta \\
\{other}\theta &= \pm\sqrt{{1-\{given}^2\theta}}.
\end{{aligned}}$$

Substituting $\{given}\theta={lx(known)}$ gives

$$\begin{{aligned}}
\{other}\theta &= \pm\sqrt{{1-\left({lx(known)}\right)^2}} \\
&=\pm\sqrt{{1-\frac{{{r}}}{{{b*b}}}}} \\
&=\pm\sqrt{{\frac{{{d}}}{{{b*b}}}}} \\
&=\pm {lx(missing)}.
\end{{aligned}}$$

We select the positive answer since $\{other}\theta$ is positive in the first quadrant. So, $\{other}\theta={lx(missing)}$.

Knowing that $\{target}\theta=\dfrac{{1}}{{\{other}\theta}}$, we have

$$\{target}\theta=\frac{{1}}{{{lx(missing)}}}=\frac{{{b}}}{{{lx(sp.sqrt(d))}}}.$$

Finally, we rationalize the denominator.

$$\begin{{aligned}}
\{target}\theta &= \frac{{{b}}}{{{lx(sp.sqrt(d))}}} \\
&=\frac{{{b}}}{{{lx(sp.sqrt(d))}}}\cdot\frac{{{lx(sp.sqrt(d))}}}{{{lx(sp.sqrt(d))}}} \\
&=\frac{{{b}\,{lx(sp.sqrt(d))}}}{{{d}}} \\
&={lx(correct)}.
\end{{aligned}}$$'''
 identity=digest({'version':VERSION,'profile':name,'axis':axis,'known':str(known),'bank':list(map(str,bank))});qid=uid('question:'+identity);fid=uid('field:'+qid+':selection')
 choices=[{':answer/id':uid('answer:'+fid+':'+str(a)),':answer/type':':answer.type/math',':answer/value':lx(a)} for a in bank];ci=next(i for i,a in enumerate(bank) if a==correct)
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',choices[ci][':answer/id']],':answer-field/choices':choices}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':name,'parameters':p,'domain':'b=3..8; rational r=1; radical r=2..b^2-1, non-square r; non-square complement; reject bank collisions','source_question':PROFILES[name]['source'],'source_basis':SOURCE['basis'],'eligible_for_learning':True,'evidence_only':False,'assets':assets,'mathematical_fingerprint':digest({'axis':axis,'coordinate':str(known),'target':target,'quadrant':1}),'dependencies':{'python':sys.version,'sympy':sp.__version__}}}

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template',choices=list(PROFILES));args=ap.parse_args()
 if args.difficulty not in SUPPORTED:ap.error('Unsupported band; see '+str(D/'capabilities.json'))
 pool=[(name,p) for name in ([args.template] if args.template else PROFILES) for p in domain(name)];random.Random(args.seed).shuffle(pool);out=[];seen=set()
 for name,p in pool:
  known=values(name,p)[0];key=(PROFILES[name]['axis'],str(known))
  if key in seen:continue
  seen.add(key);out.append(generate(args.difficulty,args.seed,name,parameters=p))
  if len(out)>=args.count:break
 if len(out)!=args.count:ap.error(f'Finite distinct-task limit: requested {args.count}, produced {len(out)}')
 print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
