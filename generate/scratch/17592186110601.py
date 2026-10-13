#!/usr/bin/env python3
"""Exact unknown-parameter perpendicular-line practice. Local only, steps 3–7.

Complete mathematical components fill captured prose/layout masks. Source profiles
are parameterized, including ambiguous observed banks explicitly reserved for replay.
Normal sampling uses defensible whole authored banks and rejects complete collisions.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as S
KP=17592186110601
VERSION='perpendicular-parameter-v1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
RAW={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
NS=uuid.UUID('6f3d7d62-686b-59c4-9ea1-695c6be3180b')
x,y,z=S.symbols('x y z')
OPEN='For the two lines to be perpendicular, their slopes must multiply to $-1.$'
# m = known slope, c = parameter's slope multiplier. Standard lines A*x+B*y=C.
CASES={
'q-215415':('easy','both_blank',dict(m='1/3',b=2,a=1,d=-1)),
'q-215416':('moderate','one_positive',dict(m=3,b=-5,a=1,B=6,C=4)),
'q-215417':('hard','two_blank',dict(A=2,B=-3,C=-6,a=1,D=2,E=2)),
'q-72548':('moderate','known_standard',dict(A=10,B=2,C=3,a=1,d=-3)),
'q-215939':('moderate','one_negative_spaced',dict(m=2,b=1,a=1,B=-10,C=3)),
'q-215941':('moderate','one_negative',dict(m=-5,b=3,a=3,B=-5,C=9)),
'q-215942':('moderate','one_negative',dict(m=7,b=-2,a=1,B=-14,C=7)),
'q-215944':('hard','two_positive',dict(A=10,B=5,C=3,a=2,D=1,E=2)),
'q-28328':('easy','both_radio',dict(a=5,b=9,m=-3,d=-8)),
'q-44407':('hard','two_negative',dict(A=4,B=-8,C=7,a=-1,D=3,E=9)),
'q-44515':('hard','two_zero',dict(A=15,B=5,C=9,a=3,D=4,E=0)),
}
TEMPLATES={key:dict(level=v[0],family=v[1],original=v[2],kind='radio' if key in ('q-28328','q-44407','q-44515') else 'blank') for key,v in CASES.items()}

def tex(v):
    v=S.sympify(v)
    if v.is_Rational:
        n,d=v.as_numer_denom(); return ('-' if n<0 else '')+(str(abs(n)) if d==1 else r'\frac{'+str(abs(n))+'}{'+str(d)+'}')
    return S.latex(v).replace(' ','')
def term(v, tail):
    v=S.sympify(v)
    return '' if v==0 else tail if v==1 else '-'+tail if v==-1 else tex(v)+tail
def add(a,b): return a+('+' if b and not b.startswith('-') else '')+b
def linear(a,b,c): return add(term(a,'x'),term(b,'y'))+'='+tex(c)
def slope(c,var):
    c=S.sympify(c)
    if var:
        n,d=c.as_numer_denom(); numerator=term(n,var)
        return numerator if d==1 else ('-' if n<0 else '')+r'\frac{'+term(abs(n),var)+'}{'+str(d)+'}'
    return tex(c)
def intercept(c,delta): return add(term(c,'x'),tex(delta) if delta else '')
def align(rows): return r'\begin{aligned}'+r' \\ '.join(l+' & ='+r for l,r in rows)+r'\end{aligned}'
def mask(text, replacement):
    # Masks whole math components, never short expressions across prose.
    pat=r'\$\$.*?\$\$|\$(?:[^$]*)\$'
    items=list(re.finditer(pat,text,re.S)); assert len(items)==len(replacement),(len(items),len(replacement))
    result=[]; end=0
    for item,value in zip(items,replacement):
        result.append(text[end:item.start()]); delim='$$' if item.group().startswith('$$') else '$'
        result.append(delim+value+delim); end=item.end()
    return ''.join(result)+text[end:]
def values(name,p):
    f=TEMPLATES[name]['family']; var='q' if name=='q-28328' else 'p' if name in ('q-72548','q-44407','q-44515') else 't' if name=='q-215416' else 'k'
    a=p['a']; first_standard=f.startswith('two') or f=='known_standard'
    m=-p['A']/p['B'] if first_standard else p['m']
    c=a if f.startswith('both') or f=='known_standard' else -a/(p.get('D',p.get('B')))
    answer=-1/(m*c)
    L1=(add(term(p['B'],'y'),term(p['A'],'x'))+'='+tex(p['C']) if f=='known_standard' else linear(p['A'],p['B'],p['C'])) if first_standard else 'y='+intercept(a*S.Symbol(var),p['b']) if f=='both_radio' else 'y='+intercept(m,p['b'])
    if f.startswith('both'):
        L2='y='+intercept(m,p['d']) if f=='both_radio' else 'y='+intercept(a*S.Symbol(var),p['d'])
    elif f=='known_standard': L2='y='+intercept(a*S.Symbol(var),p['d'])
    elif f=='two_negative': L2=add(term(p['D'],'y'),term(a,var+'x'))+'='+tex(p['E'])
    elif f=='two_zero': L2=add(term(p['D'],'y'),term(a,var+'x'))+'='+tex(p['E'])
    else: L2=add(term(a,var+'x'),term(p.get('D',p.get('B')),'y'))+'='+tex(p.get('E',p.get('C')))
    return var,m,c,answer,L1,L2

def conversion(A,B,C,var='',order='xy',positive=False,extra=False):
    lhs=add(term(A,var+'x'),term(B,'y')) if order=='xy' else add(term(B,'y'),term(A,var+'x'))
    rows=[(lhs,tex(C)),(term(B,'y'),add(term(-A,var+'x'),tex(C) if C else ''))]
    if extra: rows.append((term(-B,'y'),add(term(A,var+'x'),tex(-C) if C else '')))
    if positive and B<0: rows[1]=(term(-B,'y'),add(term(A,var+'x'),tex(-C) if C else ''))
    if B!=1: rows.append(('y',intercept(-A/B,C/B) if not var else add(slope(-A/B,var)+'x',tex(C/B) if C else '')))
    return align(rows)

def render(name,p):
    f=TEMPLATES[name]['family']; var,m,c,k,L1,L2=values(name,p)
    raw=RAW[name]
    # Preserve each captured prompt's spacing, punctuation, answer fragment and layout.
    if name=='q-215415': P=['y = '+tex(m)+'x + '+tex(p['b']),'y = '+var+'x - '+tex(-p['d']),var,var+' =']
    elif name=='q-215416': P=['y = '+tex(m)+'x - '+tex(-p['b']),var+'x + '+tex(p['B'])+'y = '+tex(p['C']),var,var+' =']
    elif name=='q-215417': P=[tex(p['A'])+'x - '+tex(-p['B'])+'y ='+tex(p['C']),var+'x + '+tex(p['D'])+'y = '+tex(p['E']),var,var+' =']
    else: P=[L1,L2,var+'?']+([] if raw[':question/problem'].count('$')==6 else [var+'='])
    if name in ('q-72548','q-44407','q-44515'): P=[L1,L2,var+'=']
    prompt=mask(raw[':question/problem'],P)
    if name=='q-72548': prompt+='\n\n{{field-1}}'
    if ':question/worked-solution' not in raw:
        solution=OPEN+'\n\n'
        if f=='both_blank': solution+='The slopes are $'+tex(m)+'$ and $'+slope(c,var)+'.$\n\n'
        else:
            if f=='two_blank': solution+='Converting the first line to slope-intercept form gives\n\n$$\n'+conversion(p['A'],p['B'],p['C'])+'\n$$\n\n'
            solution+='Converting the second line to slope-intercept form gives\n\n$$\n'+conversion(p['a'],p.get('D',p.get('B')),p.get('E',p.get('C')),var)+'\n$$\n\n'
        solution+='Multiplying the slopes together, we have\n\n$$\n('+tex(m)+')\\cdot ('+slope(c,var)+')=-1\\,⟹\\,'+var+'='+tex(k)+'.\n$$'
    else:
        if f=='both_radio': R=['-1.', 'x',L1,slope(p['a'],var)+'.',L2,tex(m)+'.','\n'+slope(p['a'],var)+r'\cdot ('+tex(m)+')=-1\\,⟹\\,'+var+'='+tex(k)+'.\n']
        elif f=='known_standard': R=['-1.','x',L2,var+'.',L1+',','\n'+conversion(p['A'],p['B'],p['C'],order='yx')+'\n',L1,tex(m)+'.','\n'+tex(m)+r'\cdot '+var+'=-1\\,⟹\\,'+var+'='+tex(k)+'.\n']
        elif f.startswith('one_negative'):
            par='('+tex(m)+')' if m<0 else tex(m)
            R=['-1.','x',L1,tex(m)+'.',L2+',','\n'+conversion(p['a'],p['B'],p['C'],var,positive=True)+'\n',L2,slope(c,var)+'.','\n'+par+r'\cdot ('+slope(c,var)+')=-1\\,⟹\\,'+var+'='+tex(k)+'.\n']
        else:
            conv1=conversion(p['A'],p['B'],p['C'],extra=f=='two_negative')
            conv2=conversion(p['a'],p['D'],p['E'],var,order='yx' if f in ('two_negative','two_zero') else 'xy')
            product=(tex(m)+r'\cdot '+slope(c,var)) if f=='two_negative' else ('('+tex(m)+r')\cdot '+slope(c,var)) if f=='two_zero' else '('+tex(m)+r')\cdot ('+slope(c,var)+')'
            R=['-1.',L1+',','\n'+conv1+'\n',L2+',','\n'+conv2+'\n',L1,tex(m)+'.',L2,slope(c,var)+'.','\n'+product+'=-1\\,⟹\\,'+var+'='+tex(k)+'.\n']
        solution=mask(raw[':question/worked-solution'],R)
    return prompt,solution

def canonical_parameters(name,p):
    if set(p)!=set(TEMPLATES[name]['original']): raise ValueError('Exact parameter keys required')
    p={key:S.Rational(str(value)) for key,value in p.items()}
    f=TEMPLATES[name]['family']
    for key,v in p.items():
        if not v.is_Rational or abs(v)>24 or v.q>12 or (v.q!=1 and not (f=='both_blank' and key=='m')): raise ValueError('Coefficient outside peer arithmetic bounds')
    required=['a']+(['A','B'] if f.startswith('two') or f=='known_standard' else ['m'])+(['D'] if f.startswith('two') else ['B'] if f.startswith('one') else [])
    if any(p[key]==0 for key in required): raise ValueError('Degenerate/vertical/horizontal case outside finite nonzero slope scope')
    # Preserve the observed arithmetic workload and sign normalization sequence.
    if f=='both_blank' and (p['b']<0 or p['d']>0 or p['a']!=1): raise ValueError('Blank prompt sign/layout bounds')
    if f=='one_positive' and (p['B']<=1 or p['b']>0 or p['a']!=1): raise ValueError('Positive standard form layout bounds')
    if f.startswith('one_negative') and p['B']>=-1: raise ValueError('Negative standard coefficient required')
    if f=='two_negative' and (p['B']>=-1 or p['D']<=1 or p['a']!=-1): raise ValueError('Signed two-conversion bounds')
    if f=='two_zero' and (p['E']!=0 or p['B']<=1 or p['D']<=1): raise ValueError('Zero-constant layout bounds')
    if f=='two_positive' and (p['B']<=1 or p['D']!=1): raise ValueError('Unit second y coefficient required')
    if f=='two_blank' and (p['A']<=0 or p['B']>=0 or p['D']<=0 or p['a']!=1): raise ValueError('Unrated prompt sign bounds')
    if f=='known_standard' and (p['A']<=0 or p['B']<=1 or p['a']!=1): raise ValueError('Known-standard scope bounds')
    return p

def sample(name,rng):
    p={key:S.Rational(str(v)) for key,v in TEMPLATES[name]['original'].items()}
    f=TEMPLATES[name]['family']
    for key in p:
        if key in ('a','D') and ((key=='a' and f in ('both_blank','one_positive','known_standard','two_negative','two_blank')) or (key=='D' and f=='two_positive')): continue
        if key=='E' and f=='two_zero': continue
        if key in ('m','A','B','D','a'):
            old=p[key]; p[key]=S.Integer(rng.randint(2,12))*(1 if old>0 else -1)
            if key=='m' and f=='both_blank': p[key]=S.Rational(rng.choice([-1,1])*rng.randint(1,6),rng.randint(2,9))
        else: p[key]=S.Integer(rng.randint(1,12))*(1 if p[key]>=0 else -1)
    return p

def bank(name,p,profile):
    var,m,c,k,_,_=values(name,p)
    if TEMPLATES[name]['kind']=='blank': return [k],['correct']
    if profile=='observed':
        if name=='q-28328': return [-(p['a']+abs(m)+4),-1/m,k,-m,-2*k],['opaque sum replay','omit a','correct','negate known slope','opaque -2 correct replay']
        if name=='q-44407': return [-k,k,-1/k,-p['D']*m,p['D']*m],['sign','correct','reciprocal sign','multiply rather than reciprocal','multiply/sign']
        if name=='q-44515': return [1/m,-(p['D']+1)/p['C'],-p['D']/p['B'],k,-2/m],['omit standard parameter factors','opaque constant ratio replay','wrong denominator','correct','opaque twice reciprocal replay']
    return [k,-k,1/k,-1/k,-m/c],['correct','wrong sign','reciprocal','signed reciprocal','parallel slopes']

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    eligible=[n for n,s in TEMPLATES.items() if s['level']==level and (field_type is None or s['kind']==field_type)]
    if not eligible or template is not None and template not in eligible: raise ValueError('Unsupported template/level/field')
    rng=random.Random(seed); name=template or rng.choice(eligible)
    kind=TEMPLATES[name]['kind']; profile=profile or ('authored' if kind=='radio' else 'blank')
    if profile not in (('authored','observed') if kind=='radio' else ('blank',)): raise ValueError('Unsupported complete bank profile')
    for attempt in range(200):
        p=canonical_parameters(name,parameters if parameters is not None else sample(name,rng))
        options,recipes=bank(name,p,profile)
        if any(v.is_Rational is not True or v.is_finite is not True for v in options) or len(set(options))!=len(options):
            if parameters is not None: raise ValueError('Complete bank collision')
            continue
        prompt,solution=render(name,p); var,m,c,k,L1,L2=values(name,p)
        # Normalize the slope equation under parameter renaming; constants and layout
        # do not affect the assessed parameter-solving operation.
        mathematical={'constraint_coefficient':str(m*c),'unknown_role':'x coefficient','domain':'unique real finite nonzero slopes'}
        finger=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()
        content=hashlib.sha256(json.dumps([VERSION,level,prompt,solution,kind,sorted(map(str,options))],sort_keys=True).encode()).hexdigest()
        qid=str(uuid.uuid5(NS,content)); fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
        answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(v))),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in options]
        correct_id=answers[options.index(k)][':answer/id']
        rng.shuffle(answers)
        q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if kind=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
        return {'knowledge_point':{'db_id':KP,'id':str(NS),'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':name,'family':TEMPLATES[name]['family'],'parameters':{a:str(b) for a,b in p.items()},'bank_profile':profile,'bank_origin':'observed with unresolved interpretations' if profile=='observed' else 'authored' if kind=='radio' else 'observed blank or supported repair','recipes':recipes,'parameter_fingerprint':finger,'content_fingerprint':content,'source_analysis':{key:SOURCE[key] for key in ('database','basis','lineage')},'source_ids':[name],'plot_rating':'none','domain':'finite nonzero slopes; unique real parameter; integer coefficients bounded by 24; easy known slope denominator at most 12','unrated_placement':name in ('q-215415','q-215416','q-215417'),'source_format_repair':name in ('q-215415','q-215416','q-215417','q-72548'),'answer':str(k),'sympy_version':S.__version__}}
    raise ValueError('No eligible complete bank after bounded resampling')

# Easy: no conversion; moderate: one conversion; hard: two conversions.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); a.add_argument('--seed',type=int,default=0); a.add_argument('--count',type=int,default=1); a.add_argument('--template'); a.add_argument('--profile'); a.add_argument('--format',choices=['markdown','json'],default='markdown'); args=a.parse_args()
    if args.count<1: a.error('Positive count required')
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
