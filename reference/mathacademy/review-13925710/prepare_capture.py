"""Normalize this completed review from saved HTML only; no website requests."""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
sys.path.insert(0, str(PROJECT / 'scripts/question_capture'))
from core import atomic_json, build_transaction
from edn import dumps, loads
from progress import changes, normalize_course
from playwright.sync_api import sync_playwright


def read(name):
    return json.loads((ROOT / name).read_text())


def main():
    history, live, assets = read('activity-capture.json'), read('live-capture.json'), read('assets/manifest.json')
    topic = loads((ROOT / 'database/topic.edn').read_text())[0][0]
    kps = {kp[':knowledge-point/title']: str(kp[':knowledge-point/id']) for kp in topic[':topic/knowledge-points']}
    extractor = (PROJECT / 'scripts/question_capture/dom.js').read_text()
    assert len(assets) == 21
    image_report = []
    for url, asset in assets.items():
        data = Path(asset['path']).read_bytes()
        assert data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR'
        width, height = struct.unpack('>II', data[16:24])
        assert width > 0 and height > 0
        image_report.append({**asset, 'sha256': hashlib.sha256(data).hexdigest(), 'width': width, 'height': height})

    content = {'task_id': live['task_id'], 'task_type': 'review', 'topic_id': live['topic_id'],
               'questions': [], 'canonical_examples': [], 'source_url': history['source_url']}
    responses = {r['question_id']: r for r in live['responses']}
    assert len(history['questions']) == len(responses) == 4
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.route('**/*', lambda route: route.abort())

        def extract(html):
            page.set_content(html, wait_until='domcontentloaded')
            result = page.locator('body > div').evaluate(extractor)
            assert not result['errors'], result['errors']
            for asset in result['assets']:
                source = re.search(r'src="([^"]+)"', asset['html'])
                if not source:
                    continue
                url = source[1]
                if url.startswith('/'):
                    url = 'https://mathacademy.com' + url
                token = '@asset-' + str(asset['index']) + '@'
                if url in assets:
                    result['problem'] = result['problem'].replace(token, assets[url]['path'])
                    result['worked_solution'] = result['worked_solution'].replace(token, assets[url]['path'])
            return result

        for record in history['questions']:
            qid = record['id'].removeprefix('question-')
            before, after = read('q' + qid + '-before.json'), read('q' + qid + '-after.json')
            prompt = extract(before['html'])['problem']
            solution = extract(record['explanation_html'])['worked_solution']
            assert prompt and solution and '@asset-' not in prompt + solution, (qid, prompt, solution)
            choices = before['fields'][0]['choices']
            assert len(choices) == 5 and before['fields'][0]['type'] == 'radio'
            response = responses[qid]
            correct = next(c for c in choices if c['option'] == response['correct_option'])
            # Check the visible explanation independently of the image naming convention.
            live_solution = extract(after['html'])['worked_solution']
            assert correct['value'] in live_solution
            assert re.fullmatch(r'/topics/2084#\d+', record['kp_href'])
            content['questions'].append({
                'math_academy_id': 'q-' + qid,
                'knowledge_point_id': kps[record['kp_title']],
                'difficulty': {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[record['difficulty']],
                'problem': prompt, 'worked_solution': solution,
                'answer_fields': [{**before['fields'][0], 'correct_value': correct['value']}],
                'provenance': {'knowledge_point_title': record['kp_title'], 'knowledge_point_href': record['kp_href'],
                               'live_before': 'q' + qid + '-before.json', 'live_after': 'q' + qid + '-after.json',
                               'activity': 'activity-capture.json', 'correct_answer_evidence': 'Visible worked explanation graph'},
            })
            assert response['actual_result'] == after['result']
        browser.close()

    transaction, reconciliation = build_transaction(content, topic, {})
    atomic_json(ROOT / 'content.json', content)
    (ROOT / 'database/transaction.edn').write_text(dumps(transaction) + '\n')
    atomic_json(ROOT / 'database/reconciliation.json', reconciliation)
    snapshots = []
    for event in live['knowledge_snapshots']:
        snapshot = read('knowledge-state/' + event + '.json')
        for course in snapshot['courses']:
            course['topics'] = normalize_course(course['course_id'], {**course, 'rows': course['topics']})
        assert sum(len(c['topics']) for c in snapshot['courses']) == 1040
        snapshots.append(snapshot)
    profile_report = {
        'scope': 'Complete displayed topic color state for courses 113, 111, 136',
        'limitations': 'Not exact continuous repetitions or full internal FIRe state. Courses read sequentially. Darkest blue=6 is a local convention.',
        'snapshots': [{'event': s['event'], 'changes': changes(snapshots[i-1], s) if i else [],
                       'course_topic_rows': sum(len(c['topics']) for c in s['courses'])} for i, s in enumerate(snapshots)],
        'overall_changes': changes(snapshots[0], snapshots[-1]),
    }
    atomic_json(ROOT / 'knowledge-state/verification.json', profile_report)
    verification = {'task_id': live['task_id'], 'questions': len(content['questions']),
                    'worked_solutions': len(content['questions']), 'choices': 20,
                    'images': image_report, 'snapshots': len(snapshots),
                    'new_database_questions_at_basis_305': len(content['questions']),
                    'transaction_maps': len(transaction), 'database_committed': False}
    atomic_json(ROOT / 'verification.json', verification)
    print(json.dumps({k: v for k, v in verification.items() if k != 'images'}, indent=2))
    print(json.dumps(profile_report['overall_changes'], indent=2))


if __name__ == '__main__':
    main()
