#!/usr/bin/env python3
"""Scalar-function times vector differentiation, local review only (math basis 1356).

Observed templates retain every source vector, stage and sentence. Independent
coordinate factors parameterize whole components, never token replacements.
Original banks are explicit evidence profiles: recovered operations are used when
symbolic equality identifies them; residual expression patterns are labeled
underdetermined and do not enter normal sampling. Default banks use four complete
product-rule errors. Authored easy/moderate/hard each have fixed workloads; see
classification.md for bounds and missing-hard curriculum justification. No EDB.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186115391
KP_UUID='b19f5f01-948e-5f44-8016-63073ed31dbc'
TITLE='Using the Scalar Function Multiple Rule for Differentiation'
VERSION='scalar-vector-1'
BASE=Path(__file__).with_suffix('')
SOURCE=json.loads((BASE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
T=sp.Symbol('t',positive=True)
VEC_RE=re.compile(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]|⟨.*?⟩',re.S)
D=r'\frac{\text{d}}{\text{d}t}'
TRANS=standard_transformations+(implicit_multiplication_application,)

def group(s,i):
    assert s[i]=='{'
    depth=1;j=i+1
    while depth:
        if s[j]=='{':depth+=1
        if s[j]=='}':depth-=1
        j+=1
    return s[i+1:j-1],j

@lru_cache(maxsize=4096)
def parse(text):
    """Read the complete small elementary-expression grammar actually displayed."""
    text=text.strip().rstrip('.,').replace('−','-').replace('⁡',' ')
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
    text=re.sub(r'\\operatorname\{(\w+)\}',r' \1 ',text)
    text=re.sub(r'\{(sin|cos|tan|sec|csc|cot)\}',r' \1 ',text)
    text=text.replace(r'\ln',' ln ').replace(r'\log',' ln ')
    text=re.sub(r'\\(sin|cos|tan|sec|csc|cot)',r' \1 ',text)
    text=re.sub(r'\b(sin|cos|tan|sec|csc|cot)\^\{(\d+)\}\{\((.*?)\)\}',lambda m:'('+m[1]+'('+m[3]+'))**('+m[2]+')',text)
    def fn(m):
        name,power,arg=m.group(1),m.group(2),m.group(3)
        return '('+name+'('+arg+'))'+('**('+power+')' if power else '')
    text=re.sub(r'\b(sin|cos|tan|sec|csc|cot|ln)(?:\^\{(\d+)\})?\s*(-?\d*t|-?\d+|t)\b',fn,text)
    def conv(s):
        out='';i=0
        while i<len(s):
            if s.startswith(r'\frac',i):
                a,j=group(s,i+5);b,i=group(s,j);out+='(('+conv(a)+')/('+conv(b)+'))'
            elif s.startswith(r'\sqrt',i):
                a,i=group(s,i+5);out+=' sqrt('+conv(a)+')'
            elif s[i]=='{':
                a,i=group(s,i);out+='('+conv(a)+')'
            else:out+=s[i];i+=1
        return out
    text=conv(text).replace('^','**')
    try:x=parse_expr(text,local_dict={'t':T,'e':sp.E,'ln':sp.log,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sec':sp.sec,'csc':sp.csc,'cot':sp.cot},transformations=TRANS)
    except Exception as exc:raise ValueError('Cannot parse '+repr(text)) from exc
    if x.free_symbols-{T}:raise ValueError('Unexpected symbols in '+text+': '+str(x))
    return x

def cells(vector):
    if vector.startswith('⟨'):return re.split(r'(?<!\\),',vector[1:-1])
    return vector[len(r'[\begin{aligned}'):-len(r'\end{aligned}]')].split(r'\\')

def vector_read(vector):return [parse(x) for x in cells(vector)]
@lru_cache(maxsize=30000)
def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def vequal(a,b):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
def tex(x):return sp.latex(x).replace(r'\log',r'\ln')
def vector(v,angle=False):return ('⟨'+r',\,'.join(tex(x) for x in v)+'⟩') if angle else r'[\begin{aligned}'+r' \\ '.join(tex(x) for x in v)+r'\end{aligned}]'

def scale_cell(cell,c):
    """A complete component slot, including a derivative's whole argument."""
    if D in cell:
        if c==1:return cell
        before,body=cell.split(D,1)
        body=body.strip();assert body[0]=='(' and body[-1]==')'
        return before+D+'('+scale_cell(body[1:-1],c)+')'
    expr=parse(cell)
    return cell if c==1 else tex(c*expr)

