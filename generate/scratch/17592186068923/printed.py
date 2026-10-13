"""Restricted independent reader for this package's printed rational/log math."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x',real=True);C=sp.Symbol('C');A=sp.Symbol('A');B=sp.Symbol('B')
def clean(t):
    return t.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
def group(t,i):
    assert t[i] in '{(',t[i:]
    op=t[i];close='}' if op=='{' else ')';depth=1;j=i+1
    while depth:
        if t[j]==op:depth+=1
        if t[j]==close:depth-=1
        j+=1
    return t[i+1:j-1],j
def scalar(t):
    t=clean(t).strip().rstrip('.,')
    t=t.replace(r'\operatorname{ln}',r'\ln').replace(r'\log',r'\ln').replace(r'\cdot','*')
    while re.search(r'\\(?:d?frac)',t):
        m=re.search(r'\\(?:d?frac)',t);i=m.end()
        while t[i].isspace():i+=1
        a,j=group(t,i)
        while t[j].isspace():j+=1
        b,j=group(t,j);t=t[:m.start()]+'(('+str(scalar(a))+')/('+str(scalar(b))+'))'+t[j:]
    while r'\sqrt' in t:
        i=t.index(r'\sqrt');a,j=group(t,i+5)
        t=t[:i]+' ('+str(sp.sqrt(scalar(a)))+') '+t[j:]
    position=0
    while True:
        match=re.search(r'\\ln',t[position:])
        if match is None:break
        start=position+match.start();end=position+match.end()
        while end<len(t) and t[end].isspace():end+=1
        if t[end] in '{(':arg,stop=group(t,end)
        elif t[end]=='|':stop=t.index('|',end+1)+1;arg='Abs('+str(scalar(t[end+1:stop-1]))+')'
        else:
            m=re.match(r'\d+',t[end:]);assert m,t[end:];arg=m[0];stop=end+len(arg)
        replacement=' ('+str(sp.log(scalar(arg)))+') ';t=t[:start]+replacement+t[stop:];position=start+len(replacement)
    while '|' in t:
        i=t.index('|');j=t.index('|',i+1);t=t[:i]+' Abs('+str(scalar(t[i+1:j]))+') '+t[j+1:]
    t=t.replace('{','(').replace('}',')').replace('^','**');assert '\\' not in t,t
    return sp.simplify(parse_expr(t,local_dict={'x':x,'C':C,'A':A,'B':B,'Abs':sp.Abs,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))
def integral(prompt):
    t=clean(prompt).replace(r'{\int }',r'\int').replace(r'\displaystyle','').replace(r'\text{d}x','dx').replace(r'\textrm{d}x','dx')
    start=t.index(r'\int')+4
    while t[start].isspace():start+=1
    assert t[start]=='_';start+=1
    if t[start]=='{':a,start=group(t,start)
    else:a=t[start];start+=1
    assert t[start]=='^';start+=1
    if t[start]=='{':b,start=group(t,start)
    else:b=t[start];start+=1
    stop=t.index('dx',start)
    return scalar(t[start:stop]),scalar(a),scalar(b)
def equivalent(a,b):return sp.simplify(sp.expand_log(a-b,force=True))==0
