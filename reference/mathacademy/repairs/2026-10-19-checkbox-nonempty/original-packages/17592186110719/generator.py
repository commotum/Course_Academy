#!/usr/bin/env python3
"""Seeded direct affine-identity checkboxes; adapted from the registered generator.

Only the source-supported easy band is served. All answer-bearing cases are
chosen before compatible coefficients/constants. No output assets or DB access.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
import sympy as sp
from math_format import normalize_prose, checked_math_content
KP_ID=17592186110719
KP_UUID="ff4e9141-5743-55f1-a8be-3e28cb047eca"
TITLE="Identifying Equations With Infinitely Many Solutions"
VERSION="direct-identities-checkbox-5"
PROMPT="Which of the following equations has infinitely many solutions?\n\nSelect all that apply."

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def ident(v): return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))

def tex(v): return sp.latex(sp.Rational(v))

def linear(a,b):
 z=('x' if a==1 else '-x' if a==-1 else tex(a)+'x') if a else ''
 return z+('+' if b>0 and z else '')+(tex(b) if b or not z else '')

def added(z,n,variable=False):
 if not n:return z
 return z+('+' if n>0 else '-')+(linear(abs(n),0) if variable else tex(abs(n)))

def eq(v): return linear(v[0],v[1])+'='+linear(v[2],v[3])

def kind(v):
 a,b,c,d=v
 return 'identity' if a==c and b==d else 'empty' if a==c else 'unique'

def solution(v,index,display,prefix):
 a,b,c,d=v;class_=kind(v);left,right=linear(a,b),linear(c,d)
 remove=a if a==c else min(a,c)
 rows=prefix+[(left,right),(added(left,-remove,True),added(right,-remove,True)),(linear(a-remove,b),linear(c-remove,d))]
 if class_=='unique':
  coeff=abs(a-c)
  if a>c:
   if b: rows += [(added(linear(coeff,b),-b),added(tex(d),-b)),(linear(coeff,0),tex(d-b))]
   value=(d-b)/(a-c)
  else:
   if d: rows += [(added(tex(b),-d),added(linear(coeff,d),-d)),('x' if coeff==1 else tex(b-d),tex(b-d) if coeff==1 else linear(coeff,0))]
   elif coeff==1: rows += [('x',tex(b))]
   value=(d-b)/(a-c)
  if coeff!=1:rows += [('x',tex(value))]
  conclusion=f'Therefore, the equation ${display}$ has the unique solution $x={tex(value)}.$'
 elif class_=='identity':conclusion=f'This equation is true for all values of $x.$ Therefore, the equation ${display}$ has infinitely many solutions.'
 else:conclusion='This equation is false for all values of $x.$'
 steps=r' \\ '.join(l+' & ='+r for l,r in rows)
 return '- For the '+('first','second','third')[index]+' equation, we have\n\n$$\n'+r'\begin{aligned}'+steps+r'.\end{aligned}'+'\n$$\n\n'+conclusion

SOURCE_CASES = {'q-287966': {'equations': [[2, 0, 1, 1], [2, 1, 2, 1], [2, 1, 2, 3]], 'field_order': [2, 1, 0]}, 'q-288419': {'equations': [[3, 0, 2, 5], [4, -2, 4, -2], [5, 3, 5, 1]], 'field_order': [1, 2, 0]}, 'q-288425': {'equations': [[-3, 2, -3, 7], [6, 1, 6, 5], [7, -4, 6, -6]], 'field_order': [2, 0, 1]}, 'q-288427': {'equations': [[2, -5, 1, -2], [6, 1, 6, 9], [-4, 3, -4, 3]], 'field_order': [2, 0, 1]}, 'q-288591': {'equations': [[3, 2, 4, 1], [2, -5, 3, -3], [5, -4, 5, -4]], 'field_order': [2, 1, 0]}, 'q-288426': {'equations': [[4, 2, 4, 2], [-2, -1, -2, -1], [3, 5, 3, 9]], 'field_order': [1, 2, 0]}, 'q-288431': {'equations': [[3, 4, 3, 4], [1, -5, 1, -2], [2, 3, 1, 3]], 'field_order': [0, 1, 2]}}

def validate_rows(rows):
    if not isinstance(rows, list) or len(rows) != 3:
        raise ValueError('three affine equations required')
    for row in rows:
        if not isinstance(row, list) or len(row) != 4 or any(type(v) is not int for v in row):
            raise ValueError('each equation needs four exact integers')
        a,b,c,d = row
        if not (1 <= abs(a) <= 7 and 1 <= abs(c) <= 7 and abs(b) <= 9 and abs(d) <= 9):
            raise ValueError('easy coefficient/constant bounds')
        if a != c and abs(a-c) != 1:
            raise ValueError('easy unique cases require unit-gap slopes')
    if len({eq(r) for r in rows}) != 3:
        raise ValueError('repeated equation')


def sample_row(case, rng):
    # Choose the decisive equality relation before compatible numerical values.
    equal_constants = case == 'identity' or (case == 'unique' and bool(rng.getrandbits(1)))
    if case == 'unique':
        a,c = rng.choice([(a,c) for a in range(-7,8) for c in (a-1,a+1)
                          if a and c and abs(c) <= 7])
    else:
        a = c = rng.choice([v for v in range(-7,8) if v])
    # For unequal slopes, equal constants (x=0) and unequal constants are
    # separate relevant cases, observed together in source q-288431/e-18854.
    b = rng.randint(-9,9)
    d = b if equal_constants else rng.choice([v for v in range(-9,10) if v != b])
    return [a,b,c,d]


@checked_math_content
def generate(level='easy', seed=0, parameters=None, cases=None, field_order=None):
    if level != 'easy':
        raise ValueError('unsupported difficulty: only easy is source-calibrated')
    rng = random.Random(seed)
    rejections = 0
    if parameters is None:
        # All eight eligible target subsets, then distinguish remaining rule cases.
        if cases is None:
            mask = rng.randrange(8)
            cases = ['identity' if mask & (1 << i) else rng.choice(['unique','empty'])
                     for i in range(3)]
        if len(cases) != 3 or any(c not in ('identity','empty','unique') for c in cases):
            raise ValueError('three valid decision cases required')
        for _ in range(1000):
            rows = [sample_row(case,rng) for case in cases]
            try:
                validate_rows(rows)
                break
            except ValueError:
                rejections += 1
        else:
            raise ValueError('sampling exhausted')
    else:
        if not isinstance(parameters,dict) or set(parameters) != {'equations'}:
            raise ValueError('parameters require equations')
        rows = parameters['equations']
        validate_rows(rows)
    order = list(range(3)) if field_order is None else field_order
    if sorted(order) != [0,1,2]:
        raise ValueError('field order must be a permutation of 0,1,2')
    classes = [kind(row) for row in rows]
    displays = [eq(row) for row in rows]
    selected = [displays[i] for i in order if classes[i] == 'identity']
    conclusion = ('; '.join('$'+e+'$' for e in selected)+' only.' if selected else '"None."')
    worked = ("Let's attempt to solve each equation in turn:\n\n" +
              '\n\n'.join(solution(list(map(sp.Integer,rows[j])),i,displays[j],[])
                            for i,j in enumerate(order))+
              '\n\nTherefore, the correct answer is '+conclusion)
    worked = normalize_prose(worked)
    keys = [normalize_prose('$'+displays[i]+'$') for i in order]
    # Canonical content before UUIDs, with every answer field owned by this question.
    qid = ident([VERSION,PROMPT,worked,keys,'easy'])
    fields = []
    for i,key in zip(order,keys):
        fid = ident([qid,key])
        choices = [{':answer/id':ident([fid,v]), ':answer/type':':answer.type/text',
                    ':answer/value':v} for v in ('false','true')]
        fields.append({':answer-field/id':fid, ':answer-field/key':key,
                       ':answer-field/type':':answer-field.type/checkbox',
                       ':answer-field/choices':choices,
                       ':answer-field/correct':[':answer/id',choices[int(classes[i]=='identity')][':answer/id']]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid, ':question/problem':normalize_prose(PROMPT),
                        ':question/worked-solution':worked,
                        ':question/difficulty':':question.difficulty/easy',
                        ':question/answer-fields':fields},
            'generation':{'version':VERSION,'seed':seed,'template':'direct',
                          'profile':'three_boolean_banks','parameters':{'equations':rows},
                          'field_order':order,'cases':classes,'sampler_rejections':rejections,
                          'domain':'x real','source_basis':4649,'source_ids':list(SOURCE_CASES),
                          'sympy':sp.__version__}}


def replay(source_id):
    data = SOURCE_CASES[source_id]
    # Captured DB reference lists do not preserve the solution's ordinal order.
    # Use its original equation sequence so visible fields and prose agree.
    return generate(parameters={'equations':data['equations']})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy',choices=['easy','moderate','hard'])
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--source-id',choices=list(SOURCE_CASES))
    args=parser.parse_args()
    if args.count < 1: parser.error('count must be positive')
    if args.difficulty != 'easy': parser.error('unsupported difficulty: only easy is source-calibrated')
    records=([replay(args.source_id)] if args.source_id else
             [generate(args.difficulty,args.seed+i) for i in range(args.count)])
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
