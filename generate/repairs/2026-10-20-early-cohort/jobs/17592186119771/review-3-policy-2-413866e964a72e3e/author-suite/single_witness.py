#!/usr/bin/env python3
"""Strict source acceptance and independent visible support-domain regression."""
import importlib.util
import itertools
import json
import subprocess
import sys
import validate as v


def main():
    canonical = {'matrix': [[-2, 0, 0], [6, -1, 0], [0, 0, 0]],
                 'letter': 'A', 'layout': 'bmatrix'}
    cmd = [sys.executable, str(v.ROOT/'17592186119771.py'), '--difficulty', 'easy',
           '--count', '1', '--seed', '739', '--format', 'json',
           '--parameters', json.dumps(canonical)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    v.save('single-witness-acceptance.json', {'command': cmd, 'parameters': canonical,
           'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    assert result.returncode == 0, result.stderr
    records = json.loads(result.stdout)
    assert len(records) == 1
    assert v.matrix(records[0]['question'][':question/problem']) == canonical['matrix']
    assert v.verify(records[0]) == 'Lower triangular matrix'
    spec = importlib.util.spec_from_file_location('candidate', v.ROOT/'17592186119771.py')
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    coverage = []
    for level, n in [('easy', 2), ('easy', 3), ('moderate', 3), ('hard', 4)]:
        # Independent combinatorial domain, not implementation metadata or thresholds.
        wanted = set()
        for upper in (False, True):
            cells = [(i, j) for i in range(n) for j in range(n)
                     if (i < j if upper else i > j)]
            for bits in itertools.product((0, 1), repeat=len(cells)):
                if not any(bits): continue
                m = [[(-2 if i == 0 else 0) if i == j else 0 for j in range(n)]
                     for i in range(n)]
                for bit, (i, j) in zip(bits, cells): m[i][j] = 6*bit
                r = g.generate(level, seed=739, parameters={**canonical, 'matrix': m})
                assert v.matrix(r['question'][':question/problem']) == m
                assert v.verify(r) == ('Upper' if upper else 'Lower')+' triangular matrix'
                wanted.add(v.structural(m))
                if level == 'easy' and n == 3 and sum(bits) == 1:
                    records.append(r)
        diagonal = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
        wanted.add(v.structural(diagonal))
        # Exhaust the normal catalog via actual generation: sparse support must
        # be reachable without the explicit-parameter override as well.
        normal = g.batch(level, 18 if level == 'easy' else len(wanted), seed=41)
        observed = {v.structural(v.matrix(r['question'][':question/problem']))
                    for r in normal if len(v.matrix(r['question'][':question/problem'])) == n}
        assert observed == wanted, (level, n, wanted-observed, observed-wanted)
        for r in normal: v.verify(r)
        coverage.append({'difficulty': level, 'size': n, 'normal_supports': len(observed),
                         'sole_witness_coordinates': [[i+1,j+1] for i in range(n)
                                                      for j in range(n) if i != j]})
    # Fixed diagonal, changed sole witness, opposite side, and empty support.
    base = canonical['matrix']
    transpose = [list(row) for row in zip(*base)]
    clear = [[v if i == j else 0 for j,v in enumerate(row)] for i,row in enumerate(base)]
    controls = [g.generate('easy', seed=739, parameters={**canonical, 'matrix': m})
                for m in (base, transpose, clear)]
    assert [v.verify(r) for r in controls] == ['Lower triangular matrix',
          'Upper triangular matrix', 'Diagonal matrix']
    irrelevant = g.generate('easy', seed=739, parameters={**canonical, 'letter': 'C',
          'matrix': [[-v for v in row] for row in base]})
    assert v.verify(irrelevant) == v.verify(controls[0])
    records += controls[1:] + [irrelevant]
    v.save('single-witness-records.json', records)
    v.save('single-witness-coverage.json', {'finding': 'dbcd1ab741c06c08a3a5',
           'coverage': coverage, 'counterfactuals_verified': True,
           'canonical_normal_acceptance': True})
    print(json.dumps({'canonical': 'passed', 'coverage': coverage}))


if __name__ == '__main__': main()
