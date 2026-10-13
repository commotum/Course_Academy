#!/usr/bin/env python3
"""Common-factor/complex-root asymptotes: faithful raw recipes and authored banks.

Raw profiles are evidence only, parameterized by the coordinate dilation x -> s*x
(s=1 recovers the capture). They never become default distractor recipes. Normal
samplers vary cancelled factors and the remaining irreducible quadratic at the
observed workload; every answer remains 'no vertical asymptotes'. No EDB writes.
"""
import argparse, copy, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
P=Path(__file__).with_suffix(''); KP_ID=17592186087845
CAP=json.loads((P/'source.json').read_text()); REC=CAP['record']
KP_UUID=REC[':knowledge-point/id']; TITLE=REC[':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
VERSION='common-complex-asymptotes-v1'; X=sp.Symbol('x',real=True)
OPEN='To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$'
MID='Factoring the numerator and denominator and canceling any common factors, we get'
NONE='The function has no vertical asymptotes'
LEVELS={'q-39927':'moderate','q-4695':'hard',**{k:v[':question/difficulty'][':db/ident'].split('/')[-1] for k,v in SOURCES.items() if ':question/difficulty' in v}}
FAMILIES={'factored':'easy','common-power':'moderate','grouped':'moderate','quadratic-numerator':'hard','grouped-numerator':'hard','quartic':'hard'}
TEMPLATES={**FAMILIES,**LEVELS}
DOUBLE_BANK_SOURCES={'q-4695','q-113547','q-113554','q-39936'}
PROFILES=['operations']+['observed:'+k for k in SOURCES]+['completed:'+k for k in SOURCES]

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+value))
def tex(expr):return sp.latex(expr).replace(' ','')
def block(s):return '$$\n'+s+'\n$$'
def fraction(n,d):return r'\frac{'+n+'}{'+d+'}'
def aligned(rows):return block(r'\begin{aligned}f(x) & ='+r' \\  & ='.join(rows)+r'\end{aligned}')
def roots(poly):return sorted((r for r in sp.solve(poly,X) if r.is_real),key=sp.default_sort_key)
def info(n,d):
    rn,rd=sp.fraction(sp.cancel(n/d)); common=sp.gcd(n,d)
    return {'numerator':str(sp.expand(n)),'denominator':str(sp.expand(d)),
            'remaining_numerator':str(rn),'remaining_denominator':str(rd),
            'original_domain_excludes':[str(r) for r in roots(d)],
            'holes':[str(r) for r in roots(common)],'remaining_poles':[str(r) for r in roots(rd)],
            'denominator_root_multiplicities':{str(r):int(m) for r,m in sp.roots(d,X).items()},
            'cancelled_root_multiplicities':{str(r):int(m) for r,m in sp.roots(common,X).items()}}

def source_math(name,s):
    # Complete symbolic source components; canonical example is not a practice case.
    base={
      'q-39927':(X,X*(X**2+X+1)), 'q-4695':(X**2-1,(X-1)*(X**2+1)),
      'q-113547':(X+1,(X+1)*(X**2+1)), 'q-113550':(X*(X-3),(X-3)*(X**2+1)),
      'q-113545':(X**2,X**2*(X**2+X+2)), 'q-39934':(X*(X+3),X*(X**2+2*X+8)),
      'q-80696':(4*X,X*(X**2+1)), 'q-6913':(X,X*(X**2+2)),
      'q-113554':(2*(X**2-3),(X**2-3)*(X**2+3)),
      'q-39936':(X**2-1,(X**2-1)*(X**2+1))}
    return tuple(sp.expand(v.subs(X,s*X)) for v in base[name])

def coordinate_expression(text,s):
    """Lossless mathematical-component template; function/answer LHS protected.

    Frozen source mathematical masks retain all nonvariable notation. Scale is
    inserted in complete independent-variable leaves, never in function labels.
    This is a genuine coordinate recipe, not a source-payload return branch.
    """
    xslot='x' if s==1 else '('+str(s)+'x)'
    return re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',lambda m:xslot,text)

