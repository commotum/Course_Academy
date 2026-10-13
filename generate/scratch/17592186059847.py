#!/usr/bin/env python3
"""Exact 3x3 determinant generators, math basis 1356; local review only.

All choices are expressions of matrix entries. Sparse-source distractor intent
is not identifiable: see extraction for explicit inferred index/product patterns.
Profiles are complete banks, selected before sampling and rejected as a whole.
No literal source payload, source-answer table, database write, or plots are used.
Easy supports observed radio/blank families; moderate and hard are explicitly
authored arithmetic workloads using exactly the same top-row cofactor method.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import uuid
import sympy as sp

KP_ID = 17592186059847
KP_UUID = '979859e4-b60c-548d-8da6-b180400e1b07'
TITLE = 'Calculating the Determinant of a 3x3 Matrix'
VERSION = 'determinant-3x3-v1'
SOURCE = {'database':'math', 'basis':1356, 'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING = 'Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:'
SYMBOLS = sp.symbols('a b c d e f g h i')
a,b,c,d,e,f,g,h,i = SYMBOLS
DET = a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

# Each profile lists all four wrong values, never an interchangeable error pool.
# Formulas with uncertain source interpretation retain algebraic index patterns.
BANK_PROFILES = {
 'diagonal': ('legacy_radio','q-38128',(a*e,-e*i,-a*e,e*i)),
 'legacy_zero_diagonal': ('legacy_radio','q-9841',(
     d*g*c-d*g*f+d*d*f, g*g*f-d*f*f, a*(e*i-f*h), c*d*f-c*g*f)),
 'signed_one_zero': ('aligned_radio','q-128309',(e*g,-g,-e*h,-a*e)),
 'upper_triangular': ('aligned_radio','q-38100',(
     a*(e*i-f*h)+b*(f*i-f*g), -a*(e*i-f*i), a*(e*e-f*f), e*e+c*f*f)),
 'lower_triangular': ('aligned_radio','q-38124',(
     a*(e*i-f*h)*2, a*(d*i-f*h)+a*(e*i-f*h), a*(g*i-f*h), a*(h*i-f*h))),
 'sparse_two_terms': ('aligned_radio','q-38174',(
     a*(d*i-f*i)+c*(d*h-e*g), -c*(d*h-e*g), -a*(e*i-f*h), a*(e*i-f*h))),
 'sparse_second_column': ('aligned_radio','q-38176',(
     a*(e*i-f*h), c*(d*h-e*g), a*(e*g-f*h)+c*(d*h-e*g), a*(e*i-f*h)+c*(d*h+e*g))),
 'zero_diagonal': ('aligned_radio','q-38180',(
     a*(e*i-f*h), b*(d*i-f*g), -DET, c*(d*h-e*g))),
 'signed_one_zero_b': ('aligned_radio','q-128308',(
     b*(d*i-e*g)+b*(d*i-f*g), a*(e*i-f*i)+c*(d*h-e*g),
     a*(e*i-f*h)+c*(e*h-e*g), -(a*(e*i+f*h)-b*(d*i-f*g)+c*(d*h-e*g)))),
 'cofactor_signs': ('aligned_radio',None,(
     a*(e*i-f*h)+b*(d*i-f*g)+c*(d*h-e*g),
     a*(e*i-f*h)-b*(d*i-f*g)-c*(d*h-e*g),
     a*(e*i+f*h)-b*(d*i+f*g)+c*(d*h+e*g), -DET)),
}
TEMPLATES = {
 'legacy_radio': {'kind':'radio','style':'evaluated','notation':'vmatrix'},
 'aligned_radio': {'kind':'radio','style':'evaluated','notation':'aligned'},
 'matrix_blank': {'kind':'blank','style':'evaluated','notation':'aligned'},
 'matrix_blank_products': {'kind':'blank','style':'products','notation':'aligned'},
}
# Source masks are structural sampling policies, not source answers.
MASKS = {
 'diagonal':(1,0,0,0,1,0,0,0,1),
 'legacy_zero_diagonal':(0,1,1,1,0,1,1,1,0),
 'signed_one_zero':(1,1,1,1,1,0,1,1,1),
 'upper_triangular':(1,1,1,0,1,1,0,0,1),
 'lower_triangular':(1,0,0,1,1,0,1,1,1),
 'sparse_two_terms':(1,0,1,0,1,1,1,0,1),
 'sparse_second_column':(1,0,1,0,1,0,1,0,1),
 'zero_diagonal':(0,1,1,1,0,1,1,1,0),
 'signed_one_zero_b':(1,1,1,0,1,1,1,1,1),
}


class SampleRejected(ValueError):
    """One option invalidates the complete selected bank."""


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def texmatrix(entries,notation='aligned'):
    rows = [ ' & '.join(map(str,entries[j:j+3])) for j in (0,3,6)]
    if notation=='vmatrix':
        return r'\begin{vmatrix}' + r' \\ '.join(rows) + r'\end{vmatrix}'
    return r'|\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}|'


def minor_tex(v):
    return r'|\begin{aligned}'+f'{v[0]} & {v[1]}' + r' \\ '+f'{v[2]} & {v[3]}' + r'\end{aligned}|'


def par(n):
    return '('+str(n)+')' if n<0 else str(n)


def signed_sum(items):
    result=''
    for val,txt in items:
        if not result:
            result=txt
        else:
            result += ('' if txt.startswith('-') else '+')+txt
    return result or '0'


def product(x,y):
    return par(x)+r'\cdot '+par(y)


def subtract(x,y):
    # Preserve minus-negative parentheses when needed, instead of malformed --.
    return str(x)+'-'+par(y)


def build_solution(m,style='evaluated'):
    aa,bb,cc,dd,ee,ff,gg,hh,ii=m
    minors=[(ee,ff,hh,ii),(dd,ff,gg,ii),(dd,ee,gg,hh)]
    coefs=[aa,-bb,cc]
    vals=[x*w-y*z for x,y,z,w in minors]
    terms=[x*y for x,y in zip(coefs,vals)]
    expansion=par(aa)+minor_tex(minors[0])+'-'+par(bb)+minor_tex(minors[1])+'+'+par(cc)+minor_tex(minors[2])
    lines=[texmatrix(m)+' & ='+expansion]
    if style=='products':
        pieces=[]
        for coef,(x,y,z,w) in zip(coefs,minors):
            if coef==0: pieces.append((0,'0')); continue
            text=par(coef)+'('+product(x,w)+'-'+product(y,z)+')'
            pieces.append((coef,text))
        lines.append(' & ='+signed_sum(pieces))
    pieces=[]
    for coef,(x,y,z,w) in zip(coefs,minors):
        if coef==0:pieces.append((0,'0'));continue
        pieces.append((coef,par(coef)+'('+subtract(x*w,y*z)+')'))
    lines.append(' & ='+signed_sum(pieces))
    pieces=[(coef,product(coef,val)) for coef,val in zip(coefs,vals) if coef!=0 and val!=0]
    if pieces: lines.append(' & ='+signed_sum(pieces))
    pieces=[(val,str(val)) for val in terms if val!=0]
    if len(pieces)>1:lines.append(' & ='+signed_sum(pieces))
    lines.append(' & ='+str(sum(terms)))
    solution=OPENING+'\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$'
    return solution,{'minors':vals,'cofactor_coefficients':coefs,'weighted_terms':terms,'determinant':sum(terms)}


def validate_parameters(parameters,template):
    if not isinstance(parameters,dict) or set(parameters)-{'matrix','name'}:
        raise ValueError('Parameters must contain only matrix and optional name.')
    m=parameters.get('matrix')
    if not isinstance(m,list) or len(m)!=9 or any(type(x) is not int for x in m):
        raise ValueError('matrix must be a flat list of nine exact integers.')
    name=parameters.get('name','A')
    if not isinstance(name,str) or len(name)!=1 or not name.isascii() or not name.isupper():
        raise ValueError('name must be a single uppercase ASCII letter.')
    if TEMPLATES[template]['kind']=='radio' and 'name' in parameters:
        raise ValueError('Radio prompts do not name the matrix.')
    return {'matrix':m,**({'name':name} if TEMPLATES[template]['kind']=='blank' else {})}


def sample(rng,level,template,profile):
    if level=='easy':
        mask=MASKS.get(profile)
        if mask is None:
            mask=rng.choice([(1,1,0,1,1,1,0,1,1),(0,1,1,1,0,1,1,1,0),
                             (0,1,1,0,0,1,0,0,1),(1,1,1,1,1,0,1,1,1),(1,)*9])
        values=list(range(-7,0))+list(range(1,9))
    elif level=='moderate':
        mask=(1,)*9
        values=list(range(-8,-1))+list(range(2,9))
    else:
        mask=(1,)*9
        values=list(range(-12,-3))+list(range(4,13))
    p={'matrix':[rng.choice(values) if keep else 0 for keep in mask]}
    if TEMPLATES[template]['kind']=='blank':p['name']=rng.choice('AHQRW')
    return p


def build(level,seed,template,p,profile):
    spec=TEMPLATES[template]
    m=p['matrix']; subs=dict(zip(SYMBOLS,m))
    solution,work=build_solution(m,spec['style'])
    correct=int(DET.subs(subs))
    if correct!=int(sp.Matrix(3,3,m).det()):raise AssertionError('determinant disagreement')
    bank=[('correct',correct)]
    if spec['kind']=='radio':
        recipes=BANK_PROFILES[profile][2]
        bank += [(str(expr),int(expr.subs(subs))) for expr in recipes]
        if len({v for _,v in bank})!=5:raise SampleRejected('Required bank has equivalent/duplicate choices')
    notation=spec['notation']
    if spec['kind']=='radio':
        prompt='Find the value of $'+texmatrix(m,notation)+('$.' if notation=='vmatrix' else '.$')
    else:
        matrix=texmatrix(m)[1:-1]
        prompt='If $'+p['name']+'=['+matrix+'],$ then $det('+p['name']+')=${{field-1}}.'
    # Mathematical fingerprint does not change with response style or bank.
    parameter_key=digest({'matrix':m})
    content_key=digest({'level':level,'prompt':prompt,'solution':solution,'kind':spec['kind'],'bank':sorted(v for _,v in bank)})
    qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+VERSION+'/'+content_key)
    key='selection' if spec['kind']=='radio' else 'field-1'
    fid=uuid.uuid5(qid,key)
    answers=[]; recipe_metadata={}
    for recipe,val in bank:
        aid=str(uuid.uuid5(fid,'math:'+str(val)))
        answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':str(val)})
        if recipe=='correct':correct_id=aid
        else:recipe_metadata[aid]=recipe
    random.Random(seed).shuffle(answers)
    source_id=BANK_PROFILES[profile][1] if profile else None
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':solution,
        ':question/answer-fields':[{
          ':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec['kind'],
          ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},
      'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,
        'parameter_fingerprint':parameter_key,'content_fingerprint':content_key,'bank_profile':profile,
        'bank_origin':'observed' if source_id else ('authored' if profile else 'not applicable'),
        'recipe_origin':'inferred entry-product generalization of observed scalar bank' if source_id else ('authored cofactor-sign errors' if profile else 'not applicable'),
        'solution_origin':'authored source-style solution (legacy originals omit solution)' if template=='legacy_radio' else 'source-style cofactor stages with normalized signed arithmetic',
        'authored_extension':level!='easy' or profile=='cofactor_signs','source_analysis':SOURCE,
        'source_question_ids':[source_id] if source_id else [],'distractor_recipes':recipe_metadata,
        'worked_values':work,'answer_shape':'integer','domain':'3x3 matrix with integer entries',
        'plot_rating':'none','plot_assets':{}}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio','blank'):raise ValueError('Unknown field type')
    if profile is not None:
        if profile not in BANK_PROFILES:raise ValueError('Unknown profile')
        required=BANK_PROFILES[profile][0]
        if template is not None and template!=required:raise ValueError('Profile/template mismatch')
        template=required
        if level!='easy' and profile!='cofactor_signs':raise ValueError('Observed profiles belong to easy (including assigned unrated originals)')
    rng=random.Random(seed)
    if template is None:
        # Uncertain observed scalar-bank generalizations are explicit replay
        # profiles, not the default source of learner distractors.
        eligible=[k for k,v in TEMPLATES.items() if (field_type is None or v['kind']==field_type) and k!='legacy_radio']
        template=rng.choice(eligible)
    if template not in TEMPLATES:raise ValueError('Unknown template')
    if level!='easy' and template=='legacy_radio':raise ValueError('Legacy notation is source-only easy')
    if field_type and TEMPLATES[template]['kind']!=field_type:raise ValueError('Field/template mismatch')
    if TEMPLATES[template]['kind']=='radio' and profile is None:
        if template=='aligned_radio':
            profile='cofactor_signs'
        else:
            eligible=[k for k,v in BANK_PROFILES.items() if v[0]==template]
            profile=rng.choice(eligible)
    elif TEMPLATES[template]['kind']=='blank' and profile is not None:raise ValueError('Blank fields have no bank')
    if parameters is not None:
        return build(level,seed,template,validate_parameters(parameters,template),profile)
    for _ in range(10000):
        p=sample(rng,level,template,profile)
        try:return build(level,seed,template,p,profile)
        except SampleRejected:continue
    raise RuntimeError('Could not sample complete valid bank')


# EASY — all observed templates, masks, and complete source banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)


# MODERATE — authored dense signed entries, same three minors, magnitudes 2..8.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)


# HARD — authored dense signed entries, same three minors, magnitudes 4..12.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question'];g=record['generation'];f=q[':question/answer-fields'][0]
    lines=['## Generated '+q[':question/difficulty'].split('/')[-1],
      'Template: `'+g['template']+'`; bank: `'+str(g['bank_profile'])+'`; origin: '+g['bank_origin']+'.','',q[':question/problem'],'']
    lines += ['- $'+v[':answer/value']+'$'+(' (correct)' if v[':answer/id']==f[':answer-field/correct'][1] else '') for v in f[':answer-field/choices']]
    lines += ['',q[':question/worked-solution']]
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=list(BANK_PROFILES))
    parser.add_argument('--field-type',choices=['radio','blank'])
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    try: records=[generate(level,args.seed+j,args.template,args.field_type,profile=args.profile) for level in levels for j in range(args.count)]
    except ValueError as exc:parser.error(str(exc))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))


if __name__=='__main__':main()
