import sys,json,hashlib,collections
from pathlib import Path
sys.path.insert(0,'scripts');from question_markers import repair_problem,validate_prompt_markers
from migrate_learner_history import dumps,kw
H=Path('reference/edb-math/repairs/2026-10-23-choice-markers');fields=[]
for q in json.loads((H/'candidates.json').read_text()):
 fs=[{':answer-field/key':f['answer-field/key'],':answer-field/type':f['type']} for f in q['fields']]
 after=repair_problem(q['v'],fs);assert after!=q['v'];validate_prompt_markers({':question/problem':after,':question/answer-fields':fs})
 assert ('?' in after)==('⟨{{selection}}' in q['v'] or ',{{selection}}' in q['v'] or '\\,{{selection}}' in q['v']) or q['markers'][0]['type']=='free' or '?' in q['v']
 fields.append({'entity':q['e'],'attribute':'question/problem','before':q['v'],'after':after,'type':q['markers'][0]['type'],'answer_fields':fs,'before_sha256':hashlib.sha256(q['v'].encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()})
(H/'fields.json').write_text(json.dumps(fields,indent=2,ensure_ascii=False)+'\n')
(H/'questions-transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in fields])+'\n')
(H/'read-query.edn').write_text('[:find ?e ?v :in $ [?e ...] :where [?e :question/problem ?v]]\n');(H/'read-inputs.edn').write_text(dumps([[f['entity'] for f in fields]])+'\n')
print('Prepared questions',len(fields),collections.Counter(f['type'] for f in fields),'embedded unknowns',sum('⟨' in f['before'] and '{{selection}}' in f['before'] for f in fields))
