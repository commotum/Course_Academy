#!/usr/bin/env python3
"""Exact two-dimensional component arithmetic, angle bracket responses only.

Frozen evidence: math basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Raw public profiles retain individually absent difficulty, fields, correct refs,
and solution attributes. Normal records complete these source-format omissions
with explicitly inferred radio fields/answers or authored solution stages.
No database writes. No plots occur in the assigned practice/canonical examples.

Profiles are complete operation banks selected BEFORE sampling parameters; an
ambiguous instance is rejected wholesale. Both recovered banks have defensible
componentwise operations, although the original error intent is not recoverable.
Easy defaults sample every observed single-operation family (sum, subtraction,
scalar multiplication). Moderate is a single scaled vector plus another, anchored
to q17611/canonical e4293. Hard scales BOTH supplied vectors before combining,
an authored extra bookkeeping demand within the same componentwise method.
See the private classification/extraction for number bounds and source omissions.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059711
KP_UUID='1735c445-9c97-5aa7-83d6-7dee23993153'
TITLE='Calculating Sums and Scalar Multiplication of Vectors Using Angle Bracket Notation'
VERSION='angle-vector-1.0'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'sum':'easy','subtract':'easy','scalar':'easy','linear':'moderate','double_scaled':'hard'}
PROFILES={'sum_method':'sum','subtract_observed':'subtract','scalar_method':'scalar',
          'linear_observed':'linear','hard_method':'double_scaled',
          'raw_q1304':'subtract','raw_q17611':'linear','raw_q1301':'sum','raw_q1389':'scalar'}
RAW={'raw_q1304':{'source_id':'q-1304','difficulty':False,'fields':True,'solution':False},
     'raw_q17611':{'source_id':'q-17611','difficulty':False,'fields':True,'solution':False},
     'raw_q1301':{'source_id':'q-1301','difficulty':True,'fields':False,'solution':True},
     'raw_q1389':{'source_id':'q-1389','difficulty':True,'fields':False,'solution':True}}
DEFAULT_PROFILE={'sum':'sum_method','subtract':'subtract_observed','scalar':'scalar_method','linear':'linear_observed','double_scaled':'hard_method'}
SOURCE_IDS={'sum':['q-1301'],'subtract':['q-1304'],'scalar':['q-1389'],'linear':['q-17611','e-4293'],'double_scaled':['e-4293','sibling-e-4294']}
OPENING='we just need to perform the required operations with each component separately:'
class SampleRejected(ValueError): pass

def exact(x):
    if isinstance(x,bool) or isinstance(x,float): raise ValueError('Use exact integers or rational strings')
    y=sp.Rational(x)
    return y

def tex(x): return sp.latex(exact(x))
def group(x): return '('+tex(x)+')' if x<0 else tex(x)
def vec(v,style='compact'):
    a,b=map(tex,v)
    if style=='source_minus':
        a=(' - '+tex(-v[0])) if v[0]<0 else a
        return '⟨'+a+', '+b+'⟩'
    if style=='source_sub_bank':
        a=(' - '+tex(-v[0])) if v[0]<0 else a
        return '⟨'+a+', '+b+'⟩'
    if style=='source_linear_bank': return '⟨'+a+(',' if v[1]<0 else ', ')+b+'⟩'
    return '⟨'+a+','+b+'⟩'
def scaled(k,v): return tuple(k*x for x in v)
def add(a,b): return tuple(x+y for x,y in zip(a,b,strict=True))
def expr(k,name):
    return ('+ ' if k>0 else '- ')+('' if abs(k)==1 else tex(abs(k)))+name

def normalize_parameters(template,p,raw=False):
    expected={'scalar':{'a','k'},'double_scaled':{'a','b','r','k'}}.get(template,{'a','b','k'} if template=='linear' else {'a','b'})
    if set(p)!=expected: raise ValueError(f'{template} requires exactly {sorted(expected)}')
    out={}
    for key,val in p.items():
        if key in ('a','b'):
            if not isinstance(val,(list,tuple)) or len(val)!=2: raise ValueError('Vectors must have exactly two components')
            out[key]=tuple(exact(x) for x in val)
        else: out[key]=exact(val)
    cap=8 if template=='double_scaled' else 15
    for key in ('a','b'):
        if key not in out: continue
        for i,x in enumerate(out[key]):
            if x==0 or abs(x)>cap: raise ValueError(f'Nonzero component magnitude must be <= {cap}')
            if template=='scalar' and key=='a' and i==1:
                if x.q!=2: raise ValueError('Scalar template retains a noninteger half as its second component')
            elif x.q!=1: raise ValueError('This template requires integer components')
    for key in ('k','r'):
        if key not in out:continue
        upper=4 if template=='double_scaled' else 5
        if out[key].q!=1 or not 2<=abs(out[key])<=upper: raise ValueError(f'{key} requires signed integer magnitude 2..{upper}')
    return out

def sample(template,rng):
    cap=8 if template=='double_scaled' else 15
    domain=[i for i in range(-cap,cap+1) if i]
    p={'a':[rng.choice(domain),rng.choice(domain)]}
    if template=='scalar':
        p['a'][1]=str(sp.Rational(rng.choice([i for i in range(-29,30,2) if i]),2))
        p['k']=rng.choice([-5,-4,-3,-2,2,3,4,5])
    else:
        p['b']=[rng.choice(domain),rng.choice(domain)]
        if template in ('linear','double_scaled'):p['k']=rng.choice([-4,-3,-2,2,3,4] if template=='double_scaled' else [-5,-4,-3,-2,2,3,4,5])
        if template=='double_scaled':p['r']=rng.choice([-4,-3,-2,2,3,4])
    return normalize_parameters(template,p)

def build(template,p):
    """Return displayed prompt and ordered, unevaluated teaching stages."""
    a=p['a']; b=p.get('b'); k=p.get('k');r=p.get('r')
    A=r'\overset{\to }{A}';B=r'\overset{\to }{B}'
    if template=='sum':
        target=A+'+'+B
        prompt=f'What is the sum of ${A}={vec(a)}$ and ${B}={vec(b)}?$'
        c=add(a,b)
        solution=f'To compute ${target},$ '+OPENING+'\n\n$$\n'+r'\begin{aligned}'+target+' & ='+vec(a)+'+'+vec(b)+r' \\  & ='+vec(c)+r'\end{aligned}'+'\n$$'
    elif template=='scalar':
        target=tex(k)+A; c=scaled(k,a)
        prompt=f'If ${A}={vec(a)}$, then ${target}=$'
        component='⟨'+group(k)+r'\cdot '+group(a[0])+','+group(k)+r'\cdot '+group(a[1])+'⟩'
        solution=f'To compute ${target},$ '+OPENING+'\n\n$$\n'+r'\begin{aligned}'+target+' & ='+tex(k)+r'\cdot '+vec(a)+r' \\  & ='+component+r' \\  & ='+vec(c)+r'\end{aligned}'+'\n$$'
    else:
        if template=='subtract':
            target='u - v';c=add(a,scaled(-1,b));pcoef,qcoef=sp.Integer(1),sp.Integer(-1)
            prompt=f'If $u = {vec(a,"source_minus")}$ and $v = {vec(b)}$, then $u - v =$'
        elif template=='linear':
            target='a '+expr(k,'b');c=add(a,scaled(k,b));pcoef,qcoef=sp.Integer(1),k
            prompt=f'Let $a = {vec(a,"source_minus")}$ and $b = {vec(b)}$. Find ${target}$.'
        else:
            target=tex(r)+'a '+expr(k,'b');c=add(scaled(r,a),scaled(k,b));pcoef,qcoef=r,k
            prompt=f'Let $a = {vec(a)}$ and $b = {vec(b)}$. Find ${target}$.'
        sa,sb=scaled(pcoef,a),scaled(qcoef,b)
        initial=(vec(a) if pcoef==1 else group(pcoef)+r'\cdot '+vec(a))+' '+('+' if qcoef>0 else '-')+' '+(vec(b) if abs(qcoef)==1 else tex(abs(qcoef))+r'\cdot '+vec(b))
        # Explicit evaluated scaled vector, followed by independent signed component additions.
        evaluated=vec(sa)+' '+('+' if qcoef>0 else '-')+' '+vec(scaled(abs(qcoef),b))
        component='⟨'+tex(sa[0])+(' + ' if qcoef>0 else ' - ')+group(abs(qcoef)*b[0])+', '+tex(sa[1])+(' + ' if qcoef>0 else ' - ')+group(abs(qcoef)*b[1])+'⟩'
        rows=[target+' &= '+initial]
        if template!='subtract':rows+=['&= '+evaluated]
        rows+=['&= '+component,'&= '+vec(c)]
        solution=f'To compute ${target}$, '+OPENING+'\n\n$$\n'+r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(rows)+'\n'+r'\end{aligned}'+'\n$$'
    return prompt,solution,c

def bank(template,p,c):
    """The five values form ONE selected complete operation bank, never a pool."""
    a=p['a'];b=p.get('b');k=p.get('k');r=p.get('r')
    if template=='subtract':
        values=[c,(a[0]-b[0],a[1]+b[1]),(-(a[0]-b[0]),a[1]-b[1]),(a[0]+b[0],a[1]-b[1]),add(a,b)]
        recipes=['correct','add_second_component','reverse_first_subtraction','add_first_component','add_both_components']
        style='source_sub_bank'
    elif template=='linear':
        values=[c,(-a[0]+k*b[0],c[1]),(-a[0]+k*b[0],-a[1]+k*b[1]),(c[0],-a[1]+k*b[1]),(c[0],-c[1])]
        recipes=['correct','negate_first_a_component','negate_both_a_components','negate_second_a_component','reverse_final_second_sign']
        style='source_linear_bank'
    elif template=='sum':
        values=[c,(a[0]-b[0],c[1]),(c[0],a[1]-b[1]),add(a,scaled(-1,b)),(c[1],c[0])]
        recipes=['correct','subtract_first_component','subtract_second_component','subtract_both_components','exchange_components'];style='compact'
    elif template=='scalar':
        values=[c,(k*a[0],a[1]),(a[0],k*a[1]),scaled(-k,a),(a[0]+k,a[1]+k)]
        recipes=['correct','scale_first_only','scale_second_only','reverse_scalar_sign','add_scalar_to_components'];style='compact'
    else:
        values=[c,add(a,scaled(k,b)),add(scaled(r,a),b),add(scaled(r,a),scaled(-k,b)),(r*a[0]+k*b[1],r*a[1]+k*b[0])]
        recipes=['correct','omit_a_scaling','omit_b_scaling','reverse_b_scalar_sign','exchange_b_components'];style='compact'
    if len(set(values))!=5:raise SampleRejected('Complete bank collision; whole instance rejected')
    return [(recipe,value,vec(value,style)) for recipe,value in zip(recipes,values,strict=True)]

def canonical(p):return {k:[str(x) for x in v] if isinstance(v,tuple) else str(v) for k,v in p.items()}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def mathematical_fingerprint(template,p):
    # Canonical assessed component products, excluding common coefficient/vector
    # scaling aliases as well as notation, banks, field aliases and shuffles.
    if template=='scalar':
        task=['scale-half-component',[str(x) for x in scaled(p['k'],p['a'])]]
    else:
        coeffs={'sum':(1,1),'subtract':(1,-1),'linear':(1,p.get('k')),'double_scaled':(p.get('r'),p.get('k'))}[template]
        terms=sorted([[bool(abs(k)>1),[str(x) for x in scaled(k,p[v])]] for k,v in zip(coeffs,('a','b'),strict=True)])
        task=['combine',terms]
    return digest(task)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only the observed/supported radio response is provided')
    rng=random.Random(seed)
    if profile is not None:
        if profile not in PROFILES:raise ValueError('Unknown profile')
        if template and template!=PROFILES[profile]:raise ValueError('Profile/template mismatch')
        template=PROFILES[profile]
    if template is None:template=rng.choice([t for t,l in TEMPLATES.items() if l==level])
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template/difficulty mismatch')
    profile=profile or DEFAULT_PROFILE[template]  # selected before parameters
    raw=profile in RAW
    for _ in range(1000):
        p=normalize_parameters(template,parameters,raw) if parameters is not None else sample(template,rng)
        prompt,solution,c=build(template,p)
        try:entries=bank(template,p,c)
        except SampleRejected:
            if parameters is not None:raise
            continue
        break
    else:raise SampleRejected('Sampler exhausted')
    shape=RAW.get(profile,{'difficulty':True,'fields':True,'solution':True})
    # For fieldless raw evidence, answer banks are not learner content or identity.
    displayed=sorted(e[2] for e in entries) if shape['fields'] else []
    content=digest({'version':VERSION,'level':level if shape['difficulty'] else None,'prompt':prompt,'solution':solution if shape['solution'] else None,'bank':displayed,'correct_present':not raw,'fields_present':shape['fields']})
    qid=uid('question:'+content);fid=uid(qid+':selection')
    question={':question/id':qid,':question/problem':prompt}
    if shape['difficulty']:question[':question/difficulty']=':question.difficulty/'+level
    if shape['solution']:question[':question/worked-solution']=solution
    recipe_meta=[]
    if shape['fields']:
        choices=[]
        for recipe,value,display in entries:
            aid=uid(fid+':'+display)
            choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':display})
            recipe_meta.append({'recipe':recipe,'value':[str(x) for x in value],'answer_id':aid})
        correct_id=choices[0][':answer/id'];rng.shuffle(choices)
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if not raw:field[':answer-field/correct']=[':answer/id',correct_id]
        question[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'difficulty_design':level,'template':template,'bank_profile':profile,'parameters':canonical(p),'source':SOURCE,'source_references':SOURCE_IDS[template],'source_id':RAW.get(profile,{}).get('source_id'),'evidence_only':raw,'eligible_for_learning':not raw,'inferred_completions':not raw and template!='double_scaled','authored_missing_level':level in ('moderate','hard'),'correct_vector':[str(x) for x in c],'recipes':recipe_meta,'content_identity':content,'mathematical_fingerprint':mathematical_fingerprint(template,p),'plot_rating':'none','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY: one operation, including the source half-integer scalar multiplication.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: exactly two scalar products and two additions; one scalar |k|2..5.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: exactly four scalar products and two additions; both scalars |r|,|k|2..4.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];g=record['generation']
    lines=[f"## {g['difficulty_design']} — {g['template']} ({g['bank_profile']})",'',q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$')
        if ':answer-field/correct' in f:
            c=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);lines+=['','Correct: $'+c[':answer/value']+'$']
        else:lines+=['','Original correct designation absent; independently computed value: $'+vec(tuple(exact(x) for x in g['correct_vector']))+'$.']
    if ':question/answer-fields' not in q:lines+=['Original answer fields absent.']
    if ':question/worked-solution' in q:lines+=['','Worked solution','',q[':question/worked-solution']]
    else:lines+=['','Original worked solution absent.']
    return '\n'.join(lines)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=PROFILES);parser.add_argument('--parameters',help='Exact JSON parameter object');parser.add_argument('--field-type',choices=['radio'])
    args=parser.parse_args()
    if args.count<1:parser.error('Count must be positive')
    if args.difficulty=='all' and (args.template or args.profile or args.parameters):parser.error('Choose a difficulty for explicit template/profile/parameters')
    try: records=[generate(l,args.seed+i,args.template,args.field_type,json.loads(args.parameters) if args.parameters else None,args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    except ValueError as e:parser.error(str(e))
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
