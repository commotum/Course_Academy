#!/usr/bin/env python3
"""Seeded coordinate-section tangent practice. No database or runtime repo imports."""
import argparse, copy, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from exact_math import x,y,z,parse,tex,line_key
from math_format import normalize_prose,normalize_tex,system_tex,validate_generated_record
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source_cases.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in DATA['questions']}
NS=uuid.UUID(DATA['kp'][':knowledge-point/id'])
LEVELS=('easy','moderate','hard')
VERSION='coordinate-section-v4'

def swap_variables(text):
    return re.sub(r'\\[a-zA-Z]+|[xy]',lambda m: {'x':'y','y':'x'}.get(m[0],m[0]),text)

def substitute_text(text, replacements):
    return re.sub(r'\\[a-zA-Z]+|[xy]',lambda m: r'\left('+replacements[m[0]]+r'\right)' if m[0] in replacements else m[0],text)

def source_parameters(q):
    p=q[':question/problem']
    coords=re.search(r'\$P\((.*?)\)\$',p)[1].split(',')
    fixed=re.search(r'plane \$([xy])=',p)[1]
    derivative=re.search(r'and that \$(.*?)\$, find',p)[1].split('=',1)[1]
    derivative=normalize_tex(derivative)
    return tuple(map(parse,coords)),fixed,derivative

def show(t): return '\n\n$$\n'+t+'\n$$\n\n'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'

def make_instance(level,template,rng,parameters=None):
    p=dict(parameters or {})
    if template=='linear':
        fixed=p.get('fixed',rng.choice(['x','y']));u=y if fixed=='x' else x
        a=sp.sympify(p.get('a',rng.choice([-3,-2,-1,0,1,2,3])))
        b=sp.sympify(p.get('b',rng.choice([-3,-2,-1,0,1,2,3])))
        k=sp.Integer(p.get('k',rng.choice([-3,-2,-1,1,2,3])))
        d=sp.Integer(p.get('d',rng.choice([-3,-2,-1,1,2,3])))
        h=sp.Integer(p.get('height',rng.randint(-5,5)))
        D=k*u+d; derivative=tex(D);pt=(a,b,h)
        refs=['tutorial:2376','tutorial:3933','e-13974']
        settings={'fixed':fixed,'a':str(a),'b':str(b),'k':int(k),'d':int(d),'height':str(h)}
    else:
        if template=='canonical_trig':
            a=sp.Integer(p.get('a',rng.choice([-2,-1,1,2])));b=sp.Integer(p.get('k',rng.choice([-1,1])))*sp.pi
            canonical_a=int(a);canonical_k=int(b/sp.pi)
            fixed='y';derivative=r'y\cos(xy)+\cos(y)'
        elif template=='log_radical':
            a,b=sp.E,sp.Integer(1);fixed='x';derivative=r'\frac{\ln x}{\sqrt{y+1}}+\frac{e^y}{x}'
        else:
            q=SOURCES[template];(a,b,_),fixed,derivative=source_parameters(q)
        # Cancellation is a legitimate exact decision case, with nonzero terms.
        if 'cancellation' not in p and template in ('q-132587','q-71216'):
            p['cancellation']=rng.randrange(4)==0
        if p.get('cancellation',False):
            if template=='q-132587':a,b=-sp.Rational(1,2),sp.Integer(2)
            elif template=='q-71216':a,b=sp.Integer(2),sp.Integer(0)
            else:raise ValueError('No authored cancellation case for '+template)
        swap=p.get('swap',rng.choice([False,True]));sign=sp.Integer(p.get('scale',rng.choice([-1,1])))
        if sign not in (-1,1):raise ValueError('scale must be a sign')
        if swap:a,b=b,a;fixed='y' if fixed=='x' else 'x';derivative=swap_variables(derivative)
        # Only varying-coordinate translation: same operator arguments and workload.
        u=y if fixed=='x' else x
        shift=sp.sympify(p.get('shift',rng.choice([-1,0,1])))
        if abs(shift)>1:raise ValueError('translation bound')
        if shift:
            derivative=substitute_text(derivative,{str(u):tex(u-shift)})
            if u==x:a+=shift
            else:b+=shift
        base_derivative=derivative
        if sign==-1:derivative=r'-\left('+derivative+r'\right)'
        h=sp.sympify(p.get('height',rng.randint(-5,5)));pt=(a,b,h);D=parse(derivative)
        refs=[('ecc7abe1-ce57-535f-91d5-75e9d448ee61' if template=='log_radical' else 'e-3069' if template=='canonical_trig' else template),'tutorial:3933','e-13978']
        settings={'swap':swap,'scale':int(sign),'shift':str(shift),'height':str(h),'cancellation':p.get('cancellation',False)}
        if template=='canonical_trig':settings.update(a=canonical_a,k=canonical_k)
    u=y if fixed=='x' else x;v=x if fixed=='x' else y
    u0=pt[1] if u==y else pt[0];v0=pt[0] if v==x else pt[1]
    m=sp.simplify(D.subs({x:pt[0],y:pt[1]}))
    if m.is_real is not True or not m.is_finite:raise ValueError('not a finite real slope')
    expr=sp.expand(pt[2]+m*(u-u0))
    evaluation=substitute_text(derivative,{'x':tex(pt[0]),'y':tex(pt[1])})
    return dict(level=level,template=template,pt=pt,fixed=fixed,u=u,v=v,u0=u0,v0=v0,D=D,derivative=derivative,m=m,expr=expr,evaluation=evaluation,base_derivative=(derivative if template=='linear' else base_derivative),outer_sign=(1 if template=='linear' else int(sign)),refs=refs,parameters=settings)

