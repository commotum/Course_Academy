"""Supplementary real cube-root checks on both signs of x and y.

The main validator checks every primitive and inversion equation. This separately
reads the displayed cube-root answer and checks its real-root derivative on both
real branches, so a CAS principal complex power cannot stand in for real TeX.
"""
import json
from pathlib import Path
import sympy as sp
import validate as v

def main():
    cases=[]
    for a in range(1,9):
        r=v.m.generate('moderate',template='q-79660',parameters={'a':a})
        q=r['question'];f=q[':question/answer-fields'][0]
        value=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1])
        assert r'\sqrt[3]' in value
        e=v.expression(value.split('=',1)[1]);assert e.is_Pow and e.exp==sp.Rational(1,3)
        rad=e.base;drad=sp.diff(rad,v.X);rhs=v.rhs_from_prompt(q[':question/problem'])
        for xv in (-2,2):
            for kv in (-20*a,20*a):
                rv=rad.subs({v.X:xv,v.K:kv});assert rv!=0
                yv=sp.real_root(rv,3);yp=drad.subs(v.X,xv)/(3*yv**2)
                assert sp.simplify(yp-rhs.subs({v.X:xv,v.Y:yv}))==0
                cases.append({'a':a,'x':xv,'K':kv,'radicand':str(rv),'real_y':str(yv),'correct':True})
    report={'status':'passed','real_cube_root_domain_cases':len(cases),
      'scope':'both signs of x and y; connected intervals avoiding x=0 and root radicand=0',
      'cases':cases,'database_writes':0}
    Path(__file__).with_name('domain-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Real cube-root domains:',len(cases),'passed')

if __name__=='__main__':main()
