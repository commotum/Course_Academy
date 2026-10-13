# Template extraction

## 1. Specific source descriptions

All exact prompts, solutions, enum types, field layouts and choice fragments remain in `source.json`; numerical/index parameters are separately listed in `source-cases.json` and replayed through the public API. Identifiers are generated field-owned UUIDs; database entity IDs and MA source IDs remain provenance rather than learner attributes.

| Source | Matrix/request | Layout and solution sequence | Observed bank |
|---|---|---|---|
|q-13495 |3x3 A; a32=8; positive single-digit entries, repeated2 and7 |aligned prompt ending period; intersection sentence, conclusion8, repeated matrix without period |8,4,1,6; text No such entry |
|q-13490 |3x3 G; g22=2; signed, zero and repeated values |same aligned radio mask; intersection/conclusion and repeated matrix without period |2,-1,5,4; text No such entry |
|q-279542 |2x2 A; a22=-3 |aligned blank including exact whitespace and `{{field-1}}`; solution repeats matrix with period |single math fragment-3 |
|q-125593 |4x4 R; r43=1; includes sqrt3 and sqrt2 |aligned radio; same intersection/conclusion; repeated matrix mistakenly named E, without period |1,sqrt2,8,-1; text No such entry |
|q-125564 |2x2 B; b32 nonexistent |aligned prompt; should-lie intersection,2x2 dimension, missing third row, final no-entry conclusion; no repeated matrix |text No such entry;1,-3,0,5 |
|q-13506 |4x4 P; p14=4; signed entries including12,13 |inline bmatrix; unrated; no worked solution and no correct ref |4,7,6,-3; text No such entry |

Sourceq-13506 screenshot confirms all five options, but supplies no observed solution/correct flag. Raw replay therefore omits all three absent attributes; normal completion explicitly assigns authored easy, independently infers4 and authors the common intersection solution. No missing original designation counts as matched.

## 2. General pattern

Decode i and j, count rows from the top and columns from the left, and return exactly the displayed cell. In the observed absent variant, check whether the requested row exists and return the source text choice. Responses are scalar math fragments or the exact text `No such entry`. Radicals are copied as entries, never evaluated or combined. There is one fixed worked solution per instance, independent of the chosen incorrect option.

## 3. Complete components and banks

Coordinates below are1-based and depend on the displayed matrix and requested i,j. Every cell operation is used as a whole bank; equality of any two mathematical values rejects the complete instance. Interpretations of historical coordinate choices are hypotheses, not recovered author intent.

| Profile/source | Complete mathematical recipes in addition to No such entry | At source | Interpretation limits |
|---|---|---|---|
|q-13495 |M[i,j], M[i,j-1], M[j,i], M[j,1] |8,4,1,6 |leftward/row-column confusion recipes; inferred |
|q-13490 |M[i,j], M[i,j-1], opaque scalar slot0, opaque scalar slot1 |2,-1,5,4 |5 and4 are absent from matrix; source underdetermines their operations. Explicit historical slots reproduce them; evidence-only, excluded from defaults |
|q-279542 |M[i,j] |-3 |blank has no distractors |
|q-125593 |M[i,j], M[i,j+1], M[i-1,j], M[i,j-1] |1,sqrt2,8,-1 |adjacent-position errors; inferred |
|q-125564 |No such entry, M[1,1],M[1,2],M[2,1],M[2,2] |No such entry,1,-3,0,5 |all four existing cells; inferred indexing errors |
|q-13506 |M[i,j],M[n,n],M[n-1,n-1],M[2,3] |4,7,6,-3 |complete coordinate pattern, historical intent uncertain |

Choice types are math for every cell/opaque scalar and text for the no-entry choice. Source correct flags are matched one-to-one at five observed refs; q-13506 retains omission. All26 answer fragments are matched, including21 numeric fragments and five text fragments. Among the five rated sources there are16 wrong options; the unrated source's four mathematically wrong alternatives are derived, not observed correct flags.

Authored normal banks are `transpose_neighbors` (q-13495 pattern), `right_up_left` (q-125593 pattern), `inline_diagonal` (q-13506 pattern), `all_four` (q-125564 pattern), `blank`, and `local_neighbors` (target,left,up,down,No such entry; method-derived replacement for opaque q-13490). Normal sampling covers every supported layout and eligible bank. It chooses the whole profile first, then parameters; no first-valid distractor selection or replacement is used.

## 4. Reusable masks, scope and identity

Complete matrix rows, index pair, requested symbol and matrix name are slots. Ordinal suffixes follow the displayed row/column. The aligned/inline masks and blank supplied fragment retain source layout; period after repeated solution matrix is a source-specific conditional. Raw q-125593 keeps E exactly; normal uses the actual requested matrix name. Raw q-13506 preserves absent difficulty/solution/correct, with authored completion separate. No unmatched TeX byte anomaly was found; no TeX normalization is claimed.

Source replay runs `generate('easy', parameters=case['parameters'], template=case['template'], profile=case['bank_profile'])`, where raw profiles name complete recipes and presentation conditions; none returns a literal source payload or answer lookup table. Changed-parameter raw variants are reviewed. Opaque slots remain explicit limitations, never claimed method recovery.

Normal entry domain: integers-13..13, sqrt2,sqrt3 (29 distinct scalar forms). This contains the observed number forms and magnitude ceiling; radicals do not add arithmetic. Easy2–4, moderate exactly5 with maxindex>=4, hard exactly6 with maxindex>=5. Authored levels only ask existing entries. Easy absent variant is2x2 with exactly one index3; normal numeric blank exists at every valid position.

Meaningful finite tasks are `(n,i,j,target)` for existing entries and `(n,i,j,No such entry)` otherwise: **845 easy** =29*(4+9+16)+4; **464 moderate** =29*(25-9); **580 hard** =29*(36-16). They exclude matrix-letter aliases, unrelated entries, choices/profiles and layout. Every target/position can be realized by a valid blank; the four absent tasks can use distinct entries. Full content identity retains actual prompt, fixed solution, complete owned bank, answer criterion, difficulty and generator version. Changed incidental cells change full identity but not task counts. Seed/shuffle/profile aliases cannot alone change identity.

Independent QA reads the matrix, indices, all choice values and worked-solution sentences back from the actual display. Source fidelity, math correctness, native grading and authored scope claims have separate checks. Delimiters/braces and deliberate corruptions are tested. No database writes or renderer are involved.
