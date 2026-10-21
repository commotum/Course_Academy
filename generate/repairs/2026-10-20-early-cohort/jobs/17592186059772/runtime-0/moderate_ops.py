"""Single row-addition family; exact source banks are replay-only profiles."""
import copy
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path

COEFFICIENTS = (-3, -2, -1, 1, 2, 3)
ORDINAL = ('first', 'second', 'third')


@lru_cache(maxsize=1)
def source_data():
    return json.loads(Path(__file__).with_name('moderate_sources.json').read_text())


def sources():
    return [copy.deepcopy(item['instance']) for item in source_data()]


def add(inst, coefficient=None):
    out = [[Fraction(x) for x in row] for row in inst['matrix']]
    t, d = inst['target'], inst['donor']
    k = Fraction(inst['coefficient'] if coefficient is None else coefficient)
    out[t] = [x + k*y for x, y in zip(out[t], out[d])]
    return out


def bank(inst):
    if inst['profile'].startswith('source:'):
        item = next(x for x in source_data() if x['instance']['profile'] == inst['profile'])
        for name in ('matrix', 'target', 'donor', 'coefficient'):
            if inst[name] != item['instance'][name]:
                raise ValueError('Source-only bank cannot be used with changed mathematical parameters')
        return copy.deepcopy(item['bank']), item['correct_index'], item['recipes'][:]
    if inst['profile'] != 'add-factor-comparison':
        raise ValueError('Unknown moderate bank profile')
    factors = [inst['coefficient']] + inst['wrong_coefficients']
    if len(factors) != 5 or len(set(factors)) != 5 or not set(factors) <= set(COEFFICIENTS):
        raise ValueError('Expected five distinct permitted coefficients')
    return [add(inst, k) for k in factors], 0, ['correct'] + [f'coefficient:{k}' for k in factors[1:]]


def sample(rng):
    n, width = rng.choice(((2, 3), (3, 4)))
    t, d = rng.sample(range(n), 2)
    k = rng.choice(COEFFICIENTS)
    inst = dict(template='add', profile='add-factor-comparison', target=t, donor=d,
                coefficient=k, wrong_coefficients=rng.sample([v for v in COEFFICIENTS if v != k], 4))
    for attempt in range(1, 1001):
        m = [[rng.randint(-9, 9) for _ in range(width)] for _ in range(n)]
        if not any(m[d]):
            continue
        inst.update(matrix=m, entry_attempts=attempt, letter=rng.choice(('A', 'M', 'N', 'T', 'U', 'V', 'X')))
        return inst
    raise RuntimeError('Unable to sample nonzero donor')


def render(inst, matrix, tex):
    t, d, k = inst['target'], inst['donor'], inst['coefficient']
    letter = inst['letter']
    row = lambda i: rf'R_{{{i+1}}}'
    operation = row(t) + ':=' + row(t) + '+(' + tex(k) + r')\cdot ' + row(d)
    original = matrix(inst['matrix'])
    expanded = [[tex(x) for x in r] for r in inst['matrix']]
    expanded[t] = [tex(x) + '+(' + tex(k) + ')(' + tex(y) + ')'
                   for x, y in zip(inst['matrix'][t], inst['matrix'][d])]
    expansion = matrix(expanded)
    if len(inst['matrix'][0]) == 4:
        expansion = r'{\scriptsize ' + expansion + '}'
    problem = (f'Consider the augmented matrix ${letter},$ given by\n\n$$\n{letter}={original}.\n$$\n\n'
               f'What matrix results from carrying out the row operation ${operation}$ on ${letter}?$')
    if len(inst['matrix'][0]) == 4:
        # Give each stage the full display width; a shared alignment column
        # otherwise clips the last expanded entry in the learning UI.
        steps = (f'{letter}=' + original + r'\,' + operation
                 + '\n$$\n\n$$\n' + r'\sim ' + expansion
                 + '\n$$\n\n$$\n' + r'\sim ' + matrix(add(inst)))
    else:
        steps = (r'\begin{aligned}' + f'{letter} &= ' + original + r'\,' + operation
                 + r' \\ &\sim ' + expansion + r' \\ &\sim ' + matrix(add(inst))
                 + r'\end{aligned}')
    solution = (f'The operation ${operation}$ means that we need to add ${tex(k)}$ times the '
                f'{ORDINAL[d]} row to the {ORDINAL[t]} row.\n\n'
                'Applying this row operation, we obtain the following:\n\n$$\n'
                + steps + '\n$$')
    return problem, solution
