#!/usr/bin/env python3
"""Scalar line-integral SETUP, math basis 1356. No evaluation is assessed.

Six captured radio families use full expression/stage masks, amplitude and
interval parameters. Historical complete banks are public evidence profiles,
not inferred error intentions. Normal defaults select a family first and use a
complete method bank (substitution, speed, omitted speed, reciprocal speed,
squared speed). A whole colliding/nonreal bank is rejected. Authored hard uses
three noncancelling coordinate substitutions with one product and one square;
it does not assess parameterization, primitive finding or integral evaluation.

Run with the repository .venv/bin/python. Evidence and source masks are local.
"""
from __future__ import annotations
import argparse, copy, functools, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s

KP_ID=17592186133829
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; TITLE=KP[':knowledge-point/title']; VERSION='scalar-line-setup-1'
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
t,x,y,z=s.symbols('t x y z',real=True)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
FAMILIES={
 'parabola':('easy','q-167608',(t,t**2),x/(4*y+1),0,1),
 'difference':('moderate','q-40253',(t**2+t,t**2-t),s.sqrt(2)*(x-y),0,s.sqrt(2)),
 'squares':('moderate','q-76377',(t**2,t-1,t+1),2*x-y**2-z**2,0,3),
 'quadratic3':('moderate','q-76356',(t**2+1,t**2-1,t**2),x+y-z,0,2),
 'helix':('moderate','q-76379',(s.cos(t),s.sin(t),t),z*(x**2-y**2),0,s.pi/2),
 'linear_cubic':('moderate','q-76368',(2*t,2-t),x**3-y,-1,2),
 'hard_product_square':('hard',None,None,None,0,2),
}
SCALAR_TEX={
 'parabola':r'\frac{x}{4y+1}', 'difference':r'\sqrt{2}(x-y)',
 'squares':r'2x-{y}^{2}-{z}^{2}', 'quadratic3':'x+y-z',
 'helix':r'z({x}^{2}-{y}^{2})', 'linear_cubic':'(x^{3} - y)',
}
INTERVAL_TEX={
 'parabola':r'0\le t\le 1', 'difference':r't\in [0,\sqrt{2}]',
 'squares':r't\in [0,3]', 'quadratic3':r't\in [0,2]',
 'helix':r'0\le t\le \frac{\pi }{2}', 'linear_cubic':r'-1 \le t \le 2',
}
RAW_RECIPES={
 'parabola':(4*t**2+1,t**2/s.sqrt(2*t+1),t/s.sqrt(4*t**2+1),t*(2*t+1),t*s.sqrt(4*t**2+1)),
 'difference':(4*t*s.sqrt(4*t**2+1),t*s.sqrt(2*t**2+1),s.sqrt(2)*t*s.sqrt(2*t**2-1),4*t*s.sqrt(8*t**2+1),2*t*s.sqrt(4*t**2+1)),
 'squares':(-2*(t**2+2*t-1)*s.sqrt(t**2+1),-2*s.sqrt(2)*s.sqrt(2*t**2+1),-2*t*s.sqrt(t**2+1),s.sqrt(2)*(t**2-2*t)*s.sqrt(2*t**2+1),(t**2+2*t)*s.sqrt(2*t**2+1)),
 'quadratic3':(2*t**2*s.sqrt(t+1),2*s.sqrt(3)*t**3,s.sqrt(2)*(t**2-t)*s.sqrt(t+1),2*t**2*s.sqrt(t**2-t),s.sqrt(3)*t**2*s.sqrt(t**2+1)),
 'helix':(s.sqrt(2)*t*s.cos(t)*s.sqrt(2*s.cos(t)**2+1),s.sqrt(2)*t*s.cos(2*t),2*s.sqrt(2)*t*s.sin(t)*s.sqrt(2*s.cos(t)**2+3),2*t*(s.cos(t)-s.sin(t)),2*t*(s.cos(t)-s.sin(t))**2),
 'linear_cubic':(s.sqrt(5)*(8*t**3+t-2),s.sqrt(2)*(4*t**3-3),2*(t**3-t**2+4*t),3*(8*t**3-t**2+4*t-4),8*t**3+t**2-4),
}

