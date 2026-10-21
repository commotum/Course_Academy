"""Read-only selection support check with the actual captured inventory pool."""
import collections, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
inventory = json.loads((ROOT.parent / 'source/inventory.json').read_text())
batch = json.loads((ROOT / 'delivery-batch/accepted.json').read_text())
source_ids = {q[':question/id'] for q in json.loads((ROOT / 'source-extract.json').read_text())['questions']}
existing = sorted(inventory['questions'], key=lambda q: q[':db/id'])
prospective = [r['question'] for r in batch]
pool = existing + prospective
assert len({q[':question/id'] for q in pool}) == len(pool)
assert all(q[':question/difficulty'] in (':question.difficulty/hard', {':db/ident': ':question.difficulty/hard'}) for q in pool)
counts = collections.Counter()
for seed in range(1000):
    digest = hashlib.sha256(f'course-academy/question-selection/v1/independent-current-pool-{seed}'.encode()).digest()
    u = (int.from_bytes(digest[8:16], 'big') >> 11) / 2**53
    counts[int(u * len(pool))] += 1
assert len(counts) == len(pool)
records = []
for index, q in enumerate(pool):
    records.append({'question_id': q[':question/id'], 'entity_id': q.get(':db/id'), 'origin': 'prospective batch' if index >= len(existing) else ('original source' if q[':question/id'] in source_ids else 'existing non-source; generation provenance unavailable'), 'family': 'vector' if 'and then solve' in q[':question/problem'] else 'matrix', 'draw_count': counts[index]})
report = {'command': 'python3 selection_pool.py', 'basis': inventory['basis'], 'native_rule': 'engine/rust/question_selection.rs:132-216: unique eligible entity IDs sorted; positive hard weight selects uniformly by digest bytes 8..16 within all-hard pool.', 'captured_inventory_count': len(existing), 'surviving_batch_count': len(prospective), 'pool_size': len(pool), 'trials': 1000, 'records': records, 'all_eligible_support_observed': len(counts) == len(pool), 'no_policy_fallback_entity': existing[0][':db/id'], 'limits': ['Fresh learner with no history exclusions and positive hard-band weight. Active learner policy/history absent; no specific live task certified.', 'New entity IDs unavailable. Prospective IDs placed after existing IDs as one possible monotone allocation. Uniform support is invariant under their ordering.', 'Source and existing non-source instances remain in the captured pool; no provenance is invented for historical instances.', 'An unconfigured policy selects the lowest eligible entity ID; eligibility changes as task/history exclusions apply.'], 'database_writes': 0}
(ROOT / 'selection-pool-results.json').write_text(json.dumps(report, indent=2))
old = json.loads((ROOT / 'learner-selection-results.json').read_text())
old['combined_captured_pool'] = {'evidence': 'selection-pool-results.json', 'existing': len(existing), 'surviving_batch': len(prospective), 'support': 'All 27 eligible records selected under positive hard weight; source and prior non-source records included.'}
(ROOT / 'learner-selection-results.json').write_text(json.dumps(old, indent=2))
v = json.loads((ROOT / 'pedagogical-variation.json').read_text())
v['delivery']['sample_refs'].append('selection-pool-results.json')
v['delivery']['result'] += ' Combined captured inventory (22 records) plus surviving batch (5) also preserves all 27 records under fresh positive-hard-weight selection; prospective entity-ID ordering does not change uniform support.'
(ROOT / 'pedagogical-variation.json').write_text(json.dumps(v, indent=2))
print(json.dumps({'pool_size': len(pool), 'support': len(counts), 'families': dict(collections.Counter(r['family'] for r in records))}))
