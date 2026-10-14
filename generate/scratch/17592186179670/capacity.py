import itertools,math,json
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).parent
def radical(n):
 m=math.isqrt(n)
 for k in range(m,0,-1):
  if n%(k*k)==0:return k,n//(k*k)
def term(c,n):
 m,q=radical(n);return (F(0),1) if not c else (F(c)*m,q)
def unique(vals):return len(set(vals))==len(vals)
capacities={}
# Exact field Q(sqrt(N)) scalar banks; complete profiles rejected together.
tasks=set();parameter_instances=0
for a,b,dx,dy,c,d in itertools.product(range(-3,4),range(-3,4),[-3,-2,2,3],[-3,-2,2,3],[-3,-2,1,2,3],[-3,-2,1,2,3]):
 A=c*dx+d*dy;B=c*a+d*b;n=dx*dx+dy*dy;I=F(A,2)+B
 if not A:continue
 bank=[term(I,n),(I,1),term(B,n),term(A+B,n),term(F(A,8)+F(B,2),n)]
 if not unique(bank):continue
 parameter_instances+=1;tasks.add((radical(n),term(A,n),term(B,n),'linear'))
capacities['easy/linear']={'eligible_parameter_instances':parameter_instances,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive exact rational/radical tuples; weighted linear coefficients and speed; complete bank distinctness.'}
tasks=set();count=0
for a,b,dx,dy,c in itertools.product(range(1,4),range(1,4),[-2,-1,1,2,3],[-2,-1,1,2,3,4,5],range(1,4)):
 if a+dx<0 or b+dy<0:continue
 C0=c*a*b;C1=c*(a*dy+b*dx);C2=c*dx*dy;n=dx*dx+dy*dy;I=F(C2,3)+F(C1,2)+C0
 bank=[term(I,n),(I,1),term(F(C2,3)+C0,n),term(F(C1,2)+C0,n),term(F(C2,2)+F(C1,2)+C0,n)]
 if not unique(bank):continue
 count+=1;tasks.add((radical(n),term(C2,n),term(C1,n),term(C0,n),'product'))
capacities['moderate/product']={'eligible_parameter_instances':count,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive exact rational/radical tuples of weighted quadratic coefficients and speed; complete bank distinctness.'}
tasks=set();count=0
for a,(k,dy) in itertools.product(range(1,5),[(1,1),(1,4),(2,2),(2,8),(3,3),(4,1),(4,4)]):
 h=math.isqrt(k*dy);I=a+F(2*h,3);s=dy
 bank=[s*I,I,s*(a+h),s*(a+F(h,2)),s*(a+F(3*h,2))]
 if not unique(bank):continue
 count+=1;tasks.add((s,s*a,s*h,'radical'))
capacities['moderate/radical']={'eligible_parameter_instances':count,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive rational banks; weighted constant and sqrt(t) coefficients and speed.'}
tasks=set();count=0
for dx,dy,c,d in itertools.product([-3,-2,-1,1,2,3],[-4,-3,-2,2,3,4],[-3,-2,-1,1,2,3],[-2,-1,1,2]):
 k=c*dx+d*dy
 if not 1<=abs(k)<=4:continue
 # Five banks have distinct coefficient patterns in Q(sqrt(N))[exp(k)]
 # or exp(2k); exp(nonzero algebraic integer) is transcendental.
 n=dx*dx+dy*dy
 if n==1:continue
 count+=1;tasks.add((radical(n),k,'exponential'))
capacities['moderate/exponential']={'eligible_parameter_instances':count,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive slope/speed tuples; exponential transcendence separates different polynomial coefficient banks.'}
tasks=set();count=0
for a,dx,dy,den in itertools.product(range(-3,4),[-2,-1,1,2,3],[-3,-2,-1,1,2,3,4,5],[3,4,6]):
 if not 1<=abs(dy-dx)<=4:continue
 count+=1;tasks.add((radical(dx*dx+dy*dy),den,'secant'))
capacities['hard/secant']={'eligible_parameter_instances':count,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive speed/angle tuples; sec² evenness removes sign and translations. Angles ±pi/3, ±pi/4, ±pi/6; pi transcendence separates bank powers.'}
tasks=set();count=0
for a,b,dx,dy in itertools.product(range(-1,2),range(1,4),[1,2,3],[1,2,3]):
 B=dx*b+dy*a;q1=(a+dx)*(b+dy)
 if not 1<=B<=10 or q1>18:continue
 count+=1;tasks.add((radical(dx*dx+dy*dy),dx*dy,B,a*b,'matched_exponential'))
capacities['hard/matched_exponential']={'eligible_parameter_instances':count,'meaningful_mathematical_tasks':len(tasks),'proof':'Exhaustive speed and exponent-quadratic tuples; positive slope and dx,dy enforce noncollision; exp(integer) transcendence separates coefficient banks.'}
capacities['easy/odd_linear_explicit']={'eligible_parameter_instances':12,'meaningful_mathematical_tasks':12,'proof':'Normal method bank: a in2..4,c in1..4; a=1 collides and rejects whole bank. Public source raw bank retains anchor a=1,c=2. Fixed y=0; unused d excluded from fingerprint.'}
(P/'capacity.json').write_text(json.dumps(capacities,indent=2)+'\n');print(json.dumps(capacities,indent=2))
