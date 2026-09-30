#!/usr/bin/env python3
"""Recover explicit answers for unmatched MA free/select fields, without DB writes.

The answer ledgers are corroborated against DATA JSON and the actual vault quiz
at a topic-matched path. Split select quizzes and converted radio composites are
mapped back to every existing answer-field and choice UUID.
"""

import collections
import csv
import json
import re
from pathlib import Path

from generate_ma_lesson_seed import ident
from reconcile_ma_instruction import resolve_images
from reconcile_ma_questions import (DATA, UNDERLINE, forms, norm, quote, topic_records,
                                    uid, value_sig, seeded_choice_index)

ROOT = Path('.local/edb/reconciliation')
UTIL = Path('/home/jake/Developer/study/util')
OUT = ROOT / 'followup-fields'
COURSES = ('MF1', 'MF2', 'MF3', 'LAL', 'MVC', 'DEQ', 'CA1', 'CA2')
ANSWER = re.compile(r'==(.+?)==')
IMAGE = re.compile(r'!\[[^]]*\]\((?:<[^>]+>|[^)]+)\)')
SPLIT_ID = re.compile(r'^ma-(\d+)-select-(\d+)$')

# Values were read from the single marked radio option in each repaired vault
# quiz. An exact, unique match to each corresponding captured field is required.
RADIO_VALUES = {
    '4026:210858': ['first', '7'], '4026:210859': ['second', '-3'],
    '4026:210947': ['second', '10'], '4026:211000': ['first', '-5'],
    '4236:211003': ['4', '5'], '4236:211005': ['3', '-8'],
    '4236:211006': ['2', '3'], '4236:211007': ['2', '-5'],
    '493:211984': ['a single solution'], '493:237043': ['infinitely many solutions'],
    '493:237046': ['no solutions'], '493:237095': ['intersect at infinitely many points'],
    '493:211986': ['do not intersect'],
    '4638:223036': ['no solutions', 'are parallel (non-intersecting)'],
    '4638:237129': ['intersect at one point', 'only one solution', 'consistent independent'],
    '4638:223043': ['coincide with each other', 'infinitely many solutions', 'consistent dependent'],
    '4638:237133': ['consistent independent'], '4638:211985': ['consistent dependent'],
    '1317:236887': ['simple', 'concave'],
    '118:277702': ['-', '+', '+'], '118:278467': ['+', '+', '+'],
}

# The answer registry's rendered full equation includes a suffix already
# printed after the original single blank. Preserve the captured problem and
# store only the expression that belongs in that field.
FIELD_VALUE_OVERRIDES = {
    '813:218426': ['${4x^2 - 3x}$'],
    '813:221838': ['${z^2 - 3z}$'],
}


def read_csv(name):
    with (UTIL / name).open(newline='', encoding='utf-8') as stream:
        return {f"{r['topic-id']}:{r['question-id']}": r for r in csv.DictReader(stream)}


def layout_signature(value):
    number = [0]

    def image(_):
        number[0] += 1
        return f'{{{{image-{number[0]}}}}}'

    return re.sub(r'\s+', ' ', IMAGE.sub(image, value)).strip()


def occurrence(record):
    return {'path': record['path'], 'line': record['line'],
            'quiz_id': record['quiz'].get('id'), 'type': record['quiz'].get('type')}


def companion_matches(record, topic, source_question):
    path = Path(record['path'])
    companion = path.parent.parent / 'Source' / path.stem / f'{topic}.json'
    if not companion.is_file():
        return False
    data = json.loads(companion.read_text())
    matches = [q for q in data['lesson']['items'] if q.get('question_id') == source_question['question_id']]
    if len(matches) != 1:
        return False
    q = matches[0]
    return (q['question_format'] == source_question['question_format']
            and q['question_number'] == source_question['question_number']
            and q['prompt']['readable_text'] == source_question['prompt']['readable_text'])


def source_image_names(problem):
    return candidate_image_names(problem)


def candidate_image_names(content):
    return {Path(match.group(0).split('(', 1)[1].rstrip(')>')).name for match in IMAGE.finditer(content)}


