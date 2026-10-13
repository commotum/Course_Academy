"""Independent restricted LaTeX reader for actual displayed segment mathematics.

No generation metadata or answer IDs are used to interpret mathematical values.
Recognizes the captured source notation plus the authored polynomial masks.
"""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,t,xp,yp=s.symbols('x y t xp yp',real=True)

def group(text,pos):
    if text[pos]!='{':raise ValueError('Expected group: '+text[pos:])
    depth=1;i=pos+1
    while depth:
        if i>=len(text):raise ValueError('Unclosed group')
        depth+=(text[i]=='{')-(text[i]=='}');i+=1
    return text[pos+1:i-1],i

def normalize(text):
    text=text.replace('⁡','').replace('′',"'")
    text=text.replace(r'\frac{\text{d}x}{\text{d}t}','(xp)').replace(r'\frac{\text{d}y}{\text{d}t}','(yp)')
    text=text.replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
    text=text.replace(r'\text{d}t','').replace(r'\,dt','').replace('dt','')
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\pi','pi')
    while r'\frac' in text:
        i=text.index(r'\frac');a,end=group(text,i+5);b,finish=group(text,end)
        text=text[:i]+'(('+normalize(a)+')/('+normalize(b)+'))'+text[finish:]
    # Familiar unparenthesized captured trigonometric arguments pi*t/pi*y.
    text=re.sub(r'\\(sin|cos)\s*pi\s*([xyt])',r'\1(pi*\2)',text)
    text=text.replace(r'\sin','sin').replace(r'\cos','cos')
    text=text.replace(r'\ln','log')
    text=text.replace('^','**').replace('{','(').replace('}',')').replace('[','(').replace(']',')')
    return text

def parse_tex(text):
    z=normalize(text.strip().rstrip('.'))
    expr=parse_expr(z,local_dict={'x':x,'y':y,'t':t,'xp':xp,'yp':yp,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
    if expr.free_symbols-{x,y,t,xp,yp}:raise ValueError('Unknown symbol in '+z+': '+str(expr))
    return expr

def read_prompt(prompt):
    points=re.findall(r'point \$[A-Z]\((-?\d+),\s*(-?\d+)\)',prompt)
    if len(points)!=2:raise ValueError('Printed endpoints missing')
    coords=tuple(int(n) for p in points for n in p)
    last=prompt.rsplit('$',2)[1].removesuffix('=')
    last=last.replace(r'{\int }_{C}','').replace(r'{\int }_C','')
    # dx/dy act as algebraically independent differentials for this reader.
    z=normalize(last).replace('dx','U').replace('dy','V')
    U,V=s.symbols('U V')
    expr=parse_expr(z,local_dict={'x':x,'y':y,'e':s.E,'pi':s.pi,'U':U,'V':V,'sin':s.sin,'cos':s.cos},transformations=standard_transformations+(implicit_multiplication_application,))
    P=s.expand(expr).coeff(U);Q=s.expand(expr).coeff(V)
    if s.simplify(expr-P*U-Q*V)!=0:raise ValueError('Not a printed one-form')
    return coords,P,Q

def integral_rows(solution):
    block=solution.rsplit('$$',2)[1].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    rows=re.split(r'\\\\\s*&\s*=',block)
    lhs,rhs=rows[0].split('& =',1)
    return lhs,[rhs.strip()]+[r.strip() for r in rows[1:]]

def row_value(row,coords):
    x0,y0,x1,y1=coords;dx=x1-x0;dy=y1-y0
    kind='scalar'
    outer=s.Integer(1)
    match=re.fullmatch(r'(-?\d+)\\left\((.*)\\right\)',row.strip())
    if match:outer=s.Integer(match[1]);row=match[2]
    if r'{\int }_{0}^{1}' in row:
        prefix,row=row.split(r'{\int }_{0}^{1}',1)
        if prefix.strip():outer*=parse_tex(prefix)
        kind='integral'
    elif re.search(r'_(?:\{0\}|0)\^(?:\{1\}|1)',row):
        # Endpoint operator applies linearly even when a scalar surrounds it.
        row=re.sub(r'_(?:\{0\}|0)\^(?:\{1\}|1)','',row)
        row=row.replace(r'{|}','').replace('|','');kind='antiderivative'
    expr=parse_tex(row)
    expr=expr.subs({x:x0+dx*t,y:y0+dy*t,xp:dx,yp:dy},simultaneous=True)
    if kind=='integral':return s.simplify(outer*s.integrate(expr,(t,0,1))),kind,outer*expr
    if kind=='antiderivative':return s.simplify(outer*(expr.subs(t,1)-expr.subs(t,0))),kind,outer*expr
    if expr.free_symbols:raise ValueError('Unevaluated scalar '+str(expr))
    return s.simplify(outer*expr),kind,outer*expr

def vector_value(text,coords):
    i,j,a,b=s.symbols('i j a b');x0,y0,x1,y1=coords
    z=normalize(text.strip().rstrip('.,')).replace('i',' i ').replace('j',' j ')
    value=parse_expr(z,local_dict={'i':i,'j':j,'a':a,'b':b,'t':t,'xp':xp,'yp':yp},transformations=standard_transformations+(implicit_multiplication_application,))
    value=value.subs({a:x0*i+y0*j,b:x1*i+y1*j,xp:x1-x0,yp:y1-y0},simultaneous=True)
    return s.expand(value),i,j

def check_path_stages(solution,coords):
    x0,y0,x1,y1=coords;dx=x1-x0;dy=y1-y0
    # Read original position-vector statements and all parameterization rows.
    vectors=re.search(r'are \$a=(.*?)\$ and \$b=(.*?)\$',solution)
    if not vectors:raise ValueError('Endpoint vector statements missing')
    for text,point in zip(vectors.groups(),(coords[:2],coords[2:])):
        v,i,j=vector_value(text,coords)
        assert s.simplify(v-point[0]*i-point[1]*j)==0
    first=solution.split('$$')[1].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    for row in re.split(r'\\\\\s*',first):
        rhs=row.split('=',1)[1]
        v,i,j=vector_value(rhs,coords)
        assert s.simplify(v-(x0+dx*t)*i-(y0+dy*t)*j)==0,('printed path stage',row)
    limits=re.search(r'where \$0\\le t\\le 1\.\$',solution)
    assert limits,'Printed limits missing/altered'
    xmatch=re.search(r'\$x\(t\)=(.*?)\$ and \$y\(t\)=(.*?)\$',solution)
    assert xmatch,'Printed x(t),y(t) missing'
    xx,yy=[parse_tex(z) for z in xmatch.groups()]
    assert s.simplify(xx-x0-dx*t)==0 and s.simplify(yy-y0-dy*t)==0
    # Reinsertion verifies traversal, not only the set of points.
    assert (xx.subs(t,0),yy.subs(t,0))==coords[:2]
    assert (xx.subs(t,1),yy.subs(t,1))==coords[2:]
    block=solution.split('$$')[3].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    sides=block.split('=',2)[1:]
    for rhs in sides:
        v,i,j=vector_value(rhs,coords)
        assert s.simplify(v-dx*i-dy*j)==0,('printed derivative stage',rhs)
    return {'parameterization_rows':len(re.split(r'\\\\\s*',first)),'limits':[0,1]}
