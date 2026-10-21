# Instructional account

The assessed operation is to inspect the coefficient and signed constant in an affine exponent, invert the exponential with a natural logarithm, and isolate the requested real variable. Choose the sign cases before numerical parameters. Numerical answers alone are not the coverage claim.

## Evidence and classification

The lesson Introduction (tutorial 2806, `0f1cb099-7970-59ba-ad74-7052da9f2872`) says to take the logarithm with the exponential's base, identifies `log_e x = ln x`, and uses `ln(e^a)=a`. It concludes that an exact answer is often given in logarithmic form. The canonical example `5e22ac55-3e84-5cb4-8231-5f882da9240e` takes logs, removes the exponential, then rearranges and applies the power rule to `e^(x-3)=2^5`. The prerequisite examples include inversion (`fd02e00f-9e2c-54f1-a5d3-fb0da9c9a413`) and exact exponential solving (`7c937587-dc81-5ee9-aa66-a509a87433e2`). Power-rule prerequisites support the harder sources but are unnecessary for the supported integer-RHS family. The neighboring approximate and exponential-isolation KPs are outside scope.

All seven supplied practice questions were inspected with complete available fields and solutions. There are no images or mathematical diagrams (plot rating none).

* `1221fa6c-5b40-5986-ab51-d9a88f1c520a` (q-66590): unrated, `e^t=6`, radio, missing correct link and solution. Complete bank: `e^-6`, `ln(e)`, `e^6`, `ln(6)`, `6`. Respectively inverse-sign confusion, constant ln(e), exponentiation, correct inversion, unchanged RHS.
* `ebbad0b2-c71f-5884-ae51-5d0945e65a81` (q-66595): unrated, `e^(2-3x)=10`, radio, missing key and solution. Bank `(2-ln10)`, `(ln10-2)`, `6-3ln10`, `(ln10-2)/3`, `(2-ln10)/3`. Let c=2,d=3,n=10: recipes c-ln(n), ln(n)-c, d(c-ln(n)), (ln(n)-c)/d, (c-ln(n))/d. Correct is last; key is inferred only for analysis.
* `f297140b-f9f4-5397-9403-cc5c9d6b1ffc` (q-100282): easy, `e^t=11`, worked solution, no answer field. Invert once; exact ln(11).
* `92f78b35-314c-56cd-8815-b47ddfe81b49` (q-66963): hard, `e^(2x+3)=root_5(7)`, worked solution, no answer field. Root-to-power, power rule, affine rearrangement.
* `06bb1232-0a8a-5e1c-9d8b-cb06e8535b98` (q-100280): hard radio, `e^(7-y)=root_7(10)`. Five complete equation choices: y=7-ln(7)/10, y=10+ln(10)/7, y=7-ln(10)/7 (key), y=1-ln(7)/10, y=1+ln(10)/7. With offset c, root index d, radicand n, observed recipes are c-ln(d)/n, n+ln(n)/d, c-ln(n)/d, 1-ln(d)/n, 1+ln(n)/d. Interpretation of constants 1 is unresolved, retained as observation.
* `d0fb4c30-2477-5421-b3da-f8a97304168e` (q-100276): hard radio, `e^(5-y)=root_4(7)`. Bank y=3-ln(7)/14, y=5+ln(4)/7, y=5-ln(7)/4 (key), y=5-ln(2)/4, y=5+ln(7)/2. Different profile from previous bank. Only literal source values are established for the first and last recipes; no unsupported inferred generalization is served.
* `ba9070de-c707-5661-a14c-cac1b4371745` (q-263058): moderate blank, `e^(4-5y)=21`, one field `field-1`, complete bank containing just `(4-ln21)/5`, key linked correctly. Stages: logs of both sides; inverse identity; subtract 4; divide by -5; collect exact rational and log terms. This is the implemented family and replay source.

No mathematical error was found in supplied keyed source questions. Capture notation includes invisible U+2061 and operatorname ln, normalized by the shared math formatter. Missing source metadata is not silently filled into the unsupported bands. Original source labels remain in the replay fixture.

## Contract, fixed structure and eligible variations

Default and supported band: **moderate**. Easy and hard are explicitly unsupported by this package: their separate response contracts and banks are not implemented. Unrated records are observations rather than a difficulty assignment. Replay fidelity claims apply to the complete supported moderate source (1/1 banks, no distractors); the remaining source families are excluded, not claimed as replayed.

One blank math field expects the RHS expression for the displayed `v=`. It has exactly one canonical answer and no distractors, as in q-263058. There is one real solution because e is injective, the RHS is positive, and the variable coefficient is nonzero. No numerical approximations, changing exponential bases, roots, additional exponential isolation, or new response formats are added.

The backbone is `e^(a*v+b)=n`. Exponential base e is fixed to assess natural logarithm inversion. An integer RHS n in 2..30 keeps the exact ln answer and source arithmetic workload, avoids ln(1) collapsing the assessed operation, and keeps positivity explicit. |a| in 2..7 preserves the nontrivial division stage in the moderate source. |b| in 1..9 preserves the nontrivial translation stage. These bounds are conservative extensions, not observed bounds. Both signs of a and b are eligible: neither source sign is essential to the logarithm inversion or linear rearrangement method. A positive a and negative b are also grounded in the canonical example's affine exponent, though coefficient magnitude >1 is retained for moderate workload. Zero coefficients and constants are excluded for those instructional reasons, not rejected after sampling.

