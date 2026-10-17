"""Prepare authorized solution text repairs; no database access or writes.

The historical audit remains immutable. Reuse only its pure exact-rational
checker functions, with the repaired text substituted into an in-memory copy.
"""
import ast
import hashlib
import importlib.util
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
OUT = Path(__file__).resolve().parent
AUDIT = ROOT / 'reference/edb-math/audits/radio2checkbox/2026-10-16/entity-17592186124704'
SNAPSHOT = AUDIT / 'snapshot.json'
CHECKER = AUDIT / 'independent-review.py'
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
COUNT_KP = 17592186124479
NONPIVOT_KP = 17592186124478


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Execute definitions only, not the old audit's file-writing top-level driver.
tree = ast.parse(CHECKER.read_text())
function_names = {
    'parse_matrix', 'rational_json', 'rref', 'echelon', 'ordinals',
    'solution_key', 'check_operation',
}
definitions = ast.Module(
    body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in function_names],
    type_ignores=[],
)
exec(compile(definitions, str(CHECKER), 'exec'), globals())


def inspect_solution(problem, solution, kp):
    original = parse_matrix(MATRIX.search(problem).group(1))
    reduced, pivots = rref(original)
    universe = list(range(1, len(original[0]) + 1))
    wanted = (len(pivots) if kp == COUNT_KP else
              [c for c in universe if c not in pivots] if kp == NONPIVOT_KP else pivots)
    matches = list(MATRIX.finditer(solution))
    matrices = [parse_matrix(m.group(1)) for m in matches]
    operations = [check_operation(a, b, solution[ma.end():mb.start()])
                  for a, b, ma, mb in zip(matrices, matrices[1:], matches, matches[1:])]
    name = re.search(r'([A-Z])=\\begin\{bmatrix\}', problem).group(1)
    conclusion_names = re.findall(r'(?:[Ww]e can see that|we see that) \$([A-Z])\$', solution)
    return {
        'matrix_name': name,
        'conclusion_matrix_names': conclusion_names,
        'matrix_names_match': bool(conclusion_names) and all(n == name for n in conclusion_names),
        'exact_rref': rational_json(reduced),
        'pivot_columns': pivots,
        'nonpivot_columns': [c for c in universe if c not in pivots],
        'rank': len(pivots),
        'mathematical_answer': wanted,
        'solution_answer': solution_key(solution, kp),
        'solution_answer_matches_exact_math': solution_key(solution, kp) == wanted,
        'first_matrix_matches_problem': matrices[0] == original,
        'all_matrices_row_equivalent': all(rref(m)[0] == reduced for m in matrices),
        'last_matrix_is_echelon': echelon(matrices[-1]),
        'operations': operations,
        'all_operations_match': all(op['matches_displayed_next_matrix'] for op in operations),
    }


def assert_valid(check):
    assert all(check[key] for key in (
        'matrix_names_match', 'solution_answer_matches_exact_math',
        'first_matrix_matches_problem', 'all_matrices_row_equivalent',
        'last_matrix_is_echelon', 'all_operations_match',
    )), check


