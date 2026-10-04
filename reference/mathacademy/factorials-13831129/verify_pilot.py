#!/usr/bin/env python3
"""Verify the pilot against EDB query/report files (read-only)."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_pilot import EXISTING, KPS


def read_edn(path):
    # This reader handles the bounded EDN forms printed by these EDB commands.
    # Tagged UUIDs/instants become strings; entity refs become integers.
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|#\{|[\[\]{}]|[^\s,\[\]{}]+', Path(path).read_text())
    pos = 0

    def value():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        if token in ('[', '{', '#{'):
            close = ']' if token == '[' else '}'
            items = []
            while tokens[pos] != close:
                items.append(value())
            pos += 1
            if token == '{':
                assert len(items) % 2 == 0
                return dict(zip(items[::2], items[1::2]))
            return items
        if token in ('#uuid', '#inst', '#edb/ref'):
            return value()
        if token.startswith('"'):
            return json.loads(token)
        if token == 'true':
            return True
        if token == 'false':
            return False
        if token == 'nil':
            return None
        if re.fullmatch(r'-?\d+', token):
            return int(token)
        if re.fullmatch(r'-?\d+\.\d+(?:[Ee][+-]?\d+)?', token):
            return float(token)
        assert token.startswith(':'), token
        return token

    result = value()
    assert pos == len(tokens)
    return result


def facts_hash(rows):
    encoded = sorted(json.dumps(r, sort_keys=True, separators=(',', ':')) for r in rows)
    return hashlib.sha256('\n'.join(encoded).encode()).hexdigest()


def verify_before(local):
    existing = {r[0][':question/math-academy-id']: r[0]
                for r in read_edn(local / 'questions-before.edn')}
    assert set(existing) == EXISTING
    source = json.loads((ROOT / 'content.json').read_text())
    for q in source['questions']:
        if q['math_academy_id'] in existing:
            record = existing[q['math_academy_id']]
            assert ':question/difficulty' not in record
            assert ':question/worked-solution' not in record
            field = record[':question/answer-fields'][0]
            assert field[':answer-field/type'][':db/ident'] == ':answer-field.type/radio'
            assert field[':answer-field/correct'][':answer/value'] == q['correct_answer_from_solution']
            assert {a[':answer/value'] for a in field[':answer-field/choices']} == set(q['source_choices'])
    preview = read_edn(local / 'preview.edn')
    assert preview[':edb/db-before-t'] == 301
    assert all(row[-1] is True for row in preview[':edb/tx-data']), 'Unexpected retraction'
    allowed = {r[0] for r in read_edn(local / 'allowed-attributes.edn')}
    assert all(row[1] in allowed for row in preview[':edb/tx-data']), 'Unexpected attribute mutation'
    print('Preview verified: all assertions, only allowed content attributes; existing fields preserved.')


def verify_after(local):
    before = {r[0][':question/math-academy-id']: r[0]
              for r in read_edn(local / 'questions-before.edn')}
    after = {r[0][':question/math-academy-id']: r[0]
             for r in read_edn(local / 'questions-after.edn')}
    source = json.loads((ROOT / 'content.json').read_text())
    review = {r['math_academy_id']: r for r in json.loads((ROOT / 'review.json').read_text())}
    assert len(after) == 9
    for q in source['questions']:
        key = q['math_academy_id']
        record = after[key]
        assert record[':question/worked-solution'] == q['worked_solution']
        assert record[':question/difficulty'][':db/ident'] == ':question.difficulty/' + q['difficulty']
        assert [k[':knowledge-point/id'] for k in record[':knowledge-point/_questions']] == [KPS[q['knowledge_point']]]
        if key in EXISTING:
            preserved = dict(record)
            del preserved[':question/difficulty'], preserved[':question/worked-solution']
            assert preserved == before[key], key
        fields = record[':question/answer-fields']
        assert len(fields) == 1
        field = fields[0]
        assert field[':answer-field/type'][':db/ident'] == ':answer-field.type/radio'
        assert field[':answer-field/key'] == 'selection'
        choices = field[':answer-field/choices']
        assert len(choices) == len(review[key]['choices'])
        assert {a[':answer/value'] for a in choices} == set(review[key]['choices'])
        assert field[':answer-field/correct'][':answer/value'] == q['correct_answer_from_solution']
        assert field[':answer-field/correct'][':db/id'] in {a[':db/id'] for a in choices}
    topic_before = read_edn(local / 'topic-before.edn')[0][0]
    topic_after = read_edn(local / 'topic-after.edn')[0][0]
    old_kps = {k[':knowledge-point/id']: k for k in topic_before[':topic/knowledge-points']}
    new_kps = {k[':knowledge-point/id']: k for k in topic_after[':topic/knowledge-points']}
    for key, old in old_kps.items():
        new = new_kps[key]
        assert old[':knowledge-point/canonical-example'] == new[':knowledge-point/canonical-example']
        old_questions = {q[':question/math-academy-id']: q for q in old[':knowledge-point/questions']}
        new_questions = {q[':question/math-academy-id']: q for q in new[':knowledge-point/questions']}
        assert all(new_questions[q] == v for q, v in old_questions.items())
        expected_new = {q['math_academy_id'] for q in source['questions']
                        if q['math_academy_id'] not in EXISTING and KPS[q['knowledge_point']] == key}
        assert set(new_questions) - set(old_questions) == expected_new
    protected_before = read_edn(local / 'protected-before.edn')
    protected_after = read_edn(local / 'protected-after.edn')
    fingerprint = facts_hash(protected_before)
    assert fingerprint == facts_hash(protected_after), 'Learner/engine state changed'
    report = read_edn(local / 'commit.edn')
    assert report[':edb/committed'] is True
    assert all(row[-1] is True for row in report[':edb/tx-data'])
    assert all(row[1] in {r[0] for r in read_edn(local / 'allowed-attributes.edn')}
               for row in report[':edb/tx-data'])
    result = {
        'committed': True, 'basis_before': report[':edb/db-before-t'],
        'basis_after': read_edn(local / 'remove-fraction-commit.edn')[':edb/db-after-t'],
        'questions_enriched': 2, 'questions_created': 7, 'radio_choices_per_question': {k: len(v['choices']) for k, v in review.items()},
        'rejected_fraction_option_removed': True,
        'kp_links_added': 7, 'protected_facts_count': len(protected_before),
        'protected_facts_sha256': fingerprint,
        'learner_and_engine_facts_unchanged': True,
        'existing_question_fields_and_canonical_examples_unchanged': True,
    }
    (ROOT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    path = Path(sys.argv[2])
    (verify_before if sys.argv[1] == 'before' else verify_after)(path)
