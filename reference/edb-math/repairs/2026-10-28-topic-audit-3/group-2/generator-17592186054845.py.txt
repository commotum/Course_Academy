#!/usr/bin/env python3
"""Seeded implicit-differentiation practice; runtime is relocation independent."""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '1.3.1'
KP = {'db_id':17592186054845,'id':'9bf25f86-6b27-5eaa-b1a1-1104478b290a','title':'Finding the Derivative of a Function Given in Implicit Form'}
x,y=s.symbols('x y', real=True)
FAMILIES={'easy':['polynomial'],'moderate':['trig_y','trig_x'],'hard':['log','exp_e','exp_base']}
SUPPORT={'polynomial':['2984bf32-2567-5b2e-b294-6e69e5cdd26e'], 'trig_y':['59d2e907-e788-5a22-93a9-c49ff94df6ca','673feb27-4ae3-559c-903e-378e7e84b56d','7c519aff-3b88-5ec5-ac50-6662be88074b'], 'trig_x':['610d7896-a073-528d-972b-ac6b8950750a'], 'log':['ee119daa-efcf-505f-b183-08b031d8df4a'], 'exp_e':['7ce22a4d-4733-52a4-87c2-c2e0529b4bfc'], 'exp_base':['6f1bcac1-7671-548e-9f90-d7ed9245d85d']}
DY=r'\frac{\mathrm{d}y}{\mathrm{d}x}'

def tex(expr):
    return normalize_tex(s.latex(expr, ln_notation=True, fold_func_brackets=False))

def uid(text):
    return str(uuid.uuid5(uuid.UUID(KP['id']),text))

def quotient(n,d):
    return s.Mul(n,s.Pow(d,-1,evaluate=False),evaluate=False)

def qtex(n,d):
    # Render division directly. Unevaluated SymPy multiplication can print
    # 1 followed by a fraction, which resembles a mixed number in the UI.
    sign='-' if n.could_extract_minus_sign() else ''
    if sign:n=-n
    return normalize_tex(sign+r'\frac{'+tex(n)+'}{'+tex(d)+'}')

def components(p):
    """An ordered derivative construction, separate from CAS verification."""
    f=p['family'];a=s.Integer(p['a']);b=s.Integer(p.get('b',1));c=s.Integer(p['c'])
    rule=''
    if f=='polynomial':
        g=y*y+b*y;h=a*x;N=a;D=2*y+b
        den=[D,y+b,2*y-b,2*y,y*y-b]
    elif f=='trig_y':
        t=s.Integer(p['t']);fun=s.sin if p['trig']=='sin' else s.cos
        v=s.cos(y) if p['trig']=='sin' else -s.sin(y)
        n=s.Integer(p.get('n',3));g=y**n+t*fun(y);h=a*x*x;N=2*a*x;D=n*y**(n-1)+t*v
        den=[D,n*y**(n-1)-t*v,y**(n-1)-t*v,n*y**(n-1)+t*fun(y),n*y**(n-1)]
        rule='Apply the chain rule to both functions of $y$, including the trigonometric derivative.'
    elif f=='trig_x':
        k=s.Integer(p['k']);g=y*y+b*y;h=a*s.tan(k*x);N=a*k*s.sec(k*x)**2;D=2*y+b
        den=[D,y+b,2*y-b,2*y,y*y-b]
        rule='The chain rule gives $'+r'\frac{\mathrm{d}}{\mathrm{d}x}('+tex(h)+')='+tex(N)+'$.'
    elif f=='log':
        base=s.Integer(p['base']);g=s.log(y)/s.log(base);h=a*x*x;N=2*a*x;D=1/(y*s.log(base))
        den=[D,1/y,s.log(base)/y,1/s.log(base),s.log(base)/(y*y)]
        rule='For $y>0$, the logarithmic chain rule gives $'+r'\frac{\mathrm{d}}{\mathrm{d}x}(\log_{'+str(base)+r'}(y))=\frac{1}{y\ln('+str(base)+')}'+DY+'$.'
    elif f in ['exp_e','exp_base']:
        base=s.E if f=='exp_e' else s.Integer(p['base']);E=base**y
        L=s.Integer(1) if base==s.E else s.log(base)
        g=E+b*y;h=a*x if f=='exp_e' else a*x*x
        N=a if f=='exp_e' else 2*a*x;D=E*L+b
        if f=='exp_e': den=[D,E-b,E,E+b*y,E/y-b]
        else: den=[D,E+b,E*L,E/L-b,E*L-b]
        rule='The exponential chain rule gives $'+r'\frac{\mathrm{d}}{\mathrm{d}x}('+tex(E)+')='+tex(E*L)+DY+'$.'
    else: raise ValueError(f)
    nums=[N,-N,N/2,-N/2,a*x*x] if f in ['trig_y','log','exp_base'] else [N,-N,s.Integer(1),s.Integer(-1),-a*x]
    if f=='trig_x':
        k=s.Integer(p['k']);q=a*k*s.cot(k*x)**2
        nums=[N,-N,q,-q,-a*k*s.sec(k*x)]
    return g,h,c,N,D,den,nums,rule

