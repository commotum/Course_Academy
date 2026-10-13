#!/usr/bin/env python3
"""Sum/constant differentiation of vector functions. Scratch-only, basis 1356.

Observed profiles retain complete expression patterns, without claiming recovered
distractor intent. Normal questions use the complete authored operation bank.
Each extracted vector slot receives an independent signed component scale; source
replay is the identity specialization of the same recipe, not a payload branch.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

KP_ID=17592186115390
KP_UUID='49b54258-61d2-549c-94e4-a251f6d2a656'
TITLE='Using the Sum and Constant Multiple Rules for Differentiation'
VERSION='1.0.0'
ROOT=Path(__file__).with_suffix('')
T=sp.Symbol('t',real=True)
I,J,K=sp.symbols('i j k')
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def balanced(s,start,opening='{',closing='}'):
    assert s[start]==opening,(s,start)
    depth=1
    for n in range(start+1,len(s)):
        if s[n]==opening: depth+=1
        elif s[n]==closing: depth-=1
        if depth==0:return s[start+1:n],n+1
    raise ValueError('Unbalanced component: '+s)

def scalar(raw):
    """Independent bounded TeX reader for every printed source/generated component."""
    s=raw.strip().replace('\\\\,','').replace(r'\,','').replace('⁡','').replace('\u2061','').replace('−','-')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\operatorname','')
    s=s.replace(r'\pi','pi').replace(r'\ln','log').replace('{ln}','log').replace('{log}','log')
    s=s.replace('{sin}','sin').replace('{cos}','cos').replace('{tan}','tan').replace('{sec}','sec')
    for name in ['sin','cos','tan','sec','exp','log']:
        s=s.replace('\\'+name,name)
    deriv=r'\frac{\text{d}}{\text{d}t}'
    if s.startswith(deriv):
        rest=s[len(deriv):].strip()
        return sp.diff(scalar(rest),T)
    while r'\frac' in s:
        n=s.index(r'\frac'); p=n+5
        num,p=balanced(s,p); den,p=balanced(s,p)
        s=s[:n]+'(('+str(scalar(num))+')/('+str(scalar(den))+'))'+s[p:]
    while r'\sqrt' in s:
        n=s.index(r'\sqrt'); inner,end=balanced(s,n+5)
        s=s[:n]+'sqrt('+str(scalar(inner))+')'+s[end:]
    # Exponential bases, including SymPy's e^{...} and source {e}^{...}.
    s=s.replace('{e}','e')
    s=re.sub(r'e\s*\^\s*\{([^{}]+)\}',lambda m:'exp('+str(scalar(m[1]))+')',s)
    s=re.sub(r'(sin|cos|tan|sec)\s*\^\s*\{?(\d+)\}?\s*\{?(\([^()]*\))\}?',r'\1\3^\2',s)
    s=re.sub(r'(sin|cos|tan|sec)\s*\^\s*\{?(\d+)\}?\s*([a-z0-9]+)',r'\1(\3)^\2',s)
    s=re.sub(r'(sin|cos|tan|sec|log)\s*([+-]?\d*t|[+-]?\d+)',r'\1(\2)',s)
    s=s.replace('{','(').replace('}',')')
    s=re.sub(r'(?<=\d)([ijk])\b',r'*\1',s) # 1j must be a basis coefficient, not Python's imaginary literal.
    return parse_expr(s,local_dict={'t':T,'i':I,'j':J,'k':K,'pi':sp.pi,'e':sp.E,
        'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sec':sp.sec,'log':sp.log,'sqrt':sp.sqrt,'exp':sp.exp},transformations=TRANS)

def split_components(raw):
    if raw.startswith('⟨'):return [x.strip() for x in raw[1:-1].replace('\\\\,','').replace(r'\,','').split(',')]
    if raw.startswith(r'[\begin{aligned}'):
        return [x.strip() for x in raw[len(r'[\begin{aligned}'):-len(r'\end{aligned}]')].split(r'\\')]
    raise ValueError(raw)

def vector(raw):
    if raw.startswith(('⟨',r'[\begin{aligned}')):
        return tuple(scalar(c) for c in split_components(raw))
    # Basis vectors in source answer banks and distributed arithmetic.
    z=sp.expand(scalar(raw))
    if sp.simplify(z-z.coeff(I)*I-z.coeff(J)*J-z.coeff(K)*K)!=0:
        raise ValueError('Not a basis-vector expression: '+raw)
    return (z.coeff(I),z.coeff(J),z.coeff(K))

def tex(x):return sp.latex(sp.simplify(x),fold_short_frac=False)
def vtex(v,layout='tuple'):
    if layout=='column':return r'[\begin{aligned}'+r' \\ '.join(tex(x) for x in v)+r'\end{aligned}]'
    if layout=='basis':
        pieces=[]
        for x,b in zip(v,'ijk'):
            if x==0:continue
            z=tex(x); term='('+z+r')\,'+b if sp.sympify(x).is_Add else z+r'\,'+b
            pieces.append(term)
        return '+'.join(pieces).replace('+-','-') or '0'
    return '⟨'+r',\,'.join(tex(x) for x in v)+'⟩'
def scale(v,s):return tuple(sp.simplify(x*y) for x,y in zip(v,s))
def eq(a,b):return all(sp.simplify(x-y)==0 for x,y in zip(a,b))
def total(vs,coeff):return tuple(sp.simplify(sum(c*v[n] for c,v in zip(coeff,vs))) for n in range(3))
def block(s):return '$$\n'+s+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')

def render_basis_expression(raw,scales):
    """Scale full summands without collapsing the source's distributed rows."""
    chunks=[];start=0;depth=0
    for n,c in enumerate(raw):
        if c in '({':depth+=1
        elif c in ')}':depth-=1
        elif c in '+-' and depth==0 and n>start:
            chunks.append(raw[start:n]);start=n
    chunks.append(raw[start:])
    pieces=[]
    for chunk in chunks:
        chunk=chunk.strip();m=re.match(r'([+-]?\d+)\(',chunk)
        if m:
            body,end=balanced(chunk,m.end()-1,'(',')')
            if end==len(chunk):
                pieces.append(m[1]+r'\left('+render_basis_expression(body,scales)+r'\right)');continue
        pieces.append(r'\left('+vtex(scale(vector(chunk),scales),'basis')+r'\right)')
    return '+'.join(pieces).replace('++','+').replace('+-','-')

