#!/usr/bin/env python3
"""Exact quartic synthetic-division generator; math basis2275; local review only.

Two supplied distinct integer roots → two synthetic divisions → factor the
remaining rational quadratic → list four ascending distinct roots or add them.
Raw observed profiles preserve defects and omissions, are evidence-only, and
are never sampled for learning. Normal solutions repair the two known typos.
No EDB operations. See adjacent evidence for extraction and finite capacities.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import normalize_prose, normalize_tex, validate_generated_record, validate_prose
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record']; KP_ID=17592186054804; KP_UUID=KP[':knowledge-point/id']; TITLE=KP[':knowledge-point/title']
VERSION='quartic-two-roots-v1'
X=sp.Symbol('x')
SPECS={
 'sum_integer':dict(level='easy',kind='radio',source='q-112638',division=[1,0]),
 'roots_integer':dict(level='easy',kind='blank',source='q-270967',division=[0,1]),
 'roots_integer_general':dict(level='easy',kind='blank',source='q-328522',division=[0,1]),
 'roots_common_denominator':dict(level='moderate',kind='blank',source='q-337081',division=[0,1]),
 'roots_distinct_denominators':dict(level='hard',kind='blank',source='q-270970',division=[0,1]),
 'historical_sum_fractional':dict(level='hard',kind='radio',source='q-40091',division=[0,1],historical=True),
 'historical_sum_halves':dict(level='moderate',kind='radio',source='q-75795',division=[0,1],historical=True),
}
# Each bank selected before parameters. Opaque banks below are numerical
# response-pattern replay recipes, not recovered error diagnoses.
PROFILES={
 'sum_method':('sum_integer','method-derived'),
 'sum_integer_opposite_method':('sum_integer','authored method-derived'),
 'sum_fractional_opposite_method':('historical_sum_fractional','authored method-derived'),
 'sum_halves_opposite_method':('historical_sum_halves','authored method-derived'),
 'observed_sum_integer':('sum_integer','observed interpretation limited'),
 'raw_q-112638':('sum_integer','raw evidence'),
 'raw_q-270967':('roots_integer','raw evidence'),
 'raw_q-328522':('roots_integer_general','raw evidence'),
 'raw_q-337081':('roots_common_denominator','raw evidence'),
 'raw_q-270970':('roots_distinct_denominators','raw evidence'),
 'raw_q-40091':('historical_sum_fractional','opaque raw evidence'),
 'raw_q-75795':('historical_sum_halves','opaque raw evidence'),
 'sum_fractional_method':('historical_sum_fractional','authored method-derived'),
 'sum_halves_method':('historical_sum_halves','authored method-derived'),
}
class SampleRejected(ValueError): pass

def tex(a): return sp.latex(sp.Rational(a)).replace(' ','')
def poly(a, historical=False):
    """Source's descending signed polynomial notation, with zero terms omitted."""
    terms=[]
    for (n,),c in sp.Poly(a,X).terms():
        if not c: continue
        magnitude=abs(c)
        variable=('x' if n==1 else ('x^{'+str(n)+'}' if historical else '{x}^{'+str(n)+'}')) if n else ''
        body=('' if magnitude==1 and n else tex(magnitude))+variable
        terms.append(('-' if c<0 else ('+' if terms else ''))+body)
    text=''.join(terms) or '0'
    if historical: text=text.replace('+',' + ').replace('-', ' - ').strip().replace('- ','-',1) if text.startswith('-') else text.replace('+',' + ').replace('-',' - ')
    return text

def linear(r, primitive=False):
    r=sp.Rational(r)
    return poly(r.q*X-r.p if primitive else X-r)

def synthetic(p,r):
    coeff=sp.Poly(p,X).all_coeffs(); out=[coeff[0]]; products=[]
    for c in coeff[1:]:
        products.append(r*out[-1]); out.append(c+products[-1])
    return sp.Poly.from_list(out[:-1],X).as_expr(),coeff,products,out

def table(p,r):
    q,coeff,products,out=synthetic(p,r); degree=len(coeff)-1
    header='|  | '+' | '.join('${x}^{'+str(n)+'}$' for n in range(degree,-1,-1))+' |'
    row=lambda left,items:'| '+left+' | '+' | '.join('$'+tex(t)+'$' for t in items)+' |'
    return '\n'.join([header,'| '+' | '.join(['---']*(degree+2))+' |',row('$'+tex(r)+'$',coeff),'|  | $↓$ | '+' | '.join('$'+tex(t)+'$' for t in products)+' |',row('',out)])

