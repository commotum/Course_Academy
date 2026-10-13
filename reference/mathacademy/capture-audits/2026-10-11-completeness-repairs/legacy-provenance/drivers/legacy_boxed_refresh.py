"""Finite sixteen-question original-source refresh; unchanged reviews stay cached."""
from pathlib import Path
import hashlib
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from scripts.legacy_recovery import (source_record, batches, batch_question, field_sources,
    review_batch, REVIEW_VALIDATOR_VERSION, SolverUnavailable)
from scripts.config import Config
from scripts.storage import read_json, atomic_json

repo = Path.cwd()
root = repo / 'reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance'
targets = set(read_json(root / 'boxed-phantom-independent-inventory.json')['decorated_question_ids'])
old_groups = [read_json(p) for p in sorted(root.glob('batch-*/source-records.json'))]
old_by_id = {i['question']['math_academy_id']: i for g in old_groups for i in g}
items = [{**i, 'question': source_record(Path(i['directory']), i['question']['math_academy_id'])}
         for g in old_groups for i in g]
groups = list(batches(items))
assert len(groups) == len(old_groups) == 220
selected = []; changed_ids = set(); expected_hashes = {}
for n, group in enumerate(groups):
    assert [i['question']['math_academy_id'] for i in group] == [i['question']['math_academy_id'] for i in old_groups[n]]
    expected_hashes[n] = hashlib.sha256(json.dumps(group, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    pending = []
    for i in group:
        mid = i['question']['math_academy_id']; old = old_by_id[mid]['question']; q = i['question']
        if old != q:
            assert mid in targets
            assert field_sources(old) == field_sources(q)
            pending.append(i); changed_ids.add(mid)
    if not pending:
        assert read_json(root / ('batch-%04d' % n) / 'result.json')['source_hash'] == expected_hashes[n]
        continue
    payload = batch_question(pending)
    forbidden = set(read_json(root / 'four-worker-export-proof-brace-refresh.json')['forbidden_keys'])
    def check(value):
        if isinstance(value, dict):
            assert not (set(value) & forbidden)
            for child in value.values(): check(child)
        elif isinstance(value, list):
            for child in value: check(child)
    check(payload)
    assert len(pending) <= 16 and len(payload['answer_fields']) <= 40 and len(payload['assets']) <= 30
    for asset in payload['assets']:
        assert Path(asset['path']).is_file()
        assert hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest() == asset['sha256']
    atomic_json(root / 'boxed-phantom-payloads' / ('batch-%04d.json' % n), payload)
    selected.append((n, group))
assert changed_ids == targets
wrapper = repo / 'reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/archived-codex'
assert '-c \'model_reasoning_effort="high"\'' in wrapper.read_text()
config = Config(account='foundations', solver_model='gpt-6.1-sol', codex_bin=str(wrapper))
assert config.solver_command is None
proof = {'questions': sorted(changed_ids), 'batches': [n for n, _ in selected],
         'model': config.solver_model, 'reasoning_effort': 'high', 'workers': 4,
         'recursively_checked_actual_payloads': True, 'forbidden_keys': sorted(forbidden),
         'credentials_read_or_exported': False, 'destination': 'Existing default Codex service',
         'unchanged_sibling_authored_reviews_reused': True, 'batch_limits': [16, 40, 30]}
atomic_json(root / 'boxed-phantom-export-proof.json', proof)
print(json.dumps({'selected': proof['batches'], 'changed_questions': len(changed_ids)}), flush=True)
stop = threading.Event()
def run(pair):
    n, group = pair; failures = 0
    while True:
        try: return review_batch(group, config, root, n, stop)
        except SolverUnavailable as error:
            failures += 1
            atomic_json(root / ('batch-%04d' % n) / 'pending-review.json',
                        {'error': str(error), 'retryable': error.retryable, 'failures': failures})
            if not error.retryable: raise
            stop.wait(min(config.recovery_max_delay, config.retry_delay * 2 ** min(failures - 1, 8)))
with ThreadPoolExecutor(max_workers=4) as pool:
    for result in as_completed([pool.submit(run, pair) for pair in selected]):
        value = result.result()
        print(json.dumps({'batch': value['batch'], 'supported': value['supported'], 'unavailable': value['unavailable']}), flush=True)
completed = [read_json(root / ('batch-%04d' % n) / 'result.json') for n in range(len(groups))]
assert all(r['source_hash'] == expected_hashes[n] and r['validator_version'] == REVIEW_VALIDATOR_VERSION for n, r in enumerate(completed))
ids = [r['id'] for batch in completed for r in batch['records']]
assert len(ids) == len(set(ids)) == 3440
totals = {'batches': 220, 'supported': sum(r['supported'] for r in completed),
          'unavailable': sum(r['unavailable'] for r in completed), 'total_questions': 3440,
          'total_batches': 220, 'evidence_version': 2, 'workers': 4, 'validator_version': REVIEW_VALIDATOR_VERSION}
prior = read_json(root / 'review-complete.json')
atomic_json(root / 'review-complete-versions' / ('before-boxed-refresh-' + str(time.time_ns()) + '.json'), prior)
atomic_json(root / 'progress.json', totals)
atomic_json(root / 'review-complete.json', {'completed_at': time.time(), **totals})
atomic_json(root / 'boxed-phantom-review-complete.json', {'completed_at': time.time(), **proof, **totals})
print(json.dumps(totals), flush=True)
