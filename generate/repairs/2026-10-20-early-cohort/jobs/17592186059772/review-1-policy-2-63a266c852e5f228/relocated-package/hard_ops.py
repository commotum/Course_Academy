"""Two-operation hard families. Source banks are explicit replay profiles."""
import copy
import math
from fractions import Fraction

HARD_SOURCES = {
    'swap-donor': '25230851-35bf-5052-9d49-2045d4671518',
    'swap-recipient': '56624c75-a028-5dc9-962f-9700b721674f',
    'scale-donor': '4f7e0cb8-b82b-5c57-8695-0b8e08268369',
}
COEFFICIENTS = (-3, -2, -1, 1, 2, 3)
SCALES = ('-3', '-2', '-1/2', '1/2', '-1/3', '1/3', '2', '3')
ORDINAL = ('first', 'second', 'third')


def sources():
    return [
        dict(template='swap-add', matrix=[[-1, 9, -2, 6], [4, 4, 6, 7], [9, 0, 5, 7]],
             pair=[0, 2], target=1, donor=2, coefficient=-1, letter='V', profile='swap-donor'),
        dict(template='scale-add', matrix=[[1, 0, 2, -2], [0, 2, 0, 6], [0, -1, -3, 4]],
             donor=1, target=2, scale='1/2', coefficient=1, letter='U', profile='scale-donor'),
        dict(template='swap-add', matrix=[[1, 0, 0, 2], [4, 3, 2, 1], [1, -1, 0, 3]],
             pair=[1, 2], target=1, donor=0, coefficient=-1, letter='V', profile='swap-recipient'),
    ]


def intermediate(inst):
    m = [[Fraction(x) for x in row] for row in inst['matrix']]
    if inst['template'] == 'swap-add':
        a, b = inst['pair']
        m[a], m[b] = m[b], m[a]
    else:
        d = inst['donor']
        m[d] = [Fraction(inst['scale'])*x for x in m[d]]
    return m


def add(m, t, d, k):
    out = copy.deepcopy(m)
    out[t] = [x + Fraction(k)*y for x, y in zip(m[t], m[d])]
    return out


def bank(inst):
    m = [[Fraction(x) for x in row] for row in inst['matrix']]
    stage = intermediate(inst)
    t, d, k = inst['target'], inst['donor'], Fraction(inst['coefficient'])
    correct = add(stage, t, d, k)
    profile = inst.get('profile', 'sequence-comparison')
    if profile == 'sequence-comparison':
        candidates = inst['candidates']
        if len(candidates) != 5:
            raise ValueError('Expected five candidate sequences')
        values, keys, recipes = [], [], []
        slot = 'pair' if inst['template'] == 'swap-add' else 'scale'
        for index, candidate in enumerate(candidates):
            other = dict(inst, **{slot: candidate[slot]})
            values.append(add(intermediate(other), t, d, candidate['coefficient']))
            if candidate[slot] == inst[slot] and candidate['coefficient'] == k:
                keys.append(index)
            recipes.append('first:' + str(candidate[slot]) + ';coefficient:' + str(candidate['coefficient']))
        if len(keys) != 1:
            raise ValueError('Exactly one candidate sequence must match both operations')
        return values, keys[0], recipes
    if profile == 'swap-donor':
        a, b = inst['pair']
        stale = add(m, t, d, k)
        stale_swapped = copy.deepcopy(stale)
        stale_swapped[a], stale_swapped[b] = stale_swapped[b], stale_swapped[a]
        wrong = copy.deepcopy(m)
        wrong[a], wrong[t] = wrong[t], wrong[a]
        wrong = add(wrong, t, d, k)
        return [stale, stale_swapped, wrong, correct, stage], 3, [
            'omit-swap', 'stale-donor', 'wrong-swap', 'correct', 'omit-add']
    if profile == 'swap-recipient':
        outs = [copy.deepcopy(correct) for _ in range(5)]
        outs[0][t] = [-x for x in correct[t]]
        for idx, second, last in ((1, -2, -1), (2, 2, -2), (4, 2, -1)):
            outs[idx][t][1] *= second
            outs[idx][t][3] *= last
        return outs, 3, ['negate-result', 'entry-pattern-1', 'entry-pattern-2', 'correct', 'entry-pattern-3']
    if profile == 'scale-donor':
        stale = add(m, t, d, k)
        extra = copy.deepcopy(stale)
        extra[t][1] += stage[d][1]
        partial = copy.deepcopy(m)
        partial[d][:-1] = stage[d][:-1]
        partial = add(partial, t, d, k)
        compound = copy.deepcopy(correct)
        compound[t] = [-x for x in correct[t]]
        compound[t][1] += stage[d][1]
        u = next(r for r in range(3) if r not in (t, d))
        compound[u][2] *= -1
        compound[u][3] *= -1
        return [stale, extra, correct, partial, compound], 2, [
            'omit-scale', 'omit-scale-extra-cell', 'correct', 'omit-constant-scaling', 'compound-signs']
    raise ValueError('Unknown hard profile')


