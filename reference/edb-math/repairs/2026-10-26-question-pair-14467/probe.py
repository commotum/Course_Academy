"""Read-only reproduction of the reported parallel-line question repetition."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

D = Path(__file__).resolve().parent
PACKAGE = Path('/media/jake/SSD/EDB/math/generators/3e/3e5be0963253ecbaff9964bd7bbb72fade1cef7a5a1fe5d8f2f5716a3b59ee0a')
sys.path.insert(0, str(PACKAGE))
spec = importlib.util.spec_from_file_location('parallel_generator', PACKAGE / 'generator.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def bank(record):
    field = record['question'][':question/answer-fields'][0]
    return tuple(sorted(a[':answer/value'] for a in field[':answer-field/choices']))


def correct(record):
    field = record['question'][':question/answer-fields'][0]
    answer_id = field[':answer-field/correct'][1]
    return next(a[':answer/value'] for a in field[':answer-field/choices']
                if a[':answer/id'] == answer_id)


rows = generator.batch('hard', 4, 1811058558)
saved = json.loads((D / 'initial.json').read_text())['questions']
matches = []
for (question,) in saved:
    field = question[':question/answer-fields'][0]
    candidates = [r for r in rows if r['question'][':question/problem'] == question[':question/problem']]
    assert len(candidates) == 1
    r = candidates[0]
    assert bank(r) == tuple(sorted(a[':answer/value'] for a in field[':answer-field/choices']))
    assert correct(r) == field[':answer-field/correct'][':answer/value']
    matches.append({'entity': question[':db/id'], 'sample_index': rows.index(r),
                    'problem': question[':question/problem'], 'correct': correct(r)})

observations = {}
for band in generator.LEVELS:
    metrics = Counter()
    for seed in range(100):
        sample = generator.batch(band, 5, seed)
        banks = [bank(r) for r in sample]
        work = [(r['generation']['given']['slope'], bank(r)) for r in sample]
        metrics['batches'] += 1
        metrics['repeated_bank_batches'] += len(set(banks)) < len(banks)
        metrics['repeated_slope_and_bank_batches'] += len(set(work)) < len(work)
        metrics['distinct_banks_total'] += len(set(banks))
    observations[band] = dict(metrics)

result = {'package': str(PACKAGE / 'generator.py'), 'seed': 1811058558,
          'exact_reported_questions_reproduced': matches,
          'reported_batch': [{'problem': r['question'][':question/problem'],
                              'slope': r['generation']['given']['slope'],
                              'correct': correct(r)} for r in rows],
          'reported_batch_distinct_banks': len({bank(r) for r in rows}),
          'five_question_batch_probe': observations}
(D / 'probe.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