def scale_vector(raw,scales):
    rawcells=cells(raw)
    out=[scale_cell(x,c) for x,c in zip(rawcells,scales)]
    if raw.startswith('⟨'):return '⟨'+','.join(out)+'⟩'
    return r'[\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}]'

def scale_text(raw,scales):return VEC_RE.sub(lambda m:scale_vector(m.group(),scales),raw)

def read_prompt(prompt):
    raw=VEC_RE.search(prompt).group();v=vector_read(raw)
    utext=re.search(r'\$u\(t\)\s*=\s*(.*?)\$',prompt,re.S).group(1)
    return parse(utext),v

def operations(u,v):
    up=sp.diff(u,T);vp=[sp.diff(x,T) for x in v]
    return {
      'correct':[up*x+u*y for x,y in zip(v,vp)],
      'omit_scalar_derivative':[u*y for y in vp],
      'omit_vector_derivative':[up*x for x in v],
      'subtract_second':[up*x-u*y for x,y in zip(v,vp)],
      'subtract_first':[u*y-up*x for x,y in zip(v,vp)],
      'product_of_derivatives':[up*y for y in vp],
      'vector_derivative_only':vp,'unchanged_vector':v,'undifferentiated_product':[u*x for x in v],
      'omit_u_multiplier':[up*x+y for x,y in zip(v,vp)],
      'omit_up_multiplier':[x+u*y for x,y in zip(v,vp)],
    }

def source_recipe(u,v,observed):
    ops=operations(u,v)
    for name,value in ops.items():
        if vequal(value,observed):return {'kind':'operation','operation':name}
    matched=[]
    for i,x in enumerate(observed):
        names=[name for name,value in ops.items() if equal(value[i],x)]
        matched.append(names[0] if names else None)
    return {'kind':'component_operations' if all(matched) else 'partial_expression_pattern','components':matched,'interpretation':'unresolved residual expressions; evidence profile only'}

TEMPLATES={qid:(q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]) for qid,q in QUESTIONS.items()}
TEMPLATES.update({'authored_easy':'easy','authored_moderate':'moderate','authored_hard':'hard'})

def authored(level,p):
    a,b,c,d=p['a'],p['b'],p['c'],p['d']
    if level=='easy':return T**2,[a*T+b,c*sp.exp(T),d*T**3]
    if level=='moderate':return sp.exp(T),[a*T**3+b,c*T**2+1,d*T-2]
    if level=='hard':return T**2+a*T+b,[c*sp.log(T),d*sp.exp(T),1/T]
    raise ValueError(level)

def derivative_vector(v,angle=False):
    cs=[D+'('+tex(x)+')' for x in v]
    return ('⟨'+r',\,'.join(cs)+'⟩') if angle else r'[\begin{aligned}'+r' \\ '.join(cs)+r'\end{aligned}]'

def authored_solution(u,v,angle=False):
    up=sp.diff(u,T);vp=[sp.diff(x,T) for x in v]
    A=[up*x for x in v];B=[u*x for x in vp];C=[sp.simplify(x+y) for x,y in zip(A,B)]
    return ("Using the scalar function multiple rule, we can write\n\n$$\n(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).\n$$\n\nLet's find $u^{′}(t)$ and $f^{′}(t).$\n\n$$\n"
     +r'\begin{aligned}f^{′}(t)&='+derivative_vector(v,angle)+r'='+vector(vp,angle)+r'\\u^{′}(t)&='+D+'('+tex(u)+')='+tex(up)+r'\end{aligned}'
     +"\n$$\n\nTherefore, we obtain:\n\n$$\n"+r'\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=('+tex(up)+')'+vector(v,angle)+'+('+tex(u)+')'+vector(vp,angle)+r'\\&='+vector(A,angle)+'+'+vector(B,angle)+r'\\&='+vector(C,angle)+r'\end{aligned}'+'\n$$')

