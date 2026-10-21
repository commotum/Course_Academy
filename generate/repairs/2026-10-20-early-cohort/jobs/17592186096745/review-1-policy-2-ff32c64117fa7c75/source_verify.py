"""External source comparison; no generator math or source-registry helpers."""
import json, re
from pathlib import Path
from review_math import matrices, prompt, semantic, correct_index

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT.parent / 'source/source.json').read_text())
questions = source['material']['kp'][':knowledge-point/questions']
replays = json.loads((ROOT / 'replays.json').read_text())
by_source = {r['generation']['source_question']: r for r in replays}

def prose(text):
    return ' '.join(re.sub(r'\$\$.*?\$\$|\$[^$]*\$', '', text, flags=re.S).split())

results = []
for q in questions:
    r = by_source[q[':question/id']]
    replay = r['question']
    field = q[':question/answer-fields'][0]
    actual = replay[':question/answer-fields'][0]
    before = matrices(q[':question/worked-solution'])
    after = matrices(replay[':question/worked-solution'])
    checks = {
        'equations': prompt(q) == prompt(replay),
        'prompt_prose': prose(q[':question/problem']) == prose(replay[':question/problem']),
        'worked_prose': prose(q[':question/worked-solution']) == prose(replay[':question/worked-solution']),
        'all_displayed_matrices': before == after,
        'complete_ordered_bank': [(a[':answer/type'][':db/ident'], semantic(a[':answer/value'])) for a in field[':answer-field/choices']] == [(a[':answer/type'], semantic(a[':answer/value'])) for a in actual[':answer-field/choices']],
        'response_contract': actual[':answer-field/type'] == field[':answer-field/type'][':db/ident'] and actual[':answer-field/key'] == field[':answer-field/key'],
        'key': correct_index(q) == correct_index(replay),
    }
    results.append({'source_id': q[':question/id'], 'profile': q[':question/math-academy-id'], 'checks': checks, 'passed': all(checks.values())})
report = {'command': 'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python source_verify.py', 'cases': results, 'passed': all(x['passed'] for x in results), 'corrections': ['q-74627 source wrong R3 scaling label changed to R2; q-74629 scalable parentheses are presentation-only.'], 'canonical': 'Canonical example has no answer bank; used for independent skill and scope analysis.'}
(ROOT / 'source-verification.json').write_text(json.dumps(report, indent=2))
print(json.dumps({'passed': report['passed'], 'cases': len(results), 'failures': [x for x in results if not x['passed']]}))
assert report['passed']
