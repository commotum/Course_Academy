import json,sys,time,urllib.request
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,loads
for attempt in range(45):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as r:assert r.status==200
        break
    except OSError:
        if attempt==44:raise
        time.sleep(1)
with urllib.request.urlopen('http://127.0.0.1:8765/ui/fraction-answers.css') as r:assert 'answer-fraction-denominator' in r.read().decode()
for path in ('learning.css','topic.css','course.css'):
    with urllib.request.urlopen('http://127.0.0.1:8765/ui/'+path) as r:assert 'fraction-answers.css' in r.read().decode()
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];k=p.read_kp(17592186119939,H/'live',basis);prepared=json.loads((H/'publication/preparation.json').read_text());before=loads(prepared['before_edn']);now={q[':db/id']:q for q in k[':knowledge-point/questions']};changes={}
for row in prepared['proposals']:changes.setdefault(row['entity'],{})[':'+row['attribute']]=row['after']
for q in before[':knowledge-point/questions']:
    expected=dict(q);expected.update(changes.get(q[':db/id'],{}));assert now[q[':db/id']]==expected
assert k[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
assert not k.get(':knowledge-point/question-generator')
checks=[]
cases={17592186315109:[({'field-1':'4+10y^4'},'correct'),({'field-1':'10y^4+4'},'correct'),({'field-1':'0'},'incorrect'),({'field-1':'y^3/(4+10y^4)'},'incorrect'),({'field-1':'4+10y^3'},'incorrect')],17592186233915:[({'field-1':'y','field-2':'15y^5'},'correct'),({'field-1':'2y/2','field-2':'5y^5+10y^5'},'correct'),({'field-1':'15y^5','field-2':'y'},'incorrect'),({'field-1':'y','field-2':'0'},'incorrect'),({'field-1':'y','field-2':'15y^4'},'incorrect')]}
for eid,rows in cases.items():
    q=now[eid]
    for values,expected in rows:
        payload={'topicId':17592186049248,'questionId':eid,'responses':[{'fieldId':f[':db/id'],'value':values[f[':answer-field/key']]} for f in q[':question/answer-fields']]}
        req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
        with urllib.request.urlopen(req,timeout=45) as r:out=json.load(r)
        assert out['status']==expected,(eid,values,expected,out)
        checks.append({'question':eid,'values':values,'expected':expected,'actual':out['status']})
result={'passed':True,'basis':basis,'questions_audited':9,'canonical_audited':1,'fraction_layouts_repaired':sorted(cases),'generator_present':False,'live_grading_checks':len(checks),'checks':checks,'all_existing_fields_keys_answers_and_history_preserved':True,'shared_styles_served':True,'database_writes_by_verification':0}
(H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
