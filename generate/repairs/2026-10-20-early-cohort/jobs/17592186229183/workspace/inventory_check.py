#!/usr/bin/env python3
"""Reproduce retained historical generator; match captured stored records read-only."""
import sys
sys.dont_write_bytecode=True
import json,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));from repair_checks import measure
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.question_capture.math_format import normalize_prose
spec=importlib.util.spec_from_file_location('legacy',R/'evidence/legacy/17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
inv=json.loads((R.parent/'source/inventory.json').read_text());by_id={q[':question/id']:q for q in inv['questions']}
historical=json.loads((R/'17592186229183/reference/replenishment/basis-2591/generated.json').read_text())
affected=[];records=[];results=[]
def bank(q):
 out=[]
 for f in q[':question/answer-fields']:
  key=f.get(':answer-field/correct');key=key[':answer/id'] if isinstance(key,dict) else key[1] if key else None
  out.append((sorted(a[':answer/value'] for a in f[':answer-field/choices']),next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key),None)))
 return out
for old in historical:
 m=old['generation'];r=g.generate(m['level'],seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
 assert r['generation']==old['generation'],'Legacy generation metadata must match'
 def unordered(record):
  z=json.loads(json.dumps(record))
  for f in z['question'][':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
  return z
 assert unordered(r)==unordered(old),'Only shuffle order may differ with explicit parameters'
 q=r['question'];qid=q[':question/id'];stored=by_id[qid]
 assert q[':question/problem']==stored[':question/problem']
 assert normalize_prose(q[':question/worked-solution'])==stored[':question/worked-solution']
 assert bank(q)==bank(stored)
 assert measure(r)['rank']==3
 records.append(r)
 affected.append({'question_id':qid,'entity_id':stored[':db/id'],'finding':'Historical whole-bank construction forces correct mass to numerical rank 3, bypassing mixture modeling.',
 'reproduction':f'{sys.executable} inventory_check.py; exact parameters are in evidence/generated-records.json generation metadata',
 'evidence_path':'../workspace/evidence/generated-records.json'})
 results.append({'question_id':qid,'entity_id':stored[':db/id'],'complete_record_and_generation_replayed_ignoring_choice_order':True,'stored_prompt_normalized_solution_bank_key_match':True,'correct_numeric_rank':3})
(R/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
(R/'evidence/generated-records.json').write_text(json.dumps(records,indent=2)+'\n')
(R/'evidence/inventory-results.json').write_text(json.dumps({'basis':inv['basis'],'inventory_count':len(inv['questions']),'generated_tested':len(records),'affected':len(affected),'source_items_not_marked_generated':len(inv['questions'])-len(records),'results':results,'limits':'All ten captured generated records have reproduction metadata and were tested; eleven supplied source items are not classified as generated. No live inventory or learner history queried. evidence_path is relative to the requested author-1 evidence root and resolves into this workspace.'},indent=2)+'\n')
print(json.dumps({'generated_reproduced':len(records),'affected':len(affected)}))
