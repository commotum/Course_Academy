#!/usr/bin/env python3
"""Local-only parameterized partial-derivative-at-a-point generator.

No numeric registered artifact is imported. All explicit parameters obey the same
family domain as sampling. The source profiles retain opaque historical banks as
ineligible evidence; normal profiles use complete method-derived five-choice banks.
See the private extraction and validation evidence beside this script.
"""
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent.parent.parent
PRIVATE=Path(__file__).with_suffix('')
ID=17592186124644
VERSION='partial-point-draft-v2-arithmetic-bounds'
SOURCE=json.loads((PRIVATE/'source.json').read_text())
KP=SOURCE['record']
TITLE=KP[':knowledge-point/title']
ORIGINALS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
_spec=importlib.util.spec_from_file_location('partial_point_math_format',ROOT/'scripts/question_capture/math_format.py')
_fmt=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_fmt)
u,v=S.symbols('u v',real=True)
a,b,n,m=S.symbols('a b n m',positive=True,integer=True)
x,y=S.symbols('x y',real=True)
LOCALS={'pi':S.pi,'e':S.E,'E':S.E,'sqrt':S.sqrt,'ln':S.log,'log':S.log,'sin':S.sin,'cos':S.cos,'tan':S.tan,'sec':S.sec,'cot':S.cot,'csc':S.csc,'u':u,'v':v,'a':a,'b':b,'n':n,'m':m}
def sym(z):
    if isinstance(z,bool): raise ValueError('Boolean is not a mathematical parameter')
    try:return S.sympify(z,locals=LOCALS)
    except Exception as exc:raise ValueError('Invalid exact parameter') from exc

def tex(z):
    text=S.latex(S.sympify(z),ln_notation=True).replace(r'\left', '').replace(r'\right','')
    for variable in ('u','v','x','y'):
        text=text.replace(r'\tan{('+variable+r' )} \sec{('+variable+r' )}',r'\sec{('+variable+r' )} \tan{('+variable+r' )}')
    # A numeric coefficient followed by Euler e is written as an actual
    # product, avoiding the native parser's scientific-notation ambiguity.
    text=re.sub(r'(?<=[0-9}]) e(?=\b|\^)',lambda _:r' \cdot e',text)
    return text
def group(z):return '('+tex(z)+')'
def coef(z):return '' if sym(z)==1 else tex(z)
def join(t1,t2,sign):
    if t2.lstrip().startswith('-'):
        t2=t2.lstrip()[1:].lstrip();sign=-sign
    return t1+('+' if sign==1 else '-')+t2

def family(source,target,level,h1,g1,h2,g2,sign,anchor,coords,ns=(2,),ms=(2,),eval_kind='terms',rewrite=False):
    return dict(source=source,target=target,level=level,h1=h1,g1=g1,h2=h2,g2=g2,sign=sign,anchor=anchor,coords=coords,ns=ns,ms=ms,eval_kind=eval_kind,rewrite=rewrite)
