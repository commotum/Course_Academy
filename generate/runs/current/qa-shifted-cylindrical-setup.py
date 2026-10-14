"""Root actual shifted circle, polar root, height transforms and full option values."""
import json,re,hashlib,sys,importlib.util,functools
from pathlib import Path
import sympy as s
import numpy as np
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186129268;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 q=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(q);sys.modules[name]=m;q.loader.exec_module(m);return m
b=load(R/'qa-cylindrical-setup.py','root_shift_base');base=b.b;p=b.p;x,y,z,r,theta=b.x,b.y,b.z,b.r,b.theta;math,eq,integral=b.math,b.eq,b.integral
@functools.lru_cache(maxsize=4096)
def value(obj,n):
 a,b,lo,hi,zlo,zhi,fn=obj;inner=s.integrate(fn,(z,zlo,zhi));f=s.lambdify((r,theta),inner,'numpy');upper=s.lambdify(theta,hi,'numpy');lower=s.lambdify(theta,lo,'numpy');nodes,weights=np.polynomial.legendre.leggauss(n);tt=float(a)+(nodes+1)*float(b-a)/2;rr=np.asarray(upper(tt))+np.zeros_like(tt);ll=np.asarray(lower(tt))+np.zeros_like(tt);rho=ll[:,None]+(rr-ll)[:,None]*(nodes[None,:]+1)/2;vals=np.asarray(f(rho,tt[:,None]),complex)+np.zeros_like(rho);assert np.all(np.isfinite(vals)) and np.max(np.abs(vals.imag))<1e-12;return float(np.sum(vals.real*(rr-ll)[:,None]*weights[:,None]*weights[None,:])*float(b-a)/4)
C={k:0 for k in ('records','actual_circle','actual_heights','actual_integrands','circle_stages','converted_heights','polar_stages','setup_stages','choice_integrals','quadrature_convergence','whole_banks','full_value_pairs','geometry')}
def read(q):
 text=q[':question/problem'];region=next(bb for bb in p.p.blocks(text) if '(x,y,z)' in bb and r'\le' in bb);region=region.replace(r'\,','');parts=region.split(':',1)[1].rstrip('},').replace(r'\}','').split(',');circle=parts[0];lhs,rs=circle.split(r'\le');cart=math(lhs);S=math(rs);cx=-s.expand(cart).coeff(x)/2;cy=-s.expand(cart).coeff(y)/2;A=s.sqrt(S);assert eq(cx*cx+cy*cy,S) and (cx==0)!=(cy==0);sub={x:r*s.cos(theta),y:r*s.sin(theta)};poly=s.expand_trig(cart.subs(sub,simultaneous=True)-S);rad=2*cx*s.cos(theta)+2*cy*s.sin(theta);assert eq(poly,r*(r-rad))
 heights=next(w for w in parts if r'\le z\le' in w);lo,hi=heights.split(r'\le z\le');lo,hi=math(lo),math(hi);zlo,zhi=[s.refine(s.trigsimp(v.subs(sub,simultaneous=True)),s.Q.nonnegative(r)) for v in (lo,hi)]
 body=next(bb for bb in p.p.blocks(text) if '{∭}_{R}' in bb);fragment=re.split(r'\\(?:,|mathrm|text)',body.replace('{∭}_{R}',''))[0];F=math(fragment);pol=s.refine(s.trigsimp(F.subs(sub,simultaneous=True)*r),s.Q.nonnegative(r))
 if cx<0:aa,bb=s.pi/2,3*s.pi/2
 elif cx>0:aa,bb=(0,s.pi/2) if r'y\ge 0' in region else (3*s.pi/2,2*s.pi) if r'y\le 0' in region else (-s.pi/2,s.pi/2)
 elif cy<0:aa,bb=s.pi,2*s.pi
 else:aa,bb=(s.pi/2,s.pi) if r'x\le 0' in region else (0,s.pi/2) if r'x\ge 0' in region else (0,s.pi)
 return (aa,bb,0,rad,zlo,zhi,pol),F,(cart,S,cx,cy,A),poly

def check(rec):
 q=rec['question'];wanted,F,(cart,S,cx,cy,A),poly=read(q);aa,bb,lo,rad,zlo,zhi,pol=wanted;C['actual_circle']+=1;C['actual_heights']+=2;C['actual_integrands']+=1;sol=q[':question/worked-solution'];groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(groups)==2
 circle=groups[0].replace('&','').split(chr(92)*2);assert len(circle)==6
 for idx,row in enumerate(circle):
  lhs,rhs=row.split('=');actual=math(lhs)-math(rhs)
  if idx==0:assert eq(actual,cart-S)
  else:assert eq(actual,poly),(row,poly)
  C['circle_stages']+=1
 assert 'cos' in circle[3] and 'sin' in circle[3] and 'r(r' in circle[-1]
 stated=math(re.search(r'we must have \$r=(.*?)\$',sol)[1]);assert eq(stated,rad)
 heights=re.findall(r'bounded (?:below|above) by \$z=(.*?)\$',sol);assert len(heights)==2
 for raw,expected in zip(heights,(zlo,zhi)):
  parts=raw.rstrip('.,').split('=');assert eq(math(parts[0]).subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True),math(parts[-1])) and eq(math(parts[-1]),expected);C['converted_heights']+=1
 chain=groups[-1];rows=chain.split(chr(92)*2);fam=rec['generation']['template'];assert len(rows)==(3 if fam in ('left_inverse','right_radical','upper_square') else 2)
 for row in rows:
  if '=' not in row:continue
  lhs,rhs=row.replace('&','').split('=',1)
  if '{∭}_{R}' in lhs:assert eq(math(re.split(r'\\(?:,|mathrm|text)',lhs.replace('{∭}_{R}',''))[0]),F)
  if '{∭}_{Δ}' in rhs:fn=re.split(r'\\,?dz|dz',rhs.replace('{∭}_{Δ}',''))[0].rstrip(' '+chr(92)+',');assert eq(math(fn),pol);C['polar_stages']+=1
  else:assert all(eq(u,v) for u,v in zip(integral(rhs),wanted));C['setup_stages']+=1
 f=q[':question/answer-fields'][0];objects=[integral(v[':answer/value']) for v in f[':answer-field/choices']];assert len(objects)==5;correct=[v[':answer/id'] for v,o in zip(f[':answer-field/choices'],objects) if all(eq(u,w) for u,w in zip(o,wanted))];assert correct==[f[':answer-field/correct'][1]]
 vals=[value(o,80) for o in objects];fresh=[value(o,128) for o in objects];assert all(abs(u-v)<1e-9*max(1,abs(u),abs(v)) for u,v in zip(vals,fresh));assert all(abs(u-v)>1e-10*max(1,abs(u),abs(v)) for i,u in enumerate(fresh) for v in fresh[:i]);C['quadrature_convergence']+=5;C['choice_integrals']+=5;C['whole_banks']+=1;C['full_value_pairs']+=10
 path=Path(re.search(r'!\[\]\((.*?)\)',sol)[1]);side=json.loads(path.with_suffix('.json').read_text());assert side['a']==A and side['center']==[cx,cy] and tuple(s.sympify(v) for v in side['angle_bounds'])==(aa,bb);C['geometry']+=1;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_shift_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,(lev,sid,params) in g.TEMPLATES.items():records.append(g.generate(lev,template=fam,seed=846))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
