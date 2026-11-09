"""Independently derive every practice answer from the stored problem's givens."""
import json
import re
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).resolve().parent
topic = json.loads((HERE / 'topic-before.json').read_text())[0][0]
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

def expression(text):
    text = re.sub(r'\\(?:mathbf|mathrm|textbf|text)\{([^{}]+)\}', r'\1', text)
    text = re.sub(r'\\(?:left|right|displaystyle)\b|\\,', '', text)
    text = re.sub(r'\{([A-Za-z])\}_\{(\d+)\}', r'\1\2', text)
    text = re.sub(r'([A-Za-z])_\{?(\d+)\}?', r'\1\2', text)
    text = text.replace('{', '(').replace('}', ')').replace('^', '**').strip()
    return parse_expr(text, transformations=TRANSFORMS,
                      local_dict={k: sp.Symbol(k) for k in ['x', 'y', 'v1', 'v2', 'u', 'w', 'b', 'c', 'q', 'r']})

def mask_vectors(text):
    vectors = []
    def replace(match):
        body = match[1] if match[1] is not None else match[2]
        if '{{' in body:
            return match[0]
        entries = re.split(r'\\\\|,', body)
        vector = sp.Matrix([expression(entry) for entry in entries])
        vectors.append(vector)
        return 'VEC' + str(len(vectors)-1)
    return re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|⟨([^⟩]+)⟩', replace, text, flags=re.S), vectors

def calls(text):
    text = re.sub(r'\\(?:left|right)\b|\\,', '', text)
    text = text.replace('\\mathbf{T}', 'T')
    return re.findall(r'T\(([^()]*)\)', text)

def vector_answer(value):
    _, vectors = mask_vectors(value)
    return vectors[0] if vectors else sp.Matrix([expression(value)])

results = []
for kp in topic[':topic/knowledge-points']:
    for q in kp[':knowledge-point/questions']:
        mid, problem = q[':question/math-academy-id'], q[':question/problem']
        result = {'entity': q[':db/id'], 'mid': mid, 'kp': kp[':knowledge-point/title']}
        masked, vectors = mask_vectors(problem)
        args = calls(masked)
        if kp[':db/id'] == 17592186087746:
            x, y, k = sp.symbols('x y k')
            x1, x2, y1, y2 = sp.symbols('x1 x2 y1 y2')
            output = vectors[1]
            scale = output.subs({x:k*x, y:k*y}, simultaneous=True) - k*output
            additive = (output.subs({x:x1+x2, y:y1+y2}, simultaneous=True)
                        - output.subs({x:x1, y:y1}, simultaneous=True)
                        - output.subs({x:x2, y:y2}, simultaneous=True))
            truths = [all(sp.expand(v)==0 for v in scale), all(sp.expand(v)==0 for v in additive)]
            linear = all(truths)
            expected = {}
            for field in q[':question/answer-fields']:
                key = field[':answer-field/key']
                if key == 'selection':
                    expected[key] = 'III only'
                elif 'None of the above' in key:
                    expected[key] = 'false'
                elif 'T(kv)' in key:
                    expected[key] = str(truths[0]).lower()
                elif 'v}_{1}' in key or 'v_1' in key:
                    expected[key] = str(truths[1]).lower()
                else:
                    expected[key] = str(not linear if 'NOT' in key else linear).lower()
            result['derivation'] = {'scaling': truths[0], 'addition': truths[1], 'linear': linear}
        else:
            if kp[':db/id'] == 17592186087747:
                factor = next(vectors[2][i]/v for i,v in enumerate(vectors[0]) if v != 0)
                assert vectors[2] == factor*vectors[0]
                answer = factor*vectors[1]
            elif kp[':db/id'] == 17592186087748:
                first, second, target = map(expression, args[:3])
                symbols = sorted(first.free_symbols | second.free_symbols | target.free_symbols, key=str)
                matrix = sp.Matrix([[v.coeff(s) for s in symbols] for v in [first, second]])
                answer = sp.zeros(vectors[0].rows, 1)
                coefficient = sp.Matrix([[target.coeff(s) for s in symbols]])
                for index in range(vectors[0].rows):
                    answer[index] = (coefficient * matrix.inv() * sp.Matrix([vectors[0][index], vectors[1][index]]))[0]
            else:
                known, target = map(expression, args[:2])
                v1, v2 = sp.symbols('v1 v2')
                target_reduced = sp.expand(target.subs(v2, -v1))
                known_reduced = sp.expand(known.subs(v2, -v1))
                factor = sp.simplify(target_reduced/known_reduced)
                answer = factor*vectors[0]
            result['derived_vector'] = list(map(str, answer))
            fields = q[':question/answer-fields']
            expected = {'selection': answer} if len(fields)==1 else {'field-'+str(i+1): answer[i] for i in range(answer.rows)}
        checks = []
        for field in q[':question/answer-fields']:
            key = field[':answer-field/key']
            correct = field.get(':answer-field/correct')
            wanted = expected[key]
            check = {'key': key, 'expected': str(wanted), 'has_correct_link': bool(correct)}
            if correct:
                value = correct[':answer/value']
                got = value if isinstance(wanted,str) else vector_answer(value) if isinstance(wanted,sp.MatrixBase) else expression(value)
                check.update(stored=value, correct=got == wanted,
                             correct_is_a_choice=correct[':db/id'] in {a[':db/id'] for a in field[':answer-field/choices']})
            checks.append(check)
        result['answer_checks'] = checks
        result['missing_worked_solution'] = not bool(q.get(':question/worked-solution'))
        results.append(result)
(HERE/'mathematics.json').write_text(json.dumps(results,indent=2)+'\n')
failures = [r for r in results if any(c.get('correct') is False or not c['has_correct_link'] for c in r['answer_checks'])]
print(json.dumps({'practice_questions':len(results), 'wrong_or_missing_keys':failures},indent=2))
