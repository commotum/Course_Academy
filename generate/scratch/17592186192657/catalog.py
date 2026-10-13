#!/usr/bin/env python3
"""Independent exhaustive census of finite integer domain; no presentation aliases.

Counts bank eligibility from exact Fraction error operations, and quotients out
whole-equation sign/GCF and equation order. Retains genuine division operands.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json
N=[i for i in range(-7,8) if i];coords=[i for i in range(-5,6) if i]
def census():
    result={}
    for level in ('easy','moderate','hard'):
        tasks=set();valid_parameters=0;profiles={'signed_substitution':0,'distribution_division':0};collapsed=0
        smalls=[1] if level=='easy' else [-3,-2,2,3]
        ratios=range(2,8) if level=='easy' else range(2,5) if level=='moderate' else range(5,8)
        ceiling={'easy':25,'moderate':35,'hard':40}[level]
        for row in (1,2):
            for small in smalls:
                for ratio in ratios:
                    for sign in (-1,1):
                        other=small*ratio*sign;b,d=(small,other) if row==1 else (other,small);k=-other//small
                        for a in N:
                            for c in N:
                                if (gcd(abs(a),abs(b))!=1 or gcd(abs(c),abs(d))!=1):
                                    collapsed+=100;continue
                                h=k*a+c if row==1 else a+k*c
                                if abs(h)<2:continue
                                A=a if row==1 else c;B=small
                                for X in coords:
                                    for Y in coords:
                                        C=a*X+b*Y;D=c*X+d*Y
                                        if max(abs(C),abs(D))>ceiling:continue
                                        R=C if row==1 else D;scaledrhs=R;unscaledrhs=D if row==1 else C
                                        n=h*X
                                        def back(v):return v,F(R-A*v,B)
                                        omitted=back(F(scaledrhs+unscaledrhs,h));signed=back(F(unscaledrhs-k*scaledrhs,h));add=(F(X),F(R+A*X,B));correct=(F(X),F(Y))
                                        banks={'signed_substitution':[correct,omitted,signed,add,(F(X),F(-Y))]}
                                        denominator=a+c
                                        if abs(B)>1 and denominator:banks['distribution_division']=[correct,back(F(n,denominator)),omitted,add,(F(X),F(R-A*X))]
                                        eligible=[name for name,bank in banks.items() if len(set(bank))==5]
                                        if not eligible:continue
                                        valid_parameters+=1
                                        for name in eligible:profiles[name]+=1
                                        normalized=[]
                                        for u,v,rhs in ((a,b,C),(c,d,D)):
                                            g=gcd(gcd(abs(u),abs(v)),abs(rhs))*(1 if u>0 else -1);normalized.append((u//g,v//g,rhs//g))
                                        task=(tuple(sorted(normalized)),normalized[row-1],abs(h),abs(B));tasks.add(task)
        result[level]={'complete_bank_eligible_parameter_sets':valid_parameters,'meaningful_tasks':len(tasks),'eligible_parameter_sets_by_profile':profiles,'nonprimitive_row_candidates_excluded':collapsed,'deduplication':'whole-line signs/GCF and equation order; bank and layout omitted; actual absolute collected/back division operands retained'}
    return result
if __name__=='__main__':
    report=census();Path(__file__).with_name('catalog.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
