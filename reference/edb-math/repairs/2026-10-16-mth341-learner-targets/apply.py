"""Add the missing MTH 341 coverage topics to Jake's explicit targets."""
import hashlib
import json
import sys
import threading
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import loads, dumps, kw
from scripts.storage import atomic_json, atomic_text

cfg = Config()
client = EDBClient(cfg, threading.Event())
snapshot = json.loads((HERE / 'snapshot.json').read_text())
identity = snapshot['identity']
learner = snapshot['learner']
missing = snapshot['missing']
source = ':person/jake'
idents = {str(i): eid for eid, i in loads((HERE / 'idents.edn').read_text())}
expected = {(learner[':db/id'], t[':db/id']) for t in missing}
transaction = dumps([
    [kw('db/add'), [kw('learner/id'), learner[':learner/id']], kw('learner/targets'),
     [kw('topic/id'), uuid.UUID(t[':topic/id'])]] for t in missing
]) + '\n'
digest = hashlib.sha256(transaction.encode()).hexdigest()

def check(report):
    actual = set()
    for e, a, v, tx, contributor, added in report[':edb/tx-data']:
        if a == idents[':db/txInstant']:
            continue
        assert a == idents[':learner/targets'] and added is True
        assert contributor == idents[source]
        actual.add((e, v))
    assert actual == expected, (actual, expected)

if sys.argv[1] == 'preview':
    assert client.status() == identity, 'Database advanced; recheck before preparing a new request'
    assert missing, 'No changes needed'
    atomic_text(HERE / 'transaction.edn', transaction)
    preview = client.command('with', '--file', HERE / 'transaction.edn', '--source', source)
    atomic_text(HERE / 'preview.edn', preview)
    report = loads(preview)
    assert report[':edb/committed'] is False and report[':edb/db-before-t'] == identity['basis']
    check(report)
    if (HERE / 'request.json').exists():
        request = json.loads((HERE / 'request.json').read_text())
        assert request['transaction'] == transaction and request['basis'] == identity['basis']
    else:
        atomic_json(HERE / 'request.json', dict(identity, source=source, endpoint=cfg.endpoint,
                    request_key='mth341-targets-' + str(uuid.uuid4()),
                    transaction=transaction, sha256=digest))
    print(f'Preview verified: {len(expected)} target additions, no other material changes.')
elif sys.argv[1] == 'commit':
    request = json.loads((HERE / 'request.json').read_text())
    assert request['transaction'] == transaction and request['sha256'] == digest
    assert (HERE / 'transaction.edn').read_text() == transaction
    assert client.status()['lineage'] == request['lineage']
    check(loads((HERE / 'preview.edn').read_text()))
    receipt = HERE / 'receipt.edn'
    if not receipt.exists():
        # If outcome is unknown, rerun with this exact saved request and key.
        result = client.command('transact', '--file', HERE / 'transaction.edn',
             '--endpoint', request['endpoint'], '--request-key', request['request_key'],
             '--basis', request['basis'], '--source', request['source'], '--timeout-ms', 45000, timeout=55)
        atomic_text(receipt, result)
    report = loads(receipt.read_text())
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == request['basis']
    check(report)
    basis = report[':edb/db-after-t']
    after = client.query((HERE / 'learner-before-query.edn').read_text(),
                        loads((HERE / 'learner-before-inputs.edn').read_text()), HERE, 'learner-after', basis)
    assert len(after) == 1
    actual = after[0][0]
    old = loads((HERE / 'learner-before.edn').read_text())[0][0]
    old_targets = {t[':db/id'] for t in old[':learner/targets']}
    new_targets = {t[':db/id'] for t in actual[':learner/targets']}
    assert new_targets == old_targets | {t[':db/id'] for t in missing}
    assert {t[':db/id'] for t in snapshot['topics']} <= new_targets
    old.pop(':learner/targets'); actual.pop(':learner/targets')
    assert dumps(old) == dumps(actual), 'Unexpected learner changes'
    result = {'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
              'learner_id': learner[':learner/id'], 'learner_entity': learner[':db/id'],
              'targets_before': len(old_targets), 'targets_after': len(new_targets),
              'targets_added': len(expected), 'mth341_coverage_topics': len(snapshot['topics']),
              'all_mth341_coverage_topics_are_targets': True, 'existing_targets_preserved': True,
              'only_targets_and_transaction_metadata_changed': True}
    atomic_json(HERE / 'verification.json', result)
    print(json.dumps(result, indent=2))
else:
    raise ValueError('Choose preview or commit')
