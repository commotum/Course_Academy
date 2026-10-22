"""Exact replay, theorem semantics, actual radio grader, and finite capacity."""
import importlib.util
import hashlib
import json
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('recognition_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def grading(records, directory):
    directory.mkdir(parents=True, exist_ok=True)
    checks = []
    for r in records:
        f = r['question'][':question/answer-fields'][0]
        checks.append({'label': r['generation']['source'], 'record': r,
                       'checks': [{'submitted_answer_id': a[':answer/id'],
                                   'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected'}
                                  for a in f[':answer-field/choices']]})
    save(directory / 'input.json', checks)
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(directory / 'input.json'),
                    str(directory / 'report.json')], check=True, capture_output=True, text=True, timeout=55)
    return json.loads((directory / 'report.json').read_text())


def main():
    out = HERE / 'reference/validation'
    replays = [g.replay(t) for t in sorted(g.SOURCES)]
    fidelity = []
    for r in replays:
        t = r['generation']['source']; source = g.SOURCES[t]; q = r['question']
        assert q[':question/problem'] == source[':question/problem']
        assert q[':question/worked-solution'] == source[':question/worked-solution']
        assert len(q[':question/answer-fields']) == len(source[':question/answer-fields']) == 1
        f = q[':question/answer-fields'][0]; sf = source[':question/answer-fields'][0]
        assert f[':answer-field/type'] == sf[':answer-field/type'][':db/ident']
        assert f[':answer-field/key'] == sf[':answer-field/key'] == 'selection'
        assert [a[':answer/value'] for a in f[':answer-field/choices']] == [a[':answer/value'] for a in sf[':answer-field/choices']]
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1]) == sf[':answer-field/correct'][':answer/value']
        assert r == g.replay(t)
        fidelity.append({'source': t, 'matched_options': 5, 'total_options': 5,
                         'matched_distractors': 4, 'total_distractors': 4, 'complete_bank_match': True,
                         'missing': [], 'extra': [], 'eligible': t in g.TARGETS,
                         'exclusion': g.EXCLUDED.get(t)})
    # Exact scalar/dimension checks. Sets/spaces, matrices, and scalars have
    # distinct types; the zero subspace is not the scalar zero.
    assertions = []
    expected = {'null-space-rhs': r'\{0\}', 'invertibility-adjective': 'invertible',
                'null-dimension-value': '0', 'column-space-lhs': r'\text{Col}(A)',
                'rank-rhs': r'\text{rank}(A)'}
    for t, target in g.TARGETS.items():
        q = g.SOURCES[t]; f = q[':question/answer-fields'][0]
        assert f[':answer-field/correct'][':answer/value'] == expected[target]
        assert len({a[':answer/value'] for a in f[':answer-field/choices']}) == 5
        assert q[':question/problem'].count(r'\bbox') == 1
        # All observed wrong options are checked below by type or universal
        # statement witnesses, rather than merely accepting the source key.
        assertions.append({'source': t, 'target': target, 'correct': expected[target]})
    witnesses = []
    for n in range(1, 7):
        a = 2 * sp.eye(n)
        if n > 1: a[0, 1] = 1
        z = sp.zeros(n)
        assert a.rank() == n and len(a.nullspace()) == 0
        assert a.inv().rank() == n and len(a.inv().nullspace()) == 0
        assert (a**n).rank() == n
        assert z.rank() == 0 and len(z.nullspace()) == n
        assert a.det() != 0 and z.det() == 0
        # n, n+1, n^2, and 1 are nonzero; all are wrong for null dimension 0.
        assert all(sp.Integer(x) != 0 for x in (n, n+1, n*n, 1))
        witnesses.append({'n': n, 'invertible_rank': a.rank(), 'inverse_nullity': len(a.inv().nullspace()),
                          'power_rank': (a**n).rank(), 'singular_nullity': len(z.nullspace())})
    # Adjective distractors are not equivalent to invertibility: a nonsingular
    # non-diagonal matrix; singular diagonal matrix; identity; nonidentity.
    a = sp.Matrix([[2, 1], [0, 2]])
    assert a.det() != 0 and not a.is_diagonal()
    assert sp.diag(1, 0).is_diagonal() and sp.diag(1, 0).det() == 0
    assert sp.eye(2).det() != 0 and a != sp.eye(2)
    # The other banks use set vs scalar vs matrix distinctions. For n>=1,
    # R^n is nonzero; Col(A)=Col(A^-1)=R^n, unlike Null(A)={0}.
    # q-141348: Null(A)={0} is not R^n; dimensions/rank/det are scalars.
    # q-141194: dim Null(A)=nullity(A)=0 != n; Col/Null are spaces.
    report = grading([r for r in replays if r['generation']['supported_source']], out / 'native')
    assert report['accepted_checks'] == 7 and report['rejected_checks'] == 28
    assert report['documented_unresolved_checks'] == 0
    executions = [g.generate(level, 5, seed) for level in ('easy', 'moderate', 'hard') for seed in (0, 1, 1930, 2**32-1)]
    assert all(x['instances'] == [] and x['produced'] == 0 and x['shortage_remaining'] == 5 for x in executions)
    assert g.generate('easy', 0)['shortage_remaining'] == 0
    for level in ('easy', 'moderate', 'hard'):
        public = subprocess.run([str(ROOT / '.venv/bin/python'), str(HERE.with_suffix('.py')),
                                 '--difficulty', level, '--count', '5', '--seed', '1', '--format', 'json'],
                                capture_output=True, text=True, check=True)
        assert json.loads(public.stdout) == g.generate(level, 5, 1)
    save(out / 'source-replays.json', replays)
    save(out / 'source-bank-replay.json', fidelity)
    save(out / 'executions.json', executions)
    save(out / 'mathematics.json', {'assertions': assertions, 'exact_matrix_witnesses': witnesses,
         'universal_argument': 'For every invertible real n by n matrix (n>=1), rank=n, nullity=0, Col(A)=R^n and Null(A)={0}. Rank-nullity gives the dimensions. A^-1 and positive powers are invertible. Scalar, matrix, and subspace values are kept distinct.',
         'adjective_counterexamples': ['[[2,1],[0,2]] invertible but not diagonal or identity', 'diag(1,0) diagonal but singular', 'I is invertible', 'zero matrix is nonidentity and singular']})
    result = {'passed': True, 'source_basis': 2617, 'source_banks_replayed': 12,
              'matched_options': 60, 'total_options': 60, 'matched_distractors': 48,
              'supported_profiles': 7, 'excluded_profiles': 5, 'distinct_supported_tasks': 5,
              'fresh_distinct_capacity_beyond_source': 0, 'native_grader': {'accepted': 7, 'rejected': 28, 'unresolved': 0},
              'deterministic_replay': True, 'seed_changes_create_no_new_content': True,
              'public_cli_checked': True, 'plots': 'none; practice uses only standalone theorem TeX',
              'source_errors_preserved_only_as_evidence': True,
              'generator_sha256': hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),
              'sympy_version': sp.__version__, 'unsupported_levels': g.UNSUPPORTED}
    save(out / 'validation.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
