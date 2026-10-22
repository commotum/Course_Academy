"""Read-only comparison of captured inventory with original source evidence."""
import json
from pathlib import Path
W=Path(__file__).resolve().parents[1]
ROOT=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186184172/source')
def canonical(x):
 if isinstance(x,dict):return {k:canonical(v) for k,v in x.items()}
 if isinstance(x,list):return sorted([canonical(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
 return x
if __name__=='__main__':
 source=json.loads((ROOT/'source.json').read_text());inv=json.loads((ROOT/'inventory.json').read_text())
 questions={q[':question/id']:q for q in source['material']['kp'][':knowledge-point/questions']};audit=[]
 for item in inv['questions']:
  original=questions.get(item[':question/id']);assert original
  for field in [':question/problem',':question/worked-solution',':question/answer-fields',':question/difficulty']:
   assert canonical(item[field])==canonical(original[field]),(item[':question/id'],field)
  assert not any('generat' in k for k in item)
  audit.append({'question_id':item[':question/id'],'entity_id':item[':db/id'],'source_id':item[':question/math-academy-id'],'result':'Original source content and full banks match, ignoring collection ordering. No generated provenance. Not relabeled as generated.'})
 (W/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
 report={'captured_basis':inv['basis'],'tested_entries':len(audit),'generated_entries_found':0,'affected_generated_instances_demonstrated':0,'entries':audit,'limits':['All 15 captured entries match original source records. No generated instance of the earlier repeated-profile shortcut is demonstrated in this inventory. The latest profile-omission finding concerns batch reachability; no individual stored question is defective merely because a sampler never selected its profile.','No claim about live or uncaptured inventory; packaging failure is a runtime problem and cannot be established from stored question content alone.']}
 (W/'evidence/inventory-audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Captured inventory:',len(audit),'matching original sources; no generated instances demonstrated')