def field_forms(rec, positions):
    result = []
    for fi, ci in enumerate(positions, 1):
        fref = f'[:answer-field/id {uid("field", f"{rec["key"]}:{fi}")}]'
        canonical = seeded_choice_index(rec, fi, ci)
        aref = f'[:answer/id {uid("answer", f"{rec["key"]}:{fi}:{canonical}")}]'
        result.extend([f'{{:db/id {fref} :answer-field/correct {aref}}}',
                       f'{{:db/id {aref} :db/ensure :answer/validate}}',
                       f'{{:db/id {fref} :db/ensure :answer-field/validate}}'])
    result.append(f'{{:db/id [:question/id {uid("question", rec["key"])}] :db/ensure :question/validate}}')
    return result


def select_position(field, value):
    positions = [i for i, (_, candidate) in enumerate(field, 1) if norm(candidate) == norm(value)]
    if len(positions) != 1:
        raise ValueError(f'select value {value!r} maps to {positions} in {field}')
    return positions[0]


def select_sig(value, path):
    """Normalize TeX fraction/integral spelling without algebraic inference."""
    base = value_sig(value, path)
    if base is None:
        return None

    def group(text, start):
        if start >= len(text) or text[start] != '{':
            raise ValueError('unbraced TeX fraction in select option')
        depth = 0
        for i in range(start, len(text)):
            depth += (text[i] == '{') - (text[i] == '}')
            if depth == 0:
                return text[start + 1:i], i + 1
        raise ValueError('unclosed TeX fraction in select option')

    def fractions(text):
        while '\\frac' in text:
            start = text.index('\\frac')
            num, after_num = group(text, start + 5)
            den, after_den = group(text, after_num)
            text = text[:start] + '(' + fractions(num) + ')/(' + fractions(den) + ')' + text[after_den:]
        return text

    converted = fractions(value).replace('\\int', '∫')
    return (norm(converted), base[1])


def split_select(rec, records):
    fields = {}
    for record in records:
        quiz = record['quiz']
        match = SPLIT_ID.fullmatch(str(quiz.get('id', '')))
        if not match or match[1] != rec['id'] or quiz.get('type') != 'select':
            continue
        fi = int(match[2])
        if fi < 1 or fi > rec['fields']:
            raise ValueError(f'split field {fi} outside DATA field count')
        underlines = [0]
        def placeholder(_):
            underlines[0] += 1
            return '{{field-' + str(underlines[0]) + '}}'
        if norm(UNDERLINE.sub(placeholder, quiz.get('content', ''))) != norm(rec['prompt']):
            raise ValueError(f'split quiz prompt differs from DATA for field {fi}')
        opts = quiz.get('options') or []
        actual = [select_sig(str(o.get('content', '')), Path(record['path'])) for o in opts]
        expected = [select_sig(f'${v}$' if t == 'math' else v, DATA / rec['topic'] / f'{rec["topic"]}.md')
                    for t, v in rec['options'][fi - 1]]
        if None in actual or None in expected or collections.Counter(actual) != collections.Counter(expected):
            raise ValueError(f'split option set differs from DATA field {fi}')
        keys = [q.get('correct_option') for q in quiz.get('questions', []) if isinstance(q, dict)]
        if len(keys) != 1:
            raise ValueError(f'split field {fi} has no unique key')
        selected = [o for o in opts if o.get('id') == keys[0]]
        if len(selected) != 1:
            raise ValueError(f'split field {fi} key does not identify one option')
        signature = select_sig(str(selected[0].get('content', '')), Path(record['path']))
        positions = [i for i, x in enumerate(expected, 1) if x == signature]
        if len(positions) != 1:
            raise ValueError(f'split field {fi} correct value is ambiguous')
        fields.setdefault(fi, []).append((positions[0], record))
    if not fields:
        return None
    if set(fields) != set(range(1, rec['fields'] + 1)):
        raise ValueError(f'incomplete split field coverage: {sorted(fields)}')
    positions = []
    evidence = []
    for fi in range(1, rec['fields'] + 1):
        choices = {position for position, _ in fields[fi]}
        if len(choices) != 1:
            raise ValueError(f'conflicting split keys in field {fi}: {sorted(choices)}')
        positions.append(choices.pop())
        evidence.extend(occurrence(item) for _, item in fields[fi])
    return positions, evidence


