#!/usr/bin/env python3
"""Inferred-from-integrand change-of-variables generators, frozen math basis1356.

Source families have public evidence-only scale profiles, retaining complete raw
banks and missing attributes. Their opaque error intent is not promoted into
learning. Normal defaults use the same family-specific five-step operative masks
and whole method-derived banks. Easy is canonical polynomial/shear; moderate is
an affine shifted polynomial (unrated source, authored assignment); hard retains
all five rated rational/trigonometric/exponential source families. No EDB writes.

Every primitive endpoint is evaluated separately, before the final subtraction.
Parameter guards apply equally to explicit inputs. Profiles are selected before
parameters. Identity excludes seed/order, mathematical identity excludes banks.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, json, random, re, sys, uuid, os, tempfile, threading
from pathlib import Path
import sympy as s
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186198374-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

KP_ID=17592186198374
KP_UUID='b2682751-23e4-5cf2-9a46-82c75765423f'
TITLE='Cases When the Transformation Is Inferred From the Integrand'
VERSION='integrand-transform-2-audit9837'
SUPPORTED_LEVELS=('easy','hard')
# Current source q-160896 was completed and rated hard after frozen basis1356.
# The previous authored moderate assignment is superseded, not a usable reserve.
ROOT=Path(__file__).resolve().parent
OUT=ROOT/str(KP_ID)
SOURCE=json.loads((OUT/'source.json').read_text())
RECORD=SOURCE['record']
SOURCES={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
x,y,u,v=s.symbols('x y u v',real=True)
FAMILIES={'polynomial':'easy','shifted_polynomial':'hard','rational':'hard','sine':'hard','exponential':'hard','exponential_square':'hard','cosine_square':'hard'}
SOURCE_FAMILY={'q-160433':'rational','q-160896':'shifted_polynomial','q-160901':'sine','q-160904':'exponential','q-160933':'exponential_square','q-160935':'cosine_square'}
RAW_EXPRESSIONS={
'q-160433':[[s.Rational(7,3)*s.log(2),s.log(2)/9,s.log(2)/3,2*s.log(2),s.Rational(2,3)*s.log(2)],[2*s.log(2),s.Rational(7,3)*s.log(2),s.log(2)/3,s.log(2)/9,s.Rational(2,3)*s.log(2)]],
'q-160896':[[42,84,64,11,21]],
'q-160901':[[2,s.pi,3/(2*s.pi),1,1/s.pi]],
'q-160904':[[3*(s.E-1)/s.E**2,1/s.E**2,(2*s.E-1)/s.E**2,s.E*(1-s.E),1/s.E]],
'q-160933':[[s.exp(4)-s.E,s.exp(3)-s.exp(2),s.exp(4)-2*s.exp(2)+3,4*s.exp(2),s.exp(3)-2*s.E+1]],
'q-160935':[[s.sin(s.pi/s.sqrt(2)),s.sin(s.pi**2/4),1,2*s.sin(s.pi**2/2),s.sqrt(2)/2]]}
ANCHORS={
'polynomial':dict(matrix=[2,1,0,1],shift=[0,0],bounds=[3,5,0,3]),
'shifted_polynomial':dict(matrix=[2,0,1,1],shift=[-1,0],bounds=[1,3,1,4]),
'rational':dict(matrix=[1,1,2,1],shift=[0,0],bounds=[1,2,1,2]),
'sine':dict(matrix=[1,0,1,1],shift=[0,0],bounds=[0,1,0,1]),
'exponential':dict(matrix=['1/2',1,1,3],shift=[0,0],bounds=[1,2,-2,-1]),
'exponential_square':dict(matrix=[1,0,2,-1],shift=[0,0],bounds=[2,4,1,2]),
'cosine_square':dict(matrix=[1,-1,1,1],shift=[0,0],bounds=[1,3,0,'pi/2'])}

def dump(obj):return json.dumps(asset_payload(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def uid(*parts):return str(uuid.uuid5(uuid.UUID(KP_UUID),dump(parts)))
def no_hyperbolic(z):
    z=s.sympify(z);return z.xreplace({a:a.rewrite(s.exp) for a in z.atoms(s.sinh,s.cosh,s.tanh)})
def tex(z):return s.latex(no_hyperbolic(z)).replace(r'\log',r'\ln')
def group(z):return r'\left('+tex(z)+r'\right)'
def parse(z):
    if isinstance(z,(int,s.Expr)): return s.sympify(z)
    if not isinstance(z,str) or not re.fullmatch(r'[0-9piE*/+(). -]+',z):raise ValueError('exact numeric parameter required')
    return s.sympify(z,locals={'pi':s.pi,'E':s.E})
def canonical_parameters(p):
    if set(p)-{'matrix','shift','bounds','scale'} or not {'matrix','shift','bounds'}<=set(p):raise ValueError('complete matrix/shift/bounds parameters required')
    q={k:[parse(z) for z in p[k]] for k in ['matrix','shift','bounds']}
    q['scale']=parse(p.get('scale',1));return q
def serial(p):return {k:[str(z) for z in val] if isinstance(val,list) else str(val) for k,val in p.items()}
def eq(a,b):return s.simplify(a-b)==0
def validate_parameters(level,family,p):
    if FAMILIES[family]!=level:raise ValueError('template outside difficulty')
    if len(p['matrix'])!=4 or len(p['shift'])!=2 or len(p['bounds'])!=4:raise ValueError('parameter arity')
    a,b,c,d=p['matrix'];h,k=p['shift'];a0,a1,b0,b1=p['bounds'];scale=p['scale']
    if any(not z.is_real or not z.is_finite for z in p['matrix']+p['shift']+p['bounds']+[scale]):raise ValueError('finite real parameters required')
    if a*d-b*c==0 or not a1>a0 or not b1>b0:raise ValueError('invertible matrix and ordered rectangle required')
    if not scale.is_Integer or not 1<=scale<=3:raise ValueError('scale integer1..3')
    if any(abs(z)>5 for z in p['matrix']+p['shift']):raise ValueError('coefficient arithmetic ceiling5')
    if any(abs(z)>8 for z in p['bounds']):raise ValueError('bounds arithmetic ceiling8')
    if family!='cosine_square' and any(not z.is_Integer for z in p['bounds']):raise ValueError('source-sized integer rectangle bounds required')
    if family=='cosine_square' and (not a0.is_Integer or not a1.is_Integer):raise ValueError('integer u bounds in cosine family')
    if family=='polynomial':
        if c!=0 or d!=1 or h!=0 or k!=0 or a not in [1,2,3] or b not in [-2,-1,1,2] or a0<1 or b0<0:raise ValueError('easy canonical shear bounds')
    if family=='shifted_polynomial':
        if b!=0 or c!=1 or a not in [2,3,4] or d not in [1,2] or h not in [-3,-2,-1,1,2,3] or k!=0 or a0<1 or b0<1:raise ValueError('moderate affine shift must remain substantive')
    if family=='rational' and (h!=0 or k!=0 or a!=1 or b!=1 or c not in [2,3,4] or d!=1 or a0<1 or b0<1):raise ValueError('hard rational family bounds')
    if family=='sine' and (a!=1 or b!=0 or c not in [1,2,3] or d!=1 or h!=0 or k!=0 or b0!=0 or b1!=1 or a0<0):raise ValueError('hard sine familiar angle family')
    if family=='exponential' and (a not in [s.Rational(1,2),1] or b!=1 or c!=1 or d not in [2,3,4] or h!=0 or k!=0 or a0<1):raise ValueError('hard exponential matrix domain')
    if family=='exponential_square' and (a!=1 or b!=0 or c not in [1,2,3] or d!=-1 or h!=0 or k!=0 or a0<0 or b0<1):raise ValueError('hard exp square domain')
    if family=='cosine_square' and (p['matrix']!=[1,-1,1,1] or h!=0 or k!=0 or a0<1 or b0!=0 or b1 not in [s.pi/2,s.pi/3,s.pi/4]):raise ValueError('hard factor-and-chain domain')

def sample(family,rng):
    p=dict(ANCHORS[family]);p['scale']=rng.choice([1,2,3]);p['matrix']=list(p['matrix']);p['shift']=list(p['shift']);p['bounds']=list(p['bounds'])
    lo=rng.randint(1,4);hi=lo+rng.randint(1,3)
    if family=='polynomial':p.update(matrix=[rng.randint(1,3),rng.choice([-2,-1,1,2]),0,1],bounds=[lo,hi,rng.randint(0,1),rng.randint(2,4)])
    elif family=='shifted_polynomial':p.update(matrix=[rng.randint(2,4),0,1,rng.randint(1,2)],shift=[rng.choice([-3,-2,-1,1,2,3]),0],bounds=[lo,hi,rng.randint(1,2),rng.randint(3,5)])
    elif family=='rational':p.update(matrix=[1,1,rng.randint(2,4),1],bounds=[lo,hi,rng.randint(1,3),rng.randint(4,6)])
    elif family=='sine':p.update(matrix=[1,0,rng.randint(1,3),1],bounds=[rng.randint(0,3),rng.randint(4,6),0,1])
    elif family=='exponential':
        a,d=rng.choice([('1/2',3),('1/2',4),(1,2),(1,3),(1,4)]);p.update(matrix=[a,1,1,d],bounds=[lo,hi,rng.choice([-3,-2,0,1]),rng.choice([2,3])])
    elif family=='exponential_square':p.update(matrix=[1,0,rng.randint(1,3),-1],bounds=[lo,hi,rng.randint(1,2),rng.randint(3,4)])
    else:p.update(bounds=[lo,hi,0,rng.choice(['pi/2','pi/3','pi/4'])])
    return canonical_parameters(p)

def components(family,p):
    a,b,c,d=p['matrix'];h,k=p['shift'];a0,a1,b0,b1=p['bounds'];sc=p['scale'];M=s.Matrix([[a,b],[c,d]]);det=M.det();J=1/det;C=sc*abs(J)
    ux=a*x+b*y+h;vx=c*x+d*y+k
    inv=M.inv()*(s.Matrix([u,v])-s.Matrix([h,k]));corners=[(a0,b0),(a1,b0),(a1,b1),(a0,b1)]
    vertices=[tuple(s.simplify(z.subs({u:U,v:V})) for z in inv) for U,V in corners]
    if family in ['polynomial','shifted_polynomial']:fu=u;fv=v**2;Au=u**2/2;Av=v**3/3
    elif family=='rational':fu=u**2;fv=1/v;Au=u**3/3;Av=s.log(v)
    elif family=='sine':fu=u;fv=s.sin(s.pi*v);Au=u**2/2;Av=-s.cos(s.pi*v)/s.pi
    elif family=='exponential':fu=u;fv=s.exp(v);Au=u**2/2;Av=s.exp(v)
    elif family=='exponential_square':fu=s.Integer(1);fv=v*s.exp(v**2);Au=u;Av=s.exp(v**2)/2
    else:fu=u;fv=v*s.cos(v**2);Au=u**2/2;Av=s.sin(v**2)/2
    F=fu*fv;fxy=F.subs({u:ux,v:vx},simultaneous=True)*sc
    if family=='cosine_square':fxy=sc*(x*x-y*y)*s.cos((x+y)**2)
    eU=[s.simplify(Au.subs(u,z)) for z in [a1,a0]];eV=[s.simplify(Av.subs(v,z)) for z in [b1,b0]]
    Iu=no_hyperbolic(s.simplify(eU[0]-eU[1]));Iv=no_hyperbolic(s.simplify(eV[0]-eV[1]));ans=no_hyperbolic(s.simplify(C*Iu*Iv))
    return dict(M=M,det=det,J=J,C=C,ux=ux,vx=vx,inv=inv,corners=corners,vertices=vertices,fu=fu,fv=fv,Au=Au,Av=Av,F=F,fxy=fxy,eU=eU,eV=eV,Iu=Iu,Iv=Iv,answer=ans)

def bank(family,p,z):
    """Complete, chosen-before-sampling method bank; never pooled replacement."""
    C,Iu,Iv,A=z['C'],z['Iu'],z['Iv'],z['answer'];a0,a1,b0,b1=p['bounds'];width=a1-a0
    if family in ['polynomial','shifted_polynomial']:vals=[A,-A,2*A,3*A,C*width*Iv];recipes=['correct','reverse u bounds','omit u primitive denominator2','omit v primitive denominator3','replace u by1']
    elif family=='rational':vals=[A,-A,3*A,C*width*Iv,C*Iu*(b1-b0)];recipes=['correct','reverse u bounds','omit u primitive denominator3','replace u^2 by1','replace1/v by1']
    elif family=='sine':vals=[A,-A,s.pi*A,s.pi**2*A,C*width*Iv];recipes=['correct','reverse bounds','omit reciprocal frequency','multiply frequency instead of divide','replace u by1']
    elif family=='exponential':vals=[A,-A,2*A,C*width*Iv,C*Iu*(z['eV'][0]+z['eV'][1])];recipes=['correct','reverse bounds','omit u primitive denominator2','replace u by1','add v endpoints']
    elif family=='exponential_square':vals=[A,-A,2*A,C*width*(s.exp(b1)-s.exp(b0)),C*width*(z['eV'][0]+z['eV'][1])];recipes=['correct','reverse bounds','omit chain factor1/2','replace exp(v^2) endpoint by exp(v)','add v endpoints']
    else:vals=[A,-A,2*A,C*Iu*(s.sin(b1)-s.sin(b0)),C*width*Iv];recipes=['correct','reverse bounds','omit chain factor1/2','replace sin(v^2) endpoint by sin(v)','replace u by1']
    vals=[no_hyperbolic(s.simplify(q)) for q in vals]
    if any(not q.is_finite or q.has(s.zoo,s.nan) for q in vals):raise ValueError('invalid whole bank')
    for i,q in enumerate(vals):
        for t in vals[:i]:
            if eq(q,t) or abs(float(s.N(q-t,18)))<1e-12:raise ValueError('ambiguous whole bank')
    return vals,recipes

_PLOT_LOCK=threading.RLock()
def rectangle_plot(p):
    # Matplotlib mathtext has process-global mutable parser state.
    with _PLOT_LOCK:return _rectangle_plot(p)

def _rectangle_plot(p):
    """Source rectangle conventions, exact bounds carried into one atomic asset."""
    path=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(OUT/'plots')));path.mkdir(parents=True,exist_ok=True);key=hashlib.sha256(dump(['rectangle-layout2',serial(p)['bounds']]).encode()).hexdigest()[:20];png=path/(key+'.png');meta=path/(key+'.json')
    if png.exists() and meta.exists():return str(png)
    a0,a1,b0,b1=p['bounds'];aa,bb,cc,dd=[float(s.N(t)) for t in p['bounds']];w=bb-aa;h=dd-cc
    fig,ax=plt.subplots(figsize=(4.8,4),dpi=125)
    ax.add_patch(Rectangle((aa,cc),w,h,facecolor='#dfeaf2',edgecolor='none'))
    ax.plot([aa,bb],[cc,cc],color='red',lw=1.5);ax.plot([aa,bb],[dd,dd],color='blue',lw=1.5)
    xmin=min(0,aa)-w*.5;xmax=max(0,bb)+w*.5;ymin=min(0,cc)-h*.55;ymax=max(0,dd)+h*.55
    ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
    ax.annotate('',(xmax,0),(xmin,0),arrowprops=dict(arrowstyle='->',color='black'));ax.annotate('',(0,ymax),(0,ymin),arrowprops=dict(arrowstyle='->',color='black'))
    for A,B in [(aa,cc),(bb,cc),(aa,dd),(bb,dd)]:
        ax.plot([A,A],[0,B],ls='--',color='.65',lw=.6);ax.plot([0,A],[B,B],ls='--',color='.65',lw=.6);ax.plot(A,B,'ko',ms=4)
    for A,B,ea,eb,up in [(aa,cc,a0,b0,False),(bb,cc,a1,b0,False),(aa,dd,a0,b1,True),(bb,dd,a1,b1,True)]:
        ax.annotate('$('+tex(ea)+','+tex(eb)+')$',(A,B),xytext=(-7 if A==aa else 7,13 if up else -20),textcoords='offset points',ha='right' if A==aa else 'left',fontsize=10)
    ax.text((aa+bb)/2,dd+h*.07,'$v='+tex(b1)+'$',color='blue',ha='center');ax.text((aa+bb)/2,cc-h*.17,'$v='+tex(b0)+'$',color='red',ha='center');ax.text((aa+bb)/2,(cc+dd)/2,r'$\Delta$',color='#477799',ha='center')
    ax.text(xmax,0,'$u$',va='bottom');ax.text(0,ymax,'$v$',ha='right');ax.axis('off');fig.tight_layout()
    fd,tmp=tempfile.mkstemp(suffix='.png',dir=path);os.close(fd)
    try:fig.savefig(tmp,facecolor='white');os.replace(tmp,png)
    finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
    payload=dict(renderer='Matplotlib',version=matplotlib.__version__,bounds=[str(t) for t in p['bounds']],geometry='rectangle with all four labelled corners; lower red upper blue; dashed coordinate guides',image_sha256=hashlib.sha256(png.read_bytes()).hexdigest())
    fd,tmp=tempfile.mkstemp(suffix='.json',dir=path);os.close(fd);Path(tmp).write_text(json.dumps(payload,indent=2));os.replace(tmp,meta)
    return str(png)

def prompt(family,p,z):
    verts=['$('+tex(A)+','+tex(B)+')$' for A,B in z['vertices']]
    return 'Use a change of variables to evaluate the double integral \n\n$$\n'+r'\iint_D '+tex(z['fxy'])+r'\,\mathrm{d}x\,\mathrm{d}y,'+'\n$$\n\nwhere $D$ is the quadrilateral region with vertices '+', '.join(verts[:3])+ ' and '+verts[3]+'.'

def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def display(t):return '\n\n$$\n'+t+'\n$$\n\n'
def shown_linear_sub(expr,A,B):
    """Construct complete numeric factors; no blind symbol replacements."""
    poly=s.Poly(expr,x,y);a=poly.coeff_monomial(x);b=poly.coeff_monomial(y);h=poly.coeff_monomial(1)
    return group(a)+r'\cdot '+group(A)+'+'+group(b)+r'\cdot '+group(B)+'+'+group(h)

def solution(family,p,z,plot):
    """Family-specific operation rows preserve source order and shared prose.
    Endpoint-detail additions are expressly documented, never collapsed by CAS.
    """
    a0,a1,b0,b1=p['bounds'];sc=p['scale'];C=z['C'];fu,fv=z['fu'],z['fv'];F=z['F'];Au,Av=z['Au'],z['Av'];eU,eV=z['eU'],z['eV']
    base=SOURCES['q-160433'][':question/worked-solution'];before=base.split('**Step 1**')[0]
    text=before+'**Step 1**: Find a suitable change of variables.\n\nThe integrand'
    factor=tex(z['fxy'])
    if family=='cosine_square':factor+='='+tex(sc)+r'(x-y)(x+y)\cos((x+y)^2)'
    text+=display('f(x,y)='+factor)+'suggests that we use the change of variables '+display('u='+tex(z['ux'])+r',\qquad v='+tex(z['vx'])+'.')
    text+='This change of variables gives us the *inverse* function ${T}^{-1},$ that is'+display(r'T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).')
    text+='**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ \n\nThe vertices of our domain $Δ$ in the $uv$-plane are as follows:'
    rows=[]
    for (A,B),(U,V) in zip(z['vertices'],z['corners']):
        rows.extend([r'T^{-1}('+tex(A)+','+tex(B)+')&=('+shown_linear_sub(z['ux'],A,B)+','+shown_linear_sub(z['vx'],A,B)+')',r'&=('+tex(U)+','+tex(V)+')'])
    text+=display(aligned(rows))+'Therefore, our domain in the $uv$-plane is the following rectangle:'+display(r'\Delta=\{(u,v):'+tex(a0)+r'\le u\le '+tex(a1)+r',\ '+tex(b0)+r'\le v\le '+tex(b1)+r'\}')+'![]('+plot+')\n\n'
    text+='**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is'
    a,b,c,d=p['matrix'];text+=display(aligned([r'\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix}',r'&=\begin{vmatrix}'+tex(a)+'&'+tex(b)+r'\\'+tex(c)+'&'+tex(d)+r'\end{vmatrix}',r'&='+tex(z['det'])+'.']))
    text+='**Step 4**: Compute the Jacobian determinant corresponding to $T:$'+display(r'\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}='+tex(z['J']))
    text+='Note that $\\frac{∂(x,y)}{∂(u,v)}\\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$\n\n'
    text+='Solving these affine equations also gives'+display('x='+tex(z['inv'][0])+r',\qquad y='+tex(z['inv'][1])+'.')
    text+='**Step 5**: Perform the change of variables, and evaluate the integral:\n\nPerforming the change of variables, we obtain'
    D=r'\iint_D ';DD=r'\iint_\Delta ';diff=r'\,\mathrm{d}u\,\mathrm{d}v';vint=r'\int_{'+tex(b0)+'}^{'+tex(b1)+'}';uint=r'\int_{'+tex(a0)+'}^{'+tex(a1)+'}'
    rows=[]
    left=D+tex(z['fxy'])+r'\,\mathrm{d}x\,\mathrm{d}y'
    if family=='cosine_square':rows.append(left+'&='+D+tex(sc)+r'(x-y)(x+y)\cos((x+y)^2)\,\mathrm{d}x\,\mathrm{d}y');left=''
    rows.append(left+'&='+DD+tex(sc*F)+r'\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|'+diff)
    rows.append('&='+DD+tex(sc*F)+r'\,\left|'+tex(z['J'])+r'\right|'+diff)
    if family=='rational':rows.append('&='+DD+tex(C*F)+diff)
    rows.append('&='+tex(C)+r'\cdot '+vint+uint+tex(F)+diff)
    # Rational original factors u first; other source families factor v first.
    vfactor=vint+tex(fv)+r'\,\mathrm{d}v';ufactor=uint+tex(fu)+r'\,\mathrm{d}u'
    if family=='rational':pairs=[('u',Au,a0,a1),('v',Av,b0,b1)];rows.append('&='+tex(C)+r'\cdot '+ufactor+r'\cdot '+vfactor)
    else:pairs=[('v',Av,b0,b1),('u',Au,a0,a1)];rows.append('&='+tex(C)+r'\cdot '+vfactor+r'\cdot '+ufactor)
    brackets=[r'\left['+tex(prim)+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}' for _,prim,lo,hi in pairs];rows.append('&='+tex(C)+r'\cdot '+r'\cdot '.join(brackets))
    # Keep each evaluated endpoint in its own signed subtraction component.
    substitutions=[];evaluations=[];differences=[]
    for name,prim,lo,hi in pairs:
        variable=u if name=='u' else v
        # Unevaluated endpoint masks survive zero and negative inputs.
        def endpoint(t):
            if name=='u':
                if family=='rational':return group(t)+r'^{3}/3'
                if family=='exponential_square':return group(t)
                return group(t)+r'^{2}/2'
            if family in ['polynomial','shifted_polynomial']:return group(t)+r'^{3}/3'
            if family=='rational':return r'\ln '+group(t)
            if family=='sine':return r'-\cos\left(\pi\cdot '+group(t)+r'\right)/\pi'
            if family=='exponential':return r'e^{'+tex(t)+'}'
            if family=='exponential_square':return r'e^{'+group(t)+r'^{2}}/2'
            return r'\sin\left('+group(t)+r'^{2}\right)/2'
        substitutions.append(r'\left('+endpoint(hi)+'-'+r'\left('+endpoint(lo)+r'\right)\right)')
        e=eU if name=='u' else eV;I=z['Iu'] if name=='u' else z['Iv']
        evaluations.append(r'\left('+group(e[0])+'-'+group(e[1])+r'\right)');differences.append(group(I))
    rows.append('&='+tex(C)+r'\cdot '+r'\cdot '.join(substitutions))
    rows.append('&='+tex(C)+r'\cdot '+r'\cdot '.join(evaluations))
    rows.append('&='+tex(C)+r'\cdot '+r'\cdot '.join(differences))
    rows.append('&='+tex(z['answer'])+'.')
    text+=display(aligned(rows))
    return text

def enum(value):return value[':db/ident'] if isinstance(value,dict) else value

def raw_scale_string(t,c):
    """Complete component scaling slot; at unit scale uses the empty multiplier."""
    prefix='' if c==1 else tex(c)+r'\cdot '
    if c==1:return prefix+t
    tail='.' if t.endswith('.') else ''
    component=t[:-1] if tail else t
    return prefix+r'\left('+component+r'\right)'+tail

def raw_question(source_id,c):
    """Extracted source masks, not a literal-payload replay branch.

    One coherent scale parameter changes the integrand, all integral-stage RHSs,
    and every answer. Unknown historical wrong recipes remain opaque evidence.
    Fixed region/transform stages intentionally stay fixed under scaling.
    """
    q=SOURCES[source_id]; family=SOURCE_FAMILY[source_id]
    problem=q[':question/problem'];sol=q.get(':question/worked-solution')
    if '$$' in problem:
        component=problem.split('$$')[1];match=re.match(r'\s*\{∬\}_\{D\}(.*)\\,dxdy,\s*',component)
        integrand=match.group(1)
    else:integrand='(2x - 1)(x + y)^{2}'
    problem=problem.replace(integrand,raw_scale_string(integrand,c))
    if sol is not None:
        # Source integrand slot appears in f(x,y) and first/optional expanded integral.
        sol=sol.replace(integrand,raw_scale_string(integrand,c))
        prefix,chain=sol.rsplit('\\begin{aligned}',1)
        body,suffix=chain.split('\\end{aligned}',1)
        chunks=body.split(' & ')
        # Integrand slots on LHS already scaled; all RHS complete expressions scale.
        scaled=[chunks[0]]
        for chunk in chunks[1:]:
            row,sep,tail=chunk.partition(' \\\\ ')
            if row.startswith('='):row='='+raw_scale_string(row[1:],c)
            else:row=raw_scale_string(row,c) # source rational primitive row lacks =
            scaled.append(row+sep+tail)
        sol=prefix+'\\begin{aligned}'+' & '.join(scaled)+'\\end{aligned}'+suffix
    result={':question/id':uid('raw',source_id,str(c),problem,sol),':question/problem':problem}
    if ':question/difficulty' in q:result[':question/difficulty']=enum(q[':question/difficulty'])
    if sol is not None:result[':question/worked-solution']=sol
    fields=[]
    for fi,f in enumerate(q.get(':question/answer-fields',[])):
        choices=[];mapping={}
        for ai,a in enumerate(f[':answer-field/choices']):
            val=raw_scale_string(a[':answer/value'],c);ID=uid('raw-answer',source_id,fi,ai,str(c),val);mapping[a[':answer/id']]=ID
            choices.append({':answer/id':ID,':answer/type':enum(a[':answer/type']),':answer/value':val})
        field={':answer-field/id':uid('raw-field',source_id,fi,str(c)),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/choices':choices}
        if ':answer-field/correct' in f:field[':answer-field/correct']=[':answer/id',mapping[f[':answer-field/correct'][':answer/id']]]
        fields.append(field)
    if ':question/answer-fields' in q:result[':question/answer-fields']=fields
    signature=[]
    for f in fields:
        selected=next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),None)
        signature.append([f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),selected])
    qid=uid('raw-content',VERSION,result.get(':question/difficulty'),problem,sol,signature)
    result[':question/id']=qid
    for fi,f in enumerate(fields):
        fid=uid('raw-field',qid,fi);f[':answer-field/id']=fid;mapping={}
        for a in f[':answer-field/choices']:
            mapping[a[':answer/id']]=uid('answer',fid,a[':answer/value']);a[':answer/id']=mapping[a[':answer/id']]
        if ':answer-field/correct' in f:f[':answer-field/correct'][1]=mapping[f[':answer-field/correct'][1]]
    return result

# Easy: canonical integrand factor u and visible y^2, one shear, power primitives.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: unrated source's affine (ax+h) factor must retain h!=0, then two powers.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed reciprocal, trig, exponential and squared-inner-function families.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported moderate: current shifted-polynomial source is rated hard; see capabilities.json')
    if field_type is not None and field_type not in ['radio',':answer-field.type/radio']:raise ValueError('only observed radio field supported')
    rng=random.Random(seed)
    if profile and profile.startswith('raw:'):
        sid=profile[4:]
        if sid not in SOURCES:raise ValueError('unknown raw source profile')
        fam=SOURCE_FAMILY[sid]
        if template not in [None,fam]:raise ValueError('raw profile family mismatch')
        if level!=FAMILIES[fam]:raise ValueError('raw family difficulty mismatch')
        params=parameters or {'scale':1}
        if set(params)!={'scale'}:raise ValueError('raw profile accepts only scale1..3')
        c=parse(params['scale'])
        if not c.is_Integer or not 1<=c<=3:raise ValueError('raw scale1..3')
        q=raw_question(sid,c)
        for f in q.get(':question/answer-fields',[]):rng.shuffle(f[':answer-field/choices'])
        z=components(fam,canonical_parameters(ANCHORS[fam]))
        return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':fam,'profile':profile,'parameters':{'scale':str(c)},'difficulty':level,'source_id':sid,'authored_level':':question/difficulty' not in SOURCES[sid],'mathematical_fingerprint':hashlib.sha256(dump([fam,str(c*z['fxy']),[[str(t) for t in vv] for vv in z['vertices']]]).encode()).hexdigest(),'eligible_for_learning':False,'evidence_only':True,'opaque_bank_interpretation':True,'answer_exact':str(c*z['answer']),'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'runtime':{'python':sys.version.split()[0],'sympy':s.__version__,'matplotlib':matplotlib.__version__}}}
    if profile not in [None,'method']:raise ValueError('unknown bank profile')
    families=[f for f,l in FAMILIES.items() if l==level]
    if template is not None and template not in families:raise ValueError('template outside difficulty')
    family=template or rng.choice(families)
    # A whole bank was selected above; sampling repeats only complete invalid instances.
    for attempt in range(200):
        p=canonical_parameters(parameters) if parameters is not None else sample(family,rng)
        validate_parameters(level,family,p);z=components(family,p)
        try:vals,recipes=bank(family,p,z)
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else:raise ValueError('no eligible whole instance')
    plot=rectangle_plot(p);prob=prompt(family,p,z);sol=solution(family,p,z,plot);value_strings=[tex(t) for t in vals]
    fp=hashlib.sha256(dump([family,str(z['fxy']),[[str(t) for t in vv] for vv in z['vertices']]]).encode()).hexdigest()
    prob=normalize_prose(prob);sol=normalize_prose(sol);value_strings=[normalize_tex(v)for v in value_strings]
    identity=[VERSION,level,prob,sol,sorted(value_strings)]
    qid=uid('question',identity);fid=uid('field',qid,'selection');answers=[{':answer/id':uid('answer',fid,value),':answer/type':':answer.type/math',':answer/value':value} for value in value_strings]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prob,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':family,'difficulty':level,'profile':'method','parameters':serial(p),'mathematical_fingerprint':fp,'eligible_for_learning':True,'evidence_only':False,'authored_level':level!='hard','authored_bank':True,'source_id':[k for k,f in SOURCE_FAMILY.items() if f==family],'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'answer_exact':str(z['answer']),'choices_exact':[str(t) for t in vals],'recipes':recipes,'domain':'affine globally injective; rectangular preimage; denominator positive where used','plot':plot,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__,'matplotlib':matplotlib.__version__}}}

def markdown(r):
    q=r['question'];text=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        for i,a in enumerate(f[':answer-field/choices']):text+=f'{i+1}. ${a[":answer/value"]}$\n'
    return text+'\n'+q.get(':question/worked-solution','[Raw source has no worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();levels=SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]
    rows=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
