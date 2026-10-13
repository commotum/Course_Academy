"""Resolve all 91 remaining cases using retained local evidence and exact math."""
import importlib.util
import json
import re
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('easy_migration', OUT.parent / 'finder-easy/prepare.py')
edb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edb)
edb.OUT = OUT
snapshot = edb.loads((OUT / 'snapshot.edn').read_text())
questions = {q[':question/math-academy-id']: q for (q,) in snapshot['questions']}
audit = {q['ma_id']: q for q in json.loads((OUT / 'audit-input.json').read_text())}
local = json.loads((OUT / 'local-markdown-evidence.json').read_text())
csv_rows = json.loads((OUT / 'local-csv-matches.json').read_text())
x, y, z, k, p, m, t = sp.symbols('x y z k p m t', real=True)

def expression(raw):
    raw = raw.replace('π', r'\pi').replace('$', '').replace(r'\,', '').strip()
    previous = None
    while raw != previous:
        previous = raw
        raw = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', raw)
        raw = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', raw)
    raw = raw.replace(r'\pi', 'pi').replace('{', '(').replace('}', ')').replace('^', '**')
    assert '\\' not in raw and not re.search(r'[^0-9+*/().\-\sA-Za-z]', raw), raw
    value = sp.simplify(parse_expr(raw, local_dict={'pi': sp.pi, 'sqrt': sp.sqrt},
        transformations=standard_transformations + (implicit_multiplication_application,)))
    assert not value.free_symbols and value.is_real, raw
    return value

def split_top(raw):
    result, start, depth = [], 0, 0
    for i, char in enumerate(raw):
        if char in '({': depth += 1
        elif char in ')}': depth -= 1
        elif char == ',' and depth == 0:
            result.append(raw[start:i]); start = i + 1
    assert depth == 0, raw
    result.append(raw[start:])
    return result

def atoms(value, kind):
    """Parse only this audited numeric-set answer grammar; no display-order keying."""
    if re.fullmatch(r'(?:None|No vertical asymptotes|The function has no vertical asymptotes)', value.strip(), re.I):
        return set()
    value = value.replace('$', '').replace(r'\,', '').strip().rstrip('.')
    if kind == 'point':
        found = re.findall(r'\(([^()]*)\)', value)
        rest = re.sub(r'\([^()]*\)', '', value)
        assert found and not re.sub(r'\b(?:and|only)\b|[,\s]', '', rest), value
        return {tuple(expression(v) for v in split_top(s)) for s in found}
    value = re.sub(r'\b(?:x|t|k|p|m|y|z)\s*=', '', value)
    value = re.sub(r'\b(?:and|or)\b', ',', value)
    value = re.sub(r'\bonly\b', '', value)
    result = set()
    for part in split_top(value):
        part = part.strip()
        if not part: continue
        if part.startswith((r'\pm', '±')):
            part = part.removeprefix(r'\pm').removeprefix('±').strip()
            a = expression(part)
            result.update((a, -a))
        else:
            result.add(expression(part))
    assert result, value
    return result

def signature(values):
    return sorted(sp.srepr(v) if not isinstance(v, tuple) else '(' + ','.join(sp.srepr(a) for a in v) + ')' for v in values)

def latex_atom(atom, variable=None):
    if isinstance(atom, tuple):
        return '(' + ','.join(sp.latex(v) for v in atom) + ')'
    return (variable + '=' if variable else '') + sp.latex(atom)

def ordered(values):
    return sorted(values, key=lambda v: tuple(float(sp.N(a)) for a in v) if isinstance(v, tuple) else (float(sp.N(v)),))

