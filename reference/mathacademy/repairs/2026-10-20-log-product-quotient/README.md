# Restore the product/quotient logarithm KP scope

User-authorized repair for KP **17592186054624**, “Rewriting an Expression Using the Product and Quotient Rules of Logarithms,” in topic 30 / **17592186049195**, “Combining the Laws of Logarithms.” No web sources were used.

## Source contract and full audit

At captured math basis 5230, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, the practice pool contained four Math Academy source questions and five authored questions. A transaction-attribution query confirms those five are the full original generated question batch, including the reported **17592186608285**. All four source questions and the canonical example are preserved.

The saved condensing examples e-4085 and q-47200 use a positive constant log plus a positive variable log minus another variable log. The expansion examples q-47203, q-100242 and q-66781 use a product in the numerator and one denominator, with the variable in the numerator. The known base power can occur in numerator or denominator. These sources do not demonstrate a single positive log with two subtracted logs, a negative leading term, or moving the expansion variable into the denominator.

`audit-ledger.json` records all nine questions. Each authored question's exact printed prompt was reconstructed from the old generator before classifying it:

- **17592186608285**, **17592186608296**, **17592186608300**: withdraw and replace. All three have one positive and two negative logarithms.
- **17592186608299**, **17592186608308**: retain their problem, bank, field/answer identities, key and rating; clarify the worked solution.

The new generator validates the source-supported factor roles and positive-positive-negative presentation even for explicit parameters. It retains all six mixed sign vectors only as wrong-answer recipes; these are not admissible correct-question structures. The two positive terms may be interchanged. Both expanding and condensing templates show the product and quotient operations in separate, compact display chains. Known numerical logs are evaluated explicitly. Original source replays preserve saved prompts, banks and existing solutions.

## Withdrawal without corrupting history

The reported question has one completed correct learner presentation. Removing its KP membership would break the engine's historical lesson ownership checks. The new documented Boolean `question/retired` therefore withdraws a question from fresh adaptive lesson, review, assessment and inventory selection while retaining its content, banks, KP ownership and saved learner presentations. All three rejected questions receive this flag; three separately identified replacements enter the same KP pool. Their original entities are not deleted or overwritten.

Only `validate_practice_question` checks retirement. Historical validation, response grading and existing lesson replay remain available. A native engine test verifies fresh lesson/inventory/assessment exclusion, saved-answer grading, saved lesson continuation and normal eligibility for absent/false retirement flags. All **169** engine unit tests pass. The rebuilt local app filter is deployed and both running workers were checked against the exact built binary in `deployment-verification.json`.

## Validation and publication

- 1,000 seeded generator records, all six admissible sign/order structures covered, deterministic replay.
- All 72 sign/order inputs checked: six accepted and 66 rejected.
- Four original source replays checked for fidelity.
- 115 representative/replacement/source/retained questions checked by the current native grader, including distractor rejection.
- Independent symbolic checks parse the printed expressions: 111 authored questions, 540 displayed expression steps and 444 rejected distractors.
- All three replacements and both clarified solutions rendered at desktop and phone widths (10 pages). Final equation chains were shortened after visual phone review.
- A new immutable generator package is registered; previous package bytes and entity remain intact.
- Schema installation and the content repair use saved exact requests, explicit contributor `:agent/codex`, native previews and basis guards. No learner item, status, response, duration, performance or progress record is modified.
- Exact receipt datoms, proposed native db_after and committed readback verify the retirement flags, replacements, solution-only repairs and registration. The original snapshot is reproduced historically.
- `finish.py` checks actual committed inventory/assessment eligibility and grades the retained saved response with the current native engine, then executes a disposable copy of the published package without repository imports.

Final commit bases, replacement IDs and checks are in `verification.json`. `schema/` retains the attribute installation request/receipt. `content/` retains the final repair request/preview/receipt/readbacks. `superseded/pre-phone-layout/` is an unsubmitted preview superseded by the shorter equation layout; no durable request was sent for that preparation. Never rerun a successful request with a new key or rebuild an unknown-outcome request.