def parse_parameters(p):
    if set(p)!={'given','remaining','scale'}: raise ValueError('Parameters require exactly given, remaining, scale')
    if len(p['given'])!=2 or len(p['remaining'])!=2: raise ValueError('Exactly two known and two remaining roots')
    try: g=list(map(sp.Rational,p['given'])); r=list(map(sp.Rational,p['remaining'])); a=sp.Rational(p['scale'])
    except Exception as e: raise ValueError('Exact rational parameters required') from e
    if not a or len(set(g))!=2 or any(t.q!=1 for t in g): raise ValueError('Nonzero scale; distinct integer known roots required')
    if len(set(g+r))!=4: raise ValueError('Four distinct rational real roots required; multiplicity is not distinctness')
    p4=sp.expand(a*sp.prod(X-t for t in g+r))
    if any(t.q!=1 for t in sp.Poly(p4,X).all_coeffs()): raise ValueError('Integral displayed coefficients required')
    return g,r,a,p4

def check_scope(name,p,raw=False):
    g,r,a,p4=parse_parameters(p)
    if raw: return g,r,a,p4
    if any(abs(t)>6 or t==0 for t in g): raise ValueError('Known roots must be nonzero integers of magnitude ≤6')
    if name in ('sum_integer','roots_integer','roots_integer_general'):
        if a!=1 or any(t.q!=1 or abs(t)>6 or t==0 for t in r): raise ValueError('Easy requires monic quartic and nonzero integer roots ≤6')
        if name=='roots_integer' and (g[0]!=-g[1] or r[0]!=-r[1]): raise ValueError('Difference-of-squares family requires two opposite pairs')
    elif name in ('roots_common_denominator','historical_sum_halves'):
        if sum(r)==0 or r[0].q!=r[1].q or not 2<=r[0].q<=4 or any(abs(t.p)>5 for t in r) or abs(a)!=r[0].q*r[1].q: raise ValueError('Moderate: two reduced fractions with nonzero sum, same denominator 2..4, numerators ≤5, primitive quadratic scale')
    elif name in ('roots_distinct_denominators','historical_sum_fractional'):
        if r[0].q==r[1].q or not all(2<=t.q<=6 and abs(t.p)<=5 for t in r) or abs(a)!=r[0].q*r[1].q: raise ValueError('Distinct reduced denominators 2..6, numerators ≤5, primitive quadratic scale')
    if max(abs(c) for c in sp.Poly(p4,X).all_coeffs())> (150 if SPECS[name]['level']=='easy' else 650): raise ValueError('Displayed arithmetic ceiling exceeded')
    return g,r,a,p4

def sample(name,rng):
    ints=list(range(-6,0))+list(range(1,7))
    if name=='roots_integer':
        u,v=rng.sample(range(1,7),2); g=[u,-u]; r=[v,-v]; a=1
    elif name in ('sum_integer','roots_integer_general'):
        z=rng.sample(ints,4); g=z[:2]; r=z[2:]; a=1
    else:
        g=rng.sample(ints,2)
        d=rng.randint(2,4) if name in ('roots_common_denominator','historical_sum_halves') else rng.randint(2,6)
        e=d if name in ('roots_common_denominator','historical_sum_halves') else rng.choice([i for i in range(2,7) if i!=d])
        numer=lambda den:rng.choice([i for i in range(-5,6) if i and sp.gcd(i,den)==1])
        r=[sp.Rational(numer(d),d),sp.Rational(numer(e),e)]; a=rng.choice([-1,1])*d*e
    return dict(given=list(map(str,g)),remaining=list(map(str,r)),scale=str(a))

