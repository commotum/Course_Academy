#!/usr/bin/env python3
"""Oddness of tangent: basis-1356 local generator; no database writes.

Easy: direct sign reversal, observed integer and rational masks.
Moderate: authored level assignment for observed unrated shifted-angle mask;
remove an integer multiple of pi then reverse sign. No periodicity-only branch.
Hard: observed fractional affine masks; periodic reduction, oddness and the
same four-stage fraction arithmetic, without new trig identities or algebra.
Profiles whose scalar historical errors underdetermine intent are evidence-only.
Explicit raw_unrated replay preserves missing difficulty, solution and key.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186176058
KP_UUID='66a1733a-d7bb-5c86-a154-9e54422053a7'
TITLE='Utilizing the Oddness Property of the Tangent Function'
VERSION='tangent-oddness-1'
ROOT=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
IMAGE='images/df/df1aba3f5ff980de82a74dde8170ad708e379caf2188873bcddc83177e87c7a6.png'
EASY_PREFIX="First, let's recall the graph of $y=tan⁡x.$\n\n![]("+IMAGE+")\n\nOur graph has rotational symmetry of order $2$ about the origin. If we rotate the graph ${180}^{∘}$ around the origin, we get the same picture. This means that $tan⁡x$ is an *odd* function, and we have\n\n$$\ntan⁡(-x)=-tan⁡x.\n$$\n\nTherefore, \n\n$$\n"
HARD_PREFIX="First, let's recall the graph of $y=tan⁡x.$\n\n![]("+IMAGE+")\n\nFrom the graph, we note the following:\n\n- The period of $tan⁡x$ is $\\pi .$\n\n- Our graph has rotational symmetry of order $2$ about the origin. This means that $tan⁡x$ is an *odd* function, and we have\n\n$$\ntan⁡(-x)=-tan⁡x.\n$$\n\nLet's now evaluate our expression:\n\n- Firstly, using the periodicity of $tan⁡x,$ we have\n\n$$\n"
TEMPLATES={'direct_integer':'easy','direct_fraction':'easy','direct_positive':'easy','shifted':'moderate','affine_integer':'hard','affine_fraction':'hard'}
DEFAULT_PROFILES={'direct_integer':'reciprocal_zero','direct_fraction':'numerator_omission','direct_positive':'reciprocal_zero','shifted':'output_shift','affine_integer':'affine_operations','affine_fraction':'affine_operations'}
PROFILES={'reciprocal_zero','numerator_omission','radical_observed','output_shift','raw_unrated','affine_operations','integer_observed','fraction_observed'}

def tex(x):
    return sp.latex(sp.sympify(x)).replace('- ', '-')
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+x))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def signed_add(left,right):
    return left+('+' if right>=0 else '-')+tex(abs(right))
def negval(v):return '-('+tex(v)+')' if v<0 else '-'+tex(v)
def arg(v,n,spaced=False):
    sign='+' if n>0 else '-'
    shift=('' if abs(n)==1 else str(abs(n)))+('π' if spaced else r'\pi ')
    return '-'+v+(' '+sign+' '+shift if spaced else sign+shift)
def rational_domain():
    return sorted({sp.Rational(s*p,q) for s in [-1,1] for q in range(2,10) for p in range(1,10) if sp.gcd(p,q)==1 and p!=q})
def domain(template):
    if template=='direct_integer':return [{'v':str(v),'variable':'a'} for v in range(-9,-1)]
    if template=='direct_positive':return [{'v':str(v),'variable':'x'} for v in range(2,10)]
    if template=='direct_fraction':return [{'v':str(v),'variable':'a'} for v in rational_domain()]
    if template=='shifted':return [{'v':str(v),'variable':'x','n':n} for v in rational_domain() for n in range(-12,13) if n]
    out=[]
    for q in range(2,9):
      for a in range(1,q):
       if sp.gcd(a,q)!=1:continue
       for v in range(-8,-1):
        if template=='affine_integer':
         if (a*(-v))%q:continue
         bs=range(1,6)
        else:
         if q<3:continue
         bs=[sp.Rational(k,q) for k in range(1,q) if sp.gcd(k,q)==1 and sp.gcd(a*(-v)+k,q)>1]
        for b in bs:
         out.append({'v':str(v),'variable':'x','n':3,'c':str(sp.Rational(a,q)),'b':str(b)})
    return out

def check_parameters(level,template,p):
    expected={'v','variable'}|({'n'} if level!='easy' else set())|({'c','b'} if level=='hard' else set())
    if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(sorted(expected)))
    if p['variable'] not in ['a','x','t']:raise ValueError('Variable must be a, x or t')
    v=sp.Rational(p['v'])
    if v==0 or abs(v)==1:raise ValueError('Nonzero tangent value with magnitude different from one required')
    if template=='direct_integer' and not (v.q==1 and -9<=v<=-2):raise ValueError('Negative integer [-9,-2]')
    if template=='direct_positive' and not (v.q==1 and 2<=v<=9):raise ValueError('Positive integer [2,9]')
    if template in ['direct_fraction','shifted'] and v not in rational_domain():raise ValueError('Reduced rational numerator1..9 denominator2..9')
    if level!='easy' and (type(p['n'])!=int or not 1<=abs(p['n'])<=12):raise ValueError('Signed nonzero integer shift magnitude1..12')
    if level=='hard':
      c,b=sp.Rational(p['c']),sp.Rational(p['b'])
      if not(v.q==1 and -8<=v<=-2 and 0<c<1 and 2<=c.q<=8):raise ValueError('Hard integer v [-8,-2], proper positive fractional c denominator2..8')
      if template=='affine_integer' and not (b.q==1 and 1<=b<=5 and (-c*v).q==1):raise ValueError('Integer offset1..5 and integral scaled value')
      if template=='affine_fraction' and not(3<=c.q<=8 and b.q==c.q and 0<b<1 and (-c*v+b).q<c.q):raise ValueError('Shared reduced denominator3..8 and reducible final sum required')
    return {k:sp.Rational(p[k]) if k in ['v','c','b'] else p[k] for k in p}

def bank(template,profile,p):
    v=p['v']; c=p.get('c',sp.Integer(1));b=p.get('b',sp.Integer(0));n=p.get('n',0)
    correct=-c*v+b
    if profile=='reciprocal_zero': vals=[-v,v,1/v,0,-1/v]; recipes=['oddness','omit_oddness','reciprocal','zero','negative_reciprocal']
    elif profile=='numerator_omission': vals=[v,1/v,-v,-1/v,-sp.Rational(1,v.q)];recipes=['omit_oddness','reciprocal','oddness','negative_reciprocal','omit_numerator']
    elif profile=='radical_observed': vals=[v,-1/v,-v,1/v,-sp.sqrt(v)];recipes=['omit_oddness','negative_reciprocal','oddness','reciprocal','opaque_negative_root_value']
    elif profile in ['output_shift','raw_unrated']: vals=[-v+n*sp.pi,v+n*sp.pi,-v,0,v];recipes=['shift_output_after_oddness','shift_output_without_oddness','oddness','zero','omit_oddness']
    elif profile=='affine_operations': vals=[correct,c*v+b,-c*v-b,-v+b,-c*v];recipes=['complete','omit_oddness','reverse_offset_sign','omit_scale','omit_offset']
    elif profile=='integer_observed':vals=[correct,0,c*v+b,-(c*v+b),b];recipes=['complete','zero','omit_oddness','global_negative_without_oddness','omit_tangent_term']
    elif profile=='fraction_observed':vals=[correct,-(c*v+b),sp.pi-(c*v+b),-1,c*v+b];recipes=['complete','negative_unreflected_affine','opaque_pi_plus_negative_unreflected_affine','opaque_negative_one','omit_oddness']
    else:raise ValueError('Unknown bank')
    vals=list(map(sp.simplify,vals))
    if any(not x.is_real for x in vals):raise ValueError('Nonreal option')
    if len(set(vals))!=5 or sum(x==correct for x in vals)!=1:raise ValueError('Whole bank collision')
    rendered=[tex(x) for x in vals]
    # Preserve observed complete expression notation, not an opaque value lookup.
    if profile in ['output_shift','raw_unrated']:
      rendered[0]=tex(-v)+(' + ' if n>0 else ' - ')+str(abs(n))+'π'
      rendered[1]=tex(v)+(' + ' if n>0 else ' - ')+str(abs(n))+'π'
    if profile=='fraction_observed':
      remainder=-(c*v+b)
      rendered[2]=r'\pi '+('+' if remainder>=0 else '-')+tex(abs(remainder))
    return vals,rendered,recipes,correct

def texts(level,template,p,raw=False):
    v,x=p['v'],p['variable'];n=p.get('n',0)
    if level=='easy':
      prompt=f'If $tan⁡{x}={tex(v)},$ then $tan⁡(-{x})=$'
      rhs=[f'-tan⁡{x}',negval(v)]
      if v<0:rhs.append(tex(-v))
      sol=EASY_PREFIX+r'\begin{aligned}'+f'tan⁡(-{x}) & ='+r' \\  & ='.join(rhs)+r'.\end{aligned}'+'\n$$'
      return prompt,sol
    angle=arg(x,n)
    tangent=f'tan⁡({angle})'
    if level=='moderate':
      prompt=f'If $\\tan {x} = {tex(v)}$, then $\\tan ({arg(x,n,True)}) =$'
    else:
      prompt=f'If $tan⁡{x}={tex(v)},$ then $'+signed_add(tex(p['c'])+tangent,p['b'])+'=$'
    periodic=r'\begin{aligned}'+tangent+f' & =tan⁡(-{x}).'+r'\end{aligned}'
    oddrhs=[f'-tan⁡{x}',negval(v)]
    if v<0:oddrhs.append(tex(-v))
    odd=r'\begin{aligned}'+f'tan⁡(-{x}) & ='+r' \\  & ='.join(oddrhs)+r'.\end{aligned}'
    sol=HARD_PREFIX+periodic+'\n$$\n\n- Secondly, using the oddness of $tan⁡x,$ we have\n\n$$\n'+odd+'\n$$'
    if level=='moderate':sol+=f'\n\nTherefore, $\\tan ({arg(x,n,True)})={tex(-v)}.$'
    else:
      c,b=p['c'],p['b'];a,q=c.p,c.q
      full=signed_add(tex(c)+tangent,b)
      r1=signed_add(tex(c)+r'\cdot '+tex(-v),b)
      r2=signed_add(r'\frac{'+str(a*(-v))+'}{'+str(q)+'}',b)
      if template=='affine_integer':r3=signed_add(tex(-c*v),b)
      else:r3=r'\frac{'+str(a*(-v)+b.p)+'}{'+str(q)+'}'
      r4=tex(-c*v+b)
      sol+='\n\nTherefore,\n\n$$\n'+r'\begin{aligned}'+full+' & ='+r' \\  & ='.join([r1,r2,r3,r4])+r'.\end{aligned}'+'\n$$'
    return prompt,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only source-shaped radio supported')
    rng=random.Random(seed)
    if template is None:
      eligible=[t for t,l in TEMPLATES.items() if l==level]
      if profile in ['numerator_omission']:eligible=['direct_fraction']
      elif profile=='radical_observed':eligible=['direct_positive']
      elif profile=='integer_observed':eligible=['affine_integer']
      elif profile=='fraction_observed':eligible=['affine_fraction']
      template=rng.choice(eligible)
    if TEMPLATES.get(template)!=level:raise ValueError('Template/level mismatch')
    profile=profile or DEFAULT_PROFILES[template]
    allowed={'direct_integer':['reciprocal_zero'],'direct_fraction':['numerator_omission','reciprocal_zero'],'direct_positive':['reciprocal_zero','radical_observed'],'shifted':['output_shift','raw_unrated'],'affine_integer':['affine_operations','integer_observed'],'affine_fraction':['affine_operations','fraction_observed']}
    if profile not in allowed[template]:raise ValueError('Profile incompatible with template')
    if parameters is None:
      candidates=domain(template);rng.shuffle(candidates)
      for candidate in candidates:
       candidate=dict(candidate)
       if level!='easy':candidate['n']=rng.choice([i for i in range(-12,13) if i])
       try:
        p=check_parameters(level,template,candidate);values,rendered,recipes,correct=bank(template,profile,p);break
       except ValueError:continue
      else:raise ValueError('No eligible whole-bank parameters')
    else:p=check_parameters(level,template,parameters);values,rendered,recipes,correct=bank(template,profile,p)
    raw=profile=='raw_unrated'
    prompt,solution=texts(level,template,p,raw)
    evidence_only=profile in ['raw_unrated','radical_observed','fraction_observed']
    keyparams={k:str(v) for k,v in p.items() if k not in ['variable','n']}
    # All integer-period shifts reduce to the same reflected function. The
    # demand to remove a period remains assessed, but its integer spelling is
    # a presentation variant. Direct sampler policies likewise are not skills.
    assessed_form='direct_oddness' if template.startswith('direct') else template
    mathfinger=digest({'level':level,'assessed_form':assessed_form,'period_removal_assessed':level!='easy','parameters':keyparams})
    content={'version':VERSION,'difficulty':None if raw else level,'prompt':prompt,'solution':None if raw else solution,'bank':sorted(rendered),'key':None if raw else tex(correct)}
    identity=digest(content);qid=uid(identity);fid=uid(identity+':selection')
    choices=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/math',':answer/value':s} for s in rendered]
    correct_id=choices[values.index(correct)][':answer/id']
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw:field[':answer-field/correct']=[':answer/id',correct_id]
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(v) if isinstance(v,sp.Rational) else v for k,v in p.items()},'mathematical_fingerprint':mathfinger,'content_fingerprint':identity,'domain':'tan(variable) finite; shift is an integer multiple of pi','recipes':dict(zip(rendered,recipes)),'evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'authored_difficulty':level=='moderate','solution_status':'missing_preserved' if raw else ('authored_completion' if level=='moderate' else 'observed_parameterized'),'python':sys.version.split()[0],'sympy':sp.__version__}}

# Easy: one direct oddness application; three observed number/solution masks.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: integer-period removal plus oddness, anchored by canonical example.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: the two observed fractional affine arithmetic structures.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];parts=[q[':question/problem'],'']
    for a in q[':question/answer-fields'][0][':answer-field/choices']:parts.append('- $'+a[':answer/value']+'$')
    parts+=['',q.get(':question/worked-solution','[Raw source has no worked solution.]')]
    return '\n'.join(parts)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
    a=parser.parse_args()
    if a.count<1:parser.error('count must be positive')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
