#!/usr/bin/env python3
"""Seeded, relocatable sum/constant multiple vector differentiation generator.
Mathematical bases and bounded reader adapted from the registered generator.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from math_format import normalize_prose, normalize_tex, validate_generated_record
KP_ID=17592186115390
KP_UUID='49b54258-61d2-549c-94e4-a251f6d2a656'
TITLE='Using the Sum and Constant Multiple Rules for Differentiation'
VERSION='2.0.2'
T=sp.Symbol('t',real=True)
I,J,K=sp.symbols('i j k')
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def balanced(s,start,opening='{',closing='}'):
    assert s[start]==opening,(s,start)
    depth=1
    for n in range(start+1,len(s)):
        if s[n]==opening: depth+=1
        elif s[n]==closing: depth-=1
        if depth==0:return s[start+1:n],n+1
    raise ValueError('Unbalanced component: '+s)

def scalar(raw):
    """Independent bounded TeX reader for every printed source/generated component."""
    s=raw.strip().replace('\\\\,','').replace(r'\,','').replace('⁡','').replace('\u2061','').replace('−','-')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\operatorname','')
    s=s.replace(r'\pi','pi').replace(r'\ln','log').replace('{ln}','log').replace('{log}','log')
    s=s.replace('{sin}','sin').replace('{cos}','cos').replace('{tan}','tan').replace('{sec}','sec')
    for name in ['sin','cos','tan','sec','exp','log']:
        s=s.replace('\\'+name,name)
    deriv=r'\frac{\text{d}}{\text{d}t}'
    if s.startswith(deriv):
        rest=s[len(deriv):].strip()
        return sp.diff(scalar(rest),T)
    while r'\frac' in s:
        n=s.index(r'\frac'); p=n+5
        num,p=balanced(s,p); den,p=balanced(s,p)
        s=s[:n]+'(('+str(scalar(num))+')/('+str(scalar(den))+'))'+s[p:]
    while r'\sqrt' in s:
        n=s.index(r'\sqrt'); inner,end=balanced(s,n+5)
        s=s[:n]+'sqrt('+str(scalar(inner))+')'+s[end:]
    # Exponential bases, including SymPy's e^{...} and source {e}^{...}.
    s=s.replace('{e}','e')
    s=re.sub(r'e\s*\^\s*\{([^{}]+)\}',lambda m:'exp('+str(scalar(m[1]))+')',s)
    s=re.sub(r'(sin|cos|tan|sec)\s*\^\s*\{?(\d+)\}?\s*\{?(\([^()]*\))\}?',r'\1\3^\2',s)
    s=re.sub(r'(sin|cos|tan|sec)\s*\^\s*\{?(\d+)\}?\s*([a-z0-9]+)',r'\1(\3)^\2',s)
    s=re.sub(r'(sin|cos|tan|sec|log)\s*([+-]?\d*t|[+-]?\d+)',r'\1(\2)',s)
    s=s.replace('{','(').replace('}',')')
    s=re.sub(r'(?<=\d)([ijk])\b',r'*\1',s) # 1j must be a basis coefficient, not Python's imaginary literal.
    return parse_expr(s,local_dict={'t':T,'i':I,'j':J,'k':K,'pi':sp.pi,'e':sp.E,
        'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sec':sp.sec,'log':sp.log,'sqrt':sp.sqrt,'exp':sp.exp},transformations=TRANS)

def split_components(raw):
    if raw.startswith('⟨'):return [x.strip() for x in raw[1:-1].replace('\\\\,','').replace(r'\,','').split(',')]
    if raw.startswith(r'[\begin{aligned}'):
        return [x.strip() for x in raw[len(r'[\begin{aligned}'):-len(r'\end{aligned}]')].split(r'\\')]
    raise ValueError(raw)

def vector(raw):
    if raw.startswith(('⟨',r'[\begin{aligned}')):
        return tuple(scalar(c) for c in split_components(raw))
    # Basis vectors in source answer banks and distributed arithmetic.
    z=sp.expand(scalar(raw))
    if sp.simplify(z-z.coeff(I)*I-z.coeff(J)*J-z.coeff(K)*K)!=0:
        raise ValueError('Not a basis-vector expression: '+raw)
    return (z.coeff(I),z.coeff(J),z.coeff(K))

def tex(x):return sp.latex(sp.simplify(x),fold_short_frac=False)
def vtex(v,layout='tuple'):
    if layout=='column':return r'[\begin{aligned}'+r' \\ '.join(tex(x) for x in v)+r'\end{aligned}]'
    if layout=='basis':
        pieces=[]
        for x,b in zip(v,'ijk'):
            if x==0:continue
            z=tex(x); term='('+z+r')\,'+b if sp.sympify(x).is_Add else z+r'\,'+b
            pieces.append(term)
        return '+'.join(pieces).replace('+-','-') or '0'
    return '⟨'+r',\,'.join(tex(x) for x in v)+'⟩'
def scale(v,s):return tuple(sp.simplify(x*y) for x,y in zip(v,s))
def eq(a,b):return all(sp.simplify(x-y)==0 for x,y in zip(a,b))
def total(vs,coeff):return tuple(sp.simplify(sum(c*v[n] for c,v in zip(coeff,vs))) for n in range(3))
def block(s):return '$$\n'+s+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')

def render_basis_expression(raw,scales):
    """Scale full summands without collapsing the source's distributed rows."""
    chunks=[];start=0;depth=0
    for n,c in enumerate(raw):
        if c in '({':depth+=1
        elif c in ')}':depth-=1
        elif c in '+-' and depth==0 and n>start:
            chunks.append(raw[start:n]);start=n
    chunks.append(raw[start:])
    pieces=[]
    for chunk in chunks:
        chunk=chunk.strip();m=re.match(r'([+-]?\d+)\(',chunk)
        if m:
            body,end=balanced(chunk,m.end()-1,'(',')')
            if end==len(chunk):
                pieces.append(m[1]+r'\left('+render_basis_expression(body,scales)+r'\right)');continue
        pieces.append(r'\left('+vtex(scale(vector(chunk),scales),'basis')+r'\right)')
    return '+'.join(pieces).replace('++','+').replace('+-','-')

