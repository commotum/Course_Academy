# Extraction

## 1. Specific source descriptions

`recipe-ledger.json` is the complete per-source component inventory: original prompt and worked text, exact number forms, field layouts, correct designations, complete choice banks, source parameters and ordered operative stages. It contains all 14 practice sources, without collapsing field-layout differences. Easy has original (a,b) values (1,2), (1,1), (1,1), (3,2), and denominators 4 and 2. Moderate uses endpoints 0 to pi/4 or pi/3, coefficient 2 or 3, or frequency2 with upper pi/6. Hard uses (a,k)=(8,5),(3,2),(9,3) with signed or nonzero lower endpoints. Every trig argument, numerator, denominator, integrand, primitive and endpoint is a dependent component.

## 2. Shared patterns and purpose

**tan-sum**: tan(x)(a sec(x)+b cos(x)); distribute → quotient identity → cancellation → split integrals → sec(x)-cos(x) primitives.

**cot-square**: 1/cos²(x) · (a cot²(x)+b cos²(x)sin(x)); distribute → replace cot² by quotient → cancel → reciprocal-square identity → split → primitives.

**cot-sin**: cot(x)sin(x)/n; quotient identity → cancellation → pull out 1/n → sin primitive.

**tan-cos**: tan(x)cos(x)/n; quotient identity → cancellation → pull out 1/n → negative cosine primitive.

**cot-difference**: cot(x)(a sin(x)-b tan(x)); distribute → both quotient identities → cancel to a cos(x)-b → sin-minus-linear primitive.

**cot-csc**: cot(x)(a sin(x)-b csc(x)); distribute → cot quotient → cancel first term → split → negative csc primitive with explicit double negative → collect.

**cos-tan**: cos(x)tan(x), definite; tangent quotient → cancellation to sine → primitive bar → ordered signed endpoint substitution → exact arithmetic.

**scaled-cos-tan**: cos(kx)tan(kx), definite; tangent quotient → cancellation → u=kx/dx=du/k → limits table → transformed integral → factor 1/k → primitive bar → endpoints → arithmetic.

**reciprocal-sec**: (a-b tan(x))/sec(x), definite; reciprocal-secant and tangent identities → distribute/cancel to a cos(x)-b sin(x) → primitive bar → both endpoints → arithmetic.

**sec-difference**: a sec(kx)(tan(kx)-b cos²(kx)), definite; distribute/sec reciprocal → cancellation → u=kx/dx=du/k → limits table → transformed integral → factor a/k → primitive bar → both endpoints → arithmetic.

**sec-cos-square**: a sec(kx)cos²(kx), definite; sec reciprocal → cancellation → u=kx/dx=du/k → limits table → transformed integral → factor a/k → sine primitive bar → both endpoints → arithmetic.

**reciprocal-cos-square**: a/cos²(kx), definite; reciprocal factor square → sec² identity → pull out a → u=kx/dx=du/k → limits table → transformed integral → factor a/k → tangent primitive bar → both endpoints → arithmetic.

## 3. Components and complete banks

The ledger assigns every source option to a single parameterized expression recipe and complete profile. Blank profiles have exactly their one expected scalar; no distractors are added. Radio profiles have source choice counts 4 or5. At original parameters every option matches exactly one generated option, with the correct designation preserved. Banks are selected as whole profiles before parameter sampling; collision rejects the entire instance. No pooled-bank or first-valid filtering exists. For indefinite banks equivalence is derivative equality on original connected domain components, so constant offsets cannot masquerade as distractors. Recipe signs, missing factors, primitive functions, and altered endpoint arithmetic are preserved as expressions; unsupported psychological labels are not invented.

## 4. Stable backbones and declared slots

Within easy source masks independently vary present coefficients a,b over builtin integers1..5; one-term denominators n over2..9. Denominator1 is excluded because its omit-factor recipe duplicates the correct primitive. This role constraint does not discard an observed original. No frequency is added at easy. All implied original1 coefficients remain valid slot values. Moderate unscaled cos-tan holds k=1; the explicitly substituted cos-tan mask has k2..6. Reciprocal-sec independently varies a,b1..5. Hard outer coefficient a1..9, present inner coefficient b1..5, frequency k2..6. Positive integer coefficients keep the source's elementary arithmetic workload and source signs; they need not retain source coincidences such as a=k². These are conservative authored bounds, not inferred observed ranges.

All definite masks independently select two ordered transformed angle slots L,H from {-pi/3,-pi/4,-pi/6,0,pi/6,pi/4,pi/3}. Actual x limits are L/k,H/k. This keeps both endpoints in a single open original cos pole component, with standard exact trig values and the same signed two-endpoint reasoning. k, outer coefficient, inner coefficient and limits vary independently. Different endpoint signs do not create a new solution branch or a within-level progression. Profiles with ambiguous source-bank continuations reject the complete parameter instance; originals and natural zero endpoints remain available.

Fixed components are mathematically justified: each family's trig product factors, subtraction/addition structure, primitive pair, answer contract and ordered method define the assessed skill; x remains the integration variable and u the substitution variable. Original poles/removable holes follow the printed factors, even after cancellation: cot-sin excludes sin(x)=0; tan-cos and tan-sum exclude cos(x)=0; cot-square and cot-difference exclude both sin(x)=0 and cos(x)=0; cot-csc excludes sin(x)=0. Definite sec/tan factors exclude cos(kx)=0, including reciprocal-sec's removable holes. Sampling never integrates across a hole. No additional operator, target skill or stages are added for variety.

Every generated prompt, bank, prose substitution, differential, table, formal integral operand, primitive bar and signed endpoint stage derives from one parameter object. `generate` and `batch` enforce exact builtin integer inputs; booleans and loose numerics are rejected. Content IDs include complete profile values; task IDs ignore option identities but retain difficulty, printed mathematical task and domain. Deduplication is batch-local and originals are eligible in normal sampling.