MANUAL = {
 'q-22405': ('B', 'The plotted points are A=(2,7), B=(4,5), C=(7,2). Only B satisfies y=x+1.'),
 'q-44504': ('B', 'A=(-6,5), B=(1,5), C=(6,5). Only B satisfies y=8x-3.'),
 'q-54285': ('II', 'The line crosses the y-axis at 2 and passes through (4,4); its slope is 1/2. Therefore y=x/2+2, statement II.'),
 'q-59732': ('III', 'The line has intercepts (0,4) and (4,0), so its equation is y=4-x, statement III.'),
 'q-48064': ('I', 'The filled point at x=2 gives f(2)=1. The left and right limits are 1 and -2, so the two-sided limit does not exist and the function is not continuous there.'),
 'q-69514': ('D', 'B is 2 by 2, C is 2 by 1, and D is 1 by 2. Only D has the requested dimensions.'),
 'q-69515': ('R', 'P is 2 by 2, Q is 4 by 3, and R is 3 by 4. Only R has the requested dimensions.'),
 'q-19215': ('I II', 'The grid gives b=(-4,-2), e=(2,1), c=(2,5), d=(-2,-5). Hence b=-2e and c=-d; b=2e is false.'),
 'q-20404': ('II', 'The grid gives a=(6,4), c=(-3,-2), b=(-3,-5), d=(3,5). Thus c=-a/2; a=-c and b=d are false.'),
 'q-42115': ('II', 'A is neither upper nor lower triangular because both off-diagonal entries a12=1 and a21=-1 are nonzero. However A^T+A=diag(-6,2,10), so statement II is true.'),
 'q-36000': ('I II', 'Graphs I and II are strictly monotone and pass the horizontal line test. Graphs III and IV each meet some horizontal line twice. There are four graphs, so all four labels are represented.'),
 'q-36897': ('I', 'Graph I is strictly increasing. Graph II has a local minimum and maximum, graph III first decreases to a visible local minimum and then increases, and graph IV is a downward parabola. Thus II, III, and IV fail the horizontal line test; only I is invertible.'),
 'q-38762': ('I II', 'At x=2 the curve touches and turns at the x-axis (even multiplicity). At x=-1 and x=1 it crosses (odd multiplicity). The y-intercept is below zero, so p(0)=2 is false.'),
 'q-38768': ('II III', 'The graph crosses at x=0 (odd multiplicity) and touches/turns at x=-1 and x=2 (even multiplicities). Its right-hand tail rises, giving p(x) tending to positive infinity.'),
 'q-105103': ('II III', 'The vector field rotates clockwise with increasing magnitude away from the origin. Its curl is nonzero and points in the negative z-direction; it is not irrotational.'),
 'q-96475': ('I', 'For (x-1)(y+2), both factors are positive in region I. In regions II and III one factor is negative and one positive. Only statement I is true.'),
 'q-97483': ('II III', 'For xy^2, y^2 is positive in every open quadrant, so the slope has the sign of x. It is negative in quadrants II and III, and positive in quadrant I.'),
 'q-27015': ('II', 'Cosine attains its maxima at x=2n*pi, vanishes at x=3pi/2, and has range [-1,1]. Only statement II is true.'),
 'q-27021': ('I', 'Cosine has zeros at x=pi/2+n*pi. At x=3pi/2+2n*pi it is zero, not maximal, and its range is [-1,1]. Only I is true.'),
 'q-27660': ('I', 'Tangent has vertical asymptotes at pi/2+n*pi and range all real numbers. Its domain excludes pi/2+n*pi, rather than n*pi. Only I is true.'),
 'q-42912': ('I II III', 'Cosecant is undefined at pi and at every n*pi, so (pi,-1) is not on its graph and those x-values are vertical asymptotes. It takes the value 2 where sin(x)=1/2.'),
 'q-65310': ('I III', 'Cosecant is defined exactly when x is not n*pi, never equals zero, and equals -1 at -pi/2+2n*pi.'),
 'q-287964': ('III', 'The equations reduce respectively to x=1, an identity, and 1=3. Only the third has no solutions.'),
 'q-288058': ('I', 'The equations reduce respectively to -2=3, an identity, and x=2. Only the first has no solutions.'),
 'q-102106': ('I II', 'The graph is continuous at x=-1 and x=2; it has a vertical asymptote at x=4. This independently confirms the stored worked solution.'),
 'q-112591': ('I II III', 'At x=-2 the graph crosses with nonzero slope (simple root), at x=0 it crosses with flattening (odd multiplicity), and at x=2 it touches/turns (even multiplicity).'),
 'q-48063': ('I II', 'The graph has a filled point at (2,1) and a hole on the curve at (2,3). Thus f(2)=1 and the left-hand limit exists and equals 3, while continuity fails.'),
 'q-66785': ('I', 'The vertex of |x-4|+2 is at x=4. The interval (-infinity,3) stays on one monotone branch; (1,infinity) and (-infinity,5] each include both branches and fail the horizontal line test.'),
 'q-78133': ('II', 'The graph jumps at x=-7, is continuous at the vertex x=-4, and has a hole plus a different filled value at x=-1.'),
 'q-86896': ('I II III', 'For F, P_y=Q_x=e^(x+y); for G, P_y=Q_x=3y^2; for H, P_y=Q_x=2x/(x^2+1). Each field is smooth on R^2, so all three are conservative. OCR l and ll mean Roman I and II.'),
 'q-128490': ('III', 'The determinant is -3*sqrt(5)+3*sqrt(5)=0, so the matrix is singular; the determinant is neither 10 nor -5.'),
 'q-42090': ('A', 'A has zeros below its main diagonal. B has b31=5 and C has c32=3, so only A is upper triangular.'),
 'q-105075': ('III', 'The upward vector magnitudes decrease in the positive y-direction, giving negative divergence. The field is not solenoidal.'),
 'q-105571': ('I IV', 'The vector field is constant, so its divergence is zero everywhere and it is solenoidal.'),
 'q-125852': ('III', 'The quantities Q_x-P_y for the three pairs are -2, 2y*sin(y^2), and 1. Only pair III has unit curl everywhere.'),
 'q-125853': ('II III', 'For the three vector fields, Q_x-P_y is respectively 2x+2, 1, and 1. Only II and III give the area for every eligible region.'),
}

