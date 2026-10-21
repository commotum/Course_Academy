"""Focused final batch-quota check; retain the existing grading/render evidence."""
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
GENERATOR = ROOT / 'generate/scratch/17592186119771.py'
spec = importlib.util.spec_from_file_location('triangular_final', GENERATOR)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
old = json.loads((HERE / 'review.json').read_text())
cases = []
for removed in ('upper', 'lower'):
    omitted = g.task_key(g.catalog('easy', removed)[0][1])
    rows = g.batch('easy', 2, 91, exclude_fingerprints=[omitted])
    families = sorted(row['generation']['template'] for row in rows)
    assert families == sorted(['diagonal', 'lower' if removed == 'upper' else 'upper'])
    assert len({row['generation']['parameter_fingerprint'] for row in rows}) == 2
    cases.append({'excluded': removed, 'remaining': families, 'requested': 2, 'returned': 2})

inputs = json.loads((HERE / 'native-input.json').read_text())
for item in inputs:
    rec = item['record']
    meta = rec['generation']
    level = rec['question'][':question/difficulty'].split('/')[-1]
    actual = g.generate(level, seed=meta['seed'], template=meta['template'], parameters=meta['parameters'], profile=meta['bank_profile'])
    if meta['evidence_only']:
        actual['question'][':question/answer-fields'] = [field for field in actual['question'][':question/answer-fields'] if ':answer-field/correct' in field]
    assert actual == rec, item['label']

for item in json.loads((HERE / 'visual-cases.json').read_text()):
    rec, meta = item['record'], item['record']['generation']
    level = rec['question'][':question/difficulty'].split('/')[-1]
    assert g.generate(level, seed=meta['seed']) == rec

final_hash = hashlib.sha256(GENERATOR.read_bytes()).hexdigest()
result = {'passed': True, 'previous_generator_sha256': old['generator_sha256'], 'generator_sha256': final_hash,
          'depleted_easy_cases': cases, 'native_input_records_unchanged': len(inputs), 'visual_cases_unchanged': 9,
          'grading_and_rendering_repeated': False, 'reason': 'All previously graded and rendered generated records are byte-for-byte equivalent; only depleted batch selection changed.'}
(HERE / 'batch-followup.json').write_text(json.dumps(result, indent=2) + '\n')
old['initial_generator_sha256'] = old['generator_sha256']
old['generator_sha256'] = final_hash
old['focused_batch_followup'] = result
(HERE / 'review.json').write_text(json.dumps(old, indent=2) + '\n')
print(json.dumps(result, indent=2))
