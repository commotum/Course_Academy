"""Read-only, exact-rational independent audit of the captured topic questions."""
import collections
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent
SNAPSHOT = ROOT / 'snapshot.json'
x = json.loads(SNAPSHOT.read_text())
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
PIVOT_KPS = {17592186124477, 17592186124480}
NONPIVOT_KP = 17592186124478
COUNT_KP = 17592186124479


def parse_matrix(text):
    text = re.sub(r'\\bbox\[[^]]*\]\{([^{}]*)\}', r'\1', text)
    rows = [[Fraction(cell.strip()) for cell in row.split('&')]
            for row in text.split('\\\\')]
    assert len(set(map(len, rows))) == 1
    return rows


def rational_json(matrix):
    return [[int(v) if v.denominator == 1 else str(v) for v in row] for row in matrix]


def rref(matrix):
    a = [row[:] for row in matrix]
    pivots = []
    row = 0
    for col in range(len(a[0])):
        pivot_row = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot_row is None:
            continue
        a[row], a[pivot_row] = a[pivot_row], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(len(a)):
            if i != row:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        pivots.append(col + 1)
        row += 1
        if row == len(a):
            break
    return a, pivots


def echelon(matrix):
    leading = [next((j for j, v in enumerate(row) if v), len(row)) for row in matrix]
    nonzero = [n for n in leading if n != len(matrix[0])]
    return nonzero == sorted(set(nonzero)) and leading == sorted(leading)


def ordinals(text):
    return [int(n) for n in re.findall(r'\$(\d+)\$(?:st|nd|rd|th)', text)]


def solution_key(solution, kp):
    if kp == COUNT_KP:
        return int(re.search(r'number of pivot columns is \$(\d+)', solution).group(1))
    if kp == NONPIVOT_KP:
        return ordinals(solution.split('Therefore,')[-1])
    if 'In particular,' in solution:
        return ordinals(solution.split('In particular,')[-1])
    return ordinals(solution.split('pivots in the')[-1].split(':')[0])


def check_operation(before, after, raw):
    compact = re.sub(r'\s|&|\\\\|∼', '', raw)
    compact = re.sub(r'\{R\}_\{(\d+)\}', r'R\1', compact)
    compact = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'\1/\2', compact)
    compact = compact.replace('(', '').replace(')', '')
    expected = [r[:] for r in before]
    swap = re.fullmatch(r'R(\d+)↔R(\d+)', compact)
    if swap:
        i, j = (int(t) - 1 for t in swap.groups())
        expected[i], expected[j] = expected[j], expected[i]
    else:
        add = re.fullmatch(r'R(\d+):=R(\d+)([+\-])([+\-\d/]*?)R(\d+)', compact)
        assert add, compact
        i, base, sign, coef, j = add.groups()
        i, base, j = int(i) - 1, int(base) - 1, int(j) - 1
        coefficient = Fraction(coef or '1') * (1 if sign == '+' else -1)
        expected[i] = [a + coefficient * b for a, b in zip(before[base], before[j])]
    return {'operation': raw.strip(), 'normalized_operation': compact,
            'matches_displayed_next_matrix': expected == after,
            **({'expected_next_matrix': rational_json(expected),
                'displayed_next_matrix': rational_json(after)} if expected != after else {})}


