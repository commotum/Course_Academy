#!/usr/bin/env python3
"""Constant×natural-log differentiation. Private draft, frozen math basis 1356.

Raw source profiles are parameterized presentation recipes, including omissions.
Normal practice uses supported observed family layouts, normalized ln notation,
and inferred completed legacy fields. Moderate/hard are explicitly authored.
No EDB operations or plots; stop after generation/validation (steps 3–7).
"""
import argparse, functools, hashlib, json, math, random, re, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186096613
KP_UUID='a71301e9-bc7f-53b9-900e-c3bd37f96b03'
TITLE='Differentiating the Product of a Constant and the Natural Logarithm Function'
VERSION='constant-ln-2.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x=sp.Symbol('x',positive=True)
LEVELS=('easy','moderate','hard')
CASES={
 'q-11909':('legacy-radio','integer',7,1,0),
 'q-11910':('legacy-radio','fraction',2,3,0),
 'q-339941':('blank','canonical',-11,1,0),
 'q-70881':('fieldless','none',2,1,0),
 'q-101600':('radio-dot','euler',2,1,1),
 'q-101604':('radio-dot','integer',-9,1,0),
 'q-308849':('blank','canonical',8,1,0),
 'q-339949':('blank','equivalent-entry',11,4,0),
 'q-339950':('blank','equivalent-entry',-7,3,0),
}
TEMPLATES={'legacy-radio':('easy','radio',('integer','fraction')),
 'radio-dot':('easy','radio',('integer','euler')),
 'blank':('easy','blank',('canonical','equivalent-entry')),
 'authored-rational-e':('moderate','blank',('canonical',)),
 'authored-signed-rational-e-power':('hard','blank',('canonical',))}
RAW_PROFILES={'raw-'+sid:sid for sid in CASES}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def latex(value):return sp.latex(value).replace(' ','')
def constant(p):return sp.Rational(p['n'],p['d'])*sp.E**p['k']
@functools.lru_cache(maxsize=8192)
def expression(text):
    """Parse the displayed constant/log/quotient grammar, not generation metadata."""
    text=text.replace('\u2061','').replace(r'\left','').replace(r'\right','')
    text=re.sub(r'\\(?:operatorname|mathrm)\{(ln|log)\}',r'\1',text)
    text=text.replace(r'\ln','ln').replace(r'\cdot','*').replace(r'\,','')
    def group(pos):
        if text[pos]!='{':raise ValueError(text)
        depth=1;j=pos+1
        while depth:
            if j>=len(text):raise ValueError(text)
            depth+=(text[j]=='{')-(text[j]=='}');j+=1
        return text[pos+1:j-1],j
    while r'\frac' in text:
        i=text.rfind(r'\frac');a,j=group(i+5);b,k=group(j)
        text=text[:i]+'(('+a+')/('+b+'))'+text[k:]
    text=re.sub(r'(?:ln|log)\s*x',' log(x)',text)
    text=text.replace('^','**').replace('{','(').replace('}',')').strip().rstrip('.,')
    if '\\' in text:raise ValueError(text)
    return parse_expr(text,local_dict={'x':x,'e':sp.E,'log':sp.log,'D':lambda value:sp.diff(value,x)},transformations=standard_transformations+(implicit_multiplication_application,))
@functools.lru_cache(maxsize=4096)
def coefficient(problem):
    m=re.search(r'\$y\s*=\s*(.*?)\$',problem)
    if not m:raise ValueError('No displayed y function')
    f=expression(m[1]);c=sp.simplify(f/sp.log(x))
    if c.free_symbols or c==0 or sp.simplify(f-c*sp.log(x))!=0:raise ValueError('Outside c ln x scope')
    return c

