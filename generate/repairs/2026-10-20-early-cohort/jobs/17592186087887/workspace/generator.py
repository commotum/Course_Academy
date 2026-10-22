#!/usr/bin/env python3
"""Relocatable, deterministic homogeneous-ODE question generator (no I/O assets)."""
import argparse
import json
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.2.0'
KP = {'id': '49eaf082-07de-5468-a2d7-4cdfce27a553', 'db_id': 17592186087887,
      'title': 'Solving a Homogeneous Differential Equation'}
SOURCES = {
 'power': ('q-8843', 'ecc5b0a4-8e5a-5917-a8c3-d4ab3b2b520d', 'moderate', None, 0),
 'square_log': ('q-8844', '19530196-afb6-5c10-98a9-988afc75a28c', 'moderate', 'moderate', 4),
 'inverse_square': ('q-14318', 'c139f739-608f-51ea-bcb4-01f8a92a8c21', 'moderate', 'moderate', 3),
 'factor_cancel': ('q-14321', '30f68eaf-916e-557d-ad03-5e30a2efe0b7', 'moderate', 'moderate', 1),
 'nested_log': ('q-8845', 'b284307a-7bac-5101-a812-75d87d197409', 'moderate', 'moderate', 3),
 'square_implicit': ('q-90688', '51ab68ae-6386-58f8-941d-fb2c589605a8', 'moderate', 'moderate', 2),
 'cube_root': ('q-90691', '2b4ed6f3-beb2-5be5-83cb-e8d41e7b8f3b', 'easy', 'easy', 3),
 'affine': ('q-90692', 'ed854c8a-5a47-5533-b48c-04deb7b81625', 'easy', 'easy', 3),
 'linear_log': ('q-90693', '73b06f86-eb7f-5333-916f-45bb6952f791', 'easy', 'easy', 2),
}
D = r'\frac{\mathrm{d}y}{\mathrm{d}x}'
V = r'\frac{\mathrm{d}v}{\mathrm{d}x}'
L = r'\ln|x|'

def coef(a):
    return '' if a == 1 else '-' if a == -1 else str(a)

def simplify_signs(text):
    """Resolve adjacent signs from substituting a signed integer into a term."""
    return text.replace('+-', '-').replace('--', '+')

def display(tex):
    return '\n\n$$\n' + tex + '\n$$\n\n'

def aligned(rows):
    return display(r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}')

