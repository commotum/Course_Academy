"""Reproduce the exact original review failures from the preserved pre-repair snapshot."""
import importlib.util,json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
from shortcut import measure
spec=importlib.util.spec_from_file_location('original_generator',W/'evidence/before-package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
expected={q[':question/id'] for q in json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
actual={r['generation']['parameters']['source_id'] for r in g.replay()}
minimal=g.generate('easy',1,913771);batch=g.generate('easy',5,4221100018)
report={'source_missing':sorted(expected-actual),'seed_913771':measure(minimal),'seed_4221100018':measure(batch)}
assert report['source_missing']==['693512da-f45c-5aae-999f-b43069296756']
assert report['seed_913771']['successes']==1 and report['seed_4221100018']['successes']==5
p=minimal[0]['generation']['parameters'];assert [p[k] for k in ('b','c','d','scales')]==[-10,-3,-14,[-8,7,4]]
(W/'evidence/before-failures.json').write_text(json.dumps(report,indent=2))
print('Original failures reproduced: missing source bank; signs-only selection 1/1 minimal and 5/5 batch.')
