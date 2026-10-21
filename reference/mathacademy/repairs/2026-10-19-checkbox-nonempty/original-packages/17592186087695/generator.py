#!/usr/bin/env python3
"""Seeded zero-matrix recognition. Offline, relocatable, source-backed easy band."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import random
import re
import uuid
import itertools
from fractions import Fraction
from pathlib import Path

from math_format import matrix_tex, normalize_prose, checked_math_content

HERE = Path(__file__).resolve().parent
KP_ID = 17592186087695
KP_UUID = 'ddb59990-7419-585f-aa1b-901d59c8cfc1'
TITLE = 'Identifying a Zero Matrix'
VERSION = '3.0.0'
SUPPORTED_LEVELS = ('easy',)
SOURCES = json.loads((HERE / 'source_specs.json').read_text())
# Complete observed radio banks, indexed by roles in their original arrays.
PROFILES = {k: SOURCES[k]['banks'][0]['values'] for k in ('q-11553', 'q-7827')}
SUBSETS = tuple(tuple(i for i in range(3) if bits & (1 << i)) for bits in range(1, 8))
ENTRY_VALUES = ('0', '1', '0.1', '3', '10')


def arrays(text):
    """Read the actual displayed named arrays, not generation metadata."""
    out = {}
    for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}', text):
        out[m[1]] = [[v.strip() for v in row.strip().split('&')] for row in m[2].split('\\\\')]
    if len(out) != 3:
        raise ValueError('Three complete distinct named matrices required')
    return out


def fingerprint_text(text):
    # Labels and positive magnitudes do not constitute new recognition tasks.
    objects = [[len(rows), len(rows[0]), [[int(Fraction(v) != 0) for v in row] for row in rows]]
               for rows in arrays(text).values()]
    return hashlib.sha256(json.dumps(objects, separators=(',', ':')).encode()).hexdigest()


def uid(scope, value):
    return str(uuid.uuid5(uuid.UUID(scope), value))


def sample_parameters(target, rng):
    attempts = 0
    while True:
        attempts += 1
        shapes = [(rng.randint(1, 4), rng.randint(1, 6)) for _ in range(3)]
        if sum(r*c for r,c in shapes) <= 50:
            break
    p = {'labels': rng.sample(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 3), 'matrices': [], 'witnesses': []}
    for i, (r,c) in enumerate(shapes):
        count = 0 if i in target else rng.randint(1, min(4,r*c))
        rows = [['0'] * c for _ in range(r)]
        cells = rng.sample(range(r*c), count)
        for cell in cells:
            rows[cell // c][cell % c] = rng.choice(ENTRY_VALUES[1:])
        p['matrices'].append(rows)
        p['witnesses'].append([cells[0] // c + 1, cells[0] % c + 1] if cells else None)
    return p, attempts-1


def validate_parameters(p):
    if not isinstance(p, dict) or set(p) != {'labels', 'matrices', 'witnesses'}:
        raise ValueError('Parameters require exactly labels, matrices, witnesses')
    labels, matrices, witnesses = p['labels'], p['matrices'], p['witnesses']
    if len(labels) != 3 or len(set(labels)) != 3 or any(not isinstance(x, str) or not re.fullmatch('[A-Z]', x) for x in labels):
        raise ValueError('Three distinct uppercase labels required')
    if len(matrices) != 3 or len(witnesses) != 3:
        raise ValueError('Three matrix/witness slots required')
    zero = []
    for i, rows in enumerate(matrices):
        if not rows or not 1 <= len(rows) <= 4 or not 1 <= len(rows[0]) <= 6 or any(len(z) != len(rows[0]) for z in rows):
            raise ValueError('Matrix outside 1–4 by 1–6 rectangular domain')
        if any(not isinstance(v, str) or v not in ENTRY_VALUES for row in rows for v in row):
            raise ValueError('Entry outside explicit observed number-form domain')
        nz = [(r+1, c+1) for r,row in enumerate(rows) for c,v in enumerate(row) if Fraction(v) != 0]
        if len(nz) > 4:
            raise ValueError('At most four nonzero entries per matrix')
        w = witnesses[i]
        if nz and (not isinstance(w,list) or len(w)!=2 or any(type(x) is not int for x in w) or tuple(w) not in nz):
            raise ValueError('Witness must identify an actually nonzero cell')
        if not nz and w is not None:
            raise ValueError('Zero matrices have no nonzero witness')
        zero.append(not nz)
    if not any(zero):
        raise ValueError('Empty qualifying subset is outside the supported source family')
    if sum(len(z)*len(z[0]) for z in matrices) > 50:
        raise ValueError('Recognition workload ceiling is 50 entries')
    return tuple(i for i,z in enumerate(zero) if z)


def choose_bank(target, rng, profile=None):
    candidates=[]
    for name, masks in PROFILES.items():
        if profile is not None and profile != name:
            continue
        for perm in itertools.permutations(range(3)):
            bank=[sorted(perm[i] for i in mask) for mask in masks]
            if list(target) in bank:
                candidates.append((name, list(perm), bank))
    if not candidates:
        raise ValueError('No compatible complete radio bank')
    return rng.choice(candidates)


def subset_text(labels, mask):
    names=['$'+labels[i]+'$' for i in mask]
    return names[0]+', '+names[1]+', and '+names[2] if len(names)==3 else ' and '.join(names)+' only'


def question_record(level, seed, problem, worked, banks, metadata):
    problem, worked = normalize_prose(problem), normalize_prose(worked)
    qid=uid(KP_UUID,json.dumps([VERSION,level,problem,worked,banks],sort_keys=True))
    rng=random.Random(seed)
    fields=[]
    for key,typ,values,correct in banks:
        fid=uid(qid,'field:'+key)
        answers=[{':answer/id':uid(fid,v), ':answer/type':':answer.type/text', ':answer/value':v} for v in values]
        rng.shuffle(answers)
        fields.append({':answer-field/id':fid, ':answer-field/key':key, ':answer-field/type':':answer-field.type/'+typ,
                       ':answer-field/choices':answers, ':answer-field/correct':[':answer/id',uid(fid,correct)]})
    q={':question/id':qid, ':question/problem':problem, ':question/worked-solution':worked, ':question/answer-fields':fields}
    if level is not None:
        q[':question/difficulty']=level if level.startswith(':') else ':question.difficulty/'+level
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE}, 'question':q,
            'generation':{'version':VERSION,'seed':seed, 'source_basis':4474,
                          'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
                          'python_version':sys.version.split()[0], 'plots':'none', **metadata}}


def conclusion(labels, zero):
    names = ['$'+x+'$' for x, z in zip(labels, zero) if z]
    if len(names) == 3:
        return 'Therefore, '+names[0]+', '+names[1]+', and '+names[2]+' are zero matrices.'
    if len(names) == 2:
        return 'Therefore, only '+' and '.join(names)+' are zero matrices.'
    return 'Therefore, only '+names[0]+' is a zero matrix.'


def build(level, seed=0, template=None, parameters=None, profile=None, target=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Only source-backed easy difficulty is supported')
    if type(seed) is not int:
        raise ValueError('Seed must be an integer')
    rng=random.Random(seed)
    template=template or ('radio' if profile else rng.choice(('checkbox','radio')))
    if template not in ('checkbox','radio'):
        raise ValueError('Unknown response template')
    if parameters is None:
        target=tuple(target) if target is not None else rng.choice(SUBSETS)
        if target not in SUBSETS:
            raise ValueError('Target must be an ordered nonempty subset of positions 0,1,2')
        # Answer-bearing assignment precedes bank, numerical values and labels.
        selected=choose_bank(target,rng,profile) if template=='radio' else None
        p,rejected_shapes=sample_parameters(target,rng)
    else:
        p=json.loads(json.dumps(parameters))
        actual=validate_parameters(p)
        if target is not None and tuple(target)!=actual:
            raise ValueError('Requested target conflicts with supplied matrices')
        target=actual
        selected=choose_bank(target,rng,profile) if template=='radio' else None
        rejected_shapes=0
    validate_parameters(p)
    labels,matrices,ws=p['labels'],p['matrices'],p['witnesses']
    named=['$'+n+'='+matrix_tex(rows)+'$' for n,rows in zip(labels,matrices)]
    problem='Which of the following are zero matrices?'
    if template=='radio':
        problem+='\n\n<div class="matrix-operands matrix-operands-stacked">\n'+'\n'.join('<div>'+v+'</div>' for v in named)+'\n</div>'
    else:
        problem+='\n\nSelect all that apply.'
    bullets=[]
    for i,n in enumerate(labels):
        if template=='radio':
            sentence='- $'+n+'$ is '+('' if i in target else 'not ')+'a zero matrix.'
        elif i in target:
            sentence='- $'+n+'$ is a zero matrix since *all* its entries are zeros.'
        else:
            r,c=ws[i]
            sentence='- $'+n+'$ is *not* a zero matrix since '+('one of its entries is not zero (' if sum(v!='0' for row in matrices[i] for v in row)==1 else 'some of its entries are not zeros (for instance, ')
            sentence+='$'+n.lower()+'_{'+str(r)+str(c)+'}='+matrices[i][r-1][c-1]+r'\ne 0$).'
        bullets.append(sentence)
    worked='\n\n'.join(bullets)+'\n\n'+conclusion(labels,[i in target for i in range(3)])
    if template=='checkbox':
        banks=[(key,'checkbox',['false','true'],str(i in target).lower()) for i,key in enumerate(named)]
        profile_name='true-false'; permutation=None; masks=None
    else:
        profile_name,permutation,masks=selected
        values=[subset_text(labels,m) for m in masks]
        banks=[('selection','radio',values,subset_text(labels,target))]
    display=problem+'\n'+'\n'.join(named) if template=='checkbox' else problem
    return question_record(level,seed,problem,worked,banks,{
        'template':template,'bank_profile':profile_name,'bank_role_permutation':permutation,'subset_masks':masks,
        'target':list(target),'parameters':p,'parameter_fingerprint':fingerprint_text(display),
        'shape_rejections':rejected_shapes,'source_ids':list(SOURCES)[:-1], 'difficulty_status':'source-backed easy'})


@checked_math_content
def generate(level='easy', seed=0, template=None, parameters=None, profile=None, target=None):
    return build(level,seed,template,parameters,profile,target)


def fill(text,p):
    for i,n in enumerate(p['labels']):
        replacements={f'@L{i}@':n,f'@l{i}@':n.lower(),f'@M{i}@':matrix_tex(p['matrices'][i])}
        if p['witnesses'][i]:
            r,c=p['witnesses'][i]
            replacements.update({f'@r{i}@':str(r),f'@c{i}@':str(c),f'@v{i}@':p['matrices'][i][r-1][c-1]})
        for k,v in replacements.items():
            text=text.replace(k,v)
    if '@' in text:
        raise ValueError('Unfilled replay template')
    return text


@checked_math_content
def replay(source_id):
    s=SOURCES[source_id]
    p=json.loads(json.dumps(s['parameters']))
    validate_parameters(p)
    banks=[]
    for b in s['banks']:
        values=[subset_text(p['labels'],m) for m in b['values']] if s['field_type']=='radio' else b['values']
        banks.append((fill(b['key'],p),s['field_type'],values,values[b['correct_index']]))
    return question_record(s['difficulty'],0,fill(s['problem_template'],p),fill(s['solution_template'],p),banks,
                           {'source_id':source_id,'parameters':p,'template':'source-replay'})


def batch(level, count, seed=0, template=None, profile=None, return_stats=False):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Only source-backed easy difficulty is supported')
    if type(count) is not int or not 1<=count<=1000:
        raise ValueError('Count must be 1–1000')
    records=[]; used=set(); duplicate_rejections=0; shape_rejections=0
    for n in range(count*100+1000):
        r=generate(level,seed+n,template=template,profile=profile)
        shape_rejections+=r['generation']['shape_rejections']
        fp=r['generation']['parameter_fingerprint']
        if fp in used:
            duplicate_rejections+=1
            continue
        used.add(fp); records.append(r)
        if len(records)==count:
            stats={'attempts':n+1,'semantic_duplicate_rejections':duplicate_rejections,'shape_rejections':shape_rejections}
            return (records,stats) if return_stats else records
    raise ValueError('Insufficient distinct mathematical tasks')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='easy')
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    parser.add_argument('--template',choices=('radio','checkbox'))
    parser.add_argument('--profile',choices=tuple(PROFILES))
    args=parser.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed,args.template,args.profile),indent=2))
