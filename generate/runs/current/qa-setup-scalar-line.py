"""Root setup-only scalar line integrals: actual operator chains and full banks."""
import json,re,hashlib,importlib.util,sys
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('scalar_shared',R/'qa-parametric-scalar-line.py');base=importlib.util.module_from_spec(z);z.loader.exec_module(base)
p,e=base.p,base.e;t,x,y,z=base.t,base.x,base.y,base.z;scalar,equal,groups,right=base.scalar,base.equal,base.groups,base.right
K=17592186133829;D=base.ROOT/f'generate/scratch/{K}'
def prompt(q):
 text=q[':question/problem'];bs=p.blocks(text);fblock=next(b for b in bs if r'\int' in b);fbody=re.sub(r'^.*?\\int(?:\s*\})?_\{?C\}?','',fblock);fbody=re.sub(r'(?:\\(?:text|mathrm)\{d\}s|ds)\s*[,.?]*$','',fbody);F=scalar(next(b.split('=',1)[1] for b in bs if re.match(r'f\(.*?\)\s*=',b))) if fbody.strip().startswith('f(') else scalar(fbody)
 rb=next(b for b in bs if re.search(r'r\(t\)\s*=',b));curve=p.vector(rb.split('=',1)[1]);nd=len(curve) if ('⟨' in rb or r'\langle' in rb) else 3 if re.search(r'(?<![A-Za-z])k(?![A-Za-z])',rb) else 2;curve=curve[:nd]
 ib=next(b for b in bs if re.search(r'\\le(?![A-Za-z])',b) or r'\in [' in b)
 if r'\in [' in ib:
  a,b=re.search(r'\\in \[(.*?),(.*?)\]',ib).groups()
 else:a,b=re.split(r'\\le\s*t\s*\\le',ib)
 bounds=(scalar(a.removeprefix(r'\,')),scalar(b));assert bounds[1]>bounds[0];pull=s.trigsimp(s.expand(F.subs(dict(zip((x,y,z),curve)),simultaneous=True)));speed=p.on_interval(p.speed(curve),bounds);return F,curve,bounds,pull,speed,s.simplify(pull*speed)
def integral(raw):
 raw=raw.strip().rstrip('.,').strip('$').rstrip('.,').replace(r'\cdot \text{d}',r'\text{d}').replace(r'\cdot\text{d}',r'\text{d}')
 m=re.fullmatch(r'(-?\d+)\\left\((.*)\\right\)',raw,re.S)
 if m:
  a,b,fn,var=integral(m[2]);return a,b,s.Integer(m[1])*fn,var
 return e.integral(raw)
def num(fn,bounds):
 mp.mp.dps=40;f=s.lambdify(t,fn,'mpmath');a,b=[mp.mpf(str(s.N(v,40))) for v in bounds];return mp.quad(f,[a,(a+b)/2,b])
def check(rec,C):
 q=rec['question'];F,curve,bounds,pull,speed,I=prompt(q);G=groups(q[':question/worked-solution']);assert len(G)==3;d=tuple(s.diff(c,t) for c in curve);nd=len(curve);assert re.sub('mathrm','text',right(G[0][0])).count(r'\frac{\text{d}')==nd
 op=right(G[0][1]);ops=[]
 for match in re.finditer(r'\\frac\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}t\}\(',op):
  st=match.end();dep=1;j=st
  while dep:dep+=(op[j]=='(')-(op[j]==')');j+=1
  ops.append(scalar(op[st:j-1]))
 assert len(ops)==nd and all(equal(a,b) for a,b in zip(ops,curve));C['formal_components']+=nd;actual=p.vector(right(G[0][2]));assert all(equal(a,b) for a,b in zip(actual,d+(s.Integer(0),)*(3-nd)));C['derivative_components']+=nd
 assert re.sub('mathrm','text',right(G[0][3])).count(r'\frac{\text{d}')==nd
 for row in G[0][4:]:assert equal(scalar(right(row)),speed,bounds),(right(row),speed);C['speed_rows']+=1
 for row in G[1]:assert equal(scalar(right(row)),pull,bounds);C['pullback_rows']+=1
 for row in G[2][1:]:
  aa,bb,fn,var=integral(right(row));assert var==t and equal(aa,bounds[0]) and equal(bb,bounds[1]) and equal(fn,I,bounds),(right(row),fn,I);C['integral_rows']+=1
 family=rec['generation']['template'];forms={'parabola':x/(4*y+1),'difference':s.sqrt(2)*(x-y),'squares':2*x-y**2-z**2,'quadratic3':x+y-z,'helix':z*(x*x-y*y),'linear_cubic':x**3-y,'hard_product_square':x*y-z**2};m=s.cancel(F/forms[family]);assert not m.free_symbols and m!=0 and equal(m,s.sympify(rec['generation']['parameters']['m']))
 if family=='parabola':wrong=m*curve[0]**2/(4*curve[1]+1)
 elif family=='difference':wrong=m*s.sqrt(2)*(curve[0]+curve[1])
 elif family=='squares':wrong=m*(2*curve[0]+curve[1]**2+curve[2]**2)
 elif family=='quadratic3':wrong=m*sum(curve)
 elif family=='helix':wrong=m*curve[2]*(curve[0]**2+curve[1]**2)
 elif family=='linear_cubic':wrong=m*(curve[0]**3+curve[1])
 else:wrong=m*(curve[0]*curve[1]+curve[2]**2)
 expected=[I,pull,pull*speed**2,pull/speed,wrong*speed];f=q[':question/answer-fields'][0];values=[]
 for a in f[':answer-field/choices']:
  aa,bb,fn,var=integral(a[':answer/value']);assert var==t and equal(aa,bounds[0]) and equal(bb,bounds[1]);values.append(fn)
 assert len(values)==5 and all(sum(equal(v,w,bounds) for v in values)==1 for w in expected);assert next(a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if equal(v,I,bounds))==f[':answer-field/correct'][1]
 nv=[num(v,bounds) for v in values];assert all(abs(a-b)>mp.mpf('1e-20') for i,a in enumerate(nv) for b in nv[:i]);C['full_value_quadratures']+=5;C['unequal_complete_value_pairs']+=10;C['choices']+=5;C['banks']+=1;C['records']+=1
 return [len(g) for g in G]
if __name__=='__main__':
 g=base.load(D.with_suffix('.py'),'scalar_setup_generator');source=base.raw(g,K,D);C={k:0 for k in ('records','formal_components','derivative_components','speed_rows','pullback_rows','integral_rows','full_value_quadratures','unequal_complete_value_pairs','choices','banks')};records=json.loads((R/f'qa/{K}-sampled.json').read_text());families={}
 for fam,(level,*_) in g.FAMILIES.items():records.append(g.generate(level,template=fam,seed=233))
 for r in records:
  roles=check(r,C);fam=r['generation']['template'];assert fam not in families or families[fam]==roles;families[fam]=roles
 out=dict(status='passed',source=source,readback=C,source_family_stage_counts=families,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
