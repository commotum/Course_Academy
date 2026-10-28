"""First-order ODE verification with independent derivative and solution cases."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import random
import sys
import uuid

import sympy as sp
import source_replay as replay
from math_format import normalize_prose, validate_generated_record

VERSION = CURRENT_VERSION = '2.2.0'
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
KP = replay.KP
MASKS = replay.MASKS
DEFAULTS = replay.DEFAULTS
LEVELS = {**replay.LEVELS, 'power_moderate': 'easy', 'affine_log': 'easy', 'exp_nonlinear': 'moderate', 'log_equation': 'hard'}
x, y = replay.x, replay.y
CASES = ((False, False), (False, True), (True, False), (True, True))
SOURCE = json.loads((Path(__file__).parent / 'source-metadata.json').read_text())


def tex(value):
    return sp.latex(value).replace(r'\log', r'\ln')


def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ode-verify:' + value))


def choose_coefficient(actual, pool, correct, rng):
    return actual if correct else rng.choice([v for v in pool if v != actual])


def sample(template, rng, decision_case=None):
    """Choose the two decisions first; coefficients then realize those decisions."""
    claim, solution = rng.choice(CASES) if decision_case is None else decision_case
    pool = (2, 3, 4, 5)
    if template in ('power_easy', 'power_moderate', 'inverse_none'):
        n = rng.choice(pool)
        p = {'n': n, 'd': choose_coefficient(n, pool, claim, rng),
             'q': choose_coefficient(n, pool, solution, rng)}
        if template == 'power_moderate':
            p['a'] = -rng.randint(2, 9)
            p['d'] *= p['a']
    elif template in ('exp_true', 'exp_none', 'sin_none', 'cos_i', 'log_all'):
        k = rng.choice(pool)
        p = {'k': k, 'd': choose_coefficient(k, pool, claim, rng),
             'q': choose_coefficient(k, pool, solution, rng)}
        if template == 'exp_none':
            p['a'] = rng.randint(2, 5)
        elif template == 'sin_none':
            p['b'] = rng.choice(pool)
        elif template == 'log_all':
            p['h'] = rng.randint(-4, 4)
    elif template == 'log_scaled':
        m = rng.randint(1, 4)
        p = {'m': m, 'd': choose_coefficient(2*m, (2, 4, 6, 8), claim, rng),
             'q': choose_coefficient(2*m, (2, 4, 6, 8), solution, rng)}
    elif template == 'affine_log':
        b = rng.randint(2, 4)
        p = {'a': rng.choice((-4, -3, -2, 2, 3, 4)), 'b': b,
             'c': rng.choice((-4, -3, -2, -1, 1, 2, 3, 4)),
             'd': choose_coefficient(b, (2, 3, 4), claim, rng),
             'q': choose_coefficient(b, (2, 3, 4), solution, rng)}
    elif template == 'exp_nonlinear':
        k = rng.choice((-2, -1, 1, 2))
        pool = (-4, -2, -1, 1, 2, 4)
        p = {'a': rng.randint(1, 3), 'k': k, 'h': rng.randint(-1, 1),
             'd': choose_coefficient(2*k, pool, claim, rng),
             'q': choose_coefficient(2*k, pool, solution, rng)}
    elif template == 'log_equation':
        n, a, r = rng.randint(2, 4), rng.randint(1, 3), rng.randint(1, 3)
        target = a*(n-r)
        p = {'n': n, 'a': a, 'r': r,
             'd': choose_coefficient(n, (1, 2, 3, 4, 5), claim, rng),
             'q': choose_coefficient(target, tuple(range(-9, 10)), solution, rng)}
    else:
        raise ValueError('Unknown template: ' + template)
    return p


PARAMETER_KEYS = {
    'exp_nonlinear': {'a', 'k', 'h', 'd', 'q'},
    'log_equation': {'n', 'a', 'r', 'd', 'q'},
    'power_easy': {'n', 'd', 'q'}, 'power_moderate': {'a', 'n', 'd', 'q'},
    'inverse_none': {'n', 'd', 'q'}, 'exp_true': {'k', 'd', 'q'},
    'exp_none': {'a', 'k', 'd', 'q'}, 'sin_none': {'b', 'k', 'd', 'q'},
    'cos_i': {'k', 'd', 'q'}, 'log_all': {'h', 'k', 'd', 'q'},
    'log_scaled': {'m', 'd', 'q'}, 'affine_log': {'a', 'b', 'c', 'd', 'q'},
}


def validate_parameters(template, p):
    if set(p) != PARAMETER_KEYS[template] or any(type(v) is not int for v in p.values()):
        raise ValueError('Unexpected or noninteger parameters')
    if template == 'exp_nonlinear':
        valid = (1 <= p['a'] <= 3 and p['k'] in (-2, -1, 1, 2) and -1 <= p['h'] <= 1
                 and p['d'] in (-4, -2, -1, 1, 2, 4) and p['q'] in (-4, -2, -1, 1, 2, 4))
    elif template == 'log_equation':
        valid = (2 <= p['n'] <= 4 and 1 <= p['a'] <= 3 and 1 <= p['r'] <= 3
                 and 1 <= p['d'] <= 5 and -9 <= p['q'] <= 9)
    elif template == 'affine_log':
        valid = (p['a'] in (-4, -3, -2, 2, 3, 4)
                 and p['c'] in (-4, -3, -2, -1, 1, 2, 3, 4)
                 and all(2 <= p[v] <= 4 for v in ('b', 'd', 'q')))
    elif template == 'log_scaled':
        valid = 1 <= p['m'] <= 4 and p['d'] in (2, 4, 6, 8) and p['q'] in (2, 4, 6, 8)
    else:
        coefficient_keys = ('n', 'k', 'b', 'q') if template == 'power_moderate' else ('n', 'k', 'b', 'd', 'q')
        valid = all(2 <= p[v] <= 5 for v in coefficient_keys if v in p)
        if template == 'power_moderate': valid = valid and -9 <= p['a'] <= -2 and -45 <= p['d'] <= -2
        if template == 'exp_none': valid = valid and 2 <= p['a'] <= 5
        if template == 'log_all': valid = valid and -4 <= p['h'] <= 4
    if not valid:
        raise ValueError('Parameters outside the source-justified bounds')


def instance(template, p):
    """One mathematical instance supplies prompt, answer, and all solution stages."""
    validate_parameters(template, p)
    d, q = p['d'], p['q']
    derivative_steps, rhs_steps = [], []
    domain = 'all real x'
    if template in ('power_easy', 'power_moderate'):
        a, n = p.get('a', 1), p['n']
        f, claim, rhs = a*x**n, d*x**(n-1), q*y/x
        derivative_steps = [tex(a) + r'\cdot ' + tex(n*x**(n-1))] if a != 1 else []
        rhs_steps = [r'\frac{' + str(q) + r'\left(' + tex(f) + r'\right)}{x}']
        domain = 'x != 0'
    elif template in ('exp_true', 'exp_none'):
        a, k = p.get('a', 1), p['k']
        sign = -1 if template == 'exp_none' else 1
        f = a*sp.exp(sign*k*x)
        claim, rhs = sign*a*d*sp.exp(sign*k*x), sign*q*y
        derivative_steps = [str(a) + r'\cdot (' + str(sign*k) + r')\,' + tex(sp.exp(sign*k*x))]
        rhs_steps = [str(sign*q) + r'\left(' + tex(f) + r'\right)']
    elif template == 'sin_none':
        k, b = p['k'], p['b']
        f, claim, rhs = sp.sin(k*x)/b, sp.Rational(d, b)*sp.cos(k*x), sp.Rational(q, b)*sp.cos(k*x)
        derivative_steps = [r'\frac{1}{' + str(b) + r'}\cdot ' + str(k) + r'\cos(' + str(k) + r'x)']
    elif template == 'cos_i':
        k = p['k']
        f, claim, rhs = sp.cos(k*x), -d*sp.sin(k*x), -q*sp.sin(k*x)
        derivative_steps = [r'-\sin(' + str(k) + r'x)\cdot ' + str(k)]
    elif template == 'inverse_none':
        n = p['n']
        f, claim, rhs = -x**(-n), d*x**(-n-1), -q*y/x
        derivative_steps = [r'-(-' + str(n) + r')x^{-' + str(n+1) + '}']
        rhs_steps = [r'\frac{-' + str(q) + r'\left(' + tex(f) + r'\right)}{x}']
        domain = 'x != 0'
    elif template == 'log_all':
        z = p['k']*x+p['h']
        f, claim, rhs = sp.log(z), d/z, q*sp.exp(-y)
        derivative_steps = [r'\frac{1}{' + tex(z) + r'}\cdot ' + str(p['k'])]
        rhs_steps = [r'\frac{' + str(q) + r'}{e^{' + tex(f) + '}}']
        domain = tex(z) + '>0'
    elif template == 'log_scaled':
        a, m = 2*p['m'], p['m']
        f, claim, rhs = a*sp.log(x), d/x, q*x*sp.exp(-y/m)
        derivative_steps = [str(a) + r'\cdot\frac{1}{x}']
        rhs_steps = [r'\frac{' + str(q) + r'x}{e^{(' + tex(f) + ')/' + str(m) + '}}',
                     r'\frac{' + str(q) + r'x}{e^{2\ln x}}',
                     r'\frac{' + str(q) + r'x}{e^{\ln(x^2)}}',
                     r'\frac{' + str(q) + r'x}{x^2}']
        domain = 'x>0'
    elif template == 'exp_nonlinear':
        a, k, h = p['a'], p['k'], p['h']
        f = a*sp.exp(k*x**2+h)
        claim, rhs = a*d*x*sp.exp(k*x**2+h), q*x*y
        derivative_steps = [tex(a*sp.exp(k*x**2+h)) + r'\cdot (' + tex(2*k*x) + ')']
        rhs_steps = [tex(q*x) + r'\left(' + tex(f) + r'\right)']
    elif template == 'log_equation':
        n, a, r = p['n'], p['a'], p['r']
        f = n*sp.log(x) + sp.log(a)
        claim = d/x
        rhs = (q*x**n + r*sp.exp(y))/(x*sp.exp(y))
        derivative_steps = [str(n) + r'\cdot\frac{1}{x}+0']
        domain = 'x>0'
    else:
        a, b, c = p['a'], p['b'], p['c']
        z = b*x+c
        f, claim, rhs = a*sp.log(z), a*d/z, a*q*sp.exp(-y/a)
        derivative_steps = [str(a) + r'\cdot\frac{' + str(b) + '}{' + tex(z) + '}']
        rhs_steps = [str(a*q) + r'e^{-(' + tex(f) + ')/(' + str(a) + ')}',
                     str(a*q) + r'e^{-\ln(' + tex(z) + ')}']
        domain = tex(z) + '>0'
    actual = sp.diff(f, x)
    substituted = sp.simplify(rhs.subs(y, f))
    decisions = (sp.simplify(actual-claim) == 0, sp.simplify(actual-substituted) == 0)
    return dict(f=f, claim=claim, rhs=rhs, actual=actual, substituted=substituted,
                derivative_steps=derivative_steps, rhs_steps=rhs_steps,
                domain=domain, decisions=decisions, template=template, parameters=p)


def render(inst):
    if inst['template'] == 'log_equation':
        return render_log_equation(inst)
    f, claim, rhs, actual, substituted = (tex(inst[v]) for v in ('f', 'claim', 'rhs', 'actual', 'substituted'))
    if inst['template'] == 'affine_log':
        p = inst['parameters']
        substituted = r'\frac{' + str(p['a']*p['q']) + '}{' + tex(p['b']*x+p['c']) + '}'
    i, ii = inst['decisions']
    domain = inst['domain']
    domain_tex = r'x\ne 0' if domain == 'x != 0' else domain
    restriction = (r',\qquad ' + domain_tex) if domain != 'all real x' else ''
    prompt = ('Consider the following differential equation.\n\n$$\ny\\prime=' + rhs + restriction
              + '\n$$\n\nLet $f(x)=' + f + '.$ Which of the following statements are true?'
              + '\n\nSelect all that apply.\n\n- **I.** $f\\prime(x)=' + claim + '.$'
              + '\n- **II.** Substituting $y=f(x)$ and $y\\prime=f\\prime(x)$ into the differential equation gives a true statement.'
              + '\n- **III.** The function $y=f(x)$ is a solution of the differential equation.')
    status = lambda value: 'true' if value else 'false'
    solution = ('For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation '
                + replay.NORMAL_DOMAIN_PHRASE + '\n\nWith that in mind, let\'s check each statement in turn.\n\n')
    derivative_rows = [r'f\prime(x)&=\left(' + f + r'\right)\prime']
    derivative_rows += ['&=' + step for step in inst['derivative_steps']]
    derivative_rows += ['&=' + actual]
    if not i: derivative_rows += [r'&\not\equiv ' + claim]
    solution += ('- Statement I is ' + status(i) + '. Differentiating $f(x)=' + f + ',$ we get\n\n$$\n'
                 + r'\begin{aligned}' + r' \\ '.join(derivative_rows) + r'\end{aligned}' + '\n$$\n\n')
    sub_rows = [r'y\prime &\overset{?}{=}' + rhs]
    sub_rows += [actual + r' &\overset{?}{=}' + step for step in inst['rhs_steps']]
    sub_rows += [actual + (' &=' if ii else r' &\not\equiv ') + substituted]
    if inst['template'] in ('affine_log', 'log_all', 'log_scaled'):
        solution += 'For a positive argument $z$, use $e^{\\ln z}=z$ and $e^{-\\ln z}=1/z$; the power rule gives $2\\ln x=\\ln(x^2)$ when $x>0$.\n\n'
    solution += ('- Statement II is ' + status(ii) + '. Substituting $y=' + f + '$ and $y\\prime=' + actual
                 + '$ into the original equation gives ' + ('an identity' if ii else 'expressions that are not identical')
                 + ':\n\n$$\n' + r'\begin{aligned}' + r' \\ '.join(sub_rows) + r'\end{aligned}' + '\n$$\n\n')
    solution += ('- Statement III is ' + status(ii) + '. Since statement II is ' + status(ii)
                 + ', the function $y=' + f + '$ is ' + ('' if ii else 'not ')
                 + 'a solution to our differential equation.\n\nTherefore, the correct answer is "'
                 + replay.ANSWERS[i, ii] + '."')
    return normalize_prose(prompt), normalize_prose(solution)



def render_log_equation(inst):
    p = inst['parameters']
    n, a, r, q = (p[v] for v in ('n', 'a', 'r', 'q'))
    f = str(n) + r'\ln x' + (r'+\ln ' + str(a) if a != 1 else '')
    claim = r'\frac{' + str(p['d']) + '}{x}'
    actual = r'\frac{' + str(n) + '}{x}'
    equation = r'xe^y y\prime-' + (str(r) if r != 1 else '') + r'e^y=' + tex(q*x**n)
    prompt = ('Consider the differential equation.\n\n$$\n' + equation + r',\qquad x>0.'
              + '\n$$\n\nLet $f(x)=' + f + '$. Which statements are true? Select all that apply.'
              + '\n\n- **I.** $f\\prime(x)=' + claim + '$.'
              + '\n- **II.** Substituting $y=f(x)$ and $y\\prime=f\\prime(x)$ into the differential equation gives a true statement.'
              + '\n- **III.** The function $y=f(x)$ is a solution of the differential equation.')
    i, ii = inst['decisions']
    yes = lambda v: 'true' if v else 'false'
    solution = ('A solution must satisfy the equation throughout the stated interval. Here $x>0$ makes the logarithm defined.\n\n'
                + 'Differentiate the candidate:\n\n$$\n' + r'f\prime(x)=' + str(n) + r'\frac{1}{x}'
                + ('+0' if a != 1 else '') + '=' + actual + '.\n$$\n\nStatement I is ' + yes(i) + '.\n\n'
                + 'Before substituting, simplify the exponential using the logarithm power rule and inverse identity:\n\n$$\n'
                + r'\begin{aligned}e^{f(x)}&=e^{' + f + r'}\\&=e^{' + str(n) + r'\ln x}'
                + (r'e^{\ln ' + str(a) + '}' if a != 1 else '')
                + r'\\&=e^{\ln(x^{' + str(n) + '})}' + (r'\cdot ' + str(a) if a != 1 else '')
                + r'\\&=' + tex(a*x**n) + r'.\end{aligned}' + '\n$$\n\n'
                + 'Substitute into the entire left side:\n\n$$\n'
                + r'\begin{aligned}xe^{f(x)}f\prime(x)-' + str(r) + r'e^{f(x)}'
                + r'&=x\left(' + tex(a*x**n) + r'\right)' + actual + '-' + str(r) + r'\left(' + tex(a*x**n) + r'\right)'
                + r'\\&=' + tex(a*n*x**n) + '-' + tex(a*r*x**n)
                + r'\\&=' + tex(a*(n-r)*x**n) + r'.\end{aligned}' + '\n$$\n\n'
                + 'The right side is $' + tex(q*x**n) + '$. These expressions '
                + ('agree' if ii else 'do not agree') + ' for every $x>0$. Statement II is ' + yes(ii)
                + ', so statement III is ' + yes(ii) + '.\n\nSelect '
                + (replay.ANSWERS[i, ii] if (i or ii) else 'None of the above') + '.')
    return normalize_prose(prompt), normalize_prose(solution)

def make_record(level, template, p, seed, inst):
    prompt, solution = render(inst)
    i, ii = inst['decisions']
    bank = MASKS[template]['bank'] if template in MASKS else {key: ['false', 'true'] for key in ('I', 'II', 'III')}
    content = json.dumps([VERSION, level, prompt, solution, bank], ensure_ascii=False, sort_keys=True)
    qid = uid(content)
    prompt, statement_block = prompt.split('\n\n- **I.** ', 1)
    statement_texts = [statement_block.split('\n- **II.** ')[0],
                       statement_block.split('\n- **II.** ')[1].split('\n- **III.** ')[0],
                       statement_block.split('\n- **III.** ')[1]]
    fields = []
    for key, correct in zip(('I', 'II', 'III'), (i, ii, ii), strict=True):
        fid = uid(qid + ':' + key)
        fields.append({':answer-field/id': fid, ':answer-field/key': normalize_prose(key + '. ' + statement_texts[len(fields)]),
                       ':answer-field/type': ':answer-field.type/checkbox',
                       ':answer-field/choices': [{':answer/id': uid(fid + ':' + v),
                          ':answer/type': ':answer.type/text', ':answer/value': v} for v in bank[key]],
                       ':answer-field/correct': [':answer/id', uid(fid + ':' + str(correct).lower())]})
    mathkey = hashlib.sha256(json.dumps([sp.srepr(inst[k]) for k in ('f', 'claim', 'rhs')] + [inst['domain']]).encode()).hexdigest()
    source_id = MASKS[template]['source_id'] if template in MASKS else None
    exemplar = {'exp_nonlinear': 'f6090809-33ff-5c55-a7b0-d65b2137fd2a',
                'log_equation': '3731fce8-2fda-5013-b83b-ab216ad70ca1'}.get(template)
    record = {'knowledge_point': KP.copy(), 'question': {
        ':question/id': qid, ':question/difficulty': ':question.difficulty/' + level,
        ':question/problem': prompt, ':question/worked-solution': solution, ':question/answer-fields': fields},
        'generation': {'version': VERSION, 'template': template, 'parameters': p, 'seed': seed,
            'bank_profile': MASKS[template]['profile'] if template in MASKS else 'authored',
            'origin': 'authored_extension' if template in ('affine_log', 'log_equation', 'exp_nonlinear') else 'same_method_decision_extension',
            'eligible_for_learning': True, 'evidence_only': False,
            'mathematical_fingerprint': mathkey,
            'content_fingerprint': hashlib.sha256(content.encode()).hexdigest(),
            'decision_case': ''.join('T' if v else 'F' for v in (i, ii, ii)),
            'domain': inst['domain'], 'plot_rating': 'none',
            'runtime': {'python': sys.version.split()[0], 'sympy': sp.__version__},
            'source_analysis': {'database': SOURCE['database'], 'basis': SOURCE['basis'], 'lineage': SOURCE['lineage'],
                'question_ids': [source_id] if source_id else [exemplar] if exemplar else [],
                'question_db_ids': [SOURCE['question_ids'][source_id]] if source_id else []}}}
    return validate_generated_record(record)


def source_replay(level, template, parameters=None, raw=False):
    """Explicit replay is separate from the normal decision-varying sampler."""
    if not raw and (parameters is None or parameters == DEFAULTS[template]):
        return json.loads((Path(__file__).parent / 'source-replays.json').read_text())[template]
    rec = replay.generate(level, template=template, parameters=parameters or DEFAULTS[template],
                          profile=('raw_' if raw else '') + MASKS[template]['profile'])
    rec['generation']['source_analysis'].update({k: SOURCE[k] for k in ('database', 'basis', 'lineage')})
    rec['generation']['source_analysis']['question_db_ids'] = [SOURCE['question_ids'][MASKS[template]['source_id']]]
    rec['generation']['origin'] = 'explicit_source_replay'
    rec['generation']['eligible_for_learning'] = False
    rec['generation']['evidence_only'] = True
    if raw:
        return rec
    question = rec['question']
    for name in (':question/problem', ':question/worked-solution'):
        question[name] = normalize_prose(question[name])
    # Normalized replay identities are also based on canonical presentation.
    qid = uid(json.dumps([VERSION, question[':question/problem'], question[':question/worked-solution']], ensure_ascii=False))
    question[':question/id'] = qid
    for field in question[':question/answer-fields']:
        fid = uid(qid + ':' + field[':answer-field/key'])
        old_correct = field[':answer-field/correct'][1]
        field[':answer-field/id'] = fid
        for answer in field[':answer-field/choices']:
            was_correct = answer[':answer/id'] == old_correct
            answer[':answer/id'] = uid(fid + ':' + answer[':answer/value'])
            if was_correct: field[':answer-field/correct'][1] = answer[':answer/id']
    return validate_generated_record(rec)


def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None, decision_case=None):
    if level not in SUPPORTED_LEVELS or field_type not in (None, 'checkbox', ':answer-field.type/checkbox'):
        raise ValueError('Unsupported level or field type')
    raw = bool(profile and profile.startswith('raw_'))
    normalized = profile[4:] if raw else profile
    if normalized not in (None, 'boolean_statements', 'authored'):
        matched = [t for t, m in MASKS.items() if m['profile'] == normalized]
        if not matched or template not in (None, matched[0]): raise ValueError('Unknown or conflicting profile')
        template = matched[0]
    eligible = [t for t, band in LEVELS.items() if band == level]
    rng = random.Random(seed)
    template = template or rng.choice(eligible)
    if template in DEFAULTS and parameters is not None and set(parameters) == set(DEFAULTS[template]):
        if level != replay.LEVELS[template]: raise ValueError('Source replay difficulty mismatch')
        return source_replay(level, template, parameters, raw=raw)
    if template not in eligible: raise ValueError('Template/difficulty mismatch')
    if raw or (parameters is not None and template in DEFAULTS and set(parameters) == set(DEFAULTS[template])):
        if decision_case is not None: raise ValueError('Decision override cannot change source replay')
        return source_replay(level, template, parameters, raw=raw)
    p = dict(parameters) if parameters is not None else sample(template, rng, decision_case)
    return make_record(level, template, p, seed, instance(template, p))


def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)
def generate_hard(seed=0, **kwargs): return generate('hard', seed, **kwargs)


def parameter_domain(template):
    """Finite coefficient domains; no symbolic rejection loop is needed."""
    if template in ('exp_nonlinear', 'log_equation'):
        # Finite enumerated domains, independent from symbolic evaluation.
        if template == 'exp_nonlinear':
            for a, k, h, d, q in itertools.product(range(1, 4), (-2, -1, 1, 2), range(-1, 2), (-4, -2, -1, 1, 2, 4), (-4, -2, -1, 1, 2, 4)):
                yield dict(a=a, k=k, h=h, d=d, q=q), (d == 2*k, q == 2*k)
        else:
            for n, a, r, d, q in itertools.product(range(2, 5), range(1, 4), range(1, 4), range(1, 6), range(-9, 10)):
                yield dict(n=n, a=a, r=r, d=d, q=q), (d == n, q == a*(n-r))
        return
    pool = (2, 3, 4, 5)
    for target, d, q in itertools.product((2, 3, 4) if template == 'affine_log' else pool, repeat=3):
        if template in ('power_easy', 'inverse_none'):
            yield {'n': target, 'd': d, 'q': q}, (d == target, q == target)
        elif template == 'power_moderate':
            for a in range(-9, -1):
                yield {'a': a, 'n': target, 'd': a*d, 'q': q}, (d == target, q == target)
        elif template in ('exp_true', 'cos_i'):
            yield {'k': target, 'd': d, 'q': q}, (d == target, q == target)
        elif template == 'exp_none':
            for a in pool:
                yield {'a': a, 'k': target, 'd': d, 'q': q}, (d == target, q == target)
        elif template == 'sin_none':
            for b in pool:
                yield {'b': b, 'k': target, 'd': d, 'q': q}, (d == target, q == target)
        elif template == 'log_all':
            for h in range(-4, 5):
                yield {'h': h, 'k': target, 'd': d, 'q': q}, (d == target, q == target)
        elif template == 'log_scaled':
            # Shift 2..5 to the four source-supported outer scales 2,4,6,8.
            yield {'m': target-1, 'd': 2*(d-1), 'q': 2*(q-1)}, (d == target, q == target)
        else:
            for a, c in itertools.product((-4, -3, -2, 2, 3, 4), (-4, -3, -2, -1, 1, 2, 3, 4)):
                yield {'a': a, 'b': target, 'c': c, 'd': d, 'q': q}, (d == target, q == target)


def batch(level, count, seed=0, template=None, profile=None):
    if type(count) is not int or count < 1 or count > 1000:
        raise ValueError('Count must be between 1 and 1000')
    if profile and profile.startswith('raw_'):
        if count != 1: raise ValueError('A captured source case has one replay instance')
        return [generate(level, seed, template=template, profile=profile)]
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty')
    if profile not in (None, 'authored', 'boolean_statements'):
        matched = [t for t, mask in MASKS.items() if mask['profile'] == profile]
        if not matched or template not in (None, matched[0]): raise ValueError('Unknown or conflicting profile')
        template = matched[0]
    eligible = [t for t, band in LEVELS.items() if band == level and template in (None, t)]
    if not eligible: raise ValueError('Template/difficulty mismatch')
    # Enumerate small integer domains without symbolic work, shuffle once, then
    # render exactly the requested records. No repeated trial/dedup generation.
    rng = random.Random(seed)
    pairs = list(itertools.product(eligible, CASES))
    rng.shuffle(pairs)
    # Balance decisions before presentation families. A shuffled family/case
    # list can accidentally couple the two judgments throughout a small batch.
    # Every full traversal still contains each family/case exactly once.
    remaining = list(pairs)
    pairs = []
    case_counts = {case: 0 for case in CASES}
    family_counts = {family: 0 for family in eligible}
    while remaining:
        pair = min(remaining, key=lambda v: (case_counts[v[1]], family_counts[v[0]]))
        remaining.remove(pair)
        pairs.append(pair)
        case_counts[pair[1]] += 1
        family_counts[pair[0]] += 1
    buckets = {pair: [] for pair in pairs}
    for family in eligible:
        for p, case in parameter_domain(family):
            buckets[family, case].append(p)
    capacity = sum(map(len, buckets.values()))
    if count > capacity: raise ValueError('Finite semantic capacity: ' + str(capacity))
    for bucket in buckets.values(): rng.shuffle(bucket)
    records = []
    while len(records) < count:
        for family, case in pairs:
            if buckets[family, case]:
                p = buckets[family, case].pop()
                records.append(make_record(level, family, p, seed, instance(family, p)))
                if len(records) == count: break
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=(*SUPPORTED_LEVELS, 'all'), default='all')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    parser.add_argument('--template')
    parser.add_argument('--profile')
    args = parser.parse_args()
    if args.difficulty == 'all' and (args.template or args.profile): parser.error('Select one difficulty for a template/profile')
    bands = SUPPORTED_LEVELS if args.difficulty == 'all' else (args.difficulty,)
    try:
        records = [rec for band in bands for rec in batch(band, args.count, args.seed, args.template, args.profile)]
    except ValueError as exc: parser.error(str(exc))
    print(json.dumps(records, ensure_ascii=False, indent=2) if args.format == 'json'
          else '\n\n---\n\n'.join(replay.markdown(rec) for rec in records))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__ == '__main__': main()
