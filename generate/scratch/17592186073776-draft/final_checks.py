"""Final direct public-contract probes and immutable registered artifact guard."""
import sys;sys.dont_write_bytecode=True
import ast,hashlib,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2]
spec=importlib.util.spec_from_file_location('local_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert (D/'source.json').read_bytes()==(R/'generate/runs/current/sources/17592186073776.json').read_bytes()
for folder in ['topics','lessons']:assert (D/'reference'/f'{folder}-17592186050240.json').read_bytes()==(R/'generate/runs/current'/folder/'17592186050240.json').read_bytes()
# The public entry point itself must reject accidental nonraw string escapes.
original=g.solution
g.solution=lambda p,t:original(p,t)+'\x0c'
try:g.generate('easy')
except ValueError as e:assert 'C0' in str(e)
else:raise AssertionError('Public generator accepted C0 content')
finally:g.solution=original
records=[g.generate(level,seed=i) for level in g.LEVELS for i in range(12)]
ids=set();answerids=set()
for r in records:
 q=r['question'];f=q[':question/answer-fields'][0]
 assert q[':question/id'] not in ids;ids.add(q[':question/id'])
 assert f[':answer-field/id']!=q[':question/id']
 for a in f[':answer-field/choices']:
  assert a[':answer/id'] not in answerids;answerids.add(a[':answer/id'])
  assert a[':answer/id']==g.ident(f[':answer-field/id']+':'+a[':answer/value'])
 assert f[':answer-field/correct'][1] in {a[':answer/id'] for a in f[':answer-field/choices']}
 assert r['generation']['math_format']=='course-academy-tex-v1'
base=json.loads((D/'immutable-baseline.json').read_text())
scratch=R/'generate/scratch';files=[scratch/'17592186073776.py',*sorted((scratch/'17592186073776').rglob('*')),*sorted((scratch/'__pycache__').glob('17592186073776.*.pyc'))]
now={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
assert now==base,'Registered script/tree/cache pathset or hashes changed'
reviewed=ast.parse(Path('/tmp/reviewed-17592186073776.py').read_text());draft=ast.parse(D.with_suffix('.py').read_text())
functions=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
a,b=functions(reviewed),functions(draft)
report={'passed':True,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'immutable_registered_pathset_files':len(now),'immutable_sha256_and_pathset_unchanged':True,'public_c0_mutation_rejected':True,'field_owned_id_records_checked':len(records),'field_owned_answer_ids_checked':len(answerids),'source_and_context_wrappers_exact':True,'prior_review_to_draft_changed_functions':sorted(k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)),'parent_independent_qa':'pending'}
(D/'final-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