# h_i(v) are held constant; g_i(u) are differentiated. Coordinates are (u0,v0),
# not physical (x0,y0). A target swap reorders the supplied point accordingly.
FAMILIES={
 'tan-reciprocal':family('q-132257','x','hard',a*v**2,S.tan(u),b*v,u**-1,1,dict(a=1,b=1,n=2,m=2,U='pi',V=2),([S.pi,2*S.pi,-S.pi,-2*S.pi],[2,3,4]),eval_kind='terms',rewrite=True),
 'base-exponential-tan':family('q-159604','x','hard',a*S.tan(v),2**u,b*v/S.pi,u**-n,1,dict(a=1,b=1,n=2,m=2,U=1,V='pi/4'),([1,2,3],[S.pi/4,3*S.pi/4]),ns=(2,3),eval_kind='terms',rewrite=True),
 'sin-cos-linear':family('q-159585','x','hard',a*S.cos(v),S.sin(u),b*v,u,-1,dict(a=1,b=1,n=2,m=2,U=0,V='pi'),([0,S.pi,-S.pi,2*S.pi],[S.pi,2*S.pi,-S.pi,-2*S.pi]),eval_kind='cos-product'),
 'power-log-root':family('q-159597','x','moderate',a*S.log(v),u**n,b*v,S.sqrt(u),-1,dict(a=1,b=2,n=3,m=2,U=1,V='e'),([1,4,9],[S.E,S.E**2,S.E**3]),ns=(2,3,4),eval_kind='omit'),
 'exp-log-power':family('q-159599','y','moderate',a*S.exp(v),S.log(u),b*v**n,u,1,dict(a=1,b=1,n=7,m=2,U='1/2',V=1),([S.Rational(1,2),S.Rational(1,3),2,3],[1,2]),ns=(3,4,5,6,7),eval_kind='omit'),
 'polynomial':family('q-159602','y','moderate',a*v**2,u,b*v,u**n,-1,dict(a=4,b=1,n=4,m=2,U=1,V=2),([1,2,3],[-3,-2,-1,1,2,3]),ns=(3,4,5)),
 'sec-power':family('q-159607','y','hard',a*v,S.sec(u),b*v**n,u,1,dict(a=1,b=1,n=4,m=2,U='pi/4',V='sqrt(2)'),([S.pi/4,-S.pi/4,3*S.pi/4],[S.sqrt(2),2*S.sqrt(2),3*S.sqrt(2)]),ns=(2,4),eval_kind='sec-product'),
 'root-reciprocal':family('q-159587','y','moderate',a*S.sqrt(v),u**n,b*v,u**-1,1,dict(a=1,b=1,n=2,m=2,U=2,V=4),([1,2,3,4],[1,4,9,16]),ns=(2,3),rewrite=True),
 'cross-roots':family('q-159600','x','moderate',a*S.sqrt(v),u,b*v,S.sqrt(u),-1,dict(a=2,b=4,n=2,m=2,U=1,V=4),([1,4,9],[1,4,9])),
 'cos-log-sin':family('q-159601','y','moderate',a*S.cos(v),S.log(u),b*v,S.sin(u),-1,dict(a=1,b=1,n=2,m=2,U='pi/2',V='pi'),([S.pi/6,S.pi/4,S.pi/3,S.pi/2],[S.pi,2*S.pi,-S.pi,-2*S.pi])),
 'cot-polynomial':family('q-159606','x','hard',a*v**n,S.cot(u),b*v**m,u**2,-1,dict(a=1,b=1,n=3,m=2,U='pi/2',V=1),([S.pi/2,3*S.pi/2,-S.pi/2],[1,2,3,-1,-2]),ns=(2,3),ms=(2,3),eval_kind='csc-product'),
 'log-power-exp':family('q-159609','x','hard',a*v,S.log(u),b*S.exp(v),u**n,-1,dict(a=1,b=2,n=5,m=2,U=1,V='ln(3)'),([1,2],[S.log(2),S.log(3),S.log(4),S.log(5)]),ns=(3,4,5),eval_kind='exp-product'),
 # Authored easy: two nonzero monomial contributions, familiar integer inputs.
 'easy-polynomial':family(None,'x','easy',a*v**2,u**2,b*v,u,1,dict(a=1,b=1,n=2,m=2,U=1,V=2),([1,2,3,4],[1,2,3,4]))
}
# Candidate catalogs are deliberately small; coupled evaluated-value guards below
# decide eligibility. Coefficients alone do not control substitution workload.
FAMILIES['tan-reciprocal']['coords']=([S.pi,2*S.pi,-S.pi,-2*S.pi],[2,3])
FAMILIES['base-exponential-tan']['coords']=([1],[S.pi/4,3*S.pi/4])
FAMILIES['power-log-root']['coords']=([1,4],[S.E,S.E**2])
FAMILIES['exp-log-power']['coords']=([S.Rational(1,2),1,2],[1,2])
FAMILIES['exp-log-power']['ns']=(2,3,4,5,6,7)
FAMILIES['polynomial']['coords']=([1,2],[-2,-1,1,2])
FAMILIES['polynomial']['ns']=(3,4)
FAMILIES['sec-power']['coords']=([S.pi/4,-S.pi/4,3*S.pi/4],[S.sqrt(2),-S.sqrt(2)])
FAMILIES['root-reciprocal']['coords']=([1,2],[1,4])
FAMILIES['cross-roots']['coords']=([1,4],[1,4])
FAMILIES['cos-log-sin']['coords']=([S.pi/3,S.pi/2],[S.pi,2*S.pi,-S.pi,-2*S.pi])
FAMILIES['cot-polynomial']['coords']=([S.pi/2,3*S.pi/2,-S.pi/2],[1,-1])
FAMILIES['cot-polynomial']['ns']=(3,)
FAMILIES['cot-polynomial']['ms']=(2,)
FAMILIES['log-power-exp']['coords']=([1,2],[S.log(2),S.log(3),S.log(4),S.log(5)])
FAMILIES['easy-polynomial']['coords']=([-3,-2,-1,1,2,3],[1,2])
for family_key,family_spec in FAMILIES.items():family_spec['key']=family_key

