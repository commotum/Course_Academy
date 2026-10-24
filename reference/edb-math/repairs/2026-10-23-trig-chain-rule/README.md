# Trig chain-rule answer representation repair

Fixed generated question **17592186491432** in `math` at **T6121**, attributed to `:agent/codex`. The registered generator remains `generate/scratch/17592186064281.py`, now version 1.0.1.

The prompt and solution use `12-2x`. Independently rendering SymPy's evaluated answer expressions changed the correct choice to `-18x²-2sin(2x-12)`. Its equality with the solution's `2sin(12-2x)-18x²` requires the sine odd-function identity. The recorded key prerequisites are topics 280 (Differentiating Trigonometric Functions) and 1108 (The Chain Rule for Differentiation); this question's source method preserves the inner argument and requires no parity conversion.

The defect was a split between symbolic answer generation and source-template solution rendering. Both sides were verified only up to mathematical equivalence. Consequently, source-bank replay, derivative checks, and radio grading all passed while the learner faced an unexplained change of representation. The new checks independently enforce the displayed trig argument and agreement between the final solution and keyed answer. Authoring guidance now requires deriving the answer and explanation from the lesson's ordered steps and checking the prerequisite scope of conversions.

The generator preserves the source inner expression in all five choices across all 16 bounded instances in this family. Existing semantic fingerprints, question/field/answer UUIDs, correct-answer links, prompts, and worked solutions are unchanged. The current database contained one generated question in this family needing repair; the original source question already used the intended form. The transaction changes five `answer/value` strings and requests native answer, field, and question validation. CAS guards preserve concurrent edits.

Verification:

- All 74 eligible instances across six profiles passed the exhaustive validator, including 146 accepted and 188 rejected checks through `learning::grade_field`.
- The previous representation fails the new check for all 16 cosine-plus-cubic instances. Corrected choices remain mathematically equivalent, and other profiles remain unchanged except generator version metadata; see `regression.json`.
- Three unit tests cover the reported UUID and corrected form, the original unexplained parity rewrite, and a different equivalent but unshown final conversion.
- `preview.edn` and `receipt.edn` contain exactly the ten expected answer-value datoms plus transaction metadata. `verification.json` confirms the complete KP/question/answer ownership closure at T6121, including unchanged identities and key links. The receipt contains no learner-state mutations.

`repair.py prepare` retains the exact CAS transaction and native preview; `repair.py apply` retains and recovers the same request identity before exact-basis verification. Retained pre-change generator and validator files preserve the original diagnosis. `before.json` records T6111; unrelated database transactions between that read and T6121 were preserved.