def tex(v): return s.latex(s.sympify(v)).replace(r'\log',r'\ln')
def mult(m,fragment):
    """Complete-component slot. Unit coefficients preserve original spelling."""
    if m==1:return fragment
    ending=fragment[-1:] if fragment[-1:] in ('.',',','?') else ''
    body=fragment[:-1] if ending else fragment
    return tex(m)+r'\left('+body+r'\right)'+ending
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+'|'+value))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def exact(v):
    if isinstance(v,float) or isinstance(v,bool):raise ValueError('exact rational/algebraic inputs required')
    q=s.sympify(v,locals={'pi':s.pi});
    if q.free_symbols or q.is_real is not True:raise ValueError('finite real numerical parameter required')
    return q

def parameters_for(family,rng):
    if family=='hard_product_square':
        return dict(a=rng.randint(1,3),b=rng.randint(1,3),d=rng.randint(1,3),c=rng.choice([-3,-2,-1,1,2,3]),e=rng.choice([-3,-2,-1,1,2,3]),m=rng.choice([-3,-2,-1,1,2,3]),lo=rng.choice([0,s.Rational(1,2),1]),hi=rng.choice([s.Rational(3,2),2,s.Rational(5,2),3]))
    if family=='helix':
        a,b=sorted(rng.sample(range(7),2));return {'m':rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]),'lo':a*s.pi/12,'hi':b*s.pi/12}
    if family=='linear_cubic':
        lo=rng.choice([-2,-s.Rational(3,2),-1,-s.Rational(1,2)]);hi=rng.choice([1,s.Rational(3,2),2,s.Rational(5,2),3])
    else:
        endpoints=sorted(set([s.Rational(n,d) for d in (1,2,3) for n in range(0,6*d+1)]+[s.sqrt(2),s.sqrt(3)]),key=float)
        lo,hi=sorted(rng.sample(endpoints,2),key=float)
    return {'m':rng.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]),'lo':lo,'hi':hi}

def guard(family,p):
    expected={'m','lo','hi'}|({'a','b','c','d','e'} if family=='hard_product_square' else set())
    if set(p)!=expected:raise ValueError('parameters must be exactly '+str(sorted(expected)))
    p={k:exact(v) for k,v in p.items()}
    if p['m'].is_integer is not True or not 1<=abs(p['m'])<=(3 if family.startswith('hard') else 6):raise ValueError('amplitude workload bound')
    lo,hi=p['lo'],p['hi']
    if not lo<hi:raise ValueError('strictly increasing interval required')
    if family=='helix':
        if not 0<=lo<hi<=s.pi/2 or any((12*v/s.pi).is_integer is not True for v in (lo,hi)):raise ValueError('helix endpoints must be familiar pi/12 multiples')
    elif family=='linear_cubic':
        if lo not in [-2,-s.Rational(3,2),-1,-s.Rational(1,2)] or hi not in [1,s.Rational(3,2),2,s.Rational(5,2),3]:raise ValueError('completed cubic interval workload')
    elif family.startswith('hard'):
        if lo not in [0,s.Rational(1,2),1] or hi not in [s.Rational(3,2),2,s.Rational(5,2),3]:raise ValueError('hard interval workload')
        for k in ('a','b','d'):
            if p[k].is_integer is not True or not 1<=p[k]<=3:raise ValueError('hard positive coefficient workload')
        for k in ('c','e'):
            if p[k].is_integer is not True or not 1<=abs(p[k])<=3:raise ValueError('hard nonzero offset workload')
    else:
        allowed=set([s.Rational(n,d) for d in (1,2,3) for n in range(0,6*d+1)]+[s.sqrt(2),s.sqrt(3)])
        if lo not in allowed or hi not in allowed:raise ValueError('observed-family endpoint workload')
    return p

