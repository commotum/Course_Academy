import re
from functools import lru_cache
import sympy as sp
x,y,z=sp.symbols("x y z", real=True)
@lru_cache(maxsize=20000)
def parse(s):
    s=s.replace('&','').replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1 ',s)
    ts=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',s); pos=0
    def atom():
        nonlocal pos
        t=ts[pos];pos+=1
        if t in ('+','-'): return (1 if t=='+' else -1)*power()
        if t in ('(','{'):
            a=expr(); assert ts[pos]==(')' if t=='(' else '}'),(s,ts,pos);pos+=1;return a
        if t==r'\frac': return atom()/atom()
        if t==r'\dfrac':return atom()/atom()
        if t==r'\sqrt':return sp.sqrt(atom())
        if t in (r'\sin',r'\cos',r'\ln'):
            return {r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log}[t](power())
        if t==r'\pi':return sp.pi
        if t=='e':return sp.E
        if t in ('x','y','z'):return {'x':x,'y':y,'z':z}[t]
        if re.fullmatch(r'\d+(?:\.\d+)?',t):return sp.Rational(t)
        raise ValueError((s,t))
    def power():
        nonlocal pos
        a=atom()
        if pos<len(ts) and ts[pos]=='^':pos+=1;a=a**atom()
        return a
    def product():
        nonlocal pos
        a=power()
        while pos<len(ts) and ts[pos] not in ('+','-',')','}',',',';','='):
            if ts[pos] in ('*',r'\cdot',r'\times'):pos+=1;a*=power()
            elif ts[pos]=='/':pos+=1;a/=power()
            else:a*=power()
        return a
    def expr():
        nonlocal pos
        a=product()
        while pos<len(ts) and ts[pos] in ('+','-'):
            t=ts[pos];pos+=1;b=product();a=a+b if t=='+' else a-b
        return a
    a=expr()
    if pos!=len(ts):raise ValueError((s,'unconsumed',ts[pos:]))
    return sp.simplify(a)
def tex(a):return sp.latex(sp.simplify(a),fold_short_frac=False).replace(r'\log',r'\ln')
def relation(v,c,e):return r'\{\begin{aligned}'+v+'='+tex(c)+r' \\ z='+tex(e)+r'\end{aligned}'
def equations(value):
    s=value.replace('\\\\', '\\') if r'\\begin' in value else value
    s=s.replace(r'\left', '').replace(r'\right.', '').replace(r'\right', '')
    s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).replace(r'\{','').lstrip('{')
    rows=re.split(r'\\\\|;',s)
    return [parse(a.strip().rstrip(','))-parse(b.strip().rstrip(',')) for row in rows if '=' in row for a,b in [row.split('=',1)]]
@lru_cache(maxsize=20000)
def line_key(value):
    es=equations(value);assert len(es)==2
    A,b=sp.linear_eq_to_matrix(es,[x,y,z]);assert A.rank()==2
    return tuple(sp.cancel(t) for t in A.row_join(b).rref()[0])
