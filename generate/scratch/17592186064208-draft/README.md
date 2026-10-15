# KP 17592186064208 draft

This pair replaces no registered artifact. The live numeric script and its complete 55-file evidence/cache tree remain byte-for-byte unchanged. `inventory-job.json` records `latest_inventory.has_generator=true`; the working queue status was not used to infer registration. No database, registration, shared engine, manifest, or git mutation was performed.

Use the repository environment:

```sh
.venv/bin/python -B generate/scratch/17592186064208-draft.py --difficulty all --count 3 --seed 23 --format json
.venv/bin/python -B generate/scratch/17592186064208-draft.py --difficulty all --count 3 --seed 23 --format markdown
.venv/bin/python -B generate/scratch/17592186064208-draft/validate.py
.venv/bin/python -B generate/scratch/17592186064208-draft/supplement.py
```

The level-first Python API is `generate(difficulty, seed, template=None, parameters=None, bank_profile=None)`; wrappers are `generate_easy`, `generate_moderate`, and `generate_hard`. `template` is an alias for an exact bank profile, since all served records share the two-reciprocal mathematical backbone. `sourcecases.json` supplies exact source/profile/parameter mappings. `source_case(source_id)` returns complete raw evidence with an explicit eligibility flag; it does not convert incomplete raw records into served questions. `canonical_reference(parameters)` separately reproduces the canonical example without inventing answer fields.

## Frozen evidence and fidelity

`source.json` is the exact basis-2275 wrapper supplied for this KP, including every raw attribute. Ten practice records are Math Academy records; nine are complete hard radios. `q-49521` has no difficulty, correct reference, or worked solution. Its raw replay is ineligible. `q-49521-completed` is a separately labeled authored completion, assigns hard, keeps the complete five-choice bank, selects the mathematically correct fifth option, and supplies the established four-row solution. The canonical `e-451` has no response fields and remains reference-only. `non-ma-inventory.json` separately records zero non-MA practice records in this supplied snapshot; no broader database claim is made.

All 50 observed answer values and all 10 prompts reproduce after the frozen shared math-format normalization. All nine supplied worked solutions and all nine supplied keys reproduce. `raw-replay.json` retains the original unmodified values and attributes. `contract.json` preserves all nine complete observed bank profiles and maps every choice to its coefficient and product/quotient recipe; the incomplete profile is explicitly completed. `sourcecases.json` includes original plus two mathematically distinct parameter variants for every practice profile. `canonical-sourcecases.json` does the same for the reference-only canonical family.

## Scope and variety

`ordered-context.json` traverses the actual lesson first-step/next chain: Introduction → Integrating a Linear Rational Function → Integrating a Linear Rational Function and Simplifying the Arbitrary Constant → The General Formula → this KP. The explicit prerequisite is Combining the Laws of Logarithms. The scope is applying the known linear-reciprocal integration formula twice, combining logarithms, and expressing the integration constant inside a single logarithm. Substitution derivations, definite integration, extra summands, variable numerators, and new response types are outside this draft.

There are no observed easy or moderate practices. Their two authored bank profiles are labeled extensions rather than source evidence. Every generated item at every band has exactly two unit-numerator linear reciprocal terms, five radio choices, and the same ordered operative stages. Easy uses slopes of magnitude one; moderate uses magnitudes 2–4; hard retains source profiles and supports magnitudes 2–8 plus the unit-slope source profiles. Each band varies signed nonzero shifts within −9…9, relative pole locations, and the product/quotient relation. The shift and scale constraints do not impose an instructional progression within a band. The source's unit-slope profiles remain restricted to their source method and full bank conditions.

`validation.json` records 60 distinct actual mathematical tasks per band, not seed or choice-order changes, with three changed instances for every band/profile. Whole observed bank profiles are chosen before sampling; if any pair has equal derivatives, or a wrong choice differentiates to the task, the complete instance is rejected. No pooled or first-valid distractor selection is used. Content IDs use full normalized rendered content and unordered keyed bank. Mathematical task dedup uses the canonical actual rendered rational integrand, separately from profile, seed, and question IDs.

## Verification and known limits

The private frozen `parser.py` reads actual rendered TeX independently of generator recipes. It reads the prompt integrand, original printed rational denominator poles, all three formal integral operands in the solution's first row, all three subsequent primitive stages, and every answer choice. It verifies derivatives and exact real-log identities. The first primitive's `C` is explicitly replaced by `log(K)/a`; both later stages must equal it exactly, detecting stale constant coefficients that a derivative-only check misses. Rational log arguments are factored into absolute linear factors and positive rational constants. No forced sign erasure or `force=True` is used. The arbitrary positive K is independent on each connected real component of the original pole-free domain. Genuine additive constants and scaled logarithm arguments are checked as valid equivalences and never used as wrong answers.

Five independent mutations fail: wrong prompt integrand, wrong formal operand, stale C-to-K coefficient, erased primitive stage, and wrong intermediate primitive. Source comparison, mathematical correctness, formatting, and actual grading remain separate evidence.

The frozen native binary SHA-256 is `71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea`. Thirteen small batches check 78 banks: 78 owned correct selections accepted and 312 owned wrong-derivative selections rejected. Another 144 foreign/malformed radio submissions return explicit unresolved errors; all inputs and outputs are retained, without pruning or engine edits. Equivalent blank spellings are inapplicable because these source and authored response contracts are radio. Mathematical equivalence probes are reported separately from radio identity grading.

The source-based hard bounds and authored easy/moderate bands are conservative instructional judgments, not captured MA difficulty evidence. This is a local review draft and has not been registered or committed. Registered hashes are checked in `registered-integrity.json`; `frozen-hashes.json` inventories final draft evidence and frozen dependencies. Plot rating is none: no plots or image assets occur in the supplied source, and docs 5/7 do not require generation.
