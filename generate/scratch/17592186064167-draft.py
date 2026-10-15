#!/usr/bin/env python3
"""Power rule on unit-coefficient monomials, source math basis 2275.

All levels use the finite 0..20 exponent domain. Moderate/hard are explicitly
authored, uncalibrated same-method labels, not exponent-based progression.
Raw profiles preserve missing keys and remain evidence-only. Production inventory
uses complete radio banks; blank previews retain the documented native C-family
limitation. No adjacent calculus skills or source identities are changed.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
KP_ID=17592186064167
KP_UUID='f2a4550c-7ed7-58aa-8928-23dd1cfd0cd7'
TITLE='Finding the Antiderivative of a Monomial'
VERSION='monomial-power-rule-v1'
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/(str(KP_ID)+'-draft')
SOURCE=json.loads((EVIDENCE/'source.json').read_text())
X,C=sp.symbols('x C',real=True)
DOMAINS={level:tuple(range(21)) for level in ('easy','moderate','hard')}
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

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
    if not raw:
        import importlib.util
        spec=importlib.util.spec_from_file_location('monomial_math_format',EVIDENCE/'math_format.py'); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.validate_generated_record(result)
    return result

# EASY — one successor and reciprocal; n=0 constant representation is observed.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    if template=='constant' and not(profile and profile.startswith('raw:')): field_type=field_type or 'blank'
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — authored uncalibrated same-method label; no additional operation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored uncalibrated same-method label; no additional operation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r,label='Generated'):
    q=r['question'];g=r['generation']; out=[f"## {label} — {q.get(':question/difficulty','unrated').split('/')[-1]}",f"Template: `{g['template']}`; profile: `{g['bank_profile']}`; evidence only: {g['evidence_only']}.",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct',[None,None])[1]
        for a in f[':answer-field/choices']: out.append('$'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==correct else ''))
        if correct is None: out.append('Correct designation missing in original; independent inferred answer: $'+primitive(g['parameters']['n'],False)+'$.')
    if q.get(':question/worked-solution'): out+=['**Worked solution**',q[':question/worked-solution']]
    return '\n\n'.join(out)
def generate_batch(difficulty='all',seed=0,count=1,template=None,field_type=None,profile=None):
    if type(seed) is not int:raise ValueError('seed must be a builtin int')
    if type(count) is not int or count<1:raise ValueError('count must be a positive builtin int')
    if difficulty not in (*DOMAINS,'all'):raise ValueError('Unknown difficulty')
    levels=tuple(DOMAINS) if difficulty=='all' else (difficulty,)
    capacity=1 if template=='constant' or profile and profile.startswith('raw:') else 19 if profile in ('observed_2022','observed_113668','observed_29994','observed_113665') else 20 if field_type=='radio' or template or profile=='observed_2005' else 21
    if count*len(levels)>capacity:raise ValueError('Finite mathematical capacity exceeded: '+str(capacity))
    records=[];seen=set()
    for level in levels:
        accepted=[]
        for offset in range(1000):
            r=generate(level,seed+offset,template,field_type,None,profile)
            fp=r['generation']['mathematical_fingerprint']
            if fp in seen:continue
            seen.add(fp);accepted.append(r)
            if len(accepted)==count:break
        if len(accepted)<count:raise ValueError('Finite variant limit')
        records.extend(accepted)
    return records

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');p.add_argument('--field-type',choices=['radio','blank']);a=p.parse_args()
    try:records=generate_batch(a.difficulty,a.seed,a.count,a.template,a.field_type,a.profile)
    except ValueError as error:p.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
