"""Restricted printed LaTeX reader; no generation metadata is consulted."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x',real=True);u=sp.Symbol('u',real=True);C=sp.Symbol('C')
def group(t,i):
    assert t[i] in '{(',t[i:]
    close='}' if t[i]=='{' else ')';op=t[i];depth=1;j=i+1
    while depth:
        if t[j]==op:depth+=1
        if t[j]==close:depth-=1
        j+=1
    return t[i+1:j-1],j

def scalar(t):
    t=t.strip().replace('y','x').replace('π','pi').replace('K','C').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').rstrip('.,')
    t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln)\}',r'\\\1',t)
    t=re.sub(r'\{(sec|csc)\}\^\{2\}',r'\\\1^2',t)
    t=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}\^\{(\d+)\}',r'\\\1^\2',t)
    t=t.replace(r'\mid','|')
    while r'\ln' in t:
        start=t.index(r'\ln');end=start+3
        while end<len(t) and t[end].isspace():end+=1
        if t[end]=='|':
            stop=t.index('|',end+1);arg=t[end+1:stop];stop+=1
        elif t[end] in '{(':arg,stop=group(t,end)
        elif t[end].isdigit():
            m=re.match(r'\d+',t[end:]);arg=m[0];stop=end+len(arg)
        else:raise ValueError('Log argument: '+t[end:])
        t=t[:start]+' ('+str(sp.log(scalar(arg)))+') '+t[stop:]
    t=t.replace(r'\pi','pi').replace(r'\cdot','*')
    while re.search(r'\\(?:d?frac)',t):
        m=re.search(r'\\(?:d?frac)',t);i=m.end()
        while t[i].isspace():i+=1
        a,j=group(t,i)
        while t[j].isspace():j+=1
        b,j=group(t,j);t=t[:m.start()]+'(('+str(scalar(a))+')/('+str(scalar(b))+'))'+t[j:]
    position=0
    while True:
        match=re.search(r'(?:\\)?(sin|cos|tan|cot|sec|csc|sqrt)(?:\^(?:\{\d+\}|\d+))?',t[position:])
        if match is None:break
        start=position+match.start();end=position+match.end();name=match[1];power=int(re.search(r'\d+',match[0])[0]) if '^' in match[0] else 1
        while end<len(t) and t[end].isspace():end+=1
        if t[end] in '{(':arg,stop=group(t,end)
        elif t[end] in 'xu':arg=t[end];stop=end+1
        elif t[end].isdigit():
            m=re.match(r'(\d+)([xu])?',t[end:]);arg=m[0];stop=end+len(arg)
        else:raise ValueError('Unrecognized trig argument: '+t[end:])
        expr=getattr(sp,name)(scalar(arg))**power
        replacement=' ('+str(expr)+') ';t=t[:start]+replacement+t[stop:];position=start+len(replacement)
    t=t.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in t,t
    return sp.simplify(parse_expr(t,local_dict={'x':x,'u':u,'C':C,'pi':sp.pi,**{f:getattr(sp,f) for f in ('sin','cos','tan','cot','sec','csc','sqrt')}},transformations=standard_transformations+(implicit_multiplication_application,)))
def integral(prompt):
    t=prompt.replace('y','x').replace(r'\text{d}y','dx').replace(r'{\int }',r'\int').replace(r'\displaystyle','').replace(r'\text{d}x','dx').replace(r'\textrm d x','dx')
    t=t.replace(r'\textrm d x','dx').replace(r'\text{d}x','dx')
    start=t.index(r'\int')+4;lo=hi=None
    while t[start].isspace():start+=1
    if t[start:start+1]=='_':
        if t[start+1]=='{':a,start=group(t,start+1)
        else:a=t[start+1];start+=2
        assert t[start]=='^';b,start=group(t,start+1);lo=scalar(a);hi=scalar(b)
    stop=t.index('dx',start)
    return scalar(t[start:stop]),lo,hi
