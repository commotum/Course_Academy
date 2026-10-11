"""Prepare two attributed transactions; this script has no durable commit path.

The Astra/ultra authors own review/{multiple,defects}.json. This program only
assembles their exact edits, normalizes captured images/layout, and validates.
"""
import collections
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
sys.path.insert(0, str(REPO / 'scripts/question_capture'))
from bs4 import BeautifulSoup
from capture import arguments
from core import ensured, ref, stable_id
from database import Database
from edn import dumps, kw, loads
from image_library import ImageLibrary, image_format
from math_content import build_math_content, field_signature, resolve_knowledge_points
from math_database import SOURCE, validate_receipt

REPAIR_SOURCE = ':agent/gpt-6-astra-ultra'
SNAP = ROOT / 'snapshot'
TX = ROOT / 'transactions'
VALID = ROOT / 'validation'
INDEX = ROOT.parent / 'held-questions.json'
DEST = Path('/media/jake/SSD/EDB/math/imports/math-academy/2026-10-10-held-repairs')


def read(path):
    return json.loads(Path(path).read_text())


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def edn(path, value):
    Path(path).write_text(dumps(value) + '\n')


def transaction(path, forms):
    Path(path).write_text('[\n' + '\n'.join(' ' + dumps(f) for f in forms) + '\n]\n')
    assert loads(Path(path).read_text()) == forms


def snapshot():
    start = read(SNAP / 'starting-state.json')
    assert sha(INDEX) == start['held_index_sha256'], 'Held index changed; replan.'
    existing = {q[':question/math-academy-id']: q for [q] in loads((SNAP / 'questions.edn').read_text())}
    topics = {q[':topic/math-academy-id']: q for [q] in loads((SNAP / 'topics.edn').read_text())}
    return start, existing, topics


def authors():
    merged = {}
    for name in ('multiple', 'defects'):
        data = read(ROOT / 'review' / (name + '.json'))
        records = data.values() if isinstance(data, dict) else data
        for row in records:
            assert row['author_model'] == 'gpt-6-astra' and row['reasoning_effort'] == 'ultra'
            assert row['id'] not in merged
            merged[row['id']] = row
    assert set(merged) == set(read(SNAP / 'starting-state.json')['held_ids'])
    return merged


def roman_layout(problem, html):
    widget = BeautifulSoup(html, 'html.parser').select_one('.questionWidget-text')
    lists = widget.select('ol.questionStatements') if widget else []
    if not lists:
        return problem
    lines = problem.splitlines()
    locations = [i for i, line in enumerate(lines) if line.startswith('- ')]
    assert len(lists) == 1 and len(locations) == len(lists[0].find_all('li', recursive=False)) == 3
    for i, label in zip(locations, ('I. ', 'II. ', 'III. ')):
        lines[i] = label + lines[i][2:]
    return '\n'.join(lines)


