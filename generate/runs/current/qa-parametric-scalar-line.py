"""Root actual parametric scalar pullbacks, speeds, substitutions and banks."""
import json,re,sys,hashlib,importlib.util
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
p=load(R/'arc-vector-parser.py','root_param_scalar');e=load(R/'arc-evaluation-parser.py','root_param_eval');t,u,x,y,z=[p.p.locals_[k] for k in ('t','u','x','y','z')]
def scalar(raw):
 raw=raw.replace(r'\qquad',r'\,').replace(r'\dfrac',r'\frac')
 while re.search(r'\\sqrt\[(\d+)\]',raw):
  m=re.search(r'\\sqrt\[(\d+)\]',raw);v,end=p.group(raw,m.end());raw=raw[:m.start()]+'('+v+')^{\\frac{1}{'+m[1]+'}}'+raw[end:]
 return p.math(raw)
e.p.math=scalar
def equal(a,b,bounds=None):
 if bounds and bounds[0]>=0 and bounds[1]<=s.pi/2:
  a,b=[p.on_interval(s.sympify(q),bounds).xreplace({s.Abs(s.cos(t)):s.cos(t)}) for q in (a,b)]
 return p.same_on(a,b,bounds) if bounds else p.same(a,b)
def read(q):
 text=q[':question/problem'];fraw=re.search(r'\$f\([^$]*?\)=(.*?)\$',text)[1];F=scalar(fraw);v=re.search(r'r\(t\)=\\langle\s*(.*?)\\rangle',text)[1];curve=tuple(scalar(c) for c in v.split(','));ab=re.search(r't\\in \[(.*?),(.*?)\]',text);bounds=(scalar(ab[1]),scalar(ab[2]));assert bounds[1]>bounds[0]
 pull=s.simplify(F.subs(dict(zip((x,y,z),curve)),simultaneous=True));speed=p.on_interval(p.speed(curve),bounds)
 # cos remains nonnegative on all source-shaped sine-line intervals.
 for a in speed.atoms(s.Abs):
  if a.args[0]==s.cos(t) and bounds[0]>=0 and bounds[1]<=s.pi/2:speed=speed.xreplace({a:s.cos(t)})
 return F,curve,bounds,pull,speed,s.simplify(pull*speed)
