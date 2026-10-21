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

VERSION = CURRENT_VERSION = '2.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
KP = replay.KP
MASKS = replay.MASKS
DEFAULTS = replay.DEFAULTS
LEVELS = replay.LEVELS
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
    else:
        raise ValueError('Unknown template: ' + template)
    return p


PARAMETER_KEYS = {
    'power_easy': {'n', 'd', 'q'}, 'power_moderate': {'a', 'n', 'd', 'q'},
    'inverse_none': {'n', 'd', 'q'}, 'exp_true': {'k', 'd', 'q'},
    'exp_none': {'a', 'k', 'd', 'q'}, 'sin_none': {'b', 'k', 'd', 'q'},
    'cos_i': {'k', 'd', 'q'}, 'log_all': {'h', 'k', 'd', 'q'},
    'log_scaled': {'m', 'd', 'q'}, 'affine_log': {'a', 'b', 'c', 'd', 'q'},
}


def validate_parameters(template, p):
    if set(p) != PARAMETER_KEYS[template] or any(type(v) is not int for v in p.values()):
        raise ValueError('Unexpected or noninteger parameters')
    if template == 'affine_log':
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
                domain=domain, decisions=decisions)


def render(inst):
    f, claim, rhs, actual, substituted = (tex(inst[v]) for v in ('f', 'claim', 'rhs', 'actual', 'substituted'))
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
    solution += ('- Statement II is ' + status(ii) + '. Substituting $y=' + f + '$ and $y\\prime=' + actual
                 + '$ into the original equation gives ' + ('an identity' if ii else 'expressions that are not identical')
                 + ':\n\n$$\n' + r'\begin{aligned}' + r' \\ '.join(sub_rows) + r'\end{aligned}' + '\n$$\n\n')
    solution += ('- Statement III is ' + status(ii) + '. Since statement II is ' + status(ii)
                 + ', the function $y=' + f + '$ is ' + ('' if ii else 'not ')
                 + 'a solution to our differential equation.\n\nTherefore, the correct answer is "'
                 + replay.ANSWERS[i, ii] + '."')
    return normalize_prose(prompt), normalize_prose(solution)


def make_record(level, template, p, seed, inst):
    prompt, solution = render(inst)
    i, ii = inst['decisions']
    bank = MASKS[template]['bank'] if template in MASKS else {key: ['false', 'true'] for key in ('I', 'II', 'III')}
    content = json.dumps([VERSION, level, prompt, solution, bank], ensure_ascii=False, sort_keys=True)
    qid = uid(content)
    fields = []
    for key, correct in zip(('I', 'II', 'III'), (i, ii, ii), strict=True):
        fid = uid(qid + ':' + key)
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/checkbox',
                       ':answer-field/choices': [{':answer/id': uid(fid + ':' + v),
                          ':answer/type': ':answer.type/text', ':answer/value': v} for v in bank[key]],
                       ':answer-field/correct': [':answer/id', uid(fid + ':' + str(correct).lower())]})
    mathkey = hashlib.sha256(json.dumps([sp.srepr(inst[k]) for k in ('f', 'claim', 'rhs')] + [inst['domain']]).encode()).hexdigest()
    source_id = MASKS[template]['source_id'] if template in MASKS else None
    record = {'knowledge_point': KP.copy(), 'question': {
        ':question/id': qid, ':question/difficulty': ':question.difficulty/' + level,
        ':question/problem': prompt, ':question/worked-solution': solution, ':question/answer-fields': fields},
        'generation': {'version': VERSION, 'template': template, 'parameters': p, 'seed': seed,
            'bank_profile': MASKS[template]['profile'] if template in MASKS else 'authored',
            'origin': 'authored_missing_level' if template == 'affine_log' else 'same_method_decision_extension',
            'eligible_for_learning': True, 'evidence_only': False,
            'mathematical_fingerprint': mathkey,
            'content_fingerprint': hashlib.sha256(content.encode()).hexdigest(),
            'decision_case': ''.join('T' if v else 'F' for v in (i, ii, ii)),
            'domain': inst['domain'], 'plot_rating': 'none',
            'runtime': {'python': sys.version.split()[0], 'sympy': sp.__version__},
            'source_analysis': {'database': SOURCE['database'], 'basis': SOURCE['basis'], 'lineage': SOURCE['lineage'],
                'question_ids': [source_id] if source_id else [],
                'question_db_ids': [SOURCE['question_ids'][source_id]] if source_id else []}}}
    return validate_generated_record(record)


def source_replay(level, template, parameters=None, raw=False):
    """Explicit replay is separate from the normal decision-varying sampler."""
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
    cases = list(CASES)
    rng.shuffle(cases)
    buckets = {case: [] for case in CASES}
    for family in eligible:
        for p, case in parameter_domain(family): buckets[case].append((family, p))
    capacity = sum(map(len, buckets.values()))
    if count > capacity: raise ValueError('Finite semantic capacity: ' + str(capacity))
    for bucket in buckets.values(): rng.shuffle(bucket)
    records = []
    for offset in range(count):
        case = cases[offset % len(cases)]
        if not buckets[case]: case = rng.choice([case for case in cases if buckets[case]])
        family, p = buckets[case].pop()
        records.append(make_record(level, family, p, seed, instance(family, p)))
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


if __name__ == '__main__': main()
