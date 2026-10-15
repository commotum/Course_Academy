#!/usr/bin/env python3
"""Seeded easy planar flux questions; see the adjacent extraction and validation.

No moderate/hard sampler: raising degree, changing topology, or adding segments
would change the extracted workload. Source replay uses explicit parameters.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import uuid
try:
    import sympy as s
except ModuleNotFoundError as error:
    # Inventory executes registered scripts with its own Python. Reuse the
    # repository's installed dependencies when that Python lacks SymPy.
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if error.name != 'sympy' or __name__ != '__main__' or not interpreter.is_file():
        raise
    if interpreter.resolve() == Path(sys.executable).resolve():
        raise
    os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])

KP_ID = 17592186179744
KP_UUID = '4c9de11e-2195-5946-a19e-235667d39631'
VERSION = '1.0.1'
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'reference/source.json').read_text())
SOURCE['lineage'] = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
X, Y, T = s.symbols('x y t', real=True)
CASES = {
    'q-127055': ('circle-linear', dict(a=3, b=3, k=1), 'signed-half'),
    'q-127060': ('cross-quadratic', dict(a=2, b=2, k=1), 'cubic-scale'),
    'q-127077': ('radial-linear', dict(a=5, b=6, k=1), 'signed-half'),
    'q-127081': ('cross-cubic', dict(a=1, b=3, k=9), 'coefficient-scale'),
    'q-127139': ('square-constant', dict(a=7, b=2, k=1), 'area-scale'),
    'q-127140': ('radial-linear', dict(a=8, b=6, k=4), 'component-scale'),
    'q-127062': ('cross-exponential', dict(a=3, b=4, k=1), 'axis-square-scale'),
    'q-127082': ('triangular-linear', dict(a=3, b=5, k=1), 'signed-half'),
}
TEMPLATES = tuple(dict.fromkeys(c[0] for c in CASES.values()))


def parameters_checked(level, template, p):
    if level != 'easy':
        raise ValueError('Unsupported difficulty: no extracted moderate/hard backbone')
    assert template in TEMPLATES and set(p) == {'a', 'b', 'k'}
    assert all(type(v) is int and 1 <= v <= 12 for v in p.values())
    a, b, k = (p[x] for x in ('a', 'b', 'k'))
    if template in ('circle-linear', 'cross-quadratic'):
        assert a == b and k == 1
    elif template != 'radial-linear' and template != 'cross-cubic':
        assert k == 1
    if template in ('radial-linear', 'cross-exponential'):
        assert a != b and min(a, b) >= 2


def objects(template, p):
    a, b, k = (s.Integer(p[x]) for x in ('a', 'b', 'k'))
    return {
        'circle-linear': (X+Y, Y-X),
        'cross-quadratic': (X*Y, X**2),
        'radial-linear': (k*X, k*Y),
        'cross-cubic': (Y, k*X**3),
        'square-constant': (X**2, s.Integer(1)),
        'cross-exponential': (s.exp(Y), s.exp(X)),
        'triangular-linear': (X, X+Y),
    }[template]


def values(template, p, profile):
    a, b, k = (s.Integer(p[x]) for x in ('a', 'b', 'k'))
    if profile == 'signed-half':
        assert template in ('circle-linear', 'radial-linear', 'triangular-linear')
        scale = k*a*b*s.pi
        return [2*scale, -2*scale, scale, -scale, s.Integer(0)]
    if profile == 'component-scale':
        assert template == 'radial-linear'
        return [2*k*a*b*s.pi, k*a*b*s.pi, k*a*s.pi, k*b*s.pi, s.Integer(0)]
    if profile == 'cubic-scale':
        assert template == 'cross-quadratic'
        v = 2*a**3*s.pi/3
    elif profile == 'coefficient-scale':
        assert template == 'cross-cubic'
        v = k/2
    elif profile == 'area-scale':
        assert template == 'square-constant'
        v = a*b*s.pi/2
    elif profile == 'axis-square-scale':
        assert template == 'cross-exponential'
        return [s.Integer(0), s.E*(a*a+b*b)/(a*b), -s.E*(a*a+b*b)/(a*b),
                s.E*(b*b-a*a)/(a*b), -s.E*(b*b-a*a)/(a*b)]
    else:
        raise ValueError(profile)
    return [s.Integer(0), v, -v, 2*v, -2*v]


def identity(text):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), text))


def task_fingerprint(template, p):
    a,b,k=(p[n] for n in ('a','b','k'))
    # Collapse alternate parameterizations that produce the same assessed
    # integral in the same instructional backbone; bank/seed/order are absent.
    data={
        'circle-linear':[a*a], 'cross-quadratic':[2*a**3],
        'radial-linear':[k*a*b], 'cross-cubic':[b*b,k*a**4],
        'square-constant':[a*a*b,a], 'cross-exponential':sorted([a,b]),
        'triangular-linear':[a*b,a*a],
    }[template]
    return hashlib.sha256(json.dumps([template,data]).encode()).hexdigest()



def generate(level='easy', seed=0, template=None, parameters=None, profile=None):
    if level != 'easy':
        raise ValueError('Unsupported difficulty: ' + level)
    rng = random.Random(seed)
    template = template or rng.choice(TEMPLATES)
    if parameters is None:
        a, b = rng.sample(range(2, 11), 2)
        if template in ('circle-linear', 'cross-quadratic'):
            b = a
        k = rng.randint(2, 9) if template in ('radial-linear', 'cross-cubic') else 1
        parameters = dict(a=a, b=b, k=k)
    p = dict(parameters)
    parameters_checked(level, template, p)
    profiles = sorted({c[2] for c in CASES.values() if c[0] == template})
    profile = profile or rng.choice(profiles)
    assert profile in profiles
    a, b, k = (s.Integer(p[x]) for x in ('a', 'b', 'k'))
    P, Q = objects(template, p)
    xt, yt = a*s.cos(T), b*s.sin(T)
    Pt, Qt = P.subs({X:xt,Y:yt}, simultaneous=True), Q.subs({X:xt,Y:yt}, simultaneous=True)
    dx, dy = s.diff(xt,T), s.diff(yt,T)
    integrand = s.expand_trig(s.expand(Pt*dy-Qt*dx))
    answer = 2*k*a*b*s.pi if template in ('circle-linear','radial-linear','triangular-linear') else s.Integer(0)
    bank = values(template,p,profile)
    assert len(bank) == 5 and all(s.simplify(x-y) != 0 for i,x in enumerate(bank) for y in bank[i+1:])
    assert sum(s.simplify(v-answer)==0 for v in bank)==1
    L = s.latex
    prompt = (rf'Calculate the flux of the vector field $F(x,y)=({L(P)})\,i+({L(Q)})\,j$ '
              rf'across the closed curve $C$ given by $r(t)={L(xt)}\,i+{L(yt)}\,j$ '
              rf'for $t\in[0,2\pi)$.')
    intro = ('If $F=P\\,i+Q\\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, '
             'then the outward flux is\n\n$$\\oint_C F\\cdot n\\,\\mathrm ds=\\oint_C P\\,\\mathrm dy-Q\\,\\mathrm dx,$$\n\n'
             'where $n$ denotes the outward-pointing unit normal vector to $C$.\n\n')
    solution = intro + (rf'Along the curve $C$, we have $x={L(xt)}$, $y={L(yt)}$.' '\n\n'
        rf'Therefore, $P={L(Pt)}$ and $Q={L(Qt)}$.' '\n\n'
        rf'Computing the derivatives gives $x\prime(t)={L(dx)}$ and $y\prime(t)={L(dy)}$.' '\n\n'
        'Finally, evaluate the integral:\n\n'
        rf'$$\begin{{aligned}}\oint_C F\cdot n\,\mathrm ds'
        rf'&=\int_0^{{2\pi}}(P y\prime-Q x\prime)\,\mathrm dt\\'
        rf'&=\int_0^{{2\pi}}\left[({L(Pt)})({L(dy)})-({L(Qt)})({L(dx)})\right]\,\mathrm dt\\'
        rf'&=\int_0^{{2\pi}}\left({L(integrand)}\right)\,\mathrm dt.\end{{aligned}}$$' '\n\n')
    if template in ('circle-linear','radial-linear'):
        solution += (rf'Using $\cos^2t+\sin^2t=1$, the integrand is ${L(k*a*b)}$. '
                     rf'Thus the flux is $[{L(k*a*b)}t]_0^{{2\pi}}={L(answer)}$.')
    elif template == 'triangular-linear':
        solution += (rf'The integrand is ${L(a*b)}+{L(a*a)}\sin t\cos t$. '
            rf'Use $u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$ in the second term: '
            rf'$$[{L(a*b)}t]_0^{{2\pi}}+{L(a*a)}\int_0^0u\,\mathrm du={L(answer)}.$$')
    elif template == 'cross-quadratic':
        solution += (rf'Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: '
                     rf'$$-{L(2*a**3)}\int_1^1u^2\,\mathrm du=0.$$')
    elif template == 'cross-cubic':
        solution += (rf'Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: '
            rf'$$-\int_1^1\left({L(b*b)}u+{L(k*a**4)}u^3\right)\,\mathrm du=0.$$')
    elif template == 'square-constant':
        solution += (rf'Write $\cos^3t=(1-\sin^2t)\cos t$ and use '
            rf'$u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$: '
            rf'$$[{L(a*a*b)}\sin t-{L(a)}\cos t]_0^{{2\pi}}'
            rf'-{L(a*a*b)}\int_0^0u^2\,\mathrm du=0.$$')
    else:
        solution += (rf'Use $u={L(b)}\sin t$, $\mathrm du={L(b)}\cos t\,\mathrm dt$ and '
            rf'$v={L(a)}\cos t$, $\mathrm dv=-{L(a)}\sin t\,\mathrm dt$: '
            rf'$$\int_0^0e^u\,\mathrm du-\int_{{{L(a)}}}^{{{L(a)}}}e^v\,\mathrm dv=0.$$')
    fp = task_fingerprint(template,p)
    qid = identity('question:'+fp+':'+profile)
    fid = identity(qid+':selection')
    choices = [{':answer/id':identity(fid+':'+s.srepr(v)), ':answer/type':':answer.type/math', ':answer/value':L(v)} for v in bank]
    correct = next(c[':answer/id'] for c,v in zip(choices,bank) if s.simplify(v-answer)==0)
    rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},
        'question':{':question/id':qid, ':question/problem':prompt, ':question/worked-solution':solution,
            ':question/difficulty':':question.difficulty/easy', ':question/answer-fields':[
                {':answer-field/id':fid, ':answer-field/key':'selection', ':answer-field/type':':answer-field.type/radio',
                 ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'generator_version':VERSION, 'sympy_version':s.__version__, 'seed':seed, 'parameters':p,
            'template':template,'bank_profile':profile,'source_ids':[sid for sid,c in CASES.items() if c[0]==template and c[2]==profile],
            'mathematical_task_fingerprint':fp,'eligible_for_learning':True, 'exact_flux':L(answer),
            'domain':'positive integer semiaxes; counterclockwise once; outward normal'}}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty',default='easy')
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--template',choices=TEMPLATES)
    ap.add_argument('--format',choices=('json','markdown'),default='json')
    args=ap.parse_args()
    records=[];seen=set()
    for i in range(max(0,args.count)*100):
        if len(records)>=args.count:break
        r=generate(args.difficulty,args.seed+i,template=args.template)
        fp=r['generation']['mathematical_task_fingerprint']
        if fp not in seen:records.append(r);seen.add(fp)
    if args.format=='json':print(json.dumps(records,indent=2))
    else:print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
