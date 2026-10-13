#!/usr/bin/env python3
"""Three-path/two-coordinate chain rule, frozen math basis1356, steps3–7 only.

Each observed family has a complete expression-slot source mask; arithmetic
stages are recomputed, not copied questions. Historical opaque distractors are
public evidence-only profiles. Defaults choose a family and a complete assessed-
method bank BEFORE parameters. The finite domains are unordered same-workload
variations. Easy is explicitly authored affine three-path practice. No plots
change: the source s/t highlighted tree diagrams are reused unchanged.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid, functools
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'17592186166750'
RAW=json.loads((OUT/'source.json').read_text()); KP=RAW['record']; VERSION='three-path-1'
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
x,y,z,s,t=S.symbols('x y z s t', real=True); c1,c2,c3=S.symbols('c1 c2 c3')
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
LOC={str(v):v for v in (x,y,z,s,t,c1,c2,c3)}|{'sin':S.sin,'cos':S.cos,'log':S.log,'exp':S.exp,'e':S.E,'C':c1,'J':c2,'K':c3}

@functools.lru_cache(maxsize=10000)
def parse(tex):
    """Independent displayed-expression reader, exact and deliberately strict."""
    q=tex.strip().rstrip('.,').replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
    q=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:' '+{'ln':'log'}.get(m[1],m[1])+' ',q)
    q=q.replace(r'\sin',' sin ').replace(r'\cos',' cos ').replace(r'\ln',' log ').replace(r'\log',' log ')
    def group(i):
        assert q[i]=='{',q
        depth=1;j=i+1
        while depth:
            depth+=(q[j]=='{')-(q[j]=='}');j+=1
        return q[i+1:j-1],j
    while r'\frac' in q:
        i=q.index(r'\frac'); a,j=group(i+5);b,k=group(j)
        q=q[:i]+'(('+a+')/('+b+'))'+q[k:]
    q=re.sub(r'\{?c\}?_\{?([123])\}?',r'c\1',q)
    q=q.replace('{','(').replace('}',')').replace('^','**')
    q=q.replace('c_(1)','c1').replace('c_(2)','c2').replace('c_(3)','c3')
    q=q.replace('c1','C ').replace('c2','J ').replace('c3','K ')
    if '\\' in q: raise ValueError('unsupported displayed notation '+q)
    return parse_expr(q,local_dict=LOC,transformations=TRANS,evaluate=True)

def tex(e):
    if isinstance(e,S.Add) and len(e.args)==3 and all(isinstance(v,S.Mul) and len(v.args)==2 for v in e.args):
        return '+'.join('('+tex(v.args[0])+')'+r'\cdot ('+tex(v.args[1])+')' for v in e.args)
    return S.latex(e,ln_notation=True,order='none').replace(r'\left', '').replace(r'\right','')
@functools.lru_cache(maxsize=20000)
def eq(a,b):
    difference=S.expand(a-b)
    if difference==0:return True
    numerator=S.together(difference).as_numer_denom()[0]
    if numerator.is_polynomial(x,y,z,s,t,c1,c2,c3):return S.expand(numerator)==0
    return S.simplify(difference)==0
def add(*args):return S.Add(*args,evaluate=False)
def mul(*args):return S.Mul(*args,evaluate=False)

# Moderate: six observed families; signed outer linear coefficients, exponential
# or quadratic substitution, at most degree2 coordinate maps (except observed
# product exponential). Bounds are applied to explicit inputs as well.
# Hard: six observed families; quotient/log cancellation, polynomial expansion,
# trigonometric held-coordinate product, and supplied coefficient extraction.
BASE={
 'q-94589':{'a':1,'b':3},'q-94814':{'a':4,'b':2},
 'q-170675':{'a':1,'b':1},'q-37132':{'a':3,'b':5},
 'q-94811':{'a':3,'b':2},'q-94812':{'a':2,'b':1,'c':1},
 'q-94813':{'a':1,'b':1},'q-94815':{'a':2,'b':3},
 'q-94816':{'a':2,'b':4},'q-170674':{'a':1,'b':1},
 'q-37208':{'a':1,'b':2,'c':1},'q-37206':{'a':1,'b':1}}
LEVEL={k:v[':question/difficulty'][':db/ident'].split('/')[-1] for k,v in QUESTIONS.items()}|{'affine':'easy'}
DOMAINS={k:{'a':list(range(1,7)),'b':list(range(1,7))} for k in BASE}
DOMAINS['q-37132']['a']=[2,3,4,5]
DOMAINS['q-94812']['b']=list(range(1,7));DOMAINS['q-94812']['c']=list(range(1,7))
DOMAINS['q-94813']['b']=list(range(1,7))
DOMAINS['q-170674']['a']=list(range(1,7));DOMAINS['q-170674']['b']=list(range(1,7))
DOMAINS['q-37208']['a']=list(range(1,7));DOMAINS['q-37208']['c']=list(range(1,7))
DOMAINS['affine']={k:[-3,-2,-1,1,2,3] for k in ['a','b','c','d','e','h']}

def objects(k,p):
    a,b=p['a'],p['b']
    if k=='q-94589':f=x*x+2*a*x*y-b*z*z; maps=[s*t,s+3*t,2*s-t];u=t
    elif k=='q-94814':f=a*x+3*y-b*z;maps=[2*s*s-t,s+3*t*t,4*s*s+t*t];u=s
    elif k=='q-170675':f=(a*y+b*z)/x;maps=[s+t,s*s,t*t];u=t
    elif k=='q-37132':f=x*x*y-b*y*z;maps=[s*t,s**a,s*S.sin(t)];u=s
    elif k=='q-94811':f=a*x-b*y+z;maps=[s+t,s*s-t*t,s];u=t
    elif k=='q-94812':f=x*y*z;maps=[S.Integer(a),s*S.exp(b*t),t*S.exp(p['c']*s)];u=t
    elif k=='q-94813':f=S.exp(x+y+z);maps=[s-t,a*t*t,b*s+t];u=t
    elif k=='q-94815':f=x*x+y*y+z*z;maps=[t+a*s,b*t-s,s*t];u=s
    elif k=='q-94816':f=S.log(x)-a*S.exp(y)+b*z;maps=[t*s*s,S.log(t*t+s*s),s*s];u=s
    elif k=='q-170674':f=z-a*x-b*y;maps=[S.exp(s)+t,s+1,1-t-s];u=s
    elif k=='q-37208':f=S.cos(x)+y*y*z;maps=[3*t,p['c']*t-a*s,b*s*t];u=t
    elif k=='q-37206':f=x*y+a*y*z+b*z*z;maps=[s*s+t*t,s/t,s*t*t];u=s
    elif k=='affine':f=a*x+b*y+p['c']*z;maps=[p['d']*s+t,p['e']*s-t,p['h']*s+2*t];u=s
    else:raise ValueError('unknown template')
    parts=[S.diff(f,v) for v in (x,y,z)]
    sub={v:e for v,e in zip((x,y,z),maps)}
    partial=[S.expand(v.subs(sub)) for v in parts]
    if k=='q-170675':
        # Preserve the single quotient numerator in the substituted partial
        # and first chain-product row, as in the source family.
        partial=[-(a*s*s+b*t*t)/(s+t)**2,a/(s+t),b/(s+t)]
    coord=[S.diff(v,u) for v in maps]
    products=[S.expand(v*d) for v,d in zip(partial,coord)]
    D=S.simplify(sum(products));whole=f.subs(sub)
    coeff=None;signature=None
    if k=='q-94589':coeff=[6*a,2*b,-b];signature=2*(s*s*t+a*s*s+c1*s*t+c2*s+c3*t)
    elif k=='q-170675':coeff=[-a,2*b,b];signature=(c1*s*s+c2*s*t+c3*t*t)/(s+t)**2
    elif k=='q-37208':coeff=[3*b*p['c']**2,-4*a*b*p['c'],a*a*b];signature=-3*S.sin(3*t)+c1*s*t*t+c2*s*s*t+c3*s**3
    elif k=='q-37206':coeff=[1,2*a,2*b];signature=3*s*s/t+c1*t+c2*s*t+c3*s*t**4
    return dict(f=f,maps=maps,u=u,parts=parts,partial=partial,coord=coord,products=products,D=D,whole=whole,coeff=coeff,signature=signature,answer=S.Integer(sum(coeff)) if coeff else D)

# Every dynamic RHS is a complete mathematical component. The compiler preserves
# source punctuation, ordered rows, repeated expansion terms and static prose.
# Source spelling is an expression-local formatter anchor, never a payload branch.
def rhs_spans(block):
    out=[]
    pattern=r'=(?:\s*)'
    for m in re.finditer(pattern,block):
        start=m.end();end=len(block)
        for delimiter in ['=',r'\\',r'\end{aligned}',r',\,']:
            pos=block.find(delimiter,start)
            if pos>=0:end=min(end,pos)
        val=block[start:end]
        val=val.rstrip();trim=len(val)
        while val and val[-1] in '.,':val=val[:-1]
        out.append((start,start+len(val),val))
    return out

def substitute_structural(e, mapping):
    if e in mapping:return mapping[e]
    if not e.args:return e
    args=[substitute_structural(a,mapping) for a in e.args]
    if e.func in [S.Add,S.Mul,S.Pow,S.exp,S.log,S.sin,S.cos]:return e.func(*args,evaluate=False)
    return e.func(*args)

def distributed(o):
    terms=[]
    for e in o['products']:
        terms.extend(S.Add.make_args(e) if isinstance(e,S.Add) else [e])
    return add(*terms)

def stage_values(k,p):
    o=objects(k,p);q=QUESTIONS[k];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    results=[];has_sub='Writing the above' in q[':question/worked-solution']
    # formal operator block remains fixed; formal partials are recomputed.
    results.append(None);results.append(o['parts'])
    index=2
    if has_sub:
        src=rhs_spans(blocks[index]);values=[];j=0
        for component in range(3):
            # Count RHSs in the ordered row, retaining redundant substitution rows.
            row=blocks[index].split(r'\\')[component]
            n=len(rhs_spans(row))
            raw=substitute_structural(o['parts'][component],dict(zip((x,y,z),o['maps'])))
            values.extend([raw]+[o['partial'][component]]*(n-1));j+=n
        results.append(values);index+=1
    results.append(o['coord']);index+=1
    count=len(rhs_spans(blocks[index]))
    product=add(*(mul(v,d) for v,d in zip(o['partial'],o['coord'])))
    if k=='q-170675':
        # The source combines the three fractions over a common denominator
        # BEFORE expanding/collecting the numerator. These are distinct stages.
        a,b=p['a'],p['b']
        numerator=add(mul(-1,add(a*s*s,b*t*t)),mul(2*b,t,add(s,t)))
        denominator=S.Pow(add(s,t),2,evaluate=False)
        common=mul(numerator,S.Pow(denominator,-1,evaluate=False))
        expanded=mul(S.expand(-a*s*s-b*t*t+2*b*t*(s+t)),S.Pow(denominator,-1,evaluate=False))
        chain=[product,common,expanded]
    elif count==2:chain=[product,o['D']]
    elif count==3:chain=[product,distributed(o),o['D']]
    elif count==4:chain=[product,distributed(o),S.expand(o['D']),S.factor(o['D'])]
    else:raise AssertionError((k,count))
    results.append(chain);index+=1
    if o['coeff'] is not None:
        # final numerical sum appears with two RHSs: unevaluated coefficient sum,
        # then its collection. Coefficients are independent of chosen wrong answer.
        results.append([add(*(S.Integer(v) for v in o['coeff'])),o['answer']])
    return results

MASKS={}
for k,q in QUESTIONS.items():
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    basevalues=stage_values(k,BASE[k]); specs=[]
    for block,vals in zip(blocks,basevalues):
        spans=rhs_spans(block) if vals is not None else []
        assert len(spans)==len(vals or []),(k,spans,vals)
        for (_,_,raw),value in zip(spans,vals or []):
            assert eq(parse(raw),value),(k,raw,value)
        specs.append((block,spans,vals))
    MASKS[k]=specs

def anchored(value,base,spelling):
    return spelling if value==base else tex(value)

def render(k,p):
    o=objects(k,p)
    if k=='affine':
        image='images/be/be6afcdd0ad9ae0d7ef377c4918442a64e1186c90c25e27ec6c224d816a602fd.png'
        prompt='Let $f(x,y,z)='+tex(o['f'])+',$ where '+', '.join('$'+str(v)+'='+tex(e)+'$' for v,e in zip((x,y,z),o['maps']))+'. Calculate $'+r'\frac{∂f}{∂s}'+'.$'
        common=QUESTIONS['q-94814'][':question/worked-solution']
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',common,re.S)
        solution=common
        vals=[None,o['parts'],o['coord'],[add(*(mul(v,d) for v,d in zip(o['partial'],o['coord']))),distributed(o),o['D']]]
        for block,values in zip(blocks,vals):
            if values is None:continue
            new=block
            for (start,end,_),value in reversed(list(zip(rhs_spans(block),values))):new=new[:start]+tex(value)+new[end:]
            solution=solution.replace(block,new,1)
        return prompt,solution
    q=QUESTIONS[k];base=objects(k,BASE[k]);prompt=q[':question/problem']
    # Complete inline f/map components, not blind short-expression replacements.
    chunks=list(re.finditer(r'\$(.*?)\$',prompt,re.S));replacements=[]
    first=True
    for m in chunks:
        raw=m[1]
        if raw.startswith('f(x,y,z)='):value=o['f'];ref=base['f'];prefix='f(x,y,z)='
        elif re.match('[xyz]=',raw):
            j='xyz'.index(raw[0]);value=o['maps'][j];ref=base['maps'][j];prefix=raw[:2]
        else:continue
        suffix=raw[-1] if raw[-1] in '.,' else ''
        spelling=raw[len(prefix):len(raw)-len(suffix) if suffix else None]
        replacements.append((m.start()+1,m.end()-1,prefix+anchored(value,ref,spelling)+suffix))
    for st,en,v in reversed(replacements):prompt=prompt[:st]+v+prompt[en:]
    if o['signature'] is not None:
        b=re.search(r'\$\$\n(.*?)\n\$\$',prompt,re.S)
        spans=rhs_spans(b[1]);st,en,raw=spans[0];new=b[1][:st]+anchored(o['signature'],base['signature'],raw)+b[1][en:]
        prompt=prompt[:b.start(1)]+new+prompt[b.end(1):]
    solution=q[':question/worked-solution'];values=stage_values(k,p)
    for (block,spans,refs),vals in zip(MASKS[k],values):
        new=block
        for (st,en,raw),value,ref in reversed(list(zip(spans,vals or [],refs or []))):
            new=new[:st]+anchored(value,ref,raw)+new[en:]
        solution=solution.replace(block,new,1)
    if o['coeff'] is not None and p!=BASE[k]:
        # Mask the complete final coefficient declaration separately from its sum.
        matches=list(re.finditer(r'\$(.*?)\$',solution,re.S))
        start=solution.index('Finally,')
        end=solution.index('and therefore',start)
        solution=solution[:start]+'Finally, $'+', '.join('c_{'+str(i+1)+'}='+str(v) for i,v in enumerate(o['coeff']))+',$ '+solution[end:]
    return prompt,solution

def bank(k,o,profile):
    C=o['answer'];parts=o['products']
    if profile.startswith('observed'):
        q=QUESTIONS[k];banks=[]
        # Opaque source offsets are retained only as explicit evidence recipes.
        # They parameterize correct+original residual; no intent is asserted.
        base=objects(k,BASE[k])['answer']
        for field in q[':question/answer-fields']:
            values=[]
            for answer in field[':answer-field/choices']:
                raw=answer[':answer/value'];e=parse(raw);value=S.simplify(C+(e-base))
                values.append((raw if eq(value,e) else tex(value),value))
            banks.append(values)
        if profile=='observed-repaired':banks=banks[-1:]
        return banks
    if o['coeff'] is not None:
        A,B,H=map(S.Integer,o['coeff'])
        if k=='q-94589':vals=[C,A,H,A+H,-C]
        elif k=='q-170675':vals=[C,-C,A,A+H,-A+B+H]
        elif k=='q-37208':vals=[C,A,B,H,A+B]
        else:vals=[C,-C,A,B+H,-B-H]
    else:
        active=[v for v in parts if v!=0];p0,p1=active[:2]
        other=t if o['u']==s else s
        vals=[C,S.simplify(C-p0),S.simplify(C-p1),S.diff(o['whole'],other),S.simplify(C+p0)]
    if any(eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('whole-bank collision')
    return [[(tex(v),v) for v in vals]]

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(tag):return str(uuid.uuid5(uuid.NAMESPACE_URL,tag))
def task_fingerprint(k,o):
    # Normalize global f scaling; omit map values unused by the assessment for
    # linear outer functions, notation, banks, seeds and profile aliases.
    numerator=S.together(o['f']).as_numer_denom()[0]
    if numerator.is_polynomial(x,y,z):pivot=S.Poly(numerator,x,y,z).terms()[0][1]
    else:
        coeffs=S.Add.make_args(S.expand(o['f']));pivot=coeffs[0].as_coeff_Mul()[0]
    normalized=S.simplify(o['f']/pivot)
    used_maps=o['coord'] if all(v.is_number for v in o['parts']) else list(o['maps'])
    if k=='q-94812':used_maps[0]=S.Integer(1)  # constant x only rescales every assessed product
    if k=='q-37208':
        coeff=list(map(S.Integer,o['coeff']));g=S.gcd_list(coeff)
        return digest([k,list(map(str,[v/g for v in coeff])),str(o['u']),'supplied coefficient sum'])
    return digest([str(normalized),list(map(str,used_maps)),str(o['u']),bool(o['coeff'])])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('only observed radio shape')
    rng=random.Random(seed)
    eligible=[k for k,l in LEVEL.items() if l==level]
    if template is not None and template not in eligible:raise ValueError('template outside difficulty')
    k=template or rng.choice(eligible)
    profile=profile or 'method'
    if profile not in ['method','observed','observed-repaired']:raise ValueError('unknown profile')
    if k=='affine' and profile!='method':raise ValueError('no observed easy profile')
    domains=DOMAINS[k]
    if parameters is not None:
        if set(parameters)!=set(domains) or any(type(v)!=int or v not in domains[a] for a,v in parameters.items()):raise ValueError('parameters outside documented workload')
        p=parameters.copy();o=objects(k,p);banks=bank(k,o,profile)
    else:
        for attempt in range(2000):
            p={a:rng.choice(v) for a,v in domains.items()};o=objects(k,p)
            try:banks=bank(k,o,profile);break
            except ValueError:continue
        else:raise ValueError('no eligible instance')
    prompt,solution=render(k,p)
    identity=digest([VERSION,level,prompt,solution,sorted([sorted(v for v,_ in b) for b in banks])])
    fields=[]
    rawfields=QUESTIONS[k][':question/answer-fields'] if k!='affine' else [{}]
    if profile=='observed-repaired':rawfields=rawfields[-1:]
    for j,b in enumerate(banks):
        fid=ident(identity+'/field/'+str(j));choices=[]
        for value,e in b:
            aid=ident(fid+'/'+value);choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
        rng.shuffle(choices)
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        # Preserve missing raw correct attribute; repair has one authoritative field.
        if profile!='observed' or ':answer-field/correct' in rawfields[j]:
            correct=[a for a in choices if eq(parse(a[':answer/value']),o['answer'])]
            if len(correct)!=1:raise ValueError('ambiguous correct bank')
            field[':answer-field/correct']=[':answer/id',correct[0][':answer/id']]
        fields.append(field)
    question={':question/id':ident(identity),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    return {'knowledge_point':{'db_id':17592186166750,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'database':RAW['database'],'basis':RAW['basis'],'lineage':RAW['lineage'],'template':k,'level':level,'seed':seed,'parameters':p,'profile':profile,'evidence_only':profile!='method','eligible_for_learning':profile=='method','authored_level':level=='easy','identity':identity,'mathematical_fingerprint':task_fingerprint(k,o),'python':sys.version.split()[0],'sympy':S.__version__,'domain':('s+t != 0' if k=='q-170675' else 't > 0 and s != 0' if k=='q-94816' else 't != 0' if k=='q-37206' else 'real s,t')}}

# Easy: authored affine maps and linear outer f; all three coordinate derivatives
# are nonzero. No powers, transcendental derivatives, substitution or coefficient
# extraction. Moderate and hard retain observed independent workload families.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];rows=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):rows.extend('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    rows+=['',q.get(':question/worked-solution','')];return '\n\n'.join(rows)
if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=1);cli.add_argument('--format',choices=['markdown','json'],default='markdown');cli.add_argument('--template');cli.add_argument('--profile');a=cli.parse_args()
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
