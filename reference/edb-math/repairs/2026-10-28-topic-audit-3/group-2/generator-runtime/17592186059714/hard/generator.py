#!/usr/bin/env python3
"""Deterministic exact magnitudes of two-component Cartesian vectors."""
import argparse
import copy
import hashlib
import json
import random
import sys
import uuid
from pathlib import Path
import sympy as sp
from math_format import checked_math_content, normalize_prose, normalize_tex, validate_prose
SOURCE = json.loads(Path(__file__).with_name('source_rows.json').read_text())
KP_ID, KP_UUID = SOURCE['kp_id'], SOURCE['uuid']
VERSION = 'vector-norm-4.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
ROWS = {q[':question/math-academy-id']:q for q in [*SOURCE['questions'], SOURCE['example']]}
STYLES = ('a','u','v')
def tex(v): return normalize_tex(sp.latex(sp.simplify(v)))
def uid(v): return str(uuid.uuid5(uuid.UUID(KP_UUID), v))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def enum(v): return v[':db/ident'] if isinstance(v,dict) else v

def replay_source(mid):
    # Evidence only. Preserve omissions; never deliver partial imported records.
    q={k:copy.deepcopy(v) for k,v in ROWS[mid].items() if k.startswith(':question/')}
    for name in (':question/problem',':question/worked-solution'):
        if name in q:q[name]=normalize_prose(q[name])
    if ':question/difficulty' in q:q[':question/difficulty']=enum(q[':question/difficulty'])
    for f in q.get(':question/answer-fields',[]):
        f.pop(':db/id',None);f[':answer-field/type']=enum(f[':answer-field/type'])
        for a in f.get(':answer-field/choices',[]):
            a.pop(':db/id',None);a[':answer/type']=enum(a[':answer/type']);a[':answer/value']=normalize_tex(a[':answer/value'])
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['title']},'question':q,
            'generation':{'evidence_only':True,'source_reference':mid,'version':VERSION}}

def errors(x,y):
    """Derive distractors from specific mistakes in this instance, not offsets."""
    a,b=abs(x),abs(y);n=x*x+y*y
    candidates=[(n,'This is the squared magnitude; take its square root.'),
       (a+b,'Adding component lengths gives a path along two legs, not the hypotenuse.'),
       (abs(x+y),'Adding signed components does not give the Euclidean length.'),
       (sp.sqrt(abs(x*x-y*y)),'The formula adds the component squares; it does not subtract them.'),
       (sp.sqrt(a+b),'Square each component before adding; do not add their absolute values inside the root.'),
       (sp.sqrt(abs(x*y)),'Use the sum of squares rather than the product of the components.'),
       (sp.sqrt(x*x+b),'The second component must also be squared.'),
       (sp.sqrt(a+y*y),'The first component must also be squared.'),
       (sp.sqrt((x+y)**2),'Squaring the sum introduces a cross term; add the two separate squares.'),
       (sp.sqrt(x**4+y*y),'Squaring the first component twice introduces a fourth power; square each component once.'),
       (sp.sqrt(x*x+y**4),'Squaring the second component twice introduces a fourth power; square each component once.'),
       (sp.sqrt(x**4+y**4),'Squaring both component squares again introduces fourth powers; the magnitude formula uses second powers.'),
       (a*b,'Multiplying component lengths does not give the hypotenuse length.')]
    unique={}
    for value,feedback in candidates:
        value=sp.simplify(value)
        if value != sp.sqrt(n): unique.setdefault(value,feedback)
    return list(unique.items())

def shape(v):
    v=sp.simplify(v)
    if v.is_Integer:return 'integer'
    c,r=v.as_coeff_Mul()
    return 'unit-radical' if c==1 else 'coefficient-radical'

def easy_bank(x,y,rng):
    correct=sp.sqrt(x*x+y*y);pool=errors(x,y)
    # Two options with the correct form prevent a unique-form giveaway.
    peers=[a for a in pool if shape(a[0])==shape(correct)]
    if len(pool)<4 or not peers: raise ValueError('Insufficient distinct plausible distractors')
    peer=rng.choice(peers);others=[a for a in pool if a!=peer]
    wrong=[peer]+rng.sample(others,3)
    return [(correct,'Correct: square both components, add, and take the nonnegative square root.')]+wrong

