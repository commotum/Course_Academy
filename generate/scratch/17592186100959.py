#!/usr/bin/env python3
"""Verify three proposed first-order ODE solutions; steps 3–7 only.

math basis 1356; source/component-mask evidence in the private sibling folder.
11 observed moderate questions and their complete five-choice radio banks replay
through the ordinary public API. Source component masks parameterize a dependent
scale c: proposed y=c*f, derivatives c*f', ODE c*F(x,y/c), and every intermediate
comparison multiplied by c. This preserves the original ordered operations rather
than returning literal question records. The native subset answer is computed from
all three derivatives, including domain eligibility and identity over the domain.
Source scale variation is useful fidelity evidence but NOT counted as substantive
variety: canonical task fingerprints divide out common dependent scaling.

Easy (authored): three simple exponentials with unit inner slope and constant
shift, checking identity for all real x. Moderate: power, exponential and trig
families with familiar integer chain/power factors. Hard (authored): three log
candidates substituted into a nonlinear exponential RHS, or three quadratic
candidates into an affine y/x RHS; distinct exact substitution/reduction workloads.
Hard is an authored design claim; the source labels all families moderate. No
ODE is solved, and no initial condition or extra curriculum branch is introduced.
Every difficulty has bounded explicit inputs, exact SymPy arithmetic, deterministic
sampling, shared fixed solution prose and complete five-choice subset banks.
No plots, database integration, feedback, engine changes, or registrations.
"""
from pathlib import Path
import argparse, hashlib, json, random, re, sys, uuid
import sympy as s
PRIVATE=Path(__file__).with_suffix('')
sys.path.insert(0,str(PRIVATE))
from mathparse import parse, X, Y
KP=17592186100959
TITLE='Identifying Solutions to First-Order Differential Equations'
VERSION='1.0.0'
RAW=json.loads((PRIVATE/'source.json').read_text())
REC=RAW['record']
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
OPENING="For a function $f(x)$ to be a solution to a differential equation, it must satisfy the equation for all values of $x$ in the equation's domain.\n\nWe check each proposed solution by differentiating and substituting it into the original equation. \n\n"
D=r'\frac{\text{d}y}{\text{d}x}'
LABELS={0:'None',1:'I only',2:'II only',4:'III only',3:'I and II only',5:'I and III only',6:'II and III only',7:'I, II, and III'}
FAMILIES={'easy':('exp',),'moderate':('exp','power','sin','cos'),'hard':('log','affine')}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(v)))
def tex(v):return s.latex(v).replace('\\log','\\ln')
def zero(v):return s.simplify(s.trigsimp(s.expand_log(v,force=True)))==0

def source_parts(q):
    prompt=q[':question/problem']
    eq=re.search(r'\$\$\n(.*?)\n\$\$',prompt,re.S)[1]
    rhs=eq.split('=',1)[1].split(r'\,x')[0].rstrip('.')
    candidates=re.findall(r'- \$y=(.*?)\$',prompt)
    return rhs,candidates

def truth(rhs,candidates):
    """Global identity, not equality at one test point. Candidate domain must
    include each allowed interval of the ODE's stated/common real domain.
    Log candidates carry x>0; power candidates integer exponents; trig poles are
    excluded by the cot/tan ODE. These closed families have no other branch.
    """
    flags=[zero(s.diff(f,X)-rhs.subs(Y,f)) for f in candidates]
    return sum(2**i for i,v in enumerate(flags) if v),flags

def scaled_component(raw,c,ode=False):
    """A complete mathematical component slot, never a blind prose replacement.
    The unity specialization renders its original notation, including optional
    parentheses and source row omissions. Nonunity stages keep their structure.
    """
    if c==1:return raw
    if ode:raw=re.sub(r'(?<![A-Za-z])y(?![A-Za-z])',lambda _:r'\left(\frac{y}{'+str(c)+r'}\right)',raw)
    if raw.strip()=='0':return raw
    return str(c)+r'\left('+raw+r'\right)'

