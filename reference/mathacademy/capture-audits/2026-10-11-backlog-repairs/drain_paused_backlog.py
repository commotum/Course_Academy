"""Drain the finite completed-capture queue after the user paused all runners."""
from pathlib import Path
import threading
import time

from scripts.config import Config
from scripts.database.pipeline import DatabasePipeline
from scripts.outbox import DatabaseWorker, FINAL
from scripts.storage import atomic_json, read_json

root = Path(__file__).resolve().parent
wrapper = root.parent / '2026-10-11-completeness-repairs' / 'archived-codex'
config = Config(account='foundations', solver_model='gpt-6.1-sol', codex_bin=str(wrapper))
stop = threading.Event()
worker = DatabaseWorker(config, stop, lambda: DatabasePipeline(config, stop))
manifest_path = root / 'paused-backlog-drain.json'
manifest = read_json(manifest_path)
if manifest is None:
    manifest = {'frozen_at': time.time(), 'captures': [
        {'spool': str(path), 'directory': item['capture_directory'],
         'account': item['account'], 'created_ns': item['created_ns']}
        for path, item in worker.pending()], 'outcomes': []}
    atomic_json(manifest_path, manifest)
    print('frozen completed captures', len(manifest['captures']), flush=True)
repeated = {}
while True:
    remaining = [row for row in manifest['captures']
                 if read_json(row['spool'], {}).get('status') not in FINAL]
    if not remaining:
        manifest['finished_at'] = time.time()
        atomic_json(manifest_path, manifest)
        print('finite paused backlog complete', flush=True)
        break
    pending = worker.pending()
    if any(str(path) not in {row['spool'] for row in manifest['captures']} for path, _ in pending):
        raise RuntimeError('New work arrived after the paused queue was frozen; scope must be reviewed')
    result = worker.process_one()
    if result.get('status') in FINAL:
        outcome = {'directory': result['capture_directory'], 'status': result['status'],
                   'result': result.get('result'), 'verified_at': time.time()}
        manifest['outcomes'].append(outcome)
        atomic_json(manifest_path, manifest)
        print(Path(outcome['directory']).name, outcome['status'],
              'omissions', len((outcome['result'] or {}).get('omissions', [])),
              'remaining', len(remaining) - 1, flush=True)
    elif result.get('capture_directory') and result.get('status') == 'pending':
        reason = str(result.get('error') or result.get('result', {}).get('reason'))
        key = (result['capture_directory'], reason)
        repeated[key] = repeated.get(key, 0) + 1
        manifest['last_pending'] = {'directory': key[0], 'reason': reason,
                                    'repeated': repeated[key], 'observed_at': time.time()}
        atomic_json(manifest_path, manifest)
        print('pending', Path(key[0]).name, reason, flush=True)
        if repeated[key] >= 3:
            raise RuntimeError('Repeated identical pending failure needs review before continuing')
    if result.get('status') not in FINAL:
        stop.wait(2)
