import json,sys,subprocess,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;entities={};idents={};questions=[]
def visit(value):
 if isinstance(value,list):return [visit(v) for v in value]
 if isinstance(value,dict):
  if ':db/ident' in value and ':db/id' not in value:
   ident=value[':db/ident'].lstrip(':')
   if ident not in idents:idents[ident]=len(idents)+1;entities[str(idents[ident])]={'db/ident':ident}
   return idents[ident]
  if ':db/id' in value:
   eid=value[':db/id'];row={k.lstrip(':'):visit(v) for k,v in value.items() if k!=':db/id'};entities.setdefault(str(eid),{}).update(row);return eid
 return value
for kp in [17592186092240,17592186092384,17592186092385]:
 K=json.loads((H/str(kp)/'kp.json').read_text())
 for q in K[':knowledge-point/questions']:questions.append(q[':db/id']);visit(q)
input=dict(entities=entities,questions=questions);(H/'eligibility-input.json').write_text(json.dumps(input,indent=2)+'\n')
helper=H.parent/'vector/eligibility';subprocess.run([str(helper),str(H/'eligibility-input.json'),str(H/'eligibility.json')],check=True)
report=json.loads((H/'eligibility.json').read_text());results={r['entity']:r for r in report['questions']};assert results[17592186710391]['eligible'],'Known good normal-line positive control failed'
ledger=json.loads((H/'stored-ledger.json').read_text());missing=[r['entity'] for r in ledger if r['missing']];assert len(missing)==6
assert all(not results[eid]['eligible'] for eid in missing)
summary=dict(passed=True,source_helper='../vector/eligibility.rs',helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),native_entry_point='learning::validate_practice_question',basis=14220,database_writes=0,known_good_control=results[17592186710391],incomplete_imports_screened=[results[eid] for eid in missing],scope_limit='Snapshot omits multistep container graph. Positive eligibility on context-dependent fragments is not a serving claim; actual source eligibility explicitly excludes them.')
(H/'eligibility-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
