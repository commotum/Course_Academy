#!/usr/bin/env python3
"""Local basis2275 vector-norm draft. Raw evidence profiles never enter sampling.
All levels assess exactly two components: square, add, take the positive root.
See private classification/extraction for source provenance and arithmetic bands.
"""
import argparse, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
@lru_cache(maxsize=20000)
def simple(x):return sp.simplify(x)
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE/'source.json').read_text())
KP_ID=17592186059714
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='vector-norm-draft-2.0.0'
SUPPORTED_LEVELS=('easy','moderate','hard')
ROWS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES=tuple(ROWS)
CALCULATORS={r[':question/math-academy-id']:r[':question/requires-calculator'] for k,r in json.loads((HERE/'calculator-requirements.json').read_text())['records'] if k==KP_ID and ':question/math-academy-id' in r and ':question/requires-calculator' in r}
ANCHORS={'q-1325':(4,-1),'q-18046':(-12,3),'q-18047':(5,9),'q-18048':(-4,8)}
RAW_BANKS={'q-1325':(25,9,17,5,7),'q-18046':(171,152,135,153,157)}
BANKS={'norm-stages':('positive root of sum of squares','omit outer square root','sum of absolute components','omit both squares','subtract squared components'),
       'omit-component':('positive root of sum of squares','omit outer square root','omit second squared component','omit first squared component','sum of absolute components')}

def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(x): return sp.latex(simple(x))
def number(x):
    # API accepts exact SymPy-compatible rational/radical strings, not floats.
    if isinstance(x,float) or isinstance(x,bool): raise ValueError('Use exact integer/rational/radical values')
    z=sp.sympify(x)
    if z.free_symbols or z.is_real is not True: raise ValueError('Components must be exact real scalars')
    if z.has(sp.Float): raise ValueError('Use exact values')
    return z

def validate_parameters(level,x,y):
    """Identical guards for explicit calls and random candidates; bands disjoint."""
    if not x or not y or x*x==y*y: raise ValueError('Nonzero unequal component magnitudes required by complete bank')
    if level=='easy':
        if not all(z.is_Integer and 1<=abs(z)<=12 for z in (x,y)): raise ValueError('Easy: nonzero integers with absolute value <=12')
    elif level=='moderate':
        if not all(z.is_Rational and not z.is_Integer and 2<=z.q<=5 and 1<=abs(z.p)<=15 for z in (x,y)): raise ValueError('Moderate: both reduced noninteger rationals; denominator2..5, numerator magnitude1..15')
        if x.q==y.q: raise ValueError('Moderate requires unequal reduced denominators')
    elif level=='hard':
        def decomposition(z):
            if z.is_Rational or not (z*z).is_Rational: raise ValueError('Hard requires radical components with rational squares')
            c,d=z.as_coeff_Mul(); rad=d**2
            if rad not in (2,3,5,6,7) or not c.is_Rational or not (1<=abs(c.p)<=9 and 2<=c.q<=5): raise ValueError('Hard: c sqrt(d)/q, reduced |c numerator|1..9, denominator2..5, d in2,3,5,6,7')
            return c,rad
        a,b=decomposition(x),decomposition(y)
        if a[0].q==b[0].q or a[1]==b[1]: raise ValueError('Hard needs unequal denominators and radicands')
    else: raise ValueError('Unknown difficulty')

def sample(level,rng):
    # Easy section: observed integer workload, including signs and nonsquare roots.
    if level=='easy': return tuple(sp.Integer(rng.choice((-1,1))*rng.randint(1,12)) for _ in range(2))
    # Moderate section: authored rational arithmetic; same two squares and sum.
    if level=='moderate': return tuple(sp.Rational(rng.choice((-1,1))*rng.randint(1,15),rng.randint(2,5)) for _ in range(2))
    # Hard section: authored rational-radical arithmetic; no extra vector operation.
    if level=='hard': return tuple(sp.Rational(rng.choice((-1,1))*rng.randint(1,9),rng.randint(2,5))*sp.sqrt(rng.choice((2,3,5,6,7))) for _ in range(2))
    raise ValueError('Unknown difficulty')

def prompt(mid,x,y):
    original=ROWS[mid][':question/problem']
    if (x,y)==tuple(map(sp.Integer,ANCHORS[mid])): return original
    return re.sub(r'⟨[^⟩]*⟩', lambda m:'⟨'+tex(x)+','+tex(y)+'⟩',original,count=1)

