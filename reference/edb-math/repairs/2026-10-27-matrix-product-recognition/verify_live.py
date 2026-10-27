"""Live readback and grading only; no learner-state mutation."""
import json,sys,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question,jsonable,loads
from scripts.generator_packages import resolve_registered_script,verify_package
from generate.matrix_product_prompt_policy import validate_delivery_batch,KP
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];proof=json.loads((H/'verification.json').read_text())
k=p.read_kp(KP,H/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['new_reference']
entry=resolve_registered_script(ref,ROOT,p.config.math_root);verify_package(entry.parent,Path(ref).parts[2])
for name in json.loads((entry.parent/'generator-package.json').read_text())['files']:
 assert (ROOT/f'generate/scratch/{KP}'/name).read_bytes()==(entry.parent/name).read_bytes()
qs={str(q[':question/id']):q for q in k[':knowledge-point/questions']};prepared=json.loads((H/'publication/preparation.json').read_text());checks=[];entities=[]
for row in prepared['records']:
 q=qs[row['question'][':question/id']];assert normalized_question(q)==normalized_question(row['question']);validate_delivery_batch([row],KP);entities.append(q[':db/id'])
 for field in q[':question/answer-fields']:
  key=field[':answer-field/correct'][':answer/value']
  for value,expected in ((key,'correct'),(key+'.000','correct'),(str(int(key)+1),'incorrect')):
   response={'fieldId':field[':db/id'],'value':value}
   responses=[response if other[':db/id']==field[':db/id'] else {'fieldId':other[':db/id'],'value':other[':answer-field/correct'][':answer/value']} for other in q[':question/answer-fields']]
   payload={'topicId':17592186048297,'questionId':q[':db/id'],'responses':responses}
   req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
   with urllib.request.urlopen(req,timeout=45) as result:out=json.load(result)
   assert out['status']==expected,(payload,out)
   checks.append({'question':q[':db/id'],'response':response,'expected':expected,'actual':out['status']})
now=jsonable(k);by_eid={q[':db/id']:q for q in now[':knowledge-point/questions']}
# Preserve responses saved between investigation and publication as well.
before=jsonable(loads(prepared['before_edn']))
for q in before[':knowledge-point/questions']:
 expected=dict(q)
 if q[':db/id'] in proof['retired_questions']:expected[':question/retired']=True
 assert by_eid[q[':db/id']]==expected
assert now[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
for q in now[':knowledge-point/questions']:
 if not q.get(':question/math-academy-id') and not q.get(':question/retired'):validate_delivery_batch([{'question':q}],KP)
usage=p.client.query('[:find ?q ?item :in $ [?q ...] :where [?item :task-item/content ?q]]',[entities],H/'live','new-usage',basis);assert not usage
assert len(entities)==5 and len(checks)==45 and 17592186695793 in proof['retired_questions']
result={'passed':True,'committed':True,'basis_readback':basis,'topic':17592186048297,'kp':KP,'generator':ref,'hinted_questions_retired':proof['retired_questions'],'new_available_easy_questions':entities,'imported_preserved':proof['imported_questions_preserved'],'canonical_preserved':True,'existing_attempt_content_preserved':True,'unhinted_moderate_hard_records_preserved':11,'live_grading_checks':len(checks),'database_writes_by_verification':0}
for name,value in [('completion',result),('live-grading-verification',{'passed':True,'database_writes':0,'checks':checks})]:(H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps(result))