def radio_select(rec, records, key, repairs):
    if key not in RADIO_VALUES:
        return None
    repair_key = key.replace(':', ':ma-', 1)
    if repair_key not in repairs or repairs[repair_key].get('type') != 'radio':
        raise ValueError('radio composite lacks vetted repair registry entry')
    hits = [r for r in records if r['quiz'].get('id') == 'ma-' + rec['id']
            and r['quiz'].get('type') == 'radio']
    if not hits:
        raise ValueError('radio composite registry entry has no actual quiz')
    selected_texts = []
    for item in hits:
        opts = item['quiz'].get('options') or []
        marked = [o for o in opts if o.get('correct') is True]
        if len(marked) != 1:
            raise ValueError('radio composite has nonunique marked option')
        selected_texts.append(str(marked[0].get('content', '')))
        if marked[0].get('id') != repairs[repair_key]['correct']:
            raise ValueError('marked radio option differs from vetted repair registry')
    if len({norm(x) for x in selected_texts}) != 1:
        raise ValueError('radio composite copies disagree')
    values = RADIO_VALUES[key]
    if len(values) != rec['fields']:
        raise ValueError('radio composite field count differs')
    selected = norm(selected_texts[0])
    if key.startswith('118:'):
        signs = re.findall(r'(?<!\w)[+\-](?!\w)', selected_texts[0].replace('−', '-'))
        if signs != values:
            raise ValueError(f'sign sequence {signs} differs from field mapping {values}')
    elif any(norm(v) not in selected for v in values):
        raise ValueError('field value not expressed in marked composite answer')
    return [select_position(field, value) for field, value in zip(rec['options'], values)], [occurrence(x) for x in hits]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob('*.edn'):
        old.unlink()
    manifest = json.loads((ROOT / 'questions/manifest.json').read_text())
    scope = json.loads((ROOT / 'scope.json').read_text())
    prior_absent = json.loads((ROOT / 'absent-key-audit.json').read_text())
    absent = {(x['topic'], x['question']): x for x in prior_absent['questions']}
    all_index = json.loads((ROOT / 'vault-audit/index.json').read_text())
    quizzes = collections.defaultdict(list)
    for entry in all_index['quizzes']:
        qid = entry['quiz'].get('id')
        if isinstance(qid, str) and qid.startswith('ma-'):
            for topic in entry['topic_ids']:
                quizzes[(topic, qid[3:].split('-select-', 1)[0])].append(entry)
    ledger = read_csv('ma_free_response_answer_key.csv')
    historical = read_csv('ma_imported_free_response_manifest.csv')
    layouts = json.loads((UTIL / 'ma_free_response_layouts.json').read_text())
    repairs = json.loads((UTIL / 'ma_missing_answer_repairs.json').read_text())
    shape_review = json.loads((ROOT / 'field-shape-review.json').read_text())
    course_for_topic = {topic: course for course in COURSES
                        for topic in scope['topics_by_first_course'][course]}
    records_by_topic = {}
    results = []
    batches = collections.defaultdict(list)
    for item in manifest['unresolved']:
        if item['reason'] != 'unmatched':
            continue
        topic, qid = item['topic'], item['question']
        source = json.loads((DATA / topic / 'Source' / f'{topic}.json').read_text())
        question = next(q for q in source['lesson']['items'] if q.get('question_id') == qid)
        kind = question['question_format']
        if kind not in ('free-response', 'select-list'):
            continue
        if topic not in records_by_topic:
            records_by_topic[topic] = {r['id']: r for r in topic_records(topic, {'56649', '156726'})}
        rec = records_by_topic[topic][qid]
        key = f'{topic}:{qid}'
        entry = {'topic': topic, 'question': qid, 'course': course_for_topic[topic],
                 'format': kind, 'fields': rec['fields'],
                 'data_json': str(DATA / topic / 'Source' / f'{topic}.json')}
        records = [r for r in quizzes[(topic, qid)] if companion_matches(r, topic, question)]
        try:
            if (topic, qid) in absent:
                entry['status'] = 'source question found without key'
                entry['reason'] = 'all associated copies have matching raw question blocks and no marked answer'
                entry['evidence'] = absent[(topic, qid)]['copies']
            elif kind == 'free-response' and key in ledger:
                meta = historical[key]
                if meta['source-prompt'] != question['prompt']['readable_text'] or int(meta['source-blank-count']) != rec['fields'] or int(meta['question-number']) != question['question_number']:
                    raise ValueError('historical ledger does not match DATA prompt, number, and field count')
                layout_answers = ANSWER.findall(layouts[key])
                matches = [r for r in records if r['quiz'].get('id') == 'ma-' + qid
                           and r['quiz'].get('type') == 'blank'
                           and layout_signature(r['quiz'].get('content', '')) == layout_signature(layouts[key])
                           and companion_matches(r, topic, question)]
                if not matches:
                    raise ValueError('no topic-matched blank quiz, answer layout, and companion JSON agree')
                for r in matches:
                    if ANSWER.findall(r['quiz']['content']) != layout_answers:
                        raise ValueError('vault blank answer differs from ledger')
                if key in shape_review:
                    review = shape_review[key]
                    if review['source_prompt'] != rec['prompt'] or review['vault_layout'] != layouts[key]:
                        raise ValueError('manual field-shape guards differ from current source/layout')
                    answers = review['answers']
                    mapping = 'reviewed original-field shape'
                else:
                    answers = FIELD_VALUE_OVERRIDES.get(key, layout_answers)
                    mapping = 'exact blank layout to original DATA fields'
                if len(answers) != rec['fields'] or not all(answers):
                    raise ValueError('answer count does not cover all original DATA fields')
                selected = min(matches, key=lambda r: (0 if '/vault/MA/' in r['path'] else 1, r['path']))
                source_names = source_image_names(rec['prompt'])
                selected_names = candidate_image_names(selected['quiz']['content'])
                if selected_names != source_names:
                    raise ValueError(f'candidate image names {selected_names} differ from DATA question images {source_names}')
                # The imported DATA problem already carries every original
                # {{field-N}} location. Some vault layouts abbreviate givens,
                # so retaining it also preserves the complete question.
                statements = forms(rec, {'match': {'answers': answers}})
                entry.update({'status': 'answer located and mapped', 'mapping': mapping,
                              'answers': answers, 'ledger': str(UTIL / 'ma_free_response_answer_key.csv'),
                              'historical_manifest': str(UTIL / 'ma_imported_free_response_manifest.csv'),
                              'evidence': [occurrence(r) for r in matches],
                              'source_problem_retained': True,
                              'manual_shape_source': str(ROOT / 'field-shape-review.json') if key in shape_review else None})
                batches[entry['course']].append(statements)
            elif kind == 'select-list':
                mapped = split_select(rec, records)
                mapping_kind = 'one keyed select quiz per DATA field'
                if mapped is None:
                    mapped = radio_select(rec, records, key, repairs)
                    mapping_kind = 'marked radio statement resolved to all DATA select fields'
                if mapped is None:
                    raise ValueError('no keyed select representation found')
                positions, evidence = mapped
                entry.update({'status': 'answer located and mapped', 'mapping': mapping_kind,
                              'choice_indexes': positions,
                              'choice_values': [rec['options'][fi][ci - 1][1] for fi, ci in enumerate(positions)],
                              'evidence': evidence})
                batches[entry['course']].append(field_forms(rec, positions))
            else:
                entry.update({'status': 'source absent', 'reason': 'no topic-matched source key or verified raw-question block',
                              'candidate_files': item['candidate_files']})
        except (ValueError, KeyError, IndexError) as error:
            entry.update({'status': 'semantic ambiguity/format blocker', 'reason': str(error),
                          'candidate_quizzes': [occurrence(r) for r in records]})
        results.append(entry)
    files = []
    for course in COURSES:
        groups = batches[course]
        for i in range(0, len(groups), 75):
            name = f'{course}-{i // 75 + 1:04d}.edn'
            statements = [line for group in groups[i:i + 75] for line in group]
            (OUT / name).write_text('[\n' + '\n'.join(statements) + '\n]\n')
            files.append(name)
    counts = collections.Counter(x['status'] for x in results)
    payload = {'scope': list(COURSES), 'counts': dict(counts), 'questions': results,
               'apply_batches_in_order': files,
               'evidence_index': str(ROOT / 'vault-audit/index.json'),
               'no_key_audit': str(ROOT / 'absent-key-audit.json')}
    (OUT / 'manifest.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'counts': dict(counts), 'files': files}, indent=2))


if __name__ == '__main__':
    main()
