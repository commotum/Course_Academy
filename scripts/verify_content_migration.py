#!/usr/bin/env python3
"""Verify a fresh EDB content import against its lossless canonical plan.

Reads offline JSONL exports only. EIDs may change; domain refs are compared by
their identity lookup refs and enum refs by ident. Writes a verification report,
never a database transaction.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
from uuid import UUID


ROOT = Path('.local/edb/content-migration')
PLAN = ROOT / 'fresh-plan'
TARGET = ROOT / 'target-datoms.jsonl'
REPORT = ROOT / 'verification.json'


def digest_file(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def canonical_line(identity_attr, identity_uuid, attr, value_edn):
    return json.dumps({'identity_attr': identity_attr, 'identity_uuid': identity_uuid,
                       'a': attr, 'value_edn': value_edn}, ensure_ascii=False, sort_keys=True) + '\n'


def lookup(identity):
    attr, uid = identity
    return f'[:{attr} #uuid "{uid}"]'


def read_jsonl(path):
    with path.open(encoding='utf-8') as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f'{path}:{line_number}: invalid JSON') from exc


def create_table(connection, name):
    connection.execute(f'''CREATE TABLE {name} (
        identity_attr TEXT NOT NULL, identity_uuid TEXT NOT NULL,
        a TEXT NOT NULL, value_edn TEXT NOT NULL,
        PRIMARY KEY (identity_attr, identity_uuid, a, value_edn)) WITHOUT ROWID''')


def insert_rows(connection, name, rows):
    statement = f'INSERT INTO {name} VALUES (?, ?, ?, ?)'
    batch = []
    count = 0
    for row in rows:
        batch.append(row)
        if len(batch) >= 10_000:
            connection.executemany(statement, batch)
            count += len(batch)
            batch.clear()
    if batch:
        connection.executemany(statement, batch)
        count += len(batch)
    return count


def table_hash(connection, name, *, without_feedback=False):
    condition = "WHERE a != 'answer/feedback'" if without_feedback else ''
    query = (f'SELECT identity_attr, identity_uuid, a, value_edn FROM {name} {condition} '
             'ORDER BY identity_attr, identity_uuid, a, value_edn')
    digest = hashlib.sha256()
    count = 0
    for values in connection.execute(query):
        digest.update(canonical_line(*values).encode('utf-8'))
        count += 1
    return digest.hexdigest(), count


def set_difference(connection, left, right):
    columns = 'identity_attr, identity_uuid, a, value_edn'
    expression = f'SELECT {columns} FROM {left} EXCEPT SELECT {columns} FROM {right}'
    count = connection.execute(f'SELECT COUNT(*) FROM ({expression})').fetchone()[0]
    sample = [dict(zip(('identity_attr', 'identity_uuid', 'a', 'value_edn'), row))
              for row in connection.execute(f'{expression} LIMIT 5')]
    return count, sample


def target_identities(path):
    identities = {}
    seen = set()
    for row in read_jsonl(path):
        if not row['a'].endswith('/id') or row['uuid'] is None:
            continue
        uid = str(UUID(row['uuid']))
        assert uid == row['uuid'], (row['e'], row['a'], row['uuid'])
        key = (row['a'], uid)
        assert row['e'] not in identities and key not in seen, (row['e'], key)
        identities[row['e']] = key
        seen.add(key)
    return identities


def verify_structure(identities, state, plan):
    errors = []
    kinds = Counter(attr for attr, _ in identities.values())
    examples = state['examples']
    worked = state['worked']
    question_fields = state['question_fields']
    practice = state['practice']
    fields = state['fields']
    field_types = state['field_types']
    choices = state['choices']
    correct = state['correct']
    answers = state['answers']
    answer_type = state['answer_type']
    answer_value = state['answer_value']

    if len(identities) != plan['target_entities']:
        errors.append(f'entity count {len(identities)} != {plan["target_entities"]}')
    if len(examples) != plan['source_attribute_counts']['example/id']:
        errors.append('worked example count changed')
    if len(practice) != plan['source_attribute_counts']['question/id']:
        errors.append('practice question count changed')
    if examples - worked:
        errors.append(f'{len(examples - worked)} examples lack worked solutions')
    if examples & question_fields.keys():
        errors.append(f'{len(examples & question_fields.keys())} migrated examples unexpectedly have fields')
    if examples & state['bank_questions']:
        errors.append(f'{len(examples & state["bank_questions"])} examples appear in practice banks')
    if set(fields) != set(field_types):
        errors.append(f'{len(set(fields) ^ set(field_types))} fields have missing/extra types')
    allowed = {':answer-field.type/radio', ':answer-field.type/blank', ':answer-field.type/select'}
    if any(len(values) != 1 or not set(values) <= allowed for values in field_types.values()):
        errors.append('field type is not a single supported enum')
    field_owners = Counter(field for members in question_fields.values() for field in members)
    if set(field_owners) != set(fields) or any(count != 1 for count in field_owners.values()):
        errors.append('answer fields do not each belong to exactly one question')
    if any(len(values) > 1 or not set(values) <= set(choices[field]) for field, values in correct.items()):
        errors.append('canonical correct answer is not a single member of its field choices')
    answer_owners = Counter(answer for members in choices.values() for answer in members)
    if set(answer_owners) != set(answers) or any(count != 1 for count in answer_owners.values()):
        errors.append('answers do not each belong to exactly one field')
    duplicate_fields = 0
    for field, members in choices.items():
        pairs = [(answer_type.get(answer), answer_value.get(answer)) for answer in members]
        if any(kind is None or value is None for kind, value in pairs) or len(set(pairs)) != len(pairs):
            duplicate_fields += 1
    if duplicate_fields:
        errors.append(f'{duplicate_fields} fields have incomplete or duplicate answer values')
    missing_correct = len(fields) - len(correct)
    source_missing_correct = (plan['field_key_completeness']['total_fields']
                              - plan['field_key_completeness']['keyed_fields'])
    if missing_correct != source_missing_correct:
        errors.append(f'missing correct keys {missing_correct} != source {source_missing_correct}')
    practice_missing_solution = len(practice - worked)
    source_missing_solution = (plan['source_attribute_counts']['question/id']
                               - plan['source_attribute_counts'].get('question/explanation', 0))
    if practice_missing_solution != source_missing_solution:
        errors.append(f'missing practice worked solutions {practice_missing_solution} != source {source_missing_solution}')
    fully_keyed = sum(bool(question_fields.get(question)) and all(field in correct for field in question_fields[question])
                      for question in practice)
    if fully_keyed != plan['practice_key_completeness']['fully_keyed']:
        errors.append(f'fully keyed questions {fully_keyed} != source {plan["practice_key_completeness"]["fully_keyed"]}')
    return errors, {
        'entity_kinds': dict(sorted(kinds.items())), 'examples': len(examples),
        'practice_questions': len(practice), 'fields': len(fields), 'answers': len(answers),
        'missing_correct_fields': missing_correct,
        'practice_questions_missing_worked_solution': practice_missing_solution,
        'fully_keyed_practice_questions': fully_keyed,
    }


def run(target, expected, source, mapping, plan_path, report_path):
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    mappings = json.loads(mapping.read_text(encoding='utf-8'))
    feedback = {item['answer_uuid']: item['feedback'] for item in mappings['mappings']}
    assert len(feedback) == len(mappings['mappings']) == mappings['feedback_count'] == 100
    assert digest_file(expected) == plan['expected_canonical_sha256'], 'plan canonical hash changed'
    assert source.exists() and target.exists(), 'source and target offline JSONL exports are required'
    identities = target_identities(target)
    answer_uuids = {uid for attr, uid in identities.values() if attr == 'answer/id'}
    assert set(feedback) <= answer_uuids, 'staged feedback refers to missing answers'

    with tempfile.TemporaryDirectory(prefix='course-academy-verify-') as temp:
        connection = sqlite3.connect(str(Path(temp) / 'canonical.sqlite'))
        connection.execute('PRAGMA synchronous=OFF')
        connection.execute('PRAGMA journal_mode=OFF')
        create_table(connection, 'expected')
        create_table(connection, 'actual')
        expected_count = insert_rows(connection, 'expected',
            ((row['identity_attr'], row['identity_uuid'], row['a'], row['value_edn'])
             for row in read_jsonl(expected)))
        assert expected_count == plan['expected_canonical_datoms']
        feedback_rows = [('answer/id', uid, 'answer/feedback', json.dumps(value, ensure_ascii=False))
                         for uid, value in sorted(feedback.items())]
        insert_rows(connection, 'expected', feedback_rows)

        state = {
            'examples': set(), 'worked': set(), 'practice': set(), 'bank_questions': set(),
            'question_fields': defaultdict(list), 'fields': set(),
            'field_types': defaultdict(list), 'choices': defaultdict(list),
            'correct': defaultdict(list), 'answers': set(),
            'answer_type': {}, 'answer_value': {},
        }
        actual_counts = Counter()
        actual_feedback = {}

        def rows():
            for row in read_jsonl(target):
                eid = row['e']
                assert eid in identities, ('entity lacks UUID identity', eid, row['a'])
                owner_attr, owner_uuid = identities[eid]
                attr = row['a']
                ref = row['ref_eid']
                if ref is None:
                    value = row['value_edn']
                elif ref in identities:
                    value = lookup(identities[ref])
                else:
                    assert row['ref_ident'], ('unresolved reference', eid, attr, ref)
                    value = ':' + row['ref_ident']
                actual_counts[attr] += 1
                if attr == 'knowledge-point/canonical-example':
                    assert ref in identities and identities[ref][0] == 'question/id'
                    state['examples'].add(identities[ref][1])
                elif attr == 'question/worked-solution':
                    state['worked'].add(owner_uuid)
                elif attr == 'knowledge-point/questions':
                    assert ref in identities and identities[ref][0] == 'question/id'
                    state['bank_questions'].add(identities[ref][1])
                elif attr == 'question/answer-fields':
                    assert ref in identities and identities[ref][0] == 'answer-field/id'
                    state['question_fields'][owner_uuid].append(identities[ref][1])
                elif attr == 'answer-field/id':
                    state['fields'].add(owner_uuid)
                elif attr == 'answer-field/type':
                    state['field_types'][owner_uuid].append(value)
                elif attr in {'answer-field/choices', 'answer-field/correct'}:
                    assert ref in identities and identities[ref][0] == 'answer/id'
                    state['choices' if attr.endswith('/choices') else 'correct'][owner_uuid].append(identities[ref][1])
                elif attr == 'answer/id':
                    state['answers'].add(owner_uuid)
                elif attr == 'answer/type':
                    state['answer_type'][owner_uuid] = value
                elif attr == 'answer/value':
                    state['answer_value'][owner_uuid] = value
                elif attr == 'answer/feedback':
                    actual_feedback[owner_uuid] = value
                yield owner_attr, owner_uuid, attr, value

        actual_count = insert_rows(connection, 'actual', rows())
        state['practice'] = {uid for attr, uid in identities.values() if attr == 'question/id'} - state['examples']
        connection.commit()
        missing_count, missing_sample = set_difference(connection, 'expected', 'actual')
        extra_count, extra_sample = set_difference(connection, 'actual', 'expected')
        target_base_hash, target_base_count = table_hash(connection, 'actual', without_feedback=True)
        target_full_hash, target_full_count = table_hash(connection, 'actual')
        expected_full_hash, expected_full_count = table_hash(connection, 'expected')
        structure_errors, structure_counts = verify_structure(identities, state, plan)
        errors = structure_errors
        if missing_count or extra_count:
            errors.append(f'canonical set differs: {missing_count} missing, {extra_count} extra')
        if target_base_hash != plan['expected_canonical_sha256']:
            errors.append('target content hash excluding staged feedback differs from plan')
        if target_full_hash != expected_full_hash:
            errors.append('target content hash including staged feedback differs')
        if actual_feedback != {uid: json.dumps(text, ensure_ascii=False) for uid, text in feedback.items()}:
            errors.append('staged feedback values differ')
        manifest_path = target.with_suffix('.manifest.json')
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            if manifest['domain_datoms'] != actual_count or manifest['attribute_counts'] != dict(actual_counts):
                errors.append('target export manifest count differs from JSONL')
        report = {
            'ok': not errors, 'errors': errors,
            'inputs': {'source': str(source), 'plan': str(plan_path), 'target': str(target),
                       'feedback_mapping': str(mapping)},
            'sha256': {'source_export': digest_file(source),
                       'plan_canonical': plan['expected_canonical_sha256'],
                       'target_without_feedback': target_base_hash,
                       'expected_with_feedback': expected_full_hash,
                       'target_with_feedback': target_full_hash},
            'datoms': {'plan': expected_count, 'staged_feedback': len(feedback),
                       'expected_total': expected_full_count, 'target_total': actual_count,
                       'target_without_feedback': target_base_count,
                       'target_hashed_total': target_full_count,
                       'missing': missing_count, 'extra': extra_count},
            'difference_samples': {'missing': missing_sample, 'extra': extra_sample},
            'structure': structure_counts,
            'target_attribute_counts': dict(sorted(actual_counts.items())),
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(json.dumps({'ok': report['ok'], 'datoms': report['datoms'],
                          'structure': structure_counts, 'errors': errors}, ensure_ascii=False))
        return not errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=TARGET)
    parser.add_argument('--expected', type=Path, default=PLAN / 'expected-canonical.jsonl')
    parser.add_argument('--source', type=Path, default=ROOT / 'source-datoms.jsonl')
    parser.add_argument('--mapping', type=Path, default=ROOT / 'mapping-summary.json')
    parser.add_argument('--plan', type=Path, default=PLAN / 'plan.json')
    parser.add_argument('--report', type=Path, default=REPORT)
    args = parser.parse_args()
    try:
        good = run(args.target, args.expected, args.source, args.mapping, args.plan, args.report)
    except (AssertionError, OSError, ValueError, sqlite3.Error) as exc:
        print(f'verification could not complete: {exc}', file=sys.stderr)
        return 2
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
