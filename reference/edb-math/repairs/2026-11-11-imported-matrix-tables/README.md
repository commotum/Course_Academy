# Published matrix/vector import repairs

Committed and read back at EDB math basis **14375**, attributed to `:agent/codex`.

Repaired **552 imported question entries** (551 with answer fields and one
fieldless worked example). The initial primary review led to 474 repairs; inspecting the broader
retained census added 78 entries. This is why the final total exceeds the earlier
534-question candidate list: 60 original candidate entries were legitimate,
and the broader search found additional defects.

Three subagents reviewed source and semantic intent, supplied-entry positions,
rowspans, operators and template context. Independent peer review checked the
complex matrix equations and all authored completions. Across primary and
supplemental review, 659 malformed matrix/vector table blocks were confirmed;
1,000 legitimate table blocks were retained. These are block counts; a question
can contain several blocks. Genuine distance/adjacency tables, division arrays,
sign charts, probability tables and other data layouts were preserved.

The saved questions now use the existing bracketed matrix/vector controls,
including partially supplied entries and multiple operands. All supplied entries,
field identities and mathematical operands are preserved. Three exact repeated
SVD operand copies were collapsed, and 23 selectors were moved out of math
wrappers so they remain usable controls. Additional review caught Newton vectors
with `≈` labels that had been incorrectly treated as table headers; the detector
now recognizes that case.

Necessary completion and notation repairs:

- Completed 17 questions with missing canonical answers or duplicate empty
  fields. Added 41 field-owned answers, linked 11 existing correct choices, and
  added 16 missing worked solutions. A required `4` option absent from one
  Jacobian select bank was added; existing choices and IDs remain intact.
- Removed only two question-to-empty-duplicate-field references. The orphan
  entities and retained history were read back unchanged.
- Corrected an upstream answer-label typo from `2^(D/2)` to `2^(D/3)`, matching the
  explicit question and its diagonal entries. This is an authored correction,
  supported by the original source screenshot, not a claim of unchanged source.
- Restored 12 solutions whose MathML import rendered `\text{\boldsymbol}f` as
  a literal command. The import formatter now prevents that artifact.
- Fixed the grader's rejection of `xyz` products in explicitly defined
  multivariable functions. The parser uses declared prompt arguments rather than
  reinterpreting arbitrary words. Unknown functions, e/i interpretation and
  domain restrictions remain covered by regression tests.

Verification:

- [Precommit verification](verification-precommit.json): 1,130 actual UI
  presentations, with all 552 final records covered in mobile active and desktop
  completed states; field coordinates/identities and empty enabled controls
  checked independently. Four superseded presentations were excluded.
- [Committed-data grading](committed-native-report.json): 2,019 accepted and 2,308
  rejected controls, zero unresolved. The saved question records match the exact
  records validated before commit.
- [Commit receipt/readback](commit-verification.json): exact prepared assertions
  and retractions, full question readback, unchanged KP membership/generators,
  intact orphan entities and historical reads. Learner/engine database facts
  were unchanged.
- [Live API check](live-api-verification.json): the deployed read-only preview
  accepts an equivalent gradient and rejects the wrong sign without recording
  learner responses, timing, progress or XP.
- [Live service](live-service.json): healthy after loading the prebuilt grader;
  generation remains disabled. The generation pipeline was not started.
- 53 formatter tests and all 297 Rust library tests passed. Grader source hashes
  and test results are recorded in
  [the code verification](review-2/declared-products-code-verification.json).

The exact reviewed plan is [plan.json](plan.json), and the transaction is
[publication/transaction.edn](publication/transaction.edn). The durable request
and receipt are archived under `publication/requests/`; there is no pending
request. An earlier prepared-only request was archived as never submitted after
validation exposed the notation issue; only the final reviewed transaction was
committed.

[Primary decisions](reviews.json), [supplemental scalar-layout decisions](review-2/supplemental-reviews.json),
[weak-array decisions](review-3/supplemental-reviews.json), and
[Newton source/geometry review](review-1/supplemental-cross-review.json) retain the
individual confirmations/disconfirmations. Exact-source comparisons are
explicitly distinguished from source-family and stored-geometry evidence.

Scope: all confirmed defects from this review are repaired. This was a table
import audit, not a certification of every image, pedagogical choice, generator,
or non-table question in the database. The existing generator registrations
were not changed. Author-created answers/solutions retain separate provenance
from observed Math Academy content.
