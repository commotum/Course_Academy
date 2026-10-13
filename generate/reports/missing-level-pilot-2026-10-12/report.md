# Three-KP missing-difficulty design pilot

**The three cases give different answers: matrix-entry lookup has a narrow scope that makes a convincing moderate level difficult to create; reciprocal-ratio calculation has a natural easy family; and 2×2 determinants can support a harder family through added algebra.** A missing difficulty label therefore needs a content judgment before we decide whether to fill it.

All three KPs came from the saved `find_candidates.py` discovery. Selection used an **individual missing-level score between 80 and 95**, not the hybrid score. We chose one missing-easy, one missing-moderate, and one missing-hard case, with manageable inventories and no associated generators. This is a deliberately varied pilot, not a random sample estimating how common each outcome is.

| KP | Requested missing level | Absence score | Easy / moderate / hard | Unrated | Captured lesson position | Design judgment |
|---|---|---:|---|---:|---|---|
| Finding an Entry of a Matrix | Moderate | 92.5497 | 5 / 0 / 0 | 2 | 1 of 3 | A convincing moderate family is difficult within literal lookup |
| Computing a Reciprocal Ratio Using the Pythagorean Identity | Easy | 94.7935 | 0 / 5 / 0 | 1 | 3 of 4 | An easy family is natural and supported by source content |
| Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries | Hard | 85.4986 | 6 / 6 / 0 | 1 | 2 of 3 | A hard extension is feasible, with difficulty from algebra |

The lesson positions come from the existing capture analysis, with source pointers retained in its [KP inventory](../../../reference/mathacademy/kp-difficulty-analysis-2026-10-12/kp-inventory.json). They are useful context, not a causal explanation of these labels. Matrix lookup comes first and has all easy labels; the reciprocal procedure appears later and has all moderate labels, despite simpler in-scope instances being possible.

## What was done

Applied [3-classify](../../docs/3-classify.md) and [4-template-extraction](../../docs/4-template-extraction.md) to **all 26 practice records** at EDB `math` basis **1522**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The native export includes difficulty, original Markdown, field types/keys, every choice and correct reference, fixed worked solutions, canonical examples, associated generators, and neighboring KPs. Canonical examples support scope analysis and are excluded from practice counts.

There are **22 rated questions**, **19 radio fields**, **7 blank fields**, **19 distinct source-bank profiles**, and **102 source answer values**. The rated sources form **16 Markdown/value templates** across the three KPs; changed numbers alone do not create templates. Each original is described separately before its family is generalized. Blank notation and expected fragments are preserved; radio banks are kept separate from template counts.

Every original choice has a source field, answer entity/UUID, complete value expression or observed value pattern, source-profile parameters, and bank profile. All **102 complete value recipes replay at the original parameters**; all **22 stored correct answers agree with independent prompt-based calculations**. This is source-parameter extraction/replay, not a claim that inferred distractor rules generalize to a complete generator. Unresolved error causes and fixed source constants remain explicitly recorded.

Four originals—`q-1088`, `q-13488`, `q-13496`, and `q-65066`—lack difficulty, a correct-answer reference, and a worked solution. Their actual prompts and banks remain in the analysis. Computed answers are distinguished from absent source markings. They do not increase the absence estimator's rated-question denominator.

For the reciprocal-ratio KP, the [plot-extraction protocol](../../docs/5-plot-extraction.md) was also applied. All eleven practice image occurrences and the canonical image were visually inspected; the source diagrams establish the first quadrant. Matching plots were created for the authored reciprocal probe. The other KPs contain typeset mathematics but no plots.

## Matrix lookup: difficulty ceiling from scope

The source's easy `q-279539` already requests entry e₅₃ in a **5×4** matrix. Our probe changes that entry to −7/3 and keeps the same blank response and row/column solution. That is easy to write, but the mathematical task is unchanged: find a cell and report its literal contents. Neither the fraction nor its sign needs to be calculated.

Larger matrices, repeated values, and less friendly entries can increase search and reading burden. They provide weak separation into a mathematical moderate level, especially because a large source instance is already easy. Asking for indices instead is an actual sibling KP; adding transposition or matrix operations requires extra skills.

**Best judgment:** preserve easy lookup variants and decline to manufacture moderate labels from clutter. The obstacle is the KP's one-operation response contract, not lack of numerical variation.