def source_prompt(q,s):
    text=q[':question/problem'];match=re.search(r'(f\(x\)\s*=)([^$]+)',text)
    return text[:match.start(2)]+coordinate_expression(match[2],s)+text[match.end(2):]

def source_solution(q,s):
    text=q.get(':question/worked-solution')
    if text is None:return None
    def math(m):
        raw=m[1]
        if 'f(x)' in raw:
            left,rest=raw.split('f(x)',1);return '$$'+left+'f(x)'+coordinate_expression(rest,s)+'$$'
        if re.search(r'\bx\b',raw):return '$$'+coordinate_expression(raw,s)+'$$'
        if 'D &' in raw and s!=1:
            # D for Q(s*x) uses a*s^2,b*s,c; keep all ordered original stages.
            name=q[':question/math-academy-id']
            if name=='q-113545':
                raw=raw.replace('1-4(1)(2)',f'{s*s}-4({s*s})(2)').replace('=-7',f'={-7*s*s}')
            elif name=='q-39934':
                raw=raw.replace(r'{2}^{2}-4(1)(8)',f'{{{2*s}}}^{{2}}-4({s*s})(8)').replace('=-28',f'={-28*s*s}')
        return '$$'+raw+'$$'
    return re.sub(r'\$\$(.*?)\$\$',math,text,flags=re.S)

def source_choice(value,s):
    # Explicit opaque evidence profile: transform every COMPLETE observed root
    # component by r -> r/s. We infer no distractor intent from those scalars.
    if value==NONE:return value
    pattern=r'(x\s*=\s*)(\\pm\s*)?(-?(?:\\frac\{\d+\}\{\d+\}|\\sqrt\{\d+\}|\d+))'
    def root(m):
        value=m[3]
        if s!=1 and value not in ('0','-0'):value=r'\frac{'+value+'}{'+str(s)+'}'
        return m[1]+(m[2] or '')+value
    return re.sub(pattern,root,value)

def enum(v):return v[':db/ident'] if isinstance(v,dict) else v

def operation_bank(n,d,multiplier):
    """Whole bank: canceled roots, flip quadratic constant, both, one root."""
    reduced_d=sp.Poly(sp.fraction(sp.cancel(n/d))[1],X).monic()
    a,b,c=reduced_d.all_coeffs(); common=sp.gcd(n,d)
    holes=roots(common)
    # The complete profile is fixed BEFORE parameter sampling. Any collision
    # rejects this whole instance; there is no answer-dependent fallback.
    wrong=roots(a*X**2+b*X-multiplier*c)
    sets=[[],holes,wrong,sorted(set(holes+wrong),key=sp.default_sort_key),[max(wrong)]]
    if len({tuple(v) for v in sets})!=5:raise ValueError('Entire operation bank has equivalent options')
    return [(':answer.type/text',NONE) if not values else (':answer.type/math',r',\,'.join('x='+tex(v) for v in values)) for values in sets]

def solution(rows,q,b,c):
    if b==0:
        return OPEN+'\n\n'+MID+'\n\n'+aligned(rows)+'\n\nNext, we set the denominator equal to zero:\n\n'+block(tex(q)+'=0')+'\n\nThis equation does not have any real solutions. Therefore, $f(x)$ has no vertical asymptotes.'
    return OPEN+'\n\n'+MID+'\n\n'+aligned(rows)+'\n\nNext, we set the denominator equal to zero:\n\n'+block(tex(q)+'=0')+'\n\nThis equation does not have any real solutions because the discriminant $D$ is negative:\n\n'+block(r'\begin{aligned}D & =b^2-4ac \\ & =('+str(b)+r')^2-4(1)('+str(c)+r') \\ & ='+str(b*b)+'-'+str(4*c)+r' \\ & ='+str(b*b-4*c)+r'\end{aligned}')+'\n\nTherefore, $f(x)$ has no vertical asymptotes.'

