"""Enumerate the valid default support with exact rational task normalization.

Radio derivative collisions occur only for a unit constant inner derivative;
those linear cases are excluded below. Other default radio values have different
polynomial/logarithm factors, so they are unequal functions. Moderate radio keeps
u(t)=1 and a>=2. Blanks require nonzero slopes. This is domain cardinality,
distinct from the sample/engine checks in validate.py.
"""
import itertools as it
from fractions import Fraction


def enumerate_variety():
    B=range(2,7);A=range(1,10);S=(-3,-2,-1,1,2,3);C=range(2,6);D=(-5,-4,-3,-2,-1,1,2,3,4,5)
    rows={}
    def key(b,c,a,k,l,d,t=None,fragment=False):
        if fragment:return (2 if b==4 else b,(2 if b==4 else 1)*3*a)
        mult=2 if b==4 else 1
        return (2 if b==4 else b,mult*a,mult*k,mult*l,Fraction(c)*Fraction(b)**d,t)
    def count(qid,values,fragment=False):
        values=list(values);tasks={key(*v,fragment=fragment) for v in values}
        rows[qid]={'valid_parameter_instances':len(values),'distinct_mathematical_tasks':len(tasks),
                    'domain':'default sampler support; normalize 4=2^2 and multiplicative exponent offset; fragments exclude unused offset'}
    count('q-48565',((b,1,a,0,0,0) for b,a in it.product(B,A)))
    count('q-48631',((b,1,a,0,0,d) for b,a,d in it.product(B,A,D)))
    count('q-107458',((b,1,-a,0,0,d) for b,a,d in it.product(B,A,range(1,6))))
    count('q-71881',((b,c,a,0,l,0) for b,c,a,l in it.product(B,C,A,S)))
    count('q-107459',((b,c,a,0,0,d) for b,c,a,d in it.product(B,C,A,D)))
    count('q-107461',((b,1,-a,0,0,1) for b,a in it.product(B,range(2,10))))
    count('q-1952',((b,1,a,0,0,0) for b,a in it.product(B,range(2,10))))
    count('q-312462',((b,1,a,0,0,d) for b,a,d in it.product(B,A,range(-5,6))),fragment=True)
    count('q-340969',((b,1,a,0,l,d,t) for b,a,l,d,t in it.product(B,S,S,range(-2,3),(-1,1))
                       if abs(a*t**3+l*t+d)<=2 and 3*a*t*t+l!=0))
    count('authored-three-term-slope',((b,c,a,k,l,z-a*t**3-k*t*t-l*t,t)
                       for b,c,a,k,l,z,t in it.product(B,range(2,5),S,S,S,(-1,0,1,2),(-1,1))
                       if abs(z-a*t**3-k*t*t-l*t)<=5 and 3*a*t*t+2*k*t+l!=0))
    count('q-48659',((b,1,a,0,0,0,Fraction(1,a)) for b,a in it.product(B,range(2,10))))
    return rows
