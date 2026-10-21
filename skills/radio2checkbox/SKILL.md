---
name: radio2checkbox
description: Find and resolve Math Academy radio questions that represent selection of a finite subset, then prepare, preview, and verify checkbox migrations in this repo's EDB. Use for continuing the candidate audit, resolving ambiguous keys or response structures, and migrating equivalent learner responses.
---

# Radio to checkbox

Convert a question's response representation while preserving what it asks and what each learner answered. A valid outcome can also be **retain radio**, **repair a missing key**, or **needs more evidence**. Do not force every discovery candidate into a checkbox transaction.

Use the repo's [EDB skill](../edb/SKILL.md) for database access, schema, provenance, transaction, and recovery semantics. This skill supplies the application-specific decisions and migration workflow. Read EDB's transaction reference before preparing writes; read its query reference when constructing an audit.

## Start or resume

Read [repo context and checkpoints](references/repo-context.md) first when continuing prior work. Locate the latest receipts and case ledger, establish the requested scope, and distinguish confirmed conversions from unresolved candidates. Historical basis numbers and candidate counts are evidence, not current database state. Creating or invoking this skill does not authorize database mutations; apply the user's existing authorization to the requested stage without asking for it again.

Capture one immutable database value for related reads. Record database lineage, basis, source, query inputs, full question/field/choice data, correct keys, difficulty, worked solution, KP/topic membership, canonical-example membership, and saved learner uses. Use explicit `:limit nil` for many-valued Pull relationships. Recheck current state before preparing a transaction.

## Resolve the question

Read [resolving cases](references/resolving-cases.md) for criteria, missing keys, images, duplicated fields, and mathematical ambiguities. Work through the evidence and record a per-question conclusion; the ledger must support resuming without reconstructing the reasoning from chat.

Essential decisions:

- A finite list of independently testable statements, matrices, points, roots, or diagrams can be a checkbox task. Combination radio options are a strong signal. A single correct selection does not by itself require radio.
- Existing database keys take priority. Study-vault keys are LLM-generated evidence for missing keys and require independent verification. A suspected incorrect database key is a separate content issue to investigate, not permission to silently replace it with the study key.
- For captured image answer options, the user's convention is that the **first answer image filename in the original capture identifies the correct image**. Display order, entity IDs, and unordered Pull results do not establish that order.
- Preserve the mathematical question, solution, difficulty, and memberships. Add “Select all that apply.” once when needed. Normalize labels/bullets only where their meaning is established. “None” normally becomes an empty selected subset, not an additional checkbox.
- Put each **complete selectable object** in its checkbox's `:answer-field/key`: the full statement, equation, matrix, point, root, list item, or independently displayable image. Remove that selectable list from the prompt while preserving shared setup. A matrix option must contain the matrix itself, possibly with its mathematical name (`$A=...$`); `A`, `I`, or “Matrix A” alone is insufficient. Preserve named objects needed by the explanation, but replace references to removed Roman choices with the actual content. Keep old choice labels in migration evidence, separate from displayed field keys. Shared-image exceptions are described in [resolving cases](references/resolving-cases.md).
- Map every old option, including wrong answers, to its actual selected subset. A migrated learner response must express what the learner chose, not the correct key.

Separate resolved conversions from unresolved cases so ambiguity in one question does not stall independent work. If the user asks to resolve all ambiguities, keep investigating available capture files, solutions, mathematics, and images; ask only for missing evidence or a decision that cannot be established. Report any remaining uncertainty honestly.

## Prepare, preview, and commit

Read [transactions and verification](references/transactions-and-verification.md) for the schema, ownership, identity, learner mapping, guards, batching, native preview, and retry procedure.

The exact enum is **`:answer-field/type :answer-field.type/checkbox`**. Create one field per selectable object with its own text answers `"false"` and `"true"`, and a correct reference to the appropriate owned answer. A type flip on the old combination bank is insufficient. Detach old fields from the question while retaining old field/answer entities and history.

When repairing labels on existing checkbox fields, CAS-update their keys and the affected prompt/solution text. Preserve field and answer identities, Boolean banks, correct references, and saved responses; a label repair does not require rebuilding the fields.

Run the read-only [presentation lint](scripts/lint_presentation.py) on the proposed questions and reviewed object mappings, then on speculative and committed readbacks. Its input and the required rendered review are described in [transactions and verification](references/transactions-and-verification.md). Passing Boolean-bank or grading checks does not establish that learners see usable options.

Prepare original logical forms with an explicit agent contributor, stable identities, appropriate ensures, prompt CAS, and a basis guard for the full read-dependent plan. Persist exact requests before submission. Preview with the installed native validators and check the proposed `db_after`, datom scope, provenance, and native grading. A speculative preview is not a commit or a lock on the live database.

If the user requested preparation only, finish with reviewable transactions and a breakdown of resolutions. If committing is authorized, submit the exact previewed requests, retain receipts, and verify at the confirmed basis. Resolve unknown outcomes with the same complete request and key; do not rebuild uncertain submissions. On a confirmed stale-basis rejection, refresh only uncommitted work and preview again.

## Finish with a durable handoff

Update the ledger and status after each meaningful resolution, preparation, or confirmed batch. Include question/KP counts, retained radios and reasons, key repairs, learner mappings, exact source, preview/commit status and bases, validation results, and paths to evidence and receipts. Keep completed IDs separate from the next queue. Flag affected generator source snapshots when relevant; database migration alone does not update generators.
