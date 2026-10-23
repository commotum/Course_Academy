"""Independent old/new finite-batch regression. Run with job Python -B."""
import sys,json,pathlib,subprocess,collections,importlib.util
sys.dont_write_bytecode=True
import math_helper as v
R=v.R;W=v.W;PY=v.PY

def features(r):
 A,_=v.s.linear_eq_to_matrix(v.rows(r['question']),[v.x,v.y]);f=r['question'][':question/answer-fields'][0];opts=[v.expr(a[':answer/value'].split('=')[1]) for a in f[':answer-field/choices']];root=v.s.Rational(v.audit(r)['root']);sign='same_sign' if A[1,0]*A[0,1]/A[0,0]>0 else 'opposite_sign'
 return dict(question_id=r['question'][':question/id'],seed=r['generation']['seed'],template=r['generation']['template'],sign=sign,root=str(root),rank=sorted(opts).index(root),position=opts.index(root),sign_extremum=root==(max(opts) if sign=='same_sign' else min(opts)),coefficient_decision=str(A),bank_spacing=str(sorted(opts)[1]-sorted(opts)[0]))
def stats(pool):
 out=collections.defaultdict(list)
 for r in pool:
  f=features(r)
  for key in [f['template'],f['template']+':'+f['sign']]:out[key].append(f)
 return {key:dict(total=len(fs),roots=dict(collections.Counter(f['root'] for f in fs)),ranks=dict(collections.Counter(f['rank'] for f in fs)),positions=dict(collections.Counter(f['position'] for f in fs)),sign_extremum_successes=sum(f['sign_extremum'] for f in fs),distinct_coefficient_decisions=len(set(f['coefficient_decision'] for f in fs))) for key,fs in out.items()}
def contrast(pool):
 groups=stats(pool);return all(z['total']>=2 and len(z['roots'])>=2 and len(z['positions'])>=2 and set(z['ranks']) & {0,4} and set(z['ranks']) & {1,2,3} and z['sign_extremum_successes']<z['total'] for key,z in groups.items() if ':' in key)
if __name__=='__main__':
 commands=[]
 def cli(path,seed,count):
  cmd=[PY,'-B',str(path),'--difficulty','easy','--seed',str(seed),'--count',str(count),'--format','json'];p=subprocess.run(cmd,capture_output=True,text=True,cwd=R);commands.append(dict(command=cmd,exit=p.returncode,stderr=p.stderr));assert p.returncode==0;return json.loads(p.stdout)
 old=cli(R.parent/'review-1-policy-2-4ad31bffc4aded8a/relocated/17592186115242.py',1475864943,5);current=cli(W/'17592186115242.py',1475864943,5);fresh=cli(W/'17592186115242.py',822101,5);rel=cli(R/'relocated/17592186115242.py',822101,5)
 assert not contrast(old);assert contrast(current) and contrast(fresh);assert fresh==rel
 batch=json.load(open(R/'runner-batch.json'));assert current==batch
 exact=[v.g.generate('easy',seed=n) for n in [1475864945,1475864946]];assert stats(exact)['inconsistent_easy:opposite_sign']['sign_extremum_successes']==2
 for name,pool in [('prior-failing-batch',old),('prior-counterexample',exact),('fresh-selected-batch',fresh)]:v.write(name+'.json',pool)
 v.write('changed-batch-results.json',dict(passed=True,old_fails_contrast=True,current_passes=True,fresh_passes=True,relocation_same=True,prior_counterexample_replay_preserved=True,old=stats(old),runner=stats(current),fresh=stats(fresh),commands=commands))
 print(json.dumps({'old_failed':True,'runner_passed':True,'fresh_passed':True,'selected_fresh_seeds':[r['generation']['seed'] for r in fresh]}))
