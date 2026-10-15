"""Validate printed inventory, independently of generator metadata.

Source decoding is analysis only: malformed stored strings never count as
available. Historical captures and current source records remain unchanged.
"""
import copy, hashlib, json, re, uuid
import sympy as s
import printed_math as pm


class SourceParser(pm.Parser):
    def __init__(self, text):
        text = pm.prepare(text)
        text = text.replace(r'\operatorname{arctan}', r'\arctan').replace('{ln}', r'\ln')
        text = re.sub(r'(\\(?:sin|cos))\s*([+-]?\d+)\s*t', r'\1(\2t)', text)
        text = re.sub(r'(\\(?:sin|cos))\s*([+-]?\d+)\s*\\pi', r'\1(\2\\pi)', text)
        pattern = r'\\(?:frac|sqrt|sin|cos|ln|log|arctan|pi|Dt|Dx|Dy|Dz)|[0-9]+|[xyz te]|[{}()+*/^,⟨⟩-]'
        residue = re.sub(pattern, '', text)
        if residue.strip():
            raise ValueError('Unparsed source math: ' + repr(residue))
        self.tokens = [v for v in re.findall(pattern, text) if v.strip()]
        self.i = 0

    def atom(self):
        if self.peek() == 'e':
            self.take()
            return s.E
        if self.peek() == r'\arctan':
            self.take()
            return s.atan(self.atom())
        return super().atom()


def parse(text):
    return SourceParser(text).parse()


def prompt_data(question):
    text = question[':question/problem']
    function = parse(re.search(r'\$f\([^$]*?=\s*([^$]+)\$', text)[1])
    curve = list(parse(re.search(r'\$r\(t\)\s*=\s*([^$]+)\$', text)[1]))
    at = parse(re.search(r'at the point \$t\s*=\s*([^$]+)\$', text)[1])
    return function, curve, at


def task(question):
    function, curve, at = prompt_data(question)
    data = [s.srepr(s.simplify(function)), [s.srepr(s.simplify(v)) for v in curve], s.srepr(at)]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def check_record(record, validator):
    validator.format_check(record)
    assert record['generation']['eligible_for_learning']
    assert not record['generation']['evidence_only']
    assert not pm.validate(record)
    # The identity and metadata cannot substitute for parsing the actual prompt.
    function, curve, at = prompt_data(record['question'])
    g = validator.g
    expected_function, expected_curve = g.model(record['generation']['template'], record['generation']['parameters'])
    assert pm.equal(function, expected_function)
    assert all(pm.equal(a, b) for a, b in zip(curve, expected_curve))
    assert len(curve) == len(expected_curve)
    assert pm.equal(at, s.sympify(record['generation']['parameters']['t0']))


def decoded_evidence(text):
    return text.replace('\\\\', '\\').replace(r'\u2061', '⁡')


def source_check(question):
    """Check full source banks and solution rows; report decoding, never repair."""
    function, curve, at = prompt_data(question)
    variables = [pm.X, pm.Y, pm.Z][:len(curve)]
    gradient = s.Matrix([s.diff(function, v) for v in variables])
    composition = gradient.subs(dict(zip(variables, curve)), simultaneous=True)
    velocity = s.Matrix([s.diff(v, pm.T) for v in curve])
    derivative = s.diff(function.subs(dict(zip(variables, curve)), simultaneous=True), pm.T)
    correct = s.simplify(derivative.subs(pm.T, at))
    field = question[':question/answer-fields'][0]
    choices = field[':answer-field/choices']
    malformed = [a[':answer/value'] for a in choices if decoded_evidence(a[':answer/value']) != a[':answer/value']]
    values = [parse(decoded_evidence(a[':answer/value'])) for a in choices]
    assert len(values) == 5 and all(not pm.equal(a, b) for i, a in enumerate(values) for b in values[i+1:])
    matches = [a for a, value in zip(choices, values) if pm.equal(value, correct)]
    assert len(matches) == 1
    assert matches[0][':answer/id'] == field[':answer-field/correct'][':answer/id']
    assert pm.equal(parse(field[':answer-field/correct'][':answer/value']), correct)
    stages = pm.blocks(question[':question/worked-solution'])
    assert len(stages) == 6
    errors = []
    checked = 0
    for index, expected in ((1, gradient), (2, composition), (3, velocity), (4, derivative), (5, correct)):
        rows = stages[index][1:] if index == 4 else stages[index]
        for row_index, row in enumerate(rows):
            for equality_part in row.split('='):
                got = parse(equality_part)
                checked += 1
                if not pm.equal(got, expected):
                    errors.append({'block': index, 'row': row_index, 'printed': equality_part, 'expected': str(expected)})
    return {'source': question.get(':question/math-academy-id'), 'question_id': str(question[':question/id']),
            'correct_scalar': str(correct), 'complete_bank_mathematically_valid_after_analysis_decoding': True,
            'choices_checked': len(values), 'malformed_stored_choices': malformed,
            'solution_rows_checked': checked, 'solution_errors': errors,
            'eligible_for_inventory': not malformed and not errors,
            'source_modified': False}