def bank(i,rng):
    """Whole two-slope/two-intercept error profiles, never arbitrary fillers."""
    m,u,u0,v0,h=i['m'],i['u'],i['u0'],i['v0'],i['pt'][2]
    c=sp.simplify(h-m*u0)
    candidates=[(-m,'slope-sign'),(2*m,'slope-factor-double'),(m/2,'slope-factor-half')]
    # Omitted addends are independent plausible evaluation errors, including cancellation.
    candidates += [(sp.simplify(t.subs({x:i['pt'][0],y:i['pt'][1]})),'partial-addend-only') for t in sp.Add.make_args(i['D'])]
    distinct=[]
    for val,label in candidates:
        if val.is_real is True and val.is_finite and sp.simplify(val-m)!=0 and all(sp.simplify(val-t[0])!=0 for t in distinct):distinct.append((val,label))
    rng.shuffle(distinct)
    for n,nrecipe in distinct:
        # d also produces a second line through P whenever u0 is nonzero.
        ds=[(h-n*u0,'wrong-slope-point-translation'),(-h-m*u0,'height-sign'),(h+m*u0,'translation-sign'),(-m*u0,'height-omitted'),(h-m*v0,'fixed-coordinate-used-in-translation'),(h-n*v0,'wrong-slope-and-fixed-coordinate-translation')]
        rng.shuffle(ds)
        for d,drecipe in ds:
            d=sp.simplify(d)
            if sp.simplify(d-c)==0:continue
            # When u0=0, d!=h, and both lines with intercept c pass through P.
            if u0!=0 and sp.simplify(d-(h-n*u0))!=0:continue
            for t,trecipe in distinct:
                if sp.simplify(t-n)==0:continue
                es=[(-t*u0,'height-omitted'),(h+t*u0,'translation-sign'),(-h-t*u0,'height-sign'),(h-t*v0,'fixed-coordinate-used-in-translation')]
                rng.shuffle(es)
                for e,erecipe in es:
                    e=sp.simplify(e)
                    expressions=[m*u+c,m*u+d,n*u+c,n*u+d,t*u+e]
                    if len(set(map(str,map(sp.expand,expressions))))!=5:continue
                    through=sum(sp.simplify(expr.subs(u,u0)-h)==0 for expr in expressions)
                    if through<2:continue
                    vals=[normalize_tex(system_tex([i['fixed']+'='+tex(v0),'z='+tex(sp.expand(expr))])) for expr in expressions]
                    if len({line_key(v) for v in vals})!=5:continue
                    recipes=['correct','correct-slope/wrong-translation:'+drecipe,nrecipe+'/true-intercept',nrecipe+'/'+drecipe,trecipe+'/'+erecipe]
                    return vals,recipes
    raise ValueError('No distinct plausible complete bank')

def additive_terms(text):
    """Split only original top-level addends; never normalize operator inputs."""
    chunks=[];start=0;depth=0;paren=0
    for j,c in enumerate(text):
        if c=='{':depth+=1
        elif c=='}':depth-=1
        elif c=='(':paren+=1
        elif c==')':paren-=1
        elif c in '+-' and j and depth==0 and paren==0:
            chunks.append(text[start:j]);start=j
    chunks.append(text[start:])
    return [t.strip() for t in chunks]

