#!/usr/bin/env python3
"""Seeded exponential-forcing general-solution generator. See instructional-account.md."""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID=17592186229164
KP_UUID='af1f1fb7-3e26-5624-ac07-0be869d2bd5e'
TITLE='Finding the General Solution to a First-Order Inhomogeneous ODE With Exponential Forcing'
VERSION='exponential-general-2'
ROOT=Path(__file__).resolve().parent/'data'
LAYOUTS=json.loads((ROOT/'layouts.json').read_text())
CASES=json.loads((ROOT/'source-cases.json').read_text())
SOURCE={'database':'math','basis':8752,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING='To find the general solution of an inhomogeneous first-order linear equation with constant coefficients on the left-hand side, we must find the sum of the complementary and particular solutions.'
TEMPLATES={'nonresonant':'easy','resonant':'moderate','mixed':'hard'}
X=sp.Symbol('x',real=True)
A,ALPHA,BETA=sp.symbols('A alpha beta',real=True)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def number(v):return sp.latex(sp.Rational(v))
def multiply(c,s):
    c=sp.Rational(c)
    return ('-' if c==-1 else '' if c==1 else number(c))+s

def signed(c,s):return ('+' if c>0 else '-')+multiply(abs(c),s)
def exponential(k):return '{e}^{'+multiply(k,'x')+'}'
def polyfactor(a):return '1'+signed(a,'x')
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def display(s):return '$$\n'+s+'\n$$'

def components(p,template,layout):
    a,k,b=p['a'],p['k'],p['b']; e=exponential(k); ea=exponential(a); resonant=template=='resonant'
    ode='{y}^{\\prime}'+signed(-a,'y')+'='+multiply(b,e)
    homogeneous='{y}_{c}^{\\prime}'+signed(-a,'{y}_{c}')+'=0'
    complement='{y}_{c}(x)=A'+ea
    complement_solution='{y}_{c}=A'+ea
    trial=r'\alpha '+('x' if resonant else '')+e
    coeff=sp.Integer(b) if resonant else sp.Rational(b,k-a)
    particular=multiply(coeff,('x' if resonant else '')+e)
    final='A'+ea+signed(coeff,('x' if resonant else '')+e)
    if resonant:
        derivative=aligned(['{y}_{p}^{\\prime} & =('+trial+')^{\\prime}',r' & =\alpha (x'+e+')^{\\prime}',r' & =\alpha ('+e+signed(k,'x'+e)+')',r' & =\alpha ('+polyfactor(k)+')'+e+('.' if layout['solution_enddot'] else '')])
        substitution=aligned(['('+r'\alpha ('+polyfactor(k)+')'+e+')'+signed(-a,r'\alpha x'+e)+' & ='+multiply(b,e),'(1'+signed(k,'x')+signed(-a,'x')+')'+r'\alpha '+e+' & ='+multiply(b,e),r'\alpha '+e+' & ='+multiply(b,e),r'\alpha  & ='+number(coeff)+('.' if layout['solution_enddot'] else '')])
    else:
        d=multiply(k,r'\alpha '+e)
        derivative='{y}_{p}^{\\prime}='+((r'\alpha '+e+r'\cdot '+str(k)+'=') if layout['derivative_chain'] else '')+d+'.'
        if layout['derivative_aligned']:derivative=aligned([derivative])
        else:derivative=derivative.rstrip('.')
        substitution=aligned([d+signed(-a,r'\alpha '+e)+' & ='+multiply(b,e),multiply(k-a,r'\alpha '+e)+' & ='+multiply(b,e),r'\alpha  & ='+number(coeff)+('.' if layout['solution_enddot'] else '')])
    return dict(ode=ode,homogeneous=homogeneous,complement=complement,complement_solution=complement_solution,forcing_inline=multiply(b,e),forcing_exponential=e,trial='{y}_{p}='+trial,derivative=derivative,substitution=substitution,particular='{y}_{p}(x)='+particular,final='y='+final), final

def fill(mask,slots):
    for key,v in slots.items():mask=mask.replace('@@'+key+'@@',v)
    if '@@' in mask:raise AssertionError('unfilled template')
    return mask

def single(p,template,key,raw):
    layout=LAYOUTS[key]; slots,answer=components(p,template,layout)
    problem=fill(layout['prompt'],slots)
    solution=fill(layout['solution'],slots)
    aliases=[answer]
    correct=0
    if key=='q-333168':
        aliases.append('('+multiply(p['b'],'x')+'+A)e^{'+multiply(p['a'],'x')+'}')
        correct=1
        solution=solution.replace('y='+answer+'.', 'y='+answer+'='+aliases[1]+'.')
        solution=solution.replace('the general solution in our case is', 'factoring the common exponential, the general solution in our case is')
    return problem,solution,aliases,correct

def mixed(p):
    """Authored hard: two nonzero components and exactly one resonance."""
    a,k,b,c=(p[t] for t in ('a','k','b','c'));ea=exponential(a);ek=exponential(k);q=sp.Rational(c,k-a)
    reverse=p.get('reverse',False)
    forcing=(multiply(c,ek)+signed(b,ea)) if reverse else (multiply(b,ea)+signed(c,ek))
    trial=r'\alpha x'+ea+r'+\beta '+ek
    d=r'\alpha ('+polyfactor(a)+')'+ea+signed(k,r'\beta '+ek)
    final='A'+ea+signed(b,'x'+ea)+signed(q,ek)
    particular=multiply(b,'x'+ea)+signed(q,ek)
    problem='Consider the differential equation \n\n'+display('{y}^{\\prime}'+signed(-a,'y')+'='+forcing+'.')+'\n\nFind the general solution to this equation given that the complementary solution is ${y}_{c}(x)=A'+ea+',$ where $A$ is an arbitrary constant.\n\n$y(x)=$\n{{field-1}}'
    parts=[OPENING,'To find the complementary solution ${y}_{c},$ we solve the corresponding homogeneous equation, given by',display('{y}_{c}^{\\prime}'+signed(-a,'{y}_{c}')+'=0.'),'Solving this equation, we find that the complementary solution is',display('{y}_{c}=A'+ea+'.'),'where $A$ is an arbitrary constant.','We now need to find the particular solution ${y}_{p}(x).$','We see that the right-hand side is $'+forcing+',$ and $'+ea+'$ is a term in the complementary solution, while $'+ek+'$ is not, so we assume that a particular solution takes the form',display('{y}_{p}='+trial+','),r'where $\alpha$ and $\beta$ are constants that are to be determined.','Calculating the first derivative of ${y}_{p}$ gives',display(aligned(['{y}_{p}^{\\prime} & =('+trial+')^{\\prime}',r' & =\alpha (x'+ea+r')^{\prime}+\beta ('+ek+')^{\\prime}',r' & =\alpha ('+ea+signed(a,'x'+ea)+')'+signed(k,r'\beta '+ek),' & ='+d+'.'])),'To find the values of $'+r'\alpha$ and $\beta'+',$ we substitute ${y}_{p}$ and ${y}_{p}^{\\prime}$ into the differential equation:',display(aligned(['('+r'\alpha x'+ea+r')^{\prime}'+signed(-a,r'\alpha x'+ea)+r' & =\alpha '+ea,'('+r'\beta '+ek+r')^{\prime}'+signed(-a,r'\beta '+ek)+' & ='+multiply(k-a,r'\beta '+ek),r'{y}_{p}^{\prime}'+signed(-a,'{y}_{p}')+r' & =\alpha '+ea+signed(k-a,r'\beta '+ek)+'.'])),'The sum must equal the forcing in the question. Equating coefficients of $'+ea+'$ and $'+ek+'$ gives',display(r'\alpha = '+str(b)+r' \quad \text{and} \quad '+multiply(k-a,r'\beta')+'='+str(c)+','),'so, we have',display(r'\alpha = '+str(b)+r' \quad \text{and} \quad \beta = '+number(q)+'.'),'Therefore, the particular solution ${y}_{p}(x)$ is',display('{y}_{p}(x)='+particular+'.'),'Now, since the general solution is given by',display('y(x)={y}_{c}(x)+{y}_{p}(x),'),'the general solution in our case is',display('y='+final+'.')]
    return problem,'\n\n'.join(parts),[final],0

def check_parameters(level,template,p):
    if set(p)!=({'a','k','b','c'} if level=='hard' else {'a','k','b'}):raise ValueError('exact parameter keys required')
    if any(type(v)!=int or not v for v in p.values()):raise ValueError('nonzero integers required')
    if abs(p['a'])>8 or abs(p['k'])>8:raise ValueError('exponent bounds')
    if level=='easy':
        if template!='nonresonant' or p['a']==p['k'] or abs(p['b'])>72 or abs(sp.Rational(p['b'],p['k']-p['a']))>8:raise ValueError('easy workload bounds')
    if level=='moderate':
        if template!='resonant' or p['a']!=p['k'] or abs(p['b'])>12:raise ValueError('moderate workload bounds')
    if level=='hard':
        if template!='mixed' or p['a']==p['k'] or abs(p['a'])>6 or abs(p['k'])>6 or abs(p['b'])>18 or abs(p['c'])>36 or sp.Rational(p['c'],p['k']-p['a']).q>6 or abs(sp.Rational(p['c'],p['k']-p['a']))>8:raise ValueError('hard workload bounds')

def sample(level,rng):
    values=[-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]
    a=rng.choice(values)
    k=a if level=='moderate' else rng.choice([v for v in values if v!=a])
    coefficient=rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])
    p=dict(a=a,k=k,b=coefficient if level!='easy' else coefficient*(k-a))
    if level=='hard':
        p['c']=rng.choice([-3,-2,-1,1,2,3])*(k-a)
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
    if field_type not in (None,'blank',':answer-field.type/blank'):raise ValueError('blank only')
    template=template or next(t for t,l in TEMPLATES.items() if l==level)
    if TEMPLATES.get(template)!=level:raise ValueError('template/level mismatch')
    rng=random.Random(seed);raw=False;key=None
    if profile is not None:
        if ':' not in profile:raise ValueError('profile prefix required')
        mode,key=profile.split(':',1)
        if mode not in ('raw','observed') or key not in LAYOUTS:raise ValueError('unknown profile')
        case=next(c for c in CASES if c['source_id']==key)
        if case['template']!=template or case['level']!=level:raise ValueError('profile template/level mismatch')
        raw=False
    if parameters is not None:p=dict(parameters);check_parameters(level,template,p)
    else:
        for _ in range(1000):
            p=sample(level,rng)
            try:check_parameters(level,template,p);break
            except ValueError:continue
        else:raise RuntimeError('sampler exhausted')
    if key is None:key='q-332801' if level=='easy' else 'q-332895'
    if level=='hard':
        presentation=dict(p,reverse=bool(seed % 2))
        problem,solution,answers,correct=mixed(presentation)
    else:problem,solution,answers,correct=single(p,template,key,raw)
    if not raw:
        clarification='Write the arbitrary constant term as $A'+exponential(p['a'])+'$.\n\n'
        before,after=problem.split('$y(x)',1)
        problem=before.rstrip()+'\n\n'+clarification+'$y(x)'+after
    problem=normalize_prose(problem)
    solution=normalize_prose(solution)
    # Explicit primes are part of the rendered derivative, never Unicode glyphs.
    answers=list(dict.fromkeys(normalize_tex(v) for v in answers))
    correct=min(correct,len(answers)-1)
    profile=profile or 'authored-default' if level=='hard' else profile or 'observed:'+key
    # Mathematical identity excludes aliases/profile/seed; all a,k,b,c alter the ODE.
    task=digest({'ode':{'a':p['a'],'forcing':sorted([(p['a'],p['b']),(p['k'],p['c'])]) if level=='hard' else [(p['k'],p['b'])]},'response':'complete arbitrary-constant family'})
    identity=digest({'version':VERSION,'prompt':problem,'solution':solution,'bank':sorted((v,i==correct) for i,v in enumerate(answers)),'field_type':'blank'})
    qid=uid('question:'+identity);fid=uid(qid+':field-1')
    bank=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in answers]
    field={':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank'}
    if answers:field.update({':answer-field/choices':bank,':answer-field/correct':[':answer/id',bank[correct][':answer/id']]})
    question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    return validate_generated_record({'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'level':level,'template':template,'bank_profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':task,'content_hash':identity,'source_analysis':SOURCE,'source_refs':['1ea06d66-de30-514a-817f-8749abb4ab25','39f45926-cbe8-53b9-99f5-41f4f4bb9db2'] if level=='hard' else [next(c['question_id'] for c in CASES if c['source_id']==key)],'authored_extension':level=='hard','source_repair':False,'notation_normalized':True,'answer_form_clarified':not raw,'domain':'x in R; A arbitrary real constant','answer_shape':'complete RHS general solution','plot_rating':'none','plot_assets':{},'sympy_version':sp.__version__}})

# Easy: one exponential distinct from the complementary exponent.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: one matching exponential, requiring x in the trial and product rule.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: two-term additive forcing, one matching exponent; same lesson method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\nAnswer: '+next((a[':answer/value'] for a in f.get(':answer-field/choices',[]) if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),'[missing captured answer]')+'\n\n'+q.get(':question/worked-solution','[missing captured solution]')

def batch(level,count,seed,profile=None):
    if count < 0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed)
    records=[]; seen=set(); recent=[]
    for i in range(count):
        for attempt in range(20000):
            item_seed=rng.getrandbits(64)
            r=generate(level,item_seed,profile=profile)
            p=r['generation']['parameters']
            identity=r['generation']['mathematical_fingerprint']
            pair=(p['a'],p['k'])
            # Spread the exponents that change the learner's actual calculation.
            # Recent window is bounded so large batches retain the finite family.
            if identity in seen or pair in recent: continue
            seen.add(identity);recent.append(pair)
            recent=recent[-(min(10, count-1)): ] if count>1 else []
            records.append(r);break
        else: raise ValueError('requested count exhausts the supported family')
    return records

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='easy')
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=['markdown','json'],default='json')
    ap.add_argument('--profile')
    args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else ['easy' if args.difficulty=='unclassified' else args.difficulty]
    records=[r for level in levels for r in batch(level,args.count,args.seed,args.profile)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
