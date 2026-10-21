"""Read-only reconstruction of captured historical defects; never marks sources generated."""
import copy,json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];R=Path('/home/jake/Developer/Course_Academy')
sys.path[:0]=[str(W),str(R)]
import generator as g
from visible_math import equations,rref,matrix
from shortcut import measure
from scripts.generator_publish import stable_identities,normalized_question
source=json.loads((W.parent/'source/source.json').read_text())['material']['kp']
original={q[':question/id'] for q in source[':knowledge-point/questions']};original.add(source[':knowledge-point/canonical-example'][':question/id'])
inv=json.loads((W.parent/'source/inventory.json').read_text());records=[];results=[]
for q in inv['questions']:
    if q[':question/id'] in original: continue
    rows=equations(q[':question/problem']);f=q[':question/answer-fields'][0]
    key=f[':answer-field/correct'][':answer/id'];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==key)
    bank=[[int(v) for v in matrix(a[':answer/value'])[0][1:]] for a in f[':answer-field/choices']]
    plan='swap2' if 'leftrightarrow R_2' in q[':question/worked-solution'] else 'swap3' if 'leftrightarrow R_3' in q[':question/worked-solution'] else 'normalize'
    p=dict(profile='historical-sign-comparison-reconstruction',difficulty='easy',scales=[int(row[0]) for row in rows],plan=plan)
    r=g.numerical_bank(p,bank,ci);r['question']=stable_identities(r['question'],source[':knowledge-point/id'])
    a=normalized_question(q);b=normalized_question(r['question']);solution_equal=a.pop(':question/worked-solution',None)==b.pop(':question/worked-solution',None)
    assert a==b,'historical prompt/bank/key/IDs reconstruction failed'
    # Preserve captured question (complete solution included) with explicit inferred metadata.
    r['question']=copy.deepcopy(q)
    r['generation'].update(numerical_bank=bank,correct_index=ci,reproduction='Parameters inferred from captured prompt and choices; original version, seed and draw are absent. Current constructor reproduces stable publication ID, complete prompt, bank and key; recorded question retains captured solution.',original_generation_metadata=None)
    trial=g.numerical_bank(p,bank,ci);shortcut=measure([trial])['successes']==1
    records.append(r);results.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],stable_id_prompt_bank_key_match=True,solution_format_equal=solution_equal,shortcut=shortcut,original_generation_metadata_present=False))
(W/'generated-records.json').write_text(json.dumps(records,indent=2))
(W/'affected-inventory.json').write_text(json.dumps({'affected_questions':[dict(question_id=x['question_id'],entity_id=x['entity_id'],finding='All five choices share absolute entries; first-equation signs uniquely select the keyed choice. Stable publication ID, complete prompt, bank and key reproduced from inferred explicit parameters. Original generation metadata absent.',reproduction='/home/jake/Developer/Course_Academy/.venv/bin/python checks/inventory.py',evidence_path='../workspace/generated-records.json') for x in results if x['shortcut']]},indent=2))
(W/'evidence/inventory-results.json').write_text(json.dumps({'basis':inv['basis'],'captured_questions':len(inv['questions']),'source_ids_excluded':len(original),'non_source_tested':len(results),'affected':sum(x['shortcut'] for x in results),'records':results,'evidence_path_base':'Job evidence_root author-1; ../workspace/generated-records.json resolves to the workspace artifact.','limitation':'Original generation seed/draw/version metadata is absent in capture, so this verifies reconstructed parameters and stored complete records, not original seed provenance. Empty untested cases are not claimed defect-free.'},indent=2))
print(json.dumps({'non_source_tested':len(results),'affected':sum(x['shortcut'] for x in results)}))
