#!/usr/bin/env python3
"""Build a two-phase, identity-preserving EDB import from an offline datom export.

Only exact same-field (answer/type, answer/value) duplicates are collapsed. The
source backup remains untouched; duplicate UUID replacements are fully audited.
"""

import argparse
import collections
import hashlib
import json
import re
import uuid
from pathlib import Path


SOURCE = Path('.local/edb/content-migration/source-datoms.jsonl')
OUTPUT = Path('.local/edb/content-migration/fresh-plan')
RENAMES = {
    'sequence/id': 'course-group/id',
    'sequence/title': 'course-group/title',
    'sequence/courses': 'course-group/courses',
    'sequence/next': 'course-group/next',
    'example/id': 'question/id',
    'example/problem': 'question/problem',
    'example/explanation': 'question/worked-solution',
    'example/math-academy-id': 'question/math-academy-id',
    'question/explanation': 'question/worked-solution',
    'knowledge-point/example': 'knowledge-point/canonical-example',
    'answer-field/answer-choices': 'answer-field/choices',
    'answer-field/correct-answer': 'answer-field/correct',
}
ENUM_REFS = {'activity/type', 'answer/type'}
QUESTION_FIELD_TYPES = {
    'question.type/multiple-choice': 'answer-field.type/radio',
    'question.type/fill-in-the-blank': 'answer-field.type/blank',
    'question.type/select-list': 'answer-field.type/select',
}
MAX_SCALAR_ENTITIES = 4_000
MAX_REFS = 12_000
MAX_BATCH_BYTES = 12_000_000


def quote(value):
    return json.dumps(value, ensure_ascii=False)


def read_source(path):
    entities = collections.defaultdict(lambda: collections.defaultdict(list))
    counts = collections.Counter()
    for number, line in enumerate(path.open(encoding='utf-8'), 1):
        row = json.loads(line)
        assert set(row) == {'e', 'a', 'value_edn', 'ref_eid', 'ref_ident', 'raw_string', 'uuid'}, number
        entities[row['e']][row['a']].append(row)
        counts[row['a']] += 1
    return entities, counts


def one(rows, attribute):
    found = rows.get(attribute, [])
    assert len(found) == 1, (attribute, len(found))
    return found[0]


def identities(entities):
    result = {}
    seen = {}
    for eid, rows in entities.items():
        identity = [(attr, value) for attr, values in rows.items() if attr.endswith('/id') for value in values]
        assert len(identity) == 1, (eid, identity)
        attr, value = identity[0]
        uid = value['uuid']
        assert uid and str(uuid.UUID(uid)) == uid, (eid, attr, value)
        attr = RENAMES.get(attr, attr)
        key = (attr, uid)
        assert key not in seen, (eid, seen.get(key), key)
        seen[key] = eid
        result[eid] = key
    return result


def duplicate_answers(entities, identity, feedback_by_uuid):
    answer = {}
    for eid, rows in entities.items():
        if 'answer/id' in rows:
            answer[eid] = (one(rows, 'answer/type')['ref_ident'], one(rows, 'answer/value')['raw_string'])
            assert answer[eid][0] and answer[eid][1] is not None
    field_owner = {}
    for eid, rows in entities.items():
        for row in rows.get('question/answer-fields', []):
            field = row['ref_eid']
            assert field not in field_owner, (field, eid, field_owner.get(field))
            field_owner[field] = eid
    fields = {eid for eid, rows in entities.items() if 'answer-field/id' in rows}
    assert set(field_owner) == fields, (len(field_owner), len(fields))
    answer_owner = {}
    remap = {}
    groups = []
    missing_correct_membership = 0
    for field in sorted(fields):
        rows = entities[field]
        choices = [item['ref_eid'] for item in rows.get('answer-field/answer-choices', [])]
        correct = [item['ref_eid'] for item in rows.get('answer-field/correct-answer', [])]
        assert len(correct) <= 1, field
        if correct and correct[0] not in choices:
            missing_correct_membership += 1
        members = set(choices + correct)
        for aid in members:
            assert aid in answer, (field, aid)
            assert aid not in answer_owner, (aid, answer_owner.get(aid), field)
            answer_owner[aid] = field
        same = collections.defaultdict(list)
        for aid in sorted(members):
            same[answer[aid]].append(aid)
        for (kind, value), aids in same.items():
            if len(aids) == 1:
                continue
            keeper = correct[0] if correct and correct[0] in aids else min(aids)
            feedbacks = {feedback_by_uuid[identity[aid][1]] for aid in aids if identity[aid][1] in feedback_by_uuid}
            assert len(feedbacks) <= 1, (field, aids, feedbacks)
            for aid in aids:
                if aid != keeper:
                    remap[aid] = keeper
            groups.append({
                'field_eid': field, 'field_uuid': identity[field][1],
                'answer_type': kind, 'answer_value': value,
                'kept_eid': keeper, 'kept_uuid': identity[keeper][1],
                'merged': [{'eid': aid, 'uuid': identity[aid][1]} for aid in aids if aid != keeper],
                'kept_correct': keeper in correct,
                'feedback': next(iter(feedbacks), None),
            })
    assert set(answer_owner) == set(answer), (len(answer_owner), len(answer))
    for eid, rows in entities.items():
        for attr, values in rows.items():
            for row in values:
                if row['ref_eid'] in remap:
                    assert attr in {'answer-field/answer-choices', 'answer-field/correct-answer'}, (eid, attr, row)
                    assert eid == answer_owner[row['ref_eid']], (eid, attr, row)
    return remap, groups, field_owner, missing_correct_membership


