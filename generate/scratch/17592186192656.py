#!/usr/bin/env python3
"""Solve a two-variable linear system using ONE first-variable elimination.

Frozen math basis 1356. Raw source profiles replay both unrated originals through
parameterized prompt/bank recipes and preserve absent grading/solution attributes.
These evidence-only banks are never defaults. Authored completions use the two
observed layouts and the canonical coefficient/multiplication/addition/solve/
back-substitution sequence. Every level is an authored design claim.

Easy: a unit smaller first-variable coefficient, integer multiplier 2–7.
Moderate: smaller coefficient 2–3, integer multiplier 2–4.
Hard: smaller coefficient 2–3, integer multiplier 5–7.
All use signed integer coefficients, integer solutions and bounded arithmetic;
there is no two-row scaling, no second-variable elimination and no progression.
Radio defaults use one whole bank of four explicit method errors, not offsets.
CLI/JSON are local review records; this script performs no database operations.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186192656
KP_UUID='2dbf4e1a-2c87-562d-8c4d-41fd32e79b86'
TITLE='Solving a System of Equations by Eliminating the First Variable'
VERSION='solve-first-one-transform-v3'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
ANCHORS={'q-18787':dict(a1=4,b1=-5,c1=0,a2=2,b2=-3,c2=2,variables='xy'),
'q-208816':dict(a1=4,b1=3,c1=5,a2=-1,b2=7,c2=-9,variables='xy')}
TEMPLATES={'radio_solution':'radio','blank_solution':'blank'}
SOURCE_TEMPLATE={'q-18787':'radio_solution','q-208816':'blank_solution'}
NS=uuid.UUID(KP_UUID)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(NS,value))
def tex(value):return sp.latex(sp.Rational(value))
def term(n,v,raw=False):
    n=sp.Rational(n)
    return (('- ' if raw else '-') if n<0 else '')+('' if abs(n)==1 else tex(abs(n)))+v

def lhs(a,b,x,y,raw=False):return term(a,x,raw)+(' + ' if b>0 else ' - ')+term(abs(b),y,raw)
def equation(a,b,c,x,y,raw=False):return lhs(a,b,x,y,raw)+(' ='+str(c) if raw and c<0 else ' = '+str(c))
def enum_projection(question):
    """Project pulled enum refs to local ident strings without adding attributes."""
    q=copy.deepcopy(question)
    for field in q.get(':question/answer-fields',[]):
        value=field.get(':answer-field/type')
        if isinstance(value,dict):field[':answer-field/type']=value[':db/ident']
        for answer in field.get(':answer-field/choices',[]):
            value=answer.get(':answer/type')
            if isinstance(value,dict):answer[':answer/type']=value[':db/ident']
    return q

def primitive_rows(p):
    """Canonical equation triples; common and separate row factors are incidental."""
    normalized=[]
    for i in (1,2):
        row=[p[f'{s}{i}'] for s in ('a','b','c')]
        factor=sp.igcd(*row);sign=sp.sign(row[0])
        normalized.append(tuple(int(z/factor*sign) for z in row))
    return normalized

def operation(p):
    row=0 if abs(p['a1'])<abs(p['a2']) else 1
    return row,-sp.Rational(p[f'a{2-row}'],p[f'a{row+1}'])
def values(p):
    determinant=p['a1']*p['b2']-p['a2']*p['b1']
    return (sp.Rational(p['c1']*p['b2']-p['c2']*p['b1'],determinant),sp.Rational(p['a1']*p['c2']-p['a2']*p['c1'],determinant))
def parameters_check(p,level,evidence=False):
    if set(p)!=set(ANCHORS['q-18787']):raise ValueError('Exactly a1,b1,c1,a2,b2,c2,variables required')
    if p['variables'] not in ('xy','ab','uv','st'):raise ValueError('Unsupported variable pair')
    if any(type(p[k]) is not int for k in p if k!='variables'):raise ValueError('Integer coefficients required')
    if any(p[k]==0 for k in ('a1','a2','b1','b2')):raise ValueError('Nonzero variable coefficients required')
    if p['a1']*p['b2']==p['a2']*p['b1']:raise ValueError('Unique solution required')
    row,m=operation(p)
    if m.q!=1 or not 2<=abs(m)<=7:raise ValueError('One integer row scaling, ratio 2–7 required')
    if evidence:return
    small=min(abs(p['a1']),abs(p['a2']))
    if level=='easy' and small!=1:raise ValueError('Easy requires one unit first-variable coefficient')
    if level!='easy' and not 2<=small<=3:raise ValueError('Moderate/hard smaller coefficient 2–3 required')
    lo,hi=(2,7) if level=='easy' else ((2,4) if level=='moderate' else (5,7))
    if not lo<=abs(m)<=hi:raise ValueError('Level multiplier bound')
    # A whole-system GCF or an individual row GCF cannot manufacture a higher
    # workload. Both printed arithmetic and equivalent primitive rows must meet
    # the same level definition. This guard is author-side eligibility only;
    # no preliminary simplification step is added to the learner solution.
    primitive=primitive_rows(p)
    reduced_small=min(z[0] for z in primitive);reduced_big=max(z[0] for z in primitive)
    reduced_ratio=sp.Rational(reduced_big,reduced_small)
    if (reduced_small!=1 if level=='easy' else not 2<=reduced_small<=3):
        raise ValueError('Primitive-row first-variable coefficient violates level workload')
    if reduced_ratio.q!=1 or not lo<=reduced_ratio<=hi:
        raise ValueError('Primitive-row multiplier violates level workload')
    if any(not 1<=abs(p[k])<=7 for k in ('b1','b2')):raise ValueError('Second-variable coefficient bound 1–7')
    bound={'easy':25,'moderate':35,'hard':40}[level]
    if any(abs(p[k])>bound for k in ('c1','c2')):raise ValueError('Level constant bound')
    answer=values(p)
    if any(v.q!=1 or not 1<=abs(v)<=5 for v in answer):raise ValueError('Nonzero integer solution coordinates, magnitude 1–5 required')

def prompt(p,template,raw=False):
    x,y=p['variables'];eqs=[equation(p[f'a{i}'],p[f'b{i}'],p[f'c{i}'],x,y,raw) for i in (1,2)]
    system='$'+('{' if raw else '\\{')+'; '.join(eqs)+'$'
    if template=='radio_solution':return f'Find the solution $({x}, {y})$ to the following system of equations using the elimination method:\n\n'+system+f'\n\n*Hint: Eliminate the variable ${x}$.*'
    ending='The solution is $($\n{{field-1}} $$,\n{{field-2}}\n$)$.' if raw else 'The solution is $($\n{{field-1}}\n$,$\n{{field-2}}\n$)$.'
    return 'Consider the following system of equations:\n'+system+f'\n\nFind the solution $({x}, {y})$ to this system by eliminating the variable ${x}$.\n\n'+ending

def tuple_string(pair,slot=None):
    # Literal whitespace is part of the five observed options, not their meaning.
    separator=',' if slot==1 else ', '
    return '('+tex(pair[0])+separator+tex(pair[1])+')'
def bank(p,profile):
    X,Y=values(p);row,m=operation(p);other=1-row
    if profile in ('raw-q-18787','completed-opaque-q-18787'):
        # Opaque evidence expressions only. Offsets recover numerical patterns,
        # not source-author intent. Never eligible for learner generation.
        return [(X,-Y-1),(X,Y),(X,-Y-3),(-Y,-X),(X,-Y-2)]
    if profile=='authored-method-errors':
        a=p[f'a{row+1}'];b=p[f'b{row+1}'];c=p[f'c{row+1}'];B=p[f'b{other+1}'];C=p[f'c{other+1}']
        if B+b==0:raise ValueError('Whole bank undefined: omitted scaling of y coefficient')
        ywrong=[sp.Rational(C+c,B+m*b),sp.Rational(C+m*c,B+b),sp.Rational(C-m*c,B+m*b)]
        # Back-substitute every mistaken y into the same original equation as
        # the fixed worked solution; the fourth error reverses subtraction.
        return [(X,Y)]+[(sp.Rational(c-b*w,a),w) for w in ywrong]+[(sp.Rational(c+b*Y,a),Y)]
    if profile in ('raw-q-208816','authored-blanks'):return [X,Y]
    raise ValueError('Unknown complete profile')
def check_bank(p,pairs):
    if len(pairs)!=5 or len(set(pairs))!=5:raise ValueError('Whole tuple bank duplicates')
    valid=[z for z in pairs if all(p[f'a{i}']*z[0]+p[f'b{i}']*z[1]==p[f'c{i}'] for i in (1,2))]
    if valid!=[values(p)]:raise ValueError('Exactly one complete solution tuple required')

def check_radio_number_forms(p,pairs):
    """Prevent a correct-only integer tuple shortcut without changing the bank."""
    correct=values(p)
    if not any(z!=correct and all(v.q==1 for v in z) for z in pairs):
        raise ValueError('Whole radio bank requires an entirely integer wrong pair')

def signed_add(first,second):return first+(' + ' if second>=0 else ' - ')+tex(abs(second))
def worked_solution(p):
    x,y=p['variables'];row,m=operation(p);names=['first','second'];X,Y=values(p)
    a=[p['a1'],p['a2']];b=[p['b1'],p['b2']];c=[p['c1'],p['c2']]
    aa=a.copy();bb=b.copy();cc=c.copy();aa[row]*=m;bb[row]*=m;cc[row]*=m
    eqs=[equation(a[i],b[i],c[i],x,y) for i in (0,1)]
    eqs[row]='('+eqs[row]+r') \cdot ('+tex(m)+')'
    grouped='('+term(bb[0],y)+(' + ' if bb[1]>0 else ' - ')+term(abs(bb[1]),y)+')'
    right='('+signed_add(tex(cc[0]),cc[1])+')'
    stages=[lhs(aa[i],bb[i],x,y)+' &= '+tex(cc[i]) for i in (0,1)]
    stages += [grouped+' &= '+right,term(bb[0]+bb[1],y)+' &= '+tex(cc[0]+cc[1]),y+' &= '+tex(Y)]
    # Exactly the canonical back-substitution operations; division is an explicit
    # additional stage whenever the substituted x coefficient is nonunit.
    ai,bi,ci=a[row],b[row],c[row]
    substitution=term(ai,x)+(' + ' if bi>0 else ' - ')+('' if abs(bi)==1 else tex(abs(bi)))+'('+tex(Y)+')'
    evaluated=signed_add(term(ai,x),bi*Y)
    back=[lhs(ai,bi,x,y)+' &= '+tex(ci),substitution+' &= '+tex(ci),evaluated+' &= '+tex(ci)]
    if abs(ai)!=1:back.append(term(ai,x)+' &= '+tex(ci-bi*Y))
    back.append(x+' &= '+tex(X))
    aligned=lambda rs:'$$\n\\begin{aligned}\n'+' \\\\\n'.join(rs)+'\n\\end{aligned}\n$$'
    return (f'Notice that the coefficient of ${x}$ in the first equation is ${a[0]}$, while in the second equation it is ${a[1]}$.\n\n'
       f'If we multiply the {names[row]} equation by ${tex(m)}$, then the ${x}$-coefficient will become ${tex(aa[row])}$, which will cancel with the coefficient of ${a[1-row]}$ in the {names[1-row]} equation.\n\n'
       '$$\n\\{'+'; '.join(eqs)+'\n$$\n\n'+f'Now, when we add the two equations, the variable ${x}$ will be eliminated:\n\n'+aligned(stages)+'\n\n'
       f'So, the solution must have ${y} = {tex(Y)}$. However, we still need to find ${x}$. To do this, we substitute ${y} = {tex(Y)}$ back into one of the equations. Let\'s choose the {names[row]} equation:\n\n'+aligned(back)+'\n\n'
       f'Therefore, the solution to the system of equations is ${x}={tex(X)}, \\,{y}={tex(Y)}$, which can be expressed as $({tex(X)},{tex(Y)})$.')

def sample(level,rng):
    lo,hi=(2,7) if level=='easy' else ((2,4) if level=='moderate' else (5,7))
    small=1 if level=='easy' else rng.randint(2,3)
    coefficients=[small,small*rng.randint(lo,hi)];rng.shuffle(coefficients)
    nonzero=[i for i in range(-7,8) if i]
    a1,a2=[z*rng.choice((-1,1)) for z in coefficients];b1,b2=[rng.choice(nonzero) for _ in (0,1)]
    X,Y=[rng.choice([i for i in range(-5,6) if i]) for _ in (0,1)]
    return dict(a1=a1,b1=b1,c1=a1*X+b1*Y,a2=a2,b2=b2,c2=a2*X+b2*Y,variables=rng.choice(('xy','ab','uv','st')))
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
    rng=random.Random(seed)
    raw=bool(profile and profile.startswith('raw-'))
    opaque=profile=='completed-opaque-q-18787'
    source_id=profile.removeprefix('raw-') if raw else ('q-18787' if opaque else None)
    if source_id and source_id not in ORIGINALS:raise ValueError('Unknown observed profile')
    if source_id:
        expected=SOURCE_TEMPLATE[source_id]
        if template not in (None,expected):raise ValueError('Source profile/layout mismatch')
        template=expected
    elif template is None:
        if profile in ('authored-method-errors','authored-blanks'):
            template='radio_solution' if profile=='authored-method-errors' else 'blank_solution'
        elif field_type not in (None,'blank','radio'):raise ValueError('Unknown field type')
        if template is None:template=field_type+'_solution' if field_type else rng.choice(tuple(TEMPLATES))
    if template not in TEMPLATES:raise ValueError('Unknown template')
    kind=TEMPLATES[template]
    if field_type not in (None,kind):raise ValueError('Layout/field type mismatch')
    profile=profile or ('authored-method-errors' if kind=='radio' else 'authored-blanks')
    if profile not in ('raw-q-18787','raw-q-208816','completed-opaque-q-18787','authored-method-errors','authored-blanks'):raise ValueError('Unknown profile')
    if (kind=='radio') != (profile in ('raw-q-18787','completed-opaque-q-18787','authored-method-errors')):raise ValueError('Profile/layout mismatch')
    for attempt in range(2000):
        p=copy.deepcopy(parameters if parameters is not None else (ANCHORS[source_id] if source_id else sample(level,rng)))
        try:
            parameters_check(p,level,raw);bankvalues=bank(p,profile)
            if kind=='radio':
                check_bank(p,bankvalues)
                if profile=='authored-method-errors':check_radio_number_forms(p,bankvalues)
            break
        except ValueError:
            if parameters is not None or source_id:raise
    else:raise ValueError('No eligible whole-bank instance')
    X,Y=values(p)
    if raw:
        # Only immutable source attribute/layout skeletons are copied. Mathematical
        # prompt and EVERY available option are always rendered by public recipes.
        q={k:v for k,v in enum_projection(ORIGINALS[source_id]).items() if k!=':question/problem'}
        q[':question/problem']=prompt(p,template,True)
        if kind=='radio':
            for slot,(answer,pair) in enumerate(zip(q[':question/answer-fields'][0][':answer-field/choices'],bankvalues)):
                answer[':answer/value']=tuple_string(pair,slot)
    else:
        q={':question/problem':prompt(p,template),':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked_solution(p),':question/answer-fields':[]}
        if kind=='radio':
            choices=[tuple_string(pair,slot if opaque else None) for slot,pair in enumerate(bankvalues)]
            q[':question/answer-fields'].append({':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':z} for z in choices],'_correct_value':choices[bankvalues.index((X,Y))]})
        else:
            for key,v in zip(('field-1','field-2'),(X,Y)):
                q[':question/answer-fields'].append({':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)}],'_correct_value':tex(v)})
    clean=copy.deepcopy(q)
    for field in clean[':question/answer-fields']:
        if ':answer-field/choices' in field:field[':answer-field/choices']=sorted(field[':answer-field/choices'],key=lambda z:z[':answer/value'])
    content=digest([VERSION,clean])
    if not raw or p!=ANCHORS[source_id]:
        q[':question/id']=uid(content)
        for field in q[':question/answer-fields']:
            key=field[':answer-field/key'];field[':answer-field/id']=uid(content+key)
            for answer in field.get(':answer-field/choices',[]):answer[':answer/id']=uid(content+key+answer[':answer/value'])
    if not raw:
        for field in q[':question/answer-fields']:
            correct=field.pop('_correct_value')
            field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value']==correct)]
            if kind=='radio':rng.shuffle(field[':answer-field/choices'])
    # Primitive rows and their multiplier deduplicate common or individual
    # equation rescalings and variable aliases. Raw printed arithmetic still
    # belongs to content identity; it cannot inflate meaningful task counts.
    normalized=primitive_rows(p)
    reduced_ratio=sp.Rational(max(z[0] for z in normalized),min(z[0] for z in normalized))
    task=digest([sorted(normalized),str(reduced_ratio)])
    return dict(knowledge_point=dict(db_id=KP_ID,id=KP_UUID,title=TITLE),question=q,generation=dict(version=VERSION,seed=seed,template=template,profile=profile,parameters=p,source={k:v for k,v in SOURCE.items() if k!='record'},mathematical_fingerprint=task,content_identity=content,evidence_only=raw or opaque,eligible_for_learning=not (raw or opaque),authored_completion=not raw,difficulty_claim='authored; both originals unrated',opaque_bank=profile in ('raw-q-18787','completed-opaque-q-18787'),python=sys.version.split()[0],sympy=sp.__version__))

# EASY: unit coefficient for the substituted first variable, integer multiplier2–7.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE: nonunit substituted coefficient2–3, multiplier2–4, explicit final division.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD: same nonunit substitution, multiplier5–7; bounded signed integer arithmetic.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(record):
    q=record['question'];text=q[':question/problem']
    for field in q.get(':question/answer-fields',[]):
        text+='\n\n'+field[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in field.get(':answer-field/choices',[]))
    return text+'\n\n'+q.get(':question/worked-solution','[Raw original omits worked solution, rating and correct references.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
