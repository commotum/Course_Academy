"""Verify the preserved speculative report without regenerating or submitting intent."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, loads, kw


def verify():
    intent = json.loads((OUT / 'intent.json').read_text())
    transaction = OUT / 'transaction.edn'
    assert hashlib.sha256(transaction.read_bytes()).hexdigest() == intent['transaction_sha256']
    forms = loads(transaction.read_text())
    ids = {str(row[1]): row[0] for row in loads((OUT / 'schema-before.edn').read_text())}
    assert all(name not in ids for name in intent['attributes'])
    cli = ROOT / '.local/edb/capture-runtime/math-edb'
    env = os.environ.copy()
    env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"

    def run(args, destination):
        result = subprocess.run([str(cli), *args], env=env, capture_output=True, text=True,
                                check=True, timeout=45)
        (OUT / destination).write_text(result.stdout)
        return result.stdout

    # EDB generates an install marker for each new attribute, in addition to txInstant.
    (OUT / 'installation-query.edn').write_text(
        '[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]\n')
    (OUT / 'installation-inputs.edn').write_text(
        dumps([[kw('db.install/attribute'), kw('db.part/db')]]) + '\n')
    rows = loads(run(['query', '--database', intent['database'], '--as-of', str(intent['read_basis']),
                     '--file', str(OUT / 'installation-query.edn'),
                     '--inputs', str(OUT / 'installation-inputs.edn')], 'installation-before.edn'))
    ids.update({str(ident): eid for eid, ident in rows})
    preview = loads((OUT / 'preview.edn').read_text())
    assert preview[':edb/committed'] is False and preview[':edb/speculative'] is True
    assert preview[':edb/db-before-t'] == intent['read_basis']
    tempids = preview[':edb/tempids']
    assert set(tempids) == {form[kw('db/id')] for form in forms}
    explicit = set()
    for form in forms:
        assert set(form) == {kw(n) for n in ['db/id', 'db/ident', 'db/valueType', 'db/cardinality', 'db/doc']}
        eid = tempids[form[kw('db/id')]]
        for attr, value in form.items():
            if attr == kw('db/id'):
                continue
            stored = ids[str(value)] if attr in [kw('db/valueType'), kw('db/cardinality')] else value
            explicit.add((eid, ids[str(attr)], stored, True))
    installation = {(ids[':db.part/db'], ids[':db.install/attribute'], eid, True)
                    for eid in tempids.values()}
    datoms = preview[':edb/tx-data']
    assert all(d[4] == intent['source_entity'] for d in datoms)
    actual = {(d[0], d[1], d[2], d[5]) for d in datoms if d[1] != ids[':db/txInstant']}
    assert actual == explicit | installation, (actual, explicit | installation)
    assert len(explicit) == 8 and len(datoms) == 11 and all(d[5] is True for d in datoms)
    status = run(['status', '--database', intent['database']], 'status-after.txt')
    match = re.search(r'lineage=(\S+) basis_t=(\d+)', status)
    assert match and match.group(1) == intent['lineage']
    assert int(match.group(2)) == intent['read_basis'], 'Basis advanced; re-review before submission.'
    verification = {
        'preview_valid': True, 'committed': False, 'read_basis': intent['read_basis'],
        'live_basis_after_preview': int(match.group(2)),
        'schema_attributes_added_in_preview': 2, 'explicit_assertions': len(explicit),
        'automatic_attribute_installation_assertions': len(installation),
        'automatic_transaction_timestamp_assertions': 1, 'retractions': 0,
        'all_preview_datoms_have_expected_source': True,
        'transaction_datoms_match_exact_scope': True,
        'transaction_sha256': intent['transaction_sha256'], 'request_key': intent['request_key'],
    }
    (OUT / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    verify()