def product_rows(text):
    if len(text)<120:return [text]
    cuts=[]
    for match in re.finditer(r'\\(?:sin|cos|ln)\b|\\operatorname\{(?:sin|cos|ln)\}',text):
        prefix=text[:match.start()]
        if prefix.count('(')==prefix.count(')') and prefix.count('{')==prefix.count('}') and match.start()>0:cuts.append(match.start())
    if not cuts:return [text]
    cut=cuts[-1]
    return [text[:cut],r'\qquad\cdot '+text[cut:]]

def partial_display(i):
    u=str(i['u']);terms=additive_terms(i['base_derivative'])
    if (len(i['derivative'])<140 and i['template']!='q-71204') or len(terms)==1:return f'f_{u}(x,y)='+i['derivative']
    terms=terms[:]
    if i['outer_sign']==-1:
        terms[0]=r'-\bigl['+terms[0];terms[-1]+=r'\bigr]'
    return aligned([f'f_{u}(x,y)&='+terms[0]]+[r'&\qquad '+t for t in terms[1:]])

def slope_derivation(i):
    a,b,_=i['pt'];u=str(i['u'])
    rows=[f'm&=f_{u}({tex(a)},{tex(b)})']
    terms=additive_terms(i['base_derivative'])
    if len(i['evaluation'])<140 or len(terms)==1:
        return rows+['&='+i['evaluation'],'&='+tex(i['m'])]
    # Separate addends keep source operator arguments intact and avoid a wide
    # single-line substitution. T_j denotes a signed addend, not a new method.
    rows=[]
    for j,t in enumerate(terms,1):
        evaluated=substitute_text(t,{'x':tex(a),'y':tex(b)})
        value=sp.simplify(parse(t).subs({x:a,y:b}))
        wrapped=product_rows(evaluated)
        rows.extend([f'T_{j}&='+wrapped[0]]+['&'+t for t in wrapped[1:]]+['&='+tex(value)])
    sum_terms='+'.join(f'T_{j}' for j in range(1,len(terms)+1))
    if i['outer_sign']==-1:sum_terms=r'-\left('+sum_terms+r'\right)'
    rows.extend([f'm=f_{u}({tex(a)},{tex(b)})&='+sum_terms,'&='+tex(i['m'])])
    return rows

def assemble(i,seed,rng):
    level=i['level'];u=str(i['u']);f=i['fixed'];a,b,h=i['pt'];m=i['m'];expr=i['expr']
    point=','.join(map(tex,i['pt']))
    prompt=f'The curve $C$ is the intersection of a surface $z=f(x,y)$ with the plane ${f}={tex(i["v0"])}$. The point $P({point})$ lies on $C$, and'+show(partial_display(i))+'Find the equations of the tangent line to $C$ at $P$.'
    if level=='easy':prompt+=f'\n\nUse $m=f_{u}({tex(a)},{tex(b)})$ and $z-z_0=m({u}-{u}_0)$, keeping ${f}={tex(i["v0"])}$.'
    if level=='hard':prompt+=f' Give exact answers, with $z$ expressed in terms of ${u}$.\n\n${f}=$\n{{{{plane}}}}\n\n$z=$\n{{{{height}}}}'
    final=normalize_tex(system_tex([f+'='+tex(i['v0']),'z='+tex(expr)]))
    slope_rows=slope_derivation(i)
    point_rows=[f'z-({tex(h)})&=({tex(m)})({u}-({tex(i["u0"])}))','z&='+tex(expr)]
    solution=f'The plane fixes ${f}$, so ${u}$ varies along the section. Evaluate the supplied partial:'+show(aligned(slope_rows))+f'Use point-slope form at $({u}_0,z_0)=({tex(i["u0"])},{tex(h)})$:'+show(aligned(point_rows))+'The tangent retains the fixed-coordinate plane:'+show(final)
    if level=='hard':
        values=[[tex(i['v0'])],[tex(expr)]];correct=[v[0] for v in values];keys=['plane','height'];kinds=['blank','blank'];recipes=[]
    else:
        values0,recipes=bank(i,rng);correct=[values0[0]];values=[values0];keys=['selection'];kinds=['radio']
    return pack(level,prompt,solution,values,correct,keys,kinds,seed,{'template':i['template'],'parameters':i['parameters'],'source_refs':i['refs'],'recipes':recipes,'solution_path':{'partial_input':i['derivative'],'evaluation':i['evaluation'],'slope':tex(m),'point_slope':point_rows[0],'final_system':final,'displayed_fragment':tex(expr),'keyed_fragment':tex(expr),'conversions':['substitute supplied coordinates','evaluate familiar exact values','expand point-slope form'],'support':i['refs']}})

