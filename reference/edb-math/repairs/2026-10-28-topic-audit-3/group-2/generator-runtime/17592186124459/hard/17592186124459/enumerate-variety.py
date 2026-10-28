#!/usr/bin/env python3
"""Independent finite-domain counts; no bank aliases/incidental magnitudes.

For nonaxis trig u,v=+/-1, G=(uv(2a+b)sin1,(a-b)cos1).
Both sin1 and cos1 are fixed positive numbers, so positive parallelism is exactly
positive scaling of the integer coefficient pair. a=b is rejected: omission of
one x contribution would supply another valid x-axis direction. For a!=b the
complete bank's remaining pairs are distinct: sin1>cos1>0, 2a+b>|a-b|, and
3a^2+4ab-b^2>0 throughout a,b=1..4 bound the swapped-vector cross products.
Axis banks are valid for all positive a,b in this domain; their actual directions
are only +/-y, irrespective of a,b or v. Negative requested orientation flips
all choices and preserves pairwise eligibility.

Hard eligibility is exact Fraction arithmetic. a=1 makes the omitted-inner-power
unit option equal the correct option; norm=1 collapses normalization distractors.
Other positive gradients have distinct complete vector values under the unit
criterion. Common positive gradient magnitude is removed in direction counts.
"""
from fractions import Fraction
from itertools import product
from math import gcd
import json
from pathlib import Path
ROOT=Path(__file__).parent
hard_parameters=[];hard_contexts=set();hard_dirs=set()
for a,b,c,u,v,w in product(range(1,7),range(1,7),range(1,7),range(1,4),range(1,4),range(1,4)):
 G=[Fraction(a,u),Fraction(b,v),Fraction(c,w)];N=sum(t*t for t in G)
 if a==1 or any(t>4 or t.denominator>3 for t in G) or N>36 or N.numerator>50 or N.denominator>9 or len(set(G))<2 or N==1:continue
 hard_parameters.append([a,b,c,u,v,w]);d=gcd(gcd(a,b),c);hard_contexts.add((a//d,b//d,c//d,u,v,w));hard_dirs.add(tuple(t/G[0]for t in G))
trig_dirs={(0,1),(0,-1)};nonaxis_contexts=0
for a,b,u,v,sg in product(range(1,5),range(1,5),[-1,1],[-1,1],[-1,1]):
 if a==b:continue
 nonaxis_contexts+=1;pair=(sg*u*v*(2*a+b),sg*(a-b));d=gcd(abs(pair[0]),abs(pair[1]));trig_dirs.add(tuple(t//d for t in pair))
r={'hard_eligible_parameter_tuples_without_orientation':len(hard_parameters),'hard_parameter_contexts_excluding_function_scaling_with_orientation':2*len(hard_contexts),'hard_canonical_oriented_unit_directions':2*len(hard_dirs),'easy_trig_eligible_axis_parameter_contexts_with_orientation':64,'easy_trig_eligible_nonaxis_parameter_contexts_with_orientation':nonaxis_contexts,'easy_trig_canonical_oriented_directions':len(trig_dirs),'easy_trig_axis_canonical_oriented_directions':2,'definition':'Canonical counts exclude every common positive gradient magnitude and all bank/notation aliases. Context counts retain function/point arithmetic data, are separate, and are not claimed additional canonical directions. Hard retains the explicit unit-normalization demand.'}
(ROOT/'variety.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
