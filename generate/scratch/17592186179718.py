#!/usr/bin/env python3
"""Function-of-y scalar line integral evaluation; fixed-basis 1356 scratch draft.
Raw source profiles parameterize endpoint/primitive components of complete banks.
Opaque profiles are evidence-only; method banks serve all supported families.
No database operations. See adjacent extraction, review and validation evidence.
"""
import argparse,hashlib,json,random,re,subprocess,sys,uuid,tempfile,os
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix(''); VERSION='function-y-evaluation-v1'
CAP=json.loads((HERE/'source.json').read_text()); KP=CAP['record']; t=s.Symbol('t',positive=True); x,y=s.symbols('x y',positive=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CASES={
'q-122271':('implicit_parabola','hard',dict(a='0',b='3',c='24',k='8')),
'q-122579':('sqrt','hard',dict(a='0',b='2',c='4',k='1')),
'q-122574':('parabola','moderate',dict(a='1',b='sqrt(6)',c='12',k='1')),
'q-122593':('reciprocal','moderate',dict(a='1',b='2',c='1',k='2')),
'q-149727':('line_log','moderate',dict(a='2',b='3',c='1',k='4')),
'q-149745':('exponential','hard',dict(a='0',b='log(2)',c='6',k='2'))}
LEVELS={'easy':['line_power'],'moderate':['parabola','reciprocal','line_log','log_curve'],'hard':['implicit_parabola','exponential','sqrt']}
def tex(v): return s.latex(s.sympify(v),ln_notation=True).replace('\\log','\\ln')
def rawtex(v):
 v=s.sympify(v)
 if v.func==s.log:return r'\operatorname{ln}⁡'+tex(v.args[0])
 return tex(v).replace(' ','')
def difftex(up,lo,factor=False):
 up,lo=s.simplify(up),s.simplify(lo)
 h=s.gcd(up.as_coeff_Mul()[0],lo.as_coeff_Mul()[0]) if factor else 1
 return (rawtex(h)+'('+rawtex(up/h)+'-'+rawtex(lo/h)+')') if h!=1 else rawtex(up)+'-'+rawtex(lo)
def frac(n,d): return r'\frac{'+str(n)+'}{'+str(d)+'}'
def ident(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+json.dumps(v,sort_keys=True)))
def same(a,b): return s.simplify(a-b)==0
def math_data(f,p):
 a,b,c,k=[s.sympify(p[z]) for z in ('a','b','c','k')]
 if f=='line_power': g=2*t+k; F=c*y; u=t; C=c*s.sqrt(5); H=C*t*t/2
 elif f=='parabola':
  g=t*t/k; F=c*x/y; u=4*t*t+1; C=c; H=c*u**s.Rational(3,2)/12
 elif f=='implicit_parabola':
  g=t*t/k; F=c*x/y; u=t*t+(k/2)**2; C=c/k*2/k; H=C*u**s.Rational(3,2)/3
 elif f=='reciprocal': g=k/t; F=c*x*y**6; u=t**4+k*k; C=c*k; H=C*u**s.Rational(3,2)/6
 elif f=='line_log': g=2*t-k; F=c/(y-x); u=k-t; C=c*s.sqrt(5); H=-C*s.log(u)
 elif f=='exponential': g=s.exp(t/k); F=c*x**6*s.exp(-4*y/k); u=s.exp(2*t/k)+k*k; C=c/k; H=c*u**s.Rational(3,2)/3
 elif f=='sqrt': g=s.sqrt(k*t); F=c*x*y; u=4*t+k; C=c*s.sqrt(k)/2; H=C/16*(s.Rational(2,5)*u**s.Rational(5,2)-k*s.Rational(2,3)*u**s.Rational(3,2))
 elif f=='log_curve': g=s.log(t); F=c*y**3*s.exp(-x); u=t*t+1; C=c; H=c*u**s.Rational(3,2)/3
 else: raise ValueError('unknown template')
 gp=s.diff(g,t); speed=s.sqrt(gp*gp+1); ft=s.simplify(F.subs({x:g,y:t})); integrand=s.simplify(ft*speed)
 result=s.expand_log(s.simplify(H.subs(t,b)-H.subs(t,a)),force=True); A=s.simplify(u.subs(t,a)); B=s.simplify(u.subs(t,b))
 if f=='line_log':result=C*s.log(s.simplify(A/B))
 return locals()
