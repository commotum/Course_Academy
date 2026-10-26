"""Regress the reported repetition and retain the generator's full domain."""
import argparse
from collections import Counter
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL = Path('/media/jake/SSD/EDB/math/generators/ed/ed98cdd6897b7ea35c995dc4d981670def9a74663801350064405a7d61d96d9c/generator.py')
BANDS = ('easy', 'moderate', 'hard')
SEEDS = (0, 1, 2, 3, 5, 7, 11, 17, 28, 43, 71, 97, 2275668537)


def load(path, name):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.path.pop(0)
    return module


def parameters(records):
    return [(r['generation']['parameters']['m'],
             Fraction(r['generation']['parameters']['c'])) for r in records]


def catalog(band):
    pairs = set()
    for m in range(3, 16, 2):
        for n in range(-9 if band == 'easy' else -17, 10 if band == 'easy' else 18):
            pairs.add((m, Fraction(m*m+n, 4)))
        pairs.update((m, Fraction(c)) for c in [*range(-3, 13), 25, 30, Fraction(5, 4)])
    return pairs


def check(path):
    original, current = load(ORIGINAL, 'original_square'), load(path, 'repaired_square')
    seed = 2275668537
    old = parameters(original.generate('moderate', 4, seed))
    new = parameters(current.generate('moderate', 4, seed))
    assert [m for m, c in old] == [7, 3, 7, 7], old
    assert len({m for m, c in new}) == 4, new

    batches = 0
    for band in BANDS:
        for seed in SEEDS:
            for count in (5, 7):
                records = current.generate(band, count, seed)
                assert len(records) == count
                assert len({m for m, c in parameters(records)}) == count, (band, seed, count)
                assert {r['generation']['remainder_case'] for r in records[:3]} == {'negative', 'zero', 'positive'}
                assert records == current.generate(band, count, seed), (band, seed, 'replay')
                batches += 1
        assert current.generate(band, 0, 0) == []

    domains = {}
    for band in BANDS:
        domain = catalog(band)
        records = current.generate(band, len(domain), 28)
        actual = parameters(records)
        assert len(actual) == len(set(actual)) == len(domain)
        assert set(actual) == domain, band
        assert set(parameters(original.generate(band, len(domain), 28))) == domain, band
        # For ordinary outcome-based choices, the least-used coefficient with
        # that outcome must win. The easy zero-original preference is explicit.
        remaining, used, eligible_checks = set(domain), Counter(), 0
        for m, c in actual:
            sign = (c > Fraction(m*m, 4)) - (c < Fraction(m*m, 4))
            eligible = {n for n, value in remaining
                        if (value > Fraction(n*n, 4)) - (value < Fraction(n*n, 4)) == sign}
            if not (band == 'easy' and c == 0):
                assert used[m] == min(used[n] for n in eligible), (band, m, c, dict(used))
                eligible_checks += 1
            remaining.remove((m, c))
            used[m] += 1
        assert not remaining
        try:
            current.generate(band, len(domain)+1, 28)
        except ValueError as error:
            assert 'semantic instances' in str(error)
        else:
            raise AssertionError('Finite domain overflow was not rejected')
        domains[band] = {'instances': len(domain), 'least_used_checks': eligible_checks,
                        'coefficient_counts': dict(sorted(used.items()))}

    fixed_cases = [(7, Fraction(65, 4), 'y'), (7, Fraction(61, 4), 'y'),
                   (3, 0, 'x'), (11, Fraction(121, 4), 't'),
                   (15, -3, 'z'), (9, 30, 'x'), (5, 25, 'y'), (13, Fraction(5, 4), 't')]
    for band in BANDS:
        for m, c, v in fixed_cases:
            assert current.construct(m, c, v, band) == original.construct(m, c, v, band)
    assert current.replay_sources() == original.replay_sources()

    return {'passed': True, 'reported_seed': 2275668537,
            'original_coefficients': [m for m, c in old],
            'repaired_coefficients': [m for m, c in new],
            'distinct_coefficient_batches': batches, 'batch_sizes': [5, 7],
            'catalogs': domains, 'unchanged_fixed_records': len(fixed_cases)*len(BANDS),
            'source_replay_unchanged': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generator', type=Path, default=HERE/'workspace/generator.py')
    parser.add_argument('--output', type=Path, default=HERE/'sampler-regression.json')
    args = parser.parse_args()
    result = check(args.generator.resolve())
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
