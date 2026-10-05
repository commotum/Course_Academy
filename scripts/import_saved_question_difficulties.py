#!/usr/bin/env python3
"""Fill missing difficulty on existing questions from saved MA evidence only.

Default prepares and previews a difficulty-only transaction. --apply submits the
prepared transaction with its basis and idempotency key, then verifies that the
only domain datoms changed are question/difficulty. No entities are created.
Conflicting stored ratings are corrected from the saved Math Academy evidence;
no other content or learner data is written.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from core import atomic_json
from database import Database, fingerprint
from edn import dumps, kw, loads

LABELS = {'E': 'easy', 'M': 'moderate', 'H': 'hard',
          'easy': 'easy', 'moderate': 'moderate', 'hard': 'hard'}
QUERY = '''[:find ?q ?id (pull ?q [{:question/difficulty [:db/ident]}])
 :in $ [?id ...] :where [?q :question/math-academy-id ?id]]'''


def evidence():
    ratings = defaultdict(list)
    sources = []

    def add(mid, difficulty, source):
        if difficulty is None:
            return
        assert re.fullmatch(r'q-\d+', mid), (mid, source)
        assert difficulty in LABELS, (difficulty, source)
        ratings[mid].append({'difficulty': LABELS[difficulty], 'source': source})

    history = ROOT / 'reference/mathacademy/progress-history-2026-10-04/observations.json'
    if history.exists():
        raw = history.read_bytes()
        sources.append({'path': str(history.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest()})
        for task in json.loads(raw)['tasks']:
            for question in task['questions']:
                add(question['id'].replace('question-', 'q-'), question['difficulty'],
                    str(history.relative_to(ROOT)) + ':' + task['task-id'])
    paths = sorted(set((ROOT / 'reference/mathacademy/question-capture').glob('*/activity-metadata.json'))
                   | set((ROOT / 'reference/mathacademy/question-capture').glob('*/content.json'))
                   | set((ROOT / 'reference/mathacademy').glob('*/content.json'))
                   | set((ROOT / 'reference/mathacademy').glob('*/content-import.json')))
    for path in paths:
        raw = path.read_bytes()
        data = json.loads(raw)
        source = str(path.relative_to(ROOT))
        sources.append({'path': source, 'sha256': hashlib.sha256(raw).hexdigest()})
        if path.name == 'activity-metadata.json':
            assert isinstance(data, list), path
            for question in data:
                add(question['id'].replace('question-', 'q-'), question.get('difficulty'), source)
        elif isinstance(data, dict):
            for question in data.get('questions', []):
                mid = question.get('math_academy_id')
                if mid:
                    add(mid, question.get('difficulty'), source)
    return ratings, sources


def verify_datoms(receipt, difficulty_attr, tx_instant_attr, planned, replacements):
    actual, retracted = [], []
    for row in receipt[':edb/tx-data']:
        assert row[1] in (difficulty_attr, tx_instant_attr), ('unexpected attribute', row)
        if row[1] == difficulty_attr:
            (actual if row[-1] is True else retracted).append((row[0], row[2]))
        else:
            assert row[-1] is True, ('unexpected transaction timestamp retraction', row)
    assert sorted(actual) == sorted(map(tuple, planned)), ('unexpected difficulty writes', len(actual), len(planned))
    assert sorted(retracted) == sorted(map(tuple, replacements)), ('unexpected difficulty retractions', len(retracted), len(replacements))


def question_rows(db, ids, out, name, basis):
    rows = []
    # Stay below the native query's value-byte limit; only observed IDs matter.
    for offset in range(0, len(ids), 200):
        rows.extend(db.query(QUERY, [ids[offset:offset + 200]], out, name + '-' + str(offset), basis))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    db = Database(SimpleNamespace(edb_bin='/home/jake/Developer/EDB/target/release/edb',
                                  database='course-academy-v2', endpoint='/tmp/course-academy-edb-v2/writer.sock'))
    intent_path = out / 'commit-intent.json'
    if not intent_path.exists():
        ratings, sources = evidence()
        basis = db.basis()
        attributes = db.attributes(out, basis)
        attr_by_name = {str(name): aid for aid, name in attributes}
        enums = db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], out, 'idents', basis)
        enum_by_name = {str(ident): eid for eid, ident in enums}
        ids = sorted(ratings)
        rows = question_rows(db, ids, out, 'questions-before', basis)
        by_id = {mid: (eid, pulled.get(':question/difficulty', {}).get(':db/ident')) for eid, mid, pulled in rows}
        assert len(by_id) == len(rows), 'Nonunique MA question identity'
        transaction, planned, matched, already, absent, conflicts, replacements = [], [], [], [], [], [], []
        for mid, observations in sorted(ratings.items()):
            labels = {record['difficulty'] for record in observations}
            if len(labels) != 1:
                # The newly saved historical DOM observations are authoritative
                # over older converted content. Never guess among conflicting
                # authoritative observations.
                recent = [record for record in observations if record['source'].startswith(
                    'reference/mathacademy/progress-history-2026-10-04/observations.json:')]
                recent_labels = {record['difficulty'] for record in recent}
                if len(recent_labels) != 1:
                    conflicts.append({'question_id': mid, 'reason': 'saved authoritative labels conflict', 'observations': observations})
                    continue
                labels = recent_labels
            label = next(iter(labels))
            ident = ':question.difficulty/' + label
            if mid not in by_id:
                absent.append({'question_id': mid, 'difficulty': label})
                continue
            eid, stored = by_id[mid]
            if stored is not None:
                if str(stored) == ident:
                    already.append(mid)
                    continue
                replacements.append([eid, enum_by_name[str(stored)]])
            transaction.append([kw('db/add'), eid, kw('question/difficulty'), kw(ident)])
            planned.append([eid, enum_by_name[ident]])
            matched.append({'question_id': mid, 'eid': eid, 'difficulty': label,
                            'previous_difficulty': str(stored) if stored is not None else None})
        report = {'database': db.args.database, 'basis': basis, 'source_files': sources,
                  'saved_unique_questions': len(ratings), 'missing_existing_ratings_to_add': matched,
                  'already_same': already, 'not_in_database': absent, 'conflicts': conflicts,
                  'new_rating_counts': dict(Counter(r['difficulty'] for r in matched))}
        atomic_json(out / 'matching-report.json', report)
        tx_path = out / 'transaction.edn'
        tx_path.write_text(dumps(transaction) + '\n')
        if not transaction:
            atomic_json(out / 'verification.json', {'already_complete': True, 'difficulty_values_added': 0})
            print(json.dumps({'already_complete': True, 'absent_questions': len(absent), 'conflicts': len(conflicts)}))
            return
        preview_text = db.command('with', '--file', tx_path)
        (out / 'preview.edn').write_text(preview_text)
        preview = loads(preview_text)
        assert preview[':edb/db-before-t'] == basis, 'Database changed; prepare a fresh attempt'
        difficulty_attr = attr_by_name[':question/difficulty']
        tx_instant_attr = attr_by_name[':db/txInstant']
        verify_datoms(preview, difficulty_attr, tx_instant_attr, planned, replacements)
        digest = hashlib.sha256(tx_path.read_bytes()).hexdigest()
        intent = {'database': db.args.database, 'endpoint': db.args.endpoint, 'basis': basis,
                  'sha256': digest, 'request_key': 'saved-difficulty-only-' + digest,
                  'planned': planned, 'replacements': replacements, 'difficulty_attr': difficulty_attr, 'tx_instant_attr': tx_instant_attr}
        atomic_json(intent_path, intent)
    else:
        intent = json.loads(intent_path.read_text())
        report = json.loads((out / 'matching-report.json').read_text())
    tx_path = out / 'transaction.edn'
    assert hashlib.sha256(tx_path.read_bytes()).hexdigest() == intent['sha256']
    summary = {'prepared': True, 'basis': intent['basis'], 'difficulty_values_to_write': len(intent['planned']),
               'missing_difficulty_values': len(intent['planned']) - len(intent['replacements']),
               'conflicting_existing_values_to_correct': len(intent['replacements']),
               'already_same': len(report['already_same']), 'absent_questions': len(report['not_in_database']),
               'conflicts': len(report['conflicts']), 'bands': report['new_rating_counts']}
    if not args.apply:
        print(json.dumps(summary, indent=2))
        return
    receipt = db._commit(intent, tx_path, out)
    verify_datoms(receipt, intent['difficulty_attr'], intent['tx_instant_attr'], intent['planned'], intent['replacements'])
    before, after = receipt[':edb/db-before-t'], receipt[':edb/db-after-t']
    attributes = db.attributes(out, before)
    protected_before = db.protected(attributes, out, 'protected-before', before)
    protected_after = db.protected(attributes, out, 'protected-after', after)
    assert fingerprint(protected_before) == fingerprint(protected_after)
    checked_ids = sorted({r['question_id'] for r in report['missing_existing_ratings_to_add']})
    rows_after = question_rows(db, checked_ids, out, 'questions-after', after)
    after_by_id = {mid: (eid, pulled.get(':question/difficulty', {}).get(':db/ident')) for eid, mid, pulled in rows_after}
    for question in report['missing_existing_ratings_to_add']:
        assert after_by_id[question['question_id']] == (question['eid'], ':question.difficulty/' + question['difficulty'])
    remaining = [r for r in report['missing_existing_ratings_to_add'] if after_by_id[r['question_id']][1] is None]
    assert not remaining
    result = {**summary, 'committed': True, 'basis_before': before, 'basis_after': after,
              'difficulty_values_added': len(intent['planned']) - len(intent['replacements']),
              'existing_ratings_corrected': len(intent['replacements']),
              'only_domain_attribute_changed': 'question/difficulty', 'new_question_entities': 0,
              'protected_fact_count': len(protected_before), 'protected_facts_sha256': fingerprint(protected_before),
              'learner_and_engine_facts_unchanged': True, 'reimport_is_noop': True}
    atomic_json(out / 'verification.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
