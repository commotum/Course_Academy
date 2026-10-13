#!/usr/bin/env python3
"""Coordinate image sets, math basis 1356; scratch only, no registration.

Observed moderate templates are component masks from source.json. Positive
coordinate dilations transport their entire worked argument and every complete
observed bank; opaque bank bounds are observed profiles, not inferred mistakes.
Normal radio generation uses a separately authored five-operation endpoint bank.
Easy assesses one affine coordinate on a half-line; hard assesses two quadratics
on the same half-line, each requiring square completion and admissibility. These
are authored level assignments within the prerequisite range/completing-square
method. No trig, relation elimination, calculus, or assessed reciprocal branch.
All choices are complete mathematical sets; explicit inputs never resample.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy.calculus.util import function_range, continuous_domain
KP_ID=17592186087722
KP_UUID='3cbf0ad0-a7c5-5c0f-a06c-9210fdc244ef'
TITLE='Determining the Range of a Parametric Equation'
VERSION='coordinate-ranges-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
T=sp.Symbol('t',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
class SampleRejected(ValueError): pass

def latex_expr(text):
    """Read the displayed TeX arithmetic, independently of generation metadata."""
    text=text.strip().rstrip('.')
    def group(s,i):
        if s[i]!='{':raise ValueError('Expected TeX group: '+s[i:])
        n=1;j=i+1
        while n:
            n+=(s[j]=='{')-(s[j]=='}');j+=1
        return s[i+1:j-1],j
    def rewrite(s):
        out='';i=0
        while i<len(s):
            if s.startswith('\\frac',i):
                a,j=group(s,i+5);b,k=group(s,j);out+='(('+rewrite(a)+')/('+rewrite(b)+'))';i=k
            elif s.startswith('\\sqrt',i):
                a,j=group(s,i+5);out+='sqrt('+rewrite(a)+')';i=j
            else:out+=s[i];i+=1
        return out
    text=rewrite(text)
    for a,b in [('\\left',''),('\\right',''),('\\,',''),('\\quad',''),('\\!',''),('\\infty','oo'),('∞','oo'),('{','('),('}',')'),('^','**')]:text=text.replace(a,b)
    return parse_expr(text,local_dict={'t':T,'sqrt':sp.sqrt,'oo':sp.oo},transformations=TRANS)

def parse_prompt(prompt):
    blocks=re.findall(r'\$\$(.*?)\$\$|\$([^$]+)\$',prompt,re.S)
    text=next(a or b for a,b in blocks if re.search(r'x\s*=',a or b) and re.search(r'y\s*=',a or b))
    clean=text.replace('\\,','').replace('\\quad','').strip().rstrip('.,')
    m=re.match(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),\s*(t.*)',clean,re.S)
    if not m:raise ValueError('Cannot read printed parametrization: '+text)
    xt,yt,dt=m.groups();dt=dt.replace(' ','').replace('\\leq','\\le').replace('\\geq','\\ge')
    if '\\in' in dt or '∈' in dt:
        interval=re.split(r'\\in|∈',dt,maxsplit=1)[1].replace('\\left','').replace('\\right','')
        if not (interval[0] in '[(' and interval[-1] in '])'):raise ValueError('Unreadable displayed interval '+interval)
        ends=interval[1:-1].split(',')
        if len(ends)!=2:raise ValueError('Unreadable interval endpoints')
        domain=sp.Interval(latex_expr(ends[0]),latex_expr(ends[1]),left_open=interval[0]=='(',right_open=interval[-1]==')')
    else:
        dm=re.match(r't(\\ge|\\le|>|<)(.+)',dt)
        if not dm:raise ValueError('Cannot read printed domain: '+dt)
        op,v=dm.groups();v=latex_expr(v)
        domain=sp.Interval(v,sp.oo,left_open=op=='>') if op in ('\\ge','>') else sp.Interval(-sp.oo,v,right_open=op=='<')
    x,y=latex_expr(xt),latex_expr(yt)
    # Both coordinates constrain admissibility, even if only one is assessed.
    admissible=domain.intersect(continuous_domain(x,T,sp.S.Reals)).intersect(continuous_domain(y,T,sp.S.Reals))
    return x,y,admissible,(xt,yt,dt)

def images(prompt,assessed):
    x,y,d,_=parse_prompt(prompt)
    return {v:function_range({'x':x,'y':y}[v],T,d) for v in assessed}

def scalar(s):return sp.latex(sp.sympify(s))
def set_tex(v,s):
    if s==sp.S.Reals:return v+r'\in\mathbb{R}'
    if isinstance(s,sp.FiniteSet):return v+'='+scalar(next(iter(s)))
    if not isinstance(s,sp.Interval):raise ValueError('Unsupported output set '+str(s))
    if s.end==sp.oo:return v+('>' if s.left_open else r'\ge ')+scalar(s.start)
    if s.start==-sp.oo:return v+('<' if s.right_open else r'\le ')+scalar(s.end)
    return scalar(s.start)+('<' if s.left_open else r'\le ')+v+('<' if s.right_open else r'\le ')+scalar(s.end)
def paired_tex(sets):return r',\,'.join(set_tex(v,s) for v,s in sets.items())

def parse_sets(tex):
    """Full Cartesian product of coordinate constraints, including finite intervals."""
    tex=tex.replace('\\,','').replace(' ','').replace('\\geq','\\ge').replace('\\leq','\\le')
    result={}
    for part in tex.split(','):
        if '\\in\\mathbb{R}' in part:result[part[0]]=sp.S.Reals;continue
        m=re.match(r'([xy])(\\ge|\\le|>|<|=)(.+)$',part)
        if m:
            v,op,b=m.groups();b=latex_expr(b)
            result[v]=sp.FiniteSet(b) if op=='=' else sp.Interval(b,sp.oo,left_open=op=='>') if op in ('\\ge','>') else sp.Interval(-sp.oo,b,right_open=op=='<');continue
        m=re.match(r'(.+?)(\\le|<)([xy])(\\le|<)(.+)$',part)
        if not m:raise ValueError('Unreadable complete constraint '+part)
        a,lo,v,hi,b=m.groups();result[v]=sp.Interval(latex_expr(a),latex_expr(b),left_open=lo=='<',right_open=hi=='<')
    return result

def dilate(s,k):
    if s==sp.S.Reals:return s
    if isinstance(s,sp.Interval):return sp.Interval(s.start*k,s.end*k,left_open=s.left_open,right_open=s.right_open)
    return sp.FiniteSet(*[a*k for a in s])
def endpoint(s):
    return (s.start,'lower',not s.left_open) if s.end==sp.oo else (s.end,'upper',not s.right_open)
def authored_bank(correct):
    """A complete five-member bank, selected as a unit before validation.

    Pair banks include one wrong coordinate at a time, so both constraints matter.
    """
    def reverse(s):
        b,side,closed=endpoint(s)
        return sp.Interval(-sp.oo,b,right_open=not closed) if side=='lower' else sp.Interval(b,sp.oo,left_open=not closed)
    def toggle(s):
        b,side,closed=endpoint(s)
        return sp.Interval(s.start,s.end,left_open=not s.left_open if side=='lower' else s.left_open,right_open=not s.right_open if side=='upper' else s.right_open)
    keys=list(correct);v=keys[0]
    if len(keys)==2:
        w=keys[1]
        return [dict(correct),{**correct,v:reverse(correct[v])},{**correct,w:reverse(correct[w])},{a:toggle(s) for a,s in correct.items()},{a:sp.FiniteSet(endpoint(s)[0]) for a,s in correct.items()}]
    s=correct[v];b,_,_=endpoint(s)
    return [dict(correct),{v:reverse(s)},{v:toggle(s)},{v:sp.FiniteSet(b)},{v:sp.S.Reals}]

# Source templates: fixed prose/layout and complete mathematical-component slots.
TEMPLATES={}
for q in SOURCE['record'][':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];problem=q[':question/problem'];x,y,d,parts=parse_prompt(problem)
    rawx=re.search(r'x\s*=\s*(.*?)\s*,(?:\s|\\,|\\quad)*y',problem,re.S)[1]
    rawy=re.search(r'y\s*=\s*(.*?)\s*,(?:\s|\\,|\\quad)*t(?:\s|\\|∈|>|<)',problem,re.S)[1]
    asked=re.search(r'(?:range of|ranges of) \$([xy])',problem)
    assessed=['x','y'] if 'ranges of' in problem else [asked.group(1)]
    fields=q.get(':question/answer-fields',[])
    kind=fields[0][':answer-field/type'][':db/ident'].split('/')[-1] if fields else 'radio'
    TEMPLATES[sid]={'level':'moderate','source_id':sid,'problem':problem,'solution':q.get(':question/worked-solution'),'x_tex':rawx,'y_tex':rawy,'assessed':assessed,'kind':kind,'fields':fields,'rated':':question/difficulty' in q}
TEMPLATES['affine_endpoint']={'level':'easy','kind':'radio','assessed':['x'],'source_id':None}
TEMPLATES['two_quadratic_endpoints']={'level':'hard','kind':'radio','assessed':['x','y'],'source_id':None}

def scaled_solution(text,p,answer):
    if text is None:return None
    def relation(s):
        # A complete coordinate equation/inequality chain is one template slot.
        # Labels and auxiliary square/root/domain facts have no coordinate slot.
        vars=re.findall(r'(?<![A-Za-z\\])([xy])(?![A-Za-z])',s)
        if not vars:return s
        if len(set(vars))>1:
            try:return paired_tex({v:dilate(st,p['s'+v]) for v,st in parse_sets(s).items()})
            except ValueError:raise ValueError('Unmapped mixed coordinate component '+s)
        v=vars[0];k=p['s'+v]
        if k==1:return s
        bits=re.split(r'(\\geq(?![A-Za-z])|\\leq(?![A-Za-z])|\\ge(?![A-Za-z])|\\le(?![A-Za-z])|>|<|=)',s)
        if len(bits)<3:return s
        result=[]
        for i,bit in enumerate(bits):
            if i%2:result.append(bit);continue
            if bit.strip()==v:result.append(v);continue
            punctuation=re.search(r'[.,]$',bit.strip());punct=punctuation[0] if punctuation else ''
            arithmetic=bit.strip().rstrip('.,')
            result.append((sp.latex(sp.expand_mul(k*latex_expr(arithmetic))) if i==len(bits)-1 else str(k)+r'\left('+arithmetic+r'\right)')+punct)
        return ''.join(result)
    def mathslot(m):
        whole=m.group(0);delim='$$' if whole.startswith('$$') else '$';body=whole[len(delim):-len(delim)]
        if r'\begin{aligned}' in body:
            a,b=body.split(r'\begin{aligned}',1);aligned,c=b.split(r'\end{aligned}',1)
            rows=aligned.split('\\\\');v=None;transport=[]
            for index,row in enumerate(rows):
                lhs,rhs=row.split('=',1)
                if lhs.replace('&','').strip():v=lhs.replace('&','').strip()
                k=p['s'+v]
                transport.append(row if k==1 else lhs+'='+(sp.latex(sp.expand_mul(k*latex_expr(rhs))) if index==len(rows)-1 else str(k)+r'\left('+rhs.strip()+r'\right)'))
            return delim+a+r'\begin{aligned}'+'\\\\'.join(transport)+r'\end{aligned}'+c+delim
        return delim+relation(body)+delim
    return re.sub(r'\$\$.*?\$\$|\$[^$]*?\$',mathslot,text,flags=re.S)

def source_build(spec,p):
    problem=spec['problem']
    # Exact masks around whole coordinate expressions; never replace short numbers.
    for v in ('x','y'):
        old=spec[v+'_tex'];k=p['s'+v];new=old if k==1 else str(k)+r'\left('+old+r'\right)'
        pattern=re.compile(r'('+v+r'\s*=\s*)'+re.escape(old))
        problem,n=pattern.subn(lambda m:m.group(1)+new,problem,count=1)
        if n!=1:raise ValueError('Coordinate component mask failed')
    correct=images(problem,spec['assessed'])
    solution=scaled_solution(spec['solution'],p,correct)
    if solution is None:
        solution="Let's consider each variable in turn.\n\n"+ '\n\n'.join('The range of $'+v+'$ on the given parameter domain is $'+set_tex(v,s)+'.$' for v,s in correct.items())
        if spec['source_id']=='q-16203':solution="Let's consider each variable in turn.\n\nFor $t\\ge0$, both $"+sp.latex(parse_prompt(problem)[0])+"$ and $"+sp.latex(parse_prompt(problem)[1])+"$ are nonnegative and attain $0$ at $t=0$. They are continuous, increase on the parameter domain, and are unbounded above. Therefore, $"+paired_tex(correct)+'.$'
        if spec['source_id']=='q-16205':solution='Completing the square gives $x='+sp.latex(p['sx']*(T-2)**2-4*p['sx'])+r'$. The square is nonnegative and is zero at the admissible value $t=2$. Therefore, $'+paired_tex(correct)+'.$'
    return problem,solution,correct

def domain_tex(bound,direction,closed):return 't'+(r'\ge ' if closed else '>')+scalar(bound) if direction=='lower' else 't'+(r'\le ' if closed else '<')+scalar(bound)
def authored_build(name,p):
    if name=='affine_endpoint':x=p['a']*T+p['b'];y=T;assessed=['x']
    else:
        x=p['a']*T**2+p['b']*T+p['c'];y=p['d']*T**2+p['e']*T+p['f'];assessed=['x','y']
    dt=domain_tex(p['bound'],p['direction'],p['closed'])
    problem='Given that a curve is defined parametrically as\n\n$$\nx='+sp.latex(x)+r',\,y='+sp.latex(y)+r',\,'+dt+',\n$$\n\n'+('determine the range of $x.$' if len(assessed)==1 else 'determine the ranges of $x$ and $y.$')
    correct=images(problem,assessed);domain=parse_prompt(problem)[2]
    rows=[]
    for v,expr in zip(['x','y'],[x,y]):
        if v not in assessed:continue
        if sp.degree(expr,T)==1:
            rows.append('- To find the range of $'+v+',$ evaluate the endpoint: $'+v+'('+scalar(p['bound'])+')='+scalar(expr.subs(T,p['bound']))+'$. The coefficient of $t$ is $'+scalar(sp.expand(expr).coeff(T))+ '$, so the coordinate is monotone on the given half-line. The parameter endpoint is '+('included' if p['closed'] else 'excluded')+'. The range is $'+set_tex(v,correct[v])+'.$')
        else:
            a=expr.coeff(T,2);h=-expr.coeff(T)/(2*a);k=sp.simplify(expr.subs(T,h));square=a*(T-h)**2+k
            vertex_allowed=domain.contains(h)==sp.true
            rows.append('- To find the range of $'+v+',$ complete the square:\n\n$$\n'+v+'='+sp.latex(expr)+'='+sp.latex(square)+' .\n$$\n\nThe vertex parameter is $t='+scalar(h)+'$, which is '+('admissible' if vertex_allowed else 'outside the given domain')+'. '+('The vertex value is $'+scalar(k)+'$ and is attained.' if vertex_allowed else 'On the given half-line the endpoint value is $'+scalar(expr.subs(T,p['bound']))+'$, and the endpoint is '+('included.' if p['closed'] else 'excluded.'))+' The coordinate is unbounded '+('above' if a>0 else 'below')+'. Consequently, $'+set_tex(v,correct[v])+'.$')
    return problem,"Let's consider each variable in turn.\n\n"+'\n\n'.join(rows),correct

def parameters_for(name,rng):
    if name.startswith('q-'):return {'sx':rng.randint(1,6),'sy':rng.randint(1,6)}
    if name=='affine_endpoint':return {'a':rng.choice([-3,-2,-1,1,2,3]),'b':rng.randint(-6,6),'bound':rng.randint(-3,3),'direction':rng.choice(['lower','upper']),'closed':rng.choice([True,False])}
    # Equal-level problems all require two nontrivial square completions.
    return {'a':rng.choice([-2,-1,1,2]),'b':rng.choice([-6,-4,-2,2,4,6]),'c':rng.randint(-5,5),'d':rng.choice([-2,-1,1,2]),'e':rng.choice([-6,-4,-2,2,4,6]),'f':rng.randint(-5,5),'bound':rng.randint(-3,3),'direction':rng.choice(['lower','upper']),'closed':rng.choice([True,False])}
def check_parameters(name,p):
    keys={'sx','sy'} if name.startswith('q-') else {'a','b','bound','direction','closed'} if name=='affine_endpoint' else {'a','b','c','d','e','f','bound','direction','closed'}
    if set(p)!=keys:raise ValueError('Explicit parameter keys must be '+str(sorted(keys)))
    if name.startswith('q-'):
        if any(type(p[v])!=int or not 1<=p[v]<=6 for v in keys):raise ValueError('Source dilation bounds are integer 1..6')
    else:
        if p['direction'] not in ('lower','upper') or type(p['closed'])!=bool:raise ValueError('Invalid half-line')
        nums={k:v for k,v in p.items() if k not in ('direction','closed')}
        if any(type(v)!=int for v in nums.values()) or abs(p['bound'])>3:raise ValueError('Invalid parameter type/bound')
        if name=='affine_endpoint':
            if p['a'] not in (-3,-2,-1,1,2,3) or abs(p['b'])>6:raise ValueError('Easy coefficient bounds')
        else:
            if any(p[k] not in (-2,-1,1,2) for k in ('a','d')) or any(p[k] not in (-6,-4,-2,2,4,6) for k in ('b','e')) or any(abs(p[k])>5 for k in ('c','f')):raise ValueError('Hard coefficient bounds')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (field_type is None or v['kind']==field_type)]
    if template is None:
        if not eligible:raise ValueError('Unsupported field type')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('Template/level/field type mismatch')
    spec=TEMPLATES[template];p=dict(parameters) if parameters is not None else parameters_for(template,rng);check_parameters(template,p)
    problem,solution,correct=source_build(spec,p) if template.startswith('q-') else authored_build(template,p)
    kind=spec['kind'];profile=profile or ('blank-observed' if kind=='blank' else 'authored-endpoint-bank')
    if profile not in ('blank-observed','observed:'+template,'authored-endpoint-bank'):raise ValueError('Unknown or ineligible profile')
    if kind=='blank' and profile!='blank-observed':raise ValueError('Blank cannot select a radio bank')
    if kind=='radio' and profile=='blank-observed':raise ValueError('Radio cannot use blank profile')
    values=[]
    if kind=='radio':
        if profile.startswith('observed:'):
            if not spec.get('fields'):raise ValueError('Fieldless original has no observed bank')
            original=spec['fields'][0][':answer-field/choices']
            for answer in original:
                sets=parse_sets(answer[':answer/value']);transported={v:dilate(s,p['s'+v]) for v,s in sets.items()}
                # Preserve raw notation at unit scale via a mathematical render slot.
                rendered=answer[':answer/value'] if all(p['s'+v]==1 for v in sets) else paired_tex(transported)
                values.append((rendered,transported))
        else:values=[(paired_tex(s),s) for s in authored_bank(correct)]
        if len(values)!=5 or len({str(s) for _,s in values})!=5 or sum(s==correct for _,s in values)!=1:raise SampleRejected('Whole bank rejected: duplicate/ambiguous sets')
        field_values=[('selection','radio',values)]
    else:
        field_values=[]
        for f in sorted(spec['fields'],key=lambda f:f[':answer-field/key']):
            key=f[':answer-field/key'];idx=int(key[-1]);v='x' if idx<=2 else 'y';b,side,closed=endpoint(correct[v]);op=('>' if not closed else r'\ge ') if side=='lower' else ('<' if not closed else r'\le ')
            field_values.append((key,'blank',[(op if idx%2 else scalar(b),None)]))
    canonical_parameters={'assessed_images':{v:str(parse_prompt(problem)[i]) for i,v in enumerate(('x','y')) if v in spec['assessed']},'admissible_domain':str(parse_prompt(problem)[2])}
    fingerprint=hashlib.sha256(json.dumps(canonical_parameters,sort_keys=True).encode()).hexdigest()
    contents={'version':VERSION,'problem':problem,'solution':solution,'bank':[(k,sorted(v for v,_ in vals)) for k,_,vals in field_values]}
    content=hashlib.sha256(json.dumps(contents,sort_keys=True).encode()).hexdigest();qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));fields=[]
    for key,ft,vals in field_values:
        fid=str(uuid.uuid5(uuid.UUID(qid),key));choices=[];cid=None
        for val,sets in vals:
            aid=str(uuid.uuid5(uuid.UUID(fid),val));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
            if ft=='blank' or sets==correct:cid=aid
        rng.shuffle(choices)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':'observed coordinate transport; intent unresolved' if profile.startswith('observed:') else 'observed blank' if kind=='blank' else 'authored endpoint operations','parameter_fingerprint':fingerprint,'content_fingerprint':content,'plot_rating':'none','plot_assets':{},'source_analysis':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'question_ids':[template] if template.startswith('q-') else [],'method_references':['e-5099','q-73604','q-73617']},'level_origin':'observed' if spec.get('rated') else 'authored','authored_missing_fields':template=='q-73604','authored_correct_designation':template in ('q-16203','q-16205','q-73604'),'sympy_version':sp.__version__}}
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
    q=record['question'];out=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:
        out+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+'):\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
    return out+'Worked solution:\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
