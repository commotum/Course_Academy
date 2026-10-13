#!/usr/bin/env python3
"""Bounded source-faithful hard line-identification families with exact arithmetic."""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import uuid
import sys
from pathlib import Path

if __name__ == '__main__' and (importlib.util.find_spec('sympy') is None or importlib.util.find_spec('matplotlib') is None):
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if interpreter.is_file() and str(interpreter) != sys.executable:
        os.execv(str(interpreter), [str(interpreter), __file__, *sys.argv[1:]])
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

KP_ID = 17592186054802
KP_UUID = '3986a3cd-c543-54e9-8d55-f744d9436313'
TITLE = 'Identifying a Line Given a Graph'
VERSION = 'graph-line-hard-v1'
PACKAGE = Path(__file__).with_suffix('')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SOURCE = json.loads((PACKAGE / 'source.json').read_text())
PROFILES = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED = ('q-71837', 'q-54293')
SOURCE_CASES = {'q-71837': {'b': 6, 't': 2}, 'q-54293': {'b': 2, 't': 4}}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), digest(value)))

def candidates(profile):
    # Explicit bounded extension of the observed positive intercepts and negative slopes.
    if profile == 'q-71837':
        return [{'b': k*t, 't': t} for k in (2, 3, 4, 5) for t in (1, 2, 3, 4)]
    if profile == 'q-54293':
        return [{'b': b, 't': t} for b in (1, 2, 3, 4) for t in (2, 3, 4, 6, 8)]
    raise ValueError('Unrated source profile is not a supported difficulty')

def line(parameters):
    b, t = sp.Rational(parameters['b']), sp.Rational(parameters['t'])
    return -b/t, b

def task_key(parameters):
    return digest([str(z) for z in line(parameters)])

def tex(value):
    return sp.latex(sp.Rational(value))

def objects(profile, p):
    m, b = line(p)
    if profile == 'q-71837':
        return [(m, b)] * 3
    return [(-b, -m), (m, b), (-m, b)]

def equations(profile, p):
    b, t = p['b'], p['t']
    c = sp.Rational(b, t)
    if profile == 'q-71837':
        k = int(c)
        return [f'y+{k}x={b}', rf'\frac{{1}}{{{k}}}y+x={t}', f'y=-{k}x+{b}']
    return [rf'y=-{b}x+{tex(c)}', rf'y=-{tex(c)}x+{b}', rf'y={tex(c)}x+{b}']

def plot(profile, p, role):
    q = PROFILES[profile]
    old = re.findall(r'!\[.*?\]\((.*?)\)', q[':question/problem' if role == 'prompt' else ':question/worked-solution'])[0]
    if p == SOURCE_CASES[profile]:
        return old, None
    m, b = line(p)
    t = p['t']
    signature = digest({'version': VERSION, 'line': [str(m), str(b)], 'role': role})
    local = PACKAGE / 'assets' / (signature + '.png')
    local.parent.mkdir(exist_ok=True)
    xmin, xmax = -2, max(6, t+2)
    ymin, ymax = -2, int(b)+2
    fig, ax = plt.subplots(figsize=(4.6, 4.6), dpi=120)
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(range(xmin, xmax+1)); ax.set_yticks(range(ymin, ymax+1))
    ax.grid(color='#c8c8c8', linewidth=.65)
    ax.set_axisbelow(True)
    ax.spines[['right', 'top']].set_visible(False)
    ax.spines[['left', 'bottom']].set_position('zero')
    ax.tick_params(length=0, labelsize=8, pad=4)
    ax.set_xticklabels(['' if z == 0 else str(z) for z in range(xmin, xmax+1)])
    ax.set_yticklabels(['' if z == 0 else str(z) for z in range(ymin, ymax+1)])
    ax.plot([xmin, xmax], [float(m*xmin+b), float(m*xmax+b)], color='red', linewidth=1.7)
    ax.plot(xmax, 0, '>k', clip_on=False, markersize=5)
    ax.plot(0, ymax, '^k', clip_on=False, markersize=5)
    ax.annotate('$x$', (xmax, 0), xytext=(10, -2), textcoords='offset points')
    ax.annotate('$y$', (0, ymax), xytext=(0, 10), textcoords='offset points')
    if role == 'solution':
        ax.scatter([0, t], [float(b), 0], color='blue', s=22, zorder=5)
        ax.annotate('$A$', (0, float(b)), xytext=(5, 7), textcoords='offset points')
        ax.annotate('$B$', (t, 0), xytext=(5, 7), textcoords='offset points')
    fig.tight_layout(pad=2)
    fig.savefig(local, metadata={'Software': VERSION})
    plt.close(fig)
    sha = hashlib.sha256(local.read_bytes()).hexdigest()
    path = f'images/{sha[:2]}/{sha}.png'
    return path, {'local': str(local), 'path': path, 'sha256': sha, 'role': role,
                  'line': [str(m), str(b)], 'points': [[0, p['b']], [t, 0]],
                  'limits': [xmin, xmax, ymin, ymax], 'renderer': 'matplotlib'}