# Explicit mathematical bases, independently derived from the source prompts.
BASES={
'q-33122':(['f','g'],[1,1],[[3*T-1,6-T,7*T],[T**2,1-T**2,T]],None,'tuple'),
'q-33143':(['h','g'],[3,-2],[[2*T**2,T-3,8+T**3],[T**2+2*T,8,2*T**3]],2,'tuple'),
'q-128137':(['f','g'],[1,-3],[[2*sp.sqrt(T+1),T**3,sp.log(T+1)],[1/(3*(T+1)),sp.sin(T),sp.tan(T)]],0,'tuple'),
'q-128452':(['f','g'],[2,-1],[[8*sp.sqrt(3-T),sp.sin(sp.pi*T),sp.log(-2*T)],[T**2-T,sp.pi*T**2,1-T**2]],-1,'tuple'),
'q-128458':(['f','g'],[2,5],[[2*sp.sqrt(3+T),sp.cos(T-1),sp.Integer(1)],[2*T-3,T**2,(T+1)**2]],1,'column'),
'q-32499':(['g','h'],[2,-1],[[sp.cos(T),3*T-3,-T**2],[sp.sin(T),-T,sp.Integer(4)]],None,'tuple'),
'q-32503':(['f','g','h'],[1,1,1],[[-1,0,1],[-T,0,T],[-T**2,0,T**2]],None,'tuple'),
'q-33123':(['f','g'],[2,3],[[2*sp.sin(T),3*sp.cos(T),-3*sp.cos(T)],[5-sp.sin(T),-1,2*sp.cos(T)]],None,'basis'),
'q-70681':(['f','g'],[1,4],[[sp.sqrt(T),sp.log(T),2],[T,1/T,T**4]],None,'tuple'),
'q-127998':(['f','g'],[1,1],[[1-2*T,T**2,(T-1)**2],[T+1,1-2*T,T**3]],None,'tuple'),
'q-128144':(['f','g'],[1,-2],[[T**2,sp.log(T),sp.exp(T-1)],[2*sp.sqrt(T),T**3,3]],1,'tuple'),
}