def render_source_math(block,c):
    if r'\begin{aligned}' in block:
        before,rest=block.split(r'\begin{aligned}',1);body,after=rest.split(r'\end{aligned}',1)
        rows=body.split(r'\\');new=[]
        for row in rows:
            lhs,right=row.split('&',1)
            m=re.match(r'(\s*)(\\overset\{\?\}\{=\}|\\ne|=)(.*)',right,re.S)
            assert m,row
            spacing,relation,rhs=m.groups()
            # Punctuation/ticks are fixed components, not part of an expression.
            m2=re.match(r'(.*?)([.]?\\,[✓]|[.]?\\,\\times\s*|[.]?)$',rhs,re.S)
            val,suffix=m2.groups()
            formal='d}y' in lhs
            lhs2=lhs if formal else scaled_component(lhs,c)
            rhs2=scaled_component(val,c,ode=formal)
            new.append(lhs2+'&'+spacing+relation+rhs2+suffix)
        return before+r'\begin{aligned}'+r'\\'.join(new)+r'\end{aligned}'+after
    if '=' in block and ('y=' in block or 'd}y' in block):
        lhs,rhs=block.split('=',1)
        # Prompt domain is not scaled; punctuation remains exact.
        m=re.match(r'(.*?)(,\\,x.*|\\,x.*|[.,]?\s*)$',rhs,re.S)
        val,suffix=m.groups()
        return lhs+'='+scaled_component(val,c,ode=('d}y' in lhs and 'y' in val))+suffix
    return block

def source_render(text,c):
    return re.sub(r'(\$\$|\$)(.*?)(\1)',lambda m:m[1]+render_source_math(m[2],c)+m[3],text,flags=re.S)

def source_instance(profile,parameters):
    if profile not in SOURCES:raise ValueError('Unknown observed bank profile')
    p={'scale':1} if parameters is None else dict(parameters)
    if set(p)!={'scale'} or type(p['scale'])!=int or p['scale']==0 or abs(p['scale'])>6:raise ValueError('Source scale must be a nonzero integer of magnitude <=6')
    q=SOURCES[profile];c=p['scale'];rhs0,fs0=source_parts(q)
    rhs=c*parse(rhs0).subs(Y,Y/c);fs=[c*parse(f) for f in fs0]
    mask,flags=truth(rhs,fs)
    bank=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
    if LABELS[mask] not in bank:raise ValueError('Complete observed bank does not contain computed criterion')
    prompt=source_render(q[':question/problem'],c);solution=source_render(q[':question/worked-solution'],c)
    return p,rhs,fs,prompt,solution,bank,mask,{'origin':'observed_component_mask','source_id':profile,'eligible_for_learning':False,'evidence_only':True,'notation_limitation':'Raw source uses equality followed by × on failed comparisons in q-141091/q-141093/q-141103; authored output uses query/nonidentity relations.'}

# Easy: authored unit-slope exponentials. Three independent tests at one workload.
def sample_easy(rng,family):
    k=rng.choice([-1,1]);cs=[]
    for i in range(3):cs.append([rng.choice([-3,-2,-1,1,2,3]),rng.choice([-1,1]),rng.choice([-2,-1,0,0,0,1,2])])
    return {'k':k,'candidates':cs}
# Moderate: observed methods, signed bounded coefficients and integer factors.
def sample_moderate(rng,family):
    k=rng.choice([-5,-4,-3,-2,2,3,4,5]) if family in ('exp','power') else rng.choice([2,3,4])
    cs=[]
    for i in range(3):
        b=rng.choice([k,k,k-1,k+1]) if family in ('exp','power') else k
        cs.append([rng.choice([-4,-3,-2,-1,1,2,3,4]),b,rng.choice([-2,-1,0,0,0,1,2])])
    return {'k':k,'candidates':cs}
# Hard: authored same-KP nonlinear substitution and affine polynomial reduction.
def sample_hard(rng,family):
    if family=='log':
        a=rng.choice([2,3,4]);b=s.Rational(1,a)
        return {'a':a,'b':str(b),'candidates':[[rng.choice([a,a,a-1,-a]),0,rng.choice([-1,0,0,0,1])] for _ in range(3)]}
    n=rng.choice([2,3,4]);a=rng.choice([-3,-2,-1,1,2,3])
    return {'n':n,'a':a,'candidates':[[rng.choice([-3,-2,-1,1,2,3]),rng.choice([a,a,a+1]),rng.choice([-1,0,0,0,1])] for _ in range(3)]}

