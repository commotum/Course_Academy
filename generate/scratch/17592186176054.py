#!/usr/bin/env python3
"""Cosecant periodicity, math basis 1356. Local review records only; steps 3–7.

Observed source masks and all seven complete banks are public parameterized
raw:<source-id> profiles. Opaque historical wrong-operation intent is unresolved;
these profiles are evidence-only, never default learning banks. Normal generation
uses separately authored complete method-derived banks and retains observed
family prose and stages. Hard is explicitly authored: two full-period reductions
and a signed rational linear combination, without oddness or other identities.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard have the same optional arguments.
Explicit invalid instances raise ValueError, never silently resample. Different
seeds reorder choices but do not alter fixed-parameter identity. No plots needed.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186176054
ROOT=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
REC=SOURCE['record']
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
VERSION='csc-periodicity-1'
C=r'\operatorname{csc}⁡'
LEVELS=('easy','moderate','hard')
ORIGINAL={
 'q-66472':dict(c='4',n=2,a='1',b='0'),
 'q-66473':dict(c='4/3',n=-1,a='1',b='0'),
 'q-103818':dict(c='3',n=6,a='5',b='0'),
 'q-103820':dict(c='sqrt(5)',n=7,a='1',b='0'),
 'q-103822':dict(c='6',n=8,a='1/3',b='5'),
 'q-66605':dict(c='2',n=-2,a='1/4',b='2'),
 'q-66667':dict(c='sqrt(2)',n=5,a='5',b='-1'),
}
FAMILY={
 'q-66472':'legacy_integer','q-66473':'legacy_fraction',
 'q-103818':'scaled_integer','q-103820':'direct_radical',
 'q-103822':'reciprocal_integer','q-66605':'reciprocal_fraction',
 'q-66667':'affine_radical',
}
TEMPLATES={**{v:k for k,v in FAMILY.items()},'two_terms':None}
TLEVEL={f:('easy' if i<4 else 'moderate') for i,f in enumerate(FAMILY.values())}|{'two_terms':'hard'}

def tex(x):
    return sp.latex(sp.sympify(x),fold_short_frac=False).replace(' - ','-').replace(' + ','+').replace(' \\sqrt',r'\sqrt').replace('- ', '-')

def rattex(x):
    x=sp.sympify(x)
    return str(x) if x.q==1 else ('-' if x<0 else '')+r'\frac{'+str(abs(x.p))+'}{'+str(x.q)+'}'

def term(a,angle):
    return ('' if a==1 else '-' if a==-1 else tex(a))+C+'('+angle+r' )'

def add(x):
    return ('+' if x>0 else '-')+tex(abs(x)) if x else ''

def angle(n,legacy=False):
    return ('x '+('+' if n>0 else '-')+' '+str(2*abs(n))+'π') if legacy else 'x'+('+' if n>0 else '-')+str(2*abs(n))+r'\pi'

def hashid(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'csc-periodicity:'+x))

def params(p):
    p=dict(p)
    for key in ('c','a','b','d'):
        if key in p:
            p[key]=sp.sympify(p[key])
            if p[key].free_symbols or not p[key].is_real or not p[key].is_finite:raise ValueError('real exact scalar required')
    for key in ('n','m'):
        if key in p:
            v=sp.sympify(p[key])
            if v.is_integer is not True or v==0 or abs(v)>12:raise ValueError('nonzero whole period index, |n|<=12')
            p[key]=int(v)
    return p

def guard(f,p):
    if set(p)!=({'c','a','b','n','d','m'} if f=='two_terms' else {'c','a','b','n'}):raise ValueError('exact parameter keys required')
    c,a,b=p['c'],p['a'],p['b']
    allowed={sp.Integer(i) for i in range(2,13)}|{sp.Rational(i,j) for j in range(2,6) for i in range(j+1,13)}|{sp.sqrt(i) for i in (2,3,5,6,7,10)}
    if c not in allowed:raise ValueError('given cosecant is a familiar real value >1, <=12')
    if f in ('legacy_integer','scaled_integer','reciprocal_integer','reciprocal_fraction') and not c.is_Rational:raise ValueError('rational source family')
    if f=='legacy_integer' and not c.is_Integer:raise ValueError('integer family')
    if f=='legacy_fraction' and (not c.is_Rational or c.q==1):raise ValueError('proper noninteger fraction family')
    if f in ('direct_radical','affine_radical') and c.is_Rational:raise ValueError('radical family')
    if f in ('legacy_integer','legacy_fraction','direct_radical'):
        if a!=1 or b!=0:raise ValueError('direct workload')
    elif f=='scaled_integer':
        if not a.is_Integer or not 2<=a<=8 or b!=0 or not c.is_Integer:raise ValueError('one integer product workload')
    elif f.startswith('reciprocal'):
        if a not in {sp.Rational(1,k) for k in range(2,7)} or not b.is_Integer or not 1<=b<=8 or not c.is_Integer:raise ValueError('reciprocal-plus-positive-integer workload')
        if f=='reciprocal_integer' and not (a*c).is_Integer:raise ValueError('integer reduction family')
        if f=='reciprocal_fraction' and (a*c).is_Integer:raise ValueError('fraction reduction family')
    elif f=='affine_radical':
        if not a.is_Integer or not 2<=a<=8 or not b.is_Integer or not -6<=b<=-1:raise ValueError('radical scale and subtraction workload')
    elif f=='two_terms':
        d=p['d']
        eligible={sp.Rational(i,j) for j in range(2,7) for i in range(-5,6) if i and abs(sp.Rational(i,j))<=3 and sp.Rational(i,j).q>1}
        if a not in eligible or d not in eligible or a*d>=0 or a+d==0 or not b.is_Integer or not 1<=abs(b)<=6 or p['n']==p['m']:raise ValueError('two distinct reductions; opposite signed noninteger weights, noncanceling, offset')

def prompt(f,p):
    c,a,b,n=(p[k] for k in ('c','a','b','n'))
    if f.startswith('legacy'):
        return 'If $\\csc x = '+tex(c)+'$, then what is $\\csc ('+angle(n,True)+')$?'
    expression=term(a,angle(n))+add(b)
    if f=='two_terms':expression+=add(p['d']).replace(tex(abs(p['d'])),term(abs(p['d']),angle(p['m'])))
    return 'If $'+C+'x='+tex(c)+',$ then what is $'+expression+'?$'

OPENING='The period of $y='+C+'x$ is $2\\pi .$ Therefore, for integer $n$ we have\n\n$$\n'+C+'x='+C+'(x+2n\\pi ).\n$$\n\n'

def reduction(p,n):
    nt=str(n) if n>0 else '('+str(n)+')'
    return 'Substituting $n='+str(n)+'$ into the right-hand-side of the above gives\n\n$$\n\\begin{aligned}'+C+'x='+C+'(x+2\\cdot '+nt+'\\cdot \\pi )='+C+'('+angle(n)+' ).\\end{aligned}\n$$\n\nTherefore, if $'+C+'x='+tex(p['c'])+',$ then $'+C+'('+angle(n)+' )='+tex(p['c'])+'.$'

def solution(f,p):
    c,a,b,n=(p[k] for k in ('c','a','b','n'))
    s=OPENING+reduction(p,n)
    expr=term(a,angle(n))+add(b)
    value=sp.simplify(a*c+b)
    if f in ('legacy_integer','legacy_fraction','direct_radical'):return s
    s+='\n\nFinally, then\n\n$$\n'
    if f=='scaled_integer':return s+expr+'='+tex(a)+r'\cdot '+tex(c)+'='+tex(value)+'.\n$$'
    if f.startswith('reciprocal'):
        denominator=a.q
        # Preserve the distinct extra unreduced quotient in the integer family.
        rows=[expr+r' & ='+rattex(a)+'('+tex(c)+')'+add(b)]
        if f=='reciprocal_integer':rows.append(r' & =\frac{'+tex(c)+'}{'+str(denominator)+'}'+add(b))
        rows.extend([r' & ='+tex(a*c)+add(b),r' & ='+tex(value)+'.'])
        return s+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    if f=='affine_radical':return s+expr+'='+tex(a*c)+add(b)+'.\n$$'
    if f=='two_terms':
        d=p['d']; total=sp.simplify((a+d)*c+b)
        s=OPENING+reduction(p,n)+'\n\n'+reduction(p,p['m'])+'\n\nFinally, then\n\n$$\n'
        expression=term(a,angle(n))+add(b)+('+' if d>0 else '-')+term(abs(d),angle(p['m']))
        substitution=tex(a)+'('+tex(c)+')'+add(b)+('+' if d>0 else '-')+tex(abs(d))+'('+tex(c)+')'
        evaluation=tex(a*c)+add(b)+add(d*c)
        return s+r'\begin{aligned}'+expression+r' & ='+substitution+r' \\  & ='+evaluation+r' \\  & ='+tex(total)+r'.\end{aligned}'+'\n$$'
    raise ValueError(f)

# Complete authored banks: one recipe set chosen BEFORE parameters.
def operation_bank(f,p):
    c,a,b,n=(p[k] for k in ('c','a','b','n'))
    if TLEVEL[f]=='easy' and a==1:
        return [c,1/c,-c,c+2*n*sp.pi,2*n*c],['periodicity','reciprocal-confusion','sign-change','shift-output','multiply-by-angle-coefficient']
    if f=='scaled_integer':return [a*c,c,a+c,a/c,a*(c+2*n*sp.pi)],['periodicity-and-product','omit-scale','add-scale','invert-given-value','shift-output-before-scale']
    if f.startswith('reciprocal'):return [a*c+b,c+b,a*c,b-a*c,a*c-b],['periodicity-affine','omit-reciprocal-scale','omit-offset','reverse-product-sign','reverse-offset-sign']
    if f=='affine_radical':return [a*c+b,c+b,a*c,a*(c+b),a*c-b],['periodicity-affine','omit-scale','omit-offset','scale-offset','reverse-offset-sign']
    d=p['d']
    return [(a+d)*c+b,a*c+b,d*c+b,(a-d)*c+b,(a+d)*c-b],['two-reductions-and-combination','omit-second-term','omit-first-term','reverse-second-sign','reverse-offset-sign']

# Public historical expressions: patterns recover values, NOT original intent.
# They remain evidence-only for every parameter set, even when mathematically valid.
def historical_bank(sid,p):
    c,a,b,n=(p[k] for k in ('c','a','b','n')); pi=sp.pi
    if sid=='q-66472':return [tex(c),'π',tex(c)+'(1 + π)',tex(c)+' + 2π',tex(2*n*c)+'π']
    if sid=='q-66473':
        u,d=c.as_numer_denom()
        return [tex(c),tex(c)+' + 2π',r'\frac{π}{'+tex(d)+'}',r'\frac{'+tex(u)+'π}{'+tex(d)+'}',tex(u)+' + π']
    if sid=='q-103818':return [tex(a*c),tex(a+c),tex(c)+r'(\pi '+('+' if n>0 else '-')+str(abs(n))+')',tex(c)+r'\pi ',r'\frac{\pi }{'+tex(c)+'}']
    if sid=='q-103820':return [tex(2*n*c),r'\pi +'+tex(c),tex(n*c),tex(c)+r'\pi ',tex(c)]
    if sid=='q-103822':return [str(n),tex(2*b),tex(a*c+b),tex(c),tex(b)]
    if sid=='q-66605':return [tex(-b),tex(a*c+b),tex(b-a*c),tex(-a)+r'+\pi ',tex(c)]
    if sid=='q-66667':return [tex(-c),tex(-b)+r'+\pi ',tex(sp.sqrt(c**2+3))+r'+2\pi ',tex((a-2)*c),tex(a*c)+add(b)]
    raise ValueError(sid)

def parse_value(s):
    """Small balanced TeX reader for this scalar/trigonometric grammar.

    This parses actual rendered values; it does not consult parameters/recipes.
    Antlr/Lark are unavailable in the primary environment; no install is needed.
    """
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    s=s.replace('π',r'\pi').replace(r'\operatorname{csc}⁡','csc').replace(r'\csc','csc').replace('⁡','')
    def group(text,i):
        if text[i]!='{':raise ValueError('required TeX group')
        depth=1;j=i+1
        while j<len(text) and depth:
            depth+=(text[j]=='{')-(text[j]=='}');j+=1
        if depth:raise ValueError('unbalanced TeX group')
        return text[i+1:j-1],j
    def convert(text):
        out='';i=0
        while i<len(text):
            if text.startswith(r'\frac',i):
                u,j=group(text,i+5);v,j=group(text,j)
                out+='(('+convert(u)+')/('+convert(v)+'))';i=j
            elif text.startswith(r'\sqrt',i):
                u,j=group(text,i+5);out+='sqrt('+convert(u)+')';i=j
            elif text.startswith(r'\pi',i):out+=' pi ';i+=3
            elif text.startswith(r'\cdot',i):out+='*';i+=5
            else:out+=text[i];i+=1
        return out.replace('{','(').replace('}',')')
    s=convert(s).strip().rstrip('.').replace('^','**')
    s=re.sub(r'csc\s*x(?![A-Za-z])','csc(x)',s)
    return sp.simplify(parse_expr(s,local_dict={'pi':sp.pi,'csc':sp.csc,'x':sp.Symbol('x',real=True),'n':sp.Symbol('n',integer=True),'y':sp.Symbol('y',real=True),'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))

def bank_guard(values):
    for v in values:
        if v.free_symbols or not v.is_real or not v.is_finite:raise ValueError('invalid whole bank')
    if any(sp.simplify(x-y)==0 for i,x in enumerate(values) for y in values[i+1:]):raise ValueError('ambiguous whole bank')

def sample(f,rng):
    p={'c':str(rng.randint(2,12)),'a':'1','b':'0','n':rng.choice([i for i in range(-12,13) if i])}
    if f=='legacy_fraction':p['c']=str(rng.choice(sorted({sp.Rational(i,j) for j in range(2,6) for i in range(j+1,13) if sp.Rational(i,j).q>1})))
    if f in ('direct_radical','affine_radical'):p['c']='sqrt('+str(rng.choice((2,3,5,6,7,10)))+')'
    if f in ('scaled_integer','affine_radical'):p['a']=str(rng.randint(2,8))
    if f.startswith('reciprocal'):
        d=rng.randint(2,6); p['a']='1/'+str(d);p['b']=str(rng.randint(1,8))
        candidates=[c for c in range(2,13) if (c%d==0)==(f=='reciprocal_integer')]
        if not candidates:raise ValueError('empty workload')
        p['c']=str(rng.choice(candidates))
    if f=='affine_radical':p['b']=str(-rng.randint(1,6))
    if f=='two_terms':
        eligible=sorted({sp.Rational(i,j) for j in range(2,7) for i in range(1,6) if sp.Rational(i,j).q>1 and sp.Rational(i,j)<=3})
        p.update(a=str(rng.choice(eligible)),d=str(-rng.choice(eligible)),m=rng.choice([i for i in range(-12,13) if i]),b=str(rng.choice([i for i in range(-6,7) if i])))
        if rng.choice([0,1]):p['a'],p['d']=p['d'],p['a']
        p['c']=str(rng.choice(sorted({sp.Rational(i,j) for j in range(1,6) for i in range(j+1,13)}|{sp.sqrt(i) for i in (2,3,5,6,7,10)},key=float)))
    return params(p)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    rng=random.Random(seed);raw=bool(profile and profile.startswith('raw:'))
    if raw:
        sid=profile[4:]
        if sid not in SOURCES:raise ValueError('unknown source profile')
        chosen=FAMILY[sid]
        if template and template!=chosen:raise ValueError('source family mismatch')
        template=chosen
    else:
        if profile not in (None,'operations'):raise ValueError('unknown bank')
        if template is None:template=rng.choice([f for f,l in TLEVEL.items() if l==level])
        if template not in TEMPLATES:raise ValueError('unknown template')
        sid=TEMPLATES[template]
    if TLEVEL[template]!=level:raise ValueError('level mismatch')
    profile=profile or 'operations'
    # Explicit calls follow exactly the sampler's guards and complete-bank rejection.
    for _ in range(1000):
        try:
            p=params(parameters) if parameters is not None else sample(template,rng)
            guard(template,p)
            if raw:
                displayed=historical_bank(sid,p);values=[parse_value(v) for v in displayed];recipes=['opaque-historical-pattern']*5
            else:
                values,recipes=operation_bank(template,p);values=[sp.simplify(v) for v in values];displayed=[tex(v) for v in values]
            bank_guard(values)
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('no eligible instance')
    prob=prompt(template,p);sol=solution(template,p)
    correct=sp.simplify((p['a']+(p.get('d',0)))*p['c']+p['b'])
    if sum(sp.simplify(v-correct)==0 for v in values)!=1:raise ValueError('correct answer missing or ambiguous')
    original_match=raw and p==params(ORIGINAL[sid])
    # Identities distinguish evidence field omissions and include actual learner content.
    raw_has_solution=not raw or ':question/worked-solution' in SOURCES[sid]
    raw_has_level=not raw or ':question/difficulty' in SOURCES[sid]
    content={'version':VERSION,'problem':prob,'solution':sol if raw_has_solution else None,'level':level if raw_has_level else None,'values':sorted(displayed),'fields':['selection','radio'],'correct':str(correct) if (not raw or ':answer-field/correct' in SOURCES[sid][':question/answer-fields'][0]) else None}
    identity=hashid(content);qid=uid(identity);fid=uid(identity+':selection')
    if raw:
        q=copy.deepcopy(SOURCES[sid]);f=q[':question/answer-fields'][0]
        q[':question/problem']=prob
        if ':question/worked-solution' in q:q[':question/worked-solution']=sol
        for item,value in zip(f[':answer-field/choices'],displayed):item[':answer/value']=value
        if ':answer-field/correct' in f:
            ix=next(i for i,v in enumerate(values) if sp.simplify(v-correct)==0)
            f[':answer-field/correct']=copy.deepcopy(f[':answer-field/choices'][ix])
        if not original_match:
            q.pop(':db/id',None);q.pop(':question/math-academy-id',None);q[':question/id']=qid
            f.pop(':db/id',None);f[':answer-field/id']=fid
            for i,a in enumerate(f[':answer-field/choices']):a.pop(':db/id',None);a[':answer/id']=uid(identity+':selection:'+displayed[i])
            if ':answer-field/correct' in f:f[':answer-field/correct']=copy.deepcopy(next(a for a,v in zip(f[':answer-field/choices'],values) if sp.simplify(v-correct)==0))
    else:
        answers=[{':answer/id':uid(identity+':selection:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in displayed]
        correct_id=answers[next(i for i,v in enumerate(values) if sp.simplify(v-correct)==0)][':answer/id']
        rng.shuffle(answers)
        f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
        q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prob,':question/worked-solution':sol,':question/answer-fields':[f]}
    # Full-period aliases and notation/profile aliases do not inflate task counts.
    task={'workload':('direct' if template.startswith('legacy') or template=='direct_radical' else template),'c':str(p['c']),'a':str(p['a']),'b':str(p['b'])}
    if template=='two_terms':task['weights']=sorted([str(p['a']),str(p['d'])]);task.pop('a')
    return {'knowledge_point':{'db_id':KP_ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(v) for k,v in p.items()},'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'recipes':recipes,'content_fingerprint':identity,'mathematical_fingerprint':hashid(task),'domain':'csc x is defined; c>1; full-period integer offsets; source-family arithmetic ceilings','python':sys.version.split()[0],'sympy':sp.__version__,'plot_rating':'none','difficulty_origin':('authored missing-level claim' if template=='two_terms' else 'authored easy assignment to unrated source' if sid in ('q-66472','q-66473') else 'observed level'),'bank_origin':('historical evidence expression patterns; intent unresolved' if raw else 'authored method-operation bank')}}

# EASY: observed direct or one integer scale; unordered rational/radical families.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed single reciprocal/radical scale plus nonzero offset.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored two full-period reductions and opposite rational weighted terms.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']));print(q.get(':question/worked-solution','[Absent in captured source]'));print()
