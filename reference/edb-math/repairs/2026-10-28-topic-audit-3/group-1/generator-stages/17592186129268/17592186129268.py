#!/usr/bin/env python3
"""Shifted-cylinder rewrite generator, frozen math basis 1356; steps 3–7 only.

Six source-shaped families. observed:<q-id> is public parameterized raw evidence,
never eligible learning content. Complete malformed/ambiguous banks are preserved.
Normal method banks use whole definite integral values for collision rejection.
All normal questions ask for the cylindrical setup, never its evaluated value.
The source solution stages are retained: Cartesian circle, substituted circle,
expanded squares, Pythagorean grouping, reduction, factorization, radial/angular
bounds, full integrand substitution, grouping (radial functions), final integral.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material
import argparse,copy,hashlib,json,math,os,random,re,sys,tempfile,uuid,threading
from pathlib import Path
from functools import lru_cache
import sympy as sp
import numpy as np
KP_ID=17592186129268
ROOT=Path(__file__).resolve().parent; EVIDENCE=ROOT/str(KP_ID)
CAPTURE=json.loads((EVIDENCE/'source.json').read_text()); SOURCE=CAPTURE['record']
QS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
VERSION='shifted-cylinder-2-format-audit-9837-v1'
x,y,z=sp.symbols('x y z',real=True);r=sp.Symbol('r',nonnegative=True);theta=sp.Symbol('theta',real=True)
TEMPLATES={
 'lower_xy':('moderate','q-161521',{'a':3,'H':2}),
 'upper_square':('easy','q-161523',{'a':1,'L':1,'H':2}),
 'left_inverse':('moderate','q-161630',{'a':3,'L':-8,'H':2,'C':1}),
 'lower_zinverse':('hard','q-161636',{'a':3,'H':6,'C':1}),
 'left_xy_sphere':('hard','q-161633',{'a':2,'L':-2,'K':16}),
 'right_radical':('hard','q-161637',{'a':4,'L':-5,'C':1}),
}
def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def digest(v):return hashlib.sha256(json.dumps(_ca_material(v),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def atomic(path,s):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='.write-',dir=path.parent)
 with os.fdopen(fd,'w') as f:f.write(s)
 os.replace(tmp,path)
def model(t,p):
 a=p['a'];L=p.get('L',0);H=p.get('H',0);C=p.get('C',1);K=p.get('K',0)
 if t=='lower_xy':return (sp.pi,2*sp.pi,-2*a*sp.sin(theta),0,H+r*r,r**3*sp.cos(theta)*sp.sin(theta),x*y,0,H+x*x+y*y,0,-a,'')
 if t=='upper_square':return (0,sp.pi/2,2*a*sp.cos(theta),L,H,r**3,x*x+y*y,L,H,a,0,r'y\ge 0')
 if t=='left_inverse':return (sp.pi/2,3*sp.pi/2,-2*a*sp.cos(theta),L,r*sp.cos(theta)+H,r/sp.sqrt(r*r+C),1/sp.sqrt(x*x+y*y+C),L,x+H,-a,0,'')
 if t=='lower_zinverse':return (3*sp.pi/2,2*sp.pi,2*a*sp.cos(theta),r*sp.sin(theta),H,r/sp.sqrt(z+C),1/sp.sqrt(z+C),y,H,a,0,r'y\le 0')
 if t=='left_xy_sphere':return (sp.pi/2,sp.pi,2*a*sp.sin(theta),L,sp.sqrt(K-r*r),2*r**3*sp.cos(theta)*sp.sin(theta),2*x*y,L,sp.sqrt(K-x*x-y*y),0,a,r'x\le 0')
 if t=='right_radical':return (0,sp.pi/2,2*a*sp.sin(theta),L,r*sp.cos(theta),r*sp.sqrt(r*r+C),sp.sqrt(x*x+y*y+C),L,x,0,a,r'x\ge 0')
 raise ValueError(t)
def integral(o):
 a,b,R,l,h,f=o
 return r'{\int }_{'+tex(a)+'}^{'+tex(b)+r'}{\int }_{0}^{'+tex(R)+r'}{\int }_{'+tex(l)+'}^{'+tex(h)+'}'+tex(f)+r'\,dz\,\text{d}r\,\text{d}\theta '
def source_banks(t,p):
 c=model(t,p)[:6];A=p['a'];H=p.get('H',0)
 def alt(**kw):
  v=list(c)
  for k,xv in kw.items():v[{'a':0,'b':1,'R':2,'l':3,'h':4,'f':5}[k]]=xv
  return tuple(v)
 a,b,R,l,h,f=c
 if t=='lower_xy':return [c,alt(R=A,h=H+r),alt(R=2*A*sp.cos(theta)),alt(R=A,h=H+r,f=f/r),alt(f=f/r)],None
 if t=='upper_square':return [alt(b=sp.pi,f=r*r),alt(R=A*sp.cos(theta),f=r*r),alt(b=sp.pi,R=-A*sp.cos(theta)),c,alt(R=-2*A*sp.sin(theta))],None
 if t=='left_inverse':return [alt(f=f/r),alt(R=-2*A*sp.sin(theta),h=r*sp.sin(theta)+H,f=f/r),alt(R=-2*A*sp.sin(theta)),alt(h=r*sp.sin(theta)+H),c],4
 if t=='lower_zinverse':return [c,alt(f=f/r),alt(R=-2*A*sp.sin(theta),f=f/r),alt(l=r*sp.cos(theta)),alt(R=-2*A*sp.sin(theta),l=r*sp.cos(theta))],0
 if t=='left_xy_sphere':return [alt(f=f/r),c,alt(b=3*sp.pi/2,R=-2*A*sp.cos(theta),f=f/r),alt(b=3*sp.pi/2),alt(R=-2*A*sp.cos(theta))],1
 if t=='right_radical':return [alt(b=sp.pi,h=r*sp.sin(theta),f=f/r),c,alt(h=r*sp.sin(theta)),alt(f=f/r),alt(b=sp.pi)],1

def method_banks(t,p):
 c=model(t,p)[:6];a,b,R,l,h,f=c
 if t=='lower_xy':
  # x->y and y->x substitutions, each with/without the Jacobian. All positive
  # while the actual odd-in-x integral is zero; reject all member collisions.
  return [c,(a,b,R,l,h,r**3*sp.sin(theta)**2),(a,b,R,l,h,r**2*sp.sin(theta)**2),(a,b,R,l,h,r**3*sp.cos(theta)**2),(a,b,R,l,h,r**2*sp.cos(theta)**2)],0
 # Complete method bank: omit J, duplicate J, forget doubled shifted radius,
 # and reverse orientation of dz. No final-value perturbations.
 return [c,(a,b,R,l,h,f/r),(a,b,R,l,h,f*r),(a,b,R/2,l,h,f),(a,b,R,h,l,f)],0

@lru_cache(maxsize=8192)
def value(o,order=72):
 a,b,R,l,h,f=o
 inner=sp.integrate(f,(z,l,h));fn=sp.lambdify((r,theta),inner,'numpy');rf=sp.lambdify(theta,R,'numpy')
 ns,ws=np.polynomial.legendre.leggauss(order);ts=float(a)+(ns+1)*float(b-a)/2
 rr=np.asarray(rf(ts))+np.zeros_like(ts);rad=rr[:,None]*(ns[None,:]+1)/2
 with np.errstate(all='ignore'):v=np.asarray(fn(rad,ts[:,None]),dtype=complex)+np.zeros_like(rad)
 result=np.sum(v*rr[:,None]*ws[None,:]*ws[:,None])*float(b-a)/4
 if not math.isfinite(result.real) or abs(result.imag)>1e-8:raise ValueError('non-real/undefined complete integral')
 return float(result.real)
def eligible(opts):
 vals=[value(tuple(o)) for o in opts]
 return all(abs(u-v)>1e-8*max(1,abs(u),abs(v)) for i,u in enumerate(vals) for v in vals[:i]),vals

# Raw evidence masks operate on COMPLETE component strings. Only parameter
# components known from the captured family are masked; no short x/y replacement.
def substitute(s,t,p):
 original=TEMPLATES[t][2];a0=original['a'];a=p['a']; replacements={}
 if t=='upper_square':s=s.replace(r'\le 1,',r'\le @@aSquared@@,')
 # Protect fixed theta ranges, exponent forms and function constants before radius
 # components: numeric aliases otherwise conflate a=3 with 3*pi/2 or r^3.
 protected={}
 pattern=r'(?:\\+frac\{(?:3)?\\+pi ?\}\{2\}|(?:3)?\\+pi ?/2|(?:3)?π ?/ ?2|2\\+pi|2π|(?:\{?[rxy]\}?|[)])\^\{[23]\}|[rxy] [23])'
 for i,m in enumerate(re.finditer(pattern,s)):
  protected['##PROTECT'+chr(65+i)+'##']=m[0]
 for key,v in protected.items():s=s.replace(v,key)
 # Height and kernel components before scale (H=6 coincides with doubled a).
 for key in ['L','H','K','C']:
  if key not in original:continue
  old=original[key];new=p[key]
  if key=='C':
   s=s.replace('+1}', '+@@C@@}').replace('+1\\', '+@@C@@\\')
  elif key=='H' and t=='lower_zinverse':
   s=s.replace('z=6','z=@@H@@').replace(r'z\le 6',r'z\le @@H@@').replace('}^{6}', '}^{@@H@@}')
  elif key=='H' and t=='upper_square':
   s=s.replace(r'z \le 2',r'z \le @@H@@').replace('}^{2}', '}^{@@H@@}')
  elif key=='L' and t=='upper_square':s=s.replace('1 \\le z','@@L@@ \\le z').replace('_{1}', '_{@@L@@}')
  else:s=re.sub(r'(?<![\d])'+str(old)+r'(?![\d])','@@'+key+'@@',s)
 # Explicit radius, squared radius, doubled radius as independent slots.
 s=s.replace('radius $'+str(a0)+'$', 'radius $@@a@@$')
 s=re.sub(r'(?<![\d])'+str(a0*a0)+r'(?![\d])','@@aSquared@@',s) if a0*a0!=a0 else s
 s=re.sub(r'(?<![\d])'+str(2*a0)+r'(?![\d])','@@twiceA@@',s)
 s=re.sub(r'(?<![\d])'+str(a0)+r'(?![\d])','@@a@@',s)
 for key,v in protected.items():s=s.replace(key,v)
 vals={**p,'aSquared':a*a,'twiceA':2*a}
 for k,v in vals.items():s=s.replace('@@'+k+'@@',str(v))
 assert '@@' not in s
 return s

def raw_question(t,p):
 src=QS[TEMPLATES[t][1]];q={}
 for k in [':question/problem',':question/worked-solution',':question/difficulty']:
  if k in src:q[k]=substitute(src[k],t,p) if isinstance(src[k],str) else src[k][':db/ident']
 fs=[]
 for fi,f0 in enumerate(src.get(':question/answer-fields',[])):
  f={':answer-field/key':f0[':answer-field/key'],':answer-field/type':f0[':answer-field/type'][':db/ident']}
  choices=[]
  for ai,v in enumerate(f0[':answer-field/choices']):choices.append({':answer/type':v[':answer/type'][':db/ident'],':answer/value':substitute(v[':answer/value'],t,p),':answer/id':v[':answer/id']})
  f[':answer-field/choices']=choices;f[':answer-field/id']=f0[':answer-field/id']
  if ':answer-field/correct' in f0:f[':answer-field/correct']=[':answer/id',f0[':answer-field/correct'][':answer/id']]
  fs.append(f)
 if ':question/answer-fields' in src:q[':question/answer-fields']=fs
 return q

# Thread-safe rendering: each call owns its figure, and writes unique files then
# atomic rename. Sidecar+PNG both required. No active cache deletion.
PLOT_LOCK=threading.RLock()
def projection(t,p):
 with PLOT_LOCK:return _projection(t,p)
def _projection(t,p):
 os.environ.setdefault('MPLCONFIGDIR',str(EVIDENCE/'matplotlib-cache'))
 import matplotlib;matplotlib.use('Agg')
 from matplotlib.figure import Figure
 from matplotlib.backends.backend_agg import FigureCanvasAgg
 a,b,R,*rest=model(t,p);cx,cy=model(t,p)[9:11]
 key=digest({'a':p['a'],'center':[cx,cy],'angles':[str(a),str(b)],'matplotlib':matplotlib.__version__,'style':2})
 dest=EVIDENCE/'images'/('projection-'+key+'.png');side=dest.with_suffix('.json')
 if dest.exists() and side.exists():return str(dest)
 dest.parent.mkdir(parents=True,exist_ok=True)
 ts=np.linspace(float(a),float(b),600);rv=sp.lambdify(theta,R,'numpy')(ts);xx=rv*np.cos(ts);yy=rv*np.sin(ts)
 A=p['a'];fig=Figure(figsize=(4.5,3.8));FigureCanvasAgg(fig);ax=fig.add_subplot();ax.set_aspect('equal')
 ax.set_xlim(min(0,cx-A)-.6*A,max(0,cx+A)+.6*A);ax.set_ylim(min(0,cy-A)-.6*A,max(0,cy+A)+.6*A)
 ax.fill(np.r_[0,xx,0],np.r_[0,yy,0],fc='#deebf4',ec='#277dbe',lw=1.5)
 xmin,xmax=ax.get_xlim();ymin,ymax=ax.get_ylim()
 ax.annotate('',xy=(xmax,0),xytext=(xmin,0),arrowprops={'arrowstyle':'->','color':'black','lw':.9})
 ax.annotate('',xy=(0,ymax),xytext=(0,ymin),arrowprops={'arrowstyle':'->','color':'black','lw':.9})
 for spine in ax.spines.values():spine.set_visible(False)
 ax.set_xticks(sorted(set([0,cx,cx-A,cx+A])));ax.set_yticks(sorted(set([0,cy,cy-A,cy+A])))
 ax.grid(alpha=.2);ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0)
 circle=(x-cx)**2+(y-cy)**2
 ax.set_title('$'+tex(circle)+'='+str(A*A)+'$',fontsize=11,pad=18)
 fd,tmp=tempfile.mkstemp(prefix='.render-',suffix='.png',dir=dest.parent);os.close(fd)
 try:fig.savefig(tmp,dpi=130,bbox_inches='tight');os.replace(tmp,dest)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 atomic(side,json.dumps({'renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0],'a':A,'center':[cx,cy],'angle_bounds':[str(a),str(b)],'xy_extents':[float(min(xx)),float(max(xx)),float(min(yy)),float(max(yy))]},indent=2))
 return str(dest)

def normal_question(t,p,options):
 a,b,R,l,h,f,F,L,H,cx,cy,condition=model(t,p);A=p['a']
 circle=(x-cx)**2+(y-cy)**2;eq=tex(circle)+'='+str(A*A)
 # Keep shifted form unevaluated (CAS expansion would hide the completed square).
 if cx:lhs='(x'+('+' if cx<0 else '-')+str(abs(cx))+r')^{2}+{y}^{2}';axis='cos';shift=cx
 else:lhs=r'{x}^{2}+(y'+('+' if cy<0 else '-')+str(abs(cy))+r')^{2}';axis='sin';shift=cy
 eq=lhs+'='+str(A*A)
 prompt='If the solid region $R$ is given by \n\n$$\nR=\\{(x,y,z)\\,:\\,'+lhs+r'\le '+str(A*A)+(','+condition if condition else '')+r',\,'+tex(L)+r'\le z\le '+tex(H)+r'\},'+'\n$$\n\nthen express the triple integral\n\n$$\n'+r'{∭}_{R}'+tex(F)+r'\,\text{d}V'+'\n$$\n\nas an equivalent integral in cylindrical polar coordinates.'
 # Preserve shared source prose and the exact operative algebra order.
 opener='We will use the change of variables formula in the form\n\n$$\n'+r'{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .'+'\n$$\n\nIf $(r,\\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas\n\n$$\n'+r'x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.'+'\n$$\n\nFirst, let\'s sketch the projection of $R$ onto the $xy$-plane:\n\n![]('+projection(t,p)+')\n\n'
 word='one-half of a right vertical cylinder' if condition else 'a right vertical cylinder'
 lowertext=tex(L)+('='+tex(l) if sp.simplify(L-l)!=0 else '')
 uppertext=tex(H)+('='+tex(h) if sp.simplify(H-h)!=0 else '')
 sol=opener+'The region $R$ is '+word+' of radius $'+str(A)+'$ whose axis passes through the point $('+str(cx)+','+str(cy)+')$ in the $xy$-plane, and is\n\n- bounded below by $z='+lowertext+',$ and\n\n- bounded above by $z='+uppertext+'.$\n\nWith that in mind, let\'s '+('now write the ' if condition else 'write the equation ')+eq+'$ in polar coordinates:\n\n'
 sol=sol.replace('write the '+eq+'$', 'write the $'+eq+'$').replace('equation '+eq+'$', 'equation $'+eq+'$')
 c=r'\operatorname{cos}⁡\theta';s=r'\operatorname{sin}⁡\theta';fun=c if cx else s
 signed=('+' if shift<0 else '-')+str(A)
 sub=(r'(r'+c+signed+r')^{2}+(r'+s+r')^{2}') if cx else (r'(r'+c+r')^{2}+(r'+s+signed+r')^{2}')
 term=('-' if shift>0 else '+')+str(2*A)+'r'+fun
 if cx:exp=r'{r}^{2}{cos}^{2}⁡\theta '+term+'+'+str(A*A)+r'+{r}^{2}{sin}^{2}⁡\theta'
 else:exp=r'{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta '+term+'+'+str(A*A)
 rows=[lhs+' & ='+str(A*A),sub+' & ='+str(A*A),exp+' & ='+str(A*A),r'{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )'+term+' & =0',r'{r}^{2}'+term+' & =0','r(r'+term[0]+str(2*A)+fun+') & =0']
 sol+='$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nSince $r$ cannot be identical to zero on the entire '+('semicircle' if condition else 'circle')+', we must have $r='+tex(R)+'.$\n\nAs a result, in cylindrical polar coordinates, our region can be expressed as \n\n$$\n'+r'Δ=\{(r,\theta ,z)\,:\,0\le r\le '+tex(R)+r',\,'+tex(a)+r'\le \theta \le '+tex(b)+r',\,'+tex(l)+r'\le z\le '+tex(h)+r'\}.'+'\n$$\n\nTherefore, using the change of variables formula, we obtain'+('  ' if t in ['left_inverse','lower_zinverse'] else '')+'\n\n'
 # Substitution is simultaneous and complete: xy becomes (r cos)(r sin).
 Fc=F.subs({x:r*sp.cos(theta),y:r*sp.sin(theta)},simultaneous=True)
 if t in ['lower_xy','left_xy_sphere']:
  coeff='2' if t=='left_xy_sphere' else ''
  fs=coeff+'(r'+c+')(r'+s+')'
 elif t=='upper_square':fs='((r'+c+r')^{2}+(r'+s+r')^{2})'
 elif t=='left_inverse':fs=r'\frac{1}{\sqrt{(r'+c+r')^{2}+(r'+s+r')^{2}+'+str(p['C'])+'}}'
 elif t=='right_radical':fs=r'\sqrt{(r'+c+r')^{2}+(r'+s+r')^{2}+'+str(p['C'])+'}'
 else:fs=tex(Fc)
 stages=[r'{∭}_{R}'+tex(F)+r'\,\text{d}V & ={∭}_{Δ}'+fs+r'\cdot r\,dz\,dr\,d\theta']
 if t in ['left_inverse','right_radical']:
  root=r'\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+'+str(p['C'])+'}'
  grouped=r'\frac{r}{'+root+'}' if t=='left_inverse' else root+r'\cdot r'
  stages.append(r' & ={∭}_{Δ}'+grouped+r'\,dz\,dr\,d\theta')
 elif t=='upper_square':stages.append(r' & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta')
 out=list(model(t,p)[:6])
 # Keep the substituted product form used by the answer bank. A double-angle
 # collection would add an unnecessary representation change at the endpoint.
 final=integral(out)
 stages.append(' & ='+final+'.')
 sol+='$$\n'+r'\begin{aligned}'+r' \\ '.join(stages)+r'\end{aligned}'+'\n$$'
 return {':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+TEMPLATES[t][0]}

# Easy: authored assignment of the unrated constant-height quarter shifted disk;
# one radial x²+y² reduction. a=1..5, height difference1..5, L=0..4.
# Moderate: full shifted disk and one nonconstant height, either radial inverse
# or xy substitution (unrated legacy); a=1..5, H=1..5, C=1..5, clearance1..5.
# Hard: half shifted disk plus clipping and a variable roof/lower surface. Three
# observed families, same respective source workloads. a=1..5, height/kernel
# clearance1..5; real-domain C>a for the z-inverse family; sphere K>=4a².
def guard(t,p,evidence=False):
 if set(p)!=set(TEMPLATES[t][2]):raise ValueError('parameter keys')
 if any(type(v)!=int for v in p.values()):raise ValueError('integer parameter domain')
 if not 1<=p['a']<=5:raise ValueError('radius domain')
 if evidence:return
 A=p['a']
 if t=='upper_square' and not (0<=p['L']<=4 and 1<=p['H']-p['L']<=5):raise ValueError('easy height domain')
 if t=='lower_xy' and not 1<=p['H']<=5:raise ValueError('moderate height domain')
 if t=='left_inverse' and not (1<=p['H']<=5 and 1<=p['C']<=5 and 1<=p['H']-2*A-p['L']<=5):raise ValueError('moderate clearance domain')
 if t=='lower_zinverse' and not (1<=p['H']<=10 and 1<=p['C']-A<=5):raise ValueError('hard real kernel domain')
 if t=='left_xy_sphere' and not (1<=-p['L']<=5 and p['K'] in [(2*A)**2,(2*A+1)**2,(2*A+2)**2]):raise ValueError('hard sphere domain')
 if t=='right_radical' and not (1<=-p['L']<=5 and 1<=p['C']<=5):raise ValueError('hard radical domain')
def sample(t,rng):
 A=rng.randint(1,5)
 if t=='upper_square':L=rng.randint(0,4);return {'a':A,'L':L,'H':L+rng.randint(1,5)}
 if t=='lower_xy':return {'a':A,'H':rng.randint(1,5)}
 if t=='left_inverse':H=rng.randint(1,5);return {'a':A,'H':H,'L':H-2*A-rng.randint(1,5),'C':rng.randint(1,5)}
 if t=='lower_zinverse':return {'a':A,'H':rng.randint(1,10),'C':A+rng.randint(1,5)}
 if t=='left_xy_sphere':return {'a':A,'L':-rng.randint(1,5),'K':(2*A+rng.randint(0,2))**2}
 if t=='right_radical':return {'a':A,'L':-rng.randint(1,5),'C':rng.randint(1,5)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError(level)
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  sid=profile.split(':',1)[1];ts=[t for t,v in TEMPLATES.items() if v[1]==sid]
  if not ts:raise ValueError(profile)
  if template and template!=ts[0]:raise ValueError('profile family mismatch')
  template=ts[0]
 t=template or rng.choice([k for k,v in TEMPLATES.items() if v[0]==level])
 if t not in TEMPLATES or TEMPLATES[t][0]!=level:raise ValueError('difficulty family mismatch')
 if profile is None and t=='right_radical':profile='source:'+TEMPLATES[t][1]
 raw=bool(profile and profile.startswith('observed:'))
 if profile not in [None,'authored:method','source:'+TEMPLATES[t][1],'observed:'+TEMPLATES[t][1]]:raise ValueError('bank profile')
 p=dict(parameters) if parameters is not None else (dict(TEMPLATES[t][2]) if raw else sample(t,rng))
 for attempt in range(100):
  guard(t,p,raw)
  if raw:q=raw_question(t,p);opts,correct=source_banks(t,p);break
  opts,correct=source_banks(t,p) if profile and profile.startswith('source:') else method_banks(t,p)
  if correct is None:raise ValueError('source lacks correct designation; use observed evidence or authored:method')
  try:ok,values=eligible(opts)
  except ValueError:ok=False
  if ok:break
  if parameters is not None:raise ValueError('whole complete bank invalid/ambiguous')
  p=sample(t,rng)
 else:raise ValueError('no eligible instance')
 if not raw:
  q=normal_question(t,p,opts);values=[integral(o) for o in opts]
  _ca_question(q);values=_ca_values(values)
  identity=digest({'version':VERSION,'level':level,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(values)})
  fid=uid(identity+'/selection');answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  corr=answers[correct][':answer/id'];rng.shuffle(answers)
  q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',corr]}]
 else:
  identity=digest({'version':VERSION,'level':level,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])})
  for fi,f in enumerate(q[':question/answer-fields']):
   previous=f.get(':answer-field/correct',[None,None])[1];fid=uid(identity+'/field/'+str(fi));f[':answer-field/id']=fid
   for a in f[':answer-field/choices']:
    old=a[':answer/id'];a[':answer/id']=uid(fid+'/'+a[':answer/value'])
    if old==previous:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
   rng.shuffle(f[':answer-field/choices'])
 q[':question/id']=uid(identity)
 # Canonical task excludes bank/profile/layout and common canceled vertical offset.
 taskp=dict(p)
 if t=='upper_square':taskp={'a':p['a'],'height':p['H']-p['L']}
 if t=='left_inverse':taskp={'a':p['a'],'C':p['C'],'height':p['H']-p['L']}
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':t,'profile':profile or 'authored:method','parameters':p,'source_id':TEMPLATES[t][1],'source':{k:CAPTURE[k] for k in ['database','basis','lineage']},'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':digest({'template':t,'parameters':taskp}),'content_fingerprint':identity,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'numpy':np.__version__}}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];lines=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$')
 if ':question/worked-solution' in q:lines+=['\nWorked solution',q[':question/worked-solution']]
 return '\n\n'.join(lines)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(v) for v in records))
if __name__=='__main__':main()