def prepared_pair():
    start, existing, topics = snapshot()
    original_reviews = read(ROOT.parent / '2026-10-10-held-complete/held-review.json')
    inputs = read(SNAP / 'source-input.json')
    proposals = authors()
    library = ImageLibrary()
    source, repaired, hashes, evidence, images = {}, {}, {}, {}, {}
    for mid in sorted(proposals):
        proposal, review, occurrence = proposals[mid], original_reviews[mid], inputs[mid]
        directory = Path(review['directory'])
        state, content = read(directory / 'state.json'), read(directory / 'content.json')
        before = state['questions'][mid]['before']
        for name, expected in review['source_hashes'].items():
            assert sha(name) == expected
            hashes[name] = expected
        assert review['source_problem'] == occurrence['source_problem']
        assert review['source_quote'] == occurrence['worked_solution']
        stage = review['solution_location']['json_pointer'].split('/')[3]
        assert state['questions'][mid][stage]['worked_solution'] == review['source_quote']
        assert hashlib.sha256(json.dumps(before, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == review['before_layout_sha256']
        assert len(before['fields']) == 1 and before['fields'][0]['type'] == 'radio'
        choices = [{k: c[k] for k in ('type', 'value')} for c in before['fields'][0]['choices']]
        index = proposal['ma_choice_index']
        assert type(index) is int and 0 <= index < len(choices)
        assert choices[index]['value'] == proposal['ma_answer_value']
        assert choices[index]['type'] == proposal.get('ma_answer_type', choices[index]['type'])
        quote = proposal['evidence']['quote']
        assert isinstance(quote, str) and quote and quote in review['source_quote'], (mid, 'source quotation')
        q = copy.deepcopy(occurrence['prepared_question'])
        q.pop('is_example', None)
        q['topic_id'] = occurrence['topic_id']
        q['problem'] = review['source_problem']
        q['worked_solution'] = review['source_quote']
        q['answer_fields'] = [{'key': before['fields'][0]['key'], 'type': 'radio',
                               'choices': choices, 'correct_value': choices[index]['value']}]
        changed = copy.deepcopy(q)
        touched = set()
        for repair in proposal['repairs']:
            attr = repair['attribute']
            if attr in ('problem', 'worked_solution'):
                assert attr not in touched and repair['old'] == changed[attr], (mid, attr, 'old value')
                assert repair['old'] != repair['new']
                changed[attr] = repair['new']
                touched.add(attr)
            elif attr == 'choice':
                f = next(f for f in changed['answer_fields'] if f['key'] == repair['field_key'])
                ix = repair['choice_index']
                old = repair['old']
                new = repair['new']
                if isinstance(old, str):
                    old = {'type': f['choices'][ix]['type'], 'value': old}
                    new = {'type': old['type'], 'value': new}
                assert f['choices'][ix] == old and old != new
                f['choices'][ix] = new
                if ix == index:
                    f['correct_value'] = new['value']
            else:
                raise AssertionError((mid, 'unsupported repair', attr))
        assert proposal['repairs']
        for obj in (q, changed):
            obj['problem'] = roman_layout(obj['problem'], before['html'])
        q = library.prepare_content(q, directory)
        changed = library.prepare_content(changed, directory)
        context = {'task_type': 'review', 'topic_id': q['topic_id'], 'questions': [q],
                   'canonical_examples': [c for c in content.get('canonical_examples', []) if c.get('knowledge_point_id') == q['knowledge_point_id']],
                   'new_knowledge_points': content.get('new_knowledge_points', [])}
        resolved = resolve_knowledge_points(context, topics, existing)
        assert not resolved['new_knowledge_points']
        q = resolved['questions'][0]
        changed['knowledge_point_id'] = q['knowledge_point_id']
        for obj in (q, changed):
            for f in obj['answer_fields']:
                field_signature(f)
            for image_ref in set(re.findall(r'images/[a-f0-9]{2}/[a-f0-9]{64}\.(?:png|jpg|gif|webp|svg)', json.dumps(obj))):
                path = library.math_root / image_ref
                assert sha(path) == path.stem and path.parent.name == path.stem[:2]
                assert image_format(path.read_bytes()) == path.suffix[1:]
                images[image_ref] = {'sha256': sha(path), 'bytes': path.stat().st_size}
        source[mid], repaired[mid] = q, changed
        evidence[mid] = {'source_location': review['solution_location'], 'quote': quote,
                         'original_choice_index': index, 'original_choice': choices[index],
                         'capture': str(directory), 'source_hashes': review['source_hashes'],
                         'before_layout_sha256': review['before_layout_sha256'],
                         'source_problem_preserved': True, 'source_solution_preserved': True,
                         'all_original_choices_preserved': True,
                         'normalizations': ['canonical image paths', 'original Roman list labels where present']}
    save(ROOT / 'original-content.json', source)
    save(ROOT / 'repaired-content.json', repaired)
    save(ROOT / 'source-evidence.json', evidence)
    save(ROOT / 'source-hashes.json', hashes)
    save(ROOT / 'image-verification.json', {'valid': True, 'references': images})
    save(ROOT / 'repair-plan.json', proposals)
    return source, repaired


def guards(existing):
    answers = sorted({a[':db/id'] for q in existing.values() for f in q.get(':question/answer-fields', []) for a in f.get(':answer-field/choices', [])})
    fields = [[f[':db/id'], kw(attr)] for q in existing.values() for f in q.get(':question/answer-fields', [])
              for attr in ('answer-field/id', 'answer-field/key', 'answer-field/type', 'answer-field/correct', 'answer-field/choices') if ':' + attr in f]
    return {'immutable_answers': answers, 'immutable_fields': fields}


def stage_questions(stage):
    return {mid: q for mid, q in loads((VALID / ('stage%d-questions.edn' % stage)).read_text())}


def prepare_original():
    start, existing, topics = snapshot()
    source, repaired = prepared_pair()
    forms, report = build_math_content({'task_type': 'review', 'questions': list(source.values()), 'canonical_examples': []}, topics, existing)
    transaction(TX / '001-math-academy-original.edn', forms)
    edn(VALID / 'stage1-guards.edn', dict(guards(existing), retractions=report['retractions']))
    edn(ROOT / 'question-ids.edn', sorted(source))
    save(ROOT / 'original-plan.json', {'basis': start['basis'], 'source': SOURCE,
         'questions': len(source), 'new': len(source)-len(existing), 'existing': len(existing),
         'forms': len(forms), 'planned_retractions': len(report['retractions']), 'transacted': False})
    print('Prepared stage 1:', len(source), 'questions;', len(forms), 'forms')


def prepare_repair():
    start, previous_existing, topics = snapshot()
    source, repaired = read(ROOT / 'original-content.json'), read(ROOT / 'repaired-content.json')
    existing = stage_questions(1)
    assert set(existing) == set(source)
    forms, retracts, log = [], [], []
    for mid, q in sorted(repaired.items()):
        old = existing[mid]
        target = ref('question/id', old[':question/id'])
        changes = []
        for attr, key in [('question/problem', 'problem'), ('question/worked-solution', 'worked_solution')]:
            assert old[':' + attr] == source[mid][key]
            if q[key] != source[mid][key]:
                forms.append([kw('db/cas'), target, kw(attr), source[mid][key], q[key]])
                retracts.append([old[':db/id'], kw(attr), source[mid][key]])
                changes.append({'attribute': ':' + attr, 'operation': 'compare-and-swap'})
        old_fields = {f[':answer-field/key']: f for f in old[':question/answer-fields']}
        for field in q['answer_fields']:
            previous = old_fields[field['key']]
            if field_signature(field) == field_signature(previous, stored=True):
                continue
            signature = field_signature(field)
            token = mid + '/gpt-6-astra-ultra-repair-field/' + hashlib.sha256(json.dumps(signature, ensure_ascii=False).encode()).hexdigest()
            old_answers = {(a[':answer/type'][':db/ident'].split('/')[-1], a[':answer/value']): a for a in previous[':answer-field/choices']}
            links, correct, created, copied = [], None, [], []
            for kind, value in signature[2]:
                answer = old_answers.get((kind, value))
                # Answers are field-scoped components: never share across fields.
                # A revised field needs fresh component identities even for its
                # unchanged values; the old field and all its answers survive.
                link = token + '/answer/' + hashlib.sha256((kind + ':' + value).encode()).hexdigest()
                forms.append(ensured('answer', **{'db/id': link, 'answer/id': stable_id('answer', link),
                             'answer/type': kw('answer.type/' + kind), 'answer/value': value}))
                if answer:
                    copied.append({'old_uuid': str(answer[':answer/id']), 'new_uuid': str(stable_id('answer', link)), 'value': value})
                else:
                    created.append(value)
                links.append(link)
                if (kind, value) == signature[3]:
                    correct = link
            assert correct is not None
            forms.append(ensured('answer-field', **{'db/id': token, 'answer-field/id': stable_id('field', token),
                         'answer-field/key': field['key'], 'answer-field/type': kw('answer-field.type/' + field['type']),
                         'answer-field/choices': links, 'answer-field/correct': correct}))
            forms.append([kw('db/retract'), target, kw('question/answer-fields'), ref('answer-field/id', previous[':answer-field/id'])])
            forms.append([kw('db/add'), target, kw('question/answer-fields'), token])
            retracts.append([old[':db/id'], kw('question/answer-fields'), previous[':db/id']])
            changes.append({'attribute': ':question/answer-fields', 'operation': 'replace ownership; retain previous field and answers',
                            'old_field_uuid': str(previous[':answer-field/id']), 'new_field_uuid': str(stable_id('field', token)),
                            'unchanged_values_copied_to_new_field_scoped_entities': copied, 'new_answer_values': created})
        assert changes, mid
        forms.append({kw('db/id'): target, kw('db/ensure'): [kw('question/validate')]})
        log.append({'id': mid, 'changes': changes})
    transaction(TX / '002-astra-surgical-repairs.edn', forms)
    edn(VALID / 'stage2-guards.edn', dict(guards(existing), retractions=retracts))
    save(ROOT / 'repair-operations.json', log)
    save(ROOT / 'repair-stage-plan.json', {'source': REPAIR_SOURCE, 'questions': len(log), 'forms': len(forms),
                                          'planned_retractions': len(retracts), 'transacted': False})
    print('Prepared stage 2:', len(log), 'questions;', len(forms), 'forms;', len(retracts), 'retractions')


def validate():
    start, base, topics = snapshot()
    attrs = loads((SNAP / 'attributes.edn').read_text())
    names = {e: str(a) for e, a in attrs}
    srcids = start['source_entities']
    original = read(ROOT / 'original-content.json')
    repaired = read(ROOT / 'repaired-content.json')
    summary = []
    for stage, source, expected in [(1, SOURCE, original), (2, REPAIR_SOURCE, repaired)]:
        receipt = loads((VALID / ('stage%d-preview.edn' % stage)).read_text())
        guard = loads((VALID / ('stage%d-guards.edn' % stage)).read_text())
        assert receipt[':edb/db-before-t'] == start['basis'] + stage - 1
        assert receipt[':edb/db-after-t'] == start['basis'] + stage
        validate_receipt(receipt, attrs, srcids[source], **guard)
        actual = stage_questions(stage)
        assert set(actual) == set(expected)
        changed_questions = set()
        for mid, want in expected.items():
            got = actual[mid]
            assert got[':question/id'] == (base[mid][':question/id'] if mid in base else stable_id('question', mid)), mid
            assert got[':question/problem'] == want['problem'] and got[':question/worked-solution'] == want['worked_solution'], mid
            assert {field_signature(f, stored=True) for f in got[':question/answer-fields']} == {field_signature(f) for f in want['answer_fields']}, mid
            assert {str(p[':knowledge-point/id']) for p in got[':knowledge-point/_questions']} == {want['knowledge_point_id']}, mid
            assert not got.get(':knowledge-point/_canonical-example'), mid
            if want.get('difficulty'):
                assert got[':question/difficulty'][':db/ident'] == ':question.difficulty/' + want['difficulty']
            if want.get('requires_calculator') is not None:
                assert got[':question/requires-calculator'] == want['requires_calculator']
        allowed_q = {q[':db/id'] for q in actual.values()}
        allowed_f = {f[':db/id'] for q in actual.values() for f in q[':question/answer-fields']}
        allowed_a = {a[':db/id'] for q in actual.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
        for e, a, v, t, s, added in receipt[':edb/tx-data']:
            attr = names[a]
            assert s == srcids[source]
            if attr.startswith(':question/'):
                assert e in allowed_q
                changed_questions.add(e)
                if stage == 2:
                    assert attr in {':question/problem', ':question/worked-solution', ':question/answer-fields'}
            elif attr.startswith(':answer-field/'):
                assert e in allowed_f
            elif attr.startswith(':answer/'):
                assert e in allowed_a
            elif attr.startswith(':knowledge-point/'):
                assert stage == 1 and attr == ':knowledge-point/questions' and v in allowed_q
            else:
                assert attr == ':db/txInstant'
        if stage == 2:
            assert changed_questions == allowed_q
            before = stage_questions(1)
            for mid in before:
                for attr in set(before[mid]) | set(actual[mid]):
                    if attr not in {':question/problem', ':question/worked-solution', ':question/answer-fields'}:
                        assert before[mid].get(attr) == actual[mid].get(attr), (mid, attr, 'unsolicited repair')
        summary.append({'stage': stage, 'source': source, 'questions': len(actual),
                        'datoms': len(receipt[':edb/tx-data']), 'exact_retractions': len(guard['retractions']),
                        'all_fields_verified': True, 'identities_preserved': True, 'knowledge_points_verified': True,
                        'old_component_definitions_untouched': True, 'attribution_verified': True})
    assert all(sha(path) == value for path, value in read(ROOT / 'source-hashes.json').items())
    helper = loads((VALID / 'manifest.edn').read_text())
    assert helper[':preview/durable-basis-before'] == helper[':preview/durable-basis-after'] == start['basis']
    assert helper[':preview/database-writes'] == 0 and helper[':edb/committed'] is False
    save(ROOT / 'verification.json', {'valid': True, 'prepared_basis': start['basis'], 'stages': summary,
         'held_index_unchanged': sha(INDEX) == start['held_index_sha256'], 'database_writes': 0,
         'transacted': False, 'sequential_preview_helper': helper})
    print('Verified both speculative stages at basis', start['basis'])


if __name__ == '__main__':
    mode = sys.argv[1]
    {'original': prepare_original, 'repair': prepare_repair, 'verify': validate}[mode]()