[Classification](17592186100988/classification.md) · [Template extraction](17592186100988/template-extraction.md) · [All originals](17592186100988/source-questions.md)

## Reciprocal ratios: lower complexity already fits

All five moderate originals require recovering an irrational complementary sine/cosine, taking its reciprocal, and rationalizing. Choosing a Pythagorean-triple coordinate removes the irrational-root and rationalization burden while preserving identity recovery, first-quadrant sign selection, and the reciprocal operation.

Our easy proposal gives x=5/13 and asks for csc θ=13/12. It has a full five-choice radio bank and matching prompt/solution figures. Its complete bank is extrapolated from `q-65066`: at b=5,c=4 the five recipes reproduce all five original values exactly; at b=13,c=12 they produce five distinct choices with one correct answer.

Importantly, **q-65066 itself supplies y=3/5 and has the correct value 5/4 in its bank**, although its difficulty and canonical correct reference are missing. The complete canonical example `e-3484` likewise produces the rational reciprocal 7/5. These sources directly support the proposed simplification's mathematical scope; neither establishes an observed easy label.

**Best judgment:** an authored easy family is straightforward. Here the high missing-easy score does not correspond to a mathematical difficulty floor. The stored labels can reflect repertoire selection or lesson design even when easier instances fit.

[Classification](17592186110756/classification.md) · [Template extraction](17592186110756/template-extraction.md) · [Plot specification](17592186110756/plot-extraction.md) · [All originals](17592186110756/source-questions.md)

## Determinants: extra difficulty from prerequisite algebra

The easy and moderate sources already vary radicals, fractions, signs, symbols, and factoring. Their shared move remains ad−bc. A same-KP harder task can use compound conjugate radical fractions in the four entries, requiring two expanded products and fraction combination before the answer is simplified.

Our proposed hard question has answer −41/210, independently verified using `SymPy Matrix.det`. It keeps a 2×2 determinant and an observed blank-field contract, needs no diagrams, and introduces no new determinant method. Its compound entry shape is an explicitly authored extension beyond the source templates.

**Best judgment:** feasible with moderate design effort. The challenge comes mainly from prerequisite radical and rational algebra. Whether that is desirable depends on what we want a hard determinant question to measure. Solving for an unknown or using a 3×3 matrix would change the assessed skill and was rejected.

[Classification](17592186059749/classification.md) · [Template extraction](17592186059749/template-extraction.md) · [All originals](17592186059749/source-questions.md)

## Implication for inventing missing levels

Use two checks: **does the proposed family stay within the KP's procedure and answer contract, and does it create meaningful difficulty separation?** A mathematically valid numerical variant can fail the second check, as matrix lookup does. A clean parameter family can meet both checks, as the reciprocal example does. A heavier algebra family can stay in scope but shift much of the assessed effort onto prerequisites, as the determinant example does.

The statistical absence scores prioritize investigation; they do not decide whether an authored missing level should exist. Keep authored difficulty assignments separate from source-observed labels. For these three KPs, our concrete recommendations are: **easy-only lookup variants; add an easy reciprocal family; allow a proposed hard determinant family with its algebra burden documented.**

## Artifacts and validation

- [All three concrete probes and worked solutions](probes.md)
- [Frozen native EDB source export](source.json), [saved query](database/selected-kps-query.edn), and [inputs](database/selected-kps-inputs.edn)
- [Every source's components and complete choice mappings](source-cases.json)
- [Source and field inventory verification](verification.json), [recipe/probe verification](probe-verification.json), and [plot asset hashes](plot-assets.json)
- [Extraction script](extract.py), [exact audit](audit_probes.py), and [probe plot renderer](render_probe_plots.py)

Reproduce local extraction and verification without database access:

```bash
.venv/bin/python generate/reports/missing-level-pilot-2026-10-12/extract.py
.venv/bin/python generate/reports/missing-level-pilot-2026-10-12/audit_probes.py
MPLCONFIGDIR=/tmp/course-academy-matplotlib /home/jake/Developer/MA/.venv/bin/python \
  generate/reports/missing-level-pilot-2026-10-12/render_probe_plots.py
```

No database facts were changed. The deliverable is classification, extraction, and reviewable missing-level experiments; these are not operational generators, and learner-engine grading is not claimed.