def guard(f,p,level,raw=False):
 d=math_data(f,p); a,b,c,k=[d[z] for z in ('a','b','c','k')]
 if not all(v.is_real for v in (a,b,c,k)) or not (b>a and c>0 and k>0): raise ValueError('positive coefficients and increasing finite bounds required')
 if f in ('reciprocal','log_curve') and a<=0: raise ValueError('positive y required')
 if f=='line_log' and b>=k: raise ValueError('denominator must stay positive')
 if f=='sqrt' and a<0: raise ValueError('square-root domain')
 if f in ('parabola','implicit_parabola') and a<0: raise ValueError('nonnegative y; continuous extension at zero')
 if raw:
  qid=next(q for q,(ff,ll,pp) in CASES.items() if ff==f); base=CASES[qid][2]
  if not same(k,s.sympify(base['k'])) or not same(c,s.sympify(base['c'])): raise ValueError('opaque replay varies endpoints only; fixed curve/coefficient')
 else:
  if f not in LEVELS[level]: raise ValueError('difficulty/template mismatch')
  if not (c.is_Integer and k.is_Integer and c<=12 and k<=8 and a>=0 and b<=8): raise ValueError('authored arithmetic bounds')
  if f in ('implicit_parabola','sqrt') and a<=0:raise ValueError('normal evaluation requires regular positive-y endpoints')
  if f=='implicit_parabola' and not (k in (4,6,8) and s.sqrt(d['A']).is_Integer and s.sqrt(d['B']).is_Integer and k/2<s.sqrt(d['A'])<s.sqrt(d['B'])<=8): raise ValueError('hard requires implicit nonunit parabola coefficient')
  if f=='parabola' and not (k==1 and a==1 and b*b in (2,6,12,20)): raise ValueError('moderate direct parabola workload')
  if f=='exponential' and not (k==2 and a==0 and s.exp(b) in (2,3,4,5,6)): raise ValueError('hard exponential half-argument workload')
  if f=='sqrt' and not (k in (1,2,3,4) and a==1 and b in (2,3,4,5)):raise ValueError('hard two-component root substitution bounds')
  if f=='reciprocal' and not (k in (1,2,3) and a==1 and b in (2,3)):raise ValueError('moderate reciprocal bounds')
  if f=='line_log' and not (k in (4,5,6,7,8) and a==1 and b.is_Integer and 2<=b<=k-2):raise ValueError('moderate reciprocal-linear logarithm bounds')
  if f=='log_curve' and not (k==1 and a==1 and b*b in (3,8,15,24)):raise ValueError('canonical log-curve familiar radical bounds')
  if f=='line_power' and not (a>=1 and b<=6 and a.is_Integer and b.is_Integer and k in (1,2,3)): raise ValueError('easy integer straight-line polynomial workload')
 return d

def integral(v,lo,hi,var='t'): return r'{\int }_{'+tex(lo)+'}^{'+tex(hi)+'}'+v+r'\,\text{d}'+var

