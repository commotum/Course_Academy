#!/usr/bin/env python3
"""Seeded vertical-base trapezoid area questions; no publication or database access."""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186105938-source-policy.json'))
    raise SystemExit(0)

import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

HERE = Path(__file__).resolve().parent
SOURCES = json.loads((HERE / 'source_cases.json').read_text())
VERSION = '1.0.2'
TITLE = 'Calculating the Area of a Trapezoid With Vertical Bases'
PROFILES = ('q-53181', 'q-53246')
DEPENDENCIES = {'python': '3.13.5', 'packages': {'matplotlib': '3.11.2'}}


def number(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    # The bounded domain uses terminating decimals only.
    return str(float(value)).rstrip('0').rstrip('.')


def uid(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:vertical-trapezoid:' + text))


def bank(a, b, h, profile):
    a, b, h = map(Fraction, (a, b, h))
    area = (a + b) * h / 2
    if profile == 'q-53181':
        values = [h*h, area, area-1, 2*area, area+1]
        recipes = ['h^2', 'A', 'A-1', '2A', 'A+1']
    elif profile == 'q-53246':
        values = [area-10, area, a+b, abs(a-b)*h/2, area/2]
        recipes = ['A-10', 'A', 'a+b', '|a-b|h/2', 'A/2']
    else:
        raise ValueError('Unknown bank profile')
    if min(values) <= 0 or len(set(values)) != 5:
        raise ValueError('Profile has nonpositive or colliding choices')
    return values, recipes


def valid_parameters(a, b, h):
    halves = {Fraction(k, 2) for k in range(3, 20, 2)}
    integers = {Fraction(k) for k in range(2, 10)}
    return ((a in halves and b in integers) or (b in halves and a in integers)) and h in (4, 6, 8, 10)


def plot(a, b, h, output_dir):
    """Coordinates preserve the actual given lengths and perpendicular height."""
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR', str(output / '.matplotlib-cache'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    from matplotlib.patches import Polygon
    relative = 'generated/trapezoid-' + hashlib.sha256(f'{a},{b},{h},v3'.encode()).hexdigest()[:24] + '.png'
    path = output / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return relative
    af, bf, hf = map(float, (a, b, h))
    left = [(0, -af/2), (0, af/2)]
    right = [(hf, -bf/2), (hf, bf/2)]
    top = min(af, bf)/2
    fig, ax = plt.subplots(figsize=(5.2, 3.6), dpi=140)
    ax.add_patch(Polygon([left[0], right[0], right[1], left[1]], facecolor='#eaf4fb', edgecolor='#111111', linewidth=1.8))
    ax.plot([0, hf], [top, top], color='#4389b9', linestyle=(0, (4, 4)), linewidth=1)
    size = min(min(hf, af, bf)*0.2, max(hf, af, bf)*0.03)
    end = hf if bf > af else 0
    inner = end-size if end else size
    ax.add_patch(Polygon([(end, top), (inner, top), (inner, top-size), (end, top-size)], facecolor='#297bb5', edgecolor='none'))
    pad = max(af, bf, hf)*0.055
    for name, (x,y), dx, dy in [('P',left[0],-pad,-pad), ('Q',right[0],pad,-pad), ('R',right[1],pad,pad), ('S',left[1],-pad,pad)]:
        ax.text(x+dx, y+dy, '$'+name+'$', fontsize=14, ha='center', va='center')
    ax.text(-pad, 0, number(a), ha='right', va='center', fontsize=13)
    ax.text(hf+pad, 0, number(b), ha='left', va='center', fontsize=13)
    ax.text(hf/2, top-pad/2, number(h), ha='center', va='top', fontsize=13,
            bbox={'facecolor':'#eaf4fb','edgecolor':'none','pad':1})
    margin = max(af, bf, hf)*0.19
    ax.set_xlim(-margin, hf+margin)
    ax.set_ylim(-max(af,bf)/2-margin, max(af,bf)/2+margin)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(path, facecolor='white', metadata={'Software':'Course Academy trapezoid generator 1.0.0'})
    plt.close(fig)
    return relative


def solution(a, b, h):
    aa, bb, hh = map(number, (a, b, h))
    total, half, area = map(number, (a+b, h/2, (a+b)*h/2))
    return normalize_prose(r'''The area of a trapezoid is given by

$$
\mathcal{A} = \dfrac{(a+b) \cdot h}{2}
$$

where $a,b$ are lengths of the bases and $h$ is the height of the trapezoid.

In our case, we have

$$
a = PS = AA, \qquad b = QR = BB, \qquad h = HH
$$

Therefore, the area of our trapezoid is

$$
\begin{aligned}
A &= \dfrac{(AA + BB) \cdot HH}{2} \\
&= TOTAL \cdot HALF \\
&= AREA
\end{aligned}
$$'''.replace('AA', aa).replace('BB', bb).replace('HH', hh).replace('TOTAL', total).replace('HALF', half).replace('AREA', area))


@checked_math_content
def generate(a, b, h, profile, *, seed=0, output_dir=None, replay=False):
    a, b, h = map(Fraction, (a,b,h))
    if not valid_parameters(a,b,h):
        raise ValueError('Parameters are outside the declared easy domain')
    values, recipes = bank(a,b,h,profile)
    source = SOURCES[profile]
    if replay:
        if [number(x) for x in (a,b,h)] != source['parameters']:
            raise ValueError('Replay must use the original source parameters')
        asset = source['image']
    else:
        output_dir = output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not output_dir:
            raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for generated assets')
        relative_asset = plot(a,b,h,output_dir)
        # The runner resolves relative noncanonical paths against the package,
        # not OUTPUT_DIR. Serve the actual path without baking it into IDs.
        asset = str((Path(output_dir).resolve() / relative_asset).resolve())
    problem = normalize_prose(f'![]({asset})\n\nWhat is the area of the trapezoid $PQRS$?')
    worked = solution(a,b,h)
    answer_values = [normalize_tex(number(v)) for v in values]
    identity_problem = problem if replay else problem.replace(asset, relative_asset)
    identity = json.dumps([identity_problem,worked,answer_values,profile], separators=(',',':'))
    qid = uid(identity)
    fid = uid(qid+':selection')
    choices = [{':answer/id':uid(fid+':'+v), ':answer/type':':answer.type/math', ':answer/value':v} for v in answer_values]
    question = {':question/id':qid, ':question/difficulty':':question.difficulty/easy',
                ':question/problem':problem, ':question/worked-solution':worked,
                ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'selection',
                    ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
                    ':answer-field/correct':[':answer/id',choices[1][':answer/id']]}]}
    return {'knowledge_point':{'db_id':17592186105938, 'id':'56c575a7-577f-5439-a366-7e0ef287d0a5','title':TITLE},
            'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':'vertical-bases-area','bank_profile':profile,
                'recipes':recipes,'parameters':{'a':number(a),'b':number(b),'h':number(h)},
                'source_question_ids':[source['id']], 'source_basis':2890,'source_difficulty':None,
                'difficulty_assignment':'authored easy: direct substitution', 'source_replay':replay,
                'dependencies':DEPENDENCIES, 'domain':'one half-integer base 1.5..9.5; one integer base 2..9; h in 4,6,8,10',
                'semantic_instance':','.join(map(number, [min(a,b),max(a,b),h])),
                'asset':asset}}


