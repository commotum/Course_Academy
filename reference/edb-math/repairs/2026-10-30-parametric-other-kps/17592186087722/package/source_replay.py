#!/usr/bin/env python3
"""Original-parameter replay helpers retained from the supplied scratch generator.

Only the current capture's 20 complete source records are bundled. This module
provides TeX/set readers and original source layouts; normal sampling and its
analytic derivations live in generator.py. No imported records are mutated.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy.calculus.util import function_range, continuous_domain
KP_ID=17592186087722
KP_UUID='3cbf0ad0-a7c5-5c0f-a06c-9210fdc244ef'
TITLE='Determining the Range of a Parametric Equation'
VERSION='coordinate-ranges-1'
ROOT=Path(__file__).parent
SOURCE=json.loads((ROOT/'source.json').read_text())
T=sp.Symbol('t',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
class SampleRejected(ValueError): pass

def latex_expr(text):
    """Read the displayed TeX arithmetic, independently of generation metadata."""
    text=text.strip().rstrip('.')
    def group(s,i):
        if s[i]!='{':raise ValueError('Expected TeX group: '+s[i:])
        n=1;j=i+1
        while n:
            n+=(s[j]=='{')-(s[j]=='}');j+=1
        return s[i+1:j-1],j
    def rewrite(s):
        out='';i=0
        while i<len(s):
            if s.startswith('\\frac',i):
                a,j=group(s,i+5);b,k=group(s,j);out+='(('+rewrite(a)+')/('+rewrite(b)+'))';i=k
            elif s.startswith('\\sqrt',i):
                a,j=group(s,i+5);out+='sqrt('+rewrite(a)+')';i=j
            else:out+=s[i];i+=1
        return out
    text=rewrite(text)
    for a,b in [('\\left',''),('\\right',''),('\\,',''),('\\quad',''),('\\!',''),('\\infty','oo'),('∞','oo'),('{','('),('}',')'),('^','**')]:text=text.replace(a,b)
    return parse_expr(text,local_dict={'t':T,'sqrt':sp.sqrt,'oo':sp.oo},transformations=TRANS)

def parse_prompt(prompt):
    blocks=re.findall(r'\$\$(.*?)\$\$|\$([^$]+)\$',prompt,re.S)
    text=next(a or b for a,b in blocks if re.search(r'x\s*=',a or b) and re.search(r'y\s*=',a or b))
    clean=text.replace('\\,','').replace('\\quad','').strip().rstrip('.,')
    m=re.match(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),\s*(t.*)',clean,re.S)
    if not m:raise ValueError('Cannot read printed parametrization: '+text)
    xt,yt,dt=m.groups();dt=dt.replace(' ','').replace('\\leq','\\le').replace('\\geq','\\ge')
    if '\\in' in dt or '∈' in dt:
        interval=re.split(r'\\in|∈',dt,maxsplit=1)[1].replace('\\left','').replace('\\right','')
        if not (interval[0] in '[(' and interval[-1] in '])'):raise ValueError('Unreadable displayed interval '+interval)
        ends=interval[1:-1].split(',')
        if len(ends)!=2:raise ValueError('Unreadable interval endpoints')
        domain=sp.Interval(latex_expr(ends[0]),latex_expr(ends[1]),left_open=interval[0]=='(',right_open=interval[-1]==')')
    else:
        dm=re.match(r't(\\ge|\\le|>|<)(.+)',dt)
        if not dm:raise ValueError('Cannot read printed domain: '+dt)
        op,v=dm.groups();v=latex_expr(v)
        domain=sp.Interval(v,sp.oo,left_open=op=='>') if op in ('\\ge','>') else sp.Interval(-sp.oo,v,right_open=op=='<')
    x,y=latex_expr(xt),latex_expr(yt)
    # Both coordinates constrain admissibility, even if only one is assessed.
    admissible=domain.intersect(continuous_domain(x,T,sp.S.Reals)).intersect(continuous_domain(y,T,sp.S.Reals))
    return x,y,admissible,(xt,yt,dt)

def images(prompt,assessed):
    x,y,d,_=parse_prompt(prompt)
    return {v:function_range({'x':x,'y':y}[v],T,d) for v in assessed}

def scalar(s):return sp.latex(sp.sympify(s))
def set_tex(v,s):
    if s==sp.S.Reals:return v+r'\in\mathbb{R}'
    if isinstance(s,sp.FiniteSet):return v+'='+scalar(next(iter(s)))
    if not isinstance(s,sp.Interval):raise ValueError('Unsupported output set '+str(s))
    if s.end==sp.oo:return v+('>' if s.left_open else r'\ge ')+scalar(s.start)
    if s.start==-sp.oo:return v+('<' if s.right_open else r'\le ')+scalar(s.end)
    return scalar(s.start)+('<' if s.left_open else r'\le ')+v+('<' if s.right_open else r'\le ')+scalar(s.end)
def paired_tex(sets):return r',\,'.join(set_tex(v,s) for v,s in sets.items())

def parse_sets(tex):
    """Full Cartesian product of coordinate constraints, including finite intervals."""
    tex=tex.replace('\\quad','').replace('\\,','').replace(' ','').replace('\\geq','\\ge').replace('\\leq','\\le')
    result={}
    for part in tex.split(','):
        if '\\in\\mathbb{R}' in part:result[part[0]]=sp.S.Reals;continue
        m=re.match(r'([xy])(\\ge|\\le|>|<|=)(.+)$',part)
        if m:
            v,op,b=m.groups();b=latex_expr(b)
            result[v]=sp.FiniteSet(b) if op=='=' else sp.Interval(b,sp.oo,left_open=op=='>') if op in ('\\ge','>') else sp.Interval(-sp.oo,b,right_open=op=='<');continue
        m=re.match(r'(.+?)(\\le|<)([xy])(\\le|<)(.+)$',part)
        if not m:raise ValueError('Unreadable complete constraint '+part)
        a,lo,v,hi,b=m.groups();result[v]=sp.Interval(latex_expr(a),latex_expr(b),left_open=lo=='<',right_open=hi=='<')
    return result

def dilate(s,k):
    if s==sp.S.Reals:return s
    if isinstance(s,sp.Interval):return sp.Interval(s.start*k,s.end*k,left_open=s.left_open,right_open=s.right_open)
    return sp.FiniteSet(*[a*k for a in s])
def endpoint(s):
    return (s.start,'lower',not s.left_open) if s.end==sp.oo else (s.end,'upper',not s.right_open)
def authored_bank(correct):
    """A complete five-member bank, selected as a unit before validation.

    Pair banks include one wrong coordinate at a time, so both constraints matter.
    """
    def reverse(s):
        b,side,closed=endpoint(s)
        return sp.Interval(-sp.oo,b,right_open=not closed) if side=='lower' else sp.Interval(b,sp.oo,left_open=not closed)
    def toggle(s):
        b,side,closed=endpoint(s)
        return sp.Interval(s.start,s.end,left_open=not s.left_open if side=='lower' else s.left_open,right_open=not s.right_open if side=='upper' else s.right_open)
    keys=list(correct);v=keys[0]
    if len(keys)==2:
        w=keys[1]
        return [dict(correct),{**correct,v:reverse(correct[v])},{**correct,w:reverse(correct[w])},{a:toggle(s) for a,s in correct.items()},{a:sp.FiniteSet(endpoint(s)[0]) for a,s in correct.items()}]
    s=correct[v];b,_,_=endpoint(s)
    return [dict(correct),{v:reverse(s)},{v:toggle(s)},{v:sp.FiniteSet(b)},{v:sp.S.Reals}]

# Source templates: fixed prose/layout and complete mathematical-component slots.
TEMPLATES={}
for q in SOURCE['record'][':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];problem=q[':question/problem'];x,y,d,parts=parse_prompt(problem)
    rawx=re.search(r'x\s*=\s*(.*?)\s*,(?:\s|\\,|\\quad)*y',problem,re.S)[1]
    rawy=re.search(r'y\s*=\s*(.*?)\s*,(?:\s|\\,|\\quad)*t(?:\s|\\|∈|>|<)',problem,re.S)[1]
    asked=re.search(r'(?:range of|ranges of) \$([xy])',problem)
    assessed=['x','y'] if 'ranges of' in problem else [asked.group(1)]
    fields=q.get(':question/answer-fields',[])
    kind=fields[0][':answer-field/type'][':db/ident'].split('/')[-1] if fields else 'radio'
    TEMPLATES[sid]={'level':'moderate','source_id':sid,'problem':problem,'solution':q.get(':question/worked-solution'),'x_tex':rawx,'y_tex':rawy,'assessed':assessed,'kind':kind,'fields':fields,'rated':':question/difficulty' in q}
TEMPLATES['affine_endpoint']={'level':'easy','kind':'radio','assessed':['x'],'source_id':None}
TEMPLATES['two_quadratic_endpoints']={'level':'hard','kind':'radio','assessed':['x','y'],'source_id':None}

def scaled_solution(text,p,answer):
    if text is None:return None
    def relation(s):
        # A complete coordinate equation/inequality chain is one template slot.
        # Labels and auxiliary square/root/domain facts have no coordinate slot.
        vars=re.findall(r'(?<![A-Za-z\\])([xy])(?![A-Za-z])',s)
        if not vars:return s
        if len(set(vars))>1:
            try:return paired_tex({v:dilate(st,p['s'+v]) for v,st in parse_sets(s).items()})
            except ValueError:raise ValueError('Unmapped mixed coordinate component '+s)
        v=vars[0];k=p['s'+v]
        if k==1:return s
        bits=re.split(r'(\\geq(?![A-Za-z])|\\leq(?![A-Za-z])|\\ge(?![A-Za-z])|\\le(?![A-Za-z])|>|<|=)',s)
        if len(bits)<3:return s
        result=[]
        for i,bit in enumerate(bits):
            if i%2:result.append(bit);continue
            if bit.strip()==v:result.append(v);continue
            punctuation=re.search(r'[.,]$',bit.strip());punct=punctuation[0] if punctuation else ''
            arithmetic=bit.strip().rstrip('.,')
            result.append((sp.latex(sp.expand_mul(k*latex_expr(arithmetic))) if i==len(bits)-1 else str(k)+r'\left('+arithmetic+r'\right)')+punct)
        return ''.join(result)
    def mathslot(m):
        whole=m.group(0);delim='$$' if whole.startswith('$$') else '$';body=whole[len(delim):-len(delim)]
        if r'\begin{aligned}' in body:
            a,b=body.split(r'\begin{aligned}',1);aligned,c=b.split(r'\end{aligned}',1)
            rows=aligned.split('\\\\');v=None;transport=[]
            for index,row in enumerate(rows):
                lhs,rhs=row.split('=',1)
                if lhs.replace('&','').strip():v=lhs.replace('&','').strip()
                k=p['s'+v]
                transport.append(row if k==1 else lhs+'='+(sp.latex(sp.expand_mul(k*latex_expr(rhs))) if index==len(rows)-1 else str(k)+r'\left('+rhs.strip()+r'\right)'))
            return delim+a+r'\begin{aligned}'+'\\\\'.join(transport)+r'\end{aligned}'+c+delim
        return delim+relation(body)+delim
    return re.sub(r'\$\$.*?\$\$|\$[^$]*?\$',mathslot,text,flags=re.S)

def source_build(spec,p):
    problem=spec['problem']
    # Exact masks around whole coordinate expressions; never replace short numbers.
    for v in ('x','y'):
        old=spec[v+'_tex'];k=p['s'+v];new=old if k==1 else str(k)+r'\left('+old+r'\right)'
        pattern=re.compile(r'('+v+r'\s*=\s*)'+re.escape(old))
        problem,n=pattern.subn(lambda m:m.group(1)+new,problem,count=1)
        if n!=1:raise ValueError('Coordinate component mask failed')
    correct=images(problem,spec['assessed'])
    solution=scaled_solution(spec['solution'],p,correct)
    if solution is None:
        solution="Let's consider each variable in turn.\n\n"+ '\n\n'.join('The range of $'+v+'$ on the given parameter domain is $'+set_tex(v,s)+'.$' for v,s in correct.items())
        if spec['source_id']=='q-16203':solution="Let's consider each variable in turn.\n\nFor $t\\ge0$, both $"+sp.latex(parse_prompt(problem)[0])+"$ and $"+sp.latex(parse_prompt(problem)[1])+"$ are nonnegative and attain $0$ at $t=0$. They are continuous, increase on the parameter domain, and are unbounded above. Therefore, $"+paired_tex(correct)+'.$'
        if spec['source_id']=='q-16205':solution='Completing the square gives $x='+sp.latex(p['sx']*(T-2)**2-4*p['sx'])+r'$. The square is nonnegative and is zero at the admissible value $t=2$. Therefore, $'+paired_tex(correct)+'.$'
    return problem,solution,correct
