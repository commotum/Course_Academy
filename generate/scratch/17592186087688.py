#!/usr/bin/env python3
"""Find the unknown x coefficient by equating slopes of parallel lines.

All three difficulty labels, answer completions and practice worked solutions
are authored: the two captured practice blanks have none of these attributes.
Public raw-* profiles reconstruct their prompts from the same parameterized
recipes and preserve absent attributes. They are evidence-only, not gradable.
No question is obtained by returning a captured payload or looking up an answer.
"""
import argparse
import hashlib
import json
import math
import random
import sys
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186087688
KP_UUID = '43401830-730c-57d7-8831-9a0580042ffe'
TITLE = 'Finding Unknown Parameters'
VERSION = '2.0.0'
HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE/'source.json').read_text())
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
TEMPLATES = ('mixed-form', 'two-standard')
BANK_PROFILES = {
    'authored-blank': {'origin':'authored', 'raw':False},
    'raw-q-214098': {'origin':'observed incomplete evidence', 'raw':True, 'template':'mixed-form', 'level':'easy', 'source':'q-214098'},
    'raw-q-214099': {'origin':'observed incomplete evidence', 'raw':True, 'template':'two-standard', 'level':'moderate', 'source':'q-214099'},
    'completed-q-214098': {'origin':'inferred completion', 'raw':False, 'template':'mixed-form', 'level':'easy', 'source':'q-214098'},
    'completed-q-214099': {'origin':'inferred completion', 'raw':False, 'template':'two-standard', 'level':'moderate', 'source':'q-214099'},
}
SLOPES = tuple(sorted({sp.Rational(n,d) for n in range(-12,13) if n for d in range(1,8)}))
COEFFICIENTS = tuple(b for b in range(-9,10) if abs(b)>=2)
DOMAIN = {
 'slope':'reduced nonzero n/d; |n|<=12, 1<=d<=7',
 'easy':'mixed forms; integer known slope; one conversion and coefficient solve',
 'moderate':'two standard forms; integer known slope; two conversions and coefficient solve',
 'hard':'two primitive standard forms; noninteger reduced known slope; gcd(|unknown y coefficient|, slope denominator)=1; noninteger answer',
 'unknown_y_coefficient':'integer with 2<=|b|<=9; unit coefficients excluded to retain isolation workload',
 'known_intercept':'integer -12..12', 'unknown_constant':'integer -15..15',
 'known_scale':'1 in authored defaults; 1..3 in source replay/completion profiles to preserve observed scaled known equation',
 'task_fingerprint':'assessed known-form information, reduced known slope, unknown y coefficient; intercepts, known scaling, bank/profile, spelling and seed excluded',
 'workload':'unknown x coefficient only, distinct nonvertical lines; no points, perpendicularity, equation construction or extra parameter branches',
}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def tex(value):
    return sp.latex(sp.Rational(value))
def signed(value):
    return (' + ' if value>=0 else ' - ')+tex(abs(value))
def term(coefficient, variable):
    return ('-' if coefficient==-1 else '' if coefficient==1 else tex(coefficient))+variable

def line(a,b,c,tight_equal=False):
    return term(a,'x')+(' - ' if b<0 else ' + ')+term(abs(b),'y')+(' =' if tight_equal else ' = ')+str(c)
def slope_coefficient(b,display=False):
    command = 'dfrac' if display else 'frac'
    return ('-' if b>0 else '')+'\\'+command+'{k}{'+str(abs(b))+'}'