# Canonical display deliberately avoids global simplification of operator inputs.
def tex(x):
    return sp.latex(sp.expand_mul(sp.sympify(x)),fold_short_frac=False,ln_notation=True)

def vtex(v,layout='column'):
    if layout=='tuple':
        return r'\langle '+r',\,'.join(tex(x) for x in v)+r'\rangle'
    if layout=='basis':
        return tex(sum(x*b for x,b in zip(v,(I,J,K))))
    return r'\begin{bmatrix}'+r' \\ '.join(tex(x) for x in v)+r'\end{bmatrix}'

SOURCE=json.loads(Path(__file__).with_name('source-banks.json').read_text())
LEVELS={name:(d['level'] or 'moderate') for name,d in SOURCE.items()}
LEVELS.update({'canonical-mixed':'hard','mixed-symbolic':'hard'})
DOMAINS={'q-70681':'t>0','q-128144':'t>0','q-128137':r'-1<t<\frac{\pi}{2}',
         'q-128452':'t<0','q-128458':'t>-3'}

def combine(names,coeff,point='t',prime=False):
    out=''
    for name,c in zip(names,coeff):
        out+=('-' if c<0 else '+' if out else '')+('' if abs(c)==1 else str(abs(c)))
        out+=name+(r'^{\prime}' if prime else '')+'('+str(point)+')'
    return out

def sumvec(vs,coeff):
    return tuple(sp.expand_mul(sum(c*v[j] for c,v in zip(coeff,vs))) for j in range(3))

def instantiate(name,rng,replay=False,parameters=None):
    if name in BASES:
        names,coeff,fs,point,layout=BASES[name]
        fs=[tuple(map(sp.sympify,f)) for f in fs]
        domain=DOMAINS.get(name,r't\in\mathbb R')
        # Correction preserves the derivative but makes the negative point real.
        # The imported ln(2t) remains untouched in source.json.
        if replay:
            p={'scales':[[1,1,1] for f in fs], 'permutation':[0,1,2], 'coefficients':coeff}
        else:
            p=parameters or {'scales':[[rng.choice([-2,-1,1,2]) for _ in range(3)] for f in fs],
                            'permutation':rng.sample(range(3),3),
                            'coefficients':[rng.choice([-3,-2,-1,1,2,3]) for f in fs]}
        fs=[tuple(f[j]*p['scales'][i][j] for j in p['permutation']) for i,f in enumerate(fs)]
        return names,p['coefficients'],fs,point,layout,domain,p
    p=parameters or {'a':rng.choice([1,2]),'b':rng.choice([-2,-1,1,2]),
                    'A':rng.choice([-2,-1,1,2]),'B':rng.choice([-2,-1,1,2]),
                    'h':rng.choice([-3,-2,-1,1,2,3]),'n':rng.choice([2,3]),'u':rng.choice([2,3]),'v':rng.choice([1,2,3]),
                    'permutation':rng.sample(range(3),3)}
    a,b,A,B,h,u,v=(p[k] for k in ['a','b','A','B','h','u','v'])
    if name=='canonical-mixed':
        fs=[(a*T**p['n']+b,-a/(T-h),sp.cos(u*T)),(b*T-a,sp.exp(v*T),sp.cos(u*T))]
        domain='t\\ne '+str(h)
    elif name=='mixed-symbolic':
        fs=[(a*sp.sqrt(T+h),sp.log(T+h),sp.cos(u*T)),(b/(T+h),sp.exp(v*T),sp.sin(u*T))]
        domain='t>'+str(-h)
    else:raise ValueError('Unknown template')
    fs=[tuple(map(sp.sympify,f)) for f in fs]
    fs=[tuple(f[j] for j in p['permutation']) for f in fs]
    return ['f','g'],[A,B],fs,None,'column',domain,p

