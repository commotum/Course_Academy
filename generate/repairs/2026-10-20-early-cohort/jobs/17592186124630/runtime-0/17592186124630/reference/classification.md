# Recognizing Parts of the Invertible Matrix Theorem

Captured math basis: **2617**. Lineage:
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
The complete KP, canonical example and 12 practice questions are retained in
`initial/kp.edn` and `initial/kp.json`. No existing generator was registered.

Every practice question is Easy, with one `radio` field keyed `selection` and
five choices. The prompt displays the same four-line equivalence for a real
square matrix and asks for one missing fragment. Solutions recall the full
theorem, display its four lines, then identify that fragment. The dimension
parameter n is symbolic and positive; there are no arithmetic parameters.

| Answer contract/template | Source profiles | Status |
|---|---|---|
| Null(A) = [zero subspace] | q-140766, q-142468 | Supported; one semantic task |
| A is [invertible] | q-141344, q-142302 | First supported; second lacks a visible blank |
| dim Null(A) = [0] = nullity(A) | q-141191, q-142471 | Supported; one semantic task |
| [Col(A)] = R^n | q-141348, q-142357 | First supported; second has equivalent correct choices |
| dim Col(A) = n = [rank(A)] | q-141194 | Supported |
| [dim Col(A)] = n = rank(A) | q-141343 | Excluded: missing marker and two correct choices |
| dim Col(A) = [n] = rank(A) | q-141192 | Excluded: missing marker and duplicate scalar choices |
| [Null(A)] = {0} | q-141345 | Excluded: Null(A^-1) also equals {0} |

Thus the observed bank has eight fragment contracts, twelve bank profiles,
seven supported profiles and **five distinct supported tasks**. All five already
exist as practice. Different banks for one target do not replenish that task.
The canonical example asks for dim Null(A), supplies no gradable practice field,
and never contributes to inventory.

Plot rating is **none** for every practice template. Practice contains standalone
TeX, not a mathematical diagram. The canonical SVGs render the same theorem;
this package neither changes their parameters nor republishes them. No plot
generation, asset publication, or image interpretation is needed for the selected
practice templates.

Moderate and Hard are unsupported by this bounded package. Increasing symbolic
recognition to matrix computations, proofs, or multiple blanks would change the
method or field contract. Absence alone is not the justification: the recovered
backbone has no numerical workload to scale. New source evidence or a separately
validated same-skill extension can reopen classification.

The current mathematical audit excludes malformed or ambiguous banks from its
own validated count; it does **not** repair or remove their database records.
