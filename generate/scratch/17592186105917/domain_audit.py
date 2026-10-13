"""Exact conservative slices of the larger finite samplers; scaling excluded."""
import itertools,json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def normalized(v):
    G=math.gcd(*[abs(x) for x in v]);return tuple(Fraction(x,G) for x in v)
# Easy integer slice: fixed b=(1,2,3), a coordinates -3..3.
easy=set();candidates=0
for a in itertools.product(range(-3,4),repeat=3):
    candidates+=1;D=a[0]+2*a[1]+3*a[2];A2=sum(x*x for x in a)
    if not A2 or not D or not a[0] or A2==14:continue
    omitted=D-a[0]
    if omitted==-D:continue
    # Different rational/radical denominator answers; exact squared comparison.
    if D*omitted>0 and D*D*14==omitted*omitted*A2:continue
    easy.add(normalized(a))
# Moderate complete orientation slice: all signed permutations of primitive norm 3/5/7 bases.
V=set()
for v in [(2,1,2),(3,4,0),(6,2,3)]:
    for perm in set(itertools.permutations(v)):
        for signs in itertools.product((-1,1),repeat=3):V.add(tuple(x*sign for x,sign in zip(perm,signs)))
moderate=set();mc=0
for a,b in itertools.product(V,repeat=2):
    A=math.isqrt(sum(x*x for x in a));B=math.isqrt(sum(x*x for x in b));D=sum(x*y for x,y in zip(a,b))
    if A==B or D==0:continue
    for op in [-1,1]:
        mc+=1;P=Fraction(D,B);Q=Fraction(D,A);R=P+op*Q
        bank=[R,P-op*Q,P,P+op*Fraction(D,A*A),-R]
        if len(set(bank))!=5:continue
        moderate.add((normalized(a),normalized(b),op))
# Hard positive mixed-root slice: exact guard arithmetic, two irrational dot terms.
# A2=2+i²+j², B2=k²+3+l²; D=k sqrt2+i sqrt3+jl.
# All five pair-bank collisions cancel common nonzero D. The possible final
# collision -R == P+op D/A² reduces 2/B+op/A+op/A²=0.
# For subtraction, squaring 2/B=(A+1)/A² gives
# A=(4*A2²-A2*B2-B2)/(2*B2), a rational value. This contradicts
# the nonsquare A2 guard. Thus no collision here.
hard=[];hc=0
for i,j,k,l in itertools.product(range(1,4),repeat=4):
    A2=2+i*i+j*j;B2=k*k+3+l*l;hc+=2
    if math.isqrt(A2)**2==A2 or math.isqrt(B2)**2==B2:continue
    G=math.gcd(A2,B2);num,den=A2//G,B2//G
    if math.isqrt(num)**2==num and math.isqrt(den)**2==den:continue
    for op in ('sum','difference'):hard.append({'a':['sqrt(2)',i,j],'b':[k,'sqrt(3)',l],'operation':op})
report={'meaningful_identity_exclusions':['positive common vector scaling','variable aliases','option order','answer-bank profile'], 'sampling_domain_claim':'The enumerated slices are conservative exact lower bounds, not full counts of the wider allowed/sampled family.', 'easy':{'slice_candidates':candidates,'distinct_eligible_tasks':len(easy),'slice':'a in -3..3 cubed; b=(1,2,3); five single_method recipes'}, 'moderate':{'orientation_vectors':len(V),'nondegenerate_pair_candidates':mc,'distinct_eligible_tasks':len(moderate),'slice':'All signed permutations of (2,1,2), (3,4,0), (6,2,3); both operations'}, 'hard':{'slice_candidates':hc,'distinct_eligible_tasks':len(hard),'slice':'a=(sqrt2,i,j), b=(k,sqrt3,l), i,j,k,l in 1..3; both operations','parameters':hard}}
(ROOT/'domain-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print({level:report[level]['distinct_eligible_tasks'] for level in ('easy','moderate','hard')})
