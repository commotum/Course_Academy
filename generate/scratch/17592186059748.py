#!/usr/bin/env python3
"""Integer 2x2 determinants, source basis 1356; no database operations.

All nine practice sources have parameterized replay. Eight source solutions are
byte-exact at their parameters. q-11648 lacks a rating, correct designation and
solution: moderate and its solution/correct value are explicitly authored.
Observed scalar banks do not identify their mistakes. Their replay profiles
support common integral matrix scaling only: all scalar options scale by t².
That is a numerical covariance recipe, NOT a recovered error model. Normal
radio generation uses a separate complete bank of four defensible operations.

Easy: |entry|<=9, at most one negative/zero, at least one product magnitude>=2.
Moderate: nonzero signed entries |entry|<=10, at least one negative and one
product magnitude>=10, matching the observed multiplication workload.
Hard (authored): integer entries 6<=|entry|<=15, two or three negatives,
both diagonal products magnitude>=50, at least one entry magnitude>=11.
Hard still evaluates exactly ad-bc, with the same four teaching stages; no
unknown entry, noninteger matrix, system solving, inverse, geometry or 3x3 work.
Observed replay domains permit integral common scaling up to |entry|=40 and are
separate from authored workload bounds. Explicit inputs are never resampled.

The full prompt, solution and unordered complete bank define content identity;
the mathematical fingerprint is the ordered integer matrix alone. Matrix names,
layouts, levels, profiles and option order do not inflate task counts.
Evidence and independent/native checks live in the same-named directory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp

KP_ID = 17592186059748
KP_UUID = '2129aee3-923d-57de-8bdc-983ffdf787f1'
TITLE = 'Calculating the Determinant of a 2x2 Matrix With Integer Entries'
VERSION = 'integer-determinant-v1'
PROVENANCE = {'database': 'math', 'basis': 1356, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES = {
    'named_dot': {'levels': ['easy','moderate','hard'], 'field_type': 'radio', 'sources': ['q-1079']},
    'named_dot_indented': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-1080']},
    'named_dot_swapped': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-11646']},
    'bare_dot': {'levels': ['moderate','hard'], 'field_type': 'radio', 'sources': ['q-127578','q-127580']},
    'vmatrix_dot': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-11648']},
    'named_parentheses_blank': {'levels': ['easy','moderate','hard'], 'field_type': 'blank', 'sources': ['q-317335','q-317336','q-317342']},
}
# Evidence scalars are coefficients in an observed covariance model, never
# arbitrary offsets or a literal-source-output branch. Correctness is computed.
OBSERVED = {
 'q-1079': {'level':'easy','template':'named_dot','matrix':[1,2,3,0],'name':'A','coefficients':['1','0','-1/6','1/6','-1']},
 'q-11648': {'level':'moderate','template':'vmatrix_dot','matrix':[2,-4,-2,7],'name':'A','coefficients':['1','1/6','-2/3','-1','2/3']},
 'q-1080': {'level':'moderate','template':'named_dot_indented','matrix':[10,-3,1,4],'name':'X','coefficients':['11/43','-34/43','1','17/43','37/43']},
 'q-11646': {'level':'moderate','template':'named_dot_swapped','matrix':[4,5,-2,3],'name':'L','coefficients':['6/11','-1','-6/11','1','0']},
 'q-127578': {'level':'moderate','template':'bare_dot','matrix':[5,-9,-3,7],'name':'A','coefficients':['1','-9/8','35/8','-5/2','31/4']},
 'q-127580': {'level':'moderate','template':'bare_dot','matrix':[-1,-10,-2,5],'name':'A','coefficients':['-2','1','3/5','-4/5','-1/5']},
 'q-317335': {'level':'easy','template':'named_parentheses_blank','matrix':[8,-5,3,4],'name':'R','coefficients':['1']},
 'q-317336': {'level':'easy','template':'named_parentheses_blank','matrix':[2,4,1,3],'name':'S','coefficients':['1']},
 'q-317342': {'level':'easy','template':'named_parentheses_blank','matrix':[6,-2,5,7],'name':'S','coefficients':['1']},
}
OPENING = 'For a $2\\times 2$ matrix, the determinant is given by the formula\n\n$$\n|\\begin{aligned}a & b \\\\ c & d\\end{aligned}|=ad-bc.\n$$\n\n'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def mat(p, env='aligned'):
    a,b,c,d=(p[k] for k in 'abcd')
    return rf'\begin{{{env}}}{a} & {b} \\ {c} & {d}\end{{{env}}}'
def factor(n):
    return f'({n})' if n<0 else str(n)
def validate_parameters(p,level,profile):
    if set(p)!=set('abcd')|{'name'}: raise ValueError('Parameters must be exactly a,b,c,d,name')
    v=[p[k] for k in 'abcd']
    if any(type(n) is not int for n in v): raise ValueError('Entries must be integers')
    if p['name'] not in ['A','X','L','R','S','B','M','N']: raise ValueError('Unsupported matrix name')
    if profile in OBSERVED:
        original=OBSERVED[profile]['matrix']
        scales=[sp.Rational(n,b) for n,b in zip(v,original) if b]
        t=scales[0]
        if not t.is_Integer or t==0 or any(n!=t*b for n,b in zip(v,original)) or max(map(abs,v))>40:
            raise ValueError('Observed covariance profile requires nonzero common integer scaling with |entry|<=40')
        return
    if level=='easy':
        valid=max(map(abs,v))<=9 and sum(n<0 for n in v)<=1 and sum(n==0 for n in v)<=1 and max(abs(v[0]*v[3]),abs(v[1]*v[2]))>=2
    elif level=='moderate':
        valid=all(n!=0 and abs(n)<=10 for n in v) and any(n<0 for n in v) and max(abs(v[0]*v[3]),abs(v[1]*v[2]))>=10
    else:
        valid=all(6<=abs(n)<=15 for n in v) and 2<=sum(n<0 for n in v)<=3 and max(map(abs,v))>=11 and min(abs(v[0]*v[3]),abs(v[1]*v[2]))>=50
    if not valid: raise ValueError('Parameters outside authored '+level+' workload bounds')

def sample(level,rng,profile):
    if profile in OBSERVED:
        ob=OBSERVED[profile];maxscale=40//max(map(abs,ob['matrix']))
        t=rng.choice([i for i in range(-maxscale,maxscale+1) if i])
        return dict(zip('abcd',[t*n for n in ob['matrix']]))|{'name':ob['name']}
    bound={'easy':9,'moderate':10,'hard':15}[level]
    return dict(zip('abcd',[rng.randint(-bound,bound) for _ in range(4)]))|{'name':rng.choice(['A','X','L','R','S','B','M','N'])}

def prose(p,template):
    a,b,c,d=(p[k] for k in 'abcd');n=p['name'];m=mat(p);det=a*d-b*c
    bare=template=='bare_dot';vmatrix=template=='vmatrix_dot';blank=template=='named_parentheses_blank'
    if blank:
        prompt=f'Calculate $det({n})$ given that\n${n}=[{m}].$\n\n$det({n})=$\n{{{{field-1}}}}'
    elif bare: prompt=f'$|{m}|=$'
    elif vmatrix: prompt=f'What is ${mat(p,"vmatrix")}$?'
    else:
        indent='    ' if template in ['named_dot_indented','named_dot_swapped'] else ''
        prompt=f'Calculate $\\text{{det}}({n})$, if\n{indent}${n}=[{m}].$'
    if blank:
        substitution=f'({a})({d})-({b})({c})'
        products=f'{a*d}+{abs(b*c)}' if b*c<0 else f'{a*d}-{b*c}'
        first=f'det({n}) & =|{m}|'
        rows=[first,' & ='+substitution,' & ='+products,' & ='+str(det)+'.']
        transition='Using the formula, we have'
    else:
        # Sources keep a as an initial signed factor and group other negatives.
        bc=[c,b] if template=='named_dot_swapped' else [b,c]
        substitution=f'{a}\\cdot {factor(d)}-{factor(bc[0])}\\cdot {factor(bc[1])}'
        products=f'{a*d}-{factor(b*c)}'
        if bare or vmatrix:
            first=f'|{m}| & ='+substitution
            rows=[first,' & ='+products,' & ='+str(det)]
        else:
            first=f'\\text{{det}}({n}) & =|{m}|'
            rows=[first,' & ='+substitution,' & ='+products,' & ='+str(det)]
        transition='Using the formula, we have:'
    solution=OPENING+transition+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
    return prompt,solution

def choices(p,profile,field_type):
    a,b,c,d=(p[k] for k in 'abcd');det=int(sp.Matrix([[a,b],[c,d]]).det())
    if profile in OBSERVED:
        values=[sp.Rational(k)*det for k in OBSERVED[profile]['coefficients']]
        recipes=['observed determinant coefficient '+k+'; intent unresolved' for k in OBSERVED[profile]['coefficients']]
    elif field_type=='blank': values=[det];recipes=['ad-bc']
    else:
        values=[det,a*d+b*c,b*c-a*d,a*d,a*b-c*d]
        recipes=['ad-bc','ad+bc','bc-ad','ad (omit off-diagonal product)','ab-cd (row products)']
    if any(not sp.Rational(v).is_Integer for v in values) or len(set(values))!=len(values):
        raise ValueError('Reject complete ambiguous/noninteger bank')
    return det,[str(v) for v in values],recipes

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']: raise ValueError('Unknown difficulty')
    if profile is not None and profile not in OBSERVED and profile!='authored_operations': raise ValueError('Unknown profile')
    if profile in OBSERVED:
        ob=OBSERVED[profile]
        if level!=ob['level'] or template not in [None,ob['template']]:raise ValueError('Observed profile level/template mismatch')
        template=ob['template']
    rng=random.Random(seed)
    eligible=[t for t,x in TEMPLATES.items() if level in x['levels'] and (field_type is None or field_type==x['field_type'])]
    if not eligible: raise ValueError('Unsupported field type')
    template=template or rng.choice(eligible)
    if template not in eligible: raise ValueError('Unsupported template/level/field layout')
    field_type=TEMPLATES[template]['field_type'];profile=profile or 'authored_operations'
    for attempt in range(20000):
        p=dict(parameters) if parameters is not None else sample(level,rng,profile)
        try:
            validate_parameters(p,level,profile);det,values,recipes=choices(p,profile,field_type)
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else: raise ValueError('No eligible complete instance')
    prompt,solution=prose(p,template)
    task_hash=digest([p[k] for k in 'abcd'])
    content_hash=digest([VERSION,prompt,solution,field_type,sorted(values)])
    qid=ident(content_hash);fid=ident(qid+'field');key='field-1' if field_type=='blank' else 'selection'
    bank=[{':answer/id':ident(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=next(x[':answer/id'] for x in bank if x[':answer/value']==str(det))
    rng.shuffle(bank)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':bank,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':profile,'provenance':PROVENANCE,'mathematical_fingerprint':task_hash,'content_fingerprint':content_hash,'recipes':dict(zip(values,recipes)),'source_ids':TEMPLATES[template]['sources'],'bank_authorship':'observed scalar covariance; error intent unresolved' if profile in OBSERVED else 'authored complete determinant operations','difficulty_authorship':'authored missing hard' if level=='hard' else 'authored moderate assignment' if profile=='q-11648' else 'observed-supported level','domain':'integer 2x2 matrix; direct ad-bc only','plot_rating':'none','sympy_version':sp.__version__}}

# Easy: preserve the four observed source presentations; small integer products.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: signed multiplication/subtraction at the observed integer scale.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored increased integer arithmetic in the SAME direct ad-bc skill.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    bank='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    return q[':question/problem']+'\n\n'+bank+'\n\n'+q[':question/worked-solution']
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    if args.count<1:ap.error('--count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
