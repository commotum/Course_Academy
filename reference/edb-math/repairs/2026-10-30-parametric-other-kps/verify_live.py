"""Read back both repairs and test canonical/incorrect complete responses."""
import json,sys,time,urllib.request
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,loads,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
for attempt in range(45):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
        break
    except OSError:
        if attempt==44:raise
        time.sleep(1)
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];reports=[];checks=[]
for kp in (17592186087717,17592186087736):
    h=H/str(kp);proof=json.loads((h/'verification.json').read_text());prepared=json.loads((h/'publication/preparation.json').read_text())
    k=p.read_kp(kp,h/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['generator']
    entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=verify_package(entry.parent,Path(ref).parts[2]).manifest
    for name in manifest['files']:assert (ROOT/f'generate/scratch/{kp}'/name).read_bytes()==(entry.parent/name).read_bytes()
    now={str(q[':question/id']):q for q in k[':knowledge-point/questions']};before=loads(prepared['before_edn'])
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in proof['unused_retired']:expected[':question/retired']=True
        assert now[str(q[':question/id'])]==expected
    assert k[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
    new=[]
    for r in prepared['records']:
        q=now[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question']);new.append(q)
        fields=q[':question/answer-fields'];correct=[{'fieldId':f[':db/id'],'value':f[':answer-field/correct'][':answer/value']} for f in fields]
        wrong=[dict(row) for row in correct];target=next(i for i,f in enumerate(fields) if f[':answer-field/key'] in ('field-1','result'))
        wrong[target]['value']='1' if wrong[target]['value']=='0' else '0'
        for responses,expected in ((correct,'correct'),(wrong,'incorrect')):
            payload={'topicId':17592186048293,'questionId':q[':db/id'],'responses':responses}
            request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
            with urllib.request.urlopen(request,timeout=45) as response:out=json.load(response)
            assert out['status']==expected,(kp,q[':db/id'],expected,out)
            checks.append({'kp':kp,'question':q[':db/id'],'expected':expected,'actual':out['status']})
    usage=p.client.query('[:find ?item :in $ [?q ...] :where [?item :task-item/content ?q]]',[[q[':db/id'] for q in new]],h/'live','new-usage',basis);assert not usage
    available=Counter(str(q[':question/difficulty'][':db/ident']).split('/')[-1] for q in new);assert available=={'easy':5,'moderate':5,'hard':5}
    reports.append({'kp':kp,'generator':ref,'unused_retired':proof['unused_retired'],'used_preserved':proof['used_preserved'],'available_new_questions':dict(available),'imports_and_canonical_preserved':True,'old_content_and_saved_responses_preserved':True})
# The ordinary range generator was examined but needed no change.
kp=17592186087722;before=json.loads((H/str(kp)/'before.json').read_text());now=p.read_kp(kp,H/str(kp)/'live',basis)
assert now[':knowledge-point/question-generator'][':question-generator/script']==before[':knowledge-point/question-generator'][':question-generator/script']
assert len(now[':knowledge-point/questions'])==len(before[':knowledge-point/questions'])
result={'passed':True,'basis':basis,'kps':reports,'unaffected_range_kp':kp,'live_grading_checks':len(checks),'checks':checks,'database_writes_by_verification':0}
(H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