def aligned(rows):
    return '$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$'

def solution(profile, p, asset):
    b, t = p['b'], p['t']; c = sp.Rational(b, t); eq = equations(profile, p)
    header = (f"Let's pick two distinct points on the line. For example, $A$ and $B$ with coordinates $(0,{b})$ and $({t},0)$, respectively.\n\n![]({asset})\n\n"
              "Now, we substitute the coordinates of both points in our equations. If both points satisfy an equation, then we can conclude that the equation represents the line in the graph. Otherwise, if any point does *not* satisfy the equation, then we can conclude that the equation does *not* represent the line in the graph.")
    if profile == 'q-71837':
        k = int(c); f = rf'\frac{{1}}{{{k}}}'
        rows = [
            [f'({b})+{k}(0) & ={b}', rf'{b} & ={b}\,✓', f'(0)+{k}({t}) & ={b}', rf'{b} & ={b}\,✓'],
            [f'{f}({b})+(0) & ={t}', f'{t}+0 & ={t}', rf'{t} & ={t}\,✓', f'{f}(0)+({t}) & ={t}', f'0+{t} & ={t}', rf'{t} & ={t}\,✓'],
            [f'({b}) & =-{k}(0)+{b}', rf'{b} & ={b}\,✓', f'(0) & =-{k}({t})+{b}', f'0 & =-{b}+{b}', rf'0 & =0\,✓']]
        blocks = []
        for i in range(3):
            concluding = f'Therefore,{eq[i]}' if i == 1 else f'Therefore, {eq[i]}'
            space = '  ' if i == 2 else ' '
            blocks.append(f'- Equation {("I", "II", "III")[i]}: ${eq[i]}.$\nSubstituting the coordinates of $A(0,{b})$ and $B({t},0)$, we obtain\n\n' + aligned(rows[i]) + f'\n\n{concluding}$ is{space}an equation of the line in the graph.')
        # Add the opening dollar at the same position as the source.
        blocks = [z.replace('Therefore,', 'Therefore,$', 1) if i == 1 else z.replace('Therefore, ', 'Therefore, $', 1) for i,z in enumerate(blocks)]
        tail = 'All the given equations represented the line in the graph. Therefore, the correct answer is "I, II and III."'
    else:
        f = tex(c)
        rows = [
            [rf'({b}) & =-{b}(0)+{f}', rf'{b} & ={f}\,\times '],
            [rf'({b}) & =-{f}(0)+{b}', rf'{b} & ={b}\,✓', rf'(0) & =-{f}({t})+{b}', f'0 & =-{b}+{b}', rf'0 & =0\,✓'],
            [rf'({b}) & ={f}(0)+{b}', rf'{b} & ={b}\,✓', rf'(0) & ={f}({t})+{b}', f'0 & ={b}+{b}', rf'0 & ={2*b}\,\times ']]
        blocks = []
        for i in range(3):
            coords = f'$A(0,{b})$' + (f' and $B({t},0)$' if i else '')
            before = f'- Equation {("I", "II", "III")[i]}: ${eq[i]}.$\nSubstituting the coordinates of {coords}, we obtain\n\n'
            if i == 1:
                after = f'Therefore,${eq[i]}$ is an equation of the line in the graph.'
            else:
                after = f'Therefore, ${eq[i]}$ is *not* equation of the line in the graph.'
            blocks.append(before + aligned(rows[i]) + '\n\n' + after)
        tail = f'Of the given equations, the only equation that represented the line in the graph was ${eq[1]},$ corresponding to answer choice II. Therefore, the correct answer is "II only."'
    return header + '\n\n' + '\n\n'.join(blocks) + '\n\n' + tail