# Explicit mathematical bases, independently derived from the source prompts.
BASES={
'q-33122':(['f','g'],[1,1],[[3*T-1,6-T,7*T],[T**2,1-T**2,T]],None,'tuple'),
'q-33143':(['h','g'],[3,-2],[[2*T**2,T-3,8+T**3],[T**2+2*T,8,2*T**3]],2,'tuple'),
'q-128137':(['f','g'],[1,-3],[[2*sp.sqrt(T+1),T**3,sp.log(T+1)],[1/(3*(T+1)),sp.sin(T),sp.tan(T)]],0,'tuple'),
'q-128452':(['f','g'],[2,-1],[[8*sp.sqrt(3-T),sp.sin(sp.pi*T),sp.log(-2*T)],[T**2-T,sp.pi*T**2,1-T**2]],-1,'tuple'),
'q-128458':(['f','g'],[2,5],[[2*sp.sqrt(3+T),sp.cos(T-1),sp.Integer(1)],[2*T-3,T**2,(T+1)**2]],1,'column'),
'q-32499':(['g','h'],[2,-1],[[sp.cos(T),3*T-3,-T**2],[sp.sin(T),-T,sp.Integer(4)]],None,'tuple'),
'q-32503':(['f','g','h'],[1,1,1],[[-1,0,1],[-T,0,T],[-T**2,0,T**2]],None,'tuple'),
'q-33123':(['f','g'],[2,3],[[2*sp.sin(T),3*sp.cos(T),-3*sp.cos(T)],[5-sp.sin(T),-1,2*sp.cos(T)]],None,'basis'),
'q-70681':(['f','g'],[1,4],[[sp.sqrt(T),sp.log(T),2],[T,1/T,T**4]],None,'tuple'),
'q-127998':(['f','g'],[1,1],[[1-2*T,T**2,(T-1)**2],[T+1,1-2*T,T**3]],None,'tuple'),
'q-128144':(['f','g'],[1,-2],[[T**2,sp.log(T),sp.exp(T-1)],[2*sp.sqrt(T),T**3,3]],1,'tuple'),
}

