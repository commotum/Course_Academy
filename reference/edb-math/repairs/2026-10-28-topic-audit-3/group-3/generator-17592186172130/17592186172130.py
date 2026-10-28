#!/usr/bin/env python3
"""Construct surface integrands; math snapshot1356; no EDB writes.

Easy: observed norm-hint families; scalar-coordinate substitution only.
Moderate: observed families plus formal held-coordinate derivatives, signed
minor expansion, norm reduction and the same substitution. Hard is authored:
a mixed quadratic coordinate contributes to both tangent vectors; no integration.
Normal a=1..3, p,q=1..4. Hard a,b,c,d,p,q=1..3, c nonzero.
Raw observed profiles parameterize scalar multiplication of the ENTIRE source
function and entire bank. Opaque historical errors are evidence-only; they are
not used in learner sampling. Full source masks preserve raw omissions/errors.
Normal profiles are complete method-derived five-option banks selected first.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
KP=17592186172130
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
REC=CAPTURE['record']; VERSION='surface-setup-1-audit9837'
Q=REC[':knowledge-point/questions']
u,v=sp.symbols('u v', real=True); x,y,z=sp.symbols('x y z',real=True)
TYPES={q[':question/math-academy-id']:q for q in Q}
NAMES=['saddle','cancel','cubic','powers','product','negative_plane','fold','mixed','plane','cylinder','signed','quadratic']
BY_NAME=dict(zip(NAMES,Q)); BY_ID={str(q[':db/id']):n for n,q in BY_NAME.items()}
LEVELS={n:q[':question/difficulty'][':db/ident'].rsplit('/',1)[1] for n,q in BY_NAME.items()}; LEVELS['mixed_hard']='hard'
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def read_math(s):
    """Independent restricted TeX reader for all displayed polynomial/radical values."""
    s=s.strip().rstrip('.,'); s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
    def groups(t):
        while r'\sqrt{' in t:
            i=t.index(r'\sqrt{'); j=i+6; depth=1; k=j
            while depth:
                if t[k]=='{':depth+=1
                if t[k]=='}':depth-=1
                k+=1
            t=t[:i]+' sqrt('+groups(t[j:k-1])+')'+t[k:]
        return t
    s=groups(s).replace('{','(').replace('}',')')
    result=parse_expr(s.strip(),local_dict={'u':u,'v':v,'x':x,'y':y,'z':z,'sqrt':sp.sqrt},transformations=TRANS)
    if not result.free_symbols <= {u,v,x,y,z}:raise ValueError('Unrecognized displayed symbols: '+str(result.free_symbols))
    return result

def tex(e):return sp.latex(e, mul_symbol=None)
def vec(parts):return '⟨'+r',\,'.join(map(tex,parts))+'⟩'
def same(a,b):
    # Every authored member is a polynomial times the common metric radical,
    # or a polynomial without it. Expanding gives an exact ring comparison;
    # independent displayed-form validation also uses full simplify below.
    return sp.expand(a-b)==0

def display_blocks(s):return re.findall(r'\$\$\n(.*?)\n\$\$',s,re.S)
def block(s):return '$$\n'+s+'\n$$'
def replace_block(s,old,new):
    assert s.count(block(old))==1
    return s.replace(block(old),block(new))
def aligned(label,rows,period=True):
    return r'\begin{aligned}'+label+r' & ='+(r' \\  & =').join(rows)+('.' if period else '')+r'\end{aligned}'

# Source order comes from first-step/next; captured Pull order is not used.
def lesson_route():
    records=json.loads((HERE/'lessons.json').read_text())['record']; out=[]
    for activity in records:
        steps={s[':db/id']:s for s in activity.get(':activity/steps',[])}
        cur=activity[':activity/first-step'][':db/id']
        while cur in steps:
            s=steps[cur]; out.append({'step':cur,'content':s.get(':step/content',{}).get(':db/id')})
            nxt=s.get(':step/next');
            if not nxt:break
            cur=nxt[':db/id']
    return out

def operands(name,a,p,q):
    """Ordered substituted operations, kept unevaluated until family reduction."""
    A=lambda e:'('+tex(e)+')'; C=lambda n:'' if n==1 else str(n)+r'\cdot '
    if name=='saddle':return C(p)+A(a*u)+r'\cdot v\cdot uv'
    if name=='cancel':return C(p)+A(a*u**2)+'+'+C(q)+r'((u-v^{2})+v^{2})'
    if name=='cubic':return C(p)+A(a*u)+r'\cdot u^{2}+'+C(q)+r'2v'
    if name=='powers':return C(p)+'('+tex(a*u**2)+r'\cdot '+tex(a*u**2)+r')\cdot v^{2}\cdot v^{2}'
    if name=='product':return '-'+C(p)+'('+tex(a*u)+r'\cdot '+tex(a*u)+')+'+C(q)+r'(u+v)\cdot v^{2}'
    if name=='negative_plane':return C(p)+A(-a*u)+r'^{2}\cdot (-v)^{2}+'+C(q)+r'(-u)'
    if name=='fold':return '-'+C(p)+A(a*u)+'-'+C(q)+r'(v^{2}-u^{2})-'+C(q)+'u'
    if name=='mixed':return C(p)+A(a*u*v)+'-'+C(q)+r'(-u)^{2}\cdot (-v^{2})'
    if name=='plane':return C(p)+A(a*u)+r'^{2}+'+C(q)+r'u^{2}'
    if name=='cylinder':return '-'+C(p)+A(a*u**3)+'-'+C(q)+r'(v^{2}\cdot v^{2})'
    if name=='signed':return C(p)+A(a*u)+r'\cdot (-v^{2})+'+C(q)+r'(-v)'
    if name=='quadratic':return C(p)+A(a*u*v)+'+'+C(q)+r'v^{2}'
    raise ValueError(name)

def model(name,par):
    if name=='mixed_hard':
        a,b,c,d,p,q=(sp.Integer(par[k]) for k in ['a','b','c','d','p','q'])
        r=sp.Matrix([a*u*v,-b*u,c*u-d*v**2]); f=p*x-q*y**2*z
        operand=tex(p*a*u*v)+'-'+str(q)+r'\cdot ('+tex(-b*u)+r')^{2}\cdot ('+tex(c*u-d*v**2)+')'
    else:
        a,p,q=(sp.Integer(par[k]) for k in ['a','p','q'])
        forms={
          'saddle':([a*u,v,u*v],p*x*y*z),
          'cancel':([a*u**2,u-v**2,v**2],p*x+q*y+q*z),
          'cubic':([a*u,u**2,2*v],p*x*y+q*z),
          'powers':([a*u**2,v,v],p*x**2*y**2*z**2),
          'product':([a*u,u+v,v**2],-p*x**2+q*y*z),
          'negative_plane':([-a*u,-u,-v],p*x**2*z**2+q*y),
          'fold':([a*u,v**2-u**2,u],-p*x-q*y-q*z),
          'mixed':([a*u*v,-u,-v**2],p*x-q*y**2*z),
          'plane':([a*u,u,v],p*x**2+q*y**2),
          'cylinder':([a*u**3,v,v**2],-p*x-q*z**2),
          'signed':([a*u,-v,-v**2],p*x*z+q*y),
          'quadratic':([a*u*v,u**2,v**2],p*x+q*z)}
        r0,f=forms[name]; r=sp.Matrix(r0); operand=operands(name,a,p,q)
    ru=r.diff(u); rv=r.diff(v); cross=ru.cross(rv); square=sp.expand(cross.dot(cross))
    # Source simplifications are valid on these explicitly stated half-planes.
    if name=='cancel':norm=2*v*sp.sqrt(4*a*a*u*u*2+1)
    elif name=='powers':norm=sp.sqrt(8)*a*u
    elif name=='fold':norm=2*v*sp.sqrt(a*a+1)
    elif name=='cylinder':norm=3*a*u*u*sp.sqrt(4*v*v+1)
    else:norm=sp.sqrt(square)
    pull=sp.expand(f.subs({x:r[0],y:r[1],z:r[2]}, simultaneous=True))
    # Preserve original factoring of the substituted polynomial in product family.
    if name=='product':pull=sp.Add(-p*a*a*u*u,sp.Mul(q,sp.Add(u,v,evaluate=False),v**2,evaluate=False),evaluate=False)
    integral=sp.Mul(pull,norm,evaluate=False)
    return {'r':r,'f':f,'ru':ru,'rv':rv,'cross':cross,'square':square,'norm':norm,'pull':pull,'integrand':integral,'operand':operand}

def derivative_block(m):
    rows=[]
    for s,der in [(u,m['ru']),(v,m['rv'])]:
        formal='⟨'+r',\,'.join(r'\frac{∂'+str(c)+'}{∂'+str(s)+'}' for c in [x,y,z])+'⟩'
        operation='⟨'+r',\,'.join(r'\frac{∂}{∂'+str(s)+'}('+tex(c)+')' for c in m['r'])+'⟩'
        rows.append(aligned('{r}_{'+str(s)+'}^{′}',[formal,operation,vec(der)],False))
    return rows[0][:-len(r'\end{aligned}')]+r' \\ '+rows[1][len(r'\begin{aligned}'):]

def cross_block(m):
    a,b=list(m['ru']),list(m['rv'])
    det='|'+r'\begin{aligned}i & j & k \\ '+ ' & '.join(map(tex,a))+r' \\ '+' & '.join(map(tex,b))+r'\end{aligned}|'
    def minor(i,j):return '|'+r'\begin{aligned}'+tex(a[i])+' & '+tex(a[j])+r' \\ '+tex(b[i])+' & '+tex(b[j])+r'\end{aligned}|'
    minors='⟨'+minor(1,2)+r',\,-'+minor(0,2)+r',\,'+minor(0,1)+'⟩'
    return aligned(r'{r}_{u}^{′}\times {r}_{v}^{′}',[det,minors,vec(m['cross'])],False)

def norm_block(name,m):
    literal=r'\sqrt{'+ '+'.join('('+tex(c)+')^{2}' for c in m['cross'])+'}'
    rows=['‖'+vec(m['cross'])+'‖',literal]
    if name in ['plane','fold','cylinder']:
        terms=[sp.expand(c*c) for c in m['cross'] if c!=0 or name=='plane']
        rows.append(r'\sqrt{'+ '+'.join(map(tex,terms))+'}')
    rows.append(tex(m['norm']))
    return aligned(r'‖{r}_{u}^{′}\times {r}_{v}^{′}‖',rows)

# For normal banks, errors are actual omitted factors, omitted coordinate terms,
# omitted derivative squares or missed signs in the displayed calculation.
def authored_bank(name,m):
    p=m['pull']; n=m['norm']; sq=m['square']; components=list(sp.Add.make_args(sp.expand(p)))
    if name=='plane':
        # Two independent squared-coordinate contributions combine to one
        # monomial; do not manufacture a missing-v-factor error.
        fx=m['f'].coeff(x,2); fy=m['f'].coeff(y,2); xx=m['r'][0]
        vals=[p*n,p,fx*xx**2*n,p.subs(u,v)*n,(fx*xx**2+fy*v**2)*n]
        recipes=['correct','omit_metric','omit_y_squared','use_v_for_both_coordinates','use_v_for_y']
    elif len(components)>1:
        t=components[0]
        vals=[p*n,p,(p-t)*n,(p-2*t)*n,p*sq]
        recipes=['correct','omit_metric','omit_one_pullback_term','reverse_one_pullback_sign','use_squared_metric']
    else:
        # These two monomial sources assess powers and products; varying a,p
        # retains the original workload. Wrong exponent/displacement values.
        vals=[p*n,p,p*n/u,p*n/v,p*sq]
        recipes=['correct','omit_metric','omit_u_factor','omit_v_factor','use_squared_metric']
    return vals,recipes

def normal_content(name,par):
    m=model(name,par); level=LEVELS[name]
    if name=='mixed_hard':source=BY_NAME['mixed']
    else:source=BY_NAME[name]
    prompt=source[':question/problem']; sol=source[':question/worked-solution']; blocks=display_blocks(sol)
    oldf=re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt).group(1)
    prompt=prompt.replace('$f(x,y,z)='+oldf+'$', '$f(x,y,z)='+tex(m['f'])+'$')
    oldr=display_blocks(prompt)[1]
    prompt=replace_block(prompt,oldr,'r(u,v)='+vec(m['r']))
    if level=='easy':
        prompt=re.sub(r'‖\{r\}_\{u\}\^\{′\}\\times \{r\}_\{v\}\^\{′\}‖=.*?\$\*',lambda _:r'‖{r}_{u}^{′}\times {r}_{v}^{′}‖='+tex(m['norm'])+'.$*',prompt)
        sol=replace_block(sol,blocks[1],r'‖{r}_{u}^{′}\times {r}_{v}^{′}‖='+tex(m['norm'])+'.')
    else:
        sol=replace_block(sol,blocks[1],derivative_block(m))
        sol=replace_block(sol,blocks[2],cross_block(m))
        sol=replace_block(sol,blocks[3],norm_block(name,m))
    pullblock=next(b for b in blocks if b.startswith(r'\begin{aligned}f(r(u,v))'))
    restriction=r'\,{|}_{'+r'\,'.join(str(s)+'='+tex(c) for s,c in zip([x,y,z],m['r']))+'}'
    pullrows=['('+tex(m['f'])+')'+restriction,m['operand']]
    if name!='quadratic':pullrows.append(tex(m['pull']))
    else:pullrows[1]=tex(m['pull'])
    sol=replace_block(sol,pullblock,aligned('f(r(u,v))',pullrows,False))
    final=blocks[-1]
    rows=[r'{∬}_{D}f(r(u,v))‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A',r'{∬}_{D}\,'+tex(m['integrand'])+r'\,\,\text{d}A']
    sol=replace_block(sol,final,aligned(r'{∬}_{S}f(x,y,z)\,\text{d}S',rows))
    if name=='cancel' or name=='fold':prompt=prompt.replace('What is the missing expression?',r'Assume $v\geq0.$ What is the missing expression?')
    if name=='powers':prompt=prompt.replace('What is the missing expression?',r'Assume $u\geq0.$ What is the missing expression?')
    prompt=prompt.replace('What is the missing expression?','What is the missing expression? Choose an integrand equal to the required expression as a function on $D$.')
    return prompt,sol,m

def scale_tex(s,k):return s if k==1 else tex(k)+r'\left('+s+r'\right)'

def raw_content(name,k):
    """Parameterized source masks. No copied payload or answer lookup dispatch.
    Only complete f/component expressions are slots, never letters in prose.
    Derivative blocks are fixed because scalar f changes leave the surface fixed.
    """
    source=BY_NAME[name]; prompt=source[':question/problem']; sol=source[':question/worked-solution']
    fstr=re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt).group(1)
    prompt=prompt.replace('$f(x,y,z)='+fstr+'$', '$f(x,y,z)='+scale_tex(fstr,k)+'$')
    blocks=display_blocks(sol)
    b=next(b for b in blocks if b.startswith(r'\begin{aligned}f(r(u,v))'))
    parts=b.split(r' & ='); newparts=[parts[0]]
    for i,piece in enumerate(parts[1:]):
        if i==0:
            head,tail=piece.split(r'\,{|}_{',1)
            expr=scale_tex(head[1:-1],k)
            newparts.append('('+expr+r')\,{|}_{'+tail)
        else:
            end=r'\end{aligned}' if r'\end{aligned}' in piece else r' \\ '
            value=piece.removesuffix(end);newparts.append(scale_tex(value,k)+end)
    sol=replace_block(sol,b,(r' & =').join(newparts))
    last=blocks[-1]; match=re.search(r'& =\{∬\}_\{D\}\\,(.*?)\\,\\,\\text\{d\}A',last)
    assert match, name
    last=last[:match.start(1)]+scale_tex(match.group(1),k)+last[match.end(1):]
    sol=replace_block(sol,blocks[-1],last)
    return prompt,sol

def digest(o):return hashlib.sha256(json.dumps(asset_payload(o),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'surface-setup/'+s))
def enum(e):return e[':db/ident'] if isinstance(e,dict) else e

def construct(level,seed,name,par,profile):
    raw=profile=='observed'; source=BY_NAME.get(name)
    if raw:
        if source is None:raise ValueError('No observed hard bank')
        if set(par)!={'k'} or not isinstance(par['k'],int) or isinstance(par['k'],bool) or not 1<=abs(par['k'])<=5:raise ValueError('Observed replay supports nonzero integer k with |k|<=5')
        prompt,sol=raw_content(name,par['k']); m=None
        spec=[]
        for field in source[':question/answer-fields']:
            vals=[scale_tex(a[':answer/value'],par['k']) for a in field[':answer-field/choices']]
            correct=field.get(':answer-field/correct'); index=next((i for i,a in enumerate(field[':answer-field/choices']) if correct and a[':answer/id']==correct[':answer/id']),None)
            spec.append((vals,index,field))
        recipes=['opaque_observed_expression_scaling']; eligible=False
    else:
        keys={'a','b','c','d','p','q'} if name=='mixed_hard' else {'a','p','q'}
        if set(par)!=keys:raise ValueError('Exact parameter keys required: '+str(sorted(keys)))
        for k,val in par.items():
            bound=3 if name=='mixed_hard' or k=='a' else 4
            if not isinstance(val,int) or isinstance(val,bool) or not 1<=val<=bound:raise ValueError(k+' outside workload bounds')
        if name in ['saddle','powers'] and par['q']!=1:raise ValueError('Unused q must equal 1')
        prompt,sol,m=normal_content(name,par); expressions,recipes=authored_bank(name,m)
        if any(same(a,b) for i,a in enumerate(expressions) for b in expressions[:i]):raise ValueError('Whole bank collision')
        spec=[([tex(t) for t in expressions],0,None)];eligible=True
    if not raw:
        prompt=normalize_prose(prompt);sol=normalize_prose(sol);spec=[([normalize_tex(v)for v in vals],correct,original)for vals,correct,original in spec]
    # Identity depends on displayed content and difficulty, never seed or profile alias.
    key=digest([VERSION,level,prompt,sol,[(sorted(v),i is not None and v[i]) for v,i,_ in spec]])
    question={':question/id':uid(key),':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[]}
    for fi,(vals,correct,original) in enumerate(spec):
        fid=uid(key+'/field/'+str(fi)); answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
        if len({a[':answer/id'] for a in answers})!=len(answers):raise ValueError('Duplicate displayed option')
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if correct is not None:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
        random.Random(str(seed)+'/'+fid).shuffle(answers);question[':question/answer-fields'].append(field)
    if raw:
        for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
            if k not in source:question.pop(k,None)
    if raw:
        printed_r=display_blocks(prompt)[1].split('=',1)[1]
        mathematical=digest([level,[tex(read_math(t)) for t in printed_r[1:-1].split(r',\,')],tex(read_math(re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt).group(1))),'norm_given' if level=='easy' else 'compute_norm'])
    else:mathematical=digest([level,[tex(t) for t in m['r']],tex(m['f']),'norm_given' if level=='easy' else 'compute_norm'])
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'level':level,'template':name,'parameters':par,'profile':profile,'seed':seed,'source':{k:CAPTURE[k] for k in ['database','basis','lineage']},'source_id':source[':db/id'] if source else None,'authored_level':level=='hard','evidence_only':raw,'eligible_for_learning':eligible,'recipes':recipes,'mathematical_fingerprint':mathematical,'content_fingerprint':key,'python':sys.version.split()[0],'sympy':sp.__version__,'domain': 'u>=0' if name=='powers' else 'v>=0' if name in ['cancel','fold'] else 'real u,v','plot_rating':'none'}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('Unknown level')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Unsupported field type')
    if profile not in [None,'authored','observed']:raise ValueError('Unknown bank profile')
    rng=random.Random(seed);name=template or rng.choice([n for n,l in LEVELS.items() if l==level])
    if name in BY_ID:name=BY_ID[name]
    if name not in LEVELS or LEVELS[name]!=level:raise ValueError('Template/difficulty mismatch')
    profile=profile or 'authored'
    if parameters is not None:return construct(level,seed,name,dict(parameters),profile)
    for _ in range(100):
        if profile=='observed':par={'k':rng.choice([-3,-2,-1,1,2,3])}
        elif name=='mixed_hard':par={k:rng.randint(1,3) for k in ['a','b','c','d','p','q']}
        else:par={'a':rng.randint(1,3),'p':rng.randint(1,4),'q':1 if name in ['saddle','powers'] else rng.randint(1,4)}
        try:return construct(level,seed,name,par,profile)
        except ValueError as e:
            if 'collision' not in str(e):raise
    raise ValueError('No eligible complete bank')

# EASY — observed hints; family-specific ordered pullback products/cancellations.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE — full formal operators, zero derivatives, signed minors and norm.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD — authored mixed coordinate; c!=0 retains extra held-coordinate demand.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];s=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        s+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
    return s+'\n'+q.get(':question/worked-solution','')+'\n'
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=['observed','authored']);args=ap.parse_args()
    rows=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(r) for r in rows))
