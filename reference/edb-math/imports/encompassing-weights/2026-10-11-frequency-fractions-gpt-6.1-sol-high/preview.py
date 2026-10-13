"""Preview the exact prepared request without committing and verify every fact."""
from collections import Counter
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
from scripts.database.client import EDBClient
from scripts.database.commit import connection_identity
from scripts.database.edn import loads


def read(name):
    return json.loads((FOLDER / name).read_text())


def main():
    request = read('request.json')
    transaction = (FOLDER / 'transaction.edn').read_text()
    digest = hashlib.sha256(transaction.encode()).hexdigest()
    assert request['transaction'] == transaction
    assert request['transaction_sha256'] == digest
    for manifest in request['evidence_manifests']:
        assert hashlib.sha256(Path(manifest['path']).read_bytes()).hexdigest() == manifest['sha256']
    config = Config(capture_only=True)
    assert all(request[k] == v for k, v in connection_identity(config).items())
    client = EDBClient(config, threading.Event())
    expected_identity = dict(database=request['database'], lineage=request['database_lineage'], basis=request['basis'])
    assert client.status() == expected_identity, 'Database changed; prepare a new bundle from fresh pinned reads.'
    output = client.command('with', '--file', FOLDER / 'transaction.edn', '--source', request['source'])
    (FOLDER / 'preview.edn').write_text(output)
    preview = loads(output)
    assert preview[':edb/committed'] is False and preview[':edb/speculative'] is True
    assert preview[':edb/db-before-t'] == request['basis']
    assert preview[':edb/db-after-t'] == request['basis'] + 1
    idents = {r[0][':db/ident']: r[0][':db/id'] for r in read('idents.json')}
    topics = {r[0][':topic/math-academy-id']: r[0][':db/id'] for r in read('topics.json')
              if ':topic/math-academy-id' in r[0]}
    tempids = preview[':edb/tempids']
    source_ref = loads(request['source'])
    source = tempids.get(source_ref, idents.get(source_ref))
    assert source is not None

    def resolve(ref):
        if isinstance(ref, list):
            assert ref[0] == ':topic/math-academy-id'
            return topics[ref[1]]
        if isinstance(ref, str):
            return tempids[ref] if ref in tempids else idents[ref]
        return ref

    expected = []
    expected_tempids = set()
    edges = 0
    for form in loads(transaction):
        entity = resolve(form[':db/id'])
        if isinstance(form[':db/id'], str) and form[':db/id'] in tempids:
            expected_tempids.add(form[':db/id'])
        for attr, value in form.items():
            if attr == ':db/id':
                continue
            if attr == ':topic/encompasses':
                for edge in value:
                    edge_id = resolve(edge[':db/id'])
                    expected_tempids.add(edge[':db/id'])
                    edges += 1
                    expected.append((entity, idents[attr], edge_id))
                    assert edge[':db/ensure'] == ':encompassing/validate'
                    for edge_attr, edge_value in edge.items():
                        if edge_attr in (':db/id', ':db/ensure'):
                            continue
                        if edge_attr == ':encompassing/topic':
                            edge_value = resolve(edge_value)
                        expected.append((edge_id, idents[edge_attr], edge_value))
            else:
                expected.append((entity, idents[attr], value))
    assert set(tempids) == expected_tempids
    assert edges == request['expected_new_relationships']
    actual = []
    timestamps = []
    for entity, attribute, value, tx, fact_source, added in preview[':edb/tx-data']:
        assert added is True and fact_source == source
        if attribute == idents[':db/txInstant']:
            assert entity == tx
            timestamps.append((entity, attribute, value))
        else:
            actual.append((entity, attribute, value))
    assert len(timestamps) == 1
    assert Counter(actual) == Counter(expected), 'Preview facts differ from the exact logical request.'
    after = client.status()
    assert after == expected_identity, 'Live database changed during the noncommitting preview.'
    verification = dict(
        status='verified noncommitting preview', committed=False, speculative=True,
        read_basis=request['basis'], speculative_after_basis=preview[':edb/db-after-t'],
        source_ident=request['source_ident'], speculative_source_entity=source,
        new_relationships=edges, new_source_entities=int(request['source_bootstrap_included']),
        domain_and_source_assertions=len(actual), timestamp_assertions=len(timestamps), retractions=0,
        all_facts_attributed_to_requested_source=True, exact_expected_facts_match=True,
        transaction_sha256=digest, preview_sha256=hashlib.sha256(output.encode()).hexdigest(),
        live_status_after_preview=after, database_writes=0,
        verified_at=datetime.now(timezone.utc).isoformat(),
        note='Preview entity IDs and the speculative basis are not durable or reserved. The exact prepared request remains unsubmitted.')
    (FOLDER / 'preview-verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    summary = read('summary.json')
    summary.update(status='prepared and previewed; not submitted', preview_verification='preview-verification.json')
    (FOLDER / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
