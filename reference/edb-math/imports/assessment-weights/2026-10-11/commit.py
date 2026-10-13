"""Validate preview, submit/reconcile the exact approved request, and verify it."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps, kw

intent = json.loads((OUT / 'intent.json').read_text())
assert hashlib.sha256((OUT / 'transaction.edn').read_bytes()).hexdigest() == intent['transaction_sha256']
source = intent['source_entity']
ident_rows = loads((OUT / 'idents.edn').read_text())
idents = {str(r[1]): r[0] for r in ident_rows}
old_docs = {str(r[1]): r[2].get(':db/doc') for r in ident_rows}


def check_scope(report):
    child = report[':edb/tempids']['assessment-weights']
    expected = {(child, idents[':question-weights/activity-type'], idents[':activity.type/assessment'], True),
                (intent['policy_entity'], idents[':policy/question-selection-weights'], child, True)}
    expected.update((child, idents[':question-weights/' + name], value, True)
                    for name, value in intent['assessment_weights'].items())
    for ident, doc in intent['schema_docs'].items():
        expected.add((idents[ident], idents[':db/doc'], doc, True))
        expected.add((idents[ident], idents[':db/doc'], old_docs[ident], False))
    assert all(d[4] == source for d in report[':edb/tx-data'])
    actual = {(d[0], d[1], d[2], d[5]) for d in report[':edb/tx-data']
              if d[1] != idents[':db/txInstant']}
    assert actual == expected, (actual, expected)
    return child


preview = loads((OUT / 'preview.edn').read_text())
assert preview[':edb/committed'] is False
assert preview[':edb/db-before-t'] == intent['read_basis']
check_scope(preview)
env = os.environ.copy()
env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
cli = str(ROOT / '.local/edb/capture-runtime/math-edb')
cmd = [cli, 'transact', '--database', intent['database'], '--endpoint', intent['endpoint'],
       '--request-key', intent['request_key'], '--source', intent['source'],
       '--basis', str(intent['read_basis']), '--file', str(OUT / 'transaction.edn'), '--timeout-ms', '30000']
result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
(OUT / 'commit.stdout.edn').write_text(result.stdout)
(OUT / 'commit.stderr.txt').write_text(result.stderr)
if result.returncode:
    raise RuntimeError('Preserve and reconcile this exact request before any new write: ' + result.stderr)
receipt = loads(result.stdout)
assert receipt[':edb/committed'] is True
(OUT / 'receipt.edn').write_text(result.stdout)
child = check_scope(receipt)
basis = receipt[':edb/db-after-t']
print('COMMITTED basis', basis, 'assessment child', child, 'source', intent['source'], flush=True)


def query(name, query_file, inputs=None):
    cmd = [cli, 'query', '--database', intent['database'], '--as-of', str(basis), '--file', str(query_file)]
    if inputs is not None:
        cmd += ['--inputs', str(inputs)]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True, timeout=30)
    (OUT / name).write_text(result.stdout)
    return loads(result.stdout)


after = query('after.edn', OUT / 'policy-query.edn')
assert len(after) == 1
new_policy = after[0][0]
assert new_policy[':db/id'] == intent['policy_entity']
old_children = loads((OUT / 'before.edn').read_text())[0][0][':policy/question-selection-weights']
new_children = {c[':db/id']: c for c in new_policy[':policy/question-selection-weights']}
assert len(new_children) == 3
assert all(new_children[c[':db/id']] == c for c in old_children)
assert str(new_children[child][':question-weights/activity-type'][':db/ident']) == ':activity.type/assessment'
for name, value in intent['assessment_weights'].items():
    assert new_children[child][':question-weights/' + name] == value
docs = query('after-idents.edn', OUT / 'idents-query.edn')
docs = {str(r[1]): r[2] for r in docs}
assert all(docs[ident][':db/doc'] == doc for ident, doc in intent['schema_docs'].items())
(OUT / 'provenance-query.edn').write_text('[:find ?e ?a ?v ?tx ?s :in $ [?e ...] :where [?e ?a ?v ?tx ?s]]\n')
(OUT / 'provenance-inputs.edn').write_text(dumps([[child, intent['policy_entity']]]) + '\n')
provenance = query('provenance.edn', OUT / 'provenance-query.edn', OUT / 'provenance-inputs.edn')
for name, value in intent['assessment_weights'].items():
    assert any(e == child and a == idents[':question-weights/' + name] and v == value and s == source
               for e, a, v, tx, s in provenance)
assert any(e == intent['policy_entity'] and a == idents[':policy/question-selection-weights'] and v == child and s == source
           for e, a, v, tx, s in provenance)
verification = {'committed': True, 'verified': True, 'basis_before': receipt[':edb/db-before-t'],
                'basis_after': basis, 'assessment_entity': child,
                'source': intent['source'], 'source_entity': source,
                'assessment_weights': intent['assessment_weights'],
                'lesson_review_values_and_children_preserved': True,
                'all_assessment_weights_and_owner_link_have_requested_source': True,
                'transaction_datoms_match_exact_scope': True, 'schema_docs_updated': True,
                'request_key': intent['request_key']}
(OUT / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
