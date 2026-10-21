"""Regression for the manifest difficulty repair; no database or publication writes."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
from fractions import Fraction

from verify_record import g, check
from probe_banks import probes

W = Path(__file__).resolve().parents[1]
E = W / 'evidence'
OUT = E / 'classification-repair'
OUT.mkdir(exist_ok=True)
ASSETS = E / 'assets'
REPO = Path('/home/jake/Developer/Course_Academy')
SOURCE = REPO / 'generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source'
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'] = str(ASSETS)

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + '\n')

def geometry(record):
    field = record['question'][':question/answer-fields'][0]
    answer = next(a for a in field[':answer-field/choices']
                  if a[':answer/id'] == field[':answer-field/correct'][1])
    return record['generation']['choice_geometry'][answer[':answer/value']]

manifest = json.loads((W / 'package.json').read_text())
assert manifest['default_difficulty'] == 'easy'
assert manifest['dependencies'] == {
    'python': sys.version.split()[0],
    'packages': {name: importlib.metadata.version(name) for name in ('sympy', 'matplotlib')},
}
old_hashes = json.loads((E / 'validation.json').read_text())['runtime_hashes']
hashes = {name: hashlib.sha256((W / name).read_bytes()).hexdigest()
          for name in manifest['files']}
assert hashes == old_hashes, 'This repair must preserve completed runtime fixes'
source = json.loads((SOURCE / 'source.json').read_text())
questions = source['material']['kp'][':knowledge-point/questions']
labels = {q[':question/math-academy-id']: q.get(':question/difficulty', {}).get(':db/ident')
          for q in questions}
assert sum(label == ':question.difficulty/easy' for label in labels.values()) == 5
assert sum(label is None for label in labels.values()) == 2

replays = []
previous_replays = json.loads((E / 'source-replays.json').read_text())
for old in previous_replays:
    meta = old['generation']
    record = g.generate('easy', meta['seed'], profile=meta['bank_profile'],
                        parameters=meta['parameters'])
    check(record)
    assert record == old
    replays.append(record)
save('source-replays.json', replays)

command = [sys.executable, str(W / manifest['entrypoint']), '--difficulty',
           manifest['default_difficulty'], '--count', '5', '--seed', '71', '--format', 'json']
run = subprocess.run(command, cwd=W, text=True, capture_output=True, check=True)
batch = json.loads(run.stdout)
assert len(batch) == 5
assert batch == json.loads((E / 'relocated-a-records.json').read_text())
for record in batch:
    check(record)
    assert record['question'][':question/difficulty'] == ':question.difficulty/easy'
save('batch.json', batch)

# Re-exercise the preserved, controlled sign/point/presentation cases in each form.
previous = {r['question'][':question/id']: r for r in json.loads((E / 'generated.json').read_text())}
controls = []
counterfactuals = json.loads((E / 'counterfactuals.json').read_text())
for case in counterfactuals:
    triple = []
    for role in ('base_id', 'negated_equation_id', 'changed_point_id'):
        old = previous[case[role]]
        meta = old['generation']
        record = g.generate('easy', meta['seed'], template=meta['template'], parameters=meta['parameters'])
        check(record)
        assert record == old
        triple.append(record)
        controls.append(record)
    base, negated, moved = triple
    assert geometry(negated) == [str(-Fraction(v)) for v in geometry(base)]
    assert geometry(negated) != geometry(base)
    index = case['changed_index']
    assert geometry(moved)[index] != geometry(base)[index]
    assert all(geometry(moved)[i] == geometry(base)[i] for i in range(3) if i != index)
    meta = base['generation']
    presentation = g.generate('easy', 980 + g.TEMPLATES.index(meta['template']),
                              template=meta['template'], parameters=meta['parameters'])
    check(presentation)
    assert presentation['question'][':question/id'] == base['question'][':question/id']
    assert geometry(presentation) == geometry(base)
    controls.append(presentation)
records = batch + controls
save('counterfactual-records.json', controls)
save('delivery-input.json', records)
delivery_command = [sys.executable, str(REPO / 'generate/pipeline/check_delivery.py'),
                    '--input', str(OUT / 'delivery-input.json'), '--source', str(SOURCE / 'source.json'),
                    '--inventory', str(SOURCE / 'inventory.json'), '--difficulty', manifest['default_difficulty'],
                    '--output', str(OUT / 'delivery'), '--asset-root', str(ASSETS),
                    '--math-root', '/media/jake/SSD/EDB/math']
subprocess.run(delivery_command, check=True, capture_output=True, text=True)
accepted = json.loads((OUT / 'delivery/accepted.json').read_text())
assert {r['generation']['mathematical_fingerprint'] for r in records} == {
    r['generation']['mathematical_fingerprint'] for r in accepted}
assert len({r['generation']['template'] for r in accepted}) == 6
# Recover geometry under normalized image paths to run the same cue probes.
by_hash = {hashlib.sha256((ASSETS / name).read_bytes()).hexdigest(): slopes
           for r in records for name, slopes in r['generation']['choice_geometry'].items()}
for record in accepted:
    for answer in record['question'][':question/answer-fields'][0][':answer-field/choices']:
        name = answer[':answer/value']
        record['generation']['choice_geometry'][name] = by_hash[Path(name).stem]
save('shortcut-probes.json', {
    'before_delivery': probes(records), 'after_delivery': probes(accepted),
    'preserved_larger_sample': '../bank-probes-before.json',
    'limits': 'Small regression controls are not a random frequency sample; prior 40-per-form normal banks remain authoritative for frequency probes. Captured inventory filtering is exercised, not live learner history or weighted selection.',
})
cases = []
for i, record in enumerate(replays + records + accepted):
    field = record['question'][':question/answer-fields'][0]
    cases.append({'label': f'classification regression {i}', 'record': record, 'checks': [
        {'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if a[':answer/id'] == field[':answer-field/correct'][1] else 'rejected',
         'purpose': 'Complete bank, including counterfactual keys and delivered normalization'}
        for a in field[':answer-field/choices']]})
save('engine-input.json', cases)
grader_command = [str(REPO / 'generate/runs/current/check-engine'),
                  str(OUT / 'engine-input.json'), str(OUT / 'engine-report.json')]
subprocess.run(grader_command, check=True, capture_output=True, text=True)
save('render-records.json', batch[:2])
save('result.json', {
    'passed': True, 'default_difficulty': manifest['default_difficulty'],
    'source_difficulties_unchanged': labels, 'runtime_files_unchanged': hashes,
    'source_banks_replayed': len(replays), 'source_options': len(replays) * 5,
    'manifest_driven_cli_batch': len(batch), 'identical_to_prior_relocated_batch': True,
    'counterfactual_forms': len(counterfactuals), 'records_before_delivery': len(records),
    'records_after_delivery': len(accepted), 'semantic_instances_preserved': True,
    'native_checks': len(cases) * 5,
    'commands': [command, delivery_command, grader_command],
})
print(json.dumps({'passed': True, 'source_banks': len(replays), 'cli_records': len(batch),
                  'delivered': len(accepted), 'native_checks': len(cases) * 5}))
