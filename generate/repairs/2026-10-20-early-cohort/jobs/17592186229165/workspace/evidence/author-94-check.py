"""Verify retained runtime and staged evidence, plus a small visible-math sample."""
import hashlib, importlib.util, json, pathlib, sys
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'checks'))
import test_role_exchange as regression
load=lambda p:json.loads(p.read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
handoff=load(root/'evidence/review-installation-handoff.json')
for artifact in handoff['files']:
 assert digest(root/artifact['source'])==artifact['sha256'], artifact['source']
provenance=load(root/'evidence/report-repair/provenance.json')
for name,expected in provenance['runtime_sha256'].items():
 assert digest(root/name)==expected,name
source_hash=digest(root.parent/'source/source.json')
assert source_hash==load(root/'evidence/source-and-inventory-results.json')['source_sha256']
g=regression.module(root/'17592186229165.py')
small=[g.generate('easy',seed=i) for i in range(901,906)]+[g.generate('moderate',seed=901)]+[g.generate('hard',template='two_nonresonant',seed=i) for i in (901,902)]
assert small==load(root/'evidence/small-regression.json')
for r in small:
 regression.V.validate_record(r,r['question'][':question/difficulty'].split('/')[-1])
strict=load(root/'evidence/report-repair/results.json')
assert strict['status']=='blocked'
assert strict['required_destination_error']=='decision_variation has an unresolved decision shortcut'
role=load(root/'evidence/role-regression/results.json')
assert role['status']=='passed'
result={
 'status':'blocked_external_evidence_installation',
 'runtime_changes':False,
 'history_events_inspected':len(load(root.parent/'repair-history.json')['events']),
 'commands':[
  {'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -E -s -B checks/check_report_installation.py','outcome':'AssertionError: required external report remains uncorrected','log':'evidence/report-repair/author-94-reproduction.log'},
  {'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -E -s -B checks/test_role_exchange.py','outcome':role['status'],'log':'evidence/author-94-role-regression.log'},
  {'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -E -s -B evidence/author-94-check.py','outcome':'passed'}],
 'required_destination':handoff['required_destination'],
 'handoff_artifacts_verified':len(handoff['files']),
 'unchanged_runtime_sha256':provenance['runtime_sha256'],
 'source_unchanged':True,
 'small_unaffected_math_sample_passed':len(small),
 'retained_findings':load(root/'repair-regressions.json')['findings'],
 'strict_report_regression':strict,
 'role_regression':{k:v for k,v in role.items() if k not in ('native_report','commands')},
 'native_grader_report':'evidence/role-regression/grader-report.json',
 'next_required_action':'Runner installs the staged corrected reports at the required destination, then reruns the strict default regression and independent review.',
 'scope':'Workspace-only verification. No external writes, generator changes, database changes, engine changes, publication, or weakened checks.'}
(root/'evidence/author-94-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','handoff_artifacts_verified','small_unaffected_math_sample_passed','source_unchanged')}))