def learner_diff(x):
    """Direct taught scalar rules; CAS differentiation is reserved for verification.
    In particular, tangent is displayed as secant squared, without requiring a
    trigonometric identity merely because a CAS prefers tan squared plus one.
    """
    x=sp.sympify(x)
    if not x.has(T):return sp.Integer(0)
    if x==T:return sp.Integer(1)
    if x.is_Add:return sum(learner_diff(z) for z in x.args)
    if x.is_Mul:
        c,f=x.as_independent(T,as_Add=False)
        if c!=1:return c*learner_diff(f)
    if x.is_Pow and not x.exp.has(T):return x.exp*x.base**(x.exp-1)*learner_diff(x.base)
    a=x.args[0]
    if x.func==sp.sin:return sp.cos(a)*learner_diff(a)
    if x.func==sp.cos:return -sp.sin(a)*learner_diff(a)
    if x.func==sp.tan:return sp.sec(a)**2*learner_diff(a)
    if x.func==sp.exp:return sp.exp(a)*learner_diff(a)
    if x.func==sp.log:return learner_diff(a)/a
    raise ValueError('Unsupported learner derivative: '+str(x))

def error_bank(fs,ds,coeff,point,rng):
    used=ds if point is None else [tuple(x.subs(T,point) for x in d) for d in ds]
    key=sumvec(used,coeff);candidates=[]
    def add(v,recipe):
        v=tuple(map(sp.expand_mul,v))
        if not eq(v,key) and not any(eq(v,w) for w,_ in candidates):candidates.append((v,recipe))
    for i in range(len(fs)):
        for wrong,label in [(0,'omit contribution'),(1,'drop multiplier'),(-coeff[i],'reverse multiplier')]:
            c=list(coeff);c[i]=wrong;add(sumvec(used,c),f'{label} of function {i+1}')
        wrong=list(used);wrong[i]=fs[i] if point is None else tuple(x.subs(T,point) for x in fs[i])
        add(sumvec(wrong,coeff),f'use function {i+1} instead of its derivative')
        for j in range(3):
            if used[i][j]==0:continue
            for factor,label in [(-1,'omit'),(-2,'reverse')]:
                z=list(key);z[j]+=factor*coeff[i]*used[i][j]
                add(z,f'{label} function {i+1} contribution in coordinate {j+1}')
    if len(candidates)<4:raise ValueError('Insufficient distinct plausible errors')
    chosen=rng.sample(candidates,4)
    return [key]+[v for v,_ in chosen],['correct']+[label for _,label in chosen]

def solution(names,coeff,fs,ds,point,layout):
    target='('+combine(names,coeff)+r')^{\prime}'
    s='Apply the **sum and constant multiple rules**:\n\n'+block(target+'='+combine(names,coeff,prime=True)+'.')
    s+='\n\nDifferentiate each component:\n\n'+aligned([name+r'^{\prime}(t)&='+vtex(d,layout) for name,d in zip(names,ds)])
    if point is not None:
        used=[tuple(sp.expand_mul(x.subs(T,point)) for x in d) for d in ds]
        s+='\n\nNow evaluate the derivatives at $t='+str(point)+'$:\n\n'+aligned([name+r'^{\prime}('+str(point)+')&='+vtex(d,layout) for name,d in zip(names,used)])
    else:used=ds
    s+='\n\nScale every component by its constant multiplier:\n\n'+aligned([
        str(c)+name+r'^{\prime}('+str(point if point is not None else 't')+')&='+vtex(tuple(c*x for x in d),layout)
        for name,c,d in zip(names,coeff,used)])
    result=sumvec(used,coeff)
    s+='\n\nAdd corresponding components and combine like terms:\n\n'+block(target+(r'\big|_{t='+str(point)+'}' if point is not None else '')+'='+vtex(result,layout)+'.')
    if any(x.has(sp.sin,sp.cos,sp.exp) for f in fs for x in f):
        s+='\n\nKeep the displayed inner arguments when applying the scalar derivative rules; any nonunit inner derivative multiplies its component.'
    return s

