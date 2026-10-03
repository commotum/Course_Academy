#!/usr/bin/env python3
"""Stage source-backed question enrichment against a current-schema snapshot.

Reads source vaults without changing them. Every existing reference comes from
the snapshot, every scalar mutation is compare-and-swap guarded, and unproved
answer mappings remain in the manifest. Does not contact or write the database.
"""

import argparse
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

import reconcile_ma_questions as prior
import reconcile_unmatched_mc as mc
import reconcile_unmatched_fields as fields
from generate_ma_lesson_seed import ident, question_blocks, question_parts

ROOT = Path('.local/edb/remaining-courses')
MANY = {'question/answer-fields', 'answer-field/choices'}
REVIEWED_TABLES = {
    ('3002', '110395'): ('e49d8c53a7d1ff9c5b5b08ad35e466e4e00a6e32dc0795a9f6cc373b2f03ba95', '376e995897948db12aeea0f3825e7fdaca5331720d5ecc352e7602f00bde1a6a', 3),
    ('3002', '142494'): ('7bbd757079c9c7426fda372279bdba875f98bdc32316c2e8a6ebf5db363781a9', 'c8f9b187c2172587d28ba7c05414d63c1a5319d2ccdc711f7b0c1a9f6801f91f', 3),
    ('3003', '114425'): ('d995b2cfa32a1b8813a467773c099c4229f9b337f178cc52c8a27bd1690f1cc0', '389657019e409d87d0745c627ba6eb3dbf0565c71d57e56c78eaa9f3e9a6c576', 3),
    ('3003', '142554'): ('f2ed0cc18613d0af854b0a9bab1617cf2241531eec9c5211595d7d9aa7eebddc', '533e77929ac7002095efffa865c8e72601b98c987396633a59d3946d3fcb29cf', 2),
}


def snapshot(path):
    entities = collections.defaultdict(dict)
    for line in path.open():
        row = json.loads(line)
        value = (row['uuid'] if row['uuid'] is not None else
                 row['ref_ident'] if row['ref_ident'] is not None else
                 row['ref_eid'] if row['ref_eid'] is not None else
                 row['raw_string'] if row['raw_string'] is not None else row['value_edn'])
        if row['a'] in MANY:
            entities[row['e']].setdefault(row['a'], []).append(value)
        else:
            entities[row['e']][row['a']] = value
    identities = {value: (eid, attr) for eid, entity in entities.items()
                  for attr, value in entity.items() if attr.endswith('/id')}
    return entities, identities


def reference(entity, kind):
    return f'[:{kind}/id #uuid "{entity[kind + "/id"]}"]'


def scalar(value):
    return 'nil' if value is None else prior.quote(value)


def cas(ref, attr, before, after):
    return f'[:db/cas {ref} :{attr} {scalar(before)} {scalar(after)}]'


def occurrence(entry):
    return {k: entry.get(k) for k in ('path', 'line', 'quiz_id')}


def blank_value(answer):
    if answer.startswith('$') and answer.endswith('$'):
        return 'math', answer[1:-1]
    if re.fullmatch(r'[0-9A-Za-z_+\-*/^().| {}]+', answer) and re.search(r'[0-9]|[+\-*/^|]', answer):
        value = re.sub(r'(?<![A-Za-z\\])pi(?![A-Za-z])', r'\\pi', answer)
        for command in ('ln', 'log'):
            value = re.sub(r'(?<![A-Za-z\\])' + command + r'(?![A-Za-z])', lambda _: '\\' + command, value)
        value = re.sub(r'(?<![A-Za-z\\])sqrt\(([^()]+)\)', r'\\sqrt{\1}', value)
        value = re.sub(r'\^\(([^()]*)\)', r'^{\1}', value)
        value = re.sub(r'^(\d+)\s+(\d+)/(\d+)$', lambda m: '\\frac{' + str(int(m[1])*int(m[3])+int(m[2])) + '}{' + m[3] + '}', value)
        return 'math', value
    return 'text', answer


