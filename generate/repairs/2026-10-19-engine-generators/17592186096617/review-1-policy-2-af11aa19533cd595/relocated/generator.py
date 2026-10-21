#!/usr/bin/env python3
"""Seeded, relocatable easy product-rule/trig generator.

Retains all eleven supplied source cases and complete banks for raw replay.
Normal output repairs missing fields/keys/solutions and q-319350's source LHS.
Supported extensions: bounded signed scalars/powers, missing-term role selection,
and primitive trig selection in the two polynomial cosine-bank profiles.
No generated assets, publication, repository imports or database operations.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache, wraps
from pathlib import Path
import sympy as s
from math_format import checked_math_content, normalize_prose, normalize_tex
X=s.Symbol('x', real=True)
KP_ID=17592186096617
KP_UUID='b194bf2f-feaa-5656-a3ee-0ff466a39e77'
TITLE='Differentiating a Product Containing a Trigonometric Function'
VERSION='product-trig-package-v4'
CAPTURE=json.loads(Path(__file__).with_name('source-data.json').read_text())
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
    t=re.sub(r'\\(sin|cos|tan|sec|csc|ln)(?=[A-Za-z])',lambda m:'\\'+m[1]+' ',t)
    return t

def masked(text, slots):
    """One-pass full component substitution; longest component wins."""
    if not slots:return text
    return re.sub('|'.join(re.escape(k) for k in sorted(slots,key=len,reverse=True)),lambda m:slots[m.group()],text)

def source_data(t,p):
    """Each operation bank is complete, and not pooled or fitted to scalars."""
    if t in ('q-1907','q-47965','q-104300'):
        c,n=p['c'],p['n']; u=c*X**n; du=s.diff(u,X); v=TRIG[p.get('trig','cos')](X) if t!='q-47965' else s.tan(X)
        slots={r'x^{2}':tex(u),r'{x}^{3}':tex(u),r'3{x}^{2}':tex(s.diff(u,X))}
        if t=='q-1907': bank=[u*v+u*derivative(v),du*v+du*derivative(v),du*v+u*derivative(v),u*v+du*derivative(v),du*v-u*derivative(v)]
        elif t=='q-104300': bank=[du*v-du*derivative(v),u*v-du*derivative(v),du*v+u*derivative(v),-u*v-du*derivative(v),-du*v+u*derivative(v)]
        else: bank=[du+u*s.sec(X)*s.tan(X),c*X**(n-1)*s.tan(X)*(n*X+s.sec(X)),du*s.sec(X)*s.tan(X),du*v+u*s.sec(X)**2,s.sec(X)*(n*c+u*s.tan(X))]
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
    du,dv=derivative(u),derivative(v)
    if t=='q-104297':bank=[-u*s.cos(X)-u*s.sin(X),u*s.cos(X)+s.sin(X),du*v+u*dv,-u*s.cos(X)+s.sin(X),u*s.cos(X)+u*s.sin(X)]
    elif t=='q-1931':bank=[u*s.sec(X)+u*s.sec(X)**2,s.sec(X)**2+u*s.tan(X),u*s.csc(X)**2+u*s.tan(X),u*s.sec(X)**2+s.tan(X),du*v+u*dv]
    else:bank=None
    fragment={'q-310188':du*v,'q-319402':u*dv,'q-319350':du*v,'q-319357':du*v,'q-319385':u*dv,'q-71004':du*v+u*dv}.get(t)
    return u,v,slots,bank,fragment

def bounds(t,level,p):
    expected={
      'q-104300':{'c','n'},'q-1907':{'c','n'},'q-47965':{'c','n'},'q-310188':{'b'},'q-319402':{'k'},
      'q-71004':{'c'},'q-104297':{'c'},'q-1931':{'c'},'q-319350':{'c','k'},'q-319357':{'c','n'},'q-319385':{'c'},
      'binomial':{'a','n','b','trig'},'affine_trig':{'a','n','b','d','trig'}}[t]
    if set(p)!=expected:raise ValueError('Parameter keys differ from template contract')
    for k,v in p.items():
        if k=='trig':
            if v not in TRIG:raise ValueError('Unsupported trig')
        elif type(v)!=int:raise ValueError('Integer required')
        elif k=='n':
            if not 1<=v<=4:raise ValueError('Power 1..4')
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
    if t in ('q-1907','q-47965','q-319357'):p['n']=r.randint(1,4)
    if t=='q-319350':p['k']=r.randint(1,6)
    return p

def derivative(e):
    # Keep the taught primitive tan derivative sec²; CAS expansion would add
    # two unrelated distribution terms and violate the declared workload.
    return s.diff(e,X).subs(s.tan(X)**2+1,s.sec(X)**2)

def solution(u,v):
    du,dv=derivative(u),derivative(v)
    # Continuation rows keep each product-rule stage visible in the actual UI.
    # The defined u,v abbreviate the long LHS without changing the operation.
    lines=[r"(u(x)v(x))' &=u'(x)\cdot v(x)+u(x)\cdot v'(x)",
      r"&=("+tex(u)+r")'\cdot ("+tex(v)+')',
      r"&\quad +("+tex(u)+r")\cdot ("+tex(v)+r")'",
      '&=('+tex(du)+')('+tex(v)+')',
      r'&\quad +('+tex(u)+')('+tex(dv)+')',
      '&='+tex(du*v),
      r'&\quad +('+tex(u*dv)+')']
    return (f'Here, we have the product of the two functions $u(x)={tex(u)}$ and $v(x)={tex(v)}.$ So, we apply the product rule:\n\n$$\n'
      +r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$')


def checked_content(function):
    """Run shared formatting checks while preserving absent raw-source keys."""
    @wraps(function)
    def checked(*args,**kwargs):
        record=function(*args,**kwargs)
        temporary={**record,'question':dict(record['question'])}
        temporary['question'].setdefault(':question/worked-solution','')
        checked_math_content(lambda:temporary)()
        return record
    return checked

@checked_content
def replay_generator(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
            if bank is not None:
                correct=s.diff(u*v,X)
                if t=='q-47965' and profile!='observed_raw':
                    du,dv=derivative(u),derivative(v)
                    correct=du*v+u*dv
                    bank=[correct,du*dv,du*v,u*dv,du*v-u*dv]
                values=[tex(e) for e in bank]
            else:
                correct=fragment; values=[norm(masked(original_fields[0][':answer-field/choices'][0][':answer/value'],slots))] if original_fields else [tex(correct)]
            if not original_fields and profile!='observed_raw':prompt+='\n\n$(('+tex(u)+')('+tex(v)+r"))'= $ {{field-1}}"
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
            v=TRIG[p['trig']](X)+(p.get('d',0));du,dv=derivative(u),derivative(v)
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
        prompt=normalize_prose(prompt);worked=normalize_prose(worked)
        if profile=='observed_raw' and ':question/worked-solution' not in raw:worked=''
        for text in (prompt,worked,*values):
            if any(ord(c)<32 and c not in '\n\t' for c in text):raise ValueError('Unintended C0 control character')
        values=[normalize_tex(value) for value in values]
        key='selection' if kind=='radio' else 'field-1'
        presence=[profile!='observed_raw' or key in raw for key in (':question/difficulty',':question/worked-solution',':question/answer-fields')]
        correct_present=profile!='observed_raw' or bool(original_fields and ':answer-field/correct' in original_fields[0])
        identity=hashlib.sha256(json.dumps([VERSION,level,prompt,worked,kind,sorted(values),presence,correct_present],sort_keys=True).encode()).hexdigest()
        qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),key))
        answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),a)),':answer/type':':answer.type/math',':answer/value':a} for a in values]
        correct_id=answers[matched[0]][':answer/id'];r.shuffle(answers)
        question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
        if profile=='observed_raw':
            for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
                if key not in raw:question.pop(key,None)
            for field,original in zip(question.get(':question/answer-fields',[]),original_fields):
                if ':answer-field/correct' not in original:field.pop(':answer-field/correct',None)
        fingerprint=hashlib.sha256(json.dumps([s.srepr(s.expand(u*v)),s.srepr(s.expand(correct.subs(s.sec(X)**2,1+s.tan(X)**2)))]).encode()).hexdigest()
        return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':s.__version__,'evidence_only':profile=='observed_raw','eligible_for_learning':profile!='observed_raw','bank_origin':'authored method-derived replacement for opaque observed bank' if t=='q-47965' and profile!='observed_raw' else ('observed' if t in SOURCES else 'authored'),'seed':seed,'template':t,'profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':fingerprint,'content_hash':identity,'domain':'x>0 and cos(x) != 0' if t=='q-319385' else 'real x where displayed factors are differentiable'}}
    raise ValueError('No valid complete bank')

def canonical_prose(text):
    # Repair legacy trig spellings inside math only, preserving source prose.
    return normalize_prose(re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',lambda m:norm(m.group()),text))


def record_for(t,p,seed,missing=None):
    u,v,slots,bank,fragment=source_data(t,p)
    du,dv=derivative(u),derivative(v)
    terms=[du*v,u*dv]
    raw=QUESTIONS[t]
    kind='radio' if bank is not None else 'blank'
    intro=canonical_prose(masked(raw[':question/problem'].split('\n\n')[0],slots))
    # Changed trig must update the problem rather than only the key.
    if t in ('q-1907','q-104300'):
        intro=f'Differentiate ${tex(u)}{tex(v)}$.'
    if bank is not None:
        correct=du*v+u*dv
        # Preserve complete mathematical source banks. Independent per-choice
        # distribution prevents the opaque tangent bank's longest-option cue.
        notation=random.Random(seed+7919)
        flags=[bool(notation.getrandbits(1)) for _ in bank] if t=='q-47965' else [False]*len(bank)
        values=[normalize_tex(tex(s.expand(e) if expand else e)) for e,expand in zip(bank,flags)]
    else:
        if t=='q-71004':
            correct=sum(terms);missing='full'
            tail='{{field-1}}'
        else:
            correct=terms[missing]
            tail=('{{field-1}} $+\\,('+tex(terms[1])+')$' if missing==0 else '$'+tex(terms[0])+r'\,+$ {{field-1}}')
        intro+='\n\n$('+tex(u*v)+r")'= $ "+tail
        values=[normalize_tex(tex(correct))]
    if len({s.srepr(s.expand(parse(z))) for z in values})!=len(values):
        raise ValueError('Duplicate bank')
    matches=[i for i,z in enumerate(values) if equivalent(parse(z),correct)]
    if len(matches)!=1:raise ValueError('Invalid key')
    for i,a in enumerate(values):
        for b in values[i+1:]:
            if equivalent(parse(a),parse(b)):raise ValueError('Equivalent choices')
    worked=normalize_prose(solution(u,v))
    prompt=normalize_prose(intro)
    key='selection' if kind=='radio' else 'field-1'
    digest=hashlib.sha256(json.dumps([VERSION,t,p,missing,prompt,values],sort_keys=True).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),digest));fid=str(uuid.uuid5(uuid.UUID(qid),key))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),z)),':answer/type':':answer.type/math',':answer/value':z} for z in values]
    correct_id=answers[matches[0]][':answer/id']
    random.Random(seed).shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':qid,':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{
      ':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},
      'generation':{'version':VERSION,'seed':seed,'template':t,'profile':('same-method-trig-extension' if t in ('q-1907','q-104300') and p.get('trig')!='cos' else 'observed-bank') if bank else 'completion-repair' if t=='q-71004' else 'completion',
       'parameters':p,'bank_expansion':flags if bank is not None else None,'missing_term':missing,'source_difficulty':raw.get(':question/difficulty'),'domain':'x>0 and cos(x)!=0' if t=='q-319385' else 'real x where the factors are differentiable',
       'source_basis':CAPTURE['basis'],'python_version':sys.version.split()[0],'sympy_version':s.__version__}}


@checked_content
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,missing_term=None):
    if level!='easy':raise ValueError('Unsupported band: only source-justified easy is supported')
    if profile=='observed_raw':
        return replay_generator(level,seed,template,field_type,parameters,profile)
    if profile not in (None,'repaired'):raise ValueError('Unsupported profile')
    r=random.Random(seed);t=template or r.choice(SOURCES)
    if t not in SOURCES:raise ValueError('Unsupported template')
    # Decision roles first; scalar values second.
    missing=missing_term if missing_term is not None else r.randrange(2)
    if missing not in (0,1):raise ValueError('Missing term must be 0 or 1')
    trig=r.choice(tuple(TRIG)) if t in ('q-1907','q-104300') else None
    p=dict(parameters) if parameters is not None else sample(t,r)
    if t=='q-104300' and parameters is None:p={'c':r.randint(1,6),'n':r.randint(1,4)}
    if t in ('q-1907','q-104300'):
        p.setdefault('trig',trig)
    scalar={k:abs(v) if k=='c' else v for k,v in p.items() if k!='trig'}
    bounds(t,level,scalar)
    if parameters is None and 'c' in p:p['c']*=r.choice([-1,1])
    out=record_for(t,p,seed,missing)
    if field_type and not out['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/'+field_type):raise ValueError('Fixed source response contract')
    return out


def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)

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
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']));print(q.get(':question/worked-solution',''))
if __name__=='__main__':main()