def validate_parameters(template,p):
    if template in QUESTIONS:
        if set(p)!={'scales'} or len(p['scales'])!=3 or any(type(x)!=int or not 1<=abs(x)<=3 for x in p['scales']):raise ValueError('scales must be three nonzero integers with abs <= 3')
    else:
        if set(p)!={'a','b','c','d'} or any(type(x)!=int or not 1<=abs(x)<=3 for x in p.values()):raise ValueError('a,b,c,d must be nonzero integers with abs <= 3')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    if template is None:template='authored_'+level
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('template difficulty mismatch')
    if profile is None:profile=('observed_'+template if template in QUESTIONS else 'authored_product_errors')
    if profile not in ('authored_product_errors','observed_'+template):raise ValueError('unknown profile')
    if template not in QUESTIONS and profile!='authored_product_errors':raise ValueError('observed profile requires observed template')
    rng=random.Random(seed)
    for attempt in range(100):
        p=parameters if parameters is not None else ({'scales':[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)]} if template in QUESTIONS else {k:rng.choice([-3,-2,-1,1,2,3]) for k in ('a','b','c','d')})
        validate_parameters(template,p)
        if template in QUESTIONS:
            q=QUESTIONS[template];u,original_v=read_prompt(q[':question/problem']);v=[c*x for c,x in zip(p['scales'],original_v)]
            prompt=scale_text(q[':question/problem'],p['scales']);angle='⟨' in prompt
            solution=scale_text(q[':question/worked-solution'],p['scales']) if ':question/worked-solution' in q else authored_solution(u,v,True).replace('f(t)','g(t)').replace('f^{′}','g^{′}')
        else:
            u,v=authored(level,p);angle=False
            prompt='Find $(u(t)f(t))^{′}$ where $f(t)='+vector(v)+'$ and $u(t)='+tex(u)+'.$'
            solution=authored_solution(u,v)
        ops=operations(u,v);correct=ops['correct']  # solve before every wrong operation
        if profile.startswith('observed_'):
            rawchoices=q[':question/answer-fields'][0][':answer-field/choices'];bank=[];recipes=[]
            for choice in rawchoices:
                raw=choice[':answer/value'];orig=vector_read(raw);recipe=source_recipe(u,original_v,orig)
                if recipe['kind']=='operation':value=ops[recipe['operation']]
                elif recipe['kind']=='component_operations':value=[ops[name][i] for i,name in enumerate(recipe['components'])]
                else:value=[ops[name][i] if name else p['scales'][i]*orig[i] for i,name in enumerate(recipe['components'])]
                rendered=scale_vector(raw,p['scales'])
                if not vequal(value,vector_read(rendered)):raise AssertionError('recipe rendering')
                bank.append(rendered);recipes.append(recipe)
        else:
            names=['correct','omit_scalar_derivative','omit_vector_derivative','subtract_second','omit_u_multiplier' if level=='moderate' else 'product_of_derivatives']
            bank=[vector([sp.expand_mul(x) for x in ops[name]],angle) for name in names];recipes=[{'kind':'operation','operation':name} for name in names]
        vals=[vector_read(x) for x in bank]
        matches=[i for i,x in enumerate(vals) if vequal(x,correct)]
        invalid=len(matches)!=1 or any(vequal(vals[i],vals[j]) for i in range(5) for j in range(i))
        if invalid:
            if parameters is not None:raise ValueError('complete bank collision; explicit instance rejected')
            continue
        break
    else:raise ValueError('no eligible complete bank')
    domain='t > 0' if any(x.has(sp.log) or any(z.is_Pow and not z.exp.is_Integer for z in sp.preorder_traversal(x)) or sp.denom(x).has(T) for x in [u]+v) else ('cos(t) != 0' if any(x.has(sp.tan) or x.has(sp.sec) for x in v) else 'real t')
    math_key=json.dumps({'u':sp.srepr(sp.expand(u)),'v':[sp.srepr(sp.expand(x)) for x in v],'domain':domain},sort_keys=True)
    fingerprint=hashlib.sha256(math_key.encode()).hexdigest()
    content=json.dumps({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(bank),'domain':domain},sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),raw)),':answer/type':':answer.type/math',':answer/value':raw} for raw in bank]
    correctid=answers[matches[0]][':answer/id'];rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':domain,'mathematical_fingerprint':fingerprint,'recipes':recipes,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[template] if template in QUESTIONS else [],'difficulty_status':'authored missing-level' if level=='hard' else ('authored assignment of unrated' if template=='q-32501' else ('observed' if template in QUESTIONS else 'authored extension')),'plots':'none','sympy_version':sp.__version__}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