def allocate(count, seed):
    """Plan both profile quotas without rendering or exhausting shared candidates."""
    # Distinct numerical triples, ignoring mirrored base positions and bank changes.
    candidates = [(Fraction(k,2), Fraction(j), Fraction(h)) for k in range(3,20,2) for j in range(2,10) for h in (4,6,8,10)]
    eligible = {}
    for triple in candidates:
        profiles = set()
        for profile in PROFILES:
            try:
                bank(*triple, profile)
            except ValueError:
                continue
            profiles.add(profile)
        if profiles:
            eligible[triple] = profiles
    available = {p: sum(p in ps for ps in eligible.values()) for p in PROFILES}
    def quotas(n):
        return {p: n//2 + int(n % 2 and p == PROFILES[seed % 2]) for p in PROFILES}
    capacity = max(n for n in range(len(eligible)+1)
                   if all(quotas(n)[p] <= available[p] for p in PROFILES))
    if not 0 <= count <= capacity:
        raise ValueError(f'count must be between 0 and {capacity} distinct instances')
    needed = quotas(count)
    rng = random.Random(seed)
    rng.shuffle(candidates)
    plan = []
    while len(plan) < count:
        profile = PROFILES[(seed+len(plan))%2]  # Complete profile chosen first.
        other = PROFILES[(seed+len(plan)+1)%2]
        for index, (a,b,h) in enumerate(candidates):
            compatible = eligible.get((a,b,h), set())
            if profile not in compatible:
                continue
            # Removing a shared triple must leave the other quota feasible.
            if other in compatible and available[other] <= needed[other]:
                continue
            candidates.pop(index)
            for p in compatible:
                available[p] -= 1
            needed[profile] -= 1
            if rng.randrange(2):
                a,b = b,a
            plan.append((a,b,h,profile))
            break
        else:
            raise AssertionError('Feasible two-profile allocation was not completed')
    return plan


def sample(count, seed, output_dir=None):
    plan = allocate(count, seed)
    return [generate(a,b,h,profile,seed=seed,output_dir=output_dir)
            for a,b,h,profile in plan]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['easy','moderate','hard','unclassified'], default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', choices=PROFILES)
    args = parser.parse_args()
    if args.difficulty not in ('easy','unclassified'):
        parser.error('Unsupported difficulty: only easy is source-justified')
    try:
        if args.replay_source:
            source = SOURCES[args.replay_source]
            result = [generate(*source['parameters'],args.replay_source,seed=args.seed,replay=True)]
        else:
            result = sample(args.count,args.seed)
    except ValueError as error:
        parser.error(str(error))
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write('\n')



from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186105938-source-policy.json'))

if __name__ == '__main__':
    main()