rows = []
for wrapped in x['questions']:
    q = wrapped[0]
    qid = q[':db/id']
    memberships = q.get(':knowledge-point/_questions', [])
    canon = q.get(':knowledge-point/_canonical-example', [])
    kpids = [a[':db/id'] for a in memberships + canon]
    assert len(kpids) == 1
    kp = kpids[0]
    problem = q[':question/problem']
    solution = q.get(':question/worked-solution', '')
    fields = q.get(':question/answer-fields', [])
    matrix = parse_matrix(MATRIX.search(problem).group(1))
    reduced, pivots = rref(matrix)
    n = len(matrix[0])
    universe = list(range(1, n + 1))
    wanted = len(pivots) if kp == COUNT_KP else (
        [i for i in universe if i not in pivots] if kp == NONPIVOT_KP else pivots)
    expected_solution_key = solution_key(solution, kp)
    field_checks = []
    for f in fields:
        choices = f.get(':answer-field/choices', [])
        key = f.get(':answer-field/correct')
        decoded = {}
        for a in choices:
            value = a[':answer/value']
            if kp == COUNT_KP:
                decoded[a[':db/id']] = int(value)
            elif value.startswith('All the columns'):
                decoded[a[':db/id']] = universe
            else:
                decoded[a[':db/id']] = ordinals(value)
                assert decoded[a[':db/id']], value
        key_value = decoded.get(key[':db/id']) if key else None
        field_checks.append({
            'field_eid': f[':db/id'], 'field_type': f[':answer-field/type'][':db/ident'],
            'choice_count': len(choices), 'has_key': key is not None,
            'key_is_in_owned_bank': key[':db/id'] in decoded if key else False,
            'database_key': key_value, 'key_matches_exact_math': key_value == wanted,
            'all_choices_reference_existing_columns': (
                all(set(subset).issubset(universe) for subset in decoded.values())
                if kp != COUNT_KP else None),
            'has_choice_feedback': any(any('feedback' in k for k in a) for a in choices),
            'extra_field_keys': sorted(set(f) - {
                ':db/id', ':answer-field/choices', ':answer-field/correct',
                ':answer-field/id', ':answer-field/key', ':answer-field/type'}),
        })
    matches = list(MATRIX.finditer(solution))
    solution_matrices = [parse_matrix(m.group(1)) for m in matches]
    operations = [check_operation(a, b, solution[ma.end():mb.start()])
                  for a, b, ma, mb in zip(solution_matrices, solution_matrices[1:], matches, matches[1:])]
    matrix_name = re.search(r'([A-Z])=\\begin\{bmatrix\}', problem).group(1)
    conclusion_names = re.findall(r'(?:[Ww]e can see that|we see that) \$([A-Z])\$', solution)
    issues = []
    if any(not op['matches_displayed_next_matrix'] for op in operations):
        issues.append('A displayed row operation does not produce the displayed next matrix; separate content repair, not a key/candidacy change.')
    if any(name != matrix_name for name in conclusion_names):
        issues.append('Conclusion names a different matrix from the prompt; separate wording correction.')
    if qid == 17592186124885:
        issues.append('Second operation should be R5 := R5 + (2/7) R4. Its final row should be [0,0,0,0,1], not [0,0,0,0,-1]. The rank/key remain 5.')
    if qid == 17592186364337:
        issues.append('Minor grammar: final sentence says "the $3$rd columns" for a single column.')
    learner_items = [item for item_qid, item in x['items'] if item_qid == qid]
    learner_checks = []
    for item in learner_items:
        answers = item.get(':task-item/responses', [])
        owned_answers = {a[':db/id'] for f in fields for a in f.get(':answer-field/choices', [])}
        correct_ids = {f[':answer-field/correct'][':db/id'] for f in fields if ':answer-field/correct' in f}
        learner_checks.append({
            'task_item_eid': item[':db/id'],
            'status': item[':task-item/status'][':db/ident'],
            'response_count': len(answers),
            'all_responses_owned': all(a[':db/id'] in owned_answers for a in answers),
            'responses_match_database_key': set(a[':db/id'] for a in answers) == correct_ids if answers else None,
            'migration_required': bool(answers) and kp != COUNT_KP,
        })
    decision = ('not_radio_canonical' if canon else 'retain_radio' if kp == COUNT_KP else 'convert')
    reason = ('Fieldless, display-only canonical example; no existing radio response to migrate.' if canon else
              'Asks for a single numerical count (rank), not a subset of columns.' if kp == COUNT_KP else
              'Asks which columns meet a property; independently selectable finite universe is every original matrix column in left-to-right order. Existing combination options map unambiguously to subsets.')
    rows.append({
        'question_eid': qid, 'math_academy_id': q[':question/math-academy-id'],
        'kp_ids': kpids, 'canonical': bool(canon), 'decision': decision,
        'strong_checkbox_candidate': decision == 'convert', 'reason': reason,
        'difficulty': q.get(':question/difficulty', {}).get(':db/ident'),
        'has_worked_solution': bool(solution), 'field_count': len(fields),
        'matrix': rational_json(matrix), 'exact_rref': rational_json(reduced),
        'pivot_columns': pivots, 'nonpivot_columns': [i for i in universe if i not in pivots],
        'rank': len(pivots), 'mathematical_answer': wanted,
        'solution_answer': expected_solution_key, 'solution_answer_matches_exact_math': expected_solution_key == wanted,
        'problem_is_echelon': echelon(matrix),
        'solution_first_matrix_matches_problem': solution_matrices[0] == matrix,
        'solution_matrices_row_equivalent': [rref(m)[0] == reduced for m in solution_matrices],
        'solution_last_matrix_is_echelon': echelon(solution_matrices[-1]),
        'solution_operations': operations, 'separate_solution_issues': issues,
        'field_checks': field_checks, 'learner_checks': learner_checks,
    })

summary = {
    'questions': len(rows), 'practice_radios': sum(not r['canonical'] for r in rows),
    'canonical_examples': sum(r['canonical'] for r in rows),
    'strong_checkbox_candidates': sum(r['strong_checkbox_candidate'] for r in rows),
    'retain_radio_count_questions': sum(r['decision'] == 'retain_radio' for r in rows),
    'all_practice_keys_match_exact_math': all(f['key_matches_exact_math'] for r in rows for f in r['field_checks']),
    'all_solution_conclusions_match_exact_math': all(r['solution_answer_matches_exact_math'] for r in rows),
    'all_practice_questions_have_key_difficulty_solution': all(
        r['difficulty'] and r['has_worked_solution'] and len(r['field_checks']) == 1
        and r['field_checks'][0]['has_key'] for r in rows if not r['canonical']),
    'candidate_saved_response_items': sum(c['migration_required'] for r in rows for c in r['learner_checks']),
    'total_saved_items': sum(len(r['learner_checks']) for r in rows),
    'solution_operations_checked': sum(len(r['solution_operations']) for r in rows),
    'solution_operations_mismatching': sum(not c['matches_displayed_next_matrix'] for r in rows for c in r['solution_operations']),
    'separate_solution_issue_question_ids': [r['question_eid'] for r in rows if r['separate_solution_issues']],
    'by_kp': {str(k): dict(collections.Counter(r['decision'] for r in rows if k in r['kp_ids'])) for k in sorted({k for r in rows for k in r['kp_ids']})},
}
out = {
    'database': x['database'], 'lineage': x['lineage'], 'basis': x['basis'],
    'source': str(SNAPSHOT), 'source_sha256': hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(),
    'method': 'Independent exact Fraction Gaussian elimination of each prompt matrix; compare existing keys and solution conclusions; execute each displayed row operation; inspect response structure and saved learner items. No database writes.',
    'summary': summary, 'questions': rows,
}
(ROOT / 'independent-review.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(summary, indent=2))
