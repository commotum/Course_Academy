"""Capture live schema and preview two additions. Never submits a transaction."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, loads, kw

assert not (OUT / 'intent.json').exists(), 'Preserve the original request; do not regenerate it.'
cli = ROOT / '.local/edb/capture-runtime/math-edb'
env = os.environ.copy()
env['EDB_POSTGRES_URL'] = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"


def run(args, destination):
    result = subprocess.run([str(cli), *args], env=env, capture_output=True, text=True, timeout=45)
    (OUT / destination).write_text(result.stdout)
    (OUT / (destination + '.stderr.txt')).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout


status = run(['status', '--database', 'math'], 'status-before.txt')
match = re.search(r'lineage=(\S+) basis_t=(\d+)', status)
assert match, status
lineage, basis = match.group(1), int(match.group(2))
assert lineage == '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
source = ':agent/gpt-6.1-sol-high'
names = ['db/ident', 'db/doc', 'db/valueType', 'db/cardinality', 'db/txInstant',
         'db.type/ref', 'db.cardinality/one', 'db.cardinality/many',
         'agent/gpt-6.1-sol-high', 'learner-task/validate', 'learner-task/activity',
         'learner-task/retake-of', 'learner-task/remediation-for']
(OUT / 'schema-query.edn').write_text(
    '[:find ?e ?ident (pull ?e [:db/doc :db/valueType :db/cardinality :db/isComponent :db/unique :db.entity/attrs]) '
    ':in $ [?ident ...] :where [?e :db/ident ?ident]]\n')
(OUT / 'schema-inputs.edn').write_text(dumps([[kw(n) for n in names]]) + '\n')
rows = loads(run(['query', '--database', 'math', '--as-of', str(basis),
                  '--file', str(OUT / 'schema-query.edn'), '--inputs', str(OUT / 'schema-inputs.edn')],
                 'schema-before.edn'))
ids = {str(row[1]): row[0] for row in rows}
assert all(':' + name in ids for name in names[:-2])
assert ':learner-task/retake-of' not in ids
assert ':learner-task/remediation-for' not in ids

forms = [
    {kw('db/id'): 'retake-of-attribute',
     kw('db/ident'): kw('learner-task/retake-of'),
     kw('db/valueType'): kw('db.type/ref'),
     kw('db/cardinality'): kw('db.cardinality/one'),
     kw('db/doc'): 'Optional reference from an assessment retake task to the exact original assessment task. This is an attempt relationship, not activity ownership. The application checks assessment task kinds, prevents self/cyclic links and duplicate generated retakes, selects never-presented questions from the original knowledge points, and offers the retake only after required remediation succeeds. The retake remains optional; this relationship alone does not schedule or require it.'},
    {kw('db/id'): 'remediation-for-attribute',
     kw('db/ident'): kw('learner-task/remediation-for'),
     kw('db/valueType'): kw('db.type/ref'),
     kw('db/cardinality'): kw('db.cardinality/many'),
     kw('db/doc'): 'Optional references from a review or replacement relearning task to the assessment task(s) whose incorrect, skipped, or unanswered-on-expiration topics triggered required practice. One practice task may address obligations from several assessments. The application matches the task topic to each assessment obligation and clears it only after qualifying successful practice; prior or unrelated practice does not count. These links preserve trigger provenance, are not component ownership, and do not themselves enforce scheduling or record invented wrong answers.'},
]
text = '[\n' + '\n'.join(' ' + dumps(form) for form in forms) + '\n]\n'
transaction = OUT / 'transaction.edn'
transaction.write_text(text)
intent = {
    'database': 'math', 'lineage': lineage, 'read_basis': basis,
    'endpoint': '/tmp/edb-math/writer.sock', 'source': source,
    'source_entity': ids[source],
    'request_key': 'assessment-retake-schema-2026-10-11-' + str(uuid.uuid4()),
    'transaction_sha256': hashlib.sha256(transaction.read_bytes()).hexdigest(),
    'basis_guard': basis, 'prepared_only': True,
    'scope': 'Install exactly two optional noncomponent task relationship attributes; no task facts, policy changes, scheduling code, or historical backfill.',
    'attributes': [str(form[kw('db/ident')]) for form in forms],
    'schema_files_for_later_update': [str(ROOT / 'schema/learner/2-1-learner-task.edn'),
                                    '/media/jake/SSD/EDB/math/schema/learner/3-learner-task.edn'],
}
(OUT / 'intent.json').write_text(json.dumps(intent, indent=2) + '\n')
run(['with', '--database', 'math', '--source', source,
     '--file', str(transaction)], 'preview.edn')
from verify import verify
verify()
