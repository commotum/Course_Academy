"""Relocatable cosine degree sum/difference generator. No I/O except JSON stdout."""
import argparse
import functools
import itertools
import json
import random
import uuid
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '2.0.0'
KP = {'db_id': 17592186059821, 'id': 'c6a58962-cb06-519a-8c64-0dfa3b9c14d7',
      'title': 'Simplifying Expressions in Degrees Using the Sum and Difference Formulas'}
SOURCE = ['b643e820-52c3-5c08-a099-aecbed7b2b2a']
ANGLES = (30,45,60,120,135,150,210,225,240,300,315,330)
HALF = S.Rational(1,2)
# Exact special values are derivation inputs, not a CAS rewrite of the final function.
VALUES = {30:(HALF,S.sqrt(3)/2),45:(S.sqrt(2)/2,S.sqrt(2)/2),60:(S.sqrt(3)/2,HALF),
          90:(S.Integer(1),S.Integer(0)),120:(S.sqrt(3)/2,-HALF),135:(S.sqrt(2)/2,-S.sqrt(2)/2),
          150:(HALF,-S.sqrt(3)/2),180:(S.Integer(0),S.Integer(-1)),210:(-HALF,-S.sqrt(3)/2),
          225:(-S.sqrt(2)/2,-S.sqrt(2)/2),240:(-S.sqrt(3)/2,-HALF),270:(S.Integer(-1),S.Integer(0)),
          300:(-S.sqrt(3)/2,HALF),315:(-S.sqrt(2)/2,S.sqrt(2)/2),330:(-HALF,S.sqrt(3)/2)}

def tex(v):
    return normalize_tex(S.latex(S.simplify(v)))

def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ca-cos-degrees-v1:' + value))

def expr(s, a):
    return rf'\cos(x{"+" if s == 1 else "-"}{a}^\circ)'

def pair(s, a):
    sn, cs = VALUES[a]
    return (-s*sn, cs) # sine first, cosine second

def linear(sn, cs):
    parts=[]
    for v, f in ((sn,r'\sin x'),(cs,r'\cos x')):
        if v == 0: continue
        prefix = '-' if v < 0 else ('+' if parts else '')
        mag = abs(v)
        parts.append(prefix + ('' if mag == 1 else tex(mag)) + f)
    return ''.join(parts) or '0'

def display(rows):
    return '$$\n' + r'\begin{aligned}' + '\n' + '\\\\\n'.join(rows) + '\n' + r'\end{aligned}' + '\n$$'

def expansion(s,a):
    sn,cs = VALUES[a]
    op = '-' if s == 1 else '+'
    ident=rf'\cos(u{"+" if s == 1 else "-"}v)=\cos u\cos v{op}\sin u\sin v'
    rows=[expr(s,a)+rf'&=\cos x\cos {a}^\circ{op}\sin x\sin {a}^\circ',
          rf'&=\cos x\left({tex(cs)}\right){op}\sin x\left({tex(sn)}\right)',
          '&='+linear(*pair(s,a))]
    return f'Use ${ident}$ with $u=x$ and $v={a}^\\circ$.\n\n'+display(rows)

def weighted(w,e,first=False):
    sign='-' if w < 0 else ('' if first else '+')
    return sign + (str(abs(w)) if abs(w)!=1 else '') + e

