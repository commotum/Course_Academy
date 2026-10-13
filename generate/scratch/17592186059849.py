#!/usr/bin/env python3
"""Parameterized determinant equations; local review only, no database writes.

Sources: refreshed math snapshot. Source profiles retain their observed variable positions,
polynomial degrees and field layouts. Each complete radio profile is evaluated
as expressions in matrix coefficients or equation roots, never a payload lookup.
The interpretations of unusual observed distractors remain unknown: their
coefficient expressions are explicitly inferred generalizations, not claims
about Math Academy's original misconception code. Whole-bank collisions reject
an instance. Default hard practice is an authored mixture of identity, linear and
quadratic singularity equations with the same prompt and complete choice bank
shape. See the evidence directory for every original and recipe.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059849
KP_UUID='ab642ad6-d9e0-5734-83b4-81627b9132eb'
TITLE='Solving for an Unknown Given the Determinant'
VERSION='determinant-unknown-checkbox-4'
EVIDENCE=Path(__file__).with_suffix('')
X=sp.Symbol('u', real=True)
NS=uuid.UUID(KP_UUID)
HARD_MIXED_PROFILE='authored:hard_mixed'
HARD_MIXED_TEMPLATE='mixed_singular_radio'
# Recipes reference cN=constant entry, vN=linear coefficient, A/B/C=equation
# coefficients, D=given determinant, r0/r1=ascending independently solved roots.
# Each tuple is a COMPLETE observed profile, with its original ordering retained.
BANKS={
'q-9657': [('c5+c7','c2*c4'),('c0','D'),('D',),('r0','r1'),('c5+c7',)],
'q-9669': [('correct',),('-c0*c4',),('-c3',),('-c2+c3',),('c0*c4',)],
'q-9852': [('all',),('(c4+c7)/2',),('0',),('v8-v2',),('v8/2','-v8/2')],
'q-128500': [('c1*c2+c1',),('-c1*c2',),('D+c0',),('correct',),('c2',)],
'q-128502': [('2*c3*c5',),('-c7*c0*c0',),('c0',),('c0*c0*c1',),('correct',)],
'q-130575': [('correct',),('c4',),('c7-1','c4'),('c2','-c2'),('c2','c0*c4')],
'q-130580': [('-r0','c2'),('c5',),('c3','c2'),('correct',),('-c3','-c2')],
'q-130620': [('correct',),('(c2-c3)/B',),('c2',),('c1',),('-c2-c3',)],
'q-130626': [('(c2+c0)/abs(c3)',),('all',),('v1','-v1'),('v1',),('-abs(c5)-abs(c3)',)],
'q-18252': [('c7+c3',),('correct',),('c0+c3',),('-r0',),('c3',)],
'q-18256': [('c8/c2','c5'),('r0','c5'),('c8/c2','-c5'),('correct',),('r1',)],
'q-18271': [('c4',),('c3',),('-r0',),('-c4',),('correct',)],
'q-18272': [('-r0','c2*c2'),('correct',),('c2*c2','r1'),('c2*c2',),('r1',)],
'q-9911': [('correct',),('-r1',),('0',),('0','-r1'),('r1',)],
'q-9961': [('c0',),('all',),('correct',),('c6',),('0',)],
'q-9913': [('-r1','r1'),('0',),('-r1','0'),('correct',),('-r1',)],
'q-128506': [('c0',),('correct',),('-(c1-c0)','c0'),('r1',),('-c1','c4')],
}
LEVEL_REPAIRS={'q-9657':'moderate','q-9852':'hard'}
class Rejected(ValueError): pass

def tex(expr): return sp.latex(sp.sympify(expr)).replace(r'\left', '').replace(r'\right','')
def block(s): return '$$\n'+s+'\n$$'
def aligned(rows): return block(r'\begin{aligned}'+' \\\\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}')
def mat_tex(m,det=False):
    inner=r'\begin{aligned}'+' \\\\ '.join(' & '.join(tex(x) for x in row) for row in m.tolist())+r'\end{aligned}'
    return '|'+inner+'|' if det else '['+inner+']'
def owned(kind,key): return str(uuid.uuid5(NS,kind+':'+key))
def fingerprint(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def parse_math(s):
    """Small exact parser for the integer, rational and radical source fragments."""
    s=s.strip().replace('$','').replace('−','-').replace(r'\,','').replace(' ','')
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
    while r'\frac' in s:
        s,n=re.subn(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
        if not n:
            s=s.replace(r'\sqrt{43}','sqrt(43)')
            if r'\frac' in s and not re.search(r'\\frac\{[^{}]+\}\{[^{}]+\}',s): raise ValueError(s)
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
    s=re.sub(r'(\d)(sqrt\()',r'\1*\2',s)
    return sp.sympify(s)

def source_definitions():
    wrapper=json.loads((EVIDENCE/'source.json').read_text())
    defs={}
    for q in wrapper['record'][':knowledge-point/questions']:
        sid=q[':question/math-academy-id']; prompt=q[':question/problem']
        m=re.search(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]|\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S)
        inner=m.group(1) or m.group(2)
        var=re.search(r'(?:constant |values of |value of )\$([a-z])',prompt)
        if var: var=var.group(1)
        else: var=next(ch for ch in 'kxypqzmn' if re.search(r'\b'+ch+r'\b',inner))
        vals=[]
        for raw in re.split(r'\\\\',inner):
            for item in raw.split('&'):
                s=item.strip().replace('{'+var+'}',var).replace('^','**').replace('{','').replace('}','')
                s=re.sub(r'(\d)('+var+r')',r'\1*\2',s)
                vals.append(sp.sympify(s,locals={var:X}))
        matrix=sp.Matrix(3,3,vals)
        singular='singular' in prompt
        if singular: target=sp.Integer(0)
        else:
            tail=prompt[m.end():]
            match=re.search(r'(?:=|is )\$?(-?\d+)',tail)
            target=sp.Integer(match.group(1))
        fields=q[':question/answer-fields']
        level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or LEVEL_REPAIRS[sid]
        layout=prompt[:m.start()]+'{matrix}'+prompt[m.end():]
        # Replace only the determinant number, never coefficients or variable labels.
        if not singular:
            layout=re.sub(r'(?<==)(-?\d+)', '{target}',layout) if 'det(' in prompt else re.sub(r'(is \$)(-?\d+)',r'\1{target}',layout)
        c=[int(sp.expand(v).coeff(X,0)) for v in vals]
        v=[int(sp.expand(t).coeff(X,1)) for t in vals]
        w=[int(sp.expand(t).coeff(X,2)) for t in vals]
        named=re.search(r'\$([A-Z])=\{matrix\}',layout)
        defs[sid]={'source':q,'level':level,'variable':var,'constants':c,'linear':v,'quadratic':w,'target':int(target),'singular':singular,'layout':layout,'named':named.group(1) if named else None,'kind':fields[0][':answer-field/type'][':db/ident'].split('/')[-1]}
    return wrapper,defs

SOURCE,DEFS=source_definitions()
CHECKBOX_RECIPES=json.loads((EVIDENCE/'checkbox-recipes.json').read_text())['questions']
ROMAN=('I','II','III','IV','V','VI','VII','VIII')
# Separate pedagogical templates from complete profiles and matrix-pattern recipes.
TEMPLATES={}
for sid,d in DEFS.items():
    d['template']=('identity_singular_radio' if d['level']=='hard' else
        ('linear_' if d['level']=='easy' else 'quadratic_')+
        ('singular_' if d['singular'] else 'named_determinant_' if d['named'] else 'determinant_')+d['kind'])
    if sid=='q-280540':d['template']='quadratic_square_determinant_blank'
    TEMPLATES.setdefault(d['template'],[]).append(sid)

def parameters(sid):
    d=DEFS[sid]
    return {'constants':d['constants'][:],'linear':d['linear'][:],'quadratic':d['quadratic'][:],'target':d['target']}

def build(sid,p):
    d=DEFS[sid]
    if set(p)!={'constants','linear','quadratic','target'}: raise ValueError('Expected constants, linear, quadratic, target')
    for key in ('constants','linear','quadratic'):
        if len(p[key])!=9 or any(type(n)!=int or abs(n)>100 for n in p[key]):raise ValueError('Nine integer coefficients in -100..100 required')
    if type(p['target'])!=int or abs(p['target'])>10000:raise ValueError('Integer target in -10000..10000 required')
    if p['linear']!=d['linear'] or p['quadratic']!=d['quadratic']:raise ValueError('Variable coefficient pattern must match the observed matrix recipe')
    if d['singular'] and p['target']!=0:raise ValueError('Singular matrix needs target zero')
    # Retain constant zeros and observed fixed-entry nonzero structure.
    if any((old==0)!=(new==0) for old,new in zip(d['constants'],p['constants'])):raise ValueError('Constant zero pattern must be retained')
    m=sp.Matrix(3,3,[c+v*X+w*X**2 for c,v,w in zip(p['constants'],p['linear'],p['quadratic'])])
    determinant=sp.expand(m.det()); residual=sp.Poly(determinant-p['target'],X)
    if d['level']=='hard':
        if determinant!=0:raise Rejected('Hard scope is an identity-singular matrix')
        roots=None
    else:
        degree=1 if d['level']=='easy' else 2
        if residual.degree()!=degree:raise Rejected('Wrong polynomial degree for source scope')
        roots=sorted(sp.solve(residual.as_expr(),X),key=lambda z: float(sp.re(z)))
        if len(roots)!=degree or any(r.is_real is not True for r in roots):raise Rejected('Need distinct real roots')
        if d['kind'] in ('radio','checkbox') and any(not r.is_Rational for r in roots):raise Rejected('Observed selection scope uses rational root sets')
        if degree==2 and d['singular'] and 0 not in roots:raise Rejected('Observed singular quadratics factor out the variable')
    A=residual.nth(2); B=residual.nth(1); C=residual.nth(0)
    env={**{f'c{i}':sp.Integer(v) for i,v in enumerate(p['constants'])},**{f'v{i}':sp.Integer(v) for i,v in enumerate(p['linear'])},'A':A,'B':B,'C':C,'D':sp.Integer(p['target']),'abs':sp.Abs}
    if roots:env.update(r0=roots[0],r1=roots[-1])
    return m,determinant,residual,roots,env

def candidate(recipe,env,roots):
    if recipe==('all',):return None
    if recipe==('correct',):return roots[:]
    return [sp.simplify(sp.sympify(s,locals=env)) for s in recipe]

def math_key(vals): return 'all-real' if vals is None else tuple(sorted(sp.srepr(x) for x in vals))
def answer_render(raw,values,var):
    if values is None:return raw.replace(re.search(r'\$([a-z])\$',raw).group(1),var) if '$' in raw else raw
    if '$' in raw:
        pieces=iter(values)
        return re.sub(r'\$[^$]+\$',lambda _: '$'+tex(next(pieces))+'$',raw)
    return tex(values[0])

def solution(sid,p,m,det,residual,roots):
    d=DEFS[sid]; var=d['variable']; symbol=sp.Symbol(var,real=True)
    render=lambda z:tex(z.subs(X,symbol))
    m=m.subs(X,symbol)
    opening=("First, let's use our formula to find an expression for the determinant in terms of $" if d['singular'] and d['kind'] in ('radio','checkbox') or sid=='q-280543' else "Let’s use our formula to find an expression for the determinant in terms of $" if sid in ('q-280540','q-280541') else "Let's use our formula to find an expression for the determinant in terms of $")+var+':$'
    terms=[]; minor_products=[]; minor_values=[]; expanded=[]; checks=[]
    for j,sgn in enumerate((1,-1,1)):
        a=m[0,j]; minor=m.minor_submatrix(0,j); b,c,e,f=list(minor)
        lead=tex(a); prefix=('+' if j==2 else '-' if j==1 else '')
        if a.could_extract_minus_sign() or a.is_Add:lead='('+lead+')'
        terms.append(prefix+lead+mat_tex(minor,True))
        value=sp.expand(b*f-c*e)
        minor_products.append(prefix+lead+r'\big('+tex(b*f)+'-('+tex(c*e)+r')\big)')
        minor_values.append(prefix+lead+'('+tex(value)+')')
        expanded.append(sp.expand(sgn*a*value))
        checks.append({'coefficient':sp.srepr(a),'minor':[[sp.srepr(t) for t in row] for row in minor.tolist()],'value':sp.srepr(value),'signed_product':sp.srepr(expanded[-1])})
    # Shared source style: minors, product differences, simplified minors,
    # distributed products, combined determinant, then solve the resulting equation.
    sumtex=''.join(('+' if i and not tex(e).lstrip().startswith('-') else '')+tex(e) for i,e in enumerate(expanded))
    stage_map={
        'q-9657':'tmvf','q-9669':'tmvpf','q-9852':'tmvf',
        'q-128500':'ntvf','q-128502':'ntvf','q-130575':'tvpf',
        'q-130580':'tvpf','q-130620':'tvpf','q-130626':'tvpf',
        'q-18252':'tvpf','q-18256':'tvpf','q-18271':'ntvpf',
        'q-18272':'ntvpf','q-280403':'ntmvpf','q-280404':'ntmvpf',
        'q-280519':'ntvpf','q-280540':'ntmvpf','q-280541':'ntmvpf',
        'q-9911':'tmvpf','q-9961':'tvf','q-280402':'ntmevpf',
        'q-280543':'tvepf','q-9913':'tvf','q-128506':'tvpf'}
    initial_label=(r'\text{det}('+d['named']+')') if d['named'] else 'det(A)' if sid in ('q-280540','q-280541') else 'det'
    stages={'n':(initial_label,mat_tex(m,True)),
            't':(mat_tex(m,True) if 'n' not in stage_map[sid] else '', ''.join(terms)),
            'm':('',''.join(minor_products)), 'v':('',''.join(minor_values)),
            'e':('', ''.join(('+' if j and (a.is_Add or not tex(a).lstrip().startswith('-')) else '')+('('+tex(a)+')' if a.is_Add else tex(a))+r'\big('+tex(b)+r'\big)' for j,(a,b) in enumerate(zip((m[0,0],-m[0,1],m[0,2]), [sp.expand(m.minor_submatrix(0,k).det()) for k in range(3)])))),
            'p':('',sumtex),'f':('',render(det))}
    if sid=='q-9913':stages['f']=('',var+'('+render(sp.cancel(det/X))+')')
    rows=[stages[stage] for stage in stage_map[sid]]
    result=opening+'\n\n'+aligned(rows)
    if roots is None:
        result+='\n\nTherefore, this matrix is singular for all values of $'+var+'.$'
        return result,checks
    since='Since the matrix is singular, the determinant is $0,$ and we have' if d['singular'] else 'Since the determinant of the matrix is $'+tex(p['target'])+',$ we have'
    if sid in ('q-18252','q-9913'):
        since='Since the matrix is singular, the determinant is $0.$ So,  we have'
    elif sid in ('q-280540','q-280541'):
        since='Since the determinant of the matrix is $'+tex(p['target'])+'$, we have'
    if d['kind'] in ('radio','checkbox'):since+=':'
    eqrows=[((var+'('+render(sp.cancel(det/X))+')') if sid=='q-9913' else render(det),tex(p['target']))]
    a,b,c=residual.nth(2),residual.nth(1),residual.nth(0)
    if residual.degree()==1:
        if sid not in ('q-9669','q-130620','q-18271'):eqrows.append((render(b*X),tex(-c)))
        if sid=='q-18252':eqrows.append((var,r'\frac{'+tex(-c)+'}{'+tex(b)+'}'))
        eqrows.append((var,tex(roots[0])+('.' if d['kind']=='blank' else '')))
    elif d['singular']:
        eqrows.append((render(sp.factor(residual.as_expr())), '0'))
        if sid!='q-9911':eqrows.append((var,',\\,'.join(tex(r) for r in roots)))
    elif sid=='q-280540':
        eqrows.extend([(render(a*X**2),tex(-c)),(var+'^2',tex(-c/a)),(var,r'\pm\sqrt{'+tex(-c/a)+'}'),('',r'\pm '+tex(roots[1]))])
    else:
        disc=sp.expand(b*b-4*a*c)
        # Preserve the source formula method while correcting q-280541's lost ±.
        aa,bb,cc=(a,b,c) if a>0 else (-a,-b,-c)
        if a<0 and sid=='q-18256':eqrows.append((render(residual.as_expr()),'0'))
        eqrows.append((render(aa*X**2+bb*X+cc),'0'))
        if sid=='q-18272':
            common=sp.igcd(sp.igcd(int(aa),int(bb)),int(cc))
            aa,bb,cc=(z/common for z in (aa,bb,cc))
            eqrows.append((render(aa*X**2+bb*X+cc),'0'))
        disc=sp.expand(bb*bb-4*aa*cc)
        eqrows.extend([(var,r'\frac{-('+tex(bb)+r')\pm\sqrt{('+tex(bb)+r')^2-4\cdot '+tex(aa)+r'\cdot ('+tex(cc)+r')}}{2\cdot '+tex(aa)+'}'),('',r'\frac{'+tex(-bb)+r'\pm\sqrt{'+tex(disc)+'}}{'+tex(2*aa)+'}'),('',r'\frac{'+tex(-bb)+r'\pm '+tex(sp.sqrt(disc))+'}{'+tex(2*aa)+'}')])
        if sid not in ('q-18272','q-280541'):eqrows.append(('',','.join(tex(r) for r in roots)))
    result+='\n\n'+since+'\n\n'+aligned(eqrows)
    if len(roots)==2:
        order=('in ascending order, ' if sid=='q-280543' else '**in ascending order**, ') if d['kind']=='blank' else ''
        result+='\n\nTherefore, '+order+'the solutions are $'+var+'='+tex(roots[0])+'$ and $'+var+'='+tex(roots[1])+'.$'
    elif d['singular'] and d['kind'] in ('radio','checkbox'): result+='\n\nTherefore, the solution is $'+var+'='+tex(roots[0])+'.$'
    return result,checks

def sample(sid,rng):
    p=parameters(sid); d=DEFS[sid]
    if d['level']=='hard':
        if sid=='q-130626':
            # Row 2 = -2 row 1 is retained; variable coefficients fixed.
            p['constants'][0]=rng.randint(1,5);p['constants'][2]=rng.randint(1,6)
            p['constants'][3]=-2*p['constants'][0];p['constants'][5]=-2*p['constants'][2]
            p['constants'][6]=rng.choice((-3,-2,-1,1,2,3));p['constants'][7]=rng.choice((-3,-2,-1,1,2,3));p['constants'][8]=rng.randint(1,4)
        else:
            for i in (1,4,7):p['constants'][i]=rng.randint(2,12)
        return p
    # Small signed constant changes retain every zero and variable position.
    eligible=[i for i,n in enumerate(p['constants']) if n]
    for i in rng.sample(eligible,min(2,len(eligible))):
        p['constants'][i]=rng.choice((-5,-4,-3,-2,-1,1,2,3,4,5))
    if not d['singular']:
        if d['level']=='easy':p['target']=rng.randint(-50,80)
        elif sid=='q-280540':p['target']=rng.randint(2,50)
        else:
            # The target is derived by evaluating the new determinant at a
            # small integer root. This guarantees one rational root, then the
            # whole-instance validator requires two distinct rational roots.
            m=sp.Matrix(3,3,[c+v*X+w*X**2 for c,v,w in zip(p['constants'],p['linear'],p['quadratic'])])
            p['target']=int(m.det().subs(X,rng.randint(-8,8)))
    return p

def authored_bank(sid,env,roots,m):
    """One complete operation-derived bank, selected before collision rejection."""
    d=DEFS[sid]
    if d['level']=='easy':
        if any(recipe==('all',) for recipe in BANKS[sid]):
            # Preserve the source's unique-solution versus identity distinction.
            return [roots,None,[-roots[0]],[-env['C']],[env['B']]], ['solve','all_real_numbers','reverse_numerator_sign','omit_coefficient_division','report_linear_coefficient']
        # Correct; reverse isolated numerator; omit division; report slope;
        # report the constant term. The latter two answer an intermediate.
        return [roots,[-roots[0]],[-env['C']], [env['B']], [env['C']]], ['solve','reverse_numerator_sign','omit_coefficient_division','report_linear_coefficient','report_constant']
    if d['level']=='moderate':
        if d['singular']:
            nonzero=next(r for r in roots if r!=0)
            return [roots,[sp.Integer(0)],[nonzero],[-nonzero],[sp.Integer(0),-nonzero]], ['solve','lose_nonzero_root','lose_zero_root','reverse_nonzero_root','reverse_nonzero_root_keep_zero']
        return [roots,[-r for r in roots],[roots[0]],[roots[1]],[sp.Integer(0),-env['B']/env['A']]], ['solve','reverse_formula_linear_sign','lose_upper_root','lose_lower_root','omit_constant_term']
    if sid=='q-9852':
        return [None,[sp.Integer(0)],[env['c1']/env['v2']],[env['c4']/env['v5']],[env['c7']/env['v8']]], ['identity','force_variable_column_zero','equate_first_row_columns','equate_second_row_columns','equate_third_row_columns']
    # Requiring each nonconstant minor alone to vanish incorrectly adds a
    # constraint to a determinant whose three terms cancel identically.
    vals=[]
    for j in (0,2):
        equation=m.minor_submatrix(0,j).det()
        rr=sp.solve(equation,X)
        if len(rr)!=1:raise Rejected('Authored hard minor bank needs linear minors')
        vals.append(rr[0])
    return [None,[sp.Integer(0)],[vals[0]],[vals[1]],[vals[0],vals[1]]], ['identity','force_parameter_zero','force_first_minor_zero','force_third_minor_zero','union_of_minor_roots']

def assemble(sid,p,seed,authored=False):
    d=DEFS[sid]; authored=authored and d['kind'] in ('radio','checkbox'); m,det,residual,roots,env=build(sid,p)
    sourcefields=d['source'][':question/answer-fields']
    ordered=sorted(sourcefields,key=lambda f:f[':answer-field/key'])
    specifications=[]
    if d['kind']=='radio':
        raw=sourcefields[0][':answer-field/choices']; recipes=BANKS[sid]
        if authored:
            values,labels=authored_bank(sid,env,roots,m); recipes=[(label,) for label in labels]
        else: values=[candidate(recipe,env,roots) for recipe in recipes]
        if len(set(math_key(v) for v in values))!=len(values):raise Rejected('Whole profile has equivalent options')
        if sum(math_key(v)==math_key(roots) for v in values)!=1:raise Rejected('Whole profile lacks exactly one correct option')
        for a,recipe,value in zip(raw,recipes,values):
            if value is not None and any(v.is_real is not True or v.has(sp.zoo,sp.nan) for v in value):raise Rejected('Invalid option')
            if authored:
                typ=':answer.type/math' if d['level']=='easy' and value is not None else ':answer.type/text'
                rendered=tex(value[0]) if typ.endswith('/math') else ('Any real number' if d['level']=='easy' else 'Any value of $'+d['variable']+'$') if value is None else ' and '.join('$'+tex(v)+'$' for v in value)+' only'
            else: typ=a[':answer/type'][':db/ident'];rendered=answer_render(a[':answer/value'],value,d['variable'])
            specifications.append((typ,rendered,value,recipe))
    elif d['kind']=='checkbox':
        assert roots is not None
        env.update(r0=roots[0],r1=roots[-1])
        if authored:
            complete,labels=authored_bank(sid,env,roots,m)
            pool={sp.srepr(sp.simplify(v)):(sp.simplify(v),label) for values,label in zip(complete,labels) for v in values}
            options=[{'label':label,'atom':v,'recipe':recipe} for label,(v,recipe) in zip(ROMAN,sorted(pool.values(),key=lambda item:float(item[0])))]
            if len(pool)>len(ROMAN) or len(pool)<=len(roots):raise Rejected('Authored checkbox pool requires both roots and a distractor')
        else:
            options=[{'label':item['label'],'atom':sp.simplify(sp.sympify(item['expression'],locals=env)),'recipe':item['expression']} for item in CHECKBOX_RECIPES[sid]]
        if any(v['atom'].is_real is not True or v['atom'].is_finite is not True for v in options):raise Rejected('Invalid checkbox value')
        if len({sp.srepr(v['atom']) for v in options})!=len(options):raise Rejected('Checkbox option atoms collide')
        if not all(any(sp.simplify(root-v['atom'])==0 for v in options) for root in roots):raise Rejected('Checkbox pool lacks a root')
        ordered=[{':answer-field/key':item['label']} for item in options]
        for item in options:
            correct=any(sp.simplify(item['atom']-root)==0 for root in roots)
            specifications.append((':answer.type/text','true' if correct else 'false',[item['atom']],(item['recipe'],)))
    else:
        for f,r in zip(ordered,roots):
            specifications.append((':answer.type/math',tex(r),[r],('correct',)))
    prompt=d['layout'].replace('{matrix}',mat_tex(m.subs(X,sp.Symbol(d['variable'],real=True)))).replace('{target}',tex(p['target']))
    if d['kind']=='checkbox':
        prompt=prompt[:prompt.index('- **I.**')]+ '\n'.join('- **'+item['label']+'.** $'+d['variable']+'='+tex(item['atom'])+'$' for item in options)
    if sid in LEVEL_REPAIRS:
        prompt=prompt.replace('[\\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
    worked,checks=solution(sid,p,m,det,residual,roots)
    parameter_key=fingerprint({'matrix':[[sp.srepr(e) for e in row] for row in m.tolist()],'target':p['target'],'variable':d['variable']})
    content_key=fingerprint({'version':VERSION,'parameter':parameter_key,'profile':('authored:'+sid if authored else sid),'problem':prompt,'solution':worked,'fields':[f[':answer-field/key'] for f in ordered],'bank':[(a,v,math_key(vals)) for a,v,vals,_ in specifications]})
    qid=owned('question',content_key)
    fields=[]
    for index,f in enumerate(ordered):
        key=f[':answer-field/key'];fid=owned('field',qid+':'+key)
        if d['kind']=='checkbox':
            typ,correct_value,vals,recipe=specifications[index]
            items=[(typ,value,vals,recipe) for value in ('false','true')]
        else:
            items=specifications if d['kind']=='radio' else [specifications[index]]
        answers=[];correct_id=None
        for typ,value,vals,recipe in items:
            aid=owned('answer',fid+':'+typ+':'+value)
            answers.append({':answer/id':aid,':answer/type':typ,':answer/value':value})
            if d['kind']=='checkbox':
                if value==correct_value:correct_id=aid
            elif d['kind']=='blank' or math_key(vals)==math_key(roots):correct_id=aid
        random.Random(seed).shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+d['kind'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+d['level'],':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':fields},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':d['template'],'matrix_recipe':sid,'bank_profile':('authored:'+sid if authored else sid) if d['kind'] in ('radio','checkbox') else None,'bank_origin':'authored operation-derived complete bank' if authored else 'observed values; unknown intent; coefficient expressions for evidence replay' if d['kind'] in ('radio','checkbox') else 'observed','parameters':p,'parameter_fingerprint':parameter_key,'content_fingerprint':content_key,'source_analysis':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'question_ids':[sid]},'authored_level_assignment':sid in LEVEL_REPAIRS,'authored_extension':authored or p!=parameters(sid),'domain':'real variable; degree and distinct-root restrictions per source','matrix':[[sp.srepr(e) for e in row] for row in m.tolist()],'determinant':sp.srepr(det),'residual':sp.srepr(residual.as_expr()),'roots':None if roots is None else [sp.srepr(r) for r in roots],'choice_math':[{'type':t,'value':v,'set':None if vals is None else [sp.srepr(x) for x in vals],'recipe':list(rec)} for t,v,vals,rec in specifications],'option_math':[{'label':v['label'],'atom':sp.srepr(v['atom']),'recipe':v['recipe']} for v in options] if d['kind']=='checkbox' else [],'solution_intermediates':checks,'plot_rating':'none','plot_assets':{},'source_repairs':['Missing source difficulty; authored level assignment. Database key is present and preserved; generator supplies a full derivation for the brief authored database solution.'] if sid in LEVEL_REPAIRS else ['Corrected source det(F) label to det(A)'] if sid=='q-280403' else ['Corrected source quadratic formula intermediate + to ±'] if sid=='q-280541' else []}}

def mixed_hard_options(anchors):
    """Choose this bank before the matrix, independently of the correct outcome."""
    r,s=map(sp.Integer,anchors)
    return [None,[r],[s],sorted([r,s]),sorted([-r,-s])]

def build_mixed_hard(p):
    if set(p)!={'constants','linear','quadratic','target','option_roots'}:
        raise ValueError('Mixed hard requires coefficient arrays, target, and option_roots')
    for key in ('constants','linear','quadratic'):
        if not isinstance(p[key],list) or len(p[key])!=9 or any(type(v)!=int or abs(v)>100 for v in p[key]):
            raise ValueError('Nine integer coefficients in -100..100 required')
    if any(p['quadratic']) or type(p['target'])!=int or p['target']!=0:
        raise ValueError('Mixed hard uses affine entries and target zero')
    anchors=p['option_roots']
    if not isinstance(anchors,list) or len(anchors)!=2 or any(type(v)!=int or not 1<=abs(v)<=6 for v in anchors):
        raise ValueError('Two nonzero integer option roots in -6..6 required')
    if anchors[0] in (anchors[1],-anchors[1]):raise ValueError('Option roots must be distinct and not opposites')
    m=sp.Matrix(3,3,[c+v*X for c,v in zip(p['constants'],p['linear'])])
    determinant=sp.expand(m.det());poly=sp.Poly(determinant,X)
    if poly.is_zero:roots=None
    else:
        if poly.degree() not in (1,2):raise ValueError('Mixed hard requires an identity, linear or quadratic equation')
        roots=sorted(sp.solve(poly.as_expr(),X),key=lambda v:float(sp.re(v)))
        if len(roots)!=poly.degree() or any(r.is_real is not True for r in roots):
            raise ValueError('Finite cases need distinct real solutions')
    options=mixed_hard_options(anchors)
    if sum(math_key(v)==math_key(roots) for v in options)!=1:
        raise ValueError('The complete root set must match exactly one supplied option')
    return m,determinant,poly,roots,options

def sample_mixed_hard(rng,anchors,correct):
    # A small affine 2x2 block determines the solution set. Invertible integer
    # row/column operations hide its construction without changing its roots.
    # One constant row keeps all cofactor contributions at degree at most two.
    first=anchors[0] if correct is None else int(correct[0])
    scale=rng.choice((-2,-1,1,2))
    last=0 if correct is None else scale if len(correct)==1 else scale*(X-correct[1])
    m=sp.Matrix([[X-first,1,0],[0,last,0],[0,0,1]])
    for dest,src in ((0,1),(1,0)):
        factor=rng.choice((-1,1));m.row_op(dest,lambda value,j:value+factor*m[src,j])
    for dest in (0,1):
        factor=rng.choice((-2,-1,1,2));m.row_op(dest,lambda value,j:value+factor*m[2,j])
    for dest,src in ((0,2),(1,0),(2,1),(0,1)):
        factor=rng.choice((-1,1));m.col_op(dest,lambda value,i:value+factor*m[i,src])
    rows=list(range(3));cols=list(range(3));rng.shuffle(rows);rng.shuffle(cols)
    m=m.extract(rows,cols).applyfunc(sp.expand)
    if any(v==0 for v in m) or sum(v.has(X) for v in m)!=6:
        raise Rejected('Keep the same dense affine-entry layout across outcomes')
    constants=[int(v.coeff(X,0)) for v in m];linear=[int(v.coeff(X,1)) for v in m]
    if max(map(abs,constants))>24 or max(map(abs,linear))>12:
        raise Rejected('Mixed hard matrix coefficients exceed the arithmetic bound')
    terms=[sp.Poly(sp.expand((-1)**j*m[0,j]*m.minor_submatrix(0,j).det()),X) for j in range(3)]
    if any(t.degree()>2 or any(abs(c)>120 for c in t.all_coeffs()) for t in terms):
        raise Rejected('Mixed hard cofactor arithmetic exceeds its degree/coefficient bound')
    return {'constants':constants,'linear':linear,'quadratic':[0]*9,'target':0,'option_roots':list(anchors)}

def generate_mixed_hard(seed=0,parameters=None):
    rng=random.Random(seed)
    if parameters is None:
        anchors=rng.sample((-4,-3,-2,-1,1,2,3,4),2)
        while anchors[0]==-anchors[1]:anchors=rng.sample((-4,-3,-2,-1,1,2,3,4),2)
        # All five answers can be correct. Select the answer before rejection,
        # so different acceptance rates cannot bias practice toward identities.
        correct=rng.choice(mixed_hard_options(anchors))
        for _ in range(256):
            try:
                p=sample_mixed_hard(rng,anchors,correct)
                m,det,poly,roots,options=build_mixed_hard(p)
                if math_key(roots)!=math_key(correct):raise AssertionError('Construction changed the selected solution set')
                break
            except Rejected:pass
        else:raise Rejected('Bounded mixed-hard sampling failed')
    else:
        p={k:v[:] if isinstance(v,list) else v for k,v in parameters.items()}
        m,det,poly,roots,options=build_mixed_hard(p)
    var='p';symbol=sp.Symbol(var,real=True)
    prompt='Find all real values of $p$ for which the following matrix is singular.\n\n'+block(mat_tex(m.subs(X,symbol)))
    # Reuse the observed cofactor -> collect -> solve renderer. It chooses the
    # solving step from the actual polynomial degree, not the difficulty label.
    worked,checks=solution('q-130626',p,m,det,poly,roots)
    rendered=['Any value of $p$' if vals is None else ' and '.join('$'+tex(v)+'$' for v in vals)+' only' for vals in options]
    parameter_key=fingerprint({'matrix':[[sp.srepr(e) for e in row] for row in m.tolist()],'target':0,'variable':var})
    content_key=fingerprint({'version':VERSION,'parameter':parameter_key,'profile':HARD_MIXED_PROFILE,'problem':prompt,'solution':worked,'bank':sorted(rendered)})
    qid=owned('question',content_key);fid=owned('field',qid+':selection')
    answers=[{':answer/id':owned('answer',fid+':text:'+text),':answer/type':':answer.type/text',':answer/value':text} for text in rendered]
    correct_id=next(a[':answer/id'] for a,vals in zip(answers,options) if math_key(vals)==math_key(roots))
    random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/hard',':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[field]},
        'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':HARD_MIXED_TEMPLATE,'matrix_recipe':HARD_MIXED_PROFILE,'bank_profile':HARD_MIXED_PROFILE,
            'bank_origin':'authored common bank, selected before the solution outcome','parameters':p,'parameter_fingerprint':parameter_key,'content_fingerprint':content_key,
            'source_analysis':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'question_ids':[],
                'reference_question_ids':['q-130626','q-9852','q-9669','q-18272']},'authored_level_assignment':True,'authored_extension':True,
            'domain':'real variable; identity, linear or two-distinct-root quadratic singularity equation','solution_class':'all_real' if roots is None else 'one_value' if len(roots)==1 else 'two_values',
            'matrix':[[sp.srepr(e) for e in row] for row in m.tolist()],'determinant':sp.srepr(det),'residual':sp.srepr(poly.as_expr()),'roots':None if roots is None else [sp.srepr(r) for r in roots],
            'choice_math':[{'type':':answer.type/text','value':text,'set':None if vals is None else [sp.srepr(v) for v in vals],'recipe':['common_candidate_set']} for text,vals in zip(rendered,options)],
            'option_math':[],'solution_intermediates':checks,'plot_rating':'none','plot_assets':{},'source_repairs':[]}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if profile==HARD_MIXED_PROFILE or template==HARD_MIXED_TEMPLATE or level=='hard' and profile is None and template is None:
        if level!='hard' or template not in (None,HARD_MIXED_TEMPLATE) or profile not in (None,HARD_MIXED_PROFILE) or field_type not in (None,'radio'):
            raise ValueError('Mixed hard practice requires hard difficulty and a radio field')
        return generate_mixed_hard(seed,parameters)
    eligible=[sid for sid,d in DEFS.items() if d['level']==level and (template is None or d['template']==template) and (field_type is None or d['kind']==field_type)]
    authored=profile is None or profile.startswith('authored:')
    if profile is not None:
        profile=profile.removeprefix('authored:')
        if profile not in eligible:raise ValueError('Profile does not belong to requested level/template/field type')
        eligible=[profile]
    if not eligible:raise ValueError('No matching observed matrix recipe')
    if parameters is not None and profile is None and len(eligible)>1:raise ValueError('Explicit parameters need an explicit profile or unambiguous template')
    rng=random.Random(seed);sid=rng.choice(eligible)
    if parameters is not None:return assemble(sid,parameters,seed,authored)
    for _ in range(256):
        try:return assemble(sid,sample(sid,rng),seed,authored)
        except Rejected:pass
    raise Rejected('Bounded whole-profile sampling failed')

# EASY: one affine determinant equation; named/unnamed and singular layouts.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: quadratic determinant equations, factorization/formula/square roots.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored identity/linear/quadratic practice; source profiles stay explicit.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];g=record['generation'];lines=[q[':question/problem'],'']
    for f in q[':question/answer-fields']:
        lines.append('Field `'+f[':answer-field/key']+'` ('+f[':answer-field/type'].split('/')[-1]+')')
        for a in f[':answer-field/choices']:
            suffix=' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''
            lines.append('- '+a[':answer/value']+suffix)
    return '\n'.join(lines)+ '\n\n**Worked solution**\n\n'+q[':question/worked-solution']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template',choices=list(TEMPLATES)+[HARD_MIXED_TEMPLATE]);parser.add_argument('--profile',choices=list(DEFS)+['authored:'+sid for sid,d in DEFS.items() if d['kind'] in ('radio','checkbox')]+[HARD_MIXED_PROFILE]);parser.add_argument('--field-type',choices=('radio','checkbox','blank'))
    a=parser.parse_args()
    if a.count<1:parser.error('count must be positive')
    if a.difficulty=='all' and (a.template or a.profile):parser.error('Select one difficulty with --template or --profile')
    levels=('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)
    rows=[generate(level,a.seed+i,a.template,a.field_type,profile=a.profile) for level in levels for i in range(a.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
