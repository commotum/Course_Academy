"""Independent final-output mathematics and native grading for both generators."""
from pathlib import Path
import hashlib
import itertools
import json
import re
import subprocess
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
INPUT = HERE.parent / 'generators/representative-records.json'
records = json.loads(INPUT.read_text())
input_hash = hashlib.sha256(INPUT.read_bytes()).hexdigest()


def matrices(text):
    return {match[1]: sp.Matrix([[sp.Rational(v.strip()) for v in row.split('&')] for row in match[2].split(r'\\')])
            for match in re.finditer(r'([ABCDE])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)}


def property_value(matrix, criterion):
    if criterion == 'diagonal':
        return matrix.rows == matrix.cols and all(matrix[i, j] == 0 for i in range(matrix.rows) for j in range(matrix.cols) if i != j)
    return matrix.rows == matrix.cols and all(matrix[i, j] == 0 for i in range(matrix.rows) for j in range(matrix.cols)
                                               if (i > j if criterion == 'upper' else i < j))


def statement(key, definitions):
    match = re.fullmatch(r'\$(.+)\$ is (upper triangular|lower triangular|diagonal)\.', key)
    assert match, key
    expr = match[1].replace('{', '').replace('}', '').replace(' ', '')
    terms = re.findall(r'([+-]?)([ABCDE])(\^T)?', expr)
    assert ''.join(sign + name + transpose for sign, name, transpose in terms) == expr
    matrix = sp.zeros(next(iter(definitions.values())).rows)
    for sign, name, transpose in terms:
        term = definitions[name].T if transpose else definitions[name]
        matrix += -term if sign == '-' else term
    return property_value(matrix, match[2].split()[0])


native, details, render = [], [], []
for index, rec in enumerate(records):
    q = rec['question']
    fields = q[':question/answer-fields']
    criterion = 'upper' if 'upper triangular' in q[':question/problem'] else 'lower'
    assert r'[\begin{aligned}' not in json.dumps(q).replace('\\\\', '\\')
    checks, mapped = [], []
    label = f"generator {rec['knowledge_point']['db_id']} representative {index}"
    if fields[0][':answer-field/type'] == ':answer-field.type/radio':
        assert len(fields) == 1
        field = fields[0]
        truths = []
        for answer in field[':answer-field/choices']:
            printed = matrices(answer[':answer/value'])
            assert len(printed) == 1
            truth = property_value(next(iter(printed.values())), criterion)
            truths.append(truth)
            assert truth == (answer[':answer/id'] == field[':answer-field/correct'][1])
            checks.append({'field_index': 0, 'submitted_answer_id': answer[':answer/id'], 'expected': 'accepted' if truth else 'rejected', 'purpose': 'independent displayed matrix triangular predicate'})
            mapped.append({'old_answer': answer[':answer/id'], 'answer_ids': [answer[':answer/id']], 'expected': truth})
        assert sum(truths) == 1
    else:
        definitions = matrices(q[':question/problem'])
        truths = []
        for i, field in enumerate(fields):
            assert field[':answer-field/type'] == ':answer-field.type/checkbox'
            key = field[':answer-field/key']
            own = matrices(key)
            truth = property_value(next(iter(own.values())), criterion) if own else statement(key, definitions)
            truths.append(truth)
            for answer in field[':answer-field/choices']:
                correct = answer[':answer/value'] == str(truth).lower()
                assert correct == (answer[':answer/id'] == field[':answer-field/correct'][1])
                checks.append({'field_index': i, 'submitted_answer_id': answer[':answer/id'], 'expected': 'accepted' if correct else 'rejected', 'purpose': 'independent displayed matrix expression/property'})
        assert any(truths)
        for bits in itertools.product((False, True), repeat=len(fields)):
            ids = [next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value'] == str(bit).lower()) for bit, f in zip(bits, fields)]
            mapped.append({'old_answer': str(bits), 'answer_ids': ids, 'expected': list(bits) == truths})
    native.append({'label': label, 'record': rec, 'checks': checks, 'mapped_responses': mapped})
    details.append({'index': index, 'kp_id': rec['knowledge_point']['db_id'], 'template': rec['generation']['template'], 'truth': truths, 'whole_responses_checked': len(mapped)})
    render.append({'id': f'generator-{index}', 'label': label, 'problem': q[':question/problem'], 'solution': q[':question/worked-solution'],
                   'fields': [{'id': 20 + i, 'key': f[':answer-field/key'], 'type': f[':answer-field/type'], 'answerType': 'text',
                               'choices': [{'id': 100 + i * 10 + j, 'value': a[':answer/value'], 'type': a[':answer/type']} for j, a in enumerate(f[':answer-field/choices'])]}
                              for i, f in enumerate(fields)]})
(HERE / 'native-input.json').write_text(json.dumps(native, indent=2) + '\n')
(HERE / 'render-cases.json').write_text(json.dumps(render, indent=2) + '\n')
subprocess.run([str(HERE.parent / 'images/check-checkbox-engine'), str(HERE / 'native-input.json'), str(HERE / 'native-grading.json')], check=True)
assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == input_hash
result = {'passed': True, 'generator_math_and_grading_passed': True, 'rendering_pending': True,
          'generators': [{'kp_id': kp, 'generator_sha256': hashlib.sha256((HERE.parent / f'generators/package-source/{kp}.py').read_bytes()).hexdigest()} for kp in (17592186119772, 17592186119784)],
          'representative_records_sha256': input_hash, 'representative_records': len(records),
          'whole_response_combinations': sum(len(item['mapped_responses']) for item in native), 'details': details, 'database_writes': 0}
(HERE / 'generator-review.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'details'}, indent=2))
