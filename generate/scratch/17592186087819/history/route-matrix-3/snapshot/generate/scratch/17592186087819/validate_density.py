"""Exercise sparse sampling without rendering hundreds of redundant PNGs."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('route_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def main():
    original_renderer = g.render_plots
    g.render_plots = lambda name, matrix: {'prompt': '/tmp/sampling-check.png', 'source_reuse': False}
    coverage = {}
    try:
        for template, level in g.TEMPLATES.items():
            totals, fingerprints, sums = [], set(), set()
            for seed in range(100):
                record = g.generate(level, seed=seed, template=template)
                generation = record['generation']
                matrix = generation['parameters']['matrix']
                size = len(matrix)
                total = sum(map(sum, matrix))
                assert 3 <= total <= (8 if size == 3 else 10), (template, seed, matrix)
                assert all(value <= 2 for row in matrix for value in row)
                assert all(matrix[i][i] <= 1 for i in range(size))
                assert generation['domain']['sampling_policy'] == 'sparse-routes-v3'
                assert generation['domain']['min_total_routes'] == 3
                values = [matrix[r][c] for r, c in generation['parameters']['holes']]
                fields = record['question'][':question/answer-fields']
                for index, field in enumerate(fields):
                    choices = field[':answer-field/choices']
                    key = field[':answer-field/correct'][1]
                    correct = [int(a[':answer/value']) for a in choices if a[':answer/id'] == key]
                    expected = values[index] if field[':answer-field/type'].endswith('/blank') else sum(values)
                    assert correct == [expected]
                    assert len({a[':answer/value'] for a in choices}) == len(choices)
                # Same seed reproduces both parameters and complete content identity.
                replay = g.generate(level, seed=seed, template=template)
                assert replay['question'] == record['question']
                totals.append(total)
                fingerprints.add(generation['mathematical_fingerprint'])
                sums.add(sum(values))
            assert len(fingerprints) >= 20, (template, len(fingerprints))
            assert len(sums) >= 3, (template, sums)
            coverage[template] = {'instances': 100, 'unique_graphs': len(fingerprints),
                                  'minimum_arrows': min(totals), 'maximum_arrows': max(totals),
                                  'distinct_correct_sums': sorted(sums)}

        base = {'holes': [[0, 1], [1, 1], [2, 0]], 'row_order': [0, 1, 2], 'col_order': [0, 1, 2]}
        invalid = {
            'nine arrows': [[1, 2, 0], [0, 1, 2], [2, 1, 0]],
            'three parallel routes': [[1, 1, 0], [0, 1, 3], [0, 1, 0]],
            'two self loops': [[2, 1, 0], [0, 1, 2], [0, 1, 0]],
        }
        for label, matrix in invalid.items():
            try:
                g.generate('moderate', template='sum_139689', parameters={**base, 'matrix': matrix})
            except ValueError:
                pass
            else:
                raise AssertionError('admitted ' + label)

        # Explicit inputs must respect the same floor as random sampling.
        blank = {'holes': [[0, 1], [1, 0], [1, 2]],
                 'row_order': [0, 1, 2], 'col_order': [0, 1, 2]}
        for total in range(3):
            matrix = [[0, 0, 0], [0, 0, 0], [total, 0, 0]]
            try:
                g.generate('easy', template='blanks_319346', parameters={**blank, 'matrix': matrix})
            except ValueError as error:
                assert 'at least three arrows' in str(error)
            else:
                raise AssertionError(f'admitted a {total}-arrow graph')
        minimum = g.generate('easy', template='blanks_319346',
                             parameters={**blank, 'matrix': [[1, 0, 0], [0, 0, 0], [2, 0, 0]]})
        assert sum(map(sum, minimum['generation']['parameters']['matrix'])) == 3

        # Source replay keeps the dense captured graph; it must not silently
        # remove routes to satisfy a sampling constraint.
        source = next(case for case in json.loads((HERE / 'source-cases.json').read_text())
                      if case['source_id'] == 'q-319429')
        replay = g.generate(source['level'], template=source['template'],
                            parameters=source['parameters'], profile=source['bank_profile'])
        assert replay['generation']['parameters'] == source['parameters']
        assert replay['generation']['domain']['sampling_policy'] == 'exact-source-replay'
    finally:
        g.render_plots = original_renderer

    report = {'passed': True, 'version': g.VERSION, 'generated_instances': 800,
              'deterministic_replays': 800, 'density_guards_rejected': list(invalid),
              'floor_rejected_totals': [0, 1, 2], 'three_arrow_boundary_accepted': True,
              'dense_source_replay_preserved': True, 'coverage': coverage}
    (HERE / 'density-validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