Answer-bearing roles are the signed coefficient a (division direction), signed offset b (translation direction), and RHS n (argument of ln). The solution is `(ln(n)-b)/a`. Choose the (sign(a),sign(b)) decision case first; sample compatible magnitudes and n next. Obligations: all four sign cases, both exponent orders (constant-first or variable-first), both signs of the solution where feasible, and boundary magnitudes/RHS. Ordering is a presentation slot and must not predict a sign case. Variable x/y/t is an irrelevant name slot; renaming must preserve the numeric answer. Source's constant-first order is reproduced at replay. Changing n, a, or b must change the numeric solution and corresponding worked steps; compare controlled cases with all other parameters fixed. No qualifying labels, choice positions, or selection counts exist in a blank family; fixed field count is the source response contract.

Normal sampling uses all permitted slots with no correctness rejection; finite in-call semantic deduplication ignores order and variable renaming. There are 6*2*9*2*29=6264 semantic triples. Requests beyond that finite family fail explicitly. Labels and layouts do not count as new semantics. Seeded sampling is reproducible and creates no files or assets.

Every generated solution preserves the source verbal stages and concrete affine steps. Replay returns the normalized original source wording and entire answer bank. Normal solutions use the same method; signs, intermediate equations, prompt variable, exact key, and explanation are derived from one instance. Native grading checks must include equivalent fractions and distributed forms, plausible sign and omitted-division mistakes, and controlled changed-evidence responses.


## Validation outcome and grader limitation

Source replay matches the moderate prompt, solution and entire one-answer bank after shared notation normalization. Independent substitution checks passed on 166 records, including 64 boundary presentations, all 29 RHS slots, a seeded 64-item normal sample, and seven controlled changes. Label/order changes preserve the response; coefficient, offset and RHS changes alter it. Delivery filtering accepted 163/166 records (three duplicates), retaining 129 distinct numeric triples, all four sign cases within each order and variable/order subgroup. Simple copy-RHS, log-only, omitted-division and reversed-translation probes never succeed; ignoring the coefficient sign succeeds only when its sign is actually positive, which is relevant evidence rather than an incidental cue.

The actual native grader accepts all 498 canonical/grouped/distributed correct submissions and both irrelevant-change preservation checks. It rejects 261 wrong submissions and returns 77 explicitly unresolved outcomes for other incorrect expressions. Inspection of `engine/rust/symbolic.rs::log_bounds` explains the latter: its interval proof declines n >=20 because |(n-1)/(n+1)| exceeds 9/10; algebraically cancelling logs still permit rejection. This includes the original n=21 source case. No wrong response was accepted. The unresolved outcomes are a native grader limitation, not claimed as rejection; no generator-side replacement grader is supplied. Five real UI screenshots, including source replay, sign counterfactuals and a positive-coefficient boundary, were visually inspected: no clipped equations, exposed TeX, missing content or mismatch between key and solution was observed.

Learner selection is inspected read-only: the existing Rust selector chooses a rated difficulty pool then a hash-seeded uniform index within it. A positive moderate weight does not prefer one sign/layout. Live history and configured weights were unavailable; coverage is conditional on the captured inventory and eligibility, not a claim about any individual learner's future sequence.

## Repair attempt 2: strict grading requirement (before edits)

Feedback requires ordinary wrong submissions to produce `rejected`, including at
source q-263058 (`ba9070de-c707-5661-a14c-cac1b4371745`, RHS 21), not an unresolved
native error. Tutorial 2806's instruction to take natural logarithms and present an
exact logarithmic answer, together with this source's single math blank, remains
the instructional contract. The learner still inspects signed affine coefficients,
inverts with ln, translates, and divides. Moderate workload and permitted sign,
coefficient, offset, RHS, variable, and order slots remain as specified above.
No random parameters or answer-bearing assignments will be changed to evade the
reported defect. The four sign cases and relevant/irrelevant counterfactuals remain
coverage obligations. No new instructional family is justified by this repair.

The earlier native-check script expected unresolved results for some wrong answers;
that is diagnostic evidence, not a passing delivery requirement. Repair that script
to require rejection and add a focused all-RHS/native regression that separates
observed outcomes from required outcomes. Preserve the working runtime and replay.
Native `learning::grade_field` invokes `symbolic::compare` for this blank, with no
record-level custom-comparator hook. The native log interval routine refuses
arguments above 19. These files are outside the supplied workspace and cannot be
edited in this job. Restricting RHS to 19 would exclude the source value 21;
changing math blanks to text or forcing a particular answer spelling would reject
valid equivalents. Neither is a defensible repair. If focused checks reproduce the
failure, report unsupported and retain the package for a future engine repair.

Repair-2 outcome: **unsupported**. `repair_validate.py --repo REPO --source SOURCE`
returned 1 after reproducing the original source failure. Shared delivery accepted
46 of 48 records (two duplicates), retaining 44 semantic triples and all four sign
cases. Source replay plus delivered records yielded 143 accepted valid responses,
130 rejected incorrect responses, and 64 incorrect responses that errored. These
errors are failures. Required outcomes and observed outcomes are stored separately
in `evidence/repair-2/native-required.json`, `native-diagnostic-report.json`, and
`result.json`. Exact commands and the strict source error are in `commands.json`.
Supported normalized source fidelity and independent numeric checks pass; native
grading and counterfactual rejection do not. Earlier rendering and packaging
findings remain applicable because runtime bytes are unchanged. No publication or
database action occurred. The scoped native fix remains outside this workspace.
