# Classification — Applying Row Operations To a Coefficients Matrix

Database `math`, basis 2366, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
All nine practice questions and the canonical example were pulled together.
`reference/initial/kp.edn` is the exact source read; `source.json` preserves all content.

| Difficulty | Response | Templates | Sources | Plot rating |
|---|---|---|---|---|
| Easy | one five-choice radio | swap rows; scale one row | q-10250, q-10244; q-130006 | none |
| Moderate | one five-choice radio; q-10248 also retains an invalid duplicate legacy field | add a multiple of another row | q-10248, q-20239 | none |
| Hard | one five-choice radio | two distinct targets with a common unchanged source; same target with two different sources | q-130064, q-130065, q-10245; q-130010 | none |

Moderate has one mathematical/Markdown backbone and two complete bank profiles.
Easy swap has two banks; scaling has one. Hard distinct-target has three banks;
hard repeated-target has one. Those banks are separate and are not pooled.

q-10248 has two `selection` fields: one historical bank omits its correct designation, and the
completed field has a correct answer. Both entire banks are identical as sets.
The source solution incorrectly negates the unchanged first row in the
intermediate matrix. Its final answer is correct. Generated instances have one
field and preserve the first row at every stage. Existing records remain intact.
q-130064 designates the first-operation-only result rather than the final result:
the stated second operation makes row 3 `[6,5,1]`; the keyed choice keeps `[1,3,0]`.
This source defect is documented and is not reproduced or repaired here.

Moderate is the requested exhausted band. The validated executable implements it.
Easy/hard remain classified, evidence-supported bands with no sampler in this
package. That is a bounded implementation capability, not an impossibility or a
claim that those inventory shortages are filled. Their implementation is pending.
