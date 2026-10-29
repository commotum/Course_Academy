"""Guard independent triangle-complement practice without fixing its parameters.

Source questions put measurements in diagrams and use both radio and blank fields.
Numerical checking here applies when all measurements also occur in prompt text;
diagram geometry and difficulty remain author/reviewer obligations.
"""
import math
import re

KP = 17592186105906
CONTRACT = 'triangle-complement-full-calculation-v1'


def _enum(value):
    return value[':db/ident'] if isinstance(value, dict) else value


def _answer_id(value):
    if isinstance(value, dict):
        return value[':answer/id']
    if isinstance(value, (list, tuple)):
        return value[1]
    return value


def inspect_record(record):
    q = record['question']
    prompt, solution = q[':question/problem'], q[':question/worked-solution']
    level = _enum(q[':question/difficulty']).rsplit('/', 1)[-1]
    if level not in ('easy', 'moderate', 'hard'):
        raise ValueError('Unknown difficulty')
    if any(x in prompt.lower() for x in ('hint', 'first use', 'then subtract', 'enclosing')) or r'\sin' in prompt:
        raise ValueError('The prompt must leave the triangle calculation and area relationship to the learner')
    if 'nearest integer' not in prompt.lower() or not solution.strip():
        raise ValueError('Supply the requested rounding and a worked solution')
    if len(q[':question/answer-fields']) != 1:
        raise ValueError('Triangle-complement practice needs one area response')
    f = q[':question/answer-fields'][0]
    kind = _enum(f[':answer-field/type']).rsplit('/', 1)[-1]
    choices = f[':answer-field/choices']
    if kind not in ('radio', 'blank') or len(choices) != (5 if kind == 'radio' else 1):
        raise ValueError('Preserve the source radio or blank response structure')
    values = []
    for answer in choices:
        match = re.match(r'^(-?\d+(?:\.\d+)?)', answer[':answer/value'])
        if not match:
            raise ValueError('Area responses must be numeric')
        values.append(float(match[1]))
    if min(values) < 0 or len(set(values)) != len(values):
        raise ValueError('Rounded area choices must be nonnegative and distinct')
    correct = _answer_id(f[':answer-field/correct'])
    keys = [v for answer, v in zip(choices, values) if answer[':answer/id'] == correct]
    if len(keys) != 1:
        raise ValueError('The correct answer must belong to its field exactly once')

    sides = [float(x) for x in re.findall(r'\$[A-D]{2}=([\d.]+)', prompt)]
    angle = re.search(r'meet at \$(\d+(?:\.\d+)?)\^\\circ\$', prompt)
    given = re.search(r'area of (?:the quadrilateral )?\$[A-D]{4}\$ is \$([\d.]+)', prompt)
    if len(sides) != 2 or not angle or not given:
        if not re.search(r'!\[[^]]*\]\([^)]+\)', prompt):
            raise ValueError('Supply side lengths and the included angle in text or a diagram')
        return {'level': level, 'values': values, 'measurements': 'diagram; requires visual mathematical review'}
    a, b = sides
    theta, quadrilateral = float(angle[1]), float(given[1])
    if not all(math.isfinite(x) for x in (a, b, theta, quadrilateral)) or min(a, b) <= 0 or not 0 < theta < 180:
        raise ValueError('Invalid triangle measurements')
    outer = a*b*math.sin(math.radians(theta))/2
    raw = outer-quadrilateral
    expected = math.floor(raw+.5)
    if not 0 < quadrilateral < outer:
        raise ValueError('Invalid area relationship')
    if keys[0] != expected:
        raise ValueError('The answer does not match the displayed measurements')
    return {'sides': sides, 'angle': theta, 'given': quadrilateral,
            'outer': outer, 'raw': raw, 'answer': expected, 'values': values}


def validate_delivery_batch(records, kp_id):
    if int(kp_id) != KP:
        return
    for record in records:
        inspect_record(record)