def authored_math(level,family,p):
    if family not in FAMILIES[level]:raise ValueError('Template outside authored level scope')
    expect={'k','candidates'} if family in ('exp','power','sin','cos') else {'a','b','candidates'} if family=='log' else {'n','a','candidates'}
    if set(p)!=expect:raise ValueError('Invalid parameter keys')
    cs=p['candidates']
    if not isinstance(cs,list) or len(cs)!=3 or any(not isinstance(c,list) or len(c)!=3 or any(type(v)!=int for v in c) for c in cs):raise ValueError('Three integer candidate triples required')
    if family in ('exp','power','sin','cos'):
        k=p['k'];valid=type(k)==int and (k in (-1,1) if level=='easy' else 2<=abs(k)<=5 if family in ('exp','power') else 2<=k<=4)
        if not valid:raise ValueError('Level-specific k bound')
        if any(a==0 or abs(a)>(3 if level=='easy' else 4) or abs(c)>2 for a,b,c in cs):raise ValueError('Candidate coefficient/offset bound')
        if any(b not in (-1,1) for a,b,c in cs) and level=='easy':raise ValueError('Easy slopes must be unit')
        if level=='moderate' and any(abs(b)>6 or b==0 for a,b,c in cs):raise ValueError('Moderate slope/power bound')
        if family in ('sin','cos') and any(b!=k for a,b,c in cs):raise ValueError('Trig candidates use the printed common slope')
        rhs=k*Y if family=='exp' else k*Y/X if family=='power' else k*Y*s.cot(k*X) if family=='sin' else -k*Y*s.tan(k*X)
        fn=s.exp if family=='exp' else (lambda z:s.sin(z)) if family=='sin' else s.cos
        fs=[a*(X**b if family=='power' else fn(b*X))+c for a,b,c in cs]
        domain='x != 0' if family=='power' else 'sin(k*x) != 0' if family=='sin' else 'cos(k*x) != 0' if family=='cos' else 'all real x'
    elif family=='log':
        a=p['a'];b=s.Rational(p['b'])
        if type(a)!=int or a not in (2,3,4) or b!=s.Rational(1,a):raise ValueError('Hard log coefficient must be 2..4 and b=1/a')
        if any(v==0 or abs(v)>5 or spare!=0 or abs(c)>1 for v,spare,c in cs):raise ValueError('Hard log candidate bound')
        rhs=a*s.exp(-b*Y);fs=[v*s.log(X)+c for v,_,c in cs];domain='x > 0'
    else:
        n,a=p['n'],p['a']
        if type(n)!=int or n not in (2,3,4) or type(a)!=int or a==0 or abs(a)>3:raise ValueError('Hard affine coefficient bounds')
        if any(v==0 or abs(v)>3 or w==0 or abs(w)>4 or abs(c)>1 for v,w,c in cs):raise ValueError('Hard affine requires both nonzero polynomial terms')
        rhs=n*Y/X+(1-n)*a;fs=[v*X**n+w*X+c for v,w,c in cs];domain='x != 0'
    if any(zero(fs[i]-fs[j]) for i in range(3) for j in range(i)):raise ValueError('Equivalent candidate functions reject the whole instance')
    return rhs,fs,domain

def substituted_tex(family,p,f):
    ft=r'\left('+tex(f)+r'\right)'
    if family=='exp':return str(p['k'])+r'\cdot '+ft
    if family=='power':return r'\frac{'+str(p['k'])+r'\cdot '+ft+'}{x}'
    if family=='sin':return str(p['k'])+r'\cdot '+ft+r'\cot\left('+tex(p['k']*X)+r'\right)'
    if family=='cos':return '-'+str(p['k'])+r'\cdot '+ft+r'\tan\left('+tex(p['k']*X)+r'\right)'
    if family=='log':return str(p['a'])+r'e^{-'+tex(s.Rational(p['b']))+r'\cdot '+ft+'}'
    return r'\frac{'+str(p['n'])+r'\cdot '+ft+'}{x}'+('+' if (1-p['n'])*p['a']>0 else '')+str((1-p['n'])*p['a'])