def validate_parameters(p,level,bank,raw=False):
    if set(p)!={'n','d','k'} or any(type(p[a]) is not int for a in p):raise ValueError('Use exact integer n,d,k')
    if not 2<=abs(p['n'])<=30 or not 1<=p['d']<=12 or math.gcd(abs(p['n']),p['d'])!=1:raise ValueError('Reduced coefficient |n|2..30, d1..12')
    if not 0<=p['k']<=4:raise ValueError('Constant Euler exponent 0..4')
    if raw or level=='easy':
        if bank=='integer' and (p['d']!=1 or p['k']!=0):raise ValueError('Integer profile')
        if bank in ('fraction','equivalent-entry') and (p['d']==1 or p['k']!=0):raise ValueError('Rational profile')
        if bank=='fraction' and p['n']<2:raise ValueError('Positive source fraction bank')
        if bank=='euler' and (p['d']!=1 or p['k']!=1):raise ValueError('Euler profile')
        if bank in ('canonical','none') and p['k']!=0:raise ValueError('Rational source blank')
    elif level=='moderate':
        if not (2<=p['n']<=12 and 2<=p['d']<=8 and p['k']==1):raise ValueError('Moderate positive reduced rational×e bounds')
    elif level=='hard':
        if not (-12<=p['n']<=-2 and 2<=p['d']<=8 and 2<=p['k']<=4):raise ValueError('Hard signed reduced rational×e^k bounds')
    else:raise ValueError('level')

def bank_values(p,bank):
    c=constant(p);n,d=p['n'],p['d']
    if bank=='integer':v=[1/x,-c/x,1/(c*x),x/c,c/x]
    elif bank=='fraction':v=[c/x,1/(d*x),n/x,d/x,1/(c*x)]
    elif bank=='euler':v=[sp.E/(n*x),n/(sp.E*x),c/x,n+sp.E/x,sp.E+n/x]
    elif bank=='none':return []
    else:v=[c/x]
    if bank in ('integer','fraction','euler') and any(sp.simplify(a-b)==0 for i,a in enumerate(v) for b in v[:i]):raise ValueError('Whole bank rejected: equivalent options')
    out=[latex(a) for a in v]
    if bank=='equivalent-entry':out.append(f'{n}/({d}x)')
    return out

def mask(text,original):
    """Mask complete coefficient/derivative slots before rendering, including final row."""
    c=constant(original)
    text=text.replace(latex(c/x),'@@DERIVATIVE@@')
    text=text.replace(latex(c),'@@COEFFICIENT@@')
    return text

def render_mask(text,p):return text.replace('@@DERIVATIVE@@',latex(constant(p)/x)).replace('@@COEFFICIENT@@',latex(constant(p)))
def source_recipe(sid,p):
    source=QS[sid];_,_,n,d,k=CASES[sid];anchor={'n':n,'d':d,'k':k}
    result={':question/problem':render_mask(mask(source[':question/problem'],anchor),p)}
    if ':question/worked-solution' in source:result[':question/worked-solution']=render_mask(mask(source[':question/worked-solution'],anchor),p)
    return result

def authored_solution(p):
    c=latex(constant(p));a=latex(constant(p)/x)
    return ('The derivative of the natural logarithm is the reciprocal function:\n\n$$\n'+r'\frac{\text{d}}{\text{d}x}(\ln x)=\frac{1}{x}'+'\n$$\n\nWe apply our formula and get\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}('+c+r'\ln x) \\  & ='+c+r'\frac{\text{d}}{\text{d}x}(\ln x) \\  & ='+c+r'\cdot \frac{1}{x} \\  & ='+a+r'.\end{aligned}'+'\n$$')

def normalize_ln(text):return text.replace('ln\u2061',r'\ln ').replace(r'\operatorname{ln}x',r'\ln x')
@functools.lru_cache(maxsize=None)
def parameter_domain(level,bank,raw=False):
    domain=[]
    for n in range(-30,31):
        for d in range(1,13):
            for k in ((2,3,4) if level=='hard' and not raw else (1,) if level=='moderate' and not raw or bank=='euler' else (0,)):
                p={'n':n,'d':d,'k':k}
                try:validate_parameters(p,level,bank,raw);bank_values(p,bank)
                except ValueError:continue
                domain.append(p)
    if not domain:raise ValueError('Empty eligible domain')
    return tuple(domain)

