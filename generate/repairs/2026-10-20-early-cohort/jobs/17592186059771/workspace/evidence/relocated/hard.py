"""Hard two-addition coefficient matrices; source replay and authored arithmetic bank."""
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path
from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex

VERSION = 'hard-row-additions-1.1.0'
KP_UUID = 'eb1afe82-86ba-5a15-9037-74717692ecb2'
COEFFICIENTS = tuple(range(-5, 0)) + tuple(range(1, 6))
PAIRS = tuple((a,b) for a in COEFFICIENTS for b in COEFFICIENTS)

def apply(matrix, operations):
    result = copy.deepcopy(matrix)
    for target, donor, factor in operations:
        result[target] = [x + factor*y for x,y in zip(result[target], result[donor])]
    return result

def canonical_parameters(parameters):
    """Translate the legacy shared-target API once, then own explicit operations."""
    p = copy.deepcopy(parameters)
    if 'operations' not in p:
        a,b = p['coefficients']
        p['operations'] = [[p['target'], p['donors'][0], a],
                           [p['target'], p['donors'][1], b]]
    for key in ('target','donors','coefficients'):
        p.pop(key, None)
    return p


def operations(p, pair=None):
    ops = p.get('operations')
    if ops is None:
        ops = canonical_parameters(p)['operations']
    if pair is None:
        return [tuple(op) for op in ops]
    return [(t, donor, factor) for (t, donor, _), factor in zip(ops, pair)]


def relationship(ops):
    if len(ops)!=2 or any(len(op)!=3 for op in ops):
        raise ValueError('Two explicit row additions are required')
    if any(type(v)!=int for op in ops for v in op):
        raise ValueError('Integer row roles and coefficients required')
    if any(t not in range(3) or d not in range(3) or t==d or k not in COEFFICIENTS for t,d,k in ops):
        raise ValueError('Distinct eligible row roles and bounded nonzero coefficients required')
    t1,d1,_ = ops[0]; t2,d2,_ = ops[1]
    if t1==t2 and d1!=d2:
        return 'shared-target'
    if d1==d2 and t1!=t2:
        return 'shared-donor'
    raise ValueError('Expected shared target with two donors or shared donor with two targets')

def op_tex(op):
    t,s,k = op
    rhs = ('+' if k>0 else '-') + (str(abs(k)) if abs(k)!=1 else '') + '{R}_{'+str(s+1)+'}'
    return '{R}_{'+str(t+1)+'}:={R}_{'+str(t+1)+'}'+rhs

def render(matrix, ops, name):
    ordinal = ['first', 'second', 'third']
    prompt = ('Consider the matrix $'+name+',$ given by\n\n$$\n'+name+'='+matrix_tex(matrix)+'.\n$$\n\n'
              'What matrix results from carrying out the following row operations on $'+name+'?$\n\n$$\n'
              +r'\begin{aligned}'+r' \\ '.join(op_tex(op).replace(':=',' & :=') for op in ops)+r'\end{aligned}'+'\n$$')
    sentences = ["Let's list the required operations:"]
    for t,s,k in ops:
        sentences.append('- The operation $'+op_tex((t,s,k))+'$ means that we need to add $'+str(k)+'$ times the '+ordinal[s]+' row to the '+ordinal[t]+' row.')
    # Separate the operations from matrices so the source's five-stage derivation
    # wraps within the actual UI; no horizontal chain wider than a single matrix.
    stages = [name+' & ='+matrix_tex(matrix)]
    current = copy.deepcopy(matrix)
    for t,s,k in ops:
        expanded = copy.deepcopy(current)
        expanded[t] = [f'{x}+({k})({y})' for x,y in zip(current[t],current[s])]
        stages[-1] += r'\quad '+op_tex((t,s,k))
        stages.append(r' & \sim '+matrix_tex(expanded))
        current = apply(current,[(t,s,k)])
        stages.append(r' & \sim '+matrix_tex(current))
    solution = '\n\n'.join(sentences)+'\n\nApplying the operations, we obtain the following:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(stages)+r'\end{aligned}'+'\n$$'
    return tuple(map(normalize_prose,(prompt,solution)))