def normal_solution(d):
 f=d['f']; g,gp,F,ft,speed,u,H,a,b,A,B,result=[d[z] for z in ('g','gp','F','ft','speed','u','H','a','b','A','B','result')]
 rows=lambda rr:r'\begin{aligned}'+r' \\  & ='.join(rr)+r'\end{aligned}'
 block=lambda z:'$$\n'+z+'\n$$'
 out='Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have\n\n'+block('x=x(t)='+tex(g)+'.')
 if f=='implicit_parabola':out='Notice that the given curve can be expressed in the form $x=x(y),$ as follows:\n\n'+block(r'y^2='+tex(d['k'])+'x'+r'\,⟹\,x='+tex(g.subs(t,y))+'.')+'\n\nTherefore, by setting $y=t,$ we have\n\n'+block('x=x(t)='+tex(g)+'.')
 out+='\n\nThis gives the following parametrization of the curve:\n\n'+block('r(t)=⟨'+tex(g)+r',\,t⟩,\,'+tex(a)+r'\le t\le '+tex(b))
 out+='\n\nNote that the domain $'+tex(a)+r'\le t\le '+tex(b)+'$ is defined by the $y$-coordinates of the end-points on the path.\n\nComputing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: \n\n'
 formal=r'{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j'
 dr=[formal,r'\frac{\text{d}}{\text{d}t}('+tex(g)+r')i+\frac{\text{d}}{\text{d}t}(t)j',tex(gp)+r'\,i+j']
 drblock=rows(dr)[:-len(r'\end{aligned}')]+r' \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}'+r' \\  & =\sqrt{('+tex(gp)+r')^2+1^2}'+r' \\  & =\sqrt{'+tex(s.expand(gp*gp))+r'+1}'+r' \\  & ='+tex(speed)+r'\end{aligned}'
 out+=block(drblock)+'\n\n \n\nNow, if  $f(x,y)='+tex(F)+',$ then we obtain \n\n'
 # Actual coordinate substitution is retained unevaluated as an independent component stage.
 substituted=tex(F).replace('x',r'\left('+tex(g)+r'\right)').replace('y','t')
 out+=block(rows(['f(r(t)) & ='+substituted,tex(ft)+'.']))
 out+='\n\nTherefore, we can write the integral as \n\n'+block(rows([integral(tex(F),a,b,'s').replace('_{'+tex(a)+'}^{'+tex(b)+'}','_{C}')+' & ='+integral(r'f(r(t))\,‖{r}^{′}(t)‖',a,b),integral(r'\left('+tex(ft)+r'\right)\cdot\left('+tex(speed)+r'\right)',a,b),integral(tex(d['integrand']),a,b)+'.']))
 if f=='line_power':
  rr=[integral(tex(d['integrand']),a,b)+' & ='+r'\left['+tex(H)+r'\right]_{'+tex(a)+'}^{'+tex(b)+'}',tex(d['C'])+r'\left(\frac{'+tex(b)+r'^2}{2}-\frac{'+tex(a)+r'^2}{2}\right)',tex(d['C'])+r'\left('+tex(b*b/2)+'-'+tex(a*a/2)+r'\right)',tex(result)]
  out+='\n\nFinally, we evaluate the integral as follows:\n\n'+block(rows(rr));return out
 du=s.diff(u,t); transformed=s.simplify(d['integrand']/du)
 if f=='sqrt': transformed=d['C']/16*(s.Symbol('u')-d['k'])*s.sqrt(s.Symbol('u'))
 elif f=='line_log':transformed=-d['C']/s.Symbol('u')
 else: transformed=s.simplify(d['integrand']/du).subs(u,s.Symbol('u'))
 primitive=H.subs(t,s.solve(s.Eq(s.Symbol('u'),u),t)[-1]) if f=='line_log' else None
 if f not in ('sqrt','line_log'): primitive=s.simplify(H/u**s.Rational(3,2))*s.Symbol('u')**s.Rational(3,2)
 if f=='sqrt': primitive=d['C']/16*(s.Rational(2,5)*s.Symbol('u')**s.Rational(5,2)-d['k']*s.Rational(2,3)*s.Symbol('u')**s.Rational(3,2))
 if f=='line_log':primitive=-d['C']*s.log(s.Symbol('u'))
 # Explicit primitive operations and individually evaluated endpoint components.
 parts=sorted(s.Add.make_args(s.expand(primitive)),key=lambda q:(q.could_extract_minus_sign(),str(q))); endpoint_sub=[]; endpoint_eval=[]
 for end in (B,A):
  endpoint_sub.append('+'.join(r'\left('+tex(q).replace('u',r'\left('+tex(end)+r'\right)')+r'\right)' for q in parts))
  endpoint_eval.append('+'.join(r'\left('+tex(s.simplify(q.subs(s.Symbol('u'),end)))+r'\right)' for q in parts))
 if f=='sqrt':first=tex(d['C'])+integral(r'\frac{u-'+tex(d['k'])+r'}{4}\cdot\sqrt{u}\cdot\frac{1}{4}',A,B,'u')
 elif f=='line_log':first=tex(d['C'])+integral(r'\frac{1}{u}\cdot(-1)',A,B,'u')
 else:
  factor={'parabola':s.Rational(1,8),'implicit_parabola':s.Rational(1,2),'reciprocal':s.Rational(1,4),'exponential':d['k']/2,'log_curve':s.Rational(1,2)}[f]
  first=tex(d['C'])+integral(r'\sqrt{u}\cdot\left('+tex(factor)+r'\right)',A,B,'u')
 if f=='sqrt':op=tex(d['C']/16)+r'\cdot\left(\frac{2}{5}u^{5/2}-('+tex(d['k'])+r')\cdot\frac{2}{3}u^{3/2}\right)'
 elif f=='line_log':op=r'-('+tex(d['C'])+r')\cdot\ln{u}'
 else:op=tex(s.simplify(primitive/s.Symbol('u')**s.Rational(3,2))*s.Rational(3,2))+r'\cdot\frac{2}{3}u^{3/2}'
 rr=[integral(tex(d['integrand']),a,b)+' & ='+first,integral(tex(s.expand(transformed)),A,B,'u'),r'\left['+op+r'\right]_{'+tex(A)+'}^{'+tex(B)+'}',r'\left['+tex(primitive)+r'\right]_{'+tex(A)+'}^{'+tex(B)+'}',r'\left('+endpoint_sub[0]+r'\right)-\left('+endpoint_sub[1]+r'\right)',r'\left('+endpoint_eval[0]+r'\right)-\left('+endpoint_eval[1]+r'\right)',tex(result)]
 out+='\n\nFinally, we solve this using the substitution $u='+tex(u)+',$ $'+r'\text{d}u='+tex(du)+r'\,\text{d}t$ as follows:'+'\n\n'+block(rows(rr))
 return out