def generate(level,seed=0,template=None,replay=False,parameters=None):
    rng=random.Random(seed)
    name=template or rng.choice([n for n,l in LEVELS.items() if l==level])
    if LEVELS[name]!=level:raise ValueError('Template/level mismatch')
    names,coeff,fs,point,layout,domain,p=instantiate(name,rng,replay,parameters)
    ds=[tuple(learner_diff(x) for x in f) for f in fs]
    # Long symbolic banks use columns to keep all components visible in the UI.
    if level=='hard' or name=='q-70681':layout='column'
    target='('+combine(names,coeff)+r')^{\prime}'+(r'\big|_{t='+str(point)+'}' if point is not None else '')
    prompt='Find $'+target+'$, where $'+domain+'$ and\n\n'+aligned([n+'(t)&='+vtex(f,layout) for n,f in zip(names,fs)])
    sol=solution(names,coeff,fs,ds,point,layout)
    vals,recipes=error_bank(fs,ds,coeff,point,rng)
    if replay and name in SOURCE and SOURCE[name]['level']:
        # Normalize observed full banks; corrections are documented, not new DB fields.
        def parse_bank(v):
            v=normalize_tex(v)
            if v.startswith(r'\begin{bmatrix}'):
                return tuple(scalar(x) for x in v[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')].split(r'\\'))
            if v.startswith(r'\langle'):
                return tuple(scalar(x) for x in v[len(r'\langle'):-len(r'\rangle')].replace(r'\,','').split(','))
            return vector(v)
        vals=[parse_bank(v) for v in SOURCE[name]['bank']]
        recipes=['observed expression pattern' for _ in vals]
    key=sumvec(ds if point is None else [tuple(x.subs(T,point) for x in d) for d in ds],coeff)
    matches=[i for i,v in enumerate(vals) if eq(v,key)]
    if len(matches)!=1 or any(eq(v,w) for i,v in enumerate(vals) for w in vals[i+1:]):raise ValueError('Nonunique bank')
    prompt=normalize_prose(prompt);sol=normalize_prose(sol)
    bank=[normalize_tex(vtex(v,layout)) for v in vals]
    # Content identities follow normalization, independent of order/seed.
    fp=hashlib.sha256(json.dumps([prompt,sol,sorted(bank)],ensure_ascii=False).encode()).hexdigest()
    qid=uuid.uuid5(uuid.NAMESPACE_URL,fp);fid=uuid.uuid5(qid,'selection')
    answers=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
    cid=answers[matches[0]][':answer/id'];rng.shuffle(answers)
    calculation=hashlib.sha256(str(([sp.srepr(sp.expand(x)) for x in sumvec(ds,coeff)],point)).encode()).hexdigest()
    source_ids=[SOURCE[name]['id']] if name in SOURCE else ['ce098ff9-2ef1-5483-b057-b3fef12af16d']
    if name=='mixed-symbolic':source_ids.append('87c2dd6b-a359-5e66-9212-aad50d85ddce')
    r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':sol,
        ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',
        ':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},
        'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'domain':domain,
        'source_analysis':{'database':'math','basis':8683,'question_ids':source_ids},
        'source_correction':'real logarithm argument sign at negative evaluation point' if name=='q-128452' else None,
        'authored_extension':not replay or name=='q-33143','calculation_fingerprint':calculation,
        'content_fingerprint':fp,'distractor_recipes':recipes,'plot_assets':{}}}
    return validate_generated_record(r)

