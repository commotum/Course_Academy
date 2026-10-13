#!/usr/bin/env python3
"""Parallel-vector scalar factor, frozen math basis 1356; stops at guide step 7.

Normal E/M/H levels are authored (both originals are unrated). E: integer
factor, integer coefficients; M: terminating-decimal input coefficient,
integer factor; H: reduced noninteger rational factor and integer coefficients.
The same two coefficient divisions, factoring and nonzero uniqueness are used
throughout. Full historical banks remain public raw evidence profiles; their
missing difficulty/solution/correct-ref attributes are deliberately absent.
Opaque historical recipes do not serve normal sampling. No plots or DB access.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None). Parameters u,v,k describe target k*(u*a+v*b), base u*a+v*b.
CLI: --difficulty easy|moderate|hard|all --seed N --count N --format markdown|json
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186096648
KP_UUID='27d5c96d-ca13-5c1e-83d3-0dc9f6da0f83'
TITLE='Determining Whether Two Vectors are Parallel'
VERSION='parallel-scalar-1'
HERE=Path(__file__).with_suffix('')
TEMPLATES=('target_first','lambda_first')
PROFILES=('method_ratio','raw_12135','raw_12139')
RAW_ANCHORS={'raw_12135':{'u':sp.Rational(1),'v':sp.Rational(-3),'k':sp.Rational(4)},'raw_12139':{'u':sp.Rational('-1/2'),'v':sp.Rational(6),'k':sp.Rational(-2)}}
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def tex(x):
    x=sp.Rational(x)
    if x.q==1:return str(x.p)
    return ('-' if x<0 else '')+r'\frac{'+str(abs(x.p))+'}{'+str(x.q)+'}'

def decimal(x):
    x=sp.Rational(x)
    if x.q==1:return str(x.p)
    if x.q not in (2,4,5):raise ValueError('only familiar terminating decimals allowed')
    return str(float(x)).rstrip('0').rstrip('.')

def lin(u,v,dec=False):
    """Complete two-term slots; never replace scalar substrings across prose."""
    fmt=decimal if dec else tex
    a=('a' if u==1 else '-a' if u==-1 else fmt(u)+'a')
    b=('b' if abs(v)==1 else fmt(abs(v))+'b')
    return a+(' + ' if v>0 else ' - ')+b

def math_key(p):
    # Normalize common scaling AND common sign of both vectors. Names/order/
    # profiles are incidental; k and base coefficient ratio retain the divisions.
    return [str(p['k']),str(p['v']/p['u'])]

def hashof(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))

def eligible(level,p,raw=False):
    if set(p)!={'u','v','k'}:raise ValueError('parameters must be exactly u,v,k')
    u,v,k=(p[n] for n in ('u','v','k'))
    if not u or not v or not k:raise ValueError('source requires nonzero vectors/factor and two nonzero components')
    if raw:
        if max(abs(u),abs(v),abs(k*u),abs(k*v))>54:raise ValueError('raw coefficient ceiling')
        return
    if level=='easy':
        ok=u.q==v.q==k.q==1 and 1<=abs(u)<=4 and 1<=abs(v)<=6 and 2<=abs(k)<=8 and max(abs(k*u),abs(k*v))<=48
    elif level=='moderate':
        ok=abs(u.p)==1 and u.q in (2,4,5) and v.q==k.q==1 and 1<=abs(v)<=6 and 2<=abs(k)<=6 and (k*u).q==1 and max(abs(k*u),abs(k*v))<=36
    elif level=='hard':
        ok=u.q==v.q==1 and 2<=k.q<=5 and 2<=abs(k.p)<=9 and k.q!=1 and (u/k.q).q==(v/k.q).q==1 and 1<=abs(u/k.q)<=4 and 1<=abs(v/k.q)<=6 and max(abs(k*u),abs(k*v))<=54
    else:raise ValueError('unknown difficulty')
    if not ok:raise ValueError('parameters outside authored '+level+' workload bounds')

@lru_cache(None)
def domain(level):
    """Enumerate finite complete eligible bank domains; no cosmetic scale counts."""
    pool={}
    for u in ([sp.Rational(s,d) for d in (2,4,5) for s in (-1,1)] if level=='moderate' else [sp.Rational(n) for n in range(-20,21) if n]):
      for v in range(-30,31):
       if not v:continue
       ks=([sp.Rational(n,d) for d in range(2,6) for n in range(-9,10) if n and math.gcd(abs(n),d)==1] if level=='hard' else [sp.Rational(n) for n in range(-8,9) if n])
       for k in ks:
        p={'u':u,'v':sp.Rational(v),'k':k}
        try:eligible(level,p)
        except ValueError:continue
        vals=bank(p,'method_ratio')
        if len({(t,x) for t,x in vals})!=5:continue
        key=tuple(math_key(p))
        # Choose a canonical representative from the WHOLE valid domain.
        rank=(abs(u)+abs(v),int(bool(u<0)),int(bool(v<0)))
        if key not in pool or rank<pool[key][0]:pool[key]=(rank,p)
    return tuple(p for _,p in sorted(pool.values(),key=lambda z:tuple(math_key(z[1]))))

def bank(p,profile):
    u,v,k=(p[n] for n in ('u','v','k'))
    # Complete bank operations; not a pool of arbitrary numerical perturbations.
    if profile=='raw_12135':numbers=[k,abs(v),-k,k/2]
    elif profile=='raw_12139':numbers=[-k,sp.Rational(0),1/k,k]
    elif profile=='method_ratio':numbers=[k,-k,1/k,-1/k]
    else:raise ValueError('unknown profile')
    result=[(':answer.type/math',tex(n)) for n in numbers]
    result.insert(2,(':answer.type/text','No such $λ$'))
    if len(set(result))!=5:raise ValueError('whole bank rejected: colliding values')
    return result

def solution(p):
    u,v,k=(p[n] for n in ('u','v','k'));target=lin(k*u,k*v);base=lin(u,v)
    # Unevaluated substitutions are kept rather than collapsing all rows with CAS.
    return ('Notice that\n\n$$\nλ('+base+')=λ('+tex(u)+')a+λ('+tex(v)+')b.\n$$\n\n'
      'The same scale factor must multiply the whole non-zero vector. Comparing the two coefficients gives\n\n$$\n'
      r'\begin{aligned}'+'\nλ &= '+r'\frac{'+tex(k*u)+'}{'+tex(u)+'}'+' = '+tex(k)+r' \\'+'\nλ &= '+r'\frac{'+tex(k*v)+'}{'+tex(v)+'}'+' = '+tex(k)+'\n'+r'\end{aligned}'+'\n$$\n\n'
      'Notice that\n\n$$\n'+target+'='+tex(k)+'('+base+').\n$$\n\n'
      'Therefore,\n\n$$\nλ='+tex(k)+'\n$$\n\n'
      'The two non-zero vectors are parallel. '+('Their directions are the same because the factor is positive.' if k>0 else 'Their directions are opposite because the factor is negative.'))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only source-shaped radio fields supported')
    profile=profile or 'method_ratio'
    if profile not in PROFILES:raise ValueError('unknown profile')
    raw=profile.startswith('raw_')
    expected='target_first' if profile=='raw_12135' else 'lambda_first' if profile=='raw_12139' else None
    if template is not None and expected is not None and template!=expected:raise ValueError('profile/template mismatch')
    rng=random.Random(seed)
    template=template or expected or rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('unknown template')
    if parameters is None:
        if raw:raise ValueError('raw evidence requires explicit parameters; never a default learner bank')
        p=dict(rng.choice(domain(level)))
    else:p={n:sp.Rational(x) for n,x in parameters.items()}
    eligible(level,p,raw=raw)
    u,v,k=(p[n] for n in ('u','v','k'))
    dec=level=='moderate' or profile=='raw_12139'
    # Observed decimal is in the base, target remains integer at source inputs.
    base,target=lin(u,v,dec),lin(k*u,k*v,dec)
    lhs,rhs=(target,'λ('+base+')') if template=='target_first' else ('λ('+base+')',target)
    prompt='Given that $'+lhs+'$ and $'+rhs+'$ are equal (non-zero) vectors, find the scale factor $λ$.'
    values=bank(p,profile)
    sol=None if raw else solution(p)
    actual=None if raw else level
    identity=hashof([VERSION,prompt,sol,sorted(values),actual])
    qid=uid(identity);fid=uid(identity+':selection')
    choices=[{':answer/id':uid(fid+':'+t+':'+value),':answer/type':t,':answer/value':value} for t,value in values]
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==tex(k))]
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
      'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':{n:str(x) for n,x in p.items()},
      'source':SOURCE,'source_ids':(['q-'+profile.removeprefix('raw_')] if raw else []),
      'original_case':bool(raw and p==RAW_ANCHORS[profile]),'actual_difficulty':actual,'authored_difficulty':level,'authored':not raw,'evidence_only':raw,'eligible_for_learning':not raw,
      'mathematical_fingerprint':hashof(math_key(p)),'content_fingerprint':identity,
      'meaningful_domain_count':None if raw else len(domain(level)),
      'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
      'zero_convention':'Curriculum explicitly calls the zero vector parallel to any vector; source scalar-factor questions exclude it.',
      'recipes':(['correct_ratio','reverse_factor_sign','reverse_ratio','reverse_ratio_and_sign','deny_existing_factor'] if not raw else 'historical complete bank; interpretation limits documented')}}

# EASY — integer scalar multiplication/factoring, source q-12135 form.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — one familiar terminating-decimal coefficient, source q-12139 form.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — reduced noninteger rational factor, canonical 7/3 form; no new method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
    lines=['## '+(('Original raw replay' if g['original_case'] else 'Generated evidence bank variant') if g['evidence_only'] else 'Generated authored '+g['actual_difficulty']),
      'Template: '+g['template']+'; profile: '+g['bank_profile'], '',q[':question/problem'],'']
    for a in f[':answer-field/choices']:
        value=a[':answer/value'];lines.append('- '+('$'+value+'$' if a[':answer/type'].endswith('/math') else value))
    if ':answer-field/correct' in f:
        answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        lines+=['','Correct: $'+answer+'$','','Worked solution:',q[':question/worked-solution']]
    else:lines+=['','Original source correct designation, difficulty and worked solution are absent; this evidence profile preserves the omissions.']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('markdown','json'),default='markdown')
    ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=PROFILES)
    ap.add_argument('--parameters',help='JSON object, required for raw evidence profiles')
    ns=ap.parse_args()
    if ns.count<1:ap.error('--count must be positive')
    try:
        records=[generate(l,ns.seed+i,ns.template,parameters=json.loads(ns.parameters) if ns.parameters else None,profile=ns.profile) for l in (('easy','moderate','hard') if ns.difficulty=='all' else (ns.difficulty,)) for i in range(ns.count)]
    except ValueError as e:ap.error(str(e))
    print(json.dumps(records,indent=2,ensure_ascii=False) if ns.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
