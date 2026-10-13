#!/usr/bin/env python3
"""Gradient product property; local steps 3–7, database math at basis 1356.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), and generate_easy/moderate/hard with the same keyword arguments.
Source profiles source:<MA-id> replay through coordinate-component masks, including
missing attributes. They are not literal payload-return branches. Opaque historical
banks remain public evidence only. Normal sampling chooses whole family/bank first.
No EDB client, transactions, engine edits or renderer are needed.

Easy: authored two linear factors, supplied gradients; four scalar products in two
components. Moderate: six rated families plus the authored unrated completion, translated inputs and
original family-specific distribution/cancellation chains. cancel varies actual
coefficients instead of incidental translations. Hard: observed unsupplied Gaussian product plus authored unsupplied 3D
binomial times reciprocal; six coordinate derivatives, twelve monomial products.
All questions use the product property, with no progression within a level.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

KP_ID=17592186124447
TITLE='Calculating the Gradient Using the Properties of the Gradient'
VERSION='gradient-properties-2'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
RAW=CAPTURE['record']; KP_UUID=RAW[':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions']}
x,y,z=s.symbols('x y z', real=True)
i,j,k=s.symbols('i j k')
VARS=(x,y,z); BASIS=(i,j,k)
FAMILIES={'poly':'q-36144','log_product':'q-37466','gaussian':'q-128521','reciprocal3':'q-128529','log':'q-65131','cancel':'q-71476','exp_linear':'q-128532','exp_product':'q-71484'}
OPAQUE={'poly','gaussian','reciprocal3','exp_linear'}
ELIGIBLE=('poly','log_product','gaussian','reciprocal3','log','cancel','exp_linear','exp_product')
FAMILY_LEVELS={f:SOURCES[q].get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1] for f,q in FAMILIES.items()}
LEVELS={'easy':('linear',),'moderate':tuple(f for f in ELIGIBLE if FAMILY_LEVELS[f]=='moderate'),'hard':tuple(f for f in ELIGIBLE if FAMILY_LEVELS[f]=='hard')+('binomial3',)}
TRANSFORMS=standard_transformations+(implicit_multiplication_application,)

def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(value): return str(uuid.uuid5(uuid.NAMESPACE_URL, 'gradient-properties:'+value))
def tex(e): return s.latex(e).replace(r'\log',r'\ln')
def vector(v): return '+'.join('('+tex(e)+')'+r'\,'+str(b) for e,b in zip(v,BASIS)).replace('+-','-')
def grad(f,vs): return tuple(s.diff(f,v) for v in vs)
def equal(a,b):
    delta=s.expand(a-b)
    if delta==0:return True
    # A single exact nonzero specialization proves expressions are unequal.
    # These coordinates lie inside every supported logarithm/reciprocal domain.
    for b in BASIS:
        probe=delta.subs({x:11,y:13,z:17,**{v:int(v==b) for v in BASIS}})
        if probe.is_zero is False:return False
    return s.cancel(delta)==0 or s.simplify(delta)==0

def _groups(text,start):
    assert text[start]=='{'; depth=1; end=start+1
    while depth and end<len(text):
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    if depth: raise ValueError('unbalanced group')
    return text[start+1:end-1],end

def parse_math(text,local=None):
    """Read actual displayed scalar/vector math, independently of generation params."""
    text=text.strip().rstrip('.,')
    text=text.replace('\u2061','').replace('∇',r'\nabla').replace('∂',r'\partial')
    text=re.sub(r'\\text\{[^}]*\}', '', text)
    for token in [r'\left',r'\right',r'\,',r'\!',r'\;',r'\quad']:text=text.replace(token,'')
    text=text.replace(r'\cdot','*').replace(r'\operatorname{ln}',r'\ln')
    for cmd,fun in [(r'\frac','frac'),(r'\dfrac','frac'),(r'\sqrt','sqrt')]:
        while cmd in text:
            start=text.index(cmd); pos=start+len(cmd)
            a,end=_groups(text,pos)
            if fun=='frac':
                b,end=_groups(text,end); sub='(('+parse_code(a)+')/('+parse_code(b)+'))'
            else:sub='sqrt('+parse_code(a)+')'
            text=text[:start]+sub+text[end:]
    code=parse_code(text)
    return parse_expr(code,local_dict={'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'e':s.E,'ln':s.log,**(local or {})},transformations=TRANSFORMS)

def parse_code(text):
    # recursively expand fractions before conversion, including nesting
    for cmd in [r'\frac',r'\dfrac',r'\sqrt']:
        while cmd in text:
            start=text.index(cmd); a,end=_groups(text,start+len(cmd))
            if cmd!=r'\sqrt':b,end=_groups(text,end);rep='(('+parse_code(a)+')/('+parse_code(b)+'))'
            else:rep='sqrt('+parse_code(a)+')'
            text=text[:start]+rep+text[end:]
    while r'\ln' in text:
        start=text.index(r'\ln');pos=start+3
        while pos<len(text) and text[pos].isspace():pos+=1
        if text[pos] in '({':
            opening=text[pos];closing=')' if opening=='(' else '}'
            depth=1;end=pos+1
            while depth:
                depth+=(text[end]==opening)-(text[end]==closing);end+=1
            arg=text[pos+1:end-1]
        else:arg=text[pos];end=pos+1
        text=text[:start]+'log('+parse_code(arg)+')'+text[end:]
    text=text.replace('{','(').replace('}',')').replace('^','**').replace('[','(').replace(']',')')
    return re.sub(r'[xyzijk]',lambda m:' '+m.group()+' ',text)

def components(expr,n):
    expr=s.expand(expr); values=tuple(expr.coeff(b) for b in BASIS[:n])
    residual=s.simplify(expr-s.Add(*(a*b for a,b in zip(values,BASIS[:n]))))
    if residual!=0:return None
    return values

def shifted_symbol(letter,amount):
    if not amount:return letter
    return '('+letter+('-'+str(amount) if amount>0 else '+'+str(-amount))+')'

def translate_math(math,parameters):
    """Compile scalar-component slots before coordinate translation.

    The protected nodes are function argument tuples and differential variables;
    commands are tokens, not substrings. Each x/y/z occurrence in a scalar
    component is its entire input node, replaced by a grouped translated input.
    Numeric coefficients, powers, operator grouping and arithmetic stages remain.
    """
    protected={}
    def protect(m):
        key='@'+str(len(protected))+'@';protected[key]=m.group();return key
    math=re.sub(r'[fgh]\(x,\s*y(?:,\s*z)?\)|\{∂[xyz]\}',protect,math)
    # Commands and their text arguments are protected as complete nodes.
    math=re.sub(r'\\(?:text|operatorname)\{[^}]*\}|\\[A-Za-z]+',protect,math)
    math=re.sub(r'[xyz]',lambda m:shifted_symbol(m.group(),parameters.get(m.group()+'0',0)),math)
    for key,val in protected.items():math=math.replace(key,val)
    return math

def translate_markdown(markdown,p):
    return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',lambda m:translate_math(m.group(),p),markdown)

def expressions(family,p):
    X=x-p.get('x0',0);Y=y-p.get('y0',0);Z=z-p.get('z0',0)
    if family=='poly':return 3*X**2-4*Y,2*X**2*Y**2,(x,y)
    if family=='log_product':return s.log(X)*s.log(Y),X**2*Y**2,(x,y)
    if family=='gaussian':return X*Y**2,s.exp(-(X**2+Y**2)),(x,y)
    if family=='reciprocal3':return X*Y**2*Z**3,1/(X*Y*Z),(x,y,z)
    if family=='log':return X*Y,s.log(X*Y),(x,y)
    if family=='cancel':return p['a']*x**2*y+p['b']*x*y**2,1/(x*y),(x,y)
    if family=='exp_linear':return s.exp(X-Y),X**2-3*X*Y,(x,y)
    if family=='exp_product':return s.exp(X*Y),X**2+Y**2,(x,y)
    if family=='linear':return p['a']*x+p['b']*y,p['c']*x+p['d']*y,(x,y)
    if family=='binomial3':
        a,b=p['a'],p['b'];r,t=p['r'],p['t']
        return a*x**2*y**r*z+b*x*y*z**t,1/(x*y*z),(x,y,z)
    raise ValueError('unknown family')

def cancel_masks(p):
    a,b=p['a'],p['b']
    # Complete source scalar nodes, not blind coefficient/string replacements.
    def linear(A,B):return tex(A*x+B*y)
    f=tex(a*x**2*y+b*x*y**2)
    fx=tex(2*a*x*y+b*y**2);fy=tex(a*x**2+2*b*x*y)
    patterns=[
      ('{x}^{2}y+x{y}^{2}', f),('2xy+{y}^{2}',fx),('{x}^{2}+2xy',fy),
      ('2x+y',linear(2*a,b)),('x+2y',linear(a,2*b)),('x+y',linear(a,b))]
    # Anchor styles are rendered by explicit polynomial masks for exact replay.
    patterns=[(old,new.replace('x^{2}','{x}^{2}').replace('y^{2}','{y}^{2}').replace(' ','').replace('x y','xy')) for old,new in patterns]
    return dict(patterns)

def render_cancel(text,p):
    mask=cancel_masks(p)
    token=re.compile('|'.join(re.escape(v) for v in sorted(mask,key=len,reverse=True)))
    text=token.sub(lambda m:mask[m.group()],text)
    # Final constants and source complete answer masks are separate nodes.
    return text

def source_render(family,p):
    q=SOURCES[FAMILIES[family]]
    render=(lambda t:render_cancel(t,p)) if family=='cancel' else (lambda t:translate_markdown(t,p))
    prompt=render(q[':question/problem'])
    solution=render(q[':question/worked-solution']) if ':question/worked-solution' in q else None
    values=[]
    if family=='cancel':
        a,b=p['a'],p['b'];gap=r'\text{ }'
        def ct(c,atom=''):
            return ('' if c==1 else str(c))+atom
        values=[ct(a,'y')+gap+'i+'+ct(b,'x')+gap+'j',
                ct(a,'x')+gap+'i+'+ct(b,'y')+gap+'j',
                ct(a)+gap+'i+'+ct(b)+gap+'j',
                '-'+ct(a)+gap+'i+'+ct(b)+gap+'j',
                ct(a)+gap+'i-'+ct(b)+gap+'j']
    else:
        values=[translate_math(ans[':answer/value'],p) for ans in q[':question/answer-fields'][0][':answer-field/choices']]
    if family=='cancel' and p!={'a':1,'b':1}:
        solution=solution.replace(r'=\text{ }i+\text{ }j', '='+vector((p['a'],p['b'])))
    correct=q[':question/answer-fields'][0].get(':answer-field/correct')
    correct_index=next((n for n,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']) if correct and a[':answer/id']==correct[':answer/id']),None)
    return prompt,solution,values,correct_index

def method_bank(F,G,vs):
    A=grad(F,vs);B=grad(G,vs)
    correct=tuple(s.simplify(G*a+F*b) for a,b in zip(A,B))
    # Complete same-method bank: omit each product-rule contribution, subtract
    # rather than add, and swap first two ordered gradient components.
    vals=[correct,tuple(G*a for a in A),tuple(F*b for b in B),tuple(G*a-F*b for a,b in zip(A,B)),tuple([correct[1],correct[0],*correct[2:]])]
    return vals

def generic_solution(F,G,vs,names=('f','g'),derive=False,local_offsets=None):
    f,g=names;args=','.join(map(str,vs));n=len(vs)
    def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    A=grad(F,vs);B=grad(G,vs)
    opening=f'The gradient of the product of two functions ${f}({args})$ and ${g}({args})$ is given by\n\n$$\n∇[{f}{g}]={g}∇{f}+{f}∇{g}.\n$$'
    parts=[opening]
    if derive:
        for label,obj,D in [(f,F,A),(g,G,B)]:
            parts.append(f'Now, we calculate the partial derivatives of ${label}({args}):$')
            rows=[]
            for v,d in zip(vs,D):
                rows.append(r'\frac{∂'+label+'}{∂'+str(v)+'} & ='+r'\frac{∂}{∂'+str(v)+'}('+tex(obj)+')='+tex(d))
            parts.append(block(rows))
            parts.append('Hence,\n\n'+block([f'∇{label}({args}) & ='+ '+'.join(r'\frac{∂'+label+'}{∂'+str(v)+'}'+str(b) for v,b in zip(vs,BASIS))+'='+vector(D)]))
    parts.append('Using the product rule, we obtain')
    D=tuple(s.simplify(G*a+F*b) for a,b in zip(A,B))
    formal=f'∇[{f}({args}){g}({args})] & ={g}({args})∇{f}({args})+{f}({args})∇{g}({args})'
    substituted='('+tex(G)+')('+vector(A)+')+('+tex(F)+')('+vector(B)+')'
    distributed='+'.join('('+tex(obj)+')('+tex(d)+')'+str(b) for obj,D0 in [(G,A),(F,B)] for d,b in zip(D0,BASIS))
    def expand_contribution(value):
        if local_offsets is None:return s.expand(value)
        # Expand in the actual translated coordinate atoms, preserving the
        # original four contributions instead of introducing incidental FOIL.
        local=s.symbols('_X _Y _Z',real=True)[:n]
        offsets=[local_offsets.get(str(v)+'0',0) for v in vs]
        rewritten=value.subs(dict(zip(vs,[a+d for a,d in zip(local,offsets)])),simultaneous=True)
        expanded=s.expand(rewritten)
        return expanded.subs(dict(zip(local,[v-d for v,d in zip(vs,offsets)])),simultaneous=True)
    terms='+'.join('('+tex(expand_contribution(obj*d))+')'+str(b) for obj,D0 in [(G,A),(F,B)] for d,b in zip(D0,BASIS))
    rows=[formal,' & ='+substituted,' & ='+distributed,' & ='+terms,' & ='+vector(D)]
    parts.append(block(rows));return '\n\n'.join(parts)

def eligible_profile(family):
    return 'method' if family in OPAQUE or family in {'linear','binomial3'} else 'observed'

def validate_parameters(level,family,p,raw=False):
    if family=='linear':
        if set(p)!={'a','b','c','d'} or not all(type(v)==int and 1<=abs(v)<=4 for v in p.values()):raise ValueError('easy signed nonzero coefficients 1..4')
        if p['a']*p['d']==p['b']*p['c']:raise ValueError('proportional factors remove independent component collection')
    elif family=='binomial3':
        if set(p)!={'a','b','r','t'} or not all(type(v)==int for v in p.values()):raise ValueError('hard parameter keys/types')
        if not all(1<=abs(p[v])<=4 for v in ('a','b')) or p['r'] not in (1,2,3) or p['t'] not in (2,3,4):raise ValueError('hard workload bounds')
    elif family=='cancel':
        if set(p)!={'a','b'} or not all(type(v)==int and 1<=v<=6 for v in p.values()):raise ValueError('cancellation positive coefficients 1..6')
    else:
        keys={'x0','y0','z0'} if family=='reciprocal3' else {'x0','y0'}
        if set(p)!=keys or not all(type(v)==int and abs(v)<=6 for v in p.values()):raise ValueError('moderate translations are integers -6..6')

def sample(family,rng):
    if family=='linear':return dict(zip(('a','b','c','d'),(rng.choice(tuple(range(-4,0))+tuple(range(1,5))) for _ in range(4))))
    if family=='binomial3':return {'a':rng.choice((-4,-3,-2,-1,1,2,3,4)),'b':rng.choice((-4,-3,-2,-1,1,2,3,4)),'r':rng.choice((1,2,3)),'t':rng.choice((2,3,4))}
    if family=='cancel':return {'a':rng.randint(1,6),'b':rng.randint(1,6)}
    return {v+'0':rng.randint(-6,6) for v in ('xyz' if family=='reciprocal3' else 'xy')}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout')
    rng=random.Random(seed)
    sourceid=None
    if profile and profile.startswith('source:'):
        sourceid=profile[7:]
        if sourceid not in SOURCES:raise ValueError('source profile')
        family=next(k for k,v in FAMILIES.items() if v==sourceid)
        if template is not None and template!=family:raise ValueError('source template/profile mismatch')
        if level!=FAMILY_LEVELS[family]:raise ValueError('source replay must retain the captured difficulty (unrated replay uses authored moderate)')
    else:
        available=LEVELS[level]
        family=template or rng.choice(available)
        if family not in available:raise ValueError('family outside difficulty workload')
    selected=profile or (rng.choice(('observed','method')) if family in FAMILIES and family not in OPAQUE else 'method')
    if not sourceid and selected not in ('observed','method'):raise ValueError('unknown profile')
    if not sourceid and selected=='observed' and family in OPAQUE|{'linear','binomial3'}:raise ValueError('opaque/no observed bank is evidence only')
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(family,rng)
        try:
            validate_parameters(level,family,p,raw=bool(sourceid));F,G,vs=expressions(family,p)
            if family in FAMILIES:
                prompt,solution,values,correct_index=source_render(family,p)
                if not sourceid:
                    if family=='reciprocal3':solution=solution.replace('$f(x,y)$ and $h(x,y)$','$f(x,y,z)$ and $h(x,y,z)$')
                    if solution is None:solution=generic_solution(F,G,vs,derive=True,local_offsets=p)
                    if selected=='method':values=[vector(v) for v in method_bank(F,G,vs)];correct_index=0
                    elif correct_index is None:correct_index=1 # independently verified log-product bank
            else:
                args=','.join(map(str,vs));prompt=f'Find the gradient of the product $f({args})g({args}),$ given that '
                if level=='easy':prompt+='\n\n$$\n'+r'\begin{aligned}'+f'f({args}) & ='+tex(F)+r',\quad ∇f('+args+')='+vector(grad(F,vs))+r' \\ '+f'g({args}) & ='+tex(G)+r',\quad ∇g('+args+')='+vector(grad(G,vs))+r'\end{aligned}'+'\n$$'
                else:prompt+=f'$f({args})={tex(F)}$ and $g({args})={tex(G)}.$'
                solution=generic_solution(F,G,vs,derive=(level=='hard'));values=[vector(v) for v in method_bank(F,G,vs)];correct_index=0
            actual=[parse_math(v) for v in values]
            if len(actual)!=5 or any(equal(a,b) for n,a in enumerate(actual) for b in actual[:n]):raise ValueError('whole bank collision')
            D=grad(F*G,vs);target=s.Add(*(a*b for a,b in zip(D,BASIS)))
            if correct_index is not None and not equal(actual[correct_index],target):raise ValueError('correct vector differs from exact gradient')
            if any(not e.is_finite and e.is_finite is not None for e in actual):raise ValueError('undefined answer')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('no valid whole instance')
    math_key=digest({'product':s.srepr(s.expand(s.simplify(F*G))),'variables':list(map(str,vs)),'information':'unsupplied' if level=='hard' or family in ('gaussian','log_product') else 'supplied'})
    identity=digest({'version':VERSION,'difficulty':None if sourceid=='q-37466' else level,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':None if correct_index is None else values[correct_index]})
    qid=uid(identity);fid=uid(qid+'/selection')
    answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if correct_index is not None:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
    rng.shuffle(answers)
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if sourceid!='q-37466':question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':family,'profile':selected,'parameters':p,'seed':seed,'mathematical_fingerprint':math_key,'content_identity':identity,'database':CAPTURE['database'],'basis':CAPTURE['basis'],'lineage':CAPTURE['lineage'],'source_id':sourceid or FAMILIES.get(family),'evidence_only':bool(sourceid and (family in OPAQUE or sourceid=='q-37466')),'eligible_for_learning':not bool(sourceid and (family in OPAQUE or sourceid=='q-37466')),'authored_level':family in ('linear','binomial3'),'domain':'nonzero translated coordinates' if family in ('reciprocal3','cancel','binomial3') else 'positive translated logarithm arguments' if family in ('log','log_product') else 'all real coordinates','runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY — authored supplied 2D gradients, one fixed four-product workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — each observed family preserves its own stages, with public raw profiles.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored unsupplied 3D binomial/reciprocal, six derivatives and twelve monomial products.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];lines=[q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        lines.extend('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q:lines.extend(['','Worked solution:',q[':question/worked-solution']])
    return '\n'.join(lines)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--parameters',type=json.loads)
    args=parser.parse_args();levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(l,args.seed+n,args.template,parameters=args.parameters,profile=args.profile) for l in levels for n in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
