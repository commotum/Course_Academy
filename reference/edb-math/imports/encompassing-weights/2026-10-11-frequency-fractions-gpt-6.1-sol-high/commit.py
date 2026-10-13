"""Submit the authorized encompassing request and verify its exact durable facts.

On recovery, reuse the saved request and key; never prepare new intent over it.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import runpy
import sys
import threading

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient, StaleBasis
from scripts.database.commit import Committer
from scripts.database.edn import dumps, loads
from scripts.storage import atomic_json
from scripts import prepare_encompassing_weights as preparation

SOURCE = ':agent/gpt-6.1-sol-high'


def read(name):
    return json.loads((FOLDER / name).read_text())


def normalized(report, idents, source):
    labels = {eid: name for name, eid in report[':edb/tempids'].items()}
    refs = {idents[':topic/encompasses'], idents[':encompassing/topic']}
    facts, timestamps = [], []
    for entity, attr, value, tx, fact_source, added in report[':edb/tx-data']:
        assert added is True, 'Unexpected retraction'
        assert fact_source == source, 'Unexpected contributor'
        if attr == idents[':db/txInstant']:
            assert entity == tx
            timestamps.append(tx)
            continue
        facts.append((labels.get(entity, entity), attr,
                      labels.get(value, value) if attr in refs else value))
    assert len(timestamps) == 1
    return Counter(facts), timestamps[0]


def main():
    if (FOLDER / 'superseded.json').exists():
        raise ValueError('Do not submit a superseded request')
    config = Config()
    client = EDBClient(config, threading.Event())
    if not (FOLDER / 'request.json').exists():
        runpy.run_path(str(FOLDER / 'read_snapshot.py'), run_name='__main__')
        idents = {r[0][':db/ident']: r[0][':db/id'] for r in read('idents.json')}
        assert SOURCE in idents, 'Reuse the established model contributor'
        preparation.SOURCE_IDENT = SOURCE
        preparation.prepare(ROOT, FOLDER, ROOT / preparation.DEFAULT_EVIDENCE_FOLDER)
        old_folder = FOLDER.parent / '2026-10-11-frequency-fractions-r2'
        old = json.loads((old_folder / 'selected-relationships.json').read_text())
        current = read('selected-relationships.json')
        fields = ('source', 'target', 'weight', 'weight_fraction', 'selected_account',
                  'rising_activities', 'eligible_activities')
        assert [tuple(e[k] for k in fields) for e in current] == [tuple(e[k] for k in fields) for e in old], 'Approved weights changed'
        assert len(current) == 1730
        runpy.run_path(str(FOLDER / 'preview.py'), run_name='__main__')
    request = read('request.json')
    assert request['source'] == SOURCE and request['source_ident'] == SOURCE
    assert request['transaction_sha256'] == hashlib.sha256((FOLDER / 'transaction.edn').read_bytes()).hexdigest()
    preview_check = read('preview-verification.json')
    assert preview_check['transaction_sha256'] == request['transaction_sha256']
    assert preview_check['read_basis'] == request['basis']
    assert preview_check['exact_expected_facts_match'] is True
    committer = Committer(config, client, FOLDER)
    atomic_json(FOLDER / 'submission-state.json', {
        'status': 'submitting or reconciling exact request',
        'request_key': request['request_key'], 'transaction_sha256': request['transaction_sha256'],
        'source_ident': SOURCE, 'basis_guard': request['basis']})
    try:
        receipt = committer.submit(request)
    except StaleBasis:
        atomic_json(FOLDER / 'submission-state.json', {
            'status': 'confirmed stale-basis rejection; no commit',
            'request_key': request['request_key'], 'transaction_sha256': request['transaction_sha256']})
        raise
    assert receipt[':edb/committed'] is True
    assert receipt[':edb/db-before-t'] == request['basis']
    basis = receipt[':edb/db-after-t']
    assert basis == request['basis'] + 1
    idents = {r[0][':db/ident']: r[0][':db/id'] for r in read('idents.json')}
    source = idents[SOURCE]
    preview = loads((FOLDER / 'preview.edn').read_text())
    expected, _ = normalized(preview, idents, source)
    actual, tx = normalized(receipt, idents, source)
    assert actual == expected, 'Committed facts differ from validated preview'
    edge_tempids = {key: value for key, value in receipt[':edb/tempids'].items() if key.startswith('encompassing-')}
    assert len(edge_tempids) == request['expected_new_relationships'] == 1730
    assert len(actual) == 1730 * 4
    entities = sorted({d[0] for d in receipt[':edb/tx-data'] if d[1] != idents[':db/txInstant']})
    groups = [entities[start:start + 100] for start in range(0, len(entities), 100)]

    def fetch(index):
        return client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',
                            [groups[index]], FOLDER / 'verification-reads', 'facts-' + str(index), basis)

    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = [row for group in pool.map(fetch, range(len(groups))) for row in group]
    stored = {(e, a, dumps(v), s) for e, a, v, s in rows}
    written = {(e, a, dumps(v), s)
               for e, a, v, _, s, added in receipt[':edb/tx-data'] if a != idents[':db/txInstant']}
    assert written.issubset(stored), 'Committed assertions or attribution absent at db-after'
    edges = set(edge_tempids.values())
    expected_edge_facts = {fact for fact in written if fact[0] in edges}
    assert {fact for fact in stored if fact[0] in edges} == expected_edge_facts, 'Unexpected edge attributes'
    allowed = {idents[a] for a in (':topic/encompasses', ':encompassing/topic', ':encompassing/weight', ':encompassing/rationale')}
    assert {d[1] for d in receipt[':edb/tx-data'] if d[1] != idents[':db/txInstant']} == allowed
    verification = dict(
        status='committed and verified', committed=True, database=request['database'],
        database_lineage=request['database_lineage'], source_ident=SOURCE, source_entity=source,
        request_key=request['request_key'], transaction_sha256=request['transaction_sha256'],
        receipt_sha256=hashlib.sha256((FOLDER / 'receipt.edn').read_bytes()).hexdigest(),
        before_basis=request['basis'], committed_basis=basis, transaction_entity=tx,
        relationships=1730, source_topics=request['expected_updated_source_topics'],
        domain_assertions=len(actual), timestamp_assertions=1, retractions=0,
        approved_weights_unchanged=True, exact_preview_facts_match=True,
        all_facts_attributed_to_requested_source=True, all_assertions_read_back_at_committed_basis=True,
        learner_and_engine_facts_unchanged=True,
        verified_at=datetime.now(timezone.utc).isoformat())
    atomic_json(FOLDER / 'commit-verification.json', verification)
    atomic_json(FOLDER / 'submission-state.json', verification)
    summary = read('summary.json')
    summary.update(status='committed and verified', committed_basis=basis,
                   commit_verification='commit-verification.json')
    atomic_json(FOLDER / 'summary.json', summary)
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