def comparison_candidates(rng, inst):
    """Two first-operation cases, each with multiple second-operation cases.

    Either first case may own the key; neither its frequency nor its size identifies it.
    """
    slot = 'pair' if inst['template'] == 'swap-add' else 'scale'
    choices = [[0, 1], [0, 2], [1, 2]] if slot == 'pair' else list(SCALES)
    other = rng.choice([value for value in choices if value != inst[slot]])
    own_count = rng.choice((2, 3))
    own_coefficients = rng.sample(COEFFICIENTS, own_count)
    other_coefficients = rng.sample(COEFFICIENTS, 5-own_count)
    inst['coefficient'] = rng.choice(own_coefficients)
    inst['candidate_coefficients'] = own_coefficients
    inst['candidates'] = ([{slot: inst[slot], 'coefficient': k} for k in own_coefficients]
                          + [{slot: other, 'coefficient': k} for k in other_coefficients])
    inst['profile'] = 'sequence-comparison'


def sample(rng, template=None):
    template = template or rng.choice(('swap-add', 'scale-add'))
    inst = dict(template=template)
    if template == 'swap-add':
        inst['pair'] = sorted(rng.sample(range(3), 2))
    inst['donor'], inst['target'] = rng.sample(range(3), 2)
    if template == 'scale-add':
        inst['scale'] = rng.choice(SCALES)
    # Select first-operation alternatives and the key before arithmetic data.
    comparison_candidates(rng, inst)
    for attempt in range(1, 1001):
        inst['matrix'] = [[rng.randint(-9, 9) for _ in range(4)] for _ in range(3)]
        if template == 'scale-add':
            den = math.lcm(*(Fraction(c['scale']).denominator for c in inst['candidates']))
            bound = min(3, 9//den)
            inst['matrix'][inst['donor']] = [den*rng.randint(-bound, bound) for _ in range(4)]
        m = inst['matrix']
        if len({tuple(r) for r in m}) != 3 or any(not any(r) for r in m):
            continue
        # Both operations should affect the learner's state, not be numeric identities.
        stage = intermediate(inst)
        if stage == m or not any(stage[inst['donor']]):
            continue
        vals, _, _ = bank(inst)
        if len({tuple(tuple(r) for r in v) for v in vals}) == 5:
            inst.update(entry_attempts=attempt, letter=rng.choice(('A', 'M', 'N', 'T', 'U', 'V', 'X')))
            return inst
    raise RuntimeError('No compatible hard instance')


def render(inst, matrix, tex):
    t, d, k = inst['target'], inst['donor'], Fraction(inst['coefficient'])
    letter = inst['letter']
    row = lambda i: rf'R_{{{i+1}}}'
    if inst['template'] == 'swap-add':
        a, b = inst['pair']
        first = row(a) + r'\leftrightarrow ' + row(b)
        first_aligned = row(a) + r' &\leftrightarrow ' + row(b)
        meaning = f'swap the {ORDINAL[a]} and {ORDINAL[b]} rows.'
    else:
        first = row(d) + ':=' + tex(inst['scale']) + row(d)
        first_aligned = row(d) + ' &:=' + tex(inst['scale']) + row(d)
        meaning = f'multiply the {ORDINAL[d]} row of the matrix by ${tex(inst["scale"])}.$'
    second_rhs = row(t) + '+(' + tex(k) + r')\cdot ' + row(d)
    second = row(t) + ':=' + second_rhs
    second_aligned = row(t) + ' &:=' + second_rhs
    original = matrix(inst['matrix'])
    stage = intermediate(inst)
    final = add(stage, t, d, k)
    expanded = [[tex(x) for x in r] for r in stage]
    expanded[t] = [tex(x)+'+('+tex(k)+')('+tex(y)+')' for x, y in zip(stage[t], stage[d])]
    problem = (f'Consider the augmented matrix ${letter},$ given by\n\n$$\n{letter}={original}.\n$$\n\n'
               f'What matrix results from carrying out the following row operations on ${letter}?$\n\n$$\n'
               + r'\begin{aligned}' + first_aligned + r' \\ ' + second_aligned + r'\end{aligned}' + '\n$$')
    solution = ("Let's list the required operations:\n\n"
                f'- The operation ${first}$ means that we need to {meaning}\n\n'
                f'- The operation ${second}$ means that we need to add ${tex(k)}$ times the '
                f'{ORDINAL[d]} row to the {ORDINAL[t]} row.\n\n'
                'Applying the operations, we obtain the following:\n\n$$\n'
                + r'\begin{aligned}' + f'{letter} &= ' + original + r'\,' + first
                + r' \\ &\sim ' + matrix(stage) + r'\,' + second
                + r' \\ &\sim {\scriptsize ' + matrix(expanded) + r'} \\ &\sim ' + matrix(final)
                + r'\end{aligned}' + '\n$$')
    return problem, solution
