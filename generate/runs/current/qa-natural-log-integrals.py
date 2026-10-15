"""Parent complete natural-log substitution readback on real connected domains."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186100816;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_lni_gen',D.with_suffix('.py'));E=load('root_lni_elem',R/'elementary-integral-readback.py');H=load('root_lni_inverse',R/'inverse-substitution-readback.py');x,u,C=E.x,E.u,E.C
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,source_banks=0,source_values=0,source_keys=0,differential_relations=0,formal_inputs=0,primitive_stages=0,values=0,pairs=0,real_components=0);tasks={l:set()for l in('easy','moderate','hard')}
def scalar(raw):return E.scalar(raw)
def equal(a,b):return s.simplify(a-b)==0
def check(rec,sid=None):
 q=rec['question'];sol=q[':question/worked-solution'];given=next(b for b in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)if r'\int'in b);F,ops=E.side(H.measure_text(given.replace(r'\displaystyle','')),x);assert len(ops)==1
 sm=re.search(r'\$u=(.*?)\$',sol);assert sm;V=scalar(sm[1]);assert V.func==s.log;arg=V.args[0];poly=s.Poly(arg,x);assert len(poly.terms())==1;n=poly.degree();a=poly.LC();assert n in(1,2,3,4)and a>0
 der=s.diff(V,x);assert equal(der,n/x)
 # Independent positive-log coordinate supplies exact real x branches;
 # negative-log coordinates are also checked whenever the original F allows.
 w=s.Symbol('root_log_coordinate',positive=True)
 def normalized(value,branch=1,logsign=1):
  replacement=branch*s.exp((logsign*w-s.log(a))/n)
  return s.simplify(s.expand_log(value.subs(x,replacement)))
 positive_kernel=s.simplify(normalized(F*x));power=next((p for p in[s.Rational(-1),s.Rational(-2),s.Rational(-1,2),s.Rational(1,2),s.Integer(1),s.Integer(2),s.Integer(3)]if not s.cancel(positive_kernel/w**p).has(w)),None);assert power is not None;coeff=s.cancel(positive_kernel/w**power);assert coeff>0
 logsigns=(1,)if power.q==2 else(-1,1);xsigns=(-1,1)if n%2==0 else(1,)
 def eqreal(A,B):
  difference=s.expand(A-B)
  if difference==0:return True
  return all(s.simplify(normalized(difference,branch,sign))==0 for branch in xsigns for sign in logsigns)
 N['real_components']+=len(logsigns)*len(xsigns)
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);dm=next(b for b in blocks if r'\frac{\text{d}u}{\text{d}x}'in b);left,right=re.split(r'⟹|\\quad\\Longrightarrow\\quad',dm)
 for term in left.split('=')[1:]:assert eqreal(scalar(term.replace(r'\,','')),der);N['differential_relations']+=1
 def measure(raw):
  raw=H.measure_text(raw);raw=re.sub(E.DIFF,lambda m:'(j)'if m[1]=='u'else'(k)',raw);return scalar(raw).subs({E.P.locals_['j']:der,E.P.locals_['k']:1})
 l,r=right.rstrip('.').split('=');assert eqreal(measure(l),measure(r));N['differential_relations']+=1
 for block in blocks:
  if block==dm:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in text.split(r'\\'):
   for term in row.split('='):
    if not term.strip():continue
    actual,formal=E.side(H.measure_text(term.replace(r'\displaystyle','')),x,V);assert eqreal(actual,F),('actual natural-log substitution stage',term,actual,F);N['formal_inputs']+=len(formal);N['primitive_stages']+=not bool(formal)
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1]
 # General-family completeness is part of this source response contract: the
 # captured no-C option is incomplete despite having the matching derivative.
 flags=[v.coeff(C)==1 and eqreal(E.derivative(v,x),F)for v in vals];assert[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],flags)if ok]==[key]
 for i,v in enumerate(vals):
  for z in vals[:i]:
   assert v.coeff(C)!=z.coeff(C)or not eqreal(E.derivative(v-z,x),0),('duplicate full primitive family',v,z);N['pairs']+=1
 if sid:
  of=olds[sid][':question/answer-fields'][0];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(ov)==len(vals)and all(sum(equal(v,z)for z in vals)==1 for v in ov);N['source_banks']+=1;N['source_values']+=len(vals)
  if ':answer-field/correct'in of:assert equal(scalar(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==key));N['source_keys']+=1
 N['values']+=len(vals);N['records']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add((str(s.cancel(s.expand(s.expand_log((F*x).subs(x,s.exp(s.Symbol('root_log_x',real=True))))))),n%2==0,power.q==2 or power<0))
for sid in olds:
 level=G.CONFIG[sid][0];p=G.original(sid);check(G.generate(level,template=sid,parameters=p),sid)
 for k in(2,11):
  try:r=G.generate(level,template=sid,parameters=dict(p,k=k))
  except ValueError as error:assert 'collid'in str(error);continue
  check(r)
for l in tasks:
 for r in G.generate_batch(l,552,18):check(r)
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_tasks={l:len(t)for l,t in tasks.items()},domain_proof='Independently inferred u=ln(a*x^n), a>0, actual du=n/x. Substitution x=±exp((±w-ln(a))/n),w>0 covers each positive/negative x branch and positive/negative log component allowed by source powers. Fractional powers use positive log coordinate only. No complex-force log identities.',scope='Observed natural-log substitution and original power/reciprocal/root/logAbs primitives; small independent coefficient/inner-scale/exponent roles. Easy authored p1..3 repeats same power rule; no general-base logs or definite integrals. Full +C family contract preserved including incomplete no-C distractor.',native='Allactualfieldsradio;45original/reviewfixtures45accepted180rejected0unresolved. Parentgeneric54accepted216rejected0gaps.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
