"""Replay all captured nonMA questions without changing their normal identities."""
import importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('independent_validator',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
items=[]
for z in json.loads((D/'independent-inventory.json').read_text())['questions']:
 q=g.normalize_raw(z['record']);obj=v.read(v.inline(q[':question/problem'])[0]);params={'a':g.canonical(obj['set'].start),'b':g.canonical(obj['set'].end)};level=q[':question/difficulty'].split('/')[-1]
 profile=('captured_interval' if '\\le x\\le' in q[':question/problem'] else 'observed_interval') if obj['form']=='chain' else ('captured_inequality' if 'x\\in' in q[':question/problem'] else 'observed_inequality')
 r=g.generate(level,0,parameters=params,profile=profile,variable='x',orientation='ascending');v.check(r)
 expected=dict(q);actual=dict(r['question'])
 expected[':question/answer-fields'][0][':answer-field/choices'].sort(key=lambda z:z[':answer/id'])
 actual[':question/answer-fields'][0][':answer-field/choices'].sort(key=lambda z:z[':answer/id'])
 assert expected==actual,(q[':question/id'],expected,actual)
 items.append({'question_id':q[':question/id'],'profile':profile,'difficulty':level,'parameters':params,'full_question_field_answer_uuids_preserved':True,'prompt_prose_solution_prose_exact':True,'whole_bank_and_correct_key_exact':True})
(D/'inventory-preservation.json').write_text(json.dumps({'exact_original_nonma_records':len(items),'reproduced_normal_questions':len(items),'matched_choices':len(items)*5,'checks':items},indent=2)+'\n')
print('Preserved',len(items),'normal question/field UUIDs, all65 answer UUIDs, full prose, banks and keys.')