def factor(n):
    # sqrt(n)=r*sqrt(d), n rational. Preserve explicit square-factor stage.
    root=sp.sqrt(n); c,z=root.as_coeff_Mul(); d=simple(z*z)
    return simple(c*c), d

def solution(mid,x,y):
    """Source operative masks preserved, including q18048 factorization row."""
    x2,y2=simple(x*x),simple(y*y); n=x2+y2; root=sp.sqrt(n)
    a,b=tex(x),tex(y); aa,bb=tex(x2),tex(y2)
    if mid=='q-18047':
        # Exact original spaces, punctuation and four-row chain.
        return ('Using the formula, we have \n\n$$\n'+r'\begin{aligned}|\,a\,| & =\sqrt{{a}_{x}^{2}+{a}_{y}^{2}} \\  & =\sqrt{('+a+r')^{2}+('+b+r')^{2}} \\  & =\sqrt{'+aa+'+'+bb+r'} \\  & =\sqrt{'+tex(n)+r'}.\end{aligned}'+'\n$$')
    if mid=='q-18048':
        f,d=factor(n)
        return ('Using the formula, we have\n\n$$\n'+r'\begin{aligned}|\,a\,| & =\sqrt{{a}_{x}^{2}+{a}_{y}^{2}} \\  & =\sqrt{('+a+r')^{2}+('+b+r')^{2}} \\  & =\sqrt{'+aa+'+'+bb+r'} \\  & =\sqrt{'+tex(n)+r'} \\  & =\sqrt{'+tex(f)+r'\cdot '+tex(d)+r'} \\  & ='+tex(root).replace(' \\sqrt',r'\sqrt')+r'.\end{aligned}'+'\n$$')
    var='v' if mid=='q-1325' else 'a'
    steps=[rf'\mid {var} \mid &= \sqrt{{{var}_{{x}}^{{2}} + {var}_{{y}}^{{2}}}}',rf'&= \sqrt{{({a})^{{2}} + ({b})^{{2}}}}',rf'&= \sqrt{{{aa} + {bb}}}',rf'&= \sqrt{{{tex(n)}}}', '&= '+tex(root)]
    return 'Using the formula, we have\n\n$$\n\\begin{aligned}\n'+' \\\\\n'.join(steps)+'\n\\end{aligned}\n$$'

def bank(x,y,profile):
    n=simple(x*x+y*y); correct=sp.sqrt(n) # Always derive correct first.
    if profile=='norm-stages': vals=[correct,n,abs(x)+abs(y),sp.sqrt(abs(x)+abs(y)),sp.sqrt(abs(x*x-y*y))]
    elif profile=='omit-component': vals=[correct,n,abs(x),abs(y),abs(x)+abs(y)]
    else: raise ValueError('Unknown normal bank')
    vals=[simple(v) for v in vals]
    if any(v.is_real is not True or v<0 for v in vals): raise ValueError('Invalid complete bank')
    if any(simple(a*a-b*b)==0 for i,a in enumerate(vals) for b in vals[i+1:]): raise ValueError('Whole-bank equivalent-option rejection')
    return vals

