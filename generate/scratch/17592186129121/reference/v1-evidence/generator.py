#!/usr/bin/env python3
"""Amplitude extraction only. Frozen basis 1356; local drafts; no EDB writes.

Raw profiles are public parameterized evidence recipes, never default learning.
Normal families are chosen before sampling a complete method-derived bank.
Easy: positive external coefficient or implicit one. Moderate: negative external
coefficient or a single quotient. Hard: authored whole-numerator external scale,
with two coefficient operations and no reduction to an integer or unit scale.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186129121
KP_UUID='7f8fa2b3-ccaa-5390-89fa-03e338cf8690'
TITLE='Determining the Amplitude of a Transformed Sinusoidal Function'
VERSION='1.0.0'
PRIVATE=Path(__file__).with_suffix('')
SOURCE=json.loads((PRIVATE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}

class SampleRejected(ValueError): pass

def rational(v):
    if isinstance(v,(float,bool)): raise ValueError('Use exact rational numbers, not floats or bools')
    z=sp.sympify(v,locals={'pi':sp.pi})
    if not z.is_number or not z.is_real: raise ValueError('Real exact numeric component required')
    return z

def tex(z):
    z=sp.sympify(z)
    if z.is_Rational:
        n,d=int(z.p),int(z.q)
        return str(n) if d==1 else ('-' if n<0 else '')+r'\frac{'+str(abs(n))+'}{'+str(d)+'}'
    return sp.latex(z)

def signed(z): return ('+' if z>=0 else '-')+tex(abs(z))
def coeff(z): return '' if z==1 else '-' if z==-1 else tex(z)
def canonical(p): return {k:str(rational(v)) if k!='trig' else v for k,v in sorted(p.items())}
def decode(p): return {k:rational(v) if k!='trig' else v for k,v in p.items()}
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def argument(p):
    b,c=p['B'],p['C']
    return coeff(b)+'x'+(signed(c) if c else '')

def trigterm(p, spelling=None, bare=False):
    t=spelling or '\\'+p['trig']
    return t+'x' if bare else t+'('+argument(p)+')'

# Nine presentation masks; numerical variation uses complete expression slots.
# All source-bank operations retain their interpretation uncertainty in metadata.
SPECS={
 'q-43277':dict(level='easy',kind='legacy_direct',trig='cos',spelling=r'\cos ',params=dict(A=5,B=1,C=0,D=0),bank=['1/abs(A)','2*abs(A)','abs(A)/2','abs(A)','A**2']),
 'q-43278':dict(level='moderate',kind='legacy_quotient',trig='cos',spelling=r'\cos ',params=dict(N=-2,D=3,Q=13,B=1,C=0),bank=['D','Q','abs(N/Q)','abs(N)','N/Q']),
 'q-117568':dict(level='easy',kind='direct',trig='cos',spelling=r'\operatorname{cos}',params=dict(A='3/2',B=2,C=-1,D=0),bank=None),
 'q-117575':dict(level='moderate',kind='direct_pi',trig='sin',spelling=r'\operatorname{sin}',params=dict(A=-5,B=3,C='-pi',D=-3),bank=None),
 'q-117569':dict(level='easy',kind='unit_divx',trig='sin',spelling='\\operatorname{sin}⁡',params=dict(A=1,B='1/3',C='1/4',D=0),bank=['1/B','1/C','B','abs(A)','C']),
 'q-117570':dict(level='easy',kind='direct',trig='cos',spelling='\\operatorname{cos}⁡',params=dict(A=4,B=2,C=3,D=0),bank=['1/B','B','abs(A)*B','abs(A)','1/abs(A)']),
 'q-117574':dict(level='moderate',kind='direct',trig='cos',spelling='\\operatorname{cos}⁡',params=dict(A=-7,B=3,C=1,D=0),bank=['1/abs(A)','B','1/B','abs(A)','C']),
 'q-117576':dict(level='moderate',kind='quotient',trig='sin',spelling='\\operatorname{sin}⁡',params=dict(N=-9,D=3,Q=5,B=1,C=0),bank=['1/Q','D/Q','abs(N/Q)','D','abs(N)']),
 'q-53428':dict(level='easy',kind='unit',trig='cos',spelling='\\operatorname{cos}⁡',params=dict(A=1,B='1/2',C='1/3',D=0),bank=['1/B','B','1/(B*C)','C','abs(A)']),
}
TEMPLATES={'positive':'easy','unit':'easy','negative':'moderate','quotient':'moderate','factored':'hard'}
NORMAL_BANKS={
 'positive':{'coefficient_parameters':['abs(A)','1/abs(A)','B','1/B','abs(A)*B']},
 'unit':{'implicit_parameters':['abs(A)','B','1/B','abs(C)','1/abs(C)']},
 'negative':{'absolute_coefficient':['abs(A)','A','B','1/B','abs(C)']},
 'quotient':{'numerator_division':['abs(N/Q)','abs(N)','abs(D/Q)','abs(D)','1/Q'],
             'signed_division':['abs(N/Q)','abs(N)','D','Q','N/Q']},
 'factored':{'whole_numerator_scale':['abs(P*N/Q)','abs(N/Q)','abs(P*N)','abs(P*D/Q)','abs(P/Q)']},
}
BANK_PROFILES={f'raw:{s}':{'template':s,'level':v['level'],'eligible_for_learning':False,'origin':'observed-evidence','recipes':v['bank']} for s,v in SPECS.items()}
for name,banks in NORMAL_BANKS.items():
    for bank,recipes in banks.items(): BANK_PROFILES[bank]={'template':name,'level':TEMPLATES[name],'eligible_for_learning':True,'origin':'authored-method-derived','recipes':recipes}


def amplitude(p): return abs(p['A']) if 'A' in p else abs(p.get('P',1)*p['N']/p['Q'])
def evaluate_recipes(recipes,p): return [sp.simplify(sp.sympify(r,locals={**p,'abs':sp.Abs})) for r in recipes]

def raw_expression(s,p):
    kind=s['kind']; t=s['spelling']
    if kind=='legacy_direct': return coeff(p['A'])+t+'x'
    if kind=='legacy_quotient':
        return r'\frac{'+tex(p['D'])+' '+('-' if p['N']<0 else '+')+' '+tex(abs(p['N']))+t+'x}{'+tex(p['Q'])+'}'
    if kind=='quotient': return r'\frac{'+tex(p['D'])+signed(p['N'])+t+'x}{'+tex(p['Q'])+'}'
    arg=argument(p)
    if kind=='unit_divx':
        arg=r'\frac{x}{'+str(1/p['B'])+'}'+signed(p['C'])
    if kind=='direct_pi' and p['C'].has(sp.pi):
        arg=coeff(p['B'])+'x'+signed(p['C'])+' '
    return coeff(p['A'])+t+'('+arg+')'+(signed(p['D']) if p['D'] else '')

def base_solution(trigspell,A, extra_space=False, now=False, quotient=False):
    head=('Now, given' if now else 'Given')+' a function in the form $f(x)=A'+trigspell+'(Bx+C)+D,$ the amplitude is $|A|.$'+(' ' if extra_space else '')
    if quotient:
        return head+'\n\nIn our case, we have that $A='+tex(A)+'.$ Therefore, the amplitude is $|A|=|'+tex(A)+'|='+tex(abs(A))+'.$'
    return head+'\n\nSince $A='+tex(A)+',$ we have that the amplitude is $|A|=|'+tex(A)+'|='+tex(abs(A))+'.$'

def raw_solution(s,p):
    if s['kind']=='quotient':
        a=p['N']/p['Q']; d=p['D']/p['Q']
        rewritten=tex(a)+r'\cdot '+s['spelling']+'x'+signed(d)
        return 'First, notice that we can rewrite the function as follows:\n\n$$\nf(x)='+raw_expression(s,p)+'='+rewritten+'\n$$\n\n'+base_solution(s['spelling'],a,now=True,quotient=True)
    return base_solution(s['spelling'],p['A'],extra_space=s['kind'] in ('unit','unit_divx'))


def check_raw(s,p):
    expected=set(s['params'])|{'trig'}
    if set(p)!=expected or p['trig']!=s['trig']: raise ValueError('Raw mask parameter keys/trig must match its documented family')
    if p['B']==0: raise ValueError('A nonconstant sinusoid requires nonzero B')
    if s['kind'] in ('legacy_direct','legacy_quotient','quotient') and (p['B']!=1 or p['C']!=0): raise ValueError('Bare-x source mask requires B=1,C=0')
    if s['kind']=='legacy_direct' and p['D']!=0: raise ValueError('Legacy direct mask has no vertical shift')
    if 'Q' in p and p['Q']==0: raise ValueError('Zero denominator')
    if 'A' in p and p['A']==0 or 'N' in p and p['N']==0: raise ValueError('Nonzero sinusoidal coefficient required')
    if s['kind']=='unit_divx' and (p['B']<=0 or not (1/p['B']).is_Integer): raise ValueError('Unit-divx mask requires reciprocal positive integer B')


def check_normal(name,p):
    expected={'trig','B','C','D'}|({'A'} if name in ('positive','unit','negative') else {'N','Q'})|({'P','E'} if name=='factored' else set())
    if set(p)!=expected or p['trig'] not in ('sin','cos'): raise ValueError('Exact parameter keys and sin/cos required')
    if not p['B'].is_Rational or not p['C'].is_Rational and not (p['C']/sp.pi).is_Rational: raise ValueError('Familiar rational or pi argument components required')
    if abs(p['C'])>3*sp.pi: raise ValueError('Horizontal shift arithmetic bound')
    if name!='unit':
        c=p['C'] if p['C'].is_Rational else p['C']/sp.pi
        if abs(c.p)>(6 if p['C'].is_Rational else 3) or c.q>6: raise ValueError('Familiar reduced horizontal offset workload required')
    if name=='unit':
        if p['A']!=1 or p['D']!=0 or p['B']<=0 or p['C']<=0 or not (1/p['B']).is_Integer or not (1/p['C']).is_Integer or not (2<=1/p['B']<=9 and 2<=1/p['C']<=9): raise ValueError('Unit family: implicit A=1, no D, reciprocal argument components 1/2..1/9')
    elif name in ('positive','negative'):
        a=p['A']; limit=12 if name=='positive' else 13
        if not a.is_Rational or not (1<=abs(a.p)<=limit and 1<=a.q<=6) or not (2<=p['B']<=6 and p['B'].is_Integer): raise ValueError('Reduced coefficient numerator/denominator or horizontal coefficient outside workload')
        if (name=='positive' and (a<=0 or p['D']!=0)) or (name=='negative' and (a>=0 or not p['D'].is_Integer or abs(p['D'])>6)): raise ValueError('Coefficient sign/vertical shift outside level')
    else:
        n,q,d=p['N'],p['Q'],p['D']
        if not all(z.is_Integer for z in (n,q,d)) or not (2<=abs(n)<=13 and 3<=q<=13 and 1<=d<=9) or math.gcd(abs(int(n)),int(q))!=1 or (n/q).q==1: raise ValueError('Primitive noninteger numerator quotient workload required')
        if name=='quotient' and (n>=0 or p['B']!=1 or p['C']!=0): raise ValueError('Moderate single-division mask requires negative N, B=1,C=0')
        if name=='factored':
            P,E=p['P'],p['E']
            if not P.is_Integer or not (2<=abs(P)<=4) or not E.is_Integer or not (1<=abs(E)<=6) or not (1<=p['B']<=4 and p['B'].is_Integer) or p['C']==0 or math.gcd(abs(int(P*n)),int(q))!=1 or (P*n/q).q==1 or abs(P*n)>36: raise ValueError('Hard requires two nonunit unreduced coefficient operations, familiar argument, two nonzero offsets, product <=36')


def sample(name,rng):
    t=rng.choice(['sin','cos'])
    if name=='unit': return decode(dict(trig=t,A=1,B=f'1/{rng.randint(2,9)}',C=f'1/{rng.randint(2,9)}',D=0))
    if name in ('positive','negative'):
        a=sp.Rational(rng.randint(1,12),rng.randint(1,6))*(1 if name=='positive' else -1)
        return decode(dict(trig=t,A=str(a),B=rng.randint(2,6),C=str(rng.choice([sp.Rational(1,3),sp.Rational(1,2),1,2,3,-1,-2,sp.pi,-sp.pi/2])),D=0 if name=='positive' else rng.randint(-6,6)))
    p=dict(trig=t,N=rng.randint(-13,-2),Q=rng.randint(3,13),D=rng.randint(1,9),B=1,C=0)
    if name=='factored': p.update(N=rng.choice(list(range(-13,-1))+list(range(2,14))),P=rng.choice([-4,-3,-2,2,3,4]),E=rng.choice([-6,-3,-1,1,3,6]),B=rng.randint(1,4),C=str(rng.choice([1,-1,sp.Rational(1,2),-sp.pi/3,sp.pi/2])))
    return decode(p)


def normal_expression(name,p):
    term=trigterm(p)
    if name in ('positive','unit','negative'): return coeff(p['A'])+term+(signed(p['D']) if p['D'] else '')
    numerator=tex(p['D'])+signed(p['N'])+term
    fraction=r'\frac{'+numerator+'}{'+tex(p['Q'])+'}'
    return fraction if name=='quotient' else tex(p['P'])+r'\left('+fraction+r'\right)'+signed(p['E'])


def normal_solution(name,p,expr):
    a=p['A'] if 'A' in p else p.get('P',1)*p['N']/p['Q']
    trigspell='\\'+p['trig']
    if name in ('positive','unit','negative'): return base_solution(trigspell,a)
    shift=p.get('P',1)*p['D']/p['Q']+p.get('E',0)
    term=trigterm(p)
    prefix='First, notice that we can rewrite the function as follows:\n\n$$\n'
    if name=='quotient':
        prefix+='f(x)='+expr+'='+tex(a)+r'\cdot '+term+signed(shift)
    else:
        # Keep the multiplication and division stages visible before collecting.
        product=tex(p['P'])+r'\cdot ('+tex(p['N'])+')'
        constant_product=tex(p['P'])+r'\cdot '+tex(p['D'])
        prefix+=r'\begin{aligned}f(x)&='+expr+r'\\&=\frac{'+product+'}{'+tex(p['Q'])+r'}\cdot '+term+r'+\frac{'+constant_product+'}{'+tex(p['Q'])+'}'+signed(p['E'])+r'\\&='+tex(a)+r'\cdot '+term+signed(shift)+r'\end{aligned}'
    return prefix+'\n$$\n\n'+base_solution(trigspell,a,now=True,quotient=True)


def task_signature(name,p):
    # Argument parameters, offsets, sin/cos aliases and banks are incidental to
    # amplitude extraction. Retain the presented coefficient operation tree.
    if name in ('positive','unit','negative'): return {'demand':'implicit' if name=='unit' else 'direct','A':str(p['A'])}
    return {'demand':'single-division' if name=='quotient' else 'multiply-divide','N':str(p['N']),'Q':str(p['Q']),**({'P':str(p['P'])} if 'P' in p else {})}


def assemble(level,seed,name,p,profile,raw=False):
    spec=SPECS[name] if raw else None
    expr=raw_expression(spec,p) if raw else normal_expression(name,p)
    prompt=('What is the amplitude of the function $f(x) = '+expr+'$?' if raw and spec['kind'].startswith('legacy') else 'What is the amplitude of the function $f(x)='+expr+'?$')
    original=QUESTIONS[name] if raw else None
    q={':question/problem':prompt}
    if not raw or ':question/difficulty' in original: q[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/worked-solution' in original: q[':question/worked-solution']=raw_solution(spec,p) if raw else normal_solution(name,p,expr)
    recipes=BANK_PROFILES[profile]['recipes']
    values=evaluate_recipes(recipes,p) if recipes else []
    correct=amplitude(p)
    if values and (len(values)!=5 or len(set(values))!=5 or values.count(correct)!=1): raise SampleRejected('Reject complete bank: duplicate/ambiguous or missing correct mathematical value')
    displays=[tex(v) for v in values]
    payload={'version':VERSION,'difficulty':q.get(':question/difficulty'),'problem':prompt,'solution':q.get(':question/worked-solution'),'banks':sorted(displays),'field_present':not raw or ':question/answer-fields' in original,'correct_present':not raw or bool(original.get(':question/answer-fields',[{}])[0].get(':answer-field/correct'))}
    content_key=digest(payload);qid=uuid.uuid5(uuid.UUID(KP_UUID),content_key)
    q[':question/id']=str(qid)
    if raw: q[':question/math-academy-id']=name
    if not raw or ':question/answer-fields' in original:
        fid=uuid.uuid5(qid,'selection'); choices=[]
        for v,value in zip(values,displays):
            aid=str(uuid.uuid5(fid,'math:'+value));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
            if v==correct: correct_id=aid
        random.Random(seed).shuffle(choices)
        field={':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if not raw or ':answer-field/correct' in original[':question/answer-fields'][0]: field[':answer-field/correct']=[':answer/id',correct_id]
        q[':question/answer-fields']=[field]
    signature=task_signature(('quotient' if 'Q' in p else 'unit' if spec and spec['kind'].startswith('unit') else 'negative' if 'A' in p and p['A']<0 else 'positive') if raw else name,p)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'bank_profile':profile,'parameters':canonical(p),'parameter_fingerprint':digest(signature),'mathematical_task':signature,'content_fingerprint':content_key,'source_analysis':PROVENANCE,'source_ids':[name] if raw else [s for s,v in SPECS.items() if v['level']==level],'authored_extension':not raw,'origin':BANK_PROFILES[profile]['origin'],'eligible_for_learning':not raw,'evidence_only':raw,'raw_attribute_presence_preserved':raw,'inferred_amplitude':str(correct) if raw else None,'recipes':recipes,'plot_rating':'none','plot_assets':{},'domain':'x real, B nonzero; rational amplitude coefficient','scope':'amplitude only; no period, range, or midline calculation'}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio'): raise ValueError('Only observed radio shape is supported for normal questions')
    if profile and profile not in BANK_PROFILES: raise ValueError('Unknown profile')
    if profile and profile.startswith('raw:'):
        source_id=profile[4:];spec=SPECS[source_id]
        if level!=spec['level'] or template not in (None,source_id): raise ValueError('Raw source family/assigned evidence level mismatch')
        p=decode(parameters if parameters is not None else {**spec['params'],'trig':spec['trig']});check_raw(spec,p)
        return assemble(level,seed,source_id,p,profile,True)
    rng=random.Random(seed)
    eligible=[n for n,l in TEMPLATES.items() if l==level]
    if profile:
        implied=BANK_PROFILES[profile]['template']
        if template not in (None,implied): raise ValueError('Profile-template mismatch')
        template=implied
    name=template or rng.choice(eligible)
    if name not in eligible: raise ValueError('Template outside requested difficulty')
    # Fixed explicit inputs select the same default profile under any seed.
    profile=profile or (random.Random(json.dumps(canonical(decode(parameters)),sort_keys=True)).choice(list(NORMAL_BANKS[name])) if parameters is not None else rng.choice(list(NORMAL_BANKS[name])))
    for _ in range(256):
        p=decode(parameters) if parameters is not None else sample(name,rng)
        try:
            check_normal(name,p)
            return assemble(level,seed,name,p,profile)
        except ValueError:
            if parameters is not None: raise
    raise SampleRejected('No complete eligible bank within bounded sampling')

# EASY — positive coefficient extraction, including an implicit unit.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Positive reduced rationals with numerator <=12/denominator <=6, or A=1."""
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — absolute value of a negative coefficient, or one primitive division.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Negative A, or (D+N trig x)/Q with coprime N,Q and noninteger N/Q."""
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored multiply-and-divide coefficient extraction, no extra topic.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """P(D+N trig(Bx+C))/Q+E; all defining operations remain nonunit."""
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q,g=record['question'],record['generation']
    lines=[f"### {'Raw evidence' if g['evidence_only'] else 'Generated authored variant'} — {g['template']}",f"Profile `{g['bank_profile']}`; eligible for learning: **{g['eligible_for_learning']}**.",'',q[':question/problem'],'']
    for field in q.get(':question/answer-fields',[]):
        for letter,a in zip('ABCDE',field[':answer-field/choices']): lines.append(f"- {letter}. ${a[':answer/value']}$")
        c=field.get(':answer-field/correct');lines+=['', '**Correct:** '+(next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==c[1]) if c else 'absent in raw source; mathematical value '+g['inferred_amplitude'])]
    if ':question/answer-fields' not in q: lines+=['**Fields:** absent in raw source.']
    lines+=['','**Worked solution**','',q.get(':question/worked-solution','Absent in raw source.')]
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    args=parser.parse_args()
    if args.count<1 or args.difficulty=='all' and (args.template or args.profile): parser.error('Positive count and specific difficulty for template/profile')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