def groups(sol):return [v.split(chr(92)*2) for v in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)]
def right(row):return row.split('=',1)[1].replace('&','').strip().rstrip('.,')
def raw(g,K,D):
 olds={q[':question/math-academy-id']:q for q in json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions']};C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_keys=0,missing_ratings=0)
 for case in json.loads((D/'source-cases.json').read_text()):
  o=olds[case['source_id']];lev=o.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or case.get('level',case.get('difficulty','moderate'));q=g.generate(lev,template=case['template'],parameters=case['parameters'],profile=case.get('profile',case.get('bank_profile')))['question']
  for k in (':question/problem',':question/worked-solution',':question/answer-fields',':question/difficulty'):assert (k in o)==(k in q)
  assert q[':question/problem']==o[':question/problem'];C['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
  else:C['missing_ratings']+=1
  assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==f0[':answer-field/key'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f0:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
   else:C['missing_keys']+=1
 return C
def check827(rec,C):
 q=rec['question'];F,curve,bounds,pull,speed,integrand=read(q);sol=q[':question/worked-solution'];G=groups(sol);assert len(G)==5
 derivatives=[s.diff(v,t) for v in curve];assert right(G[1][0]).count(r'\frac{\text{d}')==len(curve)
 ops=[]
 for m in re.finditer(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\(',right(G[1][1])):
  st=m.end();dep=1;j=st
  while dep:dep+=(right(G[1][1])[j]=='(')-(right(G[1][1])[j]==')');j+=1
  ops.append(scalar(right(G[1][1])[st:j-1]))
 assert len(ops)==len(curve) and all(equal(a,b) for a,b in zip(ops,curve));C['formal_components']+=len(curve)
 actual=p.vector(right(G[1][2]));assert all(equal(a,b) for a,b in zip(actual,derivatives+[s.Integer(0)]*(3-len(curve))));C['derivative_components']+=len(curve)
 assert right(G[1][3]).count(r'\frac{\text{d}')==len(curve)
 for row in G[1][4:]:assert equal(scalar(right(row)),speed,bounds),(right(row),speed,bounds);C['speed_rows']+=1
 for row in G[2]:assert equal(scalar(right(row)),pull,bounds);C['pullback_rows']+=1
 for row in G[3][1:]:a,b,fn,var=e.integral(right(row));assert var==t and equal(a,bounds[0]) and equal(b,bounds[1]) and equal(fn,integrand,bounds);C['setup_rows']+=1
 sub=e.substitution(sol);assert sub is not None;A,B=[s.simplify(sub.subs(t,v)) for v in bounds];C['substitutions']+=1
 value=None;primitive=None;transformed=None
 for row in G[4]:
  text=right(row)
  if r'\int' in text:
   a,b,fn,var=e.integral(text);assert var==u and equal(a,A) and equal(b,B) and equal(fn.subs(u,sub)*s.diff(sub,t),integrand,bounds);transformed=fn;C['transformed_rows']+=1
  elif '|' in text:
   primitive,var,a,b,value=e.evaluated(text);assert var==u and equal(a,A) and equal(b,B) and equal(s.diff(primitive,u),transformed);C['primitive_rows']+=1
  else:assert value is not None and equal(scalar(text),value);C['endpoint_rows']+=1
 assert value is not None and primitive is not None
 # Separate both endpoint operands in the explicit evaluated subtraction.
 text=right(G[4][-2]);assert text[0]=='(';depth=1;j=1
 while depth:depth+=(text[j]=='(')-(text[j]==')');j+=1
 assert text[j:j+2]=='-(';upper=scalar(text[1:j-1]);lower=scalar(text[j+2:-1]);assert equal(upper,primitive.subs(u,B)) and equal(lower,primitive.subs(u,A));C['individual_endpoint_components']+=2
 family=rec['generation']['template'];W=s.simplify(transformed/(s.cos(u) if family=='cos_diagonal' else u**2 if family=='sine_line' else s.sqrt(u)))
 if family=='cos_diagonal':
  aa=s.expand(curve[0]).coeff(t,2);bb=s.expand(curve[1]).coeff(t,2);kk=s.simplify(pull/s.cos(curve[0]));expected=[value,2*aa*value,W*(s.cos(B)-s.cos(A)),W*(s.sin(bounds[1])-s.sin(bounds[0])),kk*(aa+bb)/aa*(s.sin(B)-s.sin(A))]
 elif family=='sine_line':
  L=s.simplify(speed/s.cos(t));expected=[value,value/L,s.integrate(pull*speed**2,(t,*bounds)),W*(B**3-A**3),W*(B**2-A**2)/2]
 elif family=='sin_cos':
  ss=s.simplify(curve[1]/s.sin(t));expected=[value,s.integrate(pull,(t,*bounds)),s.integrate(s.expand_trig(pull*speed**2),(t,*bounds)),-2*ss**2*value,2*W*(s.sqrt(B)-s.sqrt(A))]
 else:expected=[value,value*s.expand(s.diff(sub,t)).coeff(t,3 if family=='cubic' else 1),2*W*(s.sqrt(B)-s.sqrt(A)),upper+lower,s.integrate(pull,(t,*bounds))]
 f=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(sum(equal(v,w) for v in vs)==1 for w in expected);assert next(a[':answer/id'] for a in f[':answer-field/choices'] if equal(scalar(a[':answer/value']),value))==f[':answer-field/correct'][1];C['choices']+=5;C['banks']+=1
 mp.mp.dps=35;fun=s.lambdify(t,integrand,'mpmath');a,b=[mp.mpf(str(s.N(v,35))) for v in bounds];numeric=mp.quad(fun,[a,(a+b)/2,b]);assert abs(numeric-mp.mpf(str(s.N(value,35))))<mp.mpf('1e-25');C['quadratures']+=1;C['records']+=1
if __name__=='__main__':
 K=int(sys.argv[1]);assert K==17592186133827;D=ROOT/f'generate/scratch/{K}';g=load(D.with_suffix('.py'),'root_scalar_gen');source=raw(g,K,D);C={k:0 for k in ('records','formal_components','derivative_components','speed_rows','pullback_rows','setup_rows','substitutions','transformed_rows','primitive_rows','endpoint_rows','individual_endpoint_components','choices','banks','quadratures')};records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,lev in g.LEVELS.items():records.append(g.generate(lev,template=fam,seed=370))
 for r in records:check827(r,C)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