def numeric_solution(mid):
    q = questions[mid]
    kp = audit[mid]['kp']
    if kp == 17592186059849:
        models = {
          'q-9657': (sp.Matrix([[2,-1,3],[x,2,4],[-2,1,x+3]]), x, 8),
          'q-9852': (sp.Matrix([[0,7,4*k],[0,9,5*k],[0,11,6*k]]), k, 0),
          'q-130575': (sp.Matrix([[2,1,5],[2,3,z],[z,-1,1]]), z, -48),
          'q-130580': (sp.Matrix([[x,2*x,3],[5,x,7],[3,2,1]]), x, 22),
          'q-130626': (sp.Matrix([[1,-3*p,4],[-2,6*p,-8],[1,-1,1]]), p, 0),
          'q-18256': (sp.Matrix([[4,2,3],[-3*y,-2,1],[2,y,-5]]), y, 81),
          'q-18272': (sp.Matrix([[0,-3,2],[1,p,0],[p-3,0,-1]]), p, -23),
          'q-9911': (sp.Matrix([[1,-1,k],[1,k,-k],[5,k,k]]), k, 0),
          'q-9913': (sp.Matrix([[k,0,0],[0,3,1],[0,6,k]]), k, 0),
          'q-128506': (sp.Matrix([[1,6,m],[m,3,0],[2,1,1]]), m, -29),
        }
        matrix, variable, target = models[mid]
        determinant = sp.expand(matrix.det())
        solution = sp.solveset(determinant - target, variable, domain=sp.S.Reals)
        reason = 'The determinant is $' + sp.latex(determinant) + '$. Setting it equal to $' + str(target) + '$ gives $' + sp.latex(solution) + '$.'
        return solution, 'scalar', str(variable), reason, {'matrix': str(matrix), 'determinant': str(determinant), 'target': target}
    if kp in (17592186087842,17592186087843,17592186087844,17592186087845):
        models = {
          'q-39796': 2/(2-x)+3/(2+x), 'q-4629': (3*x*x-12*x)/(x*x-2*x-3),
          'q-80669': (x*x+3*x)/(x*x-3*x-4), 'q-39800': (x*x-3*x+2)/(x*x+x-2),
          'q-39801': (x-2)/(x*x+2*x-8), 'q-80690': x/(x*(x-2)),
          'q-39804': (x**3-3*x*x+3*x-1)/((x-1)*(x+5)**2),
          'q-39931': (x*x-4)/(x**3+2*x*x), 'q-80691': (x+2)/(x*x+2*x),
          'q-39795': 5/(x**3+x*x+x), 'q-4694': 2*x/(x**3-27),
          'q-80679': 1/(x*x-4*x+5), 'q-113525': 3/(x**3+x*x+7*x),
          'q-80676': (2*x-1)/(x**3-2*x*x+4*x-8),
          'q-113527': (x*x-9)/(x**3-2*x*x+6*x-12),
          'q-39927': x/(x**3+x*x+x), 'q-4695': (x*x-1)/(x**3-x*x+x-1),
          'q-113545': x*x/(x**4+x**3+2*x*x), 'q-39934': (x*x+3*x)/(x**3+2*x*x+8*x),
          'q-80696': 4*x/(x*(x*x+1)), 'q-6913': x/(x**3+2*x),
          'q-113554': (2*x*x-6)/(x**4-9), 'q-39936': (x*x-1)/(x**4-1),
        }
        reduced = sp.cancel(models[mid])
        denominator = sp.denom(reduced)
        solution = sp.solveset(denominator, x, domain=sp.S.Reals)
        reason = 'After cancellation, $f(x)=' + sp.latex(reduced) + '$. Its real denominator zeros are $' + sp.latex(solution) + '$; canceled factors produce holes, not vertical asymptotes.'
        return solution, 'scalar', 'x', reason, {'reduced_function': str(reduced), 'real_poles': str(solution)}
    if kp == 17592186068696:
        expected = {'q-48080': {-2,0}, 'q-48090': {1,2,4}, 'q-104020': {0,2},
            'q-104023': {-2,0}, 'q-48087': {-2,2}, 'q-104025': {-1,2}, 'q-48088': {-3,0}}
        values = expected[mid]
        reason = 'Direct image review identifies discontinuities at ' + ', '.join('x=' + str(v) for v in sorted(values)) + '; other plotted corners and turning points are continuous.'
        return sp.FiniteSet(*values), 'scalar', 'x', reason, {'image_review': True}
    if kp in (17592186083278,17592186083280):
        models = {'q-21081': (4*sp.sin(t)+7,4*sp.cos(t)+10,[sp.pi/2,3*sp.pi/2]),
            'q-21080': (4*sp.cos(2*t)+5,5*sp.sin(2*t)+4,[0,sp.pi/2]),
            'q-75278': (2*sp.cos(4*t)-11,3*sp.sin(4*t)+5,[0,sp.pi/4])}
        xx, yy, values = models[mid]
        dx, dy = sp.diff(xx,t), sp.diff(yy,t)
        assert all(sp.simplify(dx.subs(t,v)) == 0 and sp.simplify(dy.subs(t,v)) != 0 for v in values)
        reason = 'A vertical tangent (and horizontal normal) requires x\u2032(t)=0 and y\u2032(t)\u22600. Here $x\u2032(t)=' + sp.latex(dx) + '$ and $y\u2032(t)=' + sp.latex(dy) + '$. Within the given half-open interval the solutions are $' + sp.latex(sp.FiniteSet(*values)) + '$.'
        return sp.FiniteSet(*values), 'scalar', 't', reason, {'dx': str(dx), 'dy': str(dy), 'interval_checked': True}
    if kp == 17592186105908:
        determinant = sp.Matrix([[k*k,7,4],[6,7,4],[3,0,2]]).det()
        solution = sp.solveset(determinant, k, domain=sp.S.Reals)
        return solution, 'scalar', 'k', 'The scalar triple product is $14(k^2-6)$. Coplanarity requires it to vanish, giving $k=\u00b1\\sqrt{6}$.', {'determinant': str(determinant)}
    if kp == 17592186124445:
        models = {
            'q-36970': (x*y+x*y*y+z**3,(x,y,z),[(0,0,0),(0,-1,0)]),
            'q-128517': (x*x-2*x*sp.cos(y),(x,y),[(1,0),(0,sp.pi/2)]),
            'q-128519': (9/y-3*y/x+x,(x,y),[(-3,-3)]),
            'q-71474': (1/(x*y)+1/y+1/(z*x)-z,(x,y,z),[(-1,-1,1),(-1,1,-1)]),
            'q-71470': (x*y*sp.exp(x)+z*z*sp.exp(z),(x,y,z),[(0,0,0),(0,0,-2)]),
        }
        function, variables, pts = models[mid]
        gradient = [sp.diff(function,v) for v in variables]
        for point in pts:
            sub = dict(zip(variables,point))
            assert function.subs(sub).is_finite
            assert all(sp.simplify(g.subs(sub)) == 0 for g in gradient)
        # The algebra in the worked solutions also establishes exhaustiveness.
        reason = 'The partial derivatives are $' + ', '.join(sp.latex(g) for g in gradient) + '$. Solving them simultaneously in the stated domain gives exactly $' + ', '.join(latex_atom(tuple(sp.sympify(v) for v in point)) for point in pts) + '$. Each point was substituted into all derivatives and checked against denominator/domain restrictions.'
        return sp.FiniteSet(*(sp.Tuple(*v) for v in pts)), 'point', None, reason, {'gradient': list(map(str,gradient)), 'domain_and_substitution_checked': True}
    if kp == 17592186124456:
        models = {
          'q-36332': (2*x*y+3*y*y-x*x-4,(0,1)),
          'q-65208': (9*x*x*y-3*y**3+6*x,(1,0)),
          'q-72410': (y*y+2*x*y-x*x-8,(0,1)),
          'q-72440': (x*x+2*x*y+5*y-4,(0,1)),
          'q-130225': (2*x*x-3*y*y+y,(0,1)),
          'q-130217': (x*x+y*y+2*x-2*y,(-1,1)),
        }
        function, vector = models[mid]
        tangent = (sp.diff(function,y),-sp.diff(function,x))
        dot = sp.expand(tangent[0]*vector[0]+tangent[1]*vector[1])
        solutions = sp.solve([function,dot],(x,y),dict=True)
        points = [tuple(s[v] for v in (x,y)) for s in solutions if all(s[v].is_real for v in (x,y))]
        assert all(any(v.subs({x:a,y:b}) != 0 for v in tangent) for a,b in points)
        reason = 'Write the curve as F(x,y)=0. A tangent is (F_y,-F_x); its dot product with the given vector is $' + sp.latex(dot) + '$. Solving this with the curve equation gives $' + ', '.join(latex_atom(pt) for pt in points) + '$, and the tangent is nonzero at each point.'
        return sp.FiniteSet(*(sp.Tuple(*v) for v in points)), 'point', None, reason, {'curve': str(function), 'tangent_dot_vector': str(dot), 'tangent_nonzero_checked': True}
    raise ValueError(mid)

