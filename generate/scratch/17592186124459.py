#!/usr/bin/env python3
"""Direction of maximum increase/decrease; frozen math basis 1356.

Six observed 5-choice radio families. Raw source profiles preserve omissions and
all original strings via parameterized whole-component masks. Opaque banks are
public evidence-only profiles. Defaults cover every supported source family with
complete method banks, selected before parameters. Hard is an authored logarithmic
3-component gradient followed by unit normalization, anchored to the canonical
log product and lesson's unit-gradient formula. No maximum-rate or dot-product task.
Easy: two held partials, small coefficients/coordinates; moderate: three held
partials, two linear-inner trig coefficients at familiar integer-pi phases.
Hard: three log chain-rule components and exact unit normalization, small reduced
rational components; explicit calls obey the same reduced workload bounds.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
from sympy.printing.latex import LatexPrinter
ROOT=Path(__file__).with_suffix('')
WRAPPER=json.loads((ROOT/'source.json').read_text())
SOURCE=WRAPPER['record']; KP=17592186124459
VERSION='maximum-direction-1'
X,Y,Z=s.symbols('x y z',real=True); VARS=(X,Y,Z)
class Printer(LatexPrinter):
 def _print_exp(self,e):return r'{e}^{'+self._print(e.args[0])+'}'
 def _print_log(self,e):return r'\operatorname{ln}⁡'+self._print(e.args[0])
def tex(v):
 t=Printer().doprint(s.sympify(v)).replace(r'\left', '').replace(r'\right','')
 t=t.replace('- ','-').replace(r' \pi',r'\pi').replace(r'- \pi',r'-\pi')
 return re.sub(r'\\pi(?![A-Za-z ])',r'\\pi ',t)
def num(v):return tex(v)
def cf(c,t):
 if c not in (1,-1) and (t[:1].isdigit() or (t.startswith('-') and t[1:2].isdigit())):return num(c)+r'\cdot ('+t+')'
 return ('' if c==1 else '-' if c==-1 else num(c))+t
def plus(*ts):return ''.join(('+' if i and not t.startswith('-') else '')+t for i,t in enumerate(ts) if t!='0') or '0'
def vec(v,style='tuple',space=r'\,'):
 v=[s.simplify(t) for t in v]
 if style=='tuple':return '⟨'+space.join([])+(','+space).join(tex(t) for t in v)+'⟩'
 parts=[]
 for c,b in zip(v,['i','j','k']):
  if c==0:continue
  t=tex(c); t='('+t+')' if c.is_Add else t
  parts.append((b if c==1 else '-'+b if c==-1 else t+space+b))
 return plus(*parts)
def tuple_text(ts):return '⟨'+r',\,'.join(ts)+'⟩'
def ij_text(ts,space=r'\,'):
 return plus(*[(('('+t+')') if ('+' in re.sub(r'\{[^{}]*\}', '', t) or ('-' in re.sub(r'\{[^{}]*\}', '', t)[1:])) else t)+space+b for t,b in zip(ts,['i','j'])])
def point(p):return '('+','.join(str(p[k]) for k in ('u','v','w') if k in p)+')'
FAMILIES={
 'cosxy':('easy',17592186124963,dict(a=1,b=1,u=1,v=1)),
 'linear_sin':('moderate',17592186124965,dict(a=1,b=2,c=1,u=1,v=1,w=2)),
 'quadratic':('easy',17592186265872,dict(a=1,b=3,c=2,u=2,v=1)),
 'mixed_sin':('moderate',17592186323874,dict(a=1,b=3,u=1,v=0,w=1)),
 'exp':('easy',17592186351517,dict(a=1,b=1,c=1,u=-1,v=1)),
 'trig_product':('easy',17592186354478,dict(a=3,b=1,u=0,v=1)),
 'log_unit':('hard',None,dict(a=2,b=3,c=4,u=1,v=1,w=2)),
}
QUESTIONS={q[':db/id']:q for q in SOURCE[':knowledge-point/questions']}
def model(t,p):
 a,b,c=p['a'],p['b'],p.get('c',1)
 if t=='cosxy':return a*s.cos(X)+b*X**2*Y
 if t=='quadratic':return a*X**2+b*X*Y+c*Y**2
 if t=='linear_sin':return a*Y**2+s.sin(b*s.pi*X+c*s.pi*Z)
 if t=='mixed_sin':return s.sin(a*s.pi*X+Y)+b*Z**2*X
 if t=='exp':return a*X*s.log(Y)+b*Y*s.exp(X)-c*X*Y
 if t=='trig_product':return a*X**2*s.sin(Y)-b*Y*s.cos(X)
 if t=='log_unit':return s.log(X**a*Y**b*Z**c)
 raise ValueError(t)
def data(t,p):
 f=model(t,p); vs=VARS[:3 if 'w'in p else 2]; d=[s.diff(f,v) for v in vs]
 sub=dict(zip(vs,[p[k] for k in ('u','v','w') if k in p]));g=[s.simplify(e.subs(sub)) for e in d]
 return f,vs,d,sub,g
# Complete-component formatting recipes. These retain each source's operative
# row structure, including the distinct trig-argument evaluation row.
def components(t,p):
 a,b,c,u,v,w=(p.get(k,1) for k in ['a','b','c','u','v','w']);spc=r'\text{ }' if t in ('exp','trig_product') else r'\,'
 if t=='cosxy':fun=cf(a,r'\cos x')+' + '+cf(b,'x^{2}y')
 elif t=='quadratic':fun=plus(cf(a,'{x}^{2}'),cf(b,'xy'),cf(c,'{y}^{2}'))
 elif t=='linear_sin':fun=cf(a,'{y}^{2}')+r'+\operatorname{sin}⁡('+cf(b,r'\pi x')+'+'+cf(c,r'\pi z')+')'
 elif t=='mixed_sin':fun=r'\operatorname{sin}⁡('+cf(a,r'\pi x')+'+y)+'+cf(b,'{z}^{2}x')
 elif t=='exp':fun=plus(cf(a,r'x\operatorname{ln}⁡y'),cf(b,r'y{e}^{x}'),cf(-c,'xy'))
 elif t=='trig_product':fun=plus(cf(a,r'{x}^{2}\operatorname{sin}⁡y'),cf(-b,r'y\operatorname{cos}⁡x'))
 else:fun=r'\ln ('+cf(1,'x^{'+str(a)+'}y^{'+str(b)+'}z^{'+str(c)+'}')+')'
 f,vs,d,sub,g=data(t,p)
 formal=[r'\frac{∂}{∂'+str(var)+'}('+fun+')' for var in vs]
 formal=tuple_text(formal) if len(vs)==3 else formal[0]+spc+'i+'+formal[1]+spc+'j'
 if t=='quadratic':
  ds=[plus(cf(2*a,'x'),cf(b,'y')),plus(cf(b,'x'),cf(2*c,'y'))]
  subst=[num(2*a)+'('+str(u)+')+'+num(b)+'('+str(v)+')',num(b)+'('+str(u)+')+'+num(2*c)+'('+str(v)+')']
 elif t=='exp':
  ds=[plus(cf(a,r'\operatorname{ln}⁡y'),cf(b,r'y{e}^{x}'),cf(-c,'y')),plus(cf(a,r'\frac{x}{y}'),cf(b,r'{e}^{x}'),cf(-c,'x'))]
  subst=[plus(cf(a,r'\operatorname{ln}⁡'+str(v)),cf(b,str(v)+r'\cdot {e}^{'+str(u)+'}'),cf(-c,str(v))),plus(cf(a,r'\frac{'+str(u)+'}{'+str(v)+'}'),cf(b,r'{e}^{'+str(u)+'}'),cf(-c,'('+str(u)+')'))]
 elif t=='trig_product':
  ds=[plus(cf(b,r'y\operatorname{sin}⁡x'),cf(2*a,r'x\operatorname{sin}⁡y')),plus(cf(a,r'{x}^{2}\operatorname{cos}⁡y'),cf(-b,r'\operatorname{cos}⁡x'))]
  subst=[plus(cf(b,str(v)+r'\cdot \operatorname{sin}⁡('+str(u)+')'),cf(2*a,r'\cdot '+str(u)+r'\cdot \operatorname{sin}⁡('+str(v)+')')),plus(cf(a,'('+str(u)+r')^{2}\operatorname{cos}⁡('+str(v)+')'),cf(-b,r'\operatorname{cos}⁡('+str(u)+')'))]
 elif t=='linear_sin':
  arg=cf(b,r'\pi x')+'+'+cf(c,r'\pi z'); val=cf(b,r'\pi \cdot '+str(u))+'+'+cf(c,r'\pi \cdot '+str(w)); theta=(b*u+c*w)*s.pi
  ds=[cf(b,r'\pi \operatorname{cos}⁡('+arg+')'),cf(2*a,'y'),cf(c,r'\pi \operatorname{cos}⁡('+arg+')')]
  subst=[cf(b,r'\pi \operatorname{cos}⁡('+val+')'),num(2*a)+r'\cdot '+str(v),cf(c,r'\pi \operatorname{cos}⁡('+val+')')]
  partial=[cf(b,r'\pi \operatorname{cos}⁡('+tex(theta)+')'),tex(2*a*v),cf(c,r'\pi \operatorname{cos}⁡('+tex(theta)+')')]
 elif t=='mixed_sin':
  arg=cf(a,r'\pi x')+'+y'; val=cf(a,r'\pi \cdot '+str(u))+'+'+str(v);theta=a*s.pi*u+v
  ds=[cf(a,r'\pi \operatorname{cos}⁡('+arg+')')+'+'+cf(b,'{z}^{2}'),r'\operatorname{cos}⁡('+arg+')',cf(2*b,'xz')]
  subst=[cf(a,r'\pi \operatorname{cos}⁡('+val+')')+'+'+num(b)+r'\cdot {'+str(w)+'}^{2}',r'\operatorname{cos}⁡('+val+')',num(2*b)+r'\cdot '+str(u)+r'\cdot '+str(w)]
  partial=[cf(a,r'\pi \operatorname{cos}⁡('+tex(theta)+')')+'+'+tex(b*w*w),r'\operatorname{cos}⁡('+tex(theta)+')',tex(2*b*u*w)]
 elif t=='cosxy':
  ds=[plus(cf(-a,r'\sin x'),cf(2*b,'xy')),cf(b,'x^{2}')]
  subst=[plus(cf(-a,r'\sin ('+str(u)+')'),num(2*b)+r'\cdot ('+str(u)+r')\cdot ('+str(v)+')'),num(b)+r'\cdot ('+str(u)+')^{2}']
 else:
  ds=[r'\frac{'+str(a)+'}{x}',r'\frac{'+str(b)+'}{y}',r'\frac{'+str(c)+'}{z}']
  subst=[r'\frac{'+str(p[q])+'}{'+str(p[r])+'}' for q,r in [('a','u'),('b','v'),('c','w')]]
 if len(vs)==2:
  deriv='('+ds[0]+')'+spc+'i+('+ds[1]+')'+spc+'j'
  evaluated='('+subst[0]+')'+spc+'i+('+subst[1]+')'+spc+'j'
 else:deriv=tuple_text(ds);evaluated=tuple_text(subst)
 final=vec(g,'tuple' if len(vs)==3 else 'ij',spc)
 # Keep source's exponent convention and positive-before-negative term order.
 if t=='exp' and p['v']==1:
  E=cf(b,r'{e}^{'+str(u)+'}')
  final=ij_text([plus(E,tex(-c)),plus(E,tex((a-c)*u))],spc).replace(r'\text{ }j','j')
 if t=='mixed_sin':final=tuple_text([plus(tex(a*s.pi*s.cos(theta)),tex(b*w*w)),tex(s.cos(theta)),tex(2*b*u*w)])
 rows=[formal,deriv,evaluated]
 if t in ('linear_sin','mixed_sin'):rows.append(tuple_text(partial))
 rows.append(final)
 return fun,rows,final

def source_bank(t,p):
 """Full historical bank formulas. Opaque recipes never enter defaults."""
 a,b,c,u,v,w=(p.get(k,1) for k in ['a','b','c','u','v','w']);g=data(t,p)[4];P=s.pi
 if t=='cosxy':
  vals=[[-a*s.sin(u),2*b*u*v],[-2*b*u*v,-b*u*u],g,[-e for e in g],[2*b*u*v,b*u*u]]
  texts=[cf(-a,r'\sin ('+str(u)+')')+'i + '+cf(2*b*u*v,'j'),tex(-2*b*u*v)+'i - '+cf(b*u*u,'j'),'('+tex(2*b*u*v)+' - '+cf(a,r'\sin ('+str(u)+')')+')i + '+cf(b*u*u,'j'),'('+cf(a,r'\sin ('+str(u)+')')+' - '+tex(2*b*u*v)+')i - '+cf(b*u*u,'j'),tex(2*b*u*v)+'i + '+cf(b*u*u,'j')];idx=2
 elif t=='quadratic':
  vals=[[v,-u],[u,v],g,[2*u,v],[b,-(a+2*c)]];texts=[vec(e,'ij') for e in vals];idx=2
 elif t=='linear_sin':
  theta=(b*u+c*w)*P;co=s.cos(theta)
  vals=[[-e for e in g],[b*co,2*a*v,c*co],[-c*P,-a*v,c*P],[c*P,2*a*v,c*P],g]
  texts=[vec(e,'tuple','') for e in vals];idx=4
 elif t=='mixed_sin':
  theta=a*P*u+v;co=s.cos(theta)
  vals=[[b*w*w,-a*P,b*u*w],[g[0],a*P,b*u*w],[b*w*w,0,g[2]],g,[a*co+b*w*w,co,g[2]]]
  texts=[vec(e) for e in vals];texts[1]=tuple_text([plus(tex(a*P*co),tex(b*w*w)),tex(a*P),tex(b*u*w)]);texts[3]=components(t,p)[2];idx=3
 elif t=='exp':
  E=s.exp(u);R=s.exp(-u)
  vals=[[a*s.log(v)+b*v*E+c*v,b*E+c*u],[a*s.log(v)+b*v*R-c*v,s.Rational(a*u,v)+b*R-c*u],[g[0]+2*c*v,g[1]],g,[a*s.log(v)+b*v*R+c*v,b*R+c*u]]
  def ef(k,sign):return plus(cf(b*v,r'{e}^{'+str(k)+'}'),tex(sign*c*v))
  def es(k,add):return plus(cf(b,r'{e}^{'+str(k)+'}'),tex(add))
  texts=[ij_text([ef(u,1),es(u,c*u)],r'\text{ }'),ij_text([ef(-u,-1),es(-u,(a-c)*u)],r'\text{ }'),ij_text([ef(u,1),es(u,(a-c)*u)],r'\text{ }'),components(t,p)[2],ij_text([ef(-u,1),es(-u,c*u)],r'\text{ }')]
  # Original positive exponential printed e, not {e}^{1}.
  texts=[v.replace(r'{e}^{1}','e') for v in texts];idx=3
 elif t=='trig_product':
  vals=[g,[-e for e in g],[b,b],[2*b,-b],[b,-b]];texts=[vec(e,'ij','') for e in vals];idx=0
 else:raise ValueError('No source bank')
 # Original exp bank omits the thin text space before j; polynomial bank uses
 # thin space only when coefficient != +/-1. Normal math remains identical.
 if t=='exp':texts=[q.replace(r'\text{ }j','j') for q in texts]
 if t=='quadratic':texts=[q.replace(r'\,i','\\,i').replace(r'\,j',r'\,j') for q in texts]
 return vals,texts,idx

def extracted(t):
 q=QUESTIONS[FAMILIES[t][1]];p=FAMILIES[t][2];fun,rows,fin=components(t,p)
 problem=q[':question/problem'];actual=re.search(r'\$[fg]\([^$]*?\)\s*=([^$]+)\$',problem).group(1)
 prompt=problem.replace(actual.strip(),'§FUNCTION§').replace(point(p),'§POINT§').replace('(1, 1)','§SPACED_POINT§')
 if ':question/worked-solution' not in q:return prompt,None
 sol=q[':question/worked-solution'];matches=re.findall(r' & =(.+?)(?= \\\\ |\\end\{aligned\})',sol)
 assert len(matches)==len(rows),(t,len(matches),len(rows))
 # Each aligned RHS is an entire slot; no replacements in prose/i/j labels.
 for i,old in enumerate(matches):sol=sol.replace(' & ='+old,' & =§ROW'+str(i)+'§',1)
 sol=sol.replace(point(p),'§POINT§')
 # Source exp's wrong label intentionally remains in raw profile.
 if t=='exp':sol=sol.replace('∇f(1,1)','∇f§LEGACY_POINT§')
 tail=re.search(r'direction of \$(.+?)\.\$',sol).group(1);sol=sol.replace('direction of $'+tail,'direction of $§FINAL§')
 return prompt,sol
MASKS={t:extracted(t) for t in FAMILIES if t!='log_unit'}
def fill(mask,t,p,rows=None,fin=None,raw=False):
 fun,r,f=components(t,p);rows=rows or r;fin=fin or f
 replacements={'FUNCTION':fun,'POINT':point(p),'SPACED_POINT':'('+str(p['u'])+', '+str(p['v'])+')','FINAL':fin,'LEGACY_POINT':point(dict(p,u=-p['u'])) if raw else point(p)}
 replacements.update({'ROW'+str(i):v for i,v in enumerate(rows)})
 for k,v in replacements.items():mask=mask.replace('§'+k+'§',v)
 assert '§'not in mask
 return mask

def guard(t,p,raw=False,bank_kind=None):
 keys=set(FAMILIES[t][2])|{'direction'}
 if set(p)-keys:raise ValueError('Unknown parameters')
 for k in FAMILIES[t][2]:
  if k not in p:raise ValueError('Missing '+k)
  if type(p[k]) is not int:raise ValueError('Integral parameters required')
 if p.get('direction','increase')not in ('increase','decrease'):raise ValueError('direction')
 if raw and p.get('direction','increase')!='increase':raise ValueError('Raw source profiles are increase')
 for k in ('a','b','c'):
  if k in p and not 1<=p[k]<= (6 if t=='log_unit' else 4):raise ValueError('Nonzero small coefficients required')
 if t in ('cosxy','quadratic') and (not 1<=abs(p['u'])<=3 or not 1<=abs(p['v'])<=3):raise ValueError('Easy nonzero coordinates <=3')
 if t=='exp' and (p['u']not in (-2,-1,1,2) or p['v']!=1):raise ValueError('Easy exact exp/log anchor workload')
 if t=='trig_product':
  if p['u']not in (-1,0,1) or p['v']not in (-1,1):raise ValueError('Easy trig evaluation bounds')
  if not raw and ((bank_kind=='axis') != (p['u']==0)):raise ValueError('Complete axis/nonaxis bank eligibility')
 if t=='linear_sin' and (p['b']==p['c'] or not all(1<=abs(p[k])<=3 for k in ('u','v','w')) or abs(p['b']*p['u']+p['c']*p['w'])>12):raise ValueError('Moderate familiar pi phase and distinct chain factors')
 if t=='mixed_sin' and (p['v']!=0 or not 1<=abs(p['u'])<=3 or not 1<=abs(p['w'])<=2 or abs(p['a']*p['u'])>6):raise ValueError('Moderate familiar pi phase')
 if t=='log_unit':
  if not all(1<=p[k]<=3 for k in ('u','v','w')):raise ValueError('Positive log-domain coordinates <=3')
  g=data(t,p)[4]
  norm2=s.factor(sum(e*e for e in g))
  if any(e>4 or s.denom(e)>3 for e in g) or norm2>36 or s.numer(norm2)>50 or s.denom(norm2)>9:raise ValueError('Reduced gradient components/norm exceed hard arithmetic bound')
  # Nonuniform direction; retain at least one genuinely assessed normalization.
  if len(set(g))<2 or sum(e*e for e in g)==1:raise ValueError('Hard normalization demand degenerates')

def method_bank(t,p):
 f,vs,d,sub,g=data(t,p);a,b,c=(p.get(k,1) for k in ['a','b','c']);u,v,w=(p.get(k,1) for k in ['u','v','w'])
 if t=='cosxy':errs=[[2*b*u*v,b*u*u],[-a*s.sin(u),b*u*u],[g[0],2*b*u*v]]
 elif t=='quadratic':errs=[[2*a*u,g[1]],[g[0],2*c*v],[a*u+b*v,b*u+c*v]]
 elif t=='linear_sin':co=s.cos((b*u+c*w)*s.pi);errs=[[s.pi*co,g[1],g[2]],[g[0],a*v,g[2]],[g[0],g[1],co]]
 elif t=='mixed_sin':co=s.cos(a*s.pi*u+v);errs=[[b*w*w,co,g[2]],[a*s.pi*co+b*w*w,co,b*u*w],[co+b*w*w,co,g[2]]]
 elif t=='exp':errs=[[a*s.log(v)+b*v*s.exp(u)+c*v,g[1]],[g[0],b*s.exp(u)-c*u],[a*s.log(v)+b*v*s.exp(-u)-c*v,s.Rational(a*u,v)+b*s.exp(-u)-c*u]]
 elif t=='trig_product':
  if u==0:
   # Complete axis bank, separately selected before random parameters.
   errs=[[b*v*s.sin(u)+2*a*s.sin(v),g[1]],[g[1],g[0]],[-b*v*s.cos(u)+2*a*u*s.sin(v),g[1]]]
  else:errs=[[2*a*u*s.sin(v),g[1]],[g[0],a*u*u*s.cos(v)+b*s.cos(u)],[g[1],g[0]]]
 elif t=='log_unit':
  N=s.sqrt(sum(e*e for e in g));target=[e/N for e in g]
  # Complete normalization bank: opposite direction, no normalization,
  # squared norm normalization, and a missing inner power in x partial.
  h=[s.Rational(1,u),g[1],g[2]];H=s.sqrt(sum(e*e for e in h))
  return [target,[-e for e in target],g,[e/N**2 for e in g],[e/H for e in h]],0
 else:raise ValueError(t)
 return [g,[-e for e in g],*errs],0

def same_direction(a,b):
 if all(s.simplify(e)==0 for e in a) or all(s.simplify(e)==0 for e in b):return False
 j=next(i for i,e in enumerate(b) if s.simplify(e)!=0)
 if not all(s.simplify(x*b[j]-y*a[j])==0 for x,y in zip(a,b)):return False
 r=s.simplify(a[j]/b[j])
 if r.is_positive is None:raise ValueError('Unresolved parallel-vector orientation')
 return bool(r.is_positive)
def eligible(v,target,unit=False):return same_direction(v,target) and (not unit or s.simplify(sum(e*e for e in v)-1)==0)
def validate_bank(vals,idx,unit):
 if len(vals)!=5 or any(all(s.simplify(e)==0 for e in v) for v in vals):raise ValueError('Undefined zero vector bank')
 for i in range(5):
  if eligible(vals[i],vals[idx],unit)!=(i==idx):raise ValueError('Ambiguous direction bank')
  for j in range(i):
   if (same_direction(vals[i],vals[j]) if not unit else all(s.simplify(a-b)==0 for a,b in zip(vals[i],vals[j]))):raise ValueError('Duplicate requested directions/vectors')

def sample(t,rng,bank_kind=None):
 p={k:rng.randint(1,4)for k in FAMILIES[t][2]}
 if t in ('cosxy','quadratic'):p.update(u=rng.choice([-3,-2,-1,1,2,3]),v=rng.choice([-3,-2,-1,1,2,3]))
 elif t=='exp':p.update(u=rng.choice([-2,-1,1,2]),v=1)
 elif t=='trig_product':p.update(u=0 if bank_kind=='axis' else rng.choice([-1,1]) if bank_kind=='nonaxis' else rng.choice([-1,0,1]),v=rng.choice([-1,1]))
 elif t=='linear_sin':p.update(u=rng.choice([-2,-1,1,2]),v=rng.choice([-2,-1,1,2]),w=rng.choice([-2,-1,1,2]))
 elif t=='mixed_sin':p.update(u=rng.choice([-2,-1,1,2]),v=0,w=rng.choice([-2,-1,1,2]))
 else:p={k:rng.randint(1,6) if k in ('a','b','c') else rng.randint(1,3) for k in FAMILIES[t][2]}
 p['direction']=rng.choice(['increase','decrease']);return p

def hard_solution(p):
 fun,rows,fin=components('log_unit',p);_,vs,ds,sub,g=data('log_unit',p);sgn=1 if p.get('direction','increase')=='increase'else -1;N=s.sqrt(sum(e*e for e in g));tar=[sgn*e/N for e in g]
 formal=rows[0]
 # Explicit held-partial chain operands precede cancellation to a/x,b/y,c/z.
 inn='x^{'+str(p['a'])+'}y^{'+str(p['b'])+'}z^{'+str(p['c'])+'}'
 chain=tuple_text([r'\frac{1}{'+inn+r'}\cdot '+cf(p[k],''.join(str(v)+'^{'+str(p[j]-(1 if v==var else 0))+'}' for v,j in zip(vs,['a','b','c']))) for k,var in zip(['a','b','c'],vs)])
 rr=[formal,chain,rows[1],rows[2],fin]
 phase='increases'if sgn==1 else 'decreases';relation='in the direction of its gradient'if sgn==1 else 'in the direction opposite to that of its gradient'
 sol=f'At a given point, a function $f(x,y,z)$ {phase} most rapidly {relation}.\n\nSo, we compute $∇f(x,y,z)$ and evaluate it at the point ${point(p)}:$\n\n$$\n'+r'\begin{aligned}∇f(x,y,z) & ='+rr[0]+r' \\ & ='+rr[1]+r' \\ & ='+rr[2]+r' \\ ∇f'+point(p)+' & ='+rr[3]+r' \\ & ='+rr[4]+r'\end{aligned}'+'\n$$\n\nThe corresponding unit direction is\n\n$$\n'+r'\begin{aligned}u & ='+('-'if sgn<0 else '')+r'\frac{∇f'+point(p)+r'}{‖∇f'+point(p)+r'‖} \\ & ='+r'\frac{'+str(sgn)+r'}{\sqrt{'+ '+'.join('('+tex(e)+')^{2}'for e in g)+'}}'+fin+r' \\ & ='+vec(tar)+r'\end{aligned}'+'\n$$\n\nTherefore, the function '+phase+' most rapidly in the unit direction of $'+vec(tar)+'.$'
 return sol

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'maximum-direction/'+v))
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio observed')
 rng=random.Random(seed);choices=[t for t,z in FAMILIES.items()if z[0]==level]
 t=template or rng.choice(choices)
 if t not in choices:raise ValueError('Template level mismatch')
 raw=profile=='source';profile=profile or 'method'
 if profile not in ('source','method','axis_method','nonaxis_method'):raise ValueError('Unknown complete bank')
 if profile in ('axis_method','nonaxis_method') and t!='trig_product':raise ValueError('Axis bank applies only to trig_product')
 bank_kind=None
 if t=='trig_product' and not raw:
  bank_kind=('axis' if profile=='axis_method' else 'nonaxis' if profile=='nonaxis_method' else ('axis' if parameters['u']==0 else 'nonaxis') if parameters is not None else rng.choice(['axis','nonaxis']))
  profile=bank_kind+'_method'
 if raw and t=='log_unit':raise ValueError('No source hard profile')
 for attempt in range(10000):
  p=dict(parameters)if parameters is not None else sample(t,rng,bank_kind)
  if raw and parameters is None:p=sample(t,rng);p['direction']='increase'
  try:
   guard(t,p,raw,bank_kind);f,vs,d,sub,g=data(t,p)
   if raw:vals,texts,idx=source_bank(t,p)
   else:vals,idx=method_bank(t,p);texts=[]
   if not raw:
    sign=1 if p.get('direction','increase')=='increase'else -1
    vals=[[s.simplify(sign*e)for e in v]for v in vals];texts=[vec(v,'tuple'if len(vs)==3 else 'ij')for v in vals]
   validate_bank(vals,idx,t=='log_unit');break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('No eligible complete instance')
 fun,rows,fin=components(t,p)
 if t=='log_unit':
  prompt='In what unit direction does the function $f(x,y,z)='+fun+'$ '+p.get('direction','increase')+' most rapidly at the point $'+point(p)+'$?';sol=hard_solution(p)
 else:
  mask,sm=MASKS[t];prompt=fill(mask,t,p)
  sol=fill(sm,t,p,raw=raw)if sm else None
  if not raw and sol is None:
   sol='At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.\n\nSo, we compute $∇f(x,y)$ and evaluate it at the point $'+point(p)+':$\n\n$$\n'+r'\begin{aligned}∇f(x,y) & ='+rows[0]+r' \\ & ='+rows[1]+r' \\ ∇f'+point(p)+' & ='+rows[2]+r' \\ & ='+rows[-1]+r'\end{aligned}'+'\n$$\n\nTherefore, the function increases most rapidly in the direction of $'+fin+'.$'
  if not raw and p.get('direction','increase')=='decrease':
   prompt=prompt.replace('increase most rapidly','decrease most rapidly');sol=sol.replace('increases most rapidly in the direction of its gradient at that point.','decreases most rapidly in the direction opposite to that of its gradient.');sol=sol.replace('Therefore, the function increases most rapidly in the direction of $'+fin,'Therefore, the function decreases most rapidly in the direction of $'+vec([-e for e in g],'tuple'if len(vs)==3 else 'ij'))
  if raw:
   q0=QUESTIONS[FAMILIES[t][1]]
   # Source row/conclusion format generated above, all original omissions kept.
 q={':question/problem':prompt}
 if sol is not None:q[':question/worked-solution']=sol
 if not raw or ':question/difficulty'in QUESTIONS[FAMILIES[t][1]]:q[':question/difficulty']=':question.difficulty/'+level
 field={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
 # Canonical task excludes common positive function scaling for direction-only
 # tasks; unit normalization itself remains part of the hard assessed demand.
 normal_f=s.expand_log(f,force=True);coeff=normal_f.as_content_primitive()[0];normal_f=s.simplify(normal_f/coeff)
 parameter_fp=digest([str(normal_f),[str(sub[v])for v in vs]])
 oriented=[(1 if p.get('direction','increase')=='increase' else -1)*e for e in g]
 first=next(e for e in oriented if e!=0)
 # Canonical direction removes every incidental positive common magnitude,
 # not only an explicit common coefficient in the printed function.
 direction_signature=[str(s.simplify(e/s.Abs(first))) for e in oriented]
 math_fp=digest([t,direction_signature,'unit normalization'if t=='log_unit'else'parallel orientation'])
 content_fp=digest([VERSION,level,q,sorted(texts),idx and texts[idx]or texts[0]])
 qid=uid(content_fp);fid=uid(qid+'/selection');field[':answer-field/id']=fid
 bank=[{':answer/id':uid(fid+'/'+text),':answer/type':':answer.type/math',':answer/value':text}for text in texts]
 if not raw or ':answer-field/correct'in QUESTIONS[FAMILIES[t][1]][':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',bank[idx][':answer/id']]
 rng.shuffle(bank);field[':answer-field/choices']=bank;q[':question/answer-fields']=[field];q[':question/id']=qid
 return {'knowledge_point':{'db_id':KP,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source':{k:WRAPPER[k]for k in ('database','basis','lineage')},'template':t,'profile':profile,'parameters':p,'seed':seed,'mathematical_fingerprint':math_fp,'parameter_fingerprint':parameter_fp,'content_fingerprint':content_fp,'source_ids':[]if t=='log_unit'else[FAMILIES[t][1]],'evidence_only':raw,'eligible_for_learning':not raw,'response_criterion':'unit direction'if t=='log_unit'else 'positive parallel direction','runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}
# Easy: same two-variable held-partial/evaluation/orientation demand across families.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: same three-variable partials and familiar linear-inner trig evaluations.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard (authored): three logarithmic chain partials plus exact unit normalization.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];txt=q[':question/problem']+'\n\n'
 for a in q[':question/answer-fields'][0][':answer-field/choices']:txt+='- $'+a[':answer/value']+'$\n'
 return txt+'\n'+q.get(':question/worked-solution','[Raw source omits worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2)if args.format=='json'else'\n\n---\n\n'.join(map(markdown,records)))
