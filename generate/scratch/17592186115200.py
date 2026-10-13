#!/usr/bin/env python3
"""One common-base rewrite, then a linear equation (math basis 1356).

All observed prose/row layouts and seven complete banks replay parametrically.
Opaque historical distractors are evidence-only profiles, not teaching recipes.
Normal output uses complete authored method-derived banks. Raw profiles preserve
missing difficulty, solution, fields and correct references. No DB access/writes.
See the adjacent evidence directory for original presence and repair denominators.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, platform
from pathlib import Path
import sympy as sp

KP_ID=17592186115200
KP_UUID='9c6b30e7-fba6-597c-8306-27d707bfc244'
TITLE='Solving Exponential Equations Containing Different Bases by Rewriting One Exponent'
VERSION='one-exponent-1.0'
EVIDENCE=Path(__file__).with_suffix('')
OPEN='To solve this equation, we need both exponential terms to have a common base.'
# Family refers to which ORIGINAL side has the perfect power, not a second rewrite.
TEMPLATES={'easy_right':'easy','easy_right_collect':'easy','easy_left':'easy',
 'moderate_right':'moderate','moderate_two_shifts':'moderate','hard_right':'hard','hard_left':'hard'}
CASES={
 'q-26817':('moderate_two_shifts',dict(base=2,n=4,a=1,c=-1,b=1,d=1,var='x')),
 'q-66877':('moderate_right',dict(base=12,n=2,a=1,c=-4,b=3,d=0,var='h')),
 'q-110539':('hard_left',dict(base=3,n=4,a=2,c=0,b=1,d=-1,var='a')),
 'q-66864':('easy_left',dict(base=3,n=2,a=1,c=-5,b=1,d=0,var='x')),
 'q-100449':('hard_right',dict(base=8,n=2,a=5,c=-12,b=1,d=4,var='a')),
 'q-110537':('moderate_right',dict(base=4,n=3,a=1,c=-1,b=2,d=0,var='k')),
 'q-3103':('hard_right',dict(base=5,n=2,a=2,c=-5,b=1,d=1,var='a')),
 'q-66863':('easy_right',dict(base=4,n=2,a=1,c=4,b=1,d=0,var='x')),
 'q-66872':('easy_right_collect',dict(base=5,n=3,a=1,c=-10,b=1,d=0,var='m'))}
RAW={q[':question/math-academy-id']:q for q in json.loads((EVIDENCE/'source.json').read_text())['record'][':knowledge-point/questions']}
BANK_PROFILES={s:dict(template=t,origin='observed',evidence_only=True,eligible_for_learning=False) for s,(t,p) in CASES.items()}
BANK_PROFILES['authored-method']=dict(origin='authored',evidence_only=False,eligible_for_learning=True)

def tex(z): return sp.latex(sp.Rational(z)).replace(' - ', '-').replace(' + ', '+').replace('- ', '-')
def linear(a,c,v):
    s=('' if a==1 else '-' if a==-1 else str(a))+v if a else ''
    return s+('+' if c>0 and s else '')+(str(c) if c else '') or '0'
def power(b,e): return '{'+str(b)+'}^{'+e+'}'
def frac(e): return r'\frac{1}{'+e+'}'
def aligned(rows): return '$$\n'+r'\begin{aligned}'+' \\\\ '.join(l+' & ='+r for l,r in rows)+r'\end{aligned}'+'\n$$'
def exact(p,t):
    n,a,c,b,d=(p[k] for k in ('n','a','c','b','d'))
    left=t.endswith('left'); hard=t.startswith('hard')
    A=n*a if left else a; C=n*c if left else c
    B=b if left else n*b; D=d if left else n*d
    if hard:B,D=-B,-D
    return sp.Rational(D-C,A-B),A,C,B,D

def validate_parameters(t,p,raw=False):
    if set(p)!=set(('base','n','a','c','b','d','var')):raise ValueError('exact parameter keys required')
    if any(type(p[k]) is not int for k in ('base','n','a','c','b','d')):raise ValueError('integer parameters required')
    if p['var'] not in ('x','m','h','k','a'):raise ValueError('unsupported variable')
    base,n,a,c,b,d=(p[k] for k in ('base','n','a','c','b','d'))
    if not (base in (2,3,4,5,6,7,8,9,10,12) and 2<=n<=4 and base**n<=1296 and 1<=a<=5 and 1<=b<=5 and abs(c)<=12 and abs(d)<=6):raise ValueError('finite arithmetic domain')
    if t.startswith('easy') and not(a==b==1 and d==0 and c!=0):raise ValueError('easy: unit slopes and one nonzero shift')
    if t=='moderate_right' and not(a==1 and 2<=b<=5 and d==0 and c!=0):raise ValueError('moderate: nonunit rewritten slope and one shift')
    if t=='moderate_two_shifts' and not(a==b==1 and c!=0 and d!=0):raise ValueError('moderate shifted: two nonzero shifts')
    if t=='hard_right' and not(2<=a<=5 and b==1 and c<0 and d>0):raise ValueError('hard right: two shifts, reciprocal, nonunit slope')
    if t=='hard_left' and not(2<=a<=5 and b==1 and c==0 and d<0):raise ValueError('hard left: rewrite product and negate shifted exponent')
    z,A,C,B,D=exact(p,t)
    if A==B or z==0:raise ValueError('unique nonzero solution required')

def historical_bank(s,p,t):
    """Complete observed scalar patterns. Interpretation deliberately unresolved.

    These component expressions are replay-only generalizations, not recovered
    source error intent. They use exponent coefficients/shifts; no payload lookup.
    """
    n,a,c,b,d=(sp.Integer(p[k]) for k in ('n','a','c','b','d'))
    z,A,C,B,D=exact(p,t); N=D-C; H=A-B
    if s=='q-26817':return [z,(-c-d)/(n-1)+sp.Rational(1,n-1),-n/(n-2),-c,(c-n*d-2)/(n-1)]
    if s=='q-66877':return [sp.Rational(n*b-1,c),-n*b+1,c, z,sp.Rational(n,c-(n*b)) * 2]
    if s=='q-100449':return [(a+n)/d,1/(a+n),-d/a,z,-1/d]
    if s=='q-110537':return [z,-c/(n*b+a),c/b,-(n*b+a),n*b-a]
    if s=='q-3103':return [-z,z,sp.Integer(0),(a+n+N)/(a+n),-(a+n+N)/N]
    if s=='q-66863':return [sp.Integer(0),c-1,sp.Integer(1),z,n]
    if s=='q-66872':return [n*c/2,-c,c/2+1,n,z]
    return []

def authored_bank(p,t):
    """Five COMPLETE operation-derived answers; reject whole bank on collisions."""
    z,A,C,B,D=exact(p,t); n,a,c,b,d=(p[k] for k in ('n','a','c','b','d'))
    if t.startswith('hard'):
        # Forget reciprocal sign, negate only variable term, omit n, reverse
        # sign while moving constants. Every wrong value solves its error equation.
        left=t.endswith('left')
        wrong1=sp.Rational((-D)-C,A-(-B))
        wrong2=sp.Rational(-D-C,A-B)
        wrong3=sp.Rational(-d-c,a+b)
        vals=([z,wrong1,wrong3,sp.Rational(-d,n+a+b),1/z] if left else [z,wrong1,wrong2,wrong3,-z])
        labels=(['correct','omit_reciprocal_negative','omit_inner_power','add_inner_power_to_slope','reverse_division'] if left else ['correct','omit_reciprocal_negative','negate_only_variable_term','omit_inner_power','reverse_constant_transposition'])
    else:
        # Neglect power rule; fail to scale constant (left) / multiply slope
        # twice (right); reverse transposition; divide by sum instead of difference.
        left=t.endswith('left')
        omit=sp.Rational(d-c,a-b) if a!=b else (sp.Rational(-n*n*c,n*n*a-b) if left else sp.Integer(n-c))
        second=sp.Rational(d-c,n*a-b) if left else sp.Rational(n*d-c,a-n*n*b)
        vals=[z,omit,second,-z,sp.Rational(D-C,A+B)]
        labels=['correct','omit_power_rule' if a!=b else 'apply_power_rule_twice' if left else 'replace_scaled_exponent_by_inner_power','omit_constant_scaling' if left else 'multiply_slope_twice_keep_shift_once' if d else 'apply_power_rule_twice','reverse_constant_transposition','add_slopes_instead_of_subtract']
    if any(not s.is_Rational or not s.is_finite for s in map(sp.sympify,vals)) or len(set(vals))!=5:raise ValueError('whole authored bank collision or undefined operation')
    return vals,labels

def render(t,p,source=None):
    base,n,a,c,b,d,v=(p[k] for k in ('base','n','a','c','b','d','var'))
    left=t.endswith('left'); hard=t.startswith('hard'); E=linear(a,c,v); F=linear(b,d,v)
    L=power(base**n if left else base,E); R=power(base if left else base**n,F)
    if hard:R=frac(R)
    eq=L+'='+R
    if source in ('q-26817','q-66877'):
        # The captured prompt uses unbraced bases and spaces within exponents.
        def old(b,e):return str(b)+'^{'+e.replace('+',' + ').replace('-',' - ')+'}'
        eq=old(base,E)+' = '+old(base**n,F)
        prompt=f'Find the value of ${v}$ that satisfies the equation ${eq}$.'
    elif source=='q-66864':prompt=f'Find the value of ${v}$ that satisfies the equation ${eq}.$'
    elif t.startswith('hard') or t=='moderate_right':prompt=f'If ${eq}$ then ${v}=$'
    else:prompt=f'Solve for ${v}$ where ${eq}.$'
    big=base**n; side='left' if left else 'right'
    prose_side=('left' if source=='q-110537' else 'right' if source=='q-110539' else side)
    ending='of exponents'
    mid='and then we rewrite' if hard else 'and then rewrite'
    solution=OPEN+f'\n\nTo do this, we write ${big}$ as $'+power(base,str(n)) + f',$ {mid} the {prose_side}-hand side using the power rule {ending}:\n\n'
    nested='{('+power(base,str(n))+')}^{'+(E if left else F)+'}'
    transformed=power(base,(str(n)+'('+E+')') if left and c else linear(n*a,n*c,v)) if left else L
    r_exp=(str(n)+'('+F+')') if d else linear(n*b,0,v)
    transformedR=power(base,F if left else r_exp)
    solution+=aligned([(L,R),(nested if left else L,frac(nested) if hard and not left else nested if not left else R),(transformed,frac(transformedR) if hard else transformedR)])
    z,A,C,B,D=exact(p,t)
    if hard:
        neg=('-' if left else '-'+str(n))+'('+F+')'
        solution+='\n\nNext, we rewrite the right-hand side using a negative exponent: \n\n'+aligned([(transformed,power(base,neg))])
        base_phrase=f'$({base}),$' if left else f'$({base})$,'
        solution+=f'\n\nFinally, since both sides of the equation share the same base {base_phrase} we equate the exponents and solve for ${v}:$\n\n'
        rows=[(linear(A,C,v),neg),(linear(A,C,v),linear(B,D,v)),(linear(A-B,0,v),str(D-C)),(v,tex(z))]
    else:
        comma=',' if t=='moderate_right' else ''
        solution+=f'\n\nNow, since both sides of the equation share the same base $({base}){comma}$'+('' if comma else ',')+f' we equate the exponents and solve for ${v}:$\n\n'
        # Exact source-style row omissions and collection direction are structural.
        if t=='easy_left': rows=[(str(n)+'('+E+')',F),(linear(A,C,v),F),(v,tex(z))]
        elif t=='easy_right':rows=[(E,linear(B,D,v)),(v,tex(z))]
        elif t=='easy_right_collect':rows=[(E,linear(B,D,v)),(linear(A-B,0,v),str(D-C)),(v,tex(z))]
        else:rows=[(E,linear(B,D,v)),(str(C-D),linear(B-A,0,v)),(v,tex(z))]
    solution+=aligned(rows)
    return prompt,solution

def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def assemble(level,seed,t,p,profile,field_type):
    raw=profile!='authored-method'; source=profile if raw else None
    validate_parameters(t,p,raw)
    prompt,solution=render(t,p,source)
    z,A,C,B,D=exact(p,t)
    vals=historical_bank(profile,p,t) if raw else authored_bank(p,t)[0]
    if vals and (any(not sp.sympify(s).is_Rational or not sp.sympify(s).is_finite for s in vals) or len(set(vals))!=5):raise ValueError('whole observed bank collision or undefined operation')
    q={':question/problem':prompt}
    original=RAW[source] if raw else {}
    if not raw or ':question/worked-solution' in original:q[':question/worked-solution']=solution
    if not raw or ':question/difficulty' in original:q[':question/difficulty']=':question.difficulty/'+level
    fields_present=not raw or ':question/answer-fields' in original
    # Content hash depends only on actual presentation, solution, complete bank,
    # presence and designation. Parameter/seed/profile aliases cannot create IDs.
    designation=(not raw or fields_present and ':answer-field/correct' in original[':question/answer-fields'][0])
    h=fingerprint([VERSION,q,sorted(tex(s) for s in vals) if fields_present else [],designation,tex(z) if designation else None])
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL,h)); fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    if fields_present:
        answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),tex(s))),':answer/type':':answer.type/math',':answer/value':tex(s)} for s in vals]
        f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if designation:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a,s in zip(answers,vals) if s==z)]
        random.Random(seed).shuffle(answers);q[':question/answer-fields']=[f]
    q[':question/id']=qid
    # Task identity ignores choice bank, variable aliases, layout and display base
    # power spelling; distinct common bases remain distinct assessed rewrites.
    task=fingerprint([p['base'],p['n'],t.endswith('left'),t.startswith('hard'),p['a'],p['c'],p['b'],p['d']])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'dependencies':{'python':platform.python_version(),'sympy':sp.__version__},'scope_level':level,'seed':seed,'template':t,'parameters':p,'bank_profile':profile,'bank_origin':'observed' if raw else 'authored','evidence_only':raw,'eligible_for_learning':not raw,'parameter_fingerprint':task,'content_fingerprint':h,'source_analysis':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_id':source},'inferred_answer':tex(z),'plot_rating':'none','domain':'positive integer base > 1; exactly one base is rewritten; nonzero unique rational root','distractor_recipes':[] if raw else authored_bank(p,t)[1]}}

def sample(t,rng):
    p=dict(base=rng.choice([2,3,4,5,6,7,8,9,10,12]),n=rng.randint(2,4),a=1,c=rng.choice([i for i in range(-12,13) if i]),b=1,d=0,var=rng.choice(['x','m','h','k','a']))
    if t=='moderate_right':p['b']=rng.randint(2,5)
    if t=='moderate_two_shifts':p['d']=rng.choice([i for i in range(-6,7) if i])
    if t=='hard_right':p.update(a=rng.randint(2,5),c=-rng.randint(1,12),d=rng.randint(1,6))
    if t=='hard_left':p.update(a=rng.randint(2,5),c=0,d=-rng.randint(1,6))
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio'):raise ValueError('only observed radio and authored radio fields supported')
    profile=profile or 'authored-method'
    if profile not in BANK_PROFILES:raise ValueError('unknown profile')
    if profile!='authored-method':
        pt=CASES[profile][0]
        if template and template!=pt:raise ValueError('profile template mismatch')
        template=pt
    eligible=[t for t,l in TEMPLATES.items() if l==level]
    if template and template not in eligible:raise ValueError('template difficulty mismatch')
    rng=random.Random(seed);t=template or rng.choice([t for t in eligible if t!='moderate_two_shifts'])
    if parameters is not None:return assemble(level,seed,t,dict(parameters),profile,field_type)
    # Historical evidence profile has a parameterized default anchor, not payload replay.
    if profile!='authored-method':return assemble(level,seed,t,dict(CASES[profile][1]),profile,field_type)
    for _ in range(2000):
        p=sample(t,rng)
        try:return assemble(level,seed,t,p,profile,field_type)
        except ValueError:pass
    raise ValueError('finite domain exhausted without eligible complete bank')

# EASY: one shift, unit original slopes; n=2..4, |shift|<=12. Both sides' rewrite
# orientations vary without adding another skill. Collection layout is source-derived.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: a nonunit original rewritten slope (2..5), one shift, same linear solve.
# Two-shift template is observed unrated, assigned moderate explicitly in evidence.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: reciprocal-to-negative-exponent step, distribution and linear collection.
# Original nonunit slopes 2..5 and small shifts preserve observed arithmetic demands.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q,g=r['question'],r['generation']
    actual=q.get(':question/difficulty')
    difficulty=actual.split('/')[-1].title() if actual else 'Unrated (original difficulty attribute absent)'
    if g['evidence_only']:
        source=g['source_analysis']['source_id']
        origin='Raw original-parameter replay' if g['parameters']==CASES[source][1] else 'Generated evidence variant'
    else:origin='Generated authored learning variant'
    lines=[f"### {difficulty} — {origin}",f"Template: `{g['template']}`; profile: `{g['bank_profile']}`; authored scope: `{g['scope_level']}`.",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$')
        if ':answer-field/correct' in f:lines.append('Correct ref: '+str(f[':answer-field/correct']))
        else:lines.append('Correct designation absent in original; independently inferred value $'+g['inferred_answer']+'$ is metadata only.')
    if ':question/answer-fields' not in q:lines.append('Answer fields absent in original; independently inferred value $'+g['inferred_answer']+'$ is metadata only.')
    lines.append(q.get(':question/worked-solution','Worked solution absent in original.'))
    return '\n\n'.join(lines)

def main():
    pa=argparse.ArgumentParser(description=__doc__);pa.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');pa.add_argument('--seed',type=int,default=0);pa.add_argument('--count',type=int,default=1);pa.add_argument('--format',choices=['markdown','json'],default='markdown');pa.add_argument('--template',choices=list(TEMPLATES));pa.add_argument('--profile',choices=list(BANK_PROFILES));pa.add_argument('--field-type',choices=['radio']);args=pa.parse_args()
    if args.count<1:pa.error('positive count required')
    levels=list(('easy','moderate','hard')) if args.difficulty=='all' else [args.difficulty]
    rr=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(rr,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rr))
if __name__=='__main__':main()