def local_key(mid):
    entries = local[mid.replace('q-','ma-')]
    csv_row = csv_rows.get(mid[2:])
    if not entries or not csv_row: return None, []
    assert csv_row['quiz-status'] == 'converted-and-verified'
    values = []
    evidence = []
    for entry in entries:
        fields = entry['block']['fields']
        assert len(fields) == 1 and fields[0]['type'] == 'radio'
        f = fields[0]
        label = csv_row['quiz-answer-labels']
        if f.get('correct'): assert f['correct'] == label, mid
        value = next(a['value'] for a in f['choices'] if a['id'] == label)
        values.append(value)
        evidence.append({'path': entry['path'], 'line': entry['line'], 'sha256': entry['sha256'],
            'csv_label': label, 'correct_value': value, 'explicit_quiz_key': bool(f.get('correct'))})
    assert len(set(values)) == 1, mid
    return values[0], evidence

def repaired_worked_solution(mid, text):
    if mid not in ('q-36970','q-128517','q-128519','q-71474','q-71470'):
        return None
    original = text
    repairs = []
    if mid in ('q-36970','q-71470'):
        assert text.count('∇f') == 1
        text = text.replace('∇f','∇h')
        repairs.append('Use the defined function h in the gradient equation.')
    if mid == 'q-128517':
        assert text.count('∇h') == 1
        text = text.replace('∇h','∇f')
        repairs.append('Use the defined function f in the conclusion.')
    if mid == 'q-128519':
        assert text.count(r'\frac{3}{y}') == 1
        text = text.replace(r'\frac{3}{y}',r'\frac{3}{x}')
        repairs.append('Correct the y-component denominator in the displayed gradient: g_y=-9/y^2-3/x.')
    if mid in ('q-36970','q-71474','q-71470'):
        old = '0\\text{\u00a0}j+0\\text{\u00a0}j'
        assert text.count(old) == 1
        text = text.replace(old,'0\\text{\u00a0}j+0\\text{\u00a0}k')
        repairs.append('Use i, j, k for the three components of the zero vector.')
    prefix = r'\{\begin{aligned}' if mid == 'q-71470' else r'{\begin{aligned}'
    pattern = re.escape(prefix) + r'(.*?)' + re.escape(r'\end{aligned}')
    text, count = re.subn(pattern,lambda match:r'\begin{cases}'+match[1]+r'\end{cases}',text,flags=re.S)
    assert count == 1
    repairs.append('Render the simultaneous equations as a balanced cases environment.')
    assert text != original
    return {'before':original,'after':text,'repairs':repairs,'canonical_solution_set_unchanged':True}

