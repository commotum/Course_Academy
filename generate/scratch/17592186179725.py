#!/usr/bin/env python3
"""Basis-2275 scalar arc-length integrals on straight 3D segments.
Seven parameterized historical profiles are evidence-only (opaque distractors;
two records have no solution/rating/key). Normal generation uses complete
method banks and the same coordinate/vector/speed/pullback/integration stages.
No plots, database clients, or writes. See adjacent extraction and validation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as S
KP_ID=17592186179725
KP_UUID='14ab317b-fd33-5d6e-9d54-87e749b78283'
TITLE='Line Integrals Along Segments in Three Dimensions'
VERSION='segments-3d-1'
BASE=Path(__file__).with_suffix('')
T,X,Y,Z,U=S.symbols('t x y z u',real=True)
LEVELS={'sum':'easy','quotient':'easy','radical':'easy','polynomial':'moderate','exponential':'hard','cosine':'hard','sine':'hard'}
SOURCES={'sum':'q-123128','quotient':'q-123431','radical':'q-123387','polynomial':'q-76569','exponential':'q-123434','cosine':'q-76577','sine':'q-76200'}
ANCHORS={'sum':{'a':[1,0,1],'b':[2,3,0]},'quotient':{'a':[-4,1,5],'b':[-2,3,3]},'radical':{'a':[3,-2,3],'b':[5,-1,7]},'polynomial':{'a':[1,2,0],'b':[2,1,3]},'exponential':{'a':[2,-2,4],'b':[4,-1,5]},'cosine':{'a':[-1,2,1],'b':[1,2,5]},'sine':{'a':[1,0,1],'b':[2,2,3]}}
FUNCTIONS={'sum':X+Y+Z,'quotient':(Y+Z)/X,'radical':S.sqrt(2*X+Y-Z),'polynomial':X*Y**2,'exponential':X*S.exp(Y*Z),'cosine':S.cos(S.pi*(X+Z)/4),'sine':S.sin(S.pi*Y/4)}
FUNCTION_TEX={'sum':'x + y + z','quotient':r'\frac{y+z}{x}','radical':r'\sqrt{2x+y-z}','polynomial':r'x{y}^{2}','exponential':r'x{e}^{yz}','cosine':r'\operatorname{cos}⁡(\frac{\pi }{4}(x+z))','sine':r'\sin (\frac{πy}{4})'}

def tex(e):
 return S.latex(e).replace(r'\log',r'\ln')
def grp(s):return '('+s+')'
def point(p,spaced=False):return '('+(', ' if spaced else ',').join(map(str,p))+')'
def align(rows):return '$$\n'+r'\begin{aligned}'+r' \\  '.join(rows)+r'\end{aligned}'+'\n$$'
def eqrows(label,items):return [label+' & ='+items[0]]+[' & ='+v for v in items[1:]]
def vector(v):
 # Three actual components retained even when a coordinate is constant.
 return '+'.join(grp(tex(e))+r'\,'+c for e,c in zip(v,('i','j','k')))
def dint(c,f):return tex(c)+r'{\int }_{0}^{1}'+grp(tex(f))+r'\,\text{d}t'
def sscalar(e):return tex(S.simplify(e))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+v))

def parameters_ok(f,p):
 if set(p)!={'a','b'}:raise ValueError('parameters must be a and b integer triples')
 if any(not isinstance(v,list) or len(v)!=3 for v in p.values()):raise ValueError('three coordinates required')
 if any(type(v)!=int or abs(v)>24 for xyz in p.values() for v in xyz):raise ValueError('bounded integer coordinates required')
 a,b=p['a'],p['b'];d=[j-i for i,j in zip(a,b)]
 if not any(d):raise ValueError('zero segment')
 if any(abs(v)>8 for v in d):raise ValueError('coordinate increments exceed fixed workload')
 if f=='sum' and (not all(d) or abs(sum(a))>12 or abs(sum(d))>9 or not sum(d)):raise ValueError('linear pullback requires three increments and nonzero slope')
 if f=='quotient':
  if a[0]*b[0]<=0:raise ValueError('denominator pole on the whole segment')
  if not all(d) or d[1]+d[2]!=0 or not a[1]+a[2] or not d[0] or abs(a[0])>8 or abs(b[0])>8:raise ValueError('constant numerator / linear pole-free denominator workload')
 if f=='radical':
  q0=2*a[0]+a[1]-a[2];q1=2*b[0]+b[1]-b[2]
  if min(q0,q1)<0:raise ValueError('radicand negative on segment')
  if not all(d) or not 1<=q0<=8 or not 1<=q1<=8 or q0==q1:raise ValueError('positive nonconstant linear radical workload')
 if f=='polynomial':
  if not all(d) or not d[0] or not d[1] or not all(1<=v<=4 for v in (a[0],b[0],a[1],b[1])) or any(abs(v)>3 for v in d):raise ValueError('nondegenerate cubic product with bounded positive coordinate factors')
 if f=='exponential':
  if not all(d) or d[0]!=2*d[1]*d[2] or a[0]!=d[1]*a[2]+d[2]*a[1]:raise ValueError('x(t) must equal derivative of y(t)z(t)')
  u0=a[1]*a[2];u1=b[1]*b[2]
  if not(-24<=u0<u1<=-1 and 2<=u1-u0<=9 and 1<=a[0]<=6 and 1<=b[0]<=14 and 1<=abs(d[1])<=2 and 1<=abs(d[2])<=2):raise ValueError('bounded reciprocal-exponential source method')
 if f in ('cosine','sine'):
  h0=a[0]+a[2] if f=='cosine' else a[1];h1=b[0]+b[2] if f=='cosine' else b[1]
  if not 1<=abs(h1-h0)<=6 or abs(h0)>8 or abs(h1)>8 or not d[0] or not d[2] or max(map(abs,d))>4:raise ValueError('bounded familiar-angle trig substitution; genuine 3D speed')
  if f=='sine' and not d[1]:raise ValueError('nonconstant sine argument')
 return a,b,d

def data(f,p):
 a,b,d=parameters_ok(f,p);r=[S.Integer(i)+j*T for i,j in zip(a,d)];n=sum(v*v for v in d);speed=S.sqrt(n)
 pulled=FUNCTIONS[f].subs(dict(zip((X,Y,Z),r)),simultaneous=True)
 pulled=S.expand(pulled) if f=='polynomial' else S.Mul(r[0],S.exp(S.expand(r[1]*r[2])),evaluate=False) if f=='exponential' else S.simplify(pulled)
 if f=='exponential':prim=S.exp(S.expand(r[1]*r[2]))
 elif f in ('cosine','sine'):
  arg=S.expand(S.pi*(r[0]+r[2] if f=='cosine' else r[1])/4);alpha=S.diff(arg,T)
  prim=(S.sin(arg) if f=='cosine' else -S.cos(arg))/alpha
 else:prim=S.integrate(pulled,T)
 iv=S.simplify(prim.subs(T,1)-prim.subs(T,0));ans=S.simplify(speed*iv)
 return dict(a=a,b=b,d=d,r=r,n=n,s=speed,pulled=pulled,prim=prim,iv=iv,answer=ans)

def prompt(f,p,raw=False):
 a,b=p['a'],p['b'];F=FUNCTION_TEX[f]
 if f=='sum':return f'Which of the following is equivalent to the line integral of the function $f(x, y, z) = {F}$, traversed along the line segment from ${point(a,True)}$ to ${point(b,True)}$?'
 if f in ('quotient','radical'):return f'Which of the following is equivalent to the line integral of the function $f(x,y,z)={F},$ traversed along the line segment from ${point(a)}$ to ${point(b)}?$'
 if f=='sine':return f'Evaluate the integral $'+(r'\displaystyle \int_(C)' if raw else r'{\int }_{C}')+F+'ds$ along the line segment from $'+point(a,True)+'$ to $'+point(b,True)+'$.'
 return r'Evaluate the integral ${\int }_{C}'+F+r'\,\text{d}s$ along the line segment from $'+point(a)+'$ to $'+point(b)+'.$'

def solution(f,p,k,raw=False):
 a,b,d,r,s,n,h=k['a'],k['b'],k['d'],k['r'],k['s'],k['n'],k['pulled']
 A,B,D=vector(a),vector(b),vector(d);R=vector(r)
 formula=r'{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,'
 out='We will use the formula\n\n$$\n'+formula+'\n$$\n\n \n\nwhere $C$ is the line segment from $'+point(a)+'$ to $'+point(b)+'.$\n\n'
 out+='The position vectors of the endpoints of our line segment are $a='+A+'$ and $b='+B+'.$ So, the parametrization of the line segment is given by\n\n'
 out+=align(eqrows('r(t)',[r'a+t\,(b-a)',grp(A)+'+t['+grp(B)+'-'+grp(A)+']',grp(A)+'+t'+grp(D),R]))
 out+='\n\nwhere $0\\le t\\le 1.$ Thus, we have that $x='+tex(r[0])+',$ $y='+tex(r[1])+',$ and $z='+tex(r[2])+'$ along the segment.\n\n'
 out+=r'Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:'+'\n\n'
 deriv=r'\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k'
 actual='+'.join(r'\frac{\text{d}}{\text{d}t}'+grp(tex(e))+c for e,c in zip(r,('i','j','k')))
 formal=r'\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}}'
 squared=r'\sqrt{'+ '+'.join(grp(str(v))+'^{2}' for v in d)+'}'
 speeds=[formal,squared]
 # Preserve the source's additional unsimplified magnitude row for its two families.
 if f in ('quotient','cosine'):speeds.append(r'\sqrt{'+str(n)+'}')
 speeds.append(tex(s))
 out+=align(eqrows(r'{r}^{′}(t)',[deriv,actual,D])+eqrows(r'‖{r}^{′}(t)‖',speeds))
 out+='\n\nNow, since $f(x,y,z)='+FUNCTION_TEX[f]+'$, we obtain\n\n'
 xx,yy,zz=map(tex,r)
 if f=='sum':sub=grp(xx)+'+'+grp(yy)+'+'+grp(zz)
 elif f=='quotient':sub=r'\frac{'+grp(yy)+'+'+grp(zz)+'}{'+xx+'}'
 elif f=='radical':sub=r'\sqrt{2'+grp(xx)+'+'+grp(yy)+'-'+grp(zz)+'}'
 elif f=='polynomial':sub=grp(xx)+grp(yy)+'^{2}'
 elif f=='exponential':sub=grp(xx)+r'{e}^{'+grp(yy)+grp(zz)+'}'
 elif f=='cosine':sub=r'\operatorname{cos}⁡(\frac{\pi }{4}('+grp(xx)+'+'+grp(zz)+'))'
 else:sub=r'\sin(\frac{\pi}{4}'+grp(yy)+')'
 pull=[sub]
 if f=='quotient':pull.append(r'\frac{'+str(a[1]+a[2])+'}{'+xx+'}')
 if f=='polynomial' and not raw:
  # Added explanatory stages preserve the actual squared y factor and each product.
  yp=S.Poly(S.expand(r[1]**2),T);parts=[c*T**e[0] for e,c in yp.terms()]
  pull += [grp(xx)+grp('+'.join(grp(tex(v)) for v in parts)), '+'.join(grp(xx)+grp(tex(v)) for v in parts)]
 pull.append(tex(h));out+=align(eqrows('f(r(t))',pull))
 out+='\n\nTherefore, we can write the integral as\n\n'
 lhs=r'{\int }_{C}'+('f(x,y,z)' if f in ('sum','quotient','radical') else FUNCTIONS_TEX_NORMAL(f))+r'\,\text{d}s'
 last_setup=dint(s*S.Rational(a[1]+a[2],d[0]),1/(T+S.Rational(a[0],d[0]))) if f=='quotient' else dint(s,h)
 integral=eqrows(lhs,[r'{\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t',r'{\int }_{0}^{1}'+grp(tex(h))+r'\cdot '+tex(s)+r'\cdot \text{d}t',last_setup])
 if f=='polynomial':
  pp=S.Poly(k['prim'],T);parts=[c*T**e[0] for e,c in pp.terms()]
  primitive='+'.join(grp(tex(v)) for v in parts)
  upper='+'.join(grp(tex(v.subs(T,1))) for v in parts)
  lower='+'.join(grp(tex(v.subs(T,0))) for v in parts)
  integral += [' & ='+tex(s)+r'\left['+primitive+r'\right]_{0}^{1}', ' & ='+tex(s)+grp(upper)+'-'+tex(s)+grp(lower), ' & ='+tex(k['answer'])+'.']
 out+=align(integral)
 if f in ('exponential','cosine','sine'):
  arg=S.expand(r[1]*r[2]) if f=='exponential' else S.expand(S.pi*(r[0]+r[2] if f=='cosine' else r[1])/4)
  ap=S.diff(arg,T);lo=arg.subs(T,0);hi=arg.subs(T,1)
  out+='\n\nWe can solve this using the substitution $u='+tex(arg)+'$, $'+r'\text{d}u='+grp(tex(ap))+r'\,\text{d}t$ as follows: '+'\n\n'
  if f=='exponential':
   co=s;fun=r'{e}^{u}';pr=r'{e}^{u}';v0=S.exp(lo);v1=S.exp(hi)
   rows=[tex(co)+r'\,{\int }_{'+tex(lo)+'}^{'+tex(hi)+'}'+fun+r'\,\text{d}u',tex(co)+r'\,'+pr+r'\,{|}_{'+tex(lo)+'}^{'+tex(hi)+'}',tex(co)+grp(r'{e}^{'+tex(hi)+'}-'+r'{e}^{'+tex(lo)+'}'),tex(co)+grp(r'\frac{1}{{e}^{'+tex(-hi)+'}}-'+r'\frac{1}{{e}^{'+tex(-lo)+'}}'),tex(co)+r'\frac{{e}^{'+tex(hi-lo)+'}-1}{{e}^{'+tex(-lo)+'}}']
  else:
   co=S.simplify(s/ap);fun=r'\operatorname{cos}⁡u' if f=='cosine' else r'\sin u';pr=r'\operatorname{sin}⁡u' if f=='cosine' else r'-\cos u'
   v0=S.sin(lo) if f=='cosine' else -S.cos(lo);v1=S.sin(hi) if f=='cosine' else -S.cos(hi)
   ep=(r'\operatorname{sin}⁡('+tex(hi)+')-'+r'\operatorname{sin}⁡('+tex(lo)+')') if f=='cosine' else (r'-\cos('+tex(hi)+')-(-'+r'\cos('+tex(lo)+'))')
   rows=[tex(co)+r'{\int }_{'+tex(lo)+'}^{'+tex(hi)+'}'+fun+r'\,\text{d}u',tex(co)+grp(pr)+r'\,{|}_{'+tex(lo)+'}^{'+tex(hi)+'}',tex(co)+grp(ep),tex(co)+grp(grp(tex(v1))+'-'+grp(tex(v0))),tex(k['answer'])]
  out+=align(eqrows(dint(s,h),rows))
 return out

def FUNCTIONS_TEX_NORMAL(f):return FUNCTION_TEX[f]

# Each historical bank is a complete explicitly selected expression profile.
# Scalar/odd-integrand intent is underdetermined. These public recipes preserve
# the recorded structural offsets, not claims about the source author's errors.
def bank(f,k,raw):
 a,b,d,r,s,n,h,I,J=k['a'],k['b'],k['d'],k['r'],k['s'],k['n'],k['pulled'],k['iv'],k['answer']
 if raw:
  if f=='sum':
   A=sum(a);B=sum(d);vals=[(s,A+B*T),(S.sqrt(d[0]**2+(d[1]+d[2])**2),a[0]-(d[1]+d[2])*T),(S.sqrt(d[0]**2+(d[1]+d[2])**2),a[0]-d[0]*T),(S.sqrt(n+2*abs(d[0])),a[0]+(B-d[0])*T),(s,a[0]+B*T)];ci=0
  elif f=='quotient':
   c=S.Rational(a[0],d[0]);q=S.Rational(a[1]+a[2],d[0]);vals=[(s*q,1/(T*T-c)),(s,1/(d[0]*T-1)),(s,T/(T+c)),(s*q,1/(T+c)),(s*q,(d[0]*T+a[1])/(T+c+1))];ci=3
  elif f=='radical':
   A=2*a[0]+a[1]-a[2];B=2*d[0]+d[1]-d[2];vals=[(s,S.sqrt(2*B*T+A)),(s,S.sqrt(B*B*T*T+2*B*T+A)),(S.sqrt(n-1),T*S.sqrt(B*T-A)),(S.sqrt(n-1),S.sqrt((B+4)*T-3*A)),(s,S.sqrt(B*T+A))];ci=4
  elif f=='polynomial':vals=[4*J,J,S.sqrt(n+2)/4,s/4,I];ci=1
  elif f=='exponential':
   lo=a[1]*a[2];hi=b[1]*b[2];delta=hi-lo;vals=[s/S.sqrt(2)*(S.exp(delta)+2)/S.exp(-lo),s*(S.exp(delta-1)-1)/S.exp(delta),J,J/s,(S.exp(delta)+1)/S.exp(-hi)];ci=2
  elif f=='cosine':
   B=d[0]+d[2];vals=[J,J/2,-2*S.sqrt(n-8)/((B-1)*S.pi),s/(S.pi/2),-J/4];ci=0
  else:
   alpha=S.pi*d[1]/4;vals=[4*alpha,J,alpha,S.Rational(1,d[1]),J/4];ci=1
 else:
  ci=0
  if f in ('sum','quotient','radical'):
   frozen=FUNCTIONS[f].subs({X:r[0],Y:S.Integer(a[1]),Z:r[2]},simultaneous=True)
   vals=[(s,h),(S.Integer(1),h),(S.Integer(n),h),(S.sqrt(d[0]**2+d[1]**2),h),(s,frozen)]
  elif f=='polynomial':vals=[J,I,n*I,s*S.integrate(r[0]*r[1],(T,0,1)),s*S.integrate(a[0]*r[1]**2,(T,0,1))]
  elif f=='exponential':
   lo=a[1]*a[2];hi=b[1]*b[2];vals=[J,I,s*(S.exp(hi)+S.exp(lo)),s*S.exp(hi),J/d[0]]
  else:
   arg=S.pi*(r[0]+r[2] if f=='cosine' else r[1])/4;alpha=S.diff(arg,T)
   vals=[J,I,-J,S.simplify(J*alpha),J/2]
 complete=[x[0]*S.Integral(x[1],(T,0,1)) if isinstance(x,tuple) else x for x in vals]
 return vals,complete,ci

def bank_value(v):return dint(*v) if isinstance(v,tuple) else tex(S.simplify(v))
def evaluated(e):
 try:return S.simplify(e.doit())
 except Exception:return e

def sample(f,rng):
 if f=='exponential':
  for _ in range(10000):
   y=rng.randint(-4,-2);z=rng.randint(2,7);dy=rng.choice([1,2]);dz=rng.choice([1,2]);dx=2*dy*dz;x=dy*z+dz*y
   p={'a':[x,y,z],'b':[x+dx,y+dy,z+dz]}
   try:parameters_ok(f,p);return p
   except ValueError:pass
 else:
  for _ in range(10000):
   if f=='polynomial':a=[rng.randint(1,4),rng.randint(1,4),rng.randint(-3,3)];b=[rng.randint(1,4),rng.randint(1,4),a[2]+rng.choice([-3,-2,-1,1,2,3])]
   elif f=='quotient':
    x=rng.choice([-6,-5,-4,2,3,4]);dx=rng.choice([-2,-1,1,2]);dy=rng.choice([-2,-1,1,2]);a=[x,rng.randint(-3,4),rng.randint(1,6)];b=[x+dx,a[1]+dy,a[2]-dy]
   else:a=[rng.randint(-4,4) for _ in range(3)];d=[rng.randint(-3,3) for _ in range(3)];b=[i+j for i,j in zip(a,d)]
   p={'a':a,'b':b}
   try:parameters_ok(f,p);return p
   except ValueError:pass
 raise ValueError('no eligible instance')

def fingerprint(f,k):
 # Pullback and full speed capture assessed mathematics; discard translations,
 # orientation and coordinate changes that do not alter either component.
 h=k['pulled'];forms=[]
 for v in (h,h.subs(T,1-T)):
  forms.append(S.srepr(S.simplify(S.expand_trig(v))))
 return digest([LEVELS[f],f,tex(k['s']),min(forms)])

# Easy: setup only. Moderate: one nondegenerate cubic product integration.
# Hard: one familiar-angle substitution or exact derivative exponential substitution.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio shape supported')
 rng=random.Random(seed)
 if profile and profile.startswith('source-'):
  sf=next((f for f,q in SOURCES.items() if profile=='source-'+q),None)
  if sf is None:raise ValueError('unknown profile')
  if template and template!=sf:raise ValueError('profile/template mismatch')
  template=sf
 f=template or rng.choice([f for f,l in LEVELS.items() if l==level])
 if f not in LEVELS or LEVELS[f]!=level:raise ValueError('template level mismatch (unrated sources explicitly assigned)')
 raw=profile is not None and profile.startswith('source-')
 if profile not in (None,'method','source-'+SOURCES[f]):raise ValueError('unknown complete bank')
 profile=profile or 'method'
 for _ in range(10000):
  p=parameters if parameters is not None else sample(f,rng)
  k=data(f,p);vals,complete,ci=bank(f,k,raw)
  if not raw and any(isinstance(v,tuple) and any(v[1].subs(T,at).is_real is False for at in (0,1)) for v in vals):
   if parameters is not None:raise ValueError('whole method bank rejected: nonreal option path')
   continue
  ev=[evaluated(v) for v in complete]
  valid=all(v.is_real is not False and not v.has(S.oo,-S.oo,S.zoo,S.nan,S.Integral) for v in ev) and all(S.simplify(ev[i]-ev[j])!=0 for i in range(5) for j in range(i))
  distinct=len(set(map(bank_value,vals)))==5 and all(S.simplify(ev[i]-ev[j])!=0 for i in range(5) for j in range(i))
  if (raw and distinct) or valid:break
  if parameters is not None:raise ValueError('whole method bank rejected: invalid/equivalent options')
 else:raise ValueError('no eligible complete bank')
 if not raw and S.simplify(ev[ci]-k['answer'])!=0:raise AssertionError('wrong key')
 q={':question/problem':prompt(f,p,raw)}
 if not(raw and f in ('sum','sine')):q[':question/worked-solution']=solution(f,p,k,raw)
 if not(raw and f in ('sum','sine')):q[':question/difficulty']=':question.difficulty/'+level
 values=[bank_value(v) for v in vals]
 # Identity ignores input aliases, seed, and shuffle, includes actual level/content.
 key=digest([VERSION,level,q,sorted(values)]);qid=uid(key);fid=uid(qid+':selection')
 choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if not(raw and f in ('sum','sine')):field[':answer-field/correct']=[':answer/id',choices[ci][':answer/id']]
 rng.shuffle(choices);q[':question/id']=qid;q[':question/answer-fields']=[field]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':f,'profile':profile,'seed':seed,'parameters':p,'source_id':SOURCES[f],'source':{'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_claim':'authored assignment of unrated source' if f in ('sum','sine') else 'observed','mathematical_fingerprint':fingerprint(f,k),'content_hash':key,'domain':'nonzero straight segment, all three coordinate derivatives; real pullback and pole-free learner bank','bank_interpretation':'historical structural profile; intent unresolved' if raw else 'complete method-derived operations','dependencies':{'python':sys.version.split()[0],'sympy':S.__version__}}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
 q=rec['question'];fld=q[':question/answer-fields'][0];s=q[':question/problem']+'\n\n'
 for a in fld[':answer-field/choices']:s+='- $'+a[':answer/value']+'$\n'
 return s+'\n'+q.get(':question/worked-solution','[Source worked solution absent.]')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,rows)))
