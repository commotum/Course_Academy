"""Independently check evaluated limits for every hard-domain sample.

Run validate.py first to rebuild samples.json, then run this script. A point
specialization must avoid distractors that accidentally have the correct limit.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('point_limit_validation', D / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
records = [r for r in json.loads((D / 'samples.json').read_text())
           if r['question'][':question/difficulty'].endswith('/hard')]
cache = {}
checked = set()
for record in records:
    question = record['question']
    field = question[':question/answer-fields'][0]
    correct = field[':answer-field/correct'][1]
    values = {}
    for answer in field[':answer-field/choices']:
        text = answer[':answer/value']
        if text not in cache:
            cache[text] = v.S.limit(v.tm.quotient(text), v.tm.SYMBOLS['h'], 0)
        values[answer[':answer/id']] = cache[text]
    assert all(v.S.simplify(value - values[correct]) != 0
               for key, value in values.items() if key != correct), record['generation']['parameters']
    checked.add(question[':question/id'])
report = {
    'passed': True,
    'hard_records': len(records),
    'distinct_records': len(checked),
    'unique_displayed_limits_evaluated': len(cache),
    'method': 'Parse every rendered choice and independently evaluate its h->0 limit; each distractor differs from the finite correct derivative.',
    'generator_sha256': hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),
}
(D / 'reference/replenishment/hard-domain-limit-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
