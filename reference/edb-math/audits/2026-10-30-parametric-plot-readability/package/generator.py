#!/usr/bin/env python3
"""Seeded, offline parametric graph recognition. See instructional-account.md."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import uuid
sys.dont_write_bytecode = True
import sympy as sp
from geometry import T, expr, shape, valid_bank, geometry_key
from math_format import normalize_prose, validate_prose, validate_generated_record
HERE = Path(__file__).resolve().parent
SPECS = json.loads((HERE/'templates.json').read_text())
VERSION = 'parametric-graphs-2'
KP = {'db_id':17592186087721,'id':'e0dc11d5-8eda-52b1-b7b1-42b481813ff4','title':'Graphing a Curve Defined Parametrically'}
# Complete bank, chosen before target; each nonzero pair is eligible.
CONTROLS = [(-1,-1),(-1,1),(1,-1),(1,1),(2,1)]
SHIFTS = [(0,0),(-2,0),(2,0),(0,-2),(0,2)]

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/parametric-v2/'+s))

def tex(v):
    return sp.latex(v)

def table(label, ts, xs, ys):
    # Keep every source table cell, but repeat row headings in narrow panels.
    # Long ruled arrays otherwise extend beyond the actual learner UI and hide
    # rightmost columns even when MathJax reports no error.
    panels = []
    width = 3 if any(r'\sqrt' in cell for row in (ts, xs, ys) for cell in row) else 5
    for start in range(0, len(ts), width):
        stop = start + width
        rows = [[r'\mathbf{'+label+'}'] + ts[start:stop],
                ['x'] + xs[start:stop], ['y'] + ys[start:stop]]
        body = r' \\ \hline '.join(' & '.join(row) for row in rows)
        panels.append('$$\n' + r'\begin{array}{|c|' + 'c|'*len(ts[start:stop])
                      + r'}\hline ' + body + r' \\ \hline\end{array}' + '\n$$')
    return '\n\n'.join(panels)

def render_plots(bank, ts, correct):
    out_root=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not out_root:
        raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an asset output directory')
    out_root=Path(out_root).resolve()
    key=digest({'version':VERSION,'bank':bank,'ts':list(map(str,ts))})
    out=out_root/key
    expected=[out/f'choice-{i}.png' for i in range(5)]+[out/f'solution-{correct}.png']
    if not all(p.exists() and p.with_suffix('.json').exists() for p in expected):
        out.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=out,delete=False) as f:
            json.dump({'bank':bank,'ts':list(map(str,ts)),'output_dir':str(out),'correct':correct},f)
            name=f.name
        try:
            subprocess.run([sys.executable,str(HERE/'render.py'),name],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        finally:
            Path(name).unlink(missing_ok=True)
    return list(map(str,expected[:5])),str(expected[-1])

def build_instance(level, seed=0, template=None, role=None, parameters=None):
    """No drawing. Decision roles are sampled first. Public for reproducible checks."""
    rng=random.Random(seed)
    role=rng.randrange(5) if role is None else role
    if role not in range(5): raise ValueError('role must be 0..4')
    if level=='easy':
        template=template or rng.choice(list(SPECS))
        s=SPECS[template]
        p=parameters or {'m':rng.choice([1,2]),'n':rng.choice([1,2]),'h':rng.randint(-2,2),'k':rng.randint(-2,2)}
        x=p['m']*expr(s['x'])+p['h']; y=p['n']*expr(s['y'])+p['k']
        bank=[shape(x+dx,y+dy,expr(s['lo']),expr(s['hi']),s['kind']) for dx,dy in SHIFTS]
        ts=list(map(expr,s['ts'])); label=s['label'].strip(); domain=s['prompt_mask'].split('{Y}',1)[1].split('\n$$')[0]
        # domain contains only delimiters, bounds and parameter; remove leading comma spacing.
        domain=re.sub(r'^(?:,|\\,|\s)+','',domain)
        source=[s['source_id']]; profile='translated-coordinate-bank'
    elif level in ('moderate','hard'):
        template='paired-cubics'
        p=parameters or {'h':rng.randint(-2,2),'k':rng.randint(-2,2),'sx':rng.choice([-1,1]),'sy':rng.choice([-1,1])}
        q=T*(T*T-4)
        bank=[shape(p['sx']*(T*(T-2)+c*q)+p['h'],p['sy']*(T*(T+2)+d*q)+p['k'],-2,2) for c,d in CONTROLS]
        ts=list(map(sp.Integer,range(-2,3))); label='t'; domain=r'-2\leq t\leq 2'
        source=['b322617c-ab21-5ce8-997f-2f10813b4280','f02a5b8b-8e80-5764-bcb7-d335f74280e8']
        profile='shared-three-checkpoints' if level=='hard' else 'endpoint-plus-interior'
        if level=='moderate':
            # Bank-first construction: two endpoint groups, with two or three
            # interior curves in each. Every graph may be the requested target.
            bank=[shape(expr(s['x'])+(0 if j<2 else 2),expr(s['y'])+(0 if j<2 else -2),-2,2) for j,s in enumerate(bank)]
    else:
        raise ValueError('difficulty must be easy, moderate or hard')
    valid_bank(bank)
    target=bank[role]
    x,y=expr(target['x']),expr(target['y'])
    # Preserve operator arguments; SymPy is not used to invent equivalent identities.
    theta=sp.Symbol('theta')
    xt=tex(x.subs(T,theta)) if label.startswith(r'\theta') else tex(x)
    yt=tex(y.subs(T,theta)) if label.startswith(r'\theta') else tex(y)
    return {'level':level,'template':template,'profile':profile,'parameters':p,'role':role,
            'bank':bank,'ts':list(map(str,ts)),'label':label,'x_tex':xt,'y_tex':yt,'domain':domain,
            'source_ids':source}

def make_record(instance, seed=0, draw=True, order=None):
    d=copy.deepcopy(instance); bank=d['bank']; role=d['role']; target=bank[role]
    ts=list(map(expr,d['ts']));x,y=expr(target['x']),expr(target['y'])
    xs=[tex(sp.simplify(x.subs(T,t))) for t in ts];ys=[tex(sp.simplify(y.subs(T,t))) for t in ts]
    tt=[tex(t) for t in ts];label=d['label'];xt=d['x_tex'];yt=d['y_tex']
    if draw:
        paths,solpath=render_plots(bank,ts,role)
    else:
        paths=['not-rendered/'+digest(s)+'.png' for s in bank];solpath=paths[role]
    prompt='Determine the graph of the following parametrically defined curve:\n\n$$\n'+r'\begin{aligned}x&='+xt+r'\\ y&='+yt+r'\\ &'+d['domain']+r'\end{aligned}'+'\n$$'
    explanation='Pair the coordinates at the same parameter value and follow the curve only over the stated interval.'
    if d['level'] in ('moderate','hard'):
        points=['$('+a+','+b+')$' for a,b in zip(xs,ys)]
        explanation='The successive paired points are '+', '.join(points)+'. '
        explanation+=('All five choices share the endpoint pair and the middle checkpoint. Compare the interior paired points and the bends between them.' if d['level']=='hard' else 'Use the endpoint pair to find the matching group, then compare an interior paired point to distinguish the remaining curves.')
    solution='First calculate the $x$-values using $x='+xt+'$:\n\n'+table(label,tt,xs,['']*len(ts))+'\n\nNow calculate $y='+yt+'$ at the **same parameter values**:\n\n'+table(label,tt,xs,ys)+'\n\n'+explanation+'\n\n![Curve through the calculated points]('+solpath+')'
    prompt=validate_prose(normalize_prose(prompt));solution=validate_prose(normalize_prose(solution))
    # Paths are delivery-local, not part of semantic identities.
    content=digest({'version':VERSION,'prompt':prompt,'solution':solution.replace(solpath,'correct-curve'),'bank':bank,'role':role,'profile':d['profile']})
    fid=uid(content+'/selection')
    choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/image',':answer/value':p} for i,p in enumerate(paths)]
    if order is None:
        order=list(range(5));random.Random(seed^0xCAFE).shuffle(order)
    if sorted(order)!=list(range(5)):raise ValueError('order must permute five choices')
    choices=[choices[i] for i in order]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+str(role))]}
    q={':question/id':uid(content),':question/difficulty':':question.difficulty/'+d['level'],':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
    d.update({'seed':seed,'version':VERSION,'table_x':xs,'table_y':ys,'choice_order':order,'math_fingerprint':digest(geometry_key(target)),'paths':paths})
    return validate_generated_record({'knowledge_point':KP,'question':q,'generation':d})

def generate(level,seed=0,template=None,role=None,parameters=None,draw=True):
    return make_record(build_instance(level,seed,template,role,parameters),seed,draw)

def replay():
    """Original source cases, normalized presentation; canonical assets stay canonical."""
    result=[]
    for original in json.loads((HERE/'replay-data.json').read_text()):
        q={k:copy.deepcopy(original[k]) for k in [':question/id',':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields']}
        q[':question/difficulty']=q[':question/difficulty'][':db/ident']
        for k in (':question/problem',':question/worked-solution'):
            q[k]=normalize_prose(re.sub(r'\$\$\s*\$\$','',q[k]))
        for f in q[':question/answer-fields']:
            f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
            for a in f[':answer-field/choices']:
                a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
        result.append(validate_generated_record({'knowledge_point':KP,'question':q,'generation':{'source_id':original.get(':question/math-academy-id',original[':question/id']),'source_replay':True}}))
    return result

def batch(level,count,seed):
    if count<0:raise ValueError('count cannot be negative')
    rng=random.Random(seed); roles=list(range(5));rng.shuffle(roles)
    templates=list(SPECS);rng.shuffle(templates)
    positions=list(range(5));rng.shuffle(positions)
    records=[];seen=set()
    for i in range(count):
        role=roles[i%5]
        for retry in range(100):
            case_seed=rng.getrandbits(64)
            d=build_instance(level,case_seed,templates[i%len(templates)] if level=='easy' else None,role)
            fingerprint=digest(geometry_key(d['bank'][role]))
            if fingerprint not in seen:break
        else:raise ValueError('could not produce distinct mathematical instances')
        seen.add(fingerprint)
        # Role and displayed position are separate decisions, neither fixed by template.
        order=list(range(5));rng.shuffle(order);order.remove(role);order.insert(positions[i%5],role)
        records.append(make_record(d,case_seed,order=order))
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay',action='store_true')
    args=ap.parse_args()
    records=replay() if args.replay else batch('easy' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
