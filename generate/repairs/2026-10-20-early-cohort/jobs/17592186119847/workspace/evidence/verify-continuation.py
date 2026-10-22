"""Verify the resumed job's existing package and newly filtered control records.

Prerequisites and exact delivery commands are recorded in commands.md.
No runtime package files, services, or database content are modified.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from check_repair import inspect, g

E = ROOT / 'evidence'
manifest = json.loads((ROOT / 'package.json').read_text())
hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
          for name in manifest['files']}
controls = {}
cases = []
for level in ('easy', 'moderate'):
    before = json.loads((E / f'continuation-controls-{level}.json').read_text())
    after = json.loads((E / f'continuation-delivery-{level}/accepted.json').read_text())
    assert len(before) == len(after)
    index = {r['question'][':question/problem']: r for r in after}
    facts = []
    for original in before:
        meta = original['generation']
        fresh = g.generate(level, meta['seed'], parameters=meta['parameters'],
                           bank_profile=meta['bank_profile'])
        assert fresh == original, 'Control no longer matches current generator'
        delivered = index[original['question'][':question/problem']]
        fact = inspect(delivered)
        assert fact == inspect(original)
        assert delivered['question'][':question/worked-solution'] == original['question'][':question/worked-solution']
        facts.append(fact)
        field = delivered['question'][':question/answer-fields'][0]
        cases.append({'label': 'continuation-' + delivered['question'][':question/id'],
                      'record': delivered, 'checks': [
            {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if int(a[':answer/value']) == fact['rank'] else 'rejected',
             'purpose': 'Visible count oracle after actual delivery normalization'}
            for a in field[':answer-field/choices']]})
    assert facts[0]['rank'] != facts[1]['rank']
    assert facts[0]['rank'] == facts[2]['rank']
    if level == 'moderate':
        assert facts[0]['rank'] != facts[3]['rank']
    controls[level] = facts

# The requested runner batch must still be exactly five distinct mathematical tasks.
sample = json.loads((E / 'sample-output.json').read_text())['records']
accepted = json.loads((E / 'delivery-requested-five/accepted.json').read_text())
assert len(sample) == len(accepted) == 5
assert len({inspect(r)['semantic'] for r in accepted}) == 5
for record in accepted:
    fact = inspect(record)
    field = record['question'][':question/answer-fields'][0]
    cases.append({'label': 'requested-five-' + record['question'][':question/id'],
                  'record': record, 'checks': [
        {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if int(a[':answer/value']) == fact['rank'] else 'rejected',
         'purpose': 'All choices of exact requested five after delivery'}
        for a in field[':answer-field/choices']]})

(E / 'continuation-grader-input.json').write_text(json.dumps(cases, indent=2) + '\n')
grader = Path('/home/jake/Developer/Course_Academy/generate/runs/current/check-engine')
command = [str(grader), str(E / 'continuation-grader-input.json'),
           str(E / 'continuation-grader-report.json')]
native = subprocess.run(command, capture_output=True, text=True)
assert native.returncode == 0, native.stdout + native.stderr
report = {'status': 'pass', 'runtime_sha256': hashes,
          'requested_count': 5, 'delivered_count': 5,
          'controlled_changes_after_delivery': controls,
          'native_command': command, 'native_result': native.stdout.strip(),
          'runtime_changes_this_continuation': 'CLI JSON envelope changed from instances to records; mathematical records unchanged.',
          'rendering': 'Four current easy/moderate records rerendered and visually inspected; see render/rendering.json.',
          'limitations': ['Finite semantic capacities remain 12 easy and 91 moderate; oversized requests fail explicitly.',
                          'No live learner history or publication was exercised.']}
(E / 'continuation-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': 'pass', 'delivered': 5, 'controlled_records': 7,
                  'native': native.stdout.strip()}))