# Maximum rational coefficient numerator/denominator in every normal option.
# Source-anchor-derived factor/product checks are listed explicitly in workload.
WORKLOAD_HEIGHTS={
 'tan-reciprocal':(9,4),'base-exponential-tan':(6,4),
 'sin-cos-linear':(3,1),'power-log-root':(9,4),'exp-log-power':(4,2),
 'polynomial':(24,1),'sec-power':(8,1),'root-reciprocal':(32,4),
 'cross-roots':(24,4),'cos-log-sin':(6,2),'cot-polynomial':(3,1),
 'log-power-exp':(30,1),'easy-polynomial':(16,1)}
SOURCE_FAMILY={f['source']:k for k,f in FAMILIES.items() if f['source']}

def parameters_for(f,parameters,rng,observed=False):
    if parameters is None:
        p=dict(f['anchor']) if observed else dict(a=rng.randint(1,4),b=rng.randint(1,4),n=rng.choice(f['ns']),m=rng.choice(f['ms']),U=rng.choice(f['coords'][0]),V=rng.choice(f['coords'][1]))
    else:
        extra=set(parameters)-{'a','b','n','m','U','V','target'}
        if extra:raise ValueError('Unknown parameters: '+str(sorted(extra)))
        p=dict(f['anchor']);p.update(parameters)
    p.setdefault('target',f['target'] if observed or parameters is not None else rng.choice(('x','y')))
    p={k:(z if k=='target' else sym(z)) for k,z in p.items()}
    if p['target'] not in ('x','y'):raise ValueError('Target must be x or y')
    for k in ('a','b'):
        if p[k].is_Integer is not True or not 1<=p[k]<=4:raise ValueError(k+' must be an integer 1..4')
    if any(p[k].is_Integer is not True for k in ('n','m')) or p['n'] not in f['ns'] or p['m'] not in f['ms']:raise ValueError('Exponent outside equal-workload family')
    for name,domain in (('U',f['coords'][0]),('V',f['coords'][1])):
        matches=[sym(value) for value in domain if S.simplify(p[name]-sym(value))==0]
        if not matches:raise ValueError('Coordinate outside familiar evaluation domain')
        p[name]=matches[0]
    return p

def instance(f,p):
    subs={a:p['a'],b:p['b'],n:p['n'],m:p['m']}
    h1,g1,h2,g2=[z.subs(subs) for z in (f['h1'],f['g1'],f['h2'],f['g2'])]
    d1,d2=S.diff(g1,u),S.diff(g2,u)
    if g1==S.cot(u):d1=-S.csc(u)**2
    if g1==S.tan(u):d1=S.sec(u)**2
    fun=h1*g1+f['sign']*h2*g2
    derivative=h1*d1+f['sign']*h2*d2
    pt={u:p['U'],v:p['V']}
    t1=S.expand_mul((h1*d1).subs(pt));t2=S.expand_mul((f['sign']*h2*d2).subs(pt));correct=S.expand_mul(t1+t2)
    if any(z.has(S.zoo,S.nan,S.oo,-S.oo) for z in (t1,t2,correct)):raise ValueError('Undefined point')
    return dict(h1=h1,g1=g1,h2=h2,g2=g2,d1=d1,d2=d2,fun=fun,derivative=derivative,t1=t1,t2=t2,correct=correct,subs=pt)