def current_question(rec, entities, identities, cache):
    uid = str(ident('question', rec['key']))
    assert uid in identities, 'question missing from snapshot'
    eid, attr = identities[uid]
    assert attr == 'question/id'
    question = entities[eid]
    assert question.get('question/math-academy-id', 'q-' + rec['id']) == 'q-' + rec['id'], 'current MA identity differs'
    base = prior.DATA / rec['topic'] / (rec['topic'] + '.md')
    asset_rec = {**rec, 'options': [value for field in rec['options'] for value in field]} if rec['format'] == 'select-list' else rec
    assert mc.value_signature(question['question/problem'], base, asset_rec, cache)[0] == mc.value_signature(rec['prompt'], base, asset_rec, cache)[0], 'current prompt differs from captured source'
    result = []
    for fi in range(1, rec['fields'] + 1):
        fuid = str(ident('field', f'{rec["key"]}:{fi}'))
        assert fuid in identities, 'field missing from snapshot'
        feid, fattr = identities[fuid]
        assert fattr == 'answer-field/id' and feid in question['question/answer-fields'], 'field ownership differs'
        field = entities[feid]
        expected_type = {'multiple-choice': 'radio', 'select-list': 'select', 'free-response': 'blank'}[rec['format']]
        assert field['answer-field/type'] == 'answer-field.type/' + expected_type, 'field type differs'
        result.append(field)
    assert len(question['question/answer-fields']) == len(result), 'field count differs'
    return question, result


def answer_by_position(rec, fi, ci, field, entities, cache):
    values = rec['options'] if rec['format'] == 'multiple-choice' else rec['options'][fi - 1]
    kind, value = values[ci - 1]
    asset_rec = {**rec, 'options': [value for field in rec['options'] for value in field]} if rec['format'] == 'select-list' else rec
    signature = mc.source_choice_signature(kind, value, asset_rec, cache)
    assert signature is not None, 'canonical answer asset absent'
    matches = []
    for aid in field.get('answer-field/choices', []):
        answer = entities[aid]
        if mc.source_choice_signature(answer['answer/type'].split('/')[-1], answer['answer/value'], asset_rec, cache) == signature:
            matches.append((aid, answer))
    assert len(matches) == 1, f'correct value maps to {len(matches)} current choices'
    return matches[0]


def render_feedback(text, path):
    def image(match):
        asset = Path(match[1].strip('<>'))
        if not asset.is_absolute():
            asset = Path(path).parent / asset
        if not asset.is_file():
            raise ValueError('feedback references a missing image')
        return '![](' + str(asset.resolve()) + ')'
    return mc.IMAGE.sub(image, text.strip())


