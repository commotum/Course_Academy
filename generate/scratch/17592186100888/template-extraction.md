# Template extraction

## 1. Describe each source specifically

The exact prompts, complete banks, fields, and worked solutions remain in `source.json`; extracted mathematical components and prose masks are in `masks.json`. In source order:

- q-140631: y'=4y/x, x≠0; f=x⁴; asserted 5x⁵; derivative 4x³; three derivative rows and three substitution rows. Statement I false, II/III true. Both derivative parentheses and punctuation differ from the other power source.
- q-141078: y'=2y; f=e²ˣ; asserted 2e²ˣ. Two derivative rows and only two substitution rows. All statements true; no redundant substituted ky row is inserted.
- q-141080: y'=2y; f=(1/2)sin2x; asserted 2cos2x. Four derivative rows retain (1/2)·2cos2x before cos2x. Three substitution rows compare cos2x with sin2x. None true.
- q-141081: y'=y cos2x; f=cos2x; asserted −2sin2x. Two derivative rows and three substitution rows. I true, II/III false. The final source cosine notation `{cos}^{2}` is preserved, with no claimed TeX repair.
- q-141082: y'=1/eʸ; f=lnx; asserted 1/x. Two derivative rows and three substitution rows; all true. Proposed-function domain is x>0 even though no explicit restriction is printed.
- q-141084: y'=y/x², x≠0; f=−1/x²; asserted −2/x³. Three derivative rows and three substitution rows, ending 2/x³≠−1/x⁴. None true.
- q-141086: y'=−3y; f=3e⁻ˣ; asserted 3e⁻ˣ. Three derivative rows and three substitution rows; none true. Derivative is −3e⁻ˣ and substituted RHS −9e⁻ˣ.
- q-141088: y'=4x/e^(y/2); f=4lnx; asserted 1/(4x). Three derivative rows and six substitution rows retain divided exponent, 2lnx, ln(x²), x² denominator, final4/x. I false, II/III true. Function domain x>0.
- q-141089: y'=2y/x, x≠0; f=−3x²; asserted −5x. Four derivative rows retain −3·2x, then −6x and the inequality. Three substitution rows; I false, II/III true.

## 2. Shared mathematical pattern and purpose

Compute the actual f′, evaluate the asserted derivative, substitute y=f and y′=f′ into the *printed* first-order ODE, and use equality as functions on the proposed function's real domain to decide II and III together. Selecting a statement combination is the response; the learner never finds an unknown solution. Raw prose and all ordered mathematical rows stay fixed per recovered layout. Normal output changes only the common overly broad domain sentence and gives the logarithmic interval explicitly.

## 3. Map every component and every option

`masks.json` records whole-expression components at the source parameters: F proposed function, D actual derivative, C asserted wrong derivative, R ODE RHS, S explicit substituted RHS, E simplified RHS, P unevaluated derivative product, H/J/K successive exponential/log stages. The extraction is longest-first, single-pass, complete-component substitution: slot insertion cannot replace a letter in unrelated prose or CAS notation. `extract.py` is the reproducible evidence extraction, separate from generation.

Each of the five choices in each profile is stored in `masks.json` in its original observed order and also in `source.json` with original UUIDs and correct designation. A categorical choice represents the subset named by its text: None={}, I only={I}, II only={II}, III only={III}, I and II only={I,II}, I and III only={I,III}, II and III only={II,III}, and I, II, and III={I,II,III}. The correct subset is computed from independent mathematical truth values. A wrong option is a different subset, including intentionally inconsistent II-only/III-only combinations. Those logical subsets are the complete reusable recipes; there is no scalar fitting or assumed historical diagnosis. Source fields all have text answer types and radio field types. All 45 choices and nine correct designations are compared one-to-one, ignoring order.

The moderate −5x assertion admits many historical explanations. The parameterized continuation uses (a−n)x^(n−1), equivalently adding the signed magnitudes instead of multiplying a and n when a<0. This is a defensible authored error operation reproducing the observed expression; its historical intent is **not recovered**. The extraction records the source value, and the README/validation limitation distinguishes this interpretation from observed bank fidelity.

## 4. Reusable masks, calculations, constraints

