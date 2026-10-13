#!/usr/bin/env python3
"""Scalar line-integral SETUP along graphs y(x), basis 1356; stop after step 7.

Observed profiles retain all nine complete banks, fixed instructional prose and
ordered stages. Their fixed expression patterns have genuinely variable bounds
and endpoints. Distractor intent is not inferred from one expression. Normal
banks are separately authored whole operation banks, rejected as a whole on
complete-definite-integral value collisions. Explicit observed_evidence is a
review-only replay API, including raw ambiguous banks; never a normal sampler.
No evaluation questions, y-graphs, general parametric branches or plots.
See 17592186152159/{classification,template-extraction,review,validation}.md/json.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
import mpmath as mp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication
D=Path(__file__).with_suffix('')
OBS=json.loads((D/'observed-templates.json').read_text())
KP_ID=17592186152159
KP_UUID='e381c74c-43ed-5588-ba9a-4c7d4fb2caf3'
TITLE='Reducing the Line Integral of a Scalar Function Along a Curve to a Definite Integral'
VERSION='scalar-graph-setup-1'
x,y,t=sp.symbols('x y t',real=True)
LOC={'x':x,'y':y,'t':t,'e':sp.E,'E':sp.E,'exp':sp.exp,'sin':sp.sin,'cos':sp.cos,'log':sp.log,'sqrt':sp.sqrt,'Abs':sp.Abs}
AUTH={'shifted_quadratic': 'moderate','shifted_quadratic_sine':'moderate','cubic_squared_quotient':'hard','cubic_squared_product':'hard'}


def expr(s): return sp.sympify(s,locals=LOC)
def tex(e):
    return sp.latex(sp.sympify(e)).replace(r'\log',r'\ln').replace(' ','')

def group(s,i):
    if i>=len(s) or s[i]!='{': raise ValueError('expected TeX group: '+s[i:])
    n=1;j=i+1
    while j<len(s) and n:
        n+=(s[j]=='{')-(s[j]=='}');j+=1
    if n: raise ValueError('unbalanced TeX group')
    return s[i+1:j-1],j

@lru_cache(maxsize=4096)
def parse_math(raw):
    """Independent reader of printed subset of TeX, no generation metadata."""
    s=raw.replace('\u2061','').replace(r'\left','').replace(r'\right','')
    s=s.replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{ln}',r'\ln')
    s=s.replace(r'\,','').replace(r'\cdot','*').replace(r'\displaystyle','')
    def convert(v):
        out='';i=0
        while i<len(v):
            if v.startswith('\\frac',i) or v.startswith('\\dfrac',i):
                i+=6 if v.startswith('\\dfrac',i) else 5
                while i<len(v) and v[i].isspace():i+=1
                a,i=group(v,i)
                while i<len(v) and v[i].isspace():i+=1
                b,i=group(v,i);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif v.startswith('\\sqrt',i):
                i+=5;a,i=group(v,i);out+=' sqrt('+convert(a)+') '
            elif v[i]=='{':
                a,i=group(v,i);out+='('+convert(a)+')'
            elif v[i]=='^':out+='**';i+=1
            elif v[i]=='\\':
                m=re.match(r'\\(sin|cos|ln|exp)',v[i:])
                if not m:raise ValueError('unsupported command '+v[i:])
                out+=' '+('log' if m[1]=='ln' else m[1])+' ';i+=len(m[0])
            else:out+=v[i];i+=1
        # Source uses unparenthesized function inputs, including sin(t^2).
        out=re.sub(r'\b(sin|cos|log)\s*([txy])(?:\*\*\(([-0-9]+)\))?',lambda m:m[1]+'('+m[2]+('**('+m[3]+')' if m[3] else '')+')',out)
        out=re.sub(r'\b(sin|cos|log)\s*\(([txy])\)\*\*\(([-0-9]+)\)',r'\1(\2**(\3))',out)
        return out
    c=convert(s)
    c=re.sub(r'(?<![A-Za-z])([xyte]{2,})(?![A-Za-z])',lambda m:'*'.join(m[1]),c)
    c=re.sub(r'\|([^|]+)\|',r' Abs(\1) ',c)
    return parse_expr(c,local_dict=LOC,transformations=standard_transformations+(implicit_multiplication,))

@lru_cache(maxsize=4096)
def parse_integral(raw):
    s=raw.replace(r'{\int }',r'\int').replace(r'\displaystyle','').strip()
    i=s.index(r'\int');prefix=s[:i].strip();i+=4
    if s[i:i+1]!='_':raise ValueError('definite lower bound missing')
    a,i=group(s,i+1)
    if s[i:i+1]!='^':raise ValueError('definite upper bound missing')
    b,i=group(s,i+1)
    body=s[i:].strip()
    body=re.sub(r'\\cdot\s*\\text\{d\}t$',r'\\,\\mathrm{d}t',body)
    for suffix in [r'\,\text{d}t',r'\,\mathrm{d}t',r'\,dt','dt']:
        if body.endswith(suffix):body=body[:-len(suffix)];break
    else:raise ValueError('differential missing: '+body)
    return sp.simplify((parse_math(prefix) if prefix else 1)*parse_math(body)),parse_math(a),parse_math(b)

@lru_cache(maxsize=4096)
def numeric_integral(e,a,b,dps=45):
    with mp.workdps(dps):
        fn=sp.lambdify(t,e,'mpmath');av=mp.mpf(str(sp.N(a,dps)));bv=mp.mpf(str(sp.N(b,dps)))
        return mp.quad(fn,[av,(av+bv)/2,bv])

@lru_cache(maxsize=8192)
def equivalent_integrals(A,B):
    ea,a,b=A;eb,c,d=B
    if a==c and b==d and ea==eb:return True
    if ea.is_polynomial(t) and eb.is_polynomial(t):
        return sp.simplify(sp.integrate(ea,(t,a,b))-sp.integrate(eb,(t,c,d)))==0
    va=numeric_integral(ea,a,b);vb=numeric_integral(eb,c,d)
    if abs(va-vb)>mp.mpf('1e-30')*max(1,abs(va),abs(vb)):return False
    va=numeric_integral(ea,a,b,80);vb=numeric_integral(eb,c,d,80)
    return abs(va-vb)<mp.mpf('1e-60')*max(1,abs(va),abs(vb))

def collisions(values):
    parsed=[parse_integral(v) for v in values]
    return [(i,j) for i in range(len(parsed)) for j in range(i) if equivalent_integrals(parsed[i],parsed[j])]

def integral(e,a,b):return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+tex(e)+r'\,\mathrm{d}t'

def normal_solution(g,f,a,b):
    gt=g.subs(x,t);dy=sp.diff(gt,t);speed=sp.sqrt(1+dy**2);sub=f.subs({x:t,y:gt}, simultaneous=True);ft=sp.simplify(sub)
    # Keep substitution and derivative squares as ordered unevaluated masks.
    sub_tex=re.sub(r'\\[A-Za-z]+|[xy]',lambda m:(('t' if m[0]=='x' else '('+tex(gt)+')') if m[0] in ['x','y'] else m[0]),tex(f))
    return ("Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)="+tex(gt)+".$ This gives the following parametrization of the curve:\n\n$$\nr(t)=\\langle t,"+tex(gt)+r'\rangle,\quad '+tex(a)+r'\le t\le '+tex(b)+"\n$$\n\nComputing $r'(t)$ and $\\|r'(t)\\|,$ we get the following:\n\n$$\n\\begin{aligned}r'(t)&=\\frac{\\mathrm{d}x}{\\mathrm{d}t}i+\\frac{\\mathrm{d}y}{\\mathrm{d}t}j\\\\&=\\frac{\\mathrm{d}}{\\mathrm{d}t}(t)i+\\frac{\\mathrm{d}}{\\mathrm{d}t}("+tex(gt)+r")j\\&=i+("+tex(dy)+r")j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+("+tex(dy)+r")^2}\\&="+tex(speed)+"\\end{aligned}\n$$\n\nNow, since $f(x,y)="+tex(f)+"$, we obtain\n\n$$\nf(r(t))="+sub_tex+"="+tex(ft)+".\n$$\n\nTherefore, we can write the integral as\n\n$$\n\\begin{aligned}\\int_C f(x,y)\\,\\mathrm{d}s&=\\int_{"+tex(a)+"}^{"+tex(b)+r"}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{"+tex(a)+"}^{"+tex(b)+"}("+tex(ft)+r")\cdot ("+tex(speed)+r")\,\mathrm{d}t\\&="+integral(sp.simplify(ft*speed),a,b)+".\\end{aligned}\n$$")

def observed(template,p):
    o=OBS[template];g=expr(o['curve']);f=expr(o['scalar']);a=expr(p['a']);b=expr(p['b'])
    def fill(mask):
        s=mask.replace('@A@',tex(a)).replace('@B@',tex(b))
        if o['endpoint_masks']:
            comma=', ' if ', ' in o['endpoint_masks'][0] else ','
            s=s.replace('@POINT_A@','('+tex(a)+comma+tex(g.subs(x,a))+')').replace('@POINT_B@','('+tex(b)+comma+tex(g.subs(x,b))+')')
        return s
    prompt=fill(o['prompt_mask']);solution=fill(o['solution_mask']) or normal_solution(g,f,a,b)
    return g,f,a,b,prompt,solution,[fill(v) for v in o['bank_masks']],o['correct_index']

def authored(template,p):
    a,b=expr(p['a']),expr(p['b'])
    if template in OBS:
        g=expr(p.get('curve_scale','1'))*expr(OBS[template]['curve']);f=expr(p.get('scalar_scale','1'))*expr(OBS[template]['scalar'])
    else:
        c,k=expr(p['c']),expr(p['k'])
        if template.startswith('shifted_quadratic'):
            g=c*x**2+k;f=x*y if template=='shifted_quadratic' else y*sp.sin(x)
        else:
            g=c*x**3+k*x;f=y**2/x if template=='cubic_squared_quotient' else x*y**2
    gt=g.subs(x,t);ft=sp.simplify(f.subs({x:t,y:gt},simultaneous=True));dy=sp.diff(gt,t);speed=sp.sqrt(1+dy**2)
    # Whole bank: correct; omit ds; omit scalar; omit dx component from speed;
    # omit square root. There is no first-valid recipe pool.
    math=[ft*speed,ft,speed,ft*sp.sqrt(dy**2),ft*(1+dy**2)]
    prompt='Which of the following is equivalent to the integral $\\int_C '+tex(f)+r'\,\mathrm{d}s$, where $C$ is the section of the curve $y='+tex(g)+'$ for $'+tex(a)+r'\le x\le '+tex(b)+'$?'
    return g,f,a,b,prompt,normal_solution(g,f,a,b),[integral(v,a,b) for v in math],0

def guard(level,template,p,profile):
    if template not in OBS and template not in AUTH:raise ValueError('unknown template')
    if template in AUTH and AUTH[template]!=level:raise ValueError('template difficulty mismatch')
    if template in OBS and level!='easy':raise ValueError('observed templates are easy')
    expected={'a','b'} if template in OBS else {'a','b','c','k'}
    if template in OBS and profile=='authored_operations' and ('curve_scale' in p or 'scalar_scale' in p):
        expected|={'curve_scale','scalar_scale'}
        for key in ['curve_scale','scalar_scale']:
            v=expr(p.get(key,'0'))
            if not v.is_Integer or not 1<=v<=3:raise ValueError('easy scales integers 1..3')
    if set(p)!=expected:raise ValueError('parameter keys must equal '+str(expected))
    a,b=expr(p['a']),expr(p['b'])
    if not a.is_real or not b.is_real or not bool(a<b):raise ValueError('finite increasing real bounds required')
    if not bool(0<=a) or not bool(b<=6):raise ValueError('bounds outside supported 0..6 graph domain')
    if template in ['reciprocal_product','log_exponential','cubic_squared_quotient'] and not bool(a>0):raise ValueError('positive x required')
    if template=='quadratic_sine' or template=='shifted_quadratic_sine':
        if not bool(b<=3):raise ValueError('sine bounds limited to positive first half-cycle')
    if template in AUTH:
        for key in ['c','k']:
            v=expr(p[key])
            if not v.is_Integer or not 1<=v<=3:raise ValueError('nonzero positive integer c,k in 1..3 required')
        if not 1<=a<b<=3:raise ValueError('authored moderate/hard bounds 1<=a<b<=3')
    if profile not in ['authored_operations','observed','observed_evidence']:raise ValueError('unknown profile')
    if profile.startswith('observed') and template not in OBS:raise ValueError('no observed bank for authored template')

def sample(level,template,r):
    if template in AUTH:
        a,b=r.choice([(1,2),(1,3),(2,3)])
        return {'a':str(a),'b':str(b),'c':str(r.randint(1,3)),'k':str(r.randint(1,3))}
    if template=='quadratic_sine':return {'a':str(r.choice([0,1])),'b':str(r.choice([2,3]))}
    if template in ['log_exponential','reciprocal_product']:return {'a':str(r.choice([1,2])),'b':str(r.choice([3,4,5]))}
    return {'a':str(r.choice([0,1])),'b':str(r.choice([2,3,4]))}

def make_identity(payload):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(payload,sort_keys=True)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('only observed radio layout supported')
    r=random.Random(seed);allowed=list(OBS) if level=='easy' else [k for k,v in AUTH.items() if v==level]
    template=template or r.choice(allowed);profile=profile or 'authored_operations'
    for attempt in range(300):
        p=dict(parameters) if parameters is not None else sample(level,template,r)
        if parameters is None and template in OBS and profile=='authored_operations':
            p.update(curve_scale=str(r.randint(1,3)),scalar_scale=str(r.randint(1,3)))
        # canonicalize numeric spellings; incidental profile aliases stay out of identity
        p={k:str(expr(v)) for k,v in p.items()};guard(level,template,p,profile)
        g,f,a,b,prompt,solution,values,correct=observed(template,p) if profile.startswith('observed') else authored(template,p)
        bad=collisions(values)
        if bad and profile!='observed_evidence':
            if parameters is not None:raise ValueError('whole bank rejected: equivalent complete definite integral choices '+str(bad))
            continue
        break
    else:raise ValueError('no eligible whole-bank instance')
    task=hashlib.sha256(json.dumps([sp.srepr(g),sp.srepr(f),sp.srepr(a),sp.srepr(b)],sort_keys=True).encode()).hexdigest()
    qid=make_identity([VERSION,prompt,solution,sorted(values),values[correct]])
    fid=make_identity([qid,'selection']);answers=[{':answer/id':make_identity([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=answers[correct][':answer/id'];r.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':task,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'source_ids':[OBS[template]['source_id']] if template in OBS else [],'authored_level':template in AUTH or template=='quadratic_ratio','evidence_only':profile=='observed_evidence','complete_integral_collisions':bad,'missing_source_correct_designation':template=='quadratic_ratio','plot_rating':'none','sympy_version':sp.__version__}}

# EASY: eight labeled sources and one unrated authored-assigned source.
# Fixed observed expressions; bounded endpoints give peer setup tasks. Normal
# defaults have separately authored complete wrong-operation banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE (authored missing level): quadratic graph with nonzero shift;
# x*y or y*sin(x) substitutions keep graph differentiation at source workload.
# c,k integers 1..3 and 1<=a<b<=3; one substitution with extra additive component.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored missing level): cubic graph plus nonzero linear term and squared
# y in the scalar; canonical y^2/x anchors quotient branch. No integration.
# Both same-level peers have two-component derivative and squared substitution.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(str(i+1)+'. $'+a[':answer/value']+'$' for i,a in enumerate(f[':answer-field/choices']))+'\n\nWorked solution:\n\n'+q[':question/worked-solution']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(v) for v in records))
if __name__=='__main__':main()