def coefficient_height(expression):
    """Height of actual reduced rational coefficients, not numeric magnitudes
    of pi/e/log atoms. For a rational scalar this checks its complete fraction.
    """
    coefficients=[term.as_coeff_Mul(rational=True)[0] for term in S.Add.make_args(S.expand_mul(expression))]
    return max(abs(int(c.p)) for c in coefficients),max(int(c.q) for c in coefficients)

def workload(f,p,z,bank=None):
    """Identical coupled bounds for explicit calls and normal resampling.

    All powers/factors here are the ones actually used by the displayed partial
    derivative and its point-substitution chain. Normal bank heights are checked
    on complete evaluated values, including wrong/wrong options.
    """
    key=f['key'];U,V,A,B,N,M=[p[k] for k in ('U','V','a','b','n','m')]
    checks=[]
    def cap(label,value,maximum):
        value=S.simplify(value);maximum=S.sympify(maximum)
        checks.append((label,value,maximum))
        if (S.Abs(value)<=maximum)!=True:raise ValueError('Arithmetic workload: '+label+' exceeds '+str(maximum))
    def height(label,value,numerator,denominator):
        hn,hd=coefficient_height(value);checks.append((label+' numerator',S.Integer(hn),S.Integer(numerator)));checks.append((label+' denominator',S.Integer(hd),S.Integer(denominator)))
        if hn>numerator or hd>denominator:raise ValueError('Arithmetic workload: '+label+' rational height')
    T1,T2=z['t1'],z['t2']
    if key=='tan-reciprocal':
        k=U/S.pi;cap('held square',V**2,9);cap('first contribution',T1,9)
        cap('reciprocal point-square coefficient',k**2,4);cap('second numerator before reciprocal',B*V,8)
        cap('reciprocal contribution coefficient',B*V/k**2,4)
    elif key=='base-exponential-tan':
        cap('exponential point value',2**U,2);cap('active reciprocal power',U**(N+1),1)
        cap('log coefficient',A*2**U,6);cap('reciprocal derivative factor',N,3)
        cap('reciprocal contribution',T2,3);height('reciprocal contribution',T2,6,4)
    elif key=='sin-cos-linear':
        cap('cosine contribution',T1,3);cap('linear pi coefficient',T2/S.pi,3)
    elif key=='power-log-root':
        cap('evaluated active power',U**(N-1),4);cap('power derivative factor',N*U**(N-1),8)
        cap('evaluated logarithm',S.log(V),2);cap('polynomial logarithm contribution',T1,9)
        cap('square-root derivative denominator',2*S.sqrt(U),4)
        cap('root contribution coefficient',B/(2*S.sqrt(U)),2)
    elif key=='exp-log-power':
        cap('evaluated held power',V**N,4);cap('held contribution',T2,4)
        cap('reciprocal derivative factor',1/U,2);cap('exponential coefficient',A/U,4)
        height('exponential coefficient',A/U,4,2)
    elif key=='polynomial':
        cap('evaluated active power',U**(N-1),2);cap('held square',V**2,4)
        cap('second derivative factor',B*N*U**(N-1),4)
        cap('first contribution',T1,16);cap('second contribution',T2,8)
        cap('total signed-term arithmetic',abs(T1)+abs(T2),24)
    elif key=='sec-power':
        cap('held power',V**N,4);cap('first contribution',T1,6);cap('second contribution',T2,4)
        cap('complete-bank largest magnitude',abs(T1)+abs(T2),8)
    elif key=='root-reciprocal':
        cap('power derivative factor',N*U**(N-1),4);cap('held square-root coefficient',A*S.sqrt(V),4)
        cap('held reciprocal numerator',B*V,8);cap('reciprocal square',U**2,4)
        cap('first contribution',T1,12);cap('second contribution',T2,4)
        cap('complete-bank largest magnitude',abs(T1)+abs(T2),12)
        height('collected key',z['correct'],24,4)
    elif key=='cross-roots':
        cap('active square root',S.sqrt(U),2);cap('held square root',S.sqrt(V),2)
        cap('held second coefficient',B*V,16);cap('sqrt derivative denominator',2*S.sqrt(U),4)
        cap('first contribution',T1,8);cap('second contribution',T2,8)
        cap('complete-bank largest magnitude',abs(T1)+abs(T2),12)
        height('collected key',z['correct'],24,4)
    elif key=='cos-log-sin':
        cap('reciprocal pi coefficient',T1*S.pi,6)
        cap('held sine coefficient',B*V/S.pi,4);cap('sine pi contribution coefficient',T2/S.pi,2)
    elif key=='cot-polynomial':
        cap('first held power',V**N,1);cap('second held power',V**M,1)
        cap('quadratic derivative pi coefficient',2*U/S.pi,3)
        cap('cosecant contribution',T1,3);cap('polynomial pi contribution',T2/S.pi,3)
    elif key=='log-power-exp':
        cap('evaluated active power',U**(N-1),1);cap('logarithm coefficient',A/U,4)
        cap('exponential held factor',B*S.exp(V),6)
        cap('power derivative prefactor',B*N*U**(N-1),10)
        cap('evaluated exponential contribution',T2,30)
    elif key=='easy-polynomial':
        cap('held square',V**2,4);cap('held first factor',A*V**2,4)
        cap('active derivative factor',2*U,6);cap('first contribution',T1,12);cap('second contribution',T2,4)
        cap('two integer contributions',abs(T1)+abs(T2),16)
    if bank is not None:
        hn,hd=WORKLOAD_HEIGHTS[key]
        for i,value in enumerate(bank):height('complete option '+str(i),value,hn,hd)
    return {label:{'actual':str(value),'maximum':str(maximum)} for label,value,maximum in checks}