DATA=json.loads((ROOT/'templates.json').read_text())
TEMPLATES={q: d['level'] for q,d in DATA.items()}
TEMPLATES['canonical-mixed']='hard'
BANK_PROFILES={q:'observed-expression-pattern' for q in DATA}
BANK_PROFILES['authored-operations']='authored'

def render_slots(mask,slots,scales,base):
    names,coeff,funcs,point,layout=base
    def render(slot):
        raw=slot['raw']; kind=slot['kind']
        if all(s==1 for s in scales):return raw
        if kind=='basis-derivative':
            f=funcs[slot['function_index']]
            return '+'.join(r'\frac{\text{d}}{\text{d}t}('+tex(sp.sympify(x)*s)+r')\,'+b for x,s,b in zip(f,scales,'ijk')).replace('+-','-')
        if kind=='basis':return render_basis_expression(raw,scales)
        vals=split_components(raw)
        rendered=[]
        for x,s in zip(vals,scales):
            deriv=r'\frac{\text{d}}{\text{d}t}'
            if x.startswith(deriv):rendered.append(deriv+'('+tex(s*scalar(x[len(deriv):]))+')')
            else:rendered.append(tex(s*scalar(x)))
        return (r'[\begin{aligned}'+r' \\ '.join(rendered)+r'\end{aligned}]') if kind=='column' else '⟨'+r',\,'.join(rendered)+'⟩'
    return re.sub(r'@@(\d+)@@',lambda m:render(slots[int(m[1])]),mask)

def combination(names,coeff,point='t',prime=False):
    out=''
    for name,c in zip(names,coeff):
        sign='-' if c<0 else '+' if out else ''
        out+=sign+('' if abs(c)==1 else tex(abs(c)))+name+(r"'(\!"+str(point)+')' if prime else '('+str(point)+')')
    return out

def solution_generic(names,coeff,funcs,point,layout):
    derivs=[tuple(sp.diff(x,T) for x in f) for f in funcs]
    target=combination(names,coeff)
    sol='Using the constant multiple rule and the sum rule, we have\n\n'+block('('+target+r")'="+combination(names,coeff,prime=True)+'.')
    sol+="\n\nLet's find the derivatives of each function:\n\n"
    rows=[]
    for name,f,d in zip(names,funcs,derivs):
        formal=[r'\frac{\text{d}}{\text{d}t}('+tex(x)+')' for x in f]
        vv=(r'[\begin{aligned}'+r' \\ '.join(formal)+r'\end{aligned}]') if layout=='column' else '⟨'+r',\,'.join(formal)+'⟩'
        rows += [name+r"'(t)&="+vv,r'&='+vtex(d,layout)]
    sol+=aligned(rows)
    used=derivs if point is None else [tuple(sp.simplify(x.subs(T,point)) for x in d) for d in derivs]
    target_at=target
    evaluation=(r'\big|_{t='+str(point)+'}') if point is not None else ''
    terms=lambda vs: '+'.join(('' if c==1 else tex(c))+r'\left('+vtex(v,layout)+r'\right)' for c,v in zip(coeff,vs)).replace('+-','-')
    final=total(used,coeff)
    sol+='\n\nTherefore, we obtain:\n\n'+aligned(['('+target_at+r")'"+evaluation+r'&='+combination(names,coeff,point if point is not None else 't',True),r'&='+terms(used),r'&='+'+'.join(r'\left('+vtex(scale(v,[c]*3),layout)+r'\right)' for c,v in zip(coeff,used)),r'&='+vtex(final,layout)+'.'])
    return sol

