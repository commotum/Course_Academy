#!/usr/bin/env python3
"""Three independent checkbox classifications of affine real equations.

All bands retain the observed affine-cancellation demand. No variable names, seeds, field
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
VERSION = '2.0.0-draft'
SUPPORTED_LEVELS = ('easy','moderate','hard')
TEMPLATES = ('detailed-scaled','detailed-unit','summary-spaced','radio-detailed-scaled')
CATALOG_SIZE_PER_TEMPLATE = 64
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
HERE = Path(__file__).resolve().with_suffix('')
KEYS = ('I', 'II', 'III')
DOMAIN = {'variable': 'x,u,y,z,w,v', 'coefficients': [-9, 9], 'constants': [-9, 9],
          'equations': 3, 'domain': 'real numbers', 'patterns': ['UIN', 'NIU', 'NNU', 'UNI', 'NUI', 'INU', 'IUN'],
          'sampling_policy': 'Observed integer affine forms; all coefficient signs permitted; one or two contradictions; at least one unique solution. No distribution or fractions in equation inputs.'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def parameters(p):
    if set(p) not in ({'variable', 'equations'},{'variable', 'equations','label_permutation'}) or p['variable'] not in 'xuyzwv' or len(p['variable']) != 1:
        raise ValueError('Invalid variable/parameter keys')
    eqs = p['equations']
    if not isinstance(eqs, list) or len(eqs) != 3 or any(not isinstance(e, list) or len(e) != 4 for e in eqs):
        raise ValueError('Three [left coefficient, left constant, right coefficient, right constant] rows required')
    if any(type(v) is not int or abs(v) > 9 for e in eqs for v in e) or any(e[0] == 0 or e[2] == 0 for e in eqs):
        raise ValueError('Nonzero integer coefficients and bounded integer constants required')
    if ''.join(kind(e) for e in eqs) not in DOMAIN['patterns']:
        raise ValueError('Unobserved classification pattern')
    result={'variable': p['variable'], 'equations': [e[:] for e in eqs]}
    if 'label_permutation' in p:
        order=p['label_permutation']
        if not isinstance(order,list) or len(order)!=3 or any(type(i) is not int for i in order) or sorted(order)!=[0,1,2]:raise ValueError('Invalid Roman-label permutation')
        if ''.join(kind(e) for e in eqs)!=''.join('NUI'[i] for i in order):raise ValueError('Permutation must preserve the source N/U/I roles')
        result['label_permutation']=order[:]
    return result

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
    pattern='NUI' if template=='radio-detailed-scaled' else rng.choice(('UIN','NIU') if template=='summary-spaced' else ('UIN','NIU','NNU','UNI'))
    eqs=[]
    nonzero=[v for v in range(-9,10) if v]
    for k in pattern:
        a=rng.choice(nonzero);b=rng.randint(-9,9)
        if k=='U' and template=='detailed-unit':
            a=rng.choice([v for v in nonzero if v-1 in nonzero]);c=a-1
        else:
            c=a if k!='U' else rng.choice([v for v in nonzero if v!=a and (template not in ('detailed-scaled','radio-detailed-scaled') or a-v!=1)])
        d=b if k=='I' else rng.randint(-9,9) if k=='U' else rng.choice([v for v in range(-9,10) if v!=b])
        eqs.append([a,b,c,d])
    return {'variable':rng.choice('xuyzwv'),'equations':eqs}

# One mathematical backbone in every band. Sparse labels never add a new skill.
FROZEN_DEPENDENCIES = {'source.json': 'e78a579d319b28f89eab504094ebc10274b9783ff6a7ebd9e5b0b32ac3ff937a', 'math_format.py': '723744b896f1ff5290bce3ac7e70a15eb60e810df118686164f87bd412295291'}
for _name,_expected in FROZEN_DEPENDENCIES.items():
    if hashlib.sha256((HERE/_name).read_bytes()).hexdigest()!=_expected:raise ValueError('Frozen private dependency changed: '+_name)
SOURCE = json.loads((HERE/'source.json').read_text())
ORIGINALS = {q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
RADIO_BANK = ('I only','I and III only','I and II only','I, II, and III','II and III only')
RADIO_SOURCE_SUBSETS=((0,),(0,2),(0,1),(0,1,2),(1,2))
RADIO_PERMUTATIONS=((0,1,2),(1,0,2),(1,2,0),(0,2,1),(2,0,1),(2,1,0))
def subset_text(indices):
    names=[KEYS[i] for i in sorted(indices)]
    return names[0]+' only' if len(names)==1 else ' and '.join(names)+' only' if len(names)==2 else 'I, II, and III'
def radio_bank(order):
    return tuple(subset_text(i for i,old_index in enumerate(order) if old_index in source_subset) for source_subset in RADIO_SOURCE_SUBSETS)

def source_parameters(question):
    import re
    expressions=re.findall(r'\$([^$]*=[^$]*)\$',question[':question/problem'])
    variable=re.search('[xuyzwv]',expressions[0])[0];x=sp.Symbol(variable)
    rows=[]
    for expression in expressions:
        row=[]
        for text in expression.split('='):
            value=sp.sympify(re.sub(r'(\d)([xuyzwv])',r'\1*\2',text),locals={variable:x})
            row.extend((int(value.coeff(x)),int(value.subs(x,0))))
        rows.append(row)
    return {'variable':variable,'equations':rows}

def original_template(mid):
    return 'radio-detailed-scaled' if mid=='q-288069' else 'summary-spaced' if mid in ('q-287964','q-288058') else 'detailed-unit' if mid=='q-288073' else 'detailed-scaled'

SOURCE_CASES = [{'source_id':mid,'parameters':dict(source_parameters(q),**({'label_permutation':[0,1,2]} if mid=='q-288069' else {})),'template':original_template(mid),'level':'easy','bank_profile':'subset-five' if mid=='q-288069' else 'boolean-per-equation'} for mid,q in ORIGINALS.items()]
CATALOG={};excluded={fingerprint(c['parameters']) for c in SOURCE_CASES}
excluded.add(fingerprint(source_parameters(SOURCE['record'][':knowledge-point/canonical-example'])))
for band_index,band in enumerate(SUPPORTED_LEVELS):
    CATALOG[band]={}
    for template_index,template in enumerate(TEMPLATES):
        rows=[];offset=0
        while len(rows)<CATALOG_SIZE_PER_TEMPLATE:
            index=offset//len(RADIO_PERMUTATIONS) if template=='radio-detailed-scaled' else offset
            candidate=sample(random.Random(100000*band_index+10000*template_index+index),template)
            if template=='radio-detailed-scaled':
                order=RADIO_PERMUTATIONS[offset%len(RADIO_PERMUTATIONS)]
                candidate['equations']=[candidate['equations'][i] for i in order]
                candidate['label_permutation']=list(order)
            candidate=parameters(candidate);offset+=1
            fp=fingerprint(candidate)
            if fp not in excluded: rows.append(candidate);excluded.add(fp)
        CATALOG[band][template]=rows
DOMAIN.update({'public_domain':'finite catalog: 64 exact parameter records per template per band, plus eight original replay parameter records on easy', 'catalog_size_per_band':256,'radio_label_permutation_slot':'new label position maps to original N/U/I row; all six permutations transform the complete five-choice source bank together','level_policy':'same backbone, same coefficient/constant bounds and workload; moderate/hard are conservative sparse-band assignments, not observed difficulty evidence','exclusions':'all source and canonical mathematical fingerprints; no cross-band duplicate tasks; variable-only and common-scaling changes do not count'})

# Freeze formatting privately. The generator never imports mutable root QA helpers.
import importlib.util
_format_path=HERE/'math_format.py'
_format_spec=importlib.util.spec_from_file_location('kp_private_math_format',_format_path)
_format=importlib.util.module_from_spec(_format_spec);_format_spec.loader.exec_module(_format)

@_format.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
    if type(seed) is not int:raise ValueError('Integer seed required')
    template=template or TEMPLATES[seed%len(TEMPLATES)]
    if template not in TEMPLATES:raise ValueError('Unsupported template')
    bank='subset-five' if template=='radio-detailed-scaled' else 'boolean-per-equation'
    if profile not in (None,bank):raise ValueError('Unsupported bank profile')
    allowed=CATALOG[level][template]+([c['parameters'] for c in SOURCE_CASES if c['template']==template] if level=='easy' else [])
    p=globals()['parameters'](parameters if parameters is not None else CATALOG[level][template][(seed//len(TEMPLATES))%CATALOG_SIZE_PER_TEMPLATE])
    if p not in allowed:raise ValueError('Parameters outside frozen finite public domain')
    if template not in ('summary-spaced',) and any((e[0]-e[2]==1)!=(template=='detailed-unit') for e in p['equations'] if kind(e)=='U'):raise ValueError('Parameter/solution sequence mismatch')
    if template=='summary-spaced' and ''.join(kind(e) for e in p['equations']) not in ('UIN','NIU'):raise ValueError('Summary requires one contradiction and one identity')
    if template=='radio-detailed-scaled' and 'label_permutation' not in p:raise ValueError('Radio requires its whole-bank label permutation')
    if template!='radio-detailed-scaled' and 'label_permutation' in p:raise ValueError('Label permutation only belongs to radio')
    radio=template=='radio-detailed-scaled'
    prompt='Which of the following equations has no solutions?\n\n'+('\n\n'.join(key+'. $'+equation(e,p['variable'])+'$' for key,e in zip(KEYS,p['equations'])) if radio else 'Select all that apply.\n\n'+'\n'.join('- **'+key+'.** $'+equation(e,p['variable'],template=='summary-spaced')+'$' for key,e in zip(KEYS,p['equations'])))
    solution=worked(p,'detailed-scaled' if radio else template)
    if template=='summary-spaced':
        reduced=['$'+p['variable']+'='+sp.latex(sp.Rational(d-b,a-c))+'$' if a!=c else 'an identity' if b==d else '$'+str(b)+'='+str(d)+'$' for a,b,c,d in p['equations']]
        ordinal=('first','second','third')[next(i for i,e in enumerate(p['equations']) if kind(e)=='N')]
        solution='The equations reduce respectively to '+', '.join(reduced[:2])+', and '+reduced[2]+'. Only the '+ordinal+' has no solutions.'
    prompt=_format.normalize_prose(prompt);solution=_format.normalize_prose(solution)
    values=radio_bank(p['label_permutation']) if radio else ('false','true')
    task=fingerprint(p);content=digest({'problem':prompt,'solution':solution,'bank':values if radio else bank,'difficulty':level});qid=uid('question:'+content)
    fields=[]
    for key,e in ([('selection',None)] if radio else zip(KEYS,p['equations'])):
        fid=uid(qid+':field:'+key)
        answers=[{':answer/id':uid(fid+':answer:'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
        correct=selection(p['equations']) if radio else 'true' if kind(e)=='N' else 'false'
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if radio else 'checkbox'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':bank,'parameter_fingerprint':task,'content_fingerprint':content,'domain':DOMAIN,'plot_rating':'none','source_analysis':{'basis':2275,'lineage':SOURCE['lineage'],'reference':str(HERE/'source.json')},'sampling_extension':'Conservative same-method finite catalogs for all three labels'}}

def replay_source(source_id):
    import copy
    if source_id not in ORIGINALS:raise ValueError('Unknown source ID')
    return copy.deepcopy(ORIGINALS[source_id])

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count=5,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
    if type(count) is not int or not 0<=count<=256:raise ValueError('Finite band capacity is 256; duplicate padding forbidden')
    return [generate(level,seed+i) for i in range(count)]
def markdown(rec):return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True,choices=(*SUPPORTED_LEVELS,'all'));parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=('json','markdown'),default='json');parser.add_argument('--output',type=Path)
    args=parser.parse_args();records=[r for level in (SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)) for r in batch(level,args.count,args.seed)]
    value=(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))+'\n'
    if args.output:args.output.write_text(value)
    else:print(value,end='')
if __name__=='__main__':main()
