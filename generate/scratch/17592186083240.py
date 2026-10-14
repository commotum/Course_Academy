#!/usr/bin/env python3
"""Parametric derivative draft, frozen math basis 1356, no database writes.

Observed source-shaped families preserve individual coordinate/quotient/evaluation
stage masks. Parameter r scales x and s scales y, so every derivative and quotient
stage is transformed by its actual differential role. Historical opaque banks are
explicit evidence profiles; normal radio banks use complete differentiation-error
operations. Hard is authored: both coordinates require a product or quotient rule.
All samplers and explicit inputs have the same bounded arithmetic workload.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
from math_parser import parse
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record'];T=sp.Symbol('t',real=True)
VERSION='parametric-derivative-2';NS=uuid.UUID(KP[':knowledge-point/id'])
QUESTIONS={str(q[':db/id']):q for q in KP[':knowledge-point/questions']}
FAMILIES=['trig','exp_poly','quadratic','expneg_poly','trig_double','exp_poly_chain','line_poly','sqrt_linear','exp_pair','quartic','exp_product','quintic','root_power','line_quad','sqrt_scaled','texp_poly','product_sin','trig_scaled']
TEMPLATES={f:{'source_id':i,'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'kind':q[':question/answer-fields'][-1][':answer-field/type'][':db/ident'].split('/')[-1]} for f,(i,q) in zip(FAMILIES,QUESTIONS.items())}
TEMPLATES.update({'product_pair':{'level':'hard','kind':'blank'},'quotient_pair':{'level':'hard','kind':'blank'}})
SCALES=[sp.Rational(i,2) for i in range(1,13)]
DY=r'\frac{dy}{dx}'
def tex(v):return sp.latex(sp.sympify(v)).replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(NS,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def fingerprint(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def same(a,b):return sp.simplify(a-b)==0

def semantic_components(x,y,point,domain,level):
    """Remove common positive coordinate amplitude, retain shapes and ratio.

    The rational content of x is a positive global amplitude for all supported
    masks. Dividing both coordinates by that same amplitude identifies common
    scaling, including authored a,c scaling, without erasing the relative y/x
    amplitude or coordinate-function forms. Banks and raw coefficients still
    participate in content identity.
    """
    amplitude,primitive=sp.sympify(x).as_content_primitive()
    if amplitude<=0:raise ValueError('positive coordinate amplitude required')
    return [str(sp.simplify(primitive)),str(sp.simplify(y/amplitude)),str(point),domain,level]

def mathematical_fingerprint(x,y,point,domain,level):
    return fingerprint(semantic_components(x,y,point,domain,level))

def derivative_domain(template,p,curve_domain):
    result={'within_curve_domain':curve_domain,'condition':"x'(t) and y'(t) exist and x'(t) != 0"}
    if template=='product_pair':result['excluded_parameters']=[str(-sp.Rational(1,int(p['b'])))]
    elif template=='quotient_pair':result['excluded_parameters']=[]
    return result

def scaled(text,k):
    """Unit coefficient elision is an arithmetic rendering rule, never source lookup."""
    k=sp.sympify(k)
    return text if k==1 else tex(k)+r'\left('+text+r'\right)'
def groups(text,start):
    assert text[start]=='{';depth=1;i=start+1
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    return text[start+1:i-1],i

def quotient_scale(text,r,s):
    # Preserve each observed quotient's numerator and denominator components.
    if text.startswith(r'\frac{'):
        n,j=groups(text,5);d,k=groups(text,j)
        return r'\frac{'+scaled(n,s)+'}{'+scaled(d,r)+'}'+text[k:]
    return scaled(text,s/r)

def coordinate_components(q):
    block=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)[0]
    m=re.fullmatch(r'x=(.*?),\\,y=(.*?),\\,(.*)',block,re.S)
    if not m:raise ValueError(block)
    return m.groups()

def clean(expr):return expr.strip().removesuffix(r'\,.').removesuffix('.').removesuffix(r'\,')
def evaluation_parameter(q):
    m=re.search(r'where \$t=(.*?)\.\$',q[':question/problem'])
    return parse(m[1]) if m else None

def source_recipe(template,p):
    """Complete source component masks, including field absence and stage sequence."""
    q=QUESTIONS[TEMPLATES[template]['source_id']];r,s=map(sp.sympify,(p['r'],p['s']));z=s/r
    x,y,domain=coordinate_components(q);xv,yv=parse(x)*r,parse(y)*s
    oldblock=f'x={x},\\,y={y},\\,{domain}'
    newblock=f'x={scaled(x,r)},\\,y={scaled(y,s)},\\,{domain}'
    problem=q[':question/problem'].replace(oldblock,newblock)
    sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    derivative=blocks[1];match=re.match(r'(.*?=)(.*?)(,\\,.*?=)(.*?)(\.)$',derivative,re.S)
    if not match:raise ValueError(derivative)
    changed=match[1]+scaled(match[2],r)+match[3]+scaled(match[4],s)+match[5]
    sol=sol.replace('$$\n'+derivative+'\n$$','$$\n'+changed+'\n$$')
    for b in blocks[2:]:
        if r'\begin{aligned}' in b:
            # Each individually substituted, evaluated and collected row is retained.
            parts=re.split(r'( & =| \\\\  & =)',b)
            for i in range(2,len(parts),2):
                tail='';expr=parts[i]
                if expr.endswith(r'\end{aligned}'):
                    expr=expr[:-len(r'\end{aligned}')];tail=r'\end{aligned}'
                punctuation=r'\,.' if expr.endswith(r'\,.') else '.' if expr.endswith('.') else ''
                body=expr[:-len(punctuation)] if punctuation else expr
                parts[i]=quotient_scale(body,r,s)+punctuation+tail
            new=''.join(parts)
        else:
            lhs,*rhs=b.split('=');new=lhs+'='+'='.join(quotient_scale(clean(v),r,s)+(r'.' if j==len(rhs)-1 and v.endswith('.') else '') for j,v in enumerate(rhs))
        sol=sol.replace('$$\n'+b+'\n$$','$$\n'+new+'\n$$')
    fields=[]
    for f in q[':question/answer-fields']:
        ff={k:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else copy.deepcopy(v)) for k,v in f.items() if k!=':db/id'}
        choices=[]
        for a in f[':answer-field/choices']:
            raw=a[':answer/value'];lhs,sep,rhs=raw.partition('=')
            val=lhs+sep+scaled(rhs,z) if sep else scaled(raw,z)
            choices.append({':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
        ff[':answer-field/choices']=choices
        if ':answer-field/correct' in f:ff[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        fields.append(ff)
    out={k:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else copy.deepcopy(v)) for k,v in q.items() if k not in [':db/id',':question/answer-fields']}
    out[':question/problem']=problem;out[':question/worked-solution']=sol;out[':question/answer-fields']=fields
    return out,xv,yv,evaluation_parameter(q),domain

# EASY: single-coordinate power/exponential/trig derivatives and y'/x'; source
# easy labels are preserved, including supplied t evaluations and familiar roots.
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)
# MODERATE: source chain/product or signed quotient simplification, with supplied
# familiar evaluation t. No Cartesian-point inversion or tangent equation.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)
# HARD (authored): both coordinates have a product or quotient-rule demand;
# coefficients 1..5, linear shifts 1..4, shared exponential rate 1..3. The same
# prerequisite rules are combined, without second derivatives or new branches.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)

def authored_hard(template,p):
    a,b,c,d=[sp.Integer(p[k]) for k in 'abcd']
    if template=='product_pair':
        x=a*T*sp.exp(b*T);y=c*(T**2+d)*sp.exp(-b*T)
        xt=tex(a)+'t e^{'+tex(b)+'t}';yt=tex(c)+r'(t^2+'+tex(d)+')e^{-'+tex(b)+'t}'
        dx=tex(a)+r'e^{'+tex(b)+'t}+ '+tex(a)+r't('+tex(b)+r'e^{'+tex(b)+'t})'
        dy=tex(c)+r'(2t)e^{-'+tex(b)+'t}+'+tex(c)+r'(t^2+'+tex(d)+r')(-'+tex(b)+r'e^{-'+tex(b)+'t})'
        fx=tex(a)+r'(1+'+tex(b)+r't)e^{'+tex(b)+'t}'
        fy=tex(c)+r'(2t-'+tex(b)+r'(t^2+'+tex(d)+r'))e^{-'+tex(b)+'t}'
        formal=r"x'(t)=a\left(\frac{d}{dt}t\right)e^{bt}+at\left(\frac{d}{dt}e^{bt}\right),\quad y'(t)=c\left(\frac{d}{dt}(t^2+d)\right)e^{-bt}+c(t^2+d)\left(\frac{d}{dt}e^{-bt}\right)"
        formal=r"x'(t)="+tex(a)+r"\left(\frac{d}{dt}\left(t\right)\right)e^{"+tex(b)+r"t}+"+tex(a)+r"t\left(\frac{d}{dt}\left(e^{"+tex(b)+r"t}\right)\right),\quad y'(t)="+tex(c)+r"\left(\frac{d}{dt}\left(t^2+"+tex(d)+r"\right)\right)e^{-"+tex(b)+r"t}+"+tex(c)+r"(t^2+"+tex(d)+r")\left(\frac{d}{dt}\left(e^{-"+tex(b)+r"t}\right)\right)"
        ratio=r'\frac{'+fy+'}{'+fx+'}'
        final=r'\frac{'+tex(c)+r'(2t-'+tex(b)+r'(t^2+'+tex(d)+r'))}{'+tex(a)+r'(1+'+tex(b)+r't)}e^{-'+tex(2*b)+'t}'
        steps=[formal,r"x'(t)="+dx+r",\quad y'(t)="+dy,r"x'(t)="+fx+r",\quad y'(t)="+fy]
        rows=[ratio,final];domain=r'-\infty<t<\infty'
    else:
        x=a*T/(T+b);y=c*T**2/(T+d)
        xt=r'\frac{'+tex(a)+'t}{t+'+tex(b)+'}';yt=r'\frac{'+tex(c)+r't^2}{t+'+tex(d)+'}'
        formal=r"x'(t)=\frac{"+tex(a)+r"\left(\frac{d}{dt}\left(t\right)\right)(t+"+tex(b)+r")-"+tex(a)+r"t\left(\frac{d}{dt}\left(t+"+tex(b)+r"\right)\right)}{(t+"+tex(b)+r")^2},\quad y'(t)=\frac{"+tex(c)+r"\left(\frac{d}{dt}\left(t^2\right)\right)(t+"+tex(d)+r")-"+tex(c)+r"t^2\left(\frac{d}{dt}\left(t+"+tex(d)+r"\right)\right)}{(t+"+tex(d)+r")^2}"
        dx=r'\frac{'+tex(a)+r'(t+'+tex(b)+r')-'+tex(a)+r't(1)}{(t+'+tex(b)+r')^2}'
        dy=r'\frac{'+tex(2*c)+r't(t+'+tex(d)+r')-'+tex(c)+r't^2(1)}{(t+'+tex(d)+r')^2}'
        ex=r'\frac{'+tex(a)+r't+'+tex(a*b)+'-'+tex(a)+r't}{(t+'+tex(b)+r')^2}'
        ey=r'\frac{'+tex(2*c)+r't^2+'+tex(2*c*d)+r't-'+tex(c)+r't^2}{(t+'+tex(d)+r')^2}'
        fx=r'\frac{'+tex(a*b)+r'}{(t+'+tex(b)+r')^2}';fy=r'\frac{'+tex(c)+r't^2+'+tex(2*c*d)+r't}{(t+'+tex(d)+r')^2}'
        rows=[r'\frac{'+fy+'}{'+fx+'}',r'\frac{('+tex(c)+r't^2+'+tex(2*c*d)+r't)(t+'+tex(b)+r')^2}{'+tex(a*b)+r'(t+'+tex(d)+r')^2}']
        steps=[formal,r"x'(t)="+dx+r",\quad y'(t)="+dy,r"x'(t)="+ex+r",\quad y'(t)="+ey,r"x'(t)="+fx+r",\quad y'(t)="+fy]
        domain=r't>0'
    problem='For the parametric curve\n\n$$\nx='+xt+r',\quad y='+yt+r',\quad '+domain+',\n$$\n\ncalculate $'+DY+'$ as a function of $t.$\n\n$'+DY+'=$\n{{field-1}}'
    if template=='product_pair':
        problem=problem.replace('as a function of $t.$','as a function of $t$ for $t\\ne '+tex(-sp.Rational(1,b))+'.$')
    sol='We will use the formula\n\n$$\n'+DY+r"=\frac{y'(t)}{x'(t)}."+'\n$$\n\nDifferentiating $x$ and $y,$ we get\n\n'+''.join('$$\n'+z+'\n$$\n\n' for z in steps)+'Therefore,\n\n$$\n'+DY+'='+'='.join(rows)+'.\n$$'
    if template=='product_pair':sol+='\n\nThis derivative is defined for $t\\ne '+tex(-sp.Rational(1,b))+'.$'
    return problem,sol,x,y,domain,rows[-1]

def operation_bank(x,y,tvalue,template):
    dx,dy=sp.diff(x,T),sp.diff(y,T)
    ev=lambda z:sp.simplify(z.subs(T,tvalue) if tvalue is not None else z)
    if tvalue==0 and template=='line_quad':
        values=[ev(dy/dx),ev(sp.diff(y,T,2)/dx),ev(dx/sp.diff(y,T,2)),ev(x/dx),ev(sp.diff(y,T,2))]
        labels=['correct','use second derivative of y','invert second derivative quotient','use x instead of y derivative','omit denominator and use second derivative']
    elif template=='product_sin':
        values=[ev(dy/dx),ev(-dy/dx),ev(dx/dy),ev(-dx/dy),ev(y/x)]
        labels=['correct','lose negative derivative sign','invert derivative quotient','invert quotient and lose negative derivative sign','differentiate neither coordinate']
    elif template=='exp_poly':
        values=[ev(dy/dx),ev(dx/dy),ev(y/x),ev(dx*dy),ev(sp.diff(y,T,2)/dx)]
        labels=['correct','invert derivative quotient','differentiate neither coordinate','multiply coordinate derivatives','differentiate y twice']
    else:
        values=[ev(dy/dx),ev(dx/dy),ev(y/x),ev(dx*dy),ev(dy/x)]
        labels=['correct','invert derivative quotient','differentiate neither coordinate','multiply coordinate derivatives','omit differentiation of x']
    if any(v.has(sp.zoo,sp.nan,sp.oo,-sp.oo) for v in values):raise ValueError('invalid complete operation bank')
    if any(same(v,w) for i,v in enumerate(values) for w in values[i+1:]):raise ValueError('ambiguous complete operation bank')
    return values,labels

def sample(rng,template):
    if TEMPLATES[template]['level']=='hard':return dict(zip('abcd',[rng.randint(1,5),rng.randint(1,3),rng.randint(1,5),rng.randint(1,4)]))
    return {'r':str(rng.choice(SCALES)),'s':str(rng.choice(SCALES))}
def check_parameters(template,p):
    if TEMPLATES[template]['level']=='hard':
        if set(p)!=set('abcd'):raise ValueError('hard parameters are a,b,c,d')
        bounds={'a':5,'b':3,'c':5,'d':4}
        if any(sp.sympify(p[k]).is_Integer is not True or not 1<=int(p[k])<=bounds[k] for k in bounds):raise ValueError('hard workload bounds')
    else:
        if set(p)!=set(['r','s']) or any(sp.sympify(p[k]) not in SCALES for k in p):raise ValueError('source scale bounds: positive half integers 1/2..6')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError(level)
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        id=profile.split(':',1)[1];matches=[k for k,v in TEMPLATES.items() if v.get('source_id')==id]
        if not matches:raise ValueError(profile)
        if template is not None and template!=matches[0]:raise ValueError('profile/template mismatch')
        template=matches[0]
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (field_type is None or field_type.split('/')[-1]==v['kind'])]
    if template is None:template=rng.choice(eligible)
    if template not in eligible:raise ValueError('template/level/field mismatch')
    observed=bool(profile and profile.startswith('observed:'))
    if profile not in [None,'method'] and not observed:raise ValueError(profile)
    for attempt in range(100):
        p=copy.deepcopy(parameters) if parameters is not None else sample(rng,template);check_parameters(template,p)
        if level=='hard':
            problem,solution,x,y,domain,answer=authored_hard(template,p);point=None
            q={':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/hard'};sourceids=[];kind='blank'
        else:
            q,x,y,point,domain=source_recipe(template,p);sourceids=[TEMPLATES[template]['source_id']];kind=TEMPLATES[template]['kind']
            answer=tex(sp.simplify((sp.diff(y,T)/sp.diff(x,T)).subs(T,point) if point is not None else sp.diff(y,T)/sp.diff(x,T)))
        correct=sp.simplify((sp.diff(y,T)/sp.diff(x,T)).subs(T,point) if point is not None else sp.diff(y,T)/sp.diff(x,T))
        if not observed:
            q.pop(':question/math-academy-id',None)
            q[':question/problem']=q[':question/problem'].replace('Do not round the answer.','Give an exact answer.')
            if kind=='radio':
                try:values,labels=operation_bank(x,y,point,template)
                except ValueError:
                    if parameters is not None:raise
                    continue
                eq=template in ['trig','trig_scaled'];choices=[{':answer/type':':answer.type/math',':answer/value':(DY+'=' if eq else '')+(re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:r'\theta',tex(v)) if eq else tex(v))} for v in values]
                field={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices};correct_index=0
            else:
                # Retain source field shape, supplied fragment and source final notation.
                orig=q.get(':question/answer-fields')
                value=orig[-1][':answer-field/choices'][0][':answer/value'] if orig else answer
                field={':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':value}]};labels=['correct'];correct_index=0
            q[':question/answer-fields']=[field]
            if level!='hard':q[':question/problem']=render_plots(q[':question/problem'],template,p,x,y)
        else:labels=['observed expression-shape scaling; historical intent unresolved']
        break
    else:raise ValueError('no eligible whole instance')
    # Identity is complete learner content plus difficulty, never ordering or unused profile.
    canonical={k:v for k,v in q.items() if k not in [':question/id']}
    for f in canonical.get(':question/answer-fields',[]):
        f.pop(':answer-field/id',None)
        if ':answer-field/correct' in f:
            id=f[':answer-field/correct'][1];f['_correct_value']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a.get(':answer/id')==id);f.pop(':answer-field/correct')
        for a in f[':answer-field/choices']:a.pop(':answer/id',None)
    identity=fingerprint([VERSION,canonical]);qid=uid(['question',identity]);q[':question/id']=qid
    for index,f in enumerate(q[':question/answer-fields']):
        f[':answer-field/id']=uid([qid,index]);fcorrect=f.pop('_correct_value',None)
        for a in f[':answer-field/choices']:a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
        if not observed:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][0][':answer/id']]
        elif fcorrect is not None:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==fcorrect)]
        rng.shuffle(f[':answer-field/choices'])
    task=mathematical_fingerprint(x,y,point,domain,level)
    return {'knowledge_point':{'db_id':17592186083240,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source':{k:RAW[k] for k in ['database','basis','lineage']},'template':template,'profile':profile or 'method','parameters':{k:str(v) for k,v in p.items()},'seed':seed,'domain':domain,'curve_domain':domain,'derivative_domain':derivative_domain(template,p,domain),'source_ids':sourceids,'evidence_only':observed,'eligible_for_learning':not observed,'recipes':labels,'mathematical_fingerprint':task,'content_fingerprint':identity,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# PLOTS: source's seven supplementary curve graphs. Frozen anchor references are
# evidence only; normal plots compute each changed coordinate from this instance.
PLOT_T={'quadratic':(-3,4),'expneg_poly':(0,2),'trig_double':(0,2*float(sp.pi)),'quartic':(-1.6,1.6),'quintic':(-1.6,1.6),'line_quad':(-1,1),'texp_poly':(0,3)}
def render_plots(problem,template,p,x,y):
    refs=re.findall(r'!\[\]\(([^)]+)\)',problem)
    if not refs:return problem
    import os
    os.environ.setdefault('MPLCONFIGDIR','/tmp/kp83240-mpl')
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    import numpy as np,os,tempfile
    low,high=PLOT_T[template];tt=np.linspace(low,high,1200)
    xx=np.broadcast_to(sp.lambdify(T,x,'numpy')(tt),tt.shape);yy=np.broadcast_to(sp.lambdify(T,y,'numpy')(tt),tt.shape)
    name=fingerprint(['renderer-2',template,str(x),str(y),low,high])[:22];dest=HERE/'plots'/f'{name}.png';side=dest.with_suffix('.json');dest.parent.mkdir(exist_ok=True)
    if not dest.exists() or not side.exists():
        fig,ax=plt.subplots(figsize=(5,4),dpi=120);ax.plot(xx,yy,color='#2578bc',lw=1.5);ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8);ax.grid(alpha=.35);ax.set_xlabel('$x$');ax.set_ylabel('$y$');ax.set_aspect('equal' if template in ['trig_double','quartic','quintic','line_quad'] else 'auto',adjustable='datalim')
        if template=='line_quad':ax.plot(xx[0],yy[0],'o',color='#2578bc');ax.plot(xx[-1],yy[-1],'o',mfc='white',mec='#2578bc')
        fig.tight_layout();fd,tmp=tempfile.mkstemp(suffix='.png',dir=dest.parent);os.close(fd);fig.savefig(tmp);plt.close(fig);os.replace(tmp,dest)
        side_text=json.dumps({'template':template,'x':str(x),'y':str(y),'parameter_window':[low,high],'samples':1200,'matplotlib':matplotlib.__version__,'numpy':np.__version__,'python':sys.version.split()[0],'domain_endpoint_markers':template=='line_quad'},indent=2)
        fd,tmp=tempfile.mkstemp(suffix='.json',dir=dest.parent);os.close(fd);Path(tmp).write_text(side_text);os.replace(tmp,side)
    return problem.replace(refs[0],str(dest.resolve()))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty];rows=[generate(l,seed=a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    if a.format=='json':print(json.dumps(rows,ensure_ascii=False,indent=2))
    else:
        for v in rows:
            print(v['question'][':question/problem']);print('\nWorked solution\n');print(v['question'].get(':question/worked-solution',''))
            for f in v['question'].get(':question/answer-fields',[]):
                print('\nChoices:');print('\n'.join('$'+x[':answer/value']+'$' for x in f[':answer-field/choices']))
if __name__=='__main__':main()
