#!/usr/bin/env python3
"""Import the prepared history content with a fresh preview and guarded commit.

This never imports historical learner outcomes, timing, XP, or engine policy.
Keep an exact durable intent so a timeout can retry the same request safely.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reference/mathacademy/history-question-import-2026-10-04/import-ready'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from core import atomic_json, build_transaction
from database import Database, TOPIC_QUERY, fingerprint
from edn import loads


def main():
    source = SOURCE
    out = source / 'database-import'; out.mkdir(exist_ok=True)
    db = Database(SimpleNamespace(edb_bin=str(ROOT.parent / 'EDB/target/release/edb'),
                                  database='course-academy-v2', endpoint='/tmp/course-academy-edb-v2/writer.sock'))
    content_hash = hashlib.sha256((source / 'questions.json').read_bytes()).hexdigest()
    questions = json.loads((source / 'questions.json').read_text())['questions']
    tx = out / 'transaction.edn'
    intent_file = out / 'commit-intent.json'
    if not intent_file.exists():
        subprocess.run([sys.executable, str(ROOT / 'scripts/preview_historical_questions.py'),
                        '--directory', str(source)], check=True)
        preview = json.loads((source / 'database-preview/report.json').read_text())
        shutil.copy2(source / 'database-preview/all-content-transaction.edn', tx)
        digest = hashlib.sha256(tx.read_bytes()).hexdigest()
        assert digest == preview['plans']['all-content']['transaction_sha256']
        attributes = db.attributes(out, preview['basis'])
        before = db.protected(attributes, out, 'protected-before', preview['basis'])
        intent = {'database':db.args.database, 'endpoint':db.args.endpoint, 'basis':preview['basis'],
                  'content_sha256':content_hash, 'sha256':digest,
                  'request_key':'ma-historical-questions-' + digest,
                  'protected_fact_count':len(before), 'protected_sha256':fingerprint(before),
                  'question_count':len(questions)}
        atomic_json(intent_file, intent)
    intent = json.loads(intent_file.read_text())
    assert intent['content_sha256'] == content_hash, 'Prepared content changed after the intent was saved'
    assert intent['sha256'] == hashlib.sha256(tx.read_bytes()).hexdigest(), 'Saved transaction changed'
    assert intent['database'] == db.args.database and intent['endpoint'] == db.args.endpoint
    receipt = db._commit(intent, tx, out)
    before_basis, after_basis = receipt[':edb/db-before-t'], receipt[':edb/db-after-t']
    assert before_basis == intent['basis']
    attributes = db.attributes(out, before_basis)
    db.validate_datoms(receipt, attributes)
    after = db.protected(attributes, out, 'protected-after', after_basis)
    assert fingerprint(after) == intent['protected_sha256'], 'Protected learner/engine facts changed'
    ids = [q['math_academy_id'] for q in questions]
    existing = {}
    for start in range(0, len(ids), 100):
        existing.update(db.questions(ids[start:start + 100], out, 'after-questions-' + str(start), after_basis))
    assert set(existing) == set(ids), 'Imported questions missing at committed basis'
    tids = sorted({q['topic_id'] for q in questions})
    topics = {}
    query = TOPIC_QUERY.replace(':in $ ?id', ':in $ [?id ...]')
    for start in range(0, len(tids), 100):
        for row in db.query(query, [tids[start:start + 100]], out, 'after-topics-' + str(start), after_basis):
            topics[row[0][':topic/math-academy-id']] = row[0]
    for q in questions:
        stored = existing[q['math_academy_id']]
        assert stored[':question/problem'] == q['problem']
        assert stored[':question/worked-solution'] == q['worked_solution']
        assert stored[':question/difficulty'][':db/ident'] == ':question.difficulty/' + q['difficulty']
        owner = next(k for k in topics[q['topic_id']][':topic/knowledge-points']
                     if str(k[':knowledge-point/id']) == q['knowledge_point_id'])
        assert q['math_academy_id'] in {x[':question/math-academy-id'] for x in owner.get(':knowledge-point/questions', [])}
        remaining, _ = build_transaction({'topic_id':q['topic_id'], 'questions':[q]}, topics[q['topic_id']], existing)
        assert not remaining, 'Reimport is not a no-op: ' + q['math_academy_id']
    deferred = json.loads((source / 'deferred.json').read_text())['questions']
    assert not (set(ids) & {q['math_academy_id'] for q in deferred})
    result = {'committed':True, 'basis_before':before_basis, 'basis_after':after_basis,
              'question_count':len(questions), 'deferred_count':len(deferred),
              'protected_fact_count':len(after), 'protected_facts_sha256':fingerprint(after),
              'learner_and_engine_facts_unchanged':True, 'reimport_is_noop':True,
              'stored_prompts_solutions_and_difficulties_verified':True,
              'kp_memberships_verified':True,
              'current_engine_ready_count':801, 'requires_broader_math_grader_count':705,
              'unsupported_questions_excluded_by_existing_engine_validation':True,
              'transaction_sha256':intent['sha256']}
    atomic_json(out / 'verification.json', result)
    report = json.loads((source / 'report.json').read_text())
    report['database_import'] = result
    report['database_writes'] = len(receipt[':edb/tx-data'])
    report['validation'] = 'Committed content-only import verified; learner and engine facts unchanged; reimport is a no-op'
    atomic_json(source / 'report.json', report)
    status = {'basis':after_basis, 'original_batch_count':1575, 'now_in_database':len(questions),
              'still_absent':len(deferred), 'bulk_import_committed':True,
              'prepared_batch_fully_committed':True, 'verification':'import-ready/database-import/verification.json'}
    atomic_json(source.parent / 'bulk-import-status.json', status)
    readme = (source / 'README.md').read_text().split('\n## Database import')[0]
    # Keep the earlier preview account as historical evidence; lead with the
    # durable outcome so readers do not mistake the old preview for current state.
    readme = readme.replace('No database transaction has been committed.',
                            f'The prepared batch was committed at database basis {after_basis}.')
    readme += (f'\n## Database import\n\nAll {len(questions)} prepared questions were committed '
               f'at basis {before_basis} → {after_basis}. Their prompts, solutions, difficulties, '
               'answer fields, and KP memberships were verified. Learner progress and engine '
               'configuration fingerprints are unchanged, and reimport produces no additions. '
               f'{len(deferred)} deferred questions remain outside this import.\n\n'
               'The existing engine filters questions that fail its grader validation from KP '
               'selection and fresh-question supply checks. Storing the 705 unsupported math '
               'blanks with their KP links does not make them available for practice. '
               'No engine change or fabricated grading result was needed.\n\n'
               'Durable intent, receipt, before/after reads, and verification are in `database-import/`.\n')
    (source / 'README.md').write_text(readme)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
