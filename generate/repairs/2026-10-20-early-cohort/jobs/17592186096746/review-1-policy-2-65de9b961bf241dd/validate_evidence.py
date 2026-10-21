import json,hashlib
from pathlib import Path
import jsonschema
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
p=json.load(open(E/'pedagogical-variation.json'));jsonschema.validate(p,json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json')))
r=json.load(open(E/'result.json'));assert set(r['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'};assert r['verdict']=='accepted' and not r['findings']
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('sample_refs','evidence_paths'):refs.extend(v)
   walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(p);walk(r)
for ref in refs:
 path=Path(ref);assert not path.is_absolute() and '..' not in path.parts,ref;assert (E/path).is_file() and (E/path).stat().st_size,ref
assert all(c['status']=='passed' and c['evidence_paths'] for c in r['checks'].values())
a=json.load(open(E/'affected-inventory.json'));g=json.load(open(E/'generated-records.json'));ids={x['question'][':question/id'] for x in g}
for x in a['affected_questions']:
 assert x['question_id'] in ids;assert (E/x['evidence_path']).is_file()
assert len(a['affected_questions'])==5
for folder in ('render','render-extra'):
 report=json.load(open(E/folder/'rendering.json'));assert report['passed'] and len(report['cases'])==6
assert json.load(open(E/'grader-results.json'))['accepted_checks']==127
current={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert current==json.load(open(E/'package-before.json'))==json.load(open(E/'package-after.json'))
result={'passed':True,'pedagogical_schema_valid':True,'relative_nonempty_evidence_refs':len(refs),'distinct_evidence_paths':len(set(refs)),'all_eight_checks_passed':True,'affected_historical_records':5,'package_unchanged':True}
(E/'evidence-contract-results.json').write_text(json.dumps(result,indent=2));s=E/'session-state.md';s.write_text(s.read_text().replace('final evidence-contract check pending.','final evidence-contract check passed.'));print(json.dumps(result))
