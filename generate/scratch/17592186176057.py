#!/usr/bin/env python3
"""Evenness of cosine; captured math basis 1356, steps 3–7 only.

Shared graph and instructional sentences are recovered exactly. Easy uses only
cos(-u)=cos(u); moderate additionally removes a whole number of periods; hard
also evaluates one affine expression. These are observed workloads, not a new
progression within any level. q-136634 is unrated and has no key or solution:
its public *_raw profile preserves that absence; *_repaired derives the unique
correct choice and supplies the common moderate solution. No source lookup is
used to generate questions. Source banks with uncertain interpretations remain
explicit structural profiles; authored default banks have complete method-based
operations and reject the entire instance on any equality collision.

Parameters: c exact rational or square-root rational cosine value, variable
x/a/t/u, n nonzero integer whole-period count; hard scale (nonunit small integer
or pi multiple), offset (nonzero rational). Fixed parameters/profile/content
retain identities across seeds and shuffle order. Mathematical task fingerprints
exclude banks and variable aliases. All layouts are one 5-choice radio field.
The invariant cosine graph is reused; no parameter-dependent plot is necessary.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186176057
KP_UUID='94645507-186a-54a7-a96b-ccfb0fb1f769'
TITLE='Utilizing the Evenness Property of the Cosine Function'
VERSION='cosine-evenness-1'
HERE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
GRAPH='images/23/2373daf4b5fd26f098bf90e998e2685db6a8b793e94ac9d80b08ea423cb535c0.png'
TEMPLATES={'even':'easy','period_even':'moderate','spaced_period_even':'moderate','affine_period_even':'hard'}
PROFILES={'q-136545':'even','q-136629':'even','q-158047':'even','q-158052':'period_even','q-136634_raw':'spaced_period_even','q-136634_repaired':'spaced_period_even','q-158059':'affine_period_even','authored_even':'even','authored_period':'period_even','authored_affine':'affine_period_even'}
DEFAULT={'easy':('even','authored_even'),'moderate':('period_even','authored_period'),'hard':('affine_period_even','authored_affine')}

def tex(v):
    return sp.latex(sp.sympify(v)).replace(' ','').replace('\\frac','\\frac')

def exact(v):
    x=sp.sympify(v,locals={'pi':sp.pi})
    if x.free_symbols or x.has(sp.Float) or x.is_real is not True: raise ValueError('Exact real numeric parameters required')
    return sp.simplify(x)

def hash_value(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))

def coeff_cos(scale,cos):
    return cos if scale==1 else '-'+cos if scale==-1 else tex(scale)+(' ' if tex(scale).endswith('\\pi') else '')+cos

def add_offset(s,b):
    return s+('+' if b>0 else '-')+tex(abs(b)) if b else s

def argument(v,n):
    return '-'+v+('+' if n>0 else '-')+str(2*abs(n))+r'\pi ' if n else '-'+v

def cosine(v,n=0): return 'cos⁡('+argument(v,n)+')'

def bank_values(profile,c,n,A,b):
    """Whole-profile recipes; interpretation limits are recorded in extraction."""
    if profile=='q-136545': return [-2*c,sp.S.Zero,2*c,-c,c]
    if profile=='q-136629': return [1+c,-1-c,-c,c,sp.sqrt(1-c*c)]
    if profile=='q-158047':
        # r,d describe the unreduced displayed radical; rational c disallowed.
        d=sp.denom(c); return [c,-sp.sqrt(1-c*c),-1/(2*d),sp.sqrt(1-c*c),-c]
    if profile=='q-158052': return [c+n*sp.pi,sp.S.Zero,c/n,c,-c]
    if profile.startswith('q-136634'): return [-c+n*sp.pi,c,-(1+c),c+n*sp.pi,-c]
    if profile=='q-158059': return [sp.S.One,A+b,c,2*A,A*c+b]
    if profile=='authored_even': return [c,-c,1-c*c,sp.sqrt(1-c*c),2*c]
    if profile=='authored_period': return [c,-c,c+2*n*sp.pi,c/(2*n),1-c*c]
    if profile=='authored_affine': return [A*c+b,-A*c+b,A*c-b,c+b,A+b]
    raise ValueError('Unknown profile')

def _parameters(level,p,profile):
    keys={'c','variable'}|({'n'} if level!='easy' else set())|({'scale','offset'} if level=='hard' else set())
    if set(p)!=keys: raise ValueError(f'Expected parameters {sorted(keys)}')
    c=exact(p['c']);v=p['variable'];n=p.get('n',0);A=exact(p.get('scale',1));b=exact(p.get('offset',0))
    if v not in ('x','a','t','u'): raise ValueError('Unsupported variable')
    if not (-1<=c<=1): raise ValueError('Cosine is in [-1,1]')
    # Same source number forms: rationals or one sqrt(integer)/integer.
    if not c.is_Rational:
        c2=sp.simplify(c*c)
        if not c2.is_Rational or sp.denom(c)>12: raise ValueError('Expected simple square-root rational')
    if isinstance(n,bool) or not isinstance(n,int) or (level!='easy' and not 1<=abs(n)<=20): raise ValueError('n must be nonzero integer with |n| <= 20')
    if level=='easy' and sp.denom(c)>12: raise ValueError('Easy denominator bound is 12')
    if level=='moderate' and sp.denom(c)>24: raise ValueError('Moderate denominator bound is 24')
    if level=='hard':
        if sp.denom(c)>10: raise ValueError('Hard denominator bound is 10')
        q=sp.simplify(A/sp.pi)
        if not (A.is_Integer and 2<=abs(A)<=5 or q.is_Integer and 1<=abs(q)<=3): raise ValueError('Hard scale: nonunit integer |A|=2..5 or nonzero pi multiple |A/pi|=1..3')
        if not b.is_Rational or b==0 or abs(b)>3 or sp.denom(b)>6: raise ValueError('Hard offset: nonzero small rational')
    if profile=='q-158047' and c.is_Rational: raise ValueError('Radical observed bank requires radical c')
    return c,v,n,A,b

# Shared prose and ordered mathematical masks. These are independent of choices.
def render(template,c,v,n,A,b):
    level=TEMPLATES[template];target=cosine(v,n);ct=tex(c)
    expr=add_offset(coeff_cos(A,target),b) if level=='hard' else target
    if template=='spaced_period_even':
        # Exact captured spaced notation, including Unicode pi.
        prompt=f'If $\\cos {v} ={ct}$, then $\\cos (-{v} '+('+' if n>0 else '-')+f' {2*abs(n)}π) =$'
    else: prompt=f'If $cos⁡{v}={ct},$ then ${expr}=$'
    opening="First, let's recall the graph of $y=cos⁡x.$\n\n![]("+GRAPH+")\n\n"
    identity='$$\ncos⁡(-x)=cos⁡x.\n$$'
    even_rows='$$\n\\begin{aligned}'+cosine(v)+' & =cos⁡'+v+' \\\\  & ='+ct+'.\\end{aligned}\n$$'
    if level=='easy':
        sol=opening+'Notice that our graph is symmetric about the $y$-axis. If we reflect the graph over the $y$-axis, we get the same picture. This means that $cos⁡x$ is an *even* function, and we have\n\n'+identity+'\n\nTherefore,\n\n'+even_rows
    else:
        sol=opening+'From the graph, we note the following:\n\n- The period of $cos⁡x$ is $2\\pi .$\n\n- Our graph is symmetric '+('over' if level=='hard' else 'about')+' the $y$-axis. This means that $cos⁡x$ is an *even* function, and we have\n\n'+identity+"\n\nLet's now evaluate our expression:\n\n- Firstly, using the periodicity of $cos⁡x,$ we have\n\n"
        expanded='-'+v+('+' if n>0 else '-')+r'2\pi \cdot '+str(abs(n))
        sol+='$$\n\\begin{aligned}'+target+' & =cos⁡('+expanded+') \\\\  & ='+cosine(v)+'.\\end{aligned}\n$$\n\n- Secondly, using the evenness of $cos⁡x,$ we have\n\n'+even_rows
        if level=='moderate': sol+='\n\nTherefore, $'+target+'='+ct+'.$'
        else:
            # Keep substitution and individually evaluated product separate.
            prod=sp.simplify(A*c);ans=sp.simplify(prod+b)
            sub=tex(A)+r' \cdot '+('('+ct+')' if c<0 else ct)
            sol+='\n\nTherefore,\n\n$$\n\\begin{aligned}'+expr+' & ='+add_offset(sub,b)+' \\\\  & ='+add_offset(tex(prod),b)+' \\\\  & ='+tex(ans)+'.\\end{aligned}\n$$'
    return prompt,sol

def sample(level,rng,profile):
    bound={'easy':12,'moderate':24,'hard':10}[level]
    vals=[sp.Rational(sign*k,d) for d in range(3,bound+1) for k in range(1,d) for sign in (-1,1)]
    vals+= [sign*sp.sqrt(r)/d for d in (3,4,5) for r in (2,3,5,7) if r<d*d for sign in (-1,1)]
    vals=sorted(set(vals),key=str)
    if profile=='q-158047': vals=[c for c in vals if not c.is_Rational]
    c=rng.choice(vals);p={'c':str(c),'variable':rng.choice(('x','a','t','u'))}
    if level!='easy':p['n']=rng.choice([n for n in range(-20,21) if n])
    if level=='hard':p.update(scale=str(rng.choice([2,3,4,5,-2,-3,sp.pi,2*sp.pi,-sp.pi])),offset=str(rng.choice([sp.Rational(k,d) for d in (1,2,3,4) for k in (-3,-2,-1,1,2,3)])))
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in DEFAULT: raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields are supported')
    if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
    template=template or (PROFILES[profile] if profile else DEFAULT[level][0])
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template/level mismatch')
    profile=profile or ('q-136634_repaired' if template=='spaced_period_even' else DEFAULT[level][1])
    if PROFILES[profile]!=template:raise ValueError('Profile/template mismatch')
    rng=random.Random(seed)
    for _ in range(2000 if parameters is None else 1):
        p=parameters if parameters is not None else sample(level,rng,profile)
        c,v,n,A,b=_parameters(level,p,profile);answer=sp.simplify(A*c+b)
        values=[sp.simplify(x) for x in bank_values(profile,c,n,A,b)]
        if any(sp.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]) or sum(sp.simplify(x-answer)==0 for x in values)!=1:
            if parameters is not None:raise ValueError('Whole bank is ambiguous; explicit inputs are not resampled')
            continue
        break
    else:raise ValueError('Could not sample eligible bank')
    prompt,solution=render(template,c,v,n,A,b)
    raw=profile=='q-136634_raw'
    if raw:solution=None
    texts=[tex(x) for x in values]
    # Exact simple TeX values; source Unicode π/spacing is a notation variation.
    canonical_p={'c':str(c),'variable':v}
    if level!='easy':canonical_p['n']=n
    if level=='hard':canonical_p.update(scale=str(A),offset=str(b))
    mathematical=hash_value({'level':level,'c':str(c),'scale':str(A),'offset':str(b)})
    fingerprint=hash_value({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(texts),'correct':None if raw else tex(answer),'field':'radio'})
    qid=uid('cos-even/question/'+fingerprint);fid=uid(qid+'/selection')
    answers=[{':answer/id':uid(fid+'/'+t),':answer/type':':answer.type/math',':answer/value':t} for t in texts]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not raw:field[':answer-field/correct']=[':answer/id',uid(fid+'/'+tex(answer))]
    rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile,'bank_profile':profile,'parameters':canonical_p,'parameter_fingerprint':mathematical,'content_fingerprint':fingerprint,'source':SOURCE,'source_profile':profile.startswith('q-'),'raw_missing_key_and_solution':raw,'authored_level_assignment':profile.startswith('q-136634'),'plot':{'rating':'none','unchanged_asset':GRAPH},'sympy_version':sp.__version__}}

# Easy: direct evenness, rational/radical given values, no periodicity.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# Moderate: negative input plus a nonzero integral number of full periods.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# Hard: same identity/period stages and a small nonunit affine calculation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];out=[q[':question/problem'],'']
    for f in q[':question/answer-fields']:
        for i,a in enumerate(f[':answer-field/choices']):out.append(f'{chr(65+i)}. $'+a[':answer/value']+'$')
    out+=['',q.get(':question/worked-solution','[Captured source has no worked solution or designated key.]')]
    return '\n'.join(out)

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=1);cli.add_argument('--format',choices=['json','markdown'],default='markdown');cli.add_argument('--template');cli.add_argument('--profile');args=cli.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (DEFAULT if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