def staged_forms(rec, chosen, good, entities, identities, cache):
    question, current_fields = current_question(rec, entities, identities, cache)
    qref = reference(question, 'question')
    statements = []
    updates = []
    conflicts = []
    positions = chosen.get('positions', [chosen.get('choice')])
    for fi, field in enumerate(current_fields, 1):
        fref = reference(field, 'answer-field')
        if 'answers' in chosen:
            kind, value = blank_value(chosen['answers'][fi - 1])
            matches = [(aid, entities[aid]) for aid in field.get('answer-field/choices', [])
                       if entities[aid]['answer/type'] == 'answer.type/' + kind and entities[aid]['answer/value'] == value]
            assert len(matches) <= 1, 'duplicate existing blank values'
            if matches:
                aid, answer = matches[0]
                aref = reference(answer, 'answer')
            else:
                aid = None
                auid = str(ident('answer', f'{rec["key"]}:{fi}:expected'))
                assert auid not in identities, 'expected answer ID already exists with different content'
                aref = prior.quote(f'expected-answer-{rec["key"]}-{fi}')
                statements.append(f'{{:db/id {aref} :answer/id #uuid "{auid}" :answer/type :answer.type/{kind} :answer/value {prior.quote(value)} :db/ensure :answer/validate}}')
                statements.append(f'{{:db/id {fref} :answer-field/choices [{aref}]}}')
                updates.append({'attribute': 'new-answer', 'id': auid, 'type': kind, 'value': value})
        elif chosen.get('added_option'):
            assert rec['topic'] == '4826' and rec['id'] == '80414'
            assert chosen['added_option'] == 'I, II, and III'
            auid = str(ident('answer', f'{rec["key"]}:1:repair'))
            assert auid not in identities, 'repair answer already exists'
            aid = None
            aref = prior.quote(f'repair-answer-{rec["key"]}')
            statements.append(f'{{:db/id {aref} :answer/id #uuid "{auid}" :answer/type :answer.type/text :answer/value "I, II, and III" :db/ensure :answer/validate}}')
            statements.append(f'{{:db/id {fref} :answer-field/choices [{aref}]}}')
            updates.append({'attribute': 'new-answer', 'id': auid, 'type': 'text', 'value': 'I, II, and III'})
        else:
            aid, answer = answer_by_position(rec, fi, positions[fi - 1], field, entities, cache)
            aref = reference(answer, 'answer')
        current = field.get('answer-field/correct')
        assert current is None or current == aid, 'existing correct key conflicts with recovered key'
        if current is None:
            statements.append(f'[:db/cas {fref} :answer-field/correct nil {aref}]')
            statements.append(f'{{:db/id {aref} :db/ensure :answer/validate}}')
            statements.append(f'{{:db/id {fref} :db/ensure :answer-field/validate}}')
            updates.append({'attribute': 'answer-field/correct', 'field_id': field['answer-field/id'], 'answer_id': answer['answer/id'] if aid else auid})
    # Only same-content renderings are candidates for presentation improvements.
    if chosen.get('prompt') and not mc.IMAGE.search(chosen['prompt']) and '{{field-' not in chosen['prompt']:
        value = chosen['prompt']
        if value != question['question/problem']:
            statements.append(cas(qref, 'question/problem', question['question/problem'], value))
            updates.append({'attribute': 'question/problem', 'before': question['question/problem'], 'after': value})
    if rec['format'] == 'multiple-choice' and chosen.get('option_updates'):
        field = current_fields[0]
        seen = set()
        for position, candidate in chosen['option_updates'].items():
            if mc.IMAGE.search(candidate):
                continue
            aid, answer = answer_by_position(rec, 1, int(position), field, entities, cache)
            if aid in seen:
                continue
            seen.add(aid)
            kind, value = ('math', candidate[1:-1].strip()) if re.fullmatch(r'\$[^$]+\$', candidate, re.S) else ('text', candidate)
            aref = reference(answer, 'answer')
            if answer['answer/type'] != 'answer.type/' + kind:
                statements.append(f'[:db/cas {aref} :answer/type :{answer["answer/type"]} :answer.type/{kind}]')
                updates.append({'attribute': 'answer/type', 'answer_id': answer['answer/id'], 'before': answer['answer/type'], 'after': 'answer.type/' + kind})
            if answer['answer/value'] != value:
                statements.append(cas(aref, 'answer/value', answer['answer/value'], value))
                updates.append({'attribute': 'answer/value', 'answer_id': answer['answer/id'], 'before': answer['answer/value'], 'after': value})
    # Feedback is transferred only from fully matched copies. Different feedback
    # texts remain a conflict rather than selecting the newest or longest one.
    feedback = collections.defaultdict(list)
    for entry in good:
        quiz = entry.get('quiz', {})
        if isinstance(quiz.get('feedback'), str) and quiz['feedback'].strip():
            feedback[('question/worked-solution', qref, question.get('question/worked-solution'))].append((quiz['feedback'], entry))
        if rec['format'] != 'multiple-choice' or chosen.get('added_option'):
            continue
        for option in quiz.get('options', []):
            if not isinstance(option.get('feedback'), str) or not option['feedback'].strip():
                continue
            sig = mc.value_signature(str(option.get('content', '')), Path(entry['path']), rec, cache)[0]
            positions_here = [i for i, (kind, value) in enumerate(rec['options'], 1) if mc.source_choice_signature(kind, value, rec, cache) == sig]
            if len(positions_here) != 1:
                continue
            _, answer = answer_by_position(rec, 1, positions_here[0], current_fields[0], entities, cache)
            feedback[('answer/feedback', reference(answer, 'answer'), answer.get('answer/feedback'))].append((option['feedback'], entry))
    for (attr, ref, before), occurrences in feedback.items():
        try:
            values = {render_feedback(text, entry['path']) for text, entry in occurrences}
        except ValueError as error:
            conflicts.append({'attribute': attr, 'reason': str(error)}); continue
        if len(values) != 1:
            conflicts.append({'attribute': attr, 'reason': 'different fully-matched feedback texts', 'sources': [occurrence(e) for _, e in occurrences]}); continue
        value = values.pop()
        if before is not None and before != value:
            conflicts.append({'attribute': attr, 'reason': 'existing feedback differs', 'existing': before}); continue
        if before != value:
            statements.append(cas(ref, attr, before, value))
            updates.append({'attribute': attr, 'ref': ref, 'after': value})
    if statements:
        statements.append(f'{{:db/id {qref} :db/ensure :question/validate}}')
    return statements, updates, conflicts


