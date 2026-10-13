"""Correct the stopped quiz's parsed XP using its preserved explicit award."""
from pathlib import Path
import hashlib
import json

from scripts.browser.parsing import parse_xp
from scripts.storage import atomic_json, read_json

root = Path(__file__).resolve().parent
capture = root.parents[3] / 'reference/mathacademy/capture/linear/14123325'
assert read_json(Path('.local/capture/linear/active.json')) is None
assert (capture / 'handoff-complete.json').exists()
assert not (capture / 'database/request.json').exists()
assert read_json(capture / 'database/result.json')['status'] == 'verified'
post = read_json(capture / 'post-activity.json')
assert (post['completion']['earned_xp'], post['completion']['base_xp']) == (15, 15)
originals = root / 'original-xp-parses'
originals.mkdir(exist_ok=True)
changed = []
hashes = {}


def correct(completion):
    if not isinstance(completion, dict):
        return False
    text = completion.get('source_text') or completion.get('text')
    if not text:
        return False
    parsed = parse_xp(text)
    assert (parsed['earned_xp'], parsed['base_xp']) == (15, 15)
    if all(completion.get(key) == parsed[key] for key in ('earned_xp', 'base_xp')):
        return False
    completion.update({key: parsed[key] for key in ('earned_xp', 'base_xp')})
    return True


for name in ('content.json', 'checkpoint.json', 'browser-state.json'):
    path = capture / name
    data = read_json(path)
    if data is None:
        continue
    completion = data.get('completion') or {}
    nested = completion.get('completion') if isinstance(completion, dict) else None
    updated = correct(nested if nested is not None else completion)
    if name == 'content.json' and data.get('base_xp') == 9:
        data['base_xp'] = 15
        updated = True
    if updated:
        source = path.read_bytes()
        archive = originals / name
        assert not archive.exists(), 'Retain existing repair originals without overwriting'
        archive.write_bytes(source)
        hashes[name] = hashlib.sha256(source).hexdigest()
        atomic_json(path, data)
        changed.append(name)

result_path = root / 'result.json'
result = read_json(result_path)
if result:
    (originals / 'operator-result.json').write_bytes(result_path.read_bytes())
    result['completion'] = post['completion']
    result['initial_completion_parse_repaired'] = True
    atomic_json(result_path, result)
atomic_json(root / 'xp-source-repair.json', {
    'task_id': '14123325', 'changed_current_records': changed,
    'original_parsed_record_sha256': hashes,
    'source_completion_text': post['completion']['text'],
    'dashboard_completion_source_text': post['completion']['source_text'],
    'earned_xp': 15, 'base_xp': 15,
    'grade_and_question_counts_unchanged': True,
    'original_html_and_observation_files_unchanged': True,
    'post_activity_and_account_ledgers_already_correct': True})
print(json.dumps({'changed': changed, 'earned_xp': 15, 'base_xp': 15}))
