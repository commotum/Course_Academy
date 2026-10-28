# Group 2 frozen audit handoff — basis 9122

The committable inputs are frozen and hashed in `handoff.json`. No database writes, learner events, publications, or shared production edits were performed by this agent.

- `proposals.json`: **193 content CAS changes** (113 worked solutions, 48 prompts, 24 answer values, seven tutorials, one checkbox display key).
- `key-proposals.json`: **69 existing owned-answer key changes**. Existing identities are retained.
- `new-blank-answer-proposals.json`: **five** independently derived answers for empty BLANK banks, with stable UUID5 identities derived from each existing field UUID and canonical type/value.
- `type-proposals.json`: **seven** source-proved option type corrections. CAS values are numeric EIDs: math **17592186045498** → text **17592186045499**.
- `relation-proposals.json`: **five** question/field membership repairs covering six duplicate-key groups. Detach obsolete duplicate fields; retain all fields, answers and history entities.
- `choice-membership-proposals.json`: **two** select-bank membership repairs. Detach only the noncanonical mathematical duplicates in q335409/q335812; retain their answer entities and history. Equivalent historical BLANK answers remain unchanged.
- `generator-candidates.json`: **three** successor descriptors in the publisher's required shape, including exact files, dependencies and approved digest.

The five new blank questions' worked solutions are **already included** in `proposals.json`: 17592186229626, 17592186229628, 17592186229635, 17592186229641, 17592186229649. Do not create a second solution CAS from the answer-creation evidence.

## Coverage and source availability

The exact inventory contains **995 distinct questions/examples**, 14 topics, 32 tutorial contents, 78 activity/step links and 31 active generators. `current.json` captures the complete bounded-pull inventory, fields, types, choices, feedback, canonical links and tutorials at basis 9122. The original scalar audit contains 9,157 fields, including checkbox display keys. All 171 blank fields have individually recorded response-class context in `blank-class-review.json`: 166 existing canonicals are mathematical expressions and five were empty banks. No prose blank was converted to math.

Every topic's retained lesson HTML/JSON archive was read. Retained capture indexing examined 1,520 files. Original prompt evidence exists for 465 question/example entities; 78 MA-identified entities have no retained original prompt in these archives/captures; 452 entities have no MA identity and are generated/authored records. `missing-source-ledger.json` names every entity and exact available source paths. Generated records are compared against their active package/templates, not described as having unavailable Math Academy originals. `coverage.json` gives per-topic counts.

| MA topic | Questions/examples | Canonical examples | Retained original prompt | MA original unavailable | Generated/no MA ID |
| --- | ---: | ---: | ---: | ---: | ---: |
| 877 | 79 | 3 | 25 | 4 | 50 |
| 4096 | 121 | 4 | 44 | 21 | 56 |
| 1929 | 79 | 3 | 33 | 6 | 40 |
| 2522 | 62 | 3 | 32 | 4 | 26 |
| 1482 | 67 | 3 | 9 | 9 | 49 |
| 6679 | 96 | 4 | 50 | 2 | 44 |
| 6353 | 64 | 4 | 23 | 1 | 40 |
| 3241 | 33 | 3 | 20 | 13 | 0 |
| 3235 | 38 | 3 | 38 | 0 | 0 |
| 1181 | 106 | 3 | 42 | 0 | 64 |
| 1717 | 39 | 3 | 29 | 10 | 0 |
| 3672 | 30 | 4 | 30 | 0 | 0 |
| 906 | 88 | 3 | 36 | 0 | 52 |
| 317 | 93 | 3 | 54 | 8 | 31 |

## Substantive findings

1. **Outer MathML and field slots.** Source `S#` markers refer to exact observed `selectList-QUESTION-INDEX` DOM controls. A nested dropdown's first MathML is not the enclosing formula. Reconstructions use the owned assistive MathML and a complete source-bank/DOM-index mapping to existing field identities. Unsolved archive defaults establish layout, never canonical answers. Source geometry and existing local image references are retained. The staged historical-importer patch and authentic solved/unsolved fixtures demonstrate this failure and correct text-vs-math option inference; root owns shared integration.
2. **Shifted complete keys.** q337133/q337259 attached prose `is`/`isn't` as keys to mathematical fields. q333727/q333756 attached later table/phase-description answers to earlier coordinate fields. Exact source indices plus independent coefficient derivatives, system residuals, numerical table values and phase direction establish the existing correct answers. q334285's `unbounded` is a valid prose key needing type correction, not a different answer.
3. **Source-origin system typo.** q332878's system has frequency 6. The retained source and database put frequency 2 in the second coordinates of its general solution. The proposed frequency 6 makes both system residuals zero and preserves the intended existing coordinate choices.
4. **Operator identity and notation.** Powered trig operators such as `<msup><mi>csc</mi><mn>2</mn></msup><mo>U+2061</mo>` had become italic letter products. Thirty-seven exact marked-operator repairs preserve their function role; no unmarked plain-word heuristic is used. Existing vector/domain notation, teaching colors and meaningful braces are restored only where source semantics agree. Valid `boldsymbol` is preserved; root added the matching MathJax extension.
5. **Undefined glued commands.** Strict rendering exposed `intg`, `inth` and `intx`, which production `noundefined` had silently rendered as red text with zero ordinary `merror`. Source-proved integral boundaries are repaired. Standalone requested integral calculations use display math, including the future KP64245 generator.
6. **Completion.** Forty-six authored worked solutions follow matching KP canonical/nearby methods and independently solve the actual targets. Every one passes the explicit independent checks in `completion-math-verification.json`; all five new blank functions have zero ODE residual and, where stated, satisfy the initial condition. Exponential growth/decay calculations include units and rounding; partial derivatives include held-variable roles and applicable domains.
7. **Bernoulli branches/equilibria.** Twenty-one targeted prompt/solution qualifications cover ten source questions and one canonical solution. Ten independently derived linearized-z identities have exact zero residual. Positive square/fourth-root branches and the `2/3` power inversion require positive z; squaring a negative z introduces extraneous functions. Admissible zero equilibria are checked separately, while original equations containing negative powers exclude y=0. Existing answer values are preserved. The fresh active Bernoulli generator already states these qualifications.

