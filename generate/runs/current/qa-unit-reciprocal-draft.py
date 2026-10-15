"""Root reciprocal c/x, real log-absolute, source repair and private-dependency audit."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186105715;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_unit_recip_gen',D.with_suffix('.py'));P=load('root_unit_recip_math',R/'elementary-integral-readback.py');x=P.x
assert Path(G._fmt_spec.origin).resolve()==(D/'math_format.py').resolve() if hasattr(G,'_fmt_spec')else 'sys.path.insert'not in D.with_suffix('.py').read_text()
N=dict(records=0,integral_sides=0,primitive_sides=0,formal_inputs=0,inline_equalities=0,values=0,pairs=0,banks=0,negative_branch_keys=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(raw_banks=0,raw_values=0,existing_keys=0,source_solutions=0,unaltered_banks=0,repaired_banks=0,preserved_values=0)
cases=json.load(open(D/'source-cases.json'))['questions']
for c in cases:
 o=olds[c['source_id']];raw=G.generate('easy',template=c['template'],parameters=c['parameters'],profile='raw')['question'];served=G.generate('easy',template=c['template'],parameters=c['parameters'])['question'];assert raw[':question/problem']==G.clean(o[':question/problem'])and served[':question/problem']==raw[':question/problem'];of=o[':question/answer-fields'][0];rf=raw[':question/answer-fields'][0];sf=served[':question/answer-fields'][0]
 assert sorted(a[':answer/value']for a in rf[':answer-field/choices'])==sorted(G.clean(a[':answer/value'],True)for a in of[':answer-field/choices']);fidelity['raw_banks']+=1;fidelity['raw_values']+=len(rf[':answer-field/choices']);original={a[':answer/value']for a in rf[':answer-field/choices']};ordinary={a[':answer/value']for a in sf[':answer-field/choices']};n=len(original&ordinary);assert n==(4 if c['source_id']in G.REPAIRS else 5);fidelity['preserved_values']+=n;fidelity['repaired_banks']+=n==4;fidelity['unaltered_banks']+=n==5
 if ':question/worked-solution'in o:assert raw[':question/worked-solution']==served[':question/worked-solution']==G.clean(o[':question/worked-solution']);fidelity['source_solutions']+=1
 else:assert ':question/worked-solution'not in raw and ':question/difficulty'not in raw and ':answer-field/correct'not in rf
 if ':answer-field/correct'in of:
  assert next(a[':answer/value']for a in rf[':answer-field/choices']if a[':answer/id']==rf[':answer-field/correct'][1])==G.clean(of[':answer-field/correct'][':answer/value'],True);fidelity['existing_keys']+=1
seen={level:set()for level in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];F,var=P.prompt(q[':question/problem']);assert var==x;c=s.cancel(F*x);assert not c.has(x)and c!=0
 level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':assert c.is_Rational and c<0 and c.q!=1
 if level=='hard':assert c.is_irrational and c<0 and s.simplify(c*c).is_Rational
 for key,value in P.stages(q[':question/worked-solution'],F,x).items():N[key]+=value
 for block in re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',q[':question/worked-solution']):
  if '='not in block:continue
  values=[P.scalar(t)for t in block.split('=')];assert all(P.eq(v,c)for v in values),('incorrect displayed coefficient rationalization',m,block,c);N['inline_equalities']+=len(values)-1
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio')and len(f[':answer-field/choices'])==5;values=[P.derivative(P.scalar(a[':answer/value']),x)for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if P.eq(v,F)];assert hits==[f[':answer-field/correct'][1]],(m,hits,F,values)
 canonical=next(v for a,v in zip(f[':answer-field/choices'],values)if a[':answer/id']==f[':answer-field/correct'][1]);assert P.eq(canonical.subs(x,-2),F.subs(x,-2));N['negative_branch_keys']+=1
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.eq(v,w),('duplicate ordinary primitive family',m);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1;seen[level].add(s.srepr(s.simplify(c)))
for i,entry in enumerate(json.load(open(D/'engine-input.json'))):
 check(entry['record'])
 if i%100==0:print('Root unit reciprocal records read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 assert len(seen[level])=={'easy':114,'moderate':107,'hard':80}[level]
 batch=G.batch(level,count=len(seen[level]),seed=37);assert len({r['generation']['mathematical_fingerprint']for r in batch})==len(seen[level])
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