def replace_components(text,mapping):
 """Slot complete mathematical components simultaneously, longest masks first."""
 keys=sorted(mapping,key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda m:mapping[m.group()],text) if keys else text

def raw_strings(qid,d):
 """Exact source formatting masks; changing endpoints changes all endpoint stages.
 Curve/integrand coefficients remain fixed for opaque evidence profiles. This
 restriction avoids pretending a numerical bank reveals source error operations.
 """
 q=SOURCES[qid]; base=math_data(d['f'],CASES[qid][2]); a,b,A,B=[d[z] for z in ('a','b','A','B')]; aa,bb,AA,BB=[base[z] for z in ('a','b','A','B')]
 p=q[':question/problem']; sol=q.get(':question/worked-solution')
 # Complete coordinate tuples and bounds are independent slots.
 g=d['g']; coords=[(g.subs(t,z),z) for z in (a,b)]
 originals=re.findall(r'\$\([^$]*?\)[.,]?\$',p)
 if len(originals)!=2:raise AssertionError('coordinate masks')
 for old,(xx,yy) in zip(originals,coords):
  punctuation=',' if old.endswith(',$') else '.' if old.endswith('.$') else ''
  sep=', ' if ', ' in old else ','
  ey=tex(yy)
  if qid=='q-149745' and yy.func==s.log:ey=r'\operatorname{ln}⁡'+tex(yy.args[0])
  p=p.replace(old,'$('+tex(xx).replace(' ','')+sep+ey.replace(' ','')+')'+punctuation+'$')
 if sol is None:return p,None
 lower=tex(aa);upper=tex(bb)
 # Preserve observed ln spelling and positive-radical endpoint style.
 if qid=='q-149745':upper=r'\operatorname{ln}⁡2'
 mapping={lower+r'\le t\le '+upper:rawtex(a)+r'\le t\le '+rawtex(b),
          '_{'+lower+'}^{'+upper+'}':'_{'+rawtex(a)+'}^{'+rawtex(b)+'}',
          '_{'+tex(AA)+'}^{'+tex(BB)+'}':'_{'+tex(A)+'}^{'+tex(B)+'}'}
 sol=replace_components(sol,mapping)
 # Terminal block masks are complete primitive components, never free digits.
 spans=list(re.finditer(r'\$\$.*?\$\$',sol,re.S)); final=spans[-1]; z=final.group()
 old_u,old_v=tex(BB),tex(AA); U,V=tex(B),tex(A)
 masks={'{'+old_u+'}^{3/2}':'{'+U+'}^{3/2}','{'+old_v+'}^{3/2}':'{'+V+'}^{3/2}',r'\sqrt{{'+old_u+'}^{3}}':r'\sqrt{{'+U+'}^{3}}',r'\sqrt{{'+old_v+'}^{3}}':r'\sqrt{{'+V+'}^{3}}'}
 if qid=='q-122271':masks.update({'(125-64)':'('+tex(B**s.Rational(3,2))+'-'+tex(A**s.Rational(3,2))+')',r'\frac{61}{4}':tex(d['result'])})
 if qid=='q-122574':masks.update({r'125-5\sqrt{5}':tex(B**s.Rational(3,2))+'-'+tex(A**s.Rational(3,2)),r'5(25-\sqrt{5})':difftex(B**s.Rational(3,2),A**s.Rational(3,2),True)})
 if qid=='q-122593':masks.update({r'\frac{40\sqrt{5}-5\sqrt{5}}{3}':frac(tex(B**s.Rational(3,2))+'-'+tex(A**s.Rational(3,2)),3),r'\frac{35\sqrt{5}}{3}':tex(d['result'])})
 if qid=='q-149745':masks.update({r'2(6\sqrt{6}-5\sqrt{5})':'2('+tex(B**s.Rational(3,2))+'-'+tex(A**s.Rational(3,2))+')',r'12\sqrt{6}-10\sqrt{5}':difftex(2*B**s.Rational(3,2),2*A**s.Rational(3,2))})
 if qid=='q-149727':
  # Original reverses u bounds to put the minus sign into the limits.
  masks.update({r'_{2}^{1}':'_{'+tex(A)+'}^{'+tex(B)+'}',r'_{1}^{2}':'_{'+tex(B)+'}^{'+tex(A)+'}',r'[\operatorname{ln}⁡u]_{1}^{2}':r'[\operatorname{ln}⁡u]_{'+tex(B)+'}^{'+tex(A)+'}',r'[\operatorname{ln}⁡2-\operatorname{ln}⁡1]':r'[\operatorname{ln}⁡'+tex(A)+r'-\operatorname{ln}⁡'+tex(B)+']',r'[\operatorname{ln}⁡2-0]':'['+rawtex(s.log(A))+'-'+rawtex(s.log(B))+']',r'\sqrt{5}\operatorname{ln}⁡2':r'\sqrt{5}\operatorname{ln}⁡'+rawtex(s.simplify(A/B))})
 masks={kk:vv.replace(' ','') for kk,vv in masks.items()}
 z=replace_components(z,masks);sol=sol[:final.start()]+z+sol[final.end():]
 return p,sol