def math_data(family,p):
    if family=='hard_product_square':
        curve=(p['a']*t**2,p['b']*t+p['c'],p['d']*t+p['e']);f=x*y-z**2
    else:curve,f=FAMILIES[family][2:4]
    f=p['m']*f;sub=s.expand(f.subs(dict(zip((x,y,z),curve)),simultaneous=True));sub=s.trigsimp(sub)
    derivative=tuple(s.diff(q,t) for q in curve)
    speed2=s.trigsimp(s.expand(sum(v*v for v in derivative)));speed=s.sqrt(speed2)
    if p['lo']>=0:speed=s.refine(speed,s.Q.nonnegative(t))
    correct=s.simplify(sub*speed)
    if family=='parabola':wrong=p['m']*t**2/(4*t**2+1)
    elif family=='difference':wrong=p['m']*s.sqrt(2)*(curve[0]+curve[1])
    elif family=='squares':wrong=p['m']*(2*curve[0]+curve[1]**2+curve[2]**2)
    elif family=='quadratic3':wrong=p['m']*(curve[0]+curve[1]+curve[2])
    elif family=='helix':wrong=p['m']*curve[2]*(curve[0]**2+curve[1]**2)
    elif family=='linear_cubic':wrong=p['m']*(curve[0]**3+curve[1])
    else:wrong=p['m']*(curve[0]*curve[1]+curve[2]**2)
    bank=(correct,s.simplify(sub),s.simplify(sub*speed2),s.simplify(sub/speed),s.simplify(wrong*speed))
    return dict(curve=curve,f=f,sub=sub,derivative=derivative,speed2=speed2,speed=speed,correct=correct,bank=bank)

def integral_tex(expr,p):return r'\int_{'+tex(p['lo'])+'}^{'+tex(p['hi'])+'}'+tex(expr)+r'\,\mathrm{d}t'

def mask_bounds(text,family,p):
    """Only full interval and full definite-integral bound components are slots."""
    oldlo,oldhi=FAMILIES[family][4:6]
    replacements={
      'parabola':(r'_{0}^{1}',), 'difference':(r'_{0}^{\sqrt{2}}',),
      'squares':(r'_{0}^{3}',), 'quadratic3':(r'_{0}^{2}',),
      'helix':(r'_{0}^{\pi /2}',), 'linear_cubic':(r'_{-1}^{2}',),
    }
    new_bounds='_{'+tex(p['lo'])+'}^{'+tex(p['hi'])+'}'
    for old in replacements[family]:text=text.replace(old,new_bounds)
    newinterval=(r't\in ['+tex(p['lo'])+','+tex(p['hi'])+']') if family in ('difference','squares','quadratic3') else tex(p['lo'])+r'\le t\le '+tex(p['hi'])
    # Preserve the exact captured notation when each mathematical component is unchanged.
    if p['lo']==oldlo and p['hi']==oldhi:
        for old in replacements[family]:text=text.replace(new_bounds,old)
        newinterval=INTERVAL_TEX[family]
    return text.replace(INTERVAL_TEX[family],newinterval)

def mask_math_scalar(text,family,m):
    component=SCALAR_TEX[family]
    def change(match):
        chunk=match[0]
        # Full scalar function expression only; no short-variable substitution.
        return chunk.replace(component,mult(m,component))
    return MATH.sub(change,text)

def source_prompt(family,p):
    return mask_math_scalar(mask_bounds(QUESTIONS[FAMILIES[family][1]][':question/problem'],family,p),family,p['m'])

