#!/usr/bin/env python3
"""Three independent checkbox classifications of affine real equations.

Only the observed easy demand is supported. No variable names, seeds, field
identities or answer ordering enter the mathematical task fingerprint.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import os
import sys
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and interpreter.is_file() and Path(sys.executable).resolve()!=interpreter.resolve():
        os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
    raise

KP_ID = 17592186204089
KP_UUID = 'd6226fdb-ee73-5a78-87d5-9d6a988a9eb4'
TITLE = 'Identifying an Equation With No Solutions'
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy',)
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
HERE = Path(__file__).resolve().with_suffix('')
KEYS = ('I', 'II', 'III')
DOMAIN = {'variable': 'x,u,y,z,w,v', 'coefficients': [-9, 9], 'constants': [-9, 9],
          'equations': 3, 'domain': 'real numbers', 'patterns': ['UIN', 'NIU', 'NNU', 'UNI'],
          'sampling_policy': 'Observed integer affine forms; all coefficient signs permitted; one or two contradictions; at least one unique solution. No distribution or fractions in equation inputs.'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def parameters(p):
    if set(p) != {'variable', 'equations'} or p['variable'] not in 'xuyzwv' or len(p['variable']) != 1:
        raise ValueError('Invalid variable/parameter keys')
    eqs = p['equations']
    if not isinstance(eqs, list) or len(eqs) != 3 or any(not isinstance(e, list) or len(e) != 4 for e in eqs):
        raise ValueError('Three [left coefficient, left constant, right coefficient, right constant] rows required')
    if any(type(v) is not int or abs(v) > 9 for e in eqs for v in e) or any(e[0] == 0 or e[2] == 0 for e in eqs):
        raise ValueError('Nonzero integer coefficients and bounded integer constants required')
    if ''.join(kind(e) for e in eqs) not in DOMAIN['patterns']:
        raise ValueError('Unobserved classification pattern')
    return {'variable': p['variable'], 'equations': [e[:] for e in eqs]}

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
    return chosen[0] + ' only' if len(chosen) == 1 else ' and '.join(chosen) + ' only'

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

def sample(rng,template):
    pattern=rng.choice(('UIN','NIU') if template=='summary-spaced' else DOMAIN['patterns'])
    eqs=[]
    nonzero=[v for v in range(-9,10) if v]
    for k in pattern:
        a=rng.choice(nonzero);b=rng.randint(-9,9)
        if k=='U' and template=='detailed-unit':
            a=rng.choice([v for v in nonzero if v-1 in nonzero]);c=a-1
        else:
            c=a if k!='U' else rng.choice([v for v in nonzero if v!=a and (template!='detailed-scaled' or a-v!=1)])
        d=b if k=='I' else rng.choice([v for v in range(-9,10) if v!=b])
        eqs.append([a,b,c,d])
    return {'variable':rng.choice('xuyzwv'),'equations':eqs}

# EASY: direct cancellation of affine terms; no authored increase in demand.
def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+str(level))
    template=template or 'detailed-scaled'
    if template not in ('detailed-scaled','detailed-unit','summary-spaced'): raise ValueError('Unsupported template')
    if profile not in (None,'boolean-per-equation'): raise ValueError('Unsupported bank profile')
    rng=random.Random(seed)
    p=globals()['parameters'](parameters if parameters is not None else sample(rng,template))
    if template!='summary-spaced' and any((e[0]-e[2]==1)!=(template=='detailed-unit') for e in p['equations'] if kind(e)=='U'):
        raise ValueError('Parameter/solution sequence mismatch')
    if template=='summary-spaced' and ''.join(kind(e) for e in p['equations']) not in ('UIN','NIU'):
        raise ValueError('Summary requires exactly one contradiction and one identity')
    prompt='Which of the following equations has no solutions?\n\nSelect all that apply.\n\n'+'\n'.join('- **'+key+'.** $'+equation(e,p['variable'],template=='summary-spaced')+'$' for key,e in zip(KEYS,p['equations']))
    solution=worked(p,template)
    task=fingerprint(p)
    content=digest({'problem':prompt,'solution':solution,'bank':'boolean-per-equation'})
    qid=uid('question:'+content)
    fields=[]
    for key,e in zip(KEYS,p['equations']):
        fid=uid(qid+':field:'+key)
        answers=[{':answer/id':uid(fid+':answer:'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[kind(e)=='N'][':answer/id']]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
            'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':'boolean-per-equation','parameter_fingerprint':task,'content_fingerprint':content,'domain':DOMAIN,'plot_rating':'none','source_analysis':{'basis':1842,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','reference':'generate/scratch/17592186204089/source-cases.json'},'sampling_extension':'Signed coefficients on either side; observed simple integer affine task only'}}

def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)

def batch(level,count=5,seed=0):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+str(level))
    if type(count) is not int or not 0<=count<=1000: raise ValueError('Bounded batch count 0..1000 required')
    result=[];seen=set()
    for offset in range(max(100,100*count)):
        if len(result)==count: return result
        rec=generate(level,seed+offset)
        fp=rec['generation']['parameter_fingerprint']
        if fp not in seen: result.append(rec);seen.add(fp)
    raise ValueError('Distinct variant limit reached; no duplicate padding')

def markdown(rec):
    return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',required=True)
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json','markdown'),default='json')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    output=batch(args.difficulty,args.count,args.seed)
    value=(json.dumps(output,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in output))+'\n'
    if args.output: args.output.write_text(value)
    else: print(value,end='')

if __name__=='__main__': main()
