#!/usr/bin/env python3
"""Eliminating the second variable by ONE integer row transformation.

No system solving, substitution, two-row scaling, transactions, or engine edits.
Two observed unrated paired-select masks have no correct refs/worked solution.
Public raw-* profiles reproduce the source parameterized masks and all omissions;
they are evidence-only. Normal records have explicitly authored levels, independently
inferred correct refs, canonical-derived four-stage elimination solutions, and a
minimal integer-multiplier clarification. See adjacent extraction/validation evidence.

Profiles are complete operation banks, selected before parameters. `difference`
uses ±integer ratio and ±(ratio−1): comparing target coefficient magnitudes by
subtraction instead of their scaling ratio. `coefficient` uses ±ratio and ±the
unchanged target coefficient: copying the coefficient without dividing. No pool.
Raw historical source1 ±ratio ±first-row first-variable coefficient is OPAQUE;
raw source2 ±ratio ±unchanged target coefficient has a plausible operation mapping.
Both raw banks remain evidence-only, including explicit completed-* versions.

Difficulty is an authored workload claim: easy smaller target magnitude 1, ratio
2–7; moderate smaller magnitude2–4, ratio2–4; hard smaller magnitude2–4, ratio5–7.
These are variations of the same integer transformation, not new methods. Non-target
coefficients/constants −10..10 (nonzero), resulting products ≤70. Explicit inputs
obey the same guards. Whole banks and FULL row/multiplier combinations are checked.

Meaningful assessment tasks retain ordered target division operands, normalized
under genuine global common scaling of the whole displayed system. Other coefficients
and constants affect only that global scale normalization; variable names and banks
are excluded. The easy/nonunit division-operand workload remains distinct.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), and generate_easy/generate_moderate/generate_hard. CLI previews.
Use .venv/bin/python. Dependency versions in metadata include actual Python.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid
import sympy as sp

KP_ID = 17592186192655
KP_UUID = '3e7bfcbe-4913-53e0-98c7-171965adfe62'
TITLE = 'Eliminating the Second Variable'
VERSION = 'second-variable-one-transformation-v1'
HERE = Path(__file__).with_suffix('')
PROVENANCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES = ('compact','spaced')
VARIABLES = (('x','y'),('w','z'),('u','v'),('a','b'))
ANCHORS = {
 'q-210947': {'a1':9,'b1':10,'c1':3,'a2':-2,'b2':-1,'c2':3,'variables':['x','y']},
 'q-211000': {'a1':3,'b1':2,'c1':-1,'a2':7,'b2':10,'c2':3,'variables':['w','z']},
}
SOURCE_TEMPLATES = {'q-210947':'compact','q-211000':'spaced'}
BOUNDS = {'easy':((1,1),(2,7)), 'moderate':((2,4),(2,4)), 'hard':((2,4),(5,7))}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, VERSION+':'+value))


def tex(n):
    return sp.latex(sp.Rational(n))


def term(n,v):
    n = sp.Rational(n)
    if n == 0: return '0'
    return ('-' if n<0 else '') + ('' if abs(n)==1 else tex(abs(n))) + v


def linear(a,b,u,v):
    first = term(a,u)
    return first + (' - ' if b<0 else ' + ') + term(abs(b),v)


def equation(row,u,v,aligned=False):
    a,b,c = row
    return linear(a,b,u,v) + (' &= ' if aligned else ' = ') + tex(c)


def operation(p):
    # Choose the row whose target coefficient has smaller absolute magnitude.
    row = 0 if abs(p['b1']) < abs(p['b2']) else 1
    small = p['b1'] if row==0 else p['b2']
    large = p['b2'] if row==0 else p['b1']
    multiplier = -sp.Rational(large,small)
    return row, multiplier


def validate_parameters(p,level,raw=False):
    if set(p) != {'a1','b1','c1','a2','b2','c2','variables'}:
        raise ValueError('Exactly a1,b1,c1,a2,b2,c2,variables required')
    if tuple(p['variables']) not in VARIABLES:
        raise ValueError('Supported variable pairs: '+str(VARIABLES))
    for k in ('a1','b1','c1','a2','b2','c2'):
        if isinstance(p[k],bool) or not isinstance(p[k],int) or p[k]==0:
            raise ValueError('Coefficients/constants must be nonzero Python integers')
    if p['a1']*p['b2']==p['a2']*p['b1']:
        raise ValueError('Avoid degeneracy: elimination must retain the first variable')
    row,m = operation(p)
    if m.q!=1 or abs(m)<2:
        raise ValueError('Exactly one nontrivial integer scaling, magnitude ≥2')
    if raw:
        if max(abs(p[k]) for k in ('a1','b1','c1','a2','b2','c2'))>70:
            raise ValueError('Evidence-profile ceiling70')
    else:
        (lo,hi),(rlo,rhi) = BOUNDS[level]
        if not lo<=min(abs(p['b1']),abs(p['b2']))<=hi or not rlo<=abs(m)<=rhi:
            raise ValueError('Parameters outside authored '+level+' number-form workload')
        common=int(abs(sp.igcd(*(p[k] for k in ('a1','b1','c1','a2','b2','c2')))))
        if level!='easy' and min(abs(p['b1']),abs(p['b2']))//common<2:
            raise ValueError('Global common scaling cannot manufacture nonunit workload')
        if any(abs(p[k])>10 for k in ('a1','a2','c1','c2')):
            raise ValueError('Non-target coefficients/constants have magnitude≤10')
    return row,m


def full_valid_combinations(p,values,integer_only=True):
    good=[]
    for label,b,other in [('first',p['b1'],p['b2']),('second',p['b2'],p['b1'])]:
        for value in values:
            m=sp.Rational(value)
            if (not integer_only or m.q==1) and m*b+other==0:
                good.append((label,tex(m)))
    return good


def bank(p,profile):
    row,m=operation(p); r=abs(m)
    if profile=='difference': n=r-1
    elif profile=='coefficient': n=abs(p['b2'] if row==0 else p['b1'])
    elif profile in ('raw-q-210947','completed-q-210947'): n=abs(p['a1'])
    elif profile in ('raw-q-211000','completed-q-211000'): n=abs(p['b2'] if row==0 else p['b1'])
    else: raise ValueError('Unknown complete bank profile '+str(profile))
    values=[r,-r,-n,n] if profile.endswith('q-210947') else [n,-r,r,-n]
    if profile in ('difference','coefficient'): values=[m,-m,n,-n]
    if len(set(values))!=4:
        raise ValueError('Whole bank rejected: collision')
    combinations=full_valid_combinations(p,values,integer_only=False)
    if combinations!=[('first' if row==0 else 'second',tex(m))]:
        # Correct pair can appear elsewhere in sequence; compare sets.
        if set(combinations)!={('first' if row==0 else 'second',tex(m))}:
            raise ValueError('Whole bank rejected: ambiguous full row/multiplier combination')
    return values


def raw_system(p,template):
    u,v=p['variables']
    if template=='compact':
        if not (p['a1']>0 and p['b1']>0 and p['a2']<0 and p['b2']<0):
            raise ValueError('Compact raw mask has +,+ / −,− source sign domain')
        first=equation((p['a1'],p['b1'],p['c1']),u,v)
        second=equation((p['a2'],p['b2'],p['c2']),u,v)
        second='- '+second[1:]
    else:
        if not all(p[k]>0 for k in ('a1','b1','a2','b2')):
            raise ValueError('Spaced raw mask has positive source coefficient domain')
        first=equation((p['a1'],p['b1'],p['c1']),u,v).replace(' = -',' =-')
        second=equation((p['a2'],p['b2'],p['c2']),u,v)
    return '${'+first+'; '+second+'$'


def prompt(p,template,raw=False):
    u,v=p['variables']
    system=raw_system(p,template) if raw else (r'$\{'+equation((p['a1'],p['b1'],p['c1']),u,v)+'; '+equation((p['a2'],p['b2'],p['c2']),u,v)+'$')
    return ('Consider the following system of equations.\n'+ ('\n' if template=='spaced' else '') +system+'\nDescribe the steps needed to eliminate the variable $'+v+'$ from the system:'+
            ('' if raw else '\nUse an integer multiplier and leave the other equation unchanged.')+
            '\n\nTo eliminate $'+v+'$, multiply the\n{{field-1}}\nequation by\n{{field-2}},\nand add the equations.')


def sum_terms(first,second):
    return first + (' - '+second[1:] if second.startswith('-') else ' + '+second)


def solution(p):
    """Canonical stages: coefficient notice; marked row; four aligned rows; conclusion."""
    u,v=p['variables']; row,m=operation(p)
    name='first' if row==0 else 'second'; other='second' if row==0 else 'first'
    bs=p['b1'] if row==0 else p['b2']; bo=p['b2'] if row==0 else p['b1']
    originals=[(p['a1'],p['b1'],p['c1']),(p['a2'],p['b2'],p['c2'])]
    changed=list(originals); changed[row]=tuple(m*k for k in originals[row])
    marked=[equation(r,u,v) for r in originals];marked[row]='('+marked[row]+r')\cdot ('+tex(m)+')'
    a,b=changed
    grouped='('+sum_terms(term(a[0],u),term(b[0],u))+') &= ('+sum_terms(tex(a[2]),tex(b[2]))+')'
    final=term(a[0]+b[0],u)+' &= '+tex(a[2]+b[2])
    rows=[equation(a,u,v,True),equation(b,u,v,True),grouped,final]
    return ('Notice that the coefficient of $'+v+'$ in the first equation is $'+tex(p['b1'])+'$, while in the second equation it is $'+tex(p['b2'])+'$.\n\n'
      'If we multiply the '+name+' equation by ${\\color{blue}'+tex(m)+'}$, then the coefficient of $'+v+'$ will turn into $'+tex(m*bs)+'$, which will cancel with the coefficient of $'+tex(bo)+'$ in the '+other+' equation.\n\n'
      '$$\n\\{'+ '; '.join(marked)+'\n$$\n\n'
      'Now, when we add the two equations, the variable $'+v+'$ will be eliminated:\n\n'
      '$$\n\\begin{aligned}\n'+' \\\\\n'.join(rows)+'\n\\end{aligned}\n$$\n\n'
      'Therefore, the correct answer is the following:\n\n> *To eliminate $'+v+'$, multiply the $\\bbox[3pt,Gainsboro]{\\color{blue}\\text{'+name+'}}$ equation by $\\bbox[3pt,Gainsboro]{\\color{blue}'+tex(m)+'}$, and add the equations*.')


def sample_parameters(level,rng,profile):
    (lo,hi),(rlo,rhi)=BOUNDS[level]
    small=rng.randint(lo,hi); ratio=rng.randint(rlo,rhi)
    bs=small*rng.choice((-1,1)); bl=small*ratio*rng.choice((-1,1))
    bs,bl=(bs,bl) if rng.choice((False,True)) else (bl,bs)
    nz=[x for x in range(-10,11) if x]
    return dict(a1=rng.choice(nz),b1=bs,c1=rng.choice(nz),a2=rng.choice(nz),b2=bl,c2=rng.choice(nz),variables=list(rng.choice(VARIABLES)))


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in BOUNDS: raise ValueError('Unknown difficulty')
    if field_type not in (None,'select',':answer-field.type/select'): raise ValueError('Paired select fields required')
    rng=random.Random(seed)
    evidence=bool(profile and (profile.startswith('raw-') or profile.startswith('completed-')))
    raw=bool(profile and profile.startswith('raw-'))
    if evidence:
        source_id=profile.split('-',1)[1]
        if source_id not in ANCHORS: raise ValueError('Unknown evidence profile')
        expected_template=SOURCE_TEMPLATES[source_id]
        if template not in (None,expected_template):raise ValueError('Evidence profile/mask mismatch')
        template=expected_template
    else:
        source_id=None
        template=template or rng.choice(TEMPLATES)
        if template not in TEMPLATES:raise ValueError('Unknown template')
        # Select eligible complete profile BEFORE parameters.
        profile=profile or ('difference' if level=='easy' or template=='compact' else 'coefficient')
        if level=='easy' and profile=='coefficient':raise ValueError('Coefficient bank collides at unit target; use difference')
        if profile not in ('difference','coefficient'):raise ValueError('Unknown normal profile')
    explicit=parameters is not None
    if evidence and not explicit: raise ValueError('Evidence profiles require explicit parameters; not a source sampler')
    for attempt in range(1000):
        p=dict(parameters) if explicit else sample_parameters(level,rng,profile)
        try:
            row,m=validate_parameters(p,level,raw=evidence)
            values=bank(p,profile)
            problem=prompt(p,template,raw=raw)
            break
        except ValueError:
            if explicit:raise
    else:raise RuntimeError('Whole-bank eligible sampling exhausted')
    worked=None if raw else solution(p)
    contents={'problem':problem,'solution':worked,'banks':{'field-2':sorted(tex(v) for v in values),'field-1':['first','second']},'difficulty':None if raw else level,'completed':not raw}
    identity=digest(contents);question_id=uid(identity)
    fields=[]
    correct={'field-2':tex(m),'field-1':'first' if row==0 else 'second'}
    # Frozen capture field order is field-2 then field-1.
    for key,vals,atype in [('field-2',[tex(v) for v in values],':answer.type/math'),('field-1',['second','first'],':answer.type/text')]:
        field_id=uid(identity+key)
        choices=[{':answer/id':uid(identity+key+value),':answer/type':atype,':answer/value':value} for value in vals]
        f={':answer-field/id':field_id,':answer-field/key':key,':answer-field/type':':answer-field.type/select',':answer-field/choices':choices}
        if not raw:f[':answer-field/correct']=[':answer/id',uid(identity+key+correct[key])]
        # Option ordering has no bearing on content identity.
        rng.shuffle(choices);fields.append(f)
    q={':question/id':question_id,':question/problem':problem,':question/answer-fields':fields}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked})
    common=sp.igcd(*(p[k] for k in ('a1','b1','c1','a2','b2','c2')))
    common=int(abs(common))
    fingerprint=digest({'ordered_target_coefficients_up_to_global_scaling':[abs(p['b1'])//common, p['b2']*int(sp.sign(p['b1']))//common],'target_variable_index':1,'smaller_is_unit':min(abs(p['b1']),abs(p['b2']))//common==1,'integer_multiplier_only':not raw})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile,'parameters':p,'source':PROVENANCE,'source_id':source_id,
       'evidence_only':evidence,'eligible_for_learning':not evidence,'authored_difficulty':not raw,'correct_designations':'missing-original' if raw else 'independently-inferred',
       'content_identity':identity,'mathematical_fingerprint':fingerprint,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
       'operation':{'transformed_row':row+1,'unchanged_row':2-row,'multiplier':str(m)},'plot_rating':'none'}}


# EASY: unit target coefficient, signed integer scaling magnitude2–7.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)


# MODERATE: nonunit target magnitude2–4, integer quotient magnitude2–4.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)


# HARD: same nonunit integer quotient, magnitude5–7 and target product≤28.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)


def markdown(record):
    q=record['question'];meta=record['generation']
    parts=[f"### {meta['level']} / {meta['template']} / {meta['profile']}",q[':question/problem']]
    for field in q.get(':question/answer-fields',[]):
        lookup=field.get(':answer-field/correct',[None,None])[1]
        parts.append('\n'+field[':answer-field/key']+': '+', '.join(('**'+a[':answer/value']+'**') if a[':answer/id']==lookup else a[':answer/value'] for a in field[':answer-field/choices']))
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    else:parts.append('Raw evidence: worked solution and correct references absent in original.')
    return '\n\n'.join(parts)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile');ap.add_argument('--parameters',help='Explicit JSON object for public replay')
    args=ap.parse_args();levels=BOUNDS if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile,parameters=json.loads(args.parameters) if args.parameters else None) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))

if __name__=='__main__':main()
