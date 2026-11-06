---
name: edb
description: Query, navigate, and transact data in the Rust EDB temporal fact database using Datalog, Pull, EDN, and native APIs. Use for EDB schema and identity design, assertions and retractions, historical reads, and translating SQL or CRUD application patterns to EDB. This is the edb-core project, not EnterpriseDB PostgreSQL products.
---

# EDB

Work with EDB's immutable database values and declarative facts. These references cover everyday application work; read only the ones needed for the task.

## Choose the reference

| Task | Read |
| --- | --- |
| Understand the model or translate SQL/CRUD assumptions | [Core concepts](references/core-concepts.md) |
| Discover attributes, define schema, choose identities or relationships | [Schema and identity](references/schema-and-identity.md) |
| Find entities, join, aggregate, select optional data or navigate references | [Query and Pull](references/query-and-pull.md) |
| Assert, retract, upsert, preview, enforce preconditions or recover a submission | [Transactions](references/transactions.md) |
| Read past state, audit changes, inspect provenance or synchronize readers | [Time and provenance](references/time-and-provenance.md) |
| Choose CLI/native entry points, connect or make an isolated fixture | [Interfaces](references/interfaces.md) |
| Need an advanced feature or exact version-specific signature | [Upstream sources](references/sources.md) |

Read core concepts once when EDB is unfamiliar. For a simple query, load the query reference and inspect the application's existing schema; do not load the whole reference set.

## Working conventions

1. Establish the intended database, its existing access configuration, and the application's schema and contributor conventions. Reuse the project's EDB integration. Do not invent domain attributes, arbitrary numeric IDs, a source, or a writer endpoint.
2. Capture one database value for related reads. Use the transaction report's `db_after` to inspect a write's exact result. Synchronize only when freshness or a known causal basis is required.
3. Build fixed EDN templates or native data structures and pass inputs separately. Prefer Datalog for selection and joins, Pull for output shapes, and the log for transaction-time event ranges.
4. For writes, assemble logical assertions/retractions with one explicit source and a stable request key. Keep the complete request until its outcome is known. Use CAS, a basis guard, or writer-side validation when correctness depends on a prior read.
5. Verify the intended result at the right basis. For authored logic, an in-memory fixture can check query shapes, identity resolution, and transaction semantics without touching live storage. Report a preview as speculative and a commit only when confirmed.

Apply the user's existing authorization to the actual task. This skill adds no permission to mutate a live database or administer storage.

## Essential guardrails

- Transaction forms describe one information set assessed against db-before. They are not sequential updates; two different cardinality-one assertions do not mean last-write-wins.
- Omitted map attributes remain unchanged; cardinality-many map values add members. Retraction is explicit. Retraction preserves retained history; it is not excision.
- Every transaction requires one source, including empty transactions and previews. It attributes all explicit and generated datoms. Sources contribute to one shared current record.
- A timeout or lost reply can mean an unknown commit outcome. Reconcile the exact original request under the same key; do not recompute or generate a new key merely to recover the reply.
- Schema intent is different from physical AVET readiness. Temporal views retain the captured schema and ident dictionary. A held value is not an indefinite storage-retention pin.

This condensation was checked against the local EDB docs on 2026-10-11. Use the installed build's documentation or source when a signature, command, compatibility issue, or omitted feature matters; do not substitute remembered Datomic/Clojure APIs. Source locations and deliberately deferred topics are in [sources](references/sources.md).
