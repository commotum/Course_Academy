# Completing the Square: committed presentation repair

**Committed and verified at math basis 3520**, following the user's instruction
“Go ahead and transact it.” The saved transaction was submitted once with its
original source, request key, hash, and basis guard, advancing basis 3519 to 3520.
The committed datoms and full readback match the validated preview.

Lesson activity: `17592186068977`. Topic: `17592186050372`.
Original question: `17592186511718`.

## Review

- [Transaction](transaction.edn): 117 compare-and-swap text updates, 74 entity
  validation requests, and one contributor identity map.
- [Readable before/after diff](changes.diff) and [structured changes](changes.json).
- [Proposed rendered content](representative-render.png), with the
  [original rendering](evidence/representative-render.png) for comparison.
- [Saved request parameters](request.json), [plan](plan.json), and
  [validation results](validation.json).
- [Durable receipt](receipt.edn) and [committed verification](commit-verification.json).
- [Original complete audit](evidence/original-audit.md).

The updates affect 46 question prompts, 69 existing worked solutions, and both
tutorials, across 74 content entities. They replace 30 misplaced underbraces,
reformat 67 equation chains, separate four prompts from their answer equations,
correct the sum/difference wording in question `17592186532655`, and normalize
inline sentence punctuation and captured closing-parenthesis grouping.

Answer values, answer identities, correct-answer links, field placeholders,
difficulty, practice memberships, canonical-example links, and the six-step
lesson route are preserved. The eight questions missing solutions and answer
keys remain separate work. This transaction does not edit question generators.

The math database lacks `:agent/codex`, the general contributor identity already
used by `capture/scripts/prepare_encompassing_weights.py`. The transaction
therefore bootstraps it with a short documentation string. Its source argument
is the EDN string `"codex-format-repair"`, referring to that map's tempid.
Preview-assigned entity IDs must not be substituted into the transaction.

## Validation

The [native preview](preview.edn) reports `:edb/committed false` and
`:edb/speculative true`. [Exact datom verification](preview-verification.json)
confirms that its only changes are the planned text replacements, the
contributor's ident/doc, and speculative transaction time. Full question,
answer-bank, captured response-reference, tutorial, activity, and knowledge-point
projections match their expected before/after values.

All 79 instructional items were rendered using the current app modules at
893 px and 375 px, in editable and answered states: 316 item renders. The
[browser check](browser-summary.json) found no browser exceptions, MathJax
errors, or horizontal overflow. Representative output was visually inspected.
All 122 adjacent equalities in the 67 reformatted equation chains were checked
with exact symbolic algebra. This does not constitute an independent audit of
every answer key.

`prepare.py` recreates the transaction from the pinned evidence using the
repository's `.venv/bin/python`. `verify_preview.py` checks the saved native
preview. Neither script can submit a transaction. `verify_commit.py` verifies
the durable receipt and exact committed readback. `browser.cjs` renders the
saved proposed cases against the local app without starting learner tasks or
submitting responses.

## Submission record

The user's subsequent approval is retained in `commit-intent.json`, together
with the exact transaction text and request parameters. `request.json` records
the confirmed commit, and `commit-verification.json` records successful readback.
The original plan and speculative preview remain as preparation evidence.
The saved request's stable key, source, basis, and transaction bytes must be
retained for any exact receipt recovery; no new submission is needed.

Transaction SHA-256:
`79f79eb5c330e19fcc214adb20d4e95e905ce3726b652bd04f212ca5277583b9`.