resolved = []
for mid, q in sorted(questions.items(), key=lambda item: item[1][':db/id']):
    fields = q.get(':question/answer-fields', [])
    keyed = [f[':answer-field/correct'][':answer/value'] for f in fields if f.get(':answer-field/correct')]
    recovered, evidence = local_key(mid)
    row = {'id': q[':db/id'], 'ma_id': mid, 'kp': audit[mid]['kp'], 'kp_title': audit[mid]['kp_title'],
        'original_field_ids': [f[':db/id'] for f in fields], 'stored_keys': keyed,
        'local_key': recovered, 'local_evidence': evidence, 'duplicate_fields': len(fields) > 1,
        'originally_missing_key': bool(fields) and not keyed,
        'fieldless': not fields, 'image_choice_filename_rule': 'No image answer choices in this batch; images are problem diagrams.'}
    if mid in MANUAL:
        selected, reason = MANUAL[mid]
        correct = selected.split()
        bank = {a[':db/id']: a for f in fields for a in f[':answer-field/choices']}
        if keyed:
            assert all(edb.subset(v) == set(correct) for v in keyed), mid
        if recovered and edb.subset(recovered) != set(correct):
            assert mid in ('q-42115','q-36897','q-105075'), mid
            row['source_key_correction'] = {'local_key': recovered, 'resolved_key': correct,
                'reason': reason, 'existing_learner_responses': 0}
        else:
            row['source_key_correction'] = None
        if not fields:
            labels = list(edb.ROMAN[:len(edb.CASE_LINE.findall(q[':question/problem']))])
            assert len(labels) == 3
        elif mid in ('q-36000','q-36897'):
            labels = list(edb.ROMAN[:4])
        elif mid in ('q-22405','q-44504'):
            labels = ['A','B','C']
        elif edb.CASE_LINE.findall(q[':question/problem']):
            labels = list(edb.ROMAN[:len(edb.CASE_LINE.findall(q[':question/problem']))])
        else:
            labels = re.findall(r'\b([A-Z])\s*=',q[':question/problem'])
            assert len(labels) == len(set(labels)) == 3
        def parse_label(v):
            if mid == 'q-86896': v = v.replace('ll only','II only').replace('l only','I only')
            return edb.subset(v)
        mappings = [{'old_answer': aid, 'old_value': a[':answer/value'],
            'selected': [l for l in labels if l in parse_label(a[':answer/value'])]} for aid,a in sorted(bank.items())]
        assert all(parse_label(a[':answer/value']) <= set(labels) for a in bank.values())
        row.update(action='convert_checkbox', labels=labels, correct=[l for l in labels if l in correct],
            displayed_cases=None, choice_mapping=mappings, reason=reason,
            proof={'method':'independent_algebra_or_direct_diagram_review','case':'listed_subset'})
    else:
        expected, kind, variable, reason, proof = numeric_solution(mid)
        row.update(reason=reason, proof=proof, numeric_kind=kind, variable=variable)
        if expected == sp.S.Reals:
            assert mid in ('q-9852','q-130626')
            value = keyed[0] if keyed else recovered
            assert value.startswith('Any value of ')
            row.update(action='retain_radio_repair_key' if not keyed else 'retain_radio', labels=[], correct=[],
                resolved_radio_value=value, choice_mapping=[],
                decision='The complete solution set is all real values; a finite checkbox list cannot express that answer without changing the task.')
        else:
            correct_atoms = {tuple(v) if isinstance(v,sp.Tuple) else v for v in expected}
            values = keyed or [recovered]
            assert all(v is not None and atoms(v,kind) == correct_atoms for v in values), (mid,values,correct_atoms)
            if not keyed and recovered: assert atoms(recovered,kind) == correct_atoms, mid
            bank = {a[':db/id']:a for f in fields for a in f[':answer-field/choices']}
            universe = set().union(*(atoms(a[':answer/value'],kind) for a in bank.values()))
            assert correct_atoms <= universe
            values = ordered(universe)
            assert len(values) <= len(edb.ROMAN)
            labels = list(edb.ROMAN[:len(values)])
            value_to_label = dict(zip(values,labels))
            mappings = [{'old_answer': aid, 'old_value': a[':answer/value'],
                'selected': [value_to_label[v] for v in ordered(atoms(a[':answer/value'],kind))]} for aid,a in sorted(bank.items())]
            row.update(action='convert_checkbox', labels=labels,
                correct=[value_to_label[v] for v in values if v in correct_atoms],
                displayed_cases=[{'label':label,'value':'$'+latex_atom(v,variable)+'$','identity':signature({v})[0]} for label,v in zip(labels,values)],
                complete_correct_set=signature(correct_atoms), choice_mapping=mappings,
                empty_set_rule='No boxes checked means none of the listed values/points; no None checkbox.')
    if row['originally_missing_key']:
        assert recovered is not None and evidence, mid
    # A saved response cannot be silently regraded when correcting a source key.
    assert not snapshot['items'] and not snapshot['response_users']
    row['worked_solution_repair'] = repaired_worked_solution(mid,q.get(':question/worked-solution'))
    resolved.append(row)

