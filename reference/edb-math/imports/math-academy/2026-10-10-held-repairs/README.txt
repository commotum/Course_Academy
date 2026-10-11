TWO PREPARED TRANSACTIONS — NOTHING COMMITTED

All 26 remaining held questions are prepared and validated against math basis 187.

1. 001-math-academy-original.edn
   Required transaction source: :org/Math-Academy
   23 new questions, 3 existing question updates. Original prompts, solutions,
   answer choices and MA-intended keys are preserved, including known errors.
   Normalization restores original Roman list labels and canonical image paths.

2. 002-astra-surgical-repairs.edn
   Required transaction source: :agent/gpt-6-astra-ultra
   All repairs authored and independently checked by GPT-6-astra / ultra.
   Changes: 25 prompts, 11 worked solutions, 2 choice values.
   Text repairs use compare-and-swap: EDB retracts the exact original value and
   asserts its replacement. Two superseded fields and their ten answer
   components are retracted from current state and replaced. Both historical
   MA assertions and agent-attributed retractions remain in history. No source
   entity, schema, question identity, or knowledge-point membership is changed.

These are sequential stages concerning the same 26 questions. Sources are
passed separately to EDB; they are not attributes embedded in the EDN file.
The held index still contains all 26 because no commit has occurred.

Both stages were applied only to an in-memory database branch (187 -> 188 ->
189). Full content and history readbacks passed, exact retractions and sources
were verified, and an independent live read remained at basis 187. The old
Math Academy question and answer graphs were recovered from the repaired
speculative database using as-of 188. No external incoming references exist
to the twelve retired component entities.

Review repair-diff.txt for the precise text/option changes. repair-plan.json
contains author reasoning and checks; review/ contains the independently
authored proposals, peer reviews and EDB conventions. validation/ contains
both speculative receipts, readbacks and history. manifest.json records exact
paths, hashes, counts and required sources. The SSD directory contains only
the two transaction EDNs; evidence and metadata remain here.

Do not submit without new authorization. Before any later commit, check the
current basis and revalidate the sequence if it has changed. Use stage 1
before stage 2. Remove questions from the held index only after verified commit.
