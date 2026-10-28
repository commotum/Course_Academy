#!/usr/bin/env python3
"""Portable monomial antiderivatives with authored three-band progression.

Original draft source templates and complete bank recipes are retained for exact,
evidence-only replay. Easy production uses symmetric five-choice banks. Moderate constructs the
primitive; hard also differentiates a proposed primitive. Integrands remain
nonnegative integer monomials, with no radical or reciprocal rewrite.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
KP_ID=17592186064167
KP_UUID='f2a4550c-7ed7-58aa-8928-23dd1cfd0cd7'
TITLE='Finding the Antiderivative of a Monomial'
VERSION='monomial-power-rule-portable-v5-format-audit-9122-v1'
ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'source-cases.json').read_text())
X,C=sp.symbols('x C',real=True)
DOMAINS={'easy':tuple(range(21))}
SUPPORTED_LEVELS=tuple(DOMAINS)
GENERATOR_UUID= str(uuid.uuid5(uuid.NAMESPACE_URL, KP_UUID+'/question-generator'))
TEMPLATES=('integral_spaced','integral_thin','function','constant','legacy_x','legacy_power','function_unicode','function_unicode_compact','canonical_power')
SOURCE_SPECS={'q-2005':('legacy_x',1),'q-2022':('legacy_power',4),'q-113665':('integral_spaced',20),'q-113670':('function',17),'q-66126':('constant',0),'q-71121':('integral_thin',10)}
SOURCE_SPECS.update({'q-113668':('function_unicode',13),'q-29994':('function_unicode_compact',4),'e-364':('canonical_power',2)})
BANK_PROFILES=('authored_power','observed_2005','observed_2022','observed_113668','observed_29994','observed_113665')
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def power(n,braced=True):
    return '{x}^{'+str(n)+'}' if braced else 'x^{'+str(n)+'}'
def primitive(n,braced=True):
    return 'x+C' if n==0 else r'\frac{'+power(n+1,braced)+'}{'+str(n+1)+'}+C'
def aligned(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def power_solution(n,template):
    if template in ('function_unicode','function_unicode_compact'):
        value=power_solution(n,'function').replace("{F}^{'}",'{F}^{′}')
        if template=='function_unicode_compact': value=value.replace(r'\cdot '+str(n+1)+r'\,',r'\cdot '+str(n+1))
        return value
    if template=='canonical_power':
        value=power_solution(n,'integral_thin');a=r'\dfrac{x^{'+str(n)+'+1}}{'+str(n)+r'+1} + C';b=r'\dfrac{x^'+str(n+1)+'}{'+str(n+1)+'}+C'
        before=value.split("\n\nLet's check")[0]
        first='We apply the power rule with $n='+str(n)+'$, and we get\n\n$$\n'+r'\int x^'+str(n)+r' \,\textrm d x = '+a+' = '+b+'.\n$$'
        return first+value[len(before):]
    m=n+1; a=primitive(n); base=r'\frac{'+power(m)+'}{'+str(m)+'}'
    check=[r'\frac{\text{d}}{\text{d}x}('+a+') & =',r'\frac{\text{d}}{\text{d}x}('+base+r')+\frac{\text{d}}{\text{d}x}(C) & =',r'\frac{1}{'+str(m)+r'}\frac{\text{d}}{\text{d}x}('+power(m)+')+0 & =',r'\frac{1}{'+str(m)+r'}\cdot '+str(m)+(r'\,' if template=='function' else '')+power(n)+' & =',power(n)+r'\,✓']
    formal=r'\frac{'+power(str(n)+'+1')+'}{'+str(n)+'+1}+C'
    opening=f'We apply the power rule with $n={n}$, and we get\n\n'
    if template=='function':
        solution="Remember that integration is the opposite of differentiation. So, if ${F}^{'}(x)=f(x),$ then integrating both sides of this equation gives\n\n"+aligned(["{F}^{'}(x) & =f(x)",r"\int {F}^{'}(x)\,\text{d}x & =\int f(x)\,\text{d}x",r'F(x) & =\int f(x)\,\text{d}x.'])+'\n\n'+opening+aligned([r'F(x) & =\int f(x)\,\text{d}x',r' & =\int '+power(n)+r'\,\text{d}x',' & ='+formal,' & ='+a+'.'])
    else:
        solution=opening+'$$\n'+r'\int '+power(n)+r'\,\text{d}x='+formal+'='+a+'.\n$$'
    return solution+"\n\nLet's check by differentiating:\n\n"+aligned(check)
def constant_solution():
    return "If we write the integrand as a power of $x$, we have ${x}^{0}=1.$ Therefore, we can use the power rule with $n=0$ and we get\n\n"+aligned([r'\int 1\,\text{d}x & =\int {x}^{0}\,\text{d}x',r' & =\frac{{x}^{0+1}}{0+1}+C',r' & =x+C.'])+"\n\nLet's check by differentiating:\n\n"+aligned([r'\frac{\text{d}}{\text{d}x}(x+C) & =',r'\frac{\text{d}}{\text{d}x}(x)+\frac{\text{d}}{\text{d}x}(C) & =',r'1+0 & =',r'1\,✓'])
def prompt(n,template,raw=False):
    if template=='canonical_power': return r'Calculate $\displaystyle \int x^'+str(n)+r' \,\textrm d x.$'
    if template in ('function_unicode','function_unicode_compact'):return prompt(n,'function',raw).replace("{F}^{'}",'{F}^{′}')
    if template=='legacy_x' and raw: return 'Calculate $\\int'+('x' if n==1 else power(n,False))+'dx$.'
    if template=='legacy_power' and raw: return 'Calculate $\\int'+power(n,False)+'dx$.'
    if template=='constant': return r'Calculate $\int 1\,\text{d}x.$'
    if template=='function': return "Calculate $F(x)$ given that $f(x)="+power(n)+"$ and ${F}^{'}(x)=f(x).$"
    return 'Calculate $\\int '+power(n)+r'\,\text{d}x.$'
def bank(n,profile):
    """Each recipe set is complete; never choose/fill individual distractors."""
    m=n+1
    good=(primitive(n,False),X**m/sp.Integer(m)+C,'power_rule')
    if profile=='observed_2005':
        vals=[(str(m)+power(m,False),m*X**m,'multiply_by_successor_omit_C'),(r'\frac{'+power(m,False)+'}{'+str(m)+'} + C',X**m/sp.Integer(m)+C,'power_rule'),(str(m)+' + C',m+C,'drop_x'),(r'\frac{'+power(m,False)+'}{'+str(m)+'}',X**m/sp.Integer(m),'omit_C'),(power(m,False)+' + C',X**m+C,'omit_division')]
    elif profile=='observed_2022':
        vals=[(power(m,False)+' + C',X**m+C,'omit_division'),(str(n)+power(n-1,False)+' + C',n*X**(n-1)+C,'differentiate'),(r'\frac{'+power(n,False)+'}{'+str(n)+'} + C',X**n/sp.Integer(n)+C,'do_not_increment'),(r'\frac{'+power(m,False)+'}{'+str(m)+'} + C',X**m/sp.Integer(m)+C,'power_rule'),(power(n-1,False)+' + C',X**(n-1)+C,'decrement_omit_factor')]
    elif profile=='observed_113665':
        vals=[(primitive(n),X**m/sp.Integer(m)+C,'power_rule'),(str(m)+power(n-1)+'+C',m*X**(n-1)+C,'decrement_then_multiply_successor'),(r'\frac{'+power(m)+'}{'+str(n-1)+'}+C',X**m/sp.Integer(n-1)+C,'increment_then_divide_predecessor'),(r'\frac{'+power(n-1)+'}{'+str(n-1)+'}+C',X**(n-1)/sp.Integer(n-1)+C,'decrement_then_divide_predecessor'),(str(n)+power(m)+'+C',n*X**m+C,'increment_then_multiply_n')]
    elif profile=='observed_113668':
        vals=[(r'\frac{'+power(n-1)+'}{'+str(n)+'}+C',X**(n-1)/sp.Integer(n)+C,'decrement_then_divide_n'),(primitive(n),X**m/sp.Integer(m)+C,'power_rule'),(r'\frac{'+power(n-1)+'}{'+str(n-1)+'}+C',X**(n-1)/sp.Integer(n-1)+C,'decrement_then_divide_predecessor'),(power(m)+'+C',X**m+C,'omit_division'),(str(n)+power(m)+'+C',n*X**m+C,'increment_then_multiply_n')]
    elif profile=='observed_29994':
        vals=[(str(n)+power(m)+'+C',n*X**m+C,'increment_then_multiply_n'),(r'\frac{'+power(n)+'}{'+str(n)+'}+C',X**n/sp.Integer(n)+C,'do_not_increment'),(str(m)+power(m)+'+C',m*X**m+C,'multiply_instead_of_divide'),(primitive(n),X**m/sp.Integer(m)+C,'power_rule'),(r'\frac{'+power(n)+'}{'+str(m)+'}+C',X**n/sp.Integer(m)+C,'do_not_increment_exponent')]
    else:
        vals=[good,(power(m,False)+'+C',X**m+C,'omit_division'),(r'\frac{'+power(n,False)+'}{'+str(m)+'}+C',X**n/sp.Integer(m)+C,'do_not_increment_exponent'),(r'\frac{'+power(m+1,False)+'}{'+str(m+1)+'}+C',X**(m+1)/sp.Integer(m+1)+C,'increment_twice'),(str(m)+power(m,False)+'+C',m*X**m+C,'multiply_instead_of_divide')]
    return vals
@lru_cache(maxsize=None)
def family_equivalent(a,b):
    # Full families are equal precisely when their nonconstant parts agree and
    # both permit an arbitrary C. Rescale/shift of C is immaterial; missing C
    # is a fixed primitive, not the full family required by an indefinite integral.
    da=sp.diff(a,C);db=sp.diff(b,C)
    return bool(da!=0)==bool(db!=0) and sp.expand(sp.diff(a-b,X))==0

def replay_generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if type(seed) is not int: raise ValueError('seed must be a builtin int')
    if level not in DOMAINS: raise ValueError('Unknown difficulty')
    raw=bool(profile and profile.startswith('raw:'))
    sid=profile[4:] if raw else None
    if raw:
        if sid not in SOURCE_SPECS: raise ValueError('Unknown raw source profile')
        st,sn=SOURCE_SPECS[sid]
        if template and template!=st: raise ValueError('Profile/template mismatch')
        template=st
    else: sn=None
    if template is None and not raw:
        if parameters is None:
            sample_domain=tuple(v for v in DOMAINS[level] if (v>0 or field_type!='radio' and profile not in ('observed_2005','observed_2022','observed_113668','observed_29994','observed_113665')) and (v>=2 or profile not in ('observed_2022','observed_113668','observed_29994','observed_113665')))
            parameters={'n':random.Random(seed).choice(sample_domain)}
        template='constant' if parameters.get('n')==0 else 'integral_thin'
    template=template or 'integral_thin'
    if template not in TEMPLATES: raise ValueError('Unknown template')
    if template=='canonical_power' and not raw: raise ValueError('Canonical fieldless presentation is evidence-only')
    if field_type not in (None,'radio','blank'): raise ValueError('Unsupported field type')
    if raw and field_type is not None: raise ValueError('Raw field layout is fixed')
    rng=random.Random(seed)
    if parameters is None:
        n=sn if raw else 0 if template=='constant' else rng.choice(tuple(v for v in DOMAINS[level] if v>0 and (v>=2 or profile not in ('observed_2022','observed_113668','observed_29994','observed_113665'))))
    else:
        if set(parameters)!={'n'} or type(parameters['n']) is not int: raise ValueError('Parameters require integer n only')
        n=parameters['n']
    if n not in DOMAINS[level]: raise ValueError('Exponent violates documented level workload')
    if template=='constant' and n!=0 or template!='constant' and n==0: raise ValueError('Template exponent constraint')
    if raw and level!='easy': raise ValueError('Raw sources use supported authored easy assignment')
    chosen=({'q-113665':'observed_113665','q-2005':'observed_2005','q-2022':'observed_2022','q-113668':'observed_113668','q-29994':'observed_29994'}.get(sid)) if raw else profile or 'authored_power'
    if chosen and chosen not in BANK_PROFILES: raise ValueError('Unknown bank profile')
    if chosen in ('observed_2022','observed_113668','observed_29994','observed_113665') and n<2: raise ValueError('Complete observed bank requires n>=2')
    kind=('radio' if chosen else None) if raw else field_type or ('blank' if template=='constant' else 'radio')
    sol=constant_solution() if n==0 else power_solution(n,'integral_thin' if template.startswith('legacy') else template)
    q={':question/problem':prompt(n,template,raw)}
    if raw:
        if sid not in ('q-2005','q-2022'):
            if sid!='e-364':q[':question/difficulty']=':question.difficulty/easy'
            q[':question/worked-solution']=sol
    else:
        q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
        if kind=='blank': q[':question/problem']+='\n\n{{answer}}'
        elif chosen=='observed_2005': q[':question/problem']+=' Include the arbitrary constant of integration.'
    vals=bank(n,chosen) if kind=='radio' else [(primitive(n,False),X**(n+1)/sp.Integer(n+1)+C,'power_rule')] if kind=='blank' else []
    # Reject complete banks before shuffling, construction or grading.
    for i,(_,a,_) in enumerate(vals):
        if any(family_equivalent(a,b) for _,b,_ in vals[:i]): raise ValueError('Ambiguous complete bank')
    if n==0 and kind=='radio' and chosen=='authored_power':
        # n=0 makes division omission equivalent; use a separate complete bank
        # for constant questions, selected by the template before construction.
        raise ValueError('Constant template requires blank field')
    identity={'version':VERSION,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'difficulty':q.get(':question/difficulty'),'kind':kind,'bank':sorted(v for v,_,_ in vals),'raw_missing_correct':raw}
    cid=digest(identity); q[':question/id']=uid(cid)
    if kind:
        fid=uid(cid+'/field'); answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v,_,_ in vals]
        f={':answer-field/id':fid,':answer-field/key':'selection' if kind=='radio' else 'answer',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
        if not raw or sid in ('q-113665','q-113668','q-29994'):
            correct=next(a[':answer/id'] for a,(_,_,r) in zip(answers,vals) if r=='power_rule');f[':answer-field/correct']=[':answer/id',correct]
        rng.shuffle(answers) if kind=='radio' else None
        q[':question/answer-fields']=[f]
    result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'n':n},'bank_profile':profile or chosen,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'difficulty_origin':'observed' if raw and sid not in ('q-2005','q-2022','e-364') else 'authored' if level=='easy' else 'authored; uncalibrated same-method label','domain':'x real','mathematical_fingerprint':digest({'integrand':str(X**n),'response':'complete primitive family'}),'content_fingerprint':cid,'recipes':[r for _,_,r in vals]}}
    return result


# Public portable production interface. No incomplete raw record can enter a batch.
from integral_display import display_integral
from math_format import normalize_prose, normalize_tex, validate_generated_record
SUPPORTED_LEVELS=('easy','moderate','hard')
CASES=('lower_lower','lower_upper','upper_lower','upper_upper')

def production_bank(n, case):
    target,surplus=case.split('_');m=n+1
    if target=='upper' and n==0 or target=='lower' and n==20:
        raise ValueError('Target must keep both integrands of its bank inside n=0..20')
    p=m if target=='lower' else m-1;q=p+1
    extra=p if surplus=='lower' else q
    vals=[]
    for exponent,divisor in ((p,p),(p,q),(q,q),(q,p)):
        good=exponent==m and divisor==m
        role='power_rule' if good else 'other_integrand_family' if exponent==divisor else 'cross_divisor'
        numerator='x' if exponent==1 else power(exponent,False)
        tex=numerator if divisor==1 else r'\frac{'+numerator+'}{'+str(divisor)+'}'
        vals.append((tex+'+C',X**exponent/sp.Integer(divisor)+C,role))
    if p==1:
        # Omitting division by one duplicates a matched/cross choice. Keep the
        # boundary bank symmetric in its two eligible targets with a distinct
        # multiplication distractor instead.
        vals.append(('2'+('x' if extra==1 else power(extra,False))+'+C',2*X**extra+C,'multiply_instead_of_divide'))
    else:
        vals.append((power(extra,False)+'+C',X**extra+C,'omit_division'))
    return vals

def production_solution(n, template):
    m=n+1
    integrand='1' if n==0 else 'x' if n==1 else power(n,False)
    integral=r'\int '+integrand+r'\,\mathrm{d}x'
    introduction=("Integration reverses differentiation, so $F'(x)=f(x)$ gives $F(x)=\\int f(x)\\,\\mathrm{d}x$.\n\n" if template=='function' else '')
    if n==0: introduction+='Write $1=x^0$.\n\n'
    introduction+='Apply the power rule with $n='+str(n)+'$ and include an arbitrary constant $C$:\n\n'
    result=primitive(n,False)
    formal=r'\frac{x^{'+str(n)+'+1}}{'+str(n)+'+1}+C'
    rows=[('F(x)&=' if template=='function' else '')+integral+('' if template=='function' else '&')+'='+formal,r'&='+result+'.']
    # Both presentations keep equality in the same alignment column.
    if template=='function': rows=[r'F(x)&='+integral,r'&='+formal,r'&='+result+'.']
    check=[r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+result+r'\right)&='+r'\frac{1}{'+str(m)+r'}\cdot '+str(m)+('' if n==0 else 'x' if n==1 else power(n,False))+'+0',r'&='+integrand+'.']
    return introduction+aligned(rows)+'\n\nCheck by differentiating:\n\n'+aligned(check)

def generate_easy(level='easy',seed=0,template=None,parameters=None,case=None):
    if level!='easy': raise ValueError('Unsupported difficulty: '+level)
    if type(seed) is not int: raise ValueError('seed must be an integer')
    rng=random.Random(seed)
    # A requested zero/maximum leaves only the lower/upper assignment eligible.
    eligible=CASES
    if parameters is not None:
        if set(parameters)!={'n'} or type(parameters['n']) is not int or not 0<=parameters['n']<=20:
            raise ValueError('Parameters require integer n in 0..20 only')
        if parameters['n']==0: eligible=CASES[:2]
        elif parameters['n']==20: eligible=CASES[2:]
    case=case or rng.choice(eligible) # Decision assignment precedes numerical sampling.
    if case not in CASES: raise ValueError('Unknown decision case')
    template=template or rng.choice(('integral_thin','function'))
    if template not in ('integral_thin','function'): raise ValueError('Unsupported production template')
    n=rng.choice(range(0,20) if case.startswith('lower_') else range(1,21)) if parameters is None else parameters['n']
    vals=production_bank(n,case)
    if any(family_equivalent(a,b) for i,(_,a,_) in enumerate(vals) for _,b,_ in vals[:i]):
        raise ValueError('Ambiguous complete bank')
    problem=prompt(n,template) if n else prompt(0,'constant') if template=='integral_thin' else prompt(0,'function').replace(power(0),'1')
    p=display_integral(normalize_prose(problem));sol=normalize_prose(production_solution(n,template))
    vals=[(normalize_tex(t),a,r) for t,a,r in vals]
    cid=digest({'version':VERSION,'problem':p,'solution':sol,'bank':sorted(t for t,_,_ in vals)})
    fid=uid(cid+'/field')
    answers=[{':answer/id':uid(fid+'/'+t),':answer/type':':answer.type/math',':answer/value':t} for t,_,_ in vals]
    correct=next(a[':answer/id'] for a,(_,_,role) in zip(answers,vals) if role=='power_rule');rng.shuffle(answers)
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':uid(cid),':question/difficulty':':question.difficulty/easy',
        ':question/problem':p,':question/worked-solution':sol,':question/answer-fields':[{
            ':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
            ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'n':n},
            'bank_profile':'authored_boundary' if (case.startswith('lower_') and n==0 or case.startswith('upper_') and n==1) else 'authored_complete','decision_case':case,'recipes':{t:r for t,_,r in vals},
            'domain':'x real; C arbitrary constant','source':{k:SOURCE[k] for k in ('database','basis','lineage')},
            'source_references':['q-2005','q-2022','q-113665','q-113668','q-29994','q-66126','e-364'],
            'semantic_instance':{'integrand_exponent':n,'response':'complete primitive family'},
            'dependencies':{'python':'3.13.5','sympy':sp.__version__}}}
    validate_generated_record(record)
    return record

def replay_source(sid):
    if sid not in SOURCE_SPECS: raise ValueError('Unknown source ID')
    return replay_generate('easy',seed=0,profile='raw:'+sid)

# Moderate removes the complete-answer bank. Hard also requires the source's
# differentiation check on a competing primitive, using mastered prerequisites.
ERROR_PROFILES=('old_divisor','omit_division','wrong_exponent','multiply','valid')

def generate(level='easy', seed=0, template=None, parameters=None, case=None, error_profile=None):
    if level=='easy':
        return generate_easy(level,seed,template,parameters,case)
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+level)
    if type(seed) is not int: raise ValueError('seed must be an integer')
    rng=random.Random(seed)
    if parameters is not None and (set(parameters)!={'n'} or type(parameters['n']) is not int):
        raise ValueError('Parameters require integer n only')
    n=rng.choice(range(21) if level=='moderate' else range(2,13)) if parameters is None else parameters['n']
    if not 0<=n<=20 or level=='hard' and not 2<=n<=12:
        raise ValueError('Exponent outside level domain')
    template=template or (rng.choice(('integral_thin','function')) if level=='moderate' else 'function')
    if template not in ('integral_thin','function') or level=='hard' and template!='function':
        raise ValueError('Unsupported template for level')
    m=n+1
    key=primitive(n,False)
    sol=production_solution(n,template)
    fields=[('antiderivative',key)]
    profile=None
    if level=='moderate':
        problem=(prompt(n,template) if n else prompt(0,'constant') if template=='integral_thin' else prompt(0,'function').replace(power(0),'1'))
        problem+=' Use $C$ for the arbitrary constant of integration.\n\n'+('$F(x)=$ ' if template=='function' else '')+'{{antiderivative}}'
    else:
        profile=error_profile or rng.choice(ERROR_PROFILES)
        if profile not in ERROR_PROFILES: raise ValueError('Unknown error profile')
        exponent,coefficient,explanation={
            'old_divisor':(m,sp.Rational(1,n),'The proposed expression divides by the old exponent rather than the new exponent.'),
            'omit_division':(m,sp.Integer(1),'The proposed expression omits division by the new exponent.'),
            'wrong_exponent':(n,sp.Rational(1,m),'The proposed expression divides by the new exponent but leaves the exponent unchanged.'),
            'multiply':(m,sp.Integer(m),'The proposed expression multiplies by the new exponent rather than dividing.'),
            'valid':(m,sp.Rational(1,m),'The proposed expression does differentiate to the given function.')
        }[profile]
        proposal=coefficient*X**exponent
        proposed_tex=sp.latex(proposal)
        derivative=sp.diff(proposal,X)
        derivative_tex=sp.latex(derivative)
        problem="Given $f(x)="+power(n,False)+"$ and $F'(x)=f(x)$, a student proposes\n\n$$\nG(x)="+proposed_tex+"+C.\n$$\n\nDifferentiate the proposed expression, then give the correct general antiderivative of $f$. Use $C$ for the arbitrary constant.\n\n1. $G'(x)=$ {{derivative}}.\n2. $F(x)=$ {{antiderivative}}."
        sol="Differentiate the proposed expression:\n\n"+aligned([r"G'(x)&=\frac{\mathrm{d}}{\mathrm{d}x}\left("+proposed_tex+r"+C\right)",r"&="+sp.latex(coefficient)+r"\cdot "+str(exponent)+power(exponent-1,False)+r"+0",r"&="+derivative_tex+"."])+"\n\n"+explanation+"\n\n"+sol
        fields=[('derivative',derivative_tex),('antiderivative',key)]
    problem=display_integral(normalize_prose(problem));sol=normalize_prose(sol)
    fields=[(k,normalize_tex(t)) for k,t in fields]
    cid=digest({'version':VERSION,'level':level,'problem':problem,'solution':sol,'fields':fields})
    answer_fields=[]
    for name,tex in fields:
        fid=uid(cid+'/'+name);aid=uid(fid+'/'+tex)
        answer_fields.append({':answer-field/id':fid,':answer-field/key':name,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex}],':answer-field/correct':[':answer/id',aid]})
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(cid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':sol,':question/answer-fields':answer_fields},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'n':n},'error_profile':profile,'domain':'x real; C arbitrary constant','difficulty_origin':'authored progression: construction, then explicit differentiation check','source_references':['e-364','q-113668','q-66126','tutorial 691','The Power Rule for Integration'],'semantic_instance':{'integrand_exponent':n,'response':'complete primitive family and candidate derivative' if level=='hard' else 'complete primitive family'}}}
    validate_generated_record(record)
    return record

def generate_batch(difficulty='easy',count=5,seed=0):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+difficulty)
    limit=11 if difficulty=='hard' else 21
    if type(count) is not int or not 1<=count<=limit: raise ValueError('count outside finite level domain')
    rng=random.Random(seed)
    # Schedule answer-bearing cases and positions across a batch before numerical
    # resampling; a fresh seed alone cannot remedy a one-sided finite practice pool.
    cases=list(CASES);rng.shuffle(cases)
    profiles=list(ERROR_PROFILES);rng.shuffle(profiles)
    positions=list(range(5));rng.shuffle(positions)
    # Keep each finite easy batch in one randomly selected source framing.
    # Splitting five scheduled roles into tiny wording groups can leave a
    # bank-only tie-break perfect within a visible subgroup. Each framing now
    # receives the complete target/surplus and position schedule across batches.
    batch_template=rng.choice(('integral_thin','function')) if difficulty=='easy' else None
    records=[];seen=set()
    for offset in range(2000):
        i=len(records)
        kwargs={'case':cases[i%4], 'template':batch_template} if difficulty=='easy' else {'error_profile':profiles[i%5]} if difficulty=='hard' else {}
        r=generate(difficulty,seed+offset,**kwargs);n=r['generation']['parameters']['n']
        if n in seen: continue
        if difficulty=='easy':
            f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
            good=next(a for a in choices if a[':answer/id']==correct)
            choices.remove(good);choices.insert(positions[i%5],good)
        records.append(r);seen.add(n)
        if len(records)==count:return records
    raise ValueError('Finite-family resampling exhausted')

def main():
    p=argparse.ArgumentParser(description='Monomial antiderivatives: recognition, construction, and verification.')
    p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--replay-source',choices=list(SOURCE_SPECS))
    a=p.parse_args()
    try: records=[replay_source(a.replay_source)] if a.replay_source else generate_batch(a.difficulty,a.count,a.seed)
    except ValueError as error:p.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
