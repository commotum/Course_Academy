import json,hashlib
from pathlib import Path
import jsonschema
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
load=lambda p:json.loads(Path(p).read_text())
ped=load(E/'pedagogical-variation.json');result=load(E/'result.json')
jsonschema.validate(ped,load(R/'generate/pipeline/pedagogical-variation.schema.json'))
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('sample_refs','evidence_paths'):refs.extend(v)
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(ped);walk(result)
for p in refs:
 q=E/p;assert not Path(p).is_absolute() and q.is_file() and q.stat().st_size>0,p
assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert all(c['status']=='passed' and c['evidence_paths'] for c in result['checks'].values())
assert result['verdict']=='accepted' and not result['findings']
assert {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}==load(E/'package-before.json')
assert load(E/'affected-inventory.json')=={'affected_questions':[]}
report={'passed':True,'schema':'passed: jsonschema Draft202012 against repository pedagogical-variation.schema.json','references_checked':len(refs),'all_nonempty_relative':True,'eight_checks':list(result['checks']),'package_unchanged':True,'command':'python3 -B verify_evidence.py'}
(E/'evidence-contract.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
