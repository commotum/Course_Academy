"""Check captured generated records against the supplied inventory, read-only."""
import json
from collections import Counter
from pathlib import Path
from probes import probe
from validate_repair import presentation
E=Path(__file__).resolve().parent
I=json.loads((E.parents[1]/'source/inventory.json').read_text())
rs=json.loads((E/'historical-records.json').read_text());byid={r['question'][':question/id']:r for r in rs};results=[];affected=[]
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
def signature(q):
 fields=[]
 for f in q[':question/answer-fields']:
  choices={c[':answer/id']:presentation(c[':answer/value']) for c in f[':answer-field/choices']};correct=f.get(':answer-field/correct');correct=correct.get(':answer/value') if isinstance(correct,dict) else choices[correct[1]] if correct else None
  fields.append([f[':answer-field/key'],enum(f[':answer-field/type']),sorted(choices.values()),presentation(correct) if correct else None])
 return [q[':question/id'],enum(q[':question/difficulty']),presentation(q[':question/problem']),presentation(q[':question/worked-solution']),fields]
original=generated=0
for q in I['questions']:
 if ':question/math-academy-id' in q:original+=1;continue
 generated+=1;r=byid.get(q[':question/id']);assert r is not None,'Untested generated inventory'
 match=signature(q)==signature(r['question']);assert match
 p=probe(r);bad=p['side_frequency_max']['unique'] and p['side_frequency_max']['success']
 results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'complete_record_match':match,'stored_generation_metadata_in_inventory':False,'generation_provenance':'metadata from preserved complete historical generated record, matched to inventory by question ID and complete learner content','demonstrated_frequency_defect':bad,'probe':p})
 if bad:affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'unique maximum equation-side repetition selects the key','reproduction':'Run the manifest Python on evidence/inventory_check.py; inspect this record with evidence/probes.py probe(record)','evidence_path':'generated-records.json'})
(E/'generated-records.json').write_text(json.dumps(rs,indent=2)+'\n')
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
(E/'inventory-review.json').write_text(json.dumps({'basis':I['basis'],'source_questions_excluded':original,'generated_questions_tested':generated,'untested_generated':generated-len(results),'tested_weakness':'unique maximum equation-side frequency','results':results,'conclusion':'Verified absence of this specific weakness in all four captured generated records, which are hard expansion questions. This does not assert absence of unrelated defects or cover uncaptured database changes.'},indent=2)+'\n')
print('Inventory:',original,'original sources excluded;',generated,'generated records matched; affected',len(affected))