def main():
    snapshot = json.loads(SNAPSHOT.read_text())
    questions = {q[':db/id']: q for [q] in snapshot['questions']}
    replacements = {
        17592186124884: [('we see that $A$ has', 'we see that $B$ has')],
        17592186124885: [
            (r'& {R}_{4} & :={R}_{4}+(\frac{2}{7}){R}_{3}',
             r'& {R}_{5} & :={R}_{5}+(\frac{2}{7}){R}_{4}'),
            (r'0 & 0 & 0 & 0 & -1\end{bmatrix}', r'0 & 0 & 0 & 0 & 1\end{bmatrix}'),
        ],
        17592186124906: [('we see that $B$ has', 'we see that $P$ has')],
        17592186266022: [('we see that $A$ has', 'we see that $B$ has')],
        17592186266026: [('we see that $A$ has', 'we see that $B$ has')],
        17592186364337: [('the only non-pivot column is the $3$rd columns.',
                          'the only non-pivot column is the $3$rd column.')],
        17592186342033: [('the only non-pivot columns are the $1$st and $3$rd column.',
                          'the only non-pivot columns are the $1$st and $3$rd columns.')],
    }
    rows = []
    for eid, edits in replacements.items():
        q = questions[eid]
        kp = q[':knowledge-point/_questions'][0][':db/id']
        before = q[':question/worked-solution']
        after = before
        for old, new in edits:
            assert after.count(old) == 1, (eid, old, after.count(old))
            after = after.replace(old, new)
        old_check = inspect_solution(q[':question/problem'], before, kp)
        check = inspect_solution(q[':question/problem'], after, kp)
        assert_valid(check)
        assert old_check['solution_answer'] == check['solution_answer']
        if eid == 17592186124885:
            reason = ('The second elimination targets row 5 using row 4: '
                      '[0,0,0,2,-1] + (2/7)[0,0,0,-7,7] = [0,0,0,0,1]. '
                      'The previously displayed row target and source were wrong, '
                      'and the last entry should be positive. Rank and key stay 5.')
        elif eid in (17592186364337, 17592186342033):
            reason = 'Match column/columns to the number of non-pivot columns in the conclusion.'
        else:
            reason = 'Use the prompt matrix name in the conclusion; arithmetic and selected columns/count are unchanged.'
        row = {
            'question_eid': eid,
            'question_id': q[':question/id'],
            'math_academy_id': q[':question/math-academy-id'],
            'kp_id': kp,
            'attribute': ':question/worked-solution',
            'before': before,
            'after': after,
            'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
            'after_sha256': hashlib.sha256(after.encode()).hexdigest(),
            'edits': [{'before': old, 'after': new} for old, new in edits],
            'reason': reason,
            'before_validation': old_check,
            'after_validation': check,
            'correct_answer_unchanged': True,
            'database_status': 'prepared-only; root must recheck current solution and CAS exact before value',
        }
        rows.append(row)
        q[':question/worked-solution'] = after
    checks = []
    for q in questions.values():
        kp = (q.get(':knowledge-point/_questions', []) + q.get(':knowledge-point/_canonical-example', []))[0][':db/id']
        check = inspect_solution(q[':question/problem'], q[':question/worked-solution'], kp)
        assert_valid(check)
        checks.append({'question_eid': q[':db/id'], **check})
    result = {
        'status': 'prepared-and-validated',
        'database': snapshot['database'], 'lineage': snapshot['lineage'],
        'captured_basis': snapshot['basis'],
        'source_snapshot': relative(SNAPSHOT), 'source_sha256': sha(SNAPSHOT),
        'independent_checker': relative(CHECKER), 'checker_sha256': sha(CHECKER),
        'method': 'Apply only exact listed solution replacements in memory; Fraction Gaussian elimination and displayed-operation execution reused as pure functions from the immutable independent audit.',
        'correction_count': len(rows), 'corrections': rows,
        'validation': {
            'questions_checked': len(checks),
            'operations_checked': sum(len(c['operations']) for c in checks),
            'all_solutions_valid_after_repairs': True,
            'historical_audit_files_unchanged': True,
            'checks': checks,
        },
    }
    (OUT / 'corrections.json').write_text(json.dumps(result, indent=2) + '\n')
    check_count_generator()
    print(json.dumps({'status': result['status'], 'corrections': len(rows), 'questions_checked': len(checks),
                      'operations_checked': result['validation']['operations_checked']}))


def check_count_generator():
    script = ROOT / 'generate/scratch/17592186124479.py'
    g = load_module(script, 'count_generator')
    source_sha = sha(script)
    records = []
    reports = []
    assert 'q-35459' in g.EXCLUDED and len(g.TEMPLATES) == 16
    for template in g.TEMPLATES:
        candidates = [g.source_replay(template)] + [g.generate(seed=seed, template=template) for seed in range(12)]
        for i, record in enumerate(candidates):
            q = record['question']
            check = inspect_solution(q[':question/problem'], q[':question/worked-solution'], COUNT_KP)
            assert_valid(check)
            fields = q[':question/answer-fields']
            assert len(fields) == 1 and fields[0][':answer-field/type'] == ':answer-field.type/radio'
            field = fields[0]
            correct = next(a for a in field[':answer-field/choices'] if a[':answer/id'] == field[':answer-field/correct'][1])
            assert int(correct[':answer/value']) == check['rank']
            checks = [{'submitted_answer_id': a[':answer/id'],
                       'expected': 'accepted' if a[':answer/id'] == correct[':answer/id'] else 'rejected',
                       'purpose': 'Retained count radio bank after checking exact solution and names'}
                      for a in field[':answer-field/choices']]
            records.append({'label': f'{template}-{i}', 'record': record, 'checks': checks})
        reports.append({'template': template, 'records': len(candidates), 'radio_type_preserved': True,
                        'all_matrix_names_match_prompt': True, 'exact_math_and_rendered_operations_passed': True})
    input_path = OUT / 'count-generator-native-input.json'
    native_report = OUT / 'count-generator-native-report.json'
    input_path.write_text(json.dumps(records, indent=2) + '\n')
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(input_path), str(native_report)], check=True)
    assert sha(script) == source_sha
    report = {
        'status': 'passed', 'generator_path': relative(script), 'sha256': source_sha,
        'change_needed': False,
        'reason': 'Current renderer uses the matrix name parsed from each source prompt; stale names from the historical source solutions are not replayed. Count questions correctly remain radio.',
        'source_replays': len(reports), 'generated_variants': len(records) - len(reports),
        'records': len(records), 'native_grading_checks': sum(len(r['checks']) for r in records),
        'native_report': relative(native_report), 'templates': reports,
        'excluded_templates': g.EXCLUDED,
        'scope_note': 'q-35459 remains excluded; this work does not expand generator difficulty or template support.',
    }
    (OUT / 'count-generator-verification.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
