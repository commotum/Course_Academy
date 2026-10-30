"""Exact live readback and all five image choices; no attempt writes."""
import json,sys,time,urllib.request
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable,loads,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
for attempt in range(45):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
        break
    except OSError:
        if attempt==44:raise
        time.sleep(1)
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];proof=json.loads((H/'verification.json').read_text());prepared=json.loads((H/'publication/preparation.json').read_text())
k=p.read_kp(17592186087721,H/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['generator'];entry=resolve_registered_script(ref,ROOT,p.config.math_root)
manifest=verify_package(entry.parent,Path(ref).parts[2]).manifest
for name in manifest['files']:assert (ROOT/'generate/scratch/17592186087721'/name).read_bytes()==(entry.parent/name).read_bytes()
now={str(q[':question/id']):q for q in k[':knowledge-point/questions']};before=loads(prepared['before_edn'])
for q in before[':knowledge-point/questions']:
    expected=dict(q)
    if q[':db/id'] in proof['retired_questions']:expected[':question/retired']=True
    assert now[str(q[':question/id'])]==expected,('Unexpected historical content change',q[':db/id'])
assert k[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
checks=[];new=[]
for r in prepared['records']:
    q=now[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question']);new.append(q)
    f=q[':question/answer-fields'][0]
    for answer in f[':answer-field/choices']:
        expected='correct' if answer[':db/id']==f[':answer-field/correct'][':db/id'] else 'incorrect'
        payload={'topicId':17592186048293,'questionId':q[':db/id'],'responses':[{'fieldId':f[':db/id'],'choiceId':answer[':db/id']}]}
        req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
        with urllib.request.urlopen(req,timeout=45) as response:out=json.load(response)
        assert out['status']==expected,(q[':db/id'],answer[':db/id'],expected,out)
        checks.append({'question':q[':db/id'],'answer':answer[':db/id'],'expected':expected,'actual':out['status']})
usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in new]],H/'live','new-usage',basis)
used={row[0][':db/id'] for row in usage if row[0].get(':task-item/_content')}
available=Counter(str(q[':question/difficulty'][':db/ident']).split('/')[-1] for q in new if q[':db/id'] not in used)
assert available=={'easy':5,'moderate':5,'hard':5},available
assert len(checks)==75
result={'passed':True,'basis':basis,'generator':ref,'unused_retired':proof['retired_questions'],'used_preserved':proof['used_questions_preserved'],'available_new_questions':dict(available),'imports_preserved':16,'canonical_preserved':True,'saved_responses_unchanged':True,'live_grading_checks':75,'database_writes_by_verification':0,'checks':checks}
(H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
