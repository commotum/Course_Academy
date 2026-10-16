"""Commit the reviewed legacy matrix repair and verify its exact db-after values."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
if '--lesson-equations' in sys.argv:
    HERE = HERE / 'lesson-equations'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads

intent = json.loads((HERE / 'commit-intent.json').read_text())
validation = json.loads((HERE / 'rendering-validation.json').read_text())
assert not validation['page_errors'] and len(validation['records']) == intent['fields']
assert all(not r['errors'] for r in validation['records'])
assert hashlib.sha256(Path(intent['file']).read_bytes()).hexdigest() == intent['sha256']
binary = '/home/jake/Developer/EDB/target/release/edb'
env = {**os.environ, 'EDB_POSTGRES_URL': 'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
common = ['--database', intent['database'], '--source', intent['source'], '--file', intent['file']]
receipt = HERE / 'receipt.edn'
if not receipt.exists():
    with (HERE / 'preview.edn').open('w') as output:
        subprocess.run([binary, 'with', *common], env=env, stdout=output, check=True, timeout=90)
saved = loads(receipt.read_text()) if receipt.exists() and receipt.stat().st_size else {}
if not saved.get(':edb/committed'):
    # An existing empty receipt may mean the reply was lost. Reconcile this
    # exact saved request and key, without generating another intent.
    with receipt.open('w') as output:
        subprocess.run([binary, 'transact', *common, '--endpoint', intent['endpoint'],
                        '--request-key', intent['request_key'], '--timeout-ms', '120000'],
                       env=env, stdout=output, timeout=150)
saved = loads(receipt.read_text())
assert saved.get(':edb/committed'), 'Outcome not confirmed; retain the exact request for reconciliation'
basis = saved[':edb/basis-t']
with (HERE / 'after.edn').open('w') as output:
    subprocess.run([binary, 'query', '--database', intent['database'], '--as-of', str(basis),
                    '--file', str(HERE / 'read-query.edn'), '--inputs', str(HERE / 'read-inputs.edn')],
                   env=env, stdout=output, check=True, timeout=90)
actual = {(eid, attr): text for eid, attr, text in loads((HERE / 'after.edn').read_text())}
expected = {(eid, attr): text for eid, attr, text in loads((HERE / 'expected.edn').read_text())}
assert actual == expected
report = {'basis': basis, 'verified_fields': len(actual), 'entities': intent['entities'],
          'request_key': intent['request_key'], 'exact_readback_matches': True}
(HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
