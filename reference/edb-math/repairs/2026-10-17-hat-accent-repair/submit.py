"""Submit the verified, authorized repair; retries preserve exact request identity."""
import datetime, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import loads
from capture.scripts.database.client import StaleBasis
HERE = Path(__file__).resolve().parent
def save(name, value):
    target = HERE / name
    temporary = target.with_suffix(target.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(target)
plan = json.loads((HERE / 'plan.json').read_text())
tx = (HERE / 'transaction.edn').read_text()
assert hashlib.sha256(tx.encode()).hexdigest() == plan['transaction_sha256']
preview = json.loads((HERE / 'preview-verification.json').read_text())
assert preview['passed'] and not preview['committed']
assert preview['transaction_sha256'] == plan['transaction_sha256']
browser = json.loads((HERE / 'browser-validation.json').read_text())
assert browser['passed'] and browser['transaction_sha256'] == plan['transaction_sha256']
publisher = Publisher.from_environment(source=plan['source'])
status = publisher.client.status()
assert status['database'] == plan['database'] and status['lineage'] == plan['lineage']
if (HERE / 'commit-intent.json').exists():
    intent = json.loads((HERE / 'commit-intent.json').read_text())
    assert intent['transaction_edn'] == tx
    assert intent['transaction_sha256'] == plan['transaction_sha256']
    assert intent['basis'] == plan['snapshot_basis']
else:
    assert status['basis'] == plan['snapshot_basis'], 'Fresh basis needed before first submission'
    intent = {
        'database': plan['database'], 'expected_lineage': plan['lineage'],
        'basis': plan['snapshot_basis'], 'source_edn': plan['source'],
        'request_key': 'hat-accent-repair-b' + str(plan['snapshot_basis']) + '-' + plan['transaction_sha256'],
        'endpoint': publisher.config.endpoint, 'transaction_file': 'transaction.edn',
        'transaction_sha256': plan['transaction_sha256'], 'transaction_edn': tx,
        'submission_authorized': True,
        'authorization': "Let's fix those, and yes audit for this additional pattern. When you've prepared the fix go ahead and push to the database. don't wait for me.",
        'authorized_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status_before': status,
    }
    save('commit-intent.json', intent)
request = {key: value for key, value in intent.items() if key != 'transaction_edn'}
request.update({'state': 'submitted-outcome-pending', 'committed': None})
save('request.json', request)
try:
    output = publisher.client.command('transact', '--file', HERE / 'transaction.edn',
        '--endpoint', intent['endpoint'], '--source', intent['source_edn'],
        '--basis', intent['basis'], '--request-key', intent['request_key'],
        '--timeout-ms', '120000', timeout=240)
except StaleBasis as error:
    request.update({'state': 'explicit-stale-basis-rejection', 'committed': False, 'error': str(error)})
    save('request.json', request)
    raise
except BaseException as error:
    request['error'] = str(error)
    save('request.json', request)
    raise
(HERE / 'receipt.edn').write_text(output)
report = loads(output)
assert report[':edb/committed'] is True
assert report[':edb/db-before-t'] == intent['basis']
assert ':edb/report-error' not in report
request.update({'state': 'confirmed', 'committed': True, 'committed_basis': report[':edb/db-after-t']})
save('request.json', request)
print(json.dumps({k: v for k, v in request.items() if k not in ['authorization', 'status_before']}, indent=2))
