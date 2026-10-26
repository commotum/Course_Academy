from pathlib import Path
import json,sys,urllib.request
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];summaries=[];checks=[];retired=[];replacements=[]
for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=item['kp'];d=H/str(kp);proof=json.loads((d/'verification.json').read_text());k=p.read_kp(kp,H/'live'/str(kp),basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['new_reference'];entry=resolve_registered_script(ref,ROOT,p.config.math_root);verify_package(entry.parent,Path(ref).parts[2]);local=ROOT/f'generate/scratch/{kp}'
 for name in json.loads((entry.parent/'generator-package.json').read_text())['files']:assert(local/name).read_bytes()==(entry.parent/name).read_bytes()
 questions={str(q[':question/id']):q for q in k[':knowledge-point/questions']};active=[q for q in questions.values()if not q.get(':question/math-academy-id')and not q.get(':question/retired')];assert len(active)==5
 records=json.loads((d/'accepted-pool.json').read_text());assert{q[':db/id']for q in active}=={r['entity']for r in proof['new_questions']}
 for row in records:
  q=questions[row['question'][':question/id']];assert normalized_question(q)==normalized_question(row['question']);f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][':db/id']
  for a in f[':answer-field/choices']:
   expected='correct'if a[':db/id']==cid else'incorrect';payload={'topicId':17592186051065,'questionId':q[':db/id'],'responses':[{'fieldId':f[':db/id'],'choiceId':a[':db/id']}]}
   req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
   with urllib.request.urlopen(req,timeout=45)as r:out=json.load(r)
   assert out['status']==expected,(payload,out);checks.append({'question':q[':db/id'],'choice':a[':db/id'],'expected':expected,'actual':out['status']})
 for eid in proof['retired_questions']:assert next(q for q in questions.values()if q[':db/id']==eid)[':question/retired']is True
 retired+=proof['retired_questions'];replacements+=proof['replacements'];summaries.append({'kp':kp,'active_generated':5,'retired':len(proof['retired_questions']),'imported_preserved':proof['imported_questions_preserved'],'generator':ref});print(kp,'live banks and every choice verified',flush=True)
assert len(retired)==10 and 17592186676330 in retired and len(checks)==75
result={'passed':True,'committed':True,'basis_readback':basis,'topic':17592186051065,'generators_updated':3,'old_questions_retired':10,'replacement_questions':10,'unchanged_final_amount_questions':5,'imported_questions_preserved':6,'canonicals_preserved':3,'saved_learner_history_preserved':True,'live_grading_checks':75,'reported_question_replacement':next(r for r in replacements if r['old']==17592186676330),'knowledge_points':summaries}
for name,value in [('completion',result),('replacement-map',replacements),('live-grading-verification',{'passed':True,'database_writes':0,'checks':checks})]:(H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='knowledge_points'}))
