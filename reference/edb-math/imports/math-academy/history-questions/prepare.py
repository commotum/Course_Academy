#!/usr/bin/env python3
"""Prepare captured MA content only. No database writes or answer derivation."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import uuid
from urllib.parse import urljoin

ROOT = Path('/home/jake/Developer/Course_Academy')
SOURCE = ROOT / 'reference/mathacademy/history-question-import-2026-10-04'
LESSONS = Path('/home/jake/Developer/MA/DATA/Lessons')
MATH = Path('/media/jake/SSD/EDB/math')
OUT = Path('/tmp/math-history-authoritative-prepared')
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from import_historical_question_content import Renderer
from edn import dumps, loads, kw
from bs4 import BeautifulSoup

def identity(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:ma:{kind}:{source}')

def read(path):
    return json.loads(path.read_text())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    selected = {q['math_academy_id'] for q in read(SOURCE / 'format-audit/questions.json')['questions']}
    originals = {q['math_academy_id']: q for q in read(SOURCE / 'prepared.json')['questions']}
    assert len(selected) == 1506 and selected <= originals.keys()
    associations = {q['question_id']: q['associations'] for q in read(ROOT / '.local/edb/missing-question-kp-audit-2026-10-04/audit.json')['questions']}
    observations = read(ROOT / 'reference/mathacademy/progress-history-2026-10-04/observations.json')
    evidence = {(t['source_file'], q['id']): q for t in observations['tasks'] for q in t['questions']}
    live_kps = {row[0][kw('knowledge-point/id')]: row[0] for row in loads(Path('/tmp/math-history-kps-result.edn').read_text())}
    existing = {row[0]: row[1] for row in loads(Path('/tmp/math-history-question-ids-result.edn').read_text())}
    assert not selected.intersection(existing), 'Existing questions require an explicit update plan'
    local_assets = read(SOURCE / 'asset-map.json')['assets']
    ready_assets = read(SOURCE / 'import-ready/asset-map.json')
    image_sources = {key: Path(value) for key, value in local_assets.items()}
    for key, value in ready_assets.items():
        image_sources[key] = Path(value['path'])
    image_manifest = {}
    raw_cache, lesson_cache = {}, {}
    totals = collections.Counter()
    fields_by_type = collections.Counter()
    questions, forms, kp_questions, decisions = [], [], collections.defaultdict(list), []

    def image(src):
        if src not in image_manifest:
            path = Path(src) if src.startswith('/') else image_sources.get(src)
            if path is None or not path.is_file():
                path = image_sources.get(src)
            assert path and path.is_file(), ('Missing captured image', src)
            data = path.read_bytes()
            assert data.startswith(b'\x89PNG\r\n\x1a\n'), ('Not captured PNG', path)
            digest = hashlib.sha256(data).hexdigest()
            relative = f'images/{digest[:2]}/{digest}.png'
            staged = OUT / relative
            staged.parent.mkdir(parents=True, exist_ok=True)
            if not staged.exists():
                staged.write_bytes(data)
            assert staged.read_bytes() == data
            image_manifest[src] = {'source_path': str(path), 'path': relative, 'sha256': digest}
        return image_manifest[src]['path']

    def rewrite(text):
        def replacement(match):
            return match[1] + image(match[2]) + ')'
        text = re.sub(r'(!\[[^\]]*\]\()([^\s)]+)\)', replacement, text)
        assert all(marker not in text for marker in ['[Missing image:', '[MATH:', '[IMG:', 'Your Answer:', 'studentAnswer'])
        return text

    for mid in sorted(selected, key=lambda x: int(x[2:])):
        source = originals[mid]
        topic = int(source['topic_id'])
        if topic not in lesson_cache:
            lesson_cache[topic] = read(LESSONS / str(topic) / 'Source' / f'{topic}.json')
        matches = copy.deepcopy(associations[mid])
        for match in matches:
            if 'source_step_id' not in match:
                captured_steps = [x for x in lesson_cache[topic]['lesson']['items'] if x['item_type'] == 'step' and x['step_type'] == 'example' and str(x['content_id']) == str(match['source_example_id'])]
                assert len(captured_steps) == 1
                match['source_step_id'] = str(captured_steps[0]['step_id'])
        assert len({(int(a['topic_id']), str(a['source_step_id']), str(a['source_example_id'])) for a in matches}) == 1
        match = matches[0]
        assert int(match['topic_id']) == topic
        sid, example = str(match['source_step_id']), str(match['source_example_id'])
        steps = [x for x in lesson_cache[topic]['lesson']['items'] if x['item_type'] == 'step' and x['step_type'] == 'example' and str(x['step_id']) == sid and str(x['content_id']) == example]
        assert len(steps) == 1, ('Source KP/example not found', mid)
        kp_id = identity('kp', sid)
        assert kp_id in live_kps, ('KP missing from new database', mid, kp_id)
        live_example = live_kps[kp_id][kw('knowledge-point/canonical-example')]
        assert live_example.get(kw('question/math-academy-id')) == 'e-' + example, ('Canonical example mismatch', mid)
        # Historical database UUIDs and EIDs are never used as entity references.
        provenance = source.get('provenance', {})
        direct_keys = set()
        if provenance.get('source_kind') == 'completed historical activity':
            file = provenance['source_file']
            original_id = provenance['original_question_id']
            observed = evidence[(file, original_id)]
            if file not in raw_cache:
                captured = read(ROOT / file)
                raw_cache[file] = {q['id']: q for q in captured['questions']}
            raw = raw_cache[file][original_id]
            renderer = Renderer(str(topic))
            prompt_soup = BeautifulSoup(observed['problem_html'], 'html.parser')
            solution_soup = BeautifulSoup(observed['worked_solution_html'], 'html.parser')
            problem = renderer.text(prompt_soup, True)
            solution = renderer.text(solution_soup)
            raw_soup = BeautifulSoup(raw['raw_html'], 'html.parser')
            graphic = raw_soup.find(class_='questionGraphicFrame')
            body = raw_soup.find(class_='questionBody')
            if graphic:
                problem = renderer.text(graphic) + '\n\n' + problem
            if body:
                problem += '\n\n' + renderer.text(body, True)
            assert not renderer.errors, (mid, renderer.errors)
            fields = renderer.fields
            assert problem == source['problem'] and solution == source['worked_solution'], ('Captured content changed', mid)
            assert fields == source.get('answer_fields', []), ('Captured controls changed', mid)
            difficulty = {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[observed['difficulty']]
            assert difficulty == source['difficulty']
            # Values displayed in history's source response boxes are distinct
            # from the submitted response in .studentAnswer. Dropdown keys are
            # explicitly marked .correctSelection by MA.
            direct_keys = {f['key'] for f in fields if f.get('correct_value')}
            totals['historical_questions'] += 1
            source_files = [file]
        else:
            assert source.get('source_kind') == 'automated lesson capture'
            folder = ROOT / 'reference/mathacademy/question-capture/13942892'
            before = read(folder / (mid + '-before.json'))
            history = read(folder / ('history-' + mid + '.json'))
            assert not before['errors'] and not history['errors']
            problem, solution = before['problem'], history['worked_solution']
            assert problem == source['problem'] and solution == source['worked_solution']
            fields = []
            for saved, prepared in zip(before['fields'], source['answer_fields'], strict=True):
                field = {'key': saved['key'], 'type': saved['type'], 'choices': [{k: c[k] for k in ['type', 'value']} for c in saved['choices']]}
                assert field['key'] == prepared['key'] and field['type'] == prepared['type'] and field['choices'] == prepared['choices']
                fields.append(field)
            # The capture's content.json correct_value was selected by the
            # solver. A successful learner submission is not a source key.
            difficulty = source['difficulty']
            metadata = read(folder / 'activity-metadata.json')
            observed = next(x for x in metadata if x['id'] == mid.replace('q-', 'question-'))
            assert difficulty == {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[observed['difficulty']]
            totals['automated_lesson_questions'] += 1
            source_files = [str((folder / (mid + '-before.json')).relative_to(ROOT)), str((folder / ('history-' + mid + '.json')).relative_to(ROOT))]

        record = {'math_academy_id': mid, 'topic_id': topic, 'source_step_id': sid, 'source_example_id': example, 'knowledge_point_id': str(kp_id), 'problem': rewrite(problem), 'worked_solution': rewrite(solution), 'difficulty': difficulty, 'answer_fields': []}
        question = {kw('db/id'): mid, kw('question/id'): identity('question', mid[2:]), kw('question/math-academy-id'): mid, kw('question/problem'): record['problem'], kw('question/worked-solution'): record['worked_solution'], kw('question/difficulty'): kw('question.difficulty/' + difficulty), kw('db/ensure'): kw('question/validate')}
        field_forms = []
        for i, f in enumerate(fields, 1):
            field_id = f'history-{mid}-field-{i}'
            field = {kw('db/id'): field_id, kw('answer-field/id'): identity('history-field', f'{mid}:{i}'), kw('answer-field/key'): f['key'], kw('answer-field/type'): kw('answer-field.type/' + f['type'])}
            answers, seen = [], {}
            captured_field = {'key': f['key'], 'type': f['type'], 'choices': []}
            for j, choice in enumerate(f.get('choices', []), 1):
                kind, value = choice['type'], choice['value']
                if kind == 'image':
                    value = image(value)
                else:
                    value = rewrite(value)
                pair = kind, value
                if pair in seen:
                    continue
                answer_id = f'{field_id}-answer-{j}'
                seen[pair] = answer_id
                answers.append({kw('db/id'): answer_id, kw('answer/id'): identity('history-answer', f'{mid}:{i}:{j}'), kw('answer/type'): kw('answer.type/' + kind), kw('answer/value'): value, kw('db/ensure'): kw('answer/validate')})
                captured_field['choices'].append({'type': kind, 'value': value})
            if answers:
                field[kw('answer-field/choices')] = answers
            if f['key'] in direct_keys:
                value = rewrite(f['correct_value'])
                correct = [aid for (kind, candidate), aid in seen.items() if candidate == value]
                assert len(correct) == 1, ('Captured key not in captured choices', mid, f['key'])
                field[kw('answer-field/correct')] = correct[0]
                field[kw('db/ensure')] = kw('answer-field/validate')
                captured_field['correct_value'] = value
                totals['captured_correct_keys'] += 1
            field_forms.append(field)
            record['answer_fields'].append(captured_field)
            totals['answer_fields'] += 1
            totals['answer_values'] += len(answers)
            fields_by_type[f['type']] += 1
        if field_forms:
            question[kw('question/answer-fields')] = field_forms
            totals['questions_with_captured_controls'] += 1
        else:
            totals['questions_without_captured_controls'] += 1
        placeholders = re.findall(r'\{\{(field-\d+|selection)\}\}', record['problem'])
        assert set(placeholders) <= {f['key'] for f in fields}, ('Dangling response placeholder', mid)
        forms.append(question)
        kp_questions[kp_id].append(mid)
        questions.append(record)
        decisions.append({'math_academy_id': mid, 'source_files': source_files, 'source_topic_id': topic, 'source_step_id': sid, 'source_example_id': example, 'new_knowledge_point_id': str(kp_id), 'captured_controls': len(fields), 'captured_key_fields': sorted(direct_keys), 'local_response_repairs_included': False, 'derived_answer_keys_included': False})
    for kp_id, ids in sorted(kp_questions.items(), key=lambda item: str(item[0])):
        forms.append({kw('db/id'): [kw('knowledge-point/id'), kp_id], kw('knowledge-point/questions'): ids, kw('db/ensure'): kw('knowledge-point/validate')})
    text = '[\n' + '\n'.join(' ' + dumps(f) for f in forms) + '\n]\n'
    assert loads(text) == forms
    assert len(text.encode()) < 16 * 1024 * 1024
    (OUT / 'questions.edn').write_text(';; Captured Math Academy content only. Not transacted.\n;; Transaction source: :org/Math-Academy\n' + text)
    save('questions.json', {'questions': questions})
    save('evidence.json', {'questions': decisions})
    save('asset-map.json', image_manifest)
    report = {'prepared': True, 'transacted': False, 'resolved_at_basis': 70, 'transaction_source': ':org/Math-Academy', 'selected_questions': len(selected), 'knowledge_points': len(kp_questions), 'topics': len({q['topic_id'] for q in questions}), **dict(totals), 'fields_by_type': dict(fields_by_type), 'unique_images': len({x['path'] for x in image_manifest.values()}), 'edn_bytes': (OUT / 'questions.edn').stat().st_size, 'excluded': ['Locally authored choices', 'Reconstructed answer controls and response instructions', 'Keys inferred from worked solutions', 'Solver-selected keys from automated lesson captures', 'Learner submissions, outcomes, times, XP and mastery'], 'verification': ['Original captured HTML rerendered and compared with original extraction', 'Automated choices matched to before-answer capture', 'KP source step/example matched to archived lesson and new database canonical example', 'No questions already present at basis 70', 'All referenced images staged byte-for-byte and named by SHA-256', 'EDN semantic round-trip passed']}
    save('report.json', report)
    (OUT / 'README.md').write_text('# Captured Math Academy historical questions\n\nPrepared only; not transacted. Use `:org/Math-Academy` as the transaction source.\n\n`questions.edn` retains captured prompts, worked solutions, observed difficulty, original answer controls where saved, and membership in existing knowledge points. Missing controls remain absent. Only keys directly displayed by MA in history response controls are included. Solver-selected keys from the separate automated lesson capture are omitted.\n\nThe 1,506-question selection matches `format-audit/questions.json`; content is recovered from the original captures, before response authoring. It includes 1,493 historical questions and 13 questions from the October 4 automated lesson capture. The 69 previously deferred questions remain outside this selection.\n\nImages use `images/<first-two-hash-characters>/<sha256>.png`, relative to the math database folder.\n\n`evidence.json` records the source files and topic/step/example identities used for each question. `report.json` records counts and validation.\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