def record(question,level,mid,profile,x,y,seed,raw,recipes):
    # Task fingerprint intentionally ignores sign/order aliases: squaring these
    # operands performs the same arithmetic; equal final norms alone are insufficient.
    fp=digest({'operation':'sqrt of sum of two squared components','squared_operands':sorted([sp.srepr(x*x),sp.srepr(y*y)])})
    content={k:v for k,v in question.items() if k!=':question/id'}
    # Before identity construction choices have no IDs: order is canonical here.
    ident=digest({'version':VERSION,'content':content})
    qid=uid('question:'+ident); question[':question/id']=qid
    for f in question.get(':question/answer-fields',[]):
        fid=uid(qid+':field:'+f[':answer-field/key']); f[':answer-field/id']=fid
        for a in f.get(':answer-field/choices',[]): a[':answer/id']=uid(fid+':value:'+a[':answer/value'])
        if ':answer-field/correct' in f:
            correct_value=f.pop(':answer-field/correct'); selected=[a for a in f[':answer-field/choices'] if a[':answer/value']==correct_value]
            f[':answer-field/correct']=[':answer/id',selected[0][':answer/id']]
        random.Random(seed).shuffle(f.get(':answer-field/choices',[]))
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':mid,'profile':profile,'parameters':{'x':str(x),'y':str(y)},'parameter_fingerprint':fp,'content_hash':ident,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_references':[mid,'e-4297'],'recipes':recipes,'evidence_only':raw,'eligible_for_learning':not raw,'authored':not raw,'answer_contract':'exact nonnegative norm; no source approximate/rounding rule','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def raw_replay(level,mid,parameters,seed):
    if mid not in ROWS: raise ValueError('Unknown source template')
    params=parameters or {}; original=ROWS[mid]
    if mid in RAW_BANKS:
        if set(params)-{'scale'}: raise ValueError('Raw radio profile accepts scale only')
        s=number(params.get('scale',1)); bound=8 if mid=='q-1325' else 3
        if not s.is_Integer or not 1<=s<=bound: raise ValueError('Raw scale outside original baseline bounds')
        x,y=[sp.Integer(z)*s for z in ANCHORS[mid]]
    else:
        if set(params)-{'x','y'}: raise ValueError('Unknown parameter')
        x,y=[number(params.get(k,v)) for k,v in zip(('x','y'),ANCHORS[mid])]
        validate_parameters('easy',x,y)
    q={':question/problem':prompt(mid,x,y),':question/math-academy-id':mid}
    if mid in CALCULATORS:q[':question/requires-calculator']=CALCULATORS[mid]
    if ':question/difficulty' in original: q[':question/difficulty']=original[':question/difficulty'][':db/ident']
    if ':question/worked-solution' in original: q[':question/worked-solution']=solution(mid,x,y)
    if ':question/answer-fields' in original:
        answers=[]
        for n,a in zip(RAW_BANKS[mid],original[':question/answer-fields'][0][':answer-field/choices']):
            val=a[':answer/value'] if s==1 else tex(s*sp.sqrt(n))
            out={':answer/type':a[':answer/type'][':db/ident'],':answer/value':val}
            if ':answer/feedback' in a: out[':answer/feedback']=a[':answer/feedback']
            answers.append(out)
        of=original[':question/answer-fields'][0]
        f={':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers}
        # Correct references are absent in both raw banks; preserve absence.
        q[':question/answer-fields']=[f]
    return record(q,level,mid,'raw-source',x,y,seed,True,['parameterized observed homogeneity pattern; opaque intent; no default learning bank'])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio normal fields supported')
    rng=random.Random(seed); mid=template or rng.choice(TEMPLATES)
    if mid not in TEMPLATES: raise ValueError('Unknown template')
    if profile=='raw-source':
        if level!='easy':raise ValueError('Original raw evidence has no moderate/hard assignment')
        return raw_replay(level,mid,parameters,seed)
    selected=profile or rng.choice(tuple(BANKS)) # Complete bank chosen before parameters.
    if selected not in BANKS: raise ValueError('Unknown profile')
    for attempt in range(10000):
        if parameters is not None:
            if set(parameters)!={'x','y'}: raise ValueError('Normal parameters require exactly x and y')
            x,y=map(number,(parameters['x'],parameters['y']))
        else:x,y=sample(level,rng)
        try:
            validate_parameters(level,x,y); values=bank(x,y,selected)
            if mid=='q-18048' and factor(x*x+y*y)[0]==1: raise ValueError('Factorization family requires nontrivial square factor')
        except ValueError:
            if parameters is not None:raise
            continue
        q={':question/problem':prompt(mid,x,y),':question/worked-solution':solution(mid,x,y),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values],':answer-field/correct':tex(values[0])}]}
        if mid in CALCULATORS:q[':question/requires-calculator']=CALCULATORS[mid]
        return record(q,level,mid,selected,x,y,seed,False,list(BANKS[selected]))
    raise RuntimeError('Could not construct a complete eligible bank')

def generate_easy(seed=0,**kwargs):
    """Observed integer square/sum/root workload, magnitudes1..12."""
    return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
    """Authored two reduced fraction squares; distinct denominators2..5."""
    return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
    """Authored two radical fraction squares; distinct denominators/radicands."""
    return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question']; parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):parts += ['\n'.join('- $'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[]))]
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=2);p.add_argument('--format',choices=('json','markdown'),default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    if a.count<0:p.error('Nonnegative count required')
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)
    try:rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    except ValueError as e:p.error(str(e))
    print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
