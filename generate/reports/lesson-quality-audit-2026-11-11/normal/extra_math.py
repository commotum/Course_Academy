import json,sys,subprocess,tempfile,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from math_tools import *
from generator_publish import Publisher
p=Publisher.from_environment();results=[]
for kp in [17592186092384,17592186092385]:
 D=H/str(kp);K=json.loads((D/'kp.json').read_text());path=p.config.math_root/K[':knowledge-point/question-generator'][':question-generator/script'];package=path.parent;manifest=json.loads((package/'generator-package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='normal-lesson-audit-extra-',dir='/tmp') as tmp:
  T=Path(tmp)
  for name in manifest['files']:shutil.copy2(package/name,T/name)
  for band in ['easy','moderate','hard']:
   for seed in [202611111,202611112]:
    if seed==202611111:rows=json.loads((D/'samples'/f'{band}.json').read_text())
    else:
     rows=json.loads(subprocess.check_output([sys.executable,str(T/'generator.py'),'--difficulty',band,'--count','20','--seed',str(seed)],cwd=T));(D/'samples'/f'{band}-seed-{seed}.json').write_text(json.dumps(rows,indent=2)+'\n')
    for r in rows:
     q=r['question'];f,x,y,m,n,b=extract(q)
     for field in q[':question/answer-fields']:
      expected=n if kp==17592186092384 else ([s.simplify(-b/n),s.Integer(0)] if '$x$-axis' in q[':question/problem'] else [s.Integer(0),b])[int(field[':answer-field/key'].split('-')[-1])-1]
      assert s.simplify(parse(key_value(field))-expected)==0
    results.append(dict(kp=kp,band=band,seed=seed,records=len(rows),all_displayed_functions_points_and_keys_checked=True))
# The independently authored hard anchor uses a named f definition; direct check.
K=json.loads((H/'17592186092385/kp.json').read_text());q=next(q for q in K[':knowledge-point/questions'] if q[':db/id']==17592186710708)
f=2*s.sqrt(X)-3*X+1;t=4;y=f.subs(X,t);m=s.diff(f,X).subs(X,t);n=-1/m;b=y-n*t;answer=s.simplify(-b/n);assert answer==s.Rational(43,2)
for field in q[':question/answer-fields']:
 expected=answer if field[':answer-field/key']=='field-1' else 0;assert s.simplify(parse(key_value(field))-expected)==0
ledger=json.loads((H/'stored-ledger.json').read_text())
for row in ledger:
 if row['entity']==17592186710708:row.update(math_status='passed',manual_independent_calculation='f(4)=-7; fprime(4)=-5/2; normal=2/5; y=2x/5-43/5; x-axis at43/2',reason='Named-function anchor independently checked explicitly')
(H/'stored-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
(H/'extra-math.json').write_text(json.dumps(dict(passed=True,samples=results,records=sum(r['records'] for r in results),manual_anchor=dict(entity=17592186710708,x_intercept=str(answer))),indent=2)+'\n');print('All240 ordinary raw samples and manual hard anchor passed independently')