def schema_attrs():
    names = set()
    for path in Path('schema').glob('*/*.edn'):
        names.update(re.findall(r':db/ident :([\w.\-/]+)', path.read_text()))
    return names


def assert_schema_types():
    text = '\n'.join(path.read_text() for path in Path('schema').glob('*/*.edn'))
    required = {
        'question/id': 'uuid', 'question/math-academy-id': 'string',
        'question/worked-solution': 'string',
        'answer-field/type': 'ref', 'answer-field/choices': 'ref',
        'answer-field/correct': 'ref', 'knowledge-point/canonical-example': 'ref',
    }
    for attribute, value_type in required.items():
        pattern = rf':db/ident :{re.escape(attribute)}\s+:db/valueType :db\.type/{value_type}\b'
        assert re.search(pattern, text), (attribute, value_type)


def batch_write(output, prefix, forms, max_items):
    batches = []
    current = []
    size = 3
    for item, units in forms:
        encoded = item.encode('utf-8')
        if current and (len(current) + units > max_items or size + len(encoded) + 1 > MAX_BATCH_BYTES):
            filename = f'{prefix}-{len(batches)+1:04d}.edn'
            (output / filename).write_text('[\n' + '\n'.join(current) + '\n]\n', encoding='utf-8')
            batches.append({'file': filename, 'items': sum(count for _, count in current_units),
                            'bytes': (output / filename).stat().st_size})
            current = []
            current_units = []
            size = 3
        if not current:
            current_units = []
        assert len(encoded) + 4 < MAX_BATCH_BYTES, prefix
        current.append(item)
        current_units.append((item, units))
        size += len(encoded) + 1
    if current:
        filename = f'{prefix}-{len(batches)+1:04d}.edn'
        (output / filename).write_text('[\n' + '\n'.join(current) + '\n]\n', encoding='utf-8')
        batches.append({'file': filename, 'items': sum(count for _, count in current_units),
                        'bytes': (output / filename).stat().st_size})
    return batches