def build(p,band,profile='rule',order=None,bank_override=None):
    g,h,c,N,D,den,nums,rule=components(p)
    f=p['family']
    # Preserve original operator arguments; no CAS rewrite of the keyed quotient.
    correct=tex(s.Mul(N,y,s.log(p['base']))) if f=='log' else qtex(N,D)
    if bank_override is None:
        # Each complete bank crosses a sign error with a derivative-rule error.
        # Both numerator and denominator decisions remain live in every bank.
        da,db=(den[1],den[2]) if profile=='rule' else (den[3],den[4])
        nm=nums[2] if profile=='rule' else nums[4]
        if f=='trig_x' and profile=='rule':nm=-nm
        pairs=[(N,D),(-N,D),(N,da),(-N,da),(nm,db)]
        expressions=[n/d for n,d in pairs]
        values=[qtex(n,d) for n,d in pairs]
        if f=='log':values=[tex(s.cancel(n/d)) for n,d in pairs]
        for i in range(5):
            for j in range(i):
                if s.simplify(expressions[i]-expressions[j])==0: raise ValueError('coincident bank')
    else:
        values=bank_override
    assert correct in values, (correct,values)
    gtex=(r'\log_{'+str(p['base'])+r'}(y)') if f=='log' else tex(g)
    # Two equivalent equation layouts exercise collection from either side.
    if p.get('layout',0)==0:
        equation=gtex+'='+tex(h+c)
    else:
        equation=gtex+'-('+tex(h)+')='+tex(c)
    problem='Given that $'+equation+'$, calculate $'+DY+'$.'
    deriv=tex(D)
    solution='Differentiate both sides with respect to $x$, treating $y$ as a function $y(x)$.'
    if rule: solution+=' '+rule
    if f=='log':
        expanded=tex(D)+DY
    elif f in ['polynomial','trig_x']:
        expanded=tex(2*y)+DY+('+' if p['b']>0 else '-')+tex(abs(p['b']))+DY
    elif f=='trig_y':
        _,_,_,_,_,_,_,_=components(p)
        v=s.cos(y) if p['trig']=='sin' else -s.sin(y)
        term=p['t']*v
        n=s.Integer(p.get('n',3))
        expanded=tex(n*y**(n-1))+DY+('+' if not term.could_extract_minus_sign() else '-')+tex(-term if term.could_extract_minus_sign() else term)+DY
    else:
        base=s.E if f=='exp_e' else s.Integer(p['base']);L=1 if f=='exp_e' else s.log(base)
        expanded=tex(base**y*L)+DY+('+' if p['b']>0 else '-')+tex(abs(p['b']))+DY
    rows=[r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+gtex+r'\right)&=\frac{\mathrm{d}}{\mathrm{d}x}\left('+tex(h+c)+r'\right)',expanded+'&='+tex(N)]
    solution+='\n\n$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
    solution+='\n\nCollect the terms containing $'+DY+'$, factor, and solve:'
    rows=[r'\left('+deriv+r'\right)'+DY+'&='+tex(N),DY+'&='+qtex(N,D)]
    if f=='log':rows.append(DY+'&='+correct)
    solution+='\n\n$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
    solution+='\n\nThis formula applies on real branches where $'+deriv+r'\ne 0$.'
    if f=='log':solution+=' The logarithm also requires $y>0$.'
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    values=[normalize_tex(v) for v in values]
    # Content-derived identities are computed only after math normalization.
    identity=json.dumps([band,problem,solution,values],sort_keys=True)
    qid=uid(identity);correct_id=uid(qid+':'+correct)
    choices=[{':answer/id':uid(qid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    if order is not None: choices=[choices[i] for i in order]
    record={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':[{':answer-field/id':uid(qid+':field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'generator_version':VERSION,'template':f,'profile':profile,'parameters':p.copy(),'source_question_ids':SUPPORT[f],'domain':'real regular implicit branches'+('; y>0' if f=='log' else ''),'final_expression':correct}}
    return validate_generated_record(record)

def sample_params(rng,f,sign=None):
    a=(rng.choice([-1,1]) if sign is None else sign)*rng.randint(2,4 if f=='polynomial' else 3)
    p={'family':f,'a':a,'b':rng.choice([-2,-1,1,2]),'c':rng.randint(-3,3),'layout':rng.randrange(2)}
    if f=='trig_y':
        p.update(n=rng.choice([2,3]),t=rng.choice([-1,1]),trig=rng.choice(['sin','cos']))
        # For a negative x² coefficient the RHS is bounded above by c.
        # Quadratic+cos has minimum t at y=0; c>t gives regular roots.
        # Quadratic+/-sin has a regular zero at y=0 and attains positives.
        # Cubic families are unbounded in both directions.
        if p['n']==2 and a<0:
            p['c']=(p['t']+rng.randint(1,3)) if p['trig']=='cos' else rng.randint(0,3)
    if f=='trig_x':p['k']=rng.randint(1,3)
    if f=='log':p['base']=rng.choice([2,3,10])
    if f=='exp_base':
        p['base']=rng.choice([2,3]);y0=rng.choice([0,1,2]);p['c']=p['base']**y0+p['b']*y0-a
    return p

def generate(band,count,seed):
    rng=random.Random(seed);out=[];seen=set()
    families=FAMILIES[band][:];rng.shuffle(families)
    profiles=['rule','term'];rng.shuffle(profiles)
    occurrences={f:0 for f in families};sign_decks={f:[] for f in families};position_decks={f:[] for f in families}
    for i in range(count):
        f=families[i%len(families)];profile=profiles[(i//len(families)+i)%2] if len(families)%2==0 else profiles[i%2]
        # The profile cycle is independent of family; a full two-family cycle changes it.
        if len(families)==2:profile=profiles[(i//2+i%2)%2]
        # Decision signs and answer positions use independent shuffled decks.
        # Every recurring family exercises both x-derivative signs before reuse.
        if not position_decks[f]:
            position_decks[f]=list(range(5));rng.shuffle(position_decks[f])
        # Profiles alternate on each recurrence of a family. A four-item
        # sign cycle balances both adjacent family pairs and repeated profiles.
        # Repeating shuffled two-sign decks alone can correlate a bank profile
        # with the correct numerical rank in an entire finite batch.
        if (occurrences[f] % 4)==0:
            sign_decks[f]=[rng.choice([-1,1])]
        start_sign=sign_decks[f][0]
        sign=start_sign * (1 if occurrences[f] % 4 in (0,3) else -1)
        position=position_decks[f].pop();occurrences[f]+=1
        for attempt in range(200):
            p=sample_params(rng,f,sign);order=list(range(1,5));rng.shuffle(order);order.insert(position,0)
            try:r=build(p,band,profile,order)
            except ValueError:continue
            gg,hh,cc,*_=components(p)
            semantic=s.srepr(gg-hh-cc)
            if semantic in seen:continue
            seen.add(semantic);r['generation'].update(seed=seed,index=i,attempt=attempt);out.append(r);break
        else:raise RuntimeError('Could not construct a distinct valid instance')
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=list(FAMILIES)+['unclassified'],default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    if a.count<0:p.error('count must be nonnegative')
    print(json.dumps(generate('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
