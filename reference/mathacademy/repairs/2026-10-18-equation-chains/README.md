# Equation-chain import repair

Committed to `math` at basis **4620** (before: 4619), attributed to `:agent/codex`.
The database receipt and exact readback are recorded in `verification.json`.

The transaction repaired **1,631 fields on 1,624 entities across 267 lessons**:
1,423 worked solutions, 199 tutorials, and 9 question prompts. This accounts for
1,627 of the original 1,628 audit fields plus four directly related prompts.
The remaining audit field had already been repaired; its exact content was
verified unchanged at basis 4620.

All **306 mixed-row cases**, comprising **395 formula blocks**, were reviewed.
305 fields were repaired here, and one was already repaired. Evidence includes
179 archived HTML fragments, 117 retained lesson captures, and 5 historical
question imports. Five records have no external source ID; their repairs only
move existing relations and terminal punctuation, with exact expression-token
and order preservation checks. `mixed-case-review.json` records each resolution.

Source-specific repairs recover proof-template blanks, derivation labels,
factor-pair crosses/checkmarks, and long-division stages. Approximation signs
remain approximations; intentionally incorrect derivations remain incorrect.
Related broken currency markers and a malformed conditional-count expression
were also repaired. Nine valid legacy-only `eqalign` fields were canonicalized.

Validation:

- All repaired content was rendered through the unchanged learner UI:
  **12,471 math expressions**, with no MathJax errors or undefined commands.
- Source-specific layouts were checked in full-page screenshots under `visual/`
  and `visual-final/`.
- The formatter and capture regression suites passed **39 tests**.
- Native database preview passed entity specs and exact before/after comparisons.
- The committed receipt contains exactly the reviewed content changes plus the
  transaction instant. Exact historical readback verifies every repaired field
  and preservation of all other pulled question, answer, and tutorial data.
  Answer choices, correct-answer links, difficulty, and learner records are unchanged.

`transaction.edn`, `commit-intent.json`, and `receipt.edn` retain the exact durable
request and result. Rejected previews/submissions are retained separately. One
intervening tutorial alignment edit was preserved in the final CAS baseline.

The shared capture/generator formatter now handles explicit mixed-row chains,
terminal annotations and punctuation, and preloaded extension declarations.
Validation rejects unresolved empty right-hand sides and runtime extension
loading. Ambiguous missing content is not inferred by the shared normalizer.
