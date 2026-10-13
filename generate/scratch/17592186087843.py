#!/usr/bin/env python3
"""Cancel common factors, then solve the reduced denominator over the reals.

Read-only draft at math basis 1356. Evidence and verification command are in
17592186087843/README.md. Each source gets a parameterized mathematical mask;
observed radio banks are evidence-only, because wrong-root author intent is not
recoverable from isolated sets. The separate normal five-option bank applies
complete root-set operations. No plots, EDB writes, or engine modifications.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186087843
KP_UUID='53b26ee4-53af-5660-a9e6-8e5cca8b3e1d'
TITLE='Calculating Vertical Asymptotes With Common Factors in the Numerator and Denominator'
VERSION='common-factor-asymptotes-1'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
X=s.Symbol('x',real=True)
OPENING='To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$'
# Easy: already-factored degree-one cancellation, one surviving linear pole.
# Moderate: quadratic/nonmonic factorization, common x^2, or cubic grouping
# with linear numerator. Hard: both quadratics; grouping with quadratic
# numerator; cubic perfect power; difference of squares and repeated pole.
TEMPLATES={
'q-278535':('easy','factored',dict(a=1,b=-2)),
'q-80690':('easy','factored_zero',dict(a=0,b=2)),
'q-269990':('moderate','linear',dict(a=-3,b=2)),
'q-39801':('moderate','linear_space',dict(a=2,b=-4,opaque=[-2,0])),
'q-278556':('moderate','nonmonic',dict(m=2,n=-1,b=-1)),
'q-278536':('moderate','monomial',dict(b=2)),
'q-278545':('moderate','grouped_linear',dict(a=2,b=1)),
'q-80691':('moderate','linear_zero',dict(a=-2)),
'q-278543':('hard','quadratic',dict(a=-2,b=1,c=3)),
'q-39800':('hard','quadratic_space',dict(a=1,b=-2,c=2)),
'q-39802':('hard','grouped_quadratic',dict(a=1,b=-7,c=2)),
'q-39804':('hard','cube',dict(a=1,b=-5,opaque=[0])),
'q-39931':('hard','squares',dict(a=2,opaque=[-1,1,0])),
}
RADIO={k for k,q in SOURCES.items() if any(f[':answer-field/type'][':db/ident'].endswith('/radio') for f in q.get(':question/answer-fields',[]))}
RAW_FIELDLESS='q-39802'

def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def digest(v):return hashlib.sha256(stable(v).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+stable(v)))
def tex(v):return s.latex(v).replace(r'\left','').replace(r'\right','')
def poly(v,style='compact'):
    """Render ordered primitive polynomial components, keeping source notation."""
    p=s.Poly(s.expand(v),X);out=[]
    for (power,),coef in p.terms():
        sign='-' if coef<0 else '+';mag=abs(int(coef))
        if power:
            term=('' if mag==1 else str(mag))+('x' if power==1 else ('x^{'+str(power)+'}' if style=='space' else '{x}^{'+str(power)+'}'))
        else:term=str(mag)
        if not out:out.append(('-' if coef<0 else '')+term)
        elif style=='space':out.append(' '+sign+' '+term)
        else:out.append(sign+term)
    return ''.join(out) or '0'
def lin(root,m=1):return poly(m*(X-s.Rational(root)))
def fac(root,m=1):return '('+lin(root,m)+')'
def frac(n,d):return r'\frac{'+n+'}{'+d+'}'
def cancel(v):return r'\cancel{'+v+'}'
def power(root,k,quirk=False):return '('+lin(root)+(r'{)}' if quirk else ')')+'^{'+str(k)+'}'

def guard(t,p):
    _,family,orig=TEMPLATES[t]
    required=set(orig); allowed=required
    if set(p)!=allowed:raise ValueError('exact parameter keys required: '+str(sorted(required)))
    for k,v in p.items():
        if k=='opaque':
            if not isinstance(v,list) or len(v)!=len(orig[k]) or any(type(n)!=int or abs(n)>8 for n in v):raise ValueError('opaque evidence slots')
        elif type(v)!=int:raise ValueError('integer primitive parameters required')
    if family in ('factored','linear','linear_space','quadratic','quadratic_space','cube'):
        if not (abs(p['a'])<=6 and abs(p['b'])<=8 and p['a']!=p['b']):raise ValueError('distinct bounded roots')
    if family in ('linear','linear_space') and (p['a']==0 or p['b']==0 or p['a']+p['b']==0):raise ValueError('quadratic must retain nonzero middle and constant terms')
    if family in ('quadratic','quadratic_space'):
        if abs(p['c'])>6 or len({p['a'],p['b'],p['c']})!=3 or any(p[k]==0 for k in ('a','b','c')) or p['a']+p['c']==0 or p['a']+p['b']==0:raise ValueError('two complete nondegenerate quadratics')
    if family=='cube' and (not p['a'] or not p['b'] or abs(p['a'])>4):raise ValueError('cubic perfect-power workload')
    if family=='factored_zero' and (p['a']!=0 or not p['b'] or abs(p['b'])>8):raise ValueError('one explicit x factor')
    if family=='linear_zero' and (not p['a'] or abs(p['a'])>8):raise ValueError('nonzero common root; zero pole')
    if family=='monomial' and (not p['b'] or abs(p['b'])>8):raise ValueError('common x^2 and linear pole')
    if family=='nonmonic':
        if not (2<=p['m']<=4 and 1<=abs(p['n'])<=5 and s.gcd(p['m'],p['n'])==1 and abs(p['b'])<=6 and p['b']!=0 and s.Rational(-p['n'],p['m'])!=p['b'] and p['n']-p['m']*p['b']!=0):raise ValueError('primitive nonunit common factor; irreducible rational cancelled root')
    if family.startswith('grouped'):
        if not (1<=p['a']<=4 and 1<=abs(p['b'])<=8 and p['b'] not in (-p['a'],p['a'])):raise ValueError('four-term cubic grouping bounds')
        if family=='grouped_quadratic' and (not p['c'] or abs(p['c'])>6 or p['c'] in (-p['a'],p['a'],p['b']) or p['c']==p['a']):raise ValueError('quadratic numerator needs distinct nonzero roots and middle term')
    if family=='squares' and not (1<=p['a']<=6):raise ValueError('bounded difference of squares')

def math_parts(t,p,observed=False):
    """All display stages derived structurally before final SymPy cancellation."""
    family=TEMPLATES[t][1];quirk=observed and family=='cube';a=p.get('a',0);b=p.get('b',0);c=p.get('c',0)
    if family=='nonmonic':
        A=p['m']*X+p['n'];a=s.Rational(-p['n'],p['m']);L=poly(A)
    else:A=X-a;L=lin(a)
    if family in ('factored','factored_zero','linear','linear_space','linear_zero','nonmonic'):
        if family=='linear_zero':b=0
        B=X-b;N=A;D=A*B;rn='1';rd=lin(b)
        style='space' if family=='linear_space' else 'compact'
        dn=poly(N,style);dd=poly(D,style)
        if family=='factored':dd=fac(b)+fac(a)
        if family=='factored_zero':
            # Actual source uses literal quotient notation rather than a fraction.
            ftex='f(x) = ('+L+')/('+L+'('+lin(b).replace('-',' - ').replace('+',' + ')+'))'
            rows=[frac(L,L+fac(b)),frac(cancel(L),cancel(L)+fac(b)),frac('1',rd)]
        else:
            ftex='f(x)'+(' = ' if family=='linear_space' else '=')+frac(dn,dd)
            if family=='factored':rows=[frac(dn,dd),frac(cancel(L),fac(b)+'('+cancel(L)+')'),frac(rn,rd)]
            elif family=='nonmonic':rows=[frac(dn,dd),frac(L,fac(b)+'('+L+')'),frac(cancel(L),fac(b)+cancel('('+L+')')),frac(rn,rd)]
            elif family=='linear_zero':rows=[frac(dn,dd),frac(L,'x'+fac(a)),frac(cancel(L),'x'+cancel(fac(a))),frac(rn,rd)]
            else:rows=[frac(dn,dd),frac(L,fac(a)+fac(b)),frac(cancel(L),cancel(fac(a))+fac(b)),frac(rn,rd)]
        poles=[s.Rational(b)]
    elif family=='monomial':
        N=X**2;D=X**2*(X-b);rn='1';rd=lin(b)
        ftex='f(x)='+frac(poly(N),poly(D))
        rows=[frac(poly(N),poly(D)),frac('{x}^{2}','{x}^{2}'+fac(b)),frac(cancel('{x}^{2}'),cancel('{x}^{2}')+fac(b)),frac(rn,rd)];poles=[s.Rational(b)]
    elif family in ('quadratic','quadratic_space'):
        N=(X-a)*(X-c);D=(X-a)*(X-b);rn=lin(c);rd=lin(b);style='space' if family=='quadratic_space' else 'compact'
        ftex='f(x)'+(' = ' if family=='quadratic_space' else '=')+frac(poly(N,style),poly(D,style))
        rows=[frac(poly(N),poly(D)),frac(fac(c)+fac(a),fac(b)+fac(a)),frac(fac(c)+cancel(fac(a)),fac(b)+cancel(fac(a))),frac(rn,rd)];poles=[s.Rational(b)]
    elif family.startswith('grouped'):
        N=X+a if family=='grouped_linear' else (X-c)*(X+a)
        D=(X**2-a*a)*(X-b);ntext=poly(N);rn='1' if family=='grouped_linear' else lin(c);rd=fac(a)+fac(b)
        ftex='f(x)='+frac(ntext,poly(D));nf=ntext if family=='grouped_linear' else fac(c)+fac(-a)
        sq='{x}^{2}'+('-'+str(a*a))
        group='{x}^{2}'+fac(b)+'-'+('' if a*a==1 else str(a*a))+fac(b)
        cf=cancel(ntext) if family=='grouped_linear' else fac(c)+cancel(fac(-a))
        rows=[frac(ntext,poly(D)),frac(nf,group),frac(nf,'('+sq+')'+fac(b)),frac(nf,fac(a)+fac(-a)+fac(b)),frac(cf,fac(a)+cancel(fac(-a))+fac(b)),frac(rn,rd)]
        poles=sorted([s.Rational(a),s.Rational(b)])
    elif family=='cube':
        N=(X-a)**3;D=(X-a)*(X-b)**2;rn=power(a,2,quirk);rd=power(b,2,quirk)
        ftex='f(x)='+frac(poly(N),fac(a)+rd)
        rows=[frac(poly(N),fac(a)+rd),frac(power(a,3,quirk),fac(a)+rd),frac(fac(a)+rn,fac(a)+rd),frac(cancel(fac(a))+rn,cancel(fac(a))+rd),frac(rn,rd)];poles=[s.Rational(b)]
    elif family=='squares':
        N=X**2-a*a;D=X**2*(X+a);rn=lin(a);rd='{x}^{2}'
        ftex='f(x)='+frac(poly(N),poly(D))
        rows=[frac(poly(N),poly(D)),frac(fac(a)+fac(-a),'{x}^{2}'+fac(-a)),frac(fac(a)+cancel(fac(-a)),'{x}^{2}'+cancel(fac(-a))),frac(rn,rd)];poles=[s.Rational(0)]
    else:raise ValueError(family)
    domain=sorted(s.solve(D,X));reduced=s.cancel(N/D)
    # Cancelled roots with remaining denominator multiplicity remain poles.
    holes=[r for r in domain if r not in poles]
    return dict(N=s.expand(N),D=s.expand(D),reduced=reduced,poles=poles,domain=domain,holes=holes,ftex=ftex,rows=rows,rn=rn,rd=rd,a=s.Rational(a),b=s.Rational(b),c=s.Rational(c))

def aligned(rows,t):
    last='' if t=='q-39931' else '.'
    return '\n'+r'\begin{aligned}f(x) & ='+rows[0]+''.join(r' \\  & ='+v for v in rows[1:])+last+r'\end{aligned}'+'\n'

def replace_math_blocks(text,values):
    """Replace complete math components only; prose and delimiters stay intact."""
    blocks=list(re.finditer(r'\$\$(.*?)\$\$|\$([^$]*?)\$',text,re.S));pieces=[];start=0
    for i,m in enumerate(blocks):
        pieces.append(text[start:m.start()]);body=m.group(1) if m.group(1) is not None else m.group(2);delim='$$' if m.group(1) is not None else '$'
        pieces.append(delim+values.get(i,body)+delim);start=m.end()
    pieces.append(text[start:]);return ''.join(pieces)

def source_solution(t,z):
    q=SOURCES[t]
    if ':question/worked-solution' not in q:return normal_solution(t,z)
    poles=z['poles']; eq=z['rd']+'=0';answer=lambda v:'x='+tex(v)
    if t=='q-39931':values={1:'\n'+aligned(z['rows'],t).strip()+'\n',2:'\n'+eq+'\n',3:answer(poles[0])+'.',4:answer(poles[0])}
    else:
        values={1:aligned(z['rows'],t),3:'\n'+eq+'\n'}
        if len(poles)==1:values.update({4:answer(poles[0])+'.',5:answer(poles[0])+('' if t=='q-39804' or t=='q-80691' else '.')})
        else:values.update({4:answer(poles[0]),5:answer(poles[1])+'.',6:answer(poles[0]),7:answer(poles[1])+'.'})
    return replace_math_blocks(q[':question/worked-solution'],values)

def normal_solution(t,z):
    # Sources' ordered math/prose is retained for every present worked solution.
    if ':question/worked-solution' in SOURCES[t]:return source_solution(t,z)
    poles=z['poles'];end=' and '.join('$x='+tex(r)+'$' for r in poles)
    return OPENING+'\n\nFactoring the numerator and denominator and canceling any common factors, we get\n\n$$'+aligned(z['rows'],t)+'$$\n\nNext, we set the denominator equal to zero and solve for $x:$\n\n$$\n'+z['rd']+'=0\n$$\n\nThis gives the solution '+end+'. Therefore, '+end+' is the only vertical asymptote.'

def prompt(t,z,raw=False):
    f=z['ftex']
    # Source punctuation lies inside its mathematical component in four prompts.
    if t in ('q-39802','q-39804','q-39931','q-80691'):f+='.'
    result=replace_math_blocks(SOURCES[t][':question/problem'],{0:f})
    if t==RAW_FIELDLESS and not raw:result+='\n\nIn **ascending order**, $x=${{field-1}} and $x=${{field-2}}.'
    return result

def roots_read(value):
    if 'no vertical asymptotes' in value:return frozenset()
    value=value.replace('$','').replace(r'\,','').replace('only','').strip()
    result=[]
    for part in value.split(','):
        rhs=part.split('=',1)[-1].strip()
        if '±' in rhs:
            v=s.Rational(rhs.replace('±','').strip());result.extend([v,-v])
        elif rhs:result.append(s.Rational(rhs))
    return frozenset(result)

def observed_bank(t,p,z):
    """Complete observed shape recipes; not a claim about wrong-root intent.

    Opaque choices use independent evidence slots (not fitted error formulas).
    Each tuple carries the complete root set and exact rendered source shape.
    """
    a,b,c=z['a'],z['b'],z['c'];st=lambda v:tex(v)
    if t=='q-39800':vals=[('$x ='+st(b)+'$ only','text'),('$x = '+st(c)+'$ only','text'),('x ='+st(b)+', x = '+st(a),'math'),('$x = '+st(a)+'$ only','text'),('x = ± '+st(abs(c))+', x = '+st(a),'math')]
    elif t=='q-39801':
        o=p['opaque'];vals=[('$x = '+st(a)+'$ only','text'),('x ='+st(b)+', x = '+st(a),'math'),('x = '+st(a)+', x = '+st(-b),'math'),('x ='+st(o[0])+', x = '+st(o[1]),'math'),('$x ='+st(b)+'$ only','text')]
    elif t=='q-80690':vals=[('x = '+st(a)+', x = '+st(b),'math'),('$x = '+st(a)+'$ only','text'),('$x = '+st(b)+'$ only','text'),('The function has no vertical asymptotes','text'),('x ='+st(-b)+', x = '+st(b),'math')]
    elif t=='q-39804':
        o=p['opaque'];vals=[('$x='+st(b)+'$ only','text'),('x='+st(o[0])+r',\,x='+st(-b),'math'),('x='+st(b)+r',\,x='+st(a),'math'),('$x='+st(a)+'$ only','text'),('x='+st(b)+r',\,x='+st(-a)+r',\,x='+st(a),'math')]
    elif t=='q-39931':
        o=p['opaque'];vals=[('$x='+st(o[1])+'$ only','text'),('The function has no vertical asymptotes','text'),('x='+st(o[0])+r',\,x='+st(o[1]),'math'),('$x='+st(o[2])+'$ only','text'),('$x='+st(o[0])+'$ only','text')]
    elif t=='q-80691':vals=[('$x='+st(-a)+'$ only','text'),('x=0'+r',\,x='+st(a),'math'),('$x=0$ only','text'),('The function has no vertical asymptotes','text'),('x='+st(a),'math')]
    else:raise ValueError('no observed radio bank')
    return vals

def normal_bank(z):
    """One entire operation bank: poles; removed roots; original denominator
    roots; no poles; sign-reversed poles. Reject all collisions together."""
    reverse=[-r for r in z['holes']] if z['poles']==[s.Rational(0)] else [-r for r in z['poles']]
    sets=[z['poles'],z['holes'],z['domain'],[],reverse]
    vals=[]
    for roots in sets:
        roots=sorted(set(roots))
        if not roots:value='The function has no vertical asymptotes';kind='text'
        elif len(roots)==1:value='$x='+tex(roots[0])+'$ only';kind='text'
        else:value=r',\,'.join('x='+tex(r) for r in roots);kind='math'
        vals.append((value,kind))
    return vals

def sample(t,rng):
    family=TEMPLATES[t][1];p=dict(TEMPLATES[t][2]);p={k:(list(v) if isinstance(v,list) else v) for k,v in p.items()}
    for k in p:
        if k=='opaque':continue
        if k=='m':p[k]=rng.randint(2,4)
        elif k=='n':p[k]=rng.choice([i for i in range(-5,6) if i])
        elif family.startswith('grouped') and k=='a':p[k]=rng.randint(1,4)
        elif family=='squares' and k=='a':p[k]=rng.randint(1,6)
        elif family=='linear_zero' and k=='a':p[k]=rng.randint(-8,8)
        elif family=='factored_zero' and k=='a':p[k]=0
        elif family=='cube' and k=='a':p[k]=rng.randint(-4,4)
        else:p[k]=rng.randint(-6 if k in ('a','c') else -8,6 if k in ('a','c') else 8)
    return p

def build(level,seed,t,p,profile,field_type):
    guard(t,p);obs=profile in ('observed','raw');z=math_parts(t,p,obs)
    raw=profile=='raw';isradio=t in RADIO
    if field_type is not None and field_type!=('radio' if isradio else 'blank'):raise ValueError('field layout is fixed per template')
    vals=observed_bank(t,p,z) if isradio and obs else normal_bank(z) if isradio else None
    if isradio:
        sets=[roots_read(v) for v,_ in vals];correct=frozenset(z['poles'])
        if len(sets)!=5 or len(set(sets))!=5 or sets.count(correct)!=1:raise ValueError('reject whole ambiguous bank')
    prob=prompt(t,z,raw);sol=source_solution(t,z) if obs else normal_solution(t,z)
    payload={'parameters_math':[s.srepr(z['N']),s.srepr(z['D'])],'problem':prob,'solution':None if raw and ':question/worked-solution' not in SOURCES[t] else sol,'omitted_correct':raw and t in ('q-39800','q-39801','q-80690'),'bank':sorted(vals) if vals else [tex(v) for v in z['poles']],'layout':'fieldless' if raw and t==RAW_FIELDLESS else 'radio' if isradio else 'blank'}
    qid=uid(payload);fields=[]
    if not(raw and t==RAW_FIELDLESS):
        if isradio:
            fkey='selection';fid=uid([qid,fkey]);answers=[]
            for value,kind in vals:
                aid=uid([fid,value,kind]);answers.append({':answer/id':aid,':answer/type':':answer.type/'+kind,':answer/value':value})
                if roots_read(value)==frozenset(z['poles']):correctid=aid
            random.Random(seed).shuffle(answers)
            fields=[{':answer-field/id':fid,':answer-field/key':fkey,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]
        else:
            keys=['field-1','field-2'] if len(z['poles'])==2 else ['field-1']
            # Exact source retains field-2 before field-1; matching by key matters.
            if t=='q-278545':keys=keys[::-1]
            for key in keys:
                value=tex(z['poles'][int(key[-1])-1]);fid=uid([qid,key]);aid=uid([fid,value])
                fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}],':answer-field/correct':[':answer/id',aid]})
    if raw and t in ('q-39800','q-39801','q-80690'):
        for field in fields:field.pop(':answer-field/correct',None)
    # Raw radio omissions remain visible in metadata; authored completion is used
    # in schema records to permit grading, and is never counted observed matched.
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prob,':question/worked-solution':sol,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_id':t,'observed_level':SOURCES[t].get(':question/difficulty',{}).get(':db/ident'),'authored_level_assignment':':question/difficulty' not in SOURCES[t],'evidence_only':obs and (isradio or raw),'eligible_for_learning':not(raw or (obs and isradio)),'source_missing_correct_ref':t in ('q-39800','q-39801','q-80690'),'source_fieldless':t==RAW_FIELDLESS,'completion':'raw fieldless evidence' if raw and t==RAW_FIELDLESS else 'independently derived fields/correct refs' if t==RAW_FIELDLESS or t in ('q-39800','q-39801','q-80690') else None,'original_domain_excludes':[tex(v) for v in z['domain']],'holes':[tex(v) for v in z['holes']],'remaining_poles':[tex(v) for v in z['poles']],'reduced_expression':str(z['reduced']),'mathematical_fingerprint':digest([s.srepr(z['N']),s.srepr(z['D']),'all remaining real denominator roots']), 'content_fingerprint':digest(payload),'plot_rating':'none'}}
    if raw:
        for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):
            if key not in SOURCES[t]:record['question'].pop(key,None)
    return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unsupported level')
    rng=random.Random(seed);choices=[t for t,(lev,_,_) in TEMPLATES.items() if lev==level and (field_type is None or field_type==('radio' if t in RADIO else 'blank'))]
    if not choices:raise ValueError('unsupported field type')
    t=template or rng.choice(choices)
    if t not in choices:raise ValueError('template does not belong to requested level/layout')
    profile=profile or 'normal'
    if profile not in ('normal','observed','raw'):raise ValueError('unknown profile')
    # Source complete banks are selected before any parameter sampling.
    if parameters is not None:return build(level,seed,t,dict(parameters),profile,field_type)
    for _ in range(5000):
        p=sample(t,rng)
        try:return build(level,seed,t,p,profile,field_type)
        except ValueError:pass
    raise ValueError('unable to sample complete eligible bank')
# Each difficulty has one unordered pool; no within-level progression.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=['normal','observed','raw']);args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            print(r['question'][':question/problem']);print('\n'+r['question'].get(':question/worked-solution','[No captured worked solution.]')+'\n')
            for f in r['question'].get(':question/answer-fields',[]):
                print(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
if __name__=='__main__':main()
