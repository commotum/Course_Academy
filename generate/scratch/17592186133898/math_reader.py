"""Independent reader of displayed vector fields, scalar expressions and solution rows."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x,y,i,j=sp.symbols('x y i j',real=True)
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
    t=re.sub(r'(cos|sin|log)\s*([xy])',r'\1(\2)',t)
    t=re.sub(r'(sin|cos|log|sqrt)',r' \1',t).replace('{','(').replace('}',')')
    assert '\\' not in t, ('unknown TeX',t)
    return parse_expr(t,local_dict={'x':x,'y':y,'i':i,'j':j,'e':sp.E,'E':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def derivative_inputs(s):
    pat=re.compile(r'\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial)\s*([xy])\}\(');out=[]
    for m in pat.finditer(s):
        depth=1;k=m.end()
        while depth:
            if s[k]=='(':depth+=1
            elif s[k]==')':depth-=1
            k+=1
        out.append((m[1],s[m.end():k-1],m.end(),k-1))
    return out

def displayed(q):
    prompt=re.sub(r'\\mathbf\{([Fij])\}',r'\1',q[':question/problem'])
    m=re.search(r'F\(x,y\)\s*=\s*([^$]+)',prompt)
    if not m:m=re.search(r'F\(x, y\)\s*=\s*([^$]+)',q[':question/problem'])
    if not m:raise ValueError('No standalone supplied vector field')
    v=parse(m[1]);P=sp.expand(v).coeff(i);Q=sp.expand(v).coeff(j)
    assert sp.simplify(v-P*i-Q*j)==0
    pm=re.search(r'at the point \$\((.*?)\)',q[':question/problem'])
    pt=tuple(parse(z) for z in pm[1].split(',')) if pm else None
    return P,Q,pt

def fingerprint(q):
    import hashlib,json
    P,Q,pt=displayed(q)
    # The two assessed partials and evaluation target determine mathematical work.
    obj=[sp.srepr(sp.simplify(sp.diff(Q,x))),sp.srepr(sp.simplify(sp.diff(P,y))),None if pt is None else [sp.srepr(z) for z in pt]]
    return hashlib.sha256(json.dumps(obj).encode()).hexdigest()
