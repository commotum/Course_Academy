#!/usr/bin/env python3
"""Seeded easy REF pivot-column generator; offline and relocatable.

Reuses the matrix parsing, identity, formatting, and per-column Boolean structure
of the supplied 17592186124477.py. Repairs source fidelity and chooses qualifying
sets before numerical entries. See instructional-account.md for the scope.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import sys
import uuid
from pathlib import Path
from math_format import checked_math_content, matrix_tex, normalize_prose

CAPTURE = json.loads(Path(__file__).with_name('source_data.json').read_text())
SOURCE = CAPTURE['record']
KP_ID = 17592186124477
VERSION = 'pivot-columns-ref-4'
LEVELS = ('easy',)
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']}
RADIO_BANK = ((1,2,3,4,5), (1,4), (1,2,4), (1,2), (1,2,3,4))


def matrix(text):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S).group(1)
    return [[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]


def pivots(a):
    return tuple(next(j+1 for j,x in enumerate(row) if x) for row in a if any(row))


def tex(a):
    return matrix_tex([[str(x) for x in row] for row in a])


def ordinal(n):
    return f'${n}$'+('st' if n==1 else 'nd' if n==2 else 'rd' if n==3 else 'th')


def column_list(target):
    parts = [ordinal(x) for x in target]
    return parts[0] if len(parts)==1 else ' and '.join(parts) if len(parts)==2 else ', '.join(parts[:-1])+', and '+parts[-1]


def radio_value(columns, n=5):
    return 'All the columns are pivot' if len(columns)==n else column_list(columns)+' only'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']), digest(value)))


def kind(profile):
    return SOURCES[profile][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]


def targets(profile):
    a = matrix(SOURCES[profile][':question/problem']); m,n = len(a),len(a[0])
    ranks = (2,3) if kind(profile)=='radio' else range(1,min(m,n)+1)
    return [t for rank in ranks for t in itertools.combinations(range(1,n+1),rank)]


def bank_sets(permutation):
    return [tuple(sorted(permutation[j-1] for j in subset)) for subset in RADIO_BANK]


def fingerprint(q):
    a = matrix(q[':question/problem'])
    return digest(['pivot-columns',len(a),len(a[0]),pivots(a)])


def fill_matrix(m,n,target,rng):
    a = [[0]*n for _ in range(m)]
    for i,p in enumerate(target):
        a[i][p-1] = rng.choice([v for v in range(-9,10) if v])
        for j in range(p,n): a[i][j] = rng.randint(-9,9)
    return a


@checked_math_content
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,replay=False):
    if level not in LEVELS: raise ValueError('Unsupported difficulty; only easy is supported')
    rng = random.Random(seed)
    profile = profile or rng.choice(sorted(SOURCES))
    if profile not in SOURCES: raise ValueError('Unknown source profile')
    src = SOURCES[profile]; response = kind(profile)
    if template not in (None,'pivot-columns-ref',response): raise ValueError('Unsupported template')
    if field_type not in (None,response,':answer-field.type/'+response): raise ValueError('Source response format required')
    original = matrix(src[':question/problem']); m,n = len(original),len(original[0])
    if replay:
        if parameters is not None: raise ValueError('Replay uses original parameters')
        a = original
        bank = list(RADIO_BANK) if response=='radio' else None
    elif parameters is None:
        target = rng.choice(targets(profile))
        a = fill_matrix(m,n,target,rng)
        bank = None
    else:
        a = json.loads(json.dumps(parameters['matrix']))
        bank = [tuple(t) for t in parameters['bank']] if response=='radio' and 'bank' in parameters else None
    if len(a)!=m or any(len(row)!=n for row in a): raise ValueError('Wrong source shape')
    if any(type(v)!=int or not -9<=v<=9 for row in a for v in row): raise ValueError('Integer range [-9,9] required')
    target = pivots(a)
    if not target or len(set(target))!=len(target) or tuple(sorted(target))!=target: raise ValueError('REF required')
    if any(not any(row) for row in a[:len(target)]) or any(any(row) for row in a[len(target):]): raise ValueError('Zero rows must be last')
    if response=='radio':
        if not replay and target not in targets(profile): raise ValueError('Generated radio rank must be 2 or 3')
        if bank is None:
            alternatives = [t for t in itertools.combinations(range(1,n+1),len(target)) if t!=target]
            bank = [target]+rng.sample(alternatives,4)
        if len(bank)!=5 or len(set(bank))!=5 or target not in bank: raise ValueError('Five distinct column sets required')
        if any(tuple(sorted(set(t)))!=t or not set(t)<=set(range(1,n+1)) for t in bank): raise ValueError('Invalid bank subset')
        if not replay and any(len(t)!=len(target) for t in bank): raise ValueError('Equal-cardinality radio bank required')
    params = {'matrix':a}
    if response=='radio': params['bank'] = [list(t) for t in bank]
    prompt = re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda _:tex(a),src[':question/problem'],flags=re.S)
    name = re.search(r'matrix \$(\w+)\$',prompt).group(1)
    if replay:
        solution = src[':question/worked-solution']
    else:
        count = len(target)
        solution = ('Remember that the pivots of a matrix in row echelon form are the first non-zero entries in each row of the matrix.\n\n'
                    f'We can see that ${name}$ has ${count}$ '+('pivot in the ' if count==1 else 'pivots in the ')
                    + column_list(target)+(' column:' if count==1 else ' columns:')+'\n\n$$\n'+name+'='+tex(a)+'\n$$')
    q = {':question/problem':normalize_prose(prompt), ':question/worked-solution':normalize_prose(solution), ':question/difficulty':':question.difficulty/easy'}
    # Include the full radio bank in content identity, not its random order or seed.
    values = [radio_value(t,n) for t in bank] if response=='radio' else None
    identity = digest([VERSION,q,sorted(values) if values else response])
    qid = uid(identity)
    fields = []
    if response=='checkbox':
        for column in range(1,n+1):
            key = normalize_prose(f'Column {column}: $'+tex([[row[column-1]] for row in a])+'$')
            fid = uid([qid,key])
            answers = [{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
            fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[int(column in target)][':answer/id']]})
    else:
        fid = uid([qid,'selection'])
        answers = [{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in values]
        correct = answers[bank.index(target)][':answer/id']
        if not replay: rng.shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
    q.update({':question/id':qid,':question/answer-fields':fields})
    return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},
            'question':q,'generation':{'version':VERSION,'template':'pivot-columns-ref-'+response,'level':level,'profile':profile,'seed':seed,
            'parameters':params,'pivot_columns':list(target),'mathematical_fingerprint':fingerprint(q),'content_identity':identity,
            'source_replay':replay,'source_question_id':src[':question/id'],'eligible_for_learning':not replay,'evidence_only':replay,
            'bank_profile':('source-observed' if replay else 'equal-cardinality-extension') if response=='radio' else 'boolean-per-column',
            'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'python':sys.version.split()[0]}}


def generate_easy(seed=0,**kwargs):
    return generate('easy',seed,**kwargs)


def generate_many(level,count,seed=0,profile=None):
    if level not in LEVELS: raise ValueError('Unsupported difficulty; only easy is supported')
    if count<0: raise ValueError('count must be nonnegative')
    rng = random.Random(seed); records = []; seen = set()
    # Finite decision domain sampled without replacement, across observed shapes.
    # Neither profile frequency nor coefficients inflate this structural count.
    domain = {}
    for p in ([profile] if profile else sorted(SOURCES)):
        original = matrix(SOURCES[p][':question/problem']); m,n = len(original),len(original[0])
        for target in targets(p):
            domain.setdefault((m,n,target),[]).append(p)
    tasks = list(domain); rng.shuffle(tasks)
    for m,n,target in tasks:
        if len(records)>=count: break
        p = rng.choice(domain[(m,n,target)])
        a = fill_matrix(m,n,target,rng)
        rec = generate(level,seed=seed+len(records),profile=p,parameters={'matrix':a})
        fp = fingerprint(rec['question'])
        if fp not in seen:
            seen.add(fp); records.append(rec)
    if len(records)<count: raise ValueError(f'Finite structural limit {len(records)}; requested {count}')
    return records



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_many']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=LEVELS,default='easy')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--profile',choices=sorted(SOURCES))
    args = parser.parse_args()
    print(json.dumps(generate_many(args.difficulty,args.count,args.seed,args.profile),indent=2))
