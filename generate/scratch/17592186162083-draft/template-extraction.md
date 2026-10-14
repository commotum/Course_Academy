# Four extraction stages

## 1. Specific observed objects

| Source | Given curves and original parameters | Statements in order | Original bank and designation |
|---|---|---|---|
| q-122478 | `(t,t²)`, t∈[0,1]; `(2u,4u²)`, u∈[0,1/2]; integral 2 | reversal =−2; reversal =2; reparametrized =4 | five radio subsets; designation absent |
| q-122571 | `(sin t,cos t)`, t∈[0,2π]; `(sin 2θ,cos 2θ)`, θ∈[0,π]; integral k | reversal =k; reparametrized =k; reparametrized =k/2 | five radio subsets; designation absent |
| q-122814 | `(t⁴−3t²,t)`, t∈[0,2]; `(16u⁴−12u²,2u)`, u∈[0,1]; integral 4 | reversal =−4; reparametrized =8; reversal =4 | three `{false,true}` banks; false,false,true |
| q-122815 | `(cos(u/2),sin(u/2))`, u∈[0,2π]; `(cos t,sin t)`, t∈[0,π]; integral 1 | reparametrized =2; reversal =−1; reversal =1 | three Boolean banks; false,false,true |
| q-122816 | `(t,t^(3/2))`, t∈[0,4]; `(4u,8u^(3/2))`, u∈[0,1]; integral 3 | reversal =3; reversal =−3; reparametrized =12 | three Boolean banks; true,false,false |
| q-122851 | `(sqrt(9t²+1),3t)`, t∈[0,1/3]; `(sqrt(4u²+1),2u)`, u∈[0,1/2]; integral k | reversal =−k; reparametrized =2k/3; reparametrized =k | three Boolean banks; false,false,true |
| q-122868 | `(2t,2sqrt t)`, t∈[0,2]; `(4u,2sqrt(2u))`, u∈[0,1]; integral k | reparametrized =k; reparametrized =2k; reversal =k | three Boolean banks; true,false,true |

The exact prompt, prose, field ownership, bank values and absence information for every original are retained in `source.json`; `bank-mapping.json` enumerates every option and correct-reference presence. All recorded parameter values are public replay cases.

## 2. Shared pattern

Two once-traversed parametrizations have identical normalized coordinate curves over the same interval. The scalar line integral with respect to arc length has the same value for the second parametrization and the reversed orientation. Determine the truth of three given equality statements. The response criterion is a finite subset of statement labels, or one Boolean per label; numerical integral values are not radio answer scalars.

## 3. Components and complete banks

The field/bank profile is chosen before parameters. Each checkbox field always owns the complete bank `{false,true}`; its correct value follows the rendered statement equality. The radio profiles retain their complete five subsets, exactly as captured. Each radio option denotes its full unordered statement subset, so different spellings of equivalent subsets would be collisions. The validator checks every pair, not merely the correct option. These categorical banks have no opaque scalar fits or claimed psychological interpretation.

The displayed incorrect claims are parameterized operations, not random perturbations: orientation sign negation; multiplication by the reparametrization speed; division by angular speed for the full circle; or the ratio of the two linear coordinate speeds for the hyperbola family. The evidence supports those visible expressions, not claims about an individual learner's intent. The full original bank is preserved in both raw replay and normal completed output.

The rated solutions keep the complete original prose and operation order: invariant rule → examine statements → orientation equality and truth labels; reparametrization equality and truth labels; Cartesian conversion (or same circular traversal); conclusion. The two families that introduce reparametrization first retain that ordering. No source arithmetic stage is replaced with generic integration work. Normal completed legacy solutions use this shared prose but are explicitly authored.

## 4. Backbone and slots

| Family | Slots and enforced domain | Dependent objects |
|---|---|---|
| easy parabola | c=1..6, T=1..4, s=2..5, nonzero integer k with absolute k≤9 | `(t,c t²)`, `(s u,c s²u²)`, intervals T and T/s; Cartesian `y=cx²`, 0≤x≤T; claims −k,k,sk |
| full circle (authored moderate completion) | R=1..12, s=2..5 | `(R sin t,R cos t)` and angular speed s, upper 2π/s; claims k,k,k/s; radius and once-traversed full circle |
| quartic moderate | a=1..3, b=1..6, T=2..6, nonzero absolute k≤9 | `(a t⁴−b t²,t)`; speed T on unit interval; Cartesian polynomial and domain; claims −k,Tk,k |
| half-circle moderate | R=1..12, d=2..4, n=1..3, nonzero absolute k≤9 | angular speeds 1/d and n; upper dπ and π/n; radius and half-circle prose; claims dnk,−k,k |
| power moderate | c=1..5, T∈{4,9,16}, nonzero absolute k≤9 | `(t,c t^(3/2))`, speed T; perfect-square endpoint retains familiar exact coefficient cT^(3/2); Cartesian relation; k,−k,Tk |
| hyperbola hard | h=1..9,L=1..5,a,b=2..5,a≠b | `(sqrt(a²t²+h),a t)` and b analogue; upper L/a,L/b; Cartesian `x=sqrt(y²+h)` and domain; −k,(b/a)k,k |
| square-root hard | A,B=2..6,T=2..5,s=2..5 | `(A t,B sqrt t)` and speed s; upper T/s; Cartesian `y=sqrt((B²/A)x)`, 0≤x≤AT; k,sk,k |

Explicit parameters receive the same guards as samplers. Numeric k=0 is excluded because it collapses sign and speed claims. Hard symbolic k may be zero in a particular function, but “must” is universal over real k; a sign or nonunit multiplier is not universally equal. Positive coordinates keep the stated square-root branches. All intervals represent one traversal, never repeated winding. Coefficients and bounds stay small integers/rationals; no new function, branch or solution operation is introduced.

Statement roles and requested curve labels remain fixed within each source template because their pairing determines the original worked-solution discussion and response contract. There is no supported variable target slot; relabeling or permuting statements would be cosmetic. Changing an endpoint, radius or polynomial coefficient changes the supplied curve being recognized. Changing only speed, k, alias or order cannot count as another mathematical task. Fingerprints use the exact normalized printed curve and unordered requested invariance roles; IDs use actual difficulty/prompt/fixed solution/full unordered field-owned banks and correct-presence contracts. Seed and profile names are excluded. Validation independently recomputes the fingerprint from the printed mathematics.

The finite default bank contains 24 easy curves, 129 moderate curves (90 quartic, 12 semicircular, 15 fractional-power, 12 full-circle), and 145 hard curves (45 hyperbola, 100 square-root). The circle bank is structurally narrow; speed changes do not inflate its 12 actual radii. These are deliberate conservative bounded domains, not a claim of unlimited conceptual variety. Every default family is sampled in the 100-seed coverage check.
