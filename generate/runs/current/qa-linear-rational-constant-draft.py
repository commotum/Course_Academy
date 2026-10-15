"""Root source-function fidelity and complete signed substitution/C-K chains."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ID=17592186064207;D=R.parents[2]/f'generate/scratch/{ID}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_linearK_gen',D.with_suffix('.py'));P=load('root_linearK_math',R/'elementary-integral-readback.py');x,u,C=P.x,P.u,P.C;K=s.Symbol('root_positive_K',positive=True);k=P.P.locals_['k'];oldscalar=P.scalar
def scalar(t):
 t=re.sub(r'\\text\{\s*\}', '',t);return s.expand_log(oldscalar(re.sub(r'(?<![A-Za-z\\])K(?![A-Za-z])','k',t)).subs(k,K))
P.scalar=scalar
# Independent root normalization of log|rational| into exact pole factors.
def normalize(expr):
 def logabs(q):
  numerator,denominator=s.fraction(s.cancel(q));v=s.Integer(0)
  for poly,sign in[(numerator,1),(denominator,-1)]:
   coef,fac=s.factor_list(poly,x);v+=sign*s.log(s.Abs(coef))
   for f,n in fac:
    assert s.degree(f,x)==1;a=f.coeff(x);root=-f.subs(x,0)/a;v+=sign*n*(s.log(s.Abs(a))+s.Function('root_logabs')(x-root))
  return v
 def positive_log(arg):
  if arg.func==s.Abs:return logabs(arg.args[0])
  if arg.is_Mul:return sum(positive_log(z)for z in arg.args)
  if arg.is_Pow:
   base,power=arg.args;assert power.is_Rational;return power*positive_log(base)
  assert not arg.has(x)and(arg==K or arg.is_positive is True),('unqualified real log domain',arg)
  return s.log(arg)
 return s.expand(s.expand_log(expr.xreplace({node:positive_log(node.args[0])for node in expr.atoms(s.log)})))

source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{ID}.json'));olds={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in source['record'][':knowledge-point/questions']};N=dict(MA_raw=0,independent_raw=0,MA_banks=0,MA_values=0,independent_banks=0,independent_values=0,source_keys=0,source_solutions=0,records=0,differential_relations=0,formal_integrals=0,primitive_stages=0,constant_equalities=0,values=0,pairs=0,real_components=0);tasks={l:set()for l in G.LEVELS}
for sid,o in olds.items():
 assert G.source_case(sid)['raw']==o;isMA=':question/math-academy-id'in o;N['MA_raw'if isMA else'independent_raw']+=1;p=G.ANCHORS[sid]['parameters'];prompt,sol=G.render(sid,p);assert prompt==G.fmt.normalize_prose(o[':question/problem']);assert sol==G.fmt.normalize_prose(o.get(':question/worked-solution',''));N['source_solutions']+=':question/worked-solution'in o
 for f in o.get(':question/answer-fields',[]):
  original=[normalize(scalar(a[':answer/value']))for a in f[':answer-field/choices']];recipes=[normalize(scalar(G.recipe(r,p)))for r in G.ANCHORS[sid]['recipes']];assert len(original)==len(recipes)and all(sum(s.simplify(v-w)==0 for w in recipes)==1 for v in original);N['MA_banks'if isMA else'independent_banks']+=1;N['MA_values'if isMA else'independent_values']+=len(original)
  if ':answer-field/correct'in f:assert sum(s.simplify(normalize(scalar(f[':answer-field/correct'][':answer/value']))-v)==0 for v in recipes)==1;N['source_keys']+=1
assert G.source_case('q-113533')['public_replay_eligible']is False
# Explicitly prove why original q113533 cannot be served as an unambiguous bank.
amb=olds['q-113533'];F,_=P.prompt(amb[':question/problem']);ambds=[s.cancel(P.derivative(scalar(z[':answer/value']),x))for z in amb[':question/answer-fields'][0][':answer-field/choices']];assert sum(s.cancel(v-F)==0 for v in ambds)==2

def check(r):
 q,m=r['question'],r['generation'];F,var=P.prompt(q[':question/problem']);assert var==x;sol=q[':question/worked-solution'];given=re.search(r'First, let \$u=(.*?)\$',sol);assert given;inner=scalar(given[1]);a=s.diff(inner,x);assert a!=0 and s.Poly(inner,x).degree()==1;n=s.cancel(F*inner);assert n.is_Rational and n!=0;alpha=n/a;mapping=alpha*s.log(K);prose=re.search(r'writing \$C\s*=\s*(.*?)\$',sol);assert prose and s.simplify(normalize(scalar(prose[1]))-normalize(mapping))==0
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==4;actual=blocks[0].split('⟹');assert len(actual)==2;first=actual[0].split('=')[1].replace(r'\,','').strip();assert scalar(first)==a;inv=actual[1].split('=')[1].replace(r'\text{d}u','').replace(r'\,','').strip().rstrip('.');inverse=s.Integer(1)if inv==''else-s.Integer(1)if inv=='-'else scalar(inv);assert inverse*a==1;N['differential_relations']+=2
 target=alpha*s.log(K*s.Abs(inner))
 for b in blocks[1:]:
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    value,ops=P.side(part,x,inner);assert s.cancel(value-F)==0,('printed integral/primitive',part,F,value)
    if ops:N['formal_integrals']+=len(ops)
    else:
     expr=scalar(part).subs(u,inner).subs(C,mapping);assert s.simplify(normalize(expr)-normalize(target))==0,('C to K stage',part);N['primitive_stages']+=1;N['constant_equalities']+=1
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value'])for z in f[':answer-field/choices']];ds=[s.cancel(P.derivative(z,x))for z in values];assert len(values)==5 and[z[':answer/id']for z,d in zip(f[':answer-field/choices'],ds)if s.cancel(d-F)==0]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for v in ds[:i]:assert s.cancel(d-v)!=0;N['pairs']+=1
 pole=s.solve(inner,x);assert len(pole)==1 and list(map(str,pole))==m['domain']['excluded_poles'];N['real_components']+=2;N['records']+=1;N['values']+=len(values);tasks[q[':question/difficulty'].split('/')[-1]].add(str(s.cancel(F)))
for r in json.load(open(D/'review-cases.json')):check(r)
for l in G.LEVELS:
 for seed in range(24):check(G.generate(l,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_integrands={l:len(t)for l,t in tasks.items()},scope='Observed single reciprocal-linear substitution, C reparameterization and single-log method; authored missing hard varies numerator and signed slope arithmetic only, retaining all operative stages. No combined integral or new substitution skill.',source_exception='q113533 has two derivative-correct positive-K equivalent answers and remains exact raw ineligible; repair is explicitly separate. Missing key/solution/field evidence exact, authored completions separate.',constant_proof='C=(n/a)ln K actual prose and every row equality verified at K>0, n/a nonzero; bijection on both real connected intervals excluding printed pole. No forced sign log laws.',database_writes=0);(R/f'qa/{ID}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