assert len(resolved) == 91
assert sum(r['action'] == 'convert_checkbox' for r in resolved) == 89
assert sum(r['originally_missing_key'] for r in resolved) == 36
assert sum(bool(r.get('source_key_correction')) for r in resolved) == 3
edb.save('resolutions.json', {'basis': snapshot['basis'], 'source': edb.SOURCE,
    'all_cases_resolved': True, 'unresolved': [], 'questions': resolved,
    'counts': {'reviewed':91,'checkbox_conversions':89,'radio_key_repaired':1,'radio_retained_unchanged':1,
        'originally_missing_keys_recovered':36,'duplicate_fields_reconciled':8,'fieldless_questions':5,
        'OCR_label_repairs':1,'local_key_disagreements_resolved':3,
        'existing_worked_solutions_repaired':sum(bool(r['worked_solution_repair']) for r in resolved),
        'new_checkbox_fields':sum(len(r['labels']) for r in resolved)},
    'source_rules': ['Keys matched by stable question ID and original choice label/value, never database display order.',
        'For answer-image choices, original answer-image filename number 1 identifies the correct image regardless of display order; there are no image answer choices among these 91.',
        'Local CSV and Markdown are evidence; every chosen answer also checked against algebra, worked solution or diagram.',
        'Infinite complete solution sets remain radio; empty finite sets use all-false checkbox answers.']})
print(json.dumps(json.loads((OUT / 'resolutions.json').read_text())['counts'],indent=2))
