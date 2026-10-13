"""Independent, deliberately narrow reader for displayed source/generator TeX.
Unsupported syntax fails closed. This is not the learner grader.
"""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
X,Y=s.symbols('x y', real=True)

def group(t, i):
    assert t[i]=='{', (t,i)
    depth=1;j=i+1
    while depth:
        if t[j]=='{':depth+=1
        if t[j]=='}':depth-=1
        j+=1
    return t[i+1:j-1],j

def convert(t):
    t=t.replace('⁡','').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\cdot','*').replace('\\times','*')
    t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|ln)\}',r'\\\1',t)
    t=t.replace('\\log','\\ln')
    out='';i=0
    while i<len(t):
        if t.startswith('\\frac',i) or t.startswith('\\dfrac',i):
            n=6 if t.startswith('\\dfrac',i) else 5
            a,j=group(t,i+n);b,j=group(t,j)
            out+='(('+convert(a)+')/('+convert(b)+'))';i=j
        elif t.startswith('\\sqrt',i):
            a,j=group(t,i+5);out+=('*' if out and (out[-1].isalnum() or out[-1]==')') else '')+'sqrt('+convert(a)+')';i=j
        elif t[i]=='{':
            a,j=group(t,i);out+='('+convert(a)+')';i=j
        elif t[i]=='^':
            if t[i+1]=='{':a,j=group(t,i+1)
            else:a=t[i+1];j=i+2
            out+='**('+convert(a)+')';i=j
        elif t[i]=='\\':
            m=re.match(r'\\(sin|cos|tan|cot|ln)',t[i:])
            if not m:raise ValueError('Unsupported TeX: '+t[i:])
            fn=m[1];fn='log' if fn=='ln' else fn;i+=len(m[0]);fpow=None
            if i<len(t) and t[i]=='^':
                if t[i+1]=='{':fpow,i=group(t,i+1)
                else:fpow=t[i+1];i+=2
            while i<len(t) and t[i]==' ':i+=1
            if t[i]=='(':
                depth=1;j=i+1
                while depth:
                    if t[j]=='(':depth+=1
                    if t[j]==')':depth-=1
                    j+=1
                arg=t[i+1:j-1]
            elif t[i]=='{':arg,j=group(t,i)
            elif t.startswith('\\sqrt',i):
                a,j=group(t,i+5);arg='\\sqrt{'+a+'}'
            else:
                m2=re.match(r'(?:[+-]?\d+)?x',t[i:])
                if not m2:raise ValueError('Bad function argument '+t[i:])
                arg=m2[0];j=i+len(arg)
            out+=('*' if out and (out[-1].isalnum() or out[-1]==')') else '')+fn+'('+convert(arg)+')'+('**('+convert(fpow)+')' if fpow is not None else '');i=j
        else:out+=t[i];i+=1
    return out

def parse(t):
    t=t.strip().rstrip('., ')
    p=convert(t)
    result=parse_expr(p,local_dict={'x':X,'y':Y,'e':s.E,'sin':s.sin,'cos':s.cos,'tan':s.tan,'cot':s.cot,'log':s.log,'sqrt':s.sqrt}, transformations=standard_transformations+(implicit_multiplication_application,))
    assert result.free_symbols <= {X,Y}, ('Unexpected displayed symbols',t,result)
    return result
