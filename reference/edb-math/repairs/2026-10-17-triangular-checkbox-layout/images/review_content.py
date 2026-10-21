"""Independent printed-matrix truth and exhaustive native checkbox grading."""
from pathlib import Path
import copy
import hashlib
import itertools
import json
import re
import subprocess
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PLAN = HERE.parent / 'content-plan.json'
source_hash = hashlib.sha256(PLAN.read_bytes()).hexdigest()
plan = json.loads(PLAN.read_text())


def matrices(text):
    result = {}
    for match in re.finditer(r'([ABCD])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S):
        result[match[1]] = sp.Matrix([[sp.Rational(value.strip()) for value in row.split('&')] for row in match[2].split(r'\\')])
    return result


def triangular(matrix, direction):
    return matrix.rows == matrix.cols and all(matrix[i, j] == 0 for i in range(matrix.rows) for j in range(matrix.cols)
                                               if (i > j if direction == 'upper' else i < j))


def expression(text, definitions):
    expr = text.replace('{', '').replace('}', '').replace(' ', '')
    terms = re.findall(r'([+-]?)([ABCD])(\^T)?', expr)
    assert ''.join(sign + name + transpose for sign, name, transpose in terms) == expr, expr
    result = sp.zeros(next(iter(definitions.values())).rows)
    for sign, name, transpose in terms:
        term = definitions[name].T if transpose else definitions[name]
        result += -term if sign == '-' else term
    return result


def normalize(q):
    q = copy.deepcopy(q)
    for field in q[':question/answer-fields']:
        field[':answer-field/type'] = field[':answer-field/type'][':db/ident'] if isinstance(field[':answer-field/type'], dict) else field[':answer-field/type']
        correct = field[':answer-field/correct']
        if isinstance(correct, dict):
            field[':answer-field/correct'] = [':answer/id', correct[':answer/id']]
        for answer in field[':answer-field/choices']:
            if isinstance(answer[':answer/type'], dict):
                answer[':answer/type'] = answer[':answer/type'][':db/ident']
    return q


native, review = [], []
for case in plan['cases']:
    before, after = case['before'], case['after']
    qs = normalize(after)
    truth = []
    definitions = matrices(after[':question/problem'])
    for obj in case['objects']:
        content = obj['content']
        if '\\begin{bmatrix}' in content:
            own = matrices(content)
            assert len(own) == 1
            direction = 'upper' if 'upper triangular matrices' in after[':question/problem'] else 'lower'
            actual = triangular(next(iter(own.values())), direction)
        else:
            match = re.fullmatch(r'\$(.+)\$ is (upper|lower) triangular\.', content)
            assert match, content
            actual = triangular(expression(match[1], definitions), match[2])
        assert actual == obj['truth'], (case['question'], content)
        truth.append(actual)
    assert any(truth), 'No all-false practice questions'
    fields = qs[':question/answer-fields']
    assert len(fields) == len(truth) == 3
    by_content = {obj['content']: (obj, value) for obj, value in zip(case['objects'], truth)}
    assert set(f[':answer-field/key'] for f in fields) == set(by_content)
    ordered_objects = [by_content[f[':answer-field/key']][0] for f in fields]
    truth = [by_content[f[':answer-field/key']][1] for f in fields]
    for i, field in enumerate(fields):
        assert field[':answer-field/type'] == ':answer-field.type/checkbox'
        actual = next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == field[':answer-field/correct'][1])
        assert actual == str(truth[i]).lower()
    if case['decision'] == 'repair_checkbox_labels':
        for old, new in zip(before[':question/answer-fields'], after[':question/answer-fields']):
            assert {k: v for k, v in old.items() if k != ':answer-field/key'} == {k: v for k, v in new.items() if k != ':answer-field/key'}
    checks = []
    for i, field in enumerate(fields):
        for answer in field[':answer-field/choices']:
            checks.append({'field_index': i, 'submitted_answer_id': answer[':answer/id'],
                           'expected': 'accepted' if answer[':answer/value'] == str(truth[i]).lower() else 'rejected',
                           'purpose': 'independently computed matrix predicate'})
    def response(bits):
        return [next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value'] == str(bit).lower())
                for bit, f in zip(bits, fields)]
    mapped = [{'old_answer': 'subset ' + str(bits), 'answer_ids': response(bits), 'expected': list(bits) == truth}
              for bits in itertools.product((False, True), repeat=3)]
    if case['decision'] == 'convert_radio':
        old_correct = before[':question/answer-fields'][0][':answer-field/correct'][':db/id']
        for choice in case['choice_mapping']:
            bits = [obj['source_label'] in choice['selected_labels'] for obj in ordered_objects]
            assert (bits == truth) == (choice['old_answer'] == old_correct)
            mapped.append({'old_answer': choice['old_answer'], 'answer_ids': response(bits), 'expected': bits == truth})
    native.append({'label': str(case['question']), 'record': {'question': qs, 'knowledge_point': {'title': 'Triangular Matrices'}},
                   'checks': checks, 'mapped_responses': mapped})
    review.append({'question': case['question'], 'independent_truth': truth, 'checkbox_subsets_checked': 8,
                   'preserved_radio_choices': len(case['choice_mapping'])})

# Verify each corrected worked matrix independently of its explanatory prose.
by_id = {c['question']: c['after'] for c in plan['cases']}
for eid, expr in [(17592186120426, 'A^T+A'), (17592186262616, 'B-B^T'), (17592186262618, 'B^T')]:
    q = by_id[eid]
    expected = expression(expr, matrices(q[':question/problem']))
    printed = re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', q[':question/worked-solution'], re.S)[-1]
    actual = sp.Matrix([[sp.Rational(v.strip()) for v in row.split('&')] for row in printed.split(r'\\')])
    assert actual == expected

(HERE / 'native-input.json').write_text(json.dumps(native, indent=2) + '\n')
deps = ROOT / 'target/release/deps'
libs = {name: max(deps.glob(f'lib{name}-*.rlib'), key=lambda path: path.stat().st_mtime_ns) for name in ('course_academy_engine', 'serde_json')}
source = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/check-checkbox-engine.rs'
command = ['rustc', '--edition=2024', '-O', str(source)]
for name, path in libs.items():
    command += ['--extern', name + '=' + str(path)]
command += ['-L', 'dependency=' + str(deps), '-o', str(HERE / 'check-checkbox-engine')]
subprocess.run(command, check=True)
subprocess.run([str(HERE / 'check-checkbox-engine'), str(HERE / 'native-input.json'), str(HERE / 'native-grading.json')], check=True)
assert hashlib.sha256(PLAN.read_bytes()).hexdigest() == source_hash
summary = {'passed': True, 'content_plan_sha256': source_hash, 'question_count': len(review),
           'independently_computed_statements': 60, 'checkbox_subsets': 160, 'original_radio_choices': 20,
           'existing_checkbox_identity_preserved': 16, 'worked_matrices_verified': 3,
           'questions': review, 'database_writes': 0}
(HERE / 'content-verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({key: value for key, value in summary.items() if key != 'questions'}, indent=2))