def rename(text,target):
    # Only complete role tokens, never letters inside commands or prose.
    return re.sub(r'(?<![A-Za-z\\])([uv])(?=[^A-Za-z]|$)',lambda mt:target if mt[1]=='u' else ('y' if target=='x' else 'x'),text)
def rt(z,p):return rename(tex(z),p['target'])
def point(p):return ','.join(tex(p[k]) for k in (('U','V') if p['target']=='x' else ('V','U')))
def diffop(t):return r'\frac{∂}{∂'+t+'}'
def target_notation(f,p,evaluated=False):
    t=p['target'];sid=f['source']
    subscript=sid in ('q-159604','q-159585','q-159607','q-159606','q-159609')
    if subscript:return '{f}_{'+t+'}('+ (point(p) if evaluated else 'x,y')+')'
    return r'\frac{∂f}{∂'+t+'}'+ (r'{|}_{('+point(p)+')}' if evaluated else '')
def unevaluated_formula(f,z,p):
    return join(rt(z['h1']*z['g1'],p),rt(z['h2']*z['g2'],p),f['sign'])
def solution(f,z,p):
    t=p['target'];op=diffop(t);sgn='+' if f['sign']==1 else '-'
    one,two=rt(z['h1']*z['g1'],p),rt(z['h2']*z['g2'],p)
    formula=one+sgn+two
    # These are source operation stages: derivative of full sum; split sum;
    # pull held-variable coefficients outside; elementary derivatives; collect.
    g2tex=rt(z['g2'],p);d2tex=rt(z['d2'],p)
    final=join(rt(z['h1']*z['d1'],p),rt(z['h2']*z['d2'],p),f['sign'])
    if f['source']=='q-159587':
        g2tex='{'+t+'}^{-1}';d2tex='-{'+t+'}^{-2}'
        two=rt(z['h2'],p)+g2tex
        final=rt(z['h1']*z['d1'],p)+'-'+rt(z['h2'],p)+'{'+t+'}^{-2}'
    rows=[op+'('+formula+')']
    if f['rewrite']:
        # Reciprocal-to-power rewrite is present in q159587. Unrated sources
        # have no observed solution, so their authored chains use the same rule.
        if f['source']=='q-159587':rows.append(op+'('+rt(z['h1']*z['g1'],p)+'+'+two+')')
    rows.extend([op+'('+one+')'+sgn+op+'('+two+')',
        rt(z['h1'],p)+r'\cdot '+op+'('+rt(z['g1'],p)+')'+sgn+rt(z['h2'],p)+r'\cdot '+op+'('+g2tex+')',
        rt(z['h1'],p)+r'\cdot ('+rt(z['d1'],p)+')'+sgn+rt(z['h2'],p)+r'\cdot ('+d2tex+')',final])
    def aligned(lhs,rs):return r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rs)+r'\end{aligned}'
    # Simultaneous literal substitution into the printed derivative, before
    # simplifying. Always group inserted coordinates; numeric juxtaposition is
    # made explicit by the printer's multiplication operation.
    derivative=final
    physical={p['target']:p['U'],('y' if p['target']=='x' else 'x'):p['V']}
    substituted=re.sub(r'(?<![A-Za-z\\])([xy])(?=[^A-Za-z]|$)',lambda mt:'('+tex(physical[mt[1]])+')',derivative)
    ers=[substituted]
    kind=f['eval_kind']
    h1v=S.expand_mul(z['h1'].subs(v,p['V']));h2v=S.expand_mul(z['h2'].subs(v,p['V']))
    d1v=S.expand_mul(z['d1'].subs(u,p['U']));d2v=S.expand_mul(z['d2'].subs(u,p['U']))
    if kind!='omit':
        if kind in ('cos-product','sec-product','csc-product'):
            # Retain each elementary trigonometric value before collection.
            if kind=='sec-product':
                first=group(h1v)+r'\cdot '+group(S.sec(p['U']))+r'\cdot '+group(S.tan(p['U']))
            elif kind=='csc-product':
                first=group(-h1v)+r'\cdot '+group(S.csc(p['U'])**2)
            else:first=group(h1v)+r'\cdot '+group(d1v)
            second=tex(S.expand_mul(h2v*d2v))
            ers.append(first+sgn+'('+second+')')
        elif kind=='exp-product':
            c2=S.expand_mul(p['b']*p['n']*p['U']**(p['n']-1))
            ers.append(tex(z['t1'])+'-'+tex(c2)+r'\cdot '+tex(S.exp(p['V'])))
        else:ers.append(tex(z['t1'])+('+' if z['t2']>=0 else '-')+'('+tex(abs(z['t2']))+')')
    ers.append(tex(z['correct']))
    text='We differentiate the given function with respect to $'+t+',$ treating all other variables as constants:\n\nAdditionally, we use the sum and constant multiple rules for differentiation, as follows:\n\n$$\n'+aligned(target_notation(f,p),rows)+'\n$$\n\nFinally, we evaluate the partial derivative at the point $('+point(p)+'):$\n\n$$\n'+aligned(target_notation(f,p,True),ers)+'\n$$'
    return text,rows,ers

