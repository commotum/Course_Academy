#!/usr/bin/env python3
"""Directional derivatives, frozen math basis 1356. Steps 3–7 only.
Raw source profiles are homogeneous-function parameterized evidence replays;
opaque scalar banks are never default learner banks. Normal generators retain
source formal derivative, unit-vector, substitution and dot-product stages.
Easy: supplied gradient or elementary 2D partials; moderate: two-term
exponential/polynomial gradient and A-to-B; moderate also includes the nested-square chain-rule family. Current moderate
source evidence supersedes the earlier authored hard claim; hard is unsupported.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186124458-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S
KP=17592186124458
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
REC=CAPTURE['record']; ORIGINALS={str(q[':db/id']):q for q in REC[':knowledge-point/questions']}
VERSION='directional-derivative-2'
SUPPORTED_LEVELS=('easy','moderate')
x,y=S.symbols('x y',real=True)
FAMILIES={'linear_y2':'easy','chain_square':'moderate','supplied_gradient':'easy','xy':'easy','log':'easy','quadratic':'easy','exp':'moderate','x2_linear':'easy'}
SOURCE_IDS=dict(zip(FAMILIES,ORIGINALS))

def tex(a):return S.latex(S.simplify(a)).replace(r'\log',r'\ln')
def expr_tex(a):return S.latex(a).replace(r'\log',r'\ln')
def grp(a):return '('+tex(a)+')'
def vec(a,b):return '⟨'+tex(a)+','+tex(b)+'⟩'
def ib(a,b):
    return tex(a)+r'\,i'+('+' if b>=0 else '-')+tex(abs(b))+r'\,j'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def subtex(e,a,b):
    # Exact held-coordinate substitution, including implicit products xy.
    t=S.latex(e)
    return re.sub(r'(?<![A-Za-z\\])x(?![A-Za-z])',lambda m:grp(a),re.sub(r'(?<![A-Za-z\\])y(?![A-Za-z])',lambda m:grp(b),t))
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def fingerprint(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

# Raw source masks: whole components, never global replacement of short numbers.
# s scales the mathematical function, so gradients and directional derivatives
# scale together. Direction and evaluation point are fixed by each raw family.
def raw_masks(f,s):
    c=lambda n: str(n*s)
    k=lambda n: '' if n*s==1 else ('-' if n*s==-1 else str(n*s))
    if f=='linear_y2':return {'2x + y^{2}':c(2)+'x + '+k(1)+'y^{2}'}
    if f=='chain_square':return {'(x + y^{2})^{2}':k(1)+'(x + y^{2})^{2}'}
    if f=='supplied_gradient':return {
        r'\text{div}\,V':k(1)+r'\text{div}\,V',
        r'4\,i+2\,j':c(4)+r'\,i+'+c(2)+r'\,j',
        r'4\cdot (-3)+2\cdot 4':c(4)+r'\cdot (-3)+'+c(2)+r'\cdot 4',
        r'-\frac{4}{5}':r'-\frac{'+c(4)+'}{5}'}
    if f=='xy':return {
        'xy':k(1)+'xy',r'y\,i+x\,j':k(1)+r'y\,i+'+k(1)+r'x\,j',
        r'i+2\,j':k(1)+'i+'+c(2)+r'\,j',r'1(\sqrt{3})+2(1)':c(1)+r'(\sqrt{3})+'+c(2)+'(1)',
        r'\frac{\sqrt{3}+2}{2}':r'\frac{'+k(1)+r'\sqrt{3}+'+c(2)+'}{2}'}
    if f=='log':return {
        r'\operatorname{ln}⁡({x}^{2}+{y}^{2})':k(1)+r'\operatorname{ln}⁡({x}^{2}+{y}^{2})',
        r'\frac{2x}':r'\frac{'+c(2)+'x}',r'\frac{2y}':r'\frac{'+c(2)+'y}',
        r'\frac{2(0)}':r'\frac{'+c(2)+'(0)}',r'\frac{2(-1)}':r'\frac{'+c(2)+'(-1)}',
        r'-2\,j': '-'+c(2)+r'\,j',r'-\frac{2(4)}{5}':r'-\frac{'+c(2)+'(4)}{5}',r'-\frac{8}{5}':r'-\frac{'+c(8)+'}{5}'}
    if f=='quadratic':return {
        '{x}^{2}+{y}^{2}-xy':k(1)+'{x}^{2}+'+k(1)+'{y}^{2}-'+k(1)+'xy',
        '2x-y':c(2)+'x-'+k(1)+'y','2y-x':c(2)+'y-'+k(1)+'x',
        '2(1)-1':c(2)+'(1)-'+c(1),'i+j':k(1)+'i+'+k(1)+'j',
        '1(1)+1(-1)':c(1)+'(1)+'+c(1)+'(-1)'}
    if f=='exp':return {
        'x{e}^{y}+{x}^{2}y':k(1)+'x{e}^{y}+'+k(1)+'{x}^{2}y',
        '{e}^{y}+2xy':k(1)+'{e}^{y}+'+c(2)+'xy','x{e}^{y}+{x}^{2}':k(1)+'x{e}^{y}+'+k(1)+'{x}^{2}',
        r'{e}^{0}+2\cdot 1\cdot 0':k(1)+r'{e}^{0}+'+c(2)+r'\cdot 1\cdot 0',
        r'1\cdot {e}^{0}+{1}^{2}':c(1)+r'\cdot {e}^{0}+'+('' if s==1 else str(s)+r'\cdot ')+'{1}^{2}',
        '⟨1,\\,2⟩':'⟨'+c(1)+',\\,'+c(2)+'⟩',
        r'\frac{\sqrt{2}}{2}':r'\frac{'+k(1)+r'\sqrt{2}}{2}'}
    return {'6{x}^{2}+2y':c(6)+'{x}^{2}+'+c(2)+'y',r'12x\,i+2\,j':c(12)+r'x\,i+'+c(2)+r'\,j',
            r'(12\cdot 0)\,i+2\,j':'('+c(12)+r'\cdot 0)\,i+'+c(2)+r'\,j',
            '2j':c(2)+'j',r'0\cdot 3+2\cdot 5':r'0\cdot 3+'+c(2)+r'\cdot 5',
            r'\frac{10\sqrt{34}}{34}':r'\frac{'+c(10)+r'\sqrt{34}}{34}'}

def slot_render(text,masks):
    # Components are masked before insertion, preventing recursive replacement.
    if not masks:return text
    return re.sub('|'.join(re.escape(v) for v in sorted(masks,key=len,reverse=True)),lambda m:masks[m.group()],text)

def scale_value(value,s):
    """Homogeneous observed expression shape; interpretation intentionally opaque."""
    # Source choices have integer/radical or integer/radical numerators. Only
    # numerator coefficients scale: denominator and radicand remain unchanged.
    if value=='0':return '0'
    if value.startswith('-'):return '-'+scale_value(value[1:],s)
    if value.startswith(r'\frac'):
        depth=0; end=None
        for i,ch in enumerate(value[5:],5):
            depth+= (ch=='{')-(ch=='}')
            if depth==0:end=i;break
        numerator=value[6:end]
        return r'\frac{'+scale_value(numerator,s)+'}'+value[end+1:]
    if '+' in value:return '+'.join(scale_value(v,s) for v in value.split('+'))
    # Internal subtraction appears only sqrt3-1.
    if '-' in value:return '-'.join(scale_value(v,s) for v in value.split('-'))
    m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',value)
    if m:
        n=int(m[1] or 1)*s
        return ('' if n==1 else str(n))+r'\sqrt{'+m[2]+'}'
    return str(int(value)*s)

# Explicit raw evidence replay preserves attribute presence; no inferred
# correct ref or authored difficulty is inserted in an incomplete source.
def raw_replay(f,level,seed,p):
    if set(p)!={'scale'} or not isinstance(p['scale'],int) or not 1<=p['scale']<=6:raise ValueError('raw profiles require integer scale 1..6')
    s=p['scale']; src=ORIGINALS[SOURCE_IDS[f]]
    q={k:copy.deepcopy(v) for k,v in src.items() if k not in (':db/id',':question/id',':question/math-academy-id')}
    masks=raw_masks(f,s)
    for key in (':question/problem',':question/worked-solution'):
        if key in q:q[key]=slot_render(q[key],masks)
    for fld in q.get(':question/answer-fields',[]):
        fld.pop(':db/id',None);fld[':answer-field/type']=fld[':answer-field/type'][':db/ident']
        for a in fld[':answer-field/choices']:
            a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=scale_value(a[':answer/value'],s)
        if ':answer-field/correct' in fld:
            old=fld[':answer-field/correct'][':answer/id'];fld[':answer-field/correct']=[':answer/id',old]
    if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    return finish(q,f,level,seed,p,'raw_'+f,False,{'source_id':SOURCE_IDS[f],'raw':True,'scale':s})

def math_data(f,p):
    a,b,c,d=map(S.sympify,[p['a'],p['b'],p['c'],p['d']]);A,B=map(S.sympify,[p['x0'],p['y0']])
    functions={'linear_y2':a*x+b*y**2,'chain_square':a*(x+b*y**2)**2,'xy':a*x*y,'log':a*S.log(x*x+y*y),'quadratic':a*x*x+b*y*y-c*x*y,'exp':a*x*S.exp(y)+b*x*x*y,'x2_linear':a*x*x+b*y,'supplied_gradient':a*x+b*y}
    F=functions[f];dx,dy=map(S.sympify,[p['dx'],p['dy']]);N=S.sqrt(dx*dx+dy*dy)
    G=[S.diff(F,t) for t in (x,y)];E=[S.simplify(g.subs({x:A,y:B})) for g in G];T=[E[0]*dx,E[1]*dy]
    return F,G,E,dx,dy,N,T,S.simplify(sum(T)/N)

def guard(f,level,p):
    if set(p)!={'a','b','c','d','x0','y0','dx','dy'}:raise ValueError('normal parameter keys must be a,b,c,d,x0,y0,dx,dy')
    for k in ('a','b','c','d','x0','y0'):
        if not isinstance(p[k],int):raise ValueError(k+' must be an integer')
    if not all(1<=p[k]<=4 for k in ('a','b','c','d')):raise ValueError('coefficients 1..4')
    if not all(abs(p[k])<=3 for k in ('x0','y0')):raise ValueError('point coordinates -3..3')
    dx,dy=S.sympify(p['dx']),S.sympify(p['dy'])
    allowed={S.Integer(i) for i in range(-5,6)}
    if f=='xy':allowed|={S.sqrt(3),-S.sqrt(3)}
    if dx not in allowed or dy not in allowed or dx==0 or dy==0:raise ValueError('direction components nonzero, integer -5..5 or ±sqrt3')
    if f=='log' and p['x0']==p['y0']==0:raise ValueError('log domain excludes origin')
    if f=='exp' and (p['y0']!=0 or p['x0']==0):raise ValueError('moderate exp evaluation requires y0=0, nonzero x0')
    if f=='chain_square' and (p['y0']==0 or p['x0']+p['b']*p['y0']**2==0):raise ValueError('hard square requires nonzero inner value and y derivative')
    if f in ('chain_square','exp') and max(abs(dx),abs(dy))>4:raise ValueError('moderate/hard direction components bounded by 4')
    if f=='chain_square':
        inner=p['x0']+p['b']*p['y0']**2
        gx=2*p['a']*inner;gy=4*p['a']*p['b']*p['y0']*inner
        if max(abs(gx),abs(gy))>48 or max(abs(gx*dx),abs(gy*dy))>192:raise ValueError('hard component arithmetic ceiling 48, products 192')

def sample(f,r):
    p={k:r.randint(1,4) for k in ('a','b','c','d')};p.update({k:r.randint(-3,3) for k in ('x0','y0')})
    ds=(-5,-4,-3,-2,-1,1,2,3,4,5) if FAMILIES[f]=='easy' else (-4,-3,-2,-1,1,2,3,4)
    p.update(dx=r.choice(ds),dy=r.choice(ds))
    if f=='exp':p.update(y0=0,x0=r.choice((-3,-2,-1,1,2,3)))
    if f=='xy' and r.randrange(2):p.update(dx='sqrt(3)',dy=r.choice((-1,1)))
    return p

# Whole method-derived banks, selected before parameters. No pool substitutions.
# dot: correct; omit y component; reverse y sign; forget normalization;
# normalize by squared norm. zero: zero; omit y; omit x; subtract the two
# component products without normalization; multiply that difference by norm.
def bank(data,profile):
    F,G,E,dx,dy,N,T,C=data
    if profile=='method':return [C,T[0]/N,(T[0]-T[1])/N,sum(T),sum(T)/(N*N)]
    if profile=='zero_method':return [C,T[0]/N,T[1]/N,T[0]-T[1],N*(T[0]-T[1])]
    raise ValueError('unknown method profile')

def normal_solution(f,p,data):
    F,G,E,dx,dy,N,T,C=data;A,B=p['x0'],p['y0'];point='('+str(A)+','+str(B)+')'
    intro="The directional derivative ${f}_{u}^{′}(a,b)$ of a function $f(x,y)$ at the point $(a,b)$ in the direction of the vector $v$ is given by\n\n$$\n{f}_{u}^{′}(a,b)=∇f(a,b)\\cdot u\n$$\n\nwhere $u$ is a unit vector in the direction of $v.$\n\n"
    if f in ('exp','chain_square'):
        intro+='First, we find the direction vector and the corresponding unit vector:\n\n'
        intro+=aligned([r'\overset{\to }{AB} & ='+vec(A+dx,B+dy)+'-'+vec(A,B),r' & ='+vec(dx,dy),r'u & =\frac{\overset{\to }{AB}}{‖\overset{\to }{AB}‖}',r' & =\frac{1}{\sqrt{'+grp(dx)+r'^{2}+'+grp(dy)+r'^{2}}}'+vec(dx,dy),r' & =\frac{1}{'+tex(N)+'}'+vec(dx,dy)])
    else:
        intro+='First, we find the unit vector $u$ in the direction of $v:$\n\n'
        intro+=aligned([r'‖v‖ & =\sqrt{'+grp(dx)+r'^{2}+'+grp(dy)+r'^{2}}='+((r'\sqrt{'+tex(dx*dx+dy*dy)+'}=' ) if f=='supplied_gradient' else '')+tex(N),r'u & =\frac{1}{'+tex(N)+'}('+ib(dx,dy)+')'])
    if f=='supplied_gradient':
        intro+='\n\nThe given gradient at the point $'+point+'$ is\n\n$$\n∇f'+point+'='+vec(*E)+'.\n$$'
    else:
        wording='calculate' if f in ('exp','chain_square') else 'compute'
        intro+='\n\nNow, we '+wording+' the gradient $∇f(x,y)$ and evaluate it at the point $'+('A' if f in ('exp','chain_square') else '')+point+':$\n\n'
        rows=[r'∇f(x,y) & =⟨\frac{∂}{∂x}('+expr_tex(F)+r'),\frac{∂}{∂y}('+expr_tex(F)+')⟩']
        if f=='chain_square':
            inn='x+'+str(p['b'])+'y^{2}';common=str(2*p['a'])+'('+inn+')'
            rows.append(r' & =⟨'+common+r'\cdot 1,'+common+r'\cdot '+str(2*p['b'])+'y⟩')
        rows.append(r' & ='+vec(*G))
        rows.append('∇f'+point+' & =⟨'+subtex(G[0],A,B)+','+subtex(G[1],A,B)+'⟩')
        # Source xy omits a redundant numeric substitution row.
        if f=='xy':rows.pop()
        rows.append(('∇f'+point if f=='xy' else '')+' & ='+vec(*E))
        intro+=aligned(rows)
    intro+='\n\nTherefore, the directional derivative is'+(':' if f=='exp' else '')+'\n\n'
    rows=['{f}_{u}^{′}'+point+' & =∇f'+point+r'\cdot u',r' & ='+vec(*E)+r'\cdot '+vec(dx/N,dy/N)]
    # Exp source reduces its final dot directly; every other source displays
    # the component products and denominator before the collected answer.
    if f!='exp':rows.append(r' & =\frac{'+grp(E[0])+r'\cdot '+grp(dx)+'+'+grp(E[1])+r'\cdot '+grp(dy)+'}{'+tex(N)+'}')
    rows.append(r' & ='+tex(C)+'.')
    return intro+aligned(rows)

def finish(q,f,level,seed,p,profile,eligible,extra):
    fields=q.get(':question/answer-fields',[])
    banks=[[a[':answer/value'] for a in fld[':answer-field/choices']] for fld in fields]
    layouts=[]
    for fld,b in zip(fields,banks):
        correct=fld.get(':answer-field/correct',[None,None])[1]
        value=next((a[':answer/value'] for a in fld[':answer-field/choices'] if a[':answer/id']==correct),None)
        layouts.append([fld[':answer-field/key'],fld[':answer-field/type'],sorted(b),value])
    identity=fingerprint([VERSION,q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution'),layouts])
    q[':question/id']=uid(identity)
    for fi,fld in enumerate(fields):
        old=fld.get(':answer-field/correct',[None,None])[1];mapping={}
        fld[':answer-field/id']=uid(identity+'/field/'+str(fi))
        for a in fld[':answer-field/choices']:
            new=uid(identity+'/field/'+str(fi)+'/answer/'+a[':answer/value']);mapping[a[':answer/id']]=new;a[':answer/id']=new
        if old is not None:fld[':answer-field/correct']=[':answer/id',mapping[old]]
        if fld[':answer-field/type']==':answer-field.type/radio':random.Random(seed+fi).shuffle(fld[':answer-field/choices'])
    if extra.get('raw'):
        task=fingerprint([f,p])
    else:
        F,G,E,dx,dy,N,T,C=math_data(f,p)
        # Common positive direction scaling is incidental. Unused coefficients
        # are excluded; the actual function, point, normalized direction define task.
        task=fingerprint([f,S.srepr(F),None if f=='supplied_gradient' else p['x0'],None if f=='supplied_gradient' else p['y0'],S.srepr(S.simplify(dx/N)),S.srepr(S.simplify(dy/N))])
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'seed':seed,'template':f,'profile':profile,'parameters':p,'content_fingerprint':identity,'mathematical_fingerprint':task,'eligible_for_learning':eligible,'evidence_only':not eligible,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},**extra}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty: '+level)
    r=random.Random(seed)
    if profile and profile.startswith('raw_'):
        f=profile[4:]
        if f not in FAMILIES or (template and template!=f):raise ValueError('raw template/profile mismatch')
        return raw_replay(f,level,seed,parameters if parameters is not None else {'scale':r.randint(1,6)})
    f=template or r.choice([f for f,l in FAMILIES.items() if l==level])
    if f not in FAMILIES or FAMILIES[f]!=level:raise ValueError('family level mismatch')
    kind=field_type or ('blank' if f=='supplied_gradient' else 'radio')
    if kind not in ('radio','blank') or (f=='supplied_gradient' and kind!='blank'):raise ValueError('field type')
    chosen=profile or ('zero_method' if f=='quadratic' and r.randrange(3)==0 else 'method')
    if chosen not in ('method','zero_method'):raise ValueError('bank profile')
    for attempt in range(3000):
        p=dict(parameters) if parameters is not None else sample(f,r)
        try:
            guard(f,level,p);data=math_data(f,p);values=[S.simplify(v) for v in bank(data,chosen)]
            if chosen=='zero_method' and data[-1]!=0:raise ValueError('zero bank requires zero dot product')
            if chosen=='method' and data[-1]==0:raise ValueError('nonzero method bank')
            if kind=='radio' and any(S.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]):raise ValueError('whole bank collision')
        except ValueError:
            if parameters is not None:raise
            continue
        F,G,E,dx,dy,N,T,C=data;point='('+str(p['x0'])+','+str(p['y0'])+')'
        if f=='supplied_gradient':problem='The gradient of $f(x,y)$ at the point $'+point+'$ is $∇f'+point+'='+vec(*E)+'$. Find the directional derivative in the direction of $v='+ib(dx,dy)+'.$'
        else:
            problem='Find the directional derivative of the function $f(x,y)='+expr_tex(F)+'$ at the point $'+('A' if f in ('exp','chain_square') else '')+point+'$ '
            if f in ('exp','chain_square'):problem+='in the direction towards the point $B('+tex(p['x0']+dx)+','+tex(p['y0']+dy)+').$'
            else:problem+='in the direction of the vector $v='+ib(dx,dy)+'.$'
        key='field-1' if kind=='blank' else 'selection'
        if kind=='blank':problem+='\n\nThe required directional derivative is ${f}_{u}^{′}'+point+'=$\n\n{{field-1}}\n\n.'
        vals=[C] if kind=='blank' else values
        answers=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':tex(v)} for i,v in enumerate(vals)]
        fld={':answer-field/id':'field',':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id','0']}
        q={':question/problem':problem,':question/worked-solution':normal_solution(f,p,data),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[fld]}
        return finish(q,f,level,seed,p,chosen,True,{'source_id':SOURCE_IDS[f],'origin':'authored completion' if f=='supplied_gradient' else ('authored level assignment' if f in ('linear_y2','chain_square') else 'observed family, authored method bank'),'recipe_operations':(['omit_y','reverse_y','omit_normalization','squared_norm'] if chosen=='method' else ['omit_y','omit_x','subtract_products','multiply_difference_by_norm'])})
    raise RuntimeError('no complete bank sampled')

# Easy includes observed direct vectors and an authored supplied-gradient completion.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate preserves exponential+polynomial partials at y=0 and A-to-B direction.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Current evidence has comparable nested squares at moderate; no validated hard template.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(rec):
    q=rec['question'];out=q[':question/problem']+'\n\n'
    for fld in q.get(':question/answer-fields',[]):
        out+='\n'.join('- $'+a[':answer/value']+'$' for a in fld[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[Source omits worked solution.]')

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186124458-source-policy.json'))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (list(SUPPORTED_LEVELS) if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
