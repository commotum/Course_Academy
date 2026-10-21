# Four extraction stages

## 1. Specific records

All original prompts, fields, full banks and supplied solutions are retained with their missing keys in source.json. Source-cases.json assigns all seven recipes their original physical parameters. Masks.json records every original prompt mask and all five supplied full worked-solution masks. The source contexts and mathematical roles are unchanged: Q is kilograms; t is minutes; volume is litres; incoming concentration is kilograms/litre; both volume rates are litres/minute. Incoming rates differ from outgoing rates in every question.

q-336439 has 300 L, 6 kg, .03 kg/L, 24 L/min in, 36 L/min out; supplied powers 1 and 3 and denominator 25; asks coefficient sum. q-336738 has 600 L, 5 kg, .04 kg/L, 15 in, 10 out, evaluation time 10. q-336743 has 420 L, 10 kg, .05, 18 in, 12 out, time 15. q-339394 has 400 L, 4 kg, .03, 20 in, 30 out; powers 1 and 3, denominator 40; asks difference. q-339396 has 240 L, 7 kg, .05, 24 in, 32 out; powers 1 and 4, denominator 30; asks difference. q-339399 has 400 L, 6 kg, .05, 16 in, 12 out, time 12. q-339400 has 500 L, 8 kg, .06, 10 in, 5 out, time 8.

All amount banks display two decimal places and kilograms; coefficient banks display bare scalar fragments. Source omission and source number spelling are preserved independently of local regenerated UUIDs and source metadata. Original radio fields have no prompt placeholders and require none.

## 2. General mathematical pattern

Let delta=rin-rout, B=V0/|delta|, s=sign(delta), m=rout/|delta|, x=B+s*t and J=c*rin. On x>0,

- volume V0+delta*t;
- concentration Q/(V0+delta*t);
- outgoing mass rate rout*Q/(V0+delta*t);
- Q'+m*Q/x=J;
- integrating factor x^(s*m), with derivative m*x^(s*m-1);
- primitive J*x^(s*m+1)/(s*(s*m+1));
- particular coefficient a=J/(m+s);
- alpha=a*B, beta=Q0-alpha;
- integration constant C=beta*B^(s*m);
- Q(t)=a*x+beta*(B/x)^(s*m).

A draining model has alpha*(1-t/B)+beta*(1-t/B)^m. The supplied coefficient sum is simply Q0; the coefficient difference is 2*alpha-Q0. Filling amount questions evaluate Q(T) and round only the final amount. Bounds and strict before-emptying guards apply to explicit and sampled parameters. No capacity is supplied and no overflow event is assessed.

## 3. Complete bank mapping

The classification table and masks.json bank arrays map every one of the 35 original values, its exact suffix and supplied correct flag to its owned field. Historical scalar banks have no evidenced wrong-operation derivation. Each public `observed:<source-id>` profile uses the exact dimensionless ratio (original displayed value)/(original displayed target), multiplied by the new displayed target and rendered in the original value/units style. This is a parameterized quantity-scale evidence replay, **not** a recovered error algorithm. It is ineligible for learning, has no inferred distractor diagnosis and preserves absence of original keys. It reproduces the entire original bank exactly and remains callable through generate and CLI. Supplied source keys match 5/5; the other 2 are absent, not matched keys.

Authored defaults use complete five-option banks, computed together:

| Family | Complete bank operations (first mathematical entry correct; positions shuffled) |
|---|---|
| supplied coefficient sum | Q0; alpha only; -beta (reverse sign and omit alpha); alpha-beta (subtract instead of add); alpha+Q0 (use initial amount as beta) |
| solved coefficient difference | alpha-beta; alpha+beta=Q0 (add instead of subtract); alpha only (omit beta); alpha+Q0 (substitute initial amount for -beta); 2*alpha (omit Q0 in 2*alpha-Q0) |
| rounded filling amount | full variable-volume solution; incorrectly freeze volume V0 in the ODE and solve; omit the transient/initial-condition term c*V(T); omit incoming mass q0*(V0/V(T))^m; use m+1 instead of m on the transient factor |

Each bank is rejected as a whole for collisions, nonpositive physical answers, noninteger coefficient answers, or a numerical-length cue. All amount options have identical two-decimal/units formatting; coefficient options have the same positive integer digit length. No random perturbation of a correct answer creates an authored distractor. Profiles are selected before sampling. Sampling covers every source-shaped eligible family, including both observed moderate powers and all three hard powers plus the early unrated amount context.

## 4. Reusable masks and bounds

Original numeric slots are occurrence-specific and grouped by stage: prompt physical inputs; incoming unit/cancellation/product; outgoing volume/rate/cancellation/simplification; ODE; log/integrating-factor sequence; distributed product derivative; primitive; general solution; each initial-condition substitution and collection row; integration constant; final amount/coefficient expression; endpoint substitution, evaluated terms, rounding; final prose evaluation time. Fixed source powers stay family-specific, including all omitted exponent-1 rows. Runtime substitution only touches explicit slots, never a blanket replacement of a short number/variable.

Normal solutions share source four-step instructional structure and include all actual multiplication, unit cancellation, formal derivative, primitive and IC stages. Normal source-context prompt masks remain parameterized. The easy authored solution explicitly substitutes t=0 into the supplied model and identifies the initial mass.

The family powers are preserved (draining m=3 or 4; filling m=1,2,3), with normalized integer B in 15..200, V0 in 100..1200 L, initial mass in 1..50 kg, concentration .01..08 kg/L, positive unequal rates 4..60 L/min, negative nonzero initial transient, and integer evaluation times 1..30 min. Default arithmetic chooses delta in {4,5,6,8,10,12}, B in {25,30,40,50,60,70,80,90,100}, q0 in 3..44 for easy and 3..25 for moderate/hard, concentration in .02..08 by .01, and times 3..25, subject to those bounds and complete-bank eligibility. Normal explicit inputs also require integer volumes, masses and rates, and concentrations in hundredth steps; opaque evidence scaling may retain fractional quantities. These are authored unordered variation bounds, anchored to the familiar integer ratios, volumes and decimal concentrations of the sources; no fractional exponent/logarithmic special branch is introduced.

Mathematical fingerprints omit banks and context labels. Easy fingerprints include only the assessed initial amount: changing unused volume/rates/powers does not count as a new task. Moderate/hard fingerprints use actual physical inputs and hard evaluation time. Full content identities include actual prompt, fixed solution, complete displayed bank and actual difficulty; seed/option order cannot change identity.

Plot extraction/spec: none; there are no source plots, so no renderer or image assets are needed. Work freezes at step 7.

Easy has a finite meaningful numeric domain under the same-length bank rule: initial masses 3, 4 and 10..44 (37 possible tasks); concentration/rates/volume variation is presentation only for its supplied-model sum and never inflates that count. The larger easy initial-mass bound changes no operation: the learner still substitutes zero and identifies Q(0).
