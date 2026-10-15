#!/usr/bin/env python3
"""Polar function → Cartesian first derivatives, math source basis 2743; validated replenishment package.

Twelve source templates and entire five-option banks. Source banks are explicit
inferred-expression replay profiles, not recovered cognitive error diagnoses.
Default banks use authored chain-rule operations. Unevaluated substitution and
identity/distribution masks retain teaching stages; source prose is a fixed
skeleton whose COMPLETE math components are filled, never a literal replay.
Easy/hard are authored missing-level designs. No database access or writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).with_suffix('')
RAW=json.loads((ROOT/'source.json').read_text())
KP=RAW['record']; KP_ID=17592186124595
VERSION='polar-cartesian-2'
R=s.Symbol('r',positive=True)
T=s.Symbol('theta',real=True)
C,S=s.cos(T),s.sin(T)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# These are source parameters, not answer lookup values.
CASES={
 'offset_sine_y':('q-37186',dict(A=1,b=1,k=2,name='w')),
 'offset_cosine_x':('q-95001',dict(A=1,b=2,name='v')),
 'sine_minus_y':('q-165282',dict(A=1,b=1,name='h')),
 'radial_plus_sine_x':('q-95129',dict(A=1,a=2,name='h')),
 'power_cosine_y':('q-95130',dict(A=1,p=2,k=3,name='g')),
 'double_sine_x':('q-95132',dict(A=1,name='f')),
 'cosine_y':('q-95133',dict(A=1,k=2,name='w')),
 'sine_y':('q-95020',dict(A=1,k=4,name='u')),
 'offset_sine_x':('q-95134',dict(A=1,b=2,name='u')),
 'offset_cosine_y':('q-95135',dict(A=1,b=1,k=2,name='v')),
 'quadratic_plus_cosine_x':('q-165283',dict(A=1,b=2,name='v')),
 'cosine_minus_x':('q-95137',dict(A=1,b=1,name='h')),
}
TEMPLATES={**{k:'moderate' for k in CASES},'radial_only':'easy','power_offset':'hard'}
DOMAIN='r>0; real theta on any locally continuous polar angle branch; x=r*cos(theta), y=r*sin(theta).'

def norm(text):
    text=text.replace('\u2061','').replace('θ',r'\theta')
    for f in ('sin','cos'):
        text=text.replace(r'\operatorname{'+f+'}', '\\'+f)
        text=re.sub(r'\{'+f+r'\}\^\{(\d+)\}',lambda m:'\\'+f+'^{'+m[1]+'}',text)
    return text

def tex(e):
    return s.latex(s.sympify(e),fold_func_brackets=True).replace(r'\left', '').replace(r'\right','')

def mul(*pieces): return ''.join(pieces)
def scale(A,body): return body if A==1 else ('-'+body if A==-1 else str(A)+body)
def add(a,b): return a+('' if b.startswith('-') else '+')+b
def fn(kind,k=1):return '\\'+kind+' '+(str(k) if k!=1 else '')+r'\theta'
def power(n):return '' if n==0 else ('r' if n==1 else '{r}^{'+str(n)+'}')
def term(c,body):return scale(c,body)
def partial(name,axis):return r'\frac{∂'+name+'}{∂'+(r'\theta' if axis=='theta' else axis)+'}'
def aligned(rows,lhs):return r'\begin{aligned}'+lhs+' & ='+r' \\ & ='.join(rows)+r'.\end{aligned}'

def object_math(template,p):
    A=s.Integer(p['A']); b=s.Integer(p.get('b',0)); k=p.get('k',1); n=p.get('p',1); a=p.get('a',2)
    if template=='offset_sine_y': F=A*R*(b+s.sin(k*T));axis='y'
    elif template=='offset_cosine_x': F=A*R*(b+C);axis='x'
    elif template=='sine_minus_y': F=A*R*(S-b);axis='y'
    elif template=='radial_plus_sine_x': F=A*(a*R+S);axis='x'
    elif template=='power_cosine_y': F=A*R**n*s.cos(k*T);axis='y'
    elif template=='double_sine_x': F=A*R*s.sin(2*T);axis='x'
    elif template=='cosine_y': F=A*R*s.cos(k*T);axis='y'
    elif template=='sine_y': F=A*R*s.sin(k*T);axis='y'
    elif template=='offset_sine_x': F=A*R*(b+S);axis='x'
    elif template=='offset_cosine_y': F=A*R*(b+s.cos(k*T));axis='y'
    elif template=='quadratic_plus_cosine_x': F=A*(R**2+b*R*C);axis='x'
    elif template=='cosine_minus_x': F=A*R*(C-b);axis='x'
    elif template=='radial_only': F=A*R**n;axis=p['axis']
    elif template=='power_offset':F=A*R**n*(b+(s.sin(k*T) if p['kind']=='sin' else s.cos(k*T)));axis=p['axis']
    else:raise ValueError('Unknown template')
    fr=s.diff(F,R);ft=s.diff(F,T)
    u,v=(fr*C,-ft*S/R) if axis=='x' else (fr*S,ft*C/R)
    answer=s.expand(u+v)
    # Limit identity collection to the source's actual teaching operations.
    if template=='offset_cosine_x':answer=A*(b*C+1)
    elif template=='sine_minus_y':answer=A*(1-b*S)
    elif template=='double_sine_x':answer=2*A*S**3
    elif template=='offset_sine_x':answer=A*b*C
    elif template=='quadratic_plus_cosine_x':answer=A*(2*R*C+b)
    elif template=='cosine_minus_x':answer=A*(1-b*C)
    return F,axis,fr,ft,u,v,answer

def source_bank(template,p):
    A=s.Integer(p['A']);b=s.Integer(p.get('b',0)); k=p.get('k',1);n=p.get('p',1);a=p.get('a',2)
    sk,ck=s.sin(k*T),s.cos(k*T)
    if template=='offset_sine_y':bank=[b*C+C*sk-k*S*ck,b*S+S*sk+k*C*ck,S*sk+k*C*ck,b*sk+S*sk+k*C*ck,b*S+C*sk-k*S*ck];correct=1
    elif template=='offset_cosine_x':bank=[b*C+1,b*C/2+1,b*S-1,b*C,b*S+1];correct=0
    elif template=='sine_minus_y':bank=[R*(1-b*S),1+b*C,R-b*S,C-b*S,1-b*S];correct=4
    elif template=='radial_plus_sine_x':bank=[a*S+a*R*s.cos(2*T),s.sin(2*T)/(2*R),a*C+R*s.sin(2*T),a*C-s.sin(2*T)/(2*R),C**2+S**2/R];correct=3
    elif template=='power_cosine_y':bank=[R**(n-1)*(k*S*ck+n*C*sk),R**(n-1)*(n*S-k*C),n*S*ck-k*C*sk,ck-sk,R**(n-1)*(n*S*ck-k*C*sk)];correct=4
    elif template=='double_sine_x':bank=[3*S**2,C**3*S,2*S**3*C,2*S**3,2*C**3];correct=3
    elif template=='cosine_y':bank=[-k*sk*C,ck*S-k*C*sk,S+k*C,ck*(S-k*C),sk*(S-k*C)];correct=1
    elif template=='sine_y':bank=[sk+k*ck*C,S*sk+k*C,S*sk+k*ck,S+k*ck*C,S*sk+k*ck*C];correct=4
    elif template=='offset_sine_x':bank=[b*R*C,b*C,b*R*S-s.sin(2*T),b*C+s.sin(2*T),b*S];correct=1
    elif template=='offset_cosine_y':bank=[k*S*C**2-C*S**2,b*S-k*C*sk,S*ck-k*C*sk,b*S+ck-k*sk,b*S+S*ck-k*C*sk];correct=4
    elif template=='quadratic_plus_cosine_x':bank=[R*C+b*S,2*R*C,2*R*C+b,R**2*(C+s.sin(2*T)),R*(C+b/2)];correct=2
    elif template=='cosine_minus_x':bank=[-b*C,1-b*C,-b*S,1-b*S,S-b*C];correct=1
    else:raise ValueError('No observed bank for authored template')
    return [A*x for x in bank],correct

def authored_bank(template,p):
    F,axis,fr,ft,u,v,answer=object_math(template,p)
    if template=='radial_only':
        rotate=s.sin(T) if axis=='x' else s.cos(T)
        A=p['A'];n=p['p'];bank=[answer,A*n*R**(n-1)*rotate,A*R**(n-1)*(C if axis=='x' else S),R*answer,-answer]
    else:
        other=fr*S+ft*C/R if axis=='x' else fr*C-ft*S/R
        bank=[answer,u,u-v,other,u+R*v]
    return bank,0

def equivalent(x,y):
    # Integer-angle trig expressions become polynomials modulo sin²+cos²=1.
    U,V=s.symbols('_sin _cos')
    expanded=s.expand_trig(x-y).xreplace({s.sin(T):U,s.cos(T):V})
    numerator=s.fraction(s.together(expanded))[0]
    return s.rem(s.expand(numerator),U**2+V**2-1,U)==0

def assert_bank(bank):
    if len(bank)!=5:raise ValueError('whole bank must have five choices')
    for i,x in enumerate(bank):
        if x.has(s.zoo,s.nan,s.oo):raise ValueError('invalid bank')
        for y in bank[:i]:
            if equivalent(x,y):raise ValueError('equivalent whole-bank choices')

def validate_parameters(template,p):
    required=set(CASES[template][1]) if template in CASES else ({'A','p','axis','name'} if template=='radial_only' else {'A','p','b','k','kind','axis','name'})
    if set(p)!=required:raise ValueError(f'parameters must be {sorted(required)}')
    if p['name'] not in ['f','g','h','u','v','w']:raise ValueError('function name')
    bound=3 if TEMPLATES[template]=='hard' else 4
    if not isinstance(p['A'],int) or isinstance(p['A'],bool) or not 1<=abs(p['A'])<=bound:raise ValueError('nonzero bounded scale')
    for key in ('a','b','p','k'):
        if key in p and (not isinstance(p[key],int) or isinstance(p[key],bool)):raise ValueError('integer '+key)
    if 'a' in p and not 2<=p['a']<=4:raise ValueError('a bound')
    if 'b' in p and not 1<=abs(p['b'])<= (3 if template=='power_offset' else 4):raise ValueError('b bound')
    if template=='offset_cosine_x' and abs(p['b'])<2:raise ValueError('bank b != 1')
    if 'p' in p and p['p'] not in (2,3):raise ValueError('radial power bound')
    if 'k' in p and not 2<=p['k']<= (4 if template in ('power_cosine_y','power_offset') else 5):raise ValueError('frequency bound')
    if 'axis' in p and p['axis'] not in ('x','y'):raise ValueError('axis')
    if 'kind' in p and p['kind'] not in ('sin','cos'):raise ValueError('kind')

def sample(template,rng):
    p=dict(CASES[template][1]) if template in CASES else (dict(A=1,p=2,axis='x',name='f') if template=='radial_only' else dict(A=1,p=2,b=1,k=2,kind='sin',axis='x',name='f'))
    bound=3 if template=='power_offset' else 4
    p['A']=rng.choice([i for i in range(-bound,bound+1) if i])
    p['name']=rng.choice(['f','g','h','u','v','w'])
    if 'b' in p:p['b']=rng.choice([i for i in range(-bound,bound+1) if i and (template!='offset_cosine_x' or abs(i)>1)])
    if 'a' in p:p['a']=rng.randint(2,4)
    if 'p' in p:p['p']=rng.choice([2,3])
    if 'k' in p:p['k']=rng.randint(2,4 if template in ('power_cosine_y','power_offset') else 5)
    if 'axis' in p:p['axis']=rng.choice(['x','y'])
    if 'kind' in p:p['kind']=rng.choice(['sin','cos'])
    return p

def render_math(template,p):
    """Ordered complete components; no CAS collapse of substitution/distribution."""
    F,axis,fr,ft,u,v,answer=object_math(template,p)
    name=p['name'];A=p['A'];b=p.get('b',0);k=p.get('k',1);n=p.get('p',1)
    tr,tt=tex(fr),tex(ft)
    sub='('+tr+')'+fn('cos' if axis=='x' else 'sin')+('-' if axis=='x' else '+')+r'\frac{1}{r}('+tt+')'+fn('sin' if axis=='x' else 'cos')
    distributed=add(tex(u),tex(v));final=tex(answer)
    if template=='power_cosine_y':
        final=scale(A,power(n-1)+'('+add(term(n,fn('sin')+fn('cos',k)),term(-k,fn('cos')+fn('sin',k)))+')')
        rows=[sub,final]
    elif template in ('cosine_y','sine_y','offset_sine_y','offset_cosine_y'):
        rows=[sub,distributed]
    elif template=='double_sine_x':
        # Keep separate trig substitution, multiplication and cancellation masks.
        rows=[sub,add(term(A,fn('sin',2)+fn('cos')),term(-2*A,fn('cos',2)+fn('sin'))),
              add(term(2*A,fn('sin')+fn('cos')+fn('cos')),term(-2*A,fn('sin')+'('+fn('cos')+'^{2}-'+fn('sin')+'^{2})')),
              add(add(term(2*A,fn('sin')+fn('cos')+'^{2}'),term(-2*A,fn('sin')+fn('cos')+'^{2}')),term(2*A,fn('sin')+'^{3}')),term(2*A,fn('sin')+'^{3}')]
        # Powers must precede arguments, not follow theta.
        rows=[re.sub(r'\\(sin|cos) \\theta\^\{(\d)\}',lambda m:'\\'+m[1]+'^{'+m[2]+'} '+r'\theta',z) for z in rows]
    elif template=='sine_minus_y':
        distributed=add(add(term(A,fn('sin')+'^{2}'),term(-A*b,fn('sin'))),term(A,fn('cos')+'^{2}'))
        distributed=re.sub(r'\\(sin|cos) \\theta\^\{(\d)\}',lambda m:'\\'+m[1]+'^{'+m[2]+'} '+r'\theta',distributed)
        rows=[sub,distributed,final]
    elif template=='cosine_minus_x':
        distributed=add(add(term(A,fn('cos')+'^{2}'),term(-A*b,fn('cos'))),term(A,fn('sin')+'^{2}'))
        distributed=re.sub(r'\\(sin|cos) \\theta\^\{(\d)\}',lambda m:'\\'+m[1]+'^{'+m[2]+'} '+r'\theta',distributed)
        rows=[sub,distributed,final]
    elif template=='quadratic_plus_cosine_x':
        rows=[sub,add(add(term(2*A,'r'+fn('cos')),term(A*b,r'\cos^{2} \theta')),term(A*b,r'\sin^{2} \theta')),add(term(2*A,'r'+fn('cos')),term(A*b,r'(\cos^{2} \theta+\sin^{2} \theta)')),final]
    elif template=='offset_sine_x':
        rows=[sub,add(add(term(A*b,fn('cos')),term(A,fn('sin')+fn('cos'))),term(-A,fn('sin')+fn('cos'))),final]
    elif template=='radial_plus_sine_x':rows=[sub,distributed,add(term(A*p['a'],fn('cos')),tex(-s.Rational(A,2)/R*s.sin(2*T)))]
    elif template=='offset_cosine_x':rows=[sub,distributed,final]
    elif template=='radial_only':rows=[sub,final]
    else:
        # Hard offset family: retain three signed distributed contributions,
        # then collect the common radial factor without eager trig rewriting.
        fkind=p['kind'];base=fn('cos' if axis=='x' else 'sin')
        partner=fn('sin' if axis=='x' else 'cos')
        angular_sign=(-1 if axis=='x' else 1)*(1 if fkind=='sin' else -1)
        components=[term(n*b,base),term(n,fn(fkind,k)+base),term(angular_sign*k,fn('cos' if fkind=='sin' else 'sin',k)+partner)]
        distributed_parts=[term(A*n*b,power(n-1)+base),term(A*n,power(n-1)+fn(fkind,k)+base),term(A*angular_sign*k,power(n-1)+fn('cos' if fkind=='sin' else 'sin',k)+partner)]
        distributed=add(add(distributed_parts[0],distributed_parts[1]),distributed_parts[2])
        final=scale(A,power(n-1)+'('+add(add(components[0],components[1]),components[2])+')')
        rows=[sub,distributed,final]
    # All stages retained in raw TeX, and independently parsed by validate.py.
    formula=partial(name,axis)+'='+partial(name,'r')+fn('cos' if axis=='x' else 'sin')+('-' if axis=='x' else '+')+r'\frac{1}{r}'+partial(name,'theta')+fn('sin' if axis=='x' else 'cos')+'.'
    derivatives=r'\begin{aligned}'+partial(name,'r')+'='+tr+r',\,'+partial(name,'theta')+'='+tt+r'\end{aligned}'
    return F,axis,formula,derivatives,rows

def render(template,p):
    F,axis,formula,derivatives,rows=render_math(template,p);name=p['name']
    if template in CASES:
        source=SOURCES[CASES[template][0]]
        prompt=norm(source[':question/problem']);inline=prompt.split('$')
        old=inline[1];punct=',' if old.endswith(',') else ''
        inline[1]=name+r'(r,\theta )='+tex(F)+punct
        prompt='$'.join(inline)
        # Replace function names only in differential tokens and complete names.
        oldname=CASES[template][1]['name']
        prompt=prompt.replace('∂'+oldname,'∂'+name)
        if ':question/worked-solution' in source:
            solution=norm(source[':question/worked-solution'])
            # Preserve complete prose skeleton and three display blocks.
            parts=solution.split('$$');assert len(parts)==7
            parts[1]='\n'+formula+'\n';parts[3]='\n'+derivatives+'\n';parts[5]='\n'+aligned(rows,partial(name,axis))+'\n'
            solution='$$'.join(parts).replace('$'+oldname+'$','$'+name+'$')
        else:solution=None
    else:
        prompt='Given that $'+name+r'(r,\theta)='+tex(F)+'$, find $'+partial(name,axis)+'$, where $(x,y)$ are Cartesian coordinates and $(r,\\theta)$ are the corresponding plane polar coordinates.'
        solution=None
    if solution is None:
        solution='We will make use of the following chain rule formula:\n\n$$\n'+formula+'\n$$\n\nFirst, we find the partial derivatives of $'+name+'$ with respect to $r$ and $\\theta:$\n\n$$\n'+derivatives+'\n$$\n\nThen, substituting these into our chain rule formula, we get\n\n$$\n'+aligned(rows,partial(name,axis))+'\n$$'
    return prompt,solution,rows

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,text))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio fields')
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        matched=[t for t,(sid,_) in CASES.items() if profile=='observed:'+sid]
        if not matched:raise ValueError('unknown profile')
        if template and template!=matched[0]:raise ValueError('profile template conflict')
        template=matched[0]
    template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
    if TEMPLATES.get(template)!=level:raise ValueError('template level')
    profile=profile or ('observed:'+CASES[template][0] if template in CASES else 'authored:chain-rule')
    if profile!='authored:chain-rule' and profile!='observed:'+CASES.get(template,('',{}))[0]:raise ValueError('profile eligibility')
    for attempt in range(100):
        p=dict(parameters) if parameters is not None else sample(template,rng)
        validate_parameters(template,p)
        bank,correct=source_bank(template,p) if profile.startswith('observed:') else authored_bank(template,p)
        try:assert_bank(bank)
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else:raise ValueError('no eligible whole bank')
    prompt,solution,rows=render(template,p)
    values=[tex(x) for x in bank]
    # Choice identity uses actual values; content identity uses an orderless bank.
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[correct],'type':'radio','domain':DOMAIN})
    qid=uid(str(KP_ID)+identity);fid=uid(qid+'selection')
    answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    cid=answers[correct][':answer/id'];rng.shuffle(answers)
    F,axis,*_=object_math(template,p)
    # Assessed operation excludes names, bank/profile/layout and difficulty.
    canonical=s.expand_trig(s.expand(F))
    task=digest({'function':s.srepr(canonical),'derivative_axis':axis,'domain':DOMAIN})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':{k:RAW[k] for k in ('database','basis','lineage')},'source_ids':[CASES[template][0]] if template in CASES else [],'authored_level':level!='moderate','domain':DOMAIN,'content_fingerprint':identity,'mathematical_fingerprint':task,'solution_stages':rows,'plot_rating':'none','bank_interpretation':'inferred expression patterns, original intent unresolved' if profile.startswith('observed:') else 'authored chain-rule operations'}}

# ── Easy: authored missing-level section ──────────────────────────────────────
def generate_easy(seed=0,**kwargs):
    """One substantive radial partial and Cartesian coordinate factor.

    radial_only uses nonzero |A|≤4, p in {2,3}, and either x or y. The
    complete finite assessed domain has 32 tasks; names are cosmetic. Its
    angular partial is zero, and its complete bank retains five radial errors.
    This level is authored from the lesson formulas, not an observed rating.
    """
    return generate('easy',seed,**kwargs)


# ── Moderate: nine observed/unrated template sections ─────────────────────────
def generate_moderate(seed=0,**kwargs):
    """Observed two-path polar→Cartesian chain-rule workloads.

    Seven sources are rated moderate; two missing ratings receive an authored
    moderate placement. Preserve all nine original complete banks by explicit
    observed:q-ID profiles and their ordered source solution masks. The normal
    authored bank uses complete chain-rule operations. Specialized cancellation
    and double-angle families retain their defining fixed frequencies.
    """
    return generate('moderate',seed,**kwargs)


# ── Hard: authored missing-level section ──────────────────────────────────────
def generate_hard(seed=0,**kwargs):
    """Two nonzero partials and three distributed first-order contributions.

    power_offset uses nonzero |A|,|b|≤3, p in {2,3}, k in {2,3,4}, supported
    sine/cosine kind, and either Cartesian axis. Unevaluated substitution,
    three-term distribution and common-radial-factor collection remain distinct.
    These are unordered peers within the same KP, authored from the canonical
    and observed power-cosine workload; no higher or inverse derivative task.
    """
    return generate('hard',seed,**kwargs)
def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');opts=a.parse_args()
    out=[generate(l,opts.seed+i,template=opts.template,profile=opts.profile) for l in (['easy','moderate','hard'] if opts.difficulty=='all' else [opts.difficulty]) for i in range(opts.count)]
    print(json.dumps(out,ensure_ascii=False,indent=2) if opts.format=='json' else '\n\n---\n\n'.join(markdown(x) for x in out))