def source_solution(family,p,raw=False):
    original=QUESTIONS[FAMILIES[family][1]].get(':question/worked-solution')
    if original is None:return None
    text=mask_bounds(original,family,p)
    def block_change(match):
        block=match[0];body=match[1]
        if body.startswith('f(r(t))'):
            rows=re.split(r'\\\\',body);rows=[r.split('=',1)[0]+'='+mult(p['m'],r.split('=',1)[1].strip()) for r in rows]
            return r'\begin{aligned}'+r' \\  '.join(rows)+r'\end{aligned}' if p['m']!=1 else block
        if body.startswith(r'{\int }'):
            rows=re.split(r'\\\\',body);result=[]
            for row in rows:
                lhs,rhs=row.split('=',1)
                lhs=lhs.replace(SCALAR_TEX[family],mult(p['m'],SCALAR_TEX[family]))
                if 'f(r(t))' not in rhs:rhs=mult(p['m'],rhs.strip()) if p['m']!=1 else rhs
                result.append(lhs+'='+rhs)
            return r'\begin{aligned}'+r' \\  '.join(result)+r'\end{aligned}' if p['m']!=1 else block
        return block
    text=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block_change,text,flags=re.S)
    # Inline function-definition math gets its complete expression slot; aligned
    # blocks were handled above and cannot be multiplied again.
    def inline(match):
        chunk=match[0]
        if chunk.startswith('$$'):return chunk
        return chunk.replace(SCALAR_TEX[family],mult(p['m'],SCALAR_TEX[family]))
    text=MATH.sub(inline,text)
    if not raw and family=='quadratic3':text=text.replace('since $t>0$ along the path of $C.$','since $t\\ge 0$ along the path of $C.$')
    return text

def authored_solution(family,p,data):
    """Source prose and complete operator/substitution/reduction stages."""
    curve=data['curve'];dim=len(curve);variables=('x','y','z')[:dim];basis=('i','j','k')[:dim]
    assignments=', '.join('$'+v+'='+tex(c)+'$' for v,c in zip(variables,curve))
    formal='+'.join(r'\frac{\mathrm{d}'+v+r'}{\mathrm{d}t}\,'+b for v,b in zip(variables,basis))
    operator='+'.join(r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(c)+')'+b for c,b in zip(curve,basis))
    derivatives='+'.join('('+tex(c)+r')\,'+b for c,b in zip(data['derivative'],basis))
    formalnorm=r'\sqrt{'+ '+'.join(r'(\frac{\mathrm{d}'+v+r'}{\mathrm{d}t})^2' for v in variables)+'}'
    substitutednorm=r'\sqrt{'+ '+'.join('('+tex(c)+')^2' for c in data['derivative'])+'}'
    submask=(r'('+tex(curve[0])+r')('+tex(curve[1])+r')-('+tex(curve[2])+r')^2') if dim==3 else r'('+tex(curve[0])+r')^3-('+tex(curve[1])+')'
    submask=mult(p['m'],submask)
    expandedmask=(mult(p['m'],tex(p['a']*p['b'])+r't^3+('+tex(p['a']*p['c'])+r')t^2-\left('+tex(p['d']**2)+r't^2+('+tex(2*p['d']*p['e'])+r')t+'+tex(p['e']**2)+r'\right)')) if dim==3 else mult(p['m'],r'8t^3-2+t')
    bounds='_{'+tex(p['lo'])+'}^{'+tex(p['hi'])+'}'
    return ('Since $r(t)=\\langle '+', '.join(tex(c) for c in curve)+'\\rangle,$ then along the curve we have '+assignments+'.\n\n'
      "Computing $r'(t)$ and $\\|r'(t)\\|,$ we get the following:\n\n$$\n\\begin{aligned}r'(t)&="+formal+r' \\ &= '+operator+r' \\ &= '+derivatives+r" \\ \|r'(t)\|&="+formalnorm+r' \\ &= '+substitutednorm+r' \\ &= '+tex(data['speed'])+r'\end{aligned}'+'\n$$\n\n'
      'Now, since $f('+','.join(variables)+')='+tex(data['f'])+'$, we obtain\n\n$$\n'+r'\begin{aligned}f(r(t))&='+submask+r' \\ &= '+expandedmask+r' \\ &= '+tex(data['sub'])+r'.\end{aligned}'+'\n$$\n\n'
      'Therefore, we can write the integral as\n\n$$\n'+r'\begin{aligned}\int_C f('+','.join(variables)+r')\,\mathrm{d}s&=\int'+bounds+r" f(r(t))\,\|r'(t)\|\,\mathrm{d}t"+r' \\ &= \int'+bounds+'('+tex(data['sub'])+')('+tex(data['speed'])+r')\,\mathrm{d}t'+r' \\ &= '+integral_tex(data['correct'],p)+r'.\end{aligned}'+'\n$$')

