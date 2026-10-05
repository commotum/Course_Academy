#!/usr/bin/env python3
"""Match and preview prepared historical content against EDB; never transact."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from core import build_transaction
from database import Database, TOPIC_QUERY
from edn import dumps, loads


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path,
                        default=ROOT / 'reference/mathacademy/history-question-import-2026-10-04/import-ready')
    args = parser.parse_args()
    source = args.directory.resolve()
    out = source / 'database-preview'; out.mkdir(exist_ok=True)
    questions = json.loads((source / 'questions.json').read_text())['questions']
    db = Database(SimpleNamespace(edb_bin=str(ROOT.parent / 'EDB/target/release/edb'),
                                  database='course-academy-v2', endpoint='/tmp/course-academy-edb-v2/writer.sock'))
    basis = db.basis()
    topics, existing = {}, {}
    tids = sorted({q['topic_id'] for q in questions})
    query = TOPIC_QUERY.replace(':in $ ?id', ':in $ [?id ...]')
    for start in range(0, len(tids), 100):
        for row in db.query(query, [tids[start:start + 100]], out, 'topics-' + str(start), basis):
            topic = row[0]; topics[topic[':topic/math-academy-id']] = topic
    ids = [q['math_academy_id'] for q in questions]
    for start in range(0, len(ids), 200):
        existing.update(db.questions(ids[start:start + 200], out, 'existing-' + str(start), basis))
    changes, conflicts = [], []
    supported_changes = []
    supported_ids = {q['math_academy_id'] for q in json.loads((source / 'runtime-readiness.json').read_text())['questions']
                     if q['accepted_by_current_grader']}
    for q in questions:
        try:
            forms, _ = build_transaction({'topic_id':q['topic_id'], 'questions':[q]}, topics[q['topic_id']], existing)
            changes.extend(forms)
            if q['math_academy_id'] in supported_ids:
                supported_changes.extend(forms)
        except (ValueError, KeyError) as error:
            conflicts.append({'math_academy_id':q['math_academy_id'], 'reason':str(error)})
    (out / 'conflicts.json').write_text(json.dumps(conflicts, indent=2) + '\n')
    if conflicts:
        raise ValueError('Native database matching found conflicts; see conflicts.json')
    attributes = db.attributes(out, basis)
    summaries = {}
    for name, forms in [('all-content',changes), ('engine-supported',supported_changes)]:
        tx = out / (name + '-transaction.edn'); tx.write_text(dumps(forms) + '\n')
        preview = db.command('with', '--file', tx)
        (out / (name + '-preview.edn')).write_text(preview)
        result = loads(preview)
        db.validate_datoms(result, attributes)
        if result[':edb/db-before-t'] != basis:
            raise ValueError('Database changed during the preview; rerun against a fresh basis')
        summaries[name] = {'transaction_entities':len(forms), 'preview_datoms':len(result[':edb/tx-data']),
                           'transaction_sha256':hashlib.sha256(tx.read_bytes()).hexdigest()}
    if db.basis() != basis:
        raise ValueError('Database changed during the preview; rerun against a fresh basis')
    report = {'basis':basis, 'question_count':len(questions), 'existing_question_count':len(existing),
              'conflicts':0, 'database_writes':0, 'preview_passed':True, 'plans':summaries}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    overall = json.loads((source / 'report.json').read_text())
    overall['database_preview'] = report
    overall['validation'] = 'Importer validation, EDN round-trip, native grader checks, and content-only EDB previews passed; no transaction committed'
    (source / 'report.json').write_text(json.dumps(overall, indent=2) + '\n')
    deferred = json.loads((source / 'deferred.json').read_text())['questions']
    image_count = sum('image' in q['reason'] for q in deferred)
    complex_questions = [q for q in deferred if 'image' not in q['reason']]
    notes = ('\n## Verified preparation\n\n'
             f'At database basis {basis}, all {len(questions)} prepared question IDs were matched '
             f'({len(existing)} already present). Both complete-content and current-engine-supported '
             'transactions passed native EDB `with` previews. Every proposed datom is an additive '
             'content fact or transaction metadata; there are no learner or engine-policy writes. '
             'No import was committed. These previews must be refreshed before a later import.\n\n'
             f'{image_count} image-answer, reconstruction, or missing-asset questions and '
             f'{len(complex_questions)} interpretation/response-design questions remain outside the drafts. '
             'Fully saved diagrams used in otherwise straightforward questions are retained.\n\n'
             f'The current native grader accepts {overall["current_engine_ready_count"]} prepared records; '
             f'{overall["needs_symbolic_grader_count"]} need broader mathematical grading support '
             '(symbolic expressions, radicals, intervals, or units). The supported subset has its own '
             'content file and transaction; the complete draft must not be used to enable unsupported '
             'blanks in a live practice pool.\n\n'
             '### Interpretation cases left for later\n\n')
    notes += '\n'.join('- `' + q['math_academy_id'] + '`: ' + q['knowledge_point']
                       for q in complex_questions) + '\n'
    readme = (source / 'README.md').read_text().split('\n## Verified preparation')[0]
    (source / 'README.md').write_text(readme + notes)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
