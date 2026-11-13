"""Bind UI/field geometry and actual grading evidence to the final records."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_evidence import record_sha256

def read(path):
    return json.loads((H/path).read_text())

records = read('final-validation/records-after.json')
final = {r['generation']['entity']: r for r in records}
expected_hash = {qid: record_sha256(r) for qid,r in final.items()}
sources = [(H/'recoverable-validation/records-after.json', H/'recoverable-validation'/('render-'+s)) for s in ('active', 'completed')]
sources += [(H/f'validation/shard-{i}/records.json', H/f'validation/shard-{i}'/('render-'+s)) for i in range(4) for s in ('active', 'completed')]
sources += [(H/'final-validation/completion-records.json', H/'final-validation/completion-render')]
sources += [(p, p.parent/('render-'+s)) for p in (H/'extension-validation').glob('shard-*/records.json') for s in ('active', 'completed')]
seen, verified, stale, grids = defaultdict(set), [], 0, 0
for input_path, directory in sources:
    if not (directory/'rendering.json').exists():
        continue
    inputs = json.loads(input_path.read_text())
    report = json.loads((directory/'rendering.json').read_text())
    assert report['passed'], directory
    for case in report['cases']:
        record = inputs[case['index']]
        qid = record['generation']['entity']
        if case['record_sha256'] != expected_hash[qid]:
            stale += 1
            continue
        assert case['record_sha256'] == record_sha256(record)
        question = record['question']
        authored = BeautifulSoup(question[':question/problem'], 'html.parser')
        expected = [[re.findall(r'\{\{(?:answer-field:)?([^{}]+)\}\}', cell.get_text()) for cell in row.find_all('td', recursive=False)]
                    for row in authored.select('.matrix-answer-brackets tr')]
        rendered_html = (directory/case['screenshot'].replace('.png', '.html')).read_text()
        # Glyph correctness is covered by the real-browser report. Removing SVG
        # payloads here keeps the independent field-coordinate audit bounded.
        rendered_html = re.sub(r'<mjx-container\b[\s\S]*?</mjx-container>', '<span class="verified-math"></span>', rendered_html)
        dom = BeautifulSoup(rendered_html, 'html.parser')
        prompt = dom.select_one('.lesson-content form > .prose') or dom.select_one('.lesson-content .content-card > .prose')
        assert prompt is not None, (qid, case['state'], directory)
        actual = [[[f['data-field-key'] for f in cell.select('.field-location')] for cell in row.find_all('td', recursive=False)]
                  for row in prompt.select('.matrix-answer-brackets tr')]
        assert expected == actual, (qid, case['state'], 'Wrong matrix field coordinates')
        identities = {f[':answer-field/key']: f[':answer-field/id'] for f in question.get(':question/answer-fields', [])}
        for control in prompt.select('.field-location'):
            key = control['data-field-key']
            wrapper = control.select_one('.answer-inline')
            assert wrapper['data-field-id'] == identities[key], (qid, key, 'Wrong field identity')
            if case['state'] == 'active':
                editor = wrapper.select_one('math-field')
                if editor:
                    assert not editor.get_text(strip=True) and editor.get('data-read-only') == 'false'
                trigger = wrapper.select_one('.answer-select-trigger')
                if trigger:
                    assert trigger.get('data-read-only') == 'false' and trigger.select_one('.answer-select-value').get_text(strip=True) == 'Select…'
        expected_keys = Counter(re.findall(r'\{\{(?:answer-field:)?([^{}]+)\}\}', question[':question/problem']))
        actual_keys = Counter(c['data-field-key'] for c in prompt.select('.field-location'))
        assert actual_keys == expected_keys, (qid, 'Missing or duplicated question controls')
        grids += len(prompt.select('.matrix-answer-brackets'))
        seen[qid].add((case['state'], case['viewport']['width']))
        verified.append({'entity': qid, 'state': case['state'], 'viewport': case['viewport'],
                         'screenshot': str(directory/case['screenshot'])})
required = {('active', 390), ('completed', 1280)}
missing = {qid: sorted(required - seen[qid]) for qid in final if not required <= seen[qid]}
assert not missing, ('Final questions missing required real-UI presentations', missing)
native = read('final-validation/native-after-report.json')
assert native['passed'] and native['documented_unresolved_checks'] == 0
assert set(native['checked_record_sha256']) == {record_sha256(r) for r in records if r['question'].get(':question/answer-fields')}
for path in ('preflight.json', 'detector-approx-regression.json'):
    assert read(path)['passed'], path
peer = read('cross-review.json')
assert peer['result'] == 'pass' and not peer['defects']
completion = read('completion-cross-review.json')
assert completion['status'] == 'mathematical and coordinate checks passed' and not completion['issues']
supplement = read('review-1/supplemental-cross-review.json')
assert supplement['fresh_capture_matches'] == 34 and supplement['marker_orphan_count'] == supplement['missing_correct_ref_count'] == 0
result = {'passed': True, 'final_questions': len(final), 'verified_ui_presentations': len(verified),
          'verified_bracketed_grids': grids, 'stale_presentations_excluded': stale,
          'all_required_mobile_active_and_desktop_completed_presentations': True,
          'field_coordinates_and_identities_preserved': True, 'active_controls_empty_and_enabled': True,
          'native_accepted_checks': native['accepted_checks'], 'native_rejected_checks': native['rejected_checks'],
          'native_unresolved_checks': 0, 'record_sha256': expected_hash,
          'plan_sha256': __import__('hashlib').sha256((H/'plan.json').read_bytes()).hexdigest()}
(H/'verification-precommit.json').write_text(json.dumps(result, indent=2)+'\n')
(H/'validated-presentations.json').write_text(json.dumps(verified, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'record_sha256'}, indent=2))
