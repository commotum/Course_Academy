#!/usr/bin/env python3
"""Number of solutions to two linear equations; local review only (basis 1356).

All practice records are unrated/incomplete. raw_* profiles reproduce their
parameterized prompts/banks AND absence of difficulty, solution and correct ref.
Normal records explicitly author these missing elements. No plots are necessary.
See adjacent classification/extraction/validation for curriculum evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
import uuid
from fractions import Fraction
from pathlib import Path
import sympy as sp

KP_ID = 17592186073776
KP_UUID = 'a24fb4f3-6e3c-5c45-b31e-85b7ce290eda'
TITLE = 'Finding the Number of Solutions to a System'
VERSION = 'solution-count-v1'
LEVELS = ('easy', 'moderate', 'hard')
TEMPLATES = ('standard', 'zero_rhs')
VALUES = ('no solutions', 'infinitely many solutions', 'a single solution')
PROFILES = {'counts': None, 'raw_211984': ('standard', 'moderate', 'spaced', VALUES),
            'raw_237043': ('zero_rhs', 'hard', 'spaced', (VALUES[2], VALUES[1], VALUES[0])),
            'raw_237046': ('standard', 'moderate', 'compact_rhs', VALUES)}
SOURCE = {'database': 'math', 'basis': 1356, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X,Y = sp.symbols('x y')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ident(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, VERSION + ':' + value))


def tex(n):
    return sp.latex(sp.Rational(n))


def polynomial(terms):
    """Ordered coefficients/components; never concatenate numeric factors."""
    out = ''
    for coeff, symbol in terms:
        if coeff == 0:
            continue
        magnitude = tex(abs(coeff))
        term = ('' if abs(coeff) == 1 and symbol else magnitude) + symbol
        if not out:
            out = ('-' if coeff < 0 else '') + term
        else:
            out += (' - ' if coeff < 0 else ' + ') + term
    return out or '0'


def left(a,b):
    return polynomial(((a,'x'),(b,'y')))


def equations(p, template, style='normal'):
    a,b,c,d,e,f = (p[k] for k in 'abcdef')
    if template == 'zero_rhs':
        rows = [polynomial(((b,'y'),(a,'x'),(-c,'')))+' = 0',
                polynomial(((e,'y'),(d,'x'),(-f,'')))+' = 0']
    else:
        rows = [left(a,b)+' = '+tex(c),left(d,e)+' = '+tex(f)]
    # Historical import has a space after initial unary minus in q-211984.
    if style == 'spaced':
        rows = [('- '+row[1:] if row.startswith('-') else row) for row in rows]
    if style == 'compact_rhs':
        rows = [row.replace(' = -',' =-') for row in rows]
    return rows


def prompt(p, template, raw=False, style='normal'):
    system = '; '.join(equations(p,template,style))
    brace = '{' if raw else r'\{'
    return 'Consider the following system of equations:\n\n$'+brace+system+'$\n\nThis system of equations has {{field-1}}.'


def result(p):
    a,b,c,d,e,f = (p[k] for k in 'abcdef')
    det = a*e-b*d
    if det:
        return VALUES[2]
    return VALUES[1] if a*f == d*c and b*f == e*c else VALUES[0]


def multiplier(p):
    """Scale the row with smaller |x coefficient|, always by an integer."""
    a,d = p['a'],p['d']
    return (1,Fraction(-d,a)) if abs(a) <= abs(d) else (2,Fraction(-a,d))


def validate_parameters(level,template,p,raw=False):
    if level not in LEVELS or template not in TEMPLATES:
        raise ValueError('Unsupported level/template')
    if set(p) != set('abcdef') or any(type(v) is not int for v in p.values()):
        raise ValueError('Exactly integer coefficients a,b,c,d,e,f are required')
    a,b,c,d,e,f = (p[k] for k in 'abcdef')
    if not all((a,b,d,e)):
        raise ValueError('Both variables must occur in both linear equations')
    if max(abs(a),abs(b),abs(d),abs(e)) > 12 or max(abs(c),abs(f)) > 30:
        raise ValueError('Coefficient/constant arithmetic ceiling exceeded')
    row,m = multiplier(p)
    if m.denominator != 1:
        raise ValueError('One integer elimination multiplier is required')
    expected = 'zero_rhs' if level == 'hard' else 'standard'
    if template != expected:
        raise ValueError('Authored level requires its documented displayed form')
    if level == 'easy':
        if abs(m) != 1 or max(abs(a),abs(b),abs(d),abs(e)) > 5 or max(abs(c),abs(f)) > 12:
            raise ValueError('Easy: direct elimination, coefficients <=5, constants <=12')
    elif level == 'moderate':
        if not 2 <= abs(m) <= 4 or max(abs(a),abs(b),abs(d),abs(e)) > 10:
            raise ValueError('Moderate: integer multiplier 2..4, coefficients <=10')
    elif not (2 <= abs(m) <= 4 and abs(b) == 1 and 2 <= abs(e) <= 4 and c != 0 and f != 0):
        raise ValueError('Hard: two zero-RHS rearrangements, unit first y coefficient, second y coefficient 2..4, nonzero constants')


def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'


def solution(p,template):
    a,b,c,d,e,f = (p[k] for k in 'abcdef')
    opening = "Let's start by solving the system using elimination."
    out = opening
    if template == 'zero_rhs':
        out += '\n\nFirst, rearrange each equation to put the variable terms on the left and the constant on the right:\n\n'
        out += aligned([left(a,b)+' &= '+tex(c),left(d,e)+' &= '+tex(f)])
    row,m = multiplier(p)
    cancelled = a if row == 2 else d
    out += (f'\n\nNotice that if we multiply the {"first" if row == 1 else "second"} equation by ${tex(m)}$, '
            f'then we will get a ${polynomial(((-cancelled,"x"),))}$ term that can cancel with '
            f'the ${polynomial(((cancelled,"x"),))}$ term in the {"second" if row == 1 else "first"} equation:\n\n')
    annotation = list(equations(p,'standard'))
    annotation[row-1] += r' \mid \mid \cdot ('+tex(m)+')'
    out += '$$\n'+r'\{'+'; '.join(annotation)+'\n$$\n\n'
    transformed = (a*m,b*m,c*m) if row == 1 else (d*m,e*m,f*m)
    u,v,w = transformed
    other = (d,e,f) if row == 1 else (a,b,c)
    oa,ob,oc = other
    sb,sc = v+ob,w+oc
    ordered = [(u,v,w),(oa,ob,oc)] if row == 1 else [(oa,ob,oc),(u,v,w)]
    first_constant,second_constant = ordered[0][2],ordered[1][2]
    rows = [left(ta,tb)+' &= '+tex(tc) for ta,tb,tc in ordered] + [
            polynomial(((sb,'y'),))+' &= ('+tex(first_constant)+(' + ' if second_constant >= 0 else ' - ')+tex(abs(second_constant))+')',
            polynomial(((sb,'y'),))+' &= '+tex(sc)]
    # Preserve the shared canonical/tutoring stages: scale, cancel, uncollected
    # constants, collected statement. A distinct final conclusion follows.
    if sb == 0:
        word = 'true' if sc == 0 else 'false'
        out += f'When we add the two equations, it turns out that both variables cancel, and we obtain a {word} statement:\n\n'
        out += aligned(rows)
        out += f'\n\nThe statement $0={tex(sc)}$ is *always {word}*. Therefore, we conclude that the system has *{result(p)}*.'
    else:
        yy = Fraction(sc,sb)
        out += 'When we add the two equations, the $x$ terms cancel, and we can solve for $y$:\n\n'
        rows.append('y &= '+tex(yy))
        out += aligned(rows)
        xx = Fraction(c-b*yy,a)
        out += '\n\nSubstituting into the first equation gives:\n\n'
        out += aligned([polynomial(((a,'x'),))+' + ('+tex(b)+')('+tex(yy)+') &= '+tex(c),
                        polynomial(((a,'x'),))+' &= '+tex(c-b*yy), 'x &= '+tex(xx)])
        out += '\n\nThe system has *a single solution*, $('+tex(xx)+','+tex(yy)+')$.'
    return out


def mathematical_fingerprint(p, template):
    """Canonical two-line task modulo equation order/scalars and x/y aliases.

    Keep distinct actual line pairs; rank/RREF alone would collapse all unique
    systems to one point. Zero-RHS information rearrangement remains workload.
    """
    def normalize(row):
        pivot = next(v for v in row if v)
        return tuple(str(Fraction(v,pivot)) for v in row)
    a,b,c,d,e,f = (p[k] for k in 'abcdef')
    forms = [sorted([normalize((a,b,c)),normalize((d,e,f))]),
             sorted([normalize((b,a,c)),normalize((e,d,f))])]
    return digest({'line_pair':min(forms),'information_form':template})


def sample(level, rng, branch):
    for _ in range(10000):
        if level == 'easy':
            a=rng.choice([-3,-2,-1,1,2,3]); b=rng.choice([-3,-2,-1,1,2,3])
            d=rng.choice([-1,1])*a; c=rng.randint(-6,6)
        else:
            a=rng.choice([-3,-2,-1,1,2,3]); b=rng.choice([-3,-2,-1,1,2,3]) if level=='moderate' else rng.choice([-1,1])
            d=rng.choice([-4,-3,-2,2,3,4])*a; c=rng.choice([i for i in range(-6,7) if i])
        m=Fraction(d,a)
        if branch == VALUES[2]:
            e=rng.choice([i for i in range(-5,6) if i and i != m*b]); f=rng.randint(-12,12)
        else:
            e=int(m*b); f=int(m*c)
            if branch == VALUES[0]:
                f += rng.choice([-3,-2,-1,1,2,3])
        if level != 'hard' and rng.choice((False,True)):
            a,b,c,d,e,f=d,e,f,a,b,c
        p=dict(zip('abcdef',(a,b,c,d,e,f)))
        template='zero_rhs' if level=='hard' else 'standard'
        try:
            validate_parameters(level,template,p)
        except ValueError:
            continue
        if result(p)==branch:
            return p
    raise ValueError('Bounded whole-instance sampling failed')


def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    if level not in LEVELS or field_type not in (None,'select',':answer-field.type/select'):
        raise ValueError('Supported levels easy/moderate/hard; observed field type select')
    profile=profile or 'counts'
    if profile not in PROFILES:
        raise ValueError('Unknown bank profile')
    raw=profile.startswith('raw_')
    spec=PROFILES[profile]
    if raw:
        family,authored_level,style,values=spec
        if level!=authored_level or template not in (None,family):
            raise ValueError('Replay profile requires its declared authored level/template')
        template=family
    else:
        template=template or ('zero_rhs' if level=='hard' else 'standard')
        style='normal'; values=VALUES
    rng=random.Random(seed)
    # Choose one categorical response branch BEFORE constructing its system.
    branch=rng.choice(VALUES)
    p=dict(parameters) if parameters is not None else sample(level,rng,branch)
    validate_parameters(level,template,p,raw)
    problem=prompt(p,template,raw,style)
    worked=None if raw else solution(p,template)
    content={'version':VERSION,'prompt':problem,'solution':worked,'bank':sorted(values),
             'difficulty':None if raw else level,'presence':{'correct':not raw,'solution':not raw,'difficulty':not raw}}
    content_key=digest(content); qid=ident(content_key); fid=ident(qid+':field-1')
    answers=[{':answer/id':ident(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
    if not raw:
        rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/select',':answer-field/choices':answers}
    q={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    if not raw:
        field[':answer-field/correct']=[':answer/id',ident(fid+':'+result(p))]
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=worked
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,
              'parameters':p,'parameter_fingerprint':mathematical_fingerprint(p,template),
              'content_fingerprint':content_key,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,
              'source_analysis':{**SOURCE,'question_ids':['q-'+profile.removeprefix('raw_')] if raw else (['q-237043'] if template=='zero_rhs' else ['q-211984','q-237046']), 'method_reference_ids':['e-14009','tutorial-17592186075063']},
              'domain':'Two real variables; both equations linear with nonzero x/y coefficients.',
              'authored_extension':not raw,'authored_level':level,
              'inferred_correct_value':result(p),'raw_evidence':raw,'eligible_for_learning':not raw,
              'plot_rating':'none','plot_assets':{},'normalization':'escaped literal system brace' if not raw else None}}


# EASY: direct cancellation; same x magnitude, signed coefficients <=5/constants <=12.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)


# MODERATE: scale one row by integer 2..4, then cancel; standard source form.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)


# HARD: observed y-first zero-RHS form; rearrange BOTH constants then integer elimination.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question']; g=record['generation']; f=q[':question/answer-fields'][0]
    lines=['## '+g['authored_level']+(' — raw incomplete evidence' if g['raw_evidence'] else ' — authored completion'),'',q[':question/problem'],'']
    lines.extend('- '+a[':answer/value'] for a in f[':answer-field/choices'])
    if ':answer-field/correct' in f:
        lines.extend(['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),'',q[':question/worked-solution']])
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all')
    ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('markdown','json'),default='markdown')
    ap.add_argument('--template',choices=TEMPLATES); ap.add_argument('--profile',choices=PROFILES)
    ap.add_argument('--field-type',choices=('select',))
    args=ap.parse_args()
    if args.count<1: ap.error('Positive count required')
    try:
        records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    except ValueError as exc: ap.error(str(exc))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

if __name__=='__main__': main()