def parameters_for(level,rng):
    if level=='hard':
        return {'r':rng.choice((2,3,5,6,7,8,10,11,12)),
                's':rng.choice((2,3,5,6,7,8,10,11,12)),
                'sx':rng.choice((-1,1)),'sy':rng.choice((-1,1)),'d':rng.choice((1,2))}
    return {'x':rng.randint(-6,6),'y':rng.randint(-6,6)}

def components(level,p):
    if level=='hard':
        if set(p)!={'r','s','sx','sy','d'} or any(type(z) is not int for z in p.values()):raise ValueError('Hard parameters require integer r,s,sx,sy,d')
        if not (0<=p['r']<=12 and 0<=p['s']<=12 and p['sx'] in (-1,1) and p['sy'] in (-1,1) and p['d'] in (1,2)):raise ValueError('Hard parameters out of range')
        return p['sx']*sp.sqrt(p['r'])/p['d'],p['sy']*sp.sqrt(p['s'])/p['d']
    if set(p)!={'x','y'} or any(type(z) is not int or abs(z)>12 for z in p.values()):raise ValueError('Components require small integers x,y')
    return sp.Integer(p['x']),sp.Integer(p['y'])

@checked_math_content
def generate(level='easy',seed=0,*,parameters=None,style=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);rejected=0
    while True:
        p=copy.deepcopy(parameters) if parameters is not None else parameters_for(level,rng)
        x,y=components(level,p)
        try:
            bank=easy_bank(x,y,rng) if level=='easy' else [(sp.sqrt(x*x+y*y),'')]
            break
        except ValueError:
            if parameters is not None:raise
            rejected+=1
            if rejected>200:raise ValueError('Cannot construct bank')
    v=style or rng.choice(STYLES)
    if v not in STYLES:raise ValueError('Unknown vector name')
    lhs=rf'|\mathbf{{{v}}}|';xs,ys=tex(x),tex(y);n=sp.simplify(x*x+y*y);answer=tex(sp.sqrt(n))
    if level=='moderate':
        # Signed basis coefficients are read as the Cartesian components.
        basis=xs+rf'\mathbf{{i}}'+('+' if y>=0 else '-')+tex(abs(y))+r'\mathbf{j}'
        prompt=rf'Let $\mathbf{{{v}}}={basis}$, where $\mathbf{{i}}$ and $\mathbf{{j}}$ are perpendicular unit basis vectors. Find its exact magnitude.'
    else:
        prompt=rf'Let $\mathbf{{{v}}}=\left\langle {xs},{ys}\right\rangle$. Find its exact magnitude.'
    if level=='easy':prompt+=rf' Use ${lhs}=\sqrt{{{v}_x^2+{v}_y^2}}$.'
    if level!='easy':prompt+=' Enter an exact value; an equivalent unsimplified radical is accepted.'
    prefix=rf'The components are ${v}_x={xs}$ and ${v}_y={ys}$. Square each entire signed component, then add.'
    steps=[lhs+rf'&=\sqrt{{{v}_x^2+{v}_y^2}}',
           rf'&=\sqrt{{\left({xs}\right)^2+\left({ys}\right)^2}}',
           rf'&=\sqrt{{{tex(x*x)}+{tex(y*y)}}}']
    if level=='hard' and p['d']==2:
        steps.append(rf'&=\sqrt{{\frac{{{p["r"]}+{p["s"]}}}{{4}}}}')
    steps.append(rf'&=\sqrt{{{tex(n)}}}')
    # Make square-factor extraction explicit, including the common denominator.
    numer,denom=sp.fraction(n);c,z=sp.sqrt(numer).as_coeff_Mul()
    if c!=1 and z!=1:
        steps.append(rf'&=\frac{{\sqrt{{{tex(c*c)}\cdot {tex(z*z)}}}}}{{{tex(sp.sqrt(denom))}}}')
    steps.append('&= '+answer)
    sol=normalize_prose(prefix+'\n\n$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(steps))+'.\n'+r'\end{aligned}'+'\n$$\n\nThe magnitude is nonnegative.')
    q={':question/problem':normalize_prose(prompt),':question/worked-solution':sol,
       ':question/difficulty':':question.difficulty/'+level,':question/requires-calculator':False}
    key='selection' if level=='easy' else 'magnitude'
    f={':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if level=='easy' else 'blank'),
       ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(a),**({':answer/feedback':validate_prose(fb)} if fb else {})} for a,fb in bank]}
    qid=uid('question:'+digest({'version':VERSION,'prompt':q[':question/problem'],'solution':sol,'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices'])}))
    q[':question/id']=qid;fid=uid(qid+':field:'+key);f[':answer-field/id']=fid
    for a in f[':answer-field/choices']:a[':answer/id']=uid(fid+':value:'+a[':answer/value'])
    f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][0][':answer/id']]
    rng.shuffle(f[':answer-field/choices']);q[':question/answer-fields']=[f]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['title']},'question':q,
       'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':{'easy':'guided-components','moderate':'basis-components','hard':'radical-components'}[level],
        'parameters':p,'components':[xs,ys],'style':v,'root_case':shape(sp.sqrt(n)),
        'rejected_candidates':rejected,'source_references':['e-4297','q-1307','q-18048','tutorial-2919'],
        'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def batch(level,seed,count):
    """Deterministic resampling avoids repeated answers and fixed bank actions.

    Rejection uses only source-relevant cases and plausible authored errors.
    No new seed or hand-picked batch is needed after a delivery cue is found.
    """
    rows=[];seen=set();i=0
    while len(rows)<count:
        if i>max(1000,count*100):raise ValueError('Requested batch exceeds this practice domain')
        q=generate(level,seed+i);i+=1
        f=q['question'][':question/answer-fields'][0]
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        if correct in seen:continue
        prospective=rows+[q]
        if level=='easy' and count>=5 and len(prospective)==count:
            if not varied_banks(prospective):
                rows=[];seen=set();continue
        seen.add(correct);rows.append(q)
        if i>max(1000,count*100):raise ValueError('Requested batch exceeds this practice domain')
    return rows