def solution(name,g,r,a,p4,raw=False):
    spec=SPECS[name]; order=spec['division']; first,second=[g[i] for i in order]
    q3,*_=synthetic(p4,first); q2,*_=synthetic(q3,second)
    P,C,Q=map(poly,[p4,q3,q2]); F1,F2=linear(first),linear(second)
    f0,f1=map(linear,g)
    block=lambda s:'$$\n'+s+'\n$$'
    s=f'Since $p({tex(g[0])})=p({tex(g[1])})=0,$ by factor theorem $({f0})$ and $({f1})$ are both factors of $p(x).$\nTo factor $p(x)$ completely we need to find its other factors.\n\n'
    s+=f'Since $({F1})$ is a factor of $p(x),$ we know that $({F1})$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $({F1})$ using synthetic division:\n\n'+table(p4,first)
    s+='\n\nTherefore,\n\n'+block(r'\frac{'+P+'}{'+F1+'}='+C+',')+'\n\nwhich means that\n\n'+block(P+'=('+F1+')('+C+').')
    punctuation='.' if name=='roots_integer_general' else ':'
    s+=f'\n\nNow, because $({F2})$ is also a factor of $p(x),$ it must be a factor of the quotient $({C}).$ So, we divide this quotient by $({F2})$ using synthetic division once more'+punctuation+'\n\n'+table(q3,second)
    s+='\n\nTherefore,\n\n'+block(r'\frac{'+C+'}{'+F2+'}='+Q+',')
    pair=[second,first] if name=='roots_distinct_denominators' else [first,second]
    factors=''.join('('+linear(z)+')' for z in pair)
    s+='\n\nwhich means that\n\n'+block(P+'='+factors+'('+Q+').')
    k=a/(r[0].q*r[1].q); prefix='-' if k==-1 else '' if k==1 else tex(k)
    final=prefix+factors+''.join('('+linear(z,True)+')' for z in r)
    finalP=poly(p4+38*X**4+153*X**3+69*X**2-137*X+21) if raw and name=='roots_distinct_denominators' else P
    s+='\n\nWe can factor the quadratic factor even further, and get\n\n'+block(finalP+'='+final+'.')
    roots=[first,second]+r if spec['kind']=='radio' else sorted(g+r)
    if spec['kind']=='radio':
        count='three' if raw else 'four'
        s+=f'\n\nWe can now equate each factor to zero and solve for $x$ to find the {count} roots:\n\n'
        s+=block(r'\begin{aligned}x & ='+r'\,,\,x='.join(tex(z) for z in roots)+r'\end{aligned}')
        addition=''.join(('+' if i and z>=0 else '')+tex(z) for i,z in enumerate(roots))
        s+='\n\nFinally, the sum of the roots of the polynomial is\n\n'+block(addition+'='+tex(sum(set(roots)))+'.')
    else:
        s+='\n\nWe can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are\n\n'+block(r'\begin{aligned}x & ='+r'\,,\,x='.join(tex(z) for z in roots)+r'.\end{aligned}')
    return s

def prompt(name,g,p4):
    if SPECS[name].get('historical'):
        P=poly(p4,True); lead=' = ' if name=='historical_sum_fractional' else ' ='
        return f'Let $p(x){lead}{P}$. Given that $p({tex(g[0])}) = p({tex(g[1])}) = 0$, find the sum of all distinct real roots of $p(x)$.'
    P=poly(p4)
    if SPECS[name]['kind']=='radio': return f'Let $p(x)={P}.$ Given that $p({tex(g[0])})=p({tex(g[1])})=0,$ find the sum of all distinct real roots of $p(x).$'
    suffix='\n\n$x=$\n{{field-1}}, \n\n$\\,x=$\n'+ ('\n' if name=='roots_integer' else '')+'{{field-2}}, \n\n$\\,x=$\n{{field-3}}, \n\n$\\,x=$\n{{field-4}}.'
    return f'Let $p(x)={P},$ and $p({tex(g[0])})=p({tex(g[1])})=0.$ In **ascending order**, the distinct real roots of $p(x)$ are'+suffix