def raw_audit(rec, paths, questions, cache):
    copies = []
    for path in paths:
        if path not in cache:
            try:
                cache[path] = question_blocks(path.read_text(), questions)
            except (AssertionError, KeyError):
                cache[path] = None
        blocks = cache[path]
        row = {'path': str(path)}
        if blocks is None:
            row['status'] = 'unparsed-question-sections'
        else:
            pos = next(i for i, q in enumerate(questions) if q['question_id'] == rec['id'])
            block = re.split(r'<!--\s*lesson-nav:start\s*-->|```update-progress|\n\[\[MA/', blocks[pos])[0]
            block = prior.clean_option(block)
            if re.search(r'```quiz|==[^=\n]+==|-\s*\[[xX]\]|(?im:^\s*(?:\*\*)?(?:Correct answer|Answer|Solution)\b)', block):
                row['status'] = 'answer-representation-present'
                match = prior.QUIZ.search(block)
                quiz = prior.yaml.safe_load(match[1]) if match else None
                if (isinstance(quiz, dict) and quiz.get('type') == 'radio' and quiz.get('options') and
                        not quiz.get('feedback') and all(not o.get('correct') and not o.get('feedback') for o in quiz['options'])):
                    # A temporary marker invokes the full prompt/choice checker;
                    # it is used only to establish identity of an unkeyed copy.
                    probe = {**quiz, 'options': [{**o, 'correct': i == 0} for i, o in enumerate(quiz['options'])]}
                    evidence = mc.candidate_evidence({'path': str(path), 'line': 0, 'quiz': probe}, rec, {}, {})
                    if evidence['diagnosis'] == 'matched-keyed-content':
                        row['status'] = 'quiz-question-no-key'
            else:
                try:
                    prompt, _ = question_parts(block, questions[pos], rec['topic'])
                    def normalized(text):
                        text = re.sub(r'(?:\n\s*---\s*)+$', '', prior.clean_option(text))
                        return mc.normalized_content(mc.IMAGE.sub(lambda m: '[image:' + Path(m[1].strip('<>')).name + ']', text))
                    row['status'] = 'raw-question-no-key' if normalized(prompt) == normalized(rec['prompt']) else 'raw-prompt-difference'
                except (AssertionError, KeyError):
                    row['status'] = 'raw-layout-difference'
        copies.append(row)
    return copies


def reviewed_radio_select(rec, entries):
    """Recover the five topic-60 radio rewrites by their actual field expressions."""
    if rec['topic'] != '60' or rec['id'] not in {'175528', '181713', '175911', '181714', '178152'}:
        return []
    found = []
    for entry in entries:
        quiz = entry['quiz']
        if quiz.get('type') != 'radio':
            continue
        correct = [o for o in quiz.get('options', []) if o.get('correct') is True]
        if len(correct) != 1:
            continue
        content = quiz.get('content', '')
        answer = correct[0].get('content', '')
        if rec['id'] == '175528':
            tail = 'Expressed in symbolic form, our statement can be written as\n{{field-1}} {{field-2}} {{field-3}}.'
            assert rec['prompt'].endswith(tail)
            expected = rec['prompt'][:-len(tail)] + 'Which symbolic form represents the statement?'
            if mc.normalized_content(content) != mc.normalized_content(expected):
                continue
            symbols = list(answer.strip().strip('$'))
            if len(symbols) != rec['fields']:
                continue
            values = symbols
        else:
            delimiter = 'For the compound statement above, we have that'
            prefix, suffix = rec['prompt'].split(delimiter, 1)
            expected = prefix + 'For the compound statement above, which truth values are correct?'
            if mc.normalized_content(content) != mc.normalized_content(expected):
                continue
            original = re.findall(r'\$([^$]+)\$ is \{\{field-(\d+)\}\}', suffix)
            supplied = re.findall(r'\$([^$]+)\$ is (true|false)', answer)
            if (len(original) != rec['fields'] or len(supplied) != rec['fields'] or
                    [mc.normalized_content(x[0]) for x in original] != [mc.normalized_content(x[0]) for x in supplied] or
                    [int(x[1]) for x in original] != list(range(1, rec['fields'] + 1))):
                continue
            values = [x[1] for x in supplied]
        positions = [fields.select_position(field, value) for field, value in zip(rec['options'], values)]
        found.append({**entry, 'match': {'positions': positions}, 'field_values': values})
    return found


