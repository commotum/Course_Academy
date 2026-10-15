#!/usr/bin/env python3
"""Product-rule trig questions, math basis 1356; steps 3–7 only.

Easy reproduces ten observed layouts (including two unrated radios and one
fieldless question repaired with a full-derivative blank). Moderate authors a
binomial polynomial times sin/cos/tan. Hard authors a two-term polynomial times
an affine trig function: same two-factor product rule, six distributed terms.
No composed trig arguments, tangent slopes, quotient rule or chain rule.
Explicit parameters obey the same bounded workload guards as random samples.
Observed raw profiles preserve the documented q-319350 incorrect first LHS;
normal generation repairs that LHS. Source masks replace complete mathematical
components in one pass, never learner prose or function-variable labels.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
X=s.Symbol('x', real=True)
KP_ID=17592186096617
KP_UUID='b194bf2f-feaa-5656-a3ee-0ff466a39e77'
TITLE='Differentiating a Product Containing a Trigonometric Function'
VERSION='product-trig-v1'
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
SOURCES=tuple(QUESTIONS)
TRIG={'sin':s.sin,'cos':s.cos,'tan':s.tan}

def tex(e):
    return s.latex(e).replace(r'\log',r'\ln')
def norm(t):
    t=t.replace('\\\\','\\').replace('\u2061','').replace('′',"'")
    t=re.sub(r'\\operatorname\{(sin|cos|tan|sec|csc|ln)\}',r'\\\1',t)
    t=re.sub(r'\{(sin|cos|tan|sec|csc|ln)\}',r'\\\1',t)
    t=re.sub(r'(?<![\\])(sin|cos|tan|sec|csc|ln)',r'\\\1',t)
    return t

def masked(text, slots):
    """One-pass full component substitution; longest component wins."""
    if not slots:return text
    return re.sub('|'.join(re.escape(k) for k in sorted(slots,key=len,reverse=True)),lambda m:slots[m.group()],text)

def source_data(t,p):
    """Each operation bank is complete, and not pooled or fitted to scalars."""
    if t in ('q-1907','q-47965'):
        c,n=p['c'],p['n']; u=c*X**n; du=s.diff(u,X); v=s.cos(X) if t=='q-1907' else s.tan(X)
        slots={r'x^{2}':tex(u)}
        if t=='q-1907': bank=[u*s.cos(X)-u*s.sin(X),du*s.cos(X)-du*s.sin(X),du*s.cos(X)-u*s.sin(X),u*s.cos(X)-du*s.sin(X),du*s.cos(X)+u*s.sin(X)]
        else: bank=[du+u*s.sec(X)*s.tan(X),c*X**(n-1)*s.tan(X)*(n*X+s.sec(X)),du*s.sec(X)*s.tan(X),s.diff(u*v,X),s.sec(X)*(n*c+u*s.tan(X))]
        return u,v,slots,bank,None
    if t=='q-310188':
        b=p['b']; u=s.Integer(b)**X; v=s.sin(X); slots={'{3}^{x}': '{'+str(b)+'}^{x}', r'\operatorname{ln}(3)':r'\operatorname{ln}('+str(b)+')'}
    elif t=='q-319402':
        k=p['k']; u=k-s.tan(X); v=s.cos(X); slots={r'2-\operatorname{tan}(x)':str(k)+r'-\operatorname{tan}(x)',r'\operatorname{tan}(x)-2':r'\operatorname{tan}(x)-'+str(k)}
    elif t in ('q-71004','q-104297','q-1931','q-319350'):
        c=p['c']; u=c*s.exp(X); v={'q-71004':s.sin(X),'q-104297':s.cos(X),'q-1931':s.tan(X),'q-319350':p.get('k',2)+s.sin(X)}[t]
        exp=('{e}^{x}' if c==1 else str(c)+'{e}^{x}')
        slots={'{e}^{x}':exp}
        if t=='q-319350':slots['2+sin⁡(x)']=str(p['k'])+'+sin⁡(x)'
        if t=='q-319350':slots[r'2+\operatorname{sin}(x)']=str(p['k'])+r'+\operatorname{sin}(x)'
    elif t=='q-319357':
        c,n=p['c'],p['n']; u=c*X**n;v=s.cos(X);slots={'2{x}^{2}':tex(u),'4x':tex(s.diff(u,X))}
    elif t=='q-319385':
        c=p['c'];u=c*s.sqrt(X);v=s.tan(X)
        slots={r'\frac{tan⁡(x)}{2\sqrt{x}}':tex(c*s.tan(X)/(2*s.sqrt(X))),r'\frac{1}{2\sqrt{x}}':tex(c/(2*s.sqrt(X))),r'\sqrt{x}':tex(u)}
    else: raise ValueError(t)
    du,dv=s.diff(u,X),s.diff(v,X)
    if t=='q-104297':bank=[-u*s.cos(X)-u*s.sin(X),u*s.cos(X)+s.sin(X),du*v+u*dv,-u*s.cos(X)+s.sin(X),u*s.cos(X)+u*s.sin(X)]
    elif t=='q-1931':bank=[u*s.sec(X)+u*s.sec(X)**2,s.sec(X)**2+u*s.tan(X),u*s.csc(X)**2+u*s.tan(X),u*s.sec(X)**2+s.tan(X),du*v+u*dv]
    else:bank=None
    fragment={'q-310188':du*v,'q-319402':u*dv,'q-319350':du*v,'q-319357':du*v,'q-319385':u*dv,'q-71004':du*v+u*dv}.get(t)
    return u,v,slots,bank,fragment

def bounds(t,level,p):
    expected={
      'q-1907':{'c','n'},'q-47965':{'c','n'},'q-310188':{'b'},'q-319402':{'k'},
      'q-71004':{'c'},'q-104297':{'c'},'q-1931':{'c'},'q-319350':{'c','k'},'q-319357':{'c','n'},'q-319385':{'c'},
      'binomial':{'a','n','b','trig'},'affine_trig':{'a','n','b','d','trig'}}[t]
    if set(p)!=expected:raise ValueError('Parameter keys differ from template contract')
    for k,v in p.items():
        if k=='trig':
            if v not in TRIG:raise ValueError('Unsupported trig')
        elif type(v)!=int:raise ValueError('Integer required')
        elif k=='n':
            if not 2<=v<=4:raise ValueError('Power 2..4')
        elif k=='b' and t=='q-310188':
            if not 2<=v<=7:raise ValueError('Base 2..7')
        elif k in ('a','b','d') and t in ('binomial','affine_trig'):
            if not 1<=abs(v)<=4:raise ValueError('Nonzero signed magnitude 1..4')
        elif not 1<=v<=6:raise ValueError('Source extension positive 1..6')

def sample(t,r):
    if t in ('binomial','affine_trig'):
        p=dict(a=r.choice([-4,-3,-2,-1,1,2,3,4]),b=r.choice([-4,-3,-2,-1,1,2,3,4]),n=r.randint(2,4),trig=r.choice(tuple(TRIG)))
        if t=='affine_trig':p['d']=r.choice([-4,-3,-2,-1,1,2,3,4])
        return p
    if t=='q-310188':return {'b':r.randint(2,7)}
    if t=='q-319402':return {'k':r.randint(1,6)}
    p={'c':r.randint(1,6)}
    if t in ('q-1907','q-47965','q-319357'):p['n']=r.randint(2,4)
    if t=='q-319350':p['k']=r.randint(1,6)
    return p

def solution(u,v):
    du,dv=s.diff(u,X),s.diff(v,X)
    applied=f'({tex(du)})({tex(v)})+({tex(u)})({tex(dv)})'
    distributed=s.expand(du*v+u*dv)
    return (f'Here, we have the product of the two functions $u(x)={tex(u)}$ and $v(x)={tex(v)}.$ So, we apply the product rule:\n\n$$\n'
      +r'\begin{aligned}(('+tex(u)+')('+tex(v)+r"))^{'} & =u'(x)\cdot v(x)+u(x)\cdot v'(x) \\ & =("+tex(u)+r")'\cdot ("+tex(v)+')+('+tex(u)+r")\cdot ("+tex(v)+r")' \\ & ="+applied+r' \\ & ='+tex(distributed)+r'\end{aligned}'+'\n$$')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type is not None and field_type not in ('radio','blank'):raise ValueError('Unsupported field type')
    allowed=SOURCES if level=='easy' else ('binomial',) if level=='moderate' else ('affine_trig',)
    r=random.Random(seed);t=template or r.choice(allowed)
    if t not in allowed:raise ValueError('Template outside level')
    profile=profile or ('authored' if t not in SOURCES else 'repaired')
    if profile not in ('authored','repaired','observed_raw'):raise ValueError('Unknown profile')
    if t not in SOURCES and profile!='authored':raise ValueError('Authored template requires authored profile')
    for attempt in range(100):
        p=parameters.copy() if parameters is not None else sample(t,r);bounds(t,level,p)
        if t in SOURCES:
            raw=QUESTIONS[t];u,v,slots,bank,fragment=source_data(t,p)
            prompt=masked(raw[':question/problem'],slots)
            worked=masked(raw.get(':question/worked-solution',''),slots)
            if not worked:worked=solution(u,v)
            if t=='q-319350' and profile!='observed_raw':
                worked=worked.replace('('+masked('{e}^{x}sec⁡(x)',slots)+')', '('+masked('{e}^{x}(2+sin⁡(x))',slots)+')',1)
            original_fields=raw.get(':question/answer-fields',[])
            kind='radio' if bank is not None else 'blank'
            if bank is not None:values=[tex(e) for e in bank];correct=s.diff(u*v,X)
            else:
                correct=fragment; values=[norm(masked(original_fields[0][':answer-field/choices'][0][':answer/value'],slots))] if original_fields else [tex(correct)]
            if not original_fields:prompt+='\n\n$(('+tex(u)+')('+tex(v)+r"))'= $ {{field-1}}"
            if bank is not None and profile=='observed_raw':
                # Render complete explicit shape recipes, not literal-value lookup.
                original=[a[':answer/value'] for a in original_fields[0][':answer-field/choices']]
                if t=='q-1907':
                    maps={r'2x':tex(s.diff(u,X)),r'x^{2}':tex(u)}
                elif t=='q-47965':
                    # Each complete answer is a mask; x( is not a valid slot
                    # because it also occurs in trig-function arguments.
                    c,n=p['c'],p['n']; pre=tex(c*X**(n-1));du=tex(s.diff(u,X));ut=tex(u)
                    shapes=[du+r' + '+ut+r'\sec x\tan x',pre+r'\tan x('+str(n)+r'x + \sec x)',du+r'\sec x\tan x',pre+'('+str(n)+r'\tan x + x\sec^{2} x)',r'\sec x('+str(n*c)+' + '+ut+r'\tan x)']
                    maps=dict(zip(original,shapes))
                else:maps=slots
                values=[masked(a,maps) for a in original]
        else:
            u=p['a']*X**p['n']+p['b']*(X if t=='affine_trig' else 1)
            v=TRIG[p['trig']](X)+(p.get('d',0));du,dv=s.diff(u,X),s.diff(v,X)
            correct=du*v+u*dv;kind=field_type or 'radio'
            prompt=f'Differentiate $({tex(u)})({tex(v)}).$'
            worked=solution(u,v)
            bank=[correct,du*dv,du*v,u*dv,du*v-u*dv]
            values=[tex(e) for e in bank] if kind=='radio' else [tex(correct)]
            if kind=='blank':prompt+='\n\n'+r"$f'(x)=$ {{field-1}}"
        if field_type and field_type!=kind:raise ValueError('Cannot change observed field layout')
        parsed=[parse(a) for a in values]
        matched=[i for i,a in enumerate(parsed) if equivalent(a,correct)]
        if len(matched)!=1 or any(equivalent(a,b) for i,a in enumerate(parsed) for b in parsed[i+1:]):
            if parameters is not None:raise ValueError('Ambiguous complete bank')
            continue
        key='selection' if kind=='radio' else 'field-1'
        identity=hashlib.sha256(json.dumps([VERSION,level,prompt,worked,kind,sorted(values)],sort_keys=True).encode()).hexdigest()
        qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),key))
        answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),a)),':answer/type':':answer.type/math',':answer/value':a} for a in values]
        correct_id=answers[matched[0]][':answer/id'];r.shuffle(answers)
        question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
        fingerprint=hashlib.sha256(json.dumps([s.srepr(s.expand(u*v)),s.srepr(s.expand(correct))]).encode()).hexdigest()
        return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'sympy_version':s.__version__,'seed':seed,'template':t,'profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':fingerprint,'content_hash':identity,'domain':'x>0 and cos(x) != 0' if t=='q-319385' else 'real x where displayed factors are differentiable'}}
    raise ValueError('No valid complete bank')

# Easy: observed partial derivatives/full radios; bounds in bounds().
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate (authored missing level): full two-term polynomial × primitive trig.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard (authored missing level): two-term polynomial × affine primitive trig,
# with six substantive distributed products and no additional calculus rule.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

# Independent displayed-expression parser; no reference to generation parameters.
# It reads standard, source operatorname, and Unicode trig notations and primes.
def parse(text,functions=None):
    text=norm(text).replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('⁡','')
    text=re.sub(r"\^\{\s*'\s*\}","'",text)
    text=re.sub(r"\{([uv])\}\^\{'\}",r"\1'",text)
    text=re.sub(r"\{([uv])\}",r"\1",text)
    text=text.replace('{e}', 'e')
    tokens=re.findall(r'\\(?:frac|sqrt|sin|cos|tan|sec|csc|ln)|[A-Za-z]+|\d+|[^\s]',text)
    pos=0; funcs=functions or {}
    def peek():return tokens[pos] if pos<len(tokens) else None
    def take():
        nonlocal pos
        z=peek();pos+=1;return z
    def atom():
        z=take()
        if z in ('+','-'): a=atom();return a if z=='+' else -a
        if z in ('(','{'):
            a=expr();assert take()==(')' if z=='(' else '}')
        elif z==r'\frac':a=atom()/atom()
        elif z==r'\sqrt':a=s.sqrt(atom())
        elif z in (r'\sin',r'\cos',r'\tan',r'\sec',r'\csc',r'\ln'):
            power=None
            if peek()=='^':take();power=atom()
            arg=atom();a={'\\sin':s.sin,'\\cos':s.cos,'\\tan':s.tan,'\\sec':s.sec,'\\csc':s.csc,'\\ln':s.log}[z](arg)
            if power is not None:a=a**power
        elif z and z.isdigit():a=s.Integer(z)
        elif z=='x':a=X
        elif z=='e':a=s.E
        elif z in funcs:
            a=funcs[z]
            if peek()=="'":take();a=s.diff(a,X)
            if peek()=='(':take();assert take()=='x';assert take()==')'
        else:raise ValueError((text,z,tokens))
        while peek() in ('^',"'"):
            op=take();a=a**atom() if op=='^' else s.diff(a,X)
        return a
    def product():
        a=atom()
        while peek() and peek() not in ('+','-',')','}'):
            if peek() in ('*','/'):
                op=take();b=atom();a=a*b if op=='*' else a/b
            else:a=a*atom()
        return a
    def expr():
        a=product()
        while peek() in ('+','-'):
            op=take();b=product();a=a+b if op=='+' else a-b
        return a
    out=expr()
    if pos!=len(tokens):raise ValueError(('unconsumed',text,tokens[pos:]))
    return out

@lru_cache(maxsize=16384)
def equivalent(a,b):
    difference=s.expand(a-b)
    if difference==0:return True
    # An exact nonzero value at a regular test point disproves equality.
    # This short circuit never proves equality by sampling.
    value=s.simplify(difference.subs(X,s.pi/4))
    if value.is_zero is False:return False
    return s.trigsimp(s.simplify(difference))==0

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']));print(q[':question/worked-solution'])
if __name__=='__main__':main()