# Each observed bank is a complete expression-pattern profile in the quantities
# printed by its own prompt. Opaque numerical entries are identified in bank-map;
# these profiles are evidence-only, never sampled as normal learner defaults.
def observed_bank(key,p,z):
    U,V,A,B,N=[p[k] for k in ('U','V','a','b','n')];T1,T2,C=z['t1'],z['t2'],z['correct']
    patterns={
      'tan-reciprocal':[V-V**2/U**2,1-V/U**2,V**2-U**2,V/U**2,C],
      'base-exponential-tan':[C,1/S.log(2),T1,S.log(2)-1,2*T1-S.pi/2],
      'sin-cos-linear':[-C,-T1+T2,C,V**2-T1,-T1-V**2],
      'power-log-root':[T1,C,T1*V,-2*T2,U+V],
      'exp-log-power':[S.exp(V/U)+z['t2'],C,S.exp(V)+T2,U*S.exp(V)+T2,T1],
      'polynomial':[T1,V,N,U,C],
      'sec-power':[C,2*T2,T2,C/2,T1],
      'root-reciprocal':[C/2,(T1-T2)/2,T1-T2,C,T1+2*T2],
      'cross-roots':[T2,S.sqrt(V),C,T1,T1+T2/2],
      'cos-log-sin':[-4*V,U,C,2*V,-T1-V],
      'cot-polynomial':[T2,-2*T1-T2,-3*T2,C,-T1+2*T2],
      'log-power-exp':[-T1*T2,T1-N,T1*S.exp(V),C,T1+T2/S.exp(V)]
    }
    return [S.expand_mul(t) for t in patterns[key]]
