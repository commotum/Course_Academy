"""Submit/reconcile the exact approved schema request and verify its committed basis."""
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
from edn import loads, dumps, kw

intent = json.loads((OUT / 'intent.json').read_text())
transaction = OUT / 'transaction.edn'
assert hashlib.sha256(transaction.read_bytes()).hexdigest() == intent['transaction_sha256']
preview = loads((OUT / 'preview.edn').read_text())
assert preview[':edb/committed'] is False
assert json.loads((OUT / 'verification.json').read_text())['transaction_datoms_match_exact_scope']
cli = ROOT / '.local/edb/capture-runtime/math-edb'
env = os.environ.copy()
env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"


def run(args, name):
    result = subprocess.run([str(cli), *args], env=env, capture_output=True, text=True, timeout=60)
    (OUT / name).write_text(result.stdout)
    (OUT / (name + '.stderr.txt')).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError('Preserve and reconcile the exact request if submission outcome is unknown: ' + result.stderr)
    return result.stdout


receipt_path = OUT / 'receipt.edn'
if receipt_path.exists():
    receipt = loads(receipt_path.read_text())
else:
    # An existing submission marker may represent a lost response. In that case
    # replay the original request, allowing the writer to resolve its receipt.
    if not (OUT / 'submission.json').exists():
        status = run(['status', '--database', intent['database']], 'status-precommit.txt')
        match = re.search(r'lineage=(\S+) basis_t=(\d+)', status)
        assert match and match.group(1) == intent['lineage']
        assert int(match.group(2)) == intent['basis_guard'], 'Basis advanced; re-preview before first submission.'
        (OUT / 'submission.json').write_text(json.dumps({
            'request_key': intent['request_key'], 'transaction_sha256': intent['transaction_sha256'],
            'source': intent['source'], 'basis_guard': intent['basis_guard'],
            'authorization': 'User instructed "do it" after reviewing the exact two-attribute transaction.'
        }, indent=2) + '\n')
    output = run(['transact', '--database', intent['database'], '--endpoint', intent['endpoint'],
                  '--request-key', intent['request_key'], '--source', intent['source'],
                  '--basis', str(intent['basis_guard']), '--file', str(transaction),
                  '--timeout-ms', '30000'], 'commit.stdout.edn')
    receipt = loads(output)
    assert receipt[':edb/committed'] is True, 'No confirmed commit; retain original intent.'
    receipt_path.write_text(output)

assert receipt[':edb/committed'] is True
assert receipt[':edb/db-before-t'] == intent['basis_guard']
basis = receipt[':edb/db-after-t']
print('Confirmed commit at basis', basis, flush=True)
before_rows = loads((OUT / 'schema-before.edn').read_text())
ids = {str(row[1]): row[0] for row in before_rows}
ids.update({str(ident): eid for eid, ident in loads((OUT / 'installation-before.edn').read_text())})
forms = loads(transaction.read_text())
tempids = receipt[':edb/tempids']
assert set(tempids) == {f[kw('db/id')] for f in forms}
expected = set()
for form in forms:
    eid = tempids[form[kw('db/id')]]
    for attr, value in form.items():
        if attr == kw('db/id'):
            continue
        stored = ids[str(value)] if attr in [kw('db/valueType'), kw('db/cardinality')] else value
        expected.add((eid, ids[str(attr)], stored, True))
expected.update((ids[':db.part/db'], ids[':db.install/attribute'], eid, True) for eid in tempids.values())
datoms = receipt[':edb/tx-data']
assert len(datoms) == 11 and all(d[4] == intent['source_entity'] and d[5] is True for d in datoms)
actual = {(d[0], d[1], d[2], d[5]) for d in datoms if d[1] != ids[':db/txInstant']}
assert actual == expected

after = loads(run(['query', '--database', intent['database'], '--as-of', str(basis),
                  '--file', str(OUT / 'schema-query.edn'), '--inputs', str(OUT / 'schema-inputs.edn')],
                 'schema-after.edn'))
after_by_ident = {str(ident): (eid, record) for eid, ident, record in after}
for eid, ident, record in before_rows:
    assert after_by_ident[str(ident)] == (eid, record), 'Existing inspected schema changed.'
for form in forms:
    eid, record = after_by_ident[str(form[kw('db/ident')])]
    assert eid == tempids[form[kw('db/id')]]
    assert record == {
        kw('db/valueType'): {kw('db/id'): ids[':db.type/ref']},
        kw('db/cardinality'): {kw('db/id'): ids[str(form[kw('db/cardinality')])]},
        kw('db/doc'): form[kw('db/doc')],
    }

(OUT / 'provenance-query.edn').write_text(
    '[:find ?e ?a ?v ?tx ?s :in $ [?e ...] :where [?e ?a ?v ?tx ?s]]\n')
(OUT / 'provenance-inputs.edn').write_text(dumps([list(tempids.values())]) + '\n')
provenance = loads(run(['query', '--database', intent['database'], '--as-of', str(basis),
                       '--file', str(OUT / 'provenance-query.edn'),
                       '--inputs', str(OUT / 'provenance-inputs.edn')], 'provenance.edn'))
assert len(provenance) == 8
assert all(s == intent['source_entity'] for e, a, v, tx, s in provenance)
assert {(e, a, v, True) for e, a, v, tx, s in provenance} == {
    d for d in expected if d[0] in tempids.values()}
verification = {
    'committed': True, 'verified': True,
    'basis_before': receipt[':edb/db-before-t'], 'basis_after': basis,
    'attribute_entities': {str(f[kw('db/ident')]): tempids[f[kw('db/id')]] for f in forms},
    'source': intent['source'], 'source_entity': intent['source_entity'],
    'request_key': intent['request_key'], 'transaction_sha256': intent['transaction_sha256'],
    'transaction_datoms_match_exact_scope': True, 'datoms_added': 11, 'datoms_retracted': 0,
    'existing_inspected_schema_and_validation_spec_unchanged': True,
    'attribute_types_cardinalities_docs_and_provenance_verified': True,
}
(OUT / 'commit-verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
