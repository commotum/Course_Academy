"""Seeded no-exchange 3x3 Gaussian elimination practice. No runtime writes."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import uuid

VERSION = '1.1.0'
KP = {'db_id': 17592186096672, 'id': '739b1cbc-c1a7-547d-a9fb-1f244bd36827',
      'title': 'Solving a 3x3 System of Equations Using Standard Gaussian Elimination'}
REFS = ['tutorial 3156 / 17592186097842', 'q-20505 / 17592186097183',
        'q-73569 / 17592186368702', 'q-130926 / 17592186266014', 'e-4701 / 17592186096459']
NS = uuid.UUID('9da32ac3-ce55-5f94-aae8-f54b4046d66c')

def uid(value):
    return str(uuid.uuid5(NS, value))

def tex(v):
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{' + str(abs(v.numerator)) + '}{' + str(v.denominator) + '}'

def matrix(rows):
    return r'\left[\begin{array}{ccc|c}' + r' \\ '.join(' & '.join(tex(v) for v in row) for row in rows) + r'\end{array}\right]'

def triple(values):
    return r'\langle ' + ','.join(tex(v) for v in values) + r'\rangle'

def polynomial(coeffs):
    terms = []
    for k, v in zip(('x', 'y', 'z'), coeffs):
        if not v:
            continue
        body = ('' if abs(v) == 1 else tex(abs(v))) + k
        terms.append(('-' if v < 0 else ('+' if terms else '')) + body)
    return ''.join(terms) or '0'

def system(rows):
    return r'\left\{\begin{aligned}' + r' \\ '.join(polynomial(row[:3]) + '&=' + tex(row[3]) for row in rows) + r'\end{aligned}\right.'

def eliminate(rows):
    current = [[Fraction(x) for x in row] for row in rows]
    stages = []
    def scale(i):
        pivot = current[i][i]
        if not pivot:
            raise ValueError('A row exchange would be required')
        if pivot != 1:
            current[i] = [v/pivot for v in current[i]]
            stages.append((rf'R_{i+1}:=' + tex(1/pivot) + rf'R_{i+1}', copy.deepcopy(current)))
    def cancel(i, j):
        multiple = -current[i][j]
        if multiple:
            current[i] = [x+multiple*y for x,y in zip(current[i], current[j])]
            sign = '+' if multiple > 0 else '-'
            coefficient = '' if abs(multiple) == 1 else tex(abs(multiple))
            stages.append((rf'R_{i+1}:=R_{i+1}' + sign + coefficient + rf'R_{j+1}', copy.deepcopy(current)))
    scale(0)
    cancel(1,0)
    cancel(2,0)
    scale(1)
    cancel(2,1)
    scale(2)
    return current, stages

def sample_parameters(rng, band):
    a,b,c = [rng.randint(-2,2) for _ in range(3)]
    u,v = [rng.randint(-4,4) for _ in range(2)]
    # Candidate bank and designated correct value are selected exchangeably.
    zs = rng.sample(list(range(-4,5)), 5)
    z = rng.choice(zs)
    profile = 'last-constraint'
    pairs = None
    if band != 'easy' and rng.choice([False,True]):
        profile = 'two-constraints'
        pairs = rng.sample([(y,z) for y in range(-4,5) for z in range(-4,5)],5)
        chosen_y,z = rng.choice(pairs)
        v = chosen_y+c*z
    nz = [-2,-1,1,2]
    if band == 'easy':
        p,d,f = 1,1,rng.choice(nz)
        m,n,t = rng.choice([0]+nz),rng.choice(nz),0
    elif band == 'moderate':
        p,d,f = rng.choice([1,-2,2,3]),1,rng.choice(nz)
        m,n,t = rng.choice([0]+nz),rng.choice(nz),rng.choice(nz)
    else:
        p,d,f = [rng.choice([-3,-2,2,3]) for _ in range(3)]
        m,n,t = [rng.choice(nz) for _ in range(3)]
    return {'a':a,'b':b,'c':c,'u':u,'v':v,'z':z,'p':p,'d':d,'f':f,
            'm':m,'n':n,'t':t,'candidates':zs,'bank_profile':profile,'pair_candidates':pairs,'given':rng.choice(['equations','matrix']),
            'response': 'ref' if band == 'easy' else rng.choice(['vector','assignments'])}

def construct(band, params):
    a,b,c,u,v,z,p,d,f,m,n,t = [params[k] for k in ('a','b','c','u','v','z','p','d','f','m','n','t')]
    U = [[1,a,b,u],[0,1,c,v],[0,0,1,z]]
    rows = [[p*x for x in U[0]],
            [m*x+d*y for x,y in zip(U[0],U[1])],
            [n*x+t*y+f*w for x,y,w in zip(*U)]]
    echelon, stages = eliminate(rows)
    assert echelon == U and stages
    x,y = u-a*(v-c*z)-b*z, v-c*z
    endpoint = params['response']
    given = params['given']
    problem = ('Consider the system of linear equations\n\n$$\n'+system(rows)+'.\n$$' if given == 'equations'
               else 'Consider the augmented matrix\n\n$$\nM='+matrix(rows)+'.\n$$')
    problem += '\n\nUse the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form'
    problem += '.' if endpoint == 'ref' else ', and then solve the linear system.'
    solution = 'The augmented matrix is\n\n$$\nM='+matrix(rows)+'.\n$$\n\n'
    for operation, state in stages:
        solution += 'Using $'+operation+'$, we obtain\n\n$$\n'+matrix(state)+'.\n$$\n\n'
    solution += 'The matrix is in row echelon form: each pivot lies to the right of the pivot above it, with zeros below each pivot.'
    if endpoint != 'ref':
        solution += '\n\nThe corresponding triangular system is\n\n$$\n'+system(U)+'.\n$$\n\n'
        solution += 'Back substitution gives\n\n$$\n'+r'\begin{aligned}z&='+tex(z)+r' \\ y&='+tex(v)+'-('+tex(c)+')('+tex(z)+')='+tex(y)+r' \\ x&='+tex(u)+'-('+tex(a)+')('+tex(y)+')-('+tex(b)+')('+tex(z)+')='+tex(x)+r'.\end{aligned}'+'\n$$\n\nTherefore, the solution is $'+triple([x,y,z])+'$.'
    values = []
    correct_index = None
    candidates = (params.get('pair_candidates') if params.get('bank_profile') == 'two-constraints'
                  else [(v-c*cz,cz) for cz in params['candidates']])
    for index,(cy,candidate) in enumerate(candidates):
        if candidate == z and cy == y:
            correct_index = index
        if endpoint == 'ref':
            C = copy.deepcopy(U); C[2][3] = candidate
            values.append('M\\sim '+matrix(C))
        else:
            cx = u-a*cy-b*candidate
            values.append(triple([cx,cy,candidate]) if endpoint == 'vector'
                          else f'x={cx},\\quad y={cy},\\quad z={candidate}')
    # Stable identities depend on substantive content, not seed or order of execution.
    token = hashlib.sha256(json.dumps([band,problem,solution,values],sort_keys=True).encode()).hexdigest()
    fieldid = uid(token+'/selection')
    choices = [{':answer/id':uid(fieldid+'/'+value), ':answer/type':{':db/ident':':answer.type/math'}, ':answer/value':value} for value in values]
    assert correct_index is not None
    key = choices[correct_index][':answer/id']
    q = {':question/id':uid(token), ':question/problem':problem, ':question/worked-solution':solution,
         ':question/difficulty':{':db/ident':':question.difficulty/'+band},
         ':question/answer-fields':[{':answer-field/id':fieldid, ':answer-field/key':'selection',
            ':answer-field/type':{':db/ident':':answer-field.type/radio'}, ':answer-field/choices':choices,
            ':answer-field/correct':[':answer/id',key]}]}
    return {'knowledge_point':KP, 'generation':{'version':VERSION,'template':given+'-to-'+endpoint+'-radio',
            'origin':'authored-from-target-teaching','source_refs':REFS,'source_basis':13939,
            'bank_profile':params.get('bank_profile','last-constraint'),'parameters':params,'augmented_matrix':rows,'solution':[x,y,z],
            'domain':'nonsingular real linear system; no exchanges; integer entries',
            'derivation':[{'operation':op,'matrix':[[str(v) for v in row] for row in M]} for op,M in stages]},'question':q}

def generate(band, count, seed):
    rng = random.Random(seed)
    records, seen = [],set()
    while len(records) < count:
        record = construct(band,sample_parameters(rng,band))
        # Do not count alternate banks or setup typography as new calculations.
        signature = json.dumps(record['generation']['augmented_matrix'])
        if signature in seen:
            continue
        seen.add(signature)
        record['generation']['seed'] = seed
        records.append(record)
    return records

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay',help='Source Math Academy ID, or all; preserves original observed bands')
    args = parser.parse_args()
    if args.count < 1:
        parser.error('--count must be positive')
    if args.replay:
        bank = json.loads(Path(__file__).with_name('source-replay.json').read_text())
        result = [r['record'] for r in bank if args.replay in ('all',r['source_math_academy_id'])]
        if not result:
            parser.error('Unknown source replay ID')
    else:
        result = generate('moderate' if args.difficulty == 'unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