## Validation evidence

- `final-rendering.json`: **9,172 final active scalar fields**, actual player Markdown and strict MathJax, **zero errors**. This includes newly authored solutions and blank answers, with detached obsolete memberships omitted from active presentation.
- `grading.json`: current release native checker, **1,626 accepted canonical responses and 4,215 rejected negative/bank responses**, across 947 questions with complete gradeable fields. No API writes or learner records were created. Questions without answer fields and the two unresolved incomplete banks are not misrepresented as graded completions.
- `ui-controls-verification.json`: **28 desktop/mobile cases**, actual rich-select menu interactions, MathLive blank input, checkbox Boolean identity toggles, source table blank mapping and source-style grouped systems. No raw field markers, MathJax errors or page overflow. Representative before/source/current geometry and final screenshots are retained; q333727 is the expected counterclockwise ellipse, q333756 the inward counterclockwise spiral, q334285 the same source phase portrait. Root separately owns exhaustive asset existence/decode checks.
- `fresh-independent-math-final.json`: **1,356 sampled fresh canonical/role checks across all 31 generators**, no remaining canonical candidates. These independently differentiate partial derivatives, check quotient increment arguments before taking limits, differentiate antiderivatives or prove generic integration-by-parts identities off the original poles, evaluate real logarithmic inverses/rounding, check ODE residuals/ICs, verify exactness coefficient/argument/sign roles, and classify linear/homogeneous/Bernoulli equations. Positive-domain absolute-value identities and branch conditions are explicitly recorded rather than assumed globally.
- `generator-rendering.json`: **11,275 fresh fields**, strict actual player, zero errors. `generator-grading.json`: **2,279 accepted and 5,895 rejected** responses. Native bank checks establish grading compatibility, not mathematical truth by themselves.
- `generator-source-eligibility-hits.json`: **zero** intersections of declared fresh source references with the basis-9122 retired/structurally-contained ledger using `scripts.generator_source_policy.source_references`.
- `successor-verification.json`, `successor-math-verification.json`, `successor-rendering.json`, `successor-grading.json`: **170 final staged samples**, **170/170 independent math passes**, **1,190 strict fields without errors**, **170 accepted/680 rejected** native responses, and zero excluded-source hits. The two operational reproducers now pass deterministic retry 1 and repeated runs are byte-identical.

## Generator prevention

- **KP64245:** all standalone integral prompts become display equations before normalization and the full-content hash/UUID. Version bumped; numerical mathematics is unchanged.
- **KP192794:** moderate count16/seed271028 previously reaches an impossible later rank-constrained batch slot. A bounded deterministic whole-batch stream retry preserves all original domain, distinctness, bank and pedagogy guards.
- **KP124639:** the same bounded whole-batch retry resolves moderate count12/seed271028's exp_sum rank-constrained dead end. Neither repair changes keys to satisfy a cue rule or relaxes inner guards.

The normal worker refill target is five. Both same-seed count5 probes already passed; the larger CLI counts are legitimate and now pass as well. Other count12 failures in KP217248/easy and KP217249/hard are explicit finite catalog limits of eight, not repaired by fabricating new variants. Current common `math_format.py` is included in each successor. Their existing full normalized content hashes already derive immutable question identity; versions are also advanced where applicable. Retained source JSON remains evidence, distinguished from fresh eligible content.

## Remaining issues and proof limits

`unresolved.json` contains exact evidence for:

- **q106074**: no existing radio option solves the stated Bernoulli equation. Correct nonzero family is the real cube root of `4x/(3+Cx^4)` on appropriate nonsingular intervals; y=0 is separately admissible. No answer bank or key was invented.
- **q337099**: integrating factor y^-4 is proved, but no existing potential choice is correct. The potential is `x^3/(3y^3)-2y`. Both nil keys and the source bank remain unchanged pending a deliberate bank repair.
- **q168079**: a legitimate structural multistep part depends on the preceding temperature model, parent17592186235310. It is already excluded from standalone generator source eligibility. No answer was inferred from isolated missing context.

This is exhaustive inventory/field/structure/source-candidate coverage, not a claim of manually proving every line of every unchanged explanation. The broad current CAS pass checked 518 cases and identified parser/role candidates; those candidates were explicitly reviewed, with domain defects repaired, harmless historical blank alternatives retained, and context-dependent parts identified. Every authored completion and changed mathematical statement has a specific independent derivation; fresh checks prove canonical/field roles for the sampled variants. They do not constitute theorem proofs of every unchanged historical distractor, every intermediate explanatory equality, or the entire finite/infinite generator parameter space. The retained-original gaps above limit source visual comparisons. Intentional figures and valid alternate methods were preserved.
