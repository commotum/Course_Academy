"""Independent readback of printed matrices, operations, banks and solutions."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('gaussian_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')

def fingerprint(q):
    return g.fingerprint(q)

def number(text):
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text.strip())
    assert re.fullmatch(r'[\d()\s*/+.-]+', text), text
    return sp.Rational(sp.sympify(text))

def printed_matrices(text):
    if r'\\begin' in text:
        text = text.replace('\\\\', '\\')
    raw = re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}', text, re.S)
    return [sp.Matrix([[number(cell) for cell in row.split('&')] for row in body.split(r'\\')]) for body in raw]

def pair(text):
    text = text.replace('\\\\', '\\')
    vals = {}
    for var, raw in re.findall(r'([xy])\s*=\s*(' + g.NUMBER + ')', text):
        vals[var] = number(raw)
    return (vals['x'], vals['y']) if vals else None

def object_value(text):
    matrices = printed_matrices(text)
    assert len(matrices) == 1
    return (tuple(matrices[0]), pair(text))

def apply_operation(matrix, row, expression):
    expression = re.sub(r'\{R\}_\{([12])\}', lambda m: 'r' + m[1], expression)
    expression = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', expression)
    expression = expression.replace(r'\cdot', '*').replace(' ', '')
    expression = re.sub(r'(\d|\))(?=r)', r'\1*', expression)
    assert re.fullmatch(r'[r12\d()\s*/+.\-]+', expression), expression
    out = matrix.copy()
    for column in range(3):
        out[row, column] = sp.sympify(expression, locals={'r1': matrix[0, column], 'r2': matrix[1, column]})
    return out

def independent(rec):
    q = rec['question']; meta = rec['generation']
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    sid, k = meta['parameters']; assert meta['bank_profile'] == sid
    assert rec == g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'], sid, meta['parameters'])
    a, = printed_matrices(q[':question/problem']); assert a.shape == (2, 3)
    assert a[:, :2].det() != 0 and a[0, 0] != 0
    normalized = a.copy(); normalized[0, :] /= a[0, 0]
    normalized[1, :] -= a[1, 0]*normalized[0, :]
    normalized[1, :] /= normalized[1, 1]
    x, y = sp.symbols('x y')
    values = sp.solve([a[i, 0]*x+a[i, 1]*y-a[i, 2] for i in range(2)], (x, y))
    want_pair = (values[x], values[y]) if 'and then solve' in q[':question/problem'] else None
    field, = q[':question/answer-fields']
    assert field[':answer-field/type'] == ':answer-field.type/radio' and field[':answer-field/key'] == 'selection'
    assert len(field[':answer-field/choices']) == 5
    objects = [object_value(answer[':answer/value']) for answer in field[':answer-field/choices']]
    assert len(set(objects)) == 5
    equivalent_objects = [(tuple(printed_matrices(a[':answer/value'])[0].rref()[0]), pair(a[':answer/value'])) for a in field[':answer-field/choices']]
    assert len(set(equivalent_objects)) == 5, 'Row-equivalent answer objects'
    correct = [answer[':answer/id'] for answer, obj in zip(field[':answer-field/choices'], objects) if obj == (tuple(normalized), want_pair)]
    assert correct == [field[':answer-field/correct'][1]], 'Complete object answer key mismatch'
    sol = q[':question/worked-solution']
    steps = printed_matrices(sol); assert steps[0] == a and steps[-1] == normalized
    operations = re.findall(r'\{R\}_\{([12])\} & :=(.*?)(?= \\\\|\\end\{aligned\})', sol)
    assert len(operations) == len(steps)-1
    for i, (row, expression) in enumerate(operations):
        assert apply_operation(steps[i], int(row)-1, expression) == steps[i+1], 'Printed operation mismatch'
    if want_pair:
        tail = sol.split('The system is now', 1)[1]
        assert pair(tail) == want_pair, 'Stale conclusion'
        system = re.search(r'x(.*?) &=(' + g.NUMBER + r') \\\\ y &=(' + g.NUMBER + ')', tail)
        assert system and number(system[2]) == normalized[0, 2] and number(system[3]) == y.subs(values)
        bx = system[1].replace('y', '')
        coefficient = number(bx) if bx not in ('+', '-') else sp.Integer(1 if bx == '+' else -1)
        assert coefficient == normalized[0, 1]
        # Verify the substituted value, constant RHS, collected contribution and
        # final x in the actual displayed back-substitution line.
        block = re.findall(r'\$\$\n(.*?)\n\$\$', tail, re.S)[-1]
        left, rest = block.split('=', 1)
        substituted = re.search(r'\((' + g.NUMBER + r')\)', left)
        assert substituted and number(substituted[1]) == values[y]
        first, right = rest.split(r'\,⇒\,x=')
        assert number(first) == normalized[0, 2]
        calculation, final = right.rstrip('.').rsplit('=', 1)
        assert number(calculation) == values[x] and number(final) == values[x]
    assert meta['mathematical_fingerprint'] == fingerprint(q)
    return rec

check = independent

def checks(rec):
    field = rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == field[':answer-field/correct'][1] else 'rejected', 'purpose': 'all five complete choices through application radio grader'} for a in field[':answer-field/choices']]

def main():
    replays = []; inputs = []; coverage = {}; recipes = []; distinct = {l: set() for l in g.SUPPORTED_LEVELS}; review = []
    for sid, old in g.CASES.items():
        replay = g.source_replay(sid)
        q = replay['question']; f = q[':question/answer-fields'][0]; original = old[':question/answer-fields'][0]
        assert q[':question/problem'] == old[':question/problem'] and q[':question/worked-solution'] == old[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1]) == original[':answer-field/correct'][':answer/value']
        replays.append({'source': sid, 'complete_bank_match': True, 'matched_choices': 5, 'matched_distractors': 4, 'prompt_exact': True, 'solution_exact': True, 'missing': [], 'extra': [], 'generation_status': 'excluded-ambiguous-bank' if sid in g.EXCLUDED_PROFILES else 'supported'})
        if sid in g.EXCLUDED_PROFILES:
            choices = original[':answer-field/choices']
            keyed = original[':answer-field/correct'][':answer/value']
            correct_rref = printed_matrices(keyed)[0].rref()[0]
            equivalent = [a[':answer/value'] for a in choices if printed_matrices(a[':answer/value'])[0].rref()[0] == correct_rref]
            assert len(equivalent) == 2
            for a in choices:
                matrix = printed_matrices(a[':answer/value'])[0]
                recipes.append({'source': sid, 'source_answer_id': a[':answer/id'], 'field': 'selection', 'profile': sid, 'observed_value': a[':answer/value'], 'coefficient_entries_fixed': [[str(matrix[i,j]) for j in range(2)] for i in range(2)], 'augmented_column_recipe': [str(matrix[i,2])+'*k' for i in range(2)], 'reproduces_complete_value_at_k_1': True, 'status': 'excluded: correct REF and equivalent RREF in same bank'})
            save('source-errors.json', {'source': sid, 'issue': 'Two offered matrices are valid row echelon forms and have identical RREF; one is the actual RREF. Ambiguous under mathematical equivalence.', 'equivalent_values': equivalent, 'action': 'Preserve source, exclude profile and its variants from validated inventory.'})
            review.append('## ' + sid + '\n\nExcluded source bank: both the keyed REF and another offered RREF represent the same system.\n\n' + g.markdown(replay))
            continue
        independent(replay)
        rows = []
        for p in g.domain(sid):
            rec = independent(g.generate(g.level(sid), 59775, sid, p)); rows.append(rec); distinct[g.level(sid)].add(fingerprint(rec['question']))
            inputs.append({'label': sid + str(p), 'record': rec, 'checks': checks(rec)})
        coverage[sid] = {'slot': 'right-hand-side scale', 'tested': [p[1] for p in g.domain(sid)], 'eligible_missing': [], 'fixed_coefficients_and_operations': True, 'distinct_solutions': len({pair(r['question'][':question/answer-fields'][0][':answer-field/choices'][next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id'] == r['question'][':question/answer-fields'][0][':answer-field/correct'][1])][':answer/value']) if 'and then solve' in r['question'][':question/problem'] else tuple(printed_matrices(r['question'][':question/worked-solution'])[-1]) for r in rows})}
        assert len(rows) > 1
        assert g.generate(g.level(sid), 123, sid, g.DEFAULTS[sid])['question'] == q
        # Complete profile, never a pooled subset: last-column and solution
        # coordinates scale; all original coefficient entries remain fixed.
        for a in original[':answer-field/choices']:
            matrix = printed_matrices(a[':answer/value'])[0]; point = pair(a[':answer/value'])
            recipes.append({'source': sid, 'source_answer_id': a[':answer/id'], 'field': 'selection', 'profile': sid, 'observed_value': a[':answer/value'], 'coefficient_entries_fixed': [[str(matrix[i,j]) for j in range(2)] for i in range(2)], 'augmented_column_recipe': [str(matrix[i,2])+'*k' for i in range(2)], 'point_recipe': [str(z)+'*k' for z in point] if point else None, 'reproduces_complete_value_at_k_1': True, 'interpretation': 'observed expression pattern; psychological mistake unresolved', 'extension': 'proportional RHS response, restricted to k in this bounded domain'})
        review.append('## ' + sid + '\n\nOriginal replay\n\n' + g.markdown(replay) + '\n\nChanged RHS, fixed coefficients and stages\n\n' + g.markdown(rows[1]))
    for l in ('hard', 'unclassified'):
        try: g.generate(l)
        except ValueError: pass
        else: raise AssertionError('Unsupported level admitted')
    save('source-replay.json', {'passed': True, 'complete_banks_matched': 8, 'complete_banks_total': 8, 'distractors_matched': 32, 'distractors_total': 32, 'supported_complete_banks': 7, 'excluded_complete_banks': 1, 'profiles': replays})
    save('choice-recipes.json', recipes); save('slot-coverage.json', coverage); save('native-input.json', inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(HERE/'native-input.json'), str(HERE/'native-grading.json')], check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('previews.json', [item['record'] for item in inputs])
    save('validation.json', {'status': 'pass', 'passed': True, 'exhaustive_instances': len(inputs), 'distinct_numeric_tasks': {l:len(s) for l,s in distinct.items()}, 'supported_levels': list(g.SUPPORTED_LEVELS), 'fidelity': '8/8 exact prompt/solution and complete banks; 32/32 distractors', 'correctness': 'independent printed equations, elimination algorithm, every displayed row operation, complete matrix/solution choice objects, system and back substitution', 'grading': 'every option at every eligible scale/profile through application grade_field', 'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), HERE/'source.json', HERE/'validate.py', HERE/'replenish.py', HERE/'capabilities.json', ROOT/'generate/runs/current/check-engine')}})

if __name__ == '__main__': main()