def observed(name,p):
    d=DATA[name]; base=BASES[name]; scales=p['scales']
    names,coeff,funcs,point,layout=base
    funcs=[scale(tuple(map(sp.sympify,f)),scales) for f in funcs]
    prompt=render_slots(d['prompt'],d['slots'],scales,base)
    solution=render_slots(d['solution'],d['slots'],scales,base) if d['solution'] else solution_generic(names,coeff,funcs,point,layout)
    return names,coeff,funcs,point,layout,prompt,solution

# EASY — six observed symbolic layouts; independent component scales preserve workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — four mixed-component evaluations plus authored-level unrated polynomial.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored equal-workload instances of canonical mixed symbolic derivatives.
def hard(p):
    a,b,A,B,n,h,u,v=p['a'],p['b'],p['A'],p['B'],p['n'],p['h'],p['u'],p['v']
    names=['f','g'];coeff=[A,B]
    funcs=[(a*T**n+b,-a/(T-h),sp.cos(u*T)),(b*T-a,sp.exp(v*T),sp.cos(u*T))]
    layout='basis'
    target=combination(names,coeff)
    prompt='Find the derivative of $'+target+'$ with respect to $t$, where\n\n'+aligned([name+'(t)&='+vtex(f,layout) for name,f in zip(names,funcs)])
    return names,coeff,funcs,None,layout,prompt,solution_generic(names,coeff,funcs,None,layout)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout is supported')
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if profile and profile!='authored-operations':
        if profile not in DATA:raise ValueError('Unknown bank profile')
        if template and template!=profile:raise ValueError('Profile/template mismatch')
        template=profile
    rng=random.Random(seed)
    eligible=[k for k,v in TEMPLATES.items() if v==level]
    name=template or rng.choice(eligible)
    if name not in eligible:raise ValueError('Template/level mismatch')
    profile=profile or 'authored-operations'
    scale_bound=6 if name=='q-32503' and profile=='authored-operations' else 3
    scale_choices=[x for x in range(-scale_bound,scale_bound+1) if x]
    for attempt in range(128):
        p=dict(parameters) if parameters is not None else ({'scales':[rng.choice(scale_choices),1 if name=='q-32503' and profile=='authored-operations' else rng.choice(scale_choices),rng.choice(scale_choices)]} if name in DATA else {'a':rng.randint(1,4),'b':rng.randint(1,4),'A':rng.choice([-3,-2,2,3]),'B':rng.choice([-3,-2,2,3]),'n':rng.choice([2,3]),'h':rng.choice([-3,-2,-1,1,2,3]),'u':rng.randint(2,4),'v':rng.randint(2,4)})
        if name in DATA:
            if set(p)!={'scales'} or len(p['scales'])!=3 or any(type(x)!=int or x not in scale_choices for x in p['scales']) or name=='q-32503' and profile=='authored-operations' and p['scales'][1]!=1:raise ValueError('Expected three bounded nonzero component scales (±1..3; triple-sum default x,z ±1..6 and y=1)')
            built=observed(name,p)
        else:
            bounds={'a':range(1,5),'b':range(1,5),'A':[-3,-2,2,3],'B':[-3,-2,2,3],'n':[2,3],'h':[-3,-2,-1,1,2,3],'u':range(2,5),'v':range(2,5)}
            if set(p)!=set(bounds) or any(type(p[k])!=int or p[k] not in bounds[k] for k in bounds):raise ValueError('Invalid hard parameters')
            built=hard(p)
        names,coeff,funcs,point,layout,prompt,sol=built
        derivs=[tuple(sp.diff(x,T) for x in f) for f in funcs]
        used=derivs if point is None else [tuple(sp.simplify(x.subs(T,point)) for x in d) for d in derivs]
        correct=total(used,coeff)
        if profile=='authored-operations':
            # Complete bank chosen before rendering: four assessed-method mistakes.
            omit_index=1 if name=='q-32503' else 0
            vals=[correct,total([v for i,v in enumerate(used) if i!=omit_index],[c for i,c in enumerate(coeff) if i!=omit_index]),total(used[:-1],coeff[:-1]),total(used,[-c if i==omit_index else c for i,c in enumerate(coeff)]),total(funcs if point is None else [tuple(x.subs(T,point) for x in f) for f in funcs],coeff)]
            recipes=['correct','omit_middle_derivative' if name=='q-32503' else 'omit_first_derivative','omit_last_derivative','reverse_middle_multiplier' if name=='q-32503' else 'reverse_first_multiplier','combine_without_differentiating']
            bank=[vtex(v,layout) for v in vals]
        else:
            vals=[scale(vector(x),p['scales']) for x in DATA[name]['bank']]
            bank=[render_slots('@@0@@',[{'raw':x,'kind':layout}],p['scales'],BASES[name]) for x in DATA[name]['bank']]
            recipes=['observed_expression_pattern_'+str(i+1) for i in range(5)]
        matches=[n for n,v in enumerate(vals) if eq(v,correct)]
        if len(matches)!=1 or any(eq(x,y) for n,x in enumerate(vals) for y in vals[n+1:]):
            if parameters is not None:raise ValueError('Complete bank has collision')
            continue
        domain='t>0' if name in ['q-70681','q-128144'] else '-1<t<pi/2' if name=='q-128137' else 't<0' if name=='q-128452' else 't>-3' if name=='q-128458' else 't!='+str(p['h']) if name=='canonical-mixed' else 'all real t'
        paramfp=hashlib.sha256(json.dumps({'functions':[[sp.srepr(x) for x in f] for f in funcs],'coefficients':coeff,'point':point,'domain':domain},sort_keys=True).encode()).hexdigest()
        content={'version':VERSION,'template':name,'profile':profile,'parameters':p,'domain':domain,'prompt':prompt,'solution':sol,'bank':sorted(bank)}
        contentfp=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
        qid=uuid.uuid5(uuid.NAMESPACE_URL,contentfp);fid=uuid.uuid5(qid,'selection')
        ans=[{':answer/id':str(uuid.uuid5(fid,x)),':answer/type':':answer.type/math',':answer/value':x} for x in bank]
        cid=ans[matches[0]][':answer/id'];rng.shuffle(ans)
        return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':ans,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile],'authored_extension':name=='canonical-mixed' or name=='q-33143' or profile=='authored-operations','source_analysis':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question_ids':[name] if name in DATA else ['e-2477']},'source_repairs':DATA[name].get('repairs',[]) if name in DATA else [],'parameter_fingerprint':paramfp,'content_fingerprint':contentfp,'domain':domain,'plot_rating':'none','plot_assets':{},'distractor_recipes':recipes,'sympy_version':sp.__version__}}
    raise ValueError('No eligible complete bank after bounded rejection')

def markdown(r):
    q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
    rows=['## '+g['template']+' — '+q[':question/difficulty'].split('/')[-1],f"Profile: `{g['bank_profile']}`; parameters: `{json.dumps(g['parameters'])}`.",'',q[':question/problem'],'']
    for a in f[':answer-field/choices']:rows.append('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
    return '\n'.join(rows)+ '\n\n'+q[':question/worked-solution']
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=list(BANK_PROFILES));a=p.parse_args()
    if a.count<1 or a.difficulty=='all' and (a.template or a.profile):p.error('Use positive count and specific difficulty with template/profile')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+n,a.template,profile=a.profile) for l in levels for n in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(x) for x in records))
if __name__=='__main__':main()
