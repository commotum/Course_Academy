"""Verify the selection gate from live queue files, without database access."""
import collections
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from inventory_jobs import InventoryJobs, priority_key
from generator_priority import PRIORITY_POLICY

queue = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
with (queue / 'jobs.lock').open('r') as lock:
    fcntl.flock(lock, fcntl.LOCK_SH)
    cursor = json.loads((queue / 'cursor.json').read_text())
    assert cursor['ranking'] == PRIORITY_POLICY
    gate = cursor['selection_gate']
    selected = set(gate['selected_knowledge_points'])
    jobs = []
    for path in queue.glob('*.json'):
        if path.name == 'cursor.json':
            continue
        job = json.loads(path.read_text())
        if 'request' in job:
            job['_path'] = path
            job['_publication_recovery'] = InventoryJobs.publication_recovery(path, job)
            jobs.append(job)

active = [job for job in jobs if job.get('state') in {'pending', 'running'}]
outside = [job for job in active if job['request']['knowledgePoint'] not in selected]
if not gate['open']:
    assert all(job['_publication_recovery'] for job in outside), 'Unselected work remains runnable'
eligible = sorted((job for job in active if job['request'].get('jobKind', 'build') == 'build'
                   and job.get('retryAt', 0) <= time.time()),
                  key=lambda job: (not job['_publication_recovery'], priority_key(job['request']), job['key']))

def compact(job, rank=None):
    request = job['request']
    title = next((r.get('topic_title') for r in request.get('priority_reasons', [])
                  if r.get('topic_entity') == request['topic'] and r.get('topic_title')), None)
    return {**{key: request.get(key) for key in ('topic', 'knowledgePoint', 'jobKind',
             'purpose', 'relevance_tier', 'shortage', 'difficulty', 'priority_policy')},
            'topic_title': title, 'state': job['state'], 'worker_order': rank,
            'publication_recovery': job['_publication_recovery']}

top = []
topics = []
for rank, job in enumerate(eligible, 1):
    topic = job['request']['topic']
    if topic not in topics:
        if len(topics) == 5:
            break
        topics.append(topic)
    top.append(compact(job, rank))
arithmetic = {17592186049501, 17592186051020, 17592186049909, 17592186050549, 17592186050742}
result = {'captured_at_unix': time.time(), 'cursor': cursor,
          'database_reads': 0, 'queue_writes': 0,
          'pending_running_jobs': len(active),
          'lanes': dict(collections.Counter(job['request'].get('jobKind', 'build') for job in active)),
          'unselected_runnable_jobs': [compact(job) for job in outside],
          'first_five_topics': top,
          'arithmetic_job_states': dict(collections.Counter(job['state'] for job in jobs
              if job['request']['topic'] in arithmetic)),
          'previous_active_draft': [compact(job) for job in jobs
              if job['request']['knowledgePoint'] == 17592186152211]}
(HERE / 'queue-snapshot.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({
    'basis': cursor['basis'], 'policy': cursor['ranking'], 'gate_open': gate['open'],
    'selected_topics': gate['selected_topic_count'], 'selected_kps': len(selected),
    'missing_generators': len(gate['missing_generators']),
    'understocked_kps': len(gate['understocked_knowledge_points']),
    'pending_running_jobs': len(active), 'unselected_runnable_jobs': len(outside),
    'arithmetic_job_states': result['arithmetic_job_states'],
    'first_five_topics': top,
}, indent=2))