def validate_parameters(level,name,p):
    if name in SOURCES:
        if set(p)!={'scale'} or type(p['scale']) is not int or not 1<=p['scale']<=3:raise ValueError('Source coordinate recipe requires integer scale 1..3')
        return
    keys={'r','b','c'}|({'leading'} if name=='factored' else set())|({'m'} if name=='common-power' else set())|({'a'} if name in ('quadratic-numerator','grouped-numerator') else set())
    if name=='quartic':keys={'c'}
    if set(p)!=keys or any(type(v) is not int for v in p.values()):raise ValueError('Unexpected/missing parameter or noninteger')
    if not 1<=p['c']<=12:raise ValueError('c must be 1..12')
    if name=='quartic':
        if p['c'] not in (2,3,5,6,7,8,10,11,12):raise ValueError('Quartic hard requires positive nonsquare c')
        return
    if not -4<=p['r']<=4 or not -4<=p['b']<=4 or p['b']**2>=4*p['c']:raise ValueError('Factor roots/bounds/negative discriminant')
    if name=='factored' and (p['r']!=0 or p['b']!=0 or p['c']>9 or not 1<=p['leading']<=5 or sp.gcd(p['leading'],p['c'])!=1):raise ValueError('Easy: ready common x, primitive positive a*x^2+c; a=1..5,c=1..9')
    if name=='common-power' and (p['r']!=0 or p['m'] not in (1,2) or (p['m']==1 and p['b']==0)):raise ValueError('Moderate extra workload: x^2 GCF or nonzero linear term')
    if name in ('grouped','grouped-numerator') and p['r']==0:raise ValueError('Grouping requires nonzero common linear shift')
    if name in ('grouped','grouped-numerator') and p['b']!=0:raise ValueError('Moderate grouped retains x^2+c times linear')
    if name=='quadratic-numerator' and (p['b']==0 or p['r']!=0):raise ValueError('Hard GCF: nonzero linear quadratic term and common x')
    if 'a' in p and (not 1<=abs(p['a'])<=5 or p['a']==-p['r']):raise ValueError('Hard numerator distinct nonzero residual linear factor')

def sample(name,rng):
    if name in SOURCES:return {'scale':rng.randint(1,3)}
    if name=='quartic':return {'c':rng.choice([2,3,5,6,7,8,10,11,12])}
    for _ in range(100):
        p={'r':rng.randint(-4,4),'b':rng.randint(-4,4),'c':rng.randint(1,12)}
        if name=='factored':p.update(r=0,b=0,c=rng.randint(1,9),leading=rng.randint(1,5))
        if name=='common-power':p.update(r=0,m=rng.choice([1,2]))
        if name in ('grouped','grouped-numerator'):p['b']=0
        if name=='quadratic-numerator':p['r']=0
        if name in ('quadratic-numerator','grouped-numerator'):p['a']=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        try:validate_parameters(FAMILIES[name],name,p);return p
        except ValueError:pass
    raise ValueError('Sampler exhausted')

# EASY: ready common x and primitive a*x^2+c; positive a,c, direct positivity.
def build_easy(name,p):
    q=p['leading']*X**2+p['c'];n=X;d=X*q
    nf='x';df='x('+tex(q)+')';rows=[fraction(nf,df),fraction(r'\cancel{x}',r'\cancel{x}('+tex(q)+')'),fraction('1',tex(q))]
    return n,d,fraction(nf,df),rows,q

# MODERATE: extract x or x^2 GCF, or group a cubic in two pairs.
def build_moderate(name,p):
    q=X**2+p['b']*X+p['c'];common=X**p['m'] if name=='common-power' else X-p['r']
    n=common;d=common*q;cf=tex(common);qf=tex(q)
    rows=[fraction(tex(sp.expand(n)),tex(sp.expand(d)))]
    if name=='grouped':rows.append(fraction(cf,'x^{2}('+cf+')+'+str(p['c'])+'('+cf+')'))
    rows+=[fraction(cf,'('+cf+')('+qf+')'),fraction(r'\cancel{'+cf+'}',r'\cancel{('+cf+')}('+qf+')'),fraction('1',qf)]
    return n,d,rows[0],rows,q