def authored_render(family,p,rhs,fs,domain,mask,flags):
    restriction='' if domain=='all real x' else r',\,x\ne 0' if domain=='x != 0' else r',\,x>0' if domain=='x > 0' else r',\,\sin('+tex(p['k']*X)+r')\ne0' if family=='sin' else r',\,\cos('+tex(p['k']*X)+r')\ne0'
    prompt='Consider the differential equation\n\n$$\n'+D+'='+tex(rhs)+restriction+'.\n$$\n\n Which of the following is a solution to this equation?\n\n'+'\n'.join('- $y='+tex(f)+'$' for f in fs)
    solution=OPENING.replace("the equation's domain","the stated domain")
    for f,ok in zip(fs,flags):
        derivative=s.diff(f,X);result=s.simplify(s.trigsimp(s.expand_log(rhs.subs(Y,f),force=True)))
        solution+='- Differentiating $y='+tex(f)+',$ we get $'+D+'='+tex(derivative)+'.$ Substituting into the original equation, we get\n\n$$\n'
        rows=[D+' & ='+tex(rhs),tex(derivative)+r' & \overset{?}{=}'+substituted_tex(family,p,f)]
        if family=='log':
            v,_,c=p['candidates'][fs.index(f)]
            # Formal logarithm rule stage remains visible, before exponential cancellation.
            rows.append(tex(derivative)+r' & \overset{?}{=}'+str(p['a'])+r'e^{'+tex(-s.Rational(p['b'])*c)+'}'+r'\cdot e^{\ln\left('+tex(X**(-s.Rational(p['b'])*v))+r'\right)}')
        rows.append(tex(derivative)+(' & =' if ok else r' & \overset{?}{=}')+tex(result))
        if not ok:rows.append(tex(s.simplify(derivative-result))+r' & \not\equiv 0')
        else:rows[-1]+=r'.\,✓'
        solution+=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
        solution+=('This statement is *true*. Therefore, the function $y='+tex(f)+'$ *is* a solution to our differential equation.\n\n' if ok else 'This statement is *not true* for all $x.$ Therefore, the function $y='+tex(f)+'$ is *not* a solution to our differential equation.\n\n')
    solution+='Therefore, the correct answer is "'+LABELS[mask]+'."'
    return prompt,solution


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in FAMILIES:raise ValueError('Invalid difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio layout is supported')
    rng=random.Random(seed)
    if profile in SOURCES:
        if level!='moderate' or template not in (None,'source_'+profile):raise ValueError('Observed sources are moderate and require their component template')
        p,rhs,fs,prompt,solution,bank,mask,meta=source_instance(profile,parameters)
        template='source_'+profile;domain='x > 0' if any(f.has(s.log) for f in fs) else 'sin(k*x) != 0' if rhs.has(s.cot) else 'cos(k*x) != 0' if rhs.has(s.tan) else 'x != 0' if rhs.has(1/X) else 'all real x'
    else:
        if profile not in (None,'authored_subset'):raise ValueError('Unknown profile')
        template=template or rng.choice(FAMILIES[level]);profile='authored_subset'
        if template not in FAMILIES[level]:raise ValueError('Unknown or wrong-level template')
        for attempt in range(1000):
            p=dict(parameters) if parameters is not None else globals()['sample_'+level](rng,template)
            try:rhs,fs,domain=authored_math(level,template,p);mask,flags=truth(rhs,fs)
            except ValueError:
                if parameters is not None:raise
                continue
            break
        else:raise ValueError('No eligible complete instance')
        prompt,solution=authored_render(template,p,rhs,fs,domain,mask,flags)
        # Entire authored bank is selected at once from the seven wrong semantic subsets.
        brng=random.Random(digest([template,p,'bank']))
        wrong=brng.sample([LABELS[m] for m in range(8) if m!=mask],4)
        bank=[LABELS[mask]]+wrong
        meta={'origin':'authored_missing_level' if level!='moderate' else 'authored_same_method','eligible_for_learning':True,'evidence_only':False}
    # Canonical task identity excludes seed, bank, profile, variable aliases and
    # common dependent scaling (source scale c is incidental for diversity).
    coeffs=[term.as_coeff_Mul()[0] for f in fs for term in s.Add.make_args(s.expand(f))]
    scale=s.Rational(s.gcd_list(coeffs))*s.sign(coeffs[0])
    if not scale:scale=s.Integer(1)
    canonical=[s.srepr(s.simplify(rhs.subs(Y,Y*scale)/scale))]+sorted(s.srepr(s.simplify(f/scale)) for f in fs)
    domain_key=['positive'] if domain=='x > 0' else ['nonzero'] if domain=='x != 0' else ['cot poles',*[s.srepr(a.args[0]) for a in rhs.atoms(s.cot)]] if rhs.has(s.cot) else ['tan poles',*[s.srepr(a.args[0]) for a in rhs.atoms(s.tan)]] if rhs.has(s.tan) else ['real']
    fp=digest([canonical,domain_key]);content=digest([VERSION,prompt,solution,sorted(bank)])
    qid=uid(content);fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
    rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+LABELS[mask])]}
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':template,'bank_profile':profile,'seed':seed,'parameters':p,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'recipe':'complete subset after three derivative/substitution identity tests','domain':domain,'mathematical_fingerprint':fp,'content_hash':content,'source':{k:RAW[k] for k in ('database','basis','lineage')},**meta}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def preview_label(r):
    """Review metadata stays outside the captured learner question strings."""
    level=r['question'][':question/difficulty'].rsplit('/',1)[1]
    code={'easy':'E','moderate':'M','hard':'H'}[level]
    meta=r['generation']
    if meta['evidence_only']:
        origin='Observed original' if meta['parameters'].get('scale')==1 else 'Observed source mask variant'
        origin+='; evidence only'
    else:
        origin='Authored missing level extension' if meta['origin']=='authored_missing_level' else 'Authored same method variant'
    return level.title()+' ('+code+') | '+origin

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    correct=f[':answer-field/correct'][1]
    answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
    bank='\n'.join('* '+a[':answer/value']+(' **(correct)**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])
    return '**Difficulty and origin:** '+preview_label(r)+'\n\n'+q[':question/problem']+'\n\n'+bank+'\n\n**Correct answer:** '+answer+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    rows=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (FAMILIES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
