#!/usr/bin/env python3
"""Seeded integer 2x2 determinant questions; see instructional-account.md.
Inherited templates repaired for basis 4643, cancellation and portable execution.
Observed profiles are exact evidence replay only; authored banks sample by case.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from math_format import normalize_prose, normalize_tex, checked_math_content, matrix_tex
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
VERSION='integer-determinant-v5-format-audit-9122-v1'
PROVENANCE = {'database': 'math', 'basis': 4643, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES = {
    'named_dot': {'levels': ['easy','moderate'], 'field_type': 'radio', 'sources': ['q-1079']},
    'named_dot_indented': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-1080']},
    'named_dot_swapped': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-11646']},
    'bare_dot': {'levels': ['easy','moderate'], 'field_type': 'radio', 'sources': ['q-1071','q-127578','q-127580']},
    'vmatrix_dot': {'levels': ['moderate'], 'field_type': 'radio', 'sources': ['q-11648']},
    'evaluate_blank': {'levels': ['easy','moderate'], 'field_type': 'blank', 'sources': ['q-317341']},
    'named_parentheses_blank': {'levels': ['easy','moderate'], 'field_type': 'blank', 'sources': ['q-317335','q-317336','q-317342']},
}
# Source cases are immutable replay evidence, not normal-generation templates.
SOURCE_CASES = json.loads(Path(__file__).with_name('source-cases.json').read_text())
OBSERVED = {
 'q-1079': {'level':'easy','template':'named_dot','matrix':[1,2,3,0],'name':'A'},
 'q-11648': {'level':'moderate','template':'vmatrix_dot','matrix':[2,-4,-2,7],'name':'A'},
 'q-1080': {'level':'moderate','template':'named_dot_indented','matrix':[10,-3,1,4],'name':'X'},
 'q-11646': {'level':'moderate','template':'named_dot_swapped','matrix':[4,5,-2,3],'name':'L'},
 'q-127578': {'level':'moderate','template':'bare_dot','matrix':[5,-9,-3,7],'name':'A'},
 'q-127580': {'level':'moderate','template':'bare_dot','matrix':[-1,-10,-2,5],'name':'A'},
 'q-317335': {'level':'easy','template':'named_parentheses_blank','matrix':[8,-5,3,4],'name':'R'},
 'q-317336': {'level':'easy','template':'named_parentheses_blank','matrix':[2,4,1,3],'name':'S'},
 'q-317342': {'level':'easy','template':'named_parentheses_blank','matrix':[6,-2,5,7],'name':'S'},
 'q-317341': {'level':'easy','template':'evaluate_blank','matrix':[7,2,5,4],'name':'A'},
 'q-1071': {'level':'easy','template':'bare_dot','matrix':[6,3,2,1],'name':'A'},
}
BANKS = {'authored_exchangeable_values': 'five band-compatible determinants; displayed matrix chosen independently'}
def sign(n): return (n>0)-(n<0)
def decision_case(p, level):
    a,b,c,d=(p[k] for k in 'abcd'); det=a*d-b*c
    if level=='easy':
        zeros=''.join(k for k in 'abcd' if p[k]==0) or 'none'
        return f'{sign(det)}:zero={zeros}'
    return f'{sign(det)}:products={sign(a*d)},{sign(b*c)}'
def decisions(level):
    if level=='easy':
        return [f'{s}:zero=none' for s in [-1,0,1]]+[f'{s}:zero={k}' for k in 'abcd' for s in [-1,1]]
    return [f'{s}:products={x},{y}' for x,y in [(1,1),(-1,-1),(1,-1),(-1,1)]
            for s in [-1,0,1] if (x==y or s==x)]
def compatible_profiles(case, field_type):
    return ['blank'] if field_type=='blank' else list(BANKS)
OPENING = 'For a $2\\times 2$ matrix, the determinant is given by the formula\n\n$$\n|\\begin{aligned}a & b \\\\ c & d\\end{aligned}|=ad-bc.\n$$\n\n'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def mat(p, env='aligned'):
    a,b,c,d=(p[k] for k in 'abcd')
    if env=='bmatrix':return matrix_tex([[a,b],[c,d]],augmented=False)
    return rf'\begin{{{env}}}{a} & {b} \\ {c} & {d}\end{{{env}}}'
def factor(n):
    return f'({n})' if n<0 else str(n)
def validate_parameters(p,level,profile):
    if set(p)!=set('abcd')|{'name'}: raise ValueError('Parameters must be exactly a,b,c,d,name')
    v=[p[k] for k in 'abcd']
    if any(type(n) is not int for n in v): raise ValueError('Entries must be integers')
    if p['name'] not in ['A','X','L','R','S','B','M','N']: raise ValueError('Unsupported matrix name')
    if profile in OBSERVED:
        if v!=OBSERVED[profile]['matrix']: raise ValueError('Replay profile requires original matrix')
        return
    if level=='easy':
        valid=max(map(abs,v))<=9 and sum(n<0 for n in v)<=1 and sum(n==0 for n in v)<=1 and max(abs(v[0]*v[3]),abs(v[1]*v[2]))>=2
    elif level=='moderate':
        valid=all(n!=0 and abs(n)<=10 for n in v) and any(n<0 for n in v) and max(abs(v[0]*v[3]),abs(v[1]*v[2]))>=10
    else: raise ValueError('Unsupported difficulty')
    if not valid: raise ValueError('Parameters outside authored '+level+' workload bounds')

def sample(level,rng,profile,decision):
    if profile in OBSERVED:
        ob=OBSERVED[profile]
        return dict(zip('abcd',ob['matrix']))|{'name':ob['name']}
    bound={'easy':9,'moderate':10}[level]
    v=[rng.randint(1,bound) for _ in range(4)]
    if level=='easy':
        zero=decision.split('=')[1]
        if zero!='none': v['abcd'.index(zero)]=0
        neg=rng.choice([None]+[i for i in range(4) if v[i]])
        if decision.startswith('0:'): neg=None
        if neg is not None:v[neg]*=-1
    else:
        import itertools
        sx,sy=map(int,decision.split('=')[1].split(','))
        patterns=[s for s in itertools.product([-1,1],repeat=4)
                  if s[0]*s[3]==sx and s[1]*s[2]==sy and -1 in s]
        v=[x*s for x,s in zip(v,rng.choice(patterns))]
    if decision.startswith('0:') and v[0] and (v[1]*v[2])%v[0]==0:
        v[3]=(v[1]*v[2])//v[0]
    return dict(zip('abcd',v))|{'name':rng.choice(['A','X','L','R','S','B','M','N'])}

def valid_candidate(level,rng,decision=None):
    # Each candidate chooses its mathematical case before any integer entries.
    case=decision or rng.choice(decisions(level))
    for attempt in range(20000):
        p=sample(level,rng,'authored_exchangeable_values',case)
        try:validate_parameters(p,level,'authored_exchangeable_values')
        except ValueError:continue
        if decision_case(p,level)==case:return p,attempt+1
    raise ValueError('No matrix for candidate case')

def exchangeable_bank(level,rng,decision=None,parameters=None):
    # In ordinary CLI sampling all five candidates are identically distributed.
    # Uniqueness rejection precedes the independent choice of displayed matrix.
    attempts=0
    for rejected in range(20000):
        candidates=[]
        for i in range(5):
            if i==0 and parameters is not None:
                p=dict(parameters)
                validate_parameters(p,level,'authored_exchangeable_values')
                if decision is not None and decision_case(p,level)!=decision:
                    raise ValueError('Wrong decision case')
                n=1
            else:p,n=valid_candidate(level,rng,decision if i==0 else None)
            candidates.append(p);attempts+=n
        values=[p['a']*p['d']-p['b']*p['c'] for p in candidates]
        if len(set(values))!=5:continue
        selected=0 if decision is not None or parameters is not None else rng.randrange(5)
        return candidates[selected],values,candidates,selected,attempts,rejected
    raise ValueError('No distinct complete candidate bank')

def prose(p,template):
    a,b,c,d=(p[k] for k in 'abcd');n=p['name'];m=mat(p);det=a*d-b*c
    bare=template=='bare_dot';vmatrix=template=='vmatrix_dot';blank=template=='named_parentheses_blank';evaluate=template=='evaluate_blank'
    if evaluate:
        prompt=f'Evaluate the determinant:\n\n${mat(p,"vmatrix")}=$\n{{{{field-1}}}}'
    elif blank:
        prompt=f'Calculate $det({n})$ given that\n${n}={mat(p, 'bmatrix')}.$\n\n$det({n})=$\n{{{{field-1}}}}'
    elif bare: prompt=f'$|{m}|=$'
    elif vmatrix: prompt=f'What is ${mat(p,"vmatrix")}$?'
    else:
        indent='    ' if template in ['named_dot_indented','named_dot_swapped'] else ''
        prompt=f'Calculate $\\text{{det}}({n})$, if\n{indent}${n}={mat(p, 'bmatrix')}.$'
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
        if bare or vmatrix or evaluate:
            first=f'|{m}| & ='+substitution
            rows=[first,' & ='+products,' & ='+str(det)+('.' if evaluate else '')]
        else:
            first=f'\\text{{det}}({n}) & =|{m}|'
            rows=[first,' & ='+substitution,' & ='+products,' & ='+str(det)]
        transition='Using the formula, we have' + ('' if evaluate else ':')
    solution=OPENING+transition+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
    return prompt,solution

def choices(p,profile,field_type,errors=None):
    a,b,c,d=(p[k] for k in 'abcd');det=int(sp.Matrix([[a,b],[c,d]]).det())
    if profile in OBSERVED:
        src=next(q for q in SOURCE_CASES if q[':question/math-academy-id']==profile)
        values=[int(x[':answer/value']) for x in src[':question/answer-fields'][0][':answer-field/choices']]
        recipes=['observed value; intent unresolved']*len(values)
    elif field_type=='blank': values=[det];recipes=['ad-bc']
    else:
        if errors is None or len(errors)!=4 or len(set(errors))!=4 or any(type(e) is not int or e==0 for e in errors):
            raise ValueError('Exactly four distinct signed nonzero controlled errors required')
        values=[det]+[det+e for e in errors]
        recipes=['ad-bc']+[f'ad-bc+({e})' for e in errors]
    if any(not sp.Rational(v).is_Integer for v in values) or len(set(values))!=len(values):
        raise ValueError('Reject complete ambiguous/noninteger bank')
    return det,[str(v) for v in values],recipes

@checked_math_content
def _generate_complete(level,seed=0,template=None,field_type=None,parameters=None,profile=None,decision=None,errors=None):
    if type(seed) is not int: raise ValueError('seed must be an integer')
    if parameters is not None and not isinstance(parameters,dict): raise ValueError('parameters must be a dictionary')
    if level not in ['easy','moderate']: raise ValueError('Unknown difficulty')
    if profile is not None and profile not in OBSERVED and profile not in BANKS and profile!='blank': raise ValueError('Unknown profile')
    if profile in OBSERVED:
        ob=OBSERVED[profile]
        if level!=ob['level'] or template not in [None,ob['template']]:raise ValueError('Observed profile level/template mismatch')
        template=ob['template']
    rng=random.Random(seed)
    eligible=[t for t,x in TEMPLATES.items() if level in x['levels'] and (field_type is None or field_type==x['field_type'])]
    if not eligible: raise ValueError('Unsupported field type')
    template=template or rng.choice(eligible)
    if template not in eligible: raise ValueError('Unsupported template/level/field layout')
    field_type=TEMPLATES[template]['field_type']
    natural_bank=profile not in OBSERVED and field_type=='radio' and parameters is None and decision is None and errors is None
    if profile not in OBSERVED:
        if not natural_bank:
            decision=decision or (decision_case(parameters,level) if parameters is not None else rng.choice(decisions(level)))
            if decision not in decisions(level): raise ValueError('Unsupported decision case')
        eligible_profiles=compatible_profiles(decision,field_type)
        profile=profile or rng.choice(eligible_profiles)
        if profile not in eligible_profiles: raise ValueError('Incompatible bank/case/field')
    candidates=[];selected=None;bank_rejections=0
    if profile=='authored_exchangeable_values' and errors is None:
        p,raw_values,candidates,selected,attempts,bank_rejections=exchangeable_bank(level,rng,decision,parameters)
        det=int(sp.Matrix([[p['a'],p['b']],[p['c'],p['d']]]).det())
        values=list(map(str,raw_values))
        recipes=['ad-bc' if v==det else 'determinant of independent band-compatible candidate' for v in raw_values]
        attempt=attempts-1
    else:
        for attempt in range(20000):
            p=dict(parameters) if parameters is not None else sample(level,rng,profile,decision)
            try:
                validate_parameters(p,level,profile)
                if decision is not None and decision_case(p,level)!=decision: raise ValueError('Wrong decision case')
                det,values,recipes=choices(p,profile,field_type,errors)
            except ValueError:
                if parameters is not None:raise
                continue
            break
        else: raise ValueError('No eligible complete instance')
    prompt,solution=prose(p,template)
    task_hash=digest([p[k] for k in 'abcd'])
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    values=[normalize_tex(v) for v in values]
    content_hash=digest([VERSION,level,prompt,solution,field_type,sorted(values)])
    qid=ident(content_hash);fid=ident(qid+'field');key='field-1' if field_type=='blank' else 'selection'
    bank=[{':answer/id':ident(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=next(x[':answer/id'] for x in bank if x[':answer/value']==str(det))
    rng.shuffle(bank)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':bank,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'evidence_only':profile in OBSERVED,'eligible_for_learning':profile not in OBSERVED,'seed':seed,'template':template,'parameters':p,'profile':profile,'provenance':PROVENANCE,'mathematical_fingerprint':task_hash,'content_fingerprint':content_hash,'recipes':dict(zip(values,recipes)),'arithmetic_errors':errors,'bank_candidates':candidates,'bank_selected_index':selected,'bank_rejections':bank_rejections,'bank_mode':('production_exchangeable' if natural_bank else 'directed_candidate_bank' if candidates else 'controlled_errors' if errors is not None else 'source_or_blank'),'decision_case':decision_case(p,level),'sampling_attempts':attempt+1,'source_ids':TEMPLATES[template]['sources'],'bank_authorship':'observed exact bank replay; error intent unresolved' if profile in OBSERVED else 'authored exchangeable determinant values' if candidates else 'controlled-test arithmetic offsets' if errors else 'integer blank','difficulty_authorship':'authored moderate assignment' if profile=='q-11648' else 'observed-supported level','domain':'integer 2x2 matrix; direct ad-bc only','plot_rating':'none','sympy_version':sp.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,decision=None,errors=None):
    r=_generate_complete(level,seed,template,field_type,parameters,profile,decision,errors)
    if profile=='q-11648':
        q=r['question'];q.pop(':question/difficulty');q.pop(':question/worked-solution')
        f=q[':question/answer-fields'][0];f.pop(':answer-field/correct')
        h=digest([VERSION,q[':question/problem'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices'])])
        q[':question/id']=ident(h);f[':answer-field/id']=ident(q[':question/id']+'field')
        for a in f[':answer-field/choices']:a[':answer/id']=ident(f[':answer-field/id']+a[':answer/value'])
        r['generation']['content_fingerprint']=h
    return r

# Easy: preserve the four observed source presentations; small integer products.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: signed multiplication/subtraction at the observed integer scale.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    bank='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    return q[':question/problem']+'\n\n'+bank+'\n\n'+q.get(':question/worked-solution','[No captured worked solution.]')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=[args.difficulty]
    if args.count<1:ap.error('--count must be positive')
    records=[];seen=set()
    for level in levels:
        for i in range(args.count):
            for offset in range(20000):
                r=generate(level,args.seed+i+offset*max(1,args.count),args.template,profile=args.profile)
                fp=r['generation']['mathematical_fingerprint']
                if fp not in seen:break
            else:raise ValueError('Exhausted distinct mathematical tasks')
            seen.add(fp);records.append(r)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
