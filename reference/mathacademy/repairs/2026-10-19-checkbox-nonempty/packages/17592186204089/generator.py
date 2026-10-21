#!/usr/bin/env python3
"""Portable seeded affine no-solution classifier, adapted from 17592186204089-draft.py.

See instructional-account.md for source evidence and conservative extensions.
No database, repository imports, publication, or generated assets.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import re
import uuid
import sympy as sp
import math_format as _format

KP_ID = 17592186204089
KP_UUID = 'd6226fdb-ee73-5a78-87d5-9d6a988a9eb4'
TITLE = 'Identifying an Equation With No Solutions'
VERSION = '3.0.0'
SUPPORTED_LEVELS = ('easy',)
TEMPLATES = ('detailed-scaled','detailed-unit','summary-spaced','radio-detailed-scaled')
KEYS = ('I','II','III')
SOURCE = json.loads(Path(__file__).with_name('source.json').read_text())
ORIGINALS = {q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
RADIO_SOURCE_SUBSETS = ((0,),(0,2),(0,1),(0,1,2),(1,2))
RADIO_PERMUTATIONS = tuple(itertools.permutations(range(3)))
DOMAIN = {'coefficients':[-9,9], 'constants':[-9,9], 'variables':'xuyzwv',
 'decision_order':'bank and qualifying subset, nonqualifying classes, then compatible numbers',
 'difficulty':'easy only; source unrated labels retained separately', 'plots':'none'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def kind(e):
    a,b,c,d = e
    return 'U' if a != c else 'I' if b == d else 'N'

def affine(a,b,x,spaced=False):
    lead = ('' if a == 1 else '-' if a == -1 else str(a)) + x if a else ''
    if b:
        tail = str(abs(b))
        if lead:
            lead += (' + ' if b > 0 else ' - ') if spaced else ('+' if b > 0 else '-')
            lead += tail
        else: lead = str(b)
    return lead or '0'

def equation(e,x,spaced=False):
    a,b,c,d = e
    return affine(a,b,x,spaced) + (' = ' if spaced else '=') + affine(c,d,x,spaced)

def operation(v, symbol=''):
    return ('+' if v > 0 else '-') + ('' if abs(v) == 1 and symbol else str(abs(v))) + symbol if v else ''

def selection(eqs):
    chosen = [key for key,e in zip(KEYS,eqs) if kind(e) == 'N']
    return subset_text(i for i,e in enumerate(eqs) if kind(e)=='N')

def worked(p,template):
    x,eqs = p['variable'],p['equations']
    if template == 'summary-spaced':
        reduced = [x+'='+sp.latex(sp.Rational(d-b,a-c)) if a != c else 'an identity' if b == d else str(b)+'='+str(d) for a,b,c,d in eqs]
        i = next(i for i,e in enumerate(eqs) if kind(e) == 'N')
        return 'The equations reduce respectively to '+', '.join(reduced[:2])+', and '+reduced[2]+'. Only the '+('first','second','third')[i]+' has no solutions.'
    pieces = ["Let's attempt to solve each equation in turn:"]
    for index,(a,b,c,d) in enumerate(eqs):
        e=[a,b,c,d]; left=affine(a,b,x);right=affine(c,d,x)
        lines = [left+' & ='+right]
        if a == c:
            op=operation(-a,x)
            lines += [left+op+' & ='+right+op, str(b)+' & ='+str(d)+'.']
        else:
            op=operation(-c,x)+operation(-b)
            lines += [left+op+' & ='+right+op]
            solution=sp.latex(sp.Rational(d-b,a-c))
            if a-c != 1: lines += [affine(a-c,0,x)+' & ='+str(d-b)]
            lines += [x+' & ='+solution+'.']
        pieces += ['- For the '+('first','second','third')[index]+' equation, we have',
                   '$$\n\\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$']
        eq=equation(e,x)
        if kind(e)=='N':
            pieces += [f'This equation is false for all values of ${x}.$ Therefore, the equation ${eq}$ has no solutions.']
        elif kind(e)=='I': pieces += [f'This equation is true for all values of ${x}.$']
        else: pieces += [f'Therefore, the equation ${eq}$ has the unique solution ${x}={solution}.$']
    pieces += ['Therefore, the correct answer is "'+selection(eqs)+'."']
    return '\n\n'.join(pieces)

def fingerprint(p):
    # Normalize the variable name and common nonzero equation scaling.
    canonical=[]
    for row in p['equations']:
        divisor=math.gcd(*row)
        sign=1 if row[0] > 0 else -1
        canonical.append([v//divisor*sign for v in row])
    return digest(canonical)


def subset_text(indices):
    names=[KEYS[i] for i in sorted(indices)]
    if len(names)==3: return 'I, II, and III'
    if not names: raise ValueError('At least one contradiction required')
    return ' and '.join(names)+' only'

def radio_bank(order):
    return tuple(subset_text(i for i,old in enumerate(order) if old in subset)
                 for subset in RADIO_SOURCE_SUBSETS)

def original_template(mid):
    return ('radio-detailed-scaled' if mid=='q-288069' else
            'summary-spaced' if mid in ('q-287964','q-288058') else
            'detailed-unit' if mid=='q-288073' else 'detailed-scaled')

def source_parameters(q):
    # Checkbox equations live in their field labels, not in the prompt.
    fs=q[':question/answer-fields']
    expressions=([f[':answer-field/key'].strip('$') for f in fs]
                 if len(fs)==3 else re.findall(r'\$([^$]*=[^$]*)\$',q[':question/problem']))
    xname=re.search('[xuyzwv]',expressions[0])[0]; x=sp.Symbol(xname)
    rows=[]
    for expression in expressions:
        row=[]
        for side in expression.split('='):
            v=sp.sympify(re.sub(r'(\d)([xuyzwv])',r'\1*\2',side),locals={xname:x})
            row.extend((int(v.coeff(x)),int(v.subs(x,0))))
        rows.append(row)
    return {'variable':xname,'equations':rows}

SOURCE_CASES=[{'source_id':mid,'parameters':source_parameters(q),'template':original_template(mid),
               'source_difficulty':q.get(':question/difficulty')} for mid,q in ORIGINALS.items()]

def sample(rng,template):
    # Decide evidence-bearing relationships before compatible incidental values.
    order=list(rng.choice(RADIO_PERMUTATIONS))
    if template=='radio-detailed-scaled':
        subset=rng.choice(RADIO_SOURCE_SUBSETS)
        pattern=['N' if old in subset else rng.choice('UI') for old in order]
    else:
        roles='NUI' if template=='summary-spaced' else rng.choice(('NUI','NNU'))
        pattern=[roles[i] for i in order]
    nonzero=[i for i in range(-9,10) if i]
    eqs=[]
    for k in pattern:
        while True:
            a=rng.choice(nonzero); b=rng.randint(-9,9)
            if k=='U' and template=='detailed-unit':
                a=rng.choice([v for v in nonzero if v-1 in nonzero]); c=a-1
            else:
                c=a if k!='U' else rng.choice([v for v in nonzero if v!=a and
                   (template not in ('detailed-scaled','radio-detailed-scaled') or a-v!=1)])
            d=b if k=='I' else rng.randint(-9,9) if k=='U' else rng.choice([v for v in range(-9,10) if v!=b])
            row=[a,b,c,d]
            if row not in eqs:
                eqs.append(row)
                break
    return {'variable':rng.choice('xuyzwv'),'equations':eqs,'label_permutation':order}

def validate_parameters(p,template):
    p=copy.deepcopy(p)
    if p.get('variable') not in tuple('xuyzwv'): raise ValueError('Invalid variable')
    eqs=p.get('equations')
    if not isinstance(eqs,list) or len(eqs)!=3: raise ValueError('Three equations required')
    for e in eqs:
        if not isinstance(e,list) or len(e)!=4 or any(type(v) is not int or abs(v)>9 for v in e):
            raise ValueError('Bounded integer affine coefficients required')
        if e[0]==0 or e[2]==0: raise ValueError('Both variable coefficients must be nonzero')
    if len({tuple(e) for e in eqs})!=3: raise ValueError('Repeated equation')
    kinds=sorted(kind(e) for e in eqs)
    order=p.setdefault('label_permutation',[0,1,2])
    if sorted(order)!=[0,1,2]: raise ValueError('Invalid bank label permutation')
    if template=='radio-detailed-scaled':
        if selection(eqs) not in radio_bank(order): raise ValueError('Key absent from selected whole bank')
    elif kinds not in (list('INU'),list('NNU')) or (template=='summary-spaced' and kinds!=list('INU')):
        raise ValueError('Unsupported checkbox role multiset')
    if template in ('detailed-unit','detailed-scaled','radio-detailed-scaled'):
        for a,b,c,d in eqs:
            if a!=c and ((a-c==1)!=(template=='detailed-unit')):
                raise ValueError('Unique-solution equation does not match solution profile')
    return p

@_format.checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,source_id=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+str(level))
    rng=random.Random(seed)
    if source_id is not None:
        q=ORIGINALS[source_id]; template=original_template(source_id)
        parameters=source_parameters(q)
    template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES: raise ValueError('Unsupported template')
    p=validate_parameters(parameters if parameters is not None else sample(rng,template),template)
    radio=template=='radio-detailed-scaled'
    if radio:
        prompt='Which of the following equations has no solutions?\n\n'+'\n\n'.join(
            key+'. $'+equation(e,p['variable'])+'$' for key,e in zip(KEYS,p['equations']))
    else:
        # The actual UI puts each equation-owned checkbox below the prompt.
        prompt='Which of the following equations has no solutions?\n\nSelect all that apply.'
    solution=worked(p,template)
    if template=='summary-spaced':
        reduced=['$'+p['variable']+'='+sp.latex(sp.Rational(d-b,a-c))+'$' if a!=c else
                 'an identity' if b==d else '$'+str(b)+'='+str(d)+'$' for a,b,c,d in p['equations']]
        ordinal=('first','second','third')[next(i for i,e in enumerate(p['equations']) if kind(e)=='N')]
        solution='The equations reduce respectively to '+', '.join(reduced[:2])+', and '+reduced[2]+'. Only the '+ordinal+' has no solutions.'
    if not radio:
        end='; '.join('$'+equation(e,p['variable'])+'$' for e in p['equations'] if kind(e)=='N')+' only.'
        if template!='summary-spaced':
            solution=solution.rsplit('Therefore, the correct answer is ',1)[0]+'Therefore, the correct answer is '+end
    prompt=_format.normalize_prose(prompt); solution=_format.normalize_prose(solution)
    values=list(radio_bank(p['label_permutation'])) if radio else ['false','true']
    # Choice position is presentation only, never a semantic instance count.
    if radio and source_id is None: rng.shuffle(values)
    content=digest({'problem':prompt,'equations':p['equations'],'solution':solution,'bank':sorted(values),'level':level})
    qid=uid('question:'+content); fields=[]
    for i,e in enumerate([None] if radio else p['equations']):
        key='selection' if radio else '$'+equation(e,p['variable'],template=='summary-spaced')+'$'
        fid=uid(qid+':field:'+str(i)); bank_values=values
        if source_id is not None:
            bank_values=[a[':answer/value'] for a in ORIGINALS[source_id][':question/answer-fields'][i][':answer-field/choices']]
            if not radio: key=ORIGINALS[source_id][':question/answer-fields'][i][':answer-field/key']
        answers=[{':answer/id':uid(fid+':answer:'+v),':answer/type':':answer.type/text',':answer/value':v} for v in bank_values]
        correct=selection(p['equations']) if radio else str(kind(e)=='N').lower()
        fields.append({':answer-field/id':fid,':answer-field/key':key,
            ':answer-field/type':':answer-field.type/'+('radio' if radio else 'checkbox'),
            ':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]})
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,
       ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    if source_id:
        original=ORIGINALS[source_id]
        if ':question/difficulty' in original: question[':question/difficulty']=copy.deepcopy(original[':question/difficulty'])
        else: question.pop(':question/difficulty')
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
        'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,
           'bank_profile':'subset-five-relabelled' if radio else 'boolean-per-equation',
           'parameter_fingerprint':fingerprint(p),'source_id':source_id,
           'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],
           'source_difficulty':ORIGINALS[source_id].get(':question/difficulty') if source_id else None,
           'domain':DOMAIN,'plot_rating':'none'}}

def replay_source(source_id):
    """Original parameters/banks and original difficulty; repaired source ordinals."""
    return generate('easy',source_id=source_id)

def batch(level,count=5,seed=0):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+level)
    if type(count) is not int or count<0: raise ValueError('Nonnegative count required')
    records=[]; seen=set(); attempts=0
    while len(records)<count:
        record=generate(level,seed+attempts); attempts+=1
        fp=record['generation']['parameter_fingerprint']
        if fp not in seen: records.append(record); seen.add(fp)
        if attempts>max(100,count*20): raise ValueError('Cannot fill unique batch')
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy',choices=SUPPORTED_LEVELS)
    parser.add_argument('--count',type=int,default=5); parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    args=parser.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__': main()
