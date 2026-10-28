#!/usr/bin/env python3
"""Two-variable vector chain rule, math basis 1356. Frozen draft v1.

Six observed five-choice radio templates retain complete profiles and the original
shared prose/ordered mathematical stages. Profiles 'observed' use defensible
symbolic patterns, not an answer lookup; several error interpretations remain
underdetermined and are replay-only defaults. Normal 'authored' complete banks
are specified operations. Unrated q-95056 has an independently inferred correct
answer and authored solution/easy assignment. No plots or database operations.

Easy: observed workloads with small coefficients and inner rates.
Moderate: authored mixed polynomial, three nonzero component contributions.
Hard: authored arctan(x*y^2), two nonunit coordinate rates and outer-chain quotient.
All explicit parameters pass the same reduced workload guards as random inputs.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
X,Y,T=s.symbols('x y t',real=True)
VERSION='two-variable-vector-chain-1'
KP_ID=17592186124469
KP_UUID='0096e314-e53e-5d9b-9cee-fe34fa3a6379'
TITLE='Applying the Vector Form of the Chain Rule to a Function of Two Variables'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCE=CAPTURE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
TEMPLATES={'square_exp':'q-36211','log_cos':'q-95056','polylog':'q-37099','cos_exp':'q-95052','log_power':'q-95054','atan_product':'q-95059','mixed_polynomial':None,'atan_squared':None}
ORIGINAL={'square_exp':{'a':1,'b':1,'k':1},'log_cos':{'a':1,'n':2,'k':1},'polylog':{'a':2,'b':1,'c':3,'n':2},'cos_exp':{'a':1,'k':'pi','l':1},'log_power':{'a':2,'n':2,'k':1},'atan_product':{'a':1,'k':1,'l':1}}
LEVEL={name:('moderate' if name=='mixed_polynomial' else 'hard' if name=='atan_squared' else 'easy') for name in TEMPLATES}
RULE=r'\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).'
OP=r'\frac{\text{d}}{\text{d}t}[f(r(t))]'

def latex(z):
    return s.latex(z).replace(r'\log',r'\ln').replace(r'\operatorname{atan}',r'\arctan')
def cf(c,z):
    """Visible coefficient: source convention, no numeric-factor concatenation."""
    c=s.sympify(c)
    if c==0:return '0'
    if c==1:return z
    if c==-1:return '-'+z
    return latex(c).replace('- ','-')+(' ' if str(c).endswith('pi') else '')+z

def add(*parts):
    return ''.join(('+' if i and not a.startswith('-') else '')+a for i,a in enumerate(parts))
def pp(v,n):return v if n==1 else '{'+v+'}^{'+str(n)+'}'
def ep(k):return pp('e',cf(k,'t'))
def tr(fn,arg='t'):return r'\operatorname{'+fn+'}⁡'+arg
LN=tr('ln')
def vec(a,b):return add(a+r'\,i',b+r'\,j')
def alg(lhs,rows):return r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}'
def gradblock(F,rows,paren=True):
    F='('+F+')' if paren else F
    return alg('∇f(x,y)',[r'\frac{∂}{∂x}'+F+r'\,i+\frac{∂}{∂y}'+F+r'\,j',*rows])
def derivative(u,v,du,dv):
    return alg('{r}^{′}(t)',[vec(r'\frac{\text{d}}{\text{d}t}('+u+')',r'\frac{\text{d}}{\text{d}t}('+v+')'),vec(du,dv)+'.'])
def final(gx,gy,dx,dy,rows):
    return alg(OP,['∇f(r(t))\u005ccdot {r}^{′}(t)','('+vec(gx,gy)+r')\cdot ('+vec(dx,dy)+')',*rows[:-1],rows[-1]+'.'])
def frac(a,b):return r'\frac{'+a+'}{'+b+'}'
def value(k):return s.pi if k=='pi' else s.Integer(k)

def validate_parameters(level,name,p,profile):
    if name not in TEMPLATES or LEVEL[name]!=level:raise ValueError('Template/difficulty mismatch')
    keys={'mixed_polynomial':{'a','b','c','k'},'atan_squared':{'a','k','l'}}.get(name,set(ORIGINAL[name]) if name in ORIGINAL else set())
    if set(p)!=keys:raise ValueError(f'Expected exactly {sorted(keys)}')
    for k,v in p.items():
        if k=='k' and name=='cos_exp' and v=='pi':continue
        if type(v) is not int or v<=0:raise ValueError('Positive integer coefficients/rates required')
    if level=='easy':
        if any(v>4 for k,v in p.items() if type(v)is int):raise ValueError('Easy coefficients/rates bounded by 4')
        if name=='polylog' and p['n']!=2:raise ValueError('Easy polylog keeps quadratic coordinate')
        if name in ('log_cos','log_power') and p['n'] not in (1,2,3):raise ValueError('Power workload bound')
        if name=='log_power' and p['a'] not in (1,2,3):raise ValueError('Log argument power bound')
    elif level=='moderate':
        if not all(1<=p[k]<=3 for k in ('a','b','c')) or p['k'] not in (1,2):raise ValueError('Moderate small nonzero mixed-term bounds')
    elif not (1<=p['a']<=4 and p['k'] in (2,3,4,5) and p['l'] in (2,3,4,5)):
        raise ValueError('Hard requires nonunit rates 2..5 and scale 1..4')
    if profile not in ('observed','authored','raw_observed'):raise ValueError('Unknown bank profile')
    if profile=='raw_observed' and name!='log_cos':raise ValueError('Raw anomaly profile is only q-95056')
    if profile=='observed' and name not in ORIGINAL:raise ValueError('No observed bank for authored template')


def build(name,p):
    """Exact math + source-compatible ordered masks; never return literal payload."""
    a=p['a'];k=value(p.get('k',1));l=p.get('l',1)
    if name=='square_exp':
        b=p['b'];f=a*X**2+b*Y**2;u=s.exp(k*T);v=s.exp(-k*T)
        F=add(cf(a,pp('x',2)),cf(b,pp('y',2)));U=ep(k);V=ep(-k)
        gx=cf(2*a,'x');gy=cf(2*b,'y');gxv=cf(2*a,U);gyv=cf(2*b,V);dx=cf(k,U);dy=cf(-k,V)
        blocks=[gradblock(F,[vec(gx,gy)]),alg('∇f(r(t))',[vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[add(cf(2*a*k,U)+r'\cdot '+U,cf(-2*b*k,V)+r'\cdot '+V),add(cf(2*a*k,ep(2*k)),cf(-2*b*k,ep(-2*k)))])]
        banks=[(2*a*k*s.exp(2*k*T)+2*b*k*s.exp(-2*k*T),add(cf(2*a*k,ep(2*k)),cf(2*b*k,ep(-2*k)))),(2*k*(a+b)*s.exp(2*k*T),cf(2*k*(a+b),ep(2*k))),(2*a*k*s.exp(2*k*T)-2*b*k*s.exp(-2*k*T),add(cf(2*a*k,ep(2*k)),cf(-2*b*k,ep(-2*k)))),(2*a*k*s.exp(k*T)-2*b*k*s.exp(-k*T),add(cf(2*a*k,U),cf(-2*b*k,V))),(a*s.exp(2*k*T)+b*s.exp(-2*k*T),add(cf(a,ep(2*k)),cf(b,ep(-2*k))))]
    elif name=='polylog':
        b,c,n=p['b'],p['c'],p['n'];f=a*X-b*X*Y**2;u=s.log(T);v=c*T**n
        F=add(cf(a,'x'),cf(-b,'x'+pp('y',2)));U=LN;V=cf(c,pp('t',n))
        gx='('+add(str(a),cf(-b,pp('y',2)))+')';gy=cf(-2*b,'xy');gxv='('+add(str(a),cf(-b*c*c,pp('t',2*n)))+')';gyv=cf(-2*b*c,pp('t',n)+LN);dx=frac('1','t');dy=cf(c*n,pp('t',n-1))
        tail=add(frac(str(a),'t'),cf(-b*c*c,pp('t',2*n-1)),cf(-2*b*c*c*n,pp('t',2*n-1)+LN))
        blocks=[gradblock(F,[vec(gx,gy)]),alg('∇f(r(t))',[vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[gxv+r'\cdot '+dx+'+('+gyv+r')\cdot '+dy,tail])]
        banks=[(a+b*c*c*T**(2*n-1)+2*b*c*T**(2*n-1)*s.log(T),add(str(a),cf(b*c*c,pp('t',2*n-1)),cf(2*b*c,pp('t',2*n-1)+LN))),(a/T-b*c*T**(n-1)-b*c*T**(n-1)*s.log(T),add(frac(str(a),'t'),cf(-b*c,pp('t',n-1)),cf(-b*c,pp('t',n-1)+LN))),(a/T-b*c*T**n+2*b*c*c*n*T**(2*n-1),add(frac(str(a),'t'),cf(-b*c,pp('t',n)),cf(2*b*c*c*n,pp('t',2*n-1)))),(a/T-b*c*c*T**n-2*b*c*n*T**n*s.log(T),add(frac(str(a),'t'),cf(-b*c*c,pp('t',n)),cf(-2*b*c*n,pp('t',n)+LN))),(a/T-b*c*c*T**(2*n-1)-2*b*c*c*n*T**(2*n-1)*s.log(T),tail)]
    elif name=='cos_exp':
        f=a*Y*s.cos(X);u=k*T;v=s.exp(l*T);F=cf(a,'y'+tr('cos','x'));U=cf(k,'t');V=ep(l)
        cs=tr('cos',U);sn=tr('sin',U);gx=cf(-a,'y'+tr('sin','x'));gy=cf(a,tr('cos','x'));gxv=cf(-a,V+sn);gyv=cf(a,cs);dx=latex(k)+(' ' if k==s.pi else '');dy=cf(l,V)
        distributed=add(cf(-a*k,V+sn),cf(a*l,V+cs));tail=V+'('+add(cf(a*l,cs),cf(-a*k,sn))+')'
        blocks=[gradblock(F,[vec(gx,gy)]),alg('∇f(r(t))',[vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[distributed,tail])]
        banks=[(a*l*v*s.cos(u)-a*s.sin(u),add(cf(a*l,V+cs),cf(-a,sn))),(a*v*(l*s.cos(u)-k*s.sin(u)),tail),(a*l*s.cos(u)-a*v*s.sin(u),add(cf(a*l,cs),cf(-a,V+sn))),(k*T+a*v*s.cos(u),add(U,cf(a,V+cs))),(k*T-a*v*s.sin(u),add(U,cf(-a,V+sn)))]
    elif name=='log_power':
        n=p['n'];f=s.log(X*Y**a);u=T**(-n);v=s.exp(k*T);F=tr('ln','(x'+pp('y',a)+')');U=pp('t',-n);V=ep(k)
        gx=frac('1','x');gy=frac(str(a),'y');gxv=pp('t',n);gyv=cf(a,ep(-k));dx=cf(-n,pp('t',-n-1));dy=cf(k,V)
        rawgrad=vec(frac(pp('y',a),'x'+pp('y',a)),frac(cf(a,'x'+(pp('y',a-1) if a>1 else '')),'x'+pp('y',a)))
        substituted=vec(frac('1',U),frac(str(a),V));reduced=add(str(a*k),'-'+frac(str(n),'t'));tail=frac(cf(a*k,'(t-'+latex(s.Rational(n,a*k))+')'),'t')
        # Preserve original factored mask n=a*k; general numerator is exact.
        if n!=a*k:tail=frac(add(cf(a*k,'t'),str(-n)),'t')
        blocks=[gradblock(F,[rawgrad,vec(gx,gy)],False),alg('∇f(r(t))',[substituted,vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[add(cf(-n,'('+gxv+')('+pp('t',-n-1)+')'),cf(a*k,ep(-k)+'('+V+')')),reduced,tail])]
        banks=[((a+n-1)*(T*T+1)/T,frac(cf(a+n-1,'('+pp('t',2)+'+1)'),'t')),((T**n*s.exp(k*T)+a)/s.exp(k*T),frac(add(pp('t',n)+V,str(a)),V)),(a*k-n/T,tail),(T*(T-n),'t(t-'+str(n)+')'),(a*(T*s.exp(k*T)-1)/s.exp(k*T),frac(cf(a,'(t'+V+'-1)'),V))]
    elif name=='atan_product' or name=='atan_squared':
        m=1 if name=='atan_product' else 2;f=s.atan(a*X*Y**m);u=s.exp(k*T);v=s.sin(l*T)
        F=tr('arctan',cf(a,'x'+pp('y',m)) if a==1 and m==1 else '('+cf(a,'x'+pp('y',m))+')');U=ep(k);V=tr('sin',cf(l,'t'));cs=tr('cos',cf(l,'t'))
        den='1+'+cf(a*a,pp('x',2)+pp('y',2*m));DV='1+'+cf(a*a,ep(2*k)+pp('sin',2*m)+'⁡'+cf(l,'t'))
        gx=frac(cf(a,pp('y',m)),den);gy=frac(cf(a*m,'x'+(pp('y',m-1) if m>1 else '')),den)
        gxv=frac(cf(a,pp('sin',m)+'⁡'+cf(l,'t') if m>1 else V),DV);gyv=frac(cf(a*m,U+(V if m>1 else '')),DV);dx=cf(k,U);dy=cf(l,cs)
        part1=frac(cf(a*k,U+(pp('sin',m)+'⁡'+cf(l,'t') if m>1 else V)),DV);part2=frac(cf(a*m*l,U+(V if m>1 else '')+cs),DV)
        tail=frac(cf(a,U)+'('+add(cf(k,pp('sin',m)+'⁡'+cf(l,'t') if m>1 else V),cf(m*l,(V if m>1 else '')+cs))+')',DV)
        gradient_rows=[vec(gx,gy)+(r'\text{ }' if m==1 else '')]
        substitution_rows=[vec(gxv,gyv)]
        if m==2:
            # Held-coordinate derivatives retain the zero contributions before reduction.
            nrx=cf(a,'(1'+pp('y',2)+'+x'+cf(2,'y')+r'\cdot 0)')
            nry=cf(a,'(0'+pp('y',2)+'+x'+cf(2,'y')+r'\cdot 1)')
            gradient_rows.insert(0,vec(frac(nrx,den),frac(nry,den)))
            ds='1+'+cf(a*a,'('+U+')^{2}('+V+')^{4}')
            substitution_rows.insert(0,vec(frac(cf(a,'('+V+')^{2}'),ds),frac(cf(2*a,'('+U+')('+V+')'),ds)))
        blocks=[gradblock(F,gradient_rows),alg('∇f(r(t))',substitution_rows),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[part1+'+'+part2,tail])]
        d=1+a*a*u*u*v**(2*m)
        banks=[(a*u*(l*s.cos(l*T)+k)/d,frac(cf(a,U)+'('+add(cf(l,cs),latex(k))+')',DV)),(a*(v+u)/d,frac(cf(a,'('+V+'+'+U+')') if a!=1 else V+'+'+U,DV)),(a*u*(k*v+l*s.cos(l*T))/d,frac(cf(a,U)+'('+add(cf(k,V),cf(l,cs))+')',DV)),(a*u*(k*v+l)/d,frac(cf(a,U)+'('+add(cf(k,V),str(l))+')',DV)),(a*(u-s.cos(l*T))/d,frac(cf(a,'('+U+'-'+cs+')') if a!=1 else U+'-'+cs,DV))] if m==1 else []
    elif name=='log_cos':
        n=p['n'];f=s.log(X*Y**a);u=s.cos(k*T);v=T**n;F=r'\ln '+('xy' if a==1 else '(x'+pp('y',a)+')');U=r'\cos '+cf(k,'t');V='t^{'+str(n)+'}' if n!=1 else 't'
        gx=frac('1','x');gy=frac(str(a),'y');gxv=frac('1',U);gyv=frac(str(a),V);dx=cf(-k,r'\sin '+cf(k,'t'));dy=cf(n,pp('t',n-1))
        den='x'+pp('y',a);blocks=[gradblock(F,[vec(frac(pp('y',a),den),frac(cf(a,'x'+(pp('y',a-1) if a>1 else '')),den)),vec(gx,gy)]),alg('∇f(r(t))',[vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,['('+gxv+')('+dx+')+('+gyv+')('+dy+')',add(frac(str(a*n),'t'),cf(-k,r'\tan '+cf(k,'t')))])]
        tangent=s.tan(k*T);sec=s.sec(k*T)
        banks=[((a*n*T+1)/T**2,frac(add(cf(a*n,'t'),'1'),pp('t',2))),((a*n-k*T*tangent)/T,frac(add(str(a*n),cf(-k,'t'+r'\tan '+cf(k,'t'))),'t')),((T*T*k*tangent+a*n)/T**2,frac(add(cf(k,pp('t',2)+r'\tan '+cf(k,'t')),str(a*n)),pp('t',2))),((a*n-k*T*sec)/T,frac(add(str(a*n),cf(-k,'t'+r'\sec '+cf(k,'t'))),'t')),((T*T*k*sec+1)/T**2,frac(add(cf(k,pp('t',2)+r'\sec '+cf(k,'t')),'1'),pp('t',2)))]
    else:
        b,c=p['b'],p['c'];f=a*X**2+b*X*Y**2;u=s.log(T);v=c*s.exp(k*T)
        F=latex(f);U=latex(u);V=latex(v);fx=s.diff(f,X);fy=s.diff(f,Y);gg=(fx.subs({X:u,Y:v},simultaneous=True),fy.subs({X:u,Y:v},simultaneous=True));dd=(s.diff(u,T),s.diff(v,T));gx,gy=map(latex,(fx,fy));gxv,gyv=map(latex,gg);gx='('+gx+')';gxv='('+gxv+')';dx,dy=map(latex,dd)
        # Substitute the actual printed coordinate expressions before reduction.
        subx='('+cf(2*a,'('+U+')')+'+'+cf(b,'('+V+')^{2}')+')';suby=cf(2*b,'('+U+')('+V+')')
        prod='('+gxv+')('+dx+')+('+gyv+')('+dy+')';distributed=latex(2*a*s.log(T)/T)+'+'+latex(b*c*c*s.exp(2*k*T)/T)+'+'+latex(2*b*c*c*k*s.log(T)*s.exp(2*k*T))
        blocks=[gradblock(F,[vec(gx,gy)]),alg('∇f(r(t))',[vec(subx,suby),vec(gxv,gyv)]),derivative(U,V,dx,dy),final(gxv,gyv,dx,dy,[prod,distributed,latex(s.diff(f.subs({X:u,Y:v},simultaneous=True),T))])];banks=[]
    fx=s.diff(f,X);fy=s.diff(f,Y);gg=[z.subs({X:u,Y:v},simultaneous=True) for z in (fx,fy)];dd=[s.diff(z,T) for z in (u,v)]
    correct=s.factor(gg[0]*dd[0]+gg[1]*dd[1])
    if name=='log_cos':banks=[(z,v.replace('{t}^{','t^{').replace('+',' + ').replace('-',' - ')) for z,v in banks]
    return dict(f=f,u=u,v=v,F=F,U=U,V=V,blocks=blocks,banks=banks,correct=correct,gg=gg,dd=dd)


def authored_solution(b):
    # Exactly the shared five formal sections; both coordinate derivatives retained.
    F,U,V=b['F'],b['U'],b['V']
    return ('The chain rule in vector form states that\n\n$$\n'+RULE+'\n$$\n\nFirst, we need to compute $∇f(x,y):$\n\n$$\n'+b['blocks'][0]+'\n$$\n\nNext, we substitute $x='+U+'$ and $y='+V+'$ into the above to find $∇f(r(t)):$\n\n$$\n'+b['blocks'][1]+'\n$$\n\nNow, we calculate the derivative of $r(t),$ which is\n\n$$\n'+b['blocks'][2]+'\n$$\n\nFinally, applying the chain rule, we get\n\n$$\n'+b['blocks'][3]+'\n$$')

def render(name,b):
    source_id=TEMPLATES[name]
    if source_id and QUESTIONS[source_id].get(':question/worked-solution'):
        raw=QUESTIONS[source_id];sol=raw[':question/worked-solution'];blocks=[RULE,*b['blocks']];i=iter(blocks)
        sol=re.sub(r'\$\$.*?\$\$',lambda m:'$$\n'+next(i)+'\n$$',sol,flags=re.S)
        sol=re.sub(r'Next, we substitute \$x=.*?\$ and \$y=.*?\$',lambda m:'Next, we substitute $x='+b['U']+'$ and $y='+b['V']+'$',sol)
        # Prompt layout is source, with complete function and curve components only.
        problem=raw[':question/problem'];problem=re.sub(r'(\$f\(x,y\)=).*?(\$ and \$r\(t\)=).*?(\$)',lambda m:m[1]+b['F']+m[2]+vec(b['U'],b['V'])+','+m[3],problem)
        return problem,sol
    if name=='log_cos':problem='If $f(x, y) = '+b['F']+'$ and $r(t) = '+b['U']+'i + '+b['V']+'j$, compute $\\frac{d}{dt}[f(r(t))]$.'
    else:problem='If $f(x,y)='+b['F']+'$ and $r(t)='+vec(b['U'],b['V'])+',$ compute $'+OP+'.$'
    return problem,authored_solution(b)

def sample(name,rng):
    if name=='mixed_polynomial':return {'a':rng.randint(1,3),'b':rng.randint(1,3),'c':rng.randint(1,3),'k':rng.randint(1,2)}
    if name=='atan_squared':return {'a':rng.randint(1,4),'k':rng.randint(2,5),'l':rng.randint(2,5)}
    p=ORIGINAL[name].copy()
    for k in p:
        if name=='polylog' and k=='n':continue
        if name=='cos_exp' and k=='k':p[k]=rng.choice([1,2,3,'pi']);continue
        p[k]=rng.randint(1,3)
    return p

def identity(payload):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(payload,sort_keys=True,ensure_ascii=False)))
def equivalent(a,b):
    # Exact rational canonicalization: common exp(kt) bases and trig relations.
    z=a-b;z=z.xreplace({e:(s.sin(e.args[0])/s.cos(e.args[0]) if e.func==s.tan else 1/s.cos(e.args[0])) for e in z.atoms(s.tan,s.sec)});E=s.Symbol('exp_base',positive=True)
    z=z.xreplace({e:E**s.simplify(e.args[0]/T) for e in z.atoms(s.exp) if s.simplify(e.args[0]/T).is_Integer})
    trig=z.atoms(s.sin,s.cos);angles={e.args[0] for e in trig};pairs={v:(s.Dummy('sin'),s.Dummy('cos')) for v in angles}
    z=z.xreplace({e:pairs[e.args[0]][0 if e.func==s.sin else 1] for e in trig})
    numerator=s.fraction(s.cancel(z))[0]
    for sv,cv in pairs.values():
        if numerator.has(cv):numerator=s.rem(numerator,cv**2+sv**2-1,cv)
    return numerator==0

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unsupported difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('This KP uses radio only')
    rng=random.Random(seed);names=[n for n in TEMPLATES if LEVEL[n]==level];name=template or rng.choice(names)
    if name not in names:raise ValueError('Template/difficulty mismatch')
    profile=profile or 'authored'
    for _ in range(300):
        p=parameters.copy() if parameters is not None else sample(name,rng)
        validate_parameters(level,name,p,profile);b=build(name,p);correct=b['correct']
        if profile in ('observed','raw_observed'):bank=b['banks']
        else:
            g,h=b['gg'];du,dv=b['dd']
            exprs=[correct,g*du,g*du-h*dv,g+h,g*dv+h*du]
            bank=[(s.factor(z),latex(s.factor(z))) for z in exprs]
        if len(bank)==5 and sum(equivalent(z,correct) for z,_ in bank)==1 and not any(equivalent(z,w) for i,(z,_) in enumerate(bank) for w,_ in bank[:i]):break
        if parameters is not None:raise ValueError('Complete bank invalid/ambiguous for explicit parameters')
    else:raise RuntimeError('No valid whole bank after rejection sampling')
    prompt,solution=render(name,b)
    if profile=='authored':
        prompt=prompt.replace('{sin}^{',r'\sin^{').replace('{cos}^{',r'\cos^{')
        solution=solution.replace('{sin}^{',r'\sin^{').replace('{cos}^{',r'\cos^{')
    values=[v for _,v in bank];correct_value=next(v for z,v in bank if equivalent(z,correct));task=[s.srepr(b['f']),s.srepr(b['u']),s.srepr(b['v'])]
    fingerprint=hashlib.sha256(json.dumps(task).encode()).hexdigest()
    content={'version':VERSION,'prompt':prompt,'solution':None if profile=='raw_observed' else solution,'bank':sorted(values),'correct':None if profile=='raw_observed' else correct_value,'type':'radio','key':'selection'}
    qid=identity(content);fid=identity([qid,'selection']);answers=[{':answer/id':identity([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=next(a[':answer/id'] for a in answers if a[':answer/value']==correct_value);rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':name,'profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fingerprint,'source_id':TEMPLATES[name],'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'authored_level':name in ('mixed_polynomial','atan_squared','log_cos'),'domain':('t>0' if name in ('polylog','mixed_polynomial') or name=='log_power' and p['n']%2 else 't != 0' if name=='log_power' else ('t != 0 and cos('+str(p['k'])+'*t)'+('*t' if p['a']*p['n']%2 else '')+'>0') if name=='log_cos' else 'all real t'),'dependencies':{'sympy':s.__version__},'bank_recipes':(['correct','omit_second_dot_term','reverse_second_dot_term','omit_coordinate_derivatives','swap_coordinate_derivatives'] if profile=='authored' else ['observed symbolic expression pattern; see extraction']),'plots':'none','evidence_only':profile!='authored','eligible_for_learning':profile=='authored'}}

    if profile=='raw_observed':
        record['question'].pop(':question/worked-solution');record['question'].pop(':question/difficulty');field.pop(':answer-field/correct')
        record['generation'].update(evidence_only=True,ineligible_for_practice=True,source_missing=['difficulty','worked-solution','correct-designation'])
    return record

# Easy — five observed rated families plus the unrated lesson exercise.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate — all three polynomial partial/dot contributions stay nonzero.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard — squared product argument and both nonunit coordinate chains are mandatory.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' [correct]' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '') for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No captured worked solution; evidence only.]')

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=['authored','observed','raw_observed']);args=ap.parse_args()
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(_apply_source_notation(records),indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
