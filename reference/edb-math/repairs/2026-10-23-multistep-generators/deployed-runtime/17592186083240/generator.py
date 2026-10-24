#!/usr/bin/env python3
"""Relocatable parametric derivative generator; no database or publication writes.

Source component replay and authored hard differentiation stages are adapted from
17592186083240.py. Normal instances add eligible coordinate/sign/evaluation roles.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186083240-source-policy.json'))
    raise SystemExit(0)

import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
from math_parser import parse
RAW=json.loads((HERE/'source_data.json').read_text());KP=RAW['record'];T=sp.Symbol('t',real=True)
VERSION='parametric-derivative-3';NS=uuid.UUID(KP[':knowledge-point/id'])
QUESTIONS={str(q[':db/id']):q for q in KP[':knowledge-point/questions']}
INVENTORY_REPLAYS={str(q[':db/id']):q for q in RAW.get('inventory_only_records',[])}
INVENTORY_FAMILIES={'17592186522901':'product_pair','17592186522908':'quotient_pair',
 '17592186522915':'product_pair','17592186522916':'product_pair',
 '17592186522919':'texp_poly','17592186522920':'quotient_pair'}
FAMILY_IDS = {
 'trig':17592186083909, 'exp_poly':17592186083911,
 'quadratic':17592186290260, 'expneg_poly':17592186321110,
 'trig_double':17592186321111, 'exp_poly_chain':17592186321112,
 'line_poly':17592186321113, 'sqrt_linear':17592186321114,
 'exp_pair':17592186321115, 'quartic':17592186335950,
 'exp_product':17592186335953, 'quintic':17592186335963,
 'root_power':17592186368467, 'line_quad':17592186395776,
 'sqrt_scaled':17592186401840, 'texp_poly':17592186401853,
 'product_sin':17592186403272, 'trig_scaled':17592186403279,
 'eagle':17592186541058, 'trig_eval':17592186578802,
 't_sin':17592186578804, 'cubic':17592186578844,
 'texp_blank':17592186616136,
}
TEMPLATES={f:{'source_id':str(i),'level':QUESTIONS[str(i)][':question/difficulty'][':db/ident'].split('/')[-1],
 'kind':QUESTIONS[str(i)][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]}
 for f,i in FAMILY_IDS.items()}
TEMPLATES.update({'product_pair':{'level':'hard','kind':'blank'},'quotient_pair':{'level':'hard','kind':'blank'}})
SCALES=[sp.Rational(i,2) for i in range(1,13)]
DY=r'\frac{dy}{dx}'
def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(NS,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def fingerprint(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def same(a,b):return sp.simplify(a-b)==0

def semantic_components(x,y,point,domain,level):
    """Remove common positive coordinate amplitude, retain shapes and ratio.

    The rational content of x is a positive global amplitude for all supported
    masks. Dividing both coordinates by that same amplitude identifies common
    scaling, including authored a,c scaling, without erasing the relative y/x
    amplitude or coordinate-function forms. Banks and raw coefficients still
    participate in content identity.
    """
    amplitude,primitive=sp.sympify(x).as_content_primitive()
    if amplitude<=0:raise ValueError('positive coordinate amplitude required')
    return [str(sp.simplify(primitive)),str(sp.simplify(y/amplitude)),str(point),domain,level]

def mathematical_fingerprint(x,y,point,domain,level):
    return fingerprint(semantic_components(x,y,point,domain,level))

def derivative_domain(template,p,curve_domain):
    result={'within_curve_domain':curve_domain,'condition':"x'(t) and y'(t) exist and x'(t) != 0"}
    if template=='product_pair':result['excluded_parameters']=[str(-sp.Rational(1,int(p['b'])))]
    elif template=='quotient_pair':result['excluded_parameters']=[]
    return result

def scaled(text,k):
    """Unit coefficient elision is an arithmetic rendering rule, never source lookup."""
    k=sp.sympify(k)
    return text if k==1 else tex(k)+r'\left('+text+r'\right)'
def groups(text,start):
    assert text[start]=='{';depth=1;i=start+1
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    return text[start+1:i-1],i

def quotient_scale(text,r,s):
    # Preserve each observed quotient's numerator and denominator components.
    if text.startswith(r'\frac{'):
        n,j=groups(text,5);d,k=groups(text,j)
        return r'\frac{'+scaled(n,s)+'}{'+scaled(d,r)+'}'+text[k:]
    return scaled(text,s/r)

def coordinate_components(q):
    block=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)[0]
    m=re.fullmatch(r'x=(.*?),\\,y=(.*?),\\,(.*)',block,re.S)
    if not m:raise ValueError(block)
    return m.groups()

def clean(expr):return expr.strip().removesuffix(r'\,.').removesuffix('.').removesuffix(r'\,')
def evaluation_parameter(q):
    m=re.search(r'where \$t=(.*?)\.\$',q[':question/problem'])
    return parse(m[1]) if m else None


def source_recipe(template,p):
    """Complete source component masks, including field absence and stage sequence."""
    q=QUESTIONS[TEMPLATES[template]['source_id']];r,s=map(sp.sympify,(p['r'],p['s']));z=s/r
    x,y,domain=coordinate_components(q);xv,yv=parse(x)*r,parse(y)*s
    oldblock=f'x={x},\\,y={y},\\,{domain}'
    newblock=f'x={scaled(x,r)},\\,y={scaled(y,s)},\\,{domain}'
    problem=q[':question/problem'].replace(oldblock,newblock)
    sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    derivative=blocks[1];match=re.match(r'(.*?=)(.*?)(,\\,.*?=)(.*?)(\.)$',derivative,re.S)
    if not match:raise ValueError(derivative)
    changed=match[1]+scaled(match[2],r)+match[3]+scaled(match[4],s)+match[5]
    sol=sol.replace('$$\n'+derivative+'\n$$','$$\n'+changed+'\n$$')
    for b in blocks[2:]:
        if r'\begin{aligned}' in b:
            # Each individually substituted, evaluated and collected row is retained.
            parts=re.split(r'( & =| \\\\  & =)',b)
            for i in range(2,len(parts),2):
                tail='';expr=parts[i]
                if expr.endswith(r'\end{aligned}'):
                    expr=expr[:-len(r'\end{aligned}')];tail=r'\end{aligned}'
                punctuation=r'\,.' if expr.endswith(r'\,.') else '.' if expr.endswith('.') else ''
                body=expr[:-len(punctuation)] if punctuation else expr
                parts[i]=quotient_scale(body,r,s)+punctuation+tail
            new=''.join(parts)
        else:
            lhs,*rhs=b.split('=');new=lhs+'='+'='.join(quotient_scale(clean(v),r,s)+(r'.' if j==len(rhs)-1 and v.endswith('.') else '') for j,v in enumerate(rhs))
        sol=sol.replace('$$\n'+b+'\n$$','$$\n'+new+'\n$$')
    fields=[]
    for f in q[':question/answer-fields']:
        ff={k:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else copy.deepcopy(v)) for k,v in f.items() if k!=':db/id'}
        choices=[]
        for a in f[':answer-field/choices']:
            raw=a[':answer/value'];lhs,sep,rhs=raw.partition('=')
            val=lhs+sep+scaled(rhs,z) if sep else scaled(raw,z)
            choices.append({':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
        ff[':answer-field/choices']=choices
        if ':answer-field/correct' in f:ff[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        fields.append(ff)
    out={k:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else copy.deepcopy(v)) for k,v in q.items() if k not in [':db/id',':question/answer-fields']}
    out[':question/problem']=problem;out[':question/worked-solution']=sol;out[':question/answer-fields']=fields
    return out,xv,yv,evaluation_parameter(q),domain


def authored_hard(template,p):
    a,b,c,d=[sp.Integer(p[k]) for k in 'abcd']
    if template=='product_pair':
        x=a*T*sp.exp(b*T);y=c*(T**2+d)*sp.exp(-b*T)
        xt=tex(a)+'t e^{'+tex(b)+'t}';yt=tex(c)+r'(t^2+'+tex(d)+')e^{-'+tex(b)+'t}'
        dx=tex(a)+r'e^{'+tex(b)+'t}+ '+tex(a)+r't('+tex(b)+r'e^{'+tex(b)+'t})'
        dy=tex(c)+r'(2t)e^{-'+tex(b)+'t}+'+tex(c)+r'(t^2+'+tex(d)+r')(-'+tex(b)+r'e^{-'+tex(b)+'t})'
        fx=tex(a)+r'(1+'+tex(b)+r't)e^{'+tex(b)+'t}'
        fy=tex(c)+r'(2t-'+tex(b)+r'(t^2+'+tex(d)+r'))e^{-'+tex(b)+'t}'
        formal=r"x'(t)=a\left(\frac{d}{dt}t\right)e^{bt}+at\left(\frac{d}{dt}e^{bt}\right),\quad y'(t)=c\left(\frac{d}{dt}(t^2+d)\right)e^{-bt}+c(t^2+d)\left(\frac{d}{dt}e^{-bt}\right)"
        formal=r"x'(t)="+tex(a)+r"\left(\frac{d}{dt}\left(t\right)\right)e^{"+tex(b)+r"t}+"+tex(a)+r"t\left(\frac{d}{dt}\left(e^{"+tex(b)+r"t}\right)\right),\quad y'(t)="+tex(c)+r"\left(\frac{d}{dt}\left(t^2+"+tex(d)+r"\right)\right)e^{-"+tex(b)+r"t}+"+tex(c)+r"(t^2+"+tex(d)+r")\left(\frac{d}{dt}\left(e^{-"+tex(b)+r"t}\right)\right)"
        ratio=r'\frac{'+fy+'}{'+fx+'}'
        final=r'\frac{'+tex(c)+r'(2t-'+tex(b)+r'(t^2+'+tex(d)+r'))}{'+tex(a)+r'(1+'+tex(b)+r't)}e^{-'+tex(2*b)+'t}'
        steps=[formal,r"x'(t)="+dx+r",\quad y'(t)="+dy,r"x'(t)="+fx+r",\quad y'(t)="+fy]
        rows=[ratio,final];domain=r'-\infty<t<\infty'
    else:
        x=a*T/(T+b);y=c*T**2/(T+d)
        xt=r'\frac{'+tex(a)+'t}{t+'+tex(b)+'}';yt=r'\frac{'+tex(c)+r't^2}{t+'+tex(d)+'}'
        formal=r"x'(t)=\frac{"+tex(a)+r"\left(\frac{d}{dt}\left(t\right)\right)(t+"+tex(b)+r")-"+tex(a)+r"t\left(\frac{d}{dt}\left(t+"+tex(b)+r"\right)\right)}{(t+"+tex(b)+r")^2},\quad y'(t)=\frac{"+tex(c)+r"\left(\frac{d}{dt}\left(t^2\right)\right)(t+"+tex(d)+r")-"+tex(c)+r"t^2\left(\frac{d}{dt}\left(t+"+tex(d)+r"\right)\right)}{(t+"+tex(d)+r")^2}"
        dx=r'\frac{'+tex(a)+r'(t+'+tex(b)+r')-'+tex(a)+r't(1)}{(t+'+tex(b)+r')^2}'
        dy=r'\frac{'+tex(2*c)+r't(t+'+tex(d)+r')-'+tex(c)+r't^2(1)}{(t+'+tex(d)+r')^2}'
        ex=r'\frac{'+tex(a)+r't+'+tex(a*b)+'-'+tex(a)+r't}{(t+'+tex(b)+r')^2}'
        ey=r'\frac{'+tex(2*c)+r't^2+'+tex(2*c*d)+r't-'+tex(c)+r't^2}{(t+'+tex(d)+r')^2}'
        fx=r'\frac{'+tex(a*b)+r'}{(t+'+tex(b)+r')^2}';fy=r'\frac{'+tex(c)+r't^2+'+tex(2*c*d)+r't}{(t+'+tex(d)+r')^2}'
        rows=[r'\frac{'+fy+'}{'+fx+'}',r'\frac{('+tex(c)+r't^2+'+tex(2*c*d)+r't)(t+'+tex(b)+r')^2}{'+tex(a*b)+r'(t+'+tex(d)+r')^2}']
        steps=[formal,r"x'(t)="+dx+r",\quad y'(t)="+dy,r"x'(t)="+ex+r",\quad y'(t)="+ey,r"x'(t)="+fx+r",\quad y'(t)="+fy]
        domain=r't>0'
    problem='For the parametric curve\n\n$$\nx='+xt+r',\quad y='+yt+r',\quad '+domain+',\n$$\n\ncalculate $'+DY+'$ as a function of $t.$\n\n$'+DY+'=$\n{{field-1}}'
    if template=='product_pair':
        problem=problem.replace('as a function of $t.$','as a function of $t$ for $t\\ne '+tex(-sp.Rational(1,b))+'.$')
    sol='We will use the formula\n\n$$\n'+DY+r"=\frac{y'(t)}{x'(t)}."+'\n$$\n\nDifferentiating $x$ and $y,$ we get\n\n'+''.join('$$\n'+z+'\n$$\n\n' for z in steps)+'Therefore,\n\n$$\n'+DY+'='+'='.join(rows)+'.\n$$'
    if template=='product_pair':sol+='\n\nThis derivative is defined for $t\\ne '+tex(-sp.Rational(1,b))+'.$'
    return problem,sol,x,y,domain,rows[-1]


from math_format import normalize_prose, normalize_tex, checked_math_content
import os

POINTS = {
 'exp_poly':['1','2','3','5'], 'quadratic':['-1','1','2','3'],
 'expneg_poly':['0','1','2'], 'trig_double':['pi/12','pi/6','pi/3','5*pi/12'],
 'exp_poly_chain':['1','2','3'], 'line_poly':['-1','0','1','2'],
 'sqrt_linear':['1','4','9'], 'quartic':['-1','0','1','2'],
 'exp_product':['0','1','2'], 'quintic':['-1','1','2'],
 'line_quad':['-1/2','0','1/2'], 'sqrt_scaled':['1','4','9'],
 'texp_poly':['0','1','2'], 'product_sin':['0'],
 'trig_eval':['pi/8','3*pi/8','5*pi/8','7*pi/8'],
 't_sin':['pi/2','pi','3*pi/2'], 'cubic':['-2','-1','1','2','3'],
 'texp_blank':['0','1','2','3'],
}
PLOT_WINDOWS = {'quadratic':(-3,4),'expneg_poly':(0,2),
 'trig_double':(0,2*float(sp.pi)), 'quartic':(-1.6,1.6),
 'quintic':(-1.6,1.6),'line_quad':(-1,1),'texp_poly':(0,3),
 'trig_eval':(0,2*float(sp.pi)),'cubic':(-3.2,3.2),'texp_blank':(0,3)}
PROFILE_STARTS = {'double-r':lambda r:2*r, 'negative-double-r':lambda r:-2*r,
 'double-reciprocal':lambda r:2/r, 'negative-double-reciprocal':lambda r:-2/r,
 'zero-slip':lambda r:sp.S.Zero}

def number(v):
    return sp.sympify(v, locals={'pi':sp.pi})

def source_coordinates(template):
    if template=='eagle':
        # This family's data are already derivatives: never invent missing coordinates.
        return 5/(25+T**2), T**2-2, r'-\infty<t<\infty'
    q=QUESTIONS[TEMPLATES[template]['source_id']]
    x,y,domain=coordinate_components(q)
    return parse(x),parse(y),domain

def validate_parameters(template,p):
    hard=TEMPLATES[template]['level']=='hard'
    keys=set('abcd') if hard else {'r','s','point','swap','sign'}
    if hard:keys|={'swap','sign'}
    if set(p)-{'gain'}!=keys:raise ValueError('Unexpected parameter keys')
    gain=number(p.get('gain',1))
    if gain not in [1,2] or (gain==2 and (hard or TEMPLATES[template]['kind']!='radio')):raise ValueError('amplitude role')
    if p['swap'] not in [False,True] or p['sign'] not in [-1,1]:raise ValueError('coordinate role/sign')
    if hard:
        for k,maximum in {'a':5,'b':3,'c':5,'d':4}.items():
            v=number(p[k])
            if v.is_Integer is not True or not 1<=v<=maximum:raise ValueError('hard workload bounds')
    else:
        if any(number(p[k]) not in SCALES for k in ['r','s']):raise ValueError('amplitude bounds')
        if gain==2 and number(p['r' if p['swap'] else 's'])>3:raise ValueError('final amplitude exceeds 6')
        points=POINTS.get(template)
        if points is None:
            if p['point'] is not None:raise ValueError('symbolic family')
        elif str(p['point']) not in points:raise ValueError('unsupported evaluation point')

def sample_parameters(rng,template,profile=None):
    # Choose answer-bearing roles/evaluation evidence first.
    swap=rng.choice([False,True]);sign=rng.choice([-1,1])
    if TEMPLATES[template]['level']=='hard':
        return {**dict(zip('abcd',[rng.randint(1,5),rng.randint(1,3),rng.randint(1,5),rng.randint(1,4)])), 'swap':swap,'sign':sign}
    gain=2 if TEMPLATES[template]['kind']=='radio' and profile in PROFILE_STARTS and profile!='zero-slip' and rng.randrange(5)==0 else 1
    if gain==2:
        swap='reciprocal' in profile;sign=-1 if profile.startswith('negative-') else 1
    point=rng.choice(POINTS[template]) if template in POINTS else None
    rscales=SCALES[:6] if gain==2 and swap else SCALES
    sscales=SCALES[:6] if gain==2 and not swap else SCALES
    return {'swap':swap,'sign':sign,'point':point,'r':str(rng.choice(rscales)),'s':str(rng.choice(sscales)),**({'gain':'2'} if gain==2 else {})}

def make_instance(template,p):
    hard=TEMPLATES[template]['level']=='hard'
    if hard:
        _,oldsolution,bx,by,domain,_=authored_hard(template,p)
        point=None
    else:
        bx,by,domain=source_coordinates(template)
        bx*=number(p['r']);by*=number(p['s'])
        point=number(p['point']) if p['point'] is not None else None
    x,y=(by,bx) if p['swap'] else (bx,by)
    y*=p['sign']*number(p.get('gain',1))
    if template=='eagle':dx,dy=x,y
    else:dx,dy=sp.diff(x,T),sp.diff(y,T)
    ev=lambda v:sp.simplify(v.subs(T,point) if point is not None else v)
    if ev(dx)==0 or any(ev(v).has(sp.zoo,sp.nan,sp.oo,-sp.oo) for v in [dx,dy]):
        raise ValueError('singular evaluation or undefined coordinate derivative')
    ratio=sp.simplify(dy/dx);correct=ev(ratio)
    if template=='eagle':
        # The captured quotient solution leaves the two quadratics factored;
        # expansion would add an unnecessary algebra stage to this easy item.
        ratio=sp.factor(ratio);correct=ratio
    return {'template':template,'parameters':p,'x':x,'y':y,'dx':dx,'dy':dy,
        'base_x':bx,'base_y':by,'point':point,'domain':domain,'ratio':ratio,'correct':correct}

def variant_bank(inst,profile):
    # The bank is independent of swap/sign; only the correct designation moves.
    bx,by=inst['base_x'],inst['base_y'];point=inst['point']
    dx,dy=(bx,by) if inst['template']=='eagle' else (sp.diff(bx,T),sp.diff(by,T))
    if point is not None:dx,dy=map(lambda v:sp.simplify(v.subs(T,point)),[dx,dy])
    if dx==0 or dy==0:
        vals=[sp.S.Zero,sp.S.One,-sp.S.One,sp.Integer(2),sp.Integer(-2)]
        labels=['zero','unit','negative-unit','double-unit','negative-double-unit']
    else:
        r=sp.simplify(dy/dx)
        if same(r*r,1):
            # Reciprocal/sign roles coincide at unit magnitude. Keep the valid
            # simplification and let ordinary, doubled and zero-slope evidence
            # move correctness through this same complete conditional bank.
            return [sp.S.One,-sp.S.One,sp.Integer(2),sp.Integer(-2),sp.S.Zero],['unit','negative-unit','double-unit','negative-double-unit','zero']
        candidates=[(r,'R'),(-r,'-R'),(1/r,'1/R'),(-1/r,'-1/R'),
          (PROFILE_STARTS[profile](r),'profile-filler'),
          (2*r,'2R'),(-2*r,'-2R'),(2/r,'2/R'),(-2/r,'-2/R'),
          (r/2,'R/2'),(-r/2,'-R/2'),(1/(2*r),'1/(2R)'),(-1/(2*r),'-1/(2R)'),(sp.S.Zero,'zero')]
        vals=[];labels=[]
        for v,label in candidates:
            v=sp.simplify(v)
            if not v.has(sp.nan,sp.zoo,sp.oo,-sp.oo) and not any(same(v,w) for w in vals):
                vals.append(v);labels.append(label)
            if len(vals)==5:break
    if len(vals)!=5 or sum(same(inst['correct'],v) for v in vals)!=1:raise ValueError('incomplete bank')
    return vals,labels

def tex_for(inst,value):
    text=tex(value)
    if inst['template'] in ['trig','trig_scaled']:
        text=re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:r'\theta',text)
    return text

def display(text):return '$$\n'+text+'\n$$'

def product_rule_display(lhs,expression,negative):
    # The two formal product-rule terms get separate rows. Fixed-size
    # parentheses span the rows when an outer coordinate sign is negative.
    depth=0
    for i,char in enumerate(expression):
        if char in '({[':depth+=1
        elif char in ')}]':depth-=1
        elif char=='+' and depth==0:
            first,second=expression[:i],expression[i+1:]
            return (r'\begin{aligned}'+lhs+'&='+ (r'-\bigl(' if negative else '')+
                    first+r'\\&\quad{}+'+second+(r'\bigr)' if negative else '')+r'\end{aligned}')
    raise ValueError('formal product rule must have two terms')

def prompt_solution(inst):
    p=inst['parameters'];template=inst['template'];point=inst['point'];domain=inst['domain']
    tf=lambda v:tex_for(inst,v)
    variable=r'\theta' if template in ['trig','trig_scaled'] else 't'
    if template=='eagle':
        problem=("The eagle's path traces a curve $C$ in the $xy$-plane. At the point $P$ at time $t,$ the coordinate derivatives are\n\n"+
          display("x'(t)="+tf(inst['dx'])+r",\qquad y'(t)="+tf(inst['dy']))+
          '\n\nExpressed in terms of $t,$ what function gives the slope of the tangent to $C$ at $P?$\n\nThe slope equals {{field-1}}.')
    else:
        problem='For the parametric curve'+(' (shown above)' if template in PLOT_WINDOWS else '')+'\n\n'+display('x='+tf(inst['x'])+r',\qquad y='+tf(inst['y']))+'\n\n'+display(domain)+'\n\n'
        if point is None:problem+='calculate $'+DY+'$'+(' as a function of $t$.' if variable=='t' else '.')
        else:problem+='find the derivative $'+DY+'$ at the point $P$ on the curve where $t='+tf(point)+'$. Give an exact answer.'
        if TEMPLATES[template]['kind']=='blank':
            lhs=DY if point is None else DY+r'\big|_{t='+tf(point)+'}'
            problem+='\n\n$'+lhs+'=$\n{{field-1}}'
    solution='We will use the formula\n\n'+display(DY+r"=\frac{y'("+variable+r")}{x'("+variable+r")}")
    # Preserve the hard source's explicit product/quotient-rule stages, remapping
    # coordinate identities and the relative sign through derivative roles.
    if TEMPLATES[template]['level']=='hard':
        _,old,_,_,_,_=authored_hard(template,p)
        steps=re.findall(r'\$\$\n(.*?)\n\$\$',old,re.S)[1:-1]
        newsteps=[]
        for index,step in enumerate(steps):
            left,right=step.split(r',\quad ')
            xv=left.partition('=')[2];yv=right.partition('=')[2]
            if p['swap']:xv,yv=yv,xv
            if template=='product_pair' and index==0:
                newsteps.extend([product_rule_display("x'(t)",xv,False),
                                 product_rule_display("y'(t)",yv,p['sign']==-1)])
                continue
            if p['sign']==-1:yv=r'-\left('+yv+r'\right)'
            # Each derivative gets its own display: the paired formal rule
            # expressions otherwise clip in the actual learner column.
            newsteps.extend(["x'(t)="+xv,"y'(t)="+yv])
        solution+='\n\nDifferentiating $x$ and $y,$ we get\n\n'+'\n\n'.join(display(z) for z in newsteps)
    else:
        solution+='\n\n'+('Using the supplied coordinate derivatives, we have' if template=='eagle' else 'Differentiating $x$ and $y,$ we get')+'\n\n'
        solution+=display("x'("+variable+")="+tf(inst['dx'])+r",\qquad y'("+variable+")="+tf(inst['dy']))
    quotient=r'\frac{'+tf(inst['dy'])+'}{'+tf(inst['dx'])+'}'
    if TEMPLATES[template]['level']=='hard':
        calculation=r'\begin{aligned}'+DY+'&='+quotient+r'\\&='+tf(inst['ratio'])+r'\end{aligned}'
    else:calculation=DY+'='+quotient+'='+tf(inst['ratio'])
    solution+='\n\nTherefore,\n\n'+display(calculation)
    if point is not None:
        # Token-safe parameter substitution: do not replace t inside \sqrt etc.
        substituted=lambda v:re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:r'\left('+tf(point)+r'\right)',tf(v))
        solution+='\n\nAt the point where $t='+tf(point)+'$ we have\n\n'+display(r'\begin{aligned}'+DY+r'\big|_{t='+tf(point)+r'}&=\frac{'+substituted(inst['dy'])+'}{'+substituted(inst['dx'])+r'}\\&='+r'\frac{'+tf(inst['dy'].subs(T,point))+'}{'+tf(inst['dx'].subs(T,point))+r'}\\&='+tf(inst['correct'])+r'\end{aligned}')
    else:
        solution+="\n\nThis formula applies where both coordinate derivatives exist and $x'("+variable+r')\ne0$.'
    return problem,solution

def render_plot(inst):
    template=inst['template']
    output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name an explicit asset directory')
    destdir=Path(output).resolve()
    # A published package is immutable; reject asset output into its runtime tree.
    if destdir.is_relative_to(HERE):raise ValueError('asset output must be outside the package directory')
    destdir.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-kp83240-mpl')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import tempfile
    low,high=PLOT_WINDOWS[template]
    tt=np.linspace(low,high,1200)
    xx=np.broadcast_to(sp.lambdify(T,inst['x'],'numpy')(tt),tt.shape)
    yy=np.broadcast_to(sp.lambdify(T,inst['y'],'numpy')(tt),tt.shape)
    narrow_x=template in ['trig_double','trig_eval'] and np.ptp(xx)*3<np.ptp(yy)
    name=fingerprint(['plot-v4-origin-x-tick' if narrow_x else 'plot-v3',template,str(inst['x']),str(inst['y']),low,high])[:24]
    dest=destdir/(name+'.png')
    if not dest.exists():
        fig,ax=plt.subplots(figsize=(5,4),dpi=120)
        ax.plot(xx,yy,color='#2578bc',lw=1.8);ax.axhline(0,color='#444',lw=.8);ax.axvline(0,color='#444',lw=.8)
        ax.grid(alpha=.3);ax.set_xlabel('$x$');ax.set_ylabel('$y$')
        if template in ['trig_double','trig_eval']:ax.set_aspect('equal',adjustable='box')
        # A tall equal-scale ellipse has too little horizontal space for three
        # tick labels. The origin and the unchanged y-scale remain readable.
        if narrow_x:ax.set_xticks([0])
        if template=='line_quad':
            ax.plot(xx[0],yy[0],'o',color='#2578bc');ax.plot(xx[-1],yy[-1],'o',mfc='white',mec='#2578bc')
        fig.tight_layout();fd,tmp=tempfile.mkstemp(suffix='.png',dir=destdir);os.close(fd)
        fig.savefig(tmp);plt.close(fig);os.replace(tmp,dest)
        dest.with_suffix('.json').write_text(json.dumps({'x':str(inst['x']),'y':str(inst['y']),'parameter_window':[low,high],'samples':1200,'template':template,'renderer':'matplotlib '+matplotlib.__version__,'x_ticks':[0] if narrow_x else 'automatic'},indent=2))
    return str(dest)

def normalize_question(q):
    for key in [':question/problem',':question/worked-solution']:q[key]=normalize_prose(q[key])
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
    return q

def finalize(q,meta,rng):
    q=normalize_question(q)
    # Field-owned IDs and content keys are derived after presentation normalization.
    q.pop(':question/math-academy-id',None)
    for f in q[':question/answer-fields']:
        old=f.pop(':answer-field/correct',None)
        if old:
            oldid=old[':answer/id'] if isinstance(old,dict) else old[1]
            f['_correct_value']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a.get(':answer/id')==oldid)
        for a in f[':answer-field/choices']:a.pop(':answer/id',None)
        f.pop(':answer-field/id',None)
    canonical=copy.deepcopy(q);canonical.pop(':question/id',None)
    # Asset directory is runtime configuration, never question identity.
    canonical[':question/problem']=re.sub(r'!\[\]\(([^)]+)\)',lambda m:'![]('+Path(m[1]).name+')',canonical[':question/problem'])
    identity=fingerprint(canonical);qid=uid(['v3',identity]);q[':question/id']=qid
    for i,f in enumerate(q[':question/answer-fields']):
        correct=f.pop('_correct_value')
        f[':answer-field/id']=uid([qid,i])
        for a in f[':answer-field/choices']:a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
        f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
        rng.shuffle(f[':answer-field/choices'])
    return {'knowledge_point':{'db_id':17592186083240,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,**meta,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'content_fingerprint':identity}}

@checked_math_content
def generate(level='moderate',seed=0,template=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('unsupported difficulty '+str(level))
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        sourceid=profile.split(':',1)[1]
        matches=[INVENTORY_FAMILIES[sourceid]] if sourceid in INVENTORY_REPLAYS else [k for k,v in TEMPLATES.items() if v.get('source_id')==sourceid]
        if not matches:raise ValueError('unknown source profile')
        if template and template!=matches[0]:raise ValueError('source profile/template mismatch')
        template=matches[0]
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level]
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('template/difficulty mismatch')
    sourceid=TEMPLATES[template].get('source_id')
    if profile and profile.startswith('observed:'):
        if parameters is not None and parameters!={'r':'1','s':'1'}:raise ValueError('source replay uses original parameters only')
        sourceid=profile.split(':',1)[1]
        raw=copy.deepcopy(INVENTORY_REPLAYS.get(sourceid) or QUESTIONS[sourceid])
        def flattened(v):
            if isinstance(v,dict):
                if set(v)=={':db/ident'}:return v[':db/ident']
                return {k:flattened(w) for k,w in v.items() if k!=':db/id'}
            if isinstance(v,list):return [flattened(w) for w in v]
            return v
        q=flattened(raw)
        return finalize(q,{'template':template,'profile':profile,'source_ids':[sourceid],'seed':seed,'parameters':{'r':'1','s':'1'},'evidence_only':True},rng)
    profile=profile or rng.choice(list(PROFILE_STARTS))
    if profile not in PROFILE_STARTS:raise ValueError('unknown authored bank profile')
    rejections=[]
    for attempt in range(100):
        p=copy.deepcopy(parameters) if parameters is not None else sample_parameters(rng,template,profile)
        validate_parameters(template,p)
        if number(p.get('gain',1))==2 and (profile=='zero-slip' or p['swap']!=('reciprocal' in profile) or p['sign']!=(-1 if profile.startswith('negative-') else 1)):
            raise ValueError('gain role must match the selected complete bank profile')
        try:inst=make_instance(template,p)
        except ValueError as err:
            if parameters is not None:raise
            rejections.append(str(err));continue
        break
    else:raise ValueError('no nonsingular instance')
    problem,solution=prompt_solution(inst)
    if template in PLOT_WINDOWS:problem='![]('+render_plot(inst)+')\n\n'+problem
    kind=TEMPLATES[template]['kind'];correct=inst['correct']
    if kind=='radio':values,recipes=variant_bank(inst,profile)
    else:values=[correct];recipes=['correct RHS']
    eq=template in ['trig','trig_scaled']
    choices=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':(DY+'=' if eq else '')+tex_for(inst,v)} for i,v in enumerate(values)]
    index=next(i for i,v in enumerate(values) if same(v,correct))
    field={':answer-field/key':'selection' if kind=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',str(index)]}
    q={':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
    # Remove common positive amplitude for semantic counting; retain relative sign,
    # coordinate assignment, evaluation point, and relative coordinate amplitude.
    cx,cy=inst['x'],inst['y'];amp,_=cx.as_content_primitive()
    semantic=fingerprint([str(sp.simplify(cx/amp)),str(sp.simplify(cy/amp)),str(inst['point']),inst['domain'],level,template=='eagle'])
    meta={'template':template,'profile':profile,'seed':seed,'source_ids':[sourceid] if sourceid else [],'parameters':{k:(str(v) if k not in ['swap','sign'] and v is not None else v) for k,v in p.items()},'recipes':recipes,'rejections':rejections,'domain':inst['domain'],'derivative_condition':"x' and y' exist, x' != 0",'mathematical_fingerprint':semantic,'evidence_only':False,'authored_extension':True}
    return finalize(q,meta,rng)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile')
    a=ap.parse_args()
    if a.count<0:ap.error('count must be nonnegative')
    rows=[generate(a.difficulty,seed=a.seed+i,template=a.template,profile=a.profile) for i in range(a.count)]
    if a.format=='json':print(json.dumps(rows,ensure_ascii=False,indent=2))
    else:
        for row in rows:print(row['question'][':question/problem']+'\n\n'+row['question'][':question/worked-solution'])

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186083240-source-policy.json'))

if __name__=='__main__':main()