@functools.lru_cache(maxsize=8192)
def full_value(expr,lo,hi):
    value=s.integrate(expr,(t,lo,hi))
    if value.has(s.Integral):return value
    # expand preserves separate logarithm coefficients; global simplify can
    # logcombine rational coefficients into enormous integer powers.
    return s.expand(value)

def distinct_bank(expressions,p):
    """Reject complete banks: every integral value must be unequal, not only setups."""
    values=[full_value(e,p['lo'],p['hi']) for e in expressions]
    for i,value in enumerate(values):
        if value.has(s.Integral):
            # Exact sign separation fallback is available for same-sign integrands.
            pass
        for j in range(i):
            delta=s.expand(value-values[j])
            if delta==0:raise ValueError('ambiguous complete integral values')
            if delta.is_zero is False:continue
            # Certified symbolic sign of the complete integrand difference on the
            # finite domain also proves its definite integrals unequal.
            diff=s.simplify(expressions[i]-expressions[j])
            interval=s.Interval(p['lo'],p['hi'])
            try:
                zero=s.solveset(diff,t,domain=interval)
                sign=s.simplify(diff.subs(t,(p['lo']+p['hi'])/2))
                if zero.is_finite_set and len(zero)<=2 and sign.is_zero is False:
                    segments=[p['lo']]+sorted([q for q in zero if p['lo']<q<p['hi']],key=float)+[p['hi']]
                    signs=[s.sign(diff.subs(t,(a+b)/2)) for a,b in zip(segments,segments[1:])]
                    if len(set(signs))==1 and signs[0] in (-1,1):continue
            except (NotImplementedError,TypeError):pass
            # Exact expressions that do not simplify to a comparison are rejected,
            # rather than deemed distinct by a floating-point closeness test.
            raise ValueError('full integral inequality not established exactly')
    return values

