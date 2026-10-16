"""Commit the reviewed legacy matrix repair and verify its exact db-after values."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
HERE = REVIEW
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps
intent = json.loads((HERE / 'commit-intent.json').read_text())
validation = json.loads((HERE / 'rendering-validation.json').read_text())
assert validation['input_sha256'] == hashlib.sha256((HERE / 'all-expected.edn').read_bytes()).hexdigest()
expected = {(eid, attr): text for eid, attr, text in loads((HERE / 'expected.edn').read_text())}
selected = [r for r in validation['records'] if (int(r['id']), r['attribute']) in expected]
assert not validation['page_errors'] and len(selected) == intent['fields']
assert all(not r['errors'] and not r['exposed'] for r in selected)
for record in selected:
    for system in record['systems']:
        assert system['braceHeight'] >= system['tableHeight'] * .9
        assert len(system['equals']) >= 1 and max(system['equals']) - min(system['equals']) < .5
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
assert receipt.exists() and receipt.stat().st_size, 'Outcome not confirmed; retain request and key'
saved = loads(receipt.read_text())
assert saved.get(':edb/committed'), 'Outcome not confirmed; retain the exact request for reconciliation'
basis = saved[':edb/basis-t']
keys = loads((HERE / 'read-inputs.edn').read_text())[0]
readback = []
for offset in range(0, len(keys), 500):
    inputs = HERE / f'verification-inputs-{offset // 500:03}.edn'
    inputs.write_text(dumps([keys[offset:offset + 500]]))
    output_file = HERE / f'verification-read-{offset // 500:03}.edn'
    with output_file.open('w') as output:
        subprocess.run([binary, 'query', '--database', intent['database'], '--as-of', str(basis),
                        '--file', str(HERE / 'read-query.edn'), '--inputs', str(inputs),
                        '--max-value-bytes', '2147483648', '--max-join-bytes', '536870912'],
                       env=env, stdout=output, check=True, timeout=90)
    readback.extend(loads(output_file.read_text()))
(HERE / 'after.edn').write_text(dumps(readback))
actual = {(eid, attr): text for eid, attr, text in loads((HERE / 'after.edn').read_text())}
expected = {(eid, attr): text for eid, attr, text in loads((HERE / 'expected.edn').read_text())}
assert actual == expected
report = {'basis': basis, 'verified_fields': len(actual), 'entities': intent['entities'],
          'request_key': intent['request_key'], 'exact_readback_matches': True}
(HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
