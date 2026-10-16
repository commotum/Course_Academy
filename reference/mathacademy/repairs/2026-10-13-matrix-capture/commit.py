"""Preview and commit the retained CAS batches with stable retry identities."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads

HERE = Path(__file__).resolve().parent
REVIEW = HERE
if sys.argv[1:] == ['--requested-topics-only']:
    HERE = HERE / 'requested-topics'
elif sys.argv[1:] == ['--pending-database-wide']:
    # Execution of this scope requires the user's explicit approval following
    # the automatic review rejection. Preparation is not permission to submit.
    HERE = HERE / 'pending-database-wide'
elif sys.argv[1:]:
    raise ValueError('Unknown commit scope')
intent = json.loads((HERE / 'commit-intent.json').read_text())
rendering = json.loads((REVIEW / 'rendering-validation.json').read_text())
assert not rendering['errors'] and not rendering['page_errors']
env = os.environ.copy()
env.setdefault('EDB_POSTGRES_URL', 'host=/tmp/edb-math port=55432 dbname=math user=edb_peer')
binary = '/home/jake/Developer/EDB/target/release/edb'
directory = HERE / 'commits'; directory.mkdir(exist_ok=True)
results = []
for index, batch in enumerate(intent['batches'], 1):
    path = Path(batch['file'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == batch['sha256']
    receipt = directory / f'{index:03}.edn'
    saved = loads(receipt.read_text()) if receipt.exists() and receipt.stat().st_size else {}
    if saved.get(':edb/committed'):
        report = saved
    else:
        common = ['--database', intent['database'], '--source', intent['source'], '--file', str(path)]
        # An existing receipt file can mean a lost reply. Reconcile the exact
        # retained request directly, without a fresh CAS preview or new key.
        if not receipt.exists():
            with (directory / f'{index:03}-preview.edn').open('w') as output:
                subprocess.run([binary, 'with', *common], env=env, stdout=output, check=True, timeout=180)
        with receipt.open('w') as output:
            result = subprocess.run([binary, 'transact', *common, '--endpoint', intent['endpoint'],
                                     '--request-key', batch['request_key'], '--timeout-ms', '120000'],
                                    env=env, stdout=output, timeout=150)
        report = loads(receipt.read_text()) if receipt.stat().st_size else {}
        if not report.get(':edb/committed'):
            raise RuntimeError(f'Commit not confirmed for batch {index}; retain the saved request key and intent')
    record = {'batch': index, 'basis': report[':edb/basis-t'], 'fields': batch['fields'],
              'request_key': batch['request_key'], 'replayed': report.get(':edb/replayed', False)}
    results.append(record)
    (HERE / 'commit-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Committed batch {index}/{len(intent["batches"])}: {batch["fields"]} fields at basis {record["basis"]}', flush=True)
print(f'Confirmed {sum(result["fields"] for result in results)} repaired fields', flush=True)
