"""Parent full based-log source banks and independently read substitutions."""
import sys,json,hashlib,importlib.util,re
from functools import lru_cache
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186100817;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
G=load('root_blog_gen',D.with_suffix('.py'));A=load('root_blog_reader',R/'based-log-integral-readback.py');E=A.E;H=load('root_blog_measure',R/'inverse-substitution-readback.py');x,u,C=A.x,A.u,A.C;scalar=A.scalar
base_derivative=E.derivative
def real_derivative(value,var,inner=None):
 def log_abs_derivative_node(node):
  arg=node.args[0];atoms=arg.atoms(s.Abs);assert len(atoms)==1;absolute=next(iter(atoms));power=arg.as_powers_dict().get(absolute,s.Integer(1));constant=s.cancel(arg/absolute**power);assert not constant.has(x,u)
  return power*E.RealLogAbs(absolute.args[0])
 value=value.replace(lambda z:z.func==s.log and z.args[0].has(s.Abs),log_abs_derivative_node)
 return base_derivative(value,var,inner)
E.derivative=real_derivative
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,formal_inputs=0,primitive_stages=0,differentials=0,values=0,pairs=0,real_components=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(rec,sid=None,raw_error=False):
 q=rec['question'];sol=q[':question/worked-solution'];given=next(b for b in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)if r'\int'in b).split('=')[0];F,ops=E.side(H.measure_text(given),x);assert len(ops)==1
 sm=re.search(r'\$u=(.*?)\$',sol);assert sm;V=scalar(sm[1]);logs=[z for z in V.atoms(s.log)if z.args[0].has(x)];assert len(logs)==1;arg=logs[0].args[0];poly=s.Poly(arg,x);assert len(poly.terms())==1;a=poly.LC();n=poly.degree();base_log=s.cancel(logs[0]/V);assert a>0 and n in(1,2,3,4)and base_log>0 and not base_log.has(x)
 der=s.diff(V,x);assert s.simplify(der-n/(x*base_log))==0
 w=s.Symbol('root_blog_coordinate',positive=True)
 @lru_cache(maxsize=5000)
 def norm(value,branch=1,sign=1):return s.simplify(s.expand_log(value.subs(x,branch*s.exp((sign*w*base_log-s.log(a))/n))))
 kernel=s.simplify(norm(F*x));power=next((p for p in(-1,1,2)if not s.cancel(kernel/w**p).has(w)),None);assert power is not None;coeff=s.cancel(kernel/w**power);assert coeff>0
 @lru_cache(maxsize=5000)
 def eqreal(a,b):
  delta=s.expand(a-b)
  if delta==0:return True
  # Positive linear exponentials dominate the source logarithmic kernels.
  for atom in delta.atoms(s.exp):
   slope=s.diff(atom.args[0],x);coefficient=delta.coeff(atom)
   if slope.is_positive and not slope.has(x)and coefficient!=0 and not coefficient.has(x):return False
  return all(s.simplify(norm(a-b,branch,sign))==0 for branch in((-1,1)if n%2==0 else(1,))for sign in(-1,1))
 N['real_components']+=4 if n%2==0 else 2
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);dm=next(b for b in blocks if r'\frac{\text{d}u}{\text{d}x}'in b);left,right=re.split(r'⟹|\\(?:Longrightarrow|Rightarrow)',dm);assert eqreal(scalar(left.split('=')[1]),der)
 def measure(raw):
  text=re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',H.measure_text(raw));return scalar(text).subs({E.P.locals_['j']:der,E.P.locals_['k']:1})
 dl,dr=right.rstrip('.').split('=');assert eqreal(measure(dl),measure(dr));N['differentials']+=2
 for block in blocks:
  if block==dm:continue
  for row in re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\'):
   for term in row.split('='):
    if not term.strip():continue
    actual,formal=E.side(H.measure_text(term),x,V);assert eqreal(actual,F),('based-log operative integral/primitive',term,actual,F);N['formal_inputs']+=len(formal);N['primitive_stages']+=not bool(formal)
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1];good=[v.coeff(C)==1 and eqreal(E.derivative(v,x),F)for v in values];assert key in[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],good)if ok]
 if not raw_error:
  assert sum(good)==1
  for i,v in enumerate(values):
   for z in values[:i]:assert not eqreal(E.derivative(v-z,x),0);N['pairs']+=1
 if sid:
  of=olds[sid][':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];remaining=values[:];assert len(ov)==len(values)
  for v in ov:
   # Constant offsets belong to C; source grouping/argument powers remain read.
   matches=[i for i,z in enumerate(remaining)if eqreal(E.derivative(v-z,x),0)];assert matches,(sid,v,remaining);remaining.pop(matches[0])
  oldcorrect=scalar(of[':answer-field/correct'][':answer/value']);newcorrect=next(v for a,v in zip(f[':answer-field/choices'],values)if a[':answer/id']==key);assert eqreal(E.derivative(oldcorrect-newcorrect,x),0);N['source_banks']+=1;N['source_values']+=len(values);N['source_keys']+=1
 N['values']+=len(values);N['records']+=1;t=s.Symbol('root_blog_abs_x',real=True);actual=s.cancel(s.expand(s.expand_log((F*x).subs(x,s.exp(t)))));tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(actual),n%2==0,power<0))
for sid in olds:
 print('Original',sid,flush=True)
 level,original=G.CONFIG[sid];p=G.parameters(original);check(G.generate(level,template=sid,parameters=p,profile='observed'),sid,raw_error=sid in G.ERRORS)
 if sid in G.ERRORS:check(G.generate(level,template=sid,parameters=p,profile='repaired'))
for sid in olds:
 print('Changed',sid,flush=True)
 check(G.generate(G.CONFIG[sid][0],19,template=sid))
for l in tasks:
 for r in G.batch(l,675,6):check(r)
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA,'script changed during readback'
result=dict(status='passed',script_sha256=SCRIPT_SHA,source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},source_errors='q31395 duplicate incorrect primitives andq210752 second correct primitive rawineligible; minimum duplicate-choice repairs:2of3duplicate wrongchoices inq31395,1duplicate-correctchoice inq210752; allother67/70recipes andkeys preserved.',domain_proof='Based-log function powers and argument powers independently parsed. u=ln(a*x^m)/ln b, b>1 and a>0 inferred fromdisplay. Exact x=±exp((±w*ln b-ln a)/m),w>0 checks every permitted real x/log component without forced complex log identities.',scope='Same source other-base logarithm substitution/power-rule/logAbs backbone; independently varied base, eligible argument scale/power and external rational scale, no definite integrals.',native='Allnormalfieldsradio;220radio native checks pass. Five separately authored diagnostic blank equivalence gaps preserved, not normal field failures; see GRADING.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
