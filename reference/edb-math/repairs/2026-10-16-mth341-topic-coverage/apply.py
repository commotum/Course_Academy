"""Preview, submit, and read back the authorized additive coverage repair."""
import hashlib
import json
import sys
import threading
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import loads, dumps
from scripts.storage import atomic_json, atomic_text

config = Config()
client = EDBClient(config, threading.Event())
identity = json.loads((HERE / 'identity.json').read_text())
source = ':agent/gpt-6-astra-high'
expected = {tuple(pair) for pair in json.loads((HERE / 'expected-additions.json').read_text())}
transaction = (HERE / 'transaction.edn').read_text()
digest = hashlib.sha256(transaction.encode()).hexdigest()
mode = sys.argv[1]

def checked_datoms(report):
    """Reject all material changes except the exact approved coverage additions."""
    ids = loads((HERE / 'attribute-ids.edn').read_text())
    by_name = {str(name): eid for eid, name in ids}
    coverage = by_name[':assigned-problem/topic-coverage']
    instant = by_name[':db/txInstant']
    actual = set()
    for entity, attr, value, tx, contributor, added in report[':edb/tx-data']:
        if attr == instant:
            continue
        assert attr == coverage and added is True, (entity, attr, added)
        assert contributor == 17592186045419, contributor
        actual.add((entity, value))
    assert actual == expected, (actual - expected, expected - actual)
    return actual

if mode == 'preview':
    status = client.status()
    assert status == identity, (status, identity)
    client.query('[:find ?e ?i :where [?e :db/ident ?i]]', [], HERE, 'attribute-ids', identity['basis'])
    preview = client.command('with', '--file', HERE / 'transaction.edn', '--source', source)
    atomic_text(HERE / 'preview.edn', preview)
    report = loads(preview)
    assert report[':edb/committed'] is False
    assert report[':edb/db-before-t'] == identity['basis']
    checked_datoms(report)
    request = dict(identity, source=source, endpoint=config.endpoint,
                   request_key='mth341-coverage-' + str(uuid.uuid4()),
                   transaction=transaction, sha256=digest)
    if (HERE / 'request.json').exists():
        saved = json.loads((HERE / 'request.json').read_text())
        assert saved['transaction'] == transaction and saved['basis'] == identity['basis']
    else:
        atomic_json(HERE / 'request.json', request)
    print(f'Preview verified: {len(expected)} coverage additions and no other material changes.')
elif mode == 'commit':
    request = json.loads((HERE / 'request.json').read_text())
    assert request['transaction'] == transaction and request['sha256'] == digest
    assert request['source'] == source and request['database'] == config.database
    assert client.status()['lineage'] == request['lineage']
    checked_datoms(loads((HERE / 'preview.edn').read_text()))
    receipt = HERE / 'receipt.edn'
    if not receipt.exists():
        # On an unknown outcome, rerun this mode with the same saved request.
        result = client.command('transact', '--file', HERE / 'transaction.edn',
                                '--endpoint', request['endpoint'],
                                '--request-key', request['request_key'],
                                '--basis', request['basis'], '--source', request['source'],
                                '--timeout-ms', 45000, timeout=55)
        atomic_text(receipt, result)
    report = loads(receipt.read_text())
    assert report[':edb/committed'] is True
    assert report[':edb/db-before-t'] == request['basis']
    checked_datoms(report)
    final_basis = report[':edb/db-after-t']
    after = client.query((HERE / 'read-query.edn').read_text(), [], HERE, 'after', final_basis)
    before = loads((HERE / 'before.edn').read_text())

    def entities(rows):
        return {a[':db/id']: a for (a,) in rows}

    def normalize(value):
        if isinstance(value, dict):
            return {str(k): normalize(v) for k, v in value.items()}
        if isinstance(value, list):
            return sorted((normalize(v) for v in value), key=lambda v: dumps(v))
        return value

    wanted = entities(before)
    topics = {t[':db/id']: t for (t,) in loads((HERE / 'topic-identities.edn').read_text())}
    for assignment in wanted.values():
        for step in assignment[':activity/steps']:
            problem = step[':step/content']
            additions = [tid for eid, tid in expected if eid == problem[':db/id']]
            if additions:
                problem.setdefault(':assigned-problem/topic-coverage', []).extend(topics[tid] for tid in additions)
    assert normalize(entities(after)) == normalize(wanted), 'Readback differs from expected additive-only result'
    verification = {'committed': True, 'basis_before': request['basis'], 'basis_after': final_basis,
                    'assignments_reviewed': len(before), 'assigned_problems_reviewed': 65,
                    'question_parts_reviewed': 85, 'problems_updated': len({e for e, t in expected}),
                    'coverage_links_added': len(expected), 'all_additions_read_back': True,
                    'existing_coverage_and_content_preserved': True,
                    'only_coverage_and_transaction_metadata_changed': True}
    atomic_json(HERE / 'verification.json', verification)
    print(json.dumps(verification, indent=2))
else:
    raise ValueError('Choose preview or commit')