def pack(level,prompt,solution,values,correct,keys,kinds,seed,meta):
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    values=[[normalize_tex(v) for v in b] for b in values];correct=list(map(normalize_tex,correct))
    payload=[VERSION,level,prompt,solution,[sorted(b) for b in values],correct]
    digest=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest()
    uid=lambda tag:str(uuid.uuid5(NS,digest+'|'+tag))
    fields=[]
    for idx,(vals,key,kind,c) in enumerate(zip(values,keys,kinds,correct)):
        choices=[{':answer/id':uid(f'{idx}|{v}'),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
        rng=random.Random(f'{seed}|{idx}');rng.shuffle(choices)
        fields.append({':answer-field/id':uid('field'+str(idx)),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(f'{idx}|{c}')]})
    return validate_generated_record({'knowledge_point':{'db_id':17592186124438,'id':str(NS),'title':DATA['kp'][':knowledge-point/title']},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':dict(version=VERSION,seed=seed,content_hash=digest,source_basis=DATA['basis'],source_lineage=DATA['lineage'],**meta)})

def replay_source(source_id,seed=0):
    """Complete normalized source bank, with fresh owned identities. Evidence only."""
    q=SOURCES[source_id];fields=q[':question/answer-fields']
    values=[[a[':answer/value'] for a in f[':answer-field/choices']] for f in fields]
    correct=[f[':answer-field/correct'][':answer/value'] for f in fields]
    return pack('moderate',q[':question/problem'],q[':question/worked-solution'],values,correct,[f[':answer-field/key'] for f in fields],['radio']*len(fields),seed,{'template':source_id,'source_refs':[source_id],'evidence_only':True,'profile':'source-bank-replay'})

def generate(level,seed=0,template=None,parameters=None):
    if level not in LEVELS:raise ValueError(level)
    rng=random.Random(seed);template=template or ('linear' if level=='easy' else rng.choice(list(SOURCES)))
    for attempt in range(200):
        i=make_instance(level,template,rng,parameters)
        try:return assemble(i,seed,rng)
        except ValueError as error:
            if parameters is not None:raise
    raise ValueError('No valid whole bank after 200 attempts')

def batch(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();families=['linear'] if level=='easy' else list(SOURCES)+(['canonical_trig','log_radical'] if level=='hard' else [])
    # Family-first cycles prevent amplitude clones in small finite batches.
    while len(out)<count:
        cycle=families[:];rng.shuffle(cycle)
        for family in cycle:
            record=generate(level,rng.randrange(2**63),family)
            # Semantic identity ignores bank recipes, option order and record UUIDs.
            p=record['question'][':question/problem'];fingerprint=hashlib.sha256(p.encode()).hexdigest()
            if fingerprint in seen:continue
            seen.add(fingerprint);out.append(record)
            if len(out)==count:break
    # Allocate answer positions across the complete CLI batch, with a random
    # offset/order, so small served batches do not accidentally teach a label.
    # The complete mathematical bank is unchanged; only its visual order moves.
    slots=[]
    while len(slots)<len(out):
        cycle=list(range(5));rng.shuffle(cycle);slots.extend(cycle)
    for record,slot in zip(out,slots):
        field=record['question'][':question/answer-fields'][0]
        if not field[':answer-field/type'].endswith('radio'):continue
        choices=field[':answer-field/choices'];cid=field[':answer-field/correct'][1]
        current=next(j for j,a in enumerate(choices) if a[':answer/id']==cid)
        choices[current],choices[slot]=choices[slot],choices[current]
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=LEVELS+('all','unclassified'),default='moderate');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    levels=LEVELS if a.difficulty=='all' else ('moderate' if a.difficulty=='unclassified' else a.difficulty,)
    print(json.dumps([r for level in levels for r in batch(level,a.count,a.seed)],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