def raw_bank(family,p):
    q=QUESTIONS[FAMILIES[family][1]];out=[]
    for choice,expr in zip(q[':question/answer-fields'][0][':answer-field/choices'],RAW_RECIPES[family]):
        value=mask_bounds(choice[':answer/value'],family,p)
        # A text option owns its dollar delimiters and trailing punctuation.
        if value.startswith('$'):value='$'+mult(p['m'],value[1:value.rfind('$')])+'$'+value[value.rfind('$')+1:]
        else:value=mult(p['m'],value)
        out.append((value,enum(choice[':answer/type']),s.simplify(p['m']*expr)))
    return out

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('observed shape is radio')
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        source_id=profile.split(':',1)[1]
        candidates=[name for name,v in FAMILIES.items() if v[1]==source_id]
        if not candidates:raise ValueError('unknown observed source')
        if template and template!=candidates[0]:raise ValueError('profile/template mismatch')
        template=candidates[0]
    if profile=='completed-source' and template is None:template='linear_cubic'
    family=template or rng.choice([k for k,v in FAMILIES.items() if v[0]==level])
    if family not in FAMILIES or FAMILIES[family][0]!=level:raise ValueError('difficulty/template scope mismatch')
    raw=bool(profile and profile.startswith('observed:'))
    if profile not in (None,'method','completed-source') and not raw:raise ValueError('unknown complete profile')
    if profile=='completed-source' and family!='linear_cubic':raise ValueError('completion is for unrated cubic')
    for attempt in range(100):
        p=guard(family,parameters if parameters is not None else parameters_for(family,rng));data=math_data(family,p)
        if raw or profile=='completed-source':
            options=raw_bank(family,p);expressions=[v[2] for v in options]
            correct_index=next(i for i,expr in enumerate(expressions) if s.simplify(expr-data['correct'])==0)
            values=None
            if not raw:
                try:values=distinct_bank(expressions,p)
                except ValueError:
                    if parameters is not None:raise
                    continue
        else:
            expressions=data['bank'];options=[(integral_tex(e,p),':answer.type/math',e) for e in expressions];correct_index=0
            if family=='linear_cubic':
                value,kind,expr=options[0]
                options[0]=('$'+value+'$.',':answer.type/text',expr)
            try:values=distinct_bank(expressions,p)
            except ValueError:
                if parameters is not None:raise
                continue
        break
    else:raise ValueError('no eligible complete instance in sampling budget')
    if family.startswith('hard'):
        prompt='Which of the following is equivalent to $\\int_C '+tex(data['f'])+r'\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle '+', '.join(tex(q) for q in data['curve'])+'\\rangle$ for $'+tex(p['lo'])+r'\le t\le '+tex(p['hi'])+'$?'
        solution=authored_solution(family,p,data)
    else:
        prompt=source_prompt(family,p);solution=source_solution(family,p,raw)
        if solution is None and not raw:solution=authored_solution(family,p,data)
        if not raw and family=='linear_cubic':prompt=prompt.replace(r'\int_(C)',r'\int_C')
    observed=QUESTIONS.get(FAMILIES[family][1]);observed_field=observed[':question/answer-fields'][0] if observed else None
    has_key=not raw or ':answer-field/correct' in observed_field
    if raw and has_key:
        correct_id=observed_field[':answer-field/correct'][':answer/id']
        correct_index=next(i for i,a in enumerate(observed_field[':answer-field/choices']) if a[':answer/id']==correct_id)
    profile=profile or 'method'
    difficulty=enum(observed[':question/difficulty']) if raw and ':question/difficulty' in observed else None if raw else ':question.difficulty/'+level
    content={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted([(v,k) for v,k,e in options]),'difficulty':difficulty,'has_key':has_key,'correct':options[correct_index][0] if has_key else None}
    qid=uid(digest(content));fid=uid(qid+'|selection')
    answers=[{':answer/id':uid(fid+'|'+kind+'|'+value),':answer/type':kind,':answer/value':value} for value,kind,expr in options]
    correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if has_key:field[':answer-field/correct']=[':answer/id',correct]
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if difficulty is not None:question[':question/difficulty']=difficulty
    if solution is not None:question[':question/worked-solution']=solution
    task={'curve':[s.srepr(q) for q in data['curve']],'f':s.srepr(data['f']),'bounds':[s.srepr(p[v]) for v in ('lo','hi')],'criterion':'scalar line-integral definite-integral setup'}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':question,
      'generation':{'version':VERSION,'seed':seed,'template':family,'bank_profile':profile,'parameters':{k:str(v) for k,v in p.items()},
      'mathematical_fingerprint':digest(task),'content_fingerprint':digest(content),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
      'source_id':FAMILIES[family][1],'authored_level':family in ('linear_cubic','hard_product_square'),'evidence_only':raw or profile=='completed-source','eligible_for_learning':not raw and profile!='completed-source',
      'raw_attribute_omissions':[k for k in (':question/difficulty',':question/worked-solution') if k not in question]+([':answer-field/correct'] if not has_key else []),
      'recipe_labels':['correct','omit_speed','square_speed','reciprocal_speed','wrong_substitution'] if profile=='method' else ['observed complete expression pattern; intent unresolved']*5,
      'authored_bank':profile=='method',
      'full_values':[str(v) for v in values] if values is not None else None,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# Easy: observed one rational substitution and cancellation with parabola speed.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed 2D/3D cancellation/identity families; cubic is an authored
# level assignment because its captured source contains no difficulty.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored three-coordinate product-minus-square substitution with no
# cancellation of degree, followed by the SAME scalar speed setup method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    text=q[':question/problem']+'\n\n'
    text+='\n'.join(f'{i+1}. '+('$'+a[':answer/value']+'$' if a[':answer/type']==':answer.type/math' else a[':answer/value']) for i,a in enumerate(f[':answer-field/choices']))
    return text+'\n\n'+q.get(':question/worked-solution','[Raw source has no worked solution.]')
def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(q) for q in records))
if __name__=='__main__':main()
