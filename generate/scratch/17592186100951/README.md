# Identifying Solutions to Initial Value Problems

Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186100951/validate.py
.venv/bin/python generate/scratch/17592186100951.py --difficulty all --seed 29 --count 2 --format json
```

The generator recovers the constant in an explicitly supplied IVP solution. It never solves a differential equation. All three entrypoints exist. Moderate and hard are authored difficulty assignments, grounded in the source families and documented workload bounds; no source example is relabeled as observed moderate/hard.

`observed:q-…` is a public, parameterized evidence replay profile: exact source prompt, bank and all present worked-solution strings; original difficulty/solution/correct-ref omissions are retained. Such records are explicitly ineligible for learner use. `completed:q-…` preserves the source bank but repairs two missing correct refs and missing solutions by independent derivation and the unmarked trig operators by explicit notation repair. Completed opaque banks also remain evidence only. Normal/default output uses authored coherent complete banks and repaired function notation.

Source snapshot: math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the entire capture wrapper; `source-cases.json` covers every practice question. `masks.json` contains reusable complete-component source prose masks, not source-answer lookups. See classification, four-stage extraction, source error evidence, review and validation records. No plots, database operations, or shared edits are required.

Source fidelity: 19/19 banks, 63/63 exact answer strings, 44/44 distractors, 19/19 exact prompts, 17/17 exact present full solutions and ordered stage sequences, 17/17 present correct designations. Two absent designations are reported separately. Native grading checks canonical constants, genuinely unreduced equivalent constants, wrong constants and every displayed radio choice through the real engine.

Version `ivp-constant-v2` closes the explicit easy-input workload bypass. Nontrig initial outputs use a 44-value reduced rational catalog; trig outputs use 14 signed familiar special-angle values. `number-domains.json` lists those catalogs and finite meaningful sampler counts (easy 3,808; moderate 384; hard 216). All profiles use the same guards, and the validator checks rejected large denominators/unsupported radicals alongside displayed catalog-boundary questions.

Markdown author previews and `review.md` visibly label E/M/H or unrated status, original/source evidence versus normal authored origin, and each present correct designation. An absent original correct attribute is stated explicitly without an inferred correct mark. These labels surround the unchanged source/question strings; JSON records, mathematics and identities are unchanged. The presentation-only verification command is:

```bash
.venv/bin/python generate/scratch/17592186100951/validate-presentation.py
```

`presentation-baseline.json` preserves pre-edit hashes for all 169 stored generated records and ten protected JSON artifacts. `presentation-validation.json` confirms deterministic rendering and unchanged records.

Version `ivp-constant-v3` replaces the generic scaling/shift radio bank with complete family-specific wrong-operation banks. `authored-banks.md` derives every member from the supplied initial substitution. Degenerate instances reject the entire selected bank; observed/completed source banks remain exact and evidence only. The mathematical validator independently reconstructs the full normal bank from the actual printed function and condition, checks explicit whole-bank rejections, and enumerates eligible finite radio supports.

After the method-bank revision, the presentation baseline refers to the final v3 question records. The normal banks and their content identities intentionally change; the exact observed source banks, prompts and present solutions remain preserved. Presentation rendering again proves those final records immutable. Eligible normal radio task counts are power nonunit 176, power unary 76, reciprocal-power nonunit 220, reciprocal-power unary 76, exponential 1,008, cosine 168, reciprocal affine 320 and log 24.
