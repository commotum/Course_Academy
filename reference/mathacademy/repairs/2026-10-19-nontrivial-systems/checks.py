"""Independent checks of displayed linear equations and their classifications."""
import re
import sympy as sp

X, Y = sp.symbols('x y')

def displayed_rows(question):
    prompt = question[':question/problem']
    match = re.search(r'\\begin\{aligned(?:at)?\}(?:\{2\})?(.*?)\\end\{aligned(?:at)?\}', prompt, re.S)
    if not match:
        # Imported unaligned source prompts are not generated repair candidates.
        return None
    rows = re.split(r'\\\\(?:\[6pt\])?', match[1])
    result = []
    for row in rows:
        row = re.sub(r'l_\{[12]\}:\\quad', '', row).replace('&', '').replace('{}', '').strip()
        left, right = row.split('=')
        assert re.fullmatch(r'[0-9xy+\-\s]+', left + right), row
        def parse(text):
            return sp.sympify(re.sub(r'(\d)([xy])', r'\1*\2', text), locals={'x': X, 'y': Y})
        equation = sp.Poly(parse(left) - parse(right), X, Y)
        assert equation.total_degree() == 1
        result.append((equation.coeff_monomial(X), equation.coeff_monomial(Y), -equation.coeff_monomial(1)))
    assert len(result) == 2, result
    return result

def trivial(rows):
    first, second = rows
    return first == second or first == tuple(-value for value in second)

def outcome(rows):
    matrix = sp.Matrix([row[:2] for row in rows])
    augmented = sp.Matrix(rows)
    if matrix.rank() < augmented.rank():
        return 'none'
    return 'one' if matrix.rank() == 2 else 'infinite'

def correct_value(question):
    field = question[':question/answer-fields'][0]
    ref = field[':answer-field/correct']
    aid = ref[':answer/id'] if isinstance(ref, dict) else ref[1]
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == aid)

COUNTS = {'none': 'no solutions', 'one': 'a single solution', 'infinite': 'infinitely many solutions'}
INTERSECTIONS = {'none': 'do not intersect', 'one': 'intersect at one point', 'infinite': 'intersect at infinitely many points'}

def check_record(record):
    q = record['question']
    rows = displayed_rows(q)
    assert rows is not None and not trivial(rows), q[':question/id']
    kp = record['knowledge_point']['db_id']
    if kp in (17592186073776, 17592186073777):
        bank = COUNTS if kp == 17592186073776 else INTERSECTIONS
        assert correct_value(q) == bank[outcome(rows)]
        assert {a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']} == set(bank.values())
    else:
        assert outcome(rows) == 'infinite'
    return rows
