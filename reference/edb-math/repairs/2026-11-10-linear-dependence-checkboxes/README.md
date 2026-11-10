# Linear dependence statement questions

Audited the complete **Linear Dependence and Independence** lesson (`17592186050426`): 73 practice questions and three canonical examples. Thirteen remaining radio questions ask for subsets of three independently testable statements.

Converted **12** of those questions, including `17592186572667` (`q-157235`), to “Select all that apply” checkboxes. Four are imported questions and eight are generated questions. Each complete statement appears beside its checkbox; shared vector givens and row-operation instructions remain in the prompt. Explanations retain their mathematics and now refer to complete statements rather than removed Roman labels.

Committed atomically at **13805 → 13806**, source **`:agent/codex`**. See [commit-intent.json](commit-intent.json) and [receipt.edn](receipt.edn).

## Decisions

| Question | Source ID | True statements in original order | Decision |
| --- | --- | --- | --- |
| 17592186511507 | q-157227 | II, III | Converted |
| 17592186564502 | q-157254 | III | Converted |
| 17592186572667 | q-157235 | I, III | Converted |
| 17592186707061 | Generated | I, III | Converted |
| 17592186707068 | Generated | I | Converted |
| 17592186707084 | Generated | III | Converted |
| 17592186707089 | Generated | I, III | Converted |
| 17592186707100 | Generated | None | Retained radio |
| 17592186564487 | q-105317 | II | Converted |
| 17592186706984 | Generated | I | Converted |
| 17592186706986 | Generated | II, III | Converted |
| 17592186707030 | Generated | I, III | Converted |
| 17592186707038 | Generated | II | Converted |

The retained question has three false statements. The current `validate_practice_question` in `engine/rust/learning.rs` rejects checkbox practice without a correct selectable option. Keeping its existing “None” radio answer preserves both the mathematical task and its availability for fresh study. The engine rule was retained. The discarded 13-question preparation is archived under `preparations/13-question-unsubmitted`; it was never submitted.

## Verification

- Independently verified all 39 statements using exact vector combinations, matrix ranks, determinants and nullspaces. All stored keys agree. Proofs are in [resolutions.json](resolutions.json).
- Every old option, including wrong combinations and “none” distractors, has an explicit mapping. All **72 original radio choices** and **96 new checkbox subsets** passed live read-only native grading.
- Native speculative checks verified all owned Boolean banks, canonical subsets, single-checkbox flips, incomplete-response rejection, every mapped old choice, and **practice eligibility of every converted question**.
- Created 36 fields and 72 owned Boolean answers. Original fields/answers remain unchanged. Your one saved attempt on `17592186572667` retains its selection, status, timing and other state.
- Proposed, speculative and committed presentation lints passed. The actual player renderer and controls passed 36 question/viewport cases at 1100px, 708px and 390px, with 216 selection toggles and 36 saved-answer feedback checks. Zero MathJax errors or outer card overflow. Genuinely wide mathematics retains existing responsive scrolling.
- Exact committed readback matches the native preview's material datoms and identities. All 76 lesson questions were verified; other questions, difficulty, memberships and canonical examples are unchanged. The historical snapshot remains readable and the lesson remains available to study.

See [verification.json](verification.json), [case-ledger.json](case-ledger.json), [status.json](status.json), and [screenshots](visual/).

## Generator follow-up

The registered generators for KPs `17592186119924` and `17592186119925` can still produce combination-radio questions. Their immutable packages were not changed by this database migration. [generator-follow-up.json](generator-follow-up.json) records their registered paths, hashes and retained source snapshots so this separate generator work can resume from exact evidence.
