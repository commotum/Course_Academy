import audit as a
import sympy as s

g=a.module(a.PKG/'17592186087877.py');inv=a.load(a.JOB/'source/inventory.json');historical=a.load(a.PKG/'17592186087877/reference/replenishment/basis-2009/generated.json')
records=[];details=[];affected=[]
for old in historical:
 meta=old['generation'];r=g.generate(old['question'][':question/difficulty'].split('/')[-1],meta['seed'],template=meta['template'])
 assert r['generation']['parameters']==meta['parameters']
 assert r['question']==old['question'],(meta['seed'],'record differs')
 stored=next(q for q in inv['questions'] if q[':question/id']==r['question'][':question/id'])
 # Compare complete learner-facing prompt, solution and answer bank by values+UUIDs.
 assert stored[':question/problem']==r['question'][':question/problem']
 assert stored[':question/worked-solution']==r['question'][':question/worked-solution']
 sf=a.field(stored);rf=a.field(r['question'])
 assert {z[':answer/id']:z[':answer/value'] for z in sf[':answer-field/choices']}=={z[':answer/id']:z[':answer/value'] for z in rf[':answer-field/choices']}
 assert a.correct_id(stored)==a.correct_id(r['question'])
 records.append(r)
 hits=a.cue(r['question']);bad=hits==[a.correct_id(r['question'])]
 details.append({'question_id':r['question'][':question/id'],'entity_id':stored[':db/id'],'seed':meta['seed'],'template':meta['template'],'parameters':meta['parameters'],'stored_question_match':True,'bank_only_shortcut_correct':bad})
 if bad:
  affected.append({'question_id':r['question'][':question/id'],'entity_id':stored[':db/id'],'finding':'Answer-bank-only reciprocal-and-square exponential signature identifies the correct choice without reading P or Q.','reproduction':f"PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory-audit.py ; generate('{old['question'][':question/difficulty'].split('/')[-1]}', seed={meta['seed']}, template='{meta['template']}')","evidence_path":"generated-records.json"})
a.save('generated-records.json',records);a.save('affected-inventory.json',{'affected_questions':affected});a.save('inventory-results.json',{'basis':inv['basis'],'captured_questions':len(inv['questions']),'original_source_questions':8,'generated_records_reproduced':len(records),'provenance':'Generation recipes recovered from package historical reference/replenishment/basis-2009/generated.json; independently rerun current executable; all nine match captured question IDs, prompt, solution, bank values/UUIDs and keys.','results':details,'demonstrated_affected':len(affected),'limits':['Original source questions were not marked generated.','Other shortcut types on moderate/hard stored questions are untested; a false bank-only result is not evidence of absence of other defects.']})
print('Reproduced',len(records),'stored records;',len(affected),'affected by demonstrated easy-bank signature')
