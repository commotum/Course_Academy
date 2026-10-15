# Template extraction

The backbone is a real definite integral of a power/radical of one polynomial, with its derivative supplied as a multiplicative factor. A single substitution changes both integrand and bounds. Every worked solution has the same four operative stages: change variable and differential; table with corresponding original/transformed endpoints; equality of original/transformed integrals; integrate a power in u and evaluate upper minus lower, retaining the signed multiplier.

`SPECS` records every original explicitly: degree n, exact exponent r, original difficulty/field, then a,b,c,l,h. `source-cases.json` contains only the thirteen MA originals. `source-replay.json` preserves original prompt/solution strings, all answer fields, all math answer objects, source answer identities and correct designation, without inventing missing data. Source db entity IDs are retained in frozen `source.json`; replay uses application transport representations.

| Source | n,r | a,b,c | original l,h | bank |
|---|---|---|---|---|
| q-49527 | 1,1/2 | 2,-1,1 | 1,2 | five choices, missing designation |
| q-49610 | 1,2 | 2,1,1 | 1,2 | five choices |
| q-17103 | 3,3/2 | 1,1,3 | 0,2 | five choices |
| q-17104 | 3,3/2 | -1,2,1 | 0,1 | five choices; negative multiplier/reversed u bounds |
| q-318994 | 3,3 | 1,5,6 | 0,1 | blank |
| q-336603 | 1,1/2 | 10,7,1 | -7/10,-1/5 | blank; zero lower radicand |
| q-336612 | 4,2 | 1,1,8 | 0,1 | blank |
| q-336783 | 1,2 | 9,2,1 | 0,1/3 | blank |
| q-336788 | 1,3 | 4,2,1 | 0,1/2 | blank |
| q-336803 | 2,3/2 | 1,1,2 | 0,sqrt(3) | blank |
| q-336804 | 2,1/2 | 1,1,2 | 0,2sqrt(2) | blank |
| q-49613 | 1,3/2 | 5,-6,1 | 2,3 | five choices |
| q-49622 | 1,1/2 | 8,1,1 | 0,1/4 | five choices |

The structural n,r and response contract remain fixed to keep the same substitution and comparable workload. This is a conservative source-family decision, not a claim that the entire KP only permits these exponents. For linear source forms the external factor c stays1 because introducing an extra amplitude would change their supplied expression structure. Nonlinear a,b,c,l,h vary together; a stays negative in q-17104 to preserve the instructive reversed-bound branch.

Normal linear slots: a=2..10; b=-6..7; transformed lower bound L=0..4 and H=L+1..5 (integer-power forms additionally sample L=-3..3); actual original endpoints derive as (L-b)/a and (H-b)/a. Normal nonlinear slots: a in{1,2}, b in1..5, c in{1,n,2n}, l in{0,1/2}, h in{1,2} (degree4 h=1, degree2 h in{1,sqrt3,2sqrt2}). Decreasing cubic family uses a=-1,b=2..5,h=1,c in{1,3,6}. Complete-bank collisions reject the whole instance. Explicit parameter API accepts nonzero builtin integer a,c and integer b with absolute value<=12, real constant endpoints in[-12,12], l<h, and the same branch restrictions. Every dependent substitution, factor, bound, primitive, endpoint component and answer derives from the one instance.

Radical inner expressions must be nonnegative on the full closed interval, including a polynomial stationary point at0 where relevant. There are no reciprocal/log primitives or poles in these source families. No absolute-value logarithm is removed because none occurs. Normal hard sampling uses nonnegative x intervals; easy original x endpoints may be negative. Zero radicands and decreasing transformed limits remain supported.

For source replay define k=c/(an), L=a*l^n+b,H=a*h^n+b,A=k*H^(r+1)/(r+1),B=k*L^(r+1)/(r+1),T=A-B. `recipes` is an executable list of complete source-bank recipes in original order. `recipe-audit.json` records every original value, its full parameterized recipe, evaluated expression, designation and profile.

q-49527 bank: [2A-2B,3A-B,A-3B,A-B,2A-3B]. q-17104 bank: [-k/(r+1)*(L^r-H^(r+1)),T,-T,-k/(r+1)*(L^(r+1)+H^(r+1)),3T]. q-49622 bank: [2T,T,A,6(A+B),(sqrt(2H+L)-sqrt(L))/2]. The final q-49622 expression is observed, with misconception interpretation unresolved.

The numeric banks q-49610,q-17103,q-49613 do not support a confident misconception interpretation for every choice. Each retains an explicit observed affine endpoint-difference pattern: `T+d_i*(H-L)/(H0-L0)`, where d_i is the exact frozen difference between source option i and source T. These are exact complete parameterized recipes, not a pooled fallback list; their interpretation is unresolved and their use is restricted to source replay/review. They are not presented as inferred mathematical mistakes.

Normal radio sampling uses a separately authored complete bank: [T,-T,T/k,A+B,A]. If k=1 an explicit second complete profile is [T,-T,A+B,A,B]. These represent reversed subtraction, omitted differential multiplier, added endpoints and omitted endpoint. Every profile is selected before construction; collisions reject the instance, including L=0 where A=T. Blanks have one exact answer fragment and no distractors. Authored banks are marked separately from observed source profiles.
