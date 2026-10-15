"""Root nonlinear power substitution: actual stages, complete original banks, real branch."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068723;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_constant_power_gen',D.with_suffix('.py'));P=load('root_constant_power_math',R/'elementary-integral-readback.py');x,u=P.x,P.u;W=s.Symbol('W',positive=True)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for sid,o in olds.items():
 assert G.source_record(sid)==o;t=G.PROFILES[sid];q=G.generate(t['difficulty'],template='source:'+sid,parameters={'b':t['b']})['question'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert q[':question/problem']==o[':question/problem'];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
@lru_cache(maxsize=40000)
def eq(a,b,U,positive):
 delta=a-b
 if delta==0:return True
 # One exact algebraic witness inside the declared interval proves inequality.
 for point in (s.Rational(1,2),s.Rational(-1,2),s.Integer(5),s.Integer(-5)):
  if positive and U.subs(x,point).is_positive is not True:continue
  witness=delta.subs(x,point)
  if witness.is_zero is False and witness.is_finite is True:return False
 if positive:delta=delta.subs(U,W)
 return s.cancel(delta)==0 or s.simplify(delta)==0
N=dict(records=0,substitutions=0,differentials=0,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0,evidence_only=0);seen={l:set()for l in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];sol=q[':question/worked-solution'];F,var=P.prompt(q[':question/problem']);assert var==x;blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);ub=next(b.strip()for b in blocks if re.match(r'\s*u=',b));U=P.scalar(ub.split('=',1)[1]);v=s.diff(U,x);assert v!=0;positive=m['domain']['constraint']!='all real x'
 eqv=lambda a,b:eq(a,b,U,positive)
 db=next(b for b in blocks if '⟹'in b);db=re.sub(r'\\(?:begin|end)\{aligned\}','',db).replace('&','');left,right=db.split('⟹');assert P.clean(left.split('=',1)[0])==r'\frac{\text{d}u}{\text{d}x}'and eqv(P.scalar(left.split('=',1)[1]),v);ll,rr=right.strip().rstrip('.,').split('=');lm=re.fullmatch('(.*?)'+P.DIFF,ll.strip());rm=re.fullmatch('(.*?)'+P.DIFF,rr.strip());assert lm and rm and{lm[2],rm[2]}=={'x','u'}
 co=lambda m:P.scalar(m[1])if P.clean(m[1])else s.Integer(1)
 assert eqv(co(lm)*(v if lm[2]=='u'else 1),co(rm)*(v if rm[2]=='u'else 1));N['differentials']+=2;N['substitutions']+=1
 for b in blocks:
  if r'\int'not in b:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    value,inputs=P.side(part,x,U);assert eqv(value,F),('actual substitution/power stage',m['template'],m['parameters'],part,value,F);N['integral_sides'if inputs else'primitive_sides']+=1;N['formal_inputs']+=len(inputs)
 f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];ds=[P.derivative(a,x)for a in vals];assert [a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if eqv(d,F)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not eqv(d,e);N['pairs']+=1
 assert m['evidence_only']==(not m['eligible_for_learning']);N['evidence_only']+=m['evidence_only'];N['records']+=1;N['values']+=len(vals)
 if not m['evidence_only']:seen[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.expand(F)))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%100==0:print('Root constant-power actual stages read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},branch_proof='Fractional powers on explicitly positive actual inner polynomial: substitute that whole parsed polynomial with positive W; no forced power identities. Integer-power comparisons rational/polynomial identities on real line.',native_scope='929owned correct IDs accepted3716owned wrong IDs rejected. Separate valid-primitive blank diagnostic limitations stay documented; no blank normal output.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
