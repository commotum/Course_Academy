#!/usr/bin/env python3
"""Stokes circulation: frozen basis 1356; local review only, stops at step 7.

Shared exact models underpin all three documented sections below. Raw historical
profiles are public evidence-only scaling recipes, retaining full prose/layout,
missing attributes and opaque complete banks. Defaults use source-shaped models
with independently authored method banks and repaired solutions. No EDB client.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133927-source-policy.json'))
    raise SystemExit(0)

import argparse,copy,hashlib,json,random,re,subprocess,sys,tempfile,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix(''); VERSION='stokes-1'
SOURCE=json.loads((HERE/'source.json').read_text()); KP=SOURCE['record']
X,Y,Z,R,T=s.symbols('x y z r theta',real=True)
Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Easy is an authored canonical-example reduction: one horizontal disk, constant
# plus one odd Cartesian term, no nonzero slope terms. h=1..4, k=1..4.
# Moderate retains graph flux and Cartesian setup; no integral evaluation asked.
# Shapes and arithmetic match observed polynomial/rational/cone/tilted families.
# Hard retains full graph substitution and polar evaluation; no new curl method.
FAMILIES={
 'horizontal':('easy',None), 'triangle':('moderate','q-161927'),
 'tilted_blank':('moderate','q-168625'), 'xy_triangle':('moderate','q-162361'),
 'reciprocal':('moderate','q-162365'), 'cone_triangle':('moderate','q-162364'),
 'exponential':('hard','q-162366'), 'odd_plane':('hard','q-162374'),
 'negative_cone':('hard','q-162371'), 'tilted_disk':('hard','q-162372'),
 'shifted_paraboloid':('hard','q-162373'), 'unrated':('easy','q-161926')}
SOURCE_FAMILY={v[1]:k for k,v in FAMILIES.items() if v[1]}
ORIGINAL={n:{'k':1,'a':1,'h':10 if n=='triangle' else 4 if n in ('tilted_blank','exponential','unrated') else 3 if n=='negative_cone' else 2 if n=='tilted_disk' else 1} for n in FAMILIES}

def tex(v):return s.latex(v).replace('\\log','\\ln')
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def vec(v):return r'\langle '+',\\,'.join(tex(t) for t in v)+r'\rangle'
def integral(f,dom):
 x0,x1,y0,y1=dom
 return rf'\int_{{{tex(x0)}}}^{{{tex(x1)}}}\int_{{{tex(y0)}}}^{{{tex(y1)}}}\left({tex(f)}\right)\,\mathrm{{d}}y\,\mathrm{{d}}x'
def model(name,p):
 k,a,h=map(s.Integer,(p['k'],p['a'],p['h'])); disk=None; dom=None
 if name=='horizontal':g=h; c=(-k*X*Z,-k*Y*Z,k*(X+Z**2));disk=a; boundary=rf'the cylinder $x^2+y^2={tex(a**2)}$ and the plane $z={h}$'
 elif name=='triangle':g=h-X**2-Y**2;c=(-2*k*Z,0,0);dom=(0,a,0,a-X)
 elif name=='tilted_blank':g=h-X-Y;c=(2*k*X*Y,k*(2*Z-Y**2),2*k*Y);dom=(0,a,0,a)
 elif name=='xy_triangle':g=h+X**2+2*Y**2;c=(k*Y,-k*X,k);dom=(0,a,X-a,0)
 elif name=='reciprocal':g=h/(X**2+Y**2+1);c=(k*X,k*Y,-2*k*Z);dom=(-a,a,-a,a)
 elif name=='cone_triangle':g=s.sqrt(X**2+Y**2);c=(0,-k*Z**3,0);dom=(-a,0,0,a+X)
 elif name=='exponential':g=h;c=(-k*X*s.exp(Z),0,k*s.exp(Z));disk=s.sqrt(h);boundary=rf'the paraboloid $z=x^2+y^2$ and the plane $z={h}$'
 elif name=='odd_plane':g=h*X;c=(0,k*Z,k*X);disk=a
 elif name=='negative_cone':g=-h;c=(k*Y,2*k*Y*Z,k*(1-Z**2));disk=h;boundary=rf'the half-cone $z=-\sqrt{{x^2+y^2}}$ and the plane $z=-{h}$'
 elif name=='tilted_disk':g=h+2*X-Y;c=(-k*Y,k*Z,-2*k*X);disk=a
 elif name=='shifted_paraboloid':g=(X-h)**2+(Y+h)**2;c=(k*(X+Y),k*(-X+Y),-2*k*Z);disk=a
 elif name=='unrated':g=h-X-2*Y;c=(0,0,-2*k*Y);disk=a
 else:raise ValueError('unknown template')
 g=s.sympify(g);c=tuple(map(s.sympify,c));sub=tuple(s.expand(t.subs(Z,g)) for t in c)
 gx,gy=s.diff(g,X),s.diff(g,Y);terms=(-sub[0]*gx,-sub[1]*gy,sub[2]);f=s.simplify(sum(terms));
 if dom:
  boundary=rf'the surface $z={tex(g)}$ and the vertical column over $D$, where ${tex(s.sympify(dom[0]))}\leq x\leq {tex(s.sympify(dom[1]))}$ and ${tex(s.sympify(dom[2]))}\leq y\leq {tex(s.sympify(dom[3]))}$'
 elif name not in ('horizontal','exponential','negative_cone'):boundary=rf'the cylinder $x^2+y^2={tex(disk**2)}$ and the surface $z={tex(g)}$'
 polar=s.expand_trig(f.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True))*R
 return dict(g=g,c=c,sub=sub,gx=gx,gy=gy,terms=terms,f=f,dom=dom,disk=disk,boundary=boundary,polar=s.expand(polar))

def polar_value(expr,m):
 return s.simplify(s.integrate(s.integrate(expr,(T,0,2*s.pi)),(R,0,m['disk'])))
def setup_value(expr,dom):
 factor=s.simplify(expr/s.sqrt(X**2+Y**2))
 if not factor.has(X,Y) and dom[0]==-dom[1]-dom[3] and dom[1]==0 and dom[2]==0:
  a=dom[3];return s.simplify(factor*a**3*(s.sqrt(2)+s.log(1+s.sqrt(2)))/3)
 return s.simplify(s.integrate(s.integrate(expr,(Y,dom[2],dom[3])),(X,dom[0],dom[1])))

def bank(name,m,p):
 """Complete method banks selected before parameters; never first-valid pools."""
 f=m['f']; k,a,h=map(s.Integer,(p['k'],p['a'],p['h']));d=m['dom'];terms=m['terms']
 if name=='triangle':
  wrong=k*(2*h-4*X**2+4*Y**2)
  pairs=[(f,d),(f,(0,a,0,a)),(wrong,(0,a,0,X)),(wrong,(0,a,0,a)),(wrong,d)]
 elif name=='xy_triangle':pairs=[(f,d),(k*(X**2+2*Y**2),(0,a,0,a-X)),(k*(-2*X*Y+1),(0,a,0,X-a)),(f,(0,a,0,X-a)),(k*(-2*X*Y+1),d)]
 elif name=='reciprocal':
  den=(X**2+Y**2+1)**2
  pairs=[(f,d),(-4*k*h/den,d),(-k*h*X*Y/den,d),(k*h*X**2/den,d),(-k*h*Y**2/den,d)]
 elif name=='cone_triangle':
  u=X**2+Y**2
  pairs=[(f,d),(k*u,d),(k*Y*u**3,(-a,0,0,a)),(k*s.sqrt(u),(-a,0,0,a)),(k*u**2,d)]
 elif name=='tilted_blank':return [f],['correct integrand'],[f]
 elif name=='unrated':return [0,s.pi*a*a*k,-s.pi*a*a*k,2*s.pi*a*a*k,s.pi*a*a*k/2],['correct','opaque area','opaque reverse','opaque double','opaque half'],None
 else:
  A=polar_value(m['polar'],m)
  if name in ('horizontal','exponential'):
   # Wrong plane input; omitted constant contribution; reversed orientation;
   # omit Jacobian (same polar substitution, incorrect area differential).
   other=h+1; bad=m['c'][2].subs(Z,other)
   vals=[A,-A,s.Integer(0),polar_value(bad.subs(X,R*s.cos(T))*R,m),polar_value(m['polar']/R,m) if name=='horizontal' else k*h*s.pi]
   recipes=['correct','reversed orientation','retain only odd x term','substitute z=h+1','omit polar Jacobian' if name=='horizontal' else 'drop the extracted exponential factor']
  elif name=='negative_cone':
   vals=[A,-A,-k*h**4*s.pi,k*(1-h)*h**2*s.pi,k*(1-h**2)*s.pi*h**4]
   recipes=['correct','reversed orientation','omit +1 in R','use z instead of z squared','use radius squared as radius']
  elif name=='odd_plane':
   # Exact zero; wrong evaluation at x=a, wrong nonzero Q contribution,
   # half-disk bounds, and omitted Jacobian with half-disk bounds.
   vals=[A,k*a*s.pi*a*a,-4*k*h*a**3/3,2*k*a**3/3,k*a*a]
   recipes=['correct','freeze x at right endpoint','replace slope zero by one and integrate |x|','use right half-disk','right half-disk without Jacobian']
  elif name=='tilted_disk':
   vals=[A,-A,polar_value((terms[0]+terms[2]).subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R,m),polar_value(m['polar']/R,m),polar_value(m['c'][1].subs(Z,h+1).subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R,m)]
   recipes=['correct','reversed orientation','omit Q slope contribution','omit polar Jacobian','replace plane by z=h+1']
  else:
   vals=[A,-A,polar_value(terms[2].subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R,m),polar_value((terms[0]+terms[1]).subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True)*R,m),polar_value(m['polar']/R,m)]
   recipes=['correct','reversed orientation','omit both slope terms','omit R component','omit polar Jacobian']
  if len(set(map(s.simplify,vals)))!=5:raise ValueError('ambiguous complete bank')
  return vals,recipes,vals
 values=[setup_value(v,dd) if name!='reciprocal' else None for v,dd in pairs]
 if name=='reciprocal':
  # Exact complete-bank distinction: I0=integral 1/(1+r^2)^2>0,
  # J=integral y^2/(1+r^2)^2>0. Symmetry gives Jx=Jy.
  # a=1: J<I0; a=2,3: J/I0 < 11/8 < 2, since
  # I1<=pi ln(1+2a^2), I0>=pi a^2/(1+a^2), ln19<3.
  # Hence -2I0,-4I0,0,+J,-J are pairwise unequal exactly.
  return [integral(v,dd) for v,dd in pairs],['correct','double constant term','odd product numerator','wrong x squared numerator sign','retain negative y squared term'],None
 if any(abs(complex(s.N(values[i]-values[j])))<1e-10 for i in range(len(values)) for j in range(i)):raise ValueError('equivalent complete integral bank')
 return [integral(v,dd) for v,dd in pairs],['correct']+['observed algebra/bounds recipe '+str(i) for i in range(1,5)],values

OPEN=Q['q-162373'][':question/worked-solution'].split('There are many surfaces')[0]
def solution(m):
 g,c,sub=m['g'],m['c'],m['sub'];dx,dy=m['gx'],m['gy'];f=m['f']
 out=OPEN+rf'''There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)={tex(g)}.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{{aligned}}\frac{{\partial g}}{{\partial x}}&=\frac{{\partial}}{{\partial x}}\left({tex(g)}\right)={tex(dx)}\\
\frac{{\partial g}}{{\partial y}}&=\frac{{\partial}}{{\partial y}}\left({tex(g)}\right)={tex(dy)}.\end{{aligned}}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{{curl}}\,F:$

$$\begin{{aligned}}\text{{curl}}\,F|_{{z=g(x,y)}}&={vec(c)}|_{{z={tex(g)}}}\\
&={vec(tuple(v.subs(Z,g) for v in c))}\\
&={vec(sub)}.\end{{aligned}}$$

So, we have

$$\begin{{aligned}}\iint_S\text{{curl}}\,F\cdot\mathrm{{d}}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{{d}}A\\
&=\iint_D\left(-\left({tex(sub[0])}\right)\left({tex(dx)}\right)-\left({tex(sub[1])}\right)\left({tex(dy)}\right)+\left({tex(sub[2])}\right)\right)\,\mathrm{{d}}A\\
&=\iint_D\left({'+'.join('('+tex(t)+')' for t in m['terms'])}\right)\,\mathrm{{d}}A\\
&=\iint_D\left({tex(f)}\right)\,\mathrm{{d}}A.\end{{aligned}}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
'''
 if m['dom']:
  out+='\nTherefore, we obtain\n\n$$'+integral(f,m['dom'])+'.$$\n'
 else:
  b=m['disk'];pol=m['polar'];prim=s.integrate(pol,T);ang=s.simplify(prim.subs(T,2*s.pi)-prim.subs(T,0));rad=s.integrate(ang,R)
  comps=s.Add.make_args(rad);endpoint=lambda v:'+'.join(r'\left('+tex(t.subs(R,v))+r'\right)' for t in comps)
  out+=rf'''Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2={tex(b**2)}.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{{d}}A=r\,\mathrm{{d}}r\,\mathrm{{d}}\theta,$$

we obtain

$$\begin{{aligned}}\iint_D\left({tex(f)}\right)\,\mathrm{{d}}A
&=\int_0^{{{tex(b)}}}\int_0^{{2\pi}}\left({tex(f.subs({X:R*s.cos(T),Y:R*s.sin(T)},simultaneous=True))}\right)r\,\mathrm{{d}}\theta\,\mathrm{{d}}r\\
&=\int_0^{{{tex(b)}}}\int_0^{{2\pi}}\left({tex(pol)}\right)\,\mathrm{{d}}\theta\,\mathrm{{d}}r\\
&=\int_0^{{{tex(b)}}}\left[{tex(prim)}\right]_0^{{2\pi}}\,\mathrm{{d}}r\\
&=\int_0^{{{tex(b)}}}\left[\left({tex(prim.subs(T,2*s.pi))}\right)-\left({tex(prim.subs(T,0))}\right)\right]\,\mathrm{{d}}r\\
&=\int_0^{{{tex(b)}}}\left({tex(ang)}\right)\,\mathrm{{d}}r\\
&=\left[{tex(rad)}\right]_0^{{{tex(b)}}}\\
&=\left[{endpoint(b)}\right]-\left[{endpoint(0)}\right]\\
&={tex(s.simplify(rad.subs(R,b)-rad.subs(R,0)))}.\end{{aligned}}$$
'''
 return out

def render_plots(name,p):
 data={'name':name,'a':p['a'],'renderer_version':4};out=HERE/'assets'/('region-'+digest(data)[:18]+'.png')
 if not (out.exists() and out.with_suffix('.json').exists()):
  with tempfile.NamedTemporaryFile(dir=HERE,suffix='.render-input.json',mode='w',delete=False) as f:
   json.dump(data,f);temp=Path(f.name)
  try:subprocess.run([sys.executable,str(HERE/'render.py'),str(temp),str(out)],check=True,stdout=subprocess.DEVNULL)
  finally:temp.unlink(missing_ok=True)
 return str(out.resolve())

def scaled_string(text,k,role):
 """Lexical unit-preserving multiplier, applied to complete mathematical slots.
 Historical solution rows stay evidence; k denotes scaling the whole curl field.
 """
 factor='' if k==1 else str(k)+r'\left('
 end='' if k==1 else r'\right)'
 if role=='bank':
  if text.startswith('$$'):return text.replace(r'\begin{aligned}',r'\begin{aligned}'+factor).replace(r'\end{aligned}',end+r'\end{aligned}')
  return factor+text+end
 # Whole vector mask; its unscaled P,Q,R components remain inside the vector.
 def cv(m):return factor+m[0]+end
 text=re.sub(r'⟨[^⟩]*⟩',cv,text)
 if role=='solution' and k!=1:
  # Existing graph/partial blocks are invariant; curl substitution has been scaled.
  # Multiply each numeric flux-stage RHS. Generic PQR are the components of the
  # unscaled vector inside k<...>, so the formal graph flux also gets k.
  parts=text.split('$$')
  for i in range(1,len(parts),2):
   if ('{∬}' in parts[i] or '{\\int ' in parts[i]) and 'F\\cdot dr={∬}' not in parts[i]:
    rows=parts[i].split(r'\\')
    for j,row in enumerate(rows):
     if '& =' in row:
      left,right=row.split('& =',1);rows[j]=left+'& ='+factor+right+end
     elif '=' in row and '\\begin{aligned}' not in row:
      left,right=row.split('=',1);rows[j]=left+'='+factor+right+end
    parts[i]=r'\\'.join(rows)
  text='$$'.join(parts)
 return text

def raw(name,k):
 src=Q[FAMILIES[name][1]];q={}
 for key,v in src.items():
  if key in (':db/id',':question/math-academy-id',':question/answer-fields',':question/id'):continue
  q[key]=scaled_string(v,k,'solution' if key==':question/worked-solution' else 'prompt') if isinstance(v,str) else v[':db/ident']
 fs=[]
 for f in src.get(':question/answer-fields',[]):
  ff={key:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else v) for key,v in f.items() if key not in (':db/id',':answer-field/choices',':answer-field/correct',':answer-field/id')}
  vals=[scaled_string(a[':answer/value'],k,'bank') for a in f[':answer-field/choices']]
  ff[':answer-field/choices']=[{':answer/value':v,':answer/type':a[':answer/type'][':db/ident']} for v,a in zip(vals,f[':answer-field/choices'])]
  if ':answer-field/correct' in f:ff[':answer-field/correct']=vals[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])]
  fs.append(ff)
 if ':question/answer-fields' in src:q[':question/answer-fields']=fs
 return q

def record(q,meta,seed):
 content=copy.deepcopy(q);identity=digest([VERSION,content]);qid=uid(identity);q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  fid=uid(qid+'/'+str(i));f[':answer-field/id']=fid;correct=f.pop(':answer-field/correct',None)
  for j,a in enumerate(f[':answer-field/choices']):
   a[':answer/id']=uid(fid+'/'+a[':answer/value']);
   if a[':answer/value']==correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  if f[':answer-field/type']==':answer-field.type/radio':random.Random(seed+i).shuffle(f[':answer-field/choices'])
 meta.update(version=VERSION,seed=seed,content_fingerprint=identity,python=sys.version.split()[0],sympy=s.__version__,database='math',basis=1356,lineage=SOURCE['lineage'])
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 if profile and profile.startswith('raw:'):
  template=SOURCE_FAMILY[profile[4:]]
 name=template or rng.choice([n for n,(lv,src) in FAMILIES.items() if lv==level and n!='unrated'])
 if name not in FAMILIES or FAMILIES[name][0]!=level:raise ValueError('template outside level')
 if profile and profile not in ('authored','normal','raw:'+str(FAMILIES[name][1])):raise ValueError('unsupported profile')
 raw_mode=bool(profile and profile.startswith('raw:'))
 p=dict(parameters) if parameters is not None else ({'k':rng.randint(1,4),'a':rng.randint(1,3),'h':rng.randint(1,4)} if not raw_mode else {'k':1})
 if raw_mode:
  if set(p)!={'k'} or type(p['k'])!=int or not 1<=p['k']<=4:raise ValueError('raw domain k=1..4')
  if field_type:raise ValueError('raw layouts fixed')
  return record(raw(name,p['k']),{'template':name,'profile':profile,'bank_profile':profile,'parameters':p,'evidence_only':True,'eligible_for_learning':False,'math_fingerprint':digest([name,p])},seed)
 if set(p)!={'k','a','h'} or any(type(v)!=int for v in p.values()) or not 1<=p['k']<=4 or not 1<=p['a']<=3 or not 1<=p['h']<=4:raise ValueError('normal domain k=1..4,a=1..3,h=1..4')
 if name in ('triangle','negative_cone') and parameters is None:p['h']=rng.randint(2,4)
 if name=='negative_cone' and p['h']==1:raise ValueError('negative-cone h>=2')
 if name=='unrated':raise ValueError('unrated evidence profile only')
 m=model(name,p)
 typ='blank' if name=='tilted_blank' else 'radio'
 if field_type and field_type!=typ:raise ValueError('source layout fixed')
 try:vals,recipes,numeric=bank(name,m,p)
 except ValueError:
  if parameters is not None:raise
  for _ in range(100):
   p={'k':rng.randint(1,4),'a':rng.randint(1,3),'h':rng.randint(2,4) if name=='negative_cone' else rng.randint(1,4)};m=model(name,p)
   try:vals,recipes,numeric=bank(name,m,p);break
   except ValueError:continue
  else:raise ValueError('no eligible complete bank')
 text=rf"Let $C$ be the intersection of {m['boundary']}. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{{curl}}\,F={vec(m['c'])}$, "
 text+='use Stokes\' theorem to '+('write down the integral that gives the circulation along $C.$' if m['dom'] else 'evaluate $\\oint_C F\\cdot\\mathrm{d}r.$')
 strings=[v if isinstance(v,str) else tex(v) for v in vals]
 if typ=='blank':text+=r' The circulation is $\int_0^{'+str(p['a'])+r'}\int_0^{'+str(p['a'])+r'}$ {{field-1}} $\mathrm{d}y\,\mathrm{d}x$.'
 answer_type=Q[FAMILIES[name][1]][':question/answer-fields'][-1][':answer-field/choices'][0][':answer/type'][':db/ident'] if FAMILIES[name][1] else ':answer.type/math'
 if answer_type==':answer.type/text':strings=['$$\n'+r'\begin{aligned}'+v+r'\end{aligned}'+'\n$$' for v in strings]
 answers=[{':answer/type':answer_type,':answer/value':v} for v in strings]
 worked=solution(m)
 if m['dom']:
  path=render_plots(name,p);worked=worked.replace('Therefore, we obtain', '![]('+path+')\n\nTherefore, we obtain')
 q={':question/problem':text,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'field-1' if typ=='blank' else 'selection',':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':answers,':answer-field/correct':strings[0]}]}
 graph_task=m['g'] if any(c.has(Z) for c in m['c']) else s.simplify(m['g']-m['g'].subs({X:0,Y:0}))
 mathematical=[level,tex(graph_task),[tex(c) for c in m['c']],str(m['dom']),str(m['disk'])]
 return record(q,{'template':name,'profile':'authored','bank_profile':'authored:'+name,'parameters':p,'evidence_only':False,'eligible_for_learning':True,'source_ids':[FAMILIES[name][1]] if FAMILIES[name][1] else ['e-12422'],'recipes':recipes,'math_fingerprint':digest(mathematical),'stages':{key:tex(m[key]) for key in ('g','gx','gy','f','polar')}},seed)

# Easy entrypoint: authored horizontal disk grounded in the canonical example.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate entrypoint: source Cartesian setup families; no evaluation demand.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard entrypoint: observed polar evaluation families, same prerequisite methods.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
 q=r['question'];meta=r['generation'];raw=meta['evidence_only'];label=('Original source evidence' if meta['parameters']['k']==1 else 'Generated source evidence') if raw else 'Generated variant'
 level=q.get(':question/difficulty','unrated').split('/')[-1]
 out='## '+label+' — '+level+'\n\n'+q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  for a in f[':answer-field/choices']:
   value=a[':answer/value'];value='$'+value+'$' if a[':answer/type']==':answer.type/math' and not value.startswith('$$') else value
   out+='- '+value+(' **(source designation)**' if raw and a[':answer/id']==correct else ' **(correct)**' if a[':answer/id']==correct else '')+'\n'
  if correct is None:out+='Original correct designation absent.\n'
 out+='\n**Worked solution**\n\n'+q.get(':question/worked-solution','Original worked solution absent.')
 return out.replace('![](images/','![](/media/jake/SSD/EDB/math/images/')

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133927-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 rec=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(rec,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rec)))