The generator fills masks with exact computed components, including explicit product and exponential simplification stages. It never branches to return raw source payloads. `source-cases.json` calls the public `generate` API with parameters and original complete raw evidence profile for every source. Raw profiles are named `raw_<source-id>_bank`; normal observed profiles omit the `raw_` prefix and retain exactly the same categorical banks. Sampled and explicit parameters share guards:

| Template | Bounds | Fixed reasoning demand |
|---|---|---|
| power_easy | n=2..5 | one power derivative; asserted exponent and coefficient each increased by1 |
| exp_true | k=1..4 | one exponential chain derivative |
| sin_none | k=2..4; amplitude1/k | reciprocal times inner derivative, nonidentical claimed derivative |
| cos_i | k=1..4 | cosine chain factor and RHS product |
| log_all | shift h=−4..4 | reciprocal derivative and exp/log cancellation on x+h>0 |
| inverse_none | n=2..5 | negative-power sign and denominator exponent |
| exp_none | a=2..5, k=1..4, b=1..5, b≠k | signed derivative and distinct ODE multiplier |
| log_scaled | m=1..4; outer scale2m | exponent divided bym becomes2lnx; same six substitution rows |
| power_moderate | a=−5..−2,n=2..5,a−n≠an | signed nonunit coefficient product; one extra derivative row |
| affine_log (authored hard) | |a|=2..4,b=2..4,|c|=1..4 | outer scale, affine chain factor, divided-exponent cancellation |

Hard f=a ln(bx+c), on bx+c>0, has claimed derivative either ab/(bx+c) or b/[a(bx+c)]. ODE RHS is either ab exp(−y/a) or −ab exp(−y/a). Its four truth states have the same workload; no instructional progression is introduced. A complete labeled authored bank uses None, I only, II and III only, I/II/III, and II only. The hard solution always displays formal derivative, chain product, reduction, formal ODE, direct substituted exponent, canceled exponent, reduced RHS, and conclusion; inequality rows are conditional on the statement being false.

There are finite meaningful bounds: 96 easy tasks over the observed families, 15 moderate tasks, and 576 authored hard tasks. Aliases, seeds, option permutations, or additional profiles do not inflate those mathematical task counts. Fingerprints canonicalize symbolic f, asserted derivative, ODE RHS, and domain, excluding banks. Presentation identity includes actual prompt, fixed solution, complete bank, and version. Choices are shuffled after correct identity is fixed; fixed parameters/profiles do not change content identity with seed.

No algebraic source errors were found. A teaching-domain wording anomaly is preserved only in explicitly raw evidence profiles: the common source sentence demands every x in the equation domain, even when the proposed logarithm is defined only on a smaller interval. Raw source presentation remains byte-exact (nine prompts and nine complete solutions). Normal solutions replace that phrase with an interval where the function is defined and the equation is valid; normal `log_all`/`log_scaled` prompts explicitly state x+h>0/x>0. Normal hard presentation retains its existing affine restriction. The independent validator separately checks all nine exact raw replays, all nine normal opening repairs, two normal source-parameter logarithmic prompt repairs, and the unchanged mathematical fingerprints and stages. No plot extraction/rendering is needed.


## Current checkbox template, version 1.2.0

Current source templates preserve each mathematical expression and ordered solution row from the historical masks. The three statement bullets gain bold Roman labels and the source sentence “Select all that apply.” Each field I, II, III owns two text answers, false and true. Statement I is the equality f'=asserted derivative; II is f'=R(x,f); III repeats the solution conclusion from II. Thus the two boolean values are the complete current bank for each field, not a pooled categorical distractor selection. The generator recreates all nine source prompts and solutions byte-exact through raw source profiles, and all 27 banks with exact correct values. Raw profiles remain ineligible for learning; normal output retains the documented interval wording repair. Normal IDs depend on the rendered question, solution and truth values; field and answer identities derive from the owning question and field key.

Version 1.2.0 keeps the exact symbolic components, parameter guards and solution masks from the preserved reference/generator-1.1.0.py. It changes the public learner response representation to the current three checkboxes. The old five-choice banks are retained only as historical extraction evidence. Batch generation enforces distinct mathematical fingerprints and reports a finite bound instead of returning repetitions. All fifteen moderate tasks, deterministic replay and the rejection of a requested count of sixteen are validated. The currently deployed engine is rebuilt locally into check-engine for the field-grading tests; no learner state is written by validation.
