#!/usr/bin/env python3
"""Scalar triple product property practice; current source math basis2557.

All19 sources are replayed by parameterized component masks. Raw banks are
explicit evidence-only profiles: homothetic extensions preserve complete banks
without claiming to recover historical distractor intent. Normal banks derive
actual swaps, omitted scalar factors, or omitted supplied-dot components.
No determinant or coordinate cross product calculations are introduced.
See private classification/extraction and validate.py. No DB writes or plots.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186105737
KP_UUID='3e0b4d33-7699-5068-90f1-663534cd662d'
TITLE='Calculating Scalar Triple Products Using Its Properties'
VERSION='scalar-properties-2'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
CASES=json.loads((ROOT/'source-cases.json').read_text())
CASE={c['template']:c for c in CASES}
TEMPLATES={k:{'level':'moderate','family':c['family'],'field_type':c['field_type']} for k,c in CASE.items()}
TEMPLATES.update({'single_scale':{'level':'easy','family':'scalar','field_type':'radio'},'double_scaling':{'level':'hard','family':'scalar','field_type':'radio'}})
class SampleRejected(ValueError): pass

def tex(x):
    return sp.latex(sp.simplify(sp.sympify(x))).replace(' ', '')
def group(x):
    t=tex(x); return '('+t+')' if sp.sympify(x)<0 else t

def scalar(s):
    s=s.strip().rstrip('.,').replace(r'\,','').replace(' ', '')
    s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
    while re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',s):
        s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
    s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
    s=s.replace(r'\cdot','*')
    s=re.sub(r'(\d)(sqrt\()',r'\1*\2',s)
    return sp.sympify(s)

def parity(order):
    return (-1)**sum(order[i]>order[j] for i in range(3) for j in range(i+1,3))
def triple(order='abc',factors=(1,1,1)):
    parts=[]
    for v,c in zip(order,factors):
        c=sp.sympify(c)
        parts.append(v if c==1 else '-'+v if c==-1 else group(c)+v)
    return parts[0]+r'\cdot ('+parts[1]+r'\times '+parts[2]+')'

def vf(s):
    s=s.strip().replace('(', '').replace(')','')
    v=s[-1]; assert v in 'abc'
    c=s[:-1]; return v,scalar(c) if c not in ('','-') else (1 if not c else -1)

def read_triple(s):
    outer,inner=s.split(r'\cdot ',1)
    inner=inner.strip()
    assert inner.startswith('(') and inner.endswith(')')
    left,right=inner[1:-1].split(r'\times ',1)
    parsed=[vf(x) for x in (outer,left,right)]
    return ''.join(v for v,c in parsed),[c for v,c in parsed]

def coords(v): return '⟨'+','.join(tex(x) for x in v)+'⟩'
def sumtex(values):
    out=''
    for v in values:
        t=tex(v); out+=('+' if out and not t.startswith('-') else '')+t
    return out

def stylefactor(v,c,style):
    if style=='paren_all': return '('+(v if c==1 else '-'+v if c==-1 else tex(c)+v)+')'
    s=v if c==1 else '-'+v if c==-1 else tex(c)+v
    return '('+s+')' if style=='paren_negative' and c<0 else s

def source_given(c,p):
    f=list(map(sp.sympify,p['factors']))
    z=[stylefactor(v,x,st) for v,x,st in zip('abc',f,c['styles'])]
    return z[0]+r'\cdot ('+z[1]+r'\times '+z[2]+')'

def source_render(c,p):
    """Replace complete math components; preserve every captured prose/row mask."""
    q=QUESTIONS[c['source_id']]
    target=c['target']; T=base(c,p); correct=parity(target)*T
    prompt=q[':question/problem']; solution=q[':question/worked-solution']
    first=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    oldbody=first.group(1); rows=oldbody.split(r'\\')
    if c['family']=='scalar':
        given=source_given(c,p); rhs=tex(p['rhs'])
        prompt=prompt.replace(c['given']+'='+c['rhs_tex'],given+'='+rhs)
        f=list(map(sp.sympify,p['factors']))
        facts=[group(x) for x in f if x!=1]
        factorrow=r'\cdot '.join(facts)+r'\cdot [a\cdot (b\times c)]'
        lhs=[given,factorrow]
        if len(rows)==4: lhs.append(group(sp.prod(f))+'[a'+r'\cdot (b\times c)]')
        lhs.append(r'a\cdot (b\times c)')
        newbody=r'\\'.join((' ' if i else '')+x+' & ='+(tex(T)+'.' if i==len(lhs)-1 else rhs)+(' ' if i<len(lhs)-1 else '') for i,x in enumerate(lhs))
    else:
        v,w=p['v'],p['w']; tuples=iter((coords(w),coords(v))); prompt=re.sub('⟨[^⟩]+⟩',lambda m:next(tuples),prompt)
        products=[sp.sympify(a)*sp.sympify(b) for a,b in zip(v,w)]
        rhs=[coords(v)+r'\cdot '+coords(w),'+'.join(group(a)+r'\cdot '+group(b) for a,b in zip(v,w)),sumtex(products),tex(T)+'.']
        newbody=r'\\'.join((r'a\cdot (b\times c)' if i==0 else ' ')+' & ='+value+(' ' if i<3 else '') for i,value in enumerate(rhs))
    solution=solution[:first.start(1)]+newbody+solution[first.end(1):]
    # Complete numeric RHS only in subsequent product equations; preserve separators/punctuation.
    start=solution.index(r'\end{aligned}')+len(r'\end{aligned}')
    tail=solution[start:]
    orders=re.findall(r'([abc])\\cdot \(([abc])\\times ([abc])\)',tail)
    signs=[parity(''.join(o)) for o in orders]
    n=iter(signs)
    tail=re.sub(r'(?<==)(?:\\,)?-?(?:\\frac\{\d+\}\{\d+\}|\d+)',lambda m: (r'\,' if m.group(0).startswith(r'\,') else '')+tex(next(n)*T),tail)
    solution=solution[:start]+tail
    return prompt,solution,correct

def base(c,p):
    if c['family']=='scalar': return sp.simplify(scalar(str(p['rhs']))/sp.prod(list(map(sp.sympify,p['factors']))))
    return sum(sp.sympify(x)*sp.sympify(y) for x,y in zip(p['v'],p['w']))

def validate_parameters(level,name,p,evidence=False):
    spec=TEMPLATES[name]
    if spec['family']=='vector':
        if set(p)!={'v','w'} or any(len(p[k])!=3 for k in ('v','w')): raise ValueError('Require two supplied 3-vectors')
        if any(not sp.sympify(x).is_Integer or abs(int(x))>9 for k in p for x in p[k]): raise ValueError('Supplied coordinates must be integers of magnitude<=9')
        if sum(sp.sympify(x)*sp.sympify(y) for x,y in zip(p['v'],p['w']))==0: raise SampleRejected('Nonzero triple product required')
        return
    if name in CASE:
        if set(p)!={'factors','rhs'} or len(p['factors'])!=3: raise ValueError('Require factors and rhs')
        f=list(map(sp.sympify,p['factors'])); r=sp.sympify(p['rhs'])
        if any(x==0 or (not x.is_Integer and x not in (sp.sqrt(2),-sp.sqrt(2))) or abs(x)>7 for x in f): raise ValueError('Observed scalar factor magnitude<=7, integers or signed sqrt2')
        anchor=CASE[name]['parameters']['factors']
        if any((sp.sympify(a)==1)!=(x==1) for a,x in zip(anchor,f)): raise ValueError('Preserve each source mask nonunit factor position')
        if sum(x!=1 for x in f)<2 or not any(abs(x)>1 for x in f): raise ValueError('Moderate retains at least two nonunit supplied factors and a substantive magnitude')
        if name=='q-20059':
            if abs(f[1])!=sp.sqrt(2) or any(not f[i].is_Integer for i in (0,2)): raise ValueError('Radical mask retains signed sqrt2 in the middle slot')
        elif any(not x.is_Integer for x in f): raise ValueError('Integer source masks retain integer factors')
        T=sp.simplify(r/sp.prod(f))
        if not T.is_Rational or T==0 or abs(T)>26 or abs(r)>500 or sp.denom(T)>12: raise ValueError('Moderate rational workload exceeded')
        if not evidence and len([x for x in f if x!=1])<2: raise ValueError('Moderate factor workload')
    else:
        expect={'factor','base','target'} if level=='easy' else {'factors','base','target','requested'}
        if set(p)!=expect or p['target'] not in ('bac','bca','cab','cba','acb'): raise ValueError('Invalid authored parameter shape/order')
        if not isinstance(p['base'],int) or not 1<=abs(p['base'])<=9: raise ValueError('Base magnitude1..9')
        if level=='easy':
            if not isinstance(p['factor'],int) or not 2<=abs(p['factor'])<=7: raise ValueError('Easy one factor magnitude2..7')
        else:
            if len(p['factors'])!=3 or len(p['requested'])!=3: raise ValueError('Hard factor triples required')
            if any(not isinstance(x,int) or not 2<=abs(x)<=5 for x in p['factors']): raise ValueError('Hard three factors magnitude2..5')
            if p['requested'][0]!=1 or any(not isinstance(x,int) or not 2<=abs(x)<=4 for x in p['requested'][1:]): raise ValueError('Hard two requested inner factors magnitude2..4')

def authored_render(level,p):
    T=sp.Integer(p['base']); order=p['target']
    f=(p['factor'],1,1) if level=='easy' else tuple(p['factors'])
    requested=(1,1,1) if level=='easy' else tuple(p['requested'])
    given=triple('abc',f); wanted=triple(order,requested); rhs=sp.prod(f)*T
    prompt='Find $'+wanted+'$, if $'+given+'='+tex(rhs)+'.$'
    solution='First, we factor out the constants and get\n\n$$\n'+r'\begin{aligned}'+given+' & ='+tex(rhs)+r' \\ '+r'\cdot '.join(group(x) for x in f if x!=1)+r'\cdot [a\cdot (b\times c)] & ='+tex(rhs)+r' \\ a\cdot (b\times c) & ='+tex(T)+r'.\end{aligned}'+'\n$$'
    # Find shortest sequence of actual pair swaps, preserving source instructional move.
    seq=['abc']; swaps=[]
    for depth in (1,2):
        found=False
        for pairs in itertools.product(((0,1),(0,2),(1,2)),repeat=depth):
            cur=list('abc'); route=[]
            for i,j in pairs:
                names=(cur[i],cur[j]);cur[i],cur[j]=cur[j],cur[i];route.append((''.join(cur),names))
            if ''.join(cur)==order: swaps=route;found=True;break
        if found: break
    for i,(o,(a,b)) in enumerate(swaps):
        solution+='\n\n'+('Then, we swap ' if not i else 'and again we swap ')+'$'+a+'$ and $'+b+'$ to get\n\n$$\n'+r'\begin{aligned}'+triple(o)+' & ='+tex(parity(o)*T)+r'.\end{aligned}'+'\n$$'
    correct=parity(order)*sp.prod(requested)*T
    if level=='hard':
        solution+='\n\nFactoring out the constants in the requested product, we get\n\n$$\n'+r'\begin{aligned}'+wanted+' & ='+r'\cdot '.join(group(x) for x in requested if x!=1)+'['+triple(order)+']'+r' \\ & ='+r'\cdot '.join(group(x) for x in requested if x!=1)+r'\cdot '+group(parity(order)*T)+r' \\ & ='+tex(correct)+r'.\end{aligned}'+'\n$$'
    return prompt,solution,correct

def bank(name,p,correct,profile):
    c=CASE.get(name)
    if profile.startswith('observed:'):
        original=c['parameters']; ratio=sp.simplify(base(c,p)/base(c,original))
        # Historical opaque complete bank homothety, never an inferred error algorithm.
        out=[]
        for val in c['bank']:
            if val.startswith('⟨'):
                vals=[scalar(x) for x in val[1:-1].split(',')]; out.append(coords([x*ratio for x in vals]))
            else: out.append(tex(scalar(val)*ratio))
        return out,['opaque historical bank homothety']*len(out)
    if TEMPLATES[name]['field_type']=='blank': return [tex(correct)],['correct']
    if c and c['family']=='vector':
        terms=[sp.sympify(x)*sp.sympify(y) for x,y in zip(p['v'],p['w'])]; sign=parity(c['target'])
        values=[correct,-correct]+[sign*(sum(terms)-t) for t in terms]
        recipes=['correct','miss swap parity','omit first dot term','omit second dot term','omit third dot term']
    else:
        if c:
            f=list(map(sp.sympify,p['factors'])); rhs=sp.sympify(p['rhs']); sign=parity(c['target']); nonunit=[x for x in f if x!=1]
            values=[correct,-correct,sign*rhs,correct*nonunit[0],correct*nonunit[-1]]
            recipes=['correct','miss swap parity','omit all supplied factors','omit first supplied factor','omit last supplied factor']
        elif name=='single_scale':
            f=p['factor'];rhs=f*p['base'];sign=parity(p['target'])
            values=[correct,-correct,sign*rhs,-sign*rhs,sign*rhs*f]
            recipes=['correct','miss swap parity','omit supplied factor','omit factor and sign swap','multiply rather than divide supplied factor']
        else:
            req=p['requested']; f=p['factors']; sign=parity(p['target']); T=p['base']
            values=[correct,-correct,sign*T,sign*T*req[1],sign*T*req[2]]
            recipes=['correct','miss swap parity','omit both requested factors','omit last requested factor','omit first requested factor']
    if len(set(map(sp.simplify,values)))!=len(values): raise SampleRejected('Whole bank collision')
    return list(map(tex,values)),recipes

def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def identity(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unsupported level')
    if profile and profile.startswith('observed:'):
        implied=profile.split(':',1)[1]
        if template and template!=implied: raise ValueError('Profile/template mismatch')
        template=implied
    eligible=[n for n,s in TEMPLATES.items() if s['level']==level and (field_type is None or s['field_type']==field_type)]
    if template and template not in eligible: raise ValueError('Unsupported template/level/field')
    rng=random.Random(seed); name=template or rng.choice(eligible); c=CASE.get(name)
    profile=profile or 'method-derived'
    if profile!='method-derived' and profile!='observed:'+name: raise ValueError('Unsupported profile')
    evidence=profile.startswith('observed:')
    for attempt in range(1000):
        if parameters is not None: p=dict(parameters)
        elif evidence: p=dict(c['parameters'])
        elif c:
            if c['family']=='vector': p={k:[rng.randint(-9,9) for _ in range(3)] for k in ('v','w')}
            else:
                f=[rng.choice((-7,-6,-5,-4,-3,-2,2,3,4,5,6,7)) if x!='1' else 1 for x in c['parameters']['factors']]
                if name=='q-20059': f[1]=rng.choice((sp.sqrt(2),-sp.sqrt(2)))
                T=sp.Rational(rng.choice([x for x in range(-9,10) if x]),rng.choice((1,2,3)))
                p={'factors':list(map(str,f)),'rhs':str(sp.prod(f)*T)}
        elif level=='easy': p={'factor':rng.choice((-7,-6,-5,-4,-3,-2,2,3,4,5,6,7)),'base':rng.choice([x for x in range(-9,10) if x]),'target':rng.choice(('bac','bca','cab','cba','acb'))}
        else: p={'factors':[rng.choice((-5,-4,-3,-2,2,3,4,5)) for _ in range(3)],'base':rng.choice([x for x in range(-9,10) if x]),'target':rng.choice(('bac','bca','cab','cba','acb')),'requested':[1,rng.choice((-4,-3,-2,2,3,4)),rng.choice((-4,-3,-2,2,3,4))]}
        try:
            validate_parameters(level,name,p,evidence)
            prompt,solution,correct=source_render(c,p) if c else authored_render(level,p)
            values,recipes=bank(name,p,correct,profile)
            # Raw source vector bank is intentionally ineligible; preserve it publicly.
            if not evidence and any(v.startswith('⟨') for v in values): raise SampleRejected('Scalar required')
            break
        except ValueError:
            if parameters is not None or evidence: raise
    else: raise SampleRejected('Bounded sampling exhausted')
    style=TEMPLATES[name]['field_type']; key='field-1' if style=='blank' else 'selection'
    if style=='blank' and '{{'+key+'}}' not in prompt: prompt+='\n\n$'+(triple(p['target'],p.get('requested',(1,1,1))) if not c else triple(c['target']))+'=$\n{{'+key+'}}'
    prompt=normalize_prose(prompt); solution=normalize_prose(solution); values=[normalize_tex(x) for x in values]
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(values),'type':style}
    contenthash=digest(content); qid=identity(contenthash); fid=identity(qid+':'+key)
    answers=[{':answer/id':identity(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    answer=next(a for a in answers if not a[':answer/value'].startswith('⟨') and scalar(a[':answer/value'])==correct)
    rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+style,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answer[':answer/id']]}
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
    # Canonicalize actual assessed relation and supplied operands; exclude banks/seed/profile aliases.
    if c and c['family']=='vector': task={'operation':'supplied-dot-then-permutation','v':p['v'],'w':p['w'],'target':c['target']}
    else:
        f=p['factors'] if c or level=='hard' else [p['factor'],1,1]
        rhs=p['rhs'] if c else str(sp.prod(f)*p['base'])
        task={'operation':'scaling-then-permutation','given_factors':list(map(lambda x:str(sp.sympify(x)),f)),'given_rhs':str(sp.sympify(rhs)),'target':c['target'] if c else p['target'],'requested_factors':p.get('requested',[1,1,1])}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'recipes':recipes,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':name if c else 'e-4349','evidence_only':evidence,'eligible_for_learning':not evidence,'authored_level':level!='moderate','mathematical_fingerprint':digest(task),'content_fingerprint':contenthash,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY — one supplied factor and one/two swaps. Authored reduced canonical workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — all19 observed masks: factor extraction or supplied dot, then swaps.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — three supplied factors and two requested factors; same taught properties.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']+[f"- ${a[':answer/value']}$" for a in f[':answer-field/choices']]
    lines+=['',q[':question/worked-solution']]
    return '\n'.join(lines)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=('all','easy','moderate','hard'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=('radio','blank'));a=ap.parse_args()
    if a.count<1: ap.error('Positive count required')
    records=[generate(l,a.seed+i,a.template,a.field_type,profile=a.profile) for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
