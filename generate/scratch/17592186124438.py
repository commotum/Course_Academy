#!/usr/bin/env python3
"""Tangent lines to coordinate-plane sections, basis 1356; local review only.

Fourteen observed moderate families, each with its own operative source chain.
Public raw_<question-id> profiles preserve opaque whole banks and legacy omissions.
Normal operation banks are authored, separately labeled, and never mix recipes.
Easy: supplied single linear partial. Moderate: source derivatives at familiar
coordinates under nonzero integer vertical scale. Hard: canonical pi/trig partial.
No progression inside a level. No database, plotting or grading-engine mutation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
from functools import lru_cache
import sympy as sp
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'17592186124438'
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
KP=CAPTURE['record']; KP_ID=17592186124438
VERSION='coordinate-section-tangent-v1'
x,y,z=sp.symbols('x y z', real=True)
NS=uuid.UUID(KP[':knowledge-point/id'])

# Small exact reader for the actual source/generated TeX arithmetic, independent
# of sampler metadata. Supports all printed derivative/substitution/line stages.
@lru_cache(maxsize=20000)
def parse(s):
    s=s.replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1 ',s)
    ts=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',s); pos=0
    def atom():
        nonlocal pos
        t=ts[pos];pos+=1
        if t in ('+','-'): return (1 if t=='+' else -1)*power()
        if t in ('(','{'):
            a=expr(); assert ts[pos]==(')' if t=='(' else '}'),(s,ts,pos);pos+=1;return a
        if t==r'\frac': return atom()/atom()
        if t==r'\dfrac':return atom()/atom()
        if t==r'\sqrt':return sp.sqrt(atom())
        if t in (r'\sin',r'\cos',r'\ln'):
            return {r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log}[t](power())
        if t==r'\pi':return sp.pi
        if t=='e':return sp.E
        if t in ('x','y','z'):return {'x':x,'y':y,'z':z}[t]
        if re.fullmatch(r'\d+(?:\.\d+)?',t):return sp.Rational(t)
        raise ValueError((s,t))
    def power():
        nonlocal pos
        a=atom()
        if pos<len(ts) and ts[pos]=='^':pos+=1;a=a**atom()
        return a
    def product():
        nonlocal pos
        a=power()
        while pos<len(ts) and ts[pos] not in ('+','-',')','}',',',';','='):
            if ts[pos] in ('*',r'\cdot',r'\times'):pos+=1;a*=power()
            elif ts[pos]=='/':pos+=1;a/=power()
            else:a*=power()
        return a
    def expr():
        nonlocal pos
        a=product()
        while pos<len(ts) and ts[pos] in ('+','-'):
            t=ts[pos];pos+=1;b=product();a=a+b if t=='+' else a-b
        return a
    a=expr()
    if pos!=len(ts):raise ValueError((s,'unconsumed',ts[pos:]))
    return sp.simplify(a)
def tex(a):return sp.latex(sp.simplify(a),fold_short_frac=False).replace(r'\log',r'\ln')
def relation(v,c,e):return r'\{\begin{aligned}'+v+'='+tex(c)+r' \\ z='+tex(e)+r'\end{aligned}'
def equations(value):
    s=value.replace('\\\\', '\\') if r'\\begin' in value else value
    s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).replace(r'\{','').lstrip('{')
    rows=re.split(r'\\\\|;',s)
    return [parse(a.strip().rstrip(','))-parse(b.strip().rstrip(',')) for row in rows if '=' in row for a,b in [row.split('=',1)]]
@lru_cache(maxsize=20000)
def line_key(value):
    es=equations(value);assert len(es)==2
    A,b=sp.linear_eq_to_matrix(es,[x,y,z]);assert A.rank()==2
    return tuple(sp.cancel(t) for t in A.row_join(b).rref()[0])
def point_data(q):
    m=re.search(r'\$P\((.*?)\)\$',q[':question/problem']); coords=m.group(1).split(',')
    p=re.search(r'plane \$([xy])=(.*?)\.\$',q[':question/problem'])
    partial=re.search(r'and that \$(.*?)\$, find',q[':question/problem']).group(1)
    return coords,p.group(1),partial.split('=',1)[1]
def blocks(solution):return re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
def rows(block):return re.split(r'\\\\',block)
def rhs_rows(block):return [r.split('=',1)[1].strip() for r in rows(block)]
TEMPLATES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}

def shifted_math(old,scale,zold,znew):return sp.expand(scale*(parse(old)-zold)+znew)
def vertical_value(value,scale,zold,znew):
    # Replace complete z RHS only; never variable letters or numeric substrings.
    pat=r'(z\s*=\s*)(.*?)(?=\\{1,2}end|$)'
    if scale==1 and zold==znew:return value
    return re.sub(pat,lambda m:m.group(1)+tex(shifted_math(m.group(2),scale,zold,znew)),value)
def source_render(q,scale,znew):
    coords,v,der=point_data(q); a,b,zold=map(parse,coords)
    oldpt='P('+','.join(coords)+')'; newpt='P('+','.join(coords[:2]+[coords[2] if znew==zold else tex(znew)])+')'
    prompt=q[':question/problem'].replace(oldpt,newpt)
    if scale!=1:prompt=prompt.replace('='+der+'$',r'='+tex(scale)+r'\left('+der+r'\right)$')
    sol=q[':question/worked-solution'].replace(oldpt,newpt)
    bs=blocks(sol); slope=parse(rhs_rows(bs[0])[-1]);u=x if v=='y' else y;u0=a if u==x else b
    # Retain each family's entire evaluated-stage structure, c applied to every
    # stage; collect only the source's final row. No generic chain replacement.
    if scale!=1:
        old=bs[0];rr=rows(old)
        for i,r in enumerate(rr):
            lhs,rhs=r.split('=',1)
            rr[i]=lhs+'='+ (tex(scale*slope) if i==len(rr)-1 else tex(scale)+r'\left('+rhs.strip()+r'\right)')
        sol=sol.replace(old,r' \\ '.join(rr),1)
    if scale!=1 or zold!=znew:
        # Full point-slope components are regenerated, keeping row-count and all
        # shared prose. Original substitution omissions remain at replay anchors.
        old=blocks(sol)[1]; rr=rows(old)
        lhs0,rhs0=rr[0].split('=',1)
        rr[1]=' z-('+tex(znew)+') & =('+tex(scale*slope)+')('+str(u)+'-('+tex(u0)+')) '
        rr[-1]=' z & ='+tex(sp.expand(scale*slope*(u-u0)+znew))
        sol=sol.replace(old,r' \\ '.join(rr),1)
        old=blocks(sol)[-1];sol=sol.replace(old, v+'='+coords[0 if v=='x' else 1]+r' \\ z='+tex(sp.expand(scale*slope*(u-u0)+znew)),1)
    return prompt,sol,(a,b,znew),v,parse(der)*scale

def normalize(s):
    # Defensive command normalization; parent byte checks found no doubled
    # commands in the source. Normal output repairs unmatched literal braces.
    s=s.replace(r'\\begin',r'\begin').replace(r'\\end',r'\end')
    s=s.replace(r'{\begin',r'\{\begin') if r'\{\begin' not in s else s
    return s

def operations(v,pt,m):
    a,b,h=pt;u=x if v=='y' else y;u0=a if u==x else b;v0=b if v=='y' else a
    correct=m*(u-u0)+h
    if u0!=0:
        out=[relation(v,v0,correct),relation(v,v0,-m*(u-u0)+h),relation(v,v0,m*(u+u0)+h),relation(v,v0,m*(u-u0)),relation('x' if v=='y' else 'y',u0,m*((y if u==x else x)-v0)+h)]
        names=['correct','negated-slope','point-offset-added','altitude-omitted','fixed-coordinate-swapped']
    else:
        out=[relation(v,v0,correct),relation(v,v0,-m*u+h),relation(v,v0,m*u),relation(v,v0,m*u-h),relation('x' if v=='y' else 'y',u0,m*((y if u==x else x)-v0)+h)]
        names=['correct','negated-slope','altitude-omitted','altitude-sign','fixed-coordinate-swapped']
    keys=[line_key(t) for t in out]
    if len(set(keys))!=5:raise ValueError('whole operation bank collision')
    return out,names

def pack(level,template,params,profile,prompt,sol,fieldbanks,corrects,seed,raw=False):
    content={'version':VERSION,'level':level,'problem':prompt,'solution':sol,'banks':[sorted(b) for b in fieldbanks],'corrects':corrects}
    digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    uid=lambda s:str(uuid.uuid5(NS,digest+'|'+s))
    fields=[]
    for i,bank in enumerate(fieldbanks):
        choices=[{':answer/id':uid(f'{i}|{value}'),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
        f={':answer-field/id':uid('field'+str(i)),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if corrects[i] is not None:f[':answer-field/correct']=[':answer/id',uid(f'{i}|{corrects[i]}')]
        random.Random(str(seed)+'|'+str(i)).shuffle(choices);fields.append(f)
    question={':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':fields}
    # Fingerprint is independent of profile, distractors, letters and ordering.
    pt,v,der=point_data({':question/problem':prompt})
    mathdata=[level,v,[str(parse(t)) for t in pt],str(parse(der))]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(v) for k,v in params.items()},'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'content_hash':digest,'mathematical_fingerprint':hashlib.sha256(json.dumps(mathdata).encode()).hexdigest(),'domain':{'real_coordinate_section':True,'fixed_coordinate':v,'supplied_partial_variable':'x' if v=='y' else 'y'},'source_refs':[template] if template in TEMPLATES else ['e-3069' if level=='hard' else 'lesson:1955/introduction'],'evidence_only':raw,'eligible_for_learning':not raw,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY: authored single-component substitution; still requests the two planes.
def easy_instance(p):
    if set(p)!={'a','b','z','k'}:raise ValueError('easy keys a,b,z,k')
    a,b,h,k=[sp.sympify(p[t]) for t in ('a','b','z','k')]
    if not all(t.is_Integer and 1<=abs(t)<=4 for t in (a,b,k)) or not h.is_Integer or not 1<=abs(h)<=12:raise ValueError('easy bounds')
    return authored('easy',p,(a,b,h),'y',k*x,[f'{tex(k)}({tex(a)})',tex(k*a)],'single_linear')
# HARD: canonical supplied y*cos(x*y)+cos(y), exact pi slope/intercept.
def hard_instance(p):
    if set(p)!={'a','k','z'}:raise ValueError('hard keys a,k,z')
    a,k,h=[sp.sympify(p[t]) for t in ('a','k','z')]
    if not a.is_Integer or not 1<=abs(a)<=4 or not k.is_Integer or not 1<=abs(k)<=3 or not h.is_Integer or not 1<=abs(h)<=12:raise ValueError('hard bounds')
    b=k*sp.pi; m=b*(-1)**int(a*k)+(-1)**int(k)
    return authored('hard',p,(a,b,h),'y',y*sp.cos(x*y)+sp.cos(y),[r'('+tex(b)+r')\cos(('+tex(a)+')('+tex(b)+r'))+\cos('+tex(b)+')',r'('+tex(b)+')('+tex((-1)**int(a*k))+')+('+tex((-1)**int(k))+')',tex(m)],'canonical_trig')
def authored(level,p,pt,v,der,stages,template):
    a,b,h=pt;u=x if v=='y' else y;u0=a if u==x else b;v0=b if v=='y' else a;m=sp.simplify(der.subs({x:a,y:b}));point=','.join(map(tex,pt))
    prompt=f'The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane ${v}={tex(v0)}.$ Given that the point $P({point})$ lies on $C$, and that $'+r'{f}_{'+str(u)+'}='+tex(der)+'$, find the equations of the tangent line to $C$ at $P.$'
    sol=f'The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane ${v}={tex(v0)}.$ Hence, the slope of the tangent to the curve at the point $P({point})$ will be given by the partial derivative $'+r'\frac{∂z}{∂'+str(u)+'}{|}_{('+tex(a)+','+tex(b)+')}.$\n\n'+f'To get the slope, we evaluate the partial derivative $'+r'\frac{∂z}{∂'+str(u)+'}$ at $('+tex(a)+','+tex(b)+'):$\n\n$$\n'+r'\begin{aligned}{f}_{'+str(u)+'}('+tex(a)+','+tex(b)+') & ='+r' \\ & ='.join(stages)+r'\end{aligned}'+'\n$$\n\nNow, we use the point-slope form of a straight line:\n\n$$\n'+r'\begin{aligned}z-z{|}_{('+tex(a)+','+tex(b)+')} & ='+r'\frac{∂z}{∂'+str(u)+'}{|}_{('+tex(a)+','+tex(b)+')}('+str(u)+'-('+tex(u0)+'))'+r' \\ z-('+tex(h)+') & =('+tex(m)+')('+str(u)+'-('+tex(u0)+'))'+r' \\ z & ='+tex(sp.expand(m*(u-u0)+h))+r'\end{aligned}'+'\n$$\n\n'+f'Finally, the tangent line to the curve $C$ at $P({point})$ can be given as the intersection of two planes, as follows:\n\n$$\n'+relation(v,v0,sp.expand(m*(u-u0)+h))+'\n$$'
    return prompt,sol,pt,v,der,template
# MODERATE: all 14 captured families remain normal default families. Signed scale ±1..±3
# changes supplied derivative, altitude ±1..12 changes point-slope arithmetic;
# coordinates retain each source's perfect squares/familiar special values.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError(level)
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio')
    rng=random.Random(seed)
    if profile and profile.startswith('raw_'):template=profile[4:]
    template=template or (rng.choice(list(TEMPLATES)) if level=='moderate' else ('single_linear' if level=='easy' else 'canonical_trig'))
    raw=bool(profile and profile.startswith('raw_'))
    if profile not in (None,'authored_operations','raw_'+template):raise ValueError('profile')
    for attempt in range(1000):
        if level=='moderate':
            if template not in TEMPLATES:raise ValueError('moderate source family')
            q=TEMPLATES[template];coords,_,_=point_data(q)
            p=parameters or {'scale':rng.choice([-3,-2,-1,1,2,3]),'z':rng.choice([i for i in range(-12,13) if i])}
            if set(p)!={'scale','z'}:raise ValueError('moderate keys scale,z')
            c,h=sp.sympify(p['scale']),sp.sympify(p['z'])
            if not c.is_Integer or not 1<=abs(c)<=3 or h.is_real is not True or abs(h)>12:raise ValueError('moderate bounds')
            if not raw and not (h.is_Rational and h.q in (1,2) or (h/sp.pi).is_Integer and abs(h/sp.pi)<=3):raise ValueError('normal altitude integer/half-integer or small pi multiple')
            prompt,sol,pt,v,der=source_render(q,c,h)
        elif level=='easy':
            if template!='single_linear' or raw:raise ValueError('easy template')
            p=parameters or {**{k:rng.choice([i for i in range(-4,5) if i]) for k in ('a','b','k')},'z':rng.choice([i for i in range(-12,13) if i])}
            prompt,sol,pt,v,der,_=easy_instance(p)
        else:
            if template!='canonical_trig' or raw:raise ValueError('hard template')
            p=parameters or {'a':rng.choice([i for i in range(-4,5) if i]),'k':rng.choice([i for i in range(-3,4) if i]),'z':rng.choice([i for i in range(-12,13) if i])}
            prompt,sol,pt,v,der,_=hard_instance(p)
        m=sp.simplify(der.subs({x:pt[0],y:pt[1]}))
        if raw:
            oldz=parse(point_data(q)[0][2]);banks=[];corrects=[]
            for f in q[':question/answer-fields']:
                bank=[vertical_value(a[':answer/value'],c,oldz,pt[2]) for a in f[':answer-field/choices']];banks.append(bank)
                cv=vertical_value(f[':answer-field/correct'][':answer/value'],c,oldz,pt[2]) if ':answer-field/correct' in f else None
                corrects.append(next(a for a in bank if line_key(a)==line_key(cv)) if cv is not None else None)
            return pack(level,template,p,profile,prompt,sol,banks,corrects,seed,True)
        try:bank,names=operations(v,pt,m)
        except ValueError:
            if parameters is not None:raise
            continue
        record=pack(level,template,p,'authored_operations',normalize(prompt),normalize(sol),[bank],[bank[0]],seed)
        record['generation']['recipes']=names
        return record
    raise ValueError('no eligible whole bank')
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];s=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):s+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
    return s+'Worked solution:\n\n'+q.get(':question/worked-solution','')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