def opaque_bank(qid,d):
 U,V,a,b,c,k=[d[z] for z in ('B','A','a','b','c','k')];r=s.sqrt
 if qid=='q-122271':vals=[(U**s.Rational(3,2)-V**s.Rational(3,2)+h)/4 for h in (-8,-14,6,-10,0)]
 elif qid=='q-122574':vals=[U-r(V),b*b-r(V),(V+1)**2-r(V+1),(V+1)*((V+1)**2-r(V+1)),d['result']]
 elif qid=='q-122593':vals=[(U+1)*r(k+1)/V,(U-8)*r(V)/(V+2),(U+3*V)/(U-8),(V+k)**2/(3*V),d['result']]
 elif qid=='q-149727':vals=[r(2)*s.log(5),(a+b-1)*r(2),d['result'],2*r(5),2*s.log(2)]
 elif qid=='q-149745':vals=[V*r(U)-U*r(V),r(U)-r(V),d['result'],U*r(U/2)-2*r(V),2*r(U)-V*r(V)]
 else:
  # Proportional scalar-pattern replay of genuinely opaque historical numerals.
  # This evidence extrapolation is NOT an inferred misconception bank.
  scale=d['result']/s.Rational(149,15)
  vals=[s.Rational(144,5)*scale,s.Rational(121,15)*scale,s.Rational(125,3)*scale,s.Rational(213,5)*scale,s.Rational(149,15)*scale]
 vals=[s.simplify(v) for v in vals]
 if qid=='q-122574':strings=[tex(U)+'-'+r'\sqrt{'+tex(V)+'}',tex(b*b)+'-'+r'\sqrt{'+tex(V)+'}',tex((V+1)**2)+'-'+r'\sqrt{'+tex(V+1)+'}',tex(V+1)+'('+tex((V+1)**2)+'-'+r'\sqrt{'+tex(V+1)+'})',difftex(U**s.Rational(3,2),V**s.Rational(3,2),True)]
 elif qid=='q-149727':strings=[r'\sqrt{2}\operatorname{ln}⁡5',tex(a+b-1)+r'\sqrt{2}',tex(s.sqrt(5))+r'\operatorname{ln}⁡'+tex(Adiv:=s.simplify(d['A']/d['B'])),r'2\sqrt{5}',r'2\operatorname{ln}⁡2']
 elif qid=='q-149745':strings=[difftex(V*r(U),U*r(V)),difftex(r(U),r(V)),difftex(2*U*r(U),2*V*r(V)),difftex(U*r(U/2),2*r(V)),difftex(2*r(U),V*r(V))]
 else:strings=[tex(v).replace(' ','') for v in vals]
 return vals,strings

