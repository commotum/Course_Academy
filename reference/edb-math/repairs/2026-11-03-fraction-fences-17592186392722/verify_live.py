"""Verify served keys and responses without recording learner attempts."""
import importlib.util,json,sys,time,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable,loads
spec=importlib.util.spec_from_file_location('fence_deploy',H/'deploy.py');deploy=importlib.util.module_from_spec(spec);spec.loader.exec_module(deploy)

def main():
    for i in range(30):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
            break
        except OSError:
            if i==29:raise
            time.sleep(1)
    p=Publisher.from_environment(source=':agent/codex');head=p.client.status()['basis'];basis=json.loads((H/'verification.json').read_text())['basis_after'];proposals=json.loads((H/'proposals.json').read_text())
    affected={r['entity'] for r in json.loads((H/'audit.json').read_text())['questions_affected']};checks=[];skipped=[];collision_count=0
    prepared=json.loads((H/'publication/preparation.json').read_text())
    expected=jsonable(deploy.reader.patched(loads(prepared['kps_edn']),proposals))
    for kp in deploy.KPS:
        now=jsonable(p.read_kp(kp,H/'live'/str(kp),basis));assert now==expected[str(kp)]
        for q in now[':knowledge-point/questions']+[now[':knowledge-point/canonical-example']]:
            if q[':db/id'] not in affected:continue
            fields=q.get(':question/answer-fields',[])
            if not fields or any(not f.get(':answer-field/correct') for f in fields):skipped.append(q[':db/id']);continue
            correct=[]
            for f in fields:
                kind=f[':answer-field/type'][':db/ident'];a=f[':answer-field/correct'];row={'fieldId':f[':db/id']}
                if kind in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):row['choiceId']=a[':db/id']
                else:row['value']=a[':answer/value']
                correct.append(row)
                if kind in (':answer-field.type/radio',':answer-field.type/select'):
                    values=[a[':answer/value'] for a in f[':answer-field/choices']];collision_count+=len(values)-len(set(values))
            variants=[(correct,'correct')]
            for i,f in enumerate(fields):
                if f[':answer-field/type'][':db/ident'] not in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):continue
                for a in f[':answer-field/choices']:
                    if a[':db/id']==f[':answer-field/correct'][':db/id']:continue
                    wrong=[dict(r) for r in correct];wrong[i]['choiceId']=a[':db/id'];variants.append((wrong,'incorrect'))
            for responses,status in variants:
                payload={'topicId':17592186048999,'questionId':q[':db/id'],'responses':responses}
                request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
                with urllib.request.urlopen(request,timeout=45) as response:result=json.load(response)
                assert result['status']==status,(q[':db/id'],status,result);checks.append({'question':q[':db/id'],'expected':status,'actual':result['status']})
    assert not collision_count
    result={'passed':True,'basis':basis,'head_at_verification':head,'live_grading_checks':len(checks),'checks':checks,'partial_imports_preserved':skipped,
        'duplicate_choices':collision_count,'all_three_knowledge_points_read_back_exactly':True,'database_writes':0,'service_healthy':True}
    (H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
