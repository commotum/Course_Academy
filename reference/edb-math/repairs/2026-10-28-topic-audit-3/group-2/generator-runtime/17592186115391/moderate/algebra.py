"""Elementary TeX reader and vector operations retained from the existing generator."""
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
SOURCE=json.loads((Path(__file__).parent/'source-banks.json').read_text())
QUESTIONS=SOURCE['questions']
T=sp.Symbol('t',positive=True)
VEC_RE=re.compile(r'\[\\begin\{aligned\}.*?\\end\{aligned\}\]|\\begin\{bmatrix\}.*?\\end\{bmatrix\}|⟨.*?⟩',re.S)
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
    if vector.startswith(r'\begin{bmatrix}'):return vector[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')].split(r'\\')
    return vector[len(r'[\begin{aligned}'):-len(r'\end{aligned}]')].split(r'\\')

def vector_read(vector):return [parse(x) for x in cells(vector)]
@lru_cache(maxsize=30000)
def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def vequal(a,b):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
def tex(x):return sp.latex(x).replace(r'\log',r'\ln')
def vector(v,angle=False):return ('⟨'+r',\,'.join(tex(x) for x in v)+'⟩') if angle else r'\begin{bmatrix}'+r' \\ '.join(tex(x) for x in v)+r'\end{bmatrix}'

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
    if raw.startswith(r'\begin{bmatrix}'):return r'\begin{bmatrix}'+r'\\'.join(out)+r'\end{bmatrix}'
    return r'[\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}]'

def scale_text(raw,scales):return VEC_RE.sub(lambda m:scale_vector(m.group(),scales),raw)

def read_prompt(prompt):
    raw=VEC_RE.search(prompt).group();v=vector_read(raw)
    utext=re.search(r'u\(t\)\s*=\s*(.*?)(?=\$|,\\qquad)',prompt,re.S).group(1)
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

