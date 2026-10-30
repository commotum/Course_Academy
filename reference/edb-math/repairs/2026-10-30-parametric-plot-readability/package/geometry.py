import sympy as sp
T=sp.Symbol('t',real=True);U=sp.Symbol('u',real=True);X,Y=sp.symbols('x y')
def expr(s):return sp.sympify(s,locals={'t':T,'pi':sp.pi},rational=True)
def shape(x,y,lo,hi,kind='poly',closed=True):
 return {'x':str(x),'y':str(y),'lo':str(lo),'hi':str(hi),'kind':kind,'closed':closed and kind!='rational','direction_assessed':False}

def geometry_key(s):
 """Complete supported simple arcs: implicit curve + endpoint pair/domain branch.
 No inferred Cartesian equation is displayed or required of the learner.
 """
 x,y=expr(s['x']),expr(s['y']);lo,hi=expr(s['lo']),expr(s['hi'])
 kind=s['kind']
 if kind=='ellipse':
  # All supported trig curves are axis-aligned full ellipses. Derive coefficients
  # from actual x/y evaluations, avoiding parameter spelling identity.
  h=sp.simplify((x.subs(T,0)+x.subs(T,sp.pi))/2);a=sp.simplify(x.subs(T,0)-h)
  k=sp.simplify((y.subs(T,sp.pi/2)+y.subs(T,3*sp.pi/2))/2);b=sp.simplify(y.subs(T,sp.pi/2)-k)
  if a==0 or b==0:raise ValueError('degenerate ellipse')
  poly=sp.Poly(b*b*(X-h)**2+a*a*(Y-k)**2-a*a*b*b,X,Y).monic().as_expr()
  return ('ellipse',str(poly))
 if kind=='root':x=x.subs(T,U**2).subs(sp.Abs(U),U);y=y.subs(T,U**2).subs(sp.Abs(U),U);v=U;lo=sp.sqrt(lo);hi=sp.sqrt(hi)
 else:v=T
 nx,dx=sp.fraction(sp.together(X-x));ny,dy=sp.fraction(sp.together(Y-y))
 poly=sp.Poly(sp.resultant(nx,ny,v),X,Y).sqf_part().monic().as_expr()
 if kind=='rational':
  # Only the positive-t branch is supported; coordinates of a known interior
  # point distinguish branches of the same implicit hyperbola.
  pp=sp.Poly(poly,X,Y);h=-pp.coeff_monomial(Y)/pp.coeff_monomial(X*Y);k=-pp.coeff_monomial(X)/pp.coeff_monomial(X*Y)
  branch=(str(sp.sign(x.subs(v,1)-h)),str(sp.sign(y.subs(v,1)-k)))
  return ('rational',str(poly),branch)
 ends=sorted((str(sp.simplify(x.subs(v,z))),str(sp.simplify(y.subs(v,z)))) for z in (lo,hi))
 return ('arc',str(poly),tuple(ends),s['closed'])

def valid_bank(bank):
 keys=[geometry_key(s) for s in bank]
 if len(set(keys))!=5:raise ValueError('equivalent graphs: reject whole bank')
 return keys

