"""Independent reader of displayed vector fields, scalar expressions and solution rows."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x,y,i,j,t=sp.symbols('x y i j t',real=True)
def clean(s):
    return s.replace(r'\u2061','').replace('⁡','').replace('\\\\','\\')
def group(s,pos):
    assert s[pos]=='{', (s,pos)
    depth=1;k=pos+1
    while depth:
        if s[k]=='{':depth+=1
        elif s[k]=='}':depth-=1
        k+=1
    return s[pos+1:k-1],k

def parse(t):
    t=clean(t).strip().rstrip('.,').replace(r'\,',' ').replace(r'\!','').replace(r'\cdot','*').replace(r'\times','*').replace('−','-')
    t=re.sub(r'\\(?:left|right|big|Big|bigl|bigr)\s*','',t)
    t=re.sub(r'\\operatorname\{(ln|sin|cos)\}',lambda m:{'ln':'log','sin':'sin','cos':'cos'}[m[1]],t)
    while re.search(r'\\(?:d?frac|sqrt)',t):
        m=re.search(r'\\(d?frac|sqrt)',t);a,end=group(t,m.end());aa=parse(a)
        if m[1].endswith('frac'):
            b,end=group(t,end);bb=parse(b);rep='(('+sp.sstr(aa)+')/('+sp.sstr(bb)+'))'
        else:rep='sqrt('+sp.sstr(aa)+')'
        t=t[:m.start()]+rep+t[end:]
    t=t.replace(r'\ln','log').replace(r'\log','log').replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\pi','pi')
    t=re.sub(r'\{?(sin|cos)\}?\^\{(\d+)\}\s*t',r'\1(t)^\2',t)
    t=re.sub(r'(cos|sin|log)\s*([xyt])',r'\1(\2)',t)
    t=re.sub(r'(sin|cos|log|sqrt)',r' \1',t).replace('{','(').replace('}',')')
    assert '\\' not in t, ('unknown TeX',t)
    return parse_expr(t,local_dict={'t':globals()['t'],'x':x,'y':y,'i':i,'j':j,'e':sp.E,'E':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))


def integral(s):
    s=clean(s).strip().rstrip('.,').replace(r'\displaystyle','')
    m=re.fullmatch(r'(\d+)\\left\((.*)\\right\)',s)
    if m:
        a,b,v=integral(m[2]);return a,b,int(m[1])*v
    s=s.replace(r'{\int }',r'\int')
    pos=s.index(r'\int');coef=parse(s[:pos]) if pos else sp.Integer(1)
    k=pos+len(r'\int');assert s[k]=='_';a,k=group(s,k+1);assert s[k]=='^';b,k=group(s,k+1)
    body=s[k:];body=re.sub(r'(?:\\,)?(?:\\text\{d\}|d)t$', '',body).strip()
    return parse(a),parse(b),sp.simplify(coef*parse(body))

def value(s):
    a,b,v=integral(s);return sp.integrate(v,(t,a,b))
