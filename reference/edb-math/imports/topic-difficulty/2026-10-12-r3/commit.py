"""Submit the authorized exact request and verify its committed database value.

Retries use the same saved key, forms, source, and basis guard. A saved confirmed
receipt is reused without resubmission. This script never creates new intent.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import threading

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient, StaleBasis
from scripts.database.commit import Committer
from scripts.database.edn import loads
from scripts.storage import atomic_json


def read(name):
    return json.loads((FOLDER / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not (FOLDER / 'superseded.json').exists(), 'Do not submit a superseded request'
    request = read('request.json')
    assert request['source'] == request['source_ident'] == ':agent/gpt-6.1-sol-high'
    assert request['transaction'] == (FOLDER / 'transaction.edn').read_text()
    assert request['transaction_sha256'] == digest(FOLDER / 'transaction.edn')
    assert request['evidence_sha256'] == digest(FOLDER / 'observations.json')
    assert request['current_policy_evidence_sha256'] == digest(FOLDER / 'current-policy-calibrations.json')
    preview_check = read('preview-verification.json')
    assert preview_check['transaction_sha256'] == request['transaction_sha256']
    assert preview_check['read_basis'] == request['basis'] and preview_check['exact_expected_facts_match']
    assert preview_check['preview_sha256'] == digest(FOLDER / 'preview.edn')
    idents = {ident: eid for eid, ident in read('idents.json')}
    source = idents[request['source']]
    topics = {r[0][':topic/math-academy-id']: r[0][':db/id'] for r in read('topics.json')
              if ':topic/math-academy-id' in r[0]}
    expected = []
    counts = Counter()
    for form in loads(request['transaction']):
        ref = form[':db/id']
        if isinstance(ref, list):
            assert ref[0] == ':topic/math-academy-id'
            entity = topics[ref[1]]
            attribute = ':topic/difficulty'
            assert form[':db/ensure'] == ':topic/difficulty-validate'
        else:
            assert isinstance(ref, int)
            entity = ref
            attribute = ':activity/expected-seconds'
            assert form[':db/ensure'] == ':activity/validate'
        assert set(form) == {':db/id', ':db/ensure', attribute}
        expected.append((entity, idents[attribute], form[attribute], source))
        counts[attribute] += 1
    assert counts[':topic/difficulty'] == request['intended_topics'] == 777
    assert counts[':activity/expected-seconds'] == request['intended_duration_updates'] == 429
    assert len({(e, a) for e, a, _, _ in expected}) == len(expected) == 1206
    client = EDBClient(Config(), threading.Event())
    atomic_json(FOLDER / 'submission-state.json', dict(
        status='submitting or reconciling exact request', request_key=request['request_key'],
        transaction_sha256=request['transaction_sha256'], source_ident=request['source_ident'],
        basis_guard=request['basis']))
    try:
        receipt = Committer(client.config, client, FOLDER).submit(request)
    except StaleBasis:
        atomic_json(FOLDER / 'submission-state.json', dict(
            status='confirmed stale-basis rejection; no commit', request_key=request['request_key'],
            transaction_sha256=request['transaction_sha256']))
        raise
    assert receipt[':edb/committed'] is True
    assert receipt[':edb/db-before-t'] == request['basis']
    basis = receipt[':edb/db-after-t']
    assert basis == request['basis'] + 1
    actual, timestamps = [], []
    for entity, attribute, value, tx, contributor, added in receipt[':edb/tx-data']:
        assert added is True, 'Unexpected retraction'
        assert contributor == source, 'Unexpected source attribution'
        if attribute == idents[':db/txInstant']:
            assert entity == tx
            timestamps.append(tx)
        else:
            actual.append((entity, attribute, value, contributor))
    assert Counter(actual) == Counter(expected), 'Committed scope differs from approved request'
    assert len(timestamps) == 1 and not receipt[':edb/tempids']
    pairs = sorted({(e, a) for e, a, _, _ in expected})
    groups = [pairs[start:start + 100] for start in range(0, len(pairs), 100)]

    def fetch(index):
        return client.query('[:find ?e ?a ?v ?s :in $ [[?e ?a]] :where [?e ?a ?v _ ?s]]',
                            [groups[index]], FOLDER / 'verification-reads', 'facts-' + str(index), basis)

    with ThreadPoolExecutor(max_workers=3) as pool:
        stored = [tuple(row) for group in pool.map(fetch, range(len(groups))) for row in group]
    assert Counter(stored) == Counter(expected), 'Stored values or provenance differ at committed db-after'
    verification = dict(
        status='committed and verified', committed=True, database=request['database'],
        database_lineage=request['database_lineage'], source_ident=request['source_ident'], source_entity=source,
        before_basis=request['basis'], committed_basis=basis, transaction_entity=timestamps[0],
        request_key=request['request_key'], transaction_sha256=request['transaction_sha256'],
        receipt_sha256=digest(FOLDER / 'receipt.edn'),
        topic_multipliers=counts[':topic/difficulty'], lesson_durations=counts[':activity/expected-seconds'],
        domain_assertions=len(actual), timestamp_assertions=1, retractions=0,
        exact_prepared_facts_match=True, all_values_and_sources_read_back_at_committed_basis=True,
        learner_and_policy_facts_unchanged=True, verified_at=datetime.now(timezone.utc).isoformat())
    atomic_json(FOLDER / 'commit-verification.json', verification)
    atomic_json(FOLDER / 'submission-state.json', verification)
    summary = read('summary.json')
    summary.update(status='committed and verified', committed_basis=basis,
                   commit_verification='commit-verification.json')
    atomic_json(FOLDER / 'summary.json', summary)
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
