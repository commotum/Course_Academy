# Extracted templates and independent inventory

Raw public `generate(level, template=sid, profile='observed_raw')` returns the **entire original question map unchanged**: prompt, solution, complete answer bank, fields, correct designation, enum maps, identities, any feedback/other attributes, and absent attributes. `source-cases.json` contains the ten MA originals only. Five no-MA inventory records are retained separately in `independent-inventory-replay.json`. Raw malformed/incomplete/unrated evidence is ineligible for normal delivery.

For the five eligible source families, original parameters replay the normalized source prompt, choice values, shared wording and all ordered worked stages. q-1900 receives only the documented dependent-variable/radian label corrections. Changed values render the same instructional sequence from a single instance. Normal fields use bare TeX math, field-owned answer UUIDs and correct lookup references. No feedback is invented.

| Template | Input / requested object | Slots, original values | Complete bank recipes, original order | Stages |
|---|---|---|---|---|
| q-1847 | a cos(x)+b sin(x); derivative operator, radio | a=4,b=2; independently 1..6, a!=b | input; b cos+a sin; **b cos-a sin**; -input; a cos-b sin | Recall trig formulas; a(-sin)+b cos; collect |
| q-30991 | a(x^n-cos(x))+5; dy/dx, radio | a=6,n=2; a=2..6,n=2,3,4 | **an x^(n-1)+a sin**; a x^(n-1)+a sin; an x^(n-1)-a sin; an x^(n-1)-sin; an x^(n-1)+sin | Formal derivative of factored input; a n x^(n-1)+a sin+0; collect |
| q-341383 | (a/4)sin(x)+(b/4)x^n; RHS dy/dx blank | a=5,b=1,n=4; a,b=1..6,n=2,3,4 | **(a/4)cos+(bn/4)x^(n-1)**, no distractors | Formal derivative; (a/4)cos+(b/4)(n x^(n-1)); collect |
| q-47985 | -a cos(x)+b x^-n; derivative, radio | a=2,b=1,n=2; a,b=1..6,n=1,2,3 | a sin-bn x^(-n+1); -a sin-bn x^(-n-1); **a sin-bn x^(-n-1)**; -a sin+bn x^(-n-1); -a sin-bn x^-n | Formal derivative; -a(-sin)+(-bn)x^(-n-1); collect |
| q-1900 | k(2x-5 cos(x)), tangent slope at pi/6, radio | k=1; positive integer 1..12 | 11k/2;21k/5;-21k/6;**9k/2**;9k/4 | Derivative input; 2k-5k(-sin); collect; substitute; sin(pi/6)=1/2; add fraction; simplify slope |

Source-bank recipes are complete profiles, never pooled. q-1900's error interpretation is unresolved: its full observed scalar pattern is transported homogeneously, with the supplied function and all intermediate values scaling together. This does not infer offsets or fabricate additional banks. Signs/exponents/omitted multipliers in the other source banks are parameterized exactly as shown. Every source distractor is accounted for and every source bank is replayed publicly before extensions.

The power and coefficient ranges are conservative authored slot extensions of the same direct-rule workload; original exponent locations remain positive or negative by family. All trig arguments are exactly x in radians. Constants such as q-30991's +5 stay fixed and never increase meaningful task counts. a=1 in q-30991 and a=b in q-1847 are rejected because complete banks duplicate. Every normal profile constructs its entire bank before validation.

The separately labeled **independently authored inventory** families use blanks:

- Easy: a sin(x)+b x^n or a cos(x)+b x^n, a,b in {-6,-3,-1,1,3,6}, n in {2,3,4}. Relationship to source templates: q-341383's trig-plus-power direct derivative, with integral signed coefficients. Two terms in every item.
- Moderate: a sin(x)+b x or a cos(x)+b x, the same six signed coefficients; familiar points {0,pi/6,pi/3,pi/2,pi,3pi/2}. Relationship to source templates: q-1900's direct derivative plus one special-angle slope evaluation. Exclude points where the trig derivative is zero so its amplitude is not an unqueried slot. Exact trig substitution, signed contribution and sum are shown from the same instance. Two terms in every item.
- Hard: a cos(x)+b sin(x)+c x^n+d x^-m, a,b in {-6,-1,1,6}, c,d in {-3,-1,1,3}, n in {2,3,4}, m in {1,2,3}. Relationship to source templates: canonical e-3631's two trig terms and monomial, plus q-47985's negative power. Four direct derivative terms in every item; no chain/product/quotient or downstream rule.

Domains: x is real, with x!=0 for negative powers. All sine/cosine arguments and evaluated points are radians; derivative outputs are complete RHS expressions or slopes. Coefficients, signs, powers, derivative operator inputs, equation fragments, intermediate derivatives, special-angle values and final answers all derive from one instance. No label or option shuffle is used as novelty. A fingerprint uses the canonical derivative and requested point; batch output deduplicates across family aliases, constants, seeds and presentation IDs.
