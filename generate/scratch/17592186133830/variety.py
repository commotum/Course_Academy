"""Enumerate every eligible finite task via exact normalized-operation banks.
The scalar field coefficient c scales every bank member, so six nonzero c values
are distinct tasks but share collision status. No bank/profile aliases counted.
"""
import importlib.util,itertools,json
from fractions import Fraction as Q
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def key(e):return s.srepr(s.expand(e))
def valid(values):return len(set(key(s.simplify(e)) for e in values))==5

def main():
 counts={};rejections={}
 # Separate rational/radical coordinates permit efficient exact enumeration.
 for family in ('sum','reciprocal'):
  accepted=0;total=0
  for a,b,lo,D in itertools.product((-4,-3,-2,-1,1,2,3,4),tuple(range(-6,0))+tuple(range(1,7)),(-2,-1,0,1),(1,2,3,4)):
   total+=1;hi=lo+D;A=abs(a)
   if family=='sum':
    H=a*(hi*hi-lo*lo)+b*D
    values=[(0,Q(A*H)),(Q(H),0),(Q(2*A*A*H),0),(0,Q(A*a*(hi*hi-lo*lo))),(0,Q(A)*(Q(a,2)*(hi*hi-lo*lo)+b*D))]
   else:
    values=[(0,Q(A*D,b)),(Q(D,b),0),(Q(2*A*A*D,b),0),(0,Q(-A*D,b)),(0,Q(A*D*b))]
   accepted+=len(set(values))==5
  counts[family]=accepted*6;rejections[family]=(total-accepted)*6
 # Remaining normalized banks use bounded small algebraic or pi expressions.
 for family in ('circle_cos','circle_sin'):
  accepted=0;total=0
  for R,(lo,hi) in itertools.product(range(1,7),g.ANGLE_INTERVALS):
   total+=1;S=s.sin(2*hi)-s.sin(2*lo);D=hi-lo
   if family=='circle_cos':
    result=R**3*S/2;values=[result,result/R,result*R,2*result,result+R**3*D]
   else:
    result=R**3*(D/2-S/4);values=[result,result/R,result*R,R**3*(D/2+S/4),R**3*(D/2-S/2)]
   accepted+=valid(values)
  counts[family]=accepted*12;rejections[family]=(total-accepted)*12
 family='cubic';accepted=0;total=0
 for (aa,bb),sx,sy,k in itertools.product(g.PAIR_DOMAIN,(-1,1),(-1,1),(1,2,3)):
  a,b=aa*sx,bb*sy;H=a**3-k*b**3;n=5;total+=1
  values=[Q(H*n,4),Q(H,7),Q(4*H*n*n,9),Q((a**3-b**3)*n,4),Q((a**3+k*b**3)*n,4)]
  accepted+=len(set(values))==5 and H!=0
 counts[family]=accepted*6;rejections[family]=(total-accepted)*6
 def power_integral(n,lo,hi):return (s.sympify(hi)**(n+1)-s.sympify(lo)**(n+1))/(n+1)
 # Scale s² multiplies all except omitted speed; enumerate scale explicitly.
 for family in ('fractional','mixed_fractional'):
  accepted=0;total=0
  ds=(0,) if family=='fractional' else g.COEFF
  # Use actual c/d ratio so common scaling does not inflate bank eligibility.
  for scale,c,d,(lo,hi) in itertools.product(range(1,6),g.COEFF,ds,g.POWER_INTERVALS):
   total+=1
   M=lambda n:power_integral(s.Rational(n),lo,hi)
   fx=Q(4,3)*c*scale
   fy=d*scale
   J=fx*scale*(M(Q(5,2))+M(Q(3,2)))+fy*scale*(M(3)/2-M(2)/2-M(1))
   omit=fx*M(Q(3,2))+fy*(M(2)/2-M(1))
   square=fx*scale**2*(M(Q(7,2))+2*M(Q(5,2))+M(Q(3,2)))+fy*scale**2*(M(4)/2-3*M(2)/2-M(1))
   if family=='fractional':values=[J,omit,square,fx*scale*M(Q(5,2)),fx*scale*(Q(2,5)*(s.sympify(hi)**Q(7,2)-s.sympify(lo)**Q(7,2))+Q(2,3)*(s.sympify(hi)**Q(5,2)-s.sympify(lo)**Q(5,2)))]
   else:values=[J,omit,square,fx*scale*(M(Q(5,2))+M(Q(3,2))),fy*scale*(M(3)/2-M(2)/2-M(1))]
   accepted+=valid(values)
  counts[family]=accepted;rejections[family]=total-accepted
 family='involute';accepted=0;total=0
 for A,c,d,(lo,hi) in itertools.product(range(1,6),g.COEFF,g.COEFF,g.INV_INTERVALS):
  total+=1;M=lambda n:power_integral(s.Integer(n),lo,hi)
  B=c*A*A+d;J=A*(B*M(1)+c*A*A*M(3))
  values=[J,B*M(0)+c*A*A*M(2),A*A*(B*M(2)+c*A*A*M(4)),c*A**3*(M(1)+M(3)),A*B*M(1)]
  accepted+=B!=0 and valid(values)
 counts[family]=accepted;rejections[family]=total-accepted
 report={'exact_eligible_task_counts_by_family':counts,'whole_instance_rejections_in_declared_domain':rejections,'exact_counts_by_level':{l:sum(v for f,v in counts.items() if g.TEMPLATES[f]==l) for l in ('easy','moderate','hard')},'meaningfulness':'actual parameterized curve/traversal, field, integrand and bounds; excludes seed, option order, bank aliases, parameter spelling and original question UUID','scope':'all finite normal domains; raw opaque profiles and separately inferred historical completions excluded','orientation':'derivative/parameterization and traversal assessed; square-field equal scalar values do not make printed coordinate tasks identical'}
 (HERE/'variety.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
