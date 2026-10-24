"""Role-based linear inverse-trigonometric integration generators.

The four entrypoints share mathematics, not source-number replacements. Bands
describe operations; imported ratings are evidence rather than sampling rules.
Every normal bank is an explicitly authored complete error-recipe profile.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid

import sympy as sp

X, U = sp.symbols('x u', real=True)
VERSION = 'inverse-trig-role-bands-1'
LEVELS = ('easy', 'moderate', 'hard')
RADICALS = (2, 3, 5, 6, 7, 10)
CASES = {
    'sine': {'easy': ('integer-inner', 'radical-inner'),
             'moderate': ('unit-numerator', 'integer-numerator', 'fractional-numerator'),
             'hard': ('combined-integer-numerator', 'combined-fractional-numerator')},
    'tangent': {'easy': ('integer-inner', 'radical-inner'),
                'moderate': ('unit-numerator', 'cancelling-numerator', 'independent-numerator'),
                'hard': ('combined-integer-ratio', 'combined-radical-ratio')},
    'secant': {'easy': ('matching-differential',),
               'moderate': ('unit-numerator', 'integer-result', 'fractional-result'),
               'hard': ('integer-normalization', 'radical-normalization', 'denominator-normalization')},
    'definite': {'easy': ('sine-special', 'tangent-special', 'tangent-general'),
                 'moderate': ('sine-square', 'sine-radical', 'sine-symmetric', 'tangent-square', 'tangent-radical'),
                 'hard': ('sine-two-positive', 'sine-cross-zero', 'tangent-two-positive', 'tangent-cross-zero')},
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def tex(value):
    return (sp.latex(sp.sympify(value)).replace(r'\operatorname{asin}', r'\operatorname{arcsin}')
            .replace(r'\operatorname{atan}', r'\operatorname{arctan}')
            .replace(r'\operatorname{asec}', r'\operatorname{arcsec}'))


def display(value):
    return '$$\n' + value + '\n$$'


def aligned(rows):
    # All rows use the same empty first column. Keeping the original integral
    # above its first equality avoids reserving its width beside every RHS.
    return display(r'\begin{aligned}& ' + rows[0] + r' \\ ' + r' \\ '.join(' &= ' + row for row in rows[1:]) + r'\end{aligned}')


def integral(body, variable='x', lower=None, upper=None):
    bounds = '' if lower is None else '_{' + tex(lower) + '}^{' + tex(upper) + '}'
    return r'\int' + bounds + ' ' + body + r'\,\mathrm{d}' + variable


def function(family, argument):
    return getattr(sp, {'sine': 'asin', 'tangent': 'atan', 'secant': 'asec'}[family])(argument)


def task_key(body, lower=None, upper=None):
    """Ignore presentation, bands, banks, and seeds when counting new tasks."""
    return digest([sp.srepr(sp.simplify(body)), None if lower is None else sp.srepr(sp.simplify(lower)),
                   None if upper is None else sp.srepr(sp.simplify(upper))])


def ratio(rng, *, fractional=False):
    if not fractional:
        return sp.Integer(rng.randint(1, 9))
    while True:
        value = sp.Rational(rng.randint(1, 9), rng.randint(2, 5))
        if value.q != 1:
            return value


def sample(kind, band, case, rng):
    a = sp.Integer(rng.randint(2, 9))
    n = ratio(rng)
    b = sp.Integer(rng.choice(RADICALS))
    p = dict(family=kind, A=sp.Integer(1), B=a*a, N=n, D=sp.Integer(1), lower_u=None, upper_u=None)
    if kind in ('sine', 'tangent'):
        if band == 'easy':
            p['B'] = a*a if case == 'integer-inner' else b
            # Unit, cancelling, reciprocal, and independent numerators all remain
            # available. Cancellation belongs to the target substitution skill.
            if kind == 'sine' and case == 'integer-inner':
                p['N'] = rng.choice((sp.Integer(1), a, 1/a, n))
        elif band == 'moderate':
            p.update(A=a*a, B=sp.Integer(1))
            if case == 'unit-numerator': p['N'] = sp.Integer(1)
            elif case == 'integer-numerator': p['N'] = sp.Integer(rng.randint(2, 9))
            elif case == 'fractional-numerator': p['N'] = ratio(rng, fractional=True)
            elif case == 'cancelling-numerator': p['N'] = a
            elif case == 'independent-numerator':
                p['N'] = rng.choice([sp.Integer(v) for v in range(2, 10) if v != a])
        else:
            p.update(A=a*a, B=b)
            if case in ('combined-fractional-numerator',): p['N'] = ratio(rng, fractional=True)
            if case == 'combined-integer-ratio':
                p.update(A=sp.Integer(rng.randint(2, 7)), B=None)
                p['B'] = p['A']*a*a
    elif kind == 'secant':
        if band == 'easy': a = sp.Integer(rng.randint(2, 16))
        p.update(A=sp.Integer(1), B=a*a)
        if band == 'easy': p['N'] = a
        elif band == 'moderate':
            if case == 'unit-numerator': p['N'] = sp.Integer(1)
            elif case == 'integer-result': p['N'] = a*sp.Integer(rng.randint(2, 5))
            else: p['N'] = rng.choice([sp.Integer(v) for v in range(2, 10) if v % a])
        elif case == 'radical-normalization': p.update(B=b, N=n)
        elif case == 'denominator-normalization': p.update(N=sp.Integer(1), D=sp.Integer(rng.randint(2, 9)))
    else:
        fn = 'sine' if case.startswith('sine-') else 'tangent'
        p['family'] = fn
        if band == 'easy':
            p.update(A=sp.Integer(1), B=a*a, lower_u=sp.Integer(0))
            p['upper_u'] = sp.Rational(1, 2) if fn == 'sine' else (sp.Integer(1) if case == 'tangent-special' else rng.choice((sp.Integer(2), sp.Integer(3), sp.Rational(1, 2))))
        elif band == 'moderate':
            p.update(A=b if case.endswith('-radical') else a*a, B=sp.Integer(1), lower_u=sp.Integer(0))
            p['upper_u'] = rng.choice((sp.Rational(1, 2), sp.sqrt(2)/2, sp.sqrt(3)/2)) if fn == 'sine' else rng.choice((sp.Integer(1), sp.sqrt(3)/3, sp.sqrt(3)))
            if case == 'sine-symmetric': p.update(lower_u=-sp.Rational(1, 2), upper_u=sp.Rational(1, 2))
        else:
            p.update(A=a*a, B=b)
            if fn == 'sine':
                left, right = rng.choice(((sp.Rational(1, 2), sp.sqrt(2)/2), (sp.Rational(1, 2), sp.sqrt(3)/2)))
            else:
                left, right = rng.choice(((sp.sqrt(3)/3, sp.Integer(1)), (sp.Integer(1), sp.sqrt(3))))
            if case.endswith('cross-zero'): left = -left
            p.update(lower_u=left, upper_u=right)
    return p


def validate_parameters(kind, band, case, p):
    if kind not in CASES or band not in LEVELS or case not in CASES[kind][band]:
        raise ValueError('Unknown family or difficulty case')
    expected = {'family', 'A', 'B', 'N', 'D', 'lower_u', 'upper_u'}
    if set(p) != expected: raise ValueError('Expected mathematical role parameters')
    if p['family'] not in ('sine', 'tangent', 'secant'): raise ValueError('Unknown inverse function')
    if kind != 'definite' and p['family'] != kind: raise ValueError('Wrong inverse function for KP')
    for key in ('A', 'B', 'N', 'D'):
        if p[key].is_positive is not True or p[key].is_Rational is not True:
            raise ValueError('Positive exact rational coefficients required')
    A, B, N, D = (p[k] for k in ('A', 'B', 'N', 'D'))
    if A == B and kind != 'secant': raise ValueError('Unit substitution would remove the target work')
    if kind == 'secant' and not (A == 1 and B > 1): raise ValueError('Secant requires a nonunit real linear factor')
    if kind == 'definite':
        if p['family'] != ('sine' if case.startswith('sine-') else 'tangent'): raise ValueError('Case and inverse function disagree')
        lo, hi = p['lower_u'], p['upper_u']
        if lo is None or hi is None or (hi-lo).is_positive is not True: raise ValueError('Ordered real bounds required')
        if p['family'] == 'sine' and not (-1 < lo < hi < 1):
            raise ValueError('Arcsine bounds must stay strictly inside the real domain; no improper endpoints')
        if band == 'easy' and not (A == 1 and sp.sqrt(B).is_Integer and lo == 0):
            raise ValueError('Easy requires direct integer substitution and a zero lower endpoint')
        if band == 'moderate' and not (A > 1 and B == 1): raise ValueError('Moderate requires one normalization')
        if band == 'hard' and not (A > 1 and B > 1 and not sp.sqrt(B/A).is_Rational and lo != 0 and hi != 0 and abs(lo) != abs(hi)):
            raise ValueError('Hard requires combined normalization, an irrational factor, and two unlike nonzero endpoints')
    elif p['lower_u'] is not None or p['upper_u'] is not None:
        raise ValueError('Indefinite question cannot have bounds')
    elif kind in ('sine', 'tangent'):
        if band == 'easy' and A != 1: raise ValueError('Easy requires a unit constant')
        if band == 'moderate' and not (A > 1 and B == 1): raise ValueError('Moderate requires constant normalization')
        if band == 'hard' and not (A > 1 and B > 1): raise ValueError('Hard requires both nonunit coefficients')
        if band == 'hard':
            outer = N/(sp.sqrt(A) if kind == 'sine' else A)
            final = outer/sp.sqrt(B/A)
            if outer == 1 or final == 1: raise ValueError('Hard cannot cancel away a normalization or substitution factor')
        if kind == 'sine' and band == 'hard' and sp.sqrt(B).is_Rational:
            raise ValueError('Sine hard requires the additional radical substitution factor')
        if case == 'integer-inner' and not sp.sqrt(B).is_Integer: raise ValueError('Integer-factor case requires a square coefficient')
        if case == 'radical-inner' and sp.sqrt(B).is_Rational: raise ValueError('Radical-factor case requires a nonsquare coefficient')
        if case == 'unit-numerator' and N != 1: raise ValueError('Unit-numerator case requires numerator one')
        if case == 'integer-numerator' and not (N.is_Integer and N >= 2): raise ValueError('Independent integer numerator required')
        if case in ('fractional-numerator','combined-fractional-numerator') and N.q == 1: raise ValueError('Fractional numerator required')
        if case == 'cancelling-numerator' and N != sp.sqrt(A): raise ValueError('Matching cancellation required')
        if case == 'independent-numerator' and N == sp.sqrt(A): raise ValueError('Noncancelling numerator required')
        if case == 'combined-integer-ratio' and not sp.sqrt(B/A).is_Integer: raise ValueError('Integer ratio required')
        if case == 'combined-radical-ratio' and sp.sqrt(B/A).is_Rational: raise ValueError('Irrational ratio required')
    elif kind == 'secant':
        s = sp.sqrt(B)
        if band == 'easy' and not (N == s and D == 1 and s.is_Integer): raise ValueError('Easy requires a matching differential')
        if band == 'moderate' and not (s.is_Integer and N != s and D == 1): raise ValueError('Moderate requires a noncancelling visible factor')
        if band != 'hard' and D != 1: raise ValueError('Denominator normalization belongs to hard')
        if case == 'unit-numerator' and N != 1: raise ValueError('Unit numerator required')
        if case == 'integer-result' and not ((N/s).is_Integer and N/s>1): raise ValueError('Nonunit integer result required')
        if case == 'fractional-result' and (N/s).is_Integer: raise ValueError('Fractional result required')
        if case == 'integer-normalization' and not (s.is_Integer and D == 1): raise ValueError('Integer normalization required')
        if case == 'radical-normalization' and not (s.is_Rational is False and D == 1): raise ValueError('Radical normalization required')
        if case == 'denominator-normalization' and not (s.is_Integer and D>1 and N == 1): raise ValueError('Denominator normalization required')


def mathematical_data(kind, band, p):
    fn, A, B, N, D = (p[k] for k in ('family', 'A', 'B', 'N', 'D'))
    s = sp.sqrt(B/A)
    if kind == 'secant':
        body = N/((sp.Abs(s*X) if band != 'hard' else D*sp.Abs(X))*sp.sqrt(B*X*X-1))
        pref = N if band != 'hard' else N*s/D
        coef = sp.simplify(pref/s)
    else:
        body = N/(sp.sqrt(A-B*X*X) if fn == 'sine' else A+B*X*X)
        pref = N/(sp.sqrt(A) if fn == 'sine' else A)
        coef = sp.simplify(pref/s)
    lo, hi = (None, None) if kind != 'definite' else (sp.simplify(p['lower_u']/s), sp.simplify(p['upper_u']/s))
    primitive = coef*function(fn, s*X)
    delta = None if lo is None else sp.simplify(function(fn, p['upper_u'])-function(fn, p['lower_u']))
    answer = primitive if delta is None else sp.simplify(coef*delta)
    return dict(s=s, pref=sp.simplify(pref), coef=coef, body=body, lower=lo, upper=hi, primitive=primitive, delta=delta, answer=answer)


DEFINITE_BANKS = {
    'differential-and-numerator': ('omit-dx', 'reverse-dx', 'drop-numerator', 'double-numerator'),
    'extra-differential': ('double-dx', 'reverse-dx', 'drop-numerator', 'reverse-bounds'),
    'differential-directions': ('omit-dx', 'double-dx', 'double-numerator', 'reverse-bounds'),
    'endpoint-and-factor': ('omit-dx', 'reverse-dx', 'wrong-endpoint', 'reverse-bounds'),
    'endpoint-and-extra-factor': ('omit-dx', 'double-dx', 'wrong-endpoint', 'reverse-bounds'),
}


def answer_bank(kind, band, p, d, profile):
    fn, s, pref, c, n = p['family'], d['s'], d['pref'], d['coef'], p['N']
    if kind == 'definite':
        delta, lo, hi = d['delta'], p['lower_u'], p['upper_u']
        endpoint = sp.atan(hi)-sp.atan(lo) if fn == 'sine' else function(fn, 1/hi)-function(fn, lo)
        recipes = {'omit-dx': pref*delta, 'reverse-dx': pref*s*delta, 'double-dx': c*delta/s,
                   'drop-numerator': d['answer']/n, 'double-numerator': d['answer']*n,
                   'reverse-bounds': -d['answer'], 'wrong-endpoint': c*endpoint}
        names = DEFINITE_BANKS[profile]
        values = [d['answer']] + [sp.simplify(recipes[name]) for name in names]
    else:
        actual = function(fn, s*X)
        if kind == 'secant':
            names = ('miss-absolute-scale', 'extra-absolute-scale', 'square-scale', 'wrong-argument') if band == 'hard' else ('omit-dx', 'double-dx', 'wrong-function', 'wrong-argument')
            values = [c*actual, c/s*actual, c*s*actual, c/(s*s)*actual, c*function(fn, s*s*X)] if band == 'hard' else [c*actual, pref*actual, c/s*actual, c*sp.atan(s*X), c*function(fn, X)]
            if band == 'easy':
                names = ('wrong-prefactor', 'extra-reciprocal', 'wrong-argument', 'square-reciprocal')
                values = [c*actual, s*c*actual, c/s*actual, c*function(fn, s*s*X), c/(s*s)*actual]
        else:
            names = ('omit-dx', 'reverse-dx', 'wrong-argument', 'wrong-function')
            other = 'tangent' if fn == 'sine' else 'sine'
            values = [c*actual, pref*actual, pref*s*actual, c*function(fn, X), c*function(other, s*X)]
    # Compare complete mathematical answers, never just different strings.
    values = [sp.simplify(v) for v in values]
    if len({sp.srepr(v) for v in values}) != 5: raise ValueError('Degenerate complete bank; resample the instance')
    if kind == 'definite':
        if any(v.is_real is not True for v in values): raise ValueError('Nonreal choice')
        if any(sp.simplify(values[i]-values[j]) == 0 for i in range(5) for j in range(i)):
            raise ValueError('Equivalent choices')
    return values, ['correct'] + list(names)


def solution(kind, band, p, d):
    fn, A, B, N, D = (p[k] for k in ('family', 'A', 'B', 'N', 'D'))
    s, pref, c = (d[k] for k in ('s', 'pref', 'coef'))
    argument = tex(s*X)
    if kind == 'secant':
        body = (r'\frac{' + tex(N) + '}{|' + argument + r'|\sqrt{(' + argument + r')^{2}-1}}' if band != 'hard'
                else r'\frac{' + tex(N) + '}{' + (tex(D) if D != 1 else '') + r'|x|\sqrt{' + tex(B*X*X-1) + '}}')
        kernel_x = r'\frac{1}{|' + argument + r'|\sqrt{(' + argument + r')^{2}-1}}'
        kernel_u = r'\frac{1}{|u|\sqrt{u^{2}-1}}'
    else:
        body = r'\frac{' + tex(N) + '}{' + (r'\sqrt{' + tex(A-B*X*X) + '}' if fn == 'sine' else tex(A+B*X*X)) + '}'
        kernel_x = r'\frac{1}{' + (r'\sqrt{1-(' + argument + r')^{2}}' if fn == 'sine' else '1+(' + argument + r')^{2}') + '}'
        kernel_u = r'\frac{1}{' + (r'\sqrt{1-u^{2}}' if fn == 'sine' else '1+u^{2}') + '}'
    I = integral(body, lower=d['lower'], upper=d['upper'])
    out = []
    if kind != 'secant' and A != 1:
        sign = '-' if fn == 'sine' else '+'
        inside = '1' + sign + '(' + tex(B/A) + r')x^{2}'
        factor = r'\sqrt{' + tex(A) + '(' + inside + ')}' if fn == 'sine' else tex(A) + '(' + inside + ')'
        out += ['First factor the constant in the denominator:',
                display((r'\sqrt{' + tex(A-B*X*X) + '}' if fn == 'sine' else tex(A+B*X*X)) + '=' + factor)]
    out += ['Use the linear substitution $u=' + argument + '.$ Then',
            display(r'\frac{\mathrm{d}u}{\mathrm{d}x}=' + tex(s) + r',\qquad \mathrm{d}x=(' + tex(1/s) + r')\,\mathrm{d}u.')]
    if kind == 'secant':
        out += ['The substitution factor is positive, so the absolute values satisfy',
                display('|u|=|' + argument + '|=' + tex(s) + r'|x|,\qquad \frac{1}{|x|}=\frac{' + tex(s) + '}{|u|}.')]
    if kind == 'definite':
        out += ['Change both bounds using the same substitution:',
                display(r'\begin{aligned}x=' + tex(d['lower']) + r'&\Longrightarrow u=(' + tex(s) + ')(' + tex(d['lower']) + ')=' + tex(p['lower_u'])
                        + r' \\ x=' + tex(d['upper']) + r'&\Longrightarrow u=(' + tex(s) + ')(' + tex(d['upper']) + ')=' + tex(p['upper_u']) + r'\end{aligned}')]
        if fn == 'sine': out += ['Both transformed endpoints lie strictly between $-1$ and $1$, so the integrand is continuous throughout the interval.']
    out += ['Apply the basic inverse-trigonometric integral:',
            display(integral(kernel_u, 'u') + '=' + tex(function(fn, U)) + '+C.')]
    bounds = (p['lower_u'], p['upper_u']) if kind == 'definite' else (None, None)
    rows = [I, tex(pref) + integral(kernel_x, lower=d['lower'], upper=d['upper']),
            tex(pref) + '(' + tex(1/s) + ')' + integral(kernel_u, 'u', *bounds),
            tex(c) + integral(kernel_u, 'u', *bounds)]
    if kind == 'definite':
        lo, hi = p['lower_u'], p['upper_u']
        rows += [tex(c) + '[' + tex(function(fn, U)) + ']_{' + tex(lo) + '}^{' + tex(hi) + '}',
                 tex(c) + '(' + tex(function(fn, hi,)) + '-(' + tex(function(fn, lo)) + '))',
                 tex(c) + '((' + tex(function(fn, hi)) + ')-(' + tex(function(fn, lo)) + '))', tex(d['answer'])]
        # Show unevaluated inverse values before exact evaluation, including
        # negative endpoints. No oddness identity is silently introduced.
        name = {'sine': 'arcsin', 'tangent': 'arctan'}[fn]
        rows[-3] = tex(c) + r'(\operatorname{' + name + '}(' + tex(hi) + r')-\operatorname{' + name + '}(' + tex(lo) + '))'
    else:
        rows += [tex(c*function(fn, U)) + '+C', tex(d['primitive']) + '+C']
    out += ['Substitute and evaluate:', aligned(rows)]
    if kind == 'secant':
        out += ['This antiderivative applies on either interval where $|' + argument + '|>1$; the constant may differ between those intervals.']
    return I, '\n\n'.join(out)


class Generator:
    def __init__(self, evidence):
        self.evidence = json.loads(Path(evidence).read_text())
        self.kind = self.evidence['kind']
        self.kp = self.evidence['kp_id']
        self.kp_uuid = self.evidence['kp_uuid']
        self.cases = CASES[self.kind]
        self.excluded = set(self.evidence['excluded_task_fingerprints'])

    def ident(self, value):
        return str(uuid.uuid5(uuid.UUID(self.kp_uuid), VERSION + '|' + digest(value)))

    def build(self, band, case, parameters, *, response='radio', bank_profile=None, seed=0):
        if type(seed) is not int: raise ValueError('Seed must be a builtin integer')
        if any(type(v) is bool for v in parameters.values()): raise ValueError('Boolean parameters are not mathematical coefficients')
        p = {k: (v if k == 'family' or v is None else sp.sympify(v)) for k, v in parameters.items()}
        validate_parameters(self.kind, band, case, p)
        if response not in ('radio', 'blank') or (self.kind != 'definite' and response != 'radio'):
            raise ValueError('Response shape outside the source-supported contract')
        d = mathematical_data(self.kind, band, p)
        key = task_key(d['body'], d['lower'], d['upper'])
        if key in self.excluded: raise ValueError('Existing imported or generated mathematical task')
        if self.kind == 'definite' and response == 'radio':
            canonical_profile = tuple(DEFINITE_BANKS)[int(key,16) % len(DEFINITE_BANKS)]
            if bank_profile is not None and bank_profile != canonical_profile:
                raise ValueError('Task belongs to a different complete bank profile; resample')
            bank_profile = canonical_profile
        else:
            bank_profile = 'exact-entry' if response == 'blank' else 'authored-substitution-errors'
        I, worked = solution(self.kind, band, p, d)
        # Identities are independent of sampling seed and option permutation.
        signature = [key, band, response, bank_profile]
        qid = self.ident(signature)
        fields = []
        problem = 'Evaluate the integral. Give an exact answer.\n\n' + display(I)
        if response == 'blank':
            if d['answer'].has(sp.atan):
                if p['lower_u'] != 0: raise ValueError('Fragment entry requires a zero lower endpoint')
                problem += '\n\n{{coefficient}} $\\operatorname{arctan}($ {{argument}} $)$'
                entries = [('coefficient', d['coef']), ('argument', p['upper_u'])]
            else:
                problem += '\n\n{{answer}}'
                entries = [('answer', d['answer'])]
            for field_key, value in entries:
                fid = self.ident([qid, field_key]);aid = self.ident([fid, tex(value)])
                fields.append({':answer-field/id': fid, ':answer-field/key': field_key, ':answer-field/type': ':answer-field.type/blank',
                               ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': tex(value)}],
                               ':answer-field/correct': [':answer/id', aid]})
            recipes = []
        else:
            values, recipes = answer_bank(self.kind, band, p, d, bank_profile)
            fid = self.ident([qid, 'selection'])
            choices = [{':answer/id': self.ident([fid, tex(v)]), ':answer/type': ':answer.type/math', ':answer/value': tex(v) + ('' if self.kind == 'definite' else '+C')} for v in values]
            correct_choice, wrong_choices = choices[0], choices[1:]
            correct = correct_choice[':answer/id']
            random.Random(int(digest([key, bank_profile, seed]), 16)).shuffle(wrong_choices)
            choices = wrong_choices
            choices.insert(seed % 5, correct_choice)
            fields = [{':answer-field/id': fid, ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio',
                       ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', correct]}]
        return {'knowledge_point': {'db_id': self.kp, 'id': self.kp_uuid, 'title': self.evidence['title']},
                'question': {':question/id': qid, ':question/problem': problem, ':question/worked-solution': worked,
                             ':question/difficulty': ':question.difficulty/' + band, ':question/answer-fields': fields},
                'generation': {'version': VERSION, 'seed': seed, 'template': case, 'family': self.kind, 'inverse_function': p['family'],
                               'parameters': {k: None if v is None else str(v) for k, v in p.items()}, 'response': response,
                               'source_ids': self.evidence['anchors'][band], 'source_basis': self.evidence['basis'],
                               'source_lineage': self.evidence['lineage'], 'mathematical_fingerprint': key,
                               'bank_profile': bank_profile, 'answer_recipes': recipes,
                               'authored': True, 'authored_bank': response == 'radio',
                               'relationship_to_source_templates': self.evidence['band_contract'][band],
                               'domain': 'positive linear factor; principal real inverse functions; secant on each component |u|>1; definite arcsine strictly -1<u<1',
                               'dependencies': {'python': sys.version.split()[0], 'sympy': sp.__version__}, 'plots': []}}

    def generate(self, difficulty='easy', seed=0, template=None, parameters=None, *, response='radio', bank_profile=None):
        if difficulty not in LEVELS or type(seed) is not int: raise ValueError('Invalid difficulty or seed')
        rng = random.Random(seed);case = template or rng.choice(self.cases[difficulty])
        if case not in self.cases[difficulty]: raise ValueError('Unknown band case')
        if parameters is not None:
            return self.build(difficulty, case, parameters, response=response, bank_profile=bank_profile, seed=seed)
        eligible_banks = tuple(DEFINITE_BANKS)
        if case in ('tangent-special', 'tangent-two-positive'):
            # At endpoint one the reciprocal is unchanged. For the positive
            # (1,sqrt(3)) pair it instead duplicates the reverse-bounds error.
            # These whole profiles are inapplicable to the two case catalogs.
            eligible_banks = tuple(v for v in eligible_banks if not v.startswith('endpoint-'))
        if bank_profile is not None and self.kind == 'definite' and response == 'radio' and bank_profile not in eligible_banks:
            raise ValueError('Complete bank profile is inapplicable to this endpoint case')
        profile = bank_profile or (rng.choice(eligible_banks) if self.kind == 'definite' else 'authored-substitution-errors')
        last_error = None
        for _ in range(300):
            p = sample(self.kind, difficulty, case, rng)
            try: return self.build(difficulty, case, p, response=response, bank_profile=profile, seed=seed)
            except ValueError as error: last_error = str(error)
        raise ValueError(f'No eligible instance: {self.kind}/{difficulty}/{case}/{profile}: {last_error}')

    def batch(self, difficulty='all', count=8, seed=0):
        if type(count) is not int or not 1 <= count <= 100 or type(seed) is not int:
            raise ValueError('Builtin integer seed and count in 1..100 required')
        if difficulty not in (*LEVELS, 'all'): raise ValueError('Invalid difficulty')
        rng = random.Random(seed);rows = [];seen = set(self.excluded)
        for band in (LEVELS if difficulty == 'all' else (difficulty,)):
            cases = list(self.cases[band]);rng.shuffle(cases)
            for i in range(count):
                case = cases[i % len(cases)]
                response = 'blank' if self.kind == 'definite' and (i // len(cases)) % 2 else 'radio'
                for _ in range(300):
                    draw_seed = rng.randrange(2**53)
                    draw_seed = draw_seed-draw_seed%5+(i//len(cases))%5
                    r = self.generate(band, draw_seed, case, response=response)
                    key = r['generation']['mathematical_fingerprint']
                    if key not in seen:
                        rows.append(r);seen.add(key);break
                else: raise ValueError('Finite family exhausted; no duplicates used as padding')
        return rows

    def source_original(self, source_id):
        """Unmodified import evidence, explicitly outside normal generation."""
        return next(q for q in self.evidence['originals'] if q.get(':question/math-academy-id') == source_id)

    def main(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--difficulty', choices=(*LEVELS, 'all'), default='all')
        parser.add_argument('--count', type=int, default=8)
        parser.add_argument('--seed', type=int, default=0)
        parser.add_argument('--format', choices=('json', 'markdown'), default='json')
        args = parser.parse_args()
        records = self.batch(args.difficulty, args.count, args.seed)
        if args.format == 'json': print(json.dumps(records, indent=2, ensure_ascii=False))
        else:
            for r in records:
                q = r['question'];print(q[':question/problem'])
                for f in q[':question/answer-fields']:
                    for a in f[':answer-field/choices']: print('- $' + a[':answer/value'] + '$')
                print('\n' + q[':question/worked-solution'] + '\n\n---\n')
