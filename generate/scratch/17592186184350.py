"""Base-only variants of complete observed exponential-substitution banks.

Easy: five prompt/solution structures, six complete source bank profiles.
Moderate: one cubic rational-exponent structure and its complete bank.
Hard: unobserved; explicitly unsupported pending source evidence.
Only power bases and their logarithms vary. Other constants, exponent signs,
scales, field shape, and solution steps stay exactly as observed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import os
import sys
try:
    import sympy as sp
except ImportError:
    if __name__ == '__main__':
        runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
        os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise
from functools import lru_cache

KP_ID = 17592186184350
KP_UUID = 'e8720b44-317d-590e-a251-bfcec97e0513'
GENERATOR_UUID = '7a978f74-e6d4-5d3c-8f0d-44b05004043d'
VERSION = 'exponential-base-only-v1'
HERE = Path(__file__).with_suffix('')
# Profile: (original base, observed difficulty, exponent, prefactor).
DATA = {
    'q-31420': (8, 'easy', '3*x**2', 'x'),
    'q-31419': (4, 'easy', 'x**2-7', 'x'),
    'q-31426': (5, 'easy', 'x**2/3', 'x'),
    'q-73665': (4, 'easy', '4*x**2-3', '4*x'),
    'q-73801': (6, 'easy', 'x**2+1', '2*x'),
    'q-73802': (7, 'easy', 'x**2-7', 'x'),
    'q-211989': (4, 'moderate', 'x**3/5', 'x**2'),
}
BASES = tuple(range(2, 13))

@lru_cache(maxsize=1)
def sources():
    return {q[':question/math-academy-id']: q for q in
            json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}

def change_base(text, old, new):
    # Every observed power base is braced; do not replace coefficients that
    # happen to have the same numeral. Logarithm arguments are a separate slot.
    text = text.replace('{'+str(old)+'}^', '{'+str(new)+'}^')
    return re.sub(r'(\\operatorname\{ln\}\u2061)'+str(old)+r'(?!\d)',
                  lambda m: m[1]+str(new), text)

def integrand(q):
    m = re.search(r'\\int (.*?)\\,\\text\{d\}x', q[':question/problem'])
    if not m:
        raise ValueError('Unsupported prompt structure')
    return m[1]

def fingerprint(q):
    return fingerprint_prompt(q[':question/problem'])

@lru_cache(maxsize=None)
def fingerprint_prompt(text):
    # Resolve the fixed rendered template to an exact mathematical integrand.
    # The bank/profile/seed/identity/order are excluded from this identity.
    m = re.search(r'\{(\d+)\}\^', text)
    if m:
        b = int(m[1])
        for t,(ob,_,exponent,prefactor) in DATA.items():
            if text == change_base(sources()[t][':question/problem'],ob,b):
                expr=sp.sympify(prefactor)*sp.Integer(b)**sp.sympify(exponent)
                return hashlib.sha256(sp.srepr(sp.simplify(expr)).encode()).hexdigest()
    # Unrated/canonical evidence outside the supported family is never generated.
    return hashlib.sha256(text.encode()).hexdigest()

def generate(level, seed, template, parameters):
    if template not in DATA or level != DATA[template][1]:
        raise ValueError('Unsupported level/template')
    b = parameters.get('base')
    if type(b) is not int or b not in BASES or set(parameters) != {'base'}:
        raise ValueError('Base must be an integer from 2 through 12')
    old = sources()[template]; ob = DATA[template][0]
    of = old[':question/answer-fields'][0]
    prompt = change_base(old[':question/problem'], ob, b)
    solution = change_base(old[':question/worked-solution'], ob, b)
    vals = [change_base(a[':answer/value'], ob, b) for a in of[':answer-field/choices']]
    ci = next(i for i,a in enumerate(of[':answer-field/choices'])
              if a[':answer/id'] == of[':answer-field/correct'][':answer/id'])
    fp = fingerprint({':question/problem':prompt})
    uid = lambda s: str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), s))
    qid = uid('question:'+fp+':profile:'+template)
    fid = uid(qid+':field:'+of[':answer-field/key'])
    answers = [{':answer/id':uid(fid+':answer:'+str(i)), ':answer/type':':answer.type/math',
                ':answer/value':s} for i,s in enumerate(vals)]
    q = {':question/id':qid, ':question/problem':prompt,
         ':question/worked-solution':solution, ':question/difficulty':':question.difficulty/'+level,
         ':question/answer-fields':[{':answer-field/id':fid, ':answer-field/key':of[':answer-field/key'],
             ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':answers,
             ':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Integrating Products Containing Other Exponential Functions'},
            'question':q, 'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,
              'seed':seed,'template':template,'profile':template,'parameters':parameters,
              'source_question':template,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],
              'domain':'Real x; integer exponential base 2..12; fixed observed exponents and prefactors.',
              'dependencies':{'sympy':sp.__version__},'mathematical_fingerprint':fp,
              'sampling_policy':'Narrower base-only transport; fixed non-base constants including the observed ln(3) distractor in q-73801.',
              'recipes':'Complete source bank chosen first; replace only exponential base b0 by b and ln(b0) by ln(b); all other components fixed.'}}

def candidates(level):
    if level not in ('easy','moderate'):
        return
    seen = {fingerprint(q) for t,q in sources().items() if t in DATA}
    for t, (b0,l,_,_) in DATA.items():
        if l != level:
            continue
        for b in BASES:
            rec = generate(level, 0, t, {'base':b}); fp = fingerprint(rec['question'])
            if fp not in seen:
                seen.add(fp)
                yield t, {'base':b}

def batch(level, count, seed):
    if level not in ('easy','moderate') or type(count) is not int or count < 1:
        raise ValueError('Unsupported level/count')
    cs = list(candidates(level)); random.Random(seed).shuffle(cs)
    if count > len(cs):
        raise ValueError('Finite validated variant limit: '+str(len(cs)))
    return [generate(level,seed,t,p) for t,p in cs[:count]]

def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value']+
        (' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '')
        for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--difficulty',required=True)
    p.add_argument('--count',type=int,default=5); p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json','markdown'],default='json')
    a=p.parse_args(); rs=batch(a.difficulty,a.count,a.seed)
    print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