def generate(difficulty='hard', seed=0, template=None, parameters=None, profile=None):
    if difficulty != 'hard':
        raise ValueError('Unsupported bounded difficulty: see capabilities.json')
    rng = random.Random(seed); profile = profile or template or rng.choice(SUPPORTED)
    p = parameters or rng.choice(candidates(profile))
    if p not in candidates(profile):
        raise ValueError('Parameters outside validated finite domain')
    eq = equations(profile, p)
    prompt_asset, a1 = plot(profile, p, 'prompt'); solution_asset, a2 = plot(profile, p, 'solution')
    prompt = f'![]({prompt_asset})\n\nWhich of the following gives the graph of the straight line above?\n\n' + '\n\n'.join(f'{label}. ${e}$' for label,e in zip(('I','II','III'),eq))
    old = PROFILES[profile][':question/answer-fields'][0]
    values = sorted(a[':answer/value'] for a in old[':answer-field/choices'])
    key = task_key(p); qid = ident(['question', VERSION, profile, key, eq, values]); fid = ident([qid, 'selection'])
    choices = [{':answer/id':ident([fid, value]), ':answer/type':':answer.type/text', ':answer/value':value} for value in values]
    correct = 'I, II and III' if profile == 'q-71837' else 'II only'
    aid = next(a[':answer/id'] for a in choices if a[':answer/value'] == correct)
    q = {':question/id':qid, ':question/problem':prompt, ':question/worked-solution':solution(profile,p,solution_asset), ':question/difficulty':':question.difficulty/hard', ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':'selection', ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices, ':answer-field/correct':[':answer/id', aid]}]}
    return {'knowledge_point':{'db_id':KP_ID, 'id':KP_UUID, 'title':TITLE}, 'question':q,
            'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':profile,'parameters':p,
                          'source_ids':[profile],'domain':'real x,y; positive integer intercepts; bounded negative slopes',
                          'parameter_fingerprint':key,'equations':eq,'choice_lines':[[str(z) for z in obj] for obj in objects(profile,p)],
                          'assets':[a for a in (a1,a2) if a], 'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}

def batch(difficulty, count, seed):
    if difficulty != 'hard' or count < 1:
        raise ValueError('Unsupported band or invalid count')
    pairs = [(sid,p) for sid in SUPPORTED for p in candidates(sid)]
    random.Random(seed).shuffle(pairs); result = []; seen = set()
    for sid,p in pairs:
        key = task_key(p)
        if key in seen:
            continue
        result.append(generate(difficulty,seed,profile=sid,parameters=p)); seen.add(key)
        if len(result) == count:
            return result
    raise ValueError('Finite distinct mathematical graph limit reached; shortage remains explicit')

def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--difficulty', default='hard'); p.add_argument('--count', type=int, default=1); p.add_argument('--seed', type=int, default=0); p.add_argument('--format', choices=['json','markdown'], default='json')
    a = p.parse_args(); records = batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,indent=2) if a.format == 'json' else '\n\n---\n\n'.join(map(markdown,records)))