def build(source, output):
    entities, source_counts = read_source(source)
    manifest = json.loads(source.with_suffix('.manifest.json').read_text())
    assert sum(source_counts.values()) == manifest['domain_datoms']
    assert dict(source_counts) == manifest['attribute_counts']
    assert not any(name.startswith(('learner/', 'learner-task/', 'task-item/', 'learner-response/'))
                   for name in source_counts), 'This snapshot unexpectedly contains learner data'
    identity = identities(entities)
    feedback_summary = json.loads(Path('.local/edb/content-migration/mapping-summary.json').read_text())
    feedback_by_uuid = {entry['answer_uuid']: entry['feedback'] for entry in feedback_summary['mappings']}
    remap, duplicate_groups, field_owner, missing_correct = duplicate_answers(entities, identity, feedback_by_uuid)
    known = schema_attrs()
    assert_schema_types()
    assert all(name in known for name in {'question/worked-solution', 'answer-field/type', 'answer-field/choices', 'answer-field/correct', 'knowledge-point/canonical-example'})
    assert 'example/id' not in known and 'question/type' not in known
    source_allowed = known | set(RENAMES) | {'question/type'}
    assert not (set(source_counts) - source_allowed), sorted(set(source_counts) - source_allowed)
    assert not (set(feedback_by_uuid) & {identity[eid][1] for eid in remap}), 'feedback targets merged UUIDs'
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob('scalar-*.edn'):
        stale.unlink()
    for stale in output.glob('refs-*.edn'):
        stale.unlink()
    duplicate_report = {
        'groups': duplicate_groups, 'group_count': len(duplicate_groups),
        'merged_entity_count': len(remap),
        'uuid_remap': {identity[old][1]: identity[new][1] for old, new in sorted(remap.items())},
        'eid_remap': {str(old): new for old, new in sorted(remap.items())},
        'rule': 'Within one answer field, merge only identical answer/type and answer/value; prefer correct, otherwise smallest original eid.',
        'source_answer_entities': sum('answer/id' in rows for rows in entities.values()),
        'target_answer_entities': sum('answer/id' in rows for eid, rows in entities.items() if eid not in remap),
    }
    (output / 'duplicate-answer-values.json').write_text(json.dumps(duplicate_report, indent=2, ensure_ascii=False) + '\n')

    scalars = collections.defaultdict(lambda: collections.defaultdict(set))
    refs = collections.defaultdict(lambda: collections.defaultdict(set))
    derived_types = {}
    for field, question in field_owner.items():
        question_type = one(entities[question], 'question/type')['ref_ident']
        assert question_type in QUESTION_FIELD_TYPES, (question, question_type)
        derived_types[field] = QUESTION_FIELD_TYPES[question_type]
    for eid, rows in entities.items():
        if eid in remap:
            continue
        for old_attr, values in rows.items():
            if old_attr == 'question/type':
                continue
            attr = RENAMES.get(old_attr, old_attr)
            assert attr in known, (old_attr, attr)
            for row in values:
                if old_attr in {'question/math-academy-id', 'example/math-academy-id'}:
                    assert row['ref_eid'] is None and re.fullmatch(r'\d+', row['value_edn'])
                    value = quote(('e-' if old_attr.startswith('example/') else 'q-') + row['value_edn'])
                    scalars[eid][attr].add(value)
                elif row['ref_eid'] is None:
                    scalars[eid][attr].add(row['value_edn'])
                elif row['ref_eid'] not in entities:
                    assert old_attr in ENUM_REFS and row['ref_ident'], (eid, old_attr, row)
                    scalars[eid][attr].add(':' + row['ref_ident'])
                else:
                    refs[eid][attr].add(remap.get(row['ref_eid'], row['ref_eid']))
        if 'example/id' in rows:
            assert 'question/worked-solution' in scalars[eid] and 'question/answer-fields' not in refs[eid]
        elif 'question/id' in rows:
            assert 'question/answer-fields' in refs[eid]
        if 'answer-field/id' in rows:
            scalars[eid]['answer-field/type'].add(':' + derived_types[eid])
            correct = refs[eid].get('answer-field/correct', set())
            assert len(correct) <= 1, (eid, correct)
            if correct:
                refs[eid]['answer-field/choices'].update(correct)
    # Every target field member belongs to its field, and its canonical answer is a member.
    answer_targets = collections.defaultdict(set)
    for eid, rows in entities.items():
        if 'answer-field/id' in rows:
            for target in refs[eid].get('answer-field/choices', set()):
                answer_targets[target].add(eid)
            assert refs[eid].get('answer-field/correct', set()) <= refs[eid].get('answer-field/choices', set())
    assert all(len(fields) == 1 for fields in answer_targets.values())
    assert answer_targets.keys() == {eid for eid, rows in entities.items() if 'answer/id' in rows and eid not in remap}
    source_keyed_fields = {eid for eid, rows in entities.items() if 'answer-field/correct-answer' in rows}
    target_keyed_fields = {eid for eid, attributes in refs.items() if attributes.get('answer-field/correct')}
    assert source_keyed_fields == target_keyed_fields
    practice = {eid: rows for eid, rows in entities.items() if 'question/id' in rows}
    source_fully_keyed = sum(all(row['ref_eid'] in source_keyed_fields for row in rows['question/answer-fields'])
                             for rows in practice.values())
    target_fully_keyed = sum(all(row['ref_eid'] in target_keyed_fields for row in rows['question/answer-fields'])
                             for rows in practice.values())
    assert source_fully_keyed == target_fully_keyed
    for eid, attributes in scalars.items():
        for attr, values in attributes.items():
            assert len(values) == 1, (eid, attr, values)
    ma_ids = [next(iter(attributes['question/math-academy-id'])) for attributes in scalars.values()
              if 'question/math-academy-id' in attributes]
    assert len(ma_ids) == len(set(ma_ids)) == source_counts['question/math-academy-id'] + source_counts['example/math-academy-id']
    for eid, attributes in refs.items():
        for attr, targets in attributes.items():
            assert all(target in identity and target not in remap for target in targets), (eid, attr, targets)

    def lookup(eid):
        attr, value = identity[eid]
        return f'[:{attr} #uuid "{value}"]'

    scalar_forms = []
    canonical = set()
    target_counts = collections.Counter()
    for eid in sorted(set(entities) - set(remap)):
        attributes = scalars[eid]
        id_attr, id_uuid = identity[eid]
        assert id_attr in attributes
        pieces = [f':db/id {quote("m-" + str(eid))}']
        for attr in sorted(attributes):
            value = next(iter(attributes[attr]))
            pieces.append(f':{attr} {value}')
            canonical.add((id_attr, id_uuid, attr, value))
            target_counts[attr] += 1
        scalar_forms.append((' {' + ' '.join(pieces) + '}', 1))
    ref_forms = []
    for eid in sorted(refs):
        id_attr, id_uuid = identity[eid]
        for attr in sorted(refs[eid]):
            for target in sorted(refs[eid][attr]):
                value = lookup(target)
                ref_forms.append((f' [:db/add {lookup(eid)} :{attr} {value}]', 1))
                canonical.add((id_attr, id_uuid, attr, value))
                target_counts[attr] += 1
    assert len(canonical) == sum(target_counts.values())
    assert target_counts['question/id'] == source_counts['question/id'] + source_counts['example/id']
    assert target_counts['question/worked-solution'] == source_counts['question/explanation'] + source_counts['example/explanation']
    assert target_counts['answer-field/choices'] == target_counts['answer/id'] == source_counts['answer/id'] - len(remap)
    assert target_counts['knowledge-point/canonical-example'] == source_counts['knowledge-point/example']
    assert not any(name.startswith('example/') for name in target_counts)
    assert 'question/type' not in target_counts
    scalar_batches = batch_write(output, 'scalar', scalar_forms, MAX_SCALAR_ENTITIES)
    ref_batches = batch_write(output, 'refs', ref_forms, MAX_REFS)
    expected = output / 'expected-canonical.jsonl'
    digest = hashlib.sha256()
    with expected.open('w', encoding='utf-8') as stream:
        for id_attr, id_uuid, attr, value in sorted(canonical):
            line = json.dumps({'identity_attr': id_attr, 'identity_uuid': id_uuid,
                               'a': attr, 'value_edn': value}, ensure_ascii=False, sort_keys=True) + '\n'
            stream.write(line)
            digest.update(line.encode('utf-8'))
    plan = {
        'source': str(source), 'source_basis_t': manifest['basis_t'],
        'source_domain_datoms': manifest['domain_datoms'], 'source_entities': len(entities),
        'target_entities': len(entities) - len(remap),
        'source_attribute_counts': dict(sorted(source_counts.items())),
        'target_attribute_counts': dict(sorted(target_counts.items())),
        'missing_correct_choice_memberships_added': missing_correct,
        'field_key_completeness': {'keyed_fields': len(source_keyed_fields),
                                   'total_fields': len(field_owner)},
        'practice_key_completeness': {'fully_keyed': source_fully_keyed,
                                      'missing_at_least_one_key': len(practice) - source_fully_keyed,
                                      'total_practice_questions': len(practice)},
        'duplicate_groups': len(duplicate_groups), 'duplicate_answers_merged': len(remap),
        'scalar_batches': scalar_batches, 'ref_batches': ref_batches,
        'apply_order': [item['file'] for item in scalar_batches + ref_batches],
        'expected_canonical_file': expected.name,
        'expected_canonical_sha256': digest.hexdigest(),
        'expected_canonical_datoms': len(canonical),
        'identity_preservation': (f'Every retained source UUID is unchanged; {len(remap)} exact same-field '
                                  'duplicate answer UUIDs are explicitly remapped in duplicate-answer-values.json.'),
        'source_incompleteness': 'Only existing correct refs are retained; no absent correct answers or worked solutions are inferred.',
    }
    (output / 'plan.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: plan[key] for key in ('source_entities', 'target_entities', 'duplicate_answers_merged',
                                                'missing_correct_choice_memberships_added', 'expected_canonical_datoms')}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    build(args.source, args.output)


if __name__ == '__main__':
    main()
