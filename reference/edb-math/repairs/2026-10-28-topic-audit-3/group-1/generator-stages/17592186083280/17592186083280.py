#!/usr/bin/env python3
"""Normal orientation generators; frozen math basis 1356. No database operations.

Observed masks preserve all source prose and stages. Raw observed profiles preserve
attribute omissions and opaque banks and are evidence-only where documented.
Normal defaults use every family with supported complete banks. Hard is an authored
two-period version of the shifted trig family: four familiar roots, not new algebra.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
T=s.Symbol('t',real=True); VERSION='normal-orientation-2-format-audit-9837-v1'
HARD_PHASES=tuple(s.Rational(n,d)for n,d in ((1,6),(1,4),(1,3),(2,3),(3,4),(5,6)))
HARD_PHASE_INPUTS=HARD_PHASES+tuple(v+1 for v in HARD_PHASES)
HARD_INTERVAL_SHIFTS=tuple(range(6))
NS=uuid.UUID(KP[':knowledge-point/id'])

def tex(v):
    return re.sub(r'(?<=\d) (?=\\)', '', s.latex(s.sympify(v))).replace(r'\log',r'\ln').replace('- ', '-')
def signed(v): return ('+' if v>=0 else '')+str(v)
def rat(v): return tex(v)
def exp(k,arg='t'): return '{e}^{'+str(k)+arg+'}'
def lin(a,b): return f'{a}t'+('+'+str(b) if b>=0 else str(b))
def uid(v): return str(uuid.uuid5(NS,v))
def digest(v): return hashlib.sha256(json.dumps(_ca_material(v),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def mask(text,old,new):
    assert len(old)==len(new)
    # Replacements are complete mathematical components, never numeric substrings.
    for i,x in enumerate(old):
        assert x in text,(x,text)
        text=text.replace(x,f'@@SLOT{i}@@')
    for i,x in enumerate(new):text=text.replace(f'@@SLOT{i}@@',x)
    return text

TEMPLATES={
 'exponential':('easy','q-21207',{'k':2,'b':1,'u':2,'c':0}),
 'logarithmic':('easy','q-122947',{'k':2,'m':2}),
 'quadratic':('easy','q-350403',{'b':1,'c':8,'a':2}),
 'cubic':('moderate','q-122946',{'a':2,'n':3,'l':7,'h':1}),
 'shifted_trig':('moderate','q-350414',{'a':4,'b':4,'h':8,'j':-5,'p':'1/3'}),
 'frequency_trig':('moderate','q-75278',{'a':2,'b':3,'h':-11,'j':5,'k':4}),
 'legacy_trig':('moderate','q-21080',{'a':4,'b':5,'h':5,'j':4,'k':2}),
 'two_period_trig':('hard',None,{'a':4,'b':3,'h':2,'j':-1,'k':2,'p':'1/3','q':0}),
}

def components(name,p):
    """Full prompt math, derivative, zero-equation, nonzero-check, conclusion slots."""
    if name=='exponential':
        k,b,u,c=map(s.Integer,(p['k'],p['b'],p['u'],p['c']));r=c/(2*b);lead='' if b==1 else str(b)
        y=f'{lead}{{t}}^{{2}}'+(f'-{c}t' if c else '')
        dy=f'{2*b}t'+(f'-{c}' if c else '')
        prompt=f'x={exp(k)},\\,y={y},\\,0\\le t\\le {u}.'
        deriv=f'{{x}}^{{′}}(t)={k}{exp(k)},\\,{{y}}^{{′}}(t)={dy}'
        solve=f'{dy}=0\\,⟹\\,t={tex(r)}.'
        check=f'{{x}}^{{′}}({tex(r)})={k}{{e}}^{{{tex(k*r)}}}={tex(k*s.exp(k*r))}\\ne 0,\\,\\,'
        return [prompt,deriv,solve,check], [r], (s.exp(k*T),b*T*T-c*T), 'vertical'
    if name=='logarithmic':
        k,m=map(s.Integer,(p['k'],p['m'])); r=1/k
        prompt=f'x=\\operatorname{{ln}}⁡(\\pi t)-{k}t,\\,y={exp(m)},\\,0<t<\\infty .'
        deriv=f'{{x}}^{{′}}(t)=\\frac{{1}}{{t}}-{k},\\,{{y}}^{{′}}(t)={m}{exp(m)}'
        solve=f'\\frac{{1}}{{t}}-{k}=0\\,⟹\\,t={tex(r)}.'
        # Keep unevaluated substituted product, then actual exponential value.
        val=m*s.exp(m*r); valtex=(str(m)+'e') if m*r==1 else tex(val)
        check=f'{{y}}^{{′}}({tex(r)})={m}{{e}}^{{{m}\\times (1/{k})}}={valtex}\\ne 0,\\,\\,'
        return [prompt,deriv,solve,check], [r], (s.log(s.pi*T)-k*T,s.exp(m*T)), 'horizontal'
    if name=='quadratic':
        b,c,a=map(s.Integer,(p['b'],p['c'],p['a']));r=c/(2*b); lead='' if b==1 else str(b)
        prompt=f'x={lead}{{t}}^{{2}}-{c}t,\\,y={a}{{t}}^{{3}}.'
        deriv=f'{{x}}^{{′}}(t)={2*b}t-{c},\\,{{y}}^{{′}}(t)={3*a}{{t}}^{{2}}'
        solve=f'\\begin{{aligned}}{2*b}t-{c} & =0 \\\\ {2*b}t & ={c} \\\\ t & ={tex(r)}.\\end{{aligned}}'
        check=f'\\begin{{aligned}}{{y}}^{{′}}({tex(r)}) & ={3*a}{{({tex(r)})}}^{{2}}={tex(3*a*r*r)}\\ne 0,\\end{{aligned}}'
        return [prompt,deriv,solve,check],[r],(b*T*T-c*T,a*T**3),'horizontal'
    if name=='cubic':
        a,n,l,h=map(s.Integer,(p['a'],p['n'],p['l'],p['h']));r=s.sqrt(n)
        prompt=f'x={l}(t-{h}),\\,y={a}{{t}}^{{3}}-{3*a*n}t,\\,-\\infty <t<\\infty .'
        deriv=f'\\begin{{aligned}}{{x}}^{{′}}(t)={l},\\,{{y}}^{{′}}(t)={3*a}{{t}}^{{2}}-{3*a*n}.\\end{{aligned}}'
        solve=f'{3*a}({{t}}^{{2}}-{n})=0\\,⟹\\,t=\\pm {tex(r)}.'
        check=f'\\begin{{aligned}}{{x}}^{{′}}(-{tex(r)}) & ={l}\\ne 0, \\\\ {{x}}^{{′}}({tex(r)}) & ={l}\\ne 0,\\end{{aligned}}'
        return [prompt,deriv,solve,check],[-r,r],(l*(T-h),a*T**3-3*a*n*T),'vertical'
    a,b,h,j=map(s.Integer,(p['a'],p['b'],p['h'],p['j']))
    if name=='shifted_trig':
        phi=s.pi*s.Rational(p['p']);z='t-'+tex(phi); roots=[phi+s.pi/2,phi+3*s.pi/2]
        prompt=f'x={a}\\operatorname{{cos}}⁡({z})+{h},\\,y={b}\\operatorname{{sin}}⁡({z}){signed(j)},\\,0\\le t<2\\pi .'.replace('+-','-')
        deriv=f'{{x}}^{{′}}(t)=-{a}\\operatorname{{sin}}⁡({z}),\\,{{y}}^{{′}}(t)={b}\\operatorname{{cos}}⁡({z})'
        solve=f'{b}\\operatorname{{cos}}⁡({z})=0\\,⟹\\,t={tex(roots[0])},{tex(roots[1])}.'
        check=f'\\begin{{aligned}}{{x}}^{{′}}({tex(roots[0])}) & =-{a}\\ne 0, \\\\ {{x}}^{{′}}({tex(roots[1])}) & ={a}\\ne 0,\\end{{aligned}}'
        # Source TeX has spaces inside pi groups, preserved through formatter below.
        return [prompt,deriv,solve,check],roots,(a*s.cos(T-phi)+h,b*s.sin(T-phi)+j),'vertical'
    k=s.Integer(p['k']);r=s.pi/k; upper=2*s.pi/k
    if name=='legacy_trig':
        prompt=f'x = {a}\\cos {k}t {'+ '+str(h) if h>=0 else '- '+str(-h)}, y = {b}\\sin {k}t {'+ '+str(j) if j>=0 else '- '+str(-j)}, 0 \\le t < {tex(upper)}'
        return [prompt],[s.Integer(0),r],(a*s.cos(k*T)+h,b*s.sin(k*T)+j),'horizontal'
    prompt=f'x={a}\\operatorname{{cos}}⁡{k}t{signed(h)},\\,y={b}\\operatorname{{sin}}⁡{k}t{signed(j)},\\,0\\le t<{tex(upper)}.'
    deriv=f'\\begin{{aligned}}{{x}}^{{′}}(t)=-{a*k}\\operatorname{{sin}}⁡{k}t,\\,{{y}}^{{′}}(t)={b*k}\\operatorname{{cos}}⁡{k}t.\\end{{aligned}}'
    solve=f'-{a*k}\\operatorname{{sin}}⁡{k}t=0\\,⟹\\,t=0,{tex(r)}.'
    check=f'\\begin{{aligned}}{{y}}^{{′}}(0) & ={b*k}\\operatorname{{cos}}⁡(0)={b*k}\\ne 0, \\\\ {{y}}^{{′}}({tex(r)}) & ={b*k}\\operatorname{{cos}}⁡(\\pi )=-{b*k}\\ne 0,\\end{{aligned}}'
    return [prompt,deriv,solve,check],[s.Integer(0),r],(a*s.cos(k*T)+h,b*s.sin(k*T)+j),'horizontal'

# Source mathematical typography is part of each mask, including pi spacing.
def typography(name,blocks):
    if name in ('shifted_trig','frequency_trig'):
        blocks=[x.replace(r'\pi}',r'\pi }') for x in blocks]
    if name=='legacy_trig': blocks=[x.replace(r'\pi','π') for x in blocks]
    return blocks

def source_render(name,p):
    level,sid,anchor=TEMPLATES[name];src=Q[sid]
    old,oldroots,_,_=components(name,anchor);new,roots,xy,orientation=components(name,p)
    old=typography(name,old);new=typography(name,new)
    # Masks use captured block boundaries; derived anchor blocks are independently
    # compared in validator, rather than branch-returning any original payload.
    original_prompt=re.findall(r'\$\$\n(.*?)\n\$\$',src[':question/problem'],re.S)
    if not original_prompt: original_prompt=[re.search(r'\$(x = .*?)\$',src[':question/problem']).group(1)]
    original_solution=re.findall(r'\$\$\n(.*?)\n\$\$',src.get(':question/worked-solution',''),re.S)
    assert old==original_prompt+original_solution,(name,old,original_prompt+original_solution)
    prompt=mask(src[':question/problem'],old[:1],new[:1])
    solution=None
    if ':question/worked-solution' in src:
        solution=mask(src[':question/worked-solution'],old[1:],new[1:])
        oldcon=conclusion(name,oldroots);newcon=conclusion(name,roots)
        solution=mask(solution,[oldcon],[newcon])
    return prompt,solution,roots,xy,orientation

def conclusion(name,roots):
    if name=='cubic':return 't=\\pm '+tex(roots[-1])
    if name in ('shifted_trig','frequency_trig'):
        return 't='+typography(name,[tex(roots[0])])[0]+'$ and $t='+typography(name,[tex(roots[1])])[0]
    return 't='+tex(roots[0])

def bank(name,p,roots,raw):
    if name=='quadratic':return [[tex(roots[0])]],'math'
    if name=='shifted_trig':return [[typography(name,[tex(r)])[0]] for r in reversed(roots)],'math'
    if name=='exponential':
        u,b,c=map(s.Integer,(p['u'],p['b'],p['c']));vs=(u/2,u/6,u,u/4,s.Integer(0)) if raw else (c/(2*b),c/b,-c/(2*b),b/(2*c),s.sqrt(c/b))
        return [['t='+tex(v) for v in vs]],'math'
    if name=='logarithmic':
        k=s.Integer(p['k']);vs=(1/(2*k),-1/(2*k),-1/k,1/k,3/(2*k)) if raw else (1/k,k,-1/k,s.pi/k,1/(s.pi*k))
        return [['t='+tex(v) for v in vs]],'math'
    if name=='cubic':
        n=s.Integer(p['n']);vs=[s.sqrt(2*n/3),s.sqrt(2*n),3*s.sqrt(2*n/3),2*s.sqrt(n),s.sqrt(n)]
        if raw:
            # Preserve ± source strings, including its unsimplified radical factors.
            vals=['t=\\pm '+tex(v) for v in vs]
            return [vals],'math'
        return [['t=\\pm '+tex(s.sqrt(n)),'t=\\pm '+tex(s.sqrt(3*n)),'t='+tex(s.sqrt(n)),'t=-'+tex(s.sqrt(n)),'t=0']],'math'
    k=s.Integer(p['k']);r=s.pi/k
    if name=='legacy_trig':
        f=lambda z:tex(z).replace(r'\pi','π')
        return [[f'$t = 0$ and $t = {f(r)}$', '$t = 0$ only',f'$t = 0$ and $t = {f(2*r)}$',f'$t = {f(r)}$ only',f'$t = {f(2*r)}$ only']],'text'
    f=lambda z:tex(z).replace(r'\pi}',r'\pi }')
    if not raw:return [[f'$t=0$ and $t={f(r)}$',f'$t={f(r/2)}$ and $t={f(3*r/2)}$','$t=0$ only',f'$t={f(r)}$ only',f'$t=0$ and $t={f(2*r)}$']],'text'
    return [[f'$t={f(r)}$ and $t={f(s.pi/(k+2))}$',f'$t=0$ and $t={f(r)}$',f'$t={f(r)}$ only',f'$t=0$ and $t={f(s.pi/(k-1))}$',f'$t={f(r)}$ and $t={f(s.pi/(k-1))}$']],'text'

def check_parameters(name,p,raw):
    anchor=TEMPLATES[name][2]
    if set(p)!=set(anchor):raise ValueError('Exact parameter keys required')
    ints=[v for k,v in p.items() if k!='p']
    if any(s.sympify(v).is_Integer is not True for v in ints):raise ValueError('Integer parameters required')
    if name=='exponential': valid=1<=p['k']<=6 and 1<=p['b']<=5 and 2<=p['u']<=8 and (p['c']==0 if raw else 1<=p['c']<=12 and 0<p['c']/(2*p['b'])<=p['u'])
    elif name=='logarithmic':valid=2<=p['k']<=8 and 1<=p['m']<=6
    elif name=='quadratic':valid=1<=p['b']<=4 and 2<=p['c']<=24 and 1<=p['a']<=5
    elif name=='cubic':valid=1<=p['a']<=4 and 2<=p['n']<=12 and 1<=p['l']<=9 and 1<=p['h']<=4
    else:
        valid=1<=p['a']<=6 and 1<=p['b']<=6 and -12<=p['h']<=12 and -12<=p['j']<=12
        if 'k'in p: valid=valid and 2<=p['k']<=6
        if 'p'in p:valid=valid and s.Rational(p['p']) in (HARD_PHASE_INPUTS if name=='two_period_trig' else [s.Rational(1,d) for d in (3,4,6)])
        if name=='two_period_trig':valid=valid and p['q'] in HARD_INTERVAL_SHIFTS
        # Captured plus-sign masks require positive x offset for shifted family.
        if name=='shifted_trig':valid=valid and p['h']>=0
    if not valid:raise ValueError('Outside documented family workload bounds')

def sample(name,rng):
    p=dict(TEMPLATES[name][2])
    for key in ('a','b','l','m'):
        if key in p:p[key]=rng.randint(1,5)
    if 'k'in p:p['k']=rng.randint(2,6)
    if 'u'in p:p['u']=rng.randint(2,8)
    if 'c'in p:p['c']=rng.randint(2,24)
    if 'n'in p:p['n']=rng.randint(2,12);p['a']=rng.randint(1,4)
    if 'h'in p:p['h']=rng.randint(1,4) if name=='cubic' else rng.randint(0,12)
    if 'j'in p:p['j']=rng.randint(-12,12)
    if 'p'in p:p['p']=str(rng.choice([s.Rational(1,d) for d in (3,4,6)]))
    if name=='quadratic':p['b']=rng.randint(1,4)
    if name=='exponential':p['k']=rng.randint(1,6);p['c']=rng.randint(1,min(12,2*p['b']*p['u']))
    if name=='logarithmic':p['k']=rng.randint(2,8);p['m']=rng.randint(1,6)
    if name=='cubic':p['l']=rng.randint(1,9)
    if name in ('shifted_trig','frequency_trig','legacy_trig','two_period_trig'):
        p['a']=rng.randint(1,6);p['b']=rng.randint(1,6)
        if name!='shifted_trig':p['h']=rng.randint(-12,12)
    if name=='two_period_trig':p['p']=str(rng.choice(HARD_PHASES));p['q']=rng.choice(HARD_INTERVAL_SHIFTS)
    return p

# Easy: one scalar root, exponential/logarithmic or quadratic derivative.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: two complete familiar roots, companion-derivative checks and interval.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard (authored): identical trig method across two periods, four ordered roots.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def hard_render(p):
    a,b,h,j,k=map(s.Integer,(p['a'],p['b'],p['h'],p['j'],p['k']));phi=s.pi*s.Rational(p['p']);z=k*T-phi
    lower=s.Integer(p['q'])*s.pi/k;upper=lower+4*s.pi/k
    # Enumerate the cosine zeros whose actual parameters lie in [lower, upper).
    # A phase alias or shifted interval can change the first index and all signs.
    first=s.ceiling((k*lower-phi-s.pi/2)/s.pi)
    stop=s.ceiling((k*upper-phi-s.pi/2)/s.pi)
    roots=[s.simplify((phi+s.pi/2+n*s.pi)/k)for n in range(int(first),int(stop))]
    assert len(roots)==4 and all(lower<=r<upper for r in roots)
    curve=f'x={a}\\cos({tex(k)}t-{tex(phi)}){signed(h)},\\,y={b}\\sin({tex(k)}t-{tex(phi)}){signed(j)},\\,{tex(lower)}\\le t<{tex(upper)}.'
    prompt='A curve is defined by the parametric equations\n\n$$\n'+curve+'\n$$\n\nDetermine the values of $t$ at which the normal to the curve is vertical. Give exact answers in ascending order.\n\n'+', '.join('$t=$\n{{field-'+str(i+1)+'}}' for i in range(4))+'.'
    derivative=f'{{x}}^{{′}}(t)=-{a*k}\\sin({tex(k)}t-{tex(phi)}),\\,{{y}}^{{′}}(t)={b*k}\\cos({tex(k)}t-{tex(phi)})'
    roottext=', '.join(tex(r) for r in roots)
    checks=r'\begin{aligned}'+r' \\ '.join(f'{{x}}^{{′}}({tex(r)}) & ={tex(s.simplify(-a*k*s.sin(k*r-phi)))}\\ne 0,' for i,r in enumerate(roots))+r'\end{aligned}'
    solution='The normal is vertical if the tangent is horizontal. Therefore, we require ${y}^{′}(t)=0$ while ${x}^{′}(t)\\ne 0.$\n\nSo, we first find the derivatives of $x$ and $y:$\n\n$$\n'+derivative+'\n$$\n\nSolving ${y}^{′}(t)=0$ gives\n\n$$\n'+f'{b*k}\\cos({tex(k)}t-{tex(phi)})=0\\,⟹\\,t={roottext}.'+'\n$$\n\nNow, we note that\n\n$$\n'+checks+'\n$$\n\nwhich confirms that the normal to the curve is indeed vertical when $t='+roottext+'.$'
    return prompt,solution,roots,(a*s.cos(z)+h,b*s.sin(z)+j),'vertical'

def _generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    raw=bool(profile and profile.startswith('observed:'))
    if profile and not raw and profile!='authored':raise ValueError('Unknown profile')
    if raw:
        sid=profile.split(':',1)[1]; names=[n for n,v in TEMPLATES.items() if v[1]==sid]
        if not names:raise ValueError('Unknown source profile')
        if template and template!=names[0]:raise ValueError('Profile/template mismatch')
        template=names[0]
    rng=random.Random(seed)
    eligible=[n for n,v in TEMPLATES.items() if v[0]==level and (not field_type or ('blank' if n in ('quadratic','shifted_trig','two_period_trig') else 'radio')==field_type)]
    name=template or rng.choice(eligible)
    if name not in eligible:raise ValueError('Template/level/layout mismatch')
    p=dict(parameters) if parameters is not None else sample(name,rng)
    if raw and name=='exponential' and parameters is None:p['c']=0
    check_parameters(name,p,raw)
    prompt,solution,roots,xy,orientation=hard_render(p) if name=='two_period_trig' else source_render(name,p)
    sid=TEMPLATES[name][1];src=Q.get(sid,{})
    if name=='two_period_trig':banks=[[tex(r)]for r in roots];atype='math'
    else:banks,atype=bank(name,p,roots,raw)
    if not raw:
        prompt=prompt.replace('Do not round the answer.','Give an exact answer.').replace('Do not round the answers.','Give exact answers.')
        if name=='cubic':prompt=prompt.replace('Determine the points','Determine the values of $t$')
        if name=='legacy_trig':
            # Missing source designation/solution inferred mathematically; normal
            # presentation reuses the complete frequency-family stage recipe.
            siblingp=dict(p);base=TEMPLATES['frequency_trig'][2]
            _,solution,_,_,_=source_render('frequency_trig',siblingp)
    if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
    from mathcheck_17592186083280 import value_set,prompt_curve
    bank_keys=[[value_set(v) for v in bank]for bank in banks]
    if any(len(b)!=len(set(b))for b in bank_keys):raise ValueError('Whole bank rejected: duplicate options')
    if not raw:prompt=_ca_problem(prompt);solution=_ca_prose(solution);banks=[_ca_values(b)for b in banks]if atype=='math'else banks
    content={'level':None if raw and ':question/difficulty' not in src else level,'prompt':prompt,'solution':solution,'banks':banks,'types':atype}
    display_x,display_y,domain=prompt_curve({'question':{':question/problem':prompt}})
    target=s.diff(display_x if orientation=='horizontal'else display_y,T)
    incidental_bound=isinstance(domain,s.Interval) and domain.end.is_finite and target.is_polynomial(T) and s.solveset(target,T,domain=s.S.Reals)==s.FiniteSet(*roots)
    task={'orientation':orientation,'interval':None if incidental_bound else s.srepr(domain),'zero_candidates':[[s.srepr(r),s.simplify(s.diff(display_y if orientation=='horizontal'else display_x,T).subs(T,r))!=0]for r in roots]}
    # This KP assesses parameter zero sets and regularity, so independent nonzero
    # derivative multipliers, curve translations and answer banks are incidental.
    fingerprint=digest(task)
    identity=digest([VERSION,content]);qid=uid(identity)
    q={':question/id':qid,':question/problem':prompt}
    if solution is not None:q[':question/worked-solution']=solution
    if not raw or ':question/difficulty'in src:q[':question/difficulty']=':question.difficulty/'+level
    fields=[]
    sourcefields=src.get(':question/answer-fields',[])
    for i,values in enumerate(banks):
        typ='blank' if len(values)==1 else 'radio'; key=sourcefields[i][':answer-field/key'] if sourcefields else 'field-'+str(i+1)
        fid=uid(identity+':field:'+key)
        answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/'+atype,':answer/value':v}for v in values]
        f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':answers}
        correct_index={'exponential':4 if raw else 0,'logarithmic':3 if raw else 0,'cubic':4 if raw else 0,'legacy_trig':0,'frequency_trig':1 if raw else 0}.get(name,0)
        if not raw or ':answer-field/correct'in sourcefields[i]:f[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
        if typ=='radio':rng.shuffle(answers)
        fields.append(f)
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':name,'profile':profile or 'authored','seed':seed,'parameters':p,'source':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'source_id':sid,'mathematical_fingerprint':fingerprint,'mathematical_task':task,'content_identity':identity,'roots':[str(r)for r in roots],'curves':[str(v)for v in xy],'orientation':orientation,'domain':str(domain),'bank_recipe':('historical complete observed bank' if raw else {'exponential':'power derivative, omitted factor, sign, swapped coefficient ratio, dropped linear t/coordinate zero','logarithmic':'reciprocal, reciprocal lost, sign, extra/missing logarithm chain factor','cubic':'two derivative roots, omitted power factor, omitted negative/positive root, omitted linear derivative','frequency_trig':'sine zero pair, cosine zero pair, omitted each root, excluded endpoint','legacy_trig':'sine zero pair, omitted each root, excluded endpoint','quadratic':'single linear derivative root','shifted_trig':'two keyed ascending cosine derivative roots','two_period_trig':'four keyed ascending cosine derivative roots'}[name]),'eligible_for_learning':not raw,'evidence_only':raw,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    # Choose an eligible complete family/profile before any parameter sampling.
    if template is None and not (profile and profile.startswith('observed:')):
        eligible=[n for n,v in TEMPLATES.items()if v[0]==level and (not field_type or ('blank'if n in ('quadratic','shifted_trig','two_period_trig')else'radio')==field_type)]
        if not eligible:raise ValueError('No eligible family')
        template=random.Random(seed).choice(eligible)
    if parameters is not None:return _generate(level,seed,template,field_type,parameters,profile)
    for attempt in range(500):
        try:
            r=_generate(level,seed+104729*attempt,template,field_type,None,profile)
            r['generation']['seed']=seed;r['generation']['sampling_attempt']=attempt
            return r
        except ValueError as exc:
            if 'Whole bank rejected' not in str(exc):raise
    raise ValueError('No eligible instance after whole-bank rejection')

def markdown(r):
    q=r['question'];out=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        if f[':answer-field/type'].endswith('/radio'):out+=['\n'+f[':answer-field/key']]+['- '+a[':answer/value']for a in f[':answer-field/choices']]
    out+=['\nWorked solution\n'+q.get(':question/worked-solution','[Absent in captured original]')]
    return '\n'.join(out)

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parent))
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records))
