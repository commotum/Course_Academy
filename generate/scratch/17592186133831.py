"""Setup-only vector line integrals, frozen math basis 1356; local JSON review.

Observed source masks replay all five easy layouts and complete historical banks.
Their scale parameter is a real field scaling, not a lookup of source answers.
Raw profiles are public evidence-only (one ambiguous bank and two solution typos).
Authored defaults use every source-shaped family, formal derivatives, substituted
components and fixed dot-product stages. Moderate adds two nonunit monomial
coordinate derivatives; hard adds four mixed-component products to the observed
spiral/product-rule layout. Neither asks for scalar integration or another method.
Identity includes actual presentation and complete bank, excluding option order,
seed and profile aliases. Mathematical fingerprints exclude banks and identities.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s

KP_ID=17592186133831
KP_UUID='e34a2cbf-0bed-50eb-9e62-7c6e55560cb9'
TITLE='Constructing Line Integrals of a Vector-Valued Functions Over Plane Curves'
VERSION='plane-vector-setup-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
SOURCES=SOURCE['record'][':knowledge-point/questions']
T,X,Y=s.symbols('t x y', real=True)
FAMILIES=('polynomial','rotation','shifted_circle','exponential_root','spiral')
TEMPLATES={**{f:'easy' for f in FAMILIES},'monomial':'moderate','mixed_spiral':'hard'}
PROFILES={**{f'observed_{f}':f for f in FAMILIES},**{f'authored_{f}':f for f in TEMPLATES}}
SOURCE_BY_FAMILY=dict(zip(FAMILIES,SOURCES))


def tex(v):
    return s.latex(s.sympify(v),order='lex',fold_short_frac=False).replace(r'\log',r'\ln')
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def block(v):return '$$\n'+v+'\n$$'
def aligned(lhs,rows):return r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'
def vector(p,q): return '('+tex(p)+r')\,i+('+tex(q)+r')\,j'
def integ(v,a,b): return r'\int_{'+tex(a)+'}^{'+tex(b)+'}('+tex(v)+r')\,dt'

def math_data(f,p):
    """Exact components; no evaluated integral appears in learner output."""
    a,b,c,d=[s.sympify(p.get(k,1)) for k in ('a','b','c','d')]
    lo,hi=s.sympify(p['lower']),s.sympify(p['upper'])
    if f=='polynomial': P,Q=a*Y**2,-b*X**2; u,v=T,T**2
    elif f=='rotation': P,Q=a*Y,-a*X;u,v=s.cos(T),s.sin(T)
    elif f=='shifted_circle':P,Q=a*X,a*Y+b;u,v=s.cos(T),s.sin(T)
    elif f=='exponential_root':P,Q=a*X*Y**2,2*b*Y;u,v=s.exp(T),s.sqrt(T)
    elif f=='spiral':P,Q=a*X,a*Y;u,v=T*s.cos(T),T*s.sin(T)
    elif f=='monomial':P,Q=a*Y**2,-b*X**2;u,v=T**p['m'],T**p['n']
    elif f=='mixed_spiral':P,Q=a*X+b*Y,c*X+d*Y;u,v=T*s.cos(T),T*s.sin(T)
    else: raise ValueError('unknown family')
    pr,qr=P.subs({X:u,Y:v}),Q.subs({X:u,Y:v})
    du,dv=s.diff(u,T),s.diff(v,T)
    z=s.collect(s.expand(pr*du+qr*dv),T) if f=='mixed_spiral' else s.trigsimp(s.expand(pr*du+qr*dv))
    return P,Q,u,v,pr,qr,du,dv,z,lo,hi


def validate_parameters(f,p,observed=False):
    if observed:
        if set(p)-{'scale','upper'}:raise ValueError('observed parameters: scale, upper only')
        if type(p.get('scale')) is not int or not 1<=abs(p['scale'])<=5:raise ValueError('scale: signed nonzero integer, magnitude <=5')
        b=s.sympify(p['upper']); canonical=s.pi if f in ('rotation','shifted_circle','spiral') else s.Integer(1)
        if b not in (canonical,canonical/2,canonical*2):raise ValueError('observed upper must be original, half or double')
        return
    expected={'a','lower','upper'}|({'b'} if f in ('polynomial','shifted_circle','exponential_root','monomial','mixed_spiral') else set())|({'m','n'} if f=='monomial' else set())|({'c','d'} if f=='mixed_spiral' else set())
    if set(p)!=expected:raise ValueError(f'parameter keys must equal {sorted(expected)}')
    for key in expected&{'a','b','c','d'}:
        if type(p[key]) is not int or not 1<=abs(p[key])<=4:raise ValueError('nonzero signed integer coefficients, magnitude <=4')
    lo,hi=s.sympify(p['lower']),s.sympify(p['upper'])
    if f in ('polynomial','monomial'):
        if lo!=0 or hi not in (1,2,3):raise ValueError('monomial interval is [0,1|2|3]')
    elif f=='exponential_root':
        if lo!=1 or hi not in (2,3):raise ValueError('normal root curves use regular interval [1,2|3]')
    else:
        if lo!=0 or hi not in (s.pi/3,2*s.pi/3,4*s.pi/3):raise ValueError('trig upper is pi/3, 2pi/3 or 4pi/3')
    if f=='monomial' and (type(p['m']) is not int or type(p['n']) is not int or p['m'] not in (2,3,4) or p['n'] not in (2,3,4) or p['m']==p['n']):raise ValueError('moderate has unequal nonunit powers 2..4')
    if f=='mixed_spiral' and (p['a']==p['d'] or p['b']==p['c']):raise ValueError('hard has four nonzero mixed terms, unequal diagonal and cross coefficients')


def sample(f,r):
    coeff=lambda:r.choice((-4,-3,-2,-1,1,2,3,4))
    p={'a':coeff(),'lower':'0','upper':str(r.choice((1,2,3)))}
    if f in ('polynomial','shifted_circle','exponential_root','monomial','mixed_spiral'):p['b']=coeff()
    if f=='exponential_root':p.update(lower='1',upper=str(r.choice((2,3))))
    if f in ('rotation','shifted_circle','spiral','mixed_spiral'):p['upper']=str(r.choice((s.pi/3,2*s.pi/3,4*s.pi/3)))
    if f=='monomial':p['m'],p['n']=r.sample((2,3,4),2)
    if f=='mixed_spiral':p.update(c=coeff(),d=coeff())
    return p


def authored(f,p):
    P,Q,u,v,pr,qr,du,dv,z,lo,hi=math_data(f,p)
    prompt='Which integral is obtained from $'+r'\int_C F\cdot\mathrm{d}r'+'$ given that $F(x,y)='+vector(P,Q)+'$ and $C$ is the path $r(t)='+vector(u,v)+'$ for $t\\in ['+tex(lo)+','+tex(hi)+']$? Use the supplied parameterization and limits to compute $F(r(t))\\cdot r\'(t)$. Do not evaluate the integral or change variables.'
    # Substitute into unexpanded coordinate components first, preserving the
    # original input structure. Positive and signed factors are always grouped.
    def substituted(expr):
        raw=tex(expr)
        raw=re.sub(r'\bx\b',lambda _:'('+tex(u)+')',raw)
        return re.sub(r'\by\b',lambda _:'('+tex(v)+')',raw)
    frows=[vector(P,Q),'('+substituted(P)+r')\,i+('+substituted(Q)+r')\,j',vector(pr,qr)]
    # Source direct linear fields omit the redundant reduction row.
    if f in ('rotation','shifted_circle','spiral','mixed_spiral'):frows=frows[:2]
    drows=[r'\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j',r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(u)+')i+'+r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(v)+')j',vector(du,dv)]
    product='('+vector(pr,qr)+r')\cdot ('+vector(du,dv)+')'
    component='('+tex(pr)+r')\cdot ('+tex(du)+')+('+tex(qr)+r')\cdot ('+tex(dv)+')'
    expanded=tex(s.expand(pr*du+qr*dv))
    dotrows=[product,component]
    if f=='mixed_spiral':
        four=[(p['a']*u,du),(p['b']*v,du),(p['c']*u,dv),(p['d']*v,dv)]
        dotrows.append('+'.join('('+tex(c)+r')\cdot ('+tex(d)+')' for c,d in four))
    if f in ('spiral','mixed_spiral'):dotrows.append(expanded)
    if f=='spiral':dotrows.append(tex(p['a']*T)+r'(\cos^2 t+\sin^2 t)')
    dotrows.append(tex(z))
    solution='We will use the formula\n\n'+block(r'\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.')+'\n\nAlong the curve $C,$ we have \n\n'+block('x='+tex(u)+r',\,y='+tex(v)+'.')+'\n\nTherefore,\n\n'+block(aligned('F(r(t))',frows))+"\n\nComputing $r'(t),$ we get \n\n"+block(aligned(r'r^{\prime}(t)',drows))+'\n\nTherefore,\n\n'+block(aligned(r'F(r(t))\cdot r^{\prime}(t)',dotrows))+'\n\nFinally, we can write the integral as follows:\n\n'+block(aligned(r'\int_C F(r)\cdot\mathrm{d}r',[r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t',integ(z,lo,hi)]))
    # A single complete method-derived bank. No first-valid distractor pool.
    exprs=[z,-z,s.expand(pr*du),s.expand(qr*dv),s.expand(pr+qr)]
    values=[integ(q,lo,hi) for q in exprs]
    return prompt,solution,values,0,['constructed dot product','reverse both derivative signs','omit second dot-product term','omit first dot-product term','omit both coordinate derivatives']


def scaled(raw,c):
    if c==1:return raw
    tail='.' if raw.endswith('.') else ''
    return '('+str(c)+')\\left('+raw.removesuffix('.')+r'\right)'+tail

def observed(f,p):
    """Complete source mathematical components are slots; only a genuine
    field scaling and interval endpoint vary. No source answer lookup branch."""
    src=SOURCE_BY_FAMILY[f];c=p['scale'];b=tex(s.sympify(p['upper']))
    prompt=src[':question/problem']
    match=re.search(r'F\(x,y\)=(.*?)\$ and',prompt)
    field=match.group(1);prompt=prompt[:match.start(1)]+scaled(field,c)+prompt[match.end(1):]
    # Replace the complete interval, never a short symbol across prose.
    prompt=re.sub(r't\\in \[0,.*?\]\?',lambda _:'t\\in [0,'+b+']?',prompt)
    solution=src[':question/worked-solution']
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
    # F(r(t)) component stages and scalar dot-product stages are complete masks.
    for idx in (2,4):
        original=blocks[idx]
        head,*rows=original.split(' & =')
        # Source continuation rows use the same &= token but retain \\\\ prefix.
        if c!=1:
            body=original
            def scale_stage(m):
                rhs=m.group(2)
                if idx==4 and r'\cdot ' in rhs and ',i' in rhs:
                    left,right=rhs.split(r'\cdot ',1)
                    rhs=scaled(left,c)+r'\cdot '+right
                else:rhs=scaled(rhs,c)
                return m.group(1)+rhs
            body=re.sub(r'( & =)(.*?)(?= \\\\  & =|\\end\{aligned\})',scale_stage,body,flags=re.S)
            solution=solution.replace(original,body)
    final=blocks[5]
    orig_b=r'\pi ' if f in ('rotation','shifted_circle','spiral') else '1'
    # Bounds are complete TeX arguments. Original exact spelling is retained.
    braw=orig_b if s.sympify(p['upper'])==(s.pi if orig_b!= '1' else 1) else b
    updated=final.replace('^{'+orig_b+'}','^{'+braw+'}')
    if c!=1:
        # Multiply the entire final displayed definite integral: no scalar evaluation.
        parts=updated.split(r' \\  & =')
        tail=parts[-1].removesuffix(r'\end{aligned}')
        parts[-1]=scaled(tail,c)+r'\end{aligned}'
        updated=r' \\  & ='.join(parts)
    solution=solution.replace(final,updated)
    values=[]
    for a in src[':question/answer-fields'][0][':answer-field/choices']:
        v=a[':answer/value'].replace('^{'+orig_b+'}','^{'+braw+'}')
        values.append(scaled(v,c))
    fieldsrc=src[':question/answer-fields'][0]
    correct=next(i for i,a in enumerate(fieldsrc[':answer-field/choices']) if a[':answer/id']==fieldsrc[':answer-field/correct'][':answer/id'])
    # Prompt original interval whitespace is a fixed source convention at default.
    if braw==orig_b:prompt=prompt.replace('t\\in [0,'+b+']?','t\\in [0,'+orig_b+']?')
    return prompt,solution,values,correct,['observed expression pattern; original error intent not recoverable']*5


def scalar_values(values):
    from importlib.machinery import SourceFileLoader
    module=SourceFileLoader('plane_setup_qa',str(ROOT/'math_parser.py')).load_module()
    return [module.integral(v)[3] for v in values]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout is supported')
    r=random.Random(seed)
    if profile:
        if profile not in PROFILES:raise ValueError('profile')
        implied=PROFILES[profile]
        if template and template!=implied:raise ValueError('profile/template mismatch')
        template=implied
    f=template or r.choice([f for f,l in TEMPLATES.items() if l==level])
    if f not in TEMPLATES or TEMPLATES[f]!=level:raise ValueError('template/level mismatch')
    raw=bool(profile and profile.startswith('observed_'))
    profile=profile or 'authored_'+f
    attempts=1 if parameters is not None or raw else 1000
    for _ in range(attempts):
        p=dict(parameters) if parameters is not None else ({'scale':1,'upper':str(s.pi if f in ('rotation','shifted_circle','spiral') else 1)} if raw else sample(f,r))
        try:
            validate_parameters(f,p,raw)
        except ValueError:
            if parameters is not None or raw:raise
            continue
        prompt,solution,values,correct,recipes=(observed if raw else authored)(f,p)
        if not raw:
            vals=scalar_values(values)
            if any(s.simplify(vals[i]-vals[j])==0 for i in range(5) for j in range(i)):
                if parameters is not None:raise ValueError('whole bank scalar collision')
                continue
        break
    else:raise ValueError('no eligible complete bank')
    payload={'version':VERSION,'difficulty':level,'prompt':prompt,'solution':solution,'bank':sorted(values)}
    content=digest(payload);qid=uid(content);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=answers[correct][':answer/id'];r.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    if raw:
        base=math_data(f,{'a':1,'b':1,'lower':'0','upper':p['upper']});P,Q,u,v,*_=base
        P,Q=p['scale']*P,p['scale']*Q
    else:P,Q,u,v,*_=math_data(f,p)
    task_integrand=s.trigsimp(s.expand(P.subs({X:u,Y:v})*s.diff(u,T)+Q.subs({X:u,Y:v})*s.diff(v,T)))
    task=digest([s.srepr(e) for e in (task_integrand,s.sympify(p.get('lower','0')),s.sympify(p['upper']))]+['supplied-parameterization-dot-product-setup'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':f,'bank_profile':profile,'seed':seed,'parameters':p,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':SOURCE_BY_FAMILY[f][':question/math-academy-id'] if f in FAMILIES else None,'origin':'observed-mask' if raw else 'authored-extension','evidence_only':raw,'eligible_for_learning':not raw,'difficulty_origin':'observed' if raw else ('authored missing level' if level!='easy' else 'authored bounds/bank with observed family'),'recipes':recipes,'recipe_values':[{'recipe':recipe,'value':value} for recipe,value in zip(recipes,values)],'mathematical_fingerprint':task,'content_fingerprint':content,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'response_criterion':'same stated bounds and integrand F(r(t)) dot rprime(t); no evaluation/change of variable','bank_equivalence_policy':'normal banks also conservatively reject coincident complete scalar values; raw preserves ambiguity','source_solution_repairs':[] if raw else (['restore j in exponential/root dot product'] if f=='exponential_root' else ['restore sin(t)cos(t) product and remove unmatched parenthesis'] if f=='spiral' else [])}}

# EASY: five observed families, signed coefficients of magnitude 1..4;
# normal root intervals exclude the singular endpoint, and trig limits avoid
# equal scalar distractors. All source easy labels remain easy during raw replay.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): two unequal monomial powers 2..4, two coordinate power
# derivatives, two substituted squares/products. Canonical and source-polynomial
# masks anchor this workload; no evaluated antiderivative is requested.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): observed product-rule spiral with two mixed linear field
# components, four nonzero field coefficients, four scalar products and their
# distribution; unequal diagonal/cross coefficients prevent easy cancellation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0];g=r['generation']
    result=['## '+g['origin']+' — '+q[':question/difficulty'].split('/')[-1],f"Template `{g['template']}`, profile `{g['bank_profile']}`; eligible: {g['eligible_for_learning']}.",'',q[':question/problem'],'']
    for a in f[':answer-field/choices']:result.append('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
    return '\n'.join(result+['','Worked solution','',q[':question/worked-solution']])
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=PROFILES);ap.add_argument('--format',choices=('json','markdown'),default='markdown');a=ap.parse_args()
    if a.count<1:ap.error('positive count required')
    if a.difficulty=='all' and (a.template or a.profile):ap.error('template/profile requires one difficulty')
    records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
