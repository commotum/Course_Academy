"""Root reconstructs actual Cartesian cylinder/heights/integrand and all substitutions."""
import json,re,sys,hashlib,importlib.util,functools
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186129267;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
b=load(R/'qa-parametric-scalar-line.py','cylinder_base');p=load(R/'polar-setup-readback.py','cylinder_parent');x,y,z,r,theta=p.p.x,p.p.y,p.p.z,p.R,p.T
math=p.scalar
def eq(a,b):return p.equal(s.sympify(a),s.sympify(b)) or s.refine(s.trigsimp(s.sympify(a)-s.sympify(b)),s.Q.nonnegative(r))==0

def integral(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','');raw=re.sub(r'\{\\int\s*\}',r'\\int',raw);starts=list(re.finditer(r'\\int\s*_',raw));assert len(starts)==3,raw;vals=[];ends=[]
 for m in starts:
  pos=m.end()
  while raw[pos].isspace():pos+=1
  lo,pos=p.group(raw,pos);assert raw[pos]=='^';hi,pos=p.group(raw,pos+1);vals.extend((math(lo),math(hi)));ends.append(pos)
 body=raw[ends[-1]:];m=re.search(r'\\,\s*dz',body);assert m;fn=math(body[:m.start()]);return (*vals,fn)

@functools.lru_cache(maxsize=10000)
def moment(n,m,a,b):return s.integrate(s.sin(theta)**n*s.cos(theta)**m,(theta,a,b))
@functools.lru_cache(maxsize=10000)
def value(obj):
 a,b,lo,hi,zlo,zhi,fn=obj;inner=s.integrate(fn,(z,zlo,zhi));U,V=s.symbols('root_sin root_cos');poly=s.Poly(s.expand(s.expand_trig(inner)).xreplace({s.sin(theta):U,s.cos(theta):V}),U,V);angular=sum(coeff*moment(n,m,a,b) for (n,m),coeff in poly.terms());assert not angular.has(theta,s.Integral)
 if angular.is_polynomial(r):return s.integrate(angular,(r,lo,hi))
 mp.mp.dps=30;f=s.lambdify(r,angular,'mpmath');aa,bb=[mp.mpf(str(s.N(w,30))) for w in (lo,hi)];return mp.quad(f,[aa,(aa+bb)/2,bb])
C={k:0 for k in ('records','actual_cylinder','actual_heights','actual_integrands','converted_height_rows','polar_stages','setup_stages','choice_integrals','whole_banks','full_value_pairs','geometry')}
def read(q):
 prompt=q[':question/problem'];S=math(re.search(r'(?:\{y\}\^\{2\}|y\^2|y\^\{2\})\s*=\s*(\d+)',prompt)[1]);hi=s.sqrt(S)
 body=next(bb for bb in p.p.blocks(prompt) if '{∭}_{R}' in bb or r'\iiint_R' in bb);body=re.sub(r'^(?:\{∭\}_\{R\}|\\iiint_R)\s*','',body);fragment=re.split(r'\\(?:,|mathrm|text)',body)[0].strip();F=math(fragment) if fragment else s.Integer(1)
 heights=re.findall(r'\$z\s*=\s*(.*?)\$',prompt);assert len(heights)==2;lower,upper=[math(w.rstrip('.,')) for w in heights];sub={x:r*s.cos(theta),y:r*s.sin(theta)};zlo,zhi=[s.refine(s.trigsimp(w.subs(sub,simultaneous=True)),s.Q.nonnegative(r)) for w in (lower,upper)];pol=s.refine(s.trigsimp(F.subs(sub,simultaneous=True)*r),s.Q.nonnegative(r))
 if r'x\le 0' in prompt:aa,bb=(s.pi/2,s.pi) if r'y\ge 0' in prompt else (s.pi/2,3*s.pi/2)
 elif r'x\ge 0' in prompt:aa,bb=-s.pi/2,s.pi/2
 elif r'y\ge 0' in prompt:aa,bb=0,s.pi
 else:aa,bb=0,2*s.pi
 return (aa,bb,s.Integer(0),hi,zlo,zhi,pol),F,S

def check(rec):
 q=rec['question'];wanted,F,S=read(q);C['actual_cylinder']+=1;C['actual_heights']+=2;C['actual_integrands']+=1;sol=q[':question/worked-solution'];aa,bb,_,hi,zlo,zhi,pol=wanted
 image=Path(re.search(r'!\[\]\((.*?)\)',sol)[1]);side=json.loads(image.with_suffix('.json').read_text());assert side['equal_scale'] is True and side['S']==S and tuple(s.sympify(t) for t in side['theta'])==(aa,bb);assert image.exists();C['geometry']+=1
 heightrows=re.findall(r'bounded (?:below|above) by \$z=(.*?)\$',sol);assert len(heightrows)==2
 for raw,expected in zip(heightrows,(zlo,zhi)):
  parts=raw.rstrip('.,').split('=',1);lhs=parts[0];rhs=parts[-1];assert eq(math(lhs).subs({x:r*s.cos(theta),y:r*s.sin(theta)},simultaneous=True),math(rhs)) and eq(math(rhs),expected);C['converted_height_rows']+=1
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);chain=groups[-1];assert 'Therefore, using the change of variables formula, we obtain' in sol
 fam=rec['generation']['template'];rows=chain.split(chr(92)*2);expected_rows={'full_cone_radial':3,'full_sphere_inverse':2,'full_z2radial':3,'full_zradial':3,'half_difference':4,'half_xz':3,'half_zdifference':4,'quarter_sphere_volume':1,'quarter_zdifference':5};assert len(rows)==expected_rows[fam]
 if fam in ('full_cone_radial','full_z2radial','full_zradial'):assert 'sqrt' in rows[0] and 'cos' in rows[0] and 'sin' in rows[0] and 'cos' in rows[1] and 'sin' in rows[1]
 if fam in ('half_difference','half_zdifference','quarter_zdifference'):assert 'cos' in rows[0] and 'sin' in rows[0] and 'cos' in rows[1] and 'sin' in rows[1] and 'cos' in rows[2] and 'sin' in rows[2]

 for row in chain.split(chr(92)*2):
  if '=' not in row:continue
  lhs,rhs=row.replace('&','').split('=',1)
  if '{∭}_{R}' in lhs or r'\iiint_R' in lhs:
   actual=re.sub(r'^(?:\{∭\}_\{R\}|\\iiint_R)\s*','',lhs);actual=re.split(r'\\(?:,|mathrm|text)',actual)[0].strip();assert eq(math(actual) if actual else 1,F)
  if '{∭}_{Δ}' in rhs or r'\iiint_\Delta' in rhs:
   fn=re.sub(r'^\s*(?:\{∭\}_\{Δ\}|\\iiint_\\Delta)\s*','',rhs);fn=re.split(r'\\,?dz|dz',fn)[0].rstrip(' '+chr(92)+',');assert eq(math(fn),pol),(fn,pol);C['polar_stages']+=1
  elif r'\int' in rhs:
   assert all(eq(a,b) for a,b in zip(integral(rhs),wanted));C['setup_stages']+=1
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];objects=[integral(a[':answer/value']) for a in f[':answer-field/choices']];assert len(objects)==5;correct=[a[':answer/id'] for a,obj in zip(f[':answer-field/choices'],objects) if all(eq(u,v) for u,v in zip(obj,wanted))];assert correct==[f[':answer-field/correct'][1]]
 vals=[value(obj) for obj in objects];nums=[complex(s.N(t,22)) if isinstance(t,s.Basic) else complex(t) for t in vals];assert all(abs(t.imag)<1e-18 for t in nums);assert all(abs(u-v)>1e-12*max(1,abs(u),abs(v)) for i,u in enumerate(nums) for v in nums[:i]);C['choice_integrals']+=5;C['whole_banks']+=1;C['full_value_pairs']+=10;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_cylinder_gen');source=b.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,(lev,sid,params) in g.TEMPLATES.items():records.append(g.generate(lev,template=fam,seed=937))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