def bank(profile,g,r):
    total=sum(set(g+r))
    if profile and profile.endswith('opposite_method'):
        return [total,sum(g),-total,r[0],r[1]],0
    if profile=='raw_q-40091': return [total*sp.Rational(4,17),total,total*sp.Rational(2,17),total*sp.Rational(24,85),total*sp.Rational(44,51)],None
    if profile=='raw_q-75795': return [sum(g)*i for i in [0,-2,1,2,-1]],None
    if profile in ('raw_q-112638','observed_sum_integer'): return [r[0],sum(g),-r[1],g[0],total],4
    # Authored complete method bank: total; only known roots; only newly found
    # roots; reverse signs of the new roots; one new root omitted.
    return [total,sum(g),sum(r),sum(g)-sum(r),sum(g)+r[0]],0

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if profile is not None:
        if profile not in PROFILES: raise ValueError('Unknown profile')
        own=PROFILES[profile][0]
        if template and template!=own: raise ValueError('Profile/template mismatch')
        template=own
    eligible=[n for n,s in SPECS.items() if s['level']==level and (field_type is None or field_type in (s['kind'],':answer-field.type/'+s['kind']))]
    if not eligible: raise ValueError('No templates support requested level/field type')
    if template and template not in eligible: raise ValueError('Template does not support requested level/field type')
    rng=random.Random(seed); name=template or rng.choice(eligible); spec=SPECS[name]
    if profile is None and spec['kind']=='radio':
        pair={'sum_integer':['sum_method','sum_integer_opposite_method'],'historical_sum_fractional':['sum_fractional_method','sum_fractional_opposite_method'],'historical_sum_halves':['sum_halves_method','sum_halves_opposite_method']}[name]
        profile=pair[int(sum(map(sp.Rational,parameters['given']))==0)] if parameters is not None else rng.choice(pair)
    raw=bool(profile and profile.startswith('raw_'))
    if raw and parameters is None: raise ValueError('Evidence-only raw replay requires explicit parameters')
    for _ in range(2000):
        p=dict(parameters) if parameters is not None else sample(name,rng)
        try:
            g,r,a,P=check_scope(name,p,raw)
            if profile and ('method' in profile) and (sum(g)==0)!=profile.endswith('opposite_method'): raise SampleRejected('Profile requires its complete known-root-sum regime')
            values,correct=bank(profile,g,r) if spec['kind']=='radio' else (sorted(g+r),None)
            if spec['kind']=='radio' and len(set(values))!=5: raise SampleRejected('Whole bank collision')
            break
        except ValueError:
            if parameters is not None: raise
    else: raise SampleRejected('Bounded sampler exhausted')
    p=dict(given=list(map(str,g)),remaining=list(map(str,r)),scale=str(a))
    problem=prompt(name,g,P); worked=None if raw and spec.get('historical') else solution(name,g,r,a,P,raw)
    if not raw:
        problem=normalize_prose(problem); worked=normalize_prose(worked)
    fields=[]; bankvalues=[[v for v in values]] if spec['kind']=='radio' else [[v] for v in values]
    # Semantic task excludes scalar aliases, given order and distractor order;
    # supplied-root SET remains meaningful because it changes division work.
    mathematical={'polynomial_monic':str(sp.Poly(P/a,X).as_expr()),'given':sorted(map(str,g)),'response':spec['kind'],'difficulty':level}
    parameter_fingerprint=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()
    content={'version':VERSION,'level':None if raw and spec.get('historical') else level,'prompt':problem,'solution':worked,'bank':[sorted(tex(v) for v in vs) for vs in bankvalues],'correct_value':(tex(values[correct]) if correct is not None else None)}
    content_fingerprint=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    qid=uuid.uuid5(uuid.UUID(KP_UUID),content_fingerprint)
    for i,vs in enumerate(bankvalues):
        key='selection' if spec['kind']=='radio' else f'field-{i+1}'; fid=uuid.uuid5(qid,key)
        answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+tex(v))),':answer/type':':answer.type/math',':answer/value':normalize_tex(tex(v))} for v in vs]
        f={':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec['kind'],':answer-field/choices':answers}
        idx=correct if spec['kind']=='radio' else 0
        if idx is not None: f[':answer-field/correct']=[':answer/id',answers[idx][':answer/id']]
        random.Random(seed+i).shuffle(answers); fields.append(f)
    question={':question/id':str(qid),':question/problem':problem,':question/answer-fields':fields}
    if not(raw and spec.get('historical')): question[':question/difficulty']=':question.difficulty/'+level; question[':question/worked-solution']=worked
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile][1] if profile else 'observed blanks','evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':spec.get('historical',False) and not raw or bool(profile and 'method' in profile),'source_analysis':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[spec['source']],'parameter_fingerprint':parameter_fingerprint,'content_fingerprint':content_fingerprint,'plot_rating':'none','plot_assets':{},'domain':'four distinct nonzero rational real roots; integral quartic coefficients','answer_math':[str(v) for v in values],'repairs':(['three roots → four roots'] if name=='sum_integer' else ['unrelated final quartic → displayed quartic'] if name=='roots_distinct_denominators' else []) if not raw else []}}
    if not raw: validate_generated_record(record)
    else:
        validate_prose(problem)
        if worked: validate_prose(worked)
    return record

# EASY: monic integer quartics, sum radio or four ascending root blanks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: nonmonic quadratic, common reduced residual denominator.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: unlike residual denominators and signed primitive factors.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question']; lines=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        lines+=['\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])]
    if ':question/worked-solution' in q: lines+=['\nWorked solution\n',q[':question/worked-solution']]
    return '\n'.join(lines)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',help='JSON object for explicit replay');args=ap.parse_args()
    if args.count<1:ap.error('Positive count required')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    out=[generate(l,args.seed+i,args.template,parameters=json.loads(args.parameters) if args.parameters else None,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
