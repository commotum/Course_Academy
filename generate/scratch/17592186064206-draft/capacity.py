"""Exact finite supported normal domain; canonical ratio keys ignore presentation."""
from fractions import Fraction as F

def enumerate_capacity():
    easy=set();moderate=set();hard=set();raw_counts={'easy':0,'moderate':0,'hard':0}
    def add(level,key,c,a,b):
        coefs=[c/a,-c/a,c,c*a,1/a]
        if level!='easy' and len(set(coefs))!=5:return
        key.add((c/a,b/a));raw_counts[level]+=1
    for c in range(2,13):
        for b in range(1,16):add('easy',easy,F(c),F(1),F(b))
    for b in list(range(-15,0))+list(range(2,16)):add('easy',easy,F(1),F(1),F(b))
    for a in range(-12,-1):
        for b in range(1,16):add('easy',easy,F(1),F(a),F(b))
    for c in range(2,13):
        for a in list(range(-12,-1))+list(range(2,13)):
            for b in list(range(-15,0))+list(range(1,16)):add('moderate',moderate,F(c),F(a),F(b))
    cs={F(n,d) for n in range(1,13) for d in range(2,13) if 0<F(n,d)<1}
    slopes={F(sign*n,d) for n in range(2,13) for d in range(2,13) for sign in (-1,1) if abs(F(n,d))!=1 and abs(F(n,d).numerator)>=2 and F(n,d).denominator>=2}
    for c in cs:
        for a in slopes:
            for b in list(range(-15,0))+list(range(1,16)):add('hard',hard,c,a,F(b))
    return {'method':'exact canceled integrand keys (c/a,b/a); no templates, profiles, variable aliases or option ordering counted','distinct_integrands':{k:len(v) for k,v in [('easy',easy),('moderate',moderate),('hard',hard)]},'eligible_parameter_tuples':raw_counts,'hard_rational_numerators':len(cs),'hard_rational_slopes':len(slopes)}
if __name__=='__main__':
    import json
    print(json.dumps(enumerate_capacity(),indent=2))
