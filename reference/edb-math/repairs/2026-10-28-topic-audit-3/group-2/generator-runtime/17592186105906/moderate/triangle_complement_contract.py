"""Check the displayed two-step task, independently of generation metadata."""
import math
import re

KP = 17592186105906
CONTRACT = 'triangle-complement-full-calculation-v1'


def inspect_record(record):
    q = record['question']
    prompt, solution = q[':question/problem'], q[':question/worked-solution']
    level = q[':question/difficulty'].rsplit('/', 1)[-1]
    sides = [float(x) for x in re.findall(r'\$[A-D]{2}=([\d.]+)', prompt)]
    angle = re.search(r'meet at \$(\d+)\^\\circ\$', prompt)
    given = re.search(r'area of the quadrilateral \$[A-D]{4}\$ is \$([\d.]+)', prompt)
    if len(sides) != 2 or not angle or not given:
        raise ValueError('Both sides, their included angle and the quadrilateral area must be supplied')
    if any(x in prompt.lower() for x in ('hint', 'first use', 'then subtract', 'enclosing', 'perpendicular')):
        raise ValueError('The prompt must leave the triangle calculation and area relationship to the learner')
    a, b = sides
    theta, quadrilateral = int(angle[1]), float(given[1])
    if not 35 <= theta <= 120 or theta == 90 or max(a,b)/min(a,b) > 3:
        raise ValueError('Preserve the nonright-angle sine calculation and readable geometry')
    if level == 'easy':
        valid = a.is_integer() and b.is_integer() and any(x in (2,4) and 4 <= y <= 10 for x,y in ((a,b),(b,a)))
    elif level == 'moderate':
        valid = a in (5,7,9,11) and b in (5,7,9,11)
    elif level == 'hard':
        valid = any(x in (2.5,3.5,4.5,5.5,6.5) and y in (5,7,9) for x,y in ((a,b),(b,a)))
    else:
        valid = False
    if not valid:
        raise ValueError('Measurements do not match the modest authored numerical progression')
    outer = a*b*math.sin(math.radians(theta))/2
    raw = outer-quadrilateral
    expected = math.floor(raw+.5)
    if not 0 < quadrilateral < outer or raw < 2 or abs(raw%1-.5) < .08:
        raise ValueError('Invalid area relationship or incidental rounding boundary')
    if 'nearest integer' not in prompt or not q.get(':question/requires-calculator'):
        raise ValueError('Use the same calculator and rounding conventions in every band')
    if not all(x in solution for x in (r'\frac12', r'\sin', 'Subtract the quadrilateral area', 'Keep full precision')):
        raise ValueError('The worked solution must explain both calculations and final-only rounding')
    f = q[':question/answer-fields'][0]
    correct = f[':answer-field/correct'][1]
    choices = f[':answer-field/choices']
    values = [float(re.match(r'^(-?\d+(?:\.\d+)?)', a[':answer/value'])[1]) for a in choices]
    key = next(v for a,v in zip(choices,values) if a[':answer/id'] == correct)
    if key != expected or values.count(expected) != 1:
        raise ValueError('The answer does not match the displayed measurements')
    if len(values)>1 and (len(values)!=5 or min(values)<=0 or min(abs(x-y) for i,x in enumerate(values) for y in values[i+1:])<2):
        raise ValueError('Rounded choices must be distinct and separated')
    return {'sides':sides,'angle':theta,'given':quadrilateral,'outer':outer,'raw':raw,'answer':expected,'values':values}


def validate_delivery_batch(records, kp_id):
    if int(kp_id) != KP:
        return
    for record in records:
        inspect_record(record)