def blocks(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(a+' &= '+b for a,b in rows)+'\n'+r'\end{aligned}'+'\n$$'
def conversion(a,b,c,first):
    # Preserve the canonical operation sequence, including its sign-normalizing row.
    rows=[(first.split('=')[0].strip(),first.split('=')[1].strip()),
          (term(b,'y'),term(-a,'x')+signed(c))]
    if b < -1:
        rows.append((term(-b,'y'),term(a,'x')+signed(-c)))
    rows.append(('y',tex(sp.Rational(-a,b))+'x'+signed(sp.Rational(c,b))))
    return blocks(rows)

def unknown_conversion(b,c,first):
    rows=[(first.split('=')[0].strip(),first.split('=')[1].strip()),
          (term(b,'y'),'-kx'+signed(c))]
    if b<0:
        rows.append((term(-b,'y'),'kx'+signed(-c)))
    rows.append(('y',slope_coefficient(b)+'x'+signed(sp.Rational(c,b))))
    return blocks(rows)

def eligible_pairs(level):
    return [(m,b) for m in SLOPES for b in COEFFICIENTS
            if (m.q==1 if level!='hard' else m.q>1 and math.gcd(abs(b),int(m.q))==1)]
DOMAIN['distinct_tasks_by_level']={level:len(eligible_pairs(level)) for level in SUPPORTED_LEVELS}

def validate_parameters(raw,level,template,profile):
    keys={'slope','known_intercept','unknown_y_coefficient','unknown_constant','known_scale'}
    if not isinstance(raw,dict) or set(raw)!=keys:
        raise ValueError('Exactly the documented five parameter keys are required')
    if isinstance(raw['slope'],bool) or isinstance(raw['slope'],float):
        raise ValueError('Use an exact rational slope, not bool/float')
    try:
        m=sp.Rational(raw['slope'])
    except Exception as exc:
        raise ValueError('An exact rational slope is required') from exc
    if m not in SLOPES:
        raise ValueError('Reduced slope outside documented coefficient bounds')
    b,h,c,s=(raw[key] for key in ('unknown_y_coefficient','known_intercept','unknown_constant','known_scale'))
    if type(b)!=int or b not in COEFFICIENTS:
        raise ValueError('Unknown y coefficient requires 2<=absolute value<=9')
    if type(h)!=int or not -12<=h<=12 or type(c)!=int or not -15<=c<=15:
        raise ValueError('Intercept/constant outside documented integer bounds')
    maximum=3 if 'source' in BANK_PROFILES[profile] else 1
    if type(s)!=int or not 1<=s<=maximum:
        raise ValueError('Known scale must be primitive 1, except source profiles allow 1..3')
    if sp.Rational(c,b)==h:
        raise ValueError('Coincident lines excluded; reject entire instance')
    if level=='easy' and (template!='mixed-form' or m.q!=1):
        raise ValueError('Easy requires mixed form and integer slope')
    if level=='moderate' and (template!='two-standard' or m.q!=1):
        raise ValueError('Moderate requires two standard forms and integer slope')
    if level=='hard' and (template!='two-standard' or m.q==1 or math.gcd(abs(b),int(m.q))!=1):
        raise ValueError('Hard requires reduced noninteger slope and noncancelling rational coefficient solve')
    return {'slope':str(m),'known_intercept':h,'unknown_y_coefficient':b,'unknown_constant':c,'known_scale':s}

def task_key(p,template):
    return digest({'assessed_known_form':template,'known_reduced_slope':str(sp.Rational(p['slope'])),
                   'unknown_y_coefficient':p['unknown_y_coefficient']})

def build(level,p,template,profile,seed):
    spec=BANK_PROFILES[profile];raw=spec['raw']
    m=sp.Rational(p['slope']);h=p['known_intercept'];b=p['unknown_y_coefficient'];c=p['unknown_constant'];s=p['known_scale']
    a=int(m.p*s);d=int(-m.q*s);e=h*d
    known='y = '+tex(m)+'x'+signed(h) if template=='mixed-form' else line(a,d,e,tight_equal=spec.get('source')=='q-214099')
    unknown='kx'+(' - ' if b<0 else ' + ')+term(abs(b),'y')+' = '+str(c)
    prompt=f'The lines ${known}$ and ${unknown}$ are parallel. What is the value of $k$?$k =$\n{{{{field-1}}}}'
    answer=-b*m
    solution='For two lines to be parallel, they must have the same slope.\n\n'
    if template=='mixed-form':
        solution+=f'- The line ${known}$ is in slope-intercept form, and its slope is ${tex(m)}$.\n'
    else:
        solution+=f'- To find the slope of the line ${known}$, we convert to slope-intercept form:\n\n'+conversion(a,d,e,known)+f'\n\nIn slope-intercept form, the slope is the $x$-coefficient. So, the slope is ${tex(m)}$.\n'
    solution+=f'- To find the slope of the line ${unknown}$, we convert to slope-intercept form:\n\n'+unknown_conversion(b,c,unknown)
    solution+=f'\n\nIn slope-intercept form, the slope is the $x$-coefficient. So, the slope is ${slope_coefficient(b,True)}$.\n\nSince the slopes of the two lines must be equal, we must have\n\n$$\n{slope_coefficient(b,True)}={tex(m)}\n$$\n\nMultiplying both sides by ${-b}$ gives $k={tex(answer)}$.\n\nConsequently, $k={tex(answer)}$.'
    # Hash actual learner content, including authored difficulty, full bank and omissions.
    content=digest({'version':VERSION,'problem':prompt,'solution':None if raw else solution,
                    'difficulty':None if raw else level,'field_type':':answer-field.type/blank',
                    'key':'field-1','bank':None if raw else [tex(answer)],'correct':None if raw else tex(answer)})
    qid=uid('question:'+content);fid=uid(qid+':field:field-1')
    field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank'}
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if raw:
        source=next(q for q in SOURCE['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==spec['source'])
        q[':db/id']=source[':db/id'];q[':question/math-academy-id']=spec['source'];field[':db/id']=source[':question/answer-fields'][0][':db/id']
    else:
        aid=uid(fid+':answer:'+tex(answer))
        field[':answer-field/choices']=[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(answer)}]
        field[':answer-field/correct']=[':answer/id',aid]
        q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,
             'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':spec['origin'],
             'evidence_only':raw,'eligible_for_learning':not raw,
             'difficulty_origin':'absent in raw evidence; all level routing and completed labels authored',
             'solution_origin':'absent in source practice; authored from canonical equality/conversion/conclusion sequence',
             'source_analysis':{**{key:SOURCE[key] for key in ('database','basis','lineage')},
                'source_ids':[spec['source']] if 'source' in spec else ['q-214098'] if template=='mixed-form' else ['q-214099'],
                'canonical_example':'e-14370','observed_correct_designation':'absent'},
             'parameter_fingerprint':task_key(p,template),'content_fingerprint':content,'domain':DOMAIN,
             'recipes':[],'answer_shape':'scalar coefficient fragment k, supplied k =','plot_rating':'none'}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Supported levels: easy, moderate, hard')
    if field_type not in (None,'blank',':answer-field.type/blank'):
        raise ValueError('Only observed blank layout is supported')
    profile=profile or 'authored-blank'
    if profile not in BANK_PROFILES:
        raise ValueError('Unknown profile')
    spec=BANK_PROFILES[profile]
    template=template or spec.get('template') or ('mixed-form' if level=='easy' else 'two-standard')
    if template not in TEMPLATES or 'template' in spec and (spec['template']!=template or spec['level']!=level):
        raise ValueError('Template/profile/level mismatch')
    if parameters is not None:
        return build(level,validate_parameters(parameters,level,template,profile),template,profile,seed)
    rng=random.Random(seed);pairs=eligible_pairs(level)
    for _ in range(200):
        m,b=rng.choice(pairs)
        candidate={'slope':str(m),'known_intercept':rng.randint(-12,12),'unknown_y_coefficient':b,
                   'unknown_constant':rng.randint(-15,15),'known_scale':1}
        try:
            p=validate_parameters(candidate,level,template,profile)
        except ValueError:
            continue
        return build(level,p,template,profile,seed)
    raise ValueError('Whole-instance bounded sampling exhausted')

# EASY — authored integer-slope mixed form, canonical one-line isolation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """One standard-form isolation, then solve -k/b=m for k; |b|>=2."""
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — authored integer-slope two-standard form, observed second prompt.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Convert both given equations before solving equal slopes; no rational slope."""
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored rational-slope two-standard form, same solving method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Primitive noninteger known slope; rational coefficient solve cannot cancel."""
    return generate('hard',seed,template,field_type,parameters,profile)

def batch(level,count,seed=0,template=None,field_type=None,profile=None):
    pairs=eligible_pairs(level)
    if type(count)!=int or not 1<=count<=len(pairs):
        raise ValueError('Count outside finite meaningful task domain: '+str(len(pairs)))
    rng=random.Random(seed);rng.shuffle(pairs);records=[]
    for i,(m,b) in enumerate(pairs[:count]):
        for _ in range(100):
            p={'slope':str(m),'known_intercept':rng.randint(-12,12),'unknown_y_coefficient':b,
               'unknown_constant':rng.randint(-15,15),'known_scale':1}
            if sp.Rational(p['unknown_constant'],b)!=p['known_intercept']:
                records.append(generate(level,seed+i,template,field_type,p,profile));break
        else:
            raise ValueError('Whole-instance sampling exhausted')
    return records

def markdown(record):
    q=record['question'];parts=[q[':question/problem']]
    if ':question/difficulty' in q:
        parts+=['Answer: $'+q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'$',q[':question/worked-solution']]
    else:
        parts+=['*Raw evidence only: difficulty, answer bank, correct reference and worked solution absent in source.*']
    return '\n\n'.join(parts)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('json','markdown'),default='markdown')
    parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=tuple(BANK_PROFILES))
    parser.add_argument('--field-type',choices=('blank',))
    args=parser.parse_args()
    if args.difficulty=='all' and (args.template or args.profile and args.profile!='authored-blank'):
        parser.error('Use a specific level with a template/source profile')
    levels=SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]
    try:
        records=[record for level in levels for record in batch(level,args.count,args.seed,args.template,args.field_type,args.profile)]
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':
    main()
