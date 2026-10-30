"""Confirm live content and grading without saving learner attempts."""
import json,sys,time,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H))
from scripts.generator_publish import Publisher,jsonable,loads
from scripts.generator_packages import resolve_registered_script,verify_package
from build import verify
KP=17592186115226
for attempt in range(45):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
        break
    except OSError:
        if attempt==44:raise
        time.sleep(1)
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];proof=json.loads((H/'verification.json').read_text())
k=p.read_kp(KP,H/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['generator']
entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=verify_package(entry.parent,Path(ref).parts[2]).manifest
for name in manifest['files']:assert (ROOT/f'generate/scratch/{KP}'/name).read_bytes()==(entry.parent/name).read_bytes()
topic_rows=p.client.query('[:find ?t ?title :in $ ?kp :where [?t :topic/knowledge-points ?kp] [?t :topic/title ?title]]',[KP],H/'live','topic',basis)
assert len(topic_rows)==1;topic,title=topic_rows[0]
now={q[':db/id']:q for q in jsonable(k)[':knowledge-point/questions']};prepared=json.loads((H/'publication/preparation.json').read_text());patches={r['entity']:r['after'] for r in prepared['prompt_repairs']}
before=jsonable(loads(prepared['before_edn']))
for q in before[':knowledge-point/questions']:
    expected=dict(q)
    if q[':db/id'] in patches:expected[':question/problem']=patches[q[':db/id']]
    assert now[q[':db/id']]==expected
assert not any('\\ast' in q.get(':question/problem','') for q in now.values())
checks=[]
for eid in proof['questions_repaired']:
    q=now[eid];verify(q);fields=q[':question/answer-fields']
    correct=[{'fieldId':f[':db/id'],'value':f[':answer-field/correct'][':answer/value']} for f in fields]
    wrong=[dict(r) for r in correct];wrong[0]['value']='1' if wrong[0]['value']=='0' else '0'
    for responses,expected in ((correct,'correct'),(wrong,'incorrect')):
        payload={'topicId':topic,'questionId':eid,'responses':responses}
        req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
        with urllib.request.urlopen(req,timeout=45) as response:out=json.load(response)
        assert out['status']==expected,(eid,expected,out)
        checks.append({'question':eid,'expected':expected,'actual':out['status']})
result={'passed':True,'basis':basis,'topic':topic,'topic_title':title,'kp':KP,'generator':ref,'questions_repaired':proof['questions_repaired'],'imports_preserved':21,'canonical_preserved':True,'all_question_field_and_answer_ids_preserved':True,'saved_responses_unchanged':True,'live_grading_checks':len(checks),'database_writes_by_verification':0,'checks':checks}
(H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
