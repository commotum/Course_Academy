"""Inspect persisted priority metadata only; no database reads or queue writes."""
import collections
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from inventory_jobs import InventoryJobs, priority_key
from generator_priority import PRIORITY_POLICY

HERE = Path(__file__).resolve().parent
QUEUE = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
AUDIT = json.loads((HERE.parent / 'selected-topics-readiness-2026-10-17/result.json').read_text())
blocked = {t['topic']: t for t in AUDIT['topics'] if not t['content_ready_for_fresh_lesson']}
deficient = {kp['kp'] for topic in blocked.values() for kp in topic['knowledge_points'] if kp['needed']}
now = time.time()
with (QUEUE / 'jobs.lock').open('r') as lock:
    fcntl.flock(lock, fcntl.LOCK_SH)
    cursor = json.loads((QUEUE / 'cursor.json').read_text())
    jobs = []
    for path in QUEUE.glob('*.json'):
        if path.name == 'cursor.json':
            continue
        job = json.loads(path.read_text())
        if 'request' not in job:
            continue
        job['_path'] = path
        job['_publication_recovery'] = InventoryJobs.publication_recovery(path, job)
        jobs.append(job)

builds = [job for job in jobs if job['request'].get('jobKind', 'build') == 'build']
pending = [job for job in builds if job.get('state') in {'pending', 'running'}]
ranked = sorted(pending, key=lambda job: (priority_key(job['request']), job['key']))
eligible = sorted((job for job in pending if job.get('retryAt', 0) <= now),
                  key=lambda job: (not job['_publication_recovery'], priority_key(job['request']), job['key']))
ranks = {job['key']: i for i, job in enumerate(ranked, 1)}
worker = {job['key']: i for i, job in enumerate(eligible, 1)}

def compact(job):
    request = job['request']
    return {**{key: request.get(key) for key in (
        'topic', 'knowledgePoint', 'priority_policy', 'relevance_tier', 'purpose',
        'shortage', 'topic_layer', 'selected_support_count', 'engine_priority',
        'review_due_at', 'difficulty', 'jobKind', 'basis')},
        'state': job['state'], 'priority_rank': ranks.get(job['key']),
        'worker_order': worker.get(job['key']),
        'publication_recovery': job['_publication_recovery'],
        'backoff': job.get('retryAt', 0) > now,
        'path': str(job['_path'].relative_to(ROOT))}

selected = [compact(job) for job in builds if job['request']['knowledgePoint'] in deficient]
selected.sort(key=lambda job: job['priority_rank'] or float('inf'))
result = {
    'captured_at_unix': now, 'cursor': cursor,
    'database_reads': 0, 'queue_writes': 0,
    'readiness_reference_basis': AUDIT['basis'],
    'note': 'Persisted ranking snapshot. Worker may skip locked KPs; prior audit deficits are historical evidence, not a new readiness scan.',
    'build_states': dict(collections.Counter(job['state'] for job in builds)),
    'pending_running_builds': len(pending),
    'policies': dict(collections.Counter(job['request'].get('priority_policy', 'legacy') for job in pending)),
    'tier_purpose_counts': dict(collections.Counter(
        f"{job['request'].get('relevance_tier', 'legacy')}/{job['request'].get('purpose')}" for job in pending)),
    'top_20': [compact(job) for job in eligible[:20]],
    'previously_blocked_topics': [
        {'topic': topic, 'title': data['title'],
         'jobs': [job for job in selected if job['topic'] == topic]}
        for topic, data in blocked.items()],
    'previously_deficient_jobs': selected,
}
(HERE / 'queue-snapshot.json').write_text(json.dumps(result, indent=2) + '\n')
assert cursor.get('ranking') == PRIORITY_POLICY, cursor
assert all(job['request'].get('priority_policy') == PRIORITY_POLICY or job['_publication_recovery']
           for job in pending), 'An ordinary pending job retains the old ranking policy'
print(json.dumps({key: result[key] for key in ('cursor', 'policies', 'tier_purpose_counts')}, indent=2))
for row in selected:
    print(json.dumps({key: row[key] for key in ('topic', 'knowledgePoint', 'relevance_tier', 'purpose', 'shortage', 'topic_layer', 'priority_rank', 'worker_order', 'state')}))