def build(level, p, order_seed=0):
    """p is the mathematical/response instance. Identities follow normalized content."""
    s,a=p['sign'],p['angle']
    sn,cs=pair(s,a)
    original=expr(s,a)
    solution=expansion(s,a)
    shape=p['shape']
    if any(key in p for key in ('sign2','angle2','weight1','weight2')):
        raise ValueError('Only one shifted cosine is in this KP family')
    correct=linear(sn,cs)
    specs=[]
    if shape=='radio':
        prompt=rf'Express ${original}$ in terms of $\sin x$ and $\cos x$.'
        if level=='easy':
            # Formula-sign, function and special-angle confusion, with neither
            # a unique counterpart nor a unique bare-function key.
            values=[r'\sin x',r'-\sin x',r'\cos x',r'-\cos x',
                    linear(S.Rational(1,2),S.sqrt(3)/2)]
        else:
            error_rng=random.Random(order_seed ^ 0xB4A912)
            es,ec=error_rng.choice((-1,1)),error_rng.choice((-1,1))
            values=[linear(i*abs(sn),j*abs(cs)) for i,j in itertools.product((-1,1),repeat=2)]
            if abs(sn)!=abs(cs):
                # A complete authored profile swaps the values and independently
                # chooses which formula/quadrant sign errors accompany it.
                values.append(linear(es*abs(cs),ec*abs(sn)))
            else:
                # Confuse 45-degree values with 1/2, with independently
                # chosen sign-error profile. The fifth option must not reveal key signs.
                values.append(linear(es*HALF,ec*HALF))
        if 'source_bank' in p:
            # Replay-only captured complete bank profiles, expressed as recipes
            # in the two magnitudes u and v plus familiar angle constants.
            sub={'u':abs(sn),'v':abs(cs),'h':HALF,'r':S.sqrt(2)/2,'q':S.sqrt(3)/2}
            values=[linear(S.sympify(left,locals=sub),S.sympify(right,locals=sub)) for left,right in p['source_bank']]
        assert len(set(values))==5 and correct in values
        random.Random(order_seed).shuffle(values)
        specs=[('selection','radio',values,correct)]
    elif shape=='expression':
        prompt=rf'Express ${original}$ in terms of $\sin x$ or $\cos x$.'+'\n\n{{field-1}}'
        specs=[('field-1','blank',[correct],correct)]
    else:
        sign2='-' if shape=='coeff-minus' and cs<0 else '+'
        prompt=rf'Simplify ${original}$ using $\sin x$ and $\cos x$. Enter signed coefficients.'
        prompt+='\n\n{{field-1}} '+rf'$\sin x{sign2}$'+' {{field-2}} '+r'$\cos x$'
        ckey= -cs if sign2=='-' else cs
        specs=[('field-1','blank',[tex(sn)],tex(sn)),('field-2','blank',[tex(ckey)],tex(ckey))]
        solution+=f'\n\nThe first blank is ${tex(sn)}$ and the second is ${tex(ckey)}$.'
        if sign2=='-':
            solution+=rf' The printed minus sign means the second entry is the negative of the cosine coefficient: $-\left({tex(ckey)}\right)={tex(cs)}$.'
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    # Content identity is calculated after all prose and answer normalization.
    signature=json.dumps([level,prompt,solution,[(k,t,list(map(normalize_tex,v)),normalize_tex(c)) for k,t,v,c in specs]],sort_keys=True)
    qid=uid(signature)
    fields=[]
    for key,kind,values,keyval in specs:
        choices=[{':answer/id':uid(qid+key+str(i)),':answer/type':':answer.type/math',':answer/value':normalize_tex(v)} for i,v in enumerate(values)]
        keyid=next(c[':answer/id'] for c in choices if c[':answer/value']==normalize_tex(keyval))
        fields.append({':answer-field/id':uid(qid+key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',keyid]})
    rec={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,
         ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
         'generation':{'version':VERSION,'parameters':p.copy(),'source_ids':[p['source_id']] if 'source_id' in p else SOURCE,
          'profile':'quadrantal-complete' if level=='easy' else ('sign-rectangle-plus-angle-error' if shape=='radio' else shape),
          'final_expression':correct}}
    return validate_generated_record(rec)

@functools.lru_cache(None)
def catalog(level):
    angles=(90,180,270) if level=='easy' else (ANGLES if level=='moderate' else tuple(a for a in ANGLES if a>90))
    entries=[]
    for sign,angle in itertools.product((-1,1),angles):
        cs=pair(sign,angle)[1]
        shapes=('radio','expression') if level=='easy' else (('radio','coeff-plus','coeff-minus') if level=='moderate' else ('coeff-plus',))
        for shape in shapes:
            if shape=='coeff-minus' and cs>=0: continue
            entries.append({'sign':sign,'angle':angle,'shape':shape})
    return entries

def generate(level,count,seed):
    if count<0: raise ValueError('count must be nonnegative')
    capacity=len({(p['sign'],p['angle']) for p in catalog(level)})
    if count>capacity:raise ValueError(f'{level} supports {capacity} mathematical shifts; requested {count}')
    rng=random.Random(seed);out=[];cycle=0
    while len(out)<count:
        # One item per displayed shift in a cycle. Response shape and shuffling
        # do not create additional mathematical inventory.
        groups={}
        for p in catalog(level):groups.setdefault((p['sign'],p['angle']),[]).append(p)
        deck=list(groups);rng.shuffle(deck)
        for key in deck:
            p=rng.choice(groups[key])
            r=build(level,p,rng.getrandbits(64))
            r['generation'].update(seed=seed,index=len(out),catalog_cycle=cycle,
                calibration='authored overlapping single-shift band' if level=='hard' else 'imported same-skill family')
            out.append(r)
            if len(out)==count:break
        cycle+=1
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    a=parser.parse_args()
    print(json.dumps(generate('moderate' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
