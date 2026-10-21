"""Verify live build/refill admission from queue files; no database reads."""
import collections
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_priority import PRIORITY_POLICY
from inventory_jobs import InventoryJobs

queue = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
with (queue / 'jobs.lock').open() as lock:
    fcntl.flock(lock, fcntl.LOCK_SH)
    cursor = json.loads((queue / 'cursor.json').read_text())
    assert cursor['ranking'] == PRIORITY_POLICY, 'Waiting for refreshed live policy'
    gate = cursor['selection_gate']
    selected = set(gate['selected_knowledge_points'])
    jobs = []
    for path in queue.glob('*.json'):
        job = json.loads(path.read_text())
        if 'request' not in job:
            continue
        request = job['request']
        jobs.append({'knowledge_point': request['knowledgePoint'],
                     'topic': request['topic'],
                     'lane': request.get('jobKind', 'build'),
                     'state': job['state'], 'stage': request.get('stage'),
                     'selected': request['knowledgePoint'] in selected,
                     'publication_recovery': InventoryJobs.publication_recovery(path, job)})

active = [job for job in jobs if job['state'] in {'pending', 'running'}]
outside_builds = [job for job in active if job['lane'] == 'build' and not job['selected']]
if not gate['open']:
    assert all(job['publication_recovery'] for job in outside_builds), outside_builds
result = {'captured_at_unix': time.time(), 'policy': cursor['ranking'],
          'basis': cursor['basis'], 'gate_open': gate['open'],
          'selected_topics': gate['selected_topic_count'],
          'selected_kps': len(selected), 'database_reads': 0, 'queue_writes': 0,
          'runnable_by_lane': dict(collections.Counter(job['lane'] for job in active)),
          'unselected_runnable_builds': outside_builds,
          'unselected_refill_states': dict(collections.Counter(job['state'] for job in jobs
              if job['lane'] == 'refill' and not job['selected'])),
          'running': [job for job in active if job['state'] == 'running']}
(HERE / 'queue-snapshot.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
