"""Read back the lesson and grade complete responses without saving attempts."""
import copy,json,sys,time,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
L=H.parent/'2026-11-03-latex-17592186247132';KPS=(17592186115398,17592186115399,17592186115400,17592186115401)

def updated(value,rows):
    result=copy.deepcopy(value);changes={}
    for row in rows:changes.setdefault(row['entity'],[]).append(row)
    def walk(node):
        if isinstance(node,dict):
            for row in changes.get(node.get(':db/id'),[]):
                key=':'+row['attribute']
                if key in node:
                    assert node[key]==row['before'] or node[key]==row['after']
                    node[key]=row['after']
            for child in node.values():walk(child)
        elif isinstance(node,list):
            for child in node:walk(child)
    walk(result);return result

def main():
    for i in range(30):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
            break
        except OSError:
            if i==29:raise
            time.sleep(1)
    p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];checks=[];skipped=[];entities=[]
    lesson=json.loads((L/'proposals.json').read_text());global_rows=json.loads((H/'proposals.json').read_text())
    for kp in KPS:
        old=json.loads((L/f'kp-{kp}.json').read_text());now=jsonable(p.read_kp(kp,H/'live'/str(kp),basis))
        assert now==updated(updated(old,lesson),global_rows)
        for q in now[':knowledge-point/questions']:
            fields=q.get(':question/answer-fields',[])
            if not fields or any(not f.get(':answer-field/correct') for f in fields):skipped.append(q[':db/id']);continue
            responses=[]
            for f in fields:
                kind=f[':answer-field/type'][':db/ident'];correct=f[':answer-field/correct']
                response={'fieldId':f[':db/id']}
                if kind in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):response['choiceId']=correct[':db/id']
                else:response['value']=correct[':answer/value']
                responses.append(response)
            variants=[(responses,'correct')]
            for i,f in enumerate(fields):
                if f[':answer-field/type'][':db/ident'] not in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):continue
                for a in f[':answer-field/choices']:
                    if a[':db/id']==f[':answer-field/correct'][':db/id']:continue
                    wrong=[dict(r) for r in responses];wrong[i]['choiceId']=a[':db/id'];variants.append((wrong,'incorrect'))
            for responses,expected in variants:
                payload={'topicId':17592186049402,'questionId':q[':db/id'],'responses':responses}
                request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
                with urllib.request.urlopen(request,timeout=45) as response:out=json.load(response)
                assert out['status']==expected,(q[':db/id'],expected,out)
                checks.append({'question':q[':db/id'],'expected':expected,'actual':out['status']})
            entities.append(q[':db/id'])
    report={'passed':True,'basis':basis,'complete_questions_graded':len(entities),'live_grading_checks':len(checks),
        'partial_imports_preserved_without_inventing_keys':skipped,'checks':checks,
        'all_four_kps_exactly_match_operator_only_changes':True,'database_writes':0,'service_healthy':True}
    (H/'live-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
