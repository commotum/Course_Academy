"""Explicit-parameter reconstruction of non-source inventory items, read-only."""
import json,sys,copy
import review as t
from probes import sign_strategy,measure
sys.path.insert(0,str(t.R))
from scripts.generator_publish import stable_identities, normalized_question
src=json.load(open(t.J/'source/source.json'));kp_uuid=src['material']['kp'][':knowledge-point/id']
records=[];results=[]
for q in json.load(open(t.E/'stored-records.json')):
 rows=t.equations(q[':question/problem']);rf=t.rref(rows);b,c,d=rf[0][1:];f=q[':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);sb=[[1 if x>0 else -1 for x in t.matrix(a[':answer/value'])[0][1:]] for a in f[':answer-field/choices']]
 plan='swap2' if 'leftrightarrow R_2' in q[':question/worked-solution'] else 'swap3' if 'leftrightarrow R_3' in q[':question/worked-solution'] else 'normalize'
 p=dict(profile='authored-sign-comparison',difficulty='easy',b=int(b),c=int(c),d=int(d),scales=[int(r[0]) for r in rows],plan=plan)
 r=t.g.authored(p,sb,ci);r['question']=stable_identities(r['question'],kp_uuid)
 r['generation'].update(sign_bank=sb,correct_index=ci,reproduction='Explicit parameters inferred from stored prompt/bank; seed/draw not captured in inventory. Not asserted as original generation metadata.')
 stored=normalized_question(q);out=normalized_question(r['question']);a=copy.deepcopy(stored);bq=copy.deepcopy(out);a.pop(':question/worked-solution',None);bq.pop(':question/worked-solution',None)
 same=out[':question/id']==q[':question/id'];assert same and a==bq
 records.append(r);results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'stable_id_equal':same,'prompt_bank_key_equal':a==bq,'solution_text_equal':stored.get(':question/worked-solution')==out.get(':question/worked-solution'),'shortcut_success':sign_strategy(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1],'generation_metadata_in_capture':False})
t.save('generated-records.json',records);t.save('inventory-reproduction-results.json',results)
t.save('affected-inventory.json',{'affected_questions':[{'question_id':x['question_id'],'entity_id':x['entity_id'],'finding':'All choices have identical absolute entries; signs of first input equation alone select the keyed matrix. Explicit-parameter reconstruction matches stored stable question ID, full prompt, answer bank and key; original seed metadata was not captured.','reproduction':str(t.PY)+' '+str(t.E/'reproduce_inventory.py'),'evidence_path':'generated-records.json'} for x in results if x['shortcut_success']]})
t.save('inventory-assessment.json',{'basis':5370,'non_source_records_inspected':5,'affected':len(results),'verified':'Matched all five stable publication IDs, complete prompts, answer banks and keys using explicit-parameter executable reconstruction. Original source IDs excluded.','limitations':['Inventory contains no generation metadata: original seed/draw unavailable and not invented. Explicit reconstruction parameters are recorded as inferred.','Worked solution TeX uses different scalable parentheses but same mathematical operations; no historical byte-exact solution assertion.']})
print(json.dumps(results,indent=2))
