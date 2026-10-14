#!/usr/bin/env python3
"""Enumerate meaningful finite sampler domains, exact logarithm signatures."""
import itertools,json
from fractions import Fraction as Q
from pathlib import Path

def factors(z):
    result={};p=2
    while p*p<=z:
        while z%p==0:result[p]=result.get(p,0)+1;z//=p
        p+=1
    if z>1:result[z]=result.get(z,0)+1
    return result

def log_signature(a,b=1,c=Q(1)):
    result={p:c*n for p,n in factors(a).items()}
    for p,n in factors(b).items():result[p]=result.get(p,Q(0))-c*n
    return tuple(sorted((p,n) for p,n in result.items() if n))

def main():
    report={}
    eligible=total=0
    for a,b,L,H,j,k in itertools.product(range(1,5),range(1,5),range(-4,2),range(2,5),range(1,4),range(4,9)):
        total+=1;W=H-L;Z=k-j;D=a+b
        if min(a,b)==1 and a!=b:bank=[Q(W*Z,D),Q(W*Z),Q(D*W*Z),Q(Z,D),Q(W+Z,D)]
        else:bank=[Q(W*Z,D),Q(W*Z),Q(D*W*Z),Q(W*Z,a),Q(W*Z,b)]
        if W<=8 and Z<=6 and len(set(bank))==5:eligible+=1
    report['easy_linear']={'sampler_combinations':total,'eligible_mathematical_tasks':eligible,'template_aliases_counted_once':['linear','linear_legacy']}
    for family in ('quotient','reciprocal','reciprocal_scaled'):
        eligible=total=0
        coefficient_pairs=[(1,1)] if family!='reciprocal_scaled' else list(itertools.product(range(2,5),range(2,5)))
        for (c,d),L,H,j,k in itertools.product(coefficient_pairs,range(1,5),range(5,10),range(1,4),range(4,9)):
            total+=1;Z=k-j
            if family=='quotient':
                if L==1:
                    bank=[('log',log_signature(H,L,Q(Z,3))),('log',log_signature(H,L,Q(Z))),('log',log_signature(H,L,Q(Z,2))),('log',log_signature(k,j,Q(Z,3))),('scalar',Q(Z*(H-L),3))]
                else:bank=[log_signature(H,L,Q(Z,3)),log_signature(H,L,Q(Z)),log_signature(H,L,Q(Z,2)),log_signature(H,1,Q(Z)),log_signature(L,1,Q(Z,3))]
            else:
                C=Q(c,2 if family=='reciprocal_scaled' else 1);F=C*(Q(1,L)-Q(1,H))
                if j==1:bank=[('log',log_signature(k,j,F)),('log',log_signature(k,j,C/L)),('log',log_signature(k,j,C/H)),('log',log_signature(k,j,C)),('scalar',F*(k-j))]
                else:bank=[log_signature(k,j,F),log_signature(k,j,C/L),log_signature(k,j,C/H),log_signature(k,1,F),log_signature(j,1,F)]
            if len(set(bank))==5:eligible+=1
        report[family]={'sampler_combinations':total,'eligible_mathematical_tasks':eligible,'equivalence_test':'exact prime-exponent vectors of logarithms','incidental_aliases_excluded':True}
    report['explanation']='All supplied transformation coefficients, actual rectangle bounds and operations matter. Choice order, seed, profile names and template aliases do not count. d cancels from the final hard area but appears in the supplied map and all determinant/cancellation stages, so it changes the assessed derivative task.'
    (Path(__file__).parent/'variety.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
