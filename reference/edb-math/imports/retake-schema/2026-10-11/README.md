# Retake relationship schema transaction

Status: **committed and verified at basis 1180**, after the user instructed “do it” following review of the prepared transaction. Prepared, previewed, and transacted using the EDB skill.

## Exact additions

The [transaction](transaction.edn) contains exactly two new optional attributes:

| Attribute | Type | Cardinality | Meaning |
| --- | --- | --- | --- |
| `:learner-task/retake-of` | Reference | One | Connect a retake task to its exact original assessment task. |
| `:learner-task/remediation-for` | Reference | Many | Connect a review or replacement relearning task to the assessment(s) that triggered required practice. |

Both are ordinary noncomponent relationships, with retained history. Neither requests uniqueness, a new index, or a predicate. The existing `:learner-task/validate` required attributes remain unchanged, so these optional links do not make old records invalid.

Each definition supplies its ident, reference type, cardinality, and documentation: **eight explicit assertions**. EDB additionally generates two attribute installation markers and one transaction timestamp, for **11 preview datoms**, all additions, with no retractions. Preview IDs are speculative and must not be submitted as durable identities.

The documentation explains required review provenance, optional retakes after successful remediation, and fresh questions from the original knowledge points. Those behaviors require application implementation; this schema-only transaction does not enforce them. The never-seen rule covers questions previously presented in lessons, reviews, assessments, or other activities, rather than only excluding the original quiz's questions.

There are no learner task records, historical links, weight updates, threshold settings, validation-spec changes, or scheduling changes in this transaction. Existing assessment weights remain initial 50/40/10 and remedial 45/40/15.

## Preserved request

- Database: `math`.
- Database lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
- Source: the existing assistant contributor `:agent/gpt-6.1-sol-high`, entity `17592186045436`.
- Read basis and intended optimistic basis guard: **1179**.
- Writer endpoint: the existing `/tmp/edb-math/writer.sock`.
- Stable request key: `assessment-retake-schema-2026-10-11-577f380c-5bff-4b7d-b159-3a5f0d43ee57`.
- Transaction SHA-256: `a2f861296727920e6ada37f98cd508711fa8de1a1ddbef16df8abfe4940804ef`.

[intent.json](intent.json) preserves these options. The established source is reused; no contributor entity is created. Preserve the original forms and request key on any later submission or unknown-outcome recovery. If the basis advances before the first submission, inspect the newer schema and re-preview before deciding how to update the guard.

## Verification and remaining work

Live reads at basis 1179 confirmed neither new ident already exists and the contributor and existing task validation spec are installed. The native CLI `with` accepted the transaction and returned `:edb/committed false` and `:edb/speculative true`. [verification.json](verification.json) confirms the exact explicit and automatic datom scope and source. A subsequent live status read remained at basis 1179.

Evidence: [schema-before.edn](schema-before.edn), [preview.edn](preview.edn), [status-before.txt](status-before.txt), and [status-after.txt](status-after.txt). [prepare.py](prepare.py) performs reads and a speculative preview only; [verify.py](verify.py) verifies the retained request/report without regenerating or submitting intent.

The original request committed from basis **1179 → 1180**. [receipt.edn](receipt.edn), [commit-verification.json](commit-verification.json), [schema-after.edn](schema-after.edn), and [provenance.edn](provenance.edn) confirm exactly 11 added datoms, no retractions, the expected source, and unchanged inspected existing schema and task validation spec. The installed attribute entities are `1165` (`retake-of`) and `1164` (`remediation-for`). [commit.py](commit.py) preserves the exact request and verifies its committed basis; it reuses a retained receipt on subsequent runs.

The same definitions were added to the workspace `schema/learner/2-1-learner-task.edn` and SSD `/media/jake/SSD/EDB/math/schema/learner/3-learner-task.edn`. [schema-mirror-verification.json](schema-mirror-verification.json) confirms that only the two definitions were inserted and all existing file contents were preserved. [mirror_schema.py](mirror_schema.py) retains the original schema file backups and verifies the additions against the transaction.

The running application's learner and home endpoints both returned HTTP 200 at database basis 1180 without a service restart; see [api-verification.json](api-verification.json).

`intent.json` retains its original preparation-time metadata for audit and exact-request recovery; this README and `commit-verification.json` record the subsequent commit. The preview remains speculative evidence, not the commit receipt. Engine/API/UI changes remain the separate implementation described in the [approved plan](../../../../analysis/assessment-selection-2026-10-11/retake-scheduling-plan.md).