def sample(rng,level,bank,raw):return dict(rng.choice(parameter_domain(level,bank,raw)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('difficulty')
    rng=random.Random(seed);raw=profile in RAW_PROFILES
    sid=RAW_PROFILES[profile] if raw else None
    if profile and not raw and profile not in ('integer','fraction','euler','canonical','equivalent-entry'):raise ValueError('Unknown profile')
    if raw:
        t,bank,*_=CASES[sid]
        if level!='easy' or template is not None and template!=t:raise ValueError('Raw profiles preserve captured easy/unrated scope')
        template=t;kind='none' if t=='fieldless' else 'blank' if t=='blank' else 'radio'
    else:
        eligible=[t for t,(l,f,banks) in TEMPLATES.items() if l==level and (field_type is None or f==field_type) and (profile is None or profile in banks)]
        if parameters is not None:
            def valid_bank(b):
                try:validate_parameters(parameters,level,b);bank_values(parameters,b);return True
                except ValueError:return False
            eligible=[t for t in eligible if any(valid_bank(b) for b in TEMPLATES[t][2] if profile is None or b==profile)]
        if template is not None and template not in eligible or not eligible:raise ValueError('Template/field/profile outside level')
        selector=random.Random(digest(parameters)) if parameters is not None else rng
        template=template or selector.choice(eligible);_,kind,banks=TEMPLATES[template]
        if parameters is not None:banks=tuple(b for b in banks if valid_bank(b))
        # Select complete profile BEFORE parameter sampling; fixed inputs keep bank identity across seeds.
        stable=random.Random(digest(parameters)) if parameters is not None else rng
        bank=profile or stable.choice(banks)
    if field_type is not None and field_type!=kind:raise ValueError('Field type mismatch')
    p=dict(parameters) if parameters is not None else sample(rng,level,bank,raw)
    validate_parameters(p,level,bank,raw);values=bank_values(p,bank)
    if sid is None and level=='easy':sid=next(s for s,(t,b,*_) in CASES.items() if t==template and b==bank)
    if sid:
        q=source_recipe(sid,p)
        if not raw:
            q={k:normalize_ln(v) for k,v in q.items()}
            q.setdefault(':question/worked-solution',authored_solution(p))
    else:
        q={':question/problem':'Given that $y='+latex(constant(p))+r'\ln x$, find $\frac{\text{d}y}{\text{d}x}.$'+'\n\n'+r'$\frac{\text{d}y}{\text{d}x}=$'+'\n{{field-1}}',':question/worked-solution':authored_solution(p)}
    source=QS[sid] if sid else {}
    if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
    identity=digest({'version':VERSION,'question':q,'kind':kind,'bank':sorted(values),'correct_present':not raw or bool(source.get(':question/answer-fields',[{}])[0].get(':answer-field/correct')) if kind!='none' else False})
    qid=uid('question:'+identity);q[':question/id']=qid
    if kind!='none':
        fid=uid('field:'+qid);key='field-1' if kind=='blank' else 'selection'
        answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
        correct=next(a[':answer/id'] for a in answers if a[':answer/value']==latex(constant(p)/x))
        rng.shuffle(answers)
        field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
        if not raw or ':answer-field/correct' in source[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct]
        q[':question/answer-fields']=[field]
    evidence_only=raw and (kind=='none' or ':question/difficulty' not in q or ':question/worked-solution' not in q or ':answer-field/correct' not in q.get(':question/answer-fields',[{}])[0])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile if raw else bank,'parameters':p,'raw_source_replay':raw,'source_id':sid,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domain':'x>0','evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'authored_level':level!='easy','math_fingerprint':digest(['differentiate c ln x',sp.srepr(coefficient(q[':question/problem'])),'x>0']),'content_fingerprint':identity,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

# EASY: all observed constant forms; complete integer, fraction, Euler banks and blanks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): recognize one positive reduced rational multiple of e as constant.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): signed reduced rational coefficient times a fixed Euler power, still constant.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
    q=rec['question'];lines=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):lines+=['\nBank: '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])]
    lines+=['\n'+q.get(':question/worked-solution','[Worked solution absent in raw source.]')]
    if rec['generation']['evidence_only']:lines+=['\nEvidence only; incomplete captured assessment attributes.']
    return '\n'.join(lines)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type');ap.add_argument('--format',choices=('json','markdown'),default='markdown');a=ap.parse_args()
    if a.count<1:ap.error('count must be positive')
    if a.difficulty=='all' and (a.template or a.profile):ap.error('specific template/profile requires specific difficulty')
    try:records=[generate(l,a.seed+i,a.template,a.field_type,None,a.profile) for l in LEVELS if a.difficulty in (l,'all') for i in range(a.count)]
    except ValueError as ex:ap.error(str(ex))
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
