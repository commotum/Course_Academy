#!/usr/bin/env python3
"""Exact circle/ellipse one-form generators; local records, no database writes.
Source-specific replay is a linear multiplier template, never a literal-return
branch. Unexplained complete observed banks remain explicit replay profiles.
Defaults are labeled authored banks with same-method coefficient/axis variety.
See evidence folder for source mapping, scope and independent native checks.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as S
KP_ID=17592186179673
KP_UUID='e5b5c517-8e13-5b70-bd1f-15ae495f0632'
TITLE='Computing Line Integrals With Respect to X and Y Along Circles and Ellipses'
VERSION='circle-ellipse-one-form-v1'
EVIDENCE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((EVIDENCE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
x,y,t=S.symbols('x y t',real=True)
D={
'q-124597':(1,1,0,1,y**2,-x**2),
'q-81192':(1,1,0,1,-x/(x*x+y*y),y/(x*x+y*y)),
'q-124656':(2,2,0,2,x*x*y,x),
'q-124657':(1,2,0,1,2/y,y*S.exp(x)),
'q-124661':(2,3,1,2,x-y,x+y),
'q-124665':(1,3,2,3,S.Integer(1),2/x),
'q-124651':(2,1,0,1,x*x,x*y),
'q-124653':(S.sqrt(3),S.sqrt(3),1,2,S.exp(x)+y,-x),
'q-124655':(1,3,1,3,x-2*y,2*x),
'q-81186':(2,2,2,3,y,x),
'q-90895':(S.sqrt(2),S.sqrt(2),0,1,y,-x)}

def tex(e):return S.latex(S.sympify(e),ln_notation=True)
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def scale_tex(s,c):
    # A complete mathematical component, never a blind short-token replacement.
    return ('' if c==1 else tex(c)+r'\left(')+s+('' if c==1 else r'\right)')
def source_parts(q):
    # Extract last aligned environment into ordered arithmetic masks.
    sol=q[':question/worked-solution']; pos=sol.rfind(r'\begin{aligned}')
    end=sol.index(r'\end{aligned}',pos)
    body=sol[pos+len(r'\begin{aligned}'):end]
    rows=body.split(r'\\  & =')
    lhs,rhs=rows[0].split(' & =',1)
    return sol[:pos],sol[end:],lhs,[rhs]+rows[1:]

def source_template(q,c):
    prompt=q[':question/problem']; start=prompt.index('$')+1; end=prompt.index('$',start)
    math=prompt[start:end]; trailing=',' if math.endswith(',') else ''
    core=math[:-1] if trailing else math
    prompt=prompt[:start]+scale_tex(core,c)+trailing+prompt[end:]
    prefix,suffix,lhs,rows=source_parts(q)
    sol=prefix+r'\begin{aligned}'+scale_tex(lhs,c)+' & ='+r'\\  & ='.join(scale_tex(z,c) for z in rows)+suffix
    # The original expression is a replay recipe with scalar linearity, not a
    # claim that the source author's numerical error mechanism was recovered.
    f=q[':question/answer-fields'][0]
    vals=[scale_tex(a[':answer/value'],c) for a in f[':answer-field/choices']]
    ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
    return prompt,sol,vals,ci

def endpoint_raw(F,v):
    return re.sub(r'\bt\b',lambda _:r'\left('+tex(v)+r'\right)',tex(F))
def endpoint_terms(F,v):
    terms=[tex(z.subs(t,v)) for z in S.Add.make_args(F)]
    return '+'.join(r'\left('+z+r'\right)' for z in terms)
def integral_tex(e,lo,hi):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\left('+tex(e)+r'\right)\,\mathrm{d}t'
def oneform_tex(P,Q):return r'\int_C\left('+tex(P)+r'\right)\,\mathrm{d}x+\left('+tex(Q)+r'\right)\,\mathrm{d}y'
def values(level,p):
    a,b,m,n,h,j,k=[S.Integer(p[z]) for z in ['a','b','m','n','h','j','k']]
    X=a*S.cos(t);Y=b*S.sin(t);lo=j*S.pi/2;hi=k*S.pi/2
    if level=='easy':P=m*x*x;Q=n*x*y
    elif level=='moderate':P=m*x-n*y;Q=n*x+h*y
    else:P=m*x*x*y-n*y;Q=n*x+h*x*y*y
    f=S.expand(P.subs({x:X,y:Y})*S.diff(X,t)+Q.subs({x:X,y:Y})*S.diff(Y,t))
    F=(n*a*b*t+a*b*(h*b*b-m*a*a)*(t/S.Integer(8)-S.sin(4*t)/32)) if level=='hard' else S.integrate(f,t);ans=S.simplify(F.subs(t,hi)-F.subs(t,lo))
    return P,Q,X,Y,lo,hi,f,F,ans

def authored(level,p):
    P,Q,X,Y,lo,hi,f,F,ans=values(level,p)
    a,b,m,n,h=[S.Integer(p[z]) for z in ['a','b','m','n','h']]
    # Complete preselected operation bank: omit dx, omit dy, reverse dx,
    # substitute coordinate values for both tangent derivatives.
    fx=S.expand(P.subs({x:X,y:Y})*S.diff(X,t));fy=S.expand(Q.subs({x:X,y:Y})*S.diff(Y,t))
    fs=[f,fy,fx,-fx+fy,S.expand(P.subs({x:X,y:Y})*X+Q.subs({x:X,y:Y})*Y)]
    bank=fs if level=='easy' else [S.simplify(S.integrate(z,(t,lo,hi))) for z in fs]
    if any(S.simplify(bank[i]-bank[j])==0 for i in range(5) for j in range(i)):raise ValueError('entire bank rejected: equivalent choices')
    if level=='easy':
        scalars=[S.simplify(S.integrate(z,(t,lo,hi))) for z in fs]
        if any(S.simplify(scalars[i]-scalars[j])==0 for i in range(5) for j in range(i)):raise ValueError('entire bank rejected: coincident scalar integral values')
    vals=[integral_tex(z,lo,hi) for z in bank] if level=='easy' else [tex(z) for z in bank]
    endpoints=[(S.simplify(X.subs(t,v)),S.simplify(Y.subs(t,v))) for v in [lo,hi]]
    curve=tex(b*b*x*x+a*a*y*y)+'='+tex(a*a*b*b)
    question=('Which of the following is equivalent to ' if level=='easy' else 'Evaluate ')+ '$'+oneform_tex(P,Q)+r',$ where $C$ is part of the '+('circle' if a==b else 'ellipse')+' $'+curve+'$ traversed in the counterclockwise direction from the point $('+','.join(tex(z) for z in endpoints[0])+')$ to the point $('+','.join(tex(z) for z in endpoints[1])+')$.'
    sub=r'\left('+tex(P.subs({x:X,y:Y}))+r'\right)\left('+tex(S.diff(X,t))+r'\right)+\left('+tex(Q.subs({x:X,y:Y}))+r'\right)\left('+tex(S.diff(Y,t))+r'\right)'
    integral_head=r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'
    first=integral_head+r'\left('+tex(P)+r'\right)x\prime(t)\,\mathrm{d}t+\left('+tex(Q)+r'\right)y\prime(t)\,\mathrm{d}t'
    generic=integral_head+r'\left(\left('+tex(P)+r'\right)x\prime(t)+\left('+tex(Q)+r'\right)y\prime(t)\right)\,\mathrm{d}t'
    s,c=S.sin(t),S.cos(t)
    if level=='easy':components=[-m*a**3*s*c**2,n*a*b**2*s*c**2];collected=f
    elif level=='moderate':components=[-m*a*a*s*c,n*a*b*s*s,n*a*b*c*c,h*b*b*s*c];collected=n*a*b+(h*b*b-m*a*a)*s*c
    else:components=[-m*a**3*b*s*s*c*c,n*a*b*s*s,n*a*b*c*c,h*a*b**3*s*s*c*c];collected=n*a*b+a*b*(h*b*b-m*a*a)*s*s*c*c
    distributed='+'.join(r'\left('+tex(term)+r'\right)' for term in components)
    rows=[first,generic,integral_head+r'\left('+sub+r'\right)\,\mathrm{d}t',integral_head+r'\left('+distributed+r'\right)\,\mathrm{d}t',integral_tex(collected,lo,hi)]
    if level=='moderate':rows.append(integral_tex(n*a*b+(h*b*b-m*a*a)*S.sin(2*t)/2,lo,hi))
    if level=='hard':
        A=a*b*(h*b*b-m*a*a);C=n*a*b
        rows.append(integral_tex(C+A*(1-S.cos(4*t))/8,lo,hi))
    if level!='easy':rows.extend([r'\left['+tex(F)+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}',r'\left('+endpoint_raw(F,hi)+r'\right)-\left('+endpoint_raw(F,lo)+r'\right)',r'\left('+endpoint_terms(F,hi)+r'\right)-\left('+endpoint_terms(F,lo)+r'\right)',tex(ans)])
    opening=('Since $C$ is a circle of radius $'+tex(a)+'$ centered at the origin, it can be parametrized as follows:' if a==b else 'Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $'+tex(a)+'$ and $'+tex(b)+',$ respectively, it can be parametrized as follows:')
    sol=opening+'\n\n$$r(t)='+tex(X)+r'\,i+'+tex(Y)+r'\,j,\quad t\in['+tex(lo)+','+tex(hi)+'].$$\n\nThe derivative of $r(t)$ is given by\n\n$$r\\prime(t)='+tex(S.diff(X,t))+r'\,i+'+tex(S.diff(Y,t))+r'\,j.$$'+'\n\n'+('Therefore, we can write our line integral as follows:' if level=='easy' else 'We can now evaluate the line integral:')+'\n\n$$\n'+r'\begin{aligned}'+oneform_tex(P,Q)+' & ='+r'\\ & ='.join(rows)+r'\end{aligned}'+'\n$$'
    return question,sol,vals,0

def parameters_for(level,rng):
    lim=3 if level=='easy' else 4
    return dict(a=rng.randint(1,4),b=rng.randint(1,4),m=rng.choice([-lim,-2,-1,1,2,lim]),n=rng.choice([-lim,-2,-1,1,2,lim]),h=rng.choice([-3,-2,-1,1,2,3]),j=rng.randint(0,3),k=0)

def guard(level,p):
    if set(p)!=set(['a','b','m','n','h','j','k']):raise ValueError('explicit authored parameter keys required')
    if any(type(v)!=int for v in p.values()):raise ValueError('integer parameters required')
    lim=3 if level=='easy' else 4
    if not(1<=p['a']<=4 and 1<=p['b']<=4 and 1<=abs(p['m'])<=lim and 1<=abs(p['n'])<=lim and 1<=abs(p['h'])<=3 and 0<=p['j']<=3 and 1<=p['k']-p['j']<=2):raise ValueError('outside documented workload bounds')
    if level=='hard' and (p['a']==p['b'] or p['h']*p['b']**2==p['m']*p['a']**2):raise ValueError('hard requires unequal axes and noncanceling quartic products')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
    rng=random.Random(seed); template=template or 'authored_'+level
    if template in SOURCES:
        q=SOURCES[template]; actual=q[':question/difficulty'][':db/ident'].split('/')[-1]
        eligible=[None,'observed_'+template]+(['repaired_'+template] if template=='q-124656' else [])
        if actual!=level or profile not in eligible:raise ValueError('ineligible source template/profile')
        p=parameters if parameters is not None else {'c':rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])}
        if set(p)!={'c'} or type(p['c'])!=int or not 1<=abs(p['c'])<=5:raise ValueError('nonzero integer multiplier |c| <= 5 required')
        profile=profile or ('repaired_'+template if template=='q-124656' else 'observed_'+template)
        prompt,sol,vals,ci=source_template(q,p['c'])
        if profile=='repaired_q-124656':
            vals[3]=scale_tex(r'4{\int }_{0}^{\pi }{cos}^{2}⁡t\,\text{d}t',p['c'])
        a,b,j,k,P,Q=D[template];X=a*S.cos(t);Y=b*S.sin(t)
        task={'P':str(p['c']*P),'Q':str(p['c']*Q),'axes':[str(a),str(b)],'assessment':'setup' if level=='easy' else 'value'}
        task['angles']=[j,k]
        sources=[template]; domain={'angle_pi_over_2':[j,k],'endpoint_interpretation':'one-sided improper; continuous composed extension' if template in ['q-124657','q-124665'] else 'ordinary regular integral','interior_poles':'forbidden'}
    else:
        if template!='authored_'+level or profile not in [None,'authored_operations']:raise ValueError('unknown/ineligible template/profile')
        profile='authored_operations';sources=[]
        if parameters is not None:p=dict(parameters);guard(level,p);prompt,sol,vals,ci=authored(level,p)
        else:
            for _ in range(500):
                p=parameters_for(level,rng);p['k']=p['j']+rng.randint(1,2)
                try:guard(level,p);prompt,sol,vals,ci=authored(level,p);break
                except ValueError:continue
            else:raise ValueError('no eligible complete bank')
        P,Q,*_=values(level,p)
        task={'P':str(P),'Q':str(Q),'axes':[str(p['a']),str(p['b'])],'assessment':'setup' if level=='easy' else 'value'}
        task['angles']=[p['j'],p['k']]
        domain={'angle_pi_over_2':[p['j'],p['k']],'endpoint_interpretation':'ordinary regular integral','interior_poles':'forbidden'}
    content=digest({'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(vals),'correct':vals[ci],'assessed_task':task,'domain':domain})
    qid=uid(content);fid=uid(content+'/selection')
    answers=[{':answer/id':uid(content+'/selection/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    correct=answers[ci][':answer/id'];random.Random(seed).shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source_ids':sources,'source_snapshot':{k:SNAPSHOT[k] for k in ['database','basis','lineage']},'domain':domain,'mathematical_fingerprint':digest(task),'content_fingerprint':content,'authored':not sources,'source_bank_repair':('q-124656 wrong sine-squared zero-valued integral replaced by omit-dx integral 4 int cos² t, value 2pi' if profile=='repaired_q-124656' else None),'raw_ambiguous_bank':profile=='observed_q-124656','dependencies':{'sympy':S.__version__}}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 out=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(out,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