def identity(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:homogeneous-ode:' + text))

def domain(template):
    if template == 'nested_log':
        return r'$x\ne0$ and $y/x>0$'
    if template == 'factor_cancel':
        return r'$x\ne0$, $y\ne0$, and $y\ne-x$'
    if template in ('cube_root', 'power', 'square_log', 'inverse_square', 'square_implicit'):
        return r'$x\ne0$ and $y\ne0$'
    return r'$x\ne0$'

def components(t, a):
    """All prompt, bank and solution mathematics derive from (template, a)."""
    c, c2, c3 = coef(a), str(2*a), str(3*a)
    note = ''
    if t == 'power':
        ode = rf'\frac{{{c}x^2+3y^2}}{{2xy}}'
        bank = [rf'y^2=Kx^3-{c}x^2', rf'y^2=Kx^3+{2*a}x^2',
                rf'y^3=Kx^3-{c}x', rf'y^2=Kx^4+{c}x^2', rf'y^2=Kx^4-{3*a}x^3']
        sub = [rf'x{V}+v&=\frac{{{a}x^2+3(vx)^2}}{{2x(vx)}}',
               rf'x{V}+v&=\frac{{{a}+3v^2}}{{2v}}',
               rf'x{V}&=\frac{{{a}+v^2}}{{2v}}', rf'\frac{{2v}}{{{a}+v^2}}{V}&=\frac{{1}}{{x}}']
        integ = [rf'\int\frac{{2v}}{{{a}+v^2}}\,\mathrm{{d}}v&=\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\ln({a}+v^2)&={L}+C_1', rf'{a}+v^2&=Kx', rf'v^2&=Kx-{a}']
        back = [rf'\frac{{y^2}}{{x^2}}&=Kx-{a}', rf'y^2&=Kx^3-{c}x^2']
        note = r'Here $K$ absorbs the exponential constant and the sign of $x$ on the interval. Use real branches where the original equation is defined.'
    elif t == 'square_log':
        ode = rf'\frac{{y^2-{c}x^2}}{{xy}}'
        bank = [rf'y^2={c}x\ln(Cx^3+x)', rf'y^2=-{c}x^3+Cx^2',
                rf'y^2={c}x\ln x+Cx^3', rf'y^3={c}x^2\ln(x^2+Cx)', rf'y^2=-{c}x^2\ln(x^2)+Cx^2']
        sub = [rf'x{V}+v&=\frac{{(vx)^2-{c}x^2}}{{x(vx)}}',
               rf'x{V}+v&=\frac{{v^2-{a}}}{{v}}',
               rf'x{V}&=\frac{{v^2-{a}}}{{v}}-v=-\frac{{{a}}}{{v}}', rf'v{V}&=-\frac{{{a}}}{{x}}']
        integ = [rf'\int v\,\mathrm{{d}}v&=-{c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\frac{{v^2}}{{2}}&=-{c}{L}+C_1', rf'v^2&=-{2*a}{L}+C']
        back = [rf'\frac{{y^2}}{{x^2}}&=-{2*a}{L}+C', rf'\frac{{y^2}}{{x^2}}&=-{c}\ln(x^2)+C',
                rf'y^2&=-{c}x^2\ln(x^2)+Cx^2']
        note = r'Here $C=2C_1$; use $2\ln|x|=\ln(x^2)$.'
    elif t == 'inverse_square':
        ode = rf'\frac{{{c}yx}}{{y^2+{c}x^2}}'
        bank = [rf'\ln|y|-{c}\frac{{y}}{{x}}=C', rf'\ln\left|\frac{{x^3}}{{y}}\right|+{2*a}\frac{{y}}{{x}}=C',
                rf'\ln\left|\frac{{y^2}}{{x^3}}\right|-{c}\frac{{x^2}}{{y^2}}=C',
                rf'2\ln|y|-{c}\frac{{x^2}}{{y^2}}=C', rf'2\ln\left|\frac{{y}}{{x^2}}\right|+{c}\frac{{y^2}}{{x^2}}=C']
        sub = [rf'x{V}+v&=\frac{{{c}(vx)x}}{{(vx)^2+{c}x^2}}',
               rf'x{V}+v&=\frac{{{c}v}}{{v^2+{a}}}',
               rf'x{V}&=\frac{{{c}v}}{{v^2+{a}}}-v=-\frac{{v^3}}{{v^2+{a}}}',
               rf'\frac{{v^2+{a}}}{{v^3}}{V}&=-\frac{{1}}{{x}}']
        integ = [rf'\int\frac{{v^2+{a}}}{{v^3}}\,\mathrm{{d}}v&=-\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\int\left(\frac{{1}}{{v}}+\frac{{{a}}}{{v^3}}\right)\,\mathrm{{d}}v&=-{L}+C_1',
                 rf'\ln|v|-\frac{{{a}}}{{2v^2}}&=-{L}+C_1', rf'2\ln|v|-\frac{{{a}}}{{v^2}}&=-2{L}+C']
        back = [rf'2\ln\left|\frac{{y}}{{x}}\right|-{c}\frac{{x^2}}{{y^2}}&=-2{L}+C',
                rf'2\ln\left|\frac{{y}}{{x}}\right|+2{L}-{c}\frac{{x^2}}{{y^2}}&=C',
                rf'2\ln|y|-{c}\frac{{x^2}}{{y^2}}&=C']
        note = r'Here $C=2C_1$. The constant solution $y=0$ was excluded by the question; division by $v$ is therefore valid.'
    elif t == 'factor_cancel':
        ode = rf'\frac{{y^3+xy^2+{c}x^2y+{c}x^3}}{{xy^2+x^2y}}'
        bank = [rf'y^2=x({c}{L}+C)', rf'y^2=x^2({2*a}{L}+C)', rf'y^2=x^2(-{c}{L}+C)',
                rf'y^2=x(-{2*a}{L})+C', rf'y^2=x^2({c}{L})+C']
        sub = [rf'x{V}+v&=\frac{{(vx)^3+x(vx)^2+{c}x^2(vx)+{c}x^3}}{{x(vx)^2+x^2(vx)}}',
               rf'x{V}+v&=\frac{{v^3+v^2+{c}v+{a}}}{{v^2+v}}',
               rf'x{V}&=\frac{{v^3+v^2+{c}v+{a}}}{{v^2+v}}-v',
               rf'x{V}&=\frac{{{c}(v+1)}}{{v(v+1)}}=\frac{{{a}}}{{v}}', rf'v{V}&=\frac{{{a}}}{{x}}']
        integ = [rf'\int v\,\mathrm{{d}}v&={c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\frac{{v^2}}{{2}}&={c}{L}+C_1', rf'v^2&={2*a}{L}+C']
        back = [rf'\frac{{y^2}}{{x^2}}&={2*a}{L}+C', rf'y^2&=x^2({2*a}{L}+C)']
        note = r'Here $C=2C_1$. The original denominator excludes $v=0$ and $v=-1$, so the cancellation is valid only on those intervals.'
    elif t == 'nested_log':
        xp = 'x' if a == 1 else rf'x^{{{a}}}'
        ode = rf'\frac{{y}}{{x}}\left({c}\ln\left(\frac{{y}}{{x}}\right)+1\right)'
        bank = [rf'y=x^2+e^{{K{xp}}}', rf'y=Ke^{{{xp}}}', rf'y=K(2+e^{{3{xp}}})',
                rf'y=xe^{{K{xp}}}', rf'y=Kx^2+e^{{{xp}}}']
        sub = [rf'x{V}+v&=\frac{{vx}}{{x}}\left({c}\ln\left(\frac{{vx}}{{x}}\right)+1\right)',
               rf'x{V}+v&=v({c}\ln v+1)', rf'x{V}&={c}v\ln v',
               rf'\frac{{1}}{{v\ln v}}{V}&=\frac{{{a}}}{{x}}']
        integ = [rf'\int\frac{{1}}{{v\ln v}}\,\mathrm{{d}}v&={c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 r'u&=\ln v,\qquad \frac{\mathrm{d}u}{\mathrm{d}v}=\frac{1}{v}',
                 rf'\int\frac{{1}}{{u}}\,\mathrm{{d}}u&={c}{L}+C', rf'\ln|\ln v|&={c}{L}+C']
        back = [rf'\ln\left|\ln\frac{{y}}{{x}}\right|&={c}{L}+C',
                rf'\left|\ln\frac{{y}}{{x}}\right|&=e^C|x|^{{{a}}}',
                rf'\ln\frac{{y}}{{x}}&=K{xp}', rf'\frac{{y}}{{x}}&=e^{{K{xp}}}', rf'y&=xe^{{K{xp}}}']
        note = r'The signed constant $K$ absorbs $e^C$ and the fixed sign of $x$ on the interval. The division by $\ln v$ excluded $v=1$; restoring it allows $K=0$, giving $y=x$.'
    elif t == 'square_implicit':
        ode = rf'\frac{{y^3}}{{xy^2+{c}x^3}}'
        bank = [rf'\frac{{y^4}}{{C-{c}\ln(y^2)}}=2x', rf'\frac{{1}}{{C+{c}\ln(y^2)}}=x^2',
                rf'\frac{{y^2}}{{C-{c}\ln(y^2)}}=x^2', rf'\frac{{y^2}}{{C+{c}\ln(y^2)}}=2x^3',
                rf'\frac{{1}}{{C-{c}\ln(y^2)}}=4x']
        sub = [rf'x{V}+v&=\frac{{(vx)^3}}{{x(vx)^2+{c}x^3}}',
               rf'x{V}+v&=\frac{{v^3}}{{v^2+{a}}}',
               rf'x{V}&=\frac{{v^3}}{{v^2+{a}}}-v=-\frac{{{c}v}}{{v^2+{a}}}',
               rf'\frac{{v^2+{a}}}{{v}}{V}&=-\frac{{{a}}}{{x}}']
        integ = [rf'\int\frac{{v^2+{a}}}{{v}}\,\mathrm{{d}}v&=-{c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\int\left(v+\frac{{{a}}}{{v}}\right)\,\mathrm{{d}}v&=-{c}{L}+C_1',
                 rf'\frac{{v^2}}{{2}}+{c}\ln|v|&=-{c}{L}+C_1', rf'v^2+{c}\ln(v^2)&=-{c}\ln(x^2)+C']
        back = [rf'\frac{{y^2}}{{x^2}}+{c}\ln\left(\frac{{y^2}}{{x^2}}\right)&=-{c}\ln(x^2)+C',
                rf'\frac{{y^2}}{{x^2}}+{c}\ln(y^2)-{c}\ln(x^2)&=-{c}\ln(x^2)+C',
                rf'\frac{{y^2}}{{x^2}}+{c}\ln(y^2)&=C', rf'\frac{{y^2}}{{x^2}}&=C-{c}\ln(y^2)',
                rf'\frac{{y^2}}{{C-{c}\ln(y^2)}}&=x^2']
        note = r'Here $C=2C_1$. The constant solution $y=0$ was excluded by the question. On the nonzero solution, the final denominator equals $y^2/x^2>0$.'
    elif t == 'cube_root':
        ode = rf'\frac{{{c}x^3+y^3}}{{xy^2}}'
        bank = [rf'y=x({3*a}{L}+C)', rf'y=x\sqrt{{{c}{L}+C}}', rf'y=x({2*a}{L}+C)^2',
                rf'y=x\sqrt[3]{{{3*a}{L}+C}}', rf'y=x^2({3*a}{L}+C)']
        sub = [rf'x{V}+v&=\frac{{{c}x^3+(vx)^3}}{{x(vx)^2}}',
               rf'x{V}+v&=\frac{{{a}+v^3}}{{v^2}}=\frac{{{a}}}{{v^2}}+v',
               rf'x{V}&=\frac{{{a}}}{{v^2}}', rf'v^2{V}&=\frac{{{a}}}{{x}}']
        integ = [rf'\int v^2\,\mathrm{{d}}v&={c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\frac{{v^3}}{{3}}&={c}{L}+C_1', rf'v^3&={3*a}{L}+C']
        back = [rf'\left(\frac{{y}}{{x}}\right)^3&={3*a}{L}+C', rf'y^3&=x^3({3*a}{L}+C)',
                rf'y&=x\sqrt[3]{{{3*a}{L}+C}}']
        note = r'Here $C=3C_1$ and the cube root is real. Restrict the solution to intervals where $y\ne0$.'
    elif t == 'affine':
        ode = rf'\frac{{{c}x+2y}}{{x}}'
        bank = [rf'y=Cx^3-{c}x^2', rf'y=Cx^3-{2*a}x', rf'y=Cx^3+{c}x',
                rf'y=Cx^2-{c}x', rf'y=Cx^2+{2*a}x']
        sub = [rf'x{V}+v&=\frac{{{c}x+2(vx)}}{{x}}', rf'x{V}+v&={a}+2v',
               rf'x{V}&={a}+v', rf'\frac{{1}}{{{a}+v}}{V}&=\frac{{1}}{{x}}']
        integ = [rf'\int\frac{{1}}{{{a}+v}}\,\mathrm{{d}}v&=\int\frac{{1}}{{x}}\,\mathrm{{d}}x',
                 rf'\ln|v+{a}|&={L}+C_1', rf'|v+{a}|&=e^{{C_1}}|x|',
                 rf'v+{a}&=Cx', rf'v&=Cx-{a}']
        back = [rf'\frac{{y}}{{x}}&=Cx-{a}', rf'y&=Cx^2-{c}x']
        note = rf'The signed constant $C$ absorbs $e^{{C_1}}$. Division by $v+{a}$ excluded $v=-{a}$; restoring it permits $C=0$, giving $y=-{c}x$.'
    elif t == 'linear_log':
        ode = rf'\frac{{{c}x+y}}{{x}}'
        bank = [rf'y={c}{L}+Cx^2', rf'y={c}{L}+Cx', rf'y={c}x{L}+Cx',
                rf'y={c}x{L}+C', rf'y={2*a}x{L}+Cx^2']
        sub = [rf'x{V}+v&=\frac{{{c}x+(vx)}}{{x}}', rf'x{V}+v&={a}+v',
               rf'x{V}&={a}', rf'{V}&=\frac{{{a}}}{{x}}']
        integ = [rf'\int\mathrm{{d}}v&={c}\int\frac{{1}}{{x}}\,\mathrm{{d}}x', rf'v&={c}{L}+C']
        back = [rf'\frac{{y}}{{x}}&={c}{L}+C', rf'y&={c}x{L}+Cx']
    else:
        raise ValueError('Unknown template')
    return (simplify_signs(ode),
            *([simplify_signs(row) for row in rows] for rows in (bank, sub, integ, back)),
            simplify_signs(note))

EASY_TEMPLATES = ('cube_root', 'affine', 'linear_log')
EASY_COEFFICIENTS = tuple(range(-9, 0)) + tuple(range(1, 10))

def coefficient_bank(index):
    """A bank is chosen before its answer-bearing prompt coefficient."""
    if not isinstance(index, int) or not 0 <= index < len(EASY_COEFFICIENTS):
        raise ValueError('Unsupported bank index')
    return tuple(EASY_COEFFICIENTS[(index+i) % len(EASY_COEFFICIENTS)] for i in range(5))

def easy_answer(template, a):
    if template == 'cube_root':
        return rf'y=x\sqrt[3]{{{3*a}{L}+C}}'
    if template == 'affine':
        return simplify_signs(rf'y=Cx^2-{coef(a)}x')
    return rf'y={coef(a)}x{L}+Cx'

@checked_math_content
def generate(template, a, seed=0, *, source_replay=False, bank_index=None):
    if template not in SOURCES or a not in values(template):
        raise ValueError('Unsupported template or parameter')
    source_name, source_id, difficulty, original_difficulty, correct = SOURCES[template]
    ode, bank, sub, integ, back, note = components(template, a)
    if source_replay and (a != 1 or bank_index is not None):
        raise ValueError('Source replay requires original parameters and bank')
    if template in EASY_TEMPLATES and not source_replay:
        if bank_index is None:
            compatible = [i for i in range(len(EASY_COEFFICIENTS)) if a in coefficient_bank(i)]
            bank_index = random.Random(f'{seed}:{template}:{a}:bank').choice(compatible)
        candidates = coefficient_bank(bank_index)
        if a not in candidates:
            raise ValueError('Prompt coefficient must be in the selected bank')
        bank = [easy_answer(template, b) for b in candidates]
        # Independent of the target: controlled changes retain exactly the same bank.
        random.Random(f'{seed}:{template}:{bank_index}:order').shuffle(bank)
        correct = bank.index(easy_answer(template, a))
    prompt = ('Find the general solution of the following differential equation.' if template in ('square_log', 'factor_cancel')
              else 'Use the transformation $y=v(x)x$ to find the general solution of the following homogeneous differential equation.')
    if template in ('inverse_square', 'square_implicit'):
        prompt += r' Consider the solutions with $y\ne0$.'
    prompt += display(D+'='+ode)
    solution = ''
    if template in ('square_log', 'factor_cancel'):
        order = '2 (quadratic)' if template == 'square_log' else '3 (cubic)'
        solution += f'This is a homogeneous equation because all terms in the numerator and denominator have degree {order}.\n\n'
    solution += 'With $y=v(x)x$, we have' + aligned([D+rf'&=x{V}+v\frac{{\mathrm{{d}}}}{{\mathrm{{d}}x}}(x)', rf'&=x{V}+v'])
    solution += 'Substituting the above into our differential equation gives' + aligned(sub)
    solution += 'Integrating both sides with respect to $x$, we obtain' + aligned(integ)
    solution += 'From the transformation $y=vx$, we get' + display(r'v=\frac{y}{x}.')
    solution += 'Substituting the above into our solution, we finally obtain' + aligned(back)
    solution += note + '\n\nThe solution is used on intervals where ' + domain(template) + '.'
    prompt, solution = normalize_prose(prompt.strip()), normalize_prose(solution.strip())
    bank = [normalize_tex(b) for b in bank]
    # Identity includes the complete profile and answer content, independent of seed.
    qid = identity(json.dumps([VERSION, template, a, prompt, solution, bank], ensure_ascii=False))
    fid = identity(qid+':selection')
    choices = [{':answer/id': identity(fid+':'+b), ':answer/type': ':answer.type/math', ':answer/value': b} for b in bank]
    return {'knowledge_point': KP.copy(), 'question': {
        ':question/id': qid, ':question/difficulty': ':question.difficulty/'+difficulty,
        ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
          ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
          ':answer-field/correct': [':answer/id', choices[correct][':answer/id']]}]},
      'generation': {'generator_version': VERSION, 'seed': seed, 'template': template,
        'parameters': {'a': a},
        'profile': ('coefficient-alternatives' if template in EASY_TEMPLATES and not source_replay else source_name+'-complete-bank'),
        'bank_index': bank_index, 'source_replay': source_replay,
        'source_question_ids': [source_id],
        'source_math_academy_id': source_name, 'original_difficulty': original_difficulty,
        'source_basis': 2793, 'extension': a != 1 or (template in EASY_TEMPLATES and not source_replay), 'domain': domain(template),
        'source_repair': template == 'power', 'dependencies': {'python': '3.13.5', 'packages': {}}}}

