"""Regenerate the never-started Quiz 8 through the application's guarded action."""
import fcntl
import json
from pathlib import Path
import sys
import uuid

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/learning_api.rs').exists())
sys.path.insert(0, str(R / 'scripts'))
import serve_graph_explorer as server
from generator_publish import Publisher, jsonable

TASK = 17592186725208
OLD = 17592186725199
REQUEST = D / 'regeneration-request.json'
if not REQUEST.exists():
    REQUEST.write_text(json.dumps({'action': 'regenerate-assessment', 'activityId': OLD,
        'requestId': 'focused-quiz8-' + str(uuid.uuid4())}, indent=2) + '\n')
body = json.loads(REQUEST.read_text())
environment = server.database_environment('math')
binary = Path('/tmp/focused-api-binary').read_text().strip()
worker = server.NativeWorker([binary, 'math', server.DEFAULT_LEARNER,
    environment['EDB_ENDPOINT'], '--serve'], environment, 'focused-quiz8')
publisher = Publisher.from_environment(database='math')

TASK_QUERY = '''[:find (pull ?t [:db/id :learner-task/id
 {:learner-task/status [:db/ident]} :learner-task/items :learner-task/elapsed-seconds
 :learner-task/finished-at :learner-task/xp-earned
 {:learner-task/activity [:db/id :activity/id :activity/steps]}])
 :in $ ?t :where [?t :learner-task/id _]]'''
TOPICS_QUERY = '''[:find ?q ?topic ?title :in $ ?task
 :where [?task :learner-task/activity ?a] [?a :activity/steps ?st]
 [?st :step/content ?q] [?kp :knowledge-point/questions ?q]
 [?topic :topic/knowledge-points ?kp] [?topic :topic/title ?title]]'''
OWNER_QUERY = '''[:find ?l ?topic :in $ ?task
 :where [?l :learner/activity ?task] [?l :learner/targets ?topic]]'''

try:
    with (Path(environment['LEARNING_REQUEST_DIR']) / 'api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        response_path = D / 'regeneration-response.json'
        if not response_path.exists() or not json.loads(response_path.read_text()).get('ok'):
            status = publisher.client.status()
            before = publisher.client.query(TASK_QUERY, [TASK], D / 'before-db', 'task', status['basis'])
            assert len(before) == 1 and before[0][0][':learner-task/activity'][':db/id'] == OLD
            (D / 'before-task.json').write_text(json.dumps(jsonable(before), indent=2) + '\n')
            result = worker.request(body)
            response_path.write_text(json.dumps(result, indent=2) + '\n')
            assert result.get('ok'), result
        result = json.loads(response_path.read_text())
        assert result['data']['taskId'] == TASK
        assert result['data']['title'] == 'Quiz 8'
        status = publisher.client.status()
        after = publisher.client.query(TASK_QUERY, [TASK], D / 'after-db', 'task', status['basis'])[0][0]
        topics = publisher.client.query(TOPICS_QUERY, [TASK], D / 'after-db', 'topics', status['basis'])
        targets = publisher.client.query(OWNER_QUERY, [TASK], D / 'after-db', 'targets', status['basis'])
        target_ids = {row[1] for row in targets}
        assert topics and all(row[1] in target_ids for row in topics)
        assert len({row[0] for row in topics}) == len(after[':learner-task/activity'][':activity/steps'])
        assert after[':learner-task/activity'][':db/id'] != OLD
        assert str(after[':learner-task/status'][':db/ident']) == ':learner-task.status/unlocked'
        assert not after.get(':learner-task/items')
        assert not after.get(':learner-task/elapsed-seconds', 0)
        assert ':learner-task/finished-at' not in after and ':learner-task/xp-earned' not in after
        proof = {'passed': True, 'basis': status['basis'], 'task_id': TASK,
            'old_activity': OLD, 'new_activity': after[':learner-task/activity'][':db/id'],
            'title': result['data']['title'], 'question_count': len(topics),
            'all_questions_in_targets': True, 'topics': topics,
            'regeneration': result['data'].get('regeneration'), 'task': jsonable(after)}
        (D / 'quiz8-completion.json').write_text(json.dumps(proof, indent=2) + '\n')
        print(json.dumps({k: v for k, v in proof.items() if k not in ('topics', 'task')}, indent=2))
finally:
    worker.close()
