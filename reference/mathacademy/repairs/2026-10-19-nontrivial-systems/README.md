# Nontrivial systems and revised difficulty bands

Committed and verified in `math` at basis **5035**, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.

All three registered generators for lesson `17592186050240` now reject
identical equations and equations differing only by a sign in learner output.
Immutable new packages are registered through new generator entities; the
previous packages/entities remain intact. See `package-updates.json`.

## Solution-count bands (KP 17592186073776)

| Band | Workload |
| --- | --- |
| Easy | Standard RHS form; elimination multiplier magnitude 2; displayed variable coefficients <=5 and constants <=12 |
| Moderate | Standard RHS form; multiplier magnitude 2–4; coefficients <=10 and constants <=30; instances satisfying easy are explicitly excluded |
| Hard | Both equations initially have zero RHS and require rearrangement; multiplier magnitude 2–4, retaining the existing signed coefficient bounds |

The bands are authored, not recovered Math Academy ratings. All three outcome
branches are selected before numerical sampling in every band. Original
parameter completions q-211984, q-237043 and q-237046 still validate. The other
two KPs retain their existing workloads; intersection-count hard sampling no
longer chooses unit row scales, and general-family validation rejects them.

## Stored questions

The entire 70-question lesson pool was checked. Seven systems were rescaled,
with matching worked solutions, and seven difficulty ratings were corrected:
ten distinct authored questions, 21 changed fields. `repairs.json` records the
individual reasoning, original/new coefficient rows and ratings.

The reported question `17592186529320` now displays `4x-2y=8` and `2x-y=4`.
The sign-flipped hard intersection-count question `17592186561213` now displays
`5x-2y=-1` and `-10x+4y=2`.

Each rescaling preserves each equation's exact solution set and the existing
correct answer. Question/field/answer identities, banks, keys, pool memberships
and learner records retain their values. Retaining membership also preserves
the engine's checks of historical lesson presentations. Captured Math Academy
source records and their absent ratings were left unchanged.

## Verification

- 63,000 structural samples across all three packages; no identical/negated pairs.
- 372 public generated records, including source completions and controlled
  classification counterfactuals, plus 10 repaired records.
- All 382 records accepted by the current native learner grader; authored
  distractors rejected. No database writes were used for grading/rendering.
- 28 pages rendered using the unchanged learner UI; no rendering errors.
- Explicit duplicate and sign-flipped inputs rejected by every package.
- Exact CAS guards, native question entity validation, saved preview/request/
  receipt and exact committed readback. EDB may assert the unchanged value of a
  same-value CAS under this contributor; receipt checks permit only those exact
  context guards in addition to the prepared changes.
- All 70 pool questions checked after commit; all 21 rated solution-count
  questions satisfy the revised bands. All other question/answer data and pool
  membership compare equal before/after.

`verification.json` is the final commit/readback proof. `commit.py` retains
the original stable request for outcome recovery; do not regenerate a request
to replay an already successful submission.
