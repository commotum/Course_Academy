"""Independent parser for the actual restricted printed TeX vocabulary.
No generation metadata is used. Rejects unconsumed notation and invalid vectors.
"""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
T,X,Y=s.symbols('t x y',real=True)

def normalize(raw):
    raw=raw.replace('⁡','').replace('′',"'")
    raw=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',raw)
    raw=re.sub(r'\{(sin|cos)\}',r'\\\1',raw)
    raw=raw.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(' ', '')
    raw=raw.replace(r'\mathrm{d}', 'd').replace(r'\text{d}','d')
    return raw

class Parser:
    def __init__(self,raw):
        self.raw=normalize(raw)
        self.ts=re.findall(r'\\(?:sin|cos|frac|sqrt|pi)|\\[A-Za-z]+|\d+|[A-Za-z]|[^\s]',self.raw);self.i=0
    def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
    def pop(self):
        v=self.peek()
        if v is None:raise ValueError('unexpected end '+self.raw)
        self.i+=1;return v
    def atom(self):
        tok=self.pop()
        if tok in ('+','-'):return (1 if tok=='+' else -1)*self.power()
        if tok in ('{','('):
            close='}' if tok=='{' else ')';value=self.sum()
            if self.pop()!=close:raise ValueError('unbalanced group')
            return value
        if tok==r'\frac':return self.atom()/self.atom()
        if tok==r'\sqrt':return s.sqrt(self.atom())
        if tok in (r'\sin',r'\cos'):
            power=1
            if self.peek()=='^':self.pop();power=self.atom()
            arg=self.atom()
            return (s.sin(arg) if tok==r'\sin' else s.cos(arg))**power
        if tok==r'\pi':return s.pi
        if tok=='e':return s.E
        if tok in ('t','x','y'):return {'t':T,'x':X,'y':Y}[tok]
        if tok.isdecimal():return s.Integer(tok)
        raise ValueError('unexpected '+tok+' in '+self.raw)
    def power(self):
        a=self.atom()
        if self.peek()=='^':self.pop();a=a**self.atom()
        return a
    def product(self):
        a=self.power()
        while self.peek() is not None and self.peek() not in ('+','-',')','}'):
            if self.peek() in ('*','/'):
                op=self.pop();v=self.power();a=a*v if op=='*' else a/v
            else:a*=self.power()
        return a
    def sum(self):
        a=self.product()
        while self.peek() in ('+','-'):
            op=self.pop();v=self.product();a=a+v if op=='+' else a-v
        return a
    def parse(self):
        a=self.sum()
        if self.peek() is not None:raise ValueError('unconsumed '+self.raw)
        return a

def expr(raw):return Parser(raw.strip().rstrip('.')).parse()
def vector(raw):
    raw=normalize(raw)
    scale=re.fullmatch(r'\(([+-]?\d+)\)\((.*)\)',raw)
    if scale:
        a,b=vector(scale[2]);return int(scale[1])*a,int(scale[1])*b
    if raw.startswith('(') and raw.endswith(')'):
        depth=0;close=None
        for i,c in enumerate(raw):
            depth+=(c=='(')-(c==')')
            if depth==0:close=i;break
        if close==len(raw)-1:return vector(raw[1:-1])
    # All supported source/generated vectors have exactly one basis marker each.
    if len(re.findall(r'i(?=[+-]|$)',raw))!=1 or raw.count('j')!=1:raise ValueError('missing/extra basis marker')
    left,other=re.split(r'i(?=[+-]|$)',raw);right,tail=other.split('j')
    if tail:raise ValueError('vector trailing notation')
    return expr(left if left not in ('','+','-') else left+'1'),expr(right if right not in ('','+','-') else right+'1')

def integral(raw):
    raw=normalize(raw)
    scale=re.fullmatch(r'\(([+-]?\d+)\)\((.*)\)',raw)
    if scale:
        f,a,b,v=integral(scale[2]);return (int(scale[1])*f if f is not None else None),a,b,int(scale[1])*v
    # Unscaled source 0 is a scalar option; meaningful scalar-equality check only.
    if raw=='0':return None,None,None,s.Integer(0)
    sign=-1 if raw.startswith('-') else 1
    if sign==-1:raw=raw[1:]
    raw=raw.replace(r'{\int}',r'\int')
    if not raw.startswith(r'\int_'):raise ValueError('invalid complete integral '+raw)
    def group(pos):
        if raw[pos]!='{':raise ValueError('bound must be grouped')
        depth=1;end=pos+1
        while depth:
            if end>=len(raw):raise ValueError('unbalanced integral bounds')
            depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
        return raw[pos+1:end-1],end
    ar,pos=group(len(r'\int_'))
    if raw[pos]!='^':raise ValueError('upper bound required')
    br,pos=group(pos+1)
    if not raw.endswith('dt'):raise ValueError('differential required')
    integrand=raw[pos:-2]
    a,b=expr(ar),expr(br);f=sign*(expr(integrand) if integrand else 1)
    value=s.simplify(s.integrate(f,(T,a,b)))
    return f,a,b,value

def prompt(raw):
    f=re.search(r'F\(x,y\)=(.*?)\$ and',raw).group(1)
    curve=re.search(r'r\(t\)=(.*?)\$ for',raw).group(1)
    limits=re.search(r't\\in \[(.*?),(.*?)\]',raw)
    P,Q=vector(f);u,v=vector(curve)
    a,b=expr(limits[1]),expr(limits[2])
    return P,Q,u,v,a,b
