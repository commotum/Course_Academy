"""Read back publication and exercise actual grading without learner writes."""
from collections import Counter
import json,re,sys,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,normalized_question,jsonable
from scripts.generator_packages import resolve_registered_script,verify_package
from generate.triangle_complement_contract import inspect_record
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];proof=json.loads((H/'verification.json').read_text())
k=p.read_kp(17592186105906,H/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['new_reference']
entry=resolve_registered_script(ref,ROOT,p.config.math_root);verify_package(entry.parent,Path(ref).parts[2])
for name in json.loads((entry.parent/'generator-package.json').read_text())['files']:
 assert (ROOT/'generate/scratch/17592186105906'/name).read_bytes()==(entry.parent/name).read_bytes()
qs={str(q[':question/id']):q for q in k[':knowledge-point/questions']};prepared=json.loads((H/'publication/preparation.json').read_text());checks=[];bank=[]
for i,row in enumerate(prepared['records']):
 q=qs[row['question'][':question/id']];assert normalized_question(q)==normalized_question(row['question']);inspect_record(row)
 f=q[':question/answer-fields'][0];key=f[':answer-field/correct'];correct=key[':db/id']
 if f[':answer-field/type'][':db/ident'].endswith('/radio'):
  cases=[({'fieldId':f[':db/id'],'choiceId':a[':db/id']},'correct' if a[':db/id']==correct else 'incorrect') for a in f[':answer-field/choices']]
 else:
  v=key[':answer/value'];cases=[({'fieldId':f[':db/id'],'value':v},'correct'),({'fieldId':f[':db/id'],'value':v+'.000'},'correct'),({'fieldId':f[':db/id'],'value':str(int(v)+1)},'incorrect')]
 for response,expected in cases:
  payload={'topicId':17592186050149,'questionId':q[':db/id'],'responses':[response]}
  request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
  with urllib.request.urlopen(request,timeout=45) as result:out=json.load(result)
  assert out['status']==expected,(payload,out)
  checks.append({'question':q[':db/id'],'response':response,'expected':expected,'actual':out['status']})
 bank.append({'entity':q[':db/id'],'band':row['question'][':question/difficulty'].split('/')[-1],'parameters':row['generation']['parameters']})
before=json.loads((H/'before.json').read_text());now=jsonable(k);by_eid={q[':db/id']:q for q in now[':knowledge-point/questions']}
for q in before[':knowledge-point/questions']:
 expected=dict(q)
 if q[':db/id'] in proof['retired_questions']:expected[':question/retired']=True
 assert by_eid[q[':db/id']]==expected
assert now[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
active=[q for q in now[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
usage=p.client.query('[:find ?q ?item :in $ [?q ...] :where [?item :task-item/content ?q]]',[[q[':db/id'] for q in active]],H/'live','active-usage',basis)
used={q for q,item in usage};available=[q for q in active if q[':db/id'] not in used]
assert {q[':db/id'] for q in available}=={r['entity'] for r in bank}
counts=Counter(q[':question/difficulty'][':db/ident'].split('/')[-1] for q in available)
assert counts=={'easy':5,'moderate':5,'hard':5} and len(checks)==63
result={'passed':True,'committed':True,'basis_readback':basis,'kp':17592186105906,'topic':17592186050149,'generator':ref,'unused_old_generated_retired':len(proof['retired_questions']),'used_old_records_preserved':proof['preserved_used_questions'],'new_available_generated':dict(counts),'imported_questions_preserved':proof['imported_questions_preserved'],'canonical_preserved':True,'live_grading_checks':len(checks),'database_writes_by_verification':0,'new_bank':bank}
(H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');(H/'live-grading-verification.json').write_text(json.dumps({'passed':True,'database_writes':0,'checks':checks},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='new_bank'}))
