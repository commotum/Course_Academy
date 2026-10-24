"""Read back the fresh pool and use the app's nonmutating answer preview."""
from collections import Counter
import json
from pathlib import Path
import sys
import urllib.request

H = Path(__file__).resolve().parent;ROOT = H.parents[3]
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher, normalized_question, jsonable
from scripts.generator_packages import resolve_registered_script, verify_package
from capture.scripts.storage import atomic_json


def main():
    publisher = Publisher.from_environment(source=':agent/codex');identity = publisher.client.status();basis = identity['basis']
    completion = json.loads((H/'completion.json').read_text());checks = [];all_new = [];grades = [];fresh_counts = Counter()
    for result in completion['knowledge_points']:
        kp = result['kp'];current = publisher.read_kp(kp,H/'live'/str(kp),basis)
        registration = current[':knowledge-point/question-generator'][':question-generator/script']
        assert registration == result['generator_reference']
        script = resolve_registered_script(registration,ROOT,publisher.config.math_root)
        verify_package(script.parent,Path(registration).parts[2])
        assert (ROOT/'generate/scratch'/f'{kp}.py').read_bytes() == script.read_bytes()
        assert (ROOT/'generate/inverse_trig.py').read_bytes() == (script.parent/'inverse_trig.py').read_bytes()
        current_q = {q[':db/id']:q for q in current[':knowledge-point/questions']}
        prepared = json.loads((H/'publication'/str(kp)/'preparation.json').read_text())
        expected = {r['question'][':question/id']:r for r in prepared['records']}
        new = []
        for entry in result['new_questions']:
            q = current_q[entry['entity']]
            assert not q.get(':question/retired') and not q.get(':question/math-academy-id')
            assert normalized_question(q) == normalized_question(expected[entry['uuid']]['question'])
            new.append(q);all_new.append(q[':db/id'])
        for band in ('easy','moderate','hard'):
            options = [q for q in new if str(q[':question/difficulty'][':db/ident']).endswith('/'+band)]
            # Exercise entered exact values in the definite KP, radio elsewhere.
            q = next((q for q in options if str(q[':question/answer-fields'][0][':answer-field/type'][':db/ident']).endswith('/blank')),options[0])
            responses = []
            for f in q[':question/answer-fields']:
                r = {'fieldId':f[':db/id']};correct = f[':answer-field/correct']
                if str(f[':answer-field/type'][':db/ident']).endswith('/blank'):r['value'] = correct[':answer/value']
                else:r['choiceId'] = correct[':db/id']
                responses.append(r)
            for wrong in (False,True) if band == 'easy' else (False,):
                submitted = [dict(r) for r in responses]
                if wrong:
                    f = q[':question/answer-fields'][0]
                    if 'value' in submitted[0]:submitted[0]['value'] = '987654321'
                    else:submitted[0]['choiceId'] = next(a[':db/id'] for a in f[':answer-field/choices'] if a[':db/id'] != f[':answer-field/correct'][':db/id'])
                payload = {'activityId':17592186064411,'questionId':q[':db/id'],'responses':submitted}
                request = urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),
                    headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
                with urllib.request.urlopen(request,timeout=60) as response:outcome = json.load(response)
                expected_status = 'incorrect' if wrong else 'correct';assert outcome['status'] == expected_status, outcome
                grades.append({'kp':kp,'band':band,'entity':q[':db/id'],'status':outcome['status'],'basis':outcome.get('basis')})
        checks.append({'kp':kp,'new_questions':len(new),'registration':registration,'local_entrypoint_matches':True,'package_verified':True})
    references = publisher.client.query('[:find (pull ?q [:db/id :question/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
        [all_new],H/'live','new-question-uses',basis)
    owners = {r[0][':db/id']:r[0].get(':task-item/_content',[]) for r in references};assert len(owners) == 102
    for result in completion['knowledge_points']:
        for q in result['new_questions']:
            if not owners[q['entity']]:fresh_counts[str(result['kp'])+'/'+q['band'].split('/')[-1]] += 1
    assert sum(fresh_counts.values()) == 102, fresh_counts
    atomic_json(H/'live-pool-verification.json',{'passed':True,'database_writes':0,'basis':basis,'new_fresh_questions':102,
        'fresh_counts':dict(fresh_counts),'checks':checks,'all_new_questions_without_saved_task_references':True})
    atomic_json(H/'live-grading-verification.json',{'passed':True,'database_writes':0,'checks':grades})
    print(json.dumps({'passed':True,'basis':basis,'new_fresh_questions':102,'live_grade_checks':len(grades)}))


if __name__ == '__main__':main()
