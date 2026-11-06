# Transactions

## Assemble intent

A transaction is one information set, not a script. Expansion and functions read the same db-before; the complete proposed db-after must satisfy constraints. Maps assert supplied facts, and omission leaves unrelated facts unchanged. Install schema before using new attribute names. Every durable or speculative transaction supplies one source.

New/upserted people and their relationship can be described together after the people schema exists:

```edn
[{:db/id "alice"
  :person/email "alice@example.com"
  :person/name "Alice"
  :person/tags [:active]
  :person/friends ["bob"]}
 {:db/id "bob"
  :person/email "bob@example.com"
  :person/name "Bob"}]
```

Tempids must be established in entity position in that transaction. A tempid used only as a ref value or source fails. Tempids are local; later transactions use IDs, idents, or lookup refs. Unique identity can upsert; unique value cannot.

| Form | Meaning |
| --- | --- |
| `[:db/add entity attribute value]` | Assert a fact; cardinality-one replacement generates an old-value retraction |
| `[:db/retract entity attribute value]` | Withdraw that stored value across all contributors |
| `[:db/retract entity attribute]` | Retract all matching db-before values of E/A |
| `[:db/cas entity attribute old new]` | Check a cardinality-one value against db-before, then propose a replacement; old nil means absence |
| `[:db/retractEntity entity]` | Retract its facts, incoming reference facts, and component descendants; retained history remains |
| `[:db/ensure entity spec]` | Request the named spec's checks of proposed db-after |

Two different assertions for one cardinality-one E/A conflict, regardless of form order. A cardinality-many map adds members; replace a set with explicit removals/additions of the membership difference. Retract-all expands from db-before, not an intermediate state.

```edn
[{:db/id [:person/email "alice@example.com"] :person/name "Alicia"}
 [:db/retract [:person/email "alice@example.com"] :person/tags :active]
 [:db/add [:person/email "alice@example.com"] :person/tags :alumni]]
```

The omitted email and friends remain. To assign nil/absence, retract; scalar nil is not an attribute value.

Nested maps describe other entities and connecting refs. An anonymous forward nested map needs a component ref or a unique attribute; an explicit `:db/id` also suffices. Anonymous reverse nested maps need a unique attribute even on a reversed component. For a many-ref lookup, supply an outer collection: `:person/friends [[:person/email "bob@example.com"]]`. For a one-ref, use the lookup directly.

## Sources and transaction metadata

Use the application's actual contributor. If none exists, bootstrap one using built-ins and supply `EntityRef::Temp("contributor")` / CLI `--source '"contributor"'` for this request:

```edn
[{:db/id "contributor"
  :db/ident :application.source/contributor
  :db/doc "Application contributor"}]
```

Later transactions use its ident or resolved ID. An exact retry of the bootstrap retains its original tempid source. `:db.source/system` is available for isolated fixtures and explicit system contributions; do not automatically attribute user work to it.

The reserved tempid `"edb.tx"` lets a map attach installed metadata such as an import URI or reason to the transaction entity. EDB automatically asserts one `:db/txInstant` with the transaction source even for empty data. An explicit time override must agree with timestamp data, be no older than the preceding instant, and for durable submission no newer than the writer clock. Preserve older source-event dates in a domain attribute when they cannot be used as Tx time.

## Preview, concurrency, and validation

`db.with_edn(text, instant_millis, source)` (or `with`/`with_forms`) returns a speculative report. Query/Pull `preview.db_after`. Preview reserves no durable IDs or request identity. Submit the original logical forms, not preview IDs or a datom diff. Filtered/temporal speculation assesses the full basis, then preserves the read view; it does not branch the past. History cannot transact.

For a read-dependent write, choose the relevant mechanism:

- CAS for a known cardinality-one precondition. Retry computation only after confirmed `transaction/cas-failed`, using a newly synchronized value and a newly chosen request.
- `TransactionRequest::comparing_basis(t)` if the entire plan requires an unchanged basis.
- A pure transaction function for logic that must use the writer's authoritative db-before. Functions return forms, and no function sees another's proposed changes.
- An explicitly ensured entity spec for invariants on complete proposed db-after. Attribute predicates validate assertions. Custom callbacks/programs must be available to every writer or preview process that needs them.

Do external effects in a separate workflow after confirmed commit. For durable reactions, see the upstream ChangeConsumer API: effect before acknowledgment, with idempotent external handling; exactly-once effects are not guaranteed.

## Durable submission and outcome recovery

Construct `TransactionRequest::from_edn(key, text, source)` or typed `new`/`from_forms`. Keep the complete request, including source, generated UUIDs, explicit time, basis guard, and representation, until the outcome is known. For restart recovery, persist it before submission in the application's outbox.

| Outcome | Next action |
| --- | --- |
| Confirmed success | Inspect exact `report.db_after`, `basis_t`, datoms, and tempid map; stop resubmitting as new intent |
| Confirmed precondition/schema rejection | Fix/recompute intent; unchanged invalid input will still fail |
| Timeout, lost reply, `UnknownOutcome` | Reconcile by resubmitting the same complete request under the same key; never recompute against newer state first |
| Key reused with different intent | Preserve/recover the original request; this conflict is not a fresh transaction |
| Confirmed commit with local report-opening/formatting error | The transaction committed; recover its report/read basis without applying a new transaction |

Equivalent effects do not establish identical request digests. Switching EDN maps to primitive forms or typed APIs, changing ordered nested collections/numeric representations, regenerating UUIDs, or changing source can change request identity. Retained receipt resolution precedes fresh schema/function assessment. Excision can replace an old receipt with an occupied-key tombstone; do not bypass that result with a new key.

Use a bounded retry policy appropriate to the task. If the exact request cannot be recovered or the outcome remains unknown, report that state and stop new dependent writes. Do not interpret cancellation or output failure as rollback. Error handling should inspect `SemanticError.category`, `code`, and `details`, not parse display text.
