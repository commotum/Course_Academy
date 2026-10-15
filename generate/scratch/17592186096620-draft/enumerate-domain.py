"""Enumerate authored finite coefficient domains, canonical actual functions."""
import itertools,json,math
from pathlib import Path
H=Path(__file__).resolve().parent

def primitive_pair(values):
 gcd=math.gcd(*values);values=tuple(v//gcd for v in values)
 if values[2]<0:values=tuple(-v for v in values)
 return values
# For c*x+e over a*x²+d and (c*x²+e*x) over a*x²+d,
# common scalar rescalings produce identical actual functions. Coincidentally
# canceling a linear factor cannot merge distinct denominator zero sets: the
# denominator has degree2 and nonzero constant; given its zero set it is unique
# up to a scalar. Thus normalized complete polynomial-pair coefficients give
# exact function-and-original-domain equivalence classes in these two families.
report={}
for level,b in [('moderate',4),('hard',3)]:
 values=[z for z in range(-b,b+1) if z];all_p=list(itertools.product(values,repeat=4));classes={primitive_pair(p) for p in all_p}
 report[level]={'coefficients':'nonzero builtin integers of magnitude <='+str(b),'raw_parameter_tuples':len(all_p),'actual_function_and_excluded_zero_set_tasks':len(classes),'slots':['numerator leading coefficient c','numerator second coefficient e','denominator leading coefficient a','denominator constant d'],'notation_or_bank_aliases_counted':False,'quotient_rule_products':4 if level=='moderate' else 6}
(H/'domain-coverage.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