def reviewed_table(rec, entries, source_question):
    review = REVIEWED_TABLES.get((rec['topic'], rec['id']))
    if review is None:
        return None
    source_digest, quiz_digest, position = review
    assert hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == source_digest
    matches = [e for e in entries if hashlib.sha256(json.dumps({k: v for k, v in e['quiz'].items() if k != '_line'}, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == quiz_digest]
    if not matches:
        return None
    # Read complete JSON cell tokens; never split a conditional probability's
    # literal vertical bar as though it were a table delimiter.
    values = {}
    for ci, choice in enumerate(source_question['choices'], 1):
        rows = [re.findall(r'\[MATH: (.*?)\]', line) for line in choice['readable_text'].splitlines()]
        assert len(rows) == 2 and len(rows[0]) == len(rows[1]) and len(rows[0]) >= 3
        rendered = ['| ' + ' | '.join('$' + cell.replace('|', r'\mid ') + '$' for cell in row) + ' |' for row in rows]
        rendered.insert(1, '| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
        values[str(ci)] = '\n'.join(rendered)
    chosen = {**matches[0], 'match': {'choice': position, 'option_updates': values}}
    return chosen, matches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--snapshot', type=Path, default=ROOT / 'before.jsonl')
    ap.add_argument('--out', type=Path, default=ROOT / 'questions')
    args = ap.parse_args()
    scope = json.loads((ROOT / 'scope.json').read_text())
    course_by_topic = {topic: code for code, topics in scope['topics_by_first_course'].items() for topic in topics}
    entities, identities = snapshot(args.snapshot)
    indexed = prior.source_index()
    repairs = json.loads(mc.REPAIRS.read_text())
    ledger = {(r['topic-id'], r['question-id']): r for r in csv.DictReader(mc.LEDGER.open())}
    quiz_cache = {}
    asset_cache = {}
    raw_cache = {}
    records = []
    batches = collections.defaultdict(list)
    for topic in course_by_topic:
        source = prior.DATA / topic / 'Source' / f'{topic}.json'
        if not source.exists():
            continue
        source_questions = [q for q in json.loads(source.read_text())['lesson']['items'] if q['item_type'] == 'question']
        paths = indexed.get(topic, [])
        entries = []
        for path in paths:
            if path not in quiz_cache:
                quiz_cache[path] = prior.quizzes(path)
            entries.extend({'path': str(path), 'line': q['_line'], 'quiz_id': q.get('id'), 'quiz': q} for q in quiz_cache[path])
        for rec in prior.topic_records(topic, {'56649', '156726'}):
            item = {'topic': topic, 'question': rec['id'], 'course': course_by_topic[topic], 'format': rec['format'], 'source': str(source)}
            ledger_row = ledger.get((topic, rec['id']), {})
            item['ledger'] = {k: ledger_row.get(k, '') for k in ('quiz-status', 'quiz-answer-source', 'quiz-answer-labels', 'quiz-answer-rule')}
            good = []
            diagnostic = []
            added = []
            for entry in entries:
                quiz = entry['quiz']
                if rec['format'] == 'multiple-choice':
                    evidence = mc.candidate_evidence(entry, rec, asset_cache, repairs)
                    if evidence['diagnosis'].startswith('matched-keyed-'):
                        good.append({**entry, 'match': evidence['match'], 'asset_evidence': evidence.get('asset_evidence', [])})
                    elif evidence['diagnosis'] == 'registered-added-option-fully-matched':
                        added.append({**entry, 'match': evidence})
                    elif str(quiz.get('id')) in ('ma-' + rec['id'], 'q-' + rec['id']):
                        diagnostic.append(evidence)
                else:
                    match = prior.match_blank(quiz, rec, Path(entry['path'])) or prior.match_select(quiz, rec, Path(entry['path']))
                    if match and 'problem' not in match:
                        good.append({**entry, 'match': match})
            chosen, issue = prior.choose(good)
            if chosen is None and rec['format'] == 'select-list':
                try:
                    mapped = fields.split_select(rec, entries)
                    if mapped:
                        positions, evidence = mapped
                        chosen = {'match': {'positions': positions}, 'path': evidence[0]['path'], 'line': evidence[0]['line'], 'quiz_id': evidence[0]['quiz_id']}
                        good = [e for e in entries if any(e['path'] == v['path'] and e['line'] == v['line'] for v in evidence)]
                        issue = None
                except ValueError as error:
                    item['field_mapping_error'] = str(error)
                if chosen is None:
                    reviewed = reviewed_radio_select(rec, entries)
                    positions = {tuple(e['match']['positions']) for e in reviewed}
                    if len(positions) == 1:
                        good = reviewed
                        chosen = reviewed[0]
                        item['additional_verification'] = 'Radio rewrite retains the exact statement and field expressions; marked option values map uniquely to each original select field.'
                        issue = None
                    elif len(positions) > 1:
                        issue = 'conflicting-radio-select-keys'
            if chosen is None and added and (topic, rec['id']) == ('4826', '80414'):
                chosen = added[0]
                item['additional_verification'] = 'Captured relation is x <= y; statements 3 <= 4, 3 <= 3, 3 <= 3 are all true. Registry-added I, II, and III supplies the missing correct choice.'
                good = added
                issue = None
            if chosen is None and (topic, rec['id']) in REVIEWED_TABLES:
                reviewed = reviewed_table(rec, entries, next(q for q in source_questions if q['question_id'] == rec['id']))
                if reviewed:
                    chosen, good = reviewed
                    item['additional_verification'] = 'Independently verified marginal or conditional probabilities from complete captured joint-distribution tables. Original JSON table headers and all distractor columns retained; defective vault table renderings not imported.'
                    item['review_guards'] = REVIEWED_TABLES[(topic, rec['id'])][:2]
                    issue = None
            if chosen is not None:
                try:
                    statements, updates, feedback_conflicts = staged_forms(rec, chosen['match'], good, entities, identities, asset_cache)
                    item.update(status='recovered' if statements else 'already-current', selected=occurrence(chosen), key=chosen['match'], matching_sources=[occurrence(e) for e in good], updates=updates, feedback_conflicts=feedback_conflicts)
                    if statements:
                        batches[item['course']].append(statements)
                except (AssertionError, KeyError, IndexError) as error:
                    item.update(status='current-state-conflict', reason=str(error), selected=occurrence(chosen), key=chosen['match'])
            else:
                copies = raw_audit(rec, paths, source_questions, raw_cache)
                absent = bool(copies) and all(c['status'] in ('raw-question-no-key', 'quiz-question-no-key') for c in copies)
                item.update(status='absent-from-checked-sources' if absent else issue or 'unmatched', copies=copies, diagnostics=diagnostic)
                if absent and (item['ledger']['quiz-status'] or f'{topic}:ma-{rec["id"]}' in repairs):
                    item['status'] = 'registry-key-needs-review'
            records.append(item)
    args.out.mkdir(parents=True, exist_ok=True)
    for stale in args.out.glob('bulk-*.edn'):
        stale.unlink()
    files = []
    for course in scope['courses']:
        groups = batches[course]
        for i in range(0, len(groups), 75):
            filename = f'bulk-{scope["courses"].index(course)+1:02d}-{course}-{i//75+1:04d}.edn'
            statements = [s for group in groups[i:i+75] for s in group]
            (args.out / filename).write_text('[\n' + '\n'.join(statements) + '\n]\n')
            files.append(filename)
    summary = {'questions': len(records), 'counts': dict(collections.Counter(r['status'] for r in records)),
               'recovered_source_classifications': dict(collections.Counter(r['ledger']['quiz-answer-source'] for r in records if r['status'] == 'recovered')),
               'updates': dict(collections.Counter(u['attribute'] for r in records for u in r.get('updates', []))),
               'by_course': {c: dict(collections.Counter(r['status'] for r in records if r['course'] == c)) for c in scope['courses'] if batches[c] or any(r['course'] == c for r in records)},
               'batch_files': files, 'snapshot': str(args.snapshot), 'snapshot_sha256': hashlib.sha256(args.snapshot.read_bytes()).hexdigest(),
               'basis_t': json.loads(args.snapshot.with_suffix('.manifest.json').read_text())['basis_t']}
    (args.out / 'manifest.json').write_text(json.dumps({**summary, 'records': records}, indent=2, ensure_ascii=False) + '\n')
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