# HARD: factor a numerator as well as a cubic, or two difference-of-squares stages.
def build_hard(name,p):
    if name=='quartic':
        c=p['c'];common=X**2-c;q=X**2+c;n=common;d=common*q
        cf=tex(common);qf=tex(q)
        rows=[fraction(tex(n),tex(sp.expand(d))),fraction(cf,'('+cf+')('+qf+')'),fraction(r'\cancel{('+cf+')}',r'\cancel{('+cf+')}('+qf+')'),fraction('1',qf)]
    else:
        common=X-p['r'];residual=X+p['a'];q=X**2+p['b']*X+p['c'];n=common*residual;d=common*q
        cf,rf,qf=tex(common),tex(residual),tex(q)
        rows=[fraction(tex(sp.expand(n)),tex(sp.expand(d)))]
        if name=='grouped-numerator':
            # Four complete grouped terms retain the cubic operation even b !=0.
            grouped='x^{2}('+cf+')'
            if p['b']:grouped+=('+' if p['b']>0 else '-')+str(abs(p['b']))+'x('+cf+')'
            grouped+='+'+str(p['c'])+'('+cf+')'
            rows.append(fraction('('+cf+')('+rf+')',grouped))
        rows+=[fraction('('+cf+')('+rf+')','('+cf+')('+qf+')'),fraction(r'\cancel{('+cf+')}('+rf+')',r'\cancel{('+cf+')}('+qf+')'),fraction(rf,qf)]
    return n,d,rows[0],rows,q
