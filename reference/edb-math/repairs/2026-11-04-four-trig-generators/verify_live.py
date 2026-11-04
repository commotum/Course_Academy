"""Read-only native grading and final active-inventory verification."""
import collections
import concurrent.futures
import json
from pathlib import Path
import sys
import urllib.request

H = Path(__file__).resolve().parent; ROOT = H.parents[3]; sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher

TOPICS = {17592186048319: (17592186059665, 17592186059666, 17592186059821),
          17592186049773: (17592186059662, 17592186059663, 17592186059820),
          17592186048703: (17592186087669, 17592186087670, 17592186087671),
          17592186048362: (17592186059671, 17592186059672, 17592186059673, 17592186059674)}


def grade(args):
    topic, qid, responses, expected = args
    payload = {'topicId': topic, 'questionId': qid, 'responses': responses}
    request = urllib.request.Request('http://127.0.0.1:8765/api/preview-answer', data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'Origin': 'http://127.0.0.1:8765'}, method='POST')
    with urllib.request.urlopen(request, timeout=60) as response: out = json.load(response)
    assert out['status'] == expected, (qid, expected, out.get('status'), out.get('error'))
    return {'question': qid, 'expected': expected, 'actual': out['status']}


def response_key(q):
    responses = []
    for f in q[':question/answer-fields']:
        row = {'fieldId': f[':db/id']}
        if str(f[':answer-field/type'][':db/ident']).endswith(('/radio', '/select')):
            row['choiceId'] = f[':answer-field/correct'][':db/id']
        else: row['value'] = f[':answer-field/correct'][':answer/value']
        responses.append(row)
    return responses


def main():
    proof = json.loads((H / 'verification.json').read_text()); assert proof['passed']
    p = Publisher.from_environment(source=':agent/codex'); basis = p.client.status()['basis']
    tasks = []; inventories = {}; history_questions = []; new_ids = []
    for publication in proof['kps']:
        kid = publication['kp']; topic = next(t for t, kids in TOPICS.items() if kid in kids)
        kp = p.read_kp(kid, H / 'live' / str(kid), basis)
        assert kp[':knowledge-point/question-generator'][':question-generator/script'] == publication['generator']
        questions = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
        assert all(questions[eid][':question/retired'] is True for eid in publication['retired'])
        counts = collections.Counter()
        for q in questions.values():
            fs = q.get(':question/answer-fields', [])
            if not q.get(':question/retired') and fs and all(f.get(':answer-field/correct') for f in fs):
                d = q.get(':question/difficulty')
                if d: counts[str(d[':db/ident']).split('/')[-1]] += 1
        assert all(counts[b] >= 5 for b in ('easy', 'moderate', 'hard')), (kid, counts)
        inventories[str(kid)] = dict(counts)
        for published in publication['new_questions']:
            q = questions[published['entity']]; new_ids.append(q[':db/id'])
            assert not q.get(':question/retired') and not q.get(':question/math-academy-id')
            fields = q[':question/answer-fields']; correct = response_key(q)
            tasks.append((topic, q[':db/id'], correct, 'correct'))
            for i, f in enumerate(fields):
                if 'choiceId' in correct[i]:
                    for a in f[':answer-field/choices']:
                        if a[':db/id'] == correct[i]['choiceId']: continue
                        wrong = [dict(row) for row in correct]; wrong[i]['choiceId'] = a[':db/id']
                        tasks.append((topic, q[':db/id'], wrong, 'incorrect'))
                else:
                    wrong = [dict(row) for row in correct]
                    wrong[i]['value'] = '1' if correct[i]['value'] == '0' else '0'
                    tasks.append((topic, q[':db/id'], wrong, 'incorrect'))
        history_questions += publication['retired_with_preserved_task_items']
        if publication['retired_with_preserved_task_items']:
            q = questions[publication['retired_with_preserved_task_items'][0]]
            tasks.append((topic, q[':db/id'], response_key(q), 'correct'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor: checks = list(executor.map(grade, tasks))
    result = {'passed': True, 'basis': basis, 'generators_registered': len(proof['kps']),
        'retired_from_future_practice': proof['retired'], 'new_questions': len(new_ids),
        'retired_questions_with_preserved_history': history_questions,
        'active_complete_inventory_by_band': inventories, 'live_grading_checks': len(checks),
        'database_writes_by_verification': 0, 'checks': checks}
    (H / 'completion.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('checks', 'active_complete_inventory_by_band', 'retired_questions_with_preserved_history')}))


if __name__ == '__main__': main()