def authored_bank(z):
    # Omit a differentiated summand, or apply the wrong sum/sign rule to it.
    t1,t2=z['t1'],z['t2']
    return [z['correct'],S.expand_mul(t1-t2),S.expand_mul(-t1+t2),t1,t2]
def nonambiguous(bank):
    return len(bank)==5 and all(S.simplify(bank[i]-bank[j])!=0 for i in range(5) for j in range(i))
def canonical(z):return S.srepr(S.simplify(z))
def fingerprint(z,p):
    # Complete task in differentiated/held roles; excludes notation, banks,
    # aliases and seeds, and includes original function (not final scalar only).
    return hashlib.sha256(json.dumps([canonical(z['fun']),canonical(p['U']),canonical(p['V'])]).encode()).hexdigest()
def uid(*parts):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(parts,sort_keys=True,ensure_ascii=False)))
def format_checks(q):
    for value in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        if any(ord(c)<32 and c not in '\n\t' for c in value):raise ValueError('C0 control character in learner content')
    # The shared full-record validator requires a solution; an observed raw
    # omission is validated with a temporary empty prose slot, without adding
    # that attribute to the public record.
    checking=copy.deepcopy(q);checking.setdefault(':question/worked-solution','')
    _fmt.validate_generated_record({'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':checking})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio response contract is supported')
    rng=random.Random(seed);observed=bool(profile and profile.startswith('observed-'))
    if profile not in (None,'method-sum-bank') and not observed:raise ValueError('Unknown bank profile')
    if observed:
        sid=profile[len('observed-'):]
        if sid not in SOURCE_FAMILY:raise ValueError('Unknown original')
        sourcekey=SOURCE_FAMILY[sid]
        if template is None:template=sourcekey
        if template!=sourcekey:raise ValueError('Source/profile family mismatch')
    if template is None:template=rng.choice([k for k,f in FAMILIES.items() if f['level']==level])
    if template not in FAMILIES:raise ValueError('Unknown template')
    f=FAMILIES[template]
    if level!=f['level']:raise ValueError('Template outside declared level')
    for attempt in range(300):
        p=parameters_for(f,parameters,rng,observed)
        z=instance(f,p)
        try:workload_metrics=workload(f,p,z)
        except ValueError:
            if parameters is not None or observed:raise
            continue
        bank=observed_bank(template,p,z) if observed else authored_bank(z)
        if not observed:
            try:workload_metrics=workload(f,p,z,bank)
            except ValueError:
                if parameters is not None:raise
                continue
        if nonambiguous(bank):break
        if parameters is not None or observed:raise ValueError('Complete bank collision; whole instance rejected')
    else:raise ValueError('No valid complete bank')
    if observed:
        # Historical banks have opaque numerical choices: publicly replay the
        # observed coordinate/coefficient domain only; do not infer their intent.
        anchor=parameters_for(f,f['anchor'],rng,True)
        if p!=anchor:raise ValueError('Opaque observed profile restricted to its documented anchor; use method-sum-bank for variations')
    sol,drows,erows=solution(f,z,p)
    formula=unevaluated_formula(f,z,p)
    subscript=f['source'] in ('q-159604','q-159585','q-159607','q-159606','q-159609')
    ask=target_notation(f,p,True) if subscript else r'\frac{∂f}{∂'+p['target']+'}'
    if f['source']:
        original_prompt=ORIGINALS[f['source']][':question/problem']
        islands=list(re.finditer(r'(?<!\$)\$(?!\$)(.*?)\$',original_prompt,re.S))
        oldformula=islands[0][1];prefix=oldformula[:oldformula.index('=')+1]
        replacements=[prefix+formula+(',' if oldformula.endswith(',') else '')]
        oldask=islands[1][1]
        if subscript:
            head=oldask[:oldask.index('(')]
            head=re.sub(r'(?<=_)\{?[xy]\}?','{'+p['target']+'}',head)
            replacements.append(head+'('+point(p)+')'+('.' if oldask.endswith('.') else ''))
        else:
            replacements.append(re.sub(r'(?<=[∂])\s*[xy]',p['target'],oldask))
            replacements.append('('+point(p)+')'+('.' if islands[2][1].endswith('.') else ''))
        prompt=original_prompt
        for match,value in reversed(list(zip(islands,replacements))):
            prompt=prompt[:match.start()]+'$'+value+'$'+prompt[match.end():]
    else:
        prompt='For the function $f(x,y)='+formula+',$ evaluate $'+ask+'$ at the point $('+point(p)+').$'
    q={':question/problem':_fmt.normalize_prose(prompt),':question/worked-solution':_fmt.normalize_prose(sol),':question/difficulty':':question.difficulty/'+level}
    bankvalues=[_fmt.normalize_tex(tex(z)) for z in bank]
    # Identity is built after shared mathematical presentation normalization;
    # option order and generation metadata never affect field/content identity.
    key_material=[VERSION,level,q[':question/problem'],q[':question/worked-solution'],sorted(bankvalues),bool(observed and ':question/difficulty' not in ORIGINALS[f['source']])]
    qid=uid('question',key_material)
    fid=uid('field',qid,'selection',':answer-field.type/radio')
    choices=[{':answer/id':uid('answer',fid,value),':answer/type':':answer.type/math',':answer/value':value} for value in bankvalues]
    matches=[i for i,t in enumerate(bank) if S.simplify(t-z['correct'])==0]
    if len(matches)!=1:raise ValueError('Bank must contain exactly one mathematically correct choice')
    correct=[':answer/id',choices[matches[0]][':answer/id']]
    if observed and ':answer-field/correct' not in ORIGINALS[f['source']][':question/answer-fields'][0]:correct=None
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if correct is not None:field[':answer-field/correct']=correct
    q.update({':question/id':qid,':question/answer-fields':[field]})
    if observed:
        original=ORIGINALS[f['source']]
        if ':question/difficulty' not in original:q.pop(':question/difficulty')
        if ':question/worked-solution' not in original:q.pop(':question/worked-solution')
    # Raw omission flags are part of the identity contract, including absent
    # solution versus present solution; recompute IDs from the actual content.
    content=[VERSION,q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution'),sorted(bankvalues),correct is not None]
    actualqid=uid('question',content);actualfid=uid('field',actualqid,'selection',':answer-field.type/radio')
    remap={aa[':answer/id']:uid('answer',actualfid,aa[':answer/value']) for aa in choices}
    for aa in choices:aa[':answer/id']=remap[aa[':answer/id']]
    q[':question/id']=actualqid;field[':answer-field/id']=actualfid
    if correct is not None:field[':answer-field/correct']=[':answer/id',remap[correct[1]]]
    format_checks(q)
    return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':{k:str(val) for k,val in p.items()},'bank_profile':profile or 'method-sum-bank','mathematical_fingerprint':fingerprint(z,p),'source_id':f['source'],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'evidence_only':observed,'eligible_for_learning':not observed,'difficulty_evidence':'observed' if f['source'] and ':question/difficulty' in ORIGINALS[f['source']] else 'authored','solution_stages':{'derivative':drows,'point_evaluation':erows},'arithmetic_workload':workload_metrics,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__}}}

def generate_easy(seed=0,**kw):return generate('easy',seed=seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed=seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed=seed,**kw)
def markdown(record):
    q=record['question'];field=q[':question/answer-fields'][0];generation=record['generation']
    difficulty=q.get(':question/difficulty','unrated (source omission)').split('/')[-1]
    header='Difficulty: '+difficulty+' · Template: `'+generation['template']+'` · Profile: `'+generation['bank_profile']+'`'
    reference=field.get(':answer-field/correct');correct=reference[1] if reference else None
    designation='' if correct else '\n\nCorrect-answer designation: absent in the captured source.'
    options='\n'.join('- $'+choice[':answer/value']+'$'+(' **(correct)**' if choice[':answer/id']==correct else '') for choice in field[':answer-field/choices'])
    return header+'\n\n'+q[':question/problem']+designation+'\n\n'+options+'\n\n'+q.get(':question/worked-solution','[No worked solution in the original captured record.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (('easy','moderate','hard') if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in records))