def bank_signature(record):
    """Visible bank-only cues, used to avoid a perfect cue in a short family pool.

    Predictions consult neither the question nor its key. The key is consulted
    only to score those predictions. A tie is an abstention, not a forced guess.
    """
    from collections import Counter
    field=record['question'][':question/answer-fields'][0]
    choices=field[':answer-field/choices']
    def components(raw):
        if raw.startswith(r'\begin{bmatrix}'):
            parts=raw[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')].split(r'\\')
            return tuple(str(sp.expand(scalar(x))) for x in parts)
        if raw.startswith(r'\langle'):
            parts=raw[len(r'\langle'):-len(r'\rangle')].replace(r'\,','').split(',')
            return tuple(str(sp.expand(scalar(x))) for x in parts)
        return tuple(str(sp.expand(x)) for x in vector(raw))
    vectors=[tuple(scalar(x) for x in a[':answer/value'][len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')].split(r'\\'))
             if a[':answer/value'].startswith(r'\begin{bmatrix}') else
             tuple(scalar(x) for x in a[':answer/value'][len(r'\langle'):-len(r'\rangle')].replace(r'\,','').split(','))
             if a[':answer/value'].startswith(r'\langle') else vector(a[':answer/value'])
             for a in choices]
    def modal_index(columns):
        modes=[]
        for column in zip(*columns):
            counts=Counter(column); maximum=max(counts.values())
            modes.append({x for x,n in counts.items() if n==maximum})
        intersection=[n for n,v in enumerate(columns) if all(v[j] in modes[j] for j in range(len(modes)))]
        return intersection[0] if len(intersection)==1 else None
    predictions=[modal_index([tuple(str(sp.expand(x)) for x in v) for v in vectors])]
    # Matching entire coordinates misses an error that changes only one term.
    # Also examine the modal coefficient of each displayed argument/power base.
    coefficients=[];features=set()
    for vector_value in vectors:
        terms={}
        for coordinate,x in enumerate(vector_value):
            for term in sp.Add.make_args(sp.expand(x)):
                coefficient,base=term.as_coeff_Mul();feature=(coordinate,sp.srepr(base))
                terms[feature]=terms.get(feature,0)+coefficient;features.add(feature)
        coefficients.append(terms)
    features=sorted(features)
    predictions.append(modal_index([tuple(str(d.get(f,0)) for f in features) for d in coefficients]))
    # Numeric bank ranks are a surface diagnostic at a fixed, arbitrary probe
    # point, independent of the task's requested evaluation point or domain.
    numeric=[[float(sp.N(x.subs(T,sp.Rational(29,4)))) for x in v] for v in vectors]
    ranks=[]
    for values in [[sum(x*x for x in v) for v in numeric]]+list(map(list,zip(*numeric))):
        ranks.append(sorted(range(5),key=lambda n:values[n]) if len(set(values))==5 else None)
    for ordering in ranks:
        predictions.extend(ordering if ordering is not None else [None]*5)
    key=next(n for n,a in enumerate(choices) if a[':answer/id']==field[':answer-field/correct'][1])
    return key, tuple(prediction==key for prediction in predictions)

def batch(level,count,seed):
    rng=random.Random(seed);names=[n for n,l in LEVELS.items() if l==level]
    cycle=[];records=[];seen=set();signatures=[]
    for _ in range(count):
        if not cycle:cycle=rng.sample(names,len(names))
        name=cycle.pop()
        for attempt in range(128):
            r=generate(level,rng.getrandbits(64),name)
            sig=r['generation']['calculation_fingerprint']
            if sig in seen:continue
            signature=bank_signature(r)
            # Check the full short pool and each recognizable family separately.
            # Keep true and false modal cases eligible; do not make "avoid the
            # modal answer" a new construction invariant.
            groups=[signatures, [s for q,s in zip(records,signatures)
                                if q['generation']['template']==name]]
            if any(len(group)>=1 and
                   (all(s[0]==signature[0] for s in group) or
                    any(hit and all(s[1][j] for s in group) for j,hit in enumerate(signature[1])))
                   for group in groups):continue
            break
        else:raise ValueError('Could not construct a fresh batch without a perfect bank cue')
        seen.add(sig);records.append(r);signatures.append(signature)
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--source-case',choices=list(SOURCE))
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(LEVELS[args.source_case],args.seed,args.source_case,True)] if args.source_case else batch(args.difficulty,args.count,args.seed)
    print(json.dumps(_apply_source_notation(records),ensure_ascii=False,indent=2))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