def validate(p):
    m = p['matrix']
    if len(m)!=3 or any(len(row)!=3 for row in m) or any(type(v)!=int or not -9<=v<=9 for row in m for v in row):
        raise ValueError('A 3x3 integer matrix with entries -9..9 is required')
    ops = operations(p)
    relationship(ops)
    pairs = p['candidate_pairs']
    if len(pairs)!=5 or len({tuple(pair) for pair in pairs})!=5 or any(tuple(pair) not in PAIRS for pair in pairs):
        raise ValueError('Five distinct nonzero bounded coefficient pairs are required')
    if [op[2] for op in ops] not in pairs or p['name'] not in ('B','C'):
        raise ValueError('Requested pair must belong to the complete bank')
    if any(not any(m[d]) for d in {op[1] for op in ops}):
        raise ValueError('Each donor must contribute nonzero evidence')
    if len({matrix_tex(apply(m,operations(p,pair))) for pair in pairs})!=5:
        raise ValueError('Candidate results collide')

def build(p, seed, attempts):
    p = canonical_parameters(p)
    validate(p)
    case = relationship(operations(p))
    pairs = sorted(p['candidate_pairs'])
    bank = [apply(p['matrix'],operations(p,pair)) for pair in pairs]
    return record(p['matrix'], operations(p), p['name'], bank, seed,
                  {'profile':'two-donor-arithmetic' if case=='shared-target' else 'two-target-arithmetic',
                   'relationship':case,'parameters':copy.deepcopy(p),
                   'sampling_attempts':attempts,'source_question':['q-130010'] if case=='shared-target' else ['q-130064','q-130065','q-10245'],
                   'candidate_pairs_in_bank_order':pairs})

def record(matrix, ops, name, bank, seed, metadata):
    prompt,solution = render(matrix,ops,name)
    values = [normalize_tex(matrix_tex(b)) for b in bank]
    correct_value = normalize_tex(matrix_tex(apply(matrix,ops)))
    assert values.count(correct_value)==1 and len(set(values))==5
    identity = json.dumps([prompt,sorted(values),VERSION],separators=(',',':'))
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID),identity))
    fid = str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),
                ':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct_id = next(c[':answer/id'] for c in choices if c[':answer/value']==correct_value)
    random.Random(seed).shuffle(choices)
    # Ignore letter, bank, answer order, seed and row labels for semantic identity.
    if len({op[0] for op in ops})==1:
        t = ops[0][0]
        semantic = [matrix[t],sorted([[matrix[s],k] for _,s,k in ops])]
    else:
        donor = ops[0][1]
        semantic = ['shared-donor',matrix[donor],sorted([[matrix[t],k] for t,_,k in ops])]
    fingerprint = hashlib.sha256(json.dumps(semantic,separators=(',',':')).encode()).hexdigest()
    return {'knowledge_point':{'db_id':17592186059771,'id':KP_UUID,'title':'Applying Row Operations To a Coefficients Matrix'},
            'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
                        ':question/difficulty':':question.difficulty/hard',
                        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
                        ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
                        ':answer-field/correct':[':answer/id',correct_id]}]},
            'generation':{'version':VERSION,'template':'two-row-additions','seed':seed,
                          'source_basis':4572,'mathematical_fingerprint':fingerprint,**metadata}}

@checked_math_content
def generate(seed=0, parameters=None):
    if parameters is not None:
        return build(copy.deepcopy(parameters),seed,1)
    rng = random.Random(seed)
    case = rng.choice(('shared-target','shared-donor'))
    anchor,r1,r2 = rng.sample(range(3),3)
    pairs = sorted([list(pair) for pair in rng.sample(PAIRS,5)])
    requested = rng.choice(pairs)
    # Key choice does not enter either the bank or its acceptance criterion.
    roles = [(anchor,r1),(anchor,r2)] if case=='shared-target' else [(r1,anchor),(r2,anchor)]
    p = {'operations':[[t,d,k] for (t,d),k in zip(roles,requested)],
         'candidate_pairs':pairs,'name':rng.choice(('B','C'))}
    for attempts in range(1,501):
        p['matrix'] = [[rng.randint(-9,9) for _ in range(3)] for _ in range(3)]
        try:
            validate(p)
        except ValueError:
            continue
        return build(p,seed,attempts)
    raise ValueError('Bounded hard sampling exhausted')

@checked_math_content
def replay(source_id, seed=0):
    """Exact original banks only; never offered as normal-generation profiles."""
    sources = json.loads(Path(__file__).with_name('hard_sources.json').read_text())
    item = sources[source_id]
    p = item['parameters']
    return record(p['matrix'],p['operations'],p['name'],item['bank'],seed,
                  {'profile':source_id,'parameters':copy.deepcopy(p),'source_question':source_id,
                   'replay_only':True,'source_difficulty':'hard','choice_recipes':'exact source bank; no inferred generalization'})