def varied_banks(rows):
    # Evaluate fixed positions, numeric ranks and extreme-radical strategies.
    groups=[rows]+[[r for r in rows if r['generation']['root_case']==s]
                   for s in ('integer','unit-radical','coefficient-radical')]
    for test in (lambda x,y:abs(x)==abs(y), lambda x,y:x*y<0,
                 lambda x,y:x*y>0, lambda x,y:x==0 or y==0):
        groups.append([r for r in rows if test(**r['generation']['parameters'])])
    if len({r['generation']['root_case'] for r in rows})<2:return False
    for group in groups:
        if len(group)<2:continue
        positions=[];ranks=[];radical_extremes=[]
        for r in group:
            p=r['generation']['parameters'];x,y=sp.Integer(p['x']),sp.Integer(p['y'])
            f=r['question'][':question/answer-fields'][0];correct=sp.sqrt(x*x+y*y)
            catalog={tex(v):v for v,_ in errors(x,y)};catalog[tex(correct)]=correct
            values=[catalog[a[':answer/value']] for a in f[':answer-field/choices']]
            positions.append(values.index(correct));ranks.append(sorted(values,key=float).index(correct))
            radicals=[v for v in values if not v.is_Integer]
            radical_extremes.append((bool(radicals) and correct==min(radicals,key=float),
                                     bool(radicals) and correct==max(radicals,key=float)))
        if len(set(positions))==1 or len(set(ranks))==1:return False
        if all(v[0] for v in radical_extremes) or all(v[1] for v in radical_extremes):return False
    return True

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='easy')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--format',choices=('json',),default='json');parser.add_argument('--replay-source',action='store_true')
    a=parser.parse_args()
    if a.count<0:parser.error('Count must be nonnegative')
    print(json.dumps([replay_source(mid) for mid in ROWS] if a.replay_source else batch(a.difficulty,a.seed,a.count),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
