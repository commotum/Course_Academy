"""Check the reported repetition, batch diversity, and unchanged construction."""
import ast
from collections import Counter
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import random
import re
import sys

D = Path(__file__).resolve().parent
OLD = Path('/media/jake/SSD/EDB/math/generators/3e/3e5be0963253ecbaff9964bd7bbb72fade1cef7a5a1fe5d8f2f5716a3b59ee0a')
NEW = D / 'workspace'
sys.path.insert(0, str(NEW))


def load(name, directory):
    spec = importlib.util.spec_from_file_location(name, directory / 'generator.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old, new = load('old_parallel', OLD), load('new_parallel', NEW)


def equation(text):
    """Independently recover a visible line's slope and intercept."""
    text = text.replace(' ', '')
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'\1/\2', text)
    if text.startswith('y='):
        match = re.fullmatch(r'y=([+-]?(?:\d+(?:/\d+)?)?)x([+-]\d+(?:/\d+)?)?', text)
        assert match, text
        slope = match[1]
        return Fraction(slope + '1' if slope in ('', '+', '-') else slope), Fraction(match[2] or '0')
    match = re.fullmatch(r'([+-]?\d*)x([+-]\d*)y=([+-]?\d+)', text)
    assert match, text
    a, b = (Fraction(v + '1' if v in ('', '+', '-') else v) for v in match.group(1, 2))
    c = Fraction(match[3])
    return -a / b, c / b


def inspect(record):
    question = record['question']
    given = equation(re.search(r'\$(.*?)\$', question[':question/problem'])[1])
    field = question[':question/answer-fields'][0]
    choices = field[':answer-field/choices']
    normalized = [equation(choice[':answer/value']) for choice in choices]
    correct = [i for i, (m, b) in enumerate(normalized) if m == given[0] and b != given[1]]
    assert len(correct) == 1
    assert choices[correct[0]][':answer/id'] == field[':answer-field/correct'][1]
    return given[0], tuple(sorted(normalized)), correct[0]


# The old case must demonstrate the defect that the new sampler repairs.
original = old.batch('hard', 4, 1811058558)
repaired = new.batch('hard', 4, 1811058558)
assert len({inspect(r)[0] for r in original}) == 2
assert len({inspect(r)[1] for r in original}) == 1
assert len({inspect(r)[0] for r in repaired}) == 4
assert len({inspect(r)[1] for r in repaired}) == 4

seeds = (0, 1, 41, 2616988511, 1811058558)
observations = {}
checked_records = 0
for band in new.LEVELS:
    pool = new.INTEGER_SLOPES if band == 'easy' else new.INTEGER_SLOPES + new.FRACTION_SLOPES
    slots = set()
    batches = []
    for seed in seeds:
        for count in (4, 5, 12, 22, 23):
            records = new.batch(band, count, seed)
            assert records == new.batch(band, count, seed)
            assert len(records) == count
            assert len({r['question'][':question/id'] for r in records}) == count
            facts = [inspect(r) for r in records]
            slopes = [row[0] for row in facts]
            assert len(set(slopes[:len(pool)])) == min(count, len(pool))
            assert len({row[1] for row in facts}) == count
            uses = Counter(slopes)
            assert max(uses[m] for m in pool) - min(uses[m] for m in pool) <= 1
            slots.update(row[2] for row in facts)
            batches.append({'seed': seed, 'count': count, 'distinct_slopes': len(uses),
                            'distinct_banks': count})
            checked_records += count
    # Changing the sampling policy must not make one stored answer position fixed.
    assert slots == set(range(5))
    observations[band] = {'batches': batches, 'observed_target_slots': sorted(slots)}

# All mathematical construction and replay code must be unchanged by this repair.
def unchanged_nodes(directory):
    tree = ast.parse((directory / 'generator.py').read_text())
    return [ast.dump(node, include_attributes=False) for node in tree.body
            if not isinstance(node, ast.FunctionDef) or node.name != 'batch']


assert unchanged_nodes(OLD) == unchanged_nodes(NEW)
fixed_records = 0
for band in new.LEVELS:
    for seed in (0, 17, 1811058558):
        old_rng, new_rng = random.Random(seed), random.Random(seed)
        old_bank, new_bank = old.make_bank(band, old_rng), new.make_bank(band, new_rng)
        assert old_bank == new_bank
        targets = [i for i, c in enumerate(old_bank)
                   if band != 'hard' or sum(d['m'] == c['m'] for d in old_bank) == 2]
        for target in targets:
            assert old.target_record(band, old_bank, target, old_rng, seed) == new.target_record(band, new_bank, target, new_rng, seed)
            fixed_records += 1
source_cases = json.loads((OLD / 'source-cases.json').read_text())
for name in source_cases:
    assert old.replay(name) == new.replay(name)
for name in ('math_format.py', 'source-cases.json'):
    assert (OLD / name).read_bytes() == (NEW / name).read_bytes()

summary = {'passed': True, 'short_and_long_batch_checks': sum(len(v['batches']) for v in observations.values()),
           'independently_checked_records': checked_records,
           'fixed_construct_records_unchanged': fixed_records,
           'source_replays_unchanged': len(source_cases), 'only_batch_function_changed': True,
           'reported_seed': 1811058558,
           'original_four_record_batch': {'distinct_banks': 1, 'distinct_slopes': 2},
           'repaired_four_record_batch': {'distinct_banks': 4, 'distinct_slopes': 4,
               'slopes': [str(inspect(r)[0]) for r in repaired]},
           'bands': observations,
           'limitations': ['Slope balancing and bank uniqueness apply within each generator call; no cross-call learner-history spacing is imposed.']}
(D / 'sampler-regression.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'bands'}, indent=2))
