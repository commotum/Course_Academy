"""Acceptance assertions: historical mode must fail; current mode must pass."""
import sys,json,importlib.util
sys.dont_write_bytecode=True
import review as t
from shortcut import measure
mode=sys.argv[1] if len(sys.argv)>1 else 'current'
if mode=='historical':
 spec=importlib.util.spec_from_file_location('before',t.W/'evidence/before-package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
else:g=t.g
expected={q[':question/id'] for q in json.load(open(t.J/'source/source.json'))['material']['kp'][':knowledge-point/questions']};actual={r['generation']['parameters']['source_id'] for r in g.replay()}
minimal=g.generate('easy',1,913771);batch=g.generate('easy',5,4221100018)
checks={'all_16_source_banks':expected<=actual,'minimal_not_uniquely_solved_by_signs':measure(minimal)['successes']==0,'exact_batch_not_all_sign_solvable':measure(batch)['successes']<len(batch)}
print(json.dumps({'mode':mode,'passed':all(checks.values()),'checks':checks,'missing':sorted(expected-actual),'minimal_successes':measure(minimal)['successes'],'batch_successes':measure(batch)['successes']}))
sys.exit(0 if all(checks.values()) else 1)
