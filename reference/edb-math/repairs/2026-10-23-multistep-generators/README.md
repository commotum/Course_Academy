# Standalone source eligibility repair

Committed to `math` at **T6208**, attributed to `:agent/codex`.
User authorization: “yeah, make the required fixes everywhere.”

The source capture admitted imported multistep parts without checking structural
containment. Generators then restored missing prior inputs, derivatives, or
results and treated the repaired fragments as standalone examples. Generated
copies had new identities and no multistep placement, so the learner's existing
structural exclusion did not recognize them. Correct mathematics and source
replay had been accepted without first establishing standalone eligibility.

## Scope and findings

- Inventoried all **650 registered KPs**, their declared Python/JSON package
  closures, and **5,073 question entities without imported source IDs** at T6170.
  The native identity export covers all **83,402 questions**, avoiding truncated
  broad query results.
- Identified **853 excluded imported sources**: **819 contained multistep parts**
  and **34 additional retired questions**. Structural traversal includes generic
  steps, legacy placements where the schema provides them, and assigned-problem
  wrappers.
- Guarded **65 registered generators whose KPs own excluded sources**: **46 legacy
  entrypoints** and **19 immutable package successors**. All 43 runtime-closure
  reference candidates are included in this set. Original package files and
  source captures remain historical evidence.
- Inspected retained generation metadata from **5,559 JSON files**. **433 of the
  435 generated questions owned by those 65 KPs** have retained metadata matched
  by exact UUID or the publisher's deterministic content identity. The other two
  older chain-rule questions were independently checked against eligible
  standalone examples; their original provenance is unavailable.
- Found **37 live question identities with excluded-source citations**. Ten
  matrix-dimension questions were independently authored and merely cited the
  entire captured source pool. They remain available, with explicit independent
  support recorded for future output. Of the other 27, one was already retired;
  **26 more were retired in this transaction**.

The retired set includes all five easy tangent-slope descendants of `q-167637`,
including **17592186510704**. Other affected families involved omitted derivative
inputs, radical antiderivatives, matrix/scalar data, matrix indexing, product-rule
slopes, integration, differential equations, and a surface-integral setup.
Exact identities, evidence paths, metadata, and decisions are retained in
[question-dispositions.json](question-dispositions.json).

## Repairs

Source capture now filters excluded question payloads from the KP, topic,
lesson, and prerequisite evidence before authoring. It retains a separate
identity ledger and computes observed difficulty coverage from eligible sources.
Inventory remains complete so reviewers can inspect existing descendants.
Structural graph reads are split into bounded queries; the initial recursive
join exceeded the live query budget and was replaced before deployment.

Publication checks each record's declared source references against current
retirement and containment facts, including manual publication. Offline delivery
checks require a current eligibility capture and apply its ledger. Author,
reviewer, classification, extraction, inventory, and preparation instructions now
require eligibility before fidelity and prohibit reconstructing excluded parts
as standalone practice. Review policy is **4**, retaining the previous
prerequisite/solution-transition requirements.

Resumed unfinished jobs archive and refresh old captures before authoring or
review. Pending durable submissions recover their exact saved bytes first.
Postcommit review cannot republish an acknowledged batch. Old approvals cannot
authorize fast refill under the new policy.

Existing runtimes prune excluded dispatch entries and validate returned records
at public generator APIs and the CLI. Normal sampling retries eligible existing
families only; explicit excluded requests and unsupported bands fail. The easy
tangent family and moderate constant-power family have no remaining standalone
support and are explicitly disabled. This repair does not claim replacement
coverage for those bands.

The transaction asserts `question/retired true` on the 26 demonstrated
descendants and replaces 19 generator registrations using CAS. It does not change
question text, answers, identities, KP membership, or learner/task facts.
The previous generator entities and immutable packages remain intact.

## Verification

- **185 generator tests passed**, covering publication, delivery, pipeline
  recovery, source filtering, runtime exclusion, and review contracts.
- All **65 repaired entrypoints** produced eligible output; **139 supported band
  checks** passed. The remaining tested bands reported unsupported scope or
  finite shortage rather than producing excluded questions.
- Live tangent source capture contains **moderate** standalone coverage and
  excludes `q-167637`; live manual preparation rejects a descendant citing it.
- Native preview passed all requested validation predicates. Both speculative
  and committed transaction reports were checked against the exact expected
  retirement and registration datoms and source attribution.
- Receipt readback at T6208 verified question ownership, saved-task references,
  new registrations, and the original immutable package hashes.

See [verification.json](verification.json), [postcheck.json](postcheck.json),
[source-verification.json](source-verification.json), and
[runtime-validation.json](runtime-validation.json). The original transaction,
request key, preview, and receipt are retained beside this report. `deploy.py
apply` recovers that same receipt; it does not invent a second submission.

The broad identity scan does not certify every question's pedagogy. This repair
addresses excluded-source lineage across all registered generators and the
existing descendants for which retained evidence or direct inspection supports
a decision. Historical source archives remain available as evidence; they are
not approved standalone template inputs.
