"""Read-only structural audit of the materialized registered generator."""
import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path

home = Path(__file__).resolve().parent
sys.path.insert(0, str(home / 'generator'))
spec = importlib.util.spec_from_file_location('audited_generator', home / 'generator/generator.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

report = {'version': generator.VERSION, 'seeds_per_level': 10000, 'levels': {}}
for level in generator.LEVELS:
    counts = Counter()
    examples = {}
    for seed in range(report['seeds_per_level']):
        rng = random.Random(seed)
        requested = rng.choice(generator.VALUES)
        p = generator.sample(level, rng, requested)
        assert generator.result(p) == requested
        first = tuple(p[k] for k in 'abc')
        second = tuple(p[k] for k in 'def')
        shape = 'identical' if first == second else 'negated' if first == tuple(-v for v in second) else 'other'
        counts[requested] += 1
        counts[shape] += 1
        key = requested + '/' + shape
        examples.setdefault(key, {'seed': seed, 'parameters': p})
        # Confirm the sampler agrees with the public generation API.
        if seed < 10:
            generated = generator.generate(level, seed)
            assert generated['generation']['parameters'] == p
            assert generated['generation']['inferred_correct_value'] == requested
    report['levels'][level] = {'counts': dict(counts), 'examples': examples}

exact = generator.generate('easy', parameters=dict(zip('abcdef', (2, -1, 4, 2, -1, 4))))
report['same_display_reproduction'] = exact
(home / 'structural-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({level: data['counts'] for level, data in report['levels'].items()}, indent=2))
