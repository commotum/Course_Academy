#!/usr/bin/env python3
"""Seeded easy matrix-dimension questions; adapted from 17592186087693-draft.py.

Preserves its explicit parameter validation, complete observed recipe banks,
content-derived field-owned identities, replay API and finite-shape batches.
Updates evidence to the supplied capture and replaces cue-bearing normal banks.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186087693-source-policy.json'))
    raise SystemExit(0)

from pathlib import Path
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
import sympy as sp
from math_format import checked_math_content, matrix_operands, matrix_tex, normalize_prose, normalize_tex

KP_ID = 17592186087693
KP_UUID = 'f6ae25fc-16eb-598b-a288-742e4b46cb12'
TITLE = 'Determining the Dimensions of a Matrix'
VERSION = '3.0.0'
HERE = Path(__file__).resolve().parent
OBSERVED = json.loads((HERE / 'recipes.json').read_text())
SOURCE = json.loads((HERE / 'source-cases.json').read_text())
SOURCE_RECORDS = {q[':question/math-academy-id']: q for q in SOURCE['questions']}
SUPPORTED_LEVELS = ('easy',)
TEMPLATES = ('radio', 'where-dual-blank', 'let-dual-blank', 'chelsea-dual-blank')
DIMENSIONS = tuple((r,c) for r in range(2,7) for c in range(2,7))
R,C = sp.symbols('r c', integer=True, positive=True)


def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def uid(x):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),x))


def validate_parameters(parameters, level='easy'):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+str(level))
    if not isinstance(parameters,dict) or set(parameters) != {'entries','name'}:
        raise ValueError('Parameters must contain exactly entries and name')
    name, entries = parameters['name'], parameters['entries']
    if not isinstance(name,str) or not re.fullmatch('[A-Z]',name):
        raise ValueError('Invalid matrix name')
    if not isinstance(entries,list) or not 2 <= len(entries) <= 6:
        raise ValueError('Easy requires 2..6 rows')
    if any(not isinstance(row,list) or not 2 <= len(row) <= 6 for row in entries) or len({len(row) for row in entries}) != 1:
        raise ValueError('Easy requires rectangular rows with 2..6 columns')
    canonical=[]
    for row in entries:
        vals=[]
        for cell in row:
            if isinstance(cell,bool) or not isinstance(cell,(str,int)):
                raise ValueError('Entry must be supported scalar text or integer')
            s=str(cell).strip()
            integer=bool(re.fullmatch(r'-?\d{1,2}',s)) and abs(int(s))<=30
            special=(re.fullmatch(r'-?\\sqrt\{(?:[2-9]|1[0-3])\}',s) or
                     re.fullmatch(r'-?\\frac\{(?:[1-9]|[12][0-9]|30)\}\{[1-9]\}',s))
            if not (integer or special):
                raise ValueError('Unsupported/illegible entry')
            vals.append(str(int(s)) if integer else s)
        canonical.append(vals)
    return {'entries':canonical,'name':name}


def recipe_value(recipe,r,c):
    return tuple(int(sp.sympify(s,locals={'r':R,'c':C}).subs({R:r,C:c})) for s in recipe.split(','))


def source_parameters(source_id):
    q=SOURCE_RECORDS[source_id]
    body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
    entries=[[v.strip() for v in row.split('&')] for row in body.split('\\\\')]
    name=re.search(r'\$([A-Z])',q[':question/problem'])[1]
    return {'entries':entries,'name':name}


def make_prompt(template,p):
    name=p['name']
    if template=='chelsea-dual-blank':
        # The captured source refers to an absent table. The displayed matrix
        # alone supplies all evidence needed for this dimension-counting task.
        operand=matrix_operands([name+' = '+matrix_tex(p['entries'])])
        return ('Chelsea represents information using the following matrix:\n\n'+operand+
                '\n\nThe dimensions of $'+name+'$ are\n\n{{field-1}} $\\times$ {{field-2}}.')
    operand=matrix_operands([name+' = '+matrix_tex(p['entries'])+('.' if template=='let-dual-blank' else '?')])
    if template=='let-dual-blank':
        return 'Let\n\n'+operand+'\n\nThe dimensions of the matrix $'+name+'$ are\n\n{{field-1}} $\\times$ {{field-2}}.'
    prompt='What are the dimensions of the matrix $'+name+'$, where\n\n'+operand
    if template=='where-dual-blank':
        prompt+='\n\nThe dimensions of $'+name+'$ are\n\n{{field-1}} $\\times$ {{field-2}}.'
    return prompt


@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,profile=None,bank=None):
    """Observed profiles are explicit replay only; normal bank has exchangeable keys.

    Explicit parameters allow controlled role tests. A caller-supplied bank must
    contain five distinct supported shapes and include the supplied shape.
    """
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+str(level))
    if profile is not None and profile not in OBSERVED:
        raise ValueError('Unknown source profile')
    rng=random.Random(seed)
    spec=OBSERVED.get(profile)
    if spec:
        if template is not None and template!=spec['template']:
            raise ValueError('Profile/template mismatch')
        if bank is not None:
            raise ValueError('Source replay requires its complete observed bank')
        template=spec['template']
        parameters=source_parameters(spec['source']) if parameters is None else parameters
    else:
        template=rng.choice(TEMPLATES) if template is None else template
    if template not in TEMPLATES:
        raise ValueError('Unknown template')
    kind='radio' if template=='radio' else 'blank'
    if kind=='blank' and bank is not None:
        raise ValueError('Blank template does not accept a bank')
    # Bank set, then correct role, then incidental values. Explicit parameter
    # tests condition the same uniform bank construction on the supplied shape.
    if parameters is None:
        values=rng.sample(DIMENSIONS,5) if kind=='radio' else []
        r,c=rng.choice(values if values else DIMENSIONS)
        pool=[str(v) for v in range(-9,10)]+[r'\sqrt{2}',r'-\sqrt{3}',r'\frac{1}{3}']
        parameters={'entries':[[rng.choice(pool) for _ in range(c)] for _ in range(r)],
                    'name':rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
    p=validate_parameters(parameters,level)
    r,c=len(p['entries']),len(p['entries'][0])
    if kind=='radio':
        if spec:
            values=[recipe_value(a['recipe'],r,c) for a in spec['bank']]
        elif bank is not None:
            values=[tuple(v) for v in bank]
        elif 'values' not in locals():
            values=[(r,c)]+rng.sample([v for v in DIMENSIONS if v!=(r,c)],4)
        if len(values)!=5 or len(set(values))!=5 or values.count((r,c))!=1:
            raise ValueError('Invalid complete bank')
        if not spec and any(v not in DIMENSIONS for v in values):
            raise ValueError('Normal bank must use supported dimensions')
    else:
        values=[]
    name=p['name']
    prompt=normalize_prose(make_prompt(template,p))
    solution=normalize_prose(f'The matrix ${name}$ has ${r}$ rows and ${c}$ columns. Therefore, its dimensions are ${r}\\times {c}.$')
    keys=['selection'] if kind=='radio' else ['field-1','field-2']
    displayed=[[normalize_tex(f'{a}\\times {b}') for a,b in values]] if kind=='radio' else [[str(r)],[str(c)]]
    # Preserve original absence of source difficulty in replay. All normal items
    # are easy. This is not a license to publish an unrated source as rated.
    raw=SOURCE_RECORDS[spec['source']] if spec else None
    has_difficulty=not spec or ':question/difficulty' in raw
    content=digest({'version':VERSION,'difficulty':level if has_difficulty else None,
                    'prompt':prompt,'solution':solution,
                    'fields':[(key,kind,sorted(vals)) for key,vals in zip(keys,displayed)]})
    fields=[]
    for key,vals in zip(keys,displayed):
        fieldid=uid(content+':field:'+key)
        answers=[{':answer/id':uid(fieldid+':answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
        index=values.index((r,c)) if kind=='radio' else 0
        correct=answers[index][':answer/id']
        rng.shuffle(answers)
        fields.append({':answer-field/id':fieldid,':answer-field/key':key,
                       ':answer-field/type':':answer-field.type/'+kind,
                       ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
    q={':question/id':uid(content),':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    if has_difficulty:
        q[':question/difficulty']=':question.difficulty/'+level
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,
                          'seed':seed,'level':level,'template':template,'parameters':p,
                          'bank_profile':profile or ('independent-dimensions' if kind=='radio' else 'dual-blank'),
                          'bank_origin':'observed-expression-pattern' if spec else 'authored-conservative-extension',
                          'bank_pairs':values,'semantic_shape':[r,c],'semantic_family_size':25,
                          'source_ids':[spec['source']] if spec else list(SOURCE_RECORDS),
                          'source_basis':SOURCE['basis'],'replay_only':bool(spec),
                          'difficulty_origin':'original-source' if spec else 'source-justified-easy',
                          'plot_rating':'none','content_fingerprint':content}}


def batch(level,count,seed=0,template=None):
    """Reject repeated semantic shapes; entry changes never fill a 26th slot."""
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: '+str(level))
    if type(count) is not int or not 1<=count<=len(DIMENSIONS):
        raise ValueError('Finite easy limit: 25 ordered dimension tasks')
    rng=random.Random(seed)
    records=[]
    seen=set()
    rejected=0
    while len(records)<count:
        rec=generate(level,rng.getrandbits(64),template)
        shape=tuple(rec['generation']['semantic_shape'])
        if shape in seen:
            rejected+=1
            continue
        seen.add(shape)
        records.append(rec)
    for rec in records:
        rec['generation']['batch_seed']=seed
        rec['generation']['batch_rejected_repeated_shapes']=rejected
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy',choices=SUPPORTED_LEVELS)
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    try:
        records=batch(args.difficulty,args.count,args.seed)
    except ValueError as e:
        parser.error(str(e))
    print(json.dumps(records,indent=2))



from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186087693-source-policy.json'))

if __name__=='__main__':
    main()
