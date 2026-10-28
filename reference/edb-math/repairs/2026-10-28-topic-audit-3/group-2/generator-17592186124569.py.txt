"""Seeded, relocatable gradient reconstruction. No database or asset writes."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

HERE = Path(__file__).resolve().parent
KP = json.loads((HERE / 'kp.json').read_text())
SOURCES = json.loads((HERE / 'source-cases.json').read_text())
x, y = s.symbols('x y', real=True)
VERSION = 'gradient-complete-practice-2'

def expression(v):
    return s.sympify(v, locals={'x': x, 'y': y})

def tex(v):
    return normalize_tex(s.latex(s.expand(v)))

def disp(v):
    return '$$\n' + v + '\n$$'

def aligned(rows):
    return disp(r'\begin{aligned}' + '\n' + '\\\\\n'.join(rows) + '\n' + r'\end{aligned}')

def full_function(F, wrap=False):
    if not wrap:
        return normalize_tex('f(x,y)='+tex(F)+'+C')
    terms=s.Add.make_args(s.expand(F))
    first=sum((t for t in terms if not t.has(s.sin,s.cos,s.exp)),s.Integer(0))
    second=s.expand(F-first)
    if first==0 or second==0:
        first=sum(terms[:max(1,len(terms)//2)],s.Integer(0));second=s.expand(F-first)
    tail=tex(second)
    if not tail.startswith('-'):tail='+'+tail
    return normalize_tex(r'\begin{aligned}f(x,y)&='+tex(first)+r'\\&'+tail+r'+C\end{aligned}')

def uid(v):
    return str(uuid.uuid5(uuid.UUID(KP['id']), v))

def shapes(level, family):
    if level == 'easy':
        raw = SOURCES[family]['formula']
        _, _, A, H = map(expression, raw[:4])
        terms = s.Add.make_args(s.expand(A))
        mixed = [t for t in terms if t.has(x) and t.has(y)]
        pure = sum((t for t in terms if not t.has(y)), s.Integer(0))
        return mixed, pure if pure != 0 else x, H if H != 0 else y**2
    mixed = [x**2*y, x*y**2]
    if level == 'hard':
        mixed = [s.sin(x+y) if family == 'sine' else s.exp(x*y)] + mixed
    return mixed, x if level == 'moderate' else x**2, y**3 if level == 'moderate' else -s.cos(y)

def plan(level, rng, family=None):
    if level not in ('easy', 'moderate', 'hard'):
        raise ValueError('difficulty must be easy, moderate, or hard')
    family = family or rng.choice(['q-35994'] if level == 'easy' else ['polynomial'] if level == 'moderate' else ['sine', 'exponential'])
    core, U, V = shapes(level, family)
    # Pick the answer-bearing role before incidental magnitudes. Every bank
    # candidate remains eligible as target; no bank cue excludes an option.
    target = rng.randrange(5)
    grid = list(itertools.product(*([(-1, 1)]*len(core) + [(-1, 0, 1), (-1, 0, 1)])))
    while True:
        vectors = rng.sample(grid, 5)
        if all(len({v[j] for v in vectors}) > 1 for j in range(len(core)+2)):
            break
    bases = [t*rng.choice((1, 2)) for t in core] + [U*rng.choice((1, 2)), V*rng.choice((1, 2))]
    swap = level == 'easy' and rng.choice((False, True))
    if swap:
        bases = [b.xreplace({x:y, y:x}) for b in bases]
    return {'level':level, 'family':family, 'target':target, 'vectors':vectors,
            'bases':bases, 'swap':swap}

def build(level, family, A, H, bank, target, metadata, guided=None):
    P, Q = s.diff(A, x), s.diff(A+H, y)
    F = s.expand(A+H)
    prompt = 'Find the general form of $f(x,y)$ such that\n\n' + aligned([
        r'\nabla f={}&\bigl(' + tex(P) + r'\bigr)\,\mathbf i',
        r'&+\bigl(' + tex(Q) + r'\bigr)\,\mathbf j.'])
    domain = r'x>0' if metadata.get('swap') else r'y>0'
    reciprocal = any(s.denom(t).has(x,y) for t in s.Add.make_args(F))
    prompt += '\n\nWork on the half-plane $'+domain+'$.' if reciprocal else '\n\nWork on $' + r'\mathbb R^2$.'
    if guided is None:
        guided = False
    if guided:
        prompt += '\n\nIntegrating the first component gives $f(x,y)='+tex(A)+r'+g(y)$. Use the second component to determine $g(y)$ and select $f(x,y)$.'
    prompt += '\n\nIn the choices, $C$ is an arbitrary constant.'
    dA, dH = s.diff(A,y), s.diff(H,y)
    solution = ('The vector components are $f_x$ and $f_y$. Integrate the first component with respect to $x$, treating $y$ as constant. Retain an arbitrary function $g(y)$ because its $x$-derivative is zero.\n\n' + aligned([
        r'f(x,y)&=\int\bigl('+tex(P)+r'\bigr)\,\mathrm dx',
        r'&='+tex(A)+r'+g(y).']) + '\n\nDifferentiate with respect to $y$ and match the second component:\n\n' + aligned([
        r'f_y&='+tex(dA)+r"+g'(y)",
        r"g'(y)&=\bigl("+tex(Q)+r'\bigr)',
        r'&\quad-\bigl('+tex(dA)+r'\bigr)',
        r'&='+tex(dH)+'.']) + '\n\nIntegrate the remaining function of $y$:\n\n' + aligned([
        r'g(y)&=\int\bigl('+tex(dH)+r'\bigr)\,\mathrm dy',
        r'&='+tex(H)+r'+C.']) + '\n\nSubstitute to obtain\n\n' + disp(full_function(F, wrap=level=='hard')) + '\n\nBoth components check:\n\n' + aligned([
        r'f_x&='+tex(P)+',',r'f_y&='+tex(Q)+'.']))
    prompt, solution = map(normalize_prose, (prompt, solution))
    values = [full_function(b, wrap=level=='hard') for b in bank]
    identity = hashlib.sha256(json.dumps([VERSION,level,prompt,solution,sorted(values),values[target]],sort_keys=True).encode()).hexdigest()
    qid = uid('question/'+identity); fid=uid(qid+'/selection')
    choices = [{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    record = {'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[
            {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
             ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[target][':answer/id']]}]},
        'generation':{'version':VERSION,'template':family,'difficulty':level,'parameters':metadata,
                      'source_question_ids':[SOURCES[family]['source_id']] if family in SOURCES else [],
                      'domain':domain if reciprocal else 'R^2','sympy':s.__version__}}
    return validate_generated_record(record)

def from_plan(p, target=None, guided=None):
    target = p['target'] if target is None else target
    bases, vectors = p['bases'], p['vectors']
    bank = [s.expand(sum((a*b for a,b in zip(v,bases)),s.Integer(0))) for v in vectors]
    F = bank[target]
    # The displayed derivation follows x-first order even for exchanged cores.
    # Separate all y-only terms exactly, rather than CAS-integrating a final key.
    A = sum((t for t in s.Add.make_args(F) if t.has(x)),s.Integer(0)); H=s.expand(F-A)
    meta={'target':target,'vectors':[list(v) for v in vectors],'bases':[str(b) for b in bases],'swap':p['swap'],
          'profile':'independent-sign-and-omission'}
    return build(p['level'],p['family'],A,H,bank,target,meta,guided)

def generate(difficulty='easy', seed=0, family=None):
    return from_plan(plan(difficulty,random.Random(seed),family))

def replay_source(family):
    raw=SOURCES[family]['formula'];P,Q,A,H=map(expression,raw[:4]);bank=list(map(expression,raw[4]))
    target=next(i for i,b in enumerate(bank) if s.simplify(s.diff(b,x)-P)==0 and s.simplify(s.diff(b,y)-Q)==0)
    return build('easy',family,A,H,bank,target,{'source_replay':True,'swap':False},guided=False)

def batch_cues(records):
    """Bank-only cues: no target field or gradient is used to propose an answer.

    A repeated success across a recognizable delivered family is rejected.
    Singleton families cannot establish such a pattern. Large hard batches
    include both supported operators, with at least two witnesses per operator.
    """
    groups = {}
    for r in records:
        f = r['question'][':question/answer-fields'][0]
        values = [a[':answer/value'] for a in f[':answer-field/choices']]
        key = next(i for i,a in enumerate(f[':answer-field/choices'])
                   if a[':answer/id'] == f[':answer-field/correct'][1])
        params = r['generation']['parameters']
        vectors, bases = params['vectors'], list(map(expression, params['bases']))
        bank = [sum(a*b for a,b in zip(v,bases)) for v in vectors]
        ranks = sorted(range(5), key=lambda i:float(bank[i].subs({x:s.Rational(2,3),y:s.Rational(4,3)}).evalf()))
        lengths = sorted(range(5), key=lambda i:len(values[i]))
        terms = sorted(range(5), key=lambda i:len(s.Add.make_args(bank[i])))
        modal = [sum(sum(w[j] == v[j] for w in vectors) for j in range(len(v))) for v in vectors]
        proposed = {'position_'+str(i):i for i in range(5)}
        proposed.update({'numeric_rank_'+str(i):ranks[i] for i in range(5)})
        proposed.update({'length_rank_'+str(i):lengths[i] for i in range(5)})
        proposed.update({'term_count_rank_'+str(i):terms[i] for i in range(5)})
        proposed['modal_coefficients'] = max(range(5), key=lambda i:modal[i])
        groups.setdefault(r['generation']['template'], []).append({k:v==key for k,v in proposed.items()})
    return groups

def batch_issues(records):
    issues = []
    groups = batch_cues(records)
    for family, rows in groups.items():
        if len(rows) >= 2:
            issues += [family+'/'+cue for cue in rows[0] if all(row[cue] for row in rows)]
    if len(records)>=4 and records[0]['generation']['difficulty']=='hard':
        if any(len(groups.get(f,[]))<2 for f in ('sine','exponential')):
            issues.append('hard/operator-coverage')
    return issues

def batch(difficulty,count,seed):
    if count < 0: raise ValueError('count must be nonnegative')
    if count == 0: return []
    rng = random.Random(seed)
    # Reject the whole prospective batch using a deterministic bounded stream.
    # This repairs recurring small-pool cues rather than changing the seed.
    for attempt in range(1000):
        records=[]; seen=set()
        for _ in range(max(100,count*20)):
            r=from_plan(plan(difficulty,rng));qid=r['question'][':question/id']
            if qid not in seen:
                r['generation']['seed']=seed;r['generation']['batch_index']=len(records)
                records.append(r);seen.add(qid)
            if len(records)==count: break
        if len(records)==count and not batch_issues(records):return records
    raise ValueError('cannot construct a varied unique batch within 1000 attempts')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    ap.add_argument('--replay-source',choices=sorted(SOURCES))
    args=ap.parse_args()
    result=[replay_source(args.replay_source)] if args.replay_source else batch('easy' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(result,ensure_ascii=False,indent=2))
