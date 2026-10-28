"""Exercise production grading without creating or changing learner attempts."""
import itertools,json,urllib.request
from migration import H,Publisher,loads,jsonable,Q_PATTERN,atomic_json
from verify import question_content
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];prep=json.loads((H/'publication/preparation.json').read_text());ids=[r['question'] for r in prep['plans']]
rows=p.client.query('[:find (pull ?q '+Q_PATTERN+') :in $ [?q ...] :where [?q :question/id _]]',[ids],H/'live','questions',basis);questions={q[':db/id']:jsonable(q) for [q] in rows};checks=[]
for plan,case in zip(prep['plans'],prep['proposed']):
 q=questions[plan['question']];assert question_content(q)==question_content(case['question']);fields=q[':question/answer-fields'];by_uuid={f[':answer-field/id']:f for f in fields}
 correct={f[':db/id']:f[':answer-field/correct'][':db/id'] for f in fields}
 def choice(f,value):return next(a[':db/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(value).lower())
 tests=[('canonical',correct,True)]
 for f in fields:
  flipped=dict(correct);flipped[f[':db/id']]=next(a[':db/id'] for a in f[':answer-field/choices'] if a[':db/id']!=correct[f[':db/id']]);tests.append(('single flip '+f[':answer-field/key'],flipped,False))
 tests.append(('empty selected subset',{f[':db/id']:choice(f,False) for f in fields},all(f[':answer-field/correct'][':answer/value']=='false' for f in fields)))
 if plan['decision']=='convert':
  correct_labels={o['source_label'] for o in plan['objects'] if o['selected']}
  for old in plan['choice_mapping']:
   subset=set(old['selected']);submitted={by_uuid[obj['field_id']][':db/id']:choice(by_uuid[obj['field_id']],obj['source_label'] in subset) for obj in plan['objects']};tests.append(('original radio '+str(old['old_answer']),submitted,subset==correct_labels))
 else:
  for bits in itertools.product((False,True),repeat=len(fields)):tests.append(('old consistent subset '+str(bits),{f[':db/id']:choice(f,b) for f,b in zip(fields,bits)},all(bits)))
 for purpose,submitted,expected in tests:
  payload={'topicId':17592186048123,'questionId':q[':db/id'],'responses':[{'fieldId':fid,'choiceId':aid} for fid,aid in submitted.items()]}
  request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
  with urllib.request.urlopen(request,timeout=45) as result:out=json.load(result)
  assert out['status']==('correct' if expected else 'incorrect'),(purpose,payload,out)
  checks.append({'question':q[':db/id'],'purpose':purpose,'expected':'correct' if expected else 'incorrect','actual':out['status']})
 print(q[':db/id'],'live subset grading verified',flush=True)
proof=json.loads((H/'verification.json').read_text());result={**proof,'live_readback_basis':basis,'live_grading_checks':len(checks),'live_verification_database_writes':0,'topic':17592186048123,'knowledge_points':2,'questions_audited':29,'radio_questions_retained':7,'missing_keys_resolved_during_conversion':2,'generators_registered':0}
atomic_json(H/'live-grading-verification.json',{'passed':True,'database_writes':0,'checks':checks});atomic_json(H/'completion.json',result);print(json.dumps(result))
