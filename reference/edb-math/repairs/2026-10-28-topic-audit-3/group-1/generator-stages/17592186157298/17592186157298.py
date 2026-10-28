from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
#!/usr/bin/env python3
"""Moderate polar-coordinate circular-cap templates. Easy/hard unsupported.
Positive homothety preserves curve/line roles, angular sector and workload.
Each profile preserves its entire source bank; scale 1 replays the source.
CLI: .venv/bin/python generate/scratch/17592186157298.py --difficulty moderate --count 5 --seed 1 --format json
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import os
try:
 import sympy as sp
except ImportError:
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if interpreter.is_file() and str(interpreter)!=sys.executable:os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
os.environ.setdefault('MPLCONFIGDIR',str(_ca_asset_output(Path('matplotlib-cache')).parent/'matplotlib-cache'))
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).with_suffix(''); ROOT=HERE.parents[2]
SNAP=json.loads((HERE/'reference/initial/source.json').read_text())
KP=17592186157298; KP_UUID=SNAP['record'][':knowledge-point/id']; TITLE=SNAP['record'][':knowledge-point/title']
NAMESPACE=uuid.UUID('c1d9eb4a-d5cd-49f3-9e87-15a08a27207d'); VERSION='polar-caps-1-format-audit-9837-v1'
t,r,x,y=sp.symbols('t r x y',real=True); s=sp.Symbol('s',positive=True)
LOC={'t':t,'r':r,'x':x,'y':y,'s':s,'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sec':sp.sec,'csc':sp.csc}
def E(z):return sp.sympify(z,locals=LOC)
def tex(z):return sp.latex(sp.simplify(z),symbol_names={t:r'\theta'})
def uid(z):return str(uuid.uuid5(NAMESPACE,z))
def digest(z):return hashlib.sha256(json.dumps(_ca_material(z),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def eq(a,b):return sp.trigsimp(sp.simplify(a-b))==0
# Center, radius, line normal and offset, angular interval, Cartesian integrand.
# Offsets are positive; normal points into the shaded cap. Fixed angular roles
# are instructional constraints: full cap vs quadrant half-cap is meaningful.
DATA={
'q-83789':([0,1],1,[0,1],1,['pi/4','3*pi/4'],'y**2'),
'q-83980':([0,0],4,[1,0],'2*sqrt(2)',['0','pi/4'],'y/x'),
'q-161101':([-1,1],'sqrt(2)',[-1,1],2,['pi/2','pi'],'x*y'),
'q-85065':([-2,0],2,[-1,0],3,['5*pi/6','7*pi/6'],'x*y'),
'q-85067':([0,0],1,[-1,0],'sqrt(2)/2',['3*pi/4','pi'],'sqrt(x**2+y**2)'),
'q-85182':([2,0],2,[1,0],3,['-pi/6','0'],'y/x**2'),
'q-161100':([1,1],'sqrt(2)',[1,1],2,['0','pi/2'],'x'),
'q-85062':([0,-2],2,[0,-1],3,['-2*pi/3','-pi/3'],'x**2+y**2'),
'q-85181':([0,2],2,[0,1],3,['pi/2','2*pi/3'],'x**2/(x**2+y**2)'),
'q-83979':([1,0],1,[1,0],1,['-pi/4','pi/4'],'x+y'),
'q-83975':([0,0],2,[0,1],'sqrt(2)',['pi/4','pi/2'],'x**2')}
# Tuple recipes: theta lower/upper, r lower/upper, angular factor, radial power.
# Each expression explicitly encodes the COMPLETE source option, including
# compound mistakes. s scales geometric limits, not angles or density.
BANKS={
'q-83789':[
['-pi/2','pi/2','s*sin(t)','2*s*sin(t)','sin(t)**2',3],['pi/4','3*pi/4',0,'2*s*sin(t)','sin(t)**2',3],
[0,'pi','s*csc(t)','2*s*sin(t)','sin(t)**2',3],[0,'pi',0,'2*s*sin(t)','sin(t)**2',3],['pi/4','3*pi/4','s*csc(t)','2*s*sin(t)','sin(t)**2',3]],
'q-83980':[
[0,'pi/4','2*s*sqrt(2)*sec(t)','4*s','tan(t)',1],[0,'pi/4','s*sqrt(2)*sec(t)','4*s','tan(t)',1],
['-pi/4','pi/4','2*s*sec(t)','4*s','tan(t)',1],[0,'pi/4',0,'4*s','tan(t)',2],[0,'4*s','2*s*sec(t)','4*s*cos(t)','tan(t)',1]],
'q-161101':[
['pi/2','pi','2*s/(sin(t)-cos(t))','2*s*(sin(t)-cos(t))','cos(t)*sin(t)',3],
['pi/2','pi','s/(sin(t)-cos(t))','s*(sin(t)-cos(t))','cos(t)*sin(t)',3],
['pi/2','3*pi/2','s/(sin(t)-cos(t))','2*s*(sin(t)-cos(t))','cos(t)*sin(t)',3],
['pi/2','3*pi/2','2*s/(sin(t)-cos(t))','2*s*(sin(t)-cos(t))','cos(t)*sin(t)',3],
['pi/2','pi','2*s/(sin(t)+cos(t))','2*s*(sin(t)+cos(t))','cos(t)*sin(t)',3]],
'q-85065':[
['-pi/6','pi/6','-s*sec(t)','-s*cos(t)','cos(t)*sin(t)',2],
['-3*s*sec(t)','-4*s*cos(t)','5*pi/6','7*pi/6','cos(t)*sin(t)',2],
['5*pi/6','7*pi/6','-3*s*sec(t)','-4*s*cos(t)','cos(t)*sin(t)',3],
[0,'pi/6','-4*s*sec(t)','-3*s*cos(t)','cos(t)*sin(t)',1],['pi/6','5*pi/6',0,'-4*s*cos(t)','cos(t)*sin(t)',3]],
'q-85067':[
['pi/2','pi','-s*sqrt(2)*sec(t)','s',1,1],['pi/4','3*pi/4','-s*sec(t)/sqrt(2)','s',1,3],
[0,'pi','s*sqrt(2)*sec(t)','s*sqrt(2)',1,3],['3*pi/4','pi','-s*sec(t)/sqrt(2)','s',1,2],['pi/4','pi','s*sec(t)/sqrt(2)','s*sqrt(2)',1,2]],
'q-85182':[
['-pi/6',0,'3*s','4*s','sec(t)*tan(t)',0],['-pi/6',0,'3*s*sec(t)','4*s*cos(t)','sec(t)**2',2],
['-pi/6','pi/6','3*s*sec(t)','4*s*cos(t)','sec(t)*tan(t)',3],['-pi/6',0,'3*s*sec(t)','4*s*cos(t)','sec(t)*tan(t)',0],['-pi/6',0,'3*s*sec(t)','4*s*cos(t)','tan(t)',-1]],
'q-161100':[
[0,'pi','s/(cos(t)+sin(t))','2*s*(cos(t)+sin(t))','cos(t)',2],
[0,'pi','2*s/sin(t)','2*s*(cos(t)+sin(t))','sin(t)',2],
[0,'pi/2','2*s/(2*cos(t)-sin(t))','2*s*(cos(t)+sin(t))','cos(t)',1],
[0,'pi/2','2*s/(cos(t)+sin(t))','2*s*(cos(t)+sin(t))','cos(t)',2],
[0,'pi/2','2*s/sin(t)','2*s*(cos(t)+sin(t))','cos(t)',1]],
'q-85062':[
['-pi/3','pi/3','-4*s*sin(t)','-3*s*csc(t)',1,1],['-2*pi/3','-pi/3','-s*csc(t)','-s*sin(t)',1,2],
['-pi/3','-pi/6','-4*s*csc(t)','-3*s*sin(t)',1,3],['-pi',0,'-s*csc(t)','-s*sin(t)',1,2],['-2*pi/3','-pi/3','-3*s*csc(t)','-4*s*sin(t)',1,3]],
'q-85181':[
['pi/2','2*pi/3','3*s*csc(t)','4*s*sin(t)','cos(t)**2',1],['pi/2','2*pi/3','3*s*csc(t)','4*s*sin(t)','cos(t)**2',2],
['pi/2','2*pi/3','3*s*csc(t)','4*s*sin(t)','cos(t)',-1],['pi/3','2*pi/3','3*s','4*s','cos(t)**2',-2],
[0,'2*pi/3','3*s','4*s*sin(t)','cos(t)**2',3]],
'q-83979':[
[0,'pi/4',0,'2*s*cos(t)','cos(t)+sin(t)',2],['-pi/6','pi/6','s*sec(t)','2*s*cos(t)','cos(t)+sin(t)',2],
['-pi/4','pi/4','s*csc(t)','2*s*sin(t)','cos(t)+sin(t)',2],[0,'pi/4','s','2*s*cos(t)','cos(t)+sin(t)',2],['-pi/4','pi/4','s*sec(t)','2*s*cos(t)','cos(t)+sin(t)',2]],
'q-83975':[
[0,'pi/2','s*csc(t)','s*sqrt(2)','cos(t)**2',3],[0,'pi/4','s*sqrt(2)','2*s*csc(t)','cos(t)**2',3],
['pi/4','3*pi/4','s*sqrt(2)*csc(t)','2*s*sin(t)','cos(t)**2',3],['pi/4','pi/2','s*sqrt(2)*csc(t)','2*s','cos(t)**2',3],['pi/4','pi/2','s*sqrt(2)','2*s*csc(t)','cos(t)**2',3]]}
ORIGINALS={q[':question/math-academy-id']:q for q in SNAP['record'][':knowledge-point/questions']}
CORRECT={sid:next(i for i,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices'])if a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id'])for sid,q in ORIGINALS.items()}
def bank(sid,scale):return [[E(z).subs(s,scale)for z in row]for row in BANKS[sid]]
def integral(row):
 a,b,lo,hi,h,p=row
 factor=''if h==1 else r'\left('+tex(h)+r'\right)'
 radial=''if p==0 else tex(r**p)
 return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+factor+r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+radial+r'\,\mathrm{d}r\,\mathrm{d}\theta'
def model(sid,scale):
 C,R,N,d,ab,f=DATA[sid];C=[E(z)*scale for z in C];R=E(R)*scale;N=list(map(E,N));d=E(d)*scale
 dot=N[0]*sp.cos(t)+N[1]*sp.sin(t)
 lo=sp.simplify(d/dot);hi=R if all(z==0 for z in C)else 2*(C[0]*sp.cos(t)+C[1]*sp.sin(t))
 return C,R,N,d,list(map(E,ab)),E(f),lo,hi
# Plot generator: same instance data controls polygon, labels and polar guides.
def render_plots(sid,scale):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 C,R,N,d,ab,f,lo,hi=model(sid,scale); key=digest([VERSION,sid,scale])[:24];assets={}
 for role in ('prompt','solution'):
  path=_ca_asset_output(HERE/'assets'/f'{key}-{role}.png');path.parent.mkdir(exist_ok=True)
  if not path.exists():
   a,b=map(float,ab);angles=np.linspace(a,b,260)
   lv=np.asarray(sp.lambdify(t,lo,'numpy')(angles))+np.zeros_like(angles);hv=np.asarray(sp.lambdify(t,hi,'numpy')(angles))+np.zeros_like(angles)
   px=np.r_[hv*np.cos(angles),(lv*np.cos(angles))[::-1]];py=np.r_[hv*np.sin(angles),(lv*np.sin(angles))[::-1]]
   fig,ax=plt.subplots(figsize=(5.6,4.6),dpi=145);ax.fill(px,py,color='#dcebf5',edgecolor='#3379a5',linewidth=1.6)
   extent=max(abs(px).max(),abs(py).max(),float(R),1);pad=0.20*extent
   ax.set_xlim(min(px.min(),0)-pad,max(px.max(),0)+pad);ax.set_ylim(min(py.min(),0)-pad,max(py.max(),0)+pad);ax.set_aspect('equal')
   ax.axhline(0,color='#555',lw=.7);ax.axvline(0,color='#555',lw=.7);ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0)
   ax.text(float(np.mean(px)),float(np.mean(py)),'$D$',color='#3379a5',ha='center')
   ax.set_title('$'+tex((x-C[0])**2+(y-C[1])**2)+'='+tex(R**2)+'$\n$'+tex(N[0]*x+N[1]*y)+'='+tex(d)+'$',fontsize=10,pad=10)
   if role=='solution':
    for angle in ab:
     av=float(angle);hval=float(hi.subs(t,angle));ax.plot([0,hval*np.cos(av)],[0,hval*np.sin(av)],'--',color='#d77e39',lw=.9)
    ax.text(.02,.02,'$'+tex(ab[0])+r'\leq\theta\leq '+tex(ab[1])+'$',transform=ax.transAxes,fontsize=10,bbox={'facecolor':'white','alpha':.85,'edgecolor':'none'})
   ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(path,metadata={'Software':VERSION});plt.close(fig)
  assets[role]=str(path.resolve())
 return assets

def generate(difficulty='moderate',seed=0,template=None,scale=None,plots=True):
 if difficulty!='moderate':raise ValueError('Unsupported difficulty: no easy/hard source evidence; do not relabel moderate templates')
 rng=random.Random(seed);sid=template or rng.choice(list(DATA));scale=int(scale if scale is not None else rng.randint(2,12))
 if not 1<=scale<=12:raise ValueError('Validated scale domain is integers 1..12')
 C,R,N,d,ab,f,lo,hi=model(sid,scale);options=bank(sid,scale);ci=CORRECT[sid]
 assets=render_plots(sid,scale)if plots else {};curve=tex((x-C[0])**2+(y-C[1])**2)+'='+tex(R**2);line=tex(N[0]*x+N[1]*y)+'='+tex(d)
 # Seed only selects mathematical data. It never changes a question's identity.
 prompt=('![]('+assets['prompt']+')\n\n'if plots else '')+'The region $D$ is enclosed between the curve $'+curve+'$ and the line $'+line+'$, as shown above. What is\n$$\\iint_D '+tex(f)+r'\,\mathrm{d}A$$'+'\nexpressed in polar coordinates?'
 transformed=sp.trigsimp(f.subs({x:r*sp.cos(t),y:r*sp.sin(t)},simultaneous=True)*r)
 # r>=0; the radical template simplifies sqrt(r^2) to r on that domain.
 transformed=sp.refine(transformed,sp.Q.positive(r))
 stages=['We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form',r'$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$','Notice that the region $D$ represents a portion of the disk of radius $'+tex(R)+'$ centered at $('+','.join(map(tex,C))+')$.','Cartesian and polar coordinates are connected by the following equations:',r'$$x=r\cos\theta,\qquad y=r\sin\theta.$$','With that in mind, let\'s now write our curves in polar coordinates.']
 if all(c==0 for c in C):stages+=['- For $'+curve+'$, we obtain $r='+tex(R)+'$.']
 else:
  eqn=sp.expand(((x-C[0])**2+(y-C[1])**2-R**2).subs({x:r*sp.cos(t),y:r*sp.sin(t)},simultaneous=True))
  stages+=['- For $'+curve+'$, we obtain',r'$$'+tex(eqn)+'=0'+r'\quad\Longleftrightarrow\quad r\left(r-\left('+tex(hi)+r'\right)\right)=0.$$','The boundary arc has $r='+tex(hi)+'$ for $r>0$.']
 stages+=['- For $'+line+'$, we get',r'$$'+tex(r*(N[0]*sp.cos(t)+N[1]*sp.sin(t)))+'='+tex(d)+r'\quad\Longrightarrow\quad r='+tex(lo)+'.$$']
 # Endpoints lie on the selected angular boundaries, which may be an axis or a circle-line intersection.
 endpoints=[(sp.simplify(hi.subs(t,a)*sp.cos(a)),sp.simplify(hi.subs(t,a)*sp.sin(a)))for a in ab]
 stages+=['Now, let\'s find the limits for the parameter $\\theta$. The endpoints of the selected arc are '+ ' and '.join('$('+tex(a)+','+tex(b)+')$'for a,b in endpoints)+'. So the shaded region lies between the polar lines $\\theta='+tex(ab[0])+'$ and $\\theta='+tex(ab[1])+'$.']
 if plots:stages+=['![]('+assets['solution']+')']
 stages+=['As a result, the region can be expressed in polar coordinates as',r'$$\Delta=\{(r,\theta):'+tex(lo)+r'\leq r\leq '+tex(hi)+r',\ '+tex(ab[0])+r'\leq\theta\leq '+tex(ab[1])+r'\}.$$','Therefore, using the change of variables formula, we obtain',r'$$\iint_D '+tex(f)+r'\,\mathrm{d}A=\iint_\Delta '+tex(transformed)+r'\,\mathrm{d}r\,\mathrm{d}\theta='+integral(options[ci])+'.$$']
 prompt=_ca_problem(prompt);solution=_ca_prose('\n\n'.join(stages));rendered=_ca_values([integral(row)for row in options])
 qid=uid('question:'+digest([VERSION,sid,scale,prompt,solution,rendered]));fid=uid(qid+':selection')
 choices=[{':answer/id':uid(fid+':recipe:'+str(i)),':answer/type':':answer.type/math',':answer/value':value}for i,value in enumerate(rendered)]
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]},'generation':{'version':VERSION,'template':sid,'profile':sid+':complete-bank','seed':seed,'parameters':{'scale':scale},'domain':'r >= 0; integer homothety 1..12; fixed depicted sector','source_basis':SNAP['basis'],'source_question_id':ORIGINALS[sid][':question/id'],'assets':assets,'eligible_for_learning':True,'evidence_only':False,'identity_excludes':['seed','choice order']}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template',choices=list(DATA));p.add_argument('--scale',type=int);args=p.parse_args()
 if args.difficulty not in ('moderate','all'):p.error('Only moderate is supported; easy/hard have no source evidence')
 candidates=[(sid,k)for sid in ([args.template]if args.template else DATA)for k in ([args.scale]if args.scale else range(2,13))];random.Random(args.seed).shuffle(candidates)
 if args.count>len(candidates):p.error('Finite domain exhausted: '+str(len(candidates))+' distinct candidates')
 out=[generate('moderate',args.seed+i,sid,k)for i,(sid,k)in enumerate(candidates[:args.count])]
 print(json.dumps(out,indent=2)if args.format=='json'else '\n\n---\n\n'.join(a['question'][':question/problem']+'\n\n'+a['question'][':question/worked-solution']for a in out))
if __name__=='__main__':main()
