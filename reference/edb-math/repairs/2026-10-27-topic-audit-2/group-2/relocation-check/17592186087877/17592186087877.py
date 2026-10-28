#!/usr/bin/env python3
"""Integrating-factor transformations, math basis 1356; local review only.

All eight captured practice banks have parameterized replay recipes. The original
bank profile is explicitly raw evidence, including three pairs of equivalent
wrong equations and one malformed differential operator. Default banks are
complete authored repairs. Normal output ends with a product derivative, never
a general solution or an initial-value computation. Source prose and ordered
math stages are retained through complete-component masks, with documented
notation normalization and one sign correction. No DB or renderer dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
from math_format import checked_math_content, normalize_prose, normalize_tex

KP_ID=17592186087877
KP_UUID='9c49e068-198f-59ab-8835-7018b02d7d0c'
TITLE='Transforming First-Order Linear ODEs Using Integrating Factors'
VERSION='integrating-factor-transform-v4'
ROOT=Path(__file__).with_suffix('')
X=s.Symbol('x', positive=True)
Y,YP=s.symbols('y yp')
D=r'\frac{dy}{dx}'
DD=r'\frac{d}{dx}'
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CURRENT=json.loads((ROOT/'source-current.json').read_text())
QUESTIONS['q-335274']=next(q for q in CURRENT['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')=='q-335274')
# Separate templates preserve standard/nonstandard layouts and source stage counts.
TEMPLATES={
 'constant_cos':('easy','q-17540'),
 'constant_exp':('easy',None),
 'linear_exp':('moderate','q-8546'),
 'scaled_constant_power':('easy','q-17533'),
 'scaled_reciprocal_cos':('moderate','q-17539'),
 'signed_constant_power':('easy','q-335278'),
 'reciprocal_exp':('moderate','q-79818'),
 'scaled_reciprocal_rhs':('moderate','q-79819'),
 'linear_sin':('moderate','q-335274'),
 'collected_mixed':('hard',None),
}
CASES=[
 ('q-17540','constant_cos',dict(a='1',b=1)),
 ('q-8546','linear_exp',dict(a=1,b=1,c=1)),
 ('q-17533','scaled_constant_power',dict(a='1',n=1)),
 ('q-17539','scaled_reciprocal_cos',dict(k=1,b=1)),
 ('q-335278','signed_constant_power',dict(a='-1/2',n=3)),
 ('q-79818','reciprocal_exp',dict(k=1,b=1)),
 ('q-79819','scaled_reciprocal_rhs',dict(k=2,c=1)),
 ('q-335274','linear_sin',dict(a=1,b=1)),
]

def tex(e):
    return s.latex(s.sympify(e)).replace(r'\log',r'\ln')
def E(e):return r'e^{'+tex(e)+'}'
def group(e):return r'\left('+tex(e)+r'\right)'
def mul(a,b):return group(a)+r'\cdot '+group(b)
def equation(A,B,R):
    lead='' if A==1 else group(A)+r'\cdot '
    sign='-' if B.could_extract_minus_sign() else '+'
    c=-B if sign=='-' else B
    term='y' if c==1 else group(c)+r'\cdot y'
    return lead+D+sign+term+'='+tex(R)
def product_derivative(f,q):
    return DD+r'\left(y\cdot '+group(f)+r'\right)='+mul(f,q)

def math(t,p):
    if t in ('constant_cos','constant_exp','scaled_constant_power','signed_constant_power'):
        P=s.Rational(p['a']); H=P*X; I=s.exp(H)
        Q=s.cos(p['b']*X) if t=='constant_cos' else p['b']*s.exp(p['c']*X) if t=='constant_exp' else X**p['n']
        A=X if t=='scaled_constant_power' else s.Integer(1)
    elif t=='linear_exp':
        P=2*p['a']*X; H=p['a']*X**2; I=s.exp(H)
        Q=2*p['b']*X*s.exp(-p['c']*X**2); A=s.Integer(1)
    elif t=='linear_sin':
        P=2*p['a']*X; H=p['a']*X**2; I=s.exp(H)
        Q=s.sin(p['b']*X); A=s.Integer(1)
    elif t=='collected_mixed':
        P=s.Integer(p['k'])/X+p['a']; H=p['k']*s.log(X)+p['a']*X; I=X**p['k']*s.exp(p['a']*X)
        Q=p['b']*s.cos(X)/X; A=s.Integer(p['scale'])*X
    else:
        P=s.Integer(p['k'])/X; H=p['k']*s.log(X); I=X**p['k']
        Q={'scaled_reciprocal_cos':lambda:s.cos(p['b']*X),'reciprocal_exp':lambda:s.exp(p['b']*X),'scaled_reciprocal_rhs':lambda:s.Integer(p['c'])/X}[t]()
        A=X**2 if t=='scaled_reciprocal_cos' else X if t=='scaled_reciprocal_rhs' else s.Integer(1)
    return A,s.simplify(A*P),s.simplify(A*Q),P,Q,H,I

def validate_parameters(t,p):
    required={'a','b','c'} if t=='constant_exp' else set(dict(CASES[[c[1] for c in CASES].index(t)][2])) if t!='collected_mixed' else {'a','b','k','scale'}
    if set(p)!=required:raise ValueError(f'{t} requires exactly {sorted(required)}')
    p=dict(p)
    for k in required:
        v=s.Rational(str(p[k]))
        if k=='a' and t in ('constant_cos','constant_exp','scaled_constant_power','signed_constant_power'):
            if not v or abs(v)>4 or v.q>3:raise ValueError('constant a must be nonzero, |a|<=4, denominator<=3')
            p[k]=str(v)
        else:
            if v.q!=1:raise ValueError(f'{k} must be integer')
            p[k]=int(v)
    if 'n' in p and not 1<=p['n']<=4:raise ValueError('power n must be 1..4')
    if 'k' in p and (not p['k'] or abs(p['k'])>4):raise ValueError('reciprocal k must be nonzero, |k|<=4')
    if 'b' in p and (not p['b'] or abs(p['b'])>4):raise ValueError('nonzero |b|<=4')
    if 'c' in p and (not p['c'] or abs(p['c'])>4):raise ValueError('nonzero |c|<=4')
    if t in ('linear_exp','linear_sin') and (not p['a'] or abs(p['a'])>3):raise ValueError('linear a must be nonzero, |a|<=3')
    if t=='collected_mixed':
        if p['scale'] not in (1,2) or not p['a'] or abs(p['a'])>3 or abs(p['k'])>2:raise ValueError('hard requires scale=1/2, nonzero |a|<=3, nonzero |k|<=2')
    return p

def sample(t,r):
    signed=lambda n:r.choice([i for i in range(-n,n+1) if i])
    if t=='constant_exp':return dict(a=str(signed(4)),b=signed(4),c=signed(4))
    if t=='constant_cos':return dict(a=str(signed(4)),b=r.randint(1,4))
    if t in ('scaled_constant_power','signed_constant_power'):return dict(a=str(r.choice([s.Rational(a,d) for a in range(-4,5) if a for d in (1,2,3)])),n=r.randint(1,4))
    if t=='linear_exp':return dict(a=signed(3),b=signed(4),c=signed(4))
    if t=='linear_sin':return dict(a=signed(3),b=r.randint(1,4))
    if t in ('scaled_reciprocal_cos','reciprocal_exp'):return dict(k=signed(4),b=r.randint(1,4))
    if t=='scaled_reciprocal_rhs':return dict(k=signed(4),c=signed(4))
    return dict(a=signed(3),b=signed(3),k=signed(2),scale=r.choice((1,2)))

# All raw banks are selected whole, not synthesized from a pooled distractor list.
# Factors below generalize complete source components; scale-only pairs are
# intentionally retained in raw replay and never eligible for normal output.
EASY_COEFFICIENTS=tuple(sorted({s.Rational(n,d) for d in (1,2,3) for n in range(-4*d,4*d+1) if n}))

def factors(t,p,profile,bank_coefficients=None):
    A,B,R,P,Q,H,I=math(t,p)
    if profile=='authored':
        if bank_coefficients is None:raise ValueError('authored output requires a complete coefficient bank')
        if TEMPLATES[t][0]=='easy':
            return [(s.exp(c*X),False) for c in bank_coefficients]
        if t in ('scaled_reciprocal_cos','reciprocal_exp','scaled_reciprocal_rhs'):
            return [(X**c,False) for c in bank_coefficients]
        if t=='collected_mixed':
            return [(X**k*s.exp(a*X),False) for a,k in bank_coefficients]
        return [(s.exp(c*X**2),False) for c in bank_coefficients]
    if t=='linear_sin' and profile=='observed_raw':
        return [(s.log(abs(2*p['a'])*X),False),(X**2,False),(s.exp(2*p['a']*X),False),(2*p['a']*X,False),(I,False)]
    if profile!='observed_raw':raise ValueError('profile must be authored or observed_raw')
    return {
      'constant_cos':lambda:[(X,False),(s.log(X),False),(X**2,True),(1/X,False),(I,False)],
      'linear_exp':lambda:[(s.exp(p['a']*X),False),(P,False),(X**2,False),(I,False),(X,False)],
      'scaled_constant_power':lambda:[(2*P*X,False),(I,False),(2*P,False),(s.exp(2*H),False),(P*X,False)],
      'signed_constant_power':lambda:[(I,False),(1/I,False),(H,False),(P,False),(-1/P,False)],
      'scaled_reciprocal_cos':lambda:[(s.exp(p['k']*X),False),(X**(2*p['k']),False),(I,False),(s.exp(-p['k']*X),False),(s.log(X),False)],
      'reciprocal_exp':lambda:[(X**(2*p['k']),False),(s.exp(p['k']*X),False),(s.exp(-p['k']*X),False),(I,False),(s.log(X),False)],
      'scaled_reciprocal_rhs':lambda:[(s.log(X),False),(I,False),(s.exp(p['k']*X/2),False),(X**(p['k']/s.Integer(2)),False),(s.Integer(p['k']),False)],
    }[t]()

# This normalized product-equation renderer preserves the complete raw factors
# and RHS multiplication, including q17540's erroneous differential denominator.
def choice(f,Q,malformed=False):
    d=r'\frac{d}{dx^{2}}' if malformed else DD
    return d+r'\left(y\cdot '+group(f)+r'\right)='+mul(f,Q)

def solution_blocks(t,p):
    A,B,R,P,Q,H,I=math(t,p)
    reciprocal=t in ('scaled_reciprocal_cos','reciprocal_exp','scaled_reciprocal_rhs')
    blocks=[]
    if A!=1:blocks.append(equation(s.Integer(1),P,Q)+'.')
    blocks.append(D+'+P(x)y=Q(x)')
    rows=[r'I(x) & =e^{\int P(x)\,dx}',r' & =e^{\int '+group(P)+r'\,dx}']
    if t=='collected_mixed':
        rows.append(r' & =e^{'+tex(H)+'}')
        rows.append(r' & ='+tex(I))
    elif reciprocal:
        rows.append(r' & =e^{'+tex(H)+'}')
        if abs(p['k'])!=1:rows.append(r' & =e^{\ln '+group(I)+'}')
        rows.append(r' & ='+tex(I))
    else:rows.append(r' & ='+tex(I))
    blocks.append(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
    # The factor and P are explicitly defined above. Abbreviate them here so
    # every multiplication row stays visible at the actual learning-card width.
    left=r'I(x)\cdot \left('+equation(s.Integer(1),P,Q).split('=')[0]+r'\right)'
    distribution=r'I(x)'+D+r'+P(x)I(x)y'
    rhs=r'I(x)\cdot '+group(Q)
    collected=t in ('scaled_reciprocal_cos','reciprocal_exp','linear_sin','collected_mixed','linear_exp','constant_exp')
    distributed_rhs=tex(s.simplify(I*Q)) if collected else mul(I,Q)
    blocks.append(r'\begin{aligned}'+left+' & ='+rhs+r' \\ '+distribution+' & ='+distributed_rhs+r'\end{aligned}')
    final=DD+r'\left(y\cdot '+group(I)+r'\right) & ='+distributed_rhs
    blocks.append(r'\begin{aligned}'+final+('.' if t=='scaled_reciprocal_cos' else '')+r'\end{aligned}')
    return blocks

# Replace entire math components, never short text across the surrounding prose.
MATH_SPAN=re.compile(r'\$\$[\s\S]*?\$\$|\$(?!\$)[^$]*?\$')
def render_observed(t,p):
    source_id=TEMPLATES[t][1]; q=QUESTIONS[source_id]
    A,B,R,P,Q,H,I=math(t,p)
    problem=q[':question/problem']
    spans=list(MATH_SPAN.finditer(problem)); target=next(m for m in spans if D in m.group() or r'\frac{\text{d}y}' in m.group())
    # The target is the actual supplied ODE, not the generic answer request.
    supplied=equation(A,B,R)
    if t in ('scaled_reciprocal_cos','reciprocal_exp'):supplied+=r',\,x>0'
    marker='$$' if target.group().startswith('$$') else '$'
    problem=problem[:target.start()]+marker+('\n' if marker=='$$' else '')+supplied+('\n' if marker=='$$' else '')+marker+problem[target.end():]
    raw_sol=q.get(':question/worked-solution')
    if raw_sol:
        blocks=iter(solution_blocks(t,p))
        def replacement(m):
            a=m.group()
            if a.startswith('$$'):return '$$\n'+next(blocks)+'\n$$'
            inner=a[1:-1]
            if inner.startswith('P(x)='):return '$P(x)='+tex(P)+'$'
            if inner.startswith('Q(x)='):return '$Q(x)='+tex(Q)+'.$'
            if inner.startswith('I(x)='):return '$I(x)='+tex(I)+'$'
            return a
        sol=MATH_SPAN.sub(replacement,raw_sol)
        try:next(blocks);raise AssertionError('unconsumed source stage')
        except StopIteration:pass
    else:
        sol=generic_solution(t,p)
    return problem,sol

def generic_solution(t,p):
    A,B,R,P,Q,H,I=math(t,p)
    bs=solution_blocks(t,p); start=0
    parts=[]
    if A!=1:parts+=['First, we write the equation in standard form. This gives','$$\n'+bs[0]+'\n$$'];start=1
    parts+=['This equation is in the standard form','$$\n'+bs[start]+'\n$$',
       'with $P(x)='+tex(P)+'$ and $Q(x)='+tex(Q)+'.$ We proceed to find an integrating factor $I(x)$ using the definition:',
       '$$\n'+bs[start+1]+'\n$$',
       'Now, we multiply our differential equation through by $I(x)='+tex(I)+'$ as follows:',
       '$$\n'+bs[start+2]+'\n$$',
       r'Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$',
       '$$\n'+bs[start+3]+'\n$$']
    return '\n\n'.join(parts)

def residual(f,Q,malformed=False):
    derivative=f*YP+s.diff(f,X)*Y
    return s.expand((derivative/(2*X) if malformed else derivative)-f*Q)
def equivalent(a,b):
    # Full equations modulo any nonzero multiplier function (same solution set
    # on the given domain); factor choices differing by constants are duplicates.
    if a==0 or b==0:return a==b
    ca,cb=a.coeff(YP),b.coeff(YP)
    if not ca or not cb:return False
    return all(s.cancel(a.coeff(z)/ca-b.coeff(z)/cb)==0 for z in (Y,)) and s.cancel(a.subs({Y:0,YP:0})/ca-b.subs({Y:0,YP:0})/cb)==0

def identity(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,value))
@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_coefficients=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio is supported')
    r=random.Random(seed)
    eligible=[t for t,(l,_) in TEMPLATES.items() if l==level]
    if template is None:template=r.choice(eligible)
    if template not in eligible:raise ValueError('template outside level')
    profile=profile or 'authored'
    if template=='collected_mixed' and profile!='authored':raise ValueError('hard is authored')
    explicit=parameters is not None
    easy_bank=None
    chosen_a=None
    chosen_pair=None
    reciprocal=template in ('scaled_reciprocal_cos','reciprocal_exp','scaled_reciprocal_rhs')
    role='k' if reciprocal else 'a'
    eligible_coefficients=EASY_COEFFICIENTS if level=='easy' else tuple(s.Integer(i) for i in range(-4 if reciprocal else -3,5 if reciprocal else 4) if i)
    if profile=='authored' and level=='hard':
        eligible_pairs=[(a,k) for a in (-3,-2,-1,1,2,3) for k in (-2,-1,1,2)]
        # Avoid singleton-sign bank clues in either component, before assigning
        # any member the target role. All 24 target pairs remain eligible.
        def balanced(bank):
            return all(sum(pair[j]>0 for pair in bank) in (2,3) for j in (0,1))
        if bank_coefficients is not None:
            easy_bank=tuple(tuple(int(s.Integer(c)) for c in pair) for pair in bank_coefficients)
            if len(easy_bank)!=5 or len(set(easy_bank))!=5 or any(pair not in eligible_pairs for pair in easy_bank) or not balanced(easy_bank):raise ValueError('hard bank requires five distinct eligible (a,k) pairs and 2/3 sign groups in both components')
        else:
            for bank_attempt in range(100):
                if explicit:
                    target=(int(parameters['a']),int(parameters['k']))
                    easy_bank=tuple([target]+r.sample([pair for pair in eligible_pairs if pair!=target],4))
                else:easy_bank=tuple(r.sample(eligible_pairs,5))
                if balanced(easy_bank):break
            else:raise ValueError('no balanced complete hard bank')
        if explicit and (int(parameters['a']),int(parameters['k'])) not in easy_bank:raise ValueError('hard bank must include target pair')
        chosen_pair=r.choice(easy_bank) if not explicit else None
    elif profile=='authored':
        if bank_coefficients is not None:
            easy_bank=tuple(s.Rational(str(c)) for c in bank_coefficients)
            if len(easy_bank)!=5 or len(set(easy_bank))!=5 or any(c not in eligible_coefficients for c in easy_bank):raise ValueError('bank must contain five distinct eligible coefficients')
        elif explicit:
            a=s.Rational(str(parameters[role]))
            easy_bank=tuple([a]+r.sample([c for c in eligible_coefficients if c!=a],4))
        else:
            easy_bank=tuple(r.sample(eligible_coefficients,5))
        if explicit and s.Rational(str(parameters[role])) not in easy_bank:raise ValueError('bank must include the target coefficient')
        chosen_a=str(r.choice(easy_bank)) if not explicit else None
    elif bank_coefficients is not None:raise ValueError('coefficient banks apply only to authored output')
    for attempt in range(100):
        supplied=parameters if explicit else sample(template,r)
        if chosen_a is not None:supplied[role]=chosen_a
        if chosen_pair is not None:supplied['a'],supplied['k']=chosen_pair
        p=validate_parameters(template,supplied)
        A,B,R,P,Q,H,I=math(template,p)
        fs=factors(template,p,profile,easy_bank)
        values=[choice(f,Q,m) for f,m in fs]
        rs=[residual(f,Q,m) for f,m in fs]
        good=[i for i,z in enumerate(rs) if equivalent(z,residual(I,Q))]
        duplicates=[(i,j) for i in range(5) for j in range(i) if equivalent(rs[i],rs[j])]
        if len(good)!=1 or (duplicates and profile!='observed_raw'):
            if explicit:raise ValueError('whole bank invalid/ambiguous')
            continue
        break
    else:raise ValueError('no valid complete instance')
    if TEMPLATES[template][1]:prompt,sol=render_observed(template,p)
    else:
        prompt='Consider the following first-order linear ODE for the function $y=y(x):$\n\n$$\n'+equation(A,B,R)+'\n$$\n\n'+r'Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.'
        sol=generic_solution(template,p)
    if template=='collected_mixed':
        lhs=equation(A,s.Integer(p['scale']*p['k']),s.Integer(0)).split('=')[0]
        right=tex(-p['scale']*p['a']*X*Y+p['scale']*p['b']*s.cos(X))
        prompt='Consider the following first-order linear ODE for the function $y=y(x)$:\n\n$$\n'+lhs+'='+right+'\n$$\n\n'+r'Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x)$, where $I(x)$ is an integrating factor.'
        collection='Collect the $y$-terms on the left:\n\n$$\n'+equation(A,B,R)+'\n$$\n\n'
        sol=collection+sol
    # Positive half-line for all families using powers/logs, or division by x.
    # q79819 omitted its necessary nonzero domain: a minimal presentation repair.
    if A.has(X) and template not in ('scaled_reciprocal_cos',):prompt+='\n\nAssume $x>0$.'
    if template=='linear_sin' or (template=='constant_cos' and profile=='observed_raw'):prompt+='\n\nAssume $x>0$.'
    domain='x>0' if A.has(X) or template in ('scaled_reciprocal_cos','reciprocal_exp','scaled_reciprocal_rhs') or template=='linear_sin' or (template=='constant_cos' and profile=='observed_raw') else 'x in R'
    prompt=normalize_prose(prompt);sol=normalize_prose(sol)
    values=[normalize_tex(v) for v in values]
    task_data=[s.srepr(s.simplify(P)),s.srepr(s.simplify(Q)),domain]
    fingerprint=hashlib.sha256(json.dumps(task_data).encode()).hexdigest()
    content=json.dumps([VERSION,prompt,sol,sorted(values),domain],ensure_ascii=False)
    qid=identity(content);fid=identity(qid+'/selection')
    answers=[{':answer/id':identity(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[good[0]][':answer/id'];r.shuffle(answers)
    question={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'bank_coefficients':[list(c) if isinstance(c,tuple) else str(c) for c in easy_bank] if easy_bank else None,'seed':seed,'template':template,'parameters':p,'profile':profile,'source':{'database':'math','basis':CURRENT['basis'] if template=='linear_sin' else 1356,'lineage':SOURCE['lineage'],'question_id':'e-21741' if template=='constant_exp' else TEMPLATES[template][1]},'domain':domain,'mathematical_fingerprint':fingerprint,'content_fingerprint':hashlib.sha256(content.encode()).hexdigest(),'origin':'authored hard scope' if level=='hard' else 'observed template; authored bank' if profile=='authored' else 'observed raw bank; notation and supported prose repairs','raw_equivalent_pairs':duplicates,'repairs':['TeX notation normalization','q335278 distributed sign correction'] if template=='signed_constant_power' else ['TeX notation normalization'],'dependencies':{'sympy':s.__version__}}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nWorked solution:\n\n'+q[':question/worked-solution']
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile',choices=['authored']);args=a.parse_args()
    if args.count<1:a.error('--count must be positive')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    rows=[]
    for level in levels:
        seen=set();offset=0
        while len(seen)<args.count:
            if offset>=max(1000,args.count*100):raise ValueError('requested batch exceeds available distinct mathematical tasks')
            row=generate(level,args.seed+offset,template=args.template,profile=args.profile);offset+=1
            fingerprint=row['generation']['mathematical_fingerprint']
            if fingerprint in seen:continue
            seen.add(fingerprint);rows.append(row)
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(row) for row in rows))
if __name__=='__main__':main()
