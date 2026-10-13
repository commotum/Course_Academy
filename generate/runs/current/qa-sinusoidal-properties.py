"""Root preserves unevaluated trig arguments while checking coefficients/stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');S=s.Function('SinusoidSine');K=s.Function('SinusoidCosine');p.functions.update(sin=S,cos=K)
def read(z,env=None):
 z=z.strip().strip('$').rstrip('.,?').replace('^{∘}','').replace(r'^\circ','').replace('°','').replace(r'\quad','').replace(r'\,','')
 z=re.sub(r'\|([^|]+)\|',r'Abs(\1)',z)
 z=z.replace('f(x)','y')
 for a,b in [('A','u'),('B','v'),('C','z'),('D','k')]:z=z.replace(a,b)
 # Protect the parser function name from the symbolic A substitution.
 z=z.replace('ubs','Abs')
 out=p.scalar(z)
 return out if env is None else out.subs({p.u:env['A'],p.v:env['B'],p.z:env['C'],p.k:env['D'],p.y:env['F']})
def physics(prompt):
 expr=re.search(r'\$(?:f\(x\)|y)\s*=\s*(.*?)\$',prompt)[1];F=read(expr);atoms=[v for v in F.atoms(s.Function) if v.func in (S,K)];assert len(atoms)==1
 trig=atoms[0];arg=trig.args[0];B=s.diff(arg,p.x);C=arg.subs(p.x,0);assert B!=0 and not B.has(p.x) and s.expand(arg-B*p.x-C)==0
 A=s.expand(F).coeff(trig);D=s.expand(F-A*trig);assert A!=0 and not D.has(p.x) and not A.has(p.x)
 return dict(F=F,A=A,B=B,C=C,D=D,trig=trig,expression=expr.rstrip('.,?'),degree='∘' in expr or '°' in expr)
def source(g,k):
 src=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());n=dict(questions=len(src),prompts=0,solutions=0,fields=0,values=0,keys=0)
 def norm(z):return z.get(':db/ident') if isinstance(z,dict) else z
 for c in cases:
  old=next(q for q in src if c['source_id'] in (q[':question/id'],q[':db/id'],q[':question/math-academy-id']));q=g.generate(c.get('level',c.get('authored_level','easy')),template=c['template'],profile=c['bank_profile'],parameters=c['parameters'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in old)==(key in q),(c,key)
   if key!=':question/answer-fields' and key in old:assert q[key]==norm(old[key]),(c,key)
  n['prompts']+=1;n['solutions']+=(':question/worked-solution' in old)
  for a,b in zip(old.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert a[':answer-field/key']==b[':answer-field/key'] and norm(a[':answer-field/type'])==b[':answer-field/type'];assert sorted((norm(v[':answer/type']),v[':answer/value']) for v in a[':answer-field/choices'])==sorted((v[':answer/type'],v[':answer/value']) for v in b[':answer-field/choices']);n['fields']+=1;n['values']+=len(a[':answer-field/choices'])
   assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   if ':answer-field/correct' in a:assert a[':answer-field/correct'][':answer/value']==next(v[':answer/value'] for v in b[':answer-field/choices'] if v[':answer/id']==b[':answer-field/correct'][1]);n['keys']+=1
 return n
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','g'+str(k));src=source(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());choices=equalities=0
 for r in records:
  q=r['question'];env=physics(q[':question/problem']);sol=q[':question/worked-solution'];A,B,C,D=(env[z] for z in ('A','B','C','D'));f=q[':question/answer-fields'][0];vals=[read(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(vals))==5
  target=abs(A) if k==17592186129121 else (360 if env['degree'] else 2*s.pi)/abs(B)
  for a,v in zip(f[':answer-field/choices'],vals):assert (v==target)==(a[':answer/id']==f[':answer-field/correct'][1]);choices+=1
  if k==17592186129122:
   base=360 if env['degree'] else 2*s.pi;expected=[target,base*abs(B),base/(2*abs(B)),2*base/abs(B),base];assert set(vals)==set(expected)
   if q[':question/difficulty'].endswith('/hard'):assert 'coefficient of $x$ in the argument' in sol
  else:
   profile=r['generation']['bank_profile']
   if profile=='coefficient_parameters':expected=[abs(A),1/abs(A),B,1/B,abs(A)*B]
   elif profile=='implicit_parameters':expected=[abs(A),B,1/B,abs(C),1/abs(C)]
   elif profile=='absolute_coefficient':expected=[abs(A),A,B,1/B,abs(C)]
   elif profile in ('numerator_division','signed_division'):
    N,Q=A.p,A.q;dn=D*Q;assert dn.is_Integer
    expected=[abs(A),abs(N),abs(dn/Q),abs(dn),s.Rational(1,Q)] if profile=='numerator_division' else [abs(A),abs(N),dn,Q,A]
   elif profile=='whole_numerator_scale':
    scale=s.Integer(re.match(r'(-?\d+)\\left\(',env['expression'])[1]);shift=s.Integer(re.search(r'\\right\)([+-]\d+)$',env['expression'])[1]);Q=A.q;N=A.p/scale;dn=(D-shift)*Q/scale;assert N.is_Integer and dn.is_Integer
    expected=[abs(A),abs(N/Q),abs(scale*N),abs(scale*dn/Q),abs(scale/Q)]
   else:raise AssertionError(profile)
   assert set(vals)==set(map(s.sympify,expected)),(profile,vals,expected)
  # All source-shaped generic rules, actual rewritten functions, coefficient
  # arithmetic and final absolute-value chains use the printed coefficient.
  for match in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
   block=next(z for z in match if z).replace(r'\begin{aligned}','').replace(r'\end{aligned}','');lhs=None
   for row in block.split(r'\\'):
    parts=row.replace('&','').split('=')
    if len(parts)<2:continue
    if not parts[0].strip():parts[0]=lhs
    else:lhs=parts[0]
    vs=[read(z,env) for z in parts]
    for z in vs[1:]:assert s.expand(vs[0]-z)==0,(k,row,vs);equalities+=1
 report=dict(status='passed',kp_id=k,source=src,normal_records=len(records),complete_choice_values=choices,actual_solution_equalities=equalities,unevaluated_trig_argument_readback=True,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
