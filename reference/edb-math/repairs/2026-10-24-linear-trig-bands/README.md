# Linear trig integration: band redesign and pool refresh

Committed to `math` at **T6391**, attributed to `:agent/codex`.
Authorization: “make the repairs. Update the generator, retire old questions,
and refresh the pool.”

The registered generator now uses the immutable package recorded in
[package-verification.json](package-verification.json). The repository entrypoint
[17592186068915.py](../../../../generate/scratch/17592186068915.py) and its local
helpers also contain the repaired implementation.

## Delivered result

| Band | New, unserved questions |
|---|---:|
| Easy | 8 |
| Moderate | 6 |
| Authored hard | 5 |
| **Total** | **19** |

The eight easy records cover all four sine/cosine and indefinite/definite
families in both response formats. The six moderate records cover every shifted,
pi-scaled, and rational-slope family. The five hard records cover both functions
and both derivative signs, with an additional endpoint sign-relation case.

The four previous generated variants were retired from fresh practice:
`17592186482716`, `17592186482718`, `17592186482722`, and `17592186482724`.
Their exact generation evidence and identities are retained in
[retirement-evidence.json](retirement-evidence.json).

All **12 imported practice questions**—7 easy and 5 moderate—the canonical
example, old question/answer content, bank membership, and saved attempts were
preserved. This includes the imported `q-350040` question 17592186319362.
Retirement does not erase or replace already saved work.

## Generator repair

The old implementation used seven sources and allowed only positive coordinate
dilation. It fixed amplitudes, trig functions, shifts, and transformed endpoints
inside each source template. Every easy definite-integral blank consequently
retained the amplitude 9 and sine. Five later cosine examples were absent from
its families. Source labels were inherited even where easy and moderate examples
had equivalent workloads.

The replacement chooses structural cases before compatible parameters. It varies
amplitude, sine/cosine, derivative sign, affine shift, endpoint values, and
response format within the explicit [band contract](package/band-contract.json).
Original and retired mathematical task fingerprints are excluded. Mathematical
deduplication ignores seed and answer-field format.

- **Easy:** one reciprocal inner derivative and a basic trig antiderivative;
  indefinite integer shifts with signed integer/simple reciprocal slopes;
  definite quarter/half-turn endpoints with values 0, 1, and -1.
- **Moderate:** shifted special-angle bounds, pi-scaled derivatives, or rational
  derivative factors with controlled endpoint work. Negative-result cases remain
  supported; source-like positive cases are not rejected to impose a sign quota.
- **Hard:** fractional amplitude and signed rational slope, angular shift, and
  two nonzero primitive endpoint values of unlike radical magnitudes. Exact
  entry requires coordinating reciprocal factors, signs, both bound changes,
  and radical subtraction. This is an **authored composition of established
  skills**, approved in the design discussion; no imported hard anchor or
  externally calibrated hard label is claimed.

The chosen trig function and affine input stay visible in the prompt, solution,
and key. Worked solutions show the derivative, reciprocal factor, transformed
bounds, integration sign, exact endpoint values, and final simplification.
Negative derivatives include an explanation of the decreasing transformed bounds.
Long derivations were reflowed after visual inspection exposed clipping.

Radio banks use explicit authored error recipes supported by the source patterns.
Zero-outcome banks generalize the complete `q-13644` bank so wrong values do not
all collapse to zero. Repeated families alternate response shape; derivative
signs use a separate schedule so they do not become fixed by field type.
Shortage and request limits fail explicitly rather than padding duplicates.

## Verification

- Independent parsing checked **74 regression records**, including **864 printed
  equalities in the main 72-record sample**. It reconstructed the actual prompt,
  derivative, bound substitutions, integration/evaluation rows, complete banks,
  and final key without treating generation metadata as mathematical proof.
- Negative controls rejected an incorrect displayed reciprocal factor, easy work
  relabeled hard, and an unsupported request size. The retained old family
  reproduced the amplitude/function variety failure.
- The actual native learner grader passed **39 accepted** and **44 rejected**
  checks, with no unresolved comparisons.
- All **19** records survived the shared delivery/preparation filters. Printed
  derivations were checked again after delivery; their content was unchanged.
  Easy definite blanks include both sine and cosine.
- Six representative cases rendered through the unmodified learner UI. The
  final hard negative-slope and easy indefinite layouts were visually inspected.
- The published package was relocated and reproduced every approved record.
- Native transaction preview and the committed receipt matched the exact planned
  assertions/retractions. Readback checked every new question, all old content,
  imported questions, the canonical example, and saved-attempt references.
- The live pool at T6391 contains all 19 new, unserved questions under the new
  registration. The running app's read-only preview graded a new blank from
  each band correctly.
- Three repository regression tests cover within-family response/sign variation,
  the zero-outcome bank, and the hard-band contract. `git diff --check` passed.

See [verification.json](verification.json),
[live-pool-verification.json](live-pool-verification.json),
[live-grading-verification.json](live-grading-verification.json),
[generator-verification.json](generator-verification.json), and
[delivery-verification.json](delivery-verification.json).

`publication/` retains the exact guarded request, native preview, receipt,
preparation, and readback. `deploy.py` recovers a pending exact request before
preparing anything new and recognizes an already verified deployment. The
original implementation and capabilities remain available for historical replay.
