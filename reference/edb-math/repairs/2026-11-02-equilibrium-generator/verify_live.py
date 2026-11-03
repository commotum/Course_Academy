"""Verify deployment, preserved responses, fresh stock and live checkbox grading."""
import json,subprocess,sys,time,urllib.request
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,loads,normalized_question
from scripts.generator_packages import resolve_registered_script,verify_package
KP=17592186166788;TOPIC=17592186051068

def main():
    for attempt in range(45):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2) as response:assert response.status==200
            break
        except OSError:
            if attempt==44:raise
            time.sleep(1)
    p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis']
    proof=json.loads((H/'verification.json').read_text());prepared=json.loads((H/'publication/preparation.json').read_text())
    k=p.read_kp(KP,H/'live',basis);ref=k[':knowledge-point/question-generator'][':question-generator/script'];assert ref==proof['generator']
    entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=verify_package(entry.parent,Path(ref).parts[2]).manifest
    for name in manifest['files']:assert (ROOT/f'generate/scratch/{KP}'/name).read_bytes()==(entry.parent/name).read_bytes()
    pool=json.loads((H/'candidate-pool.json').read_text())
    for i,band in enumerate(('easy','moderate','hard')):
        output=subprocess.check_output([sys.executable,str(entry),'--difficulty',band,'--count','5','--seed',str(202611020+i),'--format','json'],text=True)
        assert json.loads(output)==[r for r in pool if r['question'][':question/difficulty'].endswith('/'+band)]
    now={str(q[':question/id']):q for q in k[':knowledge-point/questions']};before=loads(prepared['before_edn'])
    for q in before[':knowledge-point/questions']:
        expected=dict(q)
        if q[':db/id'] in proof['unused_retired']:expected[':question/retired']=True
        for proposal in prepared['reported_question_repairs']:
            if q[':db/id']==proposal['entity']:expected[':'+proposal['attribute']]=proposal['after']
        assert now[str(q[':question/id'])]==expected
    assert k[':knowledge-point/canonical-example']==before[':knowledge-point/canonical-example']
    assert k[':knowledge-point/level-coverage']==before[':knowledge-point/level-coverage']
    new=[]
    for r in prepared['records']:
        q=now[r['question'][':question/id']];assert normalized_question(q)==normalized_question(r['question']);new.append(q)
    target=next(q for q in now.values() if q[':db/id']==17592186694294);checks=[]
    for q in new+[target]:
        fields=q[':question/answer-fields'];correct=[{'fieldId':f[':db/id'],'choiceId':f[':answer-field/correct'][':db/id']} for f in fields]
        variants=[(correct,'correct')]
        for i,field in enumerate(fields):
            wrong=[dict(row) for row in correct]
            wrong[i]['choiceId']=next(a[':db/id'] for a in field[':answer-field/choices'] if a[':db/id']!=correct[i]['choiceId'])
            variants.append((wrong,'incorrect'))
        for responses,expected in variants:
            payload={'topicId':TOPIC,'questionId':q[':db/id'],'responses':responses}
            request=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
            with urllib.request.urlopen(request,timeout=45) as response:out=json.load(response)
            assert out['status']==expected,(q[':db/id'],expected,out)
            checks.append({'question':q[':db/id'],'expected':expected,'actual':out['status']})
    usage=p.client.query('[:find ?item :in $ [?q ...] :where [?item :task-item/content ?q]]',[[q[':db/id'] for q in new]],H/'live','new-usage',basis);assert not usage
    available=Counter(str(q[':question/difficulty'][':db/ident']).split('/')[-1] for q in new);assert available=={'easy':5,'moderate':5,'hard':5}
    result={'passed':True,'basis':basis,'kp':KP,'topic':TOPIC,'generator':ref,'unused_retired':proof['unused_retired'],
        'used_preserved':proof['used_preserved'],'reported_question_equivalent_prompt_and_solution_repaired':17592186694294,
        'available_new_questions':dict(available),'imports_canonical_and_observed_levels_preserved':True,
        'all_existing_field_answer_identities_keys_and_saved_responses_preserved':True,'live_grading_checks':len(checks),
        'checks':checks,'database_writes_by_verification':0}
    (H/'completion.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key!='checks'},indent=2))

if __name__=='__main__':main()
