#!/usr/bin/env python3
"""Exact Cartesian-curve one-form generators; local review only, no DB operations.

Basis 1356; evidence, scope, source anomalies and verification beside this file.
Source recipes reconstruct extracted prose/math slots under uniform one-form
scaling. Original scalar distractor intent is underdetermined: observed profiles
are explicitly replay-only, never the default practice bank. Normal generators
use five complete operations and reject the whole instance on any collision.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'17592186179674'
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
KP=CAPTURE['record'];KP_ID=17592186179674
VERSION='cartesian-oneform-v1'
X,Y,T=sp.symbols('x y t',real=True)
SOURCE_QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Exactly observed source families; source order is not curriculum ordering.
FAMILIES={'parabola_xy':'q-39344','shift_log':'q-81178','sqrt_linear':'q-124664','cubic_recip':'q-124668','cuberoot_exp':'q-39679','sqrt_poly':'q-80983','shift_cross':'q-81098','trig_sin':'q-81180','hard_poly':'q-90848','trig_cos':'q-90871','square_cancel':'q-124666'}
TEMPLATES={name:{'level':SOURCE_QUESTIONS[sid][':question/difficulty'][':db/ident'].rsplit('/',1)[1],'source_id':sid} for name,sid in FAMILIES.items()}
TEMPLATES.update({'easy_xy':{'level':'easy','source_id':None},'easy_cross':{'level':'easy','source_id':None}})
BASE={
'parabola_xy':dict(a=1,b=1,c=1,u=0,v=2),
'shift_log':dict(a=1,b=1,h=1,u=0,v=1),
'sqrt_linear':dict(a=1,b=1,c=2,u=1,v=2),
'cubic_recip':dict(a=1,b=1,c=1,u=1,v=2),
'cuberoot_exp':dict(a=4,b=1,c=1,u=0,v=1),
'sqrt_poly':dict(a=1,b=1,c=1,d=3,e=2,u=0,v=1),
'shift_cross':dict(a=2,b=1,h=1,u=0,v=2),
 'trig_sin':dict(a=3,c=1,d=2,u=1,v=2),
'hard_poly':dict(a=5,b=1,h=1,u=0,v=2),
 'trig_cos':dict(a=4,c=1,d=1,u=0,v=1),
'square_cancel':dict(a=1,b=1,h=1,u=1,v=2),
'easy_xy':dict(a=1,b=1,c=1,u=0,v=1),
'easy_cross':dict(a=1,b=1,c=1,u=0,v=1)}


def load_parser():
    spec=importlib.util.spec_from_file_location('oneform_display_parser',ROOT.parent/'runs/current/vector-math-parser.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
PARSER=load_parser()
def normalize(raw):
    return raw.replace('\\\\','\\').replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
def scalar(raw):return PARSER.scalar(normalize(raw))
def tex(expr):return sp.latex(expr).replace(r'\log',r'\ln')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def scaled(k,body):return body if k==1 else tex(k)+r'\left('+body+r'\right)'
def integral(body,u,v):return r'{\int }_{'+tex(u)+'}^{'+tex(v)+'}'+body+r'\,dt'
def grouped(body):return r'\left('+body+r'\right)'
def substitute(raw,xt,yt):
    # Protect entire TeX commands, substitute BOTH letters in implicit xy.
    return re.sub(r'\\[A-Za-z]+|[xy]',lambda m:grouped(tex(xt if m[0]=='x' else yt)) if m[0] in ('x','y') else m[0],raw)
def expression_add(parts):
    out=''
    for z in parts:
        z=z.strip();out+=('+' if out and not z.startswith('-') else '')+z
    return out

def math_object(name,p):
    a=p.get('a',1);b=p.get('b',1);c=p.get('c',1);h=p.get('h',1);d=p.get('d',1);e=p.get('e',1)
    xt=T;yt=c*T**2;curve=c*X**2
    if name in ('parabola_xy','easy_xy'):P,Q=a*X,b*Y
    elif name=='easy_cross':P,Q=a*Y,b*X
    elif name=='shift_log':yt=(T+h)**2;curve=(X+h)**2;P,Q=a/Y,b/Y
    elif name=='sqrt_linear':xt=T**2;yt=c*T;curve=c*sp.sqrt(X);P,Q=a*(X-Y),b*(X+Y)
    elif name=='cubic_recip':yt=c*T**3;curve=c*X**3;P,Q=a/Y,b/X**2
    elif name=='cuberoot_exp':xt=T**3;yt=c*T;curve=c*X**sp.Rational(1,3);P,Q=a*Y*sp.exp(X*Y),b
    elif name=='sqrt_poly':xt=T**2;yt=c*T;curve=c*sp.sqrt(X);P,Q=a*X**2+b*Y,d*X+e*Y
    elif name=='shift_cross':yt=T**2-h*T;curve=X**2-h*X;P,Q=a*X*Y,b*X
    elif name=='trig_sin':yt=c*sp.pi*T**2;curve=c*sp.pi*X**2;P,Q=sp.sin(Y/(d*X**2)),a*X
    elif name=='hard_poly':yt=T**2-h;curve=X**2-h;P,Q=a*X**2*Y,b*X**2*(Y+h)
    elif name=='trig_cos':yt=c*sp.pi*T**2;curve=c*sp.pi*X**2;P,Q=sp.cos(Y/(d*X**2)),a*X**2
    elif name=='square_cancel':yt=T**2-h;curve=X**2-h;P,Q=a*Y**2,b*X
    else:raise ValueError(name)
    P,Q=map(sp.sympify,(P,Q))
    pp=sp.simplify(P.subs({X:xt,Y:yt},simultaneous=True));qq=sp.simplify(Q.subs({X:xt,Y:yt},simultaneous=True))
    dx,dy=sp.diff(xt,T),sp.diff(yt,T)
    dxterm,dyterm=sp.expand(pp*dx),sp.expand(qq*dy)
    integrand=sp.expand(dxterm+dyterm)
    antiderivative=sp.integrate(integrand,T)
    u,v=p['u'],p['v']
    value=sp.simplify(antiderivative.subs(T,v)-antiderivative.subs(T,u))
    return dict(xt=xt,yt=yt,curve=curve,P=P,Q=Q,pp=pp,qq=qq,dx=dx,dy=dy,dxterm=dxterm,dyterm=dyterm,integrand=integrand,F=antiderivative,value=value)

def guard(name,p,observed=False):
    if observed:
        if set(p)!={'scale'}:raise ValueError('Observed replay supports exactly one-form scale; original curve/limits stay fixed.')
        if type(p['scale']) is not int or not 1<=p['scale']<=6:raise ValueError('Replay scale must be integer 1..6')
        return
    expected=set(BASE[name]);
    if set(p)!=expected:raise ValueError(('exact parameter keys required',expected,set(p)))
    if any(type(v) is not int for v in p.values()):raise ValueError('integer parameter domain')
    if not 0<=p['u']<p['v']<=3:raise ValueError('ordered nonnegative t limits, upper bound 3')
    for key in expected-{'u','v'}:
        bound=5 if key=='a' and name in ('hard_poly','cuberoot_exp','trig_cos','trig_sin') else 3
        if not 1<=p[key]<=bound:raise ValueError(('positive nonzero coefficient',key,bound))
    if name.startswith('easy_') and (p['u']!=0 or p['v']!=1):raise ValueError('Easy uses [0,1], two low-degree products')
    if name=='parabola_xy' and p['v']<2:raise ValueError('Moderate parabola uses upper t limit 2 or 3')
    if name=='cubic_recip' and p['u']==0:raise ValueError('Reciprocal curve must avoid zero')
    if name=='cuberoot_exp' and (p['c']!=1 or p['u']!=0 or p['v']!=1):raise ValueError('Exponential source workload requires c=1,[0,1]')
    if name=='sqrt_poly' and p['v']>2:raise ValueError('Moderate polynomial root: v<=2')
    if name=='hard_poly' and p['v']>2:raise ValueError('Hard polynomial: v<=2')
    if name in ('trig_cos','trig_sin'):
        if p['d'] not in (1,2) or p['c'] not in (1,2,3):raise ValueError('familiar trig arguments only')
        if name=='trig_sin' and (p['u']==0 or p['d']!=2 or p['c'] not in (1,3)):raise ValueError('Sine preserves nonzero familiar value and nonsingular lower endpoint')
        if name=='trig_cos' and p['d']!=1:raise ValueError('Cosine retains nonzero value, pi multiples')

def samples(name,rng):
    p=dict(BASE[name]);
    for key in sorted(set(p)-{'u','v'}):p[key]=rng.randint(1,5 if key=='a' and name in ('hard_poly','cuberoot_exp','trig_cos','trig_sin') else 3)
    p['u']=rng.randint(0,1);p['v']=rng.randint(p['u']+1,3)
    if name.startswith('easy_'):p['u']=0;p['v']=1
    if name=='parabola_xy':p['v']=rng.choice([2,3])
    if name=='cubic_recip':p['u']=1;p['v']=rng.choice([2,3])
    if name=='cuberoot_exp':p['c']=1;p['u']=0;p['v']=1
    if name in ('sqrt_poly','hard_poly'):p['v']=2
    if name=='trig_sin':p['c']=rng.choice([1,3]);p['d']=2;p['u']=1;p['v']=rng.choice([2,3])
    if name=='trig_cos':p['d']=1
    return p


def source_parts(q):
    """Stage-4 masks: prose + whole math components, never tiny string replacements."""
    text=q[':question/worked-solution'];blocks=re.findall(r'\$\$.*?\$\$',text,re.S)
    assert len(blocks)==3
    rows=blocks[-1][2:-2].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\')
    masks=[]
    for row in rows:
        lhs,rhs=row.split('=',1);masks.append((lhs,rhs))
    return blocks,masks

def source_recipe(name,k,raw=False):
    """One-form scaling acts on every complete scalar stage and complete bank.

    Source expression patterns are retained, without reverse-engineering unknown
    numeric distractors into misleading error diagnoses. Profiles are replay-only.
    """
    q=SOURCE_QUESTIONS[FAMILIES[name]];blocks,rows=source_parts(q)
    problem=q[':question/problem'];matches=list(re.finditer(r'\$[^$]*\$',problem))
    slot=matches[-1];body=slot[0][1:-1];assert body.endswith('=')
    component=body[:-1];problem=problem[:slot.start()]+'$'+scaled(k,component)+'=$'+problem[slot.end():]
    rendered=[]
    for index,(lhs,rhs) in enumerate(rows):
        # The first lhs is a complete line integral; subsequent lhs are & only.
        if index==0:lhs=scaled(k,lhs.strip().rstrip('&').strip())+' & '
        rendered.append(lhs+'='+(' '+scaled(k,rhs.strip()) if k!=1 else rhs))
    evaluation='$$\n'+r'\begin{aligned}'+r'\\'.join(rendered)+r'\end{aligned}'+'\n$$'
    solution=q[':question/worked-solution'].replace(blocks[-1],evaluation)
    # k=1 reconstructed source row spaces are exact (first lhs needs no wrapping).
    if k==1:
        evaluation='$$\n'+r'\begin{aligned}'+r'\\'.join(lhs+'='+rhs for lhs,rhs in rows)+r'\end{aligned}'+'\n$$'
        solution=q[':question/worked-solution'].replace(blocks[-1],evaluation)
    original=q[':question/answer-fields'][0]
    choices=[scaled(k,a[':answer/value'] if raw else normalize(a[':answer/value'])) for a in original[':answer-field/choices']]
    correct=scaled(k,original[':answer-field/correct'][':answer/value'] if raw else normalize(original[':answer-field/correct'][':answer/value']))
    repairs=[]
    if not raw and name=='sqrt_linear':
        bad=next(i for i,a in enumerate(original[':answer-field/choices']) if normalize(a[':answer/value'])==r'\frac{42}{7}')
        # Omit the common factor 2 in the source's explicitly factored integral.
        choices[bad]=tex(k*math_object(name,BASE[name])['value']/2)
        repairs.append('replace duplicate 42/7 with the omitted common-factor result 53/12')
    if not raw and name=='trig_cos':
        problem+=' The composed integrand at the initial endpoint is interpreted by its one-sided continuous extension along $C.$'
        repairs.append('state the one-sided extension at x=0; the original one-form is undefined there')
    return problem,solution,choices,correct,repairs


def authored(name,p,m):
    xt,yt,dx,dy=m['xt'],m['yt'],m['dx'],m['dy'];u,v=p['u'],p['v']
    if name=='cuberoot_exp':curve=(str(p['c']) if p['c']!=1 else '')+r'\sqrt[3]{x}'
    else:curve=tex(m['curve'])
    Ptex,Qtex=tex(m['P']),tex(m['Q'])
    oneform=grouped(Ptex)+r'\,dx+'+grouped(Qtex)+r'\,dy'
    A=','.join(tex(z.subs(T,u)) for z in (xt,yt));B=','.join(tex(z.subs(T,v)) for z in (xt,yt))
    problem='If the path $C$ is a part of the graph $y='+curve+'$ traversed from the point $A('+A+')$ to point $B('+B+'),$ then $'+r'{\int }_C'+oneform+'=$'
    if name=='trig_cos' and u==0:problem+=' The composed integrand at the initial endpoint is interpreted by its one-sided continuous extension along $C.$'
    prose='Notice that our curve is given by the explicit Cartesian equation $y='+curve+'.$ As a result, we obtain the following parametrization of the curve:\n\n'
    prose+='$$\n'+r'\begin{aligned}r(t)=x(t)\,i+y(t)\,j='+grouped(tex(xt))+r'\,i+'+grouped(tex(yt))+r'\,j,\,t\in ['+str(u)+','+str(v)+r']\end{aligned}'+'\n$$\n\n'
    prose+='The derivative of $r(t)$ is given by\n\n$$\n'+r'\begin{aligned}{r}^{′}(t)&=\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j='+grouped(tex(dx))+r'\,i+'+grouped(tex(dy))+r'\,j.\end{aligned}'+'\n$$\n\nWe can now evaluate the line integral:\n\n'
    Psub,Qsub=substitute(Ptex,xt,yt),substitute(Qtex,xt,yt)
    symbolic1=grouped(Ptex)+r'\frac{\text{d}x}{\text{d}t}\,\text{d}t+'+grouped(Qtex)+r'\frac{\text{d}y}{\text{d}t}\,\text{d}t'
    symbolic2=grouped(Ptex)+r'\frac{\text{d}x}{\text{d}t}+'+grouped(Qtex)+r'\frac{\text{d}y}{\text{d}t}'
    row0=r'{\int }_C'+oneform+' &='+r'{\int }_{'+str(u)+'}^{'+str(v)+'}'+symbolic1
    rows=[row0,' &='+integral(grouped(symbolic2),u,v),' &='+integral(grouped(Psub)+r'\cdot '+grouped(tex(dx))+'+'+grouped(Qsub)+r'\cdot '+grouped(tex(dy)),u,v)]
    # First distributed sum retains separate dx and dy expansions before collection.
    distributed=expression_add([tex(m['dxterm']),tex(m['dyterm'])])
    rows+=[' &='+integral(distributed,u,v),' &='+integral(tex(m['integrand']),u,v)]
    # Componentwise integration keeps endpoint powers and sums unevaluated until
    # the final collection. SymPy equality alone would hide these teaching stages.
    terms=sp.Add.make_args(m['integrand']);Fterms=[sp.integrate(z,T) for z in terms]
    Ftex=expression_add([tex(z) for z in Fterms]);rows+=[' &='+r'\left['+Ftex+r'\right]_{'+str(u)+'}^{'+str(v)+'}']
    def endpoint(z,bound):return re.sub(r'\\[A-Za-z]+|t',lambda mt:grouped(str(bound)) if mt[0]=='t' else mt[0],tex(z))
    evalmask='['+expression_add([endpoint(z,v) for z in Fterms])+']-['+expression_add([endpoint(z,u) for z in Fterms])+']'
    endpoint_sum='['+expression_add([tex(z.subs(T,v)) for z in Fterms])+']-['+expression_add([tex(z.subs(T,u)) for z in Fterms])+']'
    rows+=[' &='+evalmask,' &='+endpoint_sum,' &='+tex(m['value'])]
    prose+='$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    intpart=lambda z:sp.simplify(sp.integrate(z,(T,u,v)))
    bank=[m['value'],intpart(m['dxterm']),intpart(m['dyterm']),-m['value'],intpart(m['dxterm'])-intpart(m['dyterm'])]
    if any(not z.is_real or z.has(sp.Integral,sp.oo,sp.zoo,sp.nan) for z in bank):raise ValueError('Nonfinite bank')
    if any(sp.simplify(a-b)==0 for i,a in enumerate(bank) for b in bank[i+1:]):raise ValueError('Complete operation bank collision')
    return problem,prose,[tex(z) for z in bank],tex(m['value']),[]


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only source math radio')
    rng=random.Random(seed);eligible=[n for n,t in TEMPLATES.items() if t['level']==level]
    if template is None:template=rng.choice(eligible)
    if template not in eligible:raise ValueError('template outside requested level')
    profile=profile or 'authored_method'
    if profile not in ('authored_method','observed_repaired','raw_observed'):raise ValueError('unknown profile')
    observed=profile!='authored_method'
    if observed and template.startswith('easy_'):raise ValueError('No observed easy examples')
    if observed:
        p=parameters if parameters is not None else {'scale':1};guard(template,p,True)
        k=p['scale'];m=math_object(template,BASE[template]);m={**m,'P':k*m['P'],'Q':k*m['Q'],'value':k*m['value']}
        problem,solution,choices,correct,repairs=source_recipe(template,k,profile=='raw_observed')
        # A known duplicate legacy option is evidence-only, not normal practice.
        ambiguity=profile=='raw_observed' and template=='sqrt_linear'
        limits={k:BASE[template][k] for k in ('u','v')}
    else:
        for attempt in range(2000):
            p=dict(parameters) if parameters is not None else samples(template,rng);guard(template,p)
            m=math_object(template,p)
            try:problem,solution,choices,correct,repairs=authored(template,p,m);break
            except ValueError:
                if parameters is not None:raise
        else:raise RuntimeError('whole instance rejection exhausted')
        ambiguity=False;limits={k:p[k] for k in ('u','v')}
    bank_values=[scalar(z) for z in choices]
    if not ambiguity and any(sp.simplify(a-b)==0 for i,a in enumerate(bank_values) for b in bank_values[i+1:]):raise ValueError('Equivalent complete bank options')
    # Actual assessed curve/form/limits, canonical and independent of profiles,
    # parameter aliases, unused options, seeds and answer ordering.
    task=digest({'curve':sp.srepr(m['curve']),'P':sp.srepr(m['P']),'Q':sp.srepr(m['Q']),'limits':[sp.srepr(m['xt'].subs(T,limits[z])) for z in ('u','v')]})
    content=digest({'version':VERSION,'prompt':problem,'solution':solution,'bank':sorted(choices),'correct':correct})
    qid=uid(str(KP_ID)+':question:'+content);fid=uid(qid+':field:selection')
    answers=[{':answer/id':uid(fid+':'+value+':'+str(sum(v==value for v in choices[:i]))),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(choices)]
    cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct);rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':p,'profile':profile,'source_id':TEMPLATES[template]['source_id'],'provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'math_task_fingerprint':task,'content_fingerprint':content,'bank_recipes':['correct','omit dx contribution','omit dy contribution','reverse orientation','reverse dy contribution sign'] if not observed else ['uniform one-form scaling of complete observed expression patterns; original error intent unresolved'],'evidence_only':profile=='raw_observed','repairs':repairs,'domain':'nonnegative parameter; reciprocal paths avoid zero; trig endpoint zero uses composed one-sided extension','plots':'none'}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0];lines=[q[':question/problem'],'']
    lines += [f'{i+1}. $'+a[':answer/value']+'$' for i,a in enumerate(f[':answer-field/choices'])]
    return '\n'.join(lines)+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