BUILDERS={'easy':build_easy,'moderate':build_moderate,'hard':build_hard}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard') or field_type not in (None,'radio'):raise ValueError('Unsupported level/field type')
    if profile and profile!='operations':
        if profile not in PROFILES:raise ValueError('Unknown profile')
        implied=profile.split(':',1)[1]
        if template and template!=implied:raise ValueError('Template/profile mismatch')
        template=implied
    rng=random.Random(seed);eligible=[n for n,l in FAMILIES.items() if l==level]
    name=template or rng.choice(eligible)
    if name not in TEMPLATES or TEMPLATES[name]!=level:raise ValueError('Template does not belong to difficulty')
    profile=profile or 'operations';raw=profile.startswith('observed:')
    if raw and name not in SOURCES:raise ValueError('Observed profile requires source template')
    bank_multiplier=2 if name=='quartic' or name in DOUBLE_BANK_SOURCES else 1
    for _ in range(100):
        p=dict(parameters) if parameters is not None else sample(name,rng)
        validate_parameters(level,name,p)
        if name in SOURCES:
            source=SOURCES[name];n,d=source_math(name,p['scale']);prompt=source_prompt(source,p['scale']);sol=source_solution(source,p['scale'])
            if sol is None and not raw:
                rn,rd=sp.fraction(sp.cancel(n/d));q=sp.Poly(rd,X).monic().as_expr();a,b,c=sp.Poly(q,X).all_coeffs();common=sp.gcd(n,d)
                rows=[fraction(tex(n),tex(d)),fraction('('+tex(common)+')('+tex(sp.cancel(n/common))+')','('+tex(common)+')('+tex(sp.cancel(d/common))+')'),fraction(r'\cancel{('+tex(common)+')}('+tex(sp.cancel(n/common))+')',r'\cancel{('+tex(common)+')}('+tex(sp.cancel(d/common))+')'),fraction(tex(rn),tex(rd))]
                sol=solution(rows,q,b,c)
        else:
            n,d,formula,rows,q=BUILDERS[level](name,p);prompt='Determine the vertical asymptotes of $f(x)='+formula+'.$'
            b,c=sp.Poly(q,X).all_coeffs()[1:];sol=solution(rows,q,b,c)
        try:bank=operation_bank(n,d,bank_multiplier) if not raw else None;break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('No eligible whole bank')
    data=info(n,d)
    # Meaningful workload key ignores constant numerator scaling and profile.
    common=sp.Poly(sp.gcd(n,d),X).monic().as_expr();rd=sp.Poly(sp.fraction(sp.cancel(n/d))[1],X).monic().as_expr()
    residual=sp.Poly(sp.cancel(n/sp.gcd(n,d)),X).monic().as_expr()
    taskkey=digest({'common':sp.srepr(common),'remaining_denominator':sp.srepr(rd),'residual_numerator':sp.srepr(residual),'prompt_form':'factored' if name in ('factored','q-80696') else 'expanded'})
    # Raw fields preserve source absence and missing refs. Only enum wrappers
    # and database IDs normalize into the established local review schema.
    fields=[]
    if raw:
        for f in source.get(':question/answer-fields',[]):
            choices=[{':answer/type':enum(a[':answer/type']),':answer/value':source_choice(a[':answer/value'],p['scale'])} for a in f[':answer-field/choices']]
            field={':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/choices':choices}
            if ':answer-field/correct' in f:field['_correct_value']=source_choice(f[':answer-field/correct'][':answer/value'],p['scale'])
            fields.append(field)
    else:fields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':t,':answer/value':v} for t,v in bank],'_correct_value':NONE}]
    qrecord={':question/problem':prompt}
    if not raw or ':question/difficulty' in source:qrecord[':question/difficulty']=':question.difficulty/'+level
    if sol is not None:qrecord[':question/worked-solution']=sol
    if not raw or ':question/answer-fields' in source:qrecord[':question/answer-fields']=fields
    identity=digest({'version':VERSION,'question':qrecord});qid=uid(identity)
    for i,f in enumerate(fields):
        f[':answer-field/id']=uid(identity+':field:'+str(i));correct=f.pop('_correct_value',None)
        for a in f[':answer-field/choices']:a[':answer/id']=uid(f[':answer-field/id']+':'+a[':answer/type']+':'+a[':answer/value'])
        if correct is not None:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
        rng.shuffle(f[':answer-field/choices'])
    qrecord[':question/id']=qid
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':qrecord,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'profile':profile,'bank_profile':profile if raw else 'authored:'+('doubled-constant-sign' if bank_multiplier==2 else 'constant-sign'),'operation_profile_multiplier':None if raw else bank_multiplier,'distractor_recipes':None if raw else {'H':'real_roots(gcd(N,D))','W':'real_roots(a*x^2+b*x-'+str(bank_multiplier)+'*c)','complete_bank':['empty','H','W','union(H,W)','largest_real_root(W)']},'bank_origin':'observed opaque evidence' if raw else 'authored operation-derived whole bank','evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':not raw,'source_id':name if name in SOURCES else None,'source':{k:CAP[k] for k in ('database','basis','lineage')},'authored_level_assignment':name in ('q-39927','q-4695'),'completion':None if raw else 'authored fields/bank; missing solutions completed independently','parameter_fingerprint':taskkey,'content_fingerprint':identity,'sympy_version':sp.__version__,'plot_rating':'none',**data}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q,g=record['question'],record['generation'];out=['## '+g['template']+' — '+('raw evidence' if g['evidence_only'] else 'generated authored variant'),'',q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:out.append('- '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value'])+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
        if ':answer-field/correct' not in f:out+=['','Captured correct ref absent.']
    if ':question/answer-fields' not in q:out+=['Captured fields absent.']
    out+=['',('Observed difficulty: ' if g['evidence_only'] else 'Authored difficulty: ')+q.get(':question/difficulty','absent'),'',q.get(':question/worked-solution','Captured worked solution absent.')]
    return '\n'.join(out)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=PROFILES);parser.add_argument('--field-type',choices=['radio']);parser.add_argument('--parameters',help='Explicit JSON parameter object')
    a=parser.parse_args()
    if a.count<1 or a.difficulty=='all' and (a.template or a.profile):parser.error('Positive count and specific difficulty required for template/profile')
    try:records=[generate(l,a.seed+i,a.template,a.field_type,json.loads(a.parameters) if a.parameters else None,a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    except ValueError as e:parser.error(str(e))
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
