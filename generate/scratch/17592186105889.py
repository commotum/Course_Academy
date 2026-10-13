#!/usr/bin/env python3
"""Surface-integral integrand setup; basis1356; no database operations.

Shared exact helpers precede separate easy/moderate/hard entrypoints. Source
replays use extracted prose/row masks and coefficient-scaled expression recipes,
including historical opaque banks; those profiles are evidence-only. Normal
sampling chooses a whole method bank and a supported family before parameters.
All three levels request only the integrand in Cartesian repeated integration.
No evaluation, polar conversion, or flux. See adjacent extraction and validation.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s

KP_ID=17592186105889
KP_UUID='8885504f-07fb-5308-a982-608d7baa262b'
TITLE='Express Surface Integrals as Repeated Integrals'
VERSION='cartesian-surface-setup-1'
ROOT=Path(__file__).resolve().parent/str(KP_ID)
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y,z=s.symbols('x y z', real=True)
NAMESPACE=uuid.UUID(KP_UUID)
# Observed families retain the original easy labels, even when their algebra varies.
BASE={
 'quadratic_xy':dict(source='q-161106',a='1',b='1',m=2,n=2,k='2',u=1,v=1,w=0,bounds=[-1,1,0,2]),
 'plane_xz':dict(source='q-161323',a='sqrt(2)',b='sqrt(2)',m=1,n=1,k='-3',u=1,v=0,w=1,bounds=[0,1,0,2]),
 'plane_xy_z2':dict(source='q-161319',a='-2',b='1',m=1,n=1,k='1',u=1,v=1,w=2,bounds=[-1,1,-1,1]),
 'plane_xyz':dict(source='q-161321',a='-sqrt(2)',b='-sqrt(2)',m=1,n=1,k='sqrt(2)',u=1,v=1,w=1,bounds=[-1,1,0,2]),
 'quadratic_x2_z2':dict(source='q-161325',a='-1',b='2',m=2,n=2,k='1',u=2,v=0,w=2,bounds=[-1,1,0,2]),
 'plane_x2yz':dict(source='q-161314',a='-1',b='1',m=1,n=1,k='1',u=2,v=1,w=1,bounds=[-1,1,0,2]),
 'quadratic_x2y2z':dict(source='q-161320',a='-1',b='-1',m=2,n=2,k='1',u=2,v=2,w=1,bounds=[0,1,0,1]),
 'plane_y':dict(source='q-161326',a='-sqrt(2)',b='-1',m=1,n=1,k='sqrt(2)',u=0,v=1,w=0,bounds=[-1,0,0,2]),
}
TEMPLATES={**{k:'easy' for k in BASE},'coupled_xz':'moderate','coupled_yz':'moderate','coupled_two_x':'hard','coupled_two_y':'hard'}
METHOD_PROFILES=('measure_conversion',)

def number(v):
    expr=s.sympify(v,locals={'sqrt':s.sqrt})
    if expr.free_symbols or not expr.is_real: raise ValueError('exact real scalar required')
    return expr

def tex(e): return s.latex(e,order='lex').replace(r'\left', '').replace(r'\right','')
def eq(a,b): return s.simplify(a-b)==0

def parse_scalar(t):
    """Independent strict reader for the displayed polynomial/radical grammar."""
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
    t=t.replace(r'\,','').replace(r'\:','').replace(r'\cdot','*').replace(' ','')
    def group(at):
        if at>=len(t) or t[at]!='{': raise ValueError('group required: '+t)
        dep=1;end=at+1
        while dep:
            if end>=len(t): raise ValueError('unbalanced group')
            dep+=(t[end]=='{')-(t[end]=='}');end+=1
        return t[at+1:end-1],end
    while r'\sqrt' in t:
        at=t.index(r'\sqrt');body,end=group(at+5)
        t=t[:at]+'(sqrt('+str(parse_scalar(body))+'))'+t[end:]
    while r'\frac' in t:
        at=t.index(r'\frac');numerator,end=group(at+5);denominator,end2=group(end)
        t=t[:at]+'('+str(parse_scalar(numerator))+')/('+str(parse_scalar(denominator))+')'+t[end2:]
    if '\\' in t: raise ValueError('unsupported scalar TeX: '+t)
    t=t.replace('{','(').replace('}',')').replace('^','**')
    value=parse_expr(t,local_dict={'x':x,'y':y,'z':z,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
    if not value.free_symbols <= {x,y,z}:raise ValueError('unsupported symbols in rendered scalar')
    return value

def model(template,p):
    if template in BASE:
        b=BASE[template];a=number(p['a']);bb=number(p['b']);k=number(p['k'])
        g=a*x**b['m']+bb*y**b['n'];f=k*x**b['u']*y**b['v']*z**b['w']
    else:
        a,bb,c,k=(number(p[i]) for i in ('a','b','c','k'))
        g=a*x*x+bb*x*y+c*y*y
        if template=='coupled_xz':f=k*x*z
        elif template=='coupled_yz':f=k*y*z
        elif template=='coupled_two_x':f=k*x*z+number(p['l'])*y*z*z
        elif template=='coupled_two_y':f=k*y*z+number(p['l'])*x*z*z
        else:raise ValueError('unknown template')
    dx=s.diff(g,x);dy=s.diff(g,y);metric=s.sqrt(1+dx**2+dy**2)
    pref=s.expand(f.subs(z,g));answer=pref*metric
    return f,g,dx,dy,metric,pref,answer

def check_parameters(template,level,p,raw=False):
    expected={'a','b','k','bounds'} if template in BASE else {'a','b','c','k','bounds'}|({'l'} if level=='hard' else set())
    if set(p)!=expected:raise ValueError('parameter keys must be '+str(sorted(expected)))
    bounds=p['bounds']
    if len(bounds)!=4 or any(type(i)!=int or abs(i)>3 for i in bounds) or not(bounds[0]<bounds[1] and bounds[2]<bounds[3]):raise ValueError('ordered integer rectangle within [-3,3] required')
    if raw:
        b=BASE[template]
        if not eq(number(p['a']),number(b['a'])) or not eq(number(p['b']),number(b['b'])):raise ValueError('raw opaque banks hold surface fixed; vary scalar k and bounds')
        ratio=number(p['k'])/number(b['k'])
        if ratio not in (-3,-2,-1,1,2,3):raise ValueError('raw scalar ratio must be nonzero integer of magnitude <=3')
    else:
        domain={s.Integer(i) for i in (-2,-1,1,2)}|{s.sqrt(2),-s.sqrt(2)} if level=='easy' else {s.Integer(i) for i in (-2,-1,1,2)}
        if any(number(p[k]) not in domain for k in expected-{'bounds'}):raise ValueError('coefficient outside bounded nonzero level domain')

def sample(template,rng):
    level=TEMPLATES[template];vals=[-2,-1,1,2,'sqrt(2)','-sqrt(2)'] if level=='easy' else [-2,-1,1,2]
    p={k:str(rng.choice(vals)) for k in ('a','b','k')}
    if level!='easy':p['c']=str(rng.choice(vals))
    if level=='hard':p['l']=str(rng.choice(vals))
    lo=rng.choice([-2,-1,0]);yl=rng.choice([-1,0]);p['bounds']=[lo,lo+rng.choice([1,2]),yl,yl+rng.choice([1,2])]
    return p

def original_parameters(template):
    b=BASE[template];return {k:copy.deepcopy(b[k]) for k in ('a','b','k','bounds')}

def render_like(expr,baseline):
    # Recovered component spelling is conditional, not a source-payload return.
    return baseline if eq(expr,parse_scalar(baseline)) else tex(expr)

def bounds_replace(t,old,new):
    # Only complete domain and repeated-integral components are replaced.
    ox,xx,oy,yy=old;nx,rx,ny,ry=new
    for var,lo,hi,nlo,nhi in [('x',ox,xx,nx,rx),('y',oy,yy,ny,ry)]:
        pattern=rf'{lo}(\\le(?:q)?\s*{var}\\le(?:q)?\s*){hi}(?=[.$\s])'
        t=re.sub(pattern,lambda m:str(nlo)+m[1]+str(nhi),t)
    integral_pattern=r'\{\\int \}_\{[-\d]+\}\^\{[-\d]+\}\{\\int \}_\{[-\d]+\}\^\{[-\d]+\}'
    t=re.sub(integral_pattern,lambda m:r'{\int }_{'+str(nx)+'}^{'+str(rx)+'}'+r'{\int }_{'+str(ny)+'}^{'+str(ry)+'}',t)
    # The malformed source uses spaces and a different integral mask.
    t=re.sub(r'(?<![\d-])'+str(ox)+r' \\le x \\le '+str(xx),f'{nx} '+r'\le x \le '+str(rx),t) if False else t
    if 'AAAAAAA' in t:
        t=re.sub(r'\$z = .*?\$ for .*?\.',lambda m:m[0],t) # surface handled elsewhere
        t=t.replace(f'{ox} \\le x \\le {xx}',f'{nx} \\le x \\le {rx}').replace(f'{oy} \\le y \\le {yy}',f'{ny} \\le y \\le {ry}')
        t=t.replace(r'\int_{'+str(ox)+'}^{'+str(xx)+'}',r'\int_{'+str(nx)+'}^{'+str(rx)+'}',1)
        # match second integral independently to avoid equal old bound aliasing
        t=re.sub(r'(\\displaystyle \\int_\{'+str(oy)+r'\}\^\{'+str(yy)+r'\})(AAAAAAA)',lambda m:r'\displaystyle \int_{'+str(ny)+'}^{'+str(ry)+'}'+m[2],t)
    return t

def raw_render(template,p):
    """Reusable recovered source masks: fixed prose, complete component slots."""
    b=BASE[template];src=QUESTIONS[b['source']];q=copy.deepcopy(src)
    f,g,dx,dy,metric,pref,answer=model(template,p)
    p0=original_parameters(template);f0,g0,dx0,dy0,m0,pref0,ans0=model(template,p0)
    problem=q[':question/problem']
    # isolate function definition; preserve all source spacing/punctuation
    pat=r'(\$f\(x,\s*y,\s*z\)\s*=)(.*?)(,?\$)'
    problem=re.sub(pat,lambda m:m[1]+render_like(f,m[2].rstrip(','))+(',' if m[2].endswith(',') else '')+m[3],problem,count=1)
    q[':question/problem']=bounds_replace(problem,b['bounds'],p['bounds'])
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution']
        # Preserve the original formal partial operator rows and punctuation.
        pat=r'(\\frac\{∂z\}\{∂([xy])\}=\\frac\{∂\}\{∂\2\}\()(.*?)(\)=)([^\n]+)'
        def deriv(m):
            end=m[5];punct=end[-1] if end[-1] in ',.' else '';arg=end[:-1] if punct else end
            d=dx if m[2]=='x' else dy
            return m[1]+render_like(g,m[3])+m[4]+render_like(d,arg)+punct
        sol=re.sub(pat,deriv,sol)
        # The scalar integral rows are entire slots, never short substitutions.
        pat=r'(?P<prefix>\{∬\}_\{D\}\\,|\{\\int \}_\{[-\d]+\}\^\{[-\d]+\}\{\\int \}_\{[-\d]+\}\^\{[-\d]+\}\\,)(?P<scalar>.*?)(?P<suffix>\\,\\text\{d\}A|\\,\\,\\text\{d\}y\\,\\text\{d\}x)'
        ratio=number(p['k'])/number(b['k'])
        sol=re.sub(pat,lambda m:m['prefix']+render_like(parse_scalar(m['scalar'])*ratio,m['scalar'])+m['suffix'],sol)
        q[':question/worked-solution']=bounds_replace(sol,b['bounds'],p['bounds'])
    ratio=number(p['k'])/number(b['k'])
    fields=q.get(':question/answer-fields',[])
    for field in fields:
        for choice in field[':answer-field/choices']:
            choice[':answer/value']=render_like(ratio*parse_scalar(choice[':answer/value']),choice[':answer/value'])
        if ':answer-field/correct' in field:
            orig=field[':answer-field/correct'][':answer/id'];field[':answer-field/correct']=copy.deepcopy(next(a for a in field[':answer-field/choices'] if a[':answer/id']==orig))
    return q

FORMULA=r'{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.'
OPENING='For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by'

def integral(body,bounds):
    a,b,c,d=bounds
    return rf'{{\int }}_{{{a}}}^{{{b}}}{{\int }}_{{{c}}}^{{{d}}}\,{body}\,\,\text{{d}}y\,\text{{d}}x'

def normal_render(template,p):
    f,g,dx,dy,m,pref,answer=model(template,p);a,b,c,d=p['bounds']
    prompt=f'Consider the surface integral of the function $f(x,y,z)={tex(f)},$ where the surface $S$ is defined by $z={tex(g)}$ for ${a}\\le x\\le {b}$ and ${c}\\le y\\le {d}.$\nThis surface integral can be written as a repeated integral, as shown below. \n\n$$\n'+r'{∬}_{S}f(x,y,z)\,\text{d}S='+integral(r'\boxed{}',p['bounds'])+'\n$$\n\nWhat is the missing expression?'
    rows=[r'{∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A',rf'{{∬}}_{{D}}f(x,y,g(x,y))\sqrt{{1+({tex(dx)})^2+({tex(dy)})^2}}\,\text{{d}}A']
    # Keep unsimplified substitution and multiplication, then expanded collection.
    substituted=tex(f).replace('z^{2}',f'({tex(g)})^{{2}}')
    substituted=re.sub(r'(?<![A-Za-z])z(?![A-Za-z])',lambda _:f'({tex(g)})',substituted)
    rows.append(rf'{{∬}}_{{D}}\,({substituted})\cdot ({tex(m)})\,\text{{d}}A')
    if template not in BASE or template in ('plane_xyz','plane_xz'):
        rows.append(rf'{{∬}}_{{D}}\,({tex(pref)})\cdot ({tex(m)})\,\text{{d}}A')
    rows.append(integral(tex(answer),p['bounds']))
    sol=OPENING+'\n\n$$\n'+FORMULA+'\n$$\n\nFor the partial derivatives, we have\n\n$$\n'+rf'\frac{{∂z}}{{∂x}}=\frac{{∂}}{{∂x}}({tex(g)})={tex(dx)},'+'\n$$\n\nand\n\n$$\n'+rf'\frac{{∂z}}{{∂y}}=\frac{{∂}}{{∂y}}({tex(g)})={tex(dy)}.'+'\n$$\n\nTherefore, the surface integral can be written as \n\n$$\n'+r'\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'+'\n$$'
    # Complete bank selected before parameters. Every mistake changes dS conversion.
    bank=[answer,pref,pref*m*m,pref/m,pref*s.sqrt(dx*dx+dy*dy)]
    # Exact equivalence in the requested expression form, not UUID metadata.
    if any(eq(bank[i],bank[j]) for i in range(5) for j in range(i)):raise ValueError('whole bank is ambiguous')
    return prompt,sol,[tex(v) for v in bank]

def shape(q):
    """Convert capture refs/enums to local records without inventing absent keys."""
    q=copy.deepcopy(q)
    for f in q.get(':question/answer-fields',[]):
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        for a in f.get(':answer-field/choices',[]):a[':answer/type']=a[':answer/type'][':db/ident']
    if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    return q

def content_identity(level,q):
    fields=[]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct');cid=correct[1] if correct else None
        fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],'bank':sorted((a[':answer/type'],a[':answer/value'],a[':answer/id']==cid) for a in f[':answer-field/choices'])})
    obj={'version':VERSION,'difficulty':q.get(':question/difficulty'),'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'fields':fields}
    return str(uuid.uuid5(NAMESPACE,json.dumps(obj,sort_keys=True,ensure_ascii=False)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio response supported')
    rng=random.Random(seed)
    raw=bool(profile and profile.startswith('raw:'))
    if raw:
        source_id=profile[4:];matches=[t for t,b in BASE.items() if b['source']==source_id]
        if not matches:raise ValueError('unknown raw profile')
        if template is not None and template!=matches[0]:raise ValueError('profile/template mismatch')
        template=matches[0]
        if level!='easy':raise ValueError('raw originals have easy or authored replay-level easy')
        p=original_parameters(template) if parameters is None else copy.deepcopy(parameters)
    else:
        if profile not in (None,*METHOD_PROFILES):raise ValueError('unknown bank')
        profile=profile or rng.choice(METHOD_PROFILES)
        template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
        if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('level/template mismatch')
        p=sample(template,rng) if parameters is None else copy.deepcopy(parameters)
    check_parameters(template,level,p,raw=raw)
    if raw:q=shape(raw_render(template,p))
    else:
        prompt,sol,values=normal_render(template,p)
        q={':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/id':'provisional',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v,':answer/id':str(i)} for i,v in enumerate(values)],':answer-field/correct':[':answer/id','0']}]}
    ident=content_identity(level,q)
    original_raw=raw and ident==content_identity(level,shape(QUESTIONS[BASE[template]['source']]))
    if not original_raw:
        q[':question/id']=ident
        for f in q.get(':question/answer-fields',[]):
            fid=str(uuid.uuid5(uuid.UUID(ident),f[':answer-field/key']));f[':answer-field/id']=fid
            old=f.get(':answer-field/correct',[None,None])[1]
            for a in f[':answer-field/choices']:
                oldid=a[':answer/id'];a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),a[':answer/value']))
                if oldid==old:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    for f in q.get(':question/answer-fields',[]):rng.shuffle(f[':answer-field/choices'])
    f,g,dx,dy,m,pref,answer=model(template,p)
    # Domain bounds, seed, aliases, bank and letters are not part of assessed task.
    task={'response':'integrand setup','substituted_scalar':s.srepr(s.expand(pref)),'squared_metric':s.srepr(s.expand(1+dx**2+dy**2))}
    fingerprint=hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'template':template,'profile':profile,'parameters':p,'seed':seed,'content_id':ident,'mathematical_fingerprint':fingerprint,'eligible_for_learning':not raw,'evidence_only':raw,'bank_interpretation':'coefficient-scaled opaque historical expressions' if raw else 'complete method-derived dS conversion bank','source_ids':[BASE[template]['source']] if template in BASE else [],'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'domains':'real polynomial surface on ordered rectangle; positive metric factor','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY: observed monomial scalar functions on separable planes/quadrics. All
# historical workloads are retained; the unrated xz plane is an authored repair.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): coupled quadratic surface, both partials have two terms;
# one z substitution followed by multiplication. xz and yz are unordered forms.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): same coupled surface; two distinct nonzero z-dependent terms,
# one linear and one squared substitution before collection. Never evaluation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];lines=[q[':question/problem']]
    for field in q.get(':question/answer-fields',[]):lines+=['\nChoices:']+['- $'+a[':answer/value']+'$' for a in field[':answer-field/choices']]
    lines+=['\nWorked solution:\n'+q.get(':question/worked-solution','[Absent in raw source]'),'\nReview metadata: '+json.dumps(r['generation'],ensure_ascii=False)]
    return '\n'.join(lines)
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
