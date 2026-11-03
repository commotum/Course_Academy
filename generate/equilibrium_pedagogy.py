"""Delivery checks for independent equilibrium-identification practice."""
import re
import sympy as S
from scripts.question_capture.math_format import normalize_prose

KP = 17592186166788


def validate_delivery_batch(records, kp_id):
    if int(kp_id) != KP:
        return
    y = S.Symbol('y', real=True)
    for record in records:
        q = record['question']
        prompt, solution = q[':question/problem'], q[':question/worked-solution']
        if re.search(r'constant function|derivative (?:is |to )?zero|set.*(?:dy|derivative)|hint', prompt, re.I):
            raise ValueError('Equilibrium practice must leave the equilibrium criterion to the learner')
        if 'L(c)' in solution or 'R(c)' in solution:
            raise ValueError('Use one residual throughout the equilibrium solution')
        g = record.get('generation', {})
        if not g.get('printed_residual'):
            raise ValueError('Equilibrium delivery requires a visible, unexpanded residual and candidate checks')
        equation = g['original_equation']
        read = lambda text: S.sympify(text, locals={'y': y}, evaluate=False)
        lhs, rhs = read(equation['lhs']), read(equation['rhs'])
        residual = rhs if lhs == 0 else rhs-lhs
        # A side added as an unevaluated term on the other side is the old
        # artificial difficulty wrapper. Real rearrangement moves existing terms.
        left_terms = lhs.args if lhs.is_Add else (lhs,)
        if lhs != 0 and rhs.is_Add and all(any(S.simplify(term-left) == 0 for term in rhs.args)
                                          for left in left_terms):
            raise ValueError('Do not add a cancelling copy of the left side to manufacture difficulty')
        expected = S.latex(residual, ln_notation=True, order='lex').replace('y', 'c')
        # Compare normalized display text: the normalizer may escape inline TeX.
        visible = normalize_prose('$$\nf(c)='+expected+'=0.\n$$')
        if visible not in solution:
            raise ValueError('The solution must retain the useful residual structure before substitution')
        # Derive the original domain from the actual expression, before cancellation.
        domain = []
        for expr in (lhs, rhs):
            domain += [('positive', f.args[0]) for f in expr.atoms(S.log)]
            domain += [('nonzero', p.base) for p in expr.atoms(S.Pow) if p.exp.is_negative]
        candidates = [read(c) for c in g['parameters']['candidates']]
        fields = q[':question/answer-fields']
        if len(candidates) != len(fields) or len(set(candidates)) != len(candidates):
            raise ValueError('Equilibrium candidates must be distinct and match their fields')
        states = []
        for c, field in zip(candidates, fields):
            valid = all(bool(S.simplify(expr.subs(y, c)) > 0) if kind == 'positive'
                        else S.simplify(expr.subs(y, c)) != 0 for kind, expr in domain)
            truth = valid and S.simplify(residual.subs(y, c)) == 0
            choices = {str(a[':answer/id']): a[':answer/value'] for a in field[':answer-field/choices']}
            correct = field[':answer-field/correct']
            correct = correct[-1] if isinstance(correct, list) else correct
            if choices[str(correct)] != str(truth).lower():
                raise ValueError('Equilibrium key disagrees with the original equation or domain')
            label = normalize_prose('$y='+S.latex(c, ln_notation=True, order='lex')+'$')
            if field[':answer-field/key'] != label:
                raise ValueError('Equilibrium candidate label disagrees with its mathematical value')
            states.append((valid, truth))
        if not any(truth for _, truth in states) or all(truth for _, truth in states):
            raise ValueError('Equilibrium banks need correct and incorrect candidates')
        if str(q[':question/difficulty']).endswith('/hard'):
            if not any(not valid for valid, _ in states) or not any(valid and not truth for valid, truth in states):
                raise ValueError('Hard equilibrium practice must test both domain and a valid non-equilibrium candidate')