def method_bank(d):
 """Five complete operations derived from the actual substitution/primitive."""
 f=d['f'];H,a,b,result=[d[z] for z in ('H','a','b','result')]; upper=H.subs(t,b);lower=H.subs(t,a)
 if f=='line_log':
  return [result,result/s.sqrt(5),s.sqrt(5)*result,d['C']*s.log(d['A']),d['C']*(d['A']-d['B'])],['correct','omit_arc_length','square_metric','omit_lower_logarithm','wrong_reciprocal_primitive']
 # Each is a definite integral/endpoint operation, with exact scalar value.
 omit_metric=s.integrate(d['ft'],(t,a,b))
 if f=='line_power':wrong_power=d['C']*(b**3-a**3)/3
 elif f=='line_log':wrong_power=d['C']*(d['A']-d['B'])
 else:
  # Integrate u rather than sqrt(u), while retaining the correct Jacobian.
  alpha=s.simplify(H/d['u']**s.Rational(3,2)) if f!='sqrt' else None
  if f=='sqrt':wrong_power=d['C']/16*((d['B']**3-d['A']**3)/3-d['k']*(d['B']**2-d['A']**2)/2)
  else:wrong_power=alpha*s.Rational(3,2)*(d['B']**2-d['A']**2)/2
 vals=[result,omit_metric,upper+lower,upper,wrong_power]
 # At a=0 some primitives have nonzero lower endpoint; easy excludes a=0.
 return [s.simplify(v) for v in vals],['correct','omit_arc_length','add_endpoint_values','omit_lower_endpoint','wrong_power_primitive']

def eligible(vals):
 return all(v.is_real and v.is_finite and v>0 for v in vals) and all(not same(vals[i],vals[j]) for i in range(len(vals)) for j in range(i))

