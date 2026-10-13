"""Finite bounded-family audit; exact response tasks, no seed/bank aliases.
Internal scalar checks are independent eligibility proofs, not learner work.
"""
import itertools,json
from pathlib import Path
import sympy as s
T=s.Symbol('t',real=True);A,B,C,D=s.symbols('a b c d',real=True)
COEFF=(-4,-3,-2,-1,1,2,3,4)

def count(f):
    if f=='monomial':geometries=[(0,k,T**m,T**n,m,n) for m,n in itertools.permutations((2,3,4),2) for k in (1,2,3)]
    elif f=='polynomial':geometries=[(0,k,T,T**2,None,None) for k in (1,2,3)]
    elif f=='exponential_root':geometries=[(1,k,s.exp(T),s.sqrt(T),None,None) for k in (2,3)]
    else:geometries=[(0,k,(T if f in ('spiral','mixed_spiral') else 1)*s.cos(T),(T if f in ('spiral','mixed_spiral') else 1)*s.sin(T),None,None) for k in (s.pi/3,2*s.pi/3,4*s.pi/3)]
    nominal=eligible=0;tasks=set();rejected=0
    for lo,hi,u,v,m,n in geometries:
        if f in ('polynomial','monomial'):p,q=A*v**2,-B*u**2;vars=(A,B)
        elif f=='rotation':p,q=A*v,-A*u;vars=(A,)
        elif f=='shifted_circle':p,q=A*u,A*v+B;vars=(A,B)
        elif f=='exponential_root':p,q=A*u*v**2,2*B*v;vars=(A,B)
        elif f=='spiral':p,q=A*u,A*v;vars=(A,)
        else:p,q=A*u+B*v,C*u+D*v;vars=(A,B,C,D)
        z=s.expand(p*s.diff(u,T)+q*s.diff(v,T));exprs=(z,-z,p*s.diff(u,T),q*s.diff(v,T),p+q)
        # Exact coefficientwise integration; no floating point uniqueness check.
        scalar_basis=[[s.simplify(s.integrate(s.diff(e,k),(T,lo,hi))) for k in vars] for e in exprs]
        task_basis=[s.expand(s.expand_trig(s.trigsimp(s.diff(z,k))).subs(s.cos(T)**2,1-s.sin(T)**2)) for k in vars]
        def pieces(e):
            out={}
            for term in s.Add.make_args(s.expand(e)):
                c,v=term.as_coeff_Mul();out[s.srepr(v)]=c
            return out
        scalar_parts=[[pieces(e) for e in row] for row in scalar_basis]
        task_parts=[pieces(e) for e in task_basis]
        def combine(cs,parts):
            keys=set().union(*(set(d) for d in parts))
            return tuple(sorted((k,sum(c*d.get(k,0) for c,d in zip(cs,parts))) for k in keys if sum(c*d.get(k,0) for c,d in zip(cs,parts))))
        for cs in itertools.product(COEFF,repeat=len(vars)):
            if f=='mixed_spiral' and (cs[0]==cs[3] or cs[1]==cs[2]):continue
            nominal+=1
            vals=[combine(cs,row) for row in scalar_parts]
            if len(set(vals))!=5:rejected+=1;continue
            eligible+=1
            tasks.add((combine(cs,task_parts),str(lo),str(hi)))
    return {'nominal_parameter_instances':nominal,'eligible_complete_banks':eligible,'whole_bank_rejections':rejected,'distinct_integrand_and_bounds_tasks':len(tasks)}

def main():
    report={f:count(f) for f in ('polynomial','rotation','shifted_circle','exponential_root','spiral','monomial','mixed_spiral')}
    p=Path(__file__).with_name('variety.json');p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
