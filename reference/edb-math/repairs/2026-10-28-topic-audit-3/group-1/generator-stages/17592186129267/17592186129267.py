#!/usr/bin/env python3
"""Rewriting integrals over origin-centered cylindrical solids, basis 1356.

Eight observed templates, complete source-shaped masks and banks, plus authored
hard: quadrant + z(x²-y²) + two nonconstant heights. No shifted cylinders and no
integral evaluation demanded of learner. Public observed:<q-id> profiles preserve
raw omissions and legacy banks; they are evidence-only. Normal source:<q-id>
profiles repair source mathematics/presentation and reject the entire bank when
complete definite-integral values coincide. Authored:method banks are optional complete banks deriving their errors from
source Jacobian and bound operations.
Each section below documents its equal-workload domains. No EDB writes.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
import argparse,copy,hashlib,json,math,os,random,re,sys,tempfile,uuid
from importlib.metadata import version as package_version
from pathlib import Path
from functools import lru_cache
import sympy as sp
import mpmath as mp
KP_ID=17592186129267
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/str(KP_ID)
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
SOURCE=CAPTURE['record']; QS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
VERSION='cylindrical-solid-2-format-audit-9837-v1'
x,y,z=sp.symbols('x y z',real=True);r=sp.Symbol('r',nonnegative=True);theta=sp.Symbol('theta',real=True)
TEMPLATES={
 'half_xz':('moderate','q-161520',{'S':25,'H':6}),
 'full_zradial':('easy','q-39481',{'S':9,'H':10,'L':1}),
 'full_z2radial':('easy','q-161605',{'S':1,'H':1}),
 'full_sphere_inverse':('easy','q-161607',{'S':2,'K':16}),
 'half_difference':('moderate','q-161611',{'S':9}),
 'half_zdifference':('moderate','q-161612',{'S':5,'H':2,'L':-1}),
 'quarter_sphere_volume':('moderate','q-161613',{'S':1,'K':4}),
 'full_cone_radial':('easy','q-161604',{'S':9,'H':3}),
 'quarter_zdifference':('hard',None,{'S':5,'H':2}),
}
def tex(a):return sp.latex(sp.sympify(a)).replace(r'\log',r'\ln')
def uid(a):return str(uuid.uuid5(uuid.NAMESPACE_URL,a))
def digest(a):return hashlib.sha256(json.dumps(_ca_material(a),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def atomic(path,text):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='.write-',dir=path.parent)
 with os.fdopen(fd,'w') as f:f.write(text)
 os.replace(tmp,path)
def group(a):return '{'+a+'}'
def integral(parts):
 a,b,R,lo,hi,f=parts
 return r'{\int }_'+group(tex(a))+'^'+group(tex(b))+r'{\int }_{0}^'+group(tex(R))+r'{\int }_'+group(tex(lo))+'^'+group(tex(hi))+tex(f)+r'\,dz\,\text{d}r\,\text{d}\theta '
def model(t,p):
 R=sp.sqrt(p['S']);H=p.get('H',0);L=p.get('L',0);K=p.get('K',0)
 if t=='half_xz':return (-sp.pi/2,sp.pi/2,R,0,H+r*sp.sin(theta),r**2*z*sp.cos(theta),x*z,'x\\ge 0',0,H+y)
 if t=='full_zradial':return (0,2*sp.pi,R,L,H-r*sp.cos(theta),r**2*z,z*sp.sqrt(x*x+y*y),'',L,H-x)
 if t=='full_z2radial':return (0,2*sp.pi,R,0,H,r**2*z*z,z*z*sp.sqrt(x*x+y*y),'',0,H)
 if t=='full_sphere_inverse':return (0,2*sp.pi,R,0,sp.sqrt(K-r*r),r/sp.sqrt(1+z),1/sp.sqrt(1+z),'',0,sp.sqrt(K-x*x-y*y))
 if t=='half_difference':return (sp.pi/2,3*sp.pi/2,R,r*sp.cos(theta),r*r*sp.sin(theta)**2,r**3*sp.cos(2*theta),x*x-y*y,'x\\le 0',x,y*y)
 if t=='half_zdifference':return (0,sp.pi,R,L,H+r*sp.sin(theta),r**3*z*sp.cos(2*theta),z*(x*x-y*y),'y\\ge 0',L,H+y)
 if t=='quarter_sphere_volume':return (sp.pi/2,sp.pi,R,0,sp.sqrt(K-r*r),r,sp.Integer(1),'x\\le 0$ and $y\\ge 0',0,sp.sqrt(K-x*x-y*y))
 if t=='full_cone_radial':return (0,2*sp.pi,R,r,H,r*r,sp.sqrt(x*x+y*y),'',sp.sqrt(x*x+y*y),H)
 if t=='quarter_zdifference':return (sp.pi/2,sp.pi,R,r*sp.cos(theta),H+r*r*sp.sin(theta)**2,r**3*z*sp.cos(2*theta),z*(x*x-y*y),'x\\le 0$ and $y\\ge 0',x,H+y*y)
 raise ValueError(t)
# Observed complete operation banks. Tuple order follows captured EDB, not widget.
def banks(t,p):
 a,b,R,l,h,f,*_=model(t,p);c=(a,b,R,l,h,f);S=p['S'];H=p.get('H');K=p.get('K')
 def alter(**kw):
  vals=list(c)
  for key,val in kw.items():vals[{'a':0,'b':1,'R':2,'l':3,'h':4,'f':5}[key]]=val
  return tuple(vals)
 if t=='half_xz':return [alter(a=0,f=r*r*z*sp.sin(theta)),c,alter(h=H+r*sp.cos(theta)),alter(f=f/r),alter(a=0,h=H+r*sp.cos(theta),f=r*z*sp.sin(theta))],1
 if t=='full_zradial':return [alter(h=H),alter(f=f/r),c,alter(R=S,h=H-r*sp.sin(theta)),alter(R=S,h=H)],2
 if t=='full_z2radial':return [alter(R=2*R,l=0,h=r,f=f/r,a=a),alter(R=2*R),alter(f=f/r),alter(h=r),c],4 # first radial lower differs below
 if t=='full_sphere_inverse':return [alter(h=sp.sqrt(sp.sqrt(K)-r)),alter(R=S,h=sp.sqrt(sp.sqrt(K)-r),f=f/r),c,alter(f=f/r),alter(R=S)],2
 if t=='half_difference':return [alter(b=sp.pi,l=r*sp.sin(theta),f=f/r),alter(f=f/r),alter(b=sp.pi),c,alter(l=r*sp.sin(theta))],3
 if t=='half_zdifference':return [alter(h=H+r*sp.cos(theta)),alter(b=sp.pi/2),alter(b=sp.pi/2,h=H+r*sp.cos(theta),f=f/r),c,alter(f=f/r)],3
 if t=='quarter_sphere_volume':return [c,alter(h=sp.sqrt(K-r)),alter(f=r*r),alter(a=0,h=sp.sqrt(K-r),f=r*r),alter(a=0)],0
 if t=='full_cone_radial':return [alter(f=r),c,alter(R=S,l=r*r,f=r**3),alter(l=r*r),alter(R=S,f=r)],1
 # hard bank: forgotten Jacobian, squared radial upper, lower x->y, omitted H.
 return [c,alter(f=f/r),alter(R=S),alter(l=r*sp.sin(theta)),alter(h=h-p['H'])],0

def angular_integral(expr,a,b):
 """Exact quadrant moments of the independently constructed inner primitive.

 This avoids repeated general-purpose trigonometric integration without changing
 any displayed stage. gamma half-integer values reduce exactly to rationals/pi.
 """
 U,V=sp.symbols('sin_slot cos_slot')
 expanded=sp.expand(sp.expand_trig(expr)).subs({sp.sin(theta):U,sp.cos(theta):V})
 poly=sp.Poly(expanded,U,V)
 out=sp.Integer(0)
 for (n,m),coefficient in poly.terms():
  B=sp.gamma(sp.Rational(n+1,2))*sp.gamma(sp.Rational(m+1,2))/sp.gamma(sp.Rational(n+m+2,2))
  if (a,b)==(0,2*sp.pi):moment=0 if n%2 or m%2 else 2*B
  elif (a,b)==(0,sp.pi):moment=0 if m%2 else B
  elif (a,b)==(sp.pi/2,3*sp.pi/2):moment=0 if n%2 else (-1)**m*B
  elif (a,b)==(-sp.pi/2,sp.pi/2):moment=0 if n%2 else B
  elif (a,b)==(0,sp.pi/2):moment=B/2
  elif (a,b)==(sp.pi/2,sp.pi):moment=(-1)**m*B/2
  else:return sp.integrate(expr,(theta,a,b))
  out+=coefficient*moment
 return sp.expand(out)

@lru_cache(maxsize=8192)
def value(parts,radial_lower=0):
 a,b,R,l,h,f=parts
 g=sp.integrate(f,(z,l,h))
 th=angular_integral(g,a,b)
 # Exact inner integrations; remaining numerical quadrature is only bank eligibility,
 # not an answer. Source extraction records exact unevaluated whole integrals too.
 if not th.has(sp.Integral):
  if th.is_polynomial(r):return sp.integrate(th,(r,radial_lower,R))
  mp.mp.dps=30;fn=sp.lambdify(r,th,'mpmath')
  return mp.quad(fn,[float(radial_lower),float(R)])
 fun=sp.lambdify((r,theta),g,'mpmath');mp.mp.dps=25
 return mp.quad(lambda rr:mp.quad(lambda tt:fun(rr,tt),[float(a),float(b)]),[float(radial_lower),float(R)])

def whole_bank_ok(options,lowers=None):
 vals=[value(o,(lowers or [0]*len(options))[i]) for i,o in enumerate(options)]
 nums=[complex(sp.N(v,18)) if isinstance(v,sp.Basic) else complex(v) for v in vals]
 if any(abs(v.imag)>1e-10 or not math.isfinite(v.real) for v in nums):return False,vals
 return all(abs(v-w)>1e-9*max(1,abs(v),abs(w)) for i,v in enumerate(nums) for w in nums[:i]),vals

# Complete component slots, prepared from capture once. No literal-source return branch.
# Slots replace entire cylinder equation, radius label, integration bound and height
# component; exponent/basis/function argument tokens are never globally substituted.
def masks(t):
 q=QS[TEMPLATES[t][1]];p=TEMPLATES[t][2];S=p['S'];R=tex(sp.sqrt(S));H=p.get('H');L=p.get('L');K=p.get('K')
 def mask(s):
  s=re.sub(r'(x\^\{2\} \+ y\^\{2\} = |\{x\}\^\{2\}\+\{y\}\^\{2\}=)'+str(S)+r'(?=\$)',lambda m:m[1]+'@@S@@',s)
  s=s.replace('radius $'+R+'$','radius $@@R@@$')
  s=s.replace(r'0\le r\le '+R,r'0\le r\le @@R@@')
  if t=='full_z2radial':
   s=s.replace(r'{\int }_{1}^{2}',r'{\int }_{@@R@@}^{@@TWOR@@}')
   s=s.replace(r'{\int }_{0}^{1}{\int }_{0}^{1}',r'{\int }_{0}^{@@R@@}{\int }_{0}^{@@H@@}')
   s=s.replace(r'{\int }_{0}^{1}{\int }_{0}^{r}',r'{\int }_{0}^{@@R@@}{\int }_{0}^{r}')
   s=s.replace(r'{\int }_{@@R@@}^{@@TWOR@@}{\int }_{0}^{1}',r'{\int }_{@@R@@}^{@@TWOR@@}{\int }_{0}^{@@H@@}')
  else:s=s.replace(r'{\int }_{0}^{'+R+'}',r'{\int }_{0}^{@@R@@}')
  s=s.replace(r'\displaystyle \int_{0}^{'+str(sp.sqrt(S))+'}',r'\displaystyle \int_{0}^{@@R@@}')
  # Wrong radial bound is the cylinder RHS, not radius; mask before render.
  if S!=sp.sqrt(S):
   s=s.replace(r'{\int }_{0}^{'+str(S)+'}',r'{\int }_{0}^{@@S@@}')
   s=s.replace(r'\displaystyle \int_{0}^{'+str(S)+'}',r'\displaystyle \int_{0}^{@@S@@}')
  if H is not None:
   if t=='full_z2radial':
    s=s.replace('z=1','z=@@H@@').replace(r'z\le 1',r'z\le @@H@@').replace(r'{\int }_{0}^{1}',r'{\int }_{0}^{@@H@@}')
    # The radius-1 slot must take precedence in the middle integral; normalize manually.
    s=s.replace(r'{\int }_{0}^{@@H@@}{\int }',r'{\int }_{0}^{@@R@@}{\int }')
   elif t=='half_zdifference':s=s.replace('+2','+@@H@@')
   else:s=re.sub(r'(?<![\d])'+str(H)+r'(?![\d])','@@H@@',s)
  if L is not None and L!=0:s=re.sub(r'(?<![\d])'+str(L)+r'(?![\d])','@@L@@',s)
  if t=='full_sphere_inverse':s=s.replace(r'\sqrt{4-r}',r'\sqrt{@@ROOTK@@-r}')
  if K is not None:s=re.sub(r'(?<![\d])'+str(K)+r'(?![\d])','@@K@@',s)
  return s
 return mask

def substitute(s,t,p):
 s=masks(t)(s)
 vals={**p,'R':tex(sp.sqrt(p['S'])),'TWOR':tex(2*sp.sqrt(p['S'])),'ROOTK':tex(sp.sqrt(p.get('K',0)))}
 for key,val in vals.items():s=s.replace('@@'+key+'@@',str(val))
 if '@@' in s:raise ValueError('unfilled slot '+s)
 return s

def projection(t,p):
 os.environ.setdefault('MPLCONFIGDIR',str(_ca_asset_output(Path('matplotlib-cache')).parent/'matplotlib-cache'))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 R=float(sp.sqrt(p['S']));a,b,*_=model(t,p)
 key=digest({'renderer':matplotlib.__version__,'renderer_revision':2,'S':p['S'],'a':str(a),'b':str(b)})
 dest=_ca_asset_output(EVIDENCE/'images'/('projection-'+key+'.png'));side=dest.with_suffix('.json')
 if dest.exists() and side.exists():return str(dest)
 ts=np.linspace(float(a),float(b),400)
 fig,ax=plt.subplots(figsize=(4.5,3.8));ax.set_aspect('equal');ax.set_xlim(-1.8*R,1.8*R);ax.set_ylim(-1.5*R,1.6*R)
 ax.fill(np.r_[0,R*np.cos(ts),0],np.r_[0,R*np.sin(ts),0],color='#deebf4',ec='#438ac2',lw=1.5)
 ax.annotate('',xy=(1.72*R,0),xytext=(-1.75*R,0),arrowprops={'arrowstyle':'->','color':'#333'})
 ax.annotate('',xy=(0,1.52*R),xytext=(0,-1.43*R),arrowprops={'arrowstyle':'->','color':'#333'})
 ax.text(1.75*R,-.09*R,'$x$');ax.text(.04*R,1.5*R,'$y$')
 for angle in [-sp.pi/2,0,sp.pi/2,sp.pi,3*sp.pi/2]:
  av=float(angle)
  if float(a)-1e-8<=av<=float(b)+1e-8:
   xx,yy=R*np.cos(av),R*np.sin(av)
   if abs(xx)>R/2:ax.text(xx,-.12*R,('$-$' if xx<0 else '')+'$'+tex(sp.sqrt(p['S']))+'$',ha='center',va='top')
   else:ax.text(.06*R,yy,('$-$' if yy<0 else '')+'$'+tex(sp.sqrt(p['S']))+'$',va='center')
 ax.text((-.95 if t in ['half_difference','quarter_sphere_volume','quarter_zdifference'] else .5)*R,1.05*R,'$x^2+y^2='+str(p['S'])+'$',fontsize=11)
 ax.axis('off');dest.parent.mkdir(exist_ok=True)
 fd,tmp=tempfile.mkstemp(suffix='.png',prefix='.render-',dir=dest.parent);os.close(fd)
 fig.savefig(tmp,dpi=120,bbox_inches='tight',facecolor='white');plt.close(fig);os.replace(tmp,dest)
 atomic(side,json.dumps({'renderer':'Matplotlib','version':matplotlib.__version__,'renderer_revision':2,'S':p['S'],'theta':[str(a),str(b)],'equal_scale':True}))
 return str(dest)

def clean_solution(s,t,p):
 s=s.replace(r'Δ={(r',r'Δ=\{(r').replace('}.\n$$',r'\}.'+'\n$$') if r'Δ={(r' in s else s
 if t=='full_sphere_inverse':s=s.replace(r'{∭}_{R}\frac{1}{\sqrt{z}}',r'{∭}_{R}\frac{1}{\sqrt{1+z}}')
 if t=='half_zdifference':s=s.replace(r'rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )r',r'rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )')
 return re.sub(r'!\[\]\([^)]*\)',lambda _: '![]('+projection(t,p)+')',s)

def authored_text(t,p):
 a,b,R,l,h,f,F,restriction,low,high=model(t,p)
 base=QS['q-161611'][':question/worked-solution'];opening=base[:base.index('First, let')]
 cond=' for $'+restriction+'$' if restriction else ''
 prompt='The region $R$ is enclosed inside the cylinder $x^2+y^2='+str(p['S'])+'$'+cond+', between the surfaces $z='+tex(low)+'$ and $z='+tex(high)+'$. Express the following triple integral in cylindrical polar coordinates.\n\n$$\n'+r'\iiint_R '+tex(F)+r'\,\mathrm{d}V'+'\n$$'
 fraction='one-quarter of' if t=='quarter_zdifference' else 'one-half of'
 if t=='half_xz':steps=[r'(r\cos\theta)z\cdot r',r'r^2z\cos\theta']
 else:steps=[r'z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r',r'rz(r^2\cos^2\theta-r^2\sin^2\theta)',r'r^3z(\cos^2\theta-\sin^2\theta)',r'r^3z\cos(2\theta)']
 chain=r'\begin{aligned}\iiint_R '+tex(F)+r'\,\mathrm{d}V'
 for step in steps:chain+=r'&=\iiint_\Delta '+step+r'\,dz\,dr\,d\theta \\ '
 chain+='&='+integral((a,b,R,l,h,f))+r'\end{aligned}'
 sol=opening+"First, let's sketch the projection of $R$ onto the $xy$-plane:\n\n![]("+projection(t,p)+')\n\nThe region $R$ is '+fraction+' a right vertical cylinder of radius $'+tex(R)+'$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is\n\n- bounded below by $z='+tex(low)+'='+tex(l)+',$ and\n\n- bounded above by $z='+tex(high)+'='+tex(h)+'.$\n\nAs a result, in cylindrical polar coordinates, our region can be expressed as\n\n$$\n'+r'\Delta=\{(r,\theta,z):0\le r\le '+tex(R)+','+tex(a)+r'\le\theta\le '+tex(b)+','+tex(l)+r'\le z\le '+tex(h)+r'\}.'+'\n$$\n\nTherefore, using the change of variables formula, we obtain\n\n$$\n'+chain+'\n$$'
 return prompt,sol

# EASY: full disks, one standard radial identity or unchanged z-only integrand.
# MODERATE: hemisphere/quadrant angular bookkeeping or difference-square identity.
# HARD (authored): combine quadrant, z-weighted difference identity, and two
# nonconstant heights. These demands remain absent from easy/moderate defaults.
def allowed(t,p):
 if set(p)!=set(TEMPLATES[t][2]):raise ValueError('exact parameter keys required')
 if any(type(v)!=int for v in p.values()):raise ValueError('integer parameters required')
 if not 1<=p['S']<=36:raise ValueError('1<=S<=36')
 if 'K' in p and (not p['S']<p['K']<=81 or math.isqrt(p['K'])**2!=p['K']):raise ValueError('S<K<=81; K is a perfect square')
 if 'H' in p and not 1<=p['H']<=12:raise ValueError('1<=H<=12')
 if 'L' in p and not -4<=p['L']<=4:raise ValueError('-4<=L<=4')
 if t in ('half_xz','full_zradial') and p['H']-p.get('L',0)<=sp.sqrt(p['S']):raise ValueError('top must exceed bottom everywhere')
 if t=='half_zdifference' and p['H']<=p['L']:raise ValueError('H>L')
 if t=='full_cone_radial' and p['H']<sp.sqrt(p['S']):raise ValueError('H>=sqrt(S)')

def sample(t,rng):
 p=dict(TEMPLATES[t][2]);p['S']=rng.randint(1,36)
 if 'K' in p:p['K']=rng.choice([k for k in (4,9,16,25,36,49,64,81) if k>p['S']])
 if 'L' in p:p['L']=rng.randint(-3,3)
 if 'H' in p:p['H']=rng.randint(1,12)
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed)
 if profile and profile.startswith(('observed:','source:')):
  sid=profile.split(':',1)[1];t=next((k for k,v in TEMPLATES.items() if v[1]==sid),None)
  if not t:raise ValueError('unknown source profile')
  if template is not None and template!=t:raise ValueError('profile/template mismatch')
  template=t
 t=template or rng.choice([k for k,v in TEMPLATES.items() if v[0]==level])
 if t not in TEMPLATES or TEMPLATES[t][0]!=level:raise ValueError('template/level mismatch')
 sid=TEMPLATES[t][1];profile=profile or ('source:'+sid if sid else 'authored:method')
 if profile not in (('observed:'+sid,'source:'+sid,'authored:method') if sid else ('authored:method',)):raise ValueError('profile')
 raw=profile.startswith('observed:')
 # Whole family/profile selected above, prior to parameter sampling.
 for attempt in range(500):
  p=copy.deepcopy(parameters) if parameters is not None else sample(t,rng)
  try:allowed(t,p)
  except ValueError:
   if parameters is not None:raise
   continue
  opts,ci=banks(t,p);lowers=[0]*5
  if t=='full_z2radial':lowers[:2]=[sp.sqrt(p['S'])]*2
  if profile=='authored:method':
   a,b,R,l,h,f,*_=model(t,p);c=(a,b,R,l,h,f)
   # Five source-supported errors: missing/duplicate Jacobian and treating
   # squared cylinder radius as radial bound; compound duplicate+bound error.
   opts=[c,(a,b,R,l,h,f/r),(a,b,R,l,h,f*r),(a,b,p['S'],l,h,f),(a,b,p['S'],l,h,f/r)];ci=0;lowers=[0]*5
  if raw:break
  ok,_=whole_bank_ok(opts,lowers)
  if ok:break
  if parameters is not None:raise ValueError('entire bank has equal/invalid definite-integral values; use authored profile')
 else:raise ValueError('no valid parameter bank')
 if sid:
  q0=QS[sid];prompt=substitute(q0[':question/problem'],t,p)
  sol=substitute(q0.get(':question/worked-solution',''),t,p)
 else:prompt,sol=authored_text(t,p)
 if not raw:
  if t=='half_xz':prompt,sol=authored_text(t,p)
  else:sol=clean_solution(sol,t,p)
 q={':question/problem':prompt}
 if raw:
  if ':question/difficulty' in q0:q[':question/difficulty']=q0[':question/difficulty'][':db/ident']
  if ':question/worked-solution' in q0:q[':question/worked-solution']=sol
 else:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
 raw_banks=[]
 if raw:
  for f0 in q0[':question/answer-fields']:
   raw_banks.append(([substitute(a[':answer/value'],t,p) for a in f0[':answer-field/choices']], next((i for i,a in enumerate(f0[':answer-field/choices']) if a[':answer/id']==f0.get(':answer-field/correct',{}).get(':answer/id')),None), f0[':answer-field/key']))
 else:
  rendered=[integral(o) for o in opts]
  if t=='full_z2radial' and profile.startswith('source:'):
   for i in (0,1):rendered[i]=rendered[i].replace(r'{\int }_{0}^'+group(tex(2*sp.sqrt(p['S']))),r'{\int }_'+group(tex(sp.sqrt(p['S'])))+'^'+group(tex(2*sp.sqrt(p['S']))))
  raw_banks=[(rendered,ci,'selection')]
 if not raw:_ca_question(q);raw_banks=[(_ca_values(vals),ci,key)for vals,ci,key in raw_banks]
 # Content identity includes actual difficulty, prompt/solution/key presence/banks.
 identity=digest({'version':VERSION,'question':q,'banks':[sorted(b[0]) for b in raw_banks]})
 q[':question/id']=uid(identity);fields=[]
 for fi,(values,correct,key) in enumerate(raw_banks):
  fid=uid(identity+':field:'+str(fi));answers=[{':answer/id':uid(fid+':answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
  if correct is not None:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
  rng.shuffle(answers);fields.append(field)
 q[':question/answer-fields']=fields
 m=model(t,p)
 fingerprint=digest({'criterion':'complete cylindrical integral setup','integrand':str(m[6]),'bounds':[str(v) for v in m[:5]],'level':level})
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'source_id':sid,'basis':CAPTURE['basis'],'database':CAPTURE['database'],'lineage':CAPTURE['lineage'],'identity':identity,'mathematical_fingerprint':fingerprint,'evidence_only':raw,'eligible_for_learning':not raw,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':package_version('matplotlib')},'authored_level':t in ['half_xz','quarter_zdifference']}}
# Easy entrypoint: full-disk bounds; standard radial identity or z-only function.
def generate_easy(seed=0,**kw):
 """Observed easy families; complete source banks are normal defaults."""
 return generate('easy',seed,**kw)
# Moderate entrypoint: sector bookkeeping / difference-square substitution.
def generate_moderate(seed=0,**kw):
 """Three observed moderate families plus authored placement of unrated xz."""
 return generate('moderate',seed,**kw)
# Hard entrypoint: combined quadrant, two nonconstant heights, z-weighted identity.
def generate_hard(seed=0,**kw):
 """Missing-level authored extension, never integral evaluation or shifted circle."""
 return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  for i,a in enumerate(f[':answer-field/choices']):text+=str(i+1)+'. $'+a[':answer/value']+'$\n'
 return text+'\n'+q.get(':question/worked-solution','[Original solution absent.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(rec) for rec in records))