def sample(f,rng):
 c=rng.choice([1,2,3,4,6,8,10,12]);k=1;a=rng.choice([1,2]);b=a+rng.choice([1,2,3])
 if f=='line_power':k=rng.choice([1,2,3]);b=min(b,6)
 if f=='parabola':b=s.sqrt(rng.choice([2,6,12,20]));a=1
 if f=='implicit_parabola':k=rng.choice([4,6,8]);m=s.Integer(k)/2;lo=rng.choice([m+1,m+2]);hi=rng.choice([v for v in (lo+1,lo+2) if v<=8]);a=s.sqrt(lo*lo-m*m);b=s.sqrt(hi*hi-m*m)
 if f=='reciprocal':k=rng.choice([1,2,3]);a=1;b=rng.choice([2,3])
 if f=='line_log':k=rng.choice([4,5,6,7,8]);a=1;b=rng.choice(list(range(2,k-1)))
 if f=='exponential':k=2;a=0;b=s.log(rng.choice([2,3,4,5,6]))
 if f=='sqrt':k=rng.choice([1,2,3,4]);a=1;b=rng.choice([2,3,4,5])
 if f=='log_curve':a=1;b=s.sqrt(rng.choice([3,8,15,24]));k=1
 return dict(zip(('a','b','c','k'),map(str,(a,b,c,k))))

def render_plot(d):
 asset_dir=HERE/'plots';asset_dir.mkdir(exist_ok=True)
 key=hashlib.sha256(json.dumps([d['f'],str(d['g']),str(d['a']),str(d['b']),VERSION,'label-aware-v3']).encode()).hexdigest()[:24]
 output=asset_dir/(key+'.png')
 if output.exists() and output.with_suffix('.json').exists():return str(output)
 a,b=float(d['a']),float(d['b']);ys=[a+(b-a)*i/120 for i in range(121)];fn=s.lambdify(t,d['g'],'math');xs=[fn(z) for z in ys]
 labels=['('+tex(d['g'].subs(t,e))+','+tex(e)+')' for e in (d['a'],d['b'])]
 payload={'output':str(output),'family':d['f'],'curve':str(d['g']),'a':str(d['a']),'b':str(d['b']),'x':xs,'y':ys,'labels':labels,'traversal':'increasing y; arc-length value independent of direction'}
 fd,path=tempfile.mkstemp(prefix='.input-',suffix='.json',dir=asset_dir)
 try:
  with os.fdopen(fd,'w') as h:json.dump(payload,h)
  subprocess.run([sys.executable,str(HERE/'render_plot.py'),path],check=True,capture_output=True)
 finally:os.unlink(path)
 return str(output)

