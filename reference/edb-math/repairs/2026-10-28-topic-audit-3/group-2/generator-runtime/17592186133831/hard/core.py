import sympy as s
T,X,Y=s.symbols("t x y",real=True)
def tex(v):
    return s.latex(s.sympify(v),order='lex',fold_short_frac=False).replace(r'\log',r'\ln')
def block(v):return '$$\n'+v+'\n$$'
def aligned(lhs,rows):return r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'
def vector(p,q): return '('+tex(p)+r')\,i+('+tex(q)+r')\,j'
def integ(v,a,b): return r'\int_{'+tex(a)+'}^{'+tex(b)+'}('+tex(v)+r')\,dt'

def math_data(f,p):
    """Exact components; no evaluated integral appears in learner output."""
    a,b,c,d=[s.sympify(p.get(k,1)) for k in ('a','b','c','d')]
    lo,hi=s.sympify(p['lower']),s.sympify(p['upper'])
    if f=='polynomial': P,Q=a*Y**2,-b*X**2; u,v=T,T**2
    elif f=='rotation': P,Q=a*Y,-a*X;u,v=s.cos(T),s.sin(T)
    elif f=='shifted_circle':P,Q=a*X,a*Y+b;u,v=s.cos(T),s.sin(T)
    elif f=='exponential_root':P,Q=a*X*Y**2,2*b*Y;u,v=s.exp(T),s.sqrt(T)
    elif f=='spiral':P,Q=a*X,a*Y;u,v=T*s.cos(T),T*s.sin(T)
    elif f=='monomial':P,Q=a*Y**2,-b*X**2;u,v=T**p['m'],T**p['n']
    elif f=='mixed_spiral':P,Q=a*X+b*Y,c*X+d*Y;u,v=T*s.cos(T),T*s.sin(T)
    else: raise ValueError('unknown family')
    pr,qr=P.subs({X:u,Y:v}),Q.subs({X:u,Y:v})
    du,dv=s.diff(u,T),s.diff(v,T)
    z=s.collect(s.expand(pr*du+qr*dv),T) if f=='mixed_spiral' else s.trigsimp(s.expand(pr*du+qr*dv))
    return P,Q,u,v,pr,qr,du,dv,z,lo,hi