def values(template):
    if template in ('cube_root', 'affine', 'linear_log'):
        return EASY_COEFFICIENTS
    return range(1, 5 if template == 'nested_log' else 10)

def replay_source(template, seed=0):
    return generate(template, 1, seed, source_replay=True)

def generate_batch(difficulty='easy', count=5, seed=0):
    if difficulty == 'unclassified':
        difficulty = 'easy'
    if difficulty not in ('easy', 'moderate'):
        raise ValueError('Unsupported difficulty: '+difficulty)
    if count < 0:
        raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    templates = [t for t, s in SOURCES.items() if s[2] == difficulty]
    # Each cycle covers every semantic instance. Interleave families for short batches.
    result = []
    if difficulty == 'easy':
        while len(result) < count:
            order = list(EASY_TEMPLATES)
            rng.shuffle(order)
            for t in order:
                if len(result) == count:
                    break
                bank_index = rng.randrange(len(EASY_COEFFICIENTS))
                a = rng.choice(coefficient_bank(bank_index))
                result.append(generate(t, a, seed, bank_index=bank_index))
        return result
    while len(result) < count:
        slots = {t: list(values(t)) for t in templates}
        for v in slots.values():
            rng.shuffle(v)
        while any(slots.values()) and len(result) < count:
            order = [t for t in templates if slots[t]]
            rng.shuffle(order)
            for t in order:
                if len(result) == count:
                    break
                result.append(generate(t, slots[t].pop(), seed))
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=['easy', 'moderate', 'hard', 'unclassified'])
    parser.add_argument('--count', default=5, type=int)
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--format', default='json', choices=['json'])
    args = parser.parse_args()
    try:
        records = generate_batch(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