# EASY: authored direct straight-line parametrization, constant speed, one power primitive.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE: observed direct parabola/reciprocal/line-log; canonical log-curve extension.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD: observed implicit parabola/exponential; unrated sqrt authored assignment requires
# expansion into two primitive components, not a progression within this difficulty.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 raw=bool(profile and profile.startswith('source:'));qid=profile.split(':',1)[1] if raw else None
 if raw:
  f,ll,base=CASES[qid]
  if template and template!=f:raise ValueError('profile/template mismatch')
  if level!=ll:raise ValueError('source level mismatch')
  template=f
 elif profile not in (None,'method'):raise ValueError('unknown profile')
 rng=random.Random(seed); f=template or rng.choice(LEVELS[level]); explicit=parameters is not None
 if f not in LEVELS[level]:raise ValueError('template outside difficulty')
 for attempt in range(200):
  p=parameters if explicit else dict(CASES[qid][2]) if raw else sample(f,rng)
  if set(p)!=set(('a','b','c','k')):raise ValueError('parameter keys')
  d=guard(f,p,level,raw);vals,labels=(opaque_bank(qid,d) if raw else method_bank(d))
  if raw:
   if any(same(vals[i],vals[j]) for i in range(len(vals)) for j in range(i)):raise ValueError('raw evidence bank has equivalent values at requested endpoints')
   break
  if eligible(vals):break
  if explicit:raise ValueError('complete bank collision or invalid value')
 else:raise ValueError('could not sample eligible complete bank')
 if not raw:labels=[tex(v) for v in vals]
 if raw:prompt,solution=raw_strings(qid,d)
 else:
  curve=('y^2='+tex(d['k'])+'x') if f=='implicit_parabola' else 'x='+tex(d['g'].subs(t,y))
  xx=[d['g'].subs(t,z) for z in (d['a'],d['b'])]
  prompt='Evaluate the line integral\n$'+integral(tex(d['F']),d['a'],d['b'],'s').replace('_{'+tex(d['a'])+'}^{'+tex(d['b'])+'}','_{C}')+',$\nwhere $C$ is the section of the curve $'+curve+'$ from $('+tex(xx[0])+','+tex(d['a'])+')$ to $('+tex(xx[1])+','+tex(d['b'])+').$'
  solution=normal_solution(d)
 if f in ('sqrt','parabola','reciprocal','line_log'):
  if raw:
   base=CASES[qid][2]
   if any(not same(s.sympify(p[k]),s.sympify(base[k])) for k in ('a','b')):
    prompt=re.sub(r'!\[\]\(.*?\)',lambda m:'![]('+render_plot(d)+')',prompt,count=1)
  else:prompt='![]('+render_plot(d)+')\n\n'+prompt.replace(').$', '),$')+' as shown above.'
 fingerprint_curve=d['g']-d['k'] if f=='line_power' else d['g']
 mathematical=hashlib.sha256(s.srepr(d['F']).encode()+s.srepr(fingerprint_curve).encode()+s.srepr(d['a']).encode()+s.srepr(d['b']).encode()).hexdigest()
 # Actual displayed content controls identity; seed/profile aliases do not.
 identity=[level,prompt,solution,sorted(labels),':answer-field.type/radio'];qidgen=ident(identity);fid=ident([qidgen,'selection'])
 answers=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in labels]
 correct_indices=[i for i,v in enumerate(vals) if same(v,d['result'])]
 if len(correct_indices)!=1:raise ValueError('ambiguous/missing mathematical correct choice')
 correct=answers[correct_indices[0]][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 source_q=SOURCES.get(qid,{})
 if not raw or ':answer-field/correct' in source_q[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct]
 question={':question/id':qidgen,':question/problem':prompt,':question/answer-fields':[field]}
 if not raw or ':question/difficulty' in source_q:question[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:question[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':f,'bank_profile':profile or 'method','seed':seed,'parameters':{k:str(s.sympify(v)) for k,v in p.items()},'mathematical_fingerprint':mathematical,'eligible_for_learning':not raw,'evidence_only':raw,'source_id':qid,'source':{k:CAP[k] for k in ('database','basis','lineage')},'domain':('raw zero-endpoint evidence: original integrand or curve derivative undefined at zero; interpreted only by improper limit/continuous pulled-back integrand extension' if raw and f in ('implicit_parabola','sqrt') and d['a']==0 else 'regular nonnegative-y curve; increasing endpoint y; scalar arc length'),'mathematical_correct_value':str(d['result']),'bank_values':[str(v) for v in vals],'recipes':None if raw else method_bank(d)[1],'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def markdown(r):
 q=r['question'];g=r['generation'];sid=g.get('source_id')
 original=bool(sid and all(same(s.sympify(g['parameters'][k]),s.sympify(v)) for k,v in CASES[sid][2].items()))
 level=q.get(':question/difficulty','not rated').removeprefix(':question.difficulty/')
 out=('Original source replay' if original else 'Generated variant')+' / '+level+' / '+g['template']+' / '+g['bank_profile']+'\n\n'+q[':question/problem']+'\n\n'
 field=q[':question/answer-fields'][0];correct=field.get(':answer-field/correct',[None,None])[1]
 for a in field[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' **CORRECT**' if a[':answer/id']==correct else '')+'\n'
 if correct is None:out+='[Original correct designation absent; independently derived value '+g['mathematical_correct_value']+'.]\n'
 return out+'\n'+q.get(':question/worked-solution','(Source worked solution absent.)')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=[*LEVELS,'all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
